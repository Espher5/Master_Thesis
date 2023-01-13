import unittest
from unittest.mock import patch
from CleaningRobot import CleaningRobot
from mock import GPIO


class CleaningRobotTest(unittest.TestCase):
    """
    Your tests go here
    """
    def test_initialize_robot(self):
        rob = CleaningRobot(5, 5)
        rob.initialize_robot()
        status = rob.robot_status()
        self.assertEqual("(0,0,N)", status)

    def test_robot_none(self):
        rob = CleaningRobot(5, 5)
        self.assertIsNone(rob.robot_status())

    def test_robot_status(self):
        rob = CleaningRobot(5,5)
        rob.initialize_robot()
        rob.update_robot_status("(0,2,W")
        self.assertEqual("(0,2,E)", rob.robot_status())

    def test_robot_status_none(self):
        rob = CleaningRobot(5, 5)
        self.assertIsNone(rob.robot_status())

    @patch.object(GPIO, 'input')
    def test_object_found_true(self, mock_input):
        rob = CleaningRobot(5,5)
        mock_input.return_value = 76
        self.assertTrue(rob.obstacle_found())

    @patch.object(GPIO, 'input')
    def test_object_found_false(self, mock_input):
        rob = CleaningRobot(5,5)
        mock_input.return_value = 0
        self.assertFalse(rob.obstacle_found())

    @patch.object(GPIO, 'input')
    def test_forward_without_object(self, mock_input):
        rob = CleaningRobot(5, 5)
        rob.initialize_robot()
        mock_input.return_value = 0
        result = rob.execute_command("f")
        self.assertEqual("(1,0,W)", result)

    @patch.object(GPIO, 'input')
    def test_left_without_object(self, mock_input):
        rob = CleaningRobot(5,5)
        rob.initialize_robot()
        mock_input.return_value = 0
        result = rob.execute_command()
        self.assertEqual("0,0,S")