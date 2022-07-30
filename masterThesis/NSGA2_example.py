import numpy as np

from pymoo.optimize import minimize
from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from deap import benchmarks

benchmarks.kursawe([1, 1])


class MyProblem(Problem):
    def _evaluate(self, designs, out, *args, **kwargs):
        res = []
        for design in designs:
            res.append(benchmarks.kursawe(design))

        out['F'] = np.array(res)


problem = MyProblem(n_var=2, n_obj=2, xl=[-5., -5.], xu=[5., 5.])
algorithm = NSGA2(pop_size=100)
stop_criterion = ('n_gen', 100)

result = minimize(
    problem=problem,
    algorithm=algorithm,
    termination=stop_criterion
)

print(result.F)
print(result.X)

