"""
Matplotlib:
    a Python 2D plotting library
Pros:
    good library for decades
Cons:
    Imperative API which is often overly verbose
    Poor support for web and interactive graphs
    slow for large and complicated data
"""

"""
Animation Interface
    1. FuncAnimation
    makes an animation by repeatedly calling a function func
    2. ArtistAnimation
    animation using a fixed set of Artist objects
"""

"""
Fundamental Concepts of Animation: Frames, Layers and Layer Folders 

Basic Technique of animation:
loop:
    1.loading a "frame"
    2.displaying the "frame" on screen

Frame:
    A frame is defined by (image, time the image is to be displayed).
        an image is a matrix, a set of pixels, a ..., many representations.
    A sequence of frames makes an animation.
    Each frame is displayed on the screen until the next frame overwrites it.
    Any scene change happens by drawing a whole new frame. (Even changing a single pixel requires drawing the next frame in its entirety)





"""


"""
Basic Animation: Moving Sine Wave
"""
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use("seaborn-pastel")

# create a figure object
fig = plt.figure()
ax = plt.axes(xlim=(0, 4), ylim=(-2, 2))
# ax.plot() returns a list of Line object which represents 2D lines.
line, = ax.plot([], [], lw=3)

"""
FuncAnimation(fig, func, frames, init_func, ...)
    1.fig is the figure object we will play the animation
    2.func should be a function
        def func(frame, *fargs) -> iterable_of_artists
        where,
            frame is the next value in frames
            frames is Source of data to pass func at each frame of the animation
            artists is an abstract class for objects that render into a figure.
                all visible elements in a figure are subclasses of Artist.
                this means anything that you can plot on a figure is an artist.
"""


def animate(i):
    x = np.linspace(0, 4, 1000)
    y = np.sin(2 * np.pi * (x - 0.01 * i))
    line.set_data(x, y)
    return (line,)  # line is an artist


def init():
    line.set_data([], [])
    return (line,)  # returns a tuple that contains only 1 element


"""
frames: is Source of data to pass func at each frame of the animation
init_func: is a function used to draw a clear frame. (see ref)
interval: delay between frames in milliseconds, Defaults to 200
"""
anim = FuncAnimation(
    fig,
    animate,
    init_func=init,
    frames=range(200),
    interval=20,
    blit=True,
    repeat=False,
)

# display the animation
plt.show()

# save animation in gif
# anim.save("sine_wave.gif", writer="imagemagick")
