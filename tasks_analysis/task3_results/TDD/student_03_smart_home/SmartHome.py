import time

try: # pragma: no cover
    import adafruit_dht
    import psutil
    import RPi.GPIO as GPIO
except:
    import mock.adafruit_dht as adafruit_dht
    import mock.GPIO as GPIO
    import mock.psutil as psutil


class SmartHome:
    AIR_QUALITY_PIN = 5
    SERVO_PIN = 6
    BUZZER_PIN = 16
    DHT_PIN1 = 23
    DHT_PIN2 = 24
    INFRARED_PIN = 25
    LIGHT_PIN = 26
    PHOTO_PIN = 27  # Photoresistor pin

    WINDOW_OPEN_DUTY_CYCLE = (180 / 18) + 2
    WINDOW_CLOSED_DUTY_CYCLE = (0 / 18) + 2

    def __init__(self):
        """
        Constructor
        """
        # Ignore this loop. It is required for the hardware deployment
        for proc in psutil.process_iter(): # pragma: no cover
            if proc.name() == 'libgpiod_pulsein' or proc.name() == 'libgpiod_pulsei':
                proc.kill()

        # GPIO pin setup
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.AIR_QUALITY_PIN, GPIO.IN)
        GPIO.setup(self.INFRARED_PIN, GPIO.IN)
        GPIO.setup(self.PHOTO_PIN, GPIO.IN)
        GPIO.setup(self.LIGHT_PIN, GPIO.OUT)
        GPIO.setup(self.BUZZER_PIN, GPIO.OUT)
        GPIO.setup(self.SERVO_PIN, GPIO.OUT)

        self.dht_indoor = adafruit_dht.DHT11(self.DHT_PIN1)
        self.dht_outdoor = adafruit_dht.DHT11(self.DHT_PIN2)
        self.servo = GPIO.PWM(self.SERVO_PIN, 50)
        self.servo.start(0)
        self.servo.ChangeDutyCycle(2)

        self.light_on = False
        self.window_open = False
        self.buzzer_on = False

        GPIO.output(self.LIGHT_PIN, GPIO.LOW)
        GPIO.output(self.BUZZER_PIN, GPIO.LOW)
        time.sleep(2)

    def check_room_occupancy(self) -> bool:
        """
        Checks whether the infrared distance sensor on the ceiling detects something in front of it.
        :return: True if the infrared sensor detects something, False otherwise.
        """
        return GPIO.input(self.INFRARED_PIN) == 0

    def set_light(self, state):
        if state and not self.light_on:
            GPIO.output(self.LIGHT_PIN, True)
            self.light_on = True
        elif not state and self.light_on:
            GPIO.output(self.LIGHT_PIN, False)
            self.light_on = False

    def manage_light_level(self) -> None:
        """
        User story 2:
        When the user is inside the room, the smart home system turns on the smart light bulb.
        On the other hand, the smart home system turns off the light when the user leaves the room.
        The infrared distance sensor is used to determine whether someone is inside the room.

        User story 3:
        Before turning on the smart light bulb, the system checks how much light is inside the room
        (by querying the photoresistor).
        If the measured light level inside the room is above or equal to the threshold of 500 lux,
        the smart home system does not turn on the smart light bulb even if the user is in the room;
         on the other hand, if the light level is below the threshold of 500 lux and the user is in the room,
         the system turns on the smart light bulb as usual.

        """
        presence = self.check_room_occupancy()
        lux = self.measure_lux()

        if presence:
            # Light is only updated if presence
            if lux >= 500:
                # Do nothing, enough light
                pass
            elif lux < 500:
                # Set light on, never turn it off until no presence
                self.set_light(True)

        else:
            # No user no light rule
            self.set_light(False)

    def measure_lux(self) -> float:
        """
        Measure the amount of lux inside the room by querying the photoresistor
        """
        return GPIO.input(self.PHOTO_PIN)

    def get_indoor_temp(self) -> float:
        return self.dht_indoor.temperature

    def get_outdoor_temp(self) -> float:
        return self.dht_outdoor.temperature

    def set_window_open(self, state):
        if state and not self.window_open:
            self.window_open = True
            self.servo.ChangeDutyCycle(self.WINDOW_OPEN_DUTY_CYCLE)
        elif not state and self.window_open:
            self.window_open = False
            self.servo.ChangeDutyCycle(self.WINDOW_CLOSED_DUTY_CYCLE)

    def manage_window(self) -> None:
        """
        Two temperature sensors, one indoor and one outdoor, are used to trigger the servo motor
        to manage the window.
        Whenever the indoor temperature is lower than the  outdoor temperature minus two degrees,
        the system opens the window by using the servo motor;
        on the other hand, when the indoor temperature is greater than the outdoor temperature
        plus two degrees, the system closes the window by using the servo motor.

        Please note that the above behavior is only triggered when both of the sensors measure
        temperature in the range of 18 to 30 degrees celsius. Otherwise, the window stays closed.
        """
        try:
            indoor_temp = self.get_indoor_temp()
            outdoor_temp = self.get_outdoor_temp()
            # Only manage window when both sensor report a range of 18 <= x <= 30
            if 18 <= indoor_temp <= 30 and 18 <= outdoor_temp <= 30:
                if indoor_temp < outdoor_temp - 2:  # If its warmer outside, open window
                    self.set_window_open(True)
                elif indoor_temp > outdoor_temp + 2:  # Close window when its getting colder outside then inside, keep warm in
                    self.set_window_open(False)
            else:
                self.set_window_open(False)  # Its really cold inside or outside, keep window shut.
        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2)
            return
        except Exception as error:
            self.dht_indoor.exit()
            self.dht_outdoor.exit()
            raise error

    # Gas leak detected, true if value bigger or equal 500PPM
    def read_air_quality_gas_leak(self) -> bool:
        return GPIO.input(self.AIR_QUALITY_PIN) == 0

    def set_buzzer(self, state):
        if state and not self.buzzer_on:
            self.buzzer_on = True
            GPIO.output(self.BUZZER_PIN, True)
        elif not state and self.buzzer_on:
            self.buzzer_on = False
            GPIO.output(self.BUZZER_PIN, False)

    def monitor_air_quality(self):
        """
        The air quality sensor is configured in a way such that if the amount of gas particles detected
        is below 500 PPM, the sensor returns a constant reading of 1.
        As soon as the gas measurement goes to 500 PPM or above, the sensor switches state and
        starts returning readings of 0.

        To notify the user of any gas leak an active buzzer is employed;
        if the amount of detected gas is greater than or equal to 500 PPM,
        the system turns on the buzzer until the smoke level goes below the threshold of 500 PPM.
        """
        gas = self.read_air_quality_gas_leak()
        if gas:
            self.set_buzzer(True)
        else:
            self.set_buzzer(False)
