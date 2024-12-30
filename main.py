
# Motor speed variables
def set_motor_speed():
    global forward_speed, turning_speed, left_speed, right_speed
    # Calculate forward/backward speeds and turning adjustment
    forward_speed = Y
    turning_speed = X
    # Calculate the speed for each motor
    left_speed = max(0, forward_speed + turning_speed)
    # Ensure no backward motion
    right_speed = max(0, forward_speed - turning_speed)
    # Ensure no backward motion
    # Control the left motor speed
    pins.analog_write_pin(ENABLE_LEFT, min(1023, abs(left_speed)))
    # Control the right motor speed
    pins.analog_write_pin(ENABLE_RIGHT, min(1023, abs(right_speed)))
# Write LOW

def on_received_value(name, value):
    global X, Y
    if name == "X":
        X = value if abs(value) > DEADZONE else 0
    elif name == "Y":
        Y = value if abs(value) > DEADZONE else 0
    elif name == "Servo":
        # Control the servo motor based on the received value
        if value == 1:
            pins.servo_write_pin(DigitalPin.P0, 90)
        else:
            # Turn servo to 0 degrees
            pins.servo_write_pin(DigitalPin.P0, 0)
    elif name == "Pin13":
        # Control pin13 based on received value
        if value == 1:
            pins.digital_write_pin(DigitalPin.P14, 1)
        else:
            # Write HIGH
            pins.digital_write_pin(DigitalPin.P14, 0)
radio.on_received_value(on_received_value)

right_speed = 0
left_speed = 0
turning_speed = 0
forward_speed = 0
ENABLE_RIGHT = 0
ENABLE_LEFT = 0
# Global X, Y values
X = 0
Y = 0
# Motor control pins
ENABLE_LEFT = DigitalPin.P1
# Control left motor speed
ENABLE_RIGHT = DigitalPin.P2
# Control right motor speed
# Deadzone threshold
DEADZONE = 200
# Initialize the radio group
radio.set_group(1)
basic.show_icon(IconNames.YES)

def on_forever():
    set_motor_speed()
basic.forever(on_forever)

# Button B not pressed

def on_forever2():
    radio.send_value("X", input.acceleration(Dimension.X))
    radio.send_value("Y", input.acceleration(Dimension.Y))
    # Send button A state for servo control
    if input.button_is_pressed(Button.A):
        radio.send_value("Servo", 1)
    else:
        radio.send_value("Servo", 0)
    # Send button B state for pin13 control
    if input.button_is_pressed(Button.B):
        radio.send_value("Pin13", 1)
    else:
        # Button B pressed
        radio.send_value("Pin13", 0)
basic.forever(on_forever2)
