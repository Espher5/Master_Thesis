import unittest
from unittest.mock import patch
import mock.GPIO as GPIO
from SmartHome import SmartHome


class US05(unittest.TestCase):
    def setUp(self) -> None:
        self.sh = SmartHome()

    @patch.object(GPIO, 'input')
    def test_buzzer_on_gas_detected(self, mock_gas):
        mock_gas.return_value = 0
        self.sh.monitor_air_quality()
        buzzer_on = self.sh.buzzer_on
        self.assertTrue(buzzer_on)

    @patch.object(GPIO, 'input')
    def test_buzzer_off_gas_detected(self, mock_gas):
        mock_gas.return_value = 1
        self.sh.monitor_air_quality()
        buzzer_on = self.sh.buzzer_on
        self.assertFalse(buzzer_on)
