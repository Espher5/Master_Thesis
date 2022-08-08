from typing import List

import config
from individual import Individual
from member import Member
from archive import Archive


class Problem:
    def __init__(self, config, archive: Archive):
        self._config = config
        self._archive = archive

    def generate_individual(self) -> Individual:
        raise NotImplemented()

    def deap_generate_individual(self) -> Individual:
        raise NotImplemented()

    def deap_mutate_individual(self, individual: Individual):
        individual.mutate()

    def deap_evaluate_individual(self, individual: Individual):
        raise NotImplemented()

    def deap_individual_class(self):
        raise NotImplemented()

    def on_iteration(self, idx, pop: List[Individual], logbook):
        raise NotImplemented()

    def member_class(self):
        raise NotImplemented()

    def reseed(self, population, offsprings):
        raise NotImplemented()

    def generate_random_member(self) -> Member:
        raise NotImplemented()

    def pre_evaluate_members(self, individuals: List[Individual]):
        pass
