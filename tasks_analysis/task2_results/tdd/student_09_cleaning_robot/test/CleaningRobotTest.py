import unittest
from unittest.mock import patch
from CleaningRobot import CleaningRobot


class CleaningRobotTest(unittest.TestCase):
    """
    Your tests go here
    """

    def test_initialize(self):
        robot = CleaningRobot(5, 5)
        robot.initialize_robot()
        self.assertEqual('(0,0,N)', robot.robot_status())

    def test_rotation1(self):
        robot = CleaningRobot(5, 5)
        robot.initialize_robot()
        self.assertEqual('(0,0,W)', robot.execute_command('l'))

    def test_rotation2(self):
        robot = CleaningRobot(5, 5)
        robot.initialize_robot()
        self.assertEqual('(0,0,E)', robot.execute_command('r'))