from Car import Car
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation


class TrafficFlowCA:
    """
    This class will simulate Highway traffic.
    """

    def __init__(
        self,
        lane_num,
        L,
        num_cars,
        cars_init_speed_vec,
        cars_maxspeed_vec,
        cars_initial_pos_vec,
        prob_change_lane_vec,
        prob_decrease_speed_vec,
        sim_time,  # number of time step to simulate
    ):
        self.lane_num = lane_num
        self.L = L
        self.num_cars = num_cars

        self.sim_time = sim_time
        self.config_history = []

        self.car_list = []
        self.current_config = np.zeros((lane_num, L), dtype=int)
        # initilize current_config, cars
        for i in range(num_cars):
            self.current_config[cars_initial_pos_vec[i]] = 1
            self.car_list.append(
                Car(
                    cars_init_speed_vec[i],
                    cars_maxspeed_vec[i],
                    cars_initial_pos_vec[i],
                    prob_change_lane_vec[i],
                    prob_decrease_speed_vec[i],
                )
            )
        self.config_history.append(self.current_config)

    def run_sim(self):

        for _ in range(self.sim_time):
            next_config = np.zeros((self.lane_num, self.L), dtype=int)
            # update cars and config
            for j in range(self.num_cars):
                self.car_list[j].update_position_and_velocity(self.current_config)
                next_config[self.car_list[j].position] = 1
            # update current config and save config history
            self.current_config = next_config
            self.config_history.append(next_config)


lane_num = 3
L = 20
num_cars = 6
cars_init_speed_vec = num_cars * [1]
cars_maxspeed_vec = num_cars * [3]
cars_initial_pos_vec = [(0, 1), (1, 1), (0, 2), (1, 2), (0, 0), (1, 5)]
prob_change_lane_vec = num_cars * [0.5]
prob_decrease_speed_vec = num_cars * [0.2]
sim_time = 100

t_ca = TrafficFlowCA(
    lane_num,
    L,
    num_cars,
    cars_init_speed_vec,
    cars_maxspeed_vec,
    cars_initial_pos_vec,
    prob_change_lane_vec,
    prob_decrease_speed_vec,
    sim_time,
)

t_ca.run_sim()

fig = plt.figure()
pop = []
for config in t_ca.config_history:
    plot = plt.imshow(config)
    pop.append([plot])


anima = ArtistAnimation(fig, pop, interval=200)
plt.show()
