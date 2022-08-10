import math
import numpy as np
import random
import time

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import matplotlib.pyplot as plt


class VectorMapper:
    """
    Class that conducts transformations to vectors automatically,
    using the commands "go straight", "turn left", "turn right".
    As a result it produces a set of points corresponding to a road
    """

    def __init__(self, map_size):
        self._map_size = map_size
        self._max_x = map_size
        self._max_y = map_size
        self._mix_x = 0
        self._mix_y = 0
        self._width = 10
        self._radius = 15

        self._init_pos, self._init_end = self._init_position()
        self._road_point = list()
        self._current_pos = [self._init_pos, self._init_end]
        self._pos_history = list(self._current_pos)

        self._choice = 0

    @property
    def current_pos(self):
        return self._current_pos

    @property
    def init_pos(self):
        return self._init_pos

    @property
    def init_end(self):
        return self._init_end

    def _init_position(self):
        """
        Select a random initial position from the middle of one of the boundaries
        :return: the position
        """
        choice = random.randint(0, 3)
        if choice == 0:
            pos = np.array((self._max_x / 2, 5))
            end = np.array((pos[0] + self._width, pos[1]))
        elif choice == 1:
            pos = np.array((self._max_y / 2 - self._width / 2, self._max_y / 2))
            end = np.array((self._max_y / 2 + self._width / 2, self._max_y / 2))
        elif choice == 2:
            pos = np.array((self._max_x / 2, self._max_y - 5))
            end = np.array((pos[0] + self._width, pos[1]))
        else:
            pos = np.array((self._max_x - 5, self._max_y / 2))
            end = np.array((pos[0], pos[1] + self._width))

        self._choice = choice

        return pos, end

    @staticmethod
    def position_to_line(position):
        x = [position[0][0], position[1][0], (position[0][0] + position[1][0]) / 2]
        y = [position[0][1], position[1][1], (position[0][1] + position[1][1]) / 2]
        return x, y

    def _position_to_center(self):
        x = (self._current_pos[0][0] + self._current_pos[1][0]) / 2
        y = (self._current_pos[0][1] + self._current_pos[1][1]) / 2
        self._road_point = [x, y]

    def _point_in_range(self, a):
        return 0 <= a[0] < (self._max_x - 4) and 0 <= a[1] < (self._max_y - 4)

    def _point_in_range_2(self, a):
        return ((0 + 4) < a[0] < (self._max_x - 4)) and ((0 + 4) < a[1] < (self._max_y - 4))

    def go_straight(self, distance):
        a = self._current_pos[0]
        b = self._current_pos[1]
        test_distance = 1

        if not self._point_in_range(a) or not self._point_in_range(b):
            return False

        p_a, p_b = self._get_points(a, b)
        u_v = (p_a - p_b) / np.linalg.norm(p_b - p_a)

        sector = self._choice
        if len(self._pos_history) < 2:
            if sector == 0 or sector == 3:
                r = np.array([[0, -1], [1, 0]])  # Anticlockwise
            else:
                r = np.array([[0, 1], [-1, 0]])  # Clockwise

            u_v_ = r.dot(u_v)
            p_a_ = p_a + u_v_ * distance
            p_b_ = p_b + u_v_ * distance

            self._current_pos = [p_a_, p_b_]
            self._pos_history.append(self._current_pos)
            return True
        else:
            r = np.array([[0, -1], [1, 0]])  # Anticlockwise
            u_v_ = r.dot(u_v)
            p_a_ = p_a + u_v_ * test_distance  # Make a small perturbation
            p_b_ = p_b + u_v_ * test_distance

            new_pos = [p_a_, p_b_]
            if self._in_polygon(new_pos):  # Check if it's in correct direction
                r = np.array([[0, 1], [-1, 0]])

                u_v = r.dot(u_v)

                p_a_ = p_a + u_v * distance
                p_b_ = p_b + u_v * distance

                self._current_pos = [p_a_, p_b_]
                self._pos_history.append(self._current_pos)
                return True
            else:
                p_a_ = p_a + u_v_ * distance
                p_b_ = p_b + u_v_ * distance
                self._current_pos = [p_a_, p_b_]
                self._pos_history.append(self._current_pos)
                return True

    def turn_right(self, angle):
        a = self._current_pos[0]
        b = self._current_pos[1]
        test_angle = 3

        if not self._point_in_range(a) or not self._point_in_range(b):
            print("Point not in range...")
            return False

        p_a, p_b = self._get_points(a, b)
        new_pos = self._clockwise_turn_top(test_angle, p_a, p_b)

        if self._in_polygon(new_pos):
            self._current_pos = self._clockwise_turn_bot(angle, p_a, p_b)
        else:
            self._current_pos = self._clockwise_turn_top(angle, p_a, p_b)
        self._pos_history.append(self._current_pos)
        return True

    def turn_left(self, angle):
        a = self._current_pos[0]
        b = self._current_pos[1]
        test_angle = 3

        if not self._point_in_range(a) or not self._point_in_range(b):
            print("Point not in range...")
            return False

        p_a, p_b = self._get_points(a, b)
        new_pos = self._anticlockwise_turn_top(test_angle, p_a, p_b)

        if self._in_polygon(new_pos):
            self._current_pos = self._anticlockwise_turn_bot(angle, p_a, p_b)
        else:
            self._current_pos = self._anticlockwise_turn_top(angle, p_a, p_b)
        self._pos_history.append(self._current_pos)
        return True

    def _clockwise_turn_top(self, angle, p_a, p_b):
        angle += 180
        radius = self._radius

        u_v = (p_a - p_b) / np.linalg.norm(p_a - p_b)
        o_o = p_a + u_v * radius

        o_b_norm = np.linalg.norm(o_o - p_b)
        o_a_norm = np.linalg.norm(o_o - p_a)

        o_b = (o_o - p_b) / o_b_norm
        o_a = (o_o - p_a) / o_a_norm
        r = np.array(
            [
                [np.cos(math.radians(angle)), np.sin(math.radians(angle))],
                [-np.sin(math.radians(angle)), np.cos(math.radians(angle))],
            ]
        )
        o_b_ = r.dot(o_b) * o_b_norm
        o_a_ = r.dot(o_a) * o_a_norm
        p_a_ = o_o + o_a_
        p_b_ = o_o + o_b_

        return [p_a_, p_b_]

    def _clockwise_turn_bot(self, angle, p_a, p_b):
        radius = self._radius
        u_v = (p_a - p_b) / np.linalg.norm(p_a - p_b)
        o_o = p_b - u_v * radius
        o_b_norm = np.linalg.norm(o_o - p_b)
        o_a_norm = np.linalg.norm(o_o - p_a)
        o_b = (p_b - o_o) / o_b_norm
        o_a = (p_a - o_o) / o_a_norm

        r = np.array(
            [
                [np.cos(math.radians(angle)), np.sin(math.radians(angle))],
                [-np.sin(math.radians(angle)), np.cos(math.radians(angle))],
            ]
        )

        o_b_ = r.dot(o_b) * o_b_norm
        o_a_ = r.dot(o_a) * o_a_norm
        p_a_ = o_o + o_a_
        p_b_ = o_o + o_b_

        return [p_a_, p_b_]

    def _anticlockwise_turn_top(self, angle, p_a, p_b):
        angle += 180
        radius = self._radius
        u_v = (p_a - p_b) / np.linalg.norm(p_a - p_b)
        o_o = p_a + u_v * radius

        o_b_norm = np.linalg.norm(o_o - p_b)

        o_a_norm = np.linalg.norm(o_o - p_a)

        o_b = (o_o - p_b) / o_b_norm
        o_a = (o_o - p_a) / o_a_norm

        r = np.array(
            [
                [np.cos(math.radians(angle)), -np.sin(math.radians(angle))],
                [np.sin(math.radians(angle)), np.cos(math.radians(angle))],
            ]
        )
        o_b_ = r.dot(o_b) * o_b_norm
        o_a_ = r.dot(o_a) * o_a_norm

        p_a_ = o_o + o_a_
        p_b_ = o_o + o_b_

        return [p_a_, p_b_]

    def _anticlockwise_turn_bot(self, angle, p_a, p_b):
        radius = self._radius
        u_v = (p_a - p_b) / np.linalg.norm(p_a - p_b)
        o_o = p_b - u_v * radius

        o_b_norm = np.linalg.norm(o_o - p_b)
        o_a_norm = np.linalg.norm(o_o - p_a)
        o_b = (p_b - o_o) / o_b_norm
        o_a = (p_a - o_o) / o_a_norm

        r = np.array(
            [
                [np.cos(math.radians(angle)), -np.sin(math.radians(angle))],
                [np.sin(math.radians(angle)), np.cos(math.radians(angle))],
            ]
        )
        o_b_ = r.dot(o_b) * o_b_norm
        o_a_ = r.dot(o_a) * o_a_norm

        p_a_ = o_o + o_a_
        p_b_ = o_o + o_b_

        return [p_a_, p_b_]

    @staticmethod
    def _get_points(a, b):
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

        return p_a, p_b

    def _in_polygon(self, new_position):
        """
        Checks whether a point lies within a polygon between current and previous vector
        :return: True if the polygon contains the point
        """

        if len(self._pos_history) <= 1:
            return True

        current_pos = self._pos_history[-1]
        prev_pos = self._pos_history[-2]
        new_pos_middle = (new_position[0] + new_position[1]) / 2

        point = Point(new_pos_middle[0], new_pos_middle[1])
        print(self._pos_history)
        polygon = Polygon(
            [tuple(current_pos[0]), tuple(current_pos[1]), tuple(prev_pos[0]), tuple(prev_pos[1])]
        )
        return polygon.contains(point)

    def _remove_invalid_cases(self, points, states):
        points = list(points)
        valid_points = list(points[0])
        new_states = dict()

        i = 1
        while i < len(points):
            if self._point_in_range_2(points[i]):
                valid_points.append(points[i])
                new_states.update(
                    {['st' + str(i - 1)]: states["st" + str(i - 1)]}
                )
            else:
                return new_states, valid_points
            i += 1

        return new_states, valid_points

    def get_points_from_states(self, states):
        self._init_pos, self._init_end = self._init_position()
        self._current_pos = [self._init_pos, self._init_end]
        self._pos_history = list(self._current_pos)
        self._position_to_center()

        points = list(self._road_point)
        test_case = states

        for state in test_case:
            action = test_case[state]['state']

            if action == 'straight':
                flag = self.go_straight(test_case[state]["value"])
            elif action == 'left':
                flag = self.turn_left(test_case[state]["value"])
            elif action == 'right':
                flag = self.turn_right(test_case[state]["value"])
            else:
                flag = False

            if flag:
                self._position_to_center()
                point = self._road_point
                points.append(point)

        return points

    def build_test_case(self, points):
        time_ = str(int(time.time()))

        fig, ax = plt.subplot(figsize=(12, 12))
        road_x = list()
        road_y = list()

        for p in points:
            road_x.append(p[0])
            road_y.append(p[1])

        top = self._map_size
        bottom = 0

        ax.plot(road_x, road_y, 'yo--', label='Road')
        ax.set_title('Test case fitness', fontsize=15)
        ax.set_xlim(bottom, top)
        ax.set_ylim(bottom, top)

        fig.savefig('.\\test\\' + time_ + '+test.jpg')
        ax.legend()
        plt.close(fig)


def read_schedule(test_case, size):
    time_ = str(int(time.time()))
    fig, ax1 = plt.subplots(figsize=(12, 12))
    vector_map = VectorMapper(size)

    for state in test_case:
        action = test_case[state]['state']
        print('location:', vector_map.current_pos)

        if action == 'straight':
            vector_map.go_straight(test_case[state]["value"])
        elif action == 'left':
            vector_map.turn_left(test_case[state]["value"])
        elif action == 'right':
            vector_map.turn_left(test_case[state]["value"])
        else:
            print('Unsupported action ', action)

        print(test_case[state]["value"])
        x, y = vector_map.position_to_line(vector_map.current_pos)
        ax1.plot(x, y, "o--y")

        top = size
        bottom = 0
        ax1.set_ylim(bottom, top)
        ax1.set_xlim(bottom, top)
        fig.savefig(".\\Test\\" + time_ + "+test2.jpg")
        plt.close(fig)


if __name__ == '__main__':
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
