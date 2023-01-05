import unittest
from unittest.mock import patch
from CleaningRobot import CleaningRobot
from CleaningRobotError import CleaningRobotError
from mock import GPIO


class CleaningRobotTest(unittest.TestCase):
    """
    Your tests go here
    """

    def test_initialize_robot(self):
        robot = CleaningRobot(6, 6)
        robot.initialize_robot()
        status = robot.robot_status()
        self.assertEqual("(0,0,N)", status)

    def test_initialize_robot_none(self):
        robot = CleaningRobot(6, 6)
        self.assertIsNone(robot.robot_status())

    def test_robot_status(self):
        robot = CleaningRobot(6, 6)
        robot.initialize_robot()
        robot.update_robot_status("(0,2,W)")
        self.assertEqual("(0,2,W)", robot.robot_status())

    def test_robot_status_none(self):
        robot = CleaningRobot(6, 6)
        self.assertIsNone(robot.robot_status())

    @patch.object(GPIO, 'input')
    def test_obstacle_found_true(self, mock_input):
        robot = CleaningRobot(6, 6)
        mock_input.return_value = 5
        self.assertTrue(robot.obstacle_found())

    @patch.object(GPIO, 'input')
    def test_obstacle_found_false(self, mock_input):
        robot = CleaningRobot(6, 6)
        mock_input.return_value = 0
        self.assertFalse(robot.obstacle_found())

    @patch.object(GPIO, 'input')
    def test_execute_command_forward_without_obstacle(self, mock_input):
        robot = CleaningRobot(6, 6)
        robot.initialize_robot()
        mock_input.return_value = 0
        result = robot.execute_command("f")
        self.assertEqual("(0,1,N)", result)

    @patch.object(GPIO, 'input')
    def test_execute_command_left_without_obstacle(self, mock_input):
        robot = CleaningRobot(6, 6)
        robot.initialize_robot()
        mock_input.return_value = 0
        result = robot.execute_command("l")
        self.assertEqual("(0,0,W)", result)

    @patch.object(GPIO, 'input')
    def test_execute_command_right_without_obstacle(self, mock_input):
        robot = CleaningRobot(6, 6)
        robot.initialize_robot()
        mock_input.return_value = 0
        result = robot.execute_command("r")
        self.assertEqual("(0,0,E)", result)

    @patch.object(GPIO, 'input')
    def test_execute_command_forward_with_obstacle(self, mock_input):
        robot = CleaningRobot(6, 6)
        robot.initialize_robot()
        mock_input.return_value = 1
        result = robot.execute_command("f")
        self.assertEqual("(0,0,N)(o_0,o_0)", result)

    @patch.object(GPIO, 'input')
    def test_execute_command_left_with_obstacle(self, mock_input):
        robot = CleaningRobot(6, 6)
        robot.initialize_robot()
        mock_input.return_value = 1
        result = robot.execute_command("l")
        self.assertEqual("(0,0,N)(o_0,o_0)", result)

    @patch.object(GPIO, 'input')
    def test_execute_command_right_with_obstacle(self, mock_input):
        robot = CleaningRobot(6, 6)
        robot.initialize_robot()
        mock_input.return_value = 1
        result = robot.execute_command("r")
        self.assertEqual("(0,0,N)(o_0,o_0)", result)



