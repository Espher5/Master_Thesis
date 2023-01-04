import unittest
from unittest.mock import patch
import mock.GPIO as GPIO

from IntelligentOffice import IntelligentOffice
from IntelligentOfficeError import IntelligentOfficeError


class US01(unittest.TestCase):
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
    def test_quadrant_2_occupancy_true(self, mock_input):
        mock_input.return_value = 56
        occ = self.io.check_quadrant_occupancy(IntelligentOffice.INFRARED_PIN_2)
        self.assertTrue(occ)

    @patch.object(GPIO, 'input')
    def test_quadrant_2_occupancy_false(self, mock_input):
        mock_input.return_value = 0
        occ = self.io.check_quadrant_occupancy(IntelligentOffice.INFRARED_PIN_2)
        self.assertFalse(occ)

    @patch.object(GPIO, 'input')
    def test_quadrant_3_occupancy_true(self, mock_input):
        mock_input.return_value = 7
        occ = self.io.check_quadrant_occupancy(IntelligentOffice.INFRARED_PIN_3)
        self.assertTrue(occ)

    @patch.object(GPIO, 'input')
    def test_quadrant_3_occupancy_false(self, mock_input):
        mock_input.return_value = 0
        occ = self.io.check_quadrant_occupancy(IntelligentOffice.INFRARED_PIN_3)
        self.assertFalse(occ)

    @patch.object(GPIO, 'input')
    def test_quadrant_4_occupancy_true(self, mock_input):
        mock_input.return_value = 84
        occ = self.io.check_quadrant_occupancy(IntelligentOffice.INFRARED_PIN_4)
        self.assertTrue(occ)

    @patch.object(GPIO, 'input')
    def test_quadrant_4_occupancy_false(self, mock_input):
        mock_input.return_value = 0
        occ = self.io.check_quadrant_occupancy(IntelligentOffice.INFRARED_PIN_4)
        self.assertFalse(occ)

    @patch.object(GPIO, 'input')
    def test_quadrant_occupancy_invalid_pin(self, mock_input):
        mock_input.return_value = 0
        self.assertRaises(IntelligentOfficeError, self.io.check_quadrant_occupancy, -1)

