import time

import mock.RTC
from IntelligentOfficeError import IntelligentOfficeError
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
        time = self.rtc.get_current_time_string()
        day = self.rtc.get_current_day()

        hour = int(time[0] + time[1])

        if day not in ["SATURDAY", "SUNDAY"] and 8 <= hour < 20:
            self.change_servo_angle((180 / 18) + 2) #Opening blinds(180 degrees); duty_cycle = (angle / 18) + 2
            self.blinds_open = 1
        else:
            self.change_servo_angle((0 / 18) + 2) #Closing blinds (0 degrees); duty_cycle = (angle / 18) + 2
            self.blinds_open = 0

    def manage_light_level(self) -> None:
        """
        Tries to maintain the actual light level inside the office, measure by the photoresistor,
        between LUX_MIN and LUX_MAX.
        If the actual light level is lower than LUX_MIN the system turns on the smart light bulb.
        On the other hand, if the actual light level is greater than LUX_MAX, the system turns off the smart light bulb.

        Furthermore, When the last worker leaves the office (i.e., the office is now vacant), the intelligent office system 
        stops regulating the light level in the office and then turns off the smart light bulb. 
        When the first worker goes back into the office, the system resumes regulating the light level
        """
        # 4. Manage smart light bulb based on occupancy
        worker_in_office = 0
        for i in [self.INFRARED_PIN_1, self.INFRARED_PIN_2, self.INFRARED_PIN_3, self.INFRARED_PIN_4]:
            if self.check_quadrant_occupancy(i):
                worker_in_office = 1

        # 3. Light level management
        if worker_in_office:
            if GPIO.input(self.PHOTO_PIN) < self.LUX_MIN:
                GPIO.output(self.LED_PIN, "HIGH")
                self.light_on = 1

            if GPIO.input(self.PHOTO_PIN) > self.LUX_MAX:
                GPIO.output(self.LED_PIN, "LOW")
                self.light_on = 0
        else:
            GPIO.output(self.LED_PIN, "LOW")
            self.light_on = 0

    def monitor_air_quality(self) -> None:
        """
        Use the carbon dioxide sensor to monitor the level of CO2 in the office.
        If the amount of detected CO2 is greater than or equal to 800 PPM, the system turns on the
        switch of the exhaust fan until the amount of CO2 is lower than 500 PPM.
        """

        ppm = GPIO.input(self.CO2_PIN)
        if ppm < 800:
            self.fan_switch_on = 0
            GPIO.output(self.FAN_PIN, "LOW")
            return

        self.fan_switch_on = 1
        GPIO.output(self.FAN_PIN, "HIGH")
        if ppm < 500:
            self.fan_switch_on = 0
            GPIO.output(self.FAN_PIN, "LOW")

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
