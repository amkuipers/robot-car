from microbit import *
import audio
from car import *
mecanumCar = Mecanum_Car_Driver()

val_LL = 0
val_RR = 0

FWD = 1
REV = 0

WHITE=0
BLACK=1

GEAR0 = 0 # Stop
#GEAR1 = 50 # 100 Normal speed
#GEAR2 = 60 # 120  
#GEAR3 = 110 # 220
#GEAR4 = 160 # Fast corrective turn speed

GEAR1 = 100 # 100 Normal speed
GEAR2 = 60 # 120  
GEAR3 = 110 # 220
GEAR4 = 180 # Fast corrective turn speed


# Track last action for reversible movements
last_action = None

def forward():
    """Move forward at GEAR1 speed."""
    global last_action
    mecanumCar.Motor_Upper_L(FWD, GEAR1)
    mecanumCar.Motor_Lower_L(FWD, GEAR1)
    mecanumCar.Motor_Upper_R(FWD, GEAR1)
    mecanumCar.Motor_Lower_R(FWD, GEAR1)
    last_action = 'forward'
    mecanumCar.left_led(0)
    mecanumCar.right_led(0)

def reverse():
    """Move backward at GEAR1 speed."""
    global last_action
    mecanumCar.Motor_Upper_L(REV, GEAR1)
    mecanumCar.Motor_Lower_L(REV, GEAR1)
    mecanumCar.Motor_Upper_R(REV, GEAR1)
    mecanumCar.Motor_Lower_R(REV, GEAR1)
    last_action = 'reverse'
    mecanumCar.left_led(1)
    mecanumCar.right_led(1)
    
def turn_left():
    """Turn left: left at GEAR2 (slower), right at GEAR3 (faster)."""
    global last_action
    mecanumCar.Motor_Upper_L(REV, GEAR2)
    mecanumCar.Motor_Lower_L(REV, GEAR2)
    mecanumCar.Motor_Upper_R(FWD, GEAR3)
    mecanumCar.Motor_Lower_R(FWD, GEAR3)
    last_action = 'turn_left'
    mecanumCar.left_led(1)
    mecanumCar.right_led(0)

def turn_right():
    """Turn right: left at GEAR3 (faster), right at GEAR2 (slower)."""
    global last_action
    mecanumCar.Motor_Upper_L(FWD, GEAR3)
    mecanumCar.Motor_Lower_L(FWD, GEAR3)
    mecanumCar.Motor_Upper_R(REV, GEAR2)
    mecanumCar.Motor_Lower_R(REV, GEAR2)
    last_action = 'turn_right'
    mecanumCar.left_led(0)
    mecanumCar.right_led(1)
    
def turn_left_fast():
    """Fast left correction for tight loop tiles."""
    global last_action
    mecanumCar.Motor_Upper_L(REV, GEAR3)
    mecanumCar.Motor_Lower_L(REV, GEAR3)
    mecanumCar.Motor_Upper_R(FWD, GEAR4)
    mecanumCar.Motor_Lower_R(FWD, GEAR4)
    last_action = 'turn_left'
    mecanumCar.left_led(1)
    mecanumCar.right_led(0)
    
def turn_right_fast():
    """Fast right correction for tight loop tiles."""
    global last_action
    mecanumCar.Motor_Upper_L(FWD, GEAR4)
    mecanumCar.Motor_Lower_L(FWD, GEAR4)
    mecanumCar.Motor_Upper_R(REV, GEAR3)
    mecanumCar.Motor_Lower_R(REV, GEAR3)
    last_action = 'turn_right'
    mecanumCar.left_led(0)
    mecanumCar.right_led(1)
    
def stop():
    """Stop all motors."""
    global last_action
    mecanumCar.Motor_Upper_L(FWD, GEAR0)
    mecanumCar.Motor_Lower_L(FWD, GEAR0)
    mecanumCar.Motor_Upper_R(FWD, GEAR0)
    mecanumCar.Motor_Lower_R(FWD, GEAR0)
    last_action = 'stop'

def reverse_last_action():
    """Reverse the last movement action (undo, not just go backward)."""
    global last_action
    if last_action == 'forward':
        reverse()
    elif last_action == 'reverse':
        forward()
    elif last_action == 'turn_left':
        turn_right()
    elif last_action == 'turn_right':
        turn_left()
    else:
        stop()

def recover_when_off_road():
    """Recovery when both sensors see white.

    If we were already turning, apply an extra fast turn in the same direction
    to clear tight loop tiles. Otherwise keep the existing double-reverse behavior.
    """
    if last_action == 'turn_right':
        turn_right_fast()
    elif last_action == 'turn_left':
        turn_left_fast()
    else:
        reverse()
        reverse()

while True:
    val_LL = pin1.read_digital()
    val_RR = pin2.read_digital()

    # ROAD IS BLACK
    # OFFROAD IS WHITE

    
    
    if val_LL == WHITE and val_RR == BLACK:
        turn_right()
        
    elif val_LL == BLACK and val_RR == WHITE:
        turn_left()
        
    elif val_LL == WHITE and val_RR == WHITE:
        recover_when_off_road()
        
    else:
        forward()
