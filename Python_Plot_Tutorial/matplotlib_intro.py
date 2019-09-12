#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 16:29:17 2019

@author: zhangyan
"""

from matplotlib import pyplot as plt

# print(plt.style.available)
# plt.style.use('fivethirtyeight')  # ggplot 
plt.xkcd()  # xkcd comics style

ages_x = [1, 2, 3]

dev_y = [4, 5, 6]
plt.plot(ages_x, dev_y, 
         color='#5a7d9a', 
         linestyle='--', 
         marker='.', 
         linewidth = 3, 
         label='All Devs')  # label is used to specify legend

py_dev_y = [4.4, 5.5, 6.6]
plt.plot(ages_x, py_dev_y,  
         label='Python')

# plt.legend(['All Devs', 'Python'])  # add a list of legends for each plot in the order that they are plotted

js_dev_y = [10, 20, 30]
plt.plot(ages_x, js_dev_y, label='JavaScript')

plt.xlabel('Ages')
plt.ylabel('Median Salary')
plt.title('Median Salary (USD) by Age')
plt.legend()

# plt.grid(True)
plt.tight_layout()

plt.savefig('plot.png')  # save the image in a png file
plt.show()

# format strings: https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.pyplot.plot.html
