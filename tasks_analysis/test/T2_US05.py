import unittest
from unittest.mock import patch
import mock.GPIO as GPIO
from CleaningRobot import CleaningRobot


class US05(unittest.TestCase):
    def setUp(self) -> None:
        self.robot = CleaningRobot(10, 10)
        self.robot.initialize_robot()

    @patch.object(GPIO, 'input')
    def test_low_battery_no_movement(self, mock_input):
        mock_input.return_value = 8
        status = self.robot.execute_command('f')

        self.assertEqual('(0,0,N)', status)