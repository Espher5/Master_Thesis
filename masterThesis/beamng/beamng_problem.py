import itertools
import json
import random
from typing import List

from deap import creator

from archive import Archive
from folders import folders
from logger import get_logger
from member import Member


def CpsProblem