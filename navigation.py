# navigation.py
import math
import time
import config

class Navigator:

    def __init__(self):
        self.last_time = time.time()
        self.last_turn_cmd = 0.0
        print("2D Navigator Hazır.")
        
    def _heading_error(self, target_deg, current_deg):
        
        delta = math.atan2(
            math.sin(math.radians(target_deg - current_deg)),
            math.cos(math.radians(target_deg - current_deg))
        )
        return math.degrees(delta)

    def _get_target_heading_2d(self, current_pos, target_pos):
        
        cx, cy = current_pos
        tx, ty = target_pos
        delta_x = tx - cx
        delta_y = ty - cy
        
        # Use atan2 to get the angle from the positive X-axis
        rad = math.atan2(delta_y, delta_x)
        
        # Convert atan2 angle to our rover's heading system (0=East, 90=North)
        # Pygame's Y-axis is inverted, so we negate the angle.
        heading = math.degrees(rad)
        return (heading + 360) % 360

    def get_navigation_commands(self, current_pos_m, target_pos_m, current_heading):

        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        # Calculate 2D distance
        dist_meters = math.hypot(target_pos_m[0] - current_pos_m[0], target_pos_m[1] - current_pos_m[1])

        if dist_meters < config.NAV_ARRIVAL_DISTANCE:
            return 0.0, 0.0, dist_meters

        target_heading = self._get_target_heading_2d(current_pos_m, target_pos_m)
        error = self._heading_error(target_heading, current_heading)

        turn = config.NAV_KP * error

        if abs(error) < config.NAV_DEADBAND:
            turn = 0.0

        speed_reduction_factor = max(0.0, 1.0 - abs(error) / 90.0)
        forward = config.NAV_FORWARD_SPEED * speed_reduction_factor

        turn = max(-config.NAV_TURN_MAX, min(config.NAV_TURN_MAX, turn))
        

        print(
            f"[NAV] TargetHdg:{target_heading:.1f}°, "
            f"Err:{error:.1f}°, Fwd:{forward:.2f}, Turn:{turn:.2f}"
        )

        return forward, turn, dist_meters