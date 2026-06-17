#from microbit import pin1, pin2, sleep, i2c
from microbit import *
import ustruct
import machine
from time import sleep_us, ticks_us
distance = 0

class Mecanum_Car_Driver(object):
    def __init__(self):
        """
        Initialize the Mecanum Car driver and configure I2C PWM controller.
        
        Sets up I2C communication to motor driver at address 0x47 (PCA9685),
        configures PWM channels, and initializes motor/LED state.
        Requires 5ms delays during initialization sequence for controller stability.
        """
        self.add = 0x47
        i2c.write(self.add, bytearray([0x00, 0x00]), repeat=False)
        self.set_all_pwm(0, 0)
        i2c.write(self.add, bytearray([0x01, 0x04]), repeat=False)
        i2c.write(self.add, bytearray([0x00, 0x01]), repeat=False)
        sleep(5)
        i2c.write(self.add, bytearray([0x00]), repeat=False)
        mode1s = i2c.read(self.add, 1)
        #mode1 = ustruct.unpack('<H', mode1)[0]
        mode1 = mode1s[0]
        mode1 = mode1 & ~0x10
        i2c.write(self.add, bytearray([0x00, mode1]), repeat=False)
        sleep(5)
        self.lastEchoDuration = 0  # Initialize ultrasonic echo duration

    def set_pwm(self, channel, on, off):
        """
        Set PWM on/off timing for a single channel.
        
        Args:
            channel (int): PWM channel number (0-15).
            on (int or None): PWM on time (0-4095). If None, read current value.
            off (int or None): PWM off time (0-4095). If None, read current value.
        
        Returns:
            tuple: (on, off) values if reading; None if writing.
        
        Note: on and off values determine duty cycle and frequency via I2C register writes.
        """
        if on is None or off is None:
            i2c.write(self.add, bytearray([0x06+4*channel]), repeat=False)
            data = i2c.read(self.add, 4)
            return ustruct.unpack('<HH', data)
        i2c.write(self.add, bytearray([0x06+4*channel, on & 0xFF]), repeat=False)
        i2c.write(self.add, bytearray([0x07+4*channel, on >> 8]), repeat=False)
        i2c.write(self.add, bytearray([0x08+4*channel, off & 0xFF]), repeat=False)
        i2c.write(self.add, bytearray([0x09+4*channel, off >> 8]), repeat=False)

    def set_all_pwm(self, on, off):
        """
        Set PWM on/off timing for all channels simultaneously.
        
        Args:
            on (int): PWM on time for all channels (0-4095).
            off (int): PWM off time for all channels (0-4095).
        
        Useful for emergency stop (on=0, off=0) or global brightness control.
        """
        i2c.write(self.add, bytearray([0xFA, on & 0xFF]), repeat=False)
        i2c.write(self.add, bytearray([0xFB, on >> 8]), repeat=False)
        i2c.write(self.add, bytearray([0xFC, off & 0xFF]), repeat=False)
        i2c.write(self.add, bytearray([0xFD, off >> 8]), repeat=False)

    def map(self, value, fromLow, fromHigh, toLow, toHigh):
        """
        Map a value from one numeric range to another (linear interpolation).
        
        Args:
            value (float): Value to map.
            fromLow (float): Lower bound of input range.
            fromHigh (float): Upper bound of input range.
            toLow (float): Lower bound of output range.
            toHigh (float): Upper bound of output range.
        
        Returns:
            float: Mapped value in output range.
        
        Example: map(128, 0, 255, 0, 4095) converts motor speed to PWM value.
        """
        return (toHigh-toLow)*(value-fromLow) / (fromHigh-fromLow) + toLow

    '''
    def constrain(self, Value, Low, High):
        if Value <= Low:
            return Low
        elif Value >= High:
            return High
        else:
            return Value
    '''
    def left_led(self, state):
        """
        Control left LED on/off.
        
        Args:
            state (int): 1 to turn on (full brightness), 0 to turn off.
        
        Uses PWM channel 12.
        """
        if(state == 1):
            self.set_pwm(12, 0, 4095)
        elif(state == 0):
            self.set_pwm(12, 0, 0)

    def right_led(self, state):
        """
        Control right LED on/off.
        
        Args:
            state (int): 1 to turn on (full brightness), 0 to turn off.
        
        Uses PWM channel 13.
        """
        if(state == 1):
            self.set_pwm(13, 0, 4095)
        elif(state == 0):
            self.set_pwm(13, 0, 0)

    def Motor_Upper_L(self, stateL, left1):
        """
        Control upper left motor direction and speed.
        
        Args:
            stateL (int): Motor direction (0 or 1). Determines rotation direction.
            left1 (int): Motor speed (0-255). 0 = stop, 255 = full speed.
        
        Uses PWM channels 3 (direction 1), 4 (direction 2), 5 (speed).
        """
        left = int(self.map(left1, 0, 255, 0, 4095))
        if (stateL == 0):
            self.set_pwm(4, 4096, 0)
            self.set_pwm(3, 0, 0)
            self.set_pwm(5, 0, left)
        if (stateL == 1):
            self.set_pwm(4, 0, 0)
            self.set_pwm(3, 4096, 0)
            self.set_pwm(5, 0, left)

    def Motor_Lower_L(self, stateL, left1):
        """
        Control lower left motor direction and speed.
        
        Args:
            stateL (int): Motor direction (0 or 1). Determines rotation direction.
            left1 (int): Motor speed (0-255). 0 = stop, 255 = full speed.
        
        Uses PWM channels 9 (direction 1), 10 (direction 2), 11 (speed).
        """
        left2 = int(self.map(left1, 0, 255, 0, 4095))
        if (stateL == 0):
            self.set_pwm(10, 4096, 0)
            self.set_pwm(9, 0, 0)
            self.set_pwm(11, 0, left2)
        if (stateL == 1):
            self.set_pwm(10, 0, 0)
            self.set_pwm(9, 4096, 0)
            self.set_pwm(11, 0, left2)

    def Motor_Upper_R(self, stateR, right1):
        """
        Control upper right motor direction and speed.
        
        Args:
            stateR (int): Motor direction (0 or 1). Determines rotation direction.
            right1 (int): Motor speed (0-255). 0 = stop, 255 = full speed.
        
        Uses PWM channels 1 (direction 1), 2 (direction 2), 0 (speed).
        """
        right = int(self.map(right1, 0, 255, 0, 4095))
        if (stateR == 0):
            self.set_pwm(2, 4096, 0)
            self.set_pwm(1, 0, 0)
            self.set_pwm(0, 0, right)
        if (stateR == 1):
            self.set_pwm(2, 0, 0)
            self.set_pwm(1, 4096, 0)
            self.set_pwm(0, 0, right)

    def Motor_Lower_R(self, stateR, right1):
        """
        Control lower right motor direction and speed.
        
        Args:
            stateR (int): Motor direction (0 or 1). Determines rotation direction.
            right1 (int): Motor speed (0-255). 0 = stop, 255 = full speed.
        
        Uses PWM channels 7 (direction 1), 8 (direction 2), 6 (speed).
        """
        right2 = int(self.map(right1, 0, 255, 0, 4095))
        if (stateR == 0):
            self.set_pwm(8, 4096, 0)
            self.set_pwm(7, 0, 0)
            self.set_pwm(6, 0, right2)
        if (stateR == 1):
            self.set_pwm(8, 0, 0)
            self.set_pwm(7, 4096, 0)
            self.set_pwm(6, 0, right2)

    def get_distance(self):
        """
        Read distance from ultrasonic sensor.
        
        Returns:
            int: Distance in centimeters (rounded).
        
        Uses pins 15 (trigger) and 16 (echo). Conversion factor: 0.017 cm/µs.
        Timeout: 35ms. Falls back to cached value on invalid reads.
        
        Note: Requires 35ms timeout; readings may be unreliable in noisy environments.
        """
        pin15.write_digital(0)
        sleep_us(2)
        pin15.write_digital(1)
        sleep_us(15)
        pin15.write_digital(0)

        t = machine.time_pulse_us(pin16,1,35000)
        if (t <= 0 and self.lastEchoDuration >= 0) :
            t = self.lastEchoDuration

        self.lastEchoDuration = t
        return round(t * 0.017)

    '''
    def get_distance(self):
        global distance
        for i in range(15):
            pin15.write_digital(1)
            sleep_us(15)
            pin15.write_digital(0)
            if pin16.read_digital() == 1:
                ts = ticks_us()
                while pin16.read_digital() == 1:
                    pass
                te = ticks_us()
                tc = te - ts
                distance = (tc*170)*0.0001
                if(distance > 500):
                    distance = 0
        return round(distance, 2)
    '''
