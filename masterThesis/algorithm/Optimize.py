from pymoo.optimize import minimize

from algorithm.CpsProblem import CpsProblem
from algorithm.CpsMutation import CpsMutation
from algorithm.CpsCrossover import CpsCrossover
from algorithm.CpsDuplicates import CpsDuplicatesElimination
from algorithm.CpsSampling import CpsSampling
import time
from pymoo.algorithms.nsga2 import NSGA2
import algorithm.config as cf


def optimize():
    """
    In this function the algorithm is launched and
    the Pareto optimal solutions are returned
    """

    algorithm = NSGA2(
        n_offsprings=50,
        pop_size=cf.ga["population"],
        sampling=CpsSampling(),
        crossover=CpsCrossover(cf.ga["cross_rate"]),
        mutation=CpsMutation(cf.ga["mut_rate"]),
        eliminate_duplicates=CpsDuplicatesElimination(),
    )

    t = int(time.time() * 1000)
    seed = (
        ((t & 0xFF000000) >> 24)
        + ((t & 0x00FF0000) >> 8)
        + ((t & 0x0000FF00) << 8)
        + ((t & 0x000000FF) << 24)
    )

    res = minimize(
        CpsProblem(),
        algorithm,
        ("n_gen", cf.ga["n_gen"]),
        seed=seed,
        verbose=False,
        save_history=True,
        eliminate_duplicates=True,
    )

    print("Best solution found: \nF = %s" % (res.F))
    gen = len(res.history) - 1
    test_cases = {}
    i = 0

    while i < len(res.F):
        result = res.history[gen].pop.get("X")[i]

        road_points = result[0].intp_points
        test_cases["tc" + str(i)] = road_points
        i += 1
    return test_cases
