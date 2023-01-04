import unittest
from unittest.mock import patch
import mock.GPIO as GPIO

from IntelligentOffice import IntelligentOffice


class US04(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.io = IntelligentOffice()

    @patch.object(GPIO, 'input')
    def test_light_off_no_workers(self, mock_input):
        mock_input.side_effect = [0, 0, 0, 0]
        self.io.manage_light_level()
        light = self.io.light_on
        self.assertFalse(light)

    @patch.object(GPIO, 'input')
    def test_light_on_one_worker1(self, mock_input):
        mock_input.side_effect = [43, 450]
        self.io.manage_light_level()
        light = self.io.light_on
        self.assertTrue(light)

    @patch.object(GPIO, 'input')
    def test_light_on_one_worker2(self, mock_input):
        mock_input.side_effect = [0, 0, 0, 12, 450]
        self.io.manage_light_level()
        light = self.io.light_on
        self.assertTrue(light)

    @patch.object(GPIO, 'input')
    def test_light_off_one_worker(self, mock_input):
        mock_input.side_effect = [43, 520]
        self.io.manage_light_level()
        light = self.io.light_on
        self.assertFalse(light)

