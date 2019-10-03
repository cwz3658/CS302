#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 20:07:30 2019

@author: chen
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation

fig=plt.figure()

l = 1000
x_steps = np.random.choice([-1, 1], size=l) 
y_steps = np.random.choice([-1, 1], size=l) 
x_position = np.cumsum(x_steps) # integrate the position by summing steps values
y_position = np.cumsum(y_steps)

pop=[]
for k in range(999):
    plot=plt.scatter(x_position[0:k],y_position[0:k])
    pop.append([plot])
    
anima=ArtistAnimation(fig, pop ,interval=200)
plt.show()