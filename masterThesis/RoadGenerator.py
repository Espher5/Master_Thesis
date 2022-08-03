import os
import json
import numpy as np

import config as cf
from VectorMapper import VectorMapper


class RoadGenerator:
    """
    Class for generating roads from points
    """

    def __init__(self, map_size, min_len, max_len, min_angle, max_angle):
        self._file = 'roads.json'
        self._init_file = 'init.json'
        self._points_file = 'points.json'
        self._road_points = []
        self._init_states = ['straight', 'left', 'right']
        self._states = []

        self._vector_mapper = None
        self._init_a = None
        self._init_b = None

        self._map_size = map_size

        self._min_len = min_len
        self._max_len = max_len
        self._step_len = cf.MODEL["length_step"]
        self._length_values = [
            i for i in range(self._min_len, self._max_len + 1, self._step_len)
        ]

        self._min_angle = min_angle
        self._max_angle = max_angle
        self._step_angle = cf.MODEL['angle_step']
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
        self._vector_mapper = VectorMapper(self._map_size)
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
                (self._vector_mapper.current_pos[0] + self._vector_mapper.current_pos[1] /2)
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

            if state == 'straight':
                # No state change
                if new_state == 'SS':
                    value = np.random.choice(self._length_values)
                    self._states.append([state, value])

                    flag = self._vector_mapper.go_straight(value)
                    if not flag:
                        del self._road_points[-1]
                        del self._states[-1]
                        if len(self._road_points) <= 2:
                            self._correct_manouver()

                    self._road_points.append(
                        tuple(
                            (self._vector_mapper.current_pos[0] + self._vector_mapper.current_pos[1]) / 2
                        )
                    )

                # Transition from going straight to turning left
                elif new_state == 'SL':
                    state = 'left'
                    value = np.random.choice(self._angle_values)
                    self._states.append([state, value])

                    flag = self._vector_mapper.turn_left(value)
                    if not flag:
                        self._correct_manouver()
                    self._road_points.append(
                        tuple(
                            (self._vector_mapper.current_pos[0] + self._vector_mapper.current_pos[1]) / 2
                        )
                    )

                # Transition from going straight to turning right
                else:
                    state = 'right'
                    value = np.random.choice(self._angle_values)
                    self._states.append([state, value])

                    flag = self._vector_mapper.turn_right(value)
                    if not flag:
                        self._correct_manouver()
                    self._road_points.append(
                        tuple(
                            (self._vector_mapper.current_pos[0] + self._vector_mapper.current_pos[1]) / 2
                        )
                    )


            elif state == 'left':
                if new_state == 'LS':
                    pass
                elif new_state == 'LL':
                    pass
                else:
                    pass
            elif state == 'right':
                if new_state == 'LS':
                    pass
                elif new_state == 'LL':
                    pass
                else:
                    pass
            else:
                print('Error')

    # Deals with movement failure
    def _correct_manouver(self):
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
        pass