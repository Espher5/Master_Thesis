import os
import json
import numpy as np

from car_road import Map


class RoadGenerator:
    """
    Class for generating roads from points
    """

    def __init__(self, map_size, min_len, max_len, min_angle, max_angle):
        self._file = 'json/roads.json'
        self._init_file = 'json/init.json'
        self._points_file = 'json/points.json'
        self._road_points = []
        self._init_states = ['straight', 'left', 'right']
        self._states = []

        self._vector_mapper = None
        self._init_a = None
        self._init_b = None

        self._map_size = map_size

        self._min_len = min_len
        self._max_len = max_len
        self._step_len = 1
        self._length_values = [
            i for i in range(self._min_len, self._max_len + 1, self._step_len)
        ]

        self._min_angle = min_angle
        self._max_angle = max_angle
        self._step_angle = 5
        self._angle_values = [
            i for i in range(self._min_angle, self._max_angle + 1, self._step_angle)
        ]

        self._transition_names = [
            ['SS', 'SL', 'SR'],
            ['LS', 'LL', 'LR'],
            ['RS', 'RL', 'RR']
        ]

        self._transition_probs = [
            [0.1, 0.45, 0.45],
            [0.2, 0.4, 0.4],
            [0.2, 0.4, 0.4]
        ]

    def generate_test_case(self):
        self._road_points = []
        self._init_states = ['straight', 'left', 'right']
        self._vector_mapper = Map(self._map_size)
        self._init_a = [int(self._vector_mapper.init_pos[0]), int(self._vector_mapper.init_pos[1])]
        self._init_b = [int(self._vector_mapper.init_end[0]), int(self._vector_mapper.init_end[1])]

        self._road_points.append(
            tuple(
                (
                    (self._init_a[0] + self._init_b[0]) / 2,
                    (self._init_a[1] + self._init_b[1]) / 2
                )
            )
        )

        self._vector_mapper.go_straight(5)
        self._road_points.append(
            tuple(
                (self._vector_mapper.current_pos[0] + self._vector_mapper.current_pos[1] / 2)
            )
        )

        # Go straight initially
        self._states.append(['straight', 5])
        state = 'straight'
        flag = True

        while flag:
            # Choose next state according to current state and transition table
            index = self._init_states.index(state)
            new_state = np.random.choice(
                self._transition_names[index], p=self._transition_probs[index]
            )

            if new_state in ['SS', 'LS', 'RS']:
                state = 'straight'
                value = np.random.choice(self._length_values)
                flag = self._vector_mapper.go_straight(value)
            else:
                value = np.random.choice(self._angle_values)
                if new_state in ['SL', 'LL', 'RL']:
                    state = 'left'
                    flag = self._vector_mapper.turn_left(value)
                else:
                    state = 'right'
                    flag = self._vector_mapper.turn_right(value)

            # Checks for maneuver outcome and updates state list and road points
            self._states.append([state, value])
            if not flag:
                self._correct_maneuver()
            self._road_points.append(tuple(
                (self._vector_mapper.current_pos[0] + self._vector_mapper.current_pos[1]) / 2)
            )

            # Last point may go over the boundary
            del self._road_points[-1]
            del self._states[-1]
            return self._states_to_dict()

    # Deals with movement failure
    def _correct_maneuver(self):
        del self._road_points[-1]
        del self._states[-1]
        if len(self._road_points) <= 2:
            self._vector_mapper.go_straight(1)
            self._road_points.append(
                tuple(
                    (self._vector_mapper.current_pos[0] + self._vector_mapper.current_pos[1]) / 2
                )
            )
        return self._states_to_dict()

    def _states_to_dict(self):
        test_cases = dict()
        i = 0

        for element in self._states:
            test_cases["st" + str(i)] = {}
            test_cases["st" + str(i)]["state"] = element[0]
            test_cases["st" + str(i)]["value"] = int(element[1])
            i += 1

        return test_cases

    def write_states_to_file(self):
        if os.stat(self._file).st_size == 0:
            test_cases = {}
        else:
            with open(self._file) as f:
                test_cases = json.load(f)

        if os.stat(self._init_file).st_size == 0:
            positions = {}
        else:
            with open(self._init_file) as f:
                positions = json.load(f)

        if os.stat(self._points_file).st_size == 0:
            points = {}
        else:
            with open(self._points_file) as f:
                points = json.load(f)

        n = len(test_cases)
        tc = 'tc' + str(n)
        test_cases[tc] = dict()
        positions[tc] = {'a': self._init_a, 'b': self._init_b}
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


if __name__ == "__main__":
    j = 0
    road = RoadGenerator(250, 5, 50, 10, 70)
    while j < 100:
        print("Generating test case " + str(j) + '...')

        road.generate_test_case()
        road.write_states_to_file()
        j += 1
