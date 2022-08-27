import numpy
import random

from deap import base
from deap import creator
from deap import tools

from deap_tests.core.Config import Config
from deap_tests.core.Problem import Problem

from deap_tests.CpsProblem import CpsProblem
from deap_tests.CpsIndividual import CpsIndividual


def main(problem: Problem = None):
    config = Config()
    random.seed(config.get_seed())

    # DEAP framework setup
    creator.create('Fitness', base.Fitness, weights=config.fitness_weigths)
    creator.create('Individual', problem.individual_class(), fitness=creator.Fitness)

    toolbox = base.Toolbox()
    toolbox.register('individual', problem.generate_individual)
    toolbox.register('population', tools.initRepeat, list, toolbox.individual)
    toolbox.register('evaluate', problem.evaluate_individual)
    toolbox.register('mutate', problem.mutate_individual)
    toolbox.register('select', tools.selNSGA2)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register('min', numpy.min, axis=0)
    stats.register('max', numpy.max, axis=0)
    stats.register('avg', numpy.mean, axis=0)
    stats.register('std', numpy.std, axis=0)

    logbook = tools.Logbook()
    logbook.header = 'gen', 'evals', 'min', 'max', 'avg', 'std'

    print("### Initializing population....")
    population = toolbox.population(n=config.GA['population'])
    # Evaluate the initial population.
    # Note: the fitness functions are all invalid before the first iteration since they have not been evaluated.
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    problem.pre_evaluate_members(invalid_ind)

    ind1 = toolbox.individual()
    print(toolbox.evaluate(ind1))

    fitness_values = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitness_values):
        ind.fitness.values = fit

    # This is just to assign the crowding distance to the individuals (no actual selection is done).
    population = toolbox.select(population, len(population))

    record = stats.compile(population)
    logbook.record(gen=0, evals=len(invalid_ind), **record)
    print('Logbook:', logbook.stream)

    # Begin the generational process
    for gen in range(1, config.GA['n_gen']):
        # Vary the population
        offspring = tools.selTournamentDCD(population, len(population))
        offspring = [ind.clone() for ind in offspring]

        """
        for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
            toolbox.mutate(ind1)
            toolbox.mutate(ind2)
            del ind1.fitness.values, ind2.fitness.values
        """
        # Evaluate the individuals with an invalid fitness
        to_eval = offspring + population
        invalid_ind = [ind for ind in to_eval]

        problem.pre_evaluate_members(invalid_ind)

        fitness_values = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitness_values):
            ind.fitness.values = fit

        # Select the next generation population
        population = toolbox.select(population + offspring, config.GA['population'])
        record = stats.compile(population)
        logbook.record(gen=gen, evals=len(invalid_ind), **record)
        print(logbook.stream)

    return population, logbook


if __name__ == "__main__":
    problem = CpsProblem()
    final_population, search_stats = main(problem)
