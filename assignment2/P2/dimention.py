#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 11:31:38 2019

@author: chen
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

grid=100



x=origin_x
y=origin_y
Number=[]
Epsilon=[]
for epsilon_n in range(2,100):
    H, xedges, yedges=np.histogram2d(x,y,bins=np.arange(0,grid+grid/epsilon_n,grid/epsilon_n))
    N_e=np.count_nonzero(H)
    Number=np.append(Number,N_e)
    Epsilon=np.append(Epsilon,grid/epsilon_n)    

plt.figure()
plt.loglog(Epsilon, Number)
plot_x=np.log(Epsilon)
plot_y=np.log(Number)
slope, intercept, r_value, p_value, std_err = linregress(plot_x,plot_y)
print(slope,intercept)
