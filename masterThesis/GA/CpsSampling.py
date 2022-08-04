import numpy as np
from pymoo.core.sampling import Sampling

import config as cf
from Solution import Solution
from RoadGenerator import RoadGenerator


class CpsSampling(Sampling):
    def _do(self, problem, n_samples, **kwargs):
        generator = RoadGenerator(
            cf.MODEL['map_size'],
            cf.MODEL['min_len'],
            cf.MODEL['max_len'],
            cf.MODEL['min_angle'],
            cf.MODEL['max_angle']
        )

        x = np.full((n_samples, 1), None, dtype=np.object)

        for i in range(n_samples):
            states = generator.generate_test_case()
            s = Solution()

            s.states = states
            s.get_points()
            s.remove_invalid_cases()

            x[i, 0] = s

        return x
