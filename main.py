# main.py

import time
from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import Device
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
from vision_controller import VisionController

# main.py

def main():
    
    print("ARCRover başlatılıyor...")
    Device.pin_factory = PiGPIOFactory()

    # --- Initializations ---
    motors = MotorController(left_pins=((config.MOTOR_LEFT_FRONT_FORWARD, config.MOTOR_LEFT_FRONT_BACKWARD),(config.MOTOR_LEFT_REAR_FORWARD, config.MOTOR_LEFT_REAR_BACKWARD)), right_pins=((config.MOTOR_RIGHT_FRONT_FORWARD, config.MOTOR_RIGHT_FRONT_BACKWARD),(config.MOTOR_RIGHT_REAR_FORWARD, config.MOTOR_RIGHT_REAR_BACKWARD)), left_enable_pins=(config.MOTOR_LEFT_FRONT_ENABLE,config.MOTOR_LEFT_REAR_ENABLE), right_enable_pins=(config.MOTOR_RIGHT_FRONT_ENABLE,config.MOTOR_RIGHT_REAR_ENABLE))
    arm = ArmController(shoulder_pins=(config.MOTOR_ARM_SHOULDER_FORWARD, config.MOTOR_ARM_SHOULDER_BACKWARD, config.MOTOR_ARM_SHOULDER_ENABLE), elbow_pins=(config.MOTOR_ARM_ELBOW_FORWARD, config.MOTOR_ARM_ELBOW_BACKWARD, config.MOTOR_ARM_ELBOW_ENABLE), hand_pins=(config.MOTOR_ARM_HAND_FORWARD, config.MOTOR_ARM_HAND_BACKWARD, config.MOTOR_ARM_HAND_ENABLE))
    gamepad = GamepadController()
    camera = CameraController(save_dir=f"{config.SD_CARD_PATH}/photos")
    sensors = SensorController()
    gps = GpsReader() 
    logger = DataLogger(file_path=f"{config.SD_CARD_PATH}/sensor_log.csv")
    servos = ServoController(base_pin=config.ARM_BASE_SERVO_PIN)
    navigator = Navigator()
    vision = VisionController() 

    # --- State Variables ---
    is_stabilizing = False
    current_heading = 0.0
    last_heading_time = time.time()
    target_destination = None
    control_mode = "drive"

    print("Kurulum tamamlandı. ARCRover hazır.")
   
    print(f"Kontrol Modları: '{config.GAMEPAD_BUTTON_TOGGLE_MODE}' Sürüş/Kol | '{config.GAMEPAD_BUTTON_NAV_START}' Navigasyon")

    try:
        while True:
            current_location = gps.get_location()
            _, gyro, _ = sensors.read_imu()

            if gyro and gyro[2] is not None:
                dt = time.time() - last_heading_time
                current_heading += gyro[2] * dt
                current_heading %= 360
                last_heading_time = time.time()

            #
            if gamepad.was_button_pressed(config.GAMEPAD_BUTTON_TOGGLE_MODE):
                control_mode = "arm" if control_mode == "drive" else "drive"
                motors.stop(); arm.stop(); servos.stop()
                print(f"Kontrol modu değiştirildi: {control_mode}")  

            
            if gamepad.was_button_pressed(config.GAMEPAD_BUTTON_NAV_START):
                if control_mode.startswith("NAV_"):
                    control_mode = "drive"
                    motors.stop()
                    print("Navigasyon iptal edildi. Manuel kontrol moduna geçildi.")
                elif current_location and current_location[0] is not None:
                    control_mode = "NAV_GPS"
                    waypoint_index = 0
                    motors.stop(); arm.stop(); servos.stop()
                    print(f"Navigasyon modu başlatıldı. Hedef: #{waypoint_index + 1}")
                else:
                    print("[HATA] Navigasyon başlatılamadı: GPS sinyali yok.")
            
            
            if control_mode == "drive":
                forward_speed, turn_speed = gamepad.get_drive_values()
                should_stabilize_now = (forward_speed != 0 and turn_speed == 0)
                if should_stabilize_now and not is_stabilizing: motors.set_target_heading(current_heading)
                is_stabilizing = should_stabilize_now
                motors.drive(forward_speed, turn_speed, is_stabilizing, current_heading)
            
            elif control_mode == "arm":
                shoulder, elbow, hand, base_rotation = gamepad.get_arm_values()
                arm.control_arm(shoulder, elbow, hand)
                servos.control_base_rotation(base_rotation)
           
            elif control_mode.startswith("NAV_"):
                if waypoint_index >= len(config.MISSION_PLAN):
                    print("Tüm waypointler tamamlandı! Görev başarılı.")
                    control_mode = "drive"
                    continue

                target_waypoint = config.MISSION_PLAN[waypoint_index]
                
                # PHASE 1: Waypoint'e git
                if control_mode == "NAV_GPS":
                    if current_location and current_location[0] is not None:
                        fwd, turn, dist = navigator.get_navigation_commands(current_location, target_waypoint["gps"], current_heading)
                        motors.drive(fwd, turn, False, 0)
                        if dist < config.NAV_ARRIVAL_DISTANCE:
                            motors.stop()
                            control_mode = "NAV_SCAN"
                            print(f"Waypoint #{waypoint_index + 1} yakınına ulaşıldı. ArUco ID aranıyor: {target_waypoint['id']}")
                    else:
                        motors.stop()
                
                # PHASE 2: Yerinde dönerek aruco tag'ı bul
                elif control_mode == "NAV_SCAN":
                    detected_objects, frame = vision.detect_tags()
                    found_target = False
                    if detected_objects:
                        for tag in detected_objects:
                            if tag['id'] == target_waypoint['id'] and tag['color'] == target_waypoint['color']:
                                motors.stop()
                                control_mode = "NAV_HOMING"
                                print(f"Hedef ID {target_waypoint['id']} ({target_waypoint['color']}) bulundu! Yaklaşılıyor...")
                                found_target = True
                                break
                    if not found_target:
                        motors.drive(0, config.SCAN_ROTATION_SPEED, False, 0)

                # PHASE 3: Kamerayı kullanarak onaylanan tag'e yaklaş
                elif control_mode == "NAV_HOMING":
                    detected_objects, frame = vision.detect_tags()
                    target_tag = next((tag for tag in detected_objects if tag['id'] == target_waypoint['id'] and tag['color'] == target_waypoint['color']), None)
                    
                    if target_tag:
                        fwd, turn, area = navigator.get_visual_homing_commands(frame.shape, target_tag['corners'])
                        motors.drive(fwd, turn, False, 0)
                        
                        # tag'a yaklaşıldıysa
                        if area > config.VISUAL_TARGET_TAG_AREA:
                            print(f"Waypoint #{waypoint_index + 1} tamamlandı!")
                            motors.stop()
                            time.sleep(2) # yaklaşıldığını onaylamak için bekle
                            
                            waypoint_index += 1
                            if waypoint_index >= len(config.MISSION_PLAN):
                                # görev tamamlandı, manuel kontrole geçiliyor.
                                pass
                            else:
                                print(f"Sıradaki hedefe geçiliyor: Waypoint #{waypoint_index + 1}")
                                control_mode = "NAV_GPS"
                    else:
                        # tag kaybolursa yeniden tara -> sorun çıkarabilir
                        print(f"Hedef ID {target_waypoint['id']} kayboldu, yeniden taranıyor...")
                        control_mode = "NAV_SCAN"

            
            if gamepad.was_button_pressed(config.GAMEPAD_BUTTON_PHOTO):
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
        motors.stop(); arm.stop(); servos.stop(); gps.stop(); camera.stop()
        print("Rover durduruldu.")


if __name__ == "__main__":
    main()