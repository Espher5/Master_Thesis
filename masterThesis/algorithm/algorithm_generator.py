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

    """
    def generate_test_dataset(self):
        test_dict = {}
        with Manager() as manager:
            test_cases = manager.list()
            processes = []
            for i in range(20):
                process = Process(target=self._task, args=(test_cases,))
                process.start()
                processes.append(process)

            for p in processes:
                p.join()

            print('Generated {} high fitness test cases'.format(len(test_cases)))

            for i in range(len(test_cases)):
                test_dict.update({
                    'tc_' + str(i): {
                        'points': test_cases[i],
                        'score': 'hard'
                    }
                })

            # Generates as many low-fitness test cases
            low_fitness_cases = []
            low_fitness_threshold = 4
            generator = RoadGen(
                cf.MODEL["map_size"],
                cf.MODEL["min_len"],
                cf.MODEL["max_len"],
                cf.MODEL["min_angle"],
                cf.MODEL["max_angle"],
            )

            for i in range(100):
                states = generator.test_case_generate()
                ind = Individual()
                ind.states = states
                ind.get_points()
                ind.remove_invalid_cases()
                ind.eval_fitness()

                fitness = ind.fitness * (-1)
                if fitness < low_fitness_threshold:
                    points = ind.road_points
                    low_fitness_cases.append(points)

                    test_dict.update({
                        'tc_' + str(i + len(test_cases)): {
                            'points': low_fitness_cases[i],
                            'score': fitness
                        }
                    })
            print('Generated {} low fitness test cases'.format(len(low_fitness_cases)))

            with open('../dict.json', 'w') as f:
                json.dump(test_dict, f, indent=4)
    """

    @staticmethod
    def main():
        test_dict = utils.generate_high_fitness_tests()
        with open('../dict.json', 'w') as f:
            json.dump(test_dict, f, indent=4)

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
                    print(f'Column names are {", ".join(row)}')
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

        print('Starting testing on GAN tests')
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


if __name__ == '__main__':
    ag = AlgorithmTestGenerator()
    ag.main()
