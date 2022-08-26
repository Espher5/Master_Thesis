from typing import List

from deap_tests.core.Config import Config
from deap_tests.core.Individual import Individual
from deap_tests.core.Problem import Problem
from road_gen import RoadGen

import CpsIndividual


class CpsProblem(Problem):
    """
    Class using the simplified model to execute the roads
    """
    def __init__(self):
        self._config = Config()
        self._generator: RoadGen = RoadGen(
            self._config.MODEL["map_size"],
            self._config.MODEL["min_len"],
            self._config.MODEL["max_len"],
            self._config.MODEL["min_angle"],
            self._config.MODEL["max_angle"],
        )

    def generate_individual(self):
        states = self._generator.test_case_generate()
        individual: CpsIndividual = Individual()
        individual.states = states

    def evaluate_individual(self, individual: Individual):
        return individual.evaluate()

    def pre_evaluate_members(self, individuals):
        return

    def individual_class(self):
        return CpsIndividual
