from Car import Car
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.animation import ArtistAnimation
import itertools
import random


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


def sim_driver_show(lane_num, L, num_cars, sim_time):
    """
    display a simulation
    """
    # setup a simulation
    rows = range(lane_num)
    cols = range(L)
    all_positions = list(itertools.product(rows, cols))

    cars_init_speed_vec = np.random.randint(0, 3, size=num_cars)
    cars_maxspeed_vec = np.random.randint(3, 6, size=num_cars)
    cars_initial_pos_vec = random.sample(all_positions, num_cars)
    prob_change_lane_vec = np.random.random(num_cars)
    prob_decrease_speed_vec = np.random.random(num_cars)

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
    artists = []
    for config in t_ca.config_history:
        plot = plt.imshow(config, aspect="auto")
        artists.append([plot])

    anima = ArtistAnimation(fig, artists, interval=300, repeat=False)
    plt.show()


def get_traffic_flow(t_ca, lane_num, L, sim_time):
    car_list = t_ca.car_list

    # compute total speed during this simulation
    total_speed = 0
    for car in car_list:
        total_speed = total_speed + np.sum(car.speed_history)

    tf_flow = total_speed / (sim_time * lane_num * L)
    return tf_flow


def sim_driver_traffic_flow(lane_num, L, num_cars, sim_time):
    """
    return the traffic flow for this simulation
    """
    # setup a simulation
    rows = range(lane_num)
    cols = range(L)
    all_positions = list(itertools.product(rows, cols))

    cars_init_speed_vec = np.random.randint(0, 3, size=num_cars)
    cars_maxspeed_vec = np.random.randint(3, 6, size=num_cars)
    cars_initial_pos_vec = random.sample(all_positions, num_cars)
    prob_change_lane_vec = np.random.random(num_cars)
    prob_decrease_speed_vec = np.random.random(num_cars)

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

    return get_traffic_flow(t_ca, lane_num, L, sim_time)


# print(sim_driver_traffic_flow(3, 50, 150, 100))

sim_driver_show(10, 400, 1000, 100)
