import numpy as np


class CpsPopulation:
    def __init__(self, pop_size=100):
        self._individuals_fitness = [0] * pop_size


    @property
    def individuals_fitness(self):
        return self._individuals_fitness


if __name__ == '__main__':
    p = CpsPopulation(100)
    print(p.individuals_fitness)