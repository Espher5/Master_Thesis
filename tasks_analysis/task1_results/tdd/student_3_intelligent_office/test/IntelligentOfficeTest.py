import unittest
from unittest.mock import patch
import mock.GPIO as GPIO
from mock.RTC import RTC
from IntelligentOffice import IntelligentOffice
from IntelligentOfficeError import IntelligentOfficeError


class IntelligentOfficeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.io = IntelligentOffice()

    @patch.object(GPIO, "input")
    def test_quadrant1_is_occupied(self, mock_input):
        mock_input.return_value = 20
        occ = self.io.check_quadrant_occupancy(self.io.INFRARED_PIN_1)
        self.assertTrue(occ)

    @patch.object(GPIO, "input")
    def test_quadrant1_is_not_occupied(self, mock_input):
        mock_input.return_value = 0
        occ = self.io.check_quadrant_occupancy(self.io.INFRARED_PIN_1)
        self.assertFalse(occ)

    def test_occupancy_invaild_pin(self):
        self.assertRaises(IntelligentOfficeError, self.io.check_quadrant_occupancy, -1)

    @patch.object(RTC, "get_current_day")
    @patch.object(RTC, "get_current_time_string")
    def test_open_blinds(self, mock_rtc_time, mock_rtc_day):
        mock_rtc_time.return_value = '08:00:00'
        mock_rtc_day.return_value = 'MONDAY'
        self.io.manage_blinds_based_on_time()
        self.assertTrue(self.io.blinds_open)

    @patch.object(RTC, "get_current_day")
    @patch.object(RTC, "get_current_time_string")
    def test_close_blinds(self, mock_rtc_time, mock_rtc_day):
        mock_rtc_time.return_value = '20:00:00'
        mock_rtc_day.return_value = 'MONDAY'
        self.io.manage_blinds_based_on_time()
        self.assertFalse(self.io.blinds_open)

    @patch.object(RTC, "get_current_day")
    @patch.object(RTC, "get_current_time_string")
    def test_blinds_are_open_example(self, mock_rtc_time, mock_rtc_day):
        mock_rtc_time.return_value = '18:15:00'
        mock_rtc_day.return_value = 'TUESDAY'
        self.io.manage_blinds_based_on_time()
        self.assertTrue(self.io.blinds_open)

    @patch.object(RTC, "get_current_day")
    @patch.object(RTC, "get_current_time_string")
    def test_blinds_are_closed_example(self, mock_rtc_time, mock_rtc_day):
        mock_rtc_time.return_value = '22:15:00'
        mock_rtc_day.return_value = 'TUESDAY'
        self.io.manage_blinds_based_on_time()
        self.assertFalse(self.io.blinds_open)

    @patch.object(GPIO, "input")
    def test_turn_light_on(self, mock_input):
        mock_input.return_value = 400
        self.io.manage_light_level()
        self.assertTrue(self.io.light_on)

    @patch.object(GPIO, "input")
    def test_light_is_on(self, mock_input):
        mock_input.return_value = 510
        self.io.manage_light_level()
        self.assertTrue(self.io.light_on)

    @patch.object(GPIO, "input")
    def test_turn_light_off(self, mock_input):
        mock_input.return_value = 555
        self.io.manage_light_level()
        self.assertFalse(self.io.light_on)
