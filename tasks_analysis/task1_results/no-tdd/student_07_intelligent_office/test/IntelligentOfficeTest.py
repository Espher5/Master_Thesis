import unittest
from unittest.mock import patch
import mock.GPIO as GPIO
from mock.RTC import RTC
from IntelligentOffice import IntelligentOffice
from IntelligentOfficeError import IntelligentOfficeError


class IntelligentOfficeTest(unittest.TestCase):
    """
    Define your test cases here
    """

    def setUp(self) -> None:
        self.io = IntelligentOffice()

    @patch.object(GPIO, 'input')
    def test_check_quadrant_occupancy_pin_one_false(self, mock_input):
        mock_input.return_value = 0
        occ = self.io.check_quadrant_occupancy(self.io.INFRARED_PIN_1)
        self.assertFalse(occ)

    @patch.object(GPIO, 'input')
    def test_check_quadrant_occupancy_pin_one_true(self, mock_input):
        mock_input.return_value = 50
        occ = self.io.check_quadrant_occupancy(self.io.INFRARED_PIN_1)
        self.assertTrue(occ)

    def test_check_quadrant_occupancy_wrong_pin(self):
        self.assertRaises(IntelligentOfficeError, self.io.check_quadrant_occupancy, 10)

    @patch.object(RTC, 'get_current_time_string')
    @patch.object(RTC, 'get_current_day')
    def test_manage_blinds_based_on_time_true(self, mock_rtc1, mock_rtc2):
        mock_rtc1.return_value = "MONDAY"
        mock_rtc2.return_value = "08:00:59"
        self.io.manage_blinds_based_on_time()
        self.assertTrue(self.io.is_blinds_open())

    @patch.object(RTC, 'get_current_time_string')
    @patch.object(RTC, 'get_current_day')
    def test_manage_blinds_based_on_time_false_week_end(self, mock_rtc1, mock_rtc2):
        mock_rtc1.return_value = "SUNDAY"
        mock_rtc2.return_value = "08:00:59"
        self.io.manage_blinds_based_on_time()
        self.assertFalse(self.io.is_blinds_open())

    @patch.object(RTC, 'get_current_time_string')
    @patch.object(RTC, 'get_current_day')
    def test_manage_blinds_based_on_time_false(self, mock_rtc1, mock_rtc2):
        mock_rtc1.return_value = "MONDAY"
        mock_rtc2.return_value = "20:00:59"
        self.io.manage_blinds_based_on_time()
        self.assertFalse(self.io.is_blinds_open())

    @patch.object(GPIO, 'input')
    def test_manage_light_level_on_true(self, mock_input):
        mock_input.side_effect = [10, 0, 0, 0, 490]
        self.io.manage_light_level()
        self.assertTrue(self.io.is_light_on())

    @patch.object(GPIO, 'input')
    def test_manage_light_level_on_false(self, mock_input):
        mock_input.side_effect = [10, 0, 0, 0, 510]
        self.io.manage_light_level()
        self.assertFalse(self.io.is_light_on())

    @patch.object(GPIO, 'input')
    def test_manage_light_level_on_true_with_person(self, mock_input):
        mock_input.side_effect = [10, 10, 10, 0, 490]
        self.io.manage_light_level()
        self.assertTrue(self.io.is_light_on())

    @patch.object(GPIO, 'input')
    def test_manage_light_level_on_false_with_no_person(self, mock_input):
        mock_input.side_effect = [0, 0, 0, 0, 0]
        self.io.manage_light_level()
        self.assertFalse(self.io.is_light_on())

    @patch.object(GPIO, 'input')
    def test_monitor_air_quality_fan_on(self, mock_input):
        mock_input.return_value = 800
        self.io.monitor_air_quality()
        self.assertTrue(self.io.fan_switch_on)

    @patch.object(GPIO, 'input')
    def test_monitor_air_quality_fan_off(self, mock_input):
        mock_input.return_value = 490
        self.io.monitor_air_quality()
        self.assertFalse(self.io.fan_switch_on)



