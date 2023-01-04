import unittest
from CleaningRobot import CleaningRobot


class US01(unittest.TestCase):
    def test_robot_initialization(self):
        robot = CleaningRobot(10, 10)
        robot.initialize_robot()
        self.assertEqual('(0,0,N)', robot.robot_status())

