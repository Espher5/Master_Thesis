from pymoo.model.problem import Problem

from algorithm import config


class CpsProblem(Problem):
    def __init__(self):
        # Set the population size as the number of objective functions to minimize
        super().__init__(n_var=1, n_obj=config.GA['population'], n_constr=1, elementwise_evaluation=True)

    def _evaluate(self, x, out, *args, **kwargs):
        s = x[0]
        # Transform the states into actual points
        # (mutation and crossover operations are performed on states)
        s.get_points()
        s.remove_invalid_cases()
        s.eval_fitness()

        out['F'] = [s.fitness, s.novelty]
        out['G'] = 4 - s.fitness * (-1)
