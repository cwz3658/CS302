import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from people import People
from people import Room
import scipy as sci
import pygame

def ini():
    # create a bunch of particles
    num_people = 40
    vec_v = np.array([0, 0])
    r = 0.25  # in meters
    #random initial position and check overlap
    overlap= False 
    p_list=[]
    while len(p_list)<num_people:
        P=People(np.random.rand(2) * 10, vec_v, r,np.random.rand(2),screen)
        for p_j in p_list:
            if p_j.overlap(P):
                overlap= True 
                break
            overlap= False 
        if overlap== False:
            p_list.append(P)
    return p_list

def evacuate():
    for p in p_list:
        if sci.linalg.norm(p.vec_r-room.door_middle_point)<1:
           p_list.remove(p) 

def animate(i,screen):
    F_list=[]
    dt = 0.008
    panic=0.8
    R=5 #virtual range
    for p in p_list:
        # compute forces
                
        # compute forces from others
        F_from_others = np.array([0.0, 0.0])
        ei_from_others = np.array([0.0, 0.0])
        count=0
        for p_j in p_list:
            if p_j is not p:
                F_from_others += p.F_from_other(p_j)
                if sci.linalg.norm(p_j.vec_r - p.vec_r)<R:
                    ei_from_others+=p_j.vec_ei
                    count+=1
        
        # compute forces from within
        if not count==0:
            x_ei=(1-panic)*p.vec_ei+panic*ei_from_others/count
            p.vec_ei=x_ei/sci.linalg.norm(x_ei)
        if sci.linalg.norm(room.door_middle_point - p.vec_r)<R:
            p.vec_ei = (room.door_middle_point - p.vec_r) / sci.linalg.norm(
                room.door_middle_point - p.vec_r
                )  # desired direction to middle of the door position
        p.vec_ei = (room.door_middle_point - p.vec_r) / sci.linalg.norm(
                room.door_middle_point - p.vec_r
                ) 
        F_from_self = p._F_from_self(p.vec_ei)  # F from self

        
        # compute forces from wall
        F_from_wall = p.F_from_wall(room.wall)

        Fi = F_from_self + F_from_others + F_from_wall
        F_list.append(Fi)

    for i, p in enumerate(p_list):
        p.move(F_list[i], dt)
        p.draw(screen)

# create the room
room_length,room_width=10,10
room=Room(room_length,room_width,'rec')

# norm(np.cross(p2-p1, p1-p3))/norm(p2-p1)

#create screen
background_colour = (255,255,255)
(width, height) = (600, 600)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Escape Panic')

#initalization
p_list=ini()

i=0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    i+=1
    screen.fill(background_colour)
    evacuate()
    animate(i,screen)
    room.draw(screen)
    pygame.display.flip()
