import numpy
import random

from deap import base
from deap import creator
from deap import tools



if __name__ == "__main__":
    list = [1, 2, 4, 1, 2, 4]

    for i, item in enumerate(list):
        for j in range(len(list)):
            if item == list[j] and i != j:
                print('Found in position {} and {}'.format(i, j))
                item = random.randint(0, 100)
                list[i] = item
