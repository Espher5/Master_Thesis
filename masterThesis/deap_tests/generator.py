import logging
import time

from code_pipeline.tests_generation import RoadTestFactory

from deap_tests.Optimizer import Optimizer
from deap_tests.CpsProblem import CpsProblem


class Generator:
    def __init__(self, time_budget=None, executor=None, map_size=None):
        self._map_size = map_size
        self._time_budget = time_budget
        self._executor = executor

    def start(self):
        optimizer = Optimizer(CpsProblem())
        while not self._executor.is_over():
            final_population, logbook = optimizer.optimize()
            ind1 = final_population[0]
            ind2 = final_population[1]

            if ind1.states == ind2.states:
                print('Okayeg')
            test_cases = {}

            for i, ind_ in enumerate(final_population):
                road_points = ind_.intp_points
                test_cases["tc" + str(i)] = road_points
            print('Generated {} test cases'.format(len(test_cases)))

            for case in test_cases:
                # Some debugging
                logging.info(
                    "Starting test generation. Remaining time %s",
                    self._executor.get_remaining_time(),
                )

                the_test = RoadTestFactory.create_road_test(test_cases[case])

                # Try to execute the test
                test_outcome, description, execution_data = self._executor.execute_test(
                    the_test
                )

                logging.info("test_outcome %s", test_outcome)
                logging.info("description %s", description)

                if self._executor.road_visualizer:
                    time.sleep(1)
