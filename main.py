# main.py

import time
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Device

# Import our own project files
import config
from motor_controller import MotorController
from gamepad_controller import GamepadController
from camera_controller import CameraController
from data_logger import DataLogger
from sensor_controller import SensorController
from gps_reader import GpsReader 
from arm_controller import ArmController
from servo_controller import ServoController
from navigation import Navigator

def main():
    
    print("ARCRover başlatılıyor...")


    Device.pin_factory = PiGPIOFactory()

    motors = MotorController(left_pins=((config.MOTOR_LEFT_FRONT_FORWARD, config.MOTOR_LEFT_FRONT_BACKWARD),(config.MOTOR_LEFT_REAR_FORWARD, config.MOTOR_LEFT_REAR_BACKWARD)), right_pins=((config.MOTOR_RIGHT_FRONT_FORWARD, config.MOTOR_RIGHT_FRONT_BACKWARD),(config.MOTOR_RIGHT_REAR_FORWARD, config.MOTOR_RIGHT_REAR_BACKWARD)), left_enable_pins=(config.MOTOR_LEFT_FRONT_ENABLE,config.MOTOR_LEFT_REAR_ENABLE), right_enable_pins=(config.MOTOR_RIGHT_FRONT_ENABLE,config.MOTOR_RIGHT_REAR_ENABLE))
    arm = ArmController(shoulder_pins=(config.MOTOR_ARM_SHOULDER_FORWARD, config.MOTOR_ARM_SHOULDER_BACKWARD, config.MOTOR_ARM_SHOULDER_ENABLE), elbow_pins=(config.MOTOR_ARM_ELBOW_FORWARD, config.MOTOR_ARM_ELBOW_BACKWARD, config.MOTOR_ARM_ELBOW_ENABLE), hand_pins=(config.MOTOR_ARM_HAND_FORWARD, config.MOTOR_ARM_HAND_BACKWARD, config.MOTOR_ARM_HAND_ENABLE))
    gamepad = GamepadController()
    camera = CameraController(save_dir=f"{config.SD_CARD_PATH}/photos")
    sensors = SensorController()
    gps = GpsReader() 
    logger = DataLogger(file_path=f"{config.SD_CARD_PATH}/sensor_log.csv")
    servos = ServoController(base_pin=config.ARM_BASE_SERVO_PIN)
    navigator = Navigator()

    is_stabilizing = False
    current_heading = 0.0
    last_heading_time = time.time()
    target_destination = None

    control_mode = "drive"  # Başlangıç kontrol modu

    print("Kurulum tamamlandı. ARCRover hazır.")
    print(f"Fotoğraf için '{config.GAMEPAD_BUTTON_PHOTO}' basın")
    print(f"Log için '{config.GAMEPAD_BUTTON_LOG_DATA}' basın")

    # --- Main Loop ---
    try:
        while True:
            current_location = gps.get_location()
            _, gyro, _ = sensors.read_imu()

            if gyro and gyro[2] is not None:
                dt = time.time() - last_heading_time
                current_heading += gyro[2] * dt
                current_heading %= 360
                last_heading_time = time.time()


            if gamepad.was_button_pressed(config.GAMEPAD_BUTTON_TOGGLE_MODE):
                if control_mode == "drive":
                    control_mode = "arm"
                    motors.stop()
                    
                else:
                    control_mode = "drive"
                    arm.stop()
                print(f"Kontrol modu değiştirildi: {control_mode}")  


            if gamepad.was_button_pressed(config.GAMEPAD_BUTTON_NAV_START):
                control_mode = "navigate"
                target_destination = (41.085, 29.032)  # Örnek hedef koordinatlar
                motors.stop(); arm.stop(); servos.stop()
                print(f"Navigasyon modu başlatıldı. Hedef: {target_destination}")
            else:
                print("[HATA] Navigasyon başlatıldı. Hedef koordinat yok.")

            if control_mode == "drive":
                forward_speed, turn_speed = gamepad.get_drive_values()
                should_stabilize_now = (forward_speed != 0 and turn_speed == 0)
                if should_stabilize_now and not is_stabilizing:
                    motors.set_target_heading(current_heading)
                is_stabilizing = should_stabilize_now
                motors.drive(forward_speed, turn_speed, is_stabilizing, current_heading)
            
           
            elif control_mode == "arm":
                shoulder, elbow, hand, base_rotation = gamepad.get_arm_values()
                arm.control_arm(shoulder, elbow, hand)
                servos.control_base_rotation(base_rotation)
           
            elif control_mode == "navigate":
                if current_location[0] is not None and target_destination is not None:
                    # Get autonomous commands
                    fwd, turn, dist = navigator.get_navigation_commands(
                        current_location,
                        target_destination,
                        current_heading
                    )
                    # Drive the motors with the calculated commands
                    motors.drive(fwd, turn, False, 0)
                    
                    # If we have arrived, switch back to manual drive mode
                    if dist < config.NAV_ARRIVAL_DISTANCE:
                        control_mode = "drive"
                        print("Hedefe ulaşıldı. Manuel kontrol moduna geçildi.")
                else:
                    motors.stop() # Stop if we lose GPS signal

            if gamepad.was_button_pressed(config.GAMEPAD_BUTTON_PHOTO):
                print("Fotoğraf çekme butonuna basıldı!")
                camera.take_photo()

            if gamepad.was_button_pressed(config.GAMEPAD_BUTTON_LOG_DATA):
                print("Loglama butonuna basıldı!")
                
                air_humidity, temp = sensors.read_dht11()
                soil_moisture = sensors.read_soil_moisture()
                accel, gyro, mag = sensors.read_imu()
                location = gps.get_location()

                
                logger.log(location, air_humidity, temp, soil_moisture, accel, gyro, mag)

                

            
            time.sleep(0.02)

    except KeyboardInterrupt:
        print("\nKapatılıyor...")
    finally:
        
        motors.stop()
        arm.stop()
        servos.stop()
        gps.stop()
        camera.stop()
        print("Rover durduruldu.")


if __name__ == "__main__":
    main()