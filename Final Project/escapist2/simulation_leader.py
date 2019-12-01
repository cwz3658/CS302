import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from people import People
from wall import Wall
import scipy as sci
import random
from scipy.linalg import norm

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
def create_people(
    n, room_width, room_length, door_pos, p_i_range, Rv_range, percent_p_at_loss=1
):
    """
    1.create n people in the room without overlapping
    2.also returns the circle_list, which is the representations of people
    """
    # define a helper function to create people's position randomly in the room
    def random_pos():
        return np.array(
            [random.uniform(2, room_width - 2), random.uniform(2, room_length - 2)]
        )

    def random_unit_vector():
        """
        generate a random unit 2-vector
        this should be changed to make it really random i.e. -1
        """
        # create a random unit 2-vector
        vec = np.array([random.uniform(-1, 1), random.uniform(-1, 1)])
        while vec[0] == 0 and vec[1] == 0:
            vec = np.array(random.random(), random.random())

        unit_vec = vec / norm(vec)
        return unit_vec

    def unit_vector_point_to_door(p):
        return (door_pos - p.vec_r) / norm(np.array(door_pos) - p.vec_r)

    def random_velocity(max_speed):
        # create people parameters
        speed = np.random.choice(list(range(max_speed + 1)))
        return speed * random_unit_vector()

    def random_r_i():
        return random.uniform(0.25, 0.35)

    # begin to create our people list
    people_list = []
    while len(people_list) < n:
        if (
            random.random() < percent_p_at_loss
        ):  # percent_p_at_loss% people run randomly
            new_p = People(
                random_pos(),
                random_velocity(1),
                random_unit_vector(),
                random_r_i(),
                random.uniform(p_i_range[0], p_i_range[1]),
                random.uniform(Rv_range[0], Rv_range[1]),
            )
        else:  # remaining people know the direction
            new_p = People(
                random_pos(), random_velocity(1), random_unit_vector(), random_r_i()
            )
            new_p.vec_ei = unit_vector_point_to_door(new_p)
        # check overlap
        overlap = False
        for p in people_list:
            if p.overlap(new_p):
                overlap = True
                break
        if not overlap:
            people_list.append(new_p)

    circle_list = [p.draw() for p in people_list]
    return people_list, circle_list


# create a wall
b = 19
door_width = 2  # in meters
wall_right = Wall(b, door_width)
wall_left = Wall(0, 0)
wall_up = Wall(room_length, 0)
wall_down = Wall(0, 0)

# create people


def initialize():
    global p_list, time_to_escape, timer
    p_i_range = (0, 0.1)
    Rv_range = (
        100,
        101,
    )  # this means everyone knows where is the exit and do not follow others.

    p_list, _ = create_people(
        40, room_width, room_length, wall_right.get_pos(), p_i_range, Rv_range
    )

    time_to_escape = []
    timer = 0.0


def update_observe(dt):
    """
    the task of animate function is to:
        1. create a new frame
        2. if blit = True, need to return the artists that are changed
    """
    global p_list, time_to_escape, timer
    Fi_list = []
    for p in p_list:
        # compute forces

        F_from_self = p.F_from_self()  # F from self
        # compute forces from others
        F_from_others = np.array([0.0, 0.0])
        for p_j in p_list:
            if p_j is not p:
                F_from_others += p.F_from_other(p_j)
        F_from_wall = (
            p.F_from_wall(wall_left, "left")
            + p.F_from_wall(wall_right, "right")
            + p.F_from_wall(wall_up, "up")
            + p.F_from_wall(wall_down, "down")
        )

        Fi = F_from_self + F_from_others + F_from_wall

        Fi_list.append(Fi)

    timer += dt
    for Fi, p in zip(Fi_list, p_list):
        p.determine_ei(p_list, wall_right.get_pos(), room_width, room_length)
        p.move(Fi, dt, room_width, room_length)  # need modify
        if p.reach_door(wall_right.get_pos()):
            p_list.remove(p)
            print("escapist succeed!")
            print("# of people remains:", len(p_list))
            time_to_escape.append(timer)
    return


total_sim_time = 30 * 60  # in seconds
dt = 0.01 * 0.95  # in seconds
initialize()
while timer <= total_sim_time:
    update_observe(dt)
    if len(p_list) == 0:
        break

print(time_to_escape)
print("mean time = ", np.mean(time_to_escape))
