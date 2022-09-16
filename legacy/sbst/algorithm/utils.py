import csv
import random
import json
from multiprocessing import Process, Manager

import algorithm.config as config

from algorithm.CpsIndividual import Individual
from algorithm.Optimize import optimize
from algorithm.road_gen import RoadGen


def generate_random_tests(n=1, target_fitness=1):
    """
    Generates n random tests with fitness != 0
    """
    test_dict = {}

    test_cases = []
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
        while fitness < target_fitness:
            states = generator.test_case_generate()
            ind = Individual()
            ind.states = states
            ind.get_points()
            ind.remove_invalid_cases()
            ind.eval_fitness()
            fitness = ind.fitness * (-1)
            points = ind.road_points

        test_cases.append(points)
        fitness_values.append(fitness)

    for i, (tc, fit) in enumerate(zip(test_cases, fitness_values)):
        test_dict.update({
            'tc_' + str(i): {
                'points': tc,
                'fitness': -fit
            }
        })

    return test_dict


def generate_high_fitness_tests(N=1):
    """
    Runs the Ambiegen algorithm N times in order to generate
    an initial dataset of high fitness test cases
    """
    individuals = []
    with Manager() as manager:
        individuals_ = manager.list()

        processes = []
        for i in range(N):
            process = Process(target=_task, args=(individuals_,))
            process.start()
            processes.append(process)

        for p in processes:
            p.join()

        print('Generated {} high fitness test cases'.format(len(individuals_)))

        for ind in individuals_:
            individuals.append(ind)

    return individuals


def _task(individuals_list):
    """
    The task performed on a new process that executes the genetic algorithm
    """

    individuals, cases, fitness = optimize()
    for ind in individuals:
        individuals_list.append(ind)


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


def sample_points(road_points, length):
    new_points = []

    # If the test case is shorter than average
    # duplicate a random point
    length = int(length)

    if length > len(road_points):
        n = random.randrange(0, len(road_points))
        for i in range(length):
            new_points.append(road_points[i])

            if i == n:
                for i in range((length - len(road_points)) - 1):
                    new_points.append(road_points[n])
                new_points += road_points[n:]
                break
    else:
        step = int(len(road_points) / length)

        i = 0
        while len(new_points) < length:
            new_points.append(road_points[i])
            i = min(i + step, len(road_points) - 1)

    return new_points


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


def main():
    individuals = generate_high_fitness_tests(20)

    parsed_cases = []
    average_length = 1
    for ind in individuals:
        case = []
        road_points = ind.intp_points
        average_length += len(road_points)

        for pair in road_points:
            x = pair[0]
            y = pair[1]
            case += [x, y]
        case.append(ind.fitness * (-1))

        parsed_cases.append(case)

    average_length = average_length / len(parsed_cases)
    print('Average length:', average_length)

    for i in range(len(parsed_cases)):
        points = parsed_cases[i]
        fitness = points[-1]
        del points[-1]

        parsed_cases[i] = sample_points(points, average_length * 2)
        parsed_cases[i].append(fitness)

    list_to_csv(parsed_cases)


if __name__ == '__main__':
    main()
