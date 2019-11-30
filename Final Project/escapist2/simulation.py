import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from people import People
from wall import Wall
import scipy as sci
import random

# Create the fig object, the window showing
fig = plt.figure()
fig.set_dpi(100)  # set resolution
# fig.set_size_inches(6, 6)  $ set figure size

# create a ax object, which is our plot that contains every particle
room_width = 20
room_length = 30
ax = plt.axes(
    xlim=(0, room_width), ylim=(0, room_length)
)  # also add the axes to the current figure and make it the current axes

# create people without overlap
def create_people(n):
    """
    1.create n people in the room without overlapping
    2.People initially go towards the wall with the door
    """
    # create people parameters

    vec_v_list = [
        np.array([0.0, 0.0]) for i in range(n)
    ]  # a list of people that are not moving initially

    vec_ei = [
        np.array([0, 1]) for i in range(n)
    ]  # people initially want to go to the door

    vec_r_list = []
    while True:
        # create a new people position in the room
        vec_r = np.array(
            [random.uniform(0, room_width), random.uniform(0, room_length)]
        )

    vec_v_list = [
        np.array([0.0, 0.0]) for i in range(n)
    ]  # a list of people that are not moving initially


# create a wall
b = 19
wall_width = 2  # in meters
wall = Wall(b, wall_width)


# create a bunch of particles
num_people = 3

vec_v = np.array([0, 0])
# vec_v = np.random.choice([1, -1]) * np.random.rand(2)
r = 0.25  # in meters

# add overlap detection


p_list = [
    People(np.random.rand(2) * 5, vec_v, np.array([0, 0]), r) for i in range(num_people)
]
for p in p_list:
    vec_ei = (wall.door_middle_point - p.vec_r) / sci.linalg.norm(
        wall.door_middle_point - p.vec_r
    )  # desired direction to middle of the door position
    p.vec_ei = vec_ei


p_list.append(People(np.array([10, 20]), np.array([0, 0]), np.array([0, 1]), r))

circle_list = [p.draw() for p in p_list]
# add all circles to ax


def init():
    """
    init() function serves to setup the plot for animating:
        1. create the first frame to display
    """
    for c in circle_list:
        ax.add_patch(c)
    # add door representation
    p_lower = (wall.door_pos[0][0] - 0.1, wall.door_pos[0][1])  # door thickness = 10cm
    rectangle = plt.Rectangle(p_lower, 0.1, wall.door_width)
    ax.add_patch(rectangle)
    return circle_list


def animate(i):
    """
    the task of animate function is to:
        1. create a new frame
        2. if blit = True, need to return the artists that are changed
    """
    Fi_list = []
    for p in p_list:
        # compute forces

        F_from_self = p._F_from_self()  # F from self
        # compute forces from others
        F_from_others = np.array([0.0, 0.0])
        for p_j in p_list:
            if p_j is not p:
                F_from_others += p.F_from_other(p_j)
        F_from_wall = p.F_from_wall(wall)

        Fi = F_from_self + F_from_others + F_from_wall

        Fi_list.append(Fi)

    dt = 0.05
    for Fi, p in zip(Fi_list, p_list):
        p.determine_ei(p_list, wall.get_pos(), room_width, room_length)
        p.move(Fi, dt)  # need modify

    return circle_list


# Setting blit=True ensures that only the portions of the image which have changed are updated.
# init() and animate() returns (patch, ) , this tells the animation function which artists are changing.
anim = animation.FuncAnimation(
    fig, animate, init_func=init, frames=100000, interval=200, blit=True
)
plt.show()
