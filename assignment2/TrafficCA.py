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
        lane_num: int,
        L: int,
        num_cars: int,
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

    # a simple constructor
    @classmethod
    def random_create(cls, lane_num, L, num_cars, sim_time):
        # setup a simulation
        random.seed()
        rows = range(lane_num)
        cols = range(L)
        all_positions = list(itertools.product(rows, cols))

        cars_init_speed_vec = np.random.randint(0, 5, size=num_cars)
        cars_maxspeed_vec = np.random.randint(4, 7, size=num_cars)
        cars_initial_pos_vec = random.sample(all_positions, num_cars)
        prob_change_lane_vec = np.random.random(num_cars) * 0.5 + 0.5
        prob_decrease_speed_vec = np.random.random(num_cars) * 0.2

        t_ca = cls(
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

        return t_ca

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

    def sim_show(self):
        fig = plt.figure()
        artists = []
        for config in self.config_history:
            plot = plt.imshow(config)
            artists.append([plot])

        anima = ArtistAnimation(fig, artists, interval=200, repeat=False)
        plt.show(anima)

    def sim_get_traffic_flow(self):
        car_list = self.car_list

        # compute total speed during this simulation
        total_speed = 0
        for car in car_list:
            total_speed = total_speed + np.sum(car.speed_history)

        tf_flow = total_speed / (self.sim_time * self.lane_num * self.L)
        return tf_flow


def get_traffic_flow_distribution(
    lane_num, car_density, L=1000, sim_time=600, num_trials=10
):
    """
    sim_time is in seconds: sim_time = 600 means 10 min
    L unit is 10m: L = 1000 means 1000m 
    """
    # compute car num
    num_cars = round((lane_num * L) * car_density)
    # create a t_ca
    flows = []
    for _ in range(num_trials):
        t_ca = TrafficFlowCA.random_create(lane_num, L, num_cars, sim_time)
        t_ca.run_sim()
        flows.append(t_ca.sim_get_traffic_flow())
    return flows


lane_num_list = [2, 3, 5, 10]
car_density_list = [0.2, 0.5, 0.7]
fig, ax = plt.subplots()
x_pos = range(len(lane_num_list))

flow_data = []
for car_density, lane_num in itertools.product(car_density_list, lane_num_list):
    flows = get_traffic_flow_distribution(lane_num, car_density, num_trials=10)

    flow_data.append(flows)
    if len(flow_data) == len(lane_num_list):
        y_means = np.mean(flow_data, axis=1)  # compute mean along rows
        y_std = np.std(flow_data, axis=1)
        print("flow data is ", flow_data)
        print("y means ", y_means)
        print("y std", y_std)
        ax.errorbar(
            x_pos,
            y_means,
            yerr=y_std,
            capsize=10,
            label="Car Density = {}".format(car_density),
        )
        flow_data = []

ax.set_ylabel("flow")
ax.set_xticks(x_pos)
x_labels = ["{} lanes".format(lane) for lane in lane_num_list]
ax.set_xticklabels(x_labels)
ax.set_title("Result")
ax.yaxis.grid(True)
plt.legend()
plt.savefig("TrafficCA_statistics.png")
plt.show()
