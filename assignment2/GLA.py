#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 17:43:51 2019

@author: chen
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation

a=[]
a.append([0,0])
a.append([1,-1])
b=[2,2]

#particle around or not
def neighbor_particle(walker,root):
    for i in range(len(root)):
        if np.linalg.norm(np.subtract(root[i],walker))<1.42:
            root.append(walker)
            return 1
    return 0


while (neighbor_particle(b,a)==0):
    b[0]=b[0]+np.random.choice([-1,1])
    b[1]=b[1]+np.random.choice([-1,1])

    





#
#a=np.linalg.norm(np.subtract(root,walker))
#print(a)

#x_position=3
#y_position=3
#
##random walker
#while (np.linalg.norm([0-x_position,0-y_position])>1.42):
#    x_position=x_position+np.random.choice([-1,1])
#    y_position=y_position+np.random.choice([-1,1])
#    print(x_position,y_position)
#
##









#fig=plt.figure()
#plt.scatter(x_position,y_position)


#pop=[]
#for k in range(999):
#    plot=plt.scatter(x_position[0:k],y_position[0:k])
#    pop.append([plot])
#    
#anima=ArtistAnimation(fig, pop ,interval=200)
#plt.show()
#pop=[]
#
#for i in x_position:
#        if (np.linalg.norm([0-x_position[i],0-y_position[i]])<1.42):
#            print(x_position[i],y_position[i])
#            break