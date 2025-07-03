# servo_controller.py

from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import config

class ServoController:
    """ Tüm servoların kontrolü"""
    def __init__(self, base_pin):
        
        factory = PiGPIOFactory()
        
        self.base_servo = Servo(base_pin, pin_factory=factory)

       
        self.current_base_angle = 90.0  
        self.center()
        print("Servo kontrolcüsü hazır.")

    def control_base_rotation(self, speed):
        
        angle_change = speed * config.ARM_BASE_ROTATION_SPEED
        self.current_base_angle += angle_change
        
        
        self.current_base_angle = max(0.0, min(180.0, self.current_base_angle))
        
        
        servo_value = (self.current_base_angle / 90.0) - 1.0
        self.base_servo.value = servo_value

    def center(self):
        
        self.base_servo.mid()
        self.current_base_angle = 90.0

    def stop(self):
        
        self.base_servo.detach()
        print("Servolar durduruldu.")