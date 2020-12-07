########################################################
#########  GP regression by applying  ##################
#########   Monotonicity constraints  ##################
########################################################

import numpy as np
import matplotlib.pyplot as plt
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, ConstantKernel,RBF
import seaborn as sns
import scipy.stats as st
from scipy.special import erfinv,erf,logit,erfc
import math
import copy
import theano.tensor as Te
<<<<<<< HEAD
from theano.tensor.nlinalg import matrix_inverse
import pymc3 as pm

class gp_monotonic:
    def __init__(self,model,gp,yerr,mp,xvals,ydata):
        self.model = model # default gp model
        self.gp    = gp    # gp object
        self.mp    = mp    # maximum apriori
        self.xvals = xvals # input labels
        self.ydata = ydata # data points

        self.sigma2_n = yerr
        x_temp = xvals#np.linspace(xvals[0],xvals[-1],len(xvals)+40)
        with self.model:
            y_pred,y_cov = self.gp.predict(np.atleast_2d(x_temp).T,self.mp)

        deriv = np.gradient(y_pred,x_temp)
        xm = [x_temp[pt] for pt in range(len(deriv)) if deriv[pt]<0]
        ym = [y_pred[pt] for pt in range(len(deriv)) if deriv[pt]<0]

=======

class gp_monotonic:
    def __init__(self,kernel,gp,xvals,ydata):
        self.kernel = kernel # default kernel
        self.gp    = gp    # gp object
        self.xvals = xvals # input labels
        self.ydata = ydata # data points
        y_pred = self.gp.predict(np.atleast_2d(xvals).T)
        deriv = np.gradient(y_pred,xvals)
        xm = [xvals[pt] for pt in range(len(deriv)) if deriv[pt]<0]
        ym = [y_pred[pt] for pt in range(len(deriv)) if deriv[pt]<0]
>>>>>>> 42ad9e57f2c86db396aaeed1875967fc81eb2d8e
        self.xm_ar = np.array(xm,dtype='float32')
        self.ym_ar = np.array(ym,dtype='float32')
        N,M = len(self.xvals),len(self.xm_ar)
        print('No. of virtual points : ',M)
<<<<<<< HEAD

        self.kernel = ConstantKernel() * Matern(length_scale=self.mp['l_'], length_scale_bounds=(10,100), nu=1.5)
        Kff  = self.kernel.__call__(np.atleast_2d(xvals).T,np.atleast_2d(xvals).T)
        Kff1 = self.kernel.__call__(np.atleast_2d(xvals).T,np.atleast_2d(self.xm_ar).T)
        Kf1f = self.kernel.__call__(np.atleast_2d(self.xm_ar).T,np.atleast_2d(xvals).T)
        Kf1f1= self.kernel.__call__(np.atleast_2d(self.xm_ar).T,np.atleast_2d(self.xm_ar).T)

        
        A = np.concatenate((Kff+0.001*np.eye(N) , Kf1f), axis=0)
        B = np.concatenate((Kff1, Kf1f1), axis=0)
            
        self.K_joint = np.concatenate((A,B),axis=1)
        
        #Initialise
        mu_tilde = np.zeros(M)
        v_tilde  = np.repeat(np.inf,M)
        Z_tilde  = np.ones(M)

        old_vi = copy.copy(v_tilde)
        old_mi = copy.copy(mu_tilde)
        old_si = copy.copy(Z_tilde)
        
        for iteration in range(20):
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
        K_starf   = self.kernel.__call__(np.atleast_2d(x_star).T,np.atleast_2d(self.x_joint).T)
        K_star2   = self.kernel.__call__(np.atleast_2d(x_star).T,np.atleast_2d(x_star).T)
