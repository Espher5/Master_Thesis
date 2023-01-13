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
        self.smart_home = SmartHome()

    '''test: user-story 1'''

    @patch.object(GPIO, 'input')
    def test_check_room_occupancy_true(self, mock_occupancy):
        mock_occupancy.return_value = 0
        occupancy = self.smart_home.check_room_occupancy()
        self.assertTrue(occupancy)

    @patch.object(GPIO, 'input')
    def test_check_room_occupancy_false(self, mock_occupancy):
        mock_occupancy.return_value = 5
        occupancy = self.smart_home.check_room_occupancy()
        self.assertFalse(occupancy)

    '''test: user-story 2 and 3'''

    @patch.object(GPIO, 'input')
    def test_manage_light_level_true_low_lights_and_occupancy_true(self, mock_occupancy):
        mock_occupancy.side_effect = [499, 0]
        self.smart_home.manage_light_level()
        light = self.smart_home.light_status()
        self.assertTrue(light)

    @patch.object(GPIO, 'input')
    def test_manage_light_level_false_low_lights_and_occupancy_false(self, mock_occupancy):
        mock_occupancy.side_effect = [499, 5, 500]
        self.smart_home.manage_light_level()
        light = self.smart_home.light_status()
        self.assertFalse(light)

    @patch.object(GPIO, 'input')
    def test_manage_light_level_false_high_lights_and_occupancy_true(self, mock_occupancy):
        mock_occupancy.side_effect = [500, 0]
        self.smart_home.manage_light_level()
        light = self.smart_home.light_status()
        self.assertFalse(light)

    @patch.object(GPIO, 'input')
    def test_manage_light_level_false_high_lights_and_occupancy_false(self, mock_occupancy):
        mock_occupancy.side_effect = [500, 5, 500]
        self.smart_home.manage_light_level()
        light = self.smart_home.light_status()
        self.assertFalse(light)

    '''test: user-story 4'''

    @patch('mock.adafruit_dht.DHT11.temperature', new_callable=PropertyMock)
    def test_manage_window_false_with_indoor_and_outdoor_temperature_not_in_the_range(self, mock_temperature):
        mock_temperature.side_effect = [32, 35, 0, 0, 0, 0]
        self.smart_home.manage_window()
        window = self.smart_home.window_status()
        self.assertFalse(window)

    @patch('mock.adafruit_dht.DHT11.temperature', new_callable=PropertyMock)
    def test_manage_window_true_with_temperatures_in_the_range_and_indoor_lower_than_outdoor_temperature(self, mock_temperature):
        mock_temperature.side_effect = [22, 24, 20, 24, 24, 24]
        self.smart_home.manage_window()
        window = self.smart_home.window_status()
        self.assertTrue(window)

    @patch('mock.adafruit_dht.DHT11.temperature', new_callable=PropertyMock)
    def test_manage_window_false_with_temperatures_in_the_range_and_indoor_grather_than_outdoor_temperature(self, mock_temperature):
        mock_temperature.side_effect = [24, 22, 24, 22, 24, 24]
        self.smart_home.manage_window()
        window = self.smart_home.window_status()
        self.assertFalse(window)

    '''test: user-story 5'''

    @patch.object(GPIO, 'input')
    def test_monitor_air_quality_with_air_quality_lower_than_500(self, mock_air_quality):
        mock_air_quality.return_value = 499
        self.smart_home.monitor_air_quality()
        buzzer = self.smart_home.buzzer_status()
        self.assertFalse(buzzer)

    @patch.object(GPIO, 'input')
    def test_monitor_air_quality_with_air_quality_grather_than_500(self, mock_air_quality):
        mock_air_quality.return_value = 501
        self.smart_home.monitor_air_quality()
        buzzer = self.smart_home.buzzer_status()
        self.assertTrue(buzzer)
