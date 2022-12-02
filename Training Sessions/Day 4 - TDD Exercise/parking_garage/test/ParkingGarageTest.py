import unittest
from unittest.mock import patch
from ParkingGarage import ParkingGarage
from ParkingGarageError import ParkingGarageError
import mock.GPIO as GPIO
from mock.RTC import RTC


class ParkingGarageTest(unittest.TestCase):
    def setUp(self) -> None:
        self.pg = ParkingGarage()

    @patch.object(GPIO, 'input')
    def test_occupancy_spot1_not_parked(self, mock_input):
        mock_input.return_value = 0
        occupancy = self.pg.check_occupancy(ParkingGarage.INFRARED_PIN1)
        self.assertFalse(occupancy)

    @patch.object(GPIO, 'input')
    def test_occupancy_spot1_parked(self, mock_input):
        mock_input.return_value = 52
        occupancy = self.pg.check_occupancy(ParkingGarage.INFRARED_PIN1)
        self.assertTrue(occupancy)

    @patch.object(GPIO, 'input')
    def test_occupancy_spot2_not_parked(self, mock_input):
        mock_input.return_value = 0
        occupancy = self.pg.check_occupancy(ParkingGarage.INFRARED_PIN2)
        self.assertFalse(occupancy)

    @patch.object(GPIO, 'input')
    def test_occupancy_spot2_parked(self, mock_input):
        mock_input.return_value = 98
        occupancy = self.pg.check_occupancy(ParkingGarage.INFRARED_PIN2)
        self.assertTrue(occupancy)

    @patch.object(GPIO, 'input')
    def test_occupancy_spot3_not_parked(self, mock_input):
        mock_input.return_value = 0
        occupancy = self.pg.check_occupancy(ParkingGarage.INFRARED_PIN3)
        self.assertFalse(occupancy)

    @patch.object(GPIO, 'input')
    def test_occupancy_spot3_parked(self, mock_input):
        mock_input.return_value = 12
        occupancy = self.pg.check_occupancy(ParkingGarage.INFRARED_PIN3)
        self.assertTrue(occupancy)

    @patch.object(GPIO, 'input')
    def test_occupancy_invalid_pin(self, mock_input):
        mock_input.return_value = 73
        self.assertRaises(ParkingGarageError, self.pg.check_occupancy, -1)

    @patch.object(GPIO, 'input')
    def test_occupied_spots_three_parked(self, mock_input):
        mock_input.side_effect = [65, 28, 91]
        occupancy_num = self.pg.get_occupied_spots()
        self.assertEqual(3, occupancy_num)

    @patch.object(GPIO, 'input')
    def test_occupied_spots_two_parked(self, mock_input):
        mock_input.side_effect = [34, 0, 77]
        occupancy_num = self.pg.get_occupied_spots()
        self.assertEqual(2, occupancy_num)

    @patch.object(GPIO, 'input')
    def test_occupied_spots_zero_parked(self, mock_input):
        mock_input.side_effect = [0, 0, 0]
        occupancy_num = self.pg.get_occupied_spots()
        self.assertEqual(0, occupancy_num)

    @patch.object(RTC, 'get_current_day')
    @patch.object(RTC, 'get_current_time_string')
    def test_parking_fee_week_day_3_hours(self, mock_time, mock_day):
        mock_time.return_value = '15:24:54'
        mock_day.return_value = 'MONDAY'

        fee = self.pg.calculate_parking_fee('12:30:15')
        self.assertEqual(7.50, fee)

    @patch.object(RTC, 'get_current_day')
    @patch.object(RTC, 'get_current_time_string')
    def test_parking_fee_weekend_9_hours(self, mock_time, mock_day):
        mock_time.return_value = '18:31:28'
        mock_day.return_value = 'SATURDAY'

        fee = self.pg.calculate_parking_fee('10:15:08')
        self.assertAlmostEqual(28.1, fee, 1)

    @patch.object(RTC, 'get_current_day')
    @patch.object(RTC, 'get_current_time_string')
    def test_parking_fee_weekend_invalid_hours(self, mock_time, mock_day):
        mock_time.return_value = '14:10:00'
        mock_day.return_value = 'SATURDAY'

        self.assertRaises(ParkingGarageError, self.pg.calculate_parking_fee, '20:03:15')

    def test_garage_door_open(self):
        self.pg.open_garage_door()
        door_open = self.pg.door_open
        self.assertTrue(door_open)

    def test_garage_door_close(self):
        self.pg.close_garage_door()
        door_open = self.pg.door_open
        self.assertFalse(door_open)

    def test_garage_door_open_close(self):
        self.pg.open_garage_door()
        self.pg.close_garage_door()
        door_open = self.pg.door_open
        self.assertFalse(door_open)

    def test_garage_door_close_open(self):
        self.pg.close_garage_door()
        self.pg.open_garage_door()
        door_open = self.pg.door_open
        self.assertTrue(door_open)

    @patch.object(GPIO, 'input')
    def test_light_off(self, mock_input):
        mock_input.side_effect = [0, 0, 0]
        self.pg.turn_light_off()
        light_on = self.pg.light_on
        self.assertFalse(light_on)

    @patch.object(GPIO, 'input')
    def test_light_on_1_parked(self, mock_input):
        mock_input.side_effect = [73, 0, 0]
        self.pg.turn_light_on()
        light_on = self.pg.light_on
        self.assertTrue(light_on)

    @patch.object(GPIO, 'input')
    def test_light_on_3_parked(self, mock_input):
        mock_input.side_effect = [52, 85, 33]
        self.pg.turn_light_on()
        light_on = self.pg.light_on
        self.assertTrue(light_on)
