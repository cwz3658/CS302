#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 15:55:41 2019

@author: zhangyan
"""

from pylab import *

N1, N2 = meshgrid(arange(0, 1000, 1), arange(0, 1000, 1))

r1, r2 = 0.5, 1
alpha1, alpha2 = 2, 1
K1, K2 = 800, 600
ro = 10
N1dot = r1 * N1 * (K1 - N1 - alpha2 * N2)/K1 - ro
N2dot = r2 * N2 * (K2 - N2 - alpha1 * N1)/K2 

streamplot(N1, N2, N1dot, N2dot)
show()
