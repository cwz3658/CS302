#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 15:28:17 2019

@author: zhangyan
"""

import scipy as sci
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# define constants and reference quantities 
G = 6.67408e-11 
# reference quantities
m_nd = 1.989e30 # kg, mass of the sun
r_nd = 5.326e12 # m, distance between stars in Alpha Centauri
v_nd = 30000 # m/s relative velocity of earth around the sun
t_nd = 79.91*365*24*3600*0.51 #s #orbital period of Alpha Centauri

# Net constants
K1=G*t_nd*m_nd/(r_nd**2*v_nd)
K2=v_nd*t_nd/r_nd

# since we will use the non-dimensionalized equations, all variables
# after this point will be non-dimensional, i.e. they are ratio of
# the real quantity to the reference quantity

# define masses
m1 = 1.1
m2 = 0.907 
m3 = 1.0 

# define initial position vectors
r1 = np.array([1, 0, 0])
r2 = np.array([0, 1, 0])
r3 = np.array([0, 0, 1])

# define initial velocities
v1 = np.array([0.01, 0.01, 0.001]) 
v2 = np.array([-0.05, 0, -0.1])
v3 = np.array([0, -0.01, 0])


#A function defining the equations of motion 
def ThreeBodyEquations(w,t,G,m1,m2,m3):
    r1=w[:3]
    r2=w[3:6]
    r3=w[6:9]
    v1=w[9:12]
    v2=w[12:15]
    v3=w[15:18]
    r12=sci.linalg.norm(r2-r1)
    r13=sci.linalg.norm(r3-r1)
    r23=sci.linalg.norm(r3-r2)
    
    dv1bydt=K1*m2*(r2-r1)/r12**3+K1*m3*(r3-r1)/r13**3
    dv2bydt=K1*m1*(r1-r2)/r12**3+K1*m3*(r3-r2)/r23**3
    dv3bydt=K1*m1*(r1-r3)/r13**3+K1*m2*(r2-r3)/r23**3
    dr1bydt=K2*v1
    dr2bydt=K2*v2
    dr3bydt=K2*v3
    r12_derivs=sci.concatenate((dr1bydt,dr2bydt))
    r_derivs=sci.concatenate((r12_derivs,dr3bydt))
    v12_derivs=sci.concatenate((dv1bydt,dv2bydt))
    v_derivs=sci.concatenate((v12_derivs,dv3bydt))
    derivs=sci.concatenate((r_derivs,v_derivs))
    return derivs

#Package initial parameters
init_params=sci.array([r1, r2, r3, v1, v2, v3]) #create array of initial params
init_params=init_params.flatten() #flatten array to make it 1D
time_span=sci.linspace(0,20,500) #8 orbital periods and 500 points
#Run the ODE solver
import scipy.integrate
three_body_sol=sci.integrate.odeint(ThreeBodyEquations,init_params,time_span,args=(G,m1,m2, m3))

r1_sol=three_body_sol[:,:3]
r2_sol=three_body_sol[:,3:6]
r3_sol=three_body_sol[:, 6:9]

#Create figure
fig=plt.figure(figsize=(15,15))
#Create 3D axes
ax=fig.add_subplot(111,projection="3d")
#Plot the orbits
ax.plot(r1_sol[:,0],r1_sol[:,1],r1_sol[:,2],color="darkblue", label = 'm1')
ax.plot(r2_sol[:,0],r2_sol[:,1],r2_sol[:,2],color="tab:red", label = 'm2')
ax.plot(r3_sol[:,0],r3_sol[:,1],r3_sol[:,2],color="yellow", label = 'm3')
#Plot the final positions of the stars
#ax.scatter(r1_sol[-1,0],r1_sol[-1,1],r1_sol[-1,2],color="darkblue",marker="o",s=100,label="Alpha Centauri A")
#ax.scatter(r2_sol[-1,0],r2_sol[-1,1],r2_sol[-1,2],color="tab:red",marker="o",s=100,label="Alpha Centauri B")
#Add a few more bells and whistles
ax.set_xlabel("x-coordinate",fontsize=14)
ax.set_ylabel("y-coordinate",fontsize=14)
ax.set_zlabel("z-coordinate",fontsize=14)
ax.set_title("Orbits of suns in a three-body system\n r1 = {} \n r2 = {} \n r3 = {} \n v1 = {}, \n v2 = {} \n v3 = {} ".format(r1, r2, r3, v1, v2, v3),fontsize=14)
ax.legend(loc="upper left",fontsize=14)
plt.tight_layout()