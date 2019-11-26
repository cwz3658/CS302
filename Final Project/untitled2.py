# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 15:39:58 2019

@author: cwz36
"""

from graphics import*
from time import sleep
from random import random

class people():
    def __int__(self):
        pass

def plot(P,win):
    for i in range(len(P)):
        P[i].position.draw(win)
    for i in range(200):
        sleep(.04)
        update(P)

    
def update(P):
    tau=200
    for i in range(len(P)):
        vx=(P[i].x-600)/tau
        vy=(P[i].y-300)/tau       
        P[i].position.move(-vx,-vy)  
    
    
def ini(N):
    P_list=[]
    radius = 20
    for i in range(N):
        P=people()
        P.x=random()*600
        P.y=random()*600
        P.position=Circle(Point(P.x,P.y),radius)
        P_list.append(P)
    return P_list
    

win = GraphWin("Escape panic simulation",600,600)
P=ini(20)
plot(P,win)
win.getMouse()
win.close()
