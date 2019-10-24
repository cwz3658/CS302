#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 19:48:30 2019

@author: chen
"""

import numpy as np
import matplotlib.pyplot as plt

result=[]

fig, figs = plt.subplots(2, 2, sharey=True, tight_layout=True)

M=50
N=10
for i in range(M):
    z=np.random.choice([-1, 1], size=N)
    S=np.sum(z)
    result.append(S/np.sqrt(N))    

fig1=plt.subplot(221)
fig1.hist(result,bins=20)
fig1.set_title('M=50 N=10')

result=[]
M=50
N=1000
for i in range(M):
    z=np.random.choice([-1, 1], size=N)
    S=np.sum(z)
    result.append(S/np.sqrt(N))    
fig2=plt.subplot(222)
fig2.hist(result,bins=20)
fig2.set_title('M=50 N=1000')


result=[]
M=5000
N=10
for i in range(M):
    z=np.random.choice([-1, 1], size=N)
    S=np.sum(z)
    result.append(S/np.sqrt(N))    
fig3=plt.subplot(223)
fig3.hist(result,bins=20)
fig3.set_title('M=5000 N=10')


result=[]
M=5000
N=1000
for i in range(M):
    z=np.random.choice([-1, 1], size=N)
    S=np.sum(z)
    result.append(S/np.sqrt(N))    
fig4=plt.subplot(224)
fig4.hist(result,bins=20)
fig4.set_title('M=5000 N=1000')


#z=np.random.choice([-1, 1], size=N)
#S=np.cumsum(z)
#plt.figure()
#plt.plot(S)



