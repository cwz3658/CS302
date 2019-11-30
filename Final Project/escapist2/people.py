import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate
import scipy as sci
from scipy.linalg import norm
import random


class People:
    """
    This class defines the people in the room.
    """

    # define class attributes
    # Parameters
    SD = 350  # surface density is defined to be 350 kg/m^2

    # parameters in computing forces
    A = 2000
    B = 0.08
    k = 1.2e5
    kappa = 2.4e5
    tau = 0.5  # characteristic time
    v_des = 2  # desired speed

    g = lambda x: np.max(
        [0, x]
    )  # this is a class attribute, a helper function to compute forces

    def __init__(self, vec_r, vec_v, vec_ei, r_i, p_i=0.4, Rv=5):
        """
        all vectors are assumed to be np.array(...)
        vec_r: position 2-vector
        vec_v: velocity 2-vector
        vec_ei: desired ei, i.e. desired unit vector in whcih the people want to move
        r_i: radius of a people
        p_i: degree of panic, a probability 
        Rv: vision range of the people, default to 5 m
        m: m is mass
        """
        self.vec_r = vec_r
        self.vec_v = vec_v
        self.r_i = r_i
        self.vec_ei = vec_ei
        self.p_i = p_i
        self.Rv = Rv

        self.m = self.SD * (
            np.pi * r_i ** 2
        )  # here self.SD access to a class attribute

        # the following 2 attributes are for visualizing
        # default circle styles
        self.styles = {"edgecolor": "b", "fill": True}
        # create a circle representation of itself
        self.circle = plt.Circle(self.vec_r, self.r_i, **self.styles)

    # define a class attribute
    def dydt(self, y, t0, vec_Fi, vec_Vi):
        """
        vec_Fi is the forece 
        vec_Vi is its current speed
        here y = [vec_Vi_x, vec_Vi_y, vec_ri_x, vec_ri_y]
        """
        y_dot = np.array([vec_Fi[0] / self.m, vec_Fi[1] / self.m, vec_Vi[0], vec_Vi[1]])
        return y_dot

    def move(self, vec_Fi, dt):
        """
        dt is the time step in seconds
        """
        y0 = np.array([self.vec_v[0], self.vec_v[1], self.vec_r[0], self.vec_r[1]])
        time_span = np.array([0, dt])
        solution = sci.integrate.odeint(
            self.dydt, y0, time_span, args=(vec_Fi, self.vec_v)
        )

        # update states
        self.vec_v = solution[1, 0:2]
        self.vec_r = solution[1, 2:4]
        # update its circle representation
        self.circle.center = (self.vec_r[0], self.vec_r[1])

    def _F_from_self(self):
        """
        Compute the force from v_des
        vec_ei: desired direction
        """
        vec_F_des = self.m * (self.v_des * self.vec_ei - self.vec_v) / self.tau
        return vec_F_des

    def F_from_other(self, other):
        """
        Compute the force from another people, i.e. f_ij
        other: another people
        """

        r_ij = self.r_i + other.r_i
        d_ij = norm(self.vec_r - other.vec_r)
        vec_n_ij = (self.vec_r - other.vec_r) / d_ij
        vec_t_ij = np.array([-vec_n_ij[1], vec_n_ij[0]])
        delta_v_ji = np.dot(other.vec_v - self.vec_v, vec_t_ij)

        vec_F_ij = (
            self.A * np.exp((r_ij - d_ij) / self.B) + self.k * People.g(r_ij - d_ij)
        ) * vec_n_ij + self.kappa * People.g(r_ij - d_ij) * delta_v_ji * vec_t_ij
        return vec_F_ij

    def F_from_wall(self, wall):
        """
        Compute force from wall
        """

        d_iW = norm(wall.b - self.vec_r[0])  # this computes the distance
        vec_n_iW = (self.vec_r - np.array([wall.b, self.vec_r[1]])) / d_iW
        vec_t_iW = np.array([-vec_n_iW[1], vec_n_iW[0]])

        vec_F_iW = (
            (
                self.A * np.exp((self.r_i - d_iW) / self.B)
                + self.k * People.g(self.r_i - d_iW)
            )
            * vec_n_iW
            - self.kappa
            * People.g(self.r_i - d_iW)
            * np.dot(self.vec_v, vec_t_iW)
            * vec_t_iW
        )

        return vec_F_iW

    # migh have problem
    def draw(self):
        """return its current circle representation"""
        return self.circle

    def get_pos(self):
        """
        return the position of this people
        """
        return self.vec_r

    def look_around(self, all_people_list):
        """
        all_people_list: a list of all the people in the room 
        returns people_nearby: a list of people in the area of a circle centered at this people with radius Rv
        """
        people_nearby = []
        for p in all_people_list:
            if p is not self:
                dist = norm(self.vec_r - p.vec_r)
                if dist < self.Rv:
                    people_nearby.append(p)
        return people_nearby

    def determine_ei(self, all_people_list, door_pos, room_width, room_length):
        """
        Implement eq(4) of Nature Paper
        door_pos is assumed to be the middle point of the door, should be a 2-d np array
        
        """
        # if this people is near the door, its desired direction ei is set to the door
        dist_to_door = norm(door_pos - self.vec_r)
        if dist_to_door < self.Rv:  # distance to door less than vision range
            self.vec_ei = (door_pos - self.vec_r) / dist_to_door
            return

        # if the people can not see the door, follow people
        people_nearby = self.look_around(all_people_list)
        if len(people_nearby) != 0:
            # compute average ei, i.e. <ei>
            print("I am following")
            ei_list = [p.vec_ei for p in people_nearby]
            avg_ei = np.mean(ei_list, axis=0)
            new_direction = (1 - self.p_i) * self.vec_ei + self.p_i * avg_ei
            new_ei = new_direction / norm(new_direction)
            self.vec_ei = new_ei  # update its vec_ei
            return

        # if people can not see the door and can not see other people and see a wall, do the following
        # compute direction options
        lower_left = np.array([-1, -1]) / norm([-1, -1])
        lower_right = np.array([1, -1]) / norm([1, -1])
        up_left = np.array([-1, 1]) / norm([-1, 1])
        up_right = np.array([1, 1]) / norm([1, 1])

        dist_to_up_wall = room_length - self.vec_r[1]
        if dist_to_up_wall <= self.Rv:  # sees the upwall
            self.vec_ei = random.choice([lower_left, lower_right])
            print("sees up wall")
            return

        dist_to_down_wall = self.vec_r[1]
        if dist_to_down_wall <= self.Rv:
            self.vec_ei = random.choice([up_left, up_right])
            print("sees down wall")
            return

        dist_to_left_wall = self.vec_r[0]
        if dist_to_left_wall <= self.Rv:
            self.vec_ei = random.choice([lower_right, up_right])
            print("sees left wall")
            return

        dist_to_right_wall = room_width - self.vec_r[0]
        if dist_to_right_wall <= self.Rv:
            self.vec_ei = random.choice([lower_left, up_left])
            print("sees right wall")
            return

