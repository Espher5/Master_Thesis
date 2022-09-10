import csv
import json

from multiprocessing import Process, Manager

import algorithm.config as config

from algorithm.CpsIndividual import Individual
from algorithm.Optimize import optimize
from algorithm.road_gen import RoadGen


def generate_random_tests(n=1):
    """
    Generates n random tests with fitness != 0
    """
    tests = []
    fitness_values = []
    generator = RoadGen(
        config.MODEL["map_size"],
        config.MODEL["min_len"],
        config.MODEL["max_len"],
        config.MODEL["min_angle"],
        config.MODEL["max_angle"],
    )

    for i in range(n):
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
            fitness = ind.fitness * (-1)
            points = ind.road_points

        tests.append(points)
        fitness_values.append(fitness)

    return tests, fitness_values


def generate_high_fitness_tests():
    test_dict = {}

    with Manager() as manager:
        test_cases = manager.list()
        fitness_values = manager.list()
        novelty_values = manager.list()

        processes = []
        for i in range(20):
            process = Process(target=_task, args=(test_cases, fitness_values, novelty_values,))
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

    return test_dict


def _task(test_cases, fitness_values, novelty_values):
    """
    The task performed on a new process that executes the genetic algorithm
    """

    cases, fitness = optimize()
    for key, fit in zip(cases, fitness):
        road_points = cases[key]
        test_cases.append(road_points)
        fitness_values.append(fit[0])
        novelty_values.append(fit[1])


def test_list_to_simulator_dict(test_list):
    """
    Generates a dictionary in the format required by the simulator starting from a
    list of test cases
    """
    test_dict = {}
    for i in range(len(test_list)):
        points = test_list[i]
        tuple_points = []
        for pair in points:
            x = pair[0]
            y = pair[1]
            tup = (x, y)
            tuple_points.append(tup)

        test_dict.update({'tc' + str(i): tuple_points})

    return test_dict


def test_list_fitness_to_dict(test_cases, fitness_values):
    """
    Generates a dictionary containing both the test cases and the fitness values
    """
    test_dict = {}

    for i, (tc, fit) in enumerate(zip(test_cases, fitness_values)):
        test_dict.update({
            'tc_' + str(i): {
                'points': tc,
                'fitness': -fit
            }
        })

    return test_dict


def new_points(road_points, length):
    new_points = []

    step = len(road_points) / length
    if step == 1:
        return road_points

    for i in range(length):
        new_points.append(road_points[i + step])

    return new_points


def main():
    with open('../dict.json', 'r') as in_file:
        test_cases = json.load(in_file)

    # Truncates all test cases to 200 points and deletes the shorter ones
    parsed_cases = []
    average_length = 1

    for i in range(len(test_cases)):
        tc = test_cases['tc_' + str(i)]
        points = tc['points']
        average_length += len(points)
    average_length = average_length / len(test_cases)
    print('Average test case length: {}'.format(average_length))

    print('Test cases before truncation: ', len(test_cases))

    # Keeps the first and last points and
    # Deletes tests shorter than the threshold
    for i in range(len(test_cases)):
        parsed_case = []
        tc = test_cases['tc_' + str(i)]
        points = tc['points']
        fitness = tc['fitness']

        if len(points) >= average_length:
            for tup in points[: max_threshold]:
                x = tup[0]
                y = tup[1]
                parsed_case += [x, y]


    """
    max_threshold = 5
    for i in range(len(test_cases)):
        parsed_case = []
        tc = test_cases['tc_' + str(i)]
        points = tc['points']
        fitness = tc['fitness']
        if len(points) >= max_threshold:
            for tup in points[: max_threshold]:
                x = tup[0]
                y = tup[1]
                parsed_case += [x, y]

            parsed_cases.append(parsed_case)
            parsed_case.append(fitness)

    print('{} test cases were shorter than the {} length threshold and were truncated.'
          .format(len(test_cases) - len(parsed_cases), max_threshold))

    list_to_csv(parsed_cases)
    """

def list_to_csv(items: list):
    """
    Parses the test cases and saves them to a csv file
    """

    # Get the column names for the csv in the format:
    # {x1, y1, x2, y2, ... , fitness}
    columns = []
    i = 0
    while i < (len(items[0]) - 1) / 2:
        columns += ['x' + str(i), 'y' + str(i)]
        i += 1
    columns += ['fitness']

    with open('tests.csv', 'w', newline='') as outcsv:
        writer = csv.DictWriter(outcsv, fieldnames=columns)
        writer.writeheader()
        for item in items:
            test_dict = {}
            for i, col in zip(item, columns):
                test_dict.update({
                    col: i
                })
            writer.writerow(test_dict)


if __name__ == '__main__':
     main()
