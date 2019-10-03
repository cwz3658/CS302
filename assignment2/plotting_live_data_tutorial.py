import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


plt.style.use("fivethirtyeight")

x_vals = []
y_vals = []

plt.plot(x_vals, y_vals)


index = count()  # an iterator with __next__() method


def animate(i):
    x_vals.append(next(index))
    y_vals.append(random.randint(0, 5))

    plt.cla()
    plt.plot(x_vals, y_vals)


# we want to run this function every second and plot them
# interval is in unit of ms, thus 1000 ms is 1 second
# plt.gcf() : get current fig object
# matplotlib is going to run the animate function every 1 second
ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()


# data = pd.read_csv('data.csv')
# x = data['x_value']
# y1 = data['total_1']
# y2 = data['total_2']
