import unittest
from unittest.mock import patch, PropertyMock

import mock.adafruit_dht as adafruit_dht
import mock.GPIO as GPIO
from SmartHome import SmartHome
from SmartHomeError import SmartHomeError


class SmartHomeTest(unittest.TestCase):
    """
    Your test cases go here
    """
    def setUp(self) -> None:
        self.sm = SmartHome()

    @patch.object(GPIO, "input")
    def test_check_room_occupancy_true(self, mock_input):
        mock_input.return_value = 0
        occ = self.sm.check_room_occupancy()
        self.assertTrue(occ)

    @patch.object(GPIO, "input")
    def test_check_room_occupancy_false(self, mock_input):
        mock_input.return_value = 1
        occ = self.sm.check_room_occupancy()
        self.assertFalse(occ)

    @patch.object(GPIO, "input")
    def test_manage_light_level_on(self, mock_input):
        mock_input.side_effect = [0, 499]
        self.sm.manage_light_level()
        light_on = self.sm.light_on
        self.assertTrue(light_on)

    @patch.object(GPIO, "input")
    def test_manage_light_level_off_high_lux(self, mock_input):
        mock_input.side_effect = [0, 600]
        self.sm.manage_light_level()
        light_on = self.sm.light_on
        self.assertFalse(light_on)

    @patch.object(GPIO, "input")
    def test_manage_light_level_off(self, mock_input):
        mock_input.return_value = [1, 499]
        self.sm.manage_light_level()
        light_on = self.sm.light_on
        self.assertFalse(light_on)

    @patch.object(GPIO, "input")
    def test_manage_light_level_off_high_lux(self, mock_input):
        mock_input.return_value = [1, 600]
        self.sm.manage_light_level()
        light_on = self.sm.light_on
        self.assertFalse(light_on)

    @patch('mock.adafruit_dht.DHT11.temperature', new_callable=PropertyMock)
    def test_manage_window_open_window(self, mock_temperature):
        mock_temperature.side_effect = [18.0, 21.1, 18.0, 21.1]
        self.sm.manage_window()
        window_open = self.sm.window_open
        self.assertTrue(window_open)

    @patch('mock.adafruit_dht.DHT11.temperature', new_callable=PropertyMock)
    def test_manage_window_close_window(self, mock_temperature):
        mock_temperature.side_effect = [23.2, 19.1, 23.2, 19.1, 23.2, 19.1]
        self.sm.manage_window()
        window_open = self.sm.window_open
        self.assertFalse(window_open)

    @patch('mock.adafruit_dht.DHT11.temperature', new_callable=PropertyMock)
    def test_manage_window_temperature_out_of_range_1(self, mock_temperature):
        mock_temperature.side_effect = [16.8, 20.2]
        self.sm.manage_window()
        window_open = self.sm.window_open
        self.assertFalse(window_open)

    @patch('mock.adafruit_dht.DHT11.temperature', new_callable=PropertyMock)
    def test_manage_window_temperature_out_of_range_2(self, mock_temperature):
        mock_temperature.side_effect = [18.2, 31.0]
        self.sm.manage_window()
        window_open = self.sm.window_open
        self.assertFalse(window_open)

    @patch.object(GPIO, "input")
    def test_monitor_air_quality_buzzer_on(self, mock_input):
        mock_input.return_value = 0
        self.sm.monitor_air_quality()
        buzzer_on = self.sm.buzzer_on
        self.assertTrue(buzzer_on)

    @patch.object(GPIO, "input")
    def test_monitor_air_quality_buzzer_off(self, mock_input):
        mock_input.return_value = 1
        self.sm.monitor_air_quality()
        buzzer_on = self.sm.buzzer_on
        self.assertFalse(buzzer_on)

