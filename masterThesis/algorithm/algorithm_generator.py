import csv
import json
import logging
import time

from multiprocessing import Process, Manager

from code_pipeline.tests_generation import RoadTestFactory

import algorithm.Optimize as optim

import algorithm.config as cf
from algorithm.road_gen import RoadGen
from algorithm.CpsIndividual import Individual


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
    def _task(test_cases, fitness_values, novelty_values):
        cases, fitness = optim.optimize()
        print(cases)
        for key, fit in zip(cases, fitness):
            road_points = cases[key]
            test_cases.append(road_points)
            fitness_values.append(fit[0])
            novelty_values.append(fit[1])

    def main2(self):
        test_dict = {}
        """
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
        test_cases = []
        generator = RoadGen(
            cf.MODEL["map_size"],
            cf.MODEL["min_len"],
            cf.MODEL["max_len"],
            cf.MODEL["min_angle"],
            cf.MODEL["max_angle"],
        )

        for i in range(100):
            fitness = 0
            points = []

            while fitness == 0:
                states = generator.test_case_generate()
                ind = Individual()
                ind.states = states
                ind.get_points()
                ind.remove_invalid_cases()
                ind.eval_fitness()
                fitness = ind.fitness
                points = ind.road_points

            fitness = fitness * (-1)
            test_cases.append(points)

            test_dict.update({
                'tc_' + str(i): {
                    'points': test_cases[i],
                    'fitness': fitness
                }
            })

        with open('../dict.json', 'w') as f:
            json.dump(test_dict, f, indent=4)

    def main(self):
        test_dict = {}
        with Manager() as manager:
            test_cases = manager.list()
            fitness_values = manager.list()
            novelty_values = manager.list()

            processes = []
            for i in range(20):
                process = Process(target=self._task, args=(test_cases, fitness_values, novelty_values,))
                process.start()
                processes.append(process)

            for p in processes:
                p.join()

            print('Generated {} high fitness test cases'.format(len(test_cases)))

            for i, (tc, fit) in enumerate(zip(test_cases, fitness_values)):
                test_dict.update({
                    'tc_' + str(i): {
                        'points': tc,
                        'fitness': -fit
                    }
                })

        with open('../dict.json', 'w') as f:
            json.dump(test_dict, f, indent=4)

    def start(self):
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


    def star2t(self):
        """
        AmbieGen start method
        """
        while not self.executor.is_over():

            cases, fitness = optim.optimize()
            print('Generated {} test cases'.format(len(cases)))
            print(cases)
            print('Fitness results')
            for f in fitness:
                print('Fault proneness:', f[0])
                print('Novelty:', f[1])

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


    def start11(self):
        """
        Generates and executes random tests
        """
        """
        tests = []
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
            tests.append(ind.road_points)

            print(ind.road_points)



        #generate a test from the WGAN
        candidate_test = self.model.generate_test(1)
        """
        test_dict = {}
        generator = RoadGen(
            cf.MODEL["map_size"],
            cf.MODEL["min_len"],
            cf.MODEL["max_len"],
            cf.MODEL["min_angle"],
            cf.MODEL["max_angle"],
        )

        for i in range(100):
            fitness = 0
            points = []

            # Generate tests until we get one with witness != 0
            while fitness == 0:
                states = generator.test_case_generate()
                ind = Individual()
                ind.states = states
                ind.get_points()
                ind.remove_invalid_cases()
                ind.eval_fitness()
                fitness = ind.fitness
                points = ind.road_points

            fitness = fitness * (-1)

            tuple_points = []
            for pair in points:
                x = pair[0]
                y = pair[1]
                tuple = (x, y)
                tuple_points.append(tuple)

            test_dict.update({'tc' + str(i): tuple_points})

        print(test_dict)

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

if __name__ == '__main__':
    ag = AlgorithmTestGenerator()
    ag.main()
