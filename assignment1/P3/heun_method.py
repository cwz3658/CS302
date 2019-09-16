#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 12:08:44 2019

@author: zhangyan
"""


def heun_method(y_dot, initial_condition, a, b, h):
    """
    y_dot: the function y_dot = f(t, y)
    initial_condition = y(t = a)
    [a, b]: the interval between which you want to compute y
    h: step size
    
    return the simulated time series and the corresponding y values
    """
    # initialization
    t = a
    t_list = [t]
    y = initial_condition
    y_list = [initial_condition]
    
    # compute y value inductiively
    while t < b:
        y_pre = y + h * y_dot(t, y)
        y = y + (h/2)*(y_dot(t, y) + y_dot(t + h, y_pre))
        t = t + h
        t_list.append(t)
        y_list.append(y)
    
    return t_list, y_list