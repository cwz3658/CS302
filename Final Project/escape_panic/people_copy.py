import numpy as np
import scipy as sci
import matplotlib.pyplot as plt


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
    k = 120000
    kappa = 240000
    tau = 0.5  # characteristic time
    v_des = 0.8  # desired speed

    def __init__(self, vec_r, vec_v, r_i):
        """
        vec_r: position 2-vector
        vec_v: velocity 2-vector
        radius: radius of a people
        m: m is mass
        """
        self.vec_r = vec_r
        self.vec_v = vec_v
        self.r_i = r_i
        self.m = self.SD * (
            np.pi * r_i ** 2
        )  # here self.SD access to a class attribute

        # the following 2 attributes are for visualizing
        # default circle styles
        self.styles = {"edgecolor": "b", "fill": True}
        # create a circle representation of itself
        self.circle = plt.Circle(self.vec_r, self.r_i, **self.styles)

    def move(self, vec_Fi):
        self.vec_r += self.vec_v
        # update its circle representation
        self.circle.center = (self.vec_r[0], self.vec_r[1])

    def _F_from_self(self, vec_ei):
        """
        Compute the force from v_des
        ei: desired direction
        """
        vec_F_des = self.m * (self.v_des * vec_ei - self.vec_v) / self.tau
        return vec_F_des

    g = lambda x: np.max([0, x])  # this is a class attribute

    def F_from_other(self, other):
        """
        Compute the force from another people, i.e. f_ij
        other: another people
        """

        r_ij = self.r_i + other.r_i
        d_ij = sci.linalg.norm(self.vec_r - other.vec_r)
        vec_n_ij = (self.vec_r - other.vec_r) / d_ij
        vec_t_ij = np.array([-vec_n_ij[1], vec_n_ij[0]])
        delta_v_ji = np.dot(other.vec_v - self.vec_v, vec_t_ij)

        vec_F_ij = (
            self.A * np.exp(r_ij - d_ij) / self.B + self.k * self.g(r_ij - d_ij)
        ) * vec_n_ij + self.kappa * g(r_ij - d_ij) * delta_v_ji * vec_t_ij
        return vec_F_ij

    def F_from_wall(self, wall):
        """
        Compute force from wall
        """

        d_iW = sci.linalg.norm(wall.b - self.vec_r[0])  # this computes the distance
        vec_n_iW = (self.vec_r - np.array([wall.b, self.vec_r[1]])) / d_iW
        vec_t_iW = np.array([-vec_n_iW[1], vec_n_iW[0]])

        vec_F_iW = (
            (
                self.A * np.exp(self.r_i - d_iW) / self.B
                + self.k * self.g(self.r_i - d_iW)
            )
            * vec_n_iW
            - self.kappa
            * self.g(self.r_i - d_iW)
            * np.dot(self.vec_v, vec_t_iW)
            * vec_t_iW
        )

        return vec_F_iW

    # migh have problem
    def draw(self):
        """return its current circle representation"""
        return self.circle
