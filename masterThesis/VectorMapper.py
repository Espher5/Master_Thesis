import random
import numpy as np
import math
import time

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import matplotlib.pyplot as plt

"""
Class that conducts transformations to vectors automatically 
and produces a set of points corresponding to a road
"""
class VectorMapper:
    def __init__(self, map_size):
        self._map_size = map_size
        self._width = 10
        self._max_x = map_size
        self._max_y = map_size
        self._radius = 25

        self._init_pos, self._init_end = self._init_position()
        self._current_pos = [self._init_pos, self._init_end]
        self._all_positions = [self._current_pos]

        self._option = None
        self._road_point = None

    # Randomly selects an initial position from the middle of one of the boundaries
    def _init_position(self):
        option = random.randint(0, 3)
        self._option = option

        if option == 0:
            pos = np.array((self._max_x / 2, 5))
            end = np.array((pos[0] + self._width, pos[1]))
        elif option == 1:
            pos = np.array((self._max_y / 2 - self._width / 2, self._max_y / 2))
            end = np.array((self._max_y / 2 + self._width / 2, self._max_y / 2))
        elif option == 2:
            pos = np.array((self._max_x / 2, self._max_y - 5))
            end = np.array((pos[0] + self._width, pos[1]))
        else:
            pos = np.array((self._max_x - 5, self._max_y / 2))
            end = np.array((pos[0], pos[1] + self._width))

        return pos, end

    @staticmethod
    def position_to_line(position):
        x = [position[0][0], position[1][0], (position[0][0] + position[1][0]) / 2]
        y = [position[0][1], position[1][1], (position[0][1] + position[1][1]) / 2]
        return x, y

    def position_to_center(self):
        x = (self._current_pos[0][0] + self._current_pos[1][0]) / 2
        y = (self._current_pos[0][1] + self._current_pos[1][1]) / 2
        self._road_point = [x, y]

    # Check if the point is in the acceptable range
    def _point_in_range(self, point):
        return 0 <= point[0] < (self._max_x - 4) and 0 <= point[1] < (self._max_y - 4)

    def _point_in_range_2(self, point):
        """check if point is in the acceptable range"""
        return ((0 + 4) < point[0] < (self._max_x - 4)) and ((0 + 4) < point[1] < (self._max_y - 4))


    def go_straight(self, distance):
        a = self._current_pos[0]
        b = self._current_pos[1]
        test_distance = 1

        if not self._point_in_range(a) or not self._point_in_range(b):
            return False

        if (b - a)[1] > 0:
            p_a = b
            p_b = a
        elif (b - a)[1] < 0:
            p_a = a
            p_b = b
        else:
            if (b - a)[0] > 0:
                p_a = b
                p_b = a
            else:
                p_a = a
                p_b = b

        u_v = (p_a - p_b) / np.linalg.norm(p_b - p_a)
        sector = self._option

        if len(self._all_positions) < 2:
            if sector == 0:
                R = np.array([[0, -1], [1, 0]])  # Anticlockwise
            elif sector == 1:
                R = np.array([[0, 1], [-1, 0]])  # Clockwise
            elif sector == 2:
                R = np.array([[0, 1], [-1, 0]])
            else:
                R = np.array([[0, -1], [1, 0]])

            u_v_ = R.dot(u_v)
            p_a_ = p_a + u_v_ * distance
            p_b_ = p_b + u_v_ * distance

            self._current_pos = [p_a_, p_b_]
            self._all_positions.append(self._current_pos)
            return True
        else:
            R = np.array([[0, -1], [1, 0]])
            u_v_ = R.dot(u_v)
            p_a_ = p_a + u_v_ * test_distance  # Make a small perturbation
            p_b_ = p_b + u_v_ * test_distance
            new_pos = [p_a_, p_b_]

            if self._in_polygon(new_pos):
                R = np.array([[0, 1], [-1, 0]])
                u_v = R.dot(u_v)
                p_a_ = p_a + u_v * distance
                p_b_ = p_b + u_v * distance
                self._current_pos = [p_a_, p_b_]
                self._all_positions.append(self._current_pos)
                return True
            else:
                p_a_ = p_a + u_v_ * distance
                p_b_ = p_b + u_v_ * distance
                self._current_pos = [p_a_, p_b_]
                self._all_positions.append(self._current_pos)
                return True

    def turn_left(self, angle):
        pass

    def turn_right(self, angle):
        a = self._current_pos[0]
        b = self._current_pos[1]
        test_angle = 3

        if not self._point_in_range(a) == 0 or not self._point_in_range(b):
            return False

        if (b - a)[1] > 0:
            p_a = b
            p_b = a
        elif (b - a)[1] < 0:
            p_a = a
            p_b = b
        elif (b - a)[1] == 0:
            if (b - a)[0] > 0:
                p_a = b
                p_b = a
            else:
                p_a = a
                p_b = b

        new_pos = self._clockwise_turn_top(test_angle, p_a, p_b)

        if self._in_polygon(new_pos):
            self._current_pos = self._clockwise_turn_bot(angle, p_a, p_b)
        else:
            self._current_pos = self._clockwise_turn_top(angle, p_a, p_b)

        self._all_positions.append(self._current_pos)
        return True

    # Refactor me please
    def _clockwise_turn_top(self, angle, p_a, p_b):
        angle += 180
        radius = self._radius

        u_v = (p_a - p_b) / np.linalg.norm(p_a - p_b)
        o_o = p_a + u_v * radius

        o_b_norm = np.linalg.norm(o_o - p_b)

        o_a_norm = np.linalg.norm(o_o - p_a)

        o_b = (o_o - p_b) / o_b_norm
        o_a = (o_o - p_a) / o_a_norm

        R = np.array(
            [
                [np.cos(math.radians(angle)), np.sin(math.radians(angle))],
                [-np.sin(math.radians(angle)), np.cos(math.radians(angle))],
            ]
        )
        o_b_ = R.dot(o_b) * o_b_norm
        o_a_ = R.dot(o_a) * o_a_norm

        p_a_ = o_o + o_a_
        p_b_ = o_o + o_b_

        return [p_a_, p_b_]

    # Refactor me please
    def _clockwise_turn_bot(self, angle, p_a, p_b):
        radius = self._radius
        u_v = (p_a - p_b) / np.linalg.norm(p_a - p_b)
        o_o = p_b - u_v * radius
        o_b_norm = np.linalg.norm(o_o - p_b)
        o_a_norm = np.linalg.norm(o_o - p_a)
        o_b = (p_b - o_o) / o_b_norm
        o_a = (p_a - o_o) / o_a_norm

        R = np.array(
            [
                [np.cos(math.radians(angle)), np.sin(math.radians(angle))],
                [-np.sin(math.radians(angle)), np.cos(math.radians(angle))],
            ]
        )

        o_b_ = R.dot(o_b) * o_b_norm
        o_a_ = R.dot(o_a) * o_a_norm
        p_a_ = o_o + o_a_
        p_b_ = o_o + o_b_

        return [p_a_, p_b_]

    # Refactor me please
    def _anticlockwise_turn_top(self, angle, p_a, p_b):
        angle += 180
        radius = self._radius
        u_v = (p_a - p_b) / np.linalg.norm(p_a - p_b)
        o_o = p_a + u_v * radius

        o_b_norm = np.linalg.norm(o_o - p_b)

        o_a_norm = np.linalg.norm(o_o - p_a)

        o_b = (o_o - p_b) / o_b_norm
        o_a = (o_o - p_a) / o_a_norm

        R = np.array(
            [
                [np.cos(math.radians(angle)), -np.sin(math.radians(angle))],
                [np.sin(math.radians(angle)), np.cos(math.radians(angle))],
            ]
        )
        o_b_ = R.dot(o_b) * o_b_norm
        o_a_ = R.dot(o_a) * o_a_norm

        p_a_ = o_o + o_a_
        p_b_ = o_o + o_b_

        return [p_a_, p_b_]

    # Refactor me please
    def _anticlockwise_turn_bot(self, angle, p_a, p_b):
        radius = self._radius
        u_v = (p_a - p_b) / np.linalg.norm(p_a - p_b)
        o_o = p_b - u_v * radius

        o_b_norm = np.linalg.norm(o_o - p_b)
        o_a_norm = np.linalg.norm(o_o - p_a)
        o_b = (p_b - o_o) / o_b_norm
        o_a = (p_a - o_o) / o_a_norm

        R = np.array(
            [
                [np.cos(math.radians(angle)), -np.sin(math.radians(angle))],
                [np.sin(math.radians(angle)), np.cos(math.radians(angle))],
            ]
        )
        o_b_ = R.dot(o_b) * o_b_norm
        o_a_ = R.dot(o_a) * o_a_norm

        p_a_ = o_o + o_a_
        p_b_ = o_o + o_b_

        return [p_a_, p_b_]

    def _in_polygon(self, new_position):
        if len(self._all_positions) <= 1:
            return True

        current = self._all_positions[-1]
        prev = self._all_positions[-2]
        new = new_position
        new_mid = (new[0] + new[1]) / 2

        point = Point(new_mid[0], new_mid[1])
        polygon = Polygon(
            [tuple(current[0]), tuple(current[1]), tuple(prev[0]), tuple(prev[1])]
        )
        return polygon.contains(point)

    def remove_invalid_cases(self, points, states):
        points = list(points)
        new_list = [points[0]]
        new_states = {}

        i = 1
        while i < len(points):
            if self._point_in_range_2(points[i]):
                new_list.append(points[i])
                new_states["st" + str(i - 1)] = states["st" + str(i - 1)]
            else:
                return new_states, new_list
            i += 1

        return new_states, new_list

    def get_points_from_states(self, states):
        self._init_pos, self._init_end = self._init_position()
        self._current_pos = [self._init_pos, self._init_end]
        self._all_positions = [self._current_pos]

        self.position_to_center()
        points = [self._road_point]
        tc = states

        # Refactor me please
        for state in tc:
            action = tc[state]["state"]
            if action == "straight":
                if self.go_straight(tc[state]["value"]):
                    self.position_to_center()
                    point = self._road_point
                    points.append(point)
            elif action == "left":
                if self.turn_left(tc[state]["value"]):
                    self.position_to_center()
                    point = self._road_point
                    points.append(point)
            elif action == "right":
                if self.turn_right(tc[state]["value"]):
                    self.position_to_center()
                    point = self._road_point
                    points.append(point)
            else:
                print("ERROR")

        return points

    def build_test_case(self, points):
        time_ = str(int(time.time()))

        fig, ax = plt.subplots(figsize=(12, 12))
        road_x = []
        road_y = []
        for p in points:
            road_x.append(p[0])
            road_y.append(p[1])

        ax.plot(road_x, road_y, "yo--", label="Road")

        top = self._map_size
        bottom = 0

        ax.set_title("Test case fitness ", fontsize=17)
        ax.set_ylim(bottom, top)
        ax.set_xlim(bottom, top)
        fig.savefig(".\\Test\\" + time_ + "+test.jpg")
        ax.legend()
        plt.close(fig)


