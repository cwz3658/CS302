#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 17:51:11 2019

@author: palala
introducing the idea of plotting with a stateful mind: 
    what figure we are currently working with
    what axes we are currently working with
    ...

figures and axes are objects:
    1. a figure is a container holding our plots, you can think of the figure as
    the whole window that all plots will be painted on.
    2. the axes are the actual plots
    3. a figure can have multiple plots
    
OOP approach when working with multiple figures and axes:
    
"""
from matplotlib import pyplot as plt
plt.style.use('seaborn')

ages_x = [1, 2, 3]
dev_y = [4, 5, 6]
py_dev_y = [4.4, 5.5, 6.6]
js_dev_y = [10, 20, 30]

# (ax1, ax2) = ... this is called unpack 
fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True) # by default subplots create a figure and then specify 
                         # a certain number of rows and columns of axes(i.e. plots)
                         # if rows and cols are not provided, the default is 1 by 1
                         # i.e. the default is simple one axis 

ax1.plot(ages_x, dev_y, 
         color='#5a7d9a', 
         linestyle='--', 
         marker='.', 
         linewidth = 3, 
         label='All Devs')  # label is used to specify legend

ax2.plot(ages_x, py_dev_y,  
         label='Python')

ax2.plot(ages_x, js_dev_y, label='JavaScript')

ax1.legend()
# ax1.set_xlabel('Ages')
ax1.set_ylabel('Median Salary')
ax1.set_title('Median Salary (USD) by Age')

ax2.legend()
ax2.set_xlabel('Ages')
ax2.set_ylabel('Median Salary')
# x2.set_title('Median Salary (USD) by Age')
# plt.grid(True)
plt.tight_layout()
plt.show()
