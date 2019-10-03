#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 17:43:51 2019

@author: chen
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation


global N, grid
N=30
#attraction=0.8
grid=100

#initial pints
origin_x=np.array([50,51])
origin_y=np.array([50,51])

#random walk
def random_walk(walker_x,walker_y):
    walker_x=walker_x-np.random.choice([-1, 1], size=N)
    walker_y=walker_y-np.random.choice([-1, 1], size=N)
    walker_x,walker_y=check_bound(walker_x,walker_y)
    return walker_x,walker_y

#check boundary
def check_bound(x,y):
    for i in range(N):
        if (x[i]<0 or x[i]>grid):
            x[i]=np.random.randint(grid)
            y[i]=np.random.randint(grid)
    return x,y

#particles around or not
def neighbor_particle(root_x,root_y,walker_x,walker_y):
    for i in range(len(root_x)):
        #find x in neighbor
        x_neighbor=np.argwhere(abs(walker_x-root_x[i])<=1)
        for j in range(len(x_neighbor)):
            #find y in neighbor, the real neighbor
            if (abs(walker_y[x_neighbor[j]]-root_y[i])<=1):
                #assign the neighbor to root
                root_x=np.append(root_x,walker_x[x_neighbor[j]])
                root_y=np.append(root_y,walker_y[x_neighbor[j]])
                #re-roll the walker       
                walker_x[x_neighbor[j]]=np.random.randint(grid)
                walker_y[x_neighbor[j]]=np.random.randint(grid)
    return root_x,root_y,walker_x,walker_y

#plot
def grow_plot(data1x,data1y,data2x,data2y):
    g1=(data1x,data1y)
    g2=(data2x,data2y)
    data=(g1,g2)
    colors = ("red", "green")
    groups = ("root", "particles")
    fig=plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    for data, color, group in zip(data, colors, groups):
        x, y = data
        ax.scatter(x, y, alpha=0.8, c=color, edgecolors='none', s=30, label=group)
    plt.title('DLA grow')
    plt.legend(loc=2)
    return fig

#in each step, run a random walk and checking around
pop=[]
particles_x=np.random.randint(grid,size=N)
particles_y=np.random.randint(grid,size=N)
for i in range(10):
    particles_x,particles_y=random_walk(particles_x,particles_y)
    origin_x,origin_y,particles_x,particles_y=neighbor_particle(origin_x,origin_y,particles_x,particles_y)
    plot=grow_plot(origin_x,origin_y,particles_x,particles_y)
    pop.append([plot])

anima=ArtistAnimation(plt.gcf(), pop ,interval=200)
plt.show()  

