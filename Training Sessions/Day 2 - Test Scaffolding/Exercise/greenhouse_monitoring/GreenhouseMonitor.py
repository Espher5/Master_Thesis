try:
    import RPi.GPIO as GPIO
except:
    import mock.GPIO as GPIO

from InvalidMeasurementError import InvalidMeasurementError

class GreenhouseMonitor:
    # Pins definition
    TEMPERATURE_PIN = 5
    SOIL_MOISTURE_PIN = 7
    LIGHT_PIN = 8
    LED_PIN = 10

    def __init__(self):
        self._temperature = None
        self._soil_moisture = None
        self._light_level = None
        self._sprinklers = False
        self._led_on = False

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        GPIO.setup(self.TEMPERATURE_PIN, GPIO.IN)
        GPIO.setup(self.LIGHT_PIN, GPIO.IN)
        GPIO.setup(self.LIGHT_PIN, GPIO.OUT)

    @property
    def temperature(self) -> float:
        return self._temperature

    @property
    def soil_moisture(self) -> float:
        return self._soil_moisture

    @property
    def light_level(self) -> float:
        return self._light_level

    @property
    def sprinklers(self) -> bool:
        return self._sprinklers

    @property
    def led(self) -> bool:
        return self._led_on

    def read_temperature(self) -> None:
        """
        Reads a value for the air temperature, between -10 and 50 degrees
        """
        temperature = GPIO.input(self.TEMPERATURE_PIN)
        if temperature < -10 or temperature > 50:
            raise InvalidMeasurementError
        self._temperature = temperature

    def read_soil_moisture(self) -> None:
        """
        Reads a value for the soil moisture level, between 0% and 100%
        """
        soil_moisture = GPIO.input(self.SOIL_MOISTURE_PIN)
        if soil_moisture < 0 or soil_moisture > 100:
            raise InvalidMeasurementError
        self._soil_moisture = soil_moisture

    def read_light(self) -> None:
        """
        Let's assume we get directly the lumen value, for simplicity
        Value is between 0(very dark) and 2000(very bright)
        """
        light_level = GPIO.input(self.LIGHT_PIN)
        if light_level < 0 or light_level > 2000:
            raise InvalidMeasurementError
        self._light_level = light_level

    def activate_sprinklers(self) -> bool:
        """
        Turns on the sprinklers in case of low soil moisture detected
        :return: True if the sprinkler system is activate, False if it
            doesn't need to be activated or it is already active
        """
        if self._sprinklers or self._soil_moisture is None:
            return False

        if self._soil_moisture < 50:
            self._sprinklers = True
            return True
        else:
            self._sprinklers = False
            return False

    def light_check(self) -> None:
        """
        Turns on the led if the greenhouse is too bright
        :return: True if the led is on, False otherwise
        """
        if self._light_level > 1500:
            GPIO.output(self.LED_PIN, GPIO.HIGH)
            self._led_on = True
        else:
            GPIO.output(self.LED_PIN, GPIO.LOW)
            self._led_on = False

    @staticmethod
    def cleanup():
        GPIO.cleanup()
