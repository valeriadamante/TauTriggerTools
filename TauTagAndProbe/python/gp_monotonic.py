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
from numpy import sqrt
from numpy.linalg import inv


class monotonic:
    def __init__(self,gp,xl,yl,yerr):
        self.xl = xl
        self.yl = yl
        self.sigma_2n = np.repeat(0.04985623,len(xl))# Need to optimize 
        self.l,self.eta = 15.0,1.0

        self.Xm = np.linspace(xl[80],xl[-1],int(len(xl)*0.1))
        #np.insert(self.Xm,len(self.Xm),200)
        ##To Force monotoncity
        Xtemp = np.linspace(xl[0],xl[-1],int(len(xl)*0.25))
        latent_der = np.dot(self.D1RBF(Xtemp,self.xl,self.l,self.eta),
                            np.dot(inv(self.RBF_cov(self.xl,self.xl,self.l,self.eta)+self.sigma_2n*np.eye(len(xl))),self.yl))
        Xm_list = [Xtemp[i] for i in range(len(Xtemp)) if latent_der[i]<0]
        Xm_list = [80,100,125,150]
        
        #self.Xm = np.array(Xm_list)
        #self.Xm = Xm
        self.y_pred,y_std= gp.predict(np.atleast_2d(self.Xm).T,return_std=True)
        
        M,N = len(self.Xm),len(self.xl)

        ## Computing GP prior with derivatives
        
        Kff  = self.RBF_cov(self.xl,self.xl,self.l,self.eta)
        Kff1 = self.D1RBF(self.xl,self.Xm,self.l,self.eta)
        Kf1f = self.D1RBF(self.Xm,self.xl,self.l,self.eta)
        Kf1f1= self.D2RBF(self.Xm,self.Xm,self.l,self.eta)
        
        A = np.concatenate((Kff , Kff1), axis=1)
        B = np.concatenate((Kf1f, Kf1f1), axis=1)

        self.ym = np.dot(Kff1.T,np.dot(inv(Kff+np.diag(self.sigma_2n)),self.yl))
        self.K_joint = np.concatenate((A,B),axis=0)
        self.f_joint = np.concatenate((self.yl,self.ym))
        ## Initialise posterior

        mu_tilda,v_tilda = np.zeros(M),np.repeat(0.04985623,M)
        
        self.mu_tilda,self.v_tilda,self.Z_tilda = self.deploy_EP(mu_tilda,v_tilda)
        self.mu_tilda_joint,self.S_tilda_joint = self.joint_vector(yl,self.mu_tilda,self.sigma_2n,self.v_tilda)
        #self.mu_tilda_joint,self.S_tilda_joint = self.deploy_EP(mu_tilda,v_tilda)
        
    def predict(self,xstar):
        Kffstar = self.RBF_cov(xstar,self.xl,self.l,self.eta)
        Kf1fstar= self.D1RBF(xstar,self.Xm,self.l,self.eta)
        x_joint = np.concatenate((self.xl,self.Xm))
        K_starf   = np.concatenate((Kffstar,Kf1fstar),axis=1)
        K_star2   = self.RBF_cov(xstar,xstar,self.l,self.eta)
        
        f_pred = np.dot(self.mu_tilda_joint,np.dot(np.linalg.inv(self.K_joint+self.S_tilda_joint),K_starf.T))
        f_cov  = K_star2 - np.dot(K_starf,np.dot(np.linalg.inv(self.K_joint+self.S_tilda_joint),K_starf.T))
        
        return f_pred,np.diag(f_cov)
    
    def joint_vector(self,y,mu_t,s2,s2_t):
        n,m = len(y),len(mu_t)
        mu_joint = np.concatenate((y, mu_t), axis=0)
        s_diag = np.concatenate((s2,s2_t),axis=0)
        s_joint =  np.diag(s_diag)
        #print(mu_joint.shape,'  ',s_joint.shape)
        return mu_joint,s_joint

    def approx_post(self,mu_t,v_t):
        M = len(self.Xm)
        #mu_t,v_t = np.zeros(M),np.repeat(np.infty,M)
        mu_t_joint,v_t_joint = self.joint_vector(self.yl,mu_t,self.sigma_2n,v_t)
        sigma_post = inv(inv(self.K_joint)+inv(v_t_joint))
        mu_post = np.dot(np.dot(sigma_post,inv(v_t_joint)),mu_t_joint)
        return mu_post[-M:],np.diag(sigma_post)[-M:]

        
    def deploy_EP(self,mu_tilda,v_tilda):
        M = len(self.Xm)
        N = len(self.xl)
        # Initialise data terms.
        Z_tilda = np.ones(M)
        y_i = np.ones(M)
        #mu_post,v_post =np.ones(M),np.repeat(np.infty,M)
        for iteration in range(0):
            print ("Iteration ", iteration)
            # Approximate the posterior
            mu_post,v_post = self.approx_post(mu_tilda,v_tilda)
            
            for i in range(M):
                ######################################################################################
                # Find the cavity distribution parameters.
                if self.division_zero(v_tilda[i], v_post[i]):
                    cavity_m, cavity_v = self.remove_factor(mu_tilda[i], v_tilda[i],mu_post[i], v_post[i])
                else:
                    print ("Skipping ", i, " for division of zero when removing factor for cavity funtion iiii")
                    continue
                ######################################################################################
                # minimise KL divergence, update posterior
                
                m_hat, v_hat, Z_hat = self.compute_moments(y_i[i],cavity_m,cavity_v)
                
                ######################################################################################
                # Update/remove approximate factor fi from q_new (moment matched from min KL)    
                mu_tilda[i], v_tilda[i], Z_tilda[i] = self.update_approximate_factor(cavity_m, cavity_v,m_hat,v_hat, Z_hat)
                
                
        return mu_tilda,v_tilda,Z_tilda
    
    def division_zero(self,v1, v2):
        # check if the variances divide by zero
        inv_v1 = 1. / v1
        inv_v2 = 1. / v2

        if(inv_v1 == inv_v2):
            return False
        else:
            return True
    
    
    def remove_factor(self,mi, vi, m_new, v_new):
        # remove factor from posterior
        inv_vi = 1. / vi
        inv_v_new = 1. / v_new
        cavity_v = 1. / (inv_v_new - inv_vi)
        cavity_m = cavity_v * (m_new * inv_v_new - mi * inv_vi)
        return cavity_m, cavity_v
    def compute_moments(self,y_i,cavity_m,cavity_v):
        nu = 10**(-6)
        a = math.sqrt(nu**2+abs(cavity_v))
        zi = y_i*cavity_m/(a)
        normc_zi = 0.5*erfc(-zi/math.sqrt(2))#0.35*(1+erf(zi))
        normp_zi = math.exp(-0.5*(zi**2-0.918938533204673))#/sqrt(2*math.pi)#
        
        mu_hat     = cavity_m + (y_i*cavity_v * normp_zi)/(normc_zi*a)
        sigma_hat  = cavity_v - (cavity_v**2 * normp_zi)/((nu**2 + abs(cavity_v))*normc_zi)*(zi+normp_zi/normc_zi)

        return mu_hat,sigma_hat,normc_zi

    def update_approximate_factor(self,cavity_m,cavity_v,mu_hat,v_hat,Z_hat):
        inv_v,inv_vhat = 1.0/cavity_v,1.0/v_hat
        v_new,mu_new,Z_new = cavity_v,cavity_m,1
        if(self.division_zero(cavity_v,v_hat)):
            v_new  = 1.0/(inv_vhat-inv_v)
        else:
            v_new = np.infty
        if v_new == np.infty and (inv_v == 0 or mu_new == cavity_m):
            mu_new = cavity_m
        else:
            mu_new = v_new*(inv_vhat*mu_hat-inv_v*cavity_m)
        if(math.isnan(Z_new)):
            Z_new = 1.
        else:
            Z_new = Z_hat*np.sqrt(2*np.pi)*np.sqrt(abs(cavity_v+v_hat))*np.exp(0.5*((cavity_m-mu_hat)**2)/(cavity_v+v_hat))

        return mu_new,v_new,Z_new

    def RBF_cov(self,x1,x2,rho,eta):
        D = np.array([[(i-j)**2 for j in x2] for i in x1])
        return eta**2 * np.exp(D/(-2*rho**2))
    
    def D1RBF(self,x1,x2,rho,eta):
        D = np.array([[(i-j)**2 for j in x2] for i in x1])
        M = -np.array([[(i-j) for j in x2] for i in x1])/(rho**2)
        return self.RBF_cov(x1,x2,rho,eta)*M

    def D2RBF(self,x1,x2,rho,eta):
        D = np.array([[(i-j)**2 for j in x2] for i in x1])
        M = (1-D*rho**(-2))/rho**2
        return self.RBF_cov(x1,x2,rho,eta)*M
        