=======
        #Initiation of cavity variables
        self.vi = np.repeat(np.infty, M)
        self.mi = np.zeros((M, 1))
        self.si = np.ones(M)
        # Initialise posterior with prior
        sigma2_n = 0.25#np.sqrt(self.mp['s_n'])# The noise value should be named as s_n in the model 
        m_new = np.zeros(M)
        v_new = sigma2_n
        print('v_new ',v_new)
        #EP approximation of posterior
        for iteration in range(10):
            print ("Iteration ", iteration)
            for i in range(M):
                print('factor ',i)
                ######################################################################################

                # Find the cavity distribution parameters.
                if self.division_zero(self.vi[i], v_new):
                    cavity_m, cavity_v = self.cavity_vars(self.mi[i], self.vi[i], m_new, v_new)
                else:
                    print ("Skipping ", i, " for division of zero when removing factor for cavity funtion iiii")
                    continue
                #######################################################################################
                #update posterior
                m_new,v_new,Zi = self.compute_moments(self.ym_ar[i], cavity_m,cavity_v)
                
                # Update/remove approximate factor fi from q_new  
                self.mi[i],self.vi[i],self.si[i] = self.update_approximate_factor(cavity_m, m_new, cavity_v, v_new, Zi)


            # old_vi = copy.copy(self.vi)
            # old_mi = copy.copy(self.mi)
            # old_si = copy.copy(self.si)
    
            # #Check for convergence, after iteration
            # if self.check_convergence(self.mi, self.vi, self.si, old_mi, old_vi, old_si):
            #     print ("Convergence reached.")
            #     break
            
        #tilda parameters
        mu_t = self.mi.reshape(1,-1)  
        v_t  = self.vi

        self.mu_joint,self.sigma_joint = self.joint_vector(self.ydata,mu_t[0],sigma2_n,v_t)
        self.x_joint = np.concatenate((self.xvals, self.xm_ar), axis=0)
        self.kernel_new = ConstantKernel() *Matern(length_scale=1.75, length_scale_bounds=(1,2), nu=0.75)
        
        Kff   = self.kernel_new.__call__(np.atleast_2d(self.xvals).T,np.atleast_2d(self.xvals).T)
        Kff1  = self.kernel_new.__call__(np.atleast_2d(self.xvals).T,np.atleast_2d(self.xm_ar).T)
        Kf1f  = self.kernel_new.__call__(np.atleast_2d(self.xm_ar).T,np.atleast_2d(self.xvals).T)
        Kf1f1 = self.kernel_new.__call__(np.atleast_2d(self.xm_ar).T,np.atleast_2d(self.xm_ar).T)

        print('K_ff shape : ',Kff.shape)
        print('K_ff1 shape : ',Kff1.shape)
        print('K_f1f1 shape : ',Kf1f1.shape)
        
        A = np.concatenate((Kff + (sigma2_n)*np.eye(N), Kf1f), axis=0)
        B = np.concatenate((Kff1, Kf1f1), axis=0)
        self.K_joint = np.concatenate((A,B),axis=1)

        print('Sucessfully created the montonic object')

    def predict(self,x_star,return_cov=False):
        K_starf   = self.kernel_new.__call__(np.atleast_2d(x_star).T,np.atleast_2d(self.x_joint).T)
        K_star2   = self.kernel_new.__call__(np.atleast_2d(x_star).T,np.atleast_2d(x_star).T)
>>>>>>> 42ad9e57f2c86db396aaeed1875967fc81eb2d8e

        print('K_starf shape : ',K_starf.shape)
        print('K_star2 shape : ',K_star2.shape)
        
<<<<<<< HEAD
        f_pred = np.dot(np.dot(K_starf,np.linalg.inv(self.K_joint+self.S_tilda_joint)),self.mu_tilda_joint)
        f_cov  = K_star2 - np.dot(np.dot(K_starf,np.linalg.inv(self.K_joint+self.S_tilda_joint)),K_starf.T)
=======
        f_pred = np.dot(np.dot(K_starf,np.linalg.inv(self.K_joint+self.sigma_joint)),self.mu_joint)
        f_cov  = K_star2 - np.dot(np.dot(K_starf,np.linalg.inv(self.K_joint+self.sigma_joint)),K_starf.T)
