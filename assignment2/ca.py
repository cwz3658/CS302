#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 15:53:58 2019

@author: chen
"""
import numpy as np
import matplotlib.pyplot as plt


#initiall
sparsity=0.5
lane=3
route=np.random.rand(lane, 20)<sparsity


plt.imshow(route)
#rule 1:move forward if possibale

