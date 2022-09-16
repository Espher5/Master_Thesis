import json
import numpy as np
import os

from algorithm.car_road import Map


class RoadGen:
    """
    Class for generating roads
    A Markov Chain is used to generate a sequence of road types.
    It allows to create a better initial population
    """

    def __init__(
        self,
        map_size,
        min_len,    # Minimal possible distance in meters
        max_len,    # Maximal possible distance to go straight in meters
        min_angle,  # Minimal angle of rotation in degrees
        max_angle,  # Maximal angle of rotation in degrees
    ):
        self._file = "roads.json"
        self._init_file = "init.json"
        self._points_file = "points.json"
        self._road_points = []
        self._init_states = ["straight", "left", "right"]
        self._states = []

        self._map_size = map_size
        self._min_len = min_len
        self._max_len = max_len
        self._min_angle = min_angle
        self._max_angle = max_angle
        self._step_ang = 5
        self._step_len = 1

        self._car_map = None
        self._init_a = []
        self._init_b = []

        self._transition_names = [
            ["SS", "SL", "SR"],
            ["LS", "LL", "LR"],
            ["RS", "RL", "RR"],
        ]

        # Probabilities of switching states
        self._transition_matrix = [
            [0.1, 0.45, 0.45],
            [0.2, 0.4, 0.4],
            [0.2, 0.4, 0.4],
        ]

        self._len_values = [
            i for i in range(self._min_len, self._max_len + 1, self._step_len)
        ]  # a list of distance to go forward
        self._ang_values = [
            i for i in range(self._min_angle, self._max_angle + 1, self._step_ang)
        ]  # a list of angles to turn

    def test_case_generate(self):
        """
        Function that produces a list with states and road points
        """
        self._road_points = []
        self._car_map = Map(self._map_size)
        self._init_a = [int(self._car_map.init_pos[0]), int(self._car_map.init_pos[1])]
        self._init_b = [int(self._car_map.init_end[0]), int(self._car_map.init_end[1])]

        self._road_points.append(
            tuple(
                (
                    (self._init_a[0] + self._init_b[0]) / 2,
                    (self._init_a[1] + self._init_b[1]) / 2,
                )
            )
        )

        state = np.random.choice(self._init_states)
        value = np.random.choice(self._len_values) if state == "straight" else np.random.choice(self._ang_values)

        if state == "straight":
            self._car_map.go_straight(value)
        elif state == "left":
            self._car_map.turn_left(value)
        else:
            self._car_map.turn_right(value)

        self._road_points.append(tuple((self._car_map.current_pos[0] + self._car_map.current_pos[1]) / 2))

        self._states = [[state, value]]

        flag = True
        while flag:
            if state == 'straight':
                change = np.random.choice(self._transition_names[0], p=self._transition_matrix[0])
            elif state == 'left':
                change = np.random.choice(self._transition_names[1], p=self._transition_matrix[1])
            else:
                change = np.random.choice(self._transition_names[2], p=self._transition_matrix[2])

            if change in ['SS', 'LS', 'RS']:
                value = np.random.choice(self._len_values)
                state = "straight"
                self._states.append([state, value])
                flag = self._car_map.go_straight(value)

            elif change in ['SL', 'LL', 'RL']:
                value = np.random.choice(self._ang_values)
                state = "left"
                self._states.append([state, value])
                flag = self._car_map.turn_left(value)

            elif change in ['SR', 'LR', 'RR']:
                value = np.random.choice(self._ang_values)
                state = "right"
                self._states.append([state, value])
                flag = self._car_map.turn_right(value)

            if not flag:
                return self._correct_maneuver()
            self._road_points.append(
                tuple((self._car_map.current_pos[0] + self._car_map.current_pos[1]) / 2)
            )

        del self._road_points[-1]  # Last point might be going over the border
        del self._states[-1]
        return self.states_to_dict()

    def _correct_maneuver(self):
        del self._road_points[-1]
        del self._states[-1]
        if len(self._road_points) <= 2:
            self._car_map.go_straight(1)
            self._road_points.append(tuple((self._car_map.current_pos[0] + self._car_map.current_pos[1]) / 2))
        return self.states_to_dict()

    def states_to_dict(self):
        """
        Transforms a list of test cases
        to a dictionary
        """
        test_cases = {}
        i = 0
        for element in self._states:
            test_cases["st" + str(i)] = {}
            test_cases["st" + str(i)]["state"] = element[0]
            test_cases["st" + str(i)]["value"] = int(element[1])
            i += 1

        return test_cases

    def write_states_to_file(self):
        """
        Writes the generated test case to file
        """
        if os.stat(self._file).st_size == 0:
            test_cases = {}
        else:
            with open(self._file) as file:
                test_cases = json.load(file)

        if os.stat(self._init_file).st_size == 0:
            positions = {}
        else:
            with open(self._init_file) as file:
                positions = json.load(file)

        if os.stat(self._points_file).st_size == 0:
            points = {}
        else:
            with open(self._points_file) as file:
                points = json.load(file)

        num = len(test_cases)

        tc = "tc" + str(num)
        test_cases[tc] = {}
        positions[tc] = {"a": self._init_a, "b": self._init_b}
        points[tc] = self._road_points

        i = 0
        for element in self._states:
            test_cases[tc]["st" + str(i)] = {}
            test_cases[tc]["st" + str(i)]["state"] = str(element[0])
            test_cases[tc]["st" + str(i)]["value"] = int(element[1])
            i += 1

        with open(self._file, "w") as outfile:
            json.dump(test_cases, outfile)

        with open(self._init_file, "w") as outfile:
            json.dump(positions, outfile)

        with open(self._points_file, "w") as outfile:
            json.dump(points, outfile)
