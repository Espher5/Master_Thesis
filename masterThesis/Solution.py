import config

from vehicle import Car
from car_road import Map


class Solution:
    def __init__(self):

        self._road_points = []
        self._states = {}
        self._car = Car(config.MODEL["speed"], config.MODEL["steer_ang"], config.MODEL["map_size"])
        self._road_builder = Map(config.MODEL["map_size"])
        self._fitness = 0
        self._car_path = []
        self._novelty = 0
        self._intp_points = []
        self._too_sharp = 0
        self._just_fitness = 0

    @property
    def states(self):
        return self._states

    @states.setter
    def states(self, value):
        self._states = value

    @property
    def n_states(self):
        return len(self._states)

    @property
    def fitness(self):
        return self._fitness

    @fitness.setter
    def fitness(self, value: float):
        self._fitness = value

    @property
    def car_path(self):
        return self._car_path

    @property
    def novelty(self):
        return self._novelty

    @novelty.setter
    def novelty(self, novelty):
        self._novelty = novelty

    @property
    def intp_points(self):
        return self._intp_points

    def eval_fitness(self):
        road = self._road_points
        if not road:
            self.get_points()
            self.remove_invalid_cases()
            road = self._road_points
            print("Points was empty")

        self._just_fitness = self._fitness

        if len(self._road_points) < 2:
            self._fitness = 0
        else:
            self._intp_points = self._car.interpolate_road(road)
            self._fitness, self._car_path = self._car.execute_road(self._intp_points)

        return

    def get_points(self):
        self._road_points = self._road_builder.get_points_from_states(self._states)

    def remove_invalid_cases(self):
        self._states, self._road_points = self._road_builder.remove_invalid_cases(
            self._road_points, self._states
        )

    @staticmethod
    def calc_novelty(old, new):
        novelty = 0
        difference = abs(len(new) - len(old)) / 2
        novelty += difference
        if len(new) <= len(old):
            shorter = new
        else:
            shorter = old
        for tc in shorter:
            if old[tc]["state"] == new[tc]["state"]:
                value_list = [old[tc]["value"], new[tc]["value"]]
                ratio = max(value_list) / min(value_list)
                if ratio >= 2:
                    novelty += 0.5
            else:
                novelty += 1
        # print("NOVELTY", novelty)
        return -novelty
