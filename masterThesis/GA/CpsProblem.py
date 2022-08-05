from pymoo.core.problem import Problem


class CpsProblem(Problem):
    def __init__(self):
        super().__init__(n_var=1, n_obj=2, n_constr=1, elementwise=True)

    def _evaluate(self, designs, out, *args, **kwargs):
        res = designs[0]
        res.evaluate_fitness()
        out['F'] = [res.fitness, res.novelty]
        out['G'] = 8 - res.fitness * (-1)