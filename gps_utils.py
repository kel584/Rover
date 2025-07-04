# gps_utils.py
import math

class GpsConverter:

    def __init__(self, origin_lat: float, origin_lon: float):

        self.origin_lat = origin_lat
        self.origin_lon = origin_lon
        print(f"GPS Dönüştürücü orjin: ({origin_lat}, {origin_lon})")

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        
        R = 6371000  # Radius of Earth in meters
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi/2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2)**2
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    def gps_to_local_xy(self, current_lat: float, current_lon: float) -> tuple[float, float]:

        # Calculate the 'y' distance (North/South)
        y_meters = self.haversine_distance(self.origin_lat, self.origin_lon, current_lat, self.origin_lon)
        if current_lat < self.origin_lat:
            y_meters *= -1

        # Calculate the 'x' distance (East/West)
        x_meters = self.haversine_distance(self.origin_lat, self.origin_lon, self.origin_lat, current_lon)
        if current_lon < self.origin_lon:
            x_meters *= -1
            
        return (x_meters, y_meters)