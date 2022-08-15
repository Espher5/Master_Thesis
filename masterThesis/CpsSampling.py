import numpy as np
from pymoo.model.sampling import Sampling
from Solution import Solution

import config as cf
from road_gen import RoadGen


class CpsSampling(Sampling):
    def _do(self, problem, n_samples, **kwargs):
        # singleton = OnlyOne()

        generator = RoadGen(
            cf.model["map_size"],
            cf.model["min_len"],
            cf.model["max_len"],
            cf.model["min_angle"],
            cf.model["max_angle"],
        )

        X = np.full((n_samples, 1), None, dtype=np.object)

        for i in range(n_samples):
            states = generator.test_case_generate()
            s = Solution()

            s.states = states

            s.get_points()
            s.remove_invalid_cases()

            X[i, 0] = s

        return X
