# arm_controller.py

from gpiozero import Motor

class ArmController:

    def __init__(self, shoulder_pins, elbow_pins, hand_pins):

        self.motor_shoulder = Motor(
            forward=shoulder_pins[0],
            backward=shoulder_pins[1],
            enable=shoulder_pins[2]
        )
        self.motor_elbow = Motor(
            forward=elbow_pins[0],
            backward=elbow_pins[1],
            enable=elbow_pins[2]
        )
        self.motor_hand = Motor(
            forward=hand_pins[0],
            backward=hand_pins[1],
            enable=hand_pins[2]
        )
        print("Kol kontrolcüsü hazır.")

    def control_arm(self, shoulder_speed, elbow_speed, hand_speed):

        self._set_motor_speed(self.motor_shoulder, shoulder_speed)
        self._set_motor_speed(self.motor_elbow, elbow_speed)
        self._set_motor_speed(self.motor_hand, hand_speed)

    def _set_motor_speed(self, motor, speed):
        
        speed = max(-1.0, min(1.0, speed)) # hızı sınırla
        if speed > 0:
            motor.forward(speed=speed)
        elif speed < 0:
            motor.backward(speed=abs(speed))
        else:
            motor.stop()

    def stop(self):
        
        self.motor_shoulder.stop()
        self.motor_elbow.stop()
        self.motor_hand.stop()
        print("Kol durduruldu.")