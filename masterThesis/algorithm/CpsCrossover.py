import numpy as np
import random

from pymoo.model.crossover import Crossover

from algorithm.CpsIndividual import Individual


class CpsCrossover(Crossover):
    """
    Class for one-point crossover
    """
    def __init__(self, cross_rate):
        super().__init__(2, 2)
        self.cross_rate = cross_rate

    def _do(self, problem, X, **kwargs):
        # The input of has the following shape (n_parents, n_matings, n_var)
        _, n_matings, n_var = X.shape

        # The output with the shape (n_offsprings, n_matings, n_var)
        # Because there the number of parents and offsprings are equal it keeps the shape of X
        y = np.full_like(X, None, dtype=np.object)

        # for each mating provided
        for k in range(n_matings):
            r = np.random.random()
            s_a, s_b = X[0, k, 0], X[1, k, 0]

            if r < self.cross_rate:
                tc_a = s_a.states
                tc_b = s_b.states

                if len(tc_a) > len(tc_b):
                    crossover_point = random.randint(1, len(tc_a) - 1)
                else:
                    crossover_point = random.randint(1, len(tc_b) - 1)

                if s_a.n_states > 2 and s_b.n_states > 2:

                    off_a_states = {}
                    off_b_states = {}

                    # one point crossover
                    for i in range(0, crossover_point):
                        off_a_states["st" + str(i)] = tc_a["st" + str(i)]
                        off_b_states["st" + str(i)] = tc_b["st" + str(i)]
                    for m in range(crossover_point, len(tc_b)):
                        off_a_states["st" + str(m)] = tc_b["st" + str(m)]
                    for n in range(crossover_point, len(tc_a)):
                        off_b_states["st" + str(n)] = tc_a["st" + str(n)]

                    off_a = Individual()
                    off_b = Individual()

                    off_a.states = off_a_states
                    off_b.states = off_b_states

                else:
                    print("Not enough states!")

                off_a.novelty = off_a.calc_novelty(tc_a, off_a.states)
                off_b.novelty = off_b.calc_novelty(tc_b, off_b.states)

                y[0, k, 0], y[1, k, 0] = off_a, off_b

            else:
                y[0, k, 0], y[1, k, 0] = s_a, s_b

        return y
