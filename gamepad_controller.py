# gamepad_controller.py

from inputs import get_gamepad
import threading
import config
import math

class GamepadController:
    #başka threadde çalışıyor
    def __init__(self):
        self.left_y = 0
        self.right_x = 0
        self.dpad_y = 0
        self.pressed_buttons = set()
        self.newly_pressed_buttons = set()

        # gamepad eventlerini dinlemek için bir thread başlat
        self.thread = threading.Thread(target=self._listen, daemon=True)
        self.thread.start()
        print("[READY] Gamepad listener başlatıldı.")

    def _listen(self):
        while True:
            try:
                events = get_gamepad()
                for event in events:
                    self._process_event(event)
            except Exception as e:
                print(f"[ERROR] Gamepad hatası: {e}. Takılı olduğundan emin ol.")
                
                self.left_y = 0
                self.right_x = 0
                self.pressed_buttons.clear()

    def _process_event(self, event):
        
        
        if event.ev_type == 'Absolute':
            if event.code == config.GAMEPAD_AXIS_LEFT_Y:
                # y eksenini pozitif olması için ters çevir.
                self.left_y = -event.state
            elif event.code == config.GAMEPAD_AXIS_RIGHT_X:
                self.right_x = event.state
            elif event.code == config.GAMEPAD_AXIS_DPAD_Y: 
                self.dpad_y = event.state #-1 up 1 down
        # Button events
        elif event.ev_type == 'Key':
            if event.state == 1:  # Button basıldı
                self.pressed_buttons.add(event.code)
                self.newly_pressed_buttons.add(event.code)
            elif event.state == 0:  # Button bırakıldı
                if event.code in self.pressed_buttons:
                    self.pressed_buttons.remove(event.code)

    def get_drive_values(self):
        # -1 0 arası değere kısıtla
        forward = self.left_y / 32767.0
        turn = self.right_x / 32767.0

        #Deadzone kontrolü
        if abs(forward) < config.GAMEPAD_DEADZONE:
            forward = 0.0
        if abs(turn) < config.GAMEPAD_DEADZONE:
            turn = 0.0
        turn = math.copysign(pow(abs(turn), config.GAMEPAD_TURN_EXPO), turn)
        return forward, turn
    
    def get_arm_values(self):
        shoulder_speed = 0.0
        elbow_speed = 0.0
        hand_speed = 0.0


        shoulder_speed = -self.dpad_y

        if config.GAMEPAD_BUTTON_L1 in self.pressed_buttons:
            elbow_speed = 1.0
        elif config.GAMEPAD_BUTTON_L2 in self.pressed_buttons:
            elbow_speed = -1.0
        if config.GAMEPAD_BUTTON_R1 in self.pressed_buttons:
            hand_speed = 1.0
        elif config.GAMEPAD_BUTTON_R2 in self.pressed_buttons:
            hand_speed = -1.0

        base_rotation_speed = self.right_x / 32767.0
        if abs(base_rotation_speed) < config.GAMEPAD_DEADZONE:
            base_rotation_speed = 0.0

        return shoulder_speed, elbow_speed, hand_speed, base_rotation_speed
    

    def was_button_pressed(self, button_code):

        if button_code in self.newly_pressed_buttons:
            self.newly_pressed_buttons.remove(button_code)
            return True
        return False