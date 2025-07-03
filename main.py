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

def main():
    
    print("ARCRover başlatılıyor...")


    Device.pin_factory = PiGPIOFactory()

    motors = MotorController(left_pins=((config.MOTOR_LEFT_FRONT_FORWARD, config.MOTOR_LEFT_FRONT_BACKWARD),(config.MOTOR_LEFT_REAR_FORWARD, config.MOTOR_LEFT_REAR_BACKWARD)), right_pins=((config.MOTOR_RIGHT_FRONT_FORWARD, config.MOTOR_RIGHT_FRONT_BACKWARD),(config.MOTOR_RIGHT_REAR_FORWARD, config.MOTOR_RIGHT_REAR_BACKWARD)), left_enable_pins=(config.MOTOR_LEFT_FRONT_ENABLE,config.MOTOR_LEFT_REAR_ENABLE), right_enable_pins=(config.MOTOR_RIGHT_FRONT_ENABLE,config.MOTOR_RIGHT_REAR_ENABLE))
    gamepad = GamepadController()
    camera = CameraController(save_dir=f"{config.SD_CARD_PATH}/photos")
    sensors = SensorController()
    gps = GpsReader() 
    logger = DataLogger(file_path=f"{config.SD_CARD_PATH}/sensor_log.csv")

    is_stabilizing = False
    current_heading = 0.0
    last_heading_time = time.time()

    print("Kurulum tamamlandı. ARCRover hazır.")
    print(f"Fotoğraf için '{config.GAMEPAD_BUTTON_PHOTO}' basın")
    print(f"Log için '{config.GAMEPAD_BUTTON_LOG_DATA}' basın")

    # --- Main Loop ---
    try:
        while True:
           
            forward_speed, turn_speed = gamepad.get_drive_values()
            _, gyro, _ = sensors.read_imu()

            
            if gyro and gyro[2] is not None:
                dt = time.time() - last_heading_time

                current_heading += gyro[2] * dt
                current_heading = current_heading % 360.0
                last_heading_time = time.time()

            should_stabilize_now = (forward_speed !=0 and turn_speed == 0)

            if should_stabilize_now and not is_stabilizing:
                motors.set_target_heading(current_heading)

            is_stabilizing = should_stabilize_now

            motors.drive(forward_speed, turn_speed, is_stabilizing, current_heading)
           
            if gamepad.was_button_pressed(config.GAMEPAD_BUTTON_PHOTO):
                print("Fotoğraf çekme butonuna basıldı!")
                camera.take_photo()

            if gamepad.was_button_pressed(config.GAMEPAD_BUTTON_LOG_DATA):
                print("Loglama butonuna basıldı!")
                
                air_humidity, temp = sensors.read_dht11()
                soil_moisture = sensors.read_soil_moisture()
                accel, gyro, mag = sensors.read_imu()
                location = gps.get_location() 

                
                logger.log(air_humidity, temp, soil_moisture, location, accel, gyro, mag) 

            
            time.sleep(0.02)

    except KeyboardInterrupt:
        print("\nKapatılıyor...")
    finally:
        
        motors.stop()
        gps.stop() 
        print("Rover durduruldu.")


if __name__ == "__main__":
    main()