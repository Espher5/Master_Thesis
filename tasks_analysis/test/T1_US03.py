import unittest
from unittest.mock import patch
import mock.GPIO as GPIO

from IntelligentOffice import IntelligentOffice


class US03(unittest.TestCase):
    def setUp(self) -> None:
        self.io = IntelligentOffice()

    @patch.object(GPIO, 'input')
    def test_light_off(self, mock_input):
        mock_input.return_value = 520
        self.io.manage_light_level()
        light = self.io.light_on
        self.assertFalse(light)

    @patch.object(GPIO, 'input')
    def test_light_on(self, mock_input):
        mock_input.return_value = 450
        self.io.manage_light_level()
        light = self.io.light_on
        self.assertTrue(light)

    @patch.object(GPIO, 'input')
    def test_light_on_off(self, mock_input):
        mock_input.return_value = 450
        self.io.manage_light_level()
        mock_input.return_value = 560
        self.io.manage_light_level()
        light = self.io.light_on
        self.assertFalse(light)

    @patch.object(GPIO, 'input')
    def test_light_on_on(self, mock_input):
        mock_input.return_value = 360
        self.io.manage_light_level()
        mock_input.return_value = 480
        self.io.manage_light_level()
        light = self.io.light_on
        self.assertTrue(light)

