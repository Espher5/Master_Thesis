from code_pipeline.beamng_executor import BeamngExecutor
from code_pipeline.tests_generation import RoadTestFactory

from algorithm import config
from algorithm.car_road import Map
from algorithm.vehicle import Car


class Individual:
    """
    Class representing an individual of the population
    """
    def __init__(self):
        self._car = Car(
            config.MODEL['speed'],
            config.MODEL['steer_angle'],
            config.MODEL['map_size']
        )
        self._car_path = []
        self._road_builder = Map(config.MODEL['map_size'])
        self._road_points = []
        self._states = {}
        self._fitness = 0
        self._intp_points = []
        self._too_sharp = 0
        self._just_fitness = 0

    @property
    def fitness(self):
        return self._fitness

    @property
    def states(self):
        return self._states

    @states.setter
    def states(self, states):
        self._states = states

    @property
    def n_states(self):
        return len(self._states)

    def eval_fitness(self):
        """
            Execute the road using the simplified model
        """
        road = self._road_points

        if not road:
            self.get_points()
            self.remove_invalid_cases()
            road = self._road_points

        if len(self._road_points) <= 2:
            self._fitness = 0
        else:
            self._intp_points = self._car.interpolate_road(road)
            self._fitness, self._car_path = self._car.execute_road(self._intp_points)

    def car_model_fit(self):
        """
        Execute the road using the BeamNG simulator
        """
        the_executor = BeamngExecutor(config.MODEL['map_size'])
        the_test = RoadTestFactory.create_road_test(self._road_points)
        fitness = the_executor._eval_tc(the_test)

        return fitness

    def get_points(self):
        self._road_points = self._road_builder.get_points_from_states(self._states)

    def remove_invalid_cases(self):
        self._states, self._road_points = self._road_builder.remove_invalid_cases(self._road_points, self.n_states)
