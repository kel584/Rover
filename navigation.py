# navigation.py

import math
import time
import config

class Navigator:

    def __init__(self):
       
        self.integral_error = 0.0
        self.last_time = None
        print("Navigasyon modülü hazır.")

    def get_navigation_commands(self, current_coords, target_coords, current_heading):

        current_lat, current_lon = current_coords
        target_lat, target_lon = target_coords

        
        distance = self._haversine_distance(current_lat, current_lon, target_lat, target_lon)

        if distance < config.NAV_ARRIVAL_DISTANCE:
            print(f"[NAV] Hedefe ulaşıldı! Kalan mesafe: {distance:.2f}m")
            self.integral_error = 0 # Reset for next run
            return 0.0, 0.0, distance 

        
        target_heading = self._calculate_bearing(current_lat, current_lon, target_lat, target_lon)

        
        error = target_heading - current_heading
        
        if error > 180:
            error -= 360
        elif error < -180:
            error += 360
        
    
        dt = 0.0
        if self.last_time is not None:
            dt = time.time() - self.last_time
        self.last_time = time.time()
        
        self.integral_error += error * dt
       
        self.integral_error = max(-10.0, min(10.0, self.integral_error))

        turn_speed = (config.NAV_KP * error) + (config.NAV_KI * self.integral_error)
        turn_speed = max(-1.0, min(1.0, turn_speed)) 


        forward_speed = config.NAV_FORWARD_SPEED * (1 - abs(turn_speed))

        print(f"[NAV] Mesafe: {distance:.1f}m | Yön: {current_heading:.1f}° -> {target_heading:.1f}° | Hata: {error:.1f}° | Dönüş: {turn_speed:.2f}")

        return forward_speed, turn_speed, distance

    def _haversine_distance(self, lat1, lon1, lat2, lon2):
        
        R = 6371000  #dünya yarıçapı metre
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)

        a = math.sin(delta_phi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def _calculate_bearing(self, lat1, lon1, lat2, lon2):
        
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        d_lon = lon2_rad - lon1_rad
        y = math.sin(d_lon) * math.cos(lat2_rad)
        x = math.cos(lat1_rad) * math.sin(lat2_rad) - math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(d_lon)
        
        bearing_rad = math.atan2(y, x)
        bearing_deg = math.degrees(bearing_rad)
        
        return (bearing_deg + 360) % 360