import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from people import People
from wall import Wall
import scipy as sci


# Create the fig object, the window showing
fig = plt.figure()
fig.set_dpi(100)  # set resolution
# fig.set_size_inches(6, 6)  $ set figure size

# create a ax object, which is our plot that contains every particle
ax = plt.axes(
    xlim=(0, 20), ylim=(0, 30)
)  # also add the axes to the current figure and make it the current axes


# create a bunch of particles
num_people = 10

vec_v = np.array([0, 0])
# vec_v = np.random.choice([1, -1]) * np.random.rand(2)
r = 0.25  # in meters
p_list = [People(np.random.rand(2) * 10, vec_v, r) for i in range(num_people)]
circle_list = [p.draw() for p in p_list]
# add all circles to ax

# create a wall
b = 19
wall_width = 2  # in meters
wall = Wall(b, wall_width)


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
    for p in p_list:
        # compute forces
        vec_ei = (wall.door_middle_point - p.vec_r) / sci.linalg.norm(
            wall.door_middle_point - p.vec_r
        )  # desired direction to middle of the door position
        F_from_self = p._F_from_self(vec_ei)  # F from self
        # compute forces from others
        F_from_others = np.array([0.0, 0.0])
        for p_j in p_list:
            if p_j is not p:
                F_from_others += p.F_from_other(p_j)
        F_from_wall = p.F_from_wall(wall)

        Fi = F_from_self + F_from_others + F_from_wall
        print(Fi)
        dt = 0.05
        p.move(Fi, dt)

    return circle_list


# Setting blit=True ensures that only the portions of the image which have changed are updated.
# init() and animate() returns (patch, ) , this tells the animation function which artists are changing.
anim = animation.FuncAnimation(
    fig, animate, init_func=init, frames=100000, interval=200, blit=True
)
plt.show()
