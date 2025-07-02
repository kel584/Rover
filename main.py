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

    motors = MotorController(
        left_pins=(config.MOTOR_LEFT_FORWARD, config.MOTOR_LEFT_BACKWARD),
        right_pins=(config.MOTOR_RIGHT_FORWARD, config.MOTOR_RIGHT_BACKWARD)
    )
    gamepad = GamepadController()
    camera = CameraController(save_dir=f"{config.SD_CARD_PATH}/photos")
    sensors = SensorController()
    gps = GpsReader() 
    logger = DataLogger(file_path=f"{config.SD_CARD_PATH}/sensor_log.csv")

    print("Kurulum tamamlandı. ARCRover hazır.")
    print(f"Fotoğraf için '{config.GAMEPAD_BUTTON_PHOTO}' basın")
    print(f"Log için '{config.GAMEPAD_BUTTON_LOG_DATA}' basın")

    # --- Main Loop ---
    try:
        while True:
           
            forward, turn = gamepad.get_drive_values()

            
            motors.drive(forward, turn)

           
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