from pymoo.core.crossover import Crossover


class CpsCrossover(Crossover):
    def __init__(self, crossover_rate):
        # Number of parents and offsprings
        super().__init__(2, 2)
        self._crossover_rate = crossover_rate

    def _do(self, problem, X, **kwargs):
        pass
