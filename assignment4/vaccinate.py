#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 19:48:30 2019

@author: chen
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

p=1/4
kmax=10  #assume the max degree is 10
ip=0.05  #assume around 5% of the population are infected initially 


# Initial degree distribution and number of infected, pk and I0[k].
global pk
pk=np.zeros(kmax)
Ik=np.zeros(kmax)
for i in range(kmax):
    pk[i]=(p*(1-p)**i)
    Ik[i]=((np.random.rand(1)-0.5)*0.01+ip)*pk[i]

global beta, alpha   
# Contact rate, beta, and recovery rate, gamma, (in 1/week).
beta, alpha = 0.3, 1

# A grid of time points (in weeks)
t = np.linspace(0, 160, 160)

#def SIS(Ik,t):
##    y1=lambda_I*k*(pk-Ik)*theta
#    y1=lambda_I*Ik
#    y2=lambda_I*Ik
##    theta=sum(np.array(range(0,10,1))*Ik)/sum(np.array(range(0,10,1))*pk)
#    return y1

# The SIS model differential equations.
def SIS(I, t):
    dIk=np.zeros(kmax)
    theta=sum(np.array(range(0,kmax,1))*I)/sum(np.array(range(0,kmax,1))*pk)
    for k in range(kmax):
        dIk[k] = beta*k*(pk[k]-I[k])*theta-alpha*I[k]
    return dIk
# Initial conditions vector
I0=Ik
# Integrate the SIR equations over the time grid, t.
ret = odeint(SIS, I0, t)
I=np.zeros(kmax)
I = ret.T
