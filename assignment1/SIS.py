# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 11:58:19 2019

@author: cwz36
"""

from pylab import *


    
def initialize():
    global S, I, Sresult, Iresult
    S, I  = 90 ,10 
    N, gama = 100, 0.25
    Sresult=[S]
    Iresult=[I]

def euler(f,y0,t0,te,h):
    t = t0
    timestep = [t]
    y = y0
    yresult = [y]
    while t < te:
         y = y+h * f(t,y)
         t = t+h
         yresult.append(y)
         timestep.append(t)


 
def heun(f,y0,t0,te,h):
	t,y = t0,y0   
   
	while t < te:
         y_hat = y+h * f(t,y)
         y = y + (f(t,y)+f(t+1,y_hat))*h/2 
         t = t+h
         print(y)
         print(t)
    
def Sdot(time, yva):
	return time

initialize()
euler(Sdot,1,0,2,1)
