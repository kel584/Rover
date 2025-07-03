# gamepad_controller.py

from inputs import get_gamepad
import threading
import config

class GamepadController:
    #başka threadde çalışıyor
    def __init__(self):
        self.left_y = 0
        self.right_x = 0
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
            
        return forward, turn

    def was_button_pressed(self, button_code):

        if button_code in self.newly_pressed_buttons:
            self.newly_pressed_buttons.remove(button_code)
            return True
        return False