import config as cf

from Car import Car
from VectorMapper import VectorMapper


class Solution:
    def __init__(self):
        self._road_points = []
        self._states = {}
        self._road_builder = VectorMapper(cf.MODEL['map_size'])
        self._car = Car(cf.MODEL['speed'], cf.MODEL['steering_angle'], cf.MODEL['map_size'])
        self._car_path = []

        self._fitness = 0
        self._novelty = 0
        self._intp_points = []
        self._too_sharp = 0
        self._just_fitness = 0

    def evaluate_fitness(self):
        road = self._road_points
        if not road:
            self.get_points()
            self.remove_invalid_cases()
            road = self._road_points
            print('Points was empty...')

        self._just_fitness = self._fitness

        if len(self._road_points) < 2:
            self._fitness = 0
        else:
            self._intp_points = self._car.interpolate_road(road)
            self._fitness, self._car_path = self._car.execute_road(self._intp_points)

    def get_points(self):
        self._road_points = self._road_builder.get_points_from_states(self._states)

    def remove_invalid_cases(self):
        self.states, self._road_points = self._road_builder.remove_invalid_cases(
            self._road_points, self.states
        )

    @staticmethod
    def calculate_novelty(old, new):
        novelty = 0
        difference = abs(len(new) - len(old)) / 2
        novelty += difference

        shorter = new if len(new) <= len(old) else old
        for tc in shorter:
            if old[tc]['state'] == new[tc]['state']:
                value_list = [old[tc]['value'], new[tc]['value']]
                ratio = max(value_list) / min(value_list)
                if ratio >= 2:
                    novelty += 0.5
            else:
                novelty += 1
        return -novelty

    @property
    def states(self):
        return self._states

    @states.setter
    def states(self, states):
        self._states = states

    @property
    def n_states(self):
        return len(self._states)

    @property
    def fitness(self):
        return self._fitness

    @fitness.setter
    def fitness(self, fitness):
        self._fitness = fitness

    @property
    def novelty(self):
        return self._novelty

    @novelty.setter
    def novelty(self, novelty):
        self._novelty = novelty
