import unittest
from unittest.mock import patch
import mock.GPIO as GPIO
from CleaningRobot import CleaningRobot


class US03(unittest.TestCase):
    def setUp(self) -> None:
        self.robot = CleaningRobot(10, 10)
        self.robot.initialize_robot()
        self.robot.pos_x = 0
        self.robot.pos_y = 0

    # Turning tests
    def test_left_rotation_from_00N(self):
        self.robot.facing = self.robot.N
        self.assertEqual('(0,0,W)', self.robot.execute_command('l'))

    def test_left_rotation_from_00E(self):
        self.robot.facing = self.robot.E
        self.assertEqual('(0,0,N)', self.robot.execute_command('l'))

    def test_left_rotation_from_00S(self):
        self.robot.facing = self.robot.S
        self.assertEqual('(0,0,E)', self.robot.execute_command('l'))

    def test_left_rotation_from_00W(self):
        self.robot.facing = self.robot.W
        self.assertEqual('(0,0,S)', self.robot.execute_command('l'))

    def test_right_rotation_from_00N(self):
        self.robot.facing = self.robot.N
        self.assertEqual('(0,0,E)', self.robot.execute_command('r'))

    def test_right_rotation_from_00E(self):
        self.robot.facing = self.robot.E
        self.assertEqual('(0,0,S)', self.robot.execute_command('r'))

    def test_right_rotation_from_00S(self):
        self.robot.facing = self.robot.S
        self.assertEqual('(0,0,W)', self.robot.execute_command('r'))

    def test_right_rotation_from_00W(self):
        self.robot.facing = self.robot.W
        self.assertEqual('(0,0,N)', self.robot.execute_command('r'))

    # Forward movement tests
    @patch.object(GPIO, 'input')
    def test_move_forward_facing_N(self, mock_input):
        mock_input.return_value = 0
        self.robot.facing = self.robot.N
        self.assertEqual('(0,1,N)', self.robot.execute_command('f'))

    @patch.object(GPIO, 'input')
    def test_move_forward_facing_E(self, mock_input):
        mock_input.return_value = 0
        self.robot.facing = self.robot.E
        self.assertEqual('(1,0,E)', self.robot.execute_command('f'))

    @patch.object(GPIO, 'input')
    def test_move_forward_facing_S(self, mock_input):
        mock_input.return_value = 0
        self.robot.pos_x = 1
        self.robot.pos_y = 1
        self.robot.facing = self.robot.S
        self.assertEqual('(1,0,S)', self.robot.execute_command('f'))

    @patch.object(GPIO, 'input')
    def test_move_forward_facing_W(self, mock_input):
        mock_input.return_value = 0
        self.robot.pos_x = 1
        self.robot.pos_y = 1
        self.robot.facing = self.robot.W
        self.assertEqual('(0,1,W)', self.robot.execute_command('f'))
