import pygame
import random
import math
class Particle():
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.colour = (0, 0, 0)
        self.thickness = 1
        self.speed = 0
        self.angle = 0

    def display(self):
        pygame.draw.circle(screen, self.colour, (int(self.x), int(self.y)), self.size, self.thickness)

    def move(self):
        self.angle=math.atan2(self.y-300,self.x-550) #aim to 300,300
        self.y -= math.sin(self.angle) * self.speed
        self.x -= math.cos(self.angle) * self.speed
    
        
def ini():
    number_of_particles = 20
    my_particles = []
    for n in range(number_of_particles):
        size = random.randint(10, 20)
        x = random.randint(size, width-size-50)
        y = random.randint(size, height-size)

        particle = Particle(x, y, size)
        particle.speed = 1
        particle.angle = 0
        my_particles.append(particle)
    return my_particles

def repulsive(p1,p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size:
        tangent = math.atan2(dy, dx)
        angle = 0.5 * math.pi + tangent

        angle1 = 2*tangent - p1.angle
        angle2 = 2*tangent - p2.angle
        speed1 = p2.speed
        speed2 = p1.speed

        (p1.angle, p1.speed) = (angle1, speed1)
        (p2.angle, p2.speed) = (angle2, speed2)

        p1.x += math.sin(angle)
        p1.y -= math.cos(angle)
        p2.x -= math.sin(angle)
        p2.y += math.cos(angle)


background_colour = (255,255,255)
(width, height) = (600, 600)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Escape Panic')

my_particles=ini()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(background_colour)
    pygame.draw.lines(screen,(0, 0, 0),0,[(550,310),(550,590),(5,590),(5,5),(550,5),(550,290)],10)
    for i, particle in enumerate(my_particles):
        particle.move()
        for particle2 in my_particles[i+1:]:
            repulsive(particle, particle2)
        particle.display()
    pygame.display.flip()