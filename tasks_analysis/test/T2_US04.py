import unittest
from unittest.mock import patch
import mock.GPIO as GPIO
from CleaningRobot import CleaningRobot


class US04(unittest.TestCase):
    def setUp(self) -> None:
        self.robot = CleaningRobot(10, 10)
        self.robot.initialize_robot()

    # Forward movement tests with obstacle
    @patch.object(GPIO, 'input')
    def test_move_forward_facing_N_with_obstacle(self, mock_input):
        mock_input.side_effect = [61, 10]
        self.robot.facing = self.robot.N
        self.assertEqual('(0,0,N)(0,1)', self.robot.execute_command('f'))

    @patch.object(GPIO, 'input')
    def test_move_forward_facing_S_with_obstacle(self, mock_input):
        mock_input.side_effect = [29, 32]
        self.robot.pos_x = 1
        self.robot.pos_y = 1
        self.robot.facing = self.robot.S
        self.assertEqual('(1,1,S)(1,0)', self.robot.execute_command('f'))

    @patch.object(GPIO, 'input')
    def test_move_forward_facing_W_with_obstacle(self, mock_input):
        mock_input.side_effect = [16, 15]
        self.robot.pos_x = 1
        self.robot.pos_y = 1
        self.robot.facing = self.robot.W
        self.assertEqual('(1,1,W)(0,1)', self.robot.execute_command('f'))

    # Testing combination of commands
    @patch.object(GPIO, 'input')
    def test_command_string_length3_distinct_with_obstacle(self, mock_input):
        mock_input.side_effect = [54, 0, 52, 52, 10]
        self.robot.execute_command('f')
        self.robot.execute_command('r')
        self.assertEqual('(0,1,E)(1,1)', self.robot.execute_command('f'))

    @patch.object(GPIO, 'input')
    def test_command_string_length6_distinct_with_obstacle(self, mock_input):
        mock_input.side_effect = [21, 0, 20, 82, 19, 18, 0, 18, 18, 45]
        self.robot.execute_command('f')
        self.robot.execute_command('f')
        self.robot.execute_command('r')
        self.robot.execute_command('f')
        self.robot.execute_command('l')
        self.assertEqual('(1,1,N)(1,2)', self.robot.execute_command('f'))
