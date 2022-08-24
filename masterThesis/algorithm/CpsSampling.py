import numpy as np

from pymoo.model.sampling import Sampling


import config
from CpsIndividual import Individual
from road_gen import RoadGen


class CpsSampling(Sampling):
    """
    Class that generates the initial population
    """
    def _do(self, problem, n_samples, **kwargs):
        generator = RoadGen(
            config.MODEL["map_size"],
            config.MODEL["min_len"],
            config.MODEL["max_len"],
            config.MODEL["min_angle"],
            config.MODEL["max_angle"],
        )
        x = np.full((n_samples, 1), None, dtype=np.object)

        for i in range(n_samples):
            states = generator.test_case_generate()
            s = Individual()
            s.states = states
            x[i, 0] = s

        return x
