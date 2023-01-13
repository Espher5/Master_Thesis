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
        self.sh = SmartHome()

    @patch.object(GPIO, "input")
    def test_room_occupancy(self, mock_sensor_value):
        mock_sensor_value.return_value = 0
        res = self.sh.check_room_occupancy()
        self.assertTrue(res)

    @patch.object(GPIO, "input")
    def test_room_empty(self, mock_sensor_value):
        mock_sensor_value.return_value = 10
        res = self.sh.check_room_occupancy()
        self.assertFalse(res)

    @patch.object(SmartHome, "measure_lux")
    @patch.object(GPIO, "input")
    def test_turn_light_on(self, mock_sensor_value, mock_light_level):
        mock_light_level.return_value = 490
        mock_sensor_value.return_value = 0
        self.sh.manage_light_level()
        self.assertTrue(self.sh.light_on)

    @patch.object(SmartHome, "measure_lux")
    def test_turn_light_off(self, mock_light_level):
        mock_light_level.return_value = 575
        self.sh.manage_light_level()
        self.assertFalse(self.sh.light_on)

    @patch.object(SmartHome, "measure_lux")
    @patch.object(GPIO, "input")
    def test_turn_light_off_empty_room(self, mock_sensor_value, mock_light_level):
        mock_light_level.return_value = 475
        mock_sensor_value.return_value = 1
        self.sh.manage_light_level()
        self.assertFalse(self.sh.light_on)

    @patch.object(GPIO, "input")
    def test_light_level_valid(self, mock_light_level):
        mock_light_level.return_value = 550
        value = self.sh.measure_lux()
        self.assertEqual(550, value)

    @patch('mock.adafruit_dht.DHT11.temperature', new_callable=PropertyMock)
    def test_window_open_temp_indoor_lower(self, mock_temp_values):
        mock_temp_values.side_effect = [24, 26]
        self.sh.manage_window()
        self.assertTrue(self.sh.window_open)

    @patch('mock.adafruit_dht.DHT11.temperature', new_callable=PropertyMock)
    def test_window_open_temp_indoor_grater(self, mock_temp_values):
        mock_temp_values.side_effect = [23, 21]
        self.sh.manage_window()
        self.assertTrue(self.sh.window_open)

    @patch('mock.adafruit_dht.DHT11.temperature', new_callable=PropertyMock)
    def test_window_close(self, mock_temp_values):
        mock_temp_values.side_effect = [18, 19]
        self.sh.manage_window()
        self.assertFalse(self.sh.window_open)

    @patch('mock.adafruit_dht.DHT11.temperature', new_callable=PropertyMock)
    def test_temp_out_of_range(self, mock_temp_values):
        mock_temp_values.side_effect = [16, 19]
        self.sh.manage_window()
        self.assertFalse(self.sh.window_open)

    @patch.object(GPIO, "input")
    def test_air_quality_below_threshold(self, mock_gas_level):
        mock_gas_level.return_value = 450
        self.sh.monitor_air_quality()
        self.assertFalse(self.sh.buzzer_on)

    @patch.object(GPIO, "input")
    def test_air_quality_above_threshold(self, mock_gas_level):
        mock_gas_level.return_value = 570
        self.sh.monitor_air_quality()
        self.assertTrue(self.sh.buzzer_on)