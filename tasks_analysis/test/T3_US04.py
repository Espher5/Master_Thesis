import unittest
from unittest.mock import patch, PropertyMock

import mock.adafruit_dht as adafruit_dht
from SmartHome import SmartHome


class US04(unittest.TestCase):
    def setUp(self) -> None:
        self.sh = SmartHome()

    @patch('mock.adafruit_dht.DHT11.temperature', new_callable=PropertyMock)
    def test_temperature_reading(self, mock_temperature):
        mock_temperature.return_value = 10
        dht = adafruit_dht.DHT11(23)
        temperature = dht.temperature
        self.assertEqual(10, temperature)

    @patch('mock.adafruit_dht.DHT11.temperature', new_callable=PropertyMock)
    def test_window_closed_temperature_out_of_range(self, mock_temperature):
        mock_temperature.side_effect = [10, 20]
        self.sh.manage_window()
        window_open = self.sh.window_open
        self.assertFalse(window_open)

    @patch('mock.adafruit_dht.DHT11.temperature', new_callable=PropertyMock)
    def test_window_closed_temperature_in_range(self, mock_temperature):
        mock_temperature.side_effect = [30, 25]
        self.sh.manage_window()
        window_open = self.sh.window_open
        self.assertFalse(window_open)

    @patch('mock.adafruit_dht.DHT11.temperature', new_callable=PropertyMock)
    def test_window_open_temperature_in_range(self, mock_temperature):
        mock_temperature.side_effect = [22, 28]
        self.sh.manage_window()
        window_open = self.sh.window_open
        self.assertTrue(window_open)
