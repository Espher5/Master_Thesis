import unittest
from unittest.mock import patch
from CleaningRobot import CleaningRobot
from CleaningRobotError import CleaningRobotError
import mock.GPIO as GPIO


class CleaningRobotTest(unittest.TestCase):
    """
    Your tests go here
    """
    def setUp(self) -> None:
        self.cr = CleaningRobot(2, 2)

    @patch.object(GPIO, "input")
    def test_initialize_robot(self, mock_input):
        mock_input.return_value = 4
        self.cr.initialize_robot()
        self.assertEqual(self.cr.pos_x, 0)
        self.assertEqual(self.cr.pos_y, 0)
        self.assertEqual(self.cr.facing, "N")

    #@patch.object()
    #def test_robot_status(self):

    @patch.object(GPIO, "input")
    def test_low_battery(self, mock_input):
        mock_input.return_value = 8
        self.cr.manage_battery()
        self.assertEqual(self.cr.battery_led_on, True)
        self.assertEqual(self.cr.cleaning_system_on, False)

    @patch.object(GPIO, "input")
    def test_not_low_battery(self, mock_input):
        mock_input.return_value = 80
        self.cr.manage_battery()
        self.assertEqual(self.cr.battery_led_on, False)
        self.assertEqual(self.cr.cleaning_system_on, True)

