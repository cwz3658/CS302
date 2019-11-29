"""
Patches
    1.Primative shapes in Matplotlib are known as patches
    2.Provided by the patches module
    3.Subclasses of patch provide implementations for Rectangles, Arrow, Ellipses, Arcs, Circles
    4.All of this is part of the Artist API, which also provides support for text.
    5.In fact, everything drawn using Matplotlib is part of the artists module.
    6.It's just a different level of access for drawing shapes compared to plots. 
"""


"""
Drawing
    1.Drawing is a matter of adding the patch to the current figure's axes
"""

import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure()
fig.set_dpi(100)
fig.set_size_inches(7, 6.5)

ax = plt.axes(
    xlim=(-10, 10), ylim=(-10, 10)
)  # add an axes to the current figure and make it the current axes
patch = plt.Circle((5, -5), 0.75, fc="y")  # create a circle object
ax.add_patch(patch)


def init():
    """
    init() function serves to setup the plot for animating:
        1. create the first frame to display
    """
    patch.center = (
        5,
        5,
    )  # create a user defined attribute of the patch, which is a circle
    return (patch,)


def animate(i):
    """
    the task of animate function is to:
        1. create a new frame
        2. if blit = True, need to return the artists that are changed
    """
    x, y = patch.center
    x = 5 + 3 * np.sin(np.radians(i))
    y = 5 + 3 * np.cos(np.radians(i))
    patch.center = (x, y)

    new_patch = plt.Circle((x, y), 0.75, fc="y")
    ax.add_patch(
        new_patch
    )  # this line makes ax also changes, so you need to return ax also to tell the blit algorithm
    return [patch, ax]


# Setting blit=True ensures that only the portions of the image which have changed are updated.
# init() and animate() returns (patch, ) , this tells the animation function which artists are changing.
anim = animation.FuncAnimation(
    fig, animate, init_func=init, frames=360, interval=200, blit=True
)


plt.show()
