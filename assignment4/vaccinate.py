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

# Contact rate, beta, and recovery rate, gamma, (in 1/week).
global beta, alpha 
beta, alpha = 0.3, 1

# A grid of time points (in weeks)
t = np.linspace(0, 160, 160)

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
plt.figure()
Ik = odeint(SIS, I0, t)
lines=plt.plot(t, Ik*100)
plt.legend(lines[:kmax], ["k={}".format(k) for k in range(kmax)])
plt.title('SIS outbreak of nodes in each degree (no vaccination)')
plt.xlabel ('Time (/weeks)')
plt.ylabel ('infected fraction over entire population (%)')




def SISV(I, t,nu, ro):
    dIk=np.zeros(kmax)
    theta=sum(np.array(range(0,kmax,1))*I)/sum(np.array(range(0,kmax,1))*pk)
    for k in range(kmax):
        dIk[k] = beta*k*(pk[k]-I[k])*theta*(nu*ro+1-nu)-alpha*I[k]
    return dIk

plt.figure()
# vaccinated population, nu and the transmission rate reduced factor ro
nu = 0.4
for i in range(0,11,2):
    ro=1-i/10
    Ikv = odeint(SISV, I0, t, args=(nu, ro))
    Total=sum(Ikv.T)
    plt.plot(t, Total,label="rho={}%".format(np.int((1-ro)*100)))
    plt.legend()
plt.title('SIS outbreak eradicated by vaccination')
plt.xlabel ('Time (/weeks)')
plt.ylabel ('infected fraction over entire population (%)')


#comparison 
plt.figure()
Eventual_I=[]
nu = 0.4
for i in range(0,110,2):
    ro=1-i/100
    Ikv = odeint(SISV, I0, t, args=(nu, ro))
    Total=sum(Ikv.T)
    Eventual_I.append(Total[159])
Eventual_I.reverse()
rho = np.linspace(0, 1, 55)
plt.plot(rho, Eventual_I)
plt.title('40% randomly vaccinated')
plt.xlabel ('1-rho')
plt.ylabel ('infected population when system is stable (%)')


Eventual_I=[]
plt.figure()
nu = 0.8
for i in range(0,110,2):
    ro=1-i/100
    Ikv = odeint(SISV, I0, t, args=(nu, ro))
    Total=sum(Ikv.T)
    Eventual_I.append(Total[159])
Eventual_I.reverse() 
rho = np.linspace(0, 1, 55)
plt.plot(rho, Eventual_I)
plt.title('40% population in highest degree gets vaccine')
plt.xlabel ('1-rho')
plt.ylabel ('infected population when system is stable (%)')