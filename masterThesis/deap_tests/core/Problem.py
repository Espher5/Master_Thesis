from typing import List

from deap_tests.core.Individual import Individual


class Problem:
    def generate_individual(self) -> Individual:
        raise NotImplemented()

    @staticmethod
    def evaluate_individual(individual: Individual):
        raise NotImplemented()

    @staticmethod
    def mate_individual(individual1: Individual, individual2: Individual):
        raise NotImplemented()

    @staticmethod
    def mutate_individual(individual: Individual):
        individual.mutate()

    def individual_class(self):
        raise NotImplemented()

    def on_iteration(self, idx, pop: List[Individual], logbook):
        raise NotImplemented()

    def member_class(self):
        raise NotImplemented()

    def reseed(self, population, offspring):
        raise NotImplemented()

    def pre_evaluate_members(self, individuals: List[Individual]):
        pass
