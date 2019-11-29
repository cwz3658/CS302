import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate
import scipy as sci
import pygame

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
    v_des = 4  # desired speed

    g = lambda x: np.max(
        [0, x]
    )  # this is a class attribute, a helper function to compute forces

    def __init__(self, vec_r, vec_v, r_i,screen):
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
        # self.thickness = 1
        # the following 2 attributes are for visualizing
        # default circle styles
        # self.styles = {"edgecolor": "b", "fill": True}
        # self.colour = (0, 0, 0)
        # create a circle representation of itself
        # self.circle=pygame.draw.circle(screen, self.colour, (np.int(self.vec_r[0]),np.int(self.vec_r[1])), np.int(self.r_i*100), self.thickness)


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
        # self.circle.center = (self.vec_r[0], self.vec_r[1])

    def _F_from_self(self, vec_ei):
        """
        Compute the force from v_des
        vec_ei: desired direction
        """
        vec_F_des = self.m * (self.v_des * vec_ei - self.vec_v) / self.tau
        return vec_F_des

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
            self.A * np.exp((r_ij - d_ij) / self.B) + self.k * People.g(r_ij - d_ij)
        ) * vec_n_ij + self.kappa * People.g(r_ij - d_ij) * delta_v_ji * vec_t_ij
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

    # def draw(self):
        # """return its current circle representation"""
        # return self.circle
        
    def draw(self,screen):
        self.thickness = 1
        self.colour = (0, 0, 0)
        dpi=20 # set resolution
        pygame.draw.circle(screen, self.colour, (np.int(self.vec_r[0]*dpi),np.int(self.vec_r[1]*dpi)), np.int(self.r_i*dpi), self.thickness)