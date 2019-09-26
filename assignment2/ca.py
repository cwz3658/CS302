#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 15:53:58 2019

@author: chen
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation


#parameters
sparsity=0.6
lane=3
length=20

#rule 1:move forward if possibale
def rule1(cell):
    if cell == [0,0,0]:
        return 0
    elif cell == [0,0,1]:
        return 0
    elif cell == [0,1,0]:
        return 0
    elif cell == [0,1,1]:
        return 1
    elif cell == [1,0,0]:
        return 1    
    elif cell == [1,0,1]:
        return 1
    elif cell == [1,1,0]:
        return 0
    elif cell == [1,1,1]:
        return 1

def nextstate(route):
    route_new=np.zeros((lane, length))
    for i in range(lane) :
        route_new[i][0]=rule1([route[i][length-1],route[i][0],route[i][1]])
        route_new[i][length-1]=rule1([route[i][length-2],route[i][length-1],route[i][0]])
        for j in range(1,length-1):
            route_new[i][j]=(rule1([route[i][j-1],route[i][j],route[i][j+1]]))
    return route_new


fig=plt.figure()
route=np.random.rand(lane, length)<sparsity

pop=[]
for k in range(50):
    plot=plt.imshow(route)
    pop.append([plot])
    route=nextstate(route)
    
anima=ArtistAnimation(fig, pop ,interval=200)
plt.show()






