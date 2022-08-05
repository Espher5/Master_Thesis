import numpy as np
import random
from pymoo.core.crossover import Crossover

from Solution import Solution


class CpsCrossover(Crossover):
    """
    Implements one point crossover to generate the offspring
    """
    def __init__(self, cross_rate):

        # define the crossover: number of parents and number of offsprings
        super().__init__(2, 2)
        self.cross_rate = cross_rate

    def _do(self, problem, X, **kwargs):

        # The input of has the following shape (n_parents, n_matings, n_var)
        _, n_matings, n_var = X.shape
        # print("Number of mationgs", n_matings)
        # print("X cross shape", X.shape)

        # The output owith the shape (n_offsprings, n_matings, n_var)
        # Because there the number of parents and offsprings are equal it keeps the shape of X
        Y = np.full_like(X, None, dtype=np.object)

        # for each mating provided

        for k in range(n_matings):

            r = np.random.random()

            # get the first and the second parent
            s_a, s_b = X[0, k, 0], X[1, k, 0]

            s_a.get_points()

            s_a.remove_invalid_cases()


            s_b.get_points()

            s_b.remove_invalid_cases()


            if r < self.cross_rate:

                tc_a = s_a.states
                tc_b = s_b.states
                if len(tc_a) < len(tc_b):
                    crossover_point = random.randint(1, max(len(tc_a) - 1, 2))
                elif len(tc_b) < len(tc_a):
                    crossover_point = random.randint(1, max(len(tc_b) - 1, 2))
                else:
                    crossover_point = random.randint(1, max(len(tc_a) - 1, 2))

                #
                if s_a.n_states > 2 and s_b.n_states > 2:


                    offa = {}
                    offb = {}

                    # one point crossover

                    for i in range(0, crossover_point):
                        offa["st" + str(i)] = tc_a["st" + str(i)]
                        offb["st" + str(i)] = tc_b["st" + str(i)]
                    for m in range(crossover_point, len(tc_b)):
                        offa["st" + str(m)] = tc_b["st" + str(m)]
                    for n in range(crossover_point, len(tc_a)):
                        offb["st" + str(n)] = tc_a["st" + str(n)]

                    off_a = Solution()
                    off_b = Solution()

                    off_a.states = offa
                    off_b.states = offb

                    off_a.get_points()
                    off_a.remove_invalid_cases()
                    off_a.novelty = off_a.calculate_novelty(tc_a, off_a.states)


                    off_b.get_points()
                    off_b.remove_invalid_cases()
                    off_b.novelty = off_b.calculate_novelty(tc_b, off_b.states)

                    Y[0, k, 0], Y[1, k, 0] = off_a, off_b

                else:
                    Y[0, k, 0], Y[1, k, 0] = s_a, s_b


            else:
                Y[0, k, 0], Y[1, k, 0] = s_a, s_b

        return Y
