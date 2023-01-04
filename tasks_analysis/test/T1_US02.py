import unittest
from unittest.mock import patch
from mock.RTC import RTC

from IntelligentOffice import IntelligentOffice


class US02(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.io = IntelligentOffice()

    @patch.object(RTC, 'get_current_day')
    @patch.object(RTC, 'get_current_time_string')
    def test_blinds_open_8am_monday(self, mock_time, mock_day):
        mock_time.return_value = '08:00:00'
        mock_day.return_value = 'MONDAY'
        self.io.manage_blinds_based_on_time()
        blinds_status = self.io.blinds_open
        self.assertTrue(blinds_status)

    @patch.object(RTC, 'get_current_day')
    @patch.object(RTC, 'get_current_time_string')
    def test_blinds_open_8pm_monday(self, mock_time, mock_day):
        mock_time.return_value = '20:00:00'
        mock_day.return_value = 'MONDAY'
        self.io.manage_blinds_based_on_time()
        blinds_status = self.io.blinds_open
        self.assertTrue(blinds_status)

    @patch.object(RTC, 'get_current_day')
    @patch.object(RTC, 'get_current_time_string')
    def test_blinds_open_5pm_friday(self, mock_time, mock_day):
        mock_time.return_value = '17:00:00'
        mock_day.return_value = 'FRIDAY'
        self.io.manage_blinds_based_on_time()
        blinds_status = self.io.blinds_open
        self.assertTrue(blinds_status)

    @patch.object(RTC, 'get_current_day')
    @patch.object(RTC, 'get_current_time_string')
    def test_blinds_closed_9pm_tuesday(self, mock_time, mock_day):
        mock_time.return_value = '21:00:00'
        mock_day.return_value = 'TUESDAY'
        self.io.manage_blinds_based_on_time()
        blinds_status = self.io.blinds_open
        self.assertFalse(blinds_status)

    @patch.object(RTC, 'get_current_day')
    @patch.object(RTC, 'get_current_time_string')
    def test_blinds_closed_4pm_saturday(self, mock_time, mock_day):
        mock_time.return_value = '16:00:00'
        mock_day.return_value = 'SATURDAY'
        self.io.manage_blinds_based_on_time()
        blinds_status = self.io.blinds_open
        self.assertFalse(blinds_status)
