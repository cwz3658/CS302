import numpy as np


class Wall:
    """
    the class for wall
    """

    def __init__(self, b, door_width):
        """
        b is the wall location, mathematically, it is x = b
        door_pos is the door position [(x1, y1), (x2, y2)]
        """
        self.b = b
        self.door_pos = np.array([(b, 15), (b, 15 + door_width)])
        self.door_middle_point = np.array([b, 15 + door_width / 2])
        self.door_width = door_width

