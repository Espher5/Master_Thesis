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

import torch.nn as nn
import torch.nn.functional as F
import torch
from wgan.SUT import SUT
from wgan.model import WGAN
import numpy as np

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

        noise_dim = 10
        gan_neurons = 128
        gan_learning_rate = 0.00005
        analyzer_learning_rate = 0.001
        analyzer_neurons = 32
        gp_coefficient = 10
        batch_size = 32
        train_settings_init = {"epochs": 3,
                               "analyzer_epochs": 20,
                               "critic_epochs": 5,
                               "generator_epochs": 10}
        train_settings = {"epochs": 20,
                          "analyzer_epochs": 10,
                          "critic_epochs": 50,
                          "generator_epochs": 10}

        sut = SUT()
        sut.ndimensions = 8

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model = WGAN(sut=sut, validator=None, device=device)

        self.model.train_settings_init = train_settings_init
        self.model.train_settings = train_settings
        self.model.noise_dim = noise_dim
        self.model.gan_neurons = gan_neurons
        self.model.gan_learning_rate = gan_learning_rate
        self.model.analyzer_learning_rate = analyzer_learning_rate
        self.model.analyzer_neurons = analyzer_neurons
        self.model.gp_coefficient = gp_coefficient
        self.model.batch_size = batch_size

        self.model.initialize()

    def start(self):
        tests = []
        generator = RoadGen(
            cf.MODEL["map_size"],
            cf.MODEL["min_len"],
            cf.MODEL["max_len"],
            cf.MODEL["min_angle"],
            cf.MODEL["max_angle"],
        )

        sample_X = []
        sample_Y = []
        for i in range(10):
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

            parsed_points = []
            for tup in points[1: 5]:
                x = tup[0]
                y = tup[1]
                parsed_points += [x, y]
            sample_X.append(parsed_points)
            sample_Y.append([fitness])

        sample_X = np.array(sample_X)
        sample_Y = np.array(sample_Y)

        print('Sample_X', sample_X)
        print('Sample_Y', sample_Y)

        print('SHAPE OF Sample_X', sample_X.shape)
        print('SHAPE OF Sample_Y', sample_Y.shape)

        self.model.train_with_batch(sample_X, sample_Y, train_settings=self.model.train_settings)

        candidate_tests = self.model.generate_test(10)

        tests = {}
        for test in candidate_tests:
            road_points = []
            j = 0
            while len(road_points) < len(test) / 2:
                x = float(test[j])
                y = float(test[j + 1])
                road_points.append((x, y))
                j += 2
            tests.update({'tc0': road_points})

        for case in tests:
            # Some debugging
            logging.info(
                "Starting test generation. Remaining time %s",
                self.executor.get_remaining_time(),
            )

            the_test = RoadTestFactory.create_road_test(tests[case])

            # Try to execute the test
            test_outcome, description, execution_data = self.executor.execute_test(
                the_test
            )

            logging.info("test_outcome %s", test_outcome)
            logging.info("description %s", description)

            if self.executor.road_visualizer:
                time.sleep(1)