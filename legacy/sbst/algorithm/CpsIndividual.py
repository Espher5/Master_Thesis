from algorithm.vehicle import Car
import algorithm.config as cf
from algorithm.car_road import Map


class Individual:
    """
    This is a class to represent one individual of the genetic algorithm
    """
    def __init__(self):
        self._road_points = []
        self._states = {}
        self._car = Car(cf.MODEL["speed"], cf.MODEL["steer_ang"], cf.MODEL["map_size"])
        self._road_builder = Map(cf.MODEL["map_size"])

        self._car_path = []
        self._fitness = 0
        self._novelty = 0
        self._intp_points = []

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

    @property
    def novelty(self):
        return self._novelty

    @novelty.setter
    def novelty(self, novelty):
        self._novelty = novelty

    @property
    def road_points(self):
        return self._road_points

    @road_points.setter
    def road_points(self, road_points):
        self._road_points = road_points

    @property
    def intp_points(self):
        return self._intp_points

    def eval_fitness(self):
        road = self._road_points
        if not road:  # if no road points were calculated yet
            self.get_points()
            self.remove_invalid_cases()
            road = self._road_points

        if len(self.road_points) <= 2:
            self._fitness = 0
        else:
            self._intp_points = self._car.interpolate_road(road)
            self._fitness, self._car_path = self._car.execute_road(self._intp_points)
        return

    def get_points(self):
        self._road_points = self._road_builder.get_points_from_states(self._states)

    def remove_invalid_cases(self):
        self._states, self._road_points = self._road_builder.remove_invalid_cases(self._road_points, self._states)

    @staticmethod
    def calc_novelty(old, new):
        novelty = 0
        difference = abs(len(new) - len(old))/2
        novelty += difference
        if len(new) <= len(old):
            shorter = new
        else:
            shorter = old
        for tc in shorter:
            if old[tc]["state"] == new[tc]["state"]:
                value_list = [old[tc]["value"], new[tc]["value"]]
                ratio = max(value_list)/min(value_list)
                if ratio >= 2:
                    novelty += 0.5
            else:
                novelty += 1
        return -novelty
