# AGENTS.md

## Project Overview
- This repository contains a MicroPython driver and demo loop for the Keyestudio mecanum robot car (KS4031/KS4032) on BBC micro:bit.
- Keep changes hardware-aware and compatible with the `microbit` MicroPython runtime.

## Code Layout
- `keyes_mecanum_Car.py`: hardware driver (`Mecanum_Car_Driver`) for I2C PWM control, motor channels, LEDs, and ultrasonic distance.
- `main.py`: top-level control loop that reads sensors and drives motors.

## Runtime And Environment Constraints
- Target runtime is micro:bit MicroPython, not CPython.
- Avoid CPython-only modules and APIs.
- `from microbit import *` is expected in this codebase and used by both files.
- Motor controller I2C address is hardcoded to `0x47`; initialization sequence timing is important.

## Hardware Mapping Notes
- Motor speed inputs are expected in `0..255` and mapped to PWM `0..4095` internally.
- PWM channel usage is fixed by board wiring:
  - Upper right motor: channels 0, 1, 2
  - Upper left motor: channels 3, 4, 5
  - Lower right motor: channels 6, 7, 8
  - Lower left motor: channels 9, 10, 11
  - LEDs: channels 12, 13
- Ultrasonic sensor uses `pin15` (trigger) and `pin16` (echo).

## Editing Guidance For Agents
- Preserve public driver method names unless explicitly asked to refactor API.
- Prefer small, targeted edits; do not restructure the project unless requested.
- Keep timing-sensitive initialization logic intact unless there is a confirmed bug.
- If you change motor direction/speed logic, verify behavior in `main.py` remains consistent.

## Validation Guidance
- There are no local unit tests in this repository.
- Validate by static review and, when available, on-device behavior checks (flash to micro:bit and verify motion/sensor behavior).
- If proposing commands, prefer common micro:bit workflows (for example: `uflash main.py`) and clearly mark them as environment-dependent.

## Known Pitfalls
- `get_distance()` uses `self.lastEchoDuration` but it is not initialized in `__init__`; this can raise an `AttributeError` on first read.
- `audio.play(...)` in the main loop is blocking and can affect responsiveness.