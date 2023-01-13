import unittest
from unittest.mock import patch, PropertyMock, Mock

import mock.adafruit_dht as adafruit_dht
import mock.GPIO as GPIO
from SmartHome import SmartHome
from SmartHomeError import SmartHomeError


class SmartHomeTest(unittest.TestCase):
    """
    Your test cases go here
    """
    def setUp(self):
        self.home = SmartHome()

    @patch("mock.GPIO.input")
    def test_smart_home_user_detection(self, mock_input):
        #Non-zero value: nothing is detected in front of the sensor.
        #Zero value: it indicates that an object is present in front of the sensor (i.e.,a person).
        mock_input.return_value = 0
        self.assertTrue(self.home.check_room_occupancy())

        #Boundary scan
        for i in range(1,1024):
            mock_input.return_value = i
            self.assertFalse(self.home.check_room_occupancy())

    @patch("mock.GPIO.input")
    @patch("SmartHome.SmartHome.measure_lux")
    def test_smart_home_smart_light_bulb(self, meassure_lux, mock_input):
        mock_input.return_value = 0 #Human detected
        meassure_lux.return_value = 499#Actually test should still work without this, because light will be put on when its to dark. Return val was 0. But changed for completion.
        self.home.manage_light_level()
        self.assertTrue(self.home.light_on)

        # Boundary scan
        for i in range(1, 1024):
            mock_input.return_value = i
            self.home.manage_light_level()
            self.assertFalse(self.home.light_on)

    @patch("mock.GPIO.input")
    def test_smart_home_meassure_lux(self, mock_input):
        # Boundary scan
        for i in range(0, 1024):
            mock_input.return_value = i
            lux = self.home.measure_lux()
            self.assertEqual(i, lux)
    @patch("mock.GPIO.input")
    @patch("SmartHome.SmartHome.measure_lux")
    def test_smart_home_smart_light_bulb_manage_by_light_level(self, measure_lux, mock_input):
        mock_input.return_value = 0  # Human detected

        #Ambient light is sufficient. Getting darker
        for i in reversed(range(1024, 500)):
            measure_lux.return_value = i
            self.home.manage_light_level()
            self.assertFalse(self.home.light_on)

        #It got dark
        for i in reversed(range(0, 499)):
            measure_lux.return_value = i
            self.home.manage_light_level()
            self.assertTrue(self.home.light_on)

        #Keep light on, until no pressence detected
        for i in range(0, 1024):
            measure_lux.return_value = i
            self.home.manage_light_level()
            self.assertTrue(self.home.light_on)

        mock_input.return_value = 1023  # Human went home

        for i in reversed(range(0, 1024)):
            measure_lux.return_value = i
            self.home.manage_light_level()
            self.assertFalse(self.home.light_on)

        for i in range(0, 1024):
            measure_lux.return_value = i
            self.home.manage_light_level()
            self.assertFalse(self.home.light_on)

    @patch("mock.adafruit_dht.DHT11.temperature", new_callable=PropertyMock)
    def test_smart_home_read_temperature(self, mock_dht_temperature):
        for i in range(-100,100):
            mock_dht_temperature.return_value = i
            self.assertEqual(i, self.home.get_indoor_temp())

        for i in range(-100,100):
            mock_dht_temperature.return_value = i
            self.assertEqual(i, self.home.get_outdoor_temp())

    #Task: indoor temperature is lower than the outdoor temperature, mock outdoor and indoor temp
    @patch("SmartHome.SmartHome.get_indoor_temp")
    @patch("SmartHome.SmartHome.get_outdoor_temp")
    def test_smart_home_manage_window(self, mock_outdoor, mock_indoor):
        #Boundary rule scan
        for indoor_temp in range(0, 100):
            for outdoor_temp in reversed(range(0, 100)):
                mock_indoor.return_value = indoor_temp
                mock_outdoor.return_value = outdoor_temp
                self.home.manage_window()

                if indoor_temp in range(18, 31) and outdoor_temp in range(18, 31):
                    if indoor_temp < outdoor_temp - 2:
                        self.assertTrue(self.home.window_open)
                    elif indoor_temp > outdoor_temp + 2:
                        self.assertFalse(self.home.window_open)
                else:
                    self.assertFalse(self.home.window_open)

    @patch('SmartHome.SmartHome.get_outdoor_temp')
    @patch('SmartHome.SmartHome.get_indoor_temp')
    def test_smart_home_manage_window_runtime_exception_test(self, mock_indoor, mock_outdoor):
        mock_outdoor.side_effect = RuntimeError("somearg")
        self.home.window_open = True #Window is open
        mock_indoor.return_value = 9999

        self.home.manage_window()

        self.assertTrue(self.home.window_open) #Window should be still open due to exception

    @patch('SmartHome.SmartHome.get_outdoor_temp')
    @patch('SmartHome.SmartHome.get_indoor_temp')
    def test_smart_home_manage_window_exception_test(self, mock_indoor, mock_outdoor):
        mock_outdoor.side_effect = Exception()
        self.home.window_open = True  # Window is open
        mock_indoor.return_value = 9999

        self.assertRaises(Exception, self.home.manage_window)
        self.assertTrue(self.home.window_open)  # Window should be still open due to exception

    @patch("mock.GPIO.input")
    def test_smart_home_meassure_gas(self, mock_input):
        # Boundary scan, no gas

        #I check from 1 to 1023 as "True" representation for the case the gas sensor is connected to an ADC, why?
        #Because i didnt understand where actually is defined what an ADC or Digital Pin is.
        #Because i know the presentation matches
        #val: 1-1023 => True
        #val: 0 => False

        #No gas
        for i in range(1, 1024):
            mock_input.return_value = i
            self.home.monitor_air_quality()
            self.assertFalse(self.home.buzzer_on)

        #Gas detected
        mock_input.return_value = 0
        self.home.monitor_air_quality()
        self.assertTrue(self.home.buzzer_on)

        # Gas goes away
        for i in range(1, 1024):
            mock_input.return_value = i
            self.home.monitor_air_quality()
            self.assertFalse(self.home.buzzer_on)