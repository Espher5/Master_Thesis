import csv
import json
import logging
import time

from code_pipeline.tests_generation import RoadTestFactory

import algorithm.Optimize as optim

import algorithm.utils as utils


class AlgorithmTestGenerator:
    def __init__(self, time_budget=None, executor=None, map_size=None):
        self.map_size = map_size
        self.time_budget = time_budget
        self.executor = executor

    def run_ambiegen(self):
        """
        AmbieGen start method
        """
        while not self.executor.is_over():

            cases, fitness = optim.optimize()
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

    def run_random_tests(self):
        """
        Generates and executes random tests
        """
        test_cases = utils.generate_random_tests(100)
        test_dict = utils.test_list_to_simulator_dict(test_cases)

        for case in test_dict:
            # Some debugging
            logging.info(
                "Starting test generation. Remaining time %s",
                self.executor.get_remaining_time(),
            )

            the_test = RoadTestFactory.create_road_test(test_dict[case])

            # Try to execute the test
            test_outcome, description, execution_data = self.executor.execute_test(
                the_test
            )

            logging.info("test_outcome %s", test_outcome)
            logging.info("description %s", description)

            if self.executor.road_visualizer:
                time.sleep(1)

    def start(self):
        """
        main method called for the competition
        """
        unparsed_cases = []
        test_cases = {}
        with open('C:\\Users\\Michelangelo\\CS\Master_Thesis\\masterThesis\\generated_cases.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    unparsed_cases.append(row[1:])
                    line_count += 1

        for i, tc in enumerate(unparsed_cases):
            road_points = []
            j = 0
            while len(road_points) < len(tc) / 2:
                x = float(tc[j])
                y = float(tc[j + 1])
                road_points.append((x, y))
                j += 2
            test_cases.update({'tc' + str(i): road_points})

        print('Start testing on GAN tests')
        for case in test_cases:
            # Some debugging
            logging.info(
                "Starting test generation. Remaining time %s",
                self.executor.get_remaining_time(),
            )

            the_test = RoadTestFactory.create_road_test(test_cases[case])

            # Try to execute the test
            test_outcome, description, execution_data = self.executor.execute_test(
                the_test
            )

            logging.info("test_outcome %s", test_outcome)
            logging.info("description %s", description)

            if self.executor.road_visualizer:
                time.sleep(1)

