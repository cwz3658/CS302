#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 11:56:04 2019

@author: zhangyan
"""
from euler_method import *
from heun_method import *
from matplotlib import pyplot as plt

plt.style.use('seaborn')

# model parameter
N = 100
gamma =  0.25

fig1, axes1 = plt.subplots(nrows=3, ncols=3, sharex=False)
fig1.set_size_inches(18.5, 10.5)

for beta, row in zip([0.03, 0.06, 0.1], range(0, 3)):
    for h, col in zip([0.01, 0.5, 2.0], range(0, 3)):
        # the differential equation for I 
        I_dot = lambda t, I: beta*(N - I)*I - gamma*I
        
        # set parameters
        I_initial = 10
        a = 0
        b = 50 * h
        
        # run integrator and collect data
        t_list_euler, I_list_euler = euler_method(I_dot, I_initial, a, b, h)
        t_list_heun, I_list_heun = heun_method(I_dot, I_initial, a, b, h)
        
        
        # begin plot
        ax = axes1[row, col]
        ax.plot(t_list_euler, I_list_euler, 
                label='euler method')
        ax.plot(t_list_heun, I_list_heun,
                label='heun method')
        ax.set_xlabel('time')
        ax.set_ylabel('number of infectious')
        ax.set_title('beta = {}, h = {}'.format(beta, h), loc='right')
        ax.legend(loc='lower right')

plt.tight_layout()
fig1.savefig('p4_figure.png')