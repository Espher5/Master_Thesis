import unittest
from unittest.mock import patch
import mock.GPIO as GPIO
from SmartHome import SmartHome


class US03(unittest.TestCase):
    def setUp(self) -> None:
        self.sh = SmartHome()

    @patch.object(SmartHome, 'measure_lux')
    @patch.object(GPIO, 'input')
    def test_light_off_no_user(self, mock_input, mock_lux):
        mock_input.return_value = 1
        mock_lux.return_value = 500
        self.sh.manage_light_level()
        light_on = self.sh.light_on
        self.assertFalse(light_on)

    @patch.object(SmartHome, 'measure_lux')
    @patch.object(GPIO, 'input')
    def test_light_off_user(self, mock_input, mock_lux):
        mock_input.return_value = 0
        mock_lux.return_value = 500
        self.sh.manage_light_level()
        light_on = self.sh.light_on
        self.assertFalse(light_on)

    @patch.object(SmartHome, 'measure_lux')
    @patch.object(GPIO, 'input')
    def test_light_off_user(self, mock_input, mock_lux):
        mock_input.return_value = 0
        mock_lux.return_value = 400
        self.sh.manage_light_level()
        light_on = self.sh.light_on
        self.assertTrue(light_on)
