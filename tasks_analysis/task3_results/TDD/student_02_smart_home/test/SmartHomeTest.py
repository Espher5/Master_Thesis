import unittest
from unittest.mock import patch, PropertyMock

import mock.adafruit_dht
import mock.adafruit_dht as adafruit_dht
import mock.GPIO as GPIO
from SmartHome import SmartHome
from SmartHomeError import SmartHomeError


class SmartHomeTest(unittest.TestCase):
    def setUp(self) -> None:
        self.sm = SmartHome()

    @patch.object(GPIO, 'input')
    def test_room_is_occupied(self, mock_input):
        mock_input.return_value = 0
        occ = self.sm.check_room_occupancy()
        self.assertTrue(occ)

    @patch.object(GPIO, 'input')
    def test_room_is_not_occupied(self, mock_input):
        mock_input.return_value = 3
        occ = self.sm.check_room_occupancy()
        self.assertFalse(occ)

    @patch.object(GPIO, 'input')
    def test_turn_on_light_room_occupied(self, mock_input):
        mock_input.return_value = 0
        self.sm.manage_light_level()
        self.assertTrue(self.sm.light_on)

    @patch.object(GPIO, 'input')
    def test_turn_off_light_room_not_occupied(self, mock_input):
        mock_input.return_value = 3
        self.sm.manage_light_level()
        self.assertFalse(self.sm.light_on)

    @patch.object(GPIO, 'input')
    def test_measure_lux(self, mock_input):
        mock_input.return_value = 500
        lux = self.sm.measure_lux()
        self.assertEqual(500, lux)

    @patch.object(GPIO, 'input')
    def test_light_management_room_occupied_and_low_level(self, mock_input):
        mock_input.side_effect = [0, 450]
        self.sm.manage_light_level()
        self.assertTrue(self.sm.light_on)

    @patch.object(GPIO, 'input')
    def test_light_management_room_occupied_and_threshold_level(self, mock_input):
        mock_input.side_effect = [0, 500]
        self.sm.manage_light_level()
        self.assertFalse(self.sm.light_on)

    @patch.object(GPIO, 'input')
    def test_light_management_room_occupied_and_high_level(self, mock_input):
        mock_input.side_effect = [0, 550]
        self.sm.manage_light_level()
        self.assertFalse(self.sm.light_on)

    @patch.object(GPIO, 'input')
    def test_light_management_room_not_occupied_and_low_level(self, mock_input):
        mock_input.side_effect = [3, 450]
        self.sm.manage_light_level()
        self.assertFalse(self.sm.light_on)

    @patch.object(GPIO, 'input')
    def test_light_management_room_not_occupied_and_high_level(self, mock_input):
        mock_input.side_effect = [3, 550]
        self.sm.manage_light_level()
        self.assertFalse(self.sm.light_on)

    @patch('mock.adafruit_dht.DHT11.temperature', new_callable=PropertyMock)
    def test_indoor_lower_outdoor_temp(self, mock_temperature):
        mock_temperature.side_effect = [18, 20]
        self.sm.manage_window()
        self.assertTrue(self.sm.window_open)

    @patch('mock.adafruit_dht.DHT11.temperature', new_callable=PropertyMock)
    def test_indoor_lower_outdoor_temp_example2(self, mock_temperature):
        mock_temperature.side_effect = [18, 25]
        self.sm.manage_window()
        self.assertTrue(self.sm.window_open)

    @patch('mock.adafruit_dht.DHT11.temperature', new_callable=PropertyMock)
    def test_indoor_lower_outdoor_temp_out_of_range(self, mock_temperature):
        mock_temperature.side_effect = [29, 31]
        self.sm.manage_window()
        self.assertFalse(self.sm.window_open)

    @patch('mock.adafruit_dht.DHT11.temperature', new_callable=PropertyMock)
    def test_indoor_lower_outdoor_temp_out_of_range_example2(self, mock_temperature):
        mock_temperature.side_effect = [17, 19]
        self.sm.manage_window()
        self.assertFalse(self.sm.window_open)

    @patch('mock.adafruit_dht.DHT11.temperature', new_callable=PropertyMock)
    def test_indoor_higher_outdoor_temp(self, mock_temperature):
        mock_temperature.side_effect = [20, 18]
        self.sm.manage_window()
        self.assertFalse(self.sm.window_open)

    @patch('mock.adafruit_dht.DHT11.temperature', new_callable=PropertyMock)
    def test_indoor_higher_outdoor_temp_example2(self, mock_temperature):
        mock_temperature.side_effect = [25, 20]
        self.sm.manage_window()
        self.assertFalse(self.sm.window_open)

    @patch.object(GPIO, 'input')
    def test_air_quality_500_PPM_or_above(self, mock_gas):
        mock_gas.return_value = 0
        self.sm.monitor_air_quality()
        self.assertTrue(self.sm.buzzer_on)

    @patch.object(GPIO, 'input')
    def test_air_quality_below_500_PPM(self, mock_gas):
        mock_gas.return_value = 1
        self.sm.monitor_air_quality()
        self.assertFalse(self.sm.buzzer_on)
