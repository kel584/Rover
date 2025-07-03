# motor_controller.py

from gpiozero import Motor
import time
import config

class MotorController:

    def __init__(self, left_pins, right_pins, left_enable_pins, right_enable_pins):

        self.motor_left_front = Motor(forward=left_pins[0][0], backward=left_pins[0][1], enable=left_enable_pins[0])
        self.motor_left_rear = Motor(forward=left_pins[1][0], backward=left_pins[1][1], enable=left_enable_pins[1])
        self.motor_right_front = Motor(forward=right_pins[0][0], backward=right_pins[0][1], enable=right_enable_pins[0])
        self.motor_right_rear = Motor(forward=right_pins[1][0], backward=right_pins[1][1], enable=right_enable_pins[1])

        self.target_heading = 0.0
        self.integral_error = 0.0
        self.last_time = time.time()
        print("Motor kuruldu. Motorlar hazır.")

    def set_target_heading(self, heading):
        self.target_heading = heading
        self.integral_error = 0.0 # yeni hedefte sıfırla
        print("Hedef yön ayarlandı: {:.2f} derece.".format(heading))

    def drive(self, forward_speed, turn_speed, should_stabilize, current_heading):
        if should_stabilize:
            dt = time.time() - self.last_time

            error = self.target_heading - current_heading

            if error > 180:
                error -= 360
            elif error < -180:
                error += 360

            self.integral_error += error * dt

            correction = (config.STABILIZE_KP * error) + (config.STABILIZE_KI * self.integral_error)

            turn_speed = correction

        self.last_time = time.time()

        turn_speed = max(min(turn_speed, 1.0), -1.0)

        left_speed = forward_speed - turn_speed
        right_speed = forward_speed + turn_speed

        max_speed = max(abs(left_speed), abs(right_speed))
        if max_speed > 1.0:
            left_speed /= max_speed
            right_speed /= max_speed
        if left_speed < 0:
            self.motor_left_front.backward(abs(left_speed))
            self.motor_left_rear.backward(abs(left_speed))
        elif left_speed > 0:
            self.motor_left_front.forward(left_speed)
            self.motor_left_rear.forward(left_speed)
        else:
            self.motor_left_front.stop()
            self.motor_left_rear.stop()
        if right_speed < 0:
            self.motor_right_front.backward(abs(right_speed))
            self.motor_right_rear.backward(abs(right_speed))
        elif right_speed > 0:
            self.motor_right_front.forward(right_speed)
            self.motor_right_rear.forward(right_speed)
        else:
            self.motor_right_front.stop()
            self.motor_right_rear.stop()
        

    def stop(self):
        """Stops all motors."""
        self.motor_left_front.stop()
        self.motor_left_rear.stop()
        self.motor_right_front.stop()
        self.motor_right_rear.stop()
        print("Motorlar durduruldu.")