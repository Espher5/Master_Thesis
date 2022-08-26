from typing import List

from deap_tests.core.Individual import Individual


class Problem:
    def generate_individual(self) -> Individual:
        raise NotImplemented()

    @staticmethod
    def mutate_individual(individual: Individual):
        individual.mutate()

    def evaluate_individual(self, individual: Individual):
        raise NotImplemented()

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
