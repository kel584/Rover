# gamepad_controller.py

from inputs import get_gamepad
import threading
import config
import math
import time

class GamepadController:
    def __init__(self):
        self.left_y, self.right_x = 0.0, 0.0
        self.dpad_y = 0
        self.l2_axis, self.r2_axis = 0.0, 0.0
        self.pressed_buttons, self.newly_pressed_buttons = set(), set()
        self.thread = threading.Thread(target=self._listen, daemon=True)
        self.thread.start()
        print("[READY] Gamepad listener başlatıldı.")

    def _listen(self):
        while True:
            try:
                for event in get_gamepad():
                    self._process_event(event)
            except Exception as e:
                print(f"[ERROR] Gamepad hatası: {e}")
                time.sleep(1)

    def _process_event(self, event):
        if event.ev_type == 'Absolute':
            value = event.state
            if event.code == config.GAMEPAD_AXIS_LEFT_Y: self.left_y = -value / 32767.0
            elif event.code == config.GAMEPAD_AXIS_RIGHT_X: self.right_x = value / 32767.0
            elif event.code == config.GAMEPAD_AXIS_DPAD_Y: self.dpad_y = value
            elif event.code == config.GAMEPAD_BUTTON_L2: self.l2_axis = value / 255.0
            elif event.code == config.GAMEPAD_BUTTON_R2: self.r2_axis = value / 255.0
        elif event.ev_type == 'Key':
            is_pressed = (event.state == 1)
            if is_pressed and event.code not in self.pressed_buttons: self.newly_pressed_buttons.add(event.code)
            if is_pressed: self.pressed_buttons.add(event.code)
            elif event.code in self.pressed_buttons: self.pressed_buttons.remove(event.code)

    def get_drive_values(self):
        fwd, turn = self.left_y, self.right_x
        if abs(fwd) < config.GAMEPAD_DEADZONE: fwd = 0.0
        if abs(turn) < config.GAMEPAD_DEADZONE: turn = 0.0
        turn = math.copysign(pow(abs(turn), config.GAMEPAD_TURN_EXPO), turn)
        return fwd, turn

    def get_arm_values(self):
        shoulder = -self.dpad_y
        elbow = (1.0 if config.GAMEPAD_BUTTON_L1 in self.pressed_buttons else 0.0) - self.l2_axis
        hand = (1.0 if config.GAMEPAD_BUTTON_R1 in self.pressed_buttons else 0.0) - self.r2_axis
        base_rotation = self.right_x
        if abs(base_rotation) < config.GAMEPAD_DEADZONE: base_rotation = 0.0
        return shoulder, elbow, hand, base_rotation

    def was_button_pressed(self, button_code):
        if button_code in self.newly_pressed_buttons:
            self.newly_pressed_buttons.remove(button_code)
            return True
        return False