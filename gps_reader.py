# gps_reader.py

import serial
import pynmea2
import threading
import time
import config

class GpsReader:

    def __init__(self):
        self.port = config.GPS_SERIAL_PORT
        self.baud = config.GPS_BAUD_RATE
        self.serial_port = None
        self.latitude = None
        self.longitude = None
        self.timestamp = None
        self.is_running = True

        try:
            self.serial_port = serial.Serial(self.port, self.baud, timeout=1.0)
            self.thread = threading.Thread(target=self._read_loop, daemon=True)
            self.thread.start()
            print("GPS reader started.")
        except serial.SerialException as e:
            print(f"[ERROR] Gps seri portu açılamadı: {self.port}. Error: {e}")
            self.serial_port = None
            
    def _read_loop(self):
        
        while self.is_running and self.serial_port:
            try:
                line = self.serial_port.readline().decode('ascii', errors='replace')
                if line.startswith('$GPRMC'): 
                    msg = pynmea2.parse(line)
                    if isinstance(msg, pynmea2.types.talker.RMC) and msg.status == 'A':
                        self.latitude = msg.latitude
                        self.longitude = msg.longitude
                        self.timestamp = msg.datetime
            except Exception as e:
                
                print(f"[ERROR] GPS read loop error: {e}")
            time.sleep(0.1)

    def get_location(self):

        return self.latitude, self.longitude

    def stop(self):
        
        self.is_running = False
        if self.thread.is_alive():
            self.thread.join()
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
            print("GPS reader stopped.")