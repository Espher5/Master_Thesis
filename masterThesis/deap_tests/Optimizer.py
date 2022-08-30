import numpy

from deap import base
from deap import creator
from deap import tools

from deap_tests.core.Config import Config
from deap_tests.core.Problem import Problem


class Optimizer:
    def __init__(self, problem: Problem = None):
        self._problem = problem
        self._config = Config()

        self._setup()

    def _setup(self):
        """
        DEAP framework setup
        """
        # creator.create('Fitness', base.Fitness, weights=config.fitness_weigths * 20)
        creator.create('Fitness', base.Fitness, weights=self._config.fitness_weights)
        creator.create('Individual', self._problem.individual_class(), fitness=creator.Fitness)

        self._toolbox = base.Toolbox()
        self._toolbox.register('individual', self._problem.generate_individual)
        self._toolbox.register('population', tools.initRepeat, list, self._toolbox.individual)
        self._toolbox.register('evaluate', self._problem.evaluate_individual)
        self._toolbox.register('mate', self._problem.mate_individual)
        self._toolbox.register('mutate', self._problem.mutate_individual)
        self._toolbox.register('select', tools.selNSGA2)

        self._stats = tools.Statistics(lambda ind: ind.fitness.values)
        self._stats.register('min', numpy.min, axis=0)
        self._stats.register('max', numpy.max, axis=0)
        self._stats.register('avg', numpy.mean, axis=0)
        self._stats.register('std', numpy.std, axis=0)
        self._logbook = tools.Logbook()
        self._logbook.header = 'gen', 'evals', 'min', 'max', 'avg', 'std'

    def optimize(self):
        """

        """
        population = self._toolbox.population(n=self._config.GA['population'])

        # Evaluate the initial population.
        # Note: the fitness functions are all invalid before the first iteration since they have not been evaluated.
        invalid_ind = [ind for ind in population if not ind.fitness.valid]
        self._problem.pre_evaluate_members(invalid_ind)
        fitness_values = self._toolbox.map(self._toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitness_values):
            ind.fitness.values = fit

        # This is just to assign the crowding distance to the individuals (no actual selection is done).
        population = self._toolbox.select(population, len(population))

        record = self._stats.compile(population)
        self._logbook.record(gen=0, evals=len(invalid_ind), **record)

        # Begin the generational process
        for gen in range(1, self._config.GA['n_gen']):
            # Remove duplicates in population
            for i, ind in enumerate(population):
                for j in range(len(population)):
                    if i != j and ind.states == population[j].states:
                        new_ind = self._toolbox.individual()
                        population[i] = new_ind

            invalid_ind = [ind_ for ind_ in population if not ind_.fitness.valid]
            fitness_values = self._toolbox.map(self._toolbox.evaluate, invalid_ind)
            for ind_, fit in zip(invalid_ind, fitness_values):
                ind_.fitness.values = fit
            population = self._toolbox.select(population, len(population))

            # Vary the population
            offspring = tools.selTournamentDCD(population, len(population))
            offspring = [ind.clone() for ind in offspring]

            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                self._toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

            for mutant in offspring:
                self._toolbox.mutate(mutant)
                del mutant.fitness.values

            # Evaluate the individuals with an invalid fitness
            to_eval = offspring + population
            invalid_ind = [ind for ind in to_eval]
            self._problem.pre_evaluate_members(invalid_ind)
            fitness_values = self._toolbox.map(self._toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitness_values):
                ind.fitness.values = fit

            # Select the next generation population
            population = self._toolbox.select(population + offspring, self._config.GA['population'])


            record = self._stats.compile(population)
            self._logbook.record(gen=gen, evals=len(invalid_ind), **record)
            print(self._logbook.stream)

        return population, self._logbook
