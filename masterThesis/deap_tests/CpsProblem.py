from typing import List

from deap import creator

from deap_tests.core.Config import Config
from deap_tests.core.Individual import Individual
from deap_tests.core.Problem import Problem
from deap_tests.road_gen import RoadGen

from deap_tests.CpsIndividual import CpsIndividual


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

    def generate_individual(self) -> Individual:
        states = self._generator.test_case_generate()
        individual: CpsIndividual = creator.Individual(self._config)
        individual.states = states
        return individual

    @staticmethod
    def evaluate_individual(individual: Individual):
        return individual.evaluate()

    @staticmethod
    def mate_individual(individual1: Individual, individual2: Individual):
        return individual1.mate(individual2)

    @staticmethod
    def mutate_individual(individual: Individual, prob=0.4):
        return individual.mutate(prob)

    def pre_evaluate_members(self, individuals):
        return

    def individual_class(self):
        return CpsIndividual
