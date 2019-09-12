#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 16:29:17 2019

@author: zhangyan
"""

from matplotlib import pyplot as plt

ages_x = [1, 2, 3]
dev_y = [4, 5, 6]
plt.plot(ages_x, dev_y, legend='All Devs')  # label is used to specify legend

py_dev_y = [4.4, 5.5, 6.6]
plt.plot(ages_x, py_dev_y, legend='Python')

# plt.legend(['All Devs', 'Python'])  # add a list of legends for each plot in the order that they are plotted

plt.xlabel('Ages')
plt.ylabel('Median Salary')
plt.title('Median Salary (USD) by Age')
