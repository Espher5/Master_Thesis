import unittest
from unittest.mock import patch
import mock.GPIO as GPIO
from SmartHome import SmartHome


class US01(unittest.TestCase):
    def setUp(self) -> None:
        self.sh = SmartHome()

    @patch.object(GPIO, 'input')
    def test_user_detection_true(self, mock_input):
        mock_input.return_value = 0
        occ = self.sh.check_room_occupancy()
        self.assertTrue(occ)

    @patch.object(GPIO, 'input')
    def test_user_detection_false(self, mock_input):
        mock_input.return_value = 12
        occ = self.sh.check_room_occupancy()
        self.assertFalse(occ)
