"""
The distance sensor direction is controlled by a servo.

Goal:
- 0' is looking right
- 90' is looking forward
- 180' is looking left

Tune:
1. Run code to set the servo to 90' forward.
2. In case it is not looking forward, turn the robot OFF
3. Unscrew the servo and remove it
4. Place it back in forward position and screw the servo

Code is based on project 15 by keyestudio, but this code only sets the servo forward.
In case the servo does not repositions itself, it might already be in position.
Directions are not perfect, but good enough for this robot car.
"""
from microbit import *

class Servo:
    def __init__(self, pin, freq=50, min_us=600, max_us=2400, angle=180):
        self.min_us = min_us
        self.max_us = max_us
        self.us = 0
        self.freq = freq
        self.angle = angle
        self.analog_period = 0
        self.pin = pin
        analog_period = round((1/self.freq) * 1000)  # hertz to miliseconds
        self.pin.set_analog_period(analog_period)

    def write_us(self, us):
        us = min(self.max_us, max(self.min_us, us))
        duty = round(us * 1024 * self.freq // 1000000)
        self.pin.write_analog(duty)
        sleep(100)
        self.pin.write_analog(0)

    def write_angle(self, degrees=None):
        if degrees is None:
            degrees = math.degrees(radians)
        degrees = degrees % 360
        total_range = self.max_us - self.min_us
        us = self.min_us + total_range * degrees // self.angle
        self.write_us(us)

Servo(pin14).write_angle(90)


