import numpy as np
import random
import copy
from pymoo.core.mutation import Mutation

import config as cf


class CpsMutation(Mutation):
    def __init__(self, mutation_rate):
        super().__init__()
        self._mutation_rate = mutation_rate

    def _do(self, problem, x, **kwargs):
        for i in range(len(x)):
            r = np.random.random()
            s = x[i, 0]

            if s is None:
                print('S is None')

