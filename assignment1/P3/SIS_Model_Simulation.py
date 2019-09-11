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
beta = 0.03; gamma =  0.25
N = 100

# the differential equation for I 
I_dot = lambda t, I: beta*(N - I)*I - gamma*I
I_initial = 20
a = 0
b = 50
h = 0.1

t_list, I_list = heun_method(I_dot, I_initial, a, b, h)
plt.plot(t_list, I_list)
