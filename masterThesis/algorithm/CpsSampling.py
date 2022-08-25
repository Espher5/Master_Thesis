import numpy as np
from pymoo.model.sampling import Sampling
from algorithm.CpsIndividual import Individual

import algorithm.config as cf
from algorithm.road_gen import RoadGen


class CpsSampling(Sampling):
    """
    Class that generates the initial population
    """
    def _do(self, problem, n_samples, **kwargs):
        generator = RoadGen(
            cf.MODEL["map_size"],
            cf.MODEL["min_len"],
            cf.MODEL["max_len"],
            cf.MODEL["min_angle"],
            cf.MODEL["max_angle"],
        )
        x = np.full((n_samples, 1), None, dtype=np.object)

        for i in range(n_samples):
            states = generator.test_case_generate()
            s = Individual()
            s.states = states
            x[i, 0] = s
        return x
