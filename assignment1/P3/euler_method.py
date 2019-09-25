#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 10:14:53 2019

@author: Yan Zhang, Wenzhe Chen
the script implements Euler's Method
"""


def euler_method(y_dot, initial_condition, a, b, h):
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
        y = y + y_dot(t, y) * h  # compute next y value using the current y value
        y_list.append(y)
        t = t + h
        t_list.append(t)

    return t_list, y_list
