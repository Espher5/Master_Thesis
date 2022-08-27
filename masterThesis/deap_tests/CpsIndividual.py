import copy

from vehicle import Car
from deap_tests.core.Config import Config
from deap_tests.core.Individual import Individual

from algorithm.car_road import Map
from code_pipeline.beamng_executor import BeamngExecutor
from code_pipeline.tests_generation import RoadTestFactory


class CpsIndividual(Individual):
    """
    This is a class to represent one individual of the genetic algorithm
    """
    def __init__(self, config: Config):
        super().__init__(config)

        self._road_points = []
        self._states = {}
        self.car = Car(
            self._config.MODEL["speed"],
            self._config.MODEL["steer_ang"],
            self._config.MODEL["map_size"])
        self.road_builder = Map(self._config.MODEL["map_size"])
        self._car_path = []
        self._novelty = 0
        self._intp_points = []
        self._too_sharp = 0

    @property
    def states(self):
        return self._states

    @states.setter
    def states(self, states):
        self._states = states

    def clone(self) -> 'CpsIndividual':
        return copy.deepcopy(self)

    def evaluate(self):
        road = self._road_points
        if not road:  # if no road points were calculated yet
            self.get_points()
            self.remove_invalid_cases()
            road = self._road_points

        if len(self._road_points) <= 2:
            print('A')
            fitness = 0
        else:
            self._intp_points = self.car.interpolate_road(road)
            fitness, self._car_path = self.car.execute_road(self._intp_points)

        return (fitness, )

    def car_model_fit(self):
        the_executor = BeamngExecutor(self._config.MODEL["map_size"])
        the_test = RoadTestFactory.create_road_test(self._road_points)
        fit = the_executor._eval_tc(the_test)

        return fit

    def mutate(self):
        pass

    def get_points(self):
        self._road_points = self.road_builder.get_points_from_states(self._states)

    def remove_invalid_cases(self):
        self._states, self._road_points = self.road_builder.remove_invalid_cases(self._road_points, self._states)

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
 
    @property
    def n_states(self):
        return len(self._states)
