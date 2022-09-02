import json
import logging
import time

from multiprocessing import Process, Manager

from code_pipeline.tests_generation import RoadTestFactory

import algorithm.Optimize as optim


class AlgorithmTestGenerator:
    """
    This test generator creates road points using affine transformations to vectors.
    Initially generated test cases are optimized by NSGA2 algorithm with two objectives:
    fault revealing power and diversity. We use a simplified model of a vehicle to
    estimate the fault revealing power (as the maximum deviation from the road center).
    We use 100 generations and 100 population size. In each iteration of the generator 
    the Pareto optimal solutions are provided and executed. Then the algorithm is launched again.
    """

    def __init__(self, time_budget=None, executor=None, map_size=None):
        self.map_size = map_size
        self.time_budget = time_budget
        self.executor = executor

    @staticmethod
    def _task(test_cases):
        cases = optim.optimize()
        for key in cases:
            road_points = cases[key]
            test_cases.append(road_points)

    def start(self):
        """
        with Manager() as manager:
            test_cases = manager.list()
            processes = []
            for i in range(100):
                process = Process(target=self._task, args=(test_cases,))
                process.start()
                processes.append(process)

            for p in processes:
                p.join()

            print(len(test_cases))
            with open('tests.json', 'a') as out:
                json.dump(list(test_cases), out, indent=2)
        """

        while not self.executor.is_over():

            cases = optim.optimize()
            print('Generated {} test cases'.format(len(cases)))
   
            for case in cases:
                # Some debugging
                logging.info(
                    "Starting test generation. Remaining time %s",
                    self.executor.get_remaining_time(),
                )

                the_test = RoadTestFactory.create_road_test(cases[case])

                # Try to execute the test
                test_outcome, description, execution_data = self.executor.execute_test(
                    the_test
                )

                logging.info("test_outcome %s", test_outcome)
                logging.info("description %s", description)

                if self.executor.road_visualizer:
                    time.sleep(1)
