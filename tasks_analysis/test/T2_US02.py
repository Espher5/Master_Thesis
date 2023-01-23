import unittest
from unittest.mock import patch
import mock.GPIO as GPIO
from CleaningRobot import CleaningRobot


class US02(unittest.TestCase):
    def setUp(self) -> None:
        self.robot = CleaningRobot(2, 2)

    @patch.object(GPIO, 'input')
    def test_recharge_led_on(self, mock_input):
        mock_input.return_value = 10
        self.robot.manage_battery()

        self.assertTrue(self.robot.battery_led_on)

    @patch.object(GPIO, 'input')
    def test_recharge_led_off(self, mock_input):
        mock_input.return_value = 90
        self.robot.manage_battery()

        self.assertFalse(self.robot.battery_led_on)

    @patch.object(GPIO, 'input')
    def test_cleaning_system_on(self, mock_input):
        mock_input.return_value = 57
        self.robot.manage_battery()

        self.assertTrue(self.robot.cleaning_system_on)

    @patch.object(GPIO, 'input')
    def test_cleaning_system_off(self, mock_input):
        mock_input.return_value = 8
        self.robot.manage_battery()

        self.assertFalse(self.robot.cleaning_system_on)
