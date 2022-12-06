import unittest
from unittest.mock import patch
import mock.GPIO as GPIO
from mock.RTC import RTC
from IntelligentOffice import IntelligentOffice
from IntelligentOfficeError import IntelligentOfficeError


class IntelligentOfficeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.io = IntelligentOffice()

    @patch.object(GPIO, 'input')
    def test_quadrant_1_occupancy_true(self, mock_input):
        mock_input.return_value = 12
        occ = self.io.check_quadrant_occupancy(IntelligentOffice.INFRARED_PIN_1)
        self.assertTrue(occ)

    @patch.object(GPIO, 'input')
    def test_quadrant_1_occupancy_false(self, mock_input):
        mock_input.return_value = 0
        occ = self.io.check_quadrant_occupancy(IntelligentOffice.INFRARED_PIN_1)
        self.assertFalse(occ)

    @patch.object(GPIO, 'input')
    def test_quadrant_occupancy_invalid_pin(self, mock_input):
        mock_input.return_value = 0
        self.assertRaises(IntelligentOfficeError, self.io.check_quadrant_occupancy, -1)

    @patch.object('')
    def test_open_blinds_8am_monday(self):