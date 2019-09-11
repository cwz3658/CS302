#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 11:56:04 2019

@author: zhangyan
"""
from euler_method import *
from heun_method import *
import matplotlib.pyplot as plt

# model parameter
N = 100
gamma =  0.25


for beta in [0.03, 0.06, 0.1]:
    for h in [0.01, 0.5]:
    # the differential equation for I 
        I_dot = lambda t, I: beta*(N - I)*I - gamma*I
        I_initial = 10
        a = 0
        b = 50
        h = 0.1
        
        t_list, I_list = heun_method(I_dot, I_initial, a, b, h)
        plt.plot(t_list, I_list)
