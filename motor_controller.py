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

        self.target_heading, self.integral_error = 0.0, 0.0
        self.last_time = time.time()
        print("Motor kuruldu. Motorlar hazır.")

    def set_target_heading(self, heading):
        self.target_heading, self.integral_error = heading, 0.0
        print(f"Hedef yön ayarlandı: {heading:.2f} derece.")

    def drive(self, forward_speed, turn_speed, should_stabilize, current_heading):
        if should_stabilize:
            dt = time.time() - self.last_time
            error = self.target_heading - current_heading
            if error > 180: error -= 360
            elif error < -180: error += 360
            self.integral_error += error * dt
            correction = (config.STABILIZE_KP * error) + (config.STABILIZE_KI * self.integral_error)
            turn_speed = correction

        self.last_time = time.time()
        
        turn_speed = max(-1.0, min(1.0, turn_speed))
        left_speed = forward_speed - turn_speed
        right_speed = forward_speed + turn_speed

        max_speed = max(abs(left_speed), abs(right_speed))
        if max_speed > 1.0:
            left_speed /= max_speed
            right_speed /= max_speed

        # .value property ile daha basit kontrol
        self.motor_left_front.value = left_speed
        self.motor_left_rear.value = left_speed
        self.motor_right_front.value = right_speed
        self.motor_right_rear.value = right_speed
        
        return left_speed, right_speed # son hızları döndür

    def stop(self):
        self.motor_left_front.stop()
        self.motor_left_rear.stop()
        self.motor_right_front.stop()
        self.motor_right_rear.stop()
        print("Motorlar durduruldu.")