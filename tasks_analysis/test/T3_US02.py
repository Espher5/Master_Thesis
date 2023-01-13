import unittest
from unittest.mock import patch
import mock.GPIO as GPIO
from SmartHome import SmartHome


class US02(unittest.TestCase):
    def setUp(self) -> None:
        self.sh = SmartHome()

    @patch.object(GPIO, 'input')
    def test_turn_light_on_occupancy(self, mock_input):
        mock_input.return_value = 0
        self.sh.manage_light_level()
        light_on = self.sh.light_on
        self.assertTrue(light_on)

    @patch.object(GPIO, 'input')
    def test_turn_light_off_occupancy(self, mock_input):
        mock_input.return_value = 1
        self.sh.manage_light_level()
        light_on = self.sh.light_on
        self.assertFalse(light_on)
