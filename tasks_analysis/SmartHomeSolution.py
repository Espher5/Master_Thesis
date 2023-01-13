import time
try:
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

    def __init__(self):
        """
        Constructor
        """
        # Ignore this loop. It is required for the hardware deployment
        for proc in psutil.process_iter():
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
    
    def manage_light_level(self) -> None:
        """
        User story 2:
        When the user leaves the room the smart home system turns off the smart light bulb. 
        When the user goes back into the room, the system turns on the smart light bulb.
        
        User story 3:
        When the user comes back inside the room, before turning on the smart light bulb,
        the system checks how much light is inside the room (by querying the photoresistor).
        If the measured light level inside the room is above the threshold of 500 lux,
        the smart home system does not turn on the smart light bulb even if the person is in the room;
        on the other hand, if the actual light level is below the threshold of 500 lux
        the system regulates the smart light bulb as usual.
        """
        if self.check_room_occupancy() and self.measure_lux() < 500:
            self.turn_light_on()
        else:
            self.turn_light_off()

    def measure_lux(self) -> float:
        """
        Measure the amount of lux inside the room by querying the photoresistor
        """
        return GPIO.input(self.PHOTO_PIN)

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
            # Add your code in here
            temp_indoor = self.dht_indoor.temperature
            temp_outdoor = self.dht_outdoor.temperature
            print('Temperature indoor: {}C   Temperature outdoor: {}C'.format(temp_indoor, temp_outdoor))
            
            if not 18 <= temp_indoor <= 30 or not 18 <= temp_outdoor <= 30:
                self.close_blinds()
                return
            
            if temp_indoor < temp_outdoor - 2:
                print('Opening the window')
                self.open_blinds()
            elif temp_indoor > temp_outdoor + 2:
                print('Closing the window')
                self.close_blinds()
        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2)
            return
        except Exception as error:
            self.dht_indoor.exit()
            self.dht_outdoor.exit()
            raise error
        time.sleep(2)
        
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
        smoke_detected = GPIO.input(self.AIR_QUALITY_PIN) == 0
        
        if smoke_detected:
            self.turn_buzzer_on()
        else:
            self.turn_buzzer_off()
        
    def turn_light_on(self) -> None:
        if self.light_on is False:
            GPIO.output(self.LIGHT_PIN, GPIO.HIGH)
            self.light_on = True
    
    def turn_light_off(self) -> None:
        if self.light_on is True:
            GPIO.output(self.LIGHT_PIN, GPIO.LOW)
            self.light_on = False
    
    def turn_buzzer_on(self) -> None:
        if self.buzzer_on is False:
            GPIO.output(self.BUZZER_PIN, GPIO.HIGH)
            self.buzzer_on = True
    
    def turn_buzzer_off(self) -> None:
        if self.buzzer_on is True:
            GPIO.output(self.BUZZER_PIN, GPIO.LOW)
            self.buzzer_on = False
        
    def open_blinds(self) -> None:
        if self.window_open is False:
            duty_cycle = (180 / 18) + 2
            self.servo.ChangeDutyCycle(duty_cycle)
            self.window_open = True
            
    def close_blinds(self) -> None:
        if self.window_open is True:
            duty_cycle = (0 / 18) + 2
            self.servo.ChangeDutyCycle(duty_cycle)
            self.window_open = False


if __name__ == '__main__':
    sh = SmartHome()
    while True:
        sh.manage_light_level()

