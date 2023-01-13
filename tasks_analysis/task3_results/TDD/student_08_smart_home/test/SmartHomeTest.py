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
        self.s_h = SmartHome()

    @patch.object(GPIO, 'input')
    def test_occupancy(self, mock):
        mock.return_value = 0
        occ = self.s_h.check_room_occupancy()
        self.assertTrue(occ)

    @patch.object(GPIO, "input")
    def test_light_level_someone_is_inside_and_lux_under_500(self, mock):
        mock.side_effect = [0, 499]
        self.s_h.manage_light_level()
        light_bulb = self.s_h.light_on
        self.assertTrue(light_bulb)

    @patch.object(GPIO, "input")
    def test_light_level_someone_is_inside_and_lux_over_500(self, mock):
        mock.side_effect = [0, 730]
        self.s_h.manage_light_level()
        light_bulb = self.s_h.light_on
        self.assertFalse(light_bulb)


    @patch('mock.adafruit_dht.DHT11.temperature', new_callable=PropertyMock)
    def test_opens_window_outdoor_is_higher(self, mock):
        mock.side_effect = [21, 28]
        self.s_h.manage_window()
        window = self.s_h.window_open
        self.assertTrue(window)

    @patch('mock.adafruit_dht.DHT11.temperature', new_callable=PropertyMock)
    def test_close_window_indoor_is_higher(self, mock):
        mock.side_effect = [27, 19]
        self.s_h.manage_window()
        window = self.s_h.window_open
        self.assertFalse(window)

    @patch.object(GPIO, "input")
    def test_sensor_starts_returning_0(self, mock):
        mock.return_value = 0
        self.s_h.monitor_air_quality()
        buzzer_on = self.s_h.buzzer_on
        self.assertTrue(buzzer_on)

    @patch.object(GPIO, "input")
    def test_sensor_returns_constant_1(self, mock):
        mock.return_value = 1
        self.s_h.monitor_air_quality()
        buzzer_on = self.s_h.buzzer_on
        self.assertFalse(buzzer_on)