def read_schedule(tc, size):
    time_ = str(int(time.time()))
    fig, ax1 = plt.subplots(figsize=(12, 12))
    car_map = VectorMapper(size)
    for state in tc:
        action = tc[state]["state"]
        print("location:", car_map._current_pos)
        if action == "straight":
            car_map.go_straight(tc[state]["value"])
            print(tc[state]["value"])
            x, y = car_map.position_to_line(car_map._current_pos)
            ax1.plot(x, y, "o--y")
        elif action == "left":
            car_map.turn_left(tc[state]["value"])
            print(tc[state]["value"])
            x, y = car_map.position_to_line(car_map._current_pos)
            ax1.plot(x, y, "o--y")
        elif action == "right":
            car_map.turn_right(tc[state]["value"])
            print(tc[state]["value"])
            x, y = car_map.position_to_line(car_map._current_pos)
            ax1.plot(x, y, "o--y")
        else:
            print("Wrong value")

    top = size
    bottom = 0
    ax1.set_ylim(bottom, top)
    ax1.set_xlim(bottom, top)
    # plt.yticks(np.arange(bottom, top + 1, 1.0), fontsize=12)
    # plt.grid(b=True, which="major", axis="both")

    # ax1.legend(fontsize=14)
    fig.savefig(".\\Test\\" + time_ + "+test2.jpg")
    plt.close(fig)

if __name__ == "__main__":
    # fig, ax1 = plt.subplots(figsize=(12, 12))
    """
    with open("roads.json") as file:
        test_cases = json.load(file)

    with open("init.json") as file:
        positions = json.load(file)
    case = "tc2"
    read_schedule(test_cases[case], 250, np.array(positions[case]["a"]), np.array(positions[case]["b"]))
    """
    cases = {
        "st0": {"state": "right", "value": 65},
        "st1": {"state": "straight", "value": 10},
        "st2": {"state": "left", "value": 20},
        "st3": {"state": "right", "value": 70},
    }
    my_map = VectorMapper(200)
    points = my_map.get_points_from_states(cases)
    my_map.build_test_case(points)
    read_schedule(cases, 200)