# -*- coding: utf-8 -*-
"""
Created on Tue Mar 01 11:47:28 2016

@author: yiyuezhuo
"""

import numpy as np
import math
from scipy.integrate import odeint
import matplotlib.pyplot as plt

import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd



def yc(t,y0,c0,i,a,b):
    #这个基于的是错误的解析公式
    lam1=math.sqrt(b)-1
    lam2=-math.sqrt(b)-1
    c1=0.5*y0+0.5/math.sqrt(b)*c0
    c2=-0.5*y0+0.5/math.sqrt(b)*c0
    y=c1*np.exp(lam1*t)-c2*np.exp(lam2*t)+i*t
    c=math.sqrt(b)*c1*np.exp(lam1*t)+math.sqrt(b)*c2*np.exp(lam2*t)+a*t
    return y,c
    
def close_form(t,y0,c0,I,a,b):
    #这个根据的是正确的解析公式
    sb=math.sqrt(b)
    lam1=sb-1.0
    lam2=-sb-1.0
    up=y0-(a+I)/(1.0-b)
    down=c0-(a+b*I)/(1.0-b)
    C1=(1.0/(2*sb))*(sb*up+down)
    C2=(1.0/(2*sb))*((-sb)*up+down)
    M1=C1*np.exp(lam1*t)
    M2=C2*np.exp(lam2*t)
    M3=1.0/(1.0-b)
    y=M1-M2+(a+I)*M3
    c=sb*M1+sb*M2+(b*I+a)*M3
    return y,c
    
def d_yc(y,c,y0,c0,i,a,b):
    dy=c+i-y
    dc=a+b*y-c
    return np.array([dy,dc])
    
def custom_ode(func,y0,t,maxiter=100,min_step=0.01):
    step=max(t/maxiter,min_step)
    ting=0.0
    y=np.array(y0)
    print func,y0,t,maxiter,min_step,step,ting,y
    while ting<t:
        print y
        grad=func(y,ting)
        y+=grad*step
        ting+=step
    return y
    
def scipy_way(t,y0,c0,i,a,b,niter=100):
    '''这里的t是积到t的意思,odeint接受的是“中继点”序列，并不是说计算那些点的位置，
    而是就是只在那几个点用迭代法计算下一个点，非常坑爹'''
    Y0=[y0,c0]
    def _d_yc(Y,t):
        return d_yc(Y[0],Y[1],Y0[0],Y0[1],i,a,b)
    t=np.linspace(0,t,niter)
    return odeint(_d_yc,Y0,t)
    
def custom_way(t,y0,c0,i,a,b,**kwarg):
    Y0=[y0,c0]
    def _d_yc(Y,t):
        return d_yc(Y[0],Y[1],Y0[0],Y0[1],i,a,b)
    return custom_ode(_d_yc,Y0,t,**kwarg)

def stream(i,a,b):
    '''
    dy=c+i-y
    dc=a+b*y-c
    '''
    y, c = np.mgrid[0:30:100j, 0:30:100j]
    dy=c+i-y
    dc=a+b*y-c
    plt.streamplot(c,y,dc,dy)
    plt.show()
    
def sample(i_sample=None,a=0.5,b=0.5,size=100):
    if not(i_sample):
        i=np.random.rand(size)
    else:
        i=i_sample
    y=(a+i)/(1.0-b)
    c=a+b*y
    return [{'y':y[j],'c':c[j],'i':i[j]} for j in range(size)]
    
def test(formula,**kwarg):
    df=pd.DataFrame(sample(**kwarg))
    mod=smf.ols('y~i',data=df)
    print mod.fit().summary()
