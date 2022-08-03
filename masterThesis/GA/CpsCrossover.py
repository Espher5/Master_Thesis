import numpy as np
import random
from pymoo.core.crossover import Crossover

from Solution import Solution

class CpsCrossover(Crossover):
    """
    Implements one point crossover to generate the offspring
    """
    def __init__(self, crossover_rate):
        # Number of parents and offsprings
        super().__init__(2, 2)
        self._crossover_rate = crossover_rate

    def _do(self, problem, x, **kwargs):
        _, n_matings, n_var = x.shape

        y = np.full_like(x, None, dtype=np.object)

        for k in range(n_matings):
            r = np.random.random()

            # Get first and second parents
            s_a, s_b = x[0, k, 0], x[1, k, 0]
            s_a.get_points()
            s_a.remove_invalid_cases()
            s_b.get_points()
            s_b.remove_invalid_cases()

            if r < self._crossover_rate:
                tc_a = s_a.states
                tc_b = s_a.states

                # Choose crossover point based on the length of the test cases
                if len(tc_a) < len(tc_b):
                    crossover_point = random.randint(1, len(tc_a) - 1)
                else:
                    crossover_point = random.randint(1, len(tc_b) - 1)

                if s_a.n_states > 2 and s_b.n_states > 2:
                    off_a = dict()
                    off_b = dict()

                    # One point crossover
                    for i in range(0, crossover_point):
                        off_a['st' + str(i)] = tc_a['st' + str(i)]
                        off_b['st' + str(i)] = tc_b['st' + str(i)]
                    for m in range(crossover_point, len(tc_b)):
                        off_a["st" + str(m)] = tc_b["st" + str(m)]
                    for n in range(crossover_point, len(tc_a)):
                        off_b["st" + str(n)] = tc_a["st" + str(n)]

                    offspring_a = Solution()
                    offspring_b = Solution()

                    offspring_a.states = off_a
                    offspring_b.states = off_b

                    offspring_a.get_points()
                    offspring_a.remove_invalid_cases()
                    offspring_a.novelty = offspring_a.calculate_novelty(tc_a, offspring_a.states)

                    offspring_b.get_points()
                    offspring_b.remove_invalid_cases()
                    offspring_b.novelty = offspring_b.calculate_novelty(tc_b, offspring_b.states)

                    y[0, k, 0], y[1, k, 0] = offspring_a, offspring_b
                else:
                    y[0, k, 0], y[1, k, 0] = s_a, s_b
            else:
                y[0, k, 0], y[1, k, 0] = s_a, s_b
