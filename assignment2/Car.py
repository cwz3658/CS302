import numpy as np


class Car:
    def __init__(
        self, speed, max_speed, position, prob_change_lane, prob_decrease_speed
    ):
        self.speed = speed
        self.max_speed = max_speed
        self.position = position  # represent by a tupple
        self.speed_history = [self.speed]
        self.prob_change_lane = prob_change_lane
        self.prob_decrease_speed = prob_decrease_speed
        self.l = self.speed + 1
        self.l_o = self.l
        self.l_o_back = self.max_speed

    def __in_middle_lane__(self, current_config):
        """
        check whether this car is in middle lane or not
        returns true if it is in middle lane
        """
        row_num = current_config.shape[0]
        return 0 < self.position[0] < row_num - 1

    def __is_car_in_up_far_lane__(self, current_config):
        """
        return True if there is a car in up far lane
        """
        pos_up = (self.position[0] - 2, self.position[1])
        row_num = current_config.shape[0]
        return 0 <= pos_up[0] < row_num and current_config[pos_up] == 1

    def __is_car_in_down_far_lane__(self, current_config):
        """
        return True if there is a car in down far lane
        """
        pos_down = (self.position[0] + 2, self.position[1])
        row_num = current_config.shape[0]
        return 0 <= pos_down[0] < row_num and current_config[pos_down] == 1

    def __compute_gaps__(self, current_config):
        # compute gap in my lane f: forward, b: backward
        col_num = current_config.shape[1]
        row_num = current_config.shape[0]

        row_idx = self.position[0]
        col_idx = (self.position[1] + 1) % col_num
        count = 0
        while current_config[(row_idx, col_idx)] == 0:
            count += 1
            col_idx = (col_idx + 1) % col_num
            if count >= col_num:
                break
        gap_in_mylane_f = count

        # compute gaps in its up lane and down lane (wrapped)
        row_idx = (self.position[0] - 1) % row_num  # uplane
        col_idx = (self.position[1] + 1) % col_num  # forward
        count = 0
        while current_config[(row_idx, col_idx)] == 0:
            count += 1
            if count >= col_num:
                break
            col_idx = (col_idx + 1) % col_num
        gap_in_uplane_f = count

        row_idx = (self.position[0] - 1) % row_num  # uplane
        col_idx = (self.position[1] - 1) % col_num  # backward
        count = 0
        while current_config[(row_idx, col_idx)] == 0:
            count += 1
            col_idx = (col_idx - 1) % col_num
            if count >= col_num:
                break
        gap_in_uplane_b = count

        # compute gap in downlane
        row_idx = (self.position[0] + 1) % row_num  # downlane
        col_idx = (self.position[1] + 1) % col_num  # forward
        count = 0
        while current_config[(row_idx, col_idx)] == 0:
            count += 1
            col_idx = (col_idx + 1) % col_num
            if count >= col_num:
                break
        gap_in_downlane_f = count

        row_idx = (self.position[0] + 1) % row_num  # downlane
        col_idx = (self.position[1] - 1) % col_num  # backward
        count = 0
        while current_config[(row_idx, col_idx)] == 0:
            count += 1
            col_idx = (col_idx - 1) % col_num
            if count >= col_num:
                break
        gap_in_downlane_b = count

        return (
            gap_in_mylane_f,
            gap_in_uplane_f,
            gap_in_uplane_b,
            gap_in_downlane_f,
            gap_in_downlane_b,
        )

    def __is_good_change_uplane_condition__(self, current_config):
        gap_in_mylane_f, gap_in_uplane_f, gap_in_uplane_b, _, _ = self.__compute_gaps__(
            current_config
        )
        return (
            gap_in_mylane_f < self.l
            and gap_in_uplane_f > self.l_o
            and gap_in_uplane_b > self.l_o_back
            and (not self.__is_car_in_up_far_lane__(current_config))
        )

    def __is_good_change_downlane_condition__(self, current_config):
        gap_in_mylane_f, _, _, gap_in_downlane_f, gap_in_downlane_b = self.__compute_gaps__(
            current_config
        )
        return (
            gap_in_mylane_f < self.l
            and gap_in_downlane_f > self.l_o
            and gap_in_downlane_b > self.l_o_back
            and (not self.__is_car_in_down_far_lane__(current_config))
        )

    def __change_lane__(self, current_config):
        """
        update position after change lane
        """
        if self.__in_middle_lane__(current_config):
            # try to change to uplane
            if (
                self.__is_good_change_uplane_condition__(current_config)
                and np.random.uniform() < self.prob_change_lane
            ):
                # update new position
                self.position = (self.position[0] - 1, self.position[1])
                return
            # try to change to downlane
            if (
                self.__is_good_change_downlane_condition__(current_config)
                and np.random.uniform() < self.prob_change_lane
            ):
                # update new position
                self.position = (self.position[0] + 1, self.position[1])
                return

        elif self.position[0] == 0:  # in upper lane
            if (
                self.__is_good_change_downlane_condition__(current_config)
                and np.random.uniform() < self.prob_change_lane
            ):
                self.position = (self.position[0] + 1, self.position[1])
                return
        else:  # in the down lane
            if (
                self.__is_good_change_uplane_condition__(current_config)
                and np.random.uniform() < self.prob_change_lane
            ):
                self.position = (self.position[0] - 1, self.position[1])
                return

    def __update_speed__(self, current_config):
        gap_in_mylane_f, _, _, _, _ = self.__compute_gaps__(current_config)

        if self.speed <= self.max_speed:
            self.speed = self.speed + 1
        if self.speed > gap_in_mylane_f:
            self.speed = gap_in_mylane_f
        if self.speed > 0 and np.random.uniform() < self.prob_decrease_speed:
            self.speed = self.speed - 1

        # save speed history
        self.speed_history.append(self.speed)
        # update parameters
        self.l = self.speed + 1
        self.l_o = self.l

    def __update_position__(self, current_config):
        col_num = current_config.shape[1]
        self.position = (self.position[0], (self.position[1] + self.speed) % col_num)

    def update_position_and_velocity(self, current_config):
        self.__change_lane__(current_config)  # decide whether change lane or not
        self.__update_speed__(current_config)  # update speed
        self.__update_position__(current_config)  # update position


def test_car():
    # test __in_middle_lane__()
    car = Car(1, 5, (2, 1), 0.5, 0.3)
    current_config = np.array(
        [[1, 0, 0, 0, 0], [1, 0, 0, 1, 0], [0, 1, 0, 0, 1], [0, 0, 0, 1, 0]]
    )
    print(car.__in_middle_lane__(current_config))

    # test __is_car_in_up_far_lane__, __is_car_in_down_far_lane__
    print(car.__is_car_in_down_far_lane__(current_config))
    print(car.__is_car_in_up_far_lane__(current_config))

    # test __compute_gaps__
    print(car.__compute_gaps__(current_config))

    # test __is_good_change_downlane_condition__
    current_config = np.zeros((4, 5))
    current_config[(2, 1)] = 1
    print(car.__is_good_change_downlane_condition__(current_config))
    car.update_position_and_velocity(current_config)
    print("new pos", car.position)
    print("new speed", car.speed)
    print("speed history", car.speed_history)


# test_car()