>>>>>>> 42ad9e57f2c86db396aaeed1875967fc81eb2d8e

        if(return_cov==True):
            return f_pred,f_cov
        return f_pred
        
        
    def compute_moments(self,y_i,cavity_m,cavity_v):
        nu = 10**(-6)
        a = math.sqrt(1+cavity_v/nu**2)
        zi = y_i*cavity_m/(nu*a)
        normc_zi = 0.5*erfc(-zi/math.sqrt(2))
        normp_zi = np.exp(-0.5*zi**2 -0.918938533204673)
        mu_hat     = cavity_m + (y_i*cavity_v * normp_zi)/(normc_zi*nu*a)
        sigma_hat  = cavity_v - (cavity_v**2 * normp_zi)/((nu**2 + cavity_v)*normc_zi)*(zi+normp_zi/normc_zi)
<<<<<<< HEAD
        return mu_hat,sigma_hat,normc_zi
=======
        return mu_hat[-1],sigma_hat[-1],normc_zi
>>>>>>> 42ad9e57f2c86db396aaeed1875967fc81eb2d8e

    
    def division_zero(self,v1, v2):
        # check if the variances divide by zero
        inv_v1 = 1. / v1
        inv_v2 = 1. / v2
        if inv_v1 == inv_v2:
            return False
        else:
            return True
<<<<<<< HEAD
    def compute_cavity(self,mi, vi, m_t, v_t):
        inv_vi,inv_vt = 1.0/vi,1.0/v_t
        cavity_v = 1.0/(inv_vi-inv_vt)
        cavity_m = cavity_v*(inv_vi*mi-inv_vt*m_t)
        return cavity_m,cavity_v
    
    def update_approximate_factor(self,cavity_m,cavity_v,mu_hat,v_hat,Z_hat):
        inv_v,inv_vhat = 1.0/cavity_v,1.0/v_hat
        v_new  = 1.0/(inv_vhat-inv_v)
        mu_new = v_new*(inv_vhat*mu_hat-inv_v*cavity_m)
        Z_new = Z_hat*np.sqrt(2*np.pi)*np.sqrt(cavity_v+v_hat)*np.exp(0.5*((cavity_m-mu_hat)**2)/(cavity_v+v_hat))
        return mu_new,v_new,Z_new
    
=======
    def cavity_vars(self,mi, vi, m_new, v_new):
        inv_vi = 1. / vi
        inv_v_new = 1. / v_new
        cavity_v = 1. / (inv_v_new - inv_vi)
        cavity_m = cavity_v * (m_new * inv_v_new - mi * inv_vi)
        return cavity_m, cavity_v

    def update_approximate_factor(self,cavity_m, m_new, cavity_v, v_new, Zi):
        inv_cavity_v = 1. / cavity_v
        inv_new_v = 1. / v_new
        # problem 1
        # division by zero
        if self.division_zero(cavity_v, v_new):
            vi = 1. / (inv_new_v - inv_cavity_v)
        else:
            vi = np.infty
            print ("same variance from removing new approximate factor iiii")

            # problem 2
            # 0 * infinity
        if vi == np.infty and (inv_cavity_v == 0 or m_new == cavity_m):
            mi = cavity_m
            # mi = vi * (inv_new_v * m_new - inv_cavity_v * cavity_m)
            print ("0*infinity iiii")
            print (inv_cavity_v)
        else:
            mi = vi * (inv_new_v * m_new - inv_cavity_v * cavity_m)

        si = Zi

        #print(mi, vi ,Zi)
        return mi[-1], vi ,Zi[-1]

>>>>>>> 42ad9e57f2c86db396aaeed1875967fc81eb2d8e
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
<<<<<<< HEAD
        s_diag   = np.concatenate((s2,s2_t),axis=0)
=======
        s_diag   = np.concatenate((s2*np.ones(n),s2_t),axis=0)
>>>>>>> 42ad9e57f2c86db396aaeed1875967fc81eb2d8e
        s_joint =  np.diag(s_diag)
        print(mu_joint.shape,'  ',s_joint.shape)
        return mu_joint,s_joint
    
    def kernel_func(self,x1,x2,param1):
        squared_distance = lambda x, y: np.array([[(x[i] - y[j])**2 for i in range(len(x))] for j in range(len(y))])
        D = squared_distance(x1,x2)
        cov = (1+np.sqrt(3*D)/param1)*np.exp(-np.sqrt(3*D)/param1)
        return cov
