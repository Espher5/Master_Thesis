import copy
import numpy as np
import random

from deap_tests.vehicle import Car
from deap_tests.core.Config import Config
from deap_tests.core.Individual import Individual

from algorithm.car_road import Map
from code_pipeline.beamng_executor import BeamngExecutor
from code_pipeline.tests_generation import RoadTestFactory


class CpsIndividual(Individual):
    """
    This is a class to represent one individual of the genetic algorithm
    """
    def __init__(self, config: Config):
        super().__init__(config)

        self._crossover_rate = config.GA['crossover_rate']
        self._mutation_rate = config.GA['mutation_rate']
        self._road_points = []
        self._states = {}
        self.car = Car(
            self._config.MODEL["speed"],
            self._config.MODEL["steer_ang"],
            self._config.MODEL["map_size"])
        self.road_builder = Map(self._config.MODEL["map_size"])
        self._car_path = []
        self._novelty = 0
        self._intp_points = []
        self._too_sharp = 0

    @property
    def states(self):
        return self._states

    @states.setter
    def states(self, states):
        self._states = states

    @property
    def intp_points(self):
        return self._intp_points

    @property
    def road_points(self):
        return self._road_points

    def clone(self) -> 'CpsIndividual':
        return copy.deepcopy(self)

    def evaluate(self):
        """
        population_fitness = []
        for ind in population:
            road = ind.road_points
            if not road:  # if no road points were calculated yet
                ind.get_points()
                ind.remove_invalid_cases()
                road = ind.road_points

            if len(ind.road_points) <= 2:
                population_fitness.append(0)
            else:
                self._intp_points = self.car.interpolate_road(road)
                fitness, self._car_path = self.car.execute_road(self._intp_points)
                population_fitness.append(-fitness)
        """
        road = self._road_points
        if not road:  # if no road points were calculated yet
            self.get_points()
            self.remove_invalid_cases()
            road = self._road_points

        if len(self._road_points) <= 2:
            fitness = 0
        else:
            self._intp_points = self.car.interpolate_road(road)
            fitness, self._car_path = self.car.execute_road(self._intp_points)
        
        return (-fitness,) if 4 - fitness * (-1) < 0 else (0,)

    def car_model_fit(self):
        the_executor = BeamngExecutor(self._config.MODEL["map_size"])
        the_test = RoadTestFactory.create_road_test(self._road_points)
        fit = the_executor._eval_tc(the_test)

        return fit

    def mate(self, other):
        r = np.random.random()
        original_states1 = self.states
        original_states2 = other.states

        if r < self._crossover_rate:
            tc_a = self.states
            tc_b = other.states

            if len(tc_a) > len(tc_b):
                crossover_point = random.randint(1, len(tc_b) - 1)
            else:
                crossover_point = random.randint(1, len(tc_a) - 1)

            if len(self.states) > 2 and len(other.states) > 2:
                off_a_states = {}
                off_b_states = {}

                # One point crossover
                for i in range(0, crossover_point):
                    off_a_states["st" + str(i)] = tc_a["st" + str(i)]
                    off_b_states["st" + str(i)] = tc_b["st" + str(i)]
                for m in range(crossover_point, len(tc_b)):
                    off_a_states["st" + str(m)] = tc_b["st" + str(m)]
                for n in range(crossover_point, len(tc_a)):
                    off_b_states["st" + str(n)] = tc_a["st" + str(n)]

                self.states = off_a_states
                other.states = off_b_states
            else:
                print('Not enough states')
        else:
            return

    def mutate(self):
        r = np.random.random()
        if r < self._mutation_rate:
            sn = self.clone()
            sn.get_points()
            sn.remove_invalid_cases()

            wr = np.random.random()
            child = sn.states

            if wr < 0.2:
                candidates = list(np.random.randint(0, high=len(child), size=2))
                temp = child['st' + str(candidates[0])]
                child["st" + str(candidates[0])] = child["st" + str(candidates[1])]
                child["st" + str(candidates[1])] = temp
            elif 0.2 <= wr < 0.5:
                num = np.random.randint(0, high=len(child))
                value = np.random.choice(["state", "value"])

                if value == 'value':
                    if child["st" + str(num)]["state"] == "straight":
                        duration_list = np.arange(
                            self._config.MODEL['min_len'], self._config.MODEL['max_len']
                        )
                    else:
                        duration_list = np.arange(
                            self._config.MODEL['min_angle'], self._config.MODEL['max_angle']
                        )

                    child["st" + str(num)][value] = int(
                        np.random.choice(duration_list)
                    )

                elif value == 'state':
                    if child["st" + str(num)][value] == "straight":
                        child["st" + str(num)][value] = np.random.choice(
                            ["left", "right"]
                        )
                        duration_list = np.arange(
                            self._config.MODEL["min_angle"], self._config.MODEL["max_angle"], 5
                        )
                        child["st" + str(num)]["value"] = int(
                            np.random.choice(duration_list)
                        )
                    else:
                        child["st" + str(num)][value] = "straight"
                        duration_list = np.arange(
                            self._config.MODEL["min_len"], self._config.MODEL["max_len"], 1
                        )
                        child["st" + str(num)]["value"] = int(
                            np.random.choice(duration_list)
                        )
            else:
                candidates = list(
                    np.random.randint(0, high=len(child), size=int(len(child) / 2))
                )
                while candidates:
                    c1 = np.random.choice(candidates)
                    candidates.remove(c1)
                    if candidates:
                        c2 = np.random.choice(candidates)
                        candidates.remove(c2)
                        temp = child["st" + str(c1)]
                        child["st" + str(c1)] = child["st" + str(c2)]
                        child["st" + str(c2)] = temp
                    else:
                        if child["st" + str(c1)]["state"] == "straight":
                            duration_list = np.arange(
                                self._config.MODEL["min_len"],  self._config.MODEL["max_len"], 1
                            )
                        else:
                            duration_list = np.arange(
                                self._config.MODEL["min_angle"],  self._config.MODEL["max_angle"], 5
                            )
                        child["st" + str(c1)]["value"] = int(
                            np.random.choice(duration_list)
                        )
            self.states = child
            self.get_points()
            self.remove_invalid_cases()

    def get_points(self):
        self._road_points = self.road_builder.get_points_from_states(self._states)

    def remove_invalid_cases(self):
        self._states, self._road_points = self.road_builder.remove_invalid_cases(self._road_points, self._states)

    @staticmethod
    def calc_novelty(old, new):
        novelty = 0
        difference = abs(len(new) - len(old))/2
        novelty += difference
        if len(new) <= len(old):
            shorter = new
        else:
            shorter = old
        for tc in shorter:
            if old[tc]["state"] == new[tc]["state"]:
                value_list = [old[tc]["value"], new[tc]["value"]]
                ratio = max(value_list)/min(value_list)
                if ratio >= 2:
                    novelty += 0.5
            else:
                novelty += 1
        return -novelty
 
    @property
    def n_states(self):
        return len(self._states)
