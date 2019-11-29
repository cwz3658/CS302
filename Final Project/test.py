import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from people import People
from wall import Wall
import scipy as sci
import pygame

background_colour = (255,255,255)
(width, height) = (600, 600)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Escape Panic')

# create a bunch of particles
num_people = 1

vec_v = np.array([0, 0])
# vec_v = np.random.choice([1, -1]) * np.random.rand(2)
r = 0.25  # in meters
vec_r=np.random.rand(2) * 10
# p_list = [People(np.random.rand(2) * 10, vec_v, r,screen) for i in range(num_people)]
# circle_list = [p.draw(screen) for p in p_list]
p_list = [People(np.random.rand(2) * 10, vec_v, r,screen) for i in range(num_people)]
circle_list = [p.draw() for p in p_list]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill(background_colour)
    # pygame.draw.circle(screen, colour, (np.int(x),np.int(y)), np.int(r*100), 1)
    pygame.display.flip()