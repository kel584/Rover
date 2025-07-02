# data_logger.py

import os
import csv
from datetime import datetime

class DataLogger:
    """Handles writing sensor data to a CSV file."""
    def __init__(self, file_path):
        self.file_path = file_path
        
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        
        # Write the header row if the file is new
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    "Timestamp", "AirHumidity(%)", "AirTemp(C)", "SoilMoisture(%)",
                    "AccelX(m/s^2)", "AccelY(m/s^2)", "AccelZ(m/s^2)",
                    "GyroX(deg/s)", "GyroY(deg/s)", "GyroZ(deg/s)",
                    "MagX(uT)", "MagY(uT)", "MagZ(uT)"
                ])
        print(f"Data logger hazır. Log konumu:{self.file_path}")

    def log(self, air_humidity, temp, soil_moisture, accel, gyro, mag):
        
        try:
            with open(self.file_path, 'a', newline='') as f:
                writer = csv.writer(f)
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                
                def fmt(data):
                    return data if data is not None else 'N/A'
                
                writer.writerow([
                    timestamp,
                    fmt(air_humidity), fmt(temp), fmt(soil_moisture),
                    fmt(accel[0]), fmt(accel[1]), fmt(accel[2]),
                    fmt(gyro[0]), fmt(gyro[1]), fmt(gyro[2]),
                    fmt(mag[0]), fmt(mag[1]), fmt(mag[2])
                ])
            print("[SUCCESS] Sensor data başarıyla loglandı.")
        except Exception as e:
            print(f"[ERROR] Log dosyasına yazarken hata: {e}")