import unittest
from unittest.mock import patch
from CleaningRobot import CleaningRobot
from CleaningRobotError import CleaningRobotError


class CleaningRobotTest(unittest.TestCase):
    def setUp(self) -> None:
        self.cl = CleaningRobot(3,3)

    def test_robot_status(self):
        self.cl.pos_x = 1
        self.cl.pos_y = 1
        self.cl.facing = 'S'
        status = self.cl.robot_status()
        self.assertEqual("(1,1,S)", status)

    @patch("mock.GPIO.input")
    def test_IBS_low(self, mock_input):
        mock_input.return_value = 10
        self.cl.manage_battery()
        self.assertFalse(self.cl.cleaning_system_on)
        self.assertTrue(self.cl.battery_led_on)

    @patch("mock.GPIO.input")
    def test_IBS_high(self, mock_input):
        mock_input.return_value = 20
        self.cl.manage_battery()
        self.assertTrue(self.cl.cleaning_system_on)
        self.assertFalse(self.cl.battery_led_on)

    def test_execute_command_example1(self):
        self.cl.pos_x = 0
        self.cl.pos_y = 0
        self.cl.facing = 'N'
        status = self.cl.execute_command('f')
        self.assertEqual("(0,1,N)", status)

    def test_execute_command_example2(self):
        self.cl.pos_x = 0
        self.cl.pos_y = 0
        self.cl.facing = 'N'
        status = self.cl.execute_command('r')
        self.assertEqual("(0,0,E)", status)

    def test_execute_command_example3(self):
        self.cl.pos_x = 0
        self.cl.pos_y = 0
        self.cl.facing = 'N'
        status = self.cl.execute_command('l')
        self.assertEqual("(0,0,W)", status)

    def test_execute_command_example4(self):
        self.cl.pos_x = 1
        self.cl.pos_y = 1
        self.cl.facing = 'N'
        status = self.cl.execute_command('f')
        self.assertEqual("(1,2,N)", status)

    @patch("mock.GPIO.input")
    def test_obstacle_found(self, mock_input):
        mock_input.return_value = 10
        self.assertTrue(self.cl.obstacle_found())

    @patch("mock.GPIO.input")
    def test_no_obstacle_found(self, mock_input):
        mock_input.return_value = 0
        self.assertFalse(self.cl.obstacle_found())