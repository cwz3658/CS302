import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from people import People
from wall import Wall
import scipy as sci
import pygame

def ini():
    # create a bunch of particles
    num_people = 10
    vec_v = np.array([0, 0])
    rand_ei=np.random.rand(2)-[0.5,0.5]
    vec_ei = rand_ei/sci.linalg.norm(rand_ei)
    r = 0.25  # in meters
    #random initial position and check overlap
    flag= True 
    while flag:
        p_list = [People(np.random.rand(2) * 10, vec_v, r,vec_ei,screen) for i in range(num_people)]
        flag=False
        for p in p_list:
            for p_j in p_list:
                if p_j is not p:
                    if not p.overlap(p_j):
                        flag=True
                        break
    return p_list

def animate(i,screen):
    """
    the task of animate function is to:
        1. create a new frame
        2. if blit = True, need to return the artists that are changed
    """
    F_list=[]
    dt = 0.005
    panic=0.8
    R=1  #virtual range
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
        rand_ei=np.random.rand(2)-[0.5,0.5]
        p.vec_ei=rand_ei/sci.linalg.norm(rand_ei)
        if not count==0:
            x_ei=(1-panic)*p.vec_ei+panic*ei_from_others/count
            p.vec_ei=x_ei/sci.linalg.norm(x_ei)
        if sci.linalg.norm(wall.door_middle_point - p.vec_r)<R:
            p.vec_ei = (wall.door_middle_point - p.vec_r) / sci.linalg.norm(
                wall.door_middle_point - p.vec_r
                )  # desired direction to middle of the door position
        F_from_self = p._F_from_self(p.vec_ei)  # F from self

        
        # compute forces from wall
        F_from_wall = p.F_from_wall(wall)

        Fi = F_from_self + F_from_others + F_from_wall
        F_list.append(Fi)

    for i, p in enumerate(p_list):
        p.move(F_list[i], dt)
        p.draw(screen)

#create screen
background_colour = (255,255,255)
(width, height) = (600, 600)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Escape Panic')

#initalization
p_list=ini()

# create a wall
b = 12
wall_width = 2  # in meters
wall = Wall(b, wall_width)

i=0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    i+=1
    screen.fill(background_colour)
    animate(i,screen)
    # pygame.draw.lines(screen,(0, 0, 0),0,[(550,310),(550,590),(5,590),(5,5),(550,5),(550,290)],10)
    pygame.display.flip()
