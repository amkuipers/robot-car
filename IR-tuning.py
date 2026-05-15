"""
This code is to help tuning the two line-tracking potentiometers.

Tuning without this code: 
1. Put the car on a dark surface, like a chair
2. The LED next to a potentiometer should be OFF, if its ON turn potentiometer counterclockwise
3. Put the car on a light surface, like a table
4. The LED next to a potentiometer should be ON, if its OFF turn potentiometer clockwise
5. Repeat until tuned

This code:
1. Press Right button (A) for Right IR, HAPPY when on light surface, SAD when on dark surface
2. Press Left button (B) for Left IR, HAPPY when on light surface, SAD when on dark surface

Tuning with this code:
1. Put the car on a dark surface, like a chair
2. Press A should be SAD, if its HAPPY turn Right potentiometer counterclockwise
3. Press B should be SAD, if its HAPPY turn Left potentiometer counterclockwise
4. Put the car on a light surface, like a table
5. Press A should be HAPPY, if its SAD turn Right potentiometer cclockwise
6. Press B should be HAPPY, if its SAD turn Left potentiometer clockwise
7. Repeat until tuned

"""
from microbit import *
import audio
val_LL = 0
val_RR = 0

while True:
    val_LL = pin1.read_digital()
    val_RR = pin2.read_digital()

    if button_a.is_pressed():
        # Right Button
        if val_RR == 0:
            audio.play(Sound.HAPPY)
        else:
            audio.play(Sound.SAD)

    if button_b.is_pressed():
        # Left Button
        if val_LL == 0:
            audio.play(Sound.HAPPY)
        else:
            audio.play(Sound.SAD)

