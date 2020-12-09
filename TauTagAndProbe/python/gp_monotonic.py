########################################################
#########  GP regression by applying  ##################
#########   Monotonicity constraints  ##################
########################################################

import numpy as np
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor,GaussianProcessClassifier
from sklearn.gaussian_process.kernels import Matern, ConstantKernel,RBF
import seaborn as sns
import scipy.stats as st
from scipy.special import erfinv,erf,logit,erfc
import math
import copy
#import theano.tensor as Te
#from theano.tensor.nlinalg import matrix_inverse
#import pymc3 as pm

class gp_monotonic:
    def __init__(self,gp,yerr,xvals,ydata):
        self.gp    = gp    # default gp object
        self.xvals = xvals # input labels
        self.ydata = ydata # data points

        self.sigma2_n = yerr
        
        x_temp = np.linspace(xvals[0],xvals[-1],len(xvals))
        y_pred = self.gp.predict(np.atleast_2d(x_temp).T,return_cov=False)

        print(ydata)
        ### Selecting Virtual Points ##################################
        
        deriv = np.gradient(y_pred,x_temp)
        xm = [x_temp[pt] for pt in range(len(deriv)) if deriv[pt]<0]
        ym = [y_pred[pt] for pt in range(len(deriv)) if deriv[pt]<0]
        ym_ = [1. if x_temp[pt]>90 else 0 for pt in range(len(x_temp)) ]
        
        self.xm_ar = np.array(xm,dtype='float32')#np.random.choice(x_temp,int(len(x_temp)/8),replace=False)
        self.ym_ar = np.array(ym,dtype='float32')
        
        
        N,M = len(self.xvals),len(self.xm_ar)
        print('No. of virtual points : ',M)
        ################################################################
        kernel = Matern(length_scale=50, length_scale_bounds=(10,100), nu=2.0)
        gp_new = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=0)
        
        gp_new.fit(np.atleast_2d(self.xm_ar).T,self.ym_ar)
        self.kernel_opt = gp_new.kernel_
        Kff  = self.kernel_opt(np.atleast_2d(xvals).T,np.atleast_2d(xvals).T)
        Kff1 = self.kernel_opt(np.atleast_2d(xvals).T,np.atleast_2d(self.xm_ar).T)
        Kf1f = self.kernel_opt(np.atleast_2d(self.xm_ar).T,np.atleast_2d(xvals).T)
        Kf1f1= self.kernel_opt(np.atleast_2d(self.xm_ar).T,np.atleast_2d(self.xm_ar).T)

        
        A = np.concatenate((Kff, Kf1f), axis=0)#+0.001*np.eye(N) 
        B = np.concatenate((Kff1, Kf1f1), axis=0)
            
        self.K_joint = np.concatenate((A,B),axis=1)
        
        #Initialise
        mu_tilde = np.zeros(M)
        v_tilde  = np.repeat(np.inf,M)
        Z_tilde  = np.ones(M)

        old_vi = copy.copy(v_tilde)
        old_mi = copy.copy(mu_tilde)
        old_si = copy.copy(Z_tilde)
        
        for iteration in range(50):
            print('No. of iterations: ',iteration)
            mi,vi = self.post_vars(mu_tilde,v_tilde,M)
            for i in range(M):
                cavity_mi,cavity_vi = self.compute_cavity(mi[i],vi[i],mu_tilde[i],v_tilde[i])
                mu_hat,v_hat,Z_hat = self.compute_moments(self.ym_ar[i],cavity_mi,cavity_vi)
                mu_tilde[i],v_tilde[i],Z_tilde[i] = self.update_approximate_factor(cavity_mi,cavity_vi,mu_hat,v_hat,Z_hat)

            
            self.mu_tilda_joint, self.S_tilda_joint = self.joint_vector(self.ydata,mu_tilde,self.sigma2_n,v_tilde)
            self.x_joint = np.concatenate((self.xvals, self.xm_ar), axis=0)
        
            # Check for convergence, after iteration
            if self.check_convergence(mu_tilde, v_tilde, Z_tilde, old_mi, old_vi, old_si):
                print ("Convergence reached.")
                break
                
            old_vi = copy.copy(v_tilde)
            old_mi = copy.copy(mu_tilde)
            old_si = copy.copy(Z_tilde)
            
        
        print('Sucessfully created the montonic object')
                

    def post_vars(self,mu_t,v_t,ndim):
        mu_joint,sigma_joint = self.joint_vector(self.ydata,mu_t,self.sigma2_n,v_t)
        sigma = np.linalg.inv(np.linalg.inv(self.K_joint) + np.linalg.inv(sigma_joint))
        mu = np.dot(np.dot(sigma,np.linalg.inv(sigma_joint)),mu_joint)
        sigma_diag = np.diag(sigma)
        return mu[-ndim:],sigma_diag[-ndim:]

    def predict(self,x_star,return_cov=False):
        K_starf   = self.kernel_opt(np.atleast_2d(x_star).T,np.atleast_2d(self.x_joint).T)
        K_star2   = self.kernel_opt(np.atleast_2d(x_star).T,np.atleast_2d(x_star).T)

        print('K_starf shape : ',K_starf.shape)
        print('K_star2 shape : ',K_star2.shape)
        
        f_pred = np.dot(np.dot(K_starf,np.linalg.inv(self.K_joint+self.S_tilda_joint)),self.mu_tilda_joint)
        f_cov  = K_star2 - np.dot(np.dot(K_starf,np.linalg.inv(self.K_joint+self.S_tilda_joint)),K_starf.T)

        if(return_cov==True):
            return f_pred,f_cov
        return f_pred
    
    def compute_moments(self,y_i,cavity_m,cavity_v):
        nu = 10**(-6)
        a = math.sqrt(1+abs(cavity_v)/nu**2)
        zi = y_i*cavity_m/(nu*a)
        normc_zi = 0.5*erfc(-zi/math.sqrt(2))
        normp_zi = math.exp(-0.5*zi**2)
        mu_hat     = cavity_m + (y_i*cavity_v * normp_zi)/(normc_zi*nu*a)
        sigma_hat  = cavity_v - (cavity_v**2 * normp_zi)/((nu**2 + cavity_v)*normc_zi)*(zi+normp_zi/normc_zi)
        return mu_hat,sigma_hat,normc_zi

    
    def division_zero(self,v1, v2):
        # check if the variances divide by zero
        inv_v1 = 1. / v1
        inv_v2 = 1. / v2
        if inv_v1 == inv_v2:
            return False
        else:
            return True
    def compute_cavity(self,mi, vi, m_t, v_t):
        inv_vi,inv_vt = 1.0/vi,1.0/v_t
        cavity_v = 1.0/(inv_vi-inv_vt)
        cavity_m = cavity_v*(inv_vi*mi-inv_vt*m_t)
        return cavity_m,cavity_v
    
    def update_approximate_factor(self,cavity_m,cavity_v,mu_hat,v_hat,Z_hat):
        inv_v,inv_vhat = 1.0/cavity_v,1.0/v_hat
        v_new,mu_new = cavity_v,cavity_m
        if(self.division_zero(cavity_v,v_hat)):
            v_new  = 1.0/(inv_vhat-inv_v)
        else:
            v_new = np.infty
        if v_new == np.infty and (inv_v == 0 or mu_new == cavity_m):
            mu_new = cavity_m
        else:
            mu_new = v_new*(inv_vhat*mu_hat-inv_v*cavity_m)
        Z_new = Z_hat*np.sqrt(2*np.pi)*np.sqrt(cavity_v+v_hat)*np.exp(0.5*((cavity_m-mu_hat)**2)/(cavity_v+v_hat))
       
        return mu_new,v_new,Z_new
        
    
    def param_dist(self,new, old):
        """Measures distance between two vectors of parameters."""
        new_finfo = np.finfo(new.dtype)
        new_clipped = np.clip(new, new_finfo.min, new_finfo.max)
        old_finfo = np.finfo(old.dtype)
        old_clipped = np.clip(old, old_finfo.min, old_finfo.max)
        return max(np.sum(np.atleast_2d((new_clipped - old_clipped) ** 2), axis=1))

    def check_convergence(self,mi, vi, si, old_mi, old_vi, old_si):
        tol = 10**4
        dist = max(self.param_dist(new, old) for (new, old) in ((vi, old_vi), (mi, old_mi), (si, old_si)))
        #print("m_new = ", self.m_new, " v_new = ", self.v_new)
        print ("Maximum distance from last parameter values: ", dist)
    
        if dist <= tol:
            return True
        else:
            return False
    def joint_vector(self,y,mu_t,s2,s2_t):
        n,m = len(y),len(mu_t)
        mu_joint = np.concatenate((y, mu_t), axis=0)
        s_diag   = np.concatenate((s2,s2_t),axis=0)
        s_joint =  np.diag(s_diag)
        print(mu_joint.shape,'  ',s_joint.shape)
        return mu_joint,s_joint
    
    
