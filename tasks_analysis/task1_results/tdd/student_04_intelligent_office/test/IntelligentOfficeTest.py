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
    def test_check_quadrant_occupancy_true(self, mock_input):
        mock_input.return_value = 5
        result = self.io.check_quadrant_occupancy(IntelligentOffice.INFRARED_PIN_1)
        self.assertTrue(result)

    @patch.object(GPIO, 'input')
    def test_check_quadrant_occupancy_false(self, mock_input):
        mock_input.return_value = 0
        result = self.io.check_quadrant_occupancy(IntelligentOffice.INFRARED_PIN_1)
        self.assertFalse(result)

    def test_check_quadrant_occupancy_error(self):
        self.assertRaises(IntelligentOfficeError, self.io.check_quadrant_occupancy, 4)

    @patch.object(RTC, 'get_current_time_string')
    @patch.object(RTC, 'get_current_day')
    def test_manage_blinds_based_on_time_true(self, rtc_day, rtc_time):
        rtc_time.return_value = "09:00:00"
        rtc_day.return_value = "MONDAY"
        self.io.manage_blinds_based_on_time()
        result = self.io.open_blinds()
        self.assertTrue(result)

    @patch.object(RTC, 'get_current_time_string')
    @patch.object(RTC, 'get_current_day')
    def test_manage_blinds_based_on_time_false(self, rtc_day, rtc_time):
        rtc_time.return_value = "22:00:00"
        rtc_day.return_value = "MONDAY"
        self.io.manage_blinds_based_on_time()
        result = self.io.open_blinds()
        self.assertFalse(result)

    @patch.object(GPIO, 'input')
    def test_manage_light_level_on(self, mock_input):
        mock_input.return_value = 499
        self.io.manage_light_level()
        light = self.io.light()
        self.assertTrue(light)

    @patch.object(GPIO, 'input')
    def test_manage_light_level_off(self, mock_input):
        mock_input.return_value = 501
        self.io.manage_light_level()
        light = self.io.light()
        self.assertFalse(light)

    @patch.object(GPIO, 'input')
    def test_manage_light_level_off_nothing(self, mock_input):
        mock_input.return_value = 0
        self.io.manage_light_level()
        light = self.io.light()
        self.assertFalse(light)

    @patch.object(GPIO, 'input')
    def test_monitor_air_quality_co2_high(self, mock_input):
        mock_input.return_value = 800
        self.io.monitor_air_quality()
        co2 = self.io.co2()
        self.assertTrue(co2)

    @patch.object(GPIO, 'input')
    def test_monitor_air_quality_co2_low(self, mock_input):
        mock_input.return_value = 400
        self.io.monitor_air_quality()
        co2 = self.io.co2()
        self.assertIsNone(co2)







