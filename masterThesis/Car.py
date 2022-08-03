import numpy as np
import math as m
import json

from numpy.ma import arange
from shapely.geometry import Point
import matplotlib.pyplot as plt
from scipy.interpolate import splprep, splev
from shapely.geometry import LineString, Point


class Car:
    """
    Class that conducts transformations to vectors automatically,
    using the commands "go straight", "turn left", and "turn right"
    """

    def __init__(self, speed, steer_angle, map_size):
        self._speed = speed
        self._steer_angle = steer_angle
        self._steer_angle_o = steer_angle
        self._map_size = map_size

    def interpolate_road(self, road):
        test_road = LineString([(t[0], t[1]) for t in road])
        length = test_road.length

