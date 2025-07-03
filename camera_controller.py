# camera_controller.py

from picamera2 import Picamera2
import time
import os

class CameraController:
    
    def __init__(self, save_dir):
        self.camera = Picamera2()
        self.save_dir = save_dir
        
        
        os.makedirs(self.save_dir, exist_ok=True)
        
        # fotoğraf çekmek için ayar
        self.config = self.camera.create_still_configuration()
        self.camera.configure(self.config)
        
        # kamerayı çalıştır ve bekle
        self.camera.start()
        time.sleep(2) 
        print("Camera kuruldu ve hazır.")

    def take_photo(self):
        
        try:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = f"{self.save_dir}/photo_{timestamp}.jpg"
            
            
            self.camera.capture_file(filename)
            print(f"[SUCCESS] Fotoğraf kaydedildi: {filename}")
        except Exception as e:
            print(f"[ERROR] Fotoğrafı çekerken hata: {e}")

    def stop(self):
        if self.camera.started:
            self.camera.stop()
            print("Kamera durduruldu.")