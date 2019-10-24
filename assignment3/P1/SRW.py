#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 19:48:30 2019

@author: chen
"""

import numpy as np
import matplotlib.pyplot as plt

M=5000
result=[]
for i in range(M):
    N=np.random.randint(1000)
    z=np.random.choice([-1, 1], size=N)
    S=np.sum(z)
    result.append(S/np.sqrt(N))
    
plt.figure()
plt.hist(result)
#z=np.random.choice([-1, 1], size=N)
#S=np.cumsum(z)
#plt.figure()
#plt.plot(S)



