# motor_controller.py

from gpiozero import Motor
import math

class MotorController:

    def __init__(self, left_pins, right_pins):

        self.motor_left = Motor(forward=left_pins[0], backward=left_pins[1])
        self.motor_right = Motor(forward=right_pins[0], backward=right_pins[1])
        print("Motor kuruldu. Motorlar hazır.")

    def drive(self, forward_speed, turn_speed):
        """
        :param forward_speed: -1 geri vites, 1 ileri vites, 0 durma.
        :param turn_speed: -1 full sol, 1 full sağ, 0 dönüş yok.
        """
        # Clamp input values to be safe
        forward_speed = max(-1.0, min(1.0, forward_speed))
        turn_speed = max(-1.0, min(1.0, turn_speed))

        # Mix the forward and turn speeds to get left and right motor speeds
        left_speed = forward_speed - turn_speed
        right_speed = forward_speed + turn_speed

        # Normalize 
        max_speed = max(abs(left_speed), abs(right_speed))
        if max_speed > 1.0:
            left_speed /= max_speed
            right_speed /= max_speed

        # Control the left motor
        if left_speed > 0:
            self.motor_left.forward(speed=left_speed)
        elif left_speed < 0:
            self.motor_left.backward(speed=abs(left_speed))
        else:
            self.motor_left.stop()

        # Control the right motor
        if right_speed > 0:
            self.motor_right.forward(speed=right_speed)
        elif right_speed < 0:
            self.motor_right.backward(speed=abs(right_speed))
        else:
            self.motor_right.stop()

    def stop(self):
        """Stops all motors."""
        self.motor_left.stop()
        self.motor_right.stop()
        print("Motorlar durduruldu.")