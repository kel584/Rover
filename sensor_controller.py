# sensor_controller.py

import adafruit_dht
import board
from adafruit_mcp3xxx.mcp3008 import MCP3008
from adafruit_mcp3xxx.analog_in import AnalogIn
import busio
import digitalio
import config
from mpu9250_jmdev.mpu_9250 import MPU9250
from mpu9250_jmdev.ak8963 import AK8963

class SensorController:
    """tüm sensörler için"""

    def __init__(self):
        #dht 11 kurulum
        try:
            self.dht_device = adafruit_dht.DHT11(board.D4) # Uses board.D# from config
        except Exception as e:
            self.dht_device = None
            print(f"[ERROR] DHT11 Kurulamadı:{e}")
            
        # --- MCP3008 (Soil Moisture) Setup ---
        try:
            spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
            cs = digitalio.DigitalInOut(board.CE0)
            mcp = MCP3008(spi, cs)
            self.soil_sensor = AnalogIn(mcp, config.SOIL_SENSOR_ADC_CHANNEL)
        except Exception as e:
            self.soil_sensor = None
            print(f"[ERROR] MCP3008 ADC: {e}")

        # --- MPU9255 (IMU) Setup ---
        try:
            self.imu = MPU9250()
        except Exception as e:
            self.imu = None
            print(f"[ERROR] MPU9250 IMU: {e}")

        print("Sensor controller hazır.")

    def read_dht11(self):
        if not self.dht_device:
            return None, None
        try:
            temperature = self.dht_device.temperature
            humidity = self.dht_device.humidity
            # The DHT11 can occasionally return None, so we handle that.
            if temperature is not None and humidity is not None:
                return humidity, temperature
        except RuntimeError as e:
            # DHT sensors are prone to timing errors
            print(f"[ERROR] DHT11 okuma hatası: {e}")
        return None, None

    def read_soil_moisture(self):
   
        if not self.soil_sensor:
            return None
        try:
            raw_value = self.soil_sensor.value
            # Convert the 16-bit value from library to 10-bit equivalent
            raw_10bit = raw_value >> 6 
            
            # Map the raw value to a percentage
            dry = config.SOIL_MOISTURE_DRY_VALUE
            wet = config.SOIL_MOISTURE_WET_VALUE
            
            percentage = 100.0 * (dry - raw_10bit) / (dry - wet)
            # Clamp the value between 0 and 100
            percentage = max(0.0, min(100.0, percentage))
            return percentage
        except Exception as e:
            print(f"[ERROR] Toprak nemi okuma hatası: {e}")
            return None

    def read_imu(self):
        
        if not self.imu:
            return (None,None,None), (None,None,None), (None,None,None)
        try:
            accel = self.imu.read_accelerometer() # Returns (x, y, z) in m/s^2
            gyro = self.imu.read_gyroscope()     # Returns (x, y, z) in deg/s
            mag = self.imu.read_magnetometer()   # Returns (x, y, z) in uT
            return accel, gyro, mag
        except Exception as e:
            print(f"IMU read error: {e}")
            return (None,None,None), (None,None,None), (None,None,None)