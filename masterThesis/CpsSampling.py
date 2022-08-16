import numpy as np

from pymoo.model.sampling import Sampling

import config
from road_gen import RoadGen
from Solution import Solution


class CpsSampling(Sampling):
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
            s = Solution()

            s.states = states

            s.get_points()
            s.remove_invalid_cases()

            x[i, 0] = s

        return x
