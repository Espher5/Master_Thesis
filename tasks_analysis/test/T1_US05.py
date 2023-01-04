import unittest
from unittest.mock import patch
import mock.GPIO as GPIO

from IntelligentOffice import IntelligentOffice


class US05(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.io = IntelligentOffice()

    @patch.object(GPIO, 'input')
    def test_vent_off(self, mock_input):
        mock_input.return_value = 790
        self.io.monitor_air_quality()
        fan_on = self.io.fan_switch_on
        self.assertFalse(fan_on)

    @patch.object(GPIO, 'input')
    def test_vent_on(self, mock_input):
        mock_input.return_value = 810
        self.io.monitor_air_quality()
        fan_on = self.io.fan_switch_on
        self.assertTrue(fan_on)

    @patch.object(GPIO, 'input')
    def test_vent_on_off(self, mock_input):
        mock_input.return_value = 820
        self.io.monitor_air_quality()
        mock_input.return_value = 780
        self.io.monitor_air_quality()
        mock_input.return_value = 700
        self.io.monitor_air_quality()
        mock_input.return_value = 620
        self.io.monitor_air_quality()
        mock_input.return_value = 512
        self.io.monitor_air_quality()
        mock_input.return_value = 490
        self.io.monitor_air_quality()

        fan_on = self.io.fan_switch_on
        self.assertFalse(fan_on)
