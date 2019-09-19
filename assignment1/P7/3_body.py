#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 15:28:17 2019

@author: zhangyan
"""

from scipy.integrate import solve_ivp
import numpy as np
from numpy import linalg as LA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def three_body_model(t, y):
    """
    t: a scalar
    y: an array of state variables
       y = [v1, v2, v3, r1, r2, r3], each element in the array is a 3-vector
    we are modeling the 3-body problem in 3-D space
    returns y 
    """
    # define constants
    G = 6.67e-11
    m1 = 1e30
    m2 = 2e30
    m3 = 3e30

    # initialize y with a 3-D array
    y_dot = np.zeros(18)
    
    # compute each axis iteratively
    
    for i in range(3):
        # extract state variables from y
        v1 = y[i*6 + 0]
        v2 = y[i*6 + 1]
        v3 = y[i*6+ 2]
        r1 = y[i*6+ 3]
        r2 = y[i*6+ 4]
        r3 = y[i*6+ 5]
        
        # compute derivatives
        v1_dot = -G*m2*(r1 - r2)/LA.norm(r1 - r2)**3 - G*m3*(r1 - r3)/LA.norm(r1 - r3)**3
        v2_dot = -G*m3*(r2 - r3)/LA.norm(r2 - r3)**3 - G*m1*(r2 - r1)/LA.norm(r2 - r1)**3
        v3_dot = -G*m1*(r3 - r1)/LA.norm(r3 - r1)**3 - G*m2*(r3 - r2)/LA.norm(r3 - r2)**3
        r1_dot = v1
        r2_dot = v2
        r3_dot = v3
        
        
        # store back
        y_dot[i*6 + 0] = v1_dot
        y_dot[i*6 + 1] = v2_dot
        y_dot[i*6 + 2] = v3_dot
        y_dot[i*6 + 3] = r1_dot
        y_dot[i*6 + 4] = r2_dot
        y_dot[i*6 + 5] = r3_dot
    return y_dot

y0 = [-2e3, 7e3, -4e3, 1e11, 6e11, 7e11, 0.5e3, 0.5e3, -0.5, 3e11, -5e11, 8e11, 5e3, 2e3, -3e3, 2e11, 4e11, -7e11]

end_time = 10*365.26*24*3600 # simulate for 10 years
h = 2 * 3600 # step size is two days


soln = solve_ivp(three_body_model, [0, end_time], y0, max_step = 10)

# extract the position information
y = soln.y
t = soln.t
# 3-D plot
fig = plt.figure(figsize = (10, 10))
ax = fig.gca(projection='3d')

for i in range(3):
    rx, ry, rz = y[3 + i , :], y[9 + i, :], y[15 + i, :]
    ax.plot(rx, ry, rz, label = "Three Body")


ax.legend()
plt.show()
    