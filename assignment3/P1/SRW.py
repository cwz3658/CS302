#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 19:48:30 2019

@author: chen
"""

import numpy as np
import matplotlib.pyplot as plt

def SRW(M,N,placement):
    result=[]
    for i in range(M):
        z=np.random.choice([-1, 1], size=N)
        S=np.sum(z)
        result.append(S/np.sqrt(N))
    fig=plt.subplot(placement)
    fig.hist(result,bins=20)
    fig.set_title('M=' +str(M)+ ' N=' +str(N))

plt.subplots(2, 2, sharey=True, tight_layout=True)
SRW(50,10,221) 
SRW(50,1000,222) 
SRW(5000,10,223) 
SRW(5000,1000,224) 