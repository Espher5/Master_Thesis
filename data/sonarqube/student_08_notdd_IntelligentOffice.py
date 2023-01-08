import time

import mock.GPIO as GPIO
from mock.RTC import RTC


class IntelligentOffice:
    # Pin number definition
    INFRARED_PIN_1 = 11
    INFRARED_PIN_2 = 12
    INFRARED_PIN_3 = 13
    INFRARED_PIN_4 = 15
    RTC_PIN = 16
    SERVO_PIN = 18
    PHOTO_PIN = 22  # photoresistor
    LED_PIN = 29
    CO2_PIN = 31
    FAN_PIN = 32

    LUX_MIN = 500
    LUX_MAX = 550

    def __init__(self):
        """
        Constructor
        """
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.INFRARED_PIN_1, GPIO.IN)
        GPIO.setup(self.INFRARED_PIN_2, GPIO.IN)
        GPIO.setup(self.INFRARED_PIN_3, GPIO.IN)
        GPIO.setup(self.INFRARED_PIN_4, GPIO.IN)
        GPIO.setup(self.PHOTO_PIN, GPIO.IN)
        GPIO.setup(self.SERVO_PIN, GPIO.OUT)
        GPIO.setup(self.LED_PIN, GPIO.OUT)
        GPIO.setup(self.CO2_PIN, GPIO.IN)
        GPIO.setup(self.FAN_PIN, GPIO.OUT)

        self.rtc = RTC(self.RTC_PIN)
        self.pwm = GPIO.PWM(self.SERVO_PIN, 50)
        self.pwm.start(0)

        self.blinds_open = False
        self.light_on = False
        self.fan_switch_on = False

    def check_quadrant_occupancy(self, pin: int) -> bool:
        """
        Checks whether one of the infrared distance sensor on the ceiling detects something in front of it.
        :param pin: The data pin of the sensor that is being checked (e.g., INFRARED_PIN1).
        :return: True if the infrared sensor detects something, False otherwise.
        """
        if GPIO.input(pin) > 0:

            return True

        return False


    def manage_blinds_based_on_time(self) -> None:
        """
        Uses the RTC and servo motor to open/close the blinds based on current time and day.
        The system fully opens the blinds at 8:00 and fully closes them at 20:00
        each day except for Saturday and Sunday.
        """

        time_now = self.rtc.get_current_time_string()
        day = self.rtc.get_current_day()

        hour_now = int(time_now[0] + time_now[1])
        min_now = int(time_now[3] + time_now[4])

        duty_cycle_fully_open = (180 / 18 )+ 2
        duty_cycle_fully_closed = (0 / 18) + 2

        if day in ["Saturday", "Sunday"]:
            return False

        if hour_now == "08" and min_now == "00":  """ dont know how to compare the exact time in python"""

            self.change_servo_angle(self, duty_cycle_fully_open)
            blinds_open = True




        if hour_now == "20" and min_now == "00":

            self.change_servo_angle(self, duty_cycle_fully_closed)
            blinds_open = False

        """dont know the syntax"""




        return blinds_open

    def manage_light_level(self) -> None:
        """
        Tries to maintain the actual light level inside the office, measure by the photoresitor,
        between LUX_MIN and LUX_MAX.
        If the actual light level is lower than LUX_MIN the system turns on the smart light bulb.
        On the other hand, if the actual light level is greater than LUX_MAX, the system turns off the smart light bulb.

        Furthermore, When the last worker leaves the office (i.e., the office is now vacant), the intelligent office system 
        stops regulating the light level in the office and then turns off the smart light bulb. 
        When the first worker goes back into the office, the system resumes regulating the light level
        """
        while GPIO.input(22) <= 500:

            GPIO.output(29, True)

        while GPIO.input(22) >= 500:
            GPIO.output(29, False)



        if GPIO.input(22) <= 500:
            GPIO.output(29, True)

        if GPIO.input(22) >= 550:
            GPIO.ouput(29, False)


        office_is_empty = self.check_quadrant_occupancy()

        if office_is_empty:
            GPIO.ouput(29, False)
            self.light_on = False



    def monitor_air_quality(self) -> None:
        """
        Use the carbon dioxide sensor to monitor the level of CO2 in the office.
        If the amount of detected CO2 is greater than or equal to 800 PPM, the system turns on the
        switch of the exhaust fan until the amount of CO2 is lower than 500 PPM.
        """
        if GPIO.input(31) >= 800:
            GPIO.output(32, False)

        if GPIO.input(31) < 500:
            GPIO.ouput(32, True)

    def change_servo_angle(self, duty_cycle: float) -> None:
        """
        Changes the servo motor's angle by passing to it the corresponding PWM duty cycle signal
        :param duty_cycle: the length of the duty cycle
        """
        GPIO.output(self.SERVO_PIN, GPIO.HIGH)
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(1)
        GPIO.output(self.SERVO_PIN, GPIO.LOW)
        self.pwm.ChangeDutyCycle(0)
