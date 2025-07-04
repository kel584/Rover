# config.py
import cv2

SD_CARD_PATH = "/home/pi/ARCRover/SDCard"

MISSION_PLAN = [
    {"id": 11, "gps": (41.0851, 29.0451), "color": "red"},
    {"id": 40, "gps": (41.0852, 29.0452), "color": "green"},
    {"id": 17, "gps": (41.0853, 29.0453), "color": "blue"},
    {"id": 65, "gps": (41.0854, 29.0454), "color": "red"},
    {"id": 72, "gps": (41.0855, 29.0455), "color": "green"},
    {"id": 77, "gps": (41.0856, 29.0456), "color": "blue"},
    {"id": 93, "gps": (41.0857, 29.0457), "color": "red"},
    {"id": 93, "gps": (41.0858, 29.0458), "color": "green"},
    {"id":  1, "gps": (41.0859, 29.0459), "color": "blue"},
    {"id": 60, "gps": (41.0860, 29.0460), "color": "red"}
]

ARUCO_DICTIONARY = cv2.aruco.DICT_5X5_100

COLOR_RANGES = {
    "red": ((0, 120, 70), (10, 255, 255)),
    "green": ((36, 100, 70), (86, 255, 255)),
    "blue": ((94, 100, 70), (126, 255, 255)),
}

SCAN_ROTATION_SPEED = 0.3      # arama modunda dönme hızı
VISUAL_HOMING_KP_TURN = 0.5    # görsel homing için P kazancı
VISUAL_HOMING_KP_FORWARD = 0.01# görsel homing için P kazancı
VISUAL_TARGET_TAG_AREA = 15000 # (pixels^2) hedef etiket alanı


NAV_ARRIVAL_DISTANCE = 2.0
NAV_ARRIVAL_DISTANCE_PX = 25.0
NAV_FORWARD_SPEED = 0.5
NAV_KP = 1.2
NAV_KI = 0.01
NAV_KD = 0.05
SCAN_ROTATION_SPEED = 0.3
NAV_DEADBAND = 5.0
NAV_TURN_RATE_LIMIT = 60.0
NAV_TURN_MAX = 1.0
NAV_STATE_ERROR_THRESHOLD = 10.0
NAV_KP_MOVE = 0.3
NAV_TURN_MOVE_MAX = 0.4
NAV_ARRIVAL_DISTANCE = 0.2
VISUAL_HOMING_KP_TURN = 0.5
VISUAL_HOMING_KP_FORWARD = 0.01
VISUAL_TARGET_TAG_AREA = 15000

GAMEPAD_AXIS_LEFT_Y = 'ABS_Y'
GAMEPAD_AXIS_RIGHT_X = 'ABS_RX'
GAMEPAD_BUTTON_A = 'BTN_SOUTH'  
GAMEPAD_BUTTON_B = 'BTN_EAST'  
GAMEPAD_BUTTON_X = 'BTN_WEST'   
GAMEPAD_BUTTON_Y = 'BTN_NORTH'    
GAMEPAD_BUTTON_PHOTO = GAMEPAD_BUTTON_X  
GAMEPAD_BUTTON_LOG_DATA = GAMEPAD_BUTTON_A 
GAMEPAD_BUTTON_TOGGLE_MODE = GAMEPAD_BUTTON_Y
GAMEPAD_BUTTON_NAV_START = GAMEPAD_BUTTON_B

GAMEPAD_BUTTON_L1 = 'BTN_TL'      # Left Bumper (Elbow)
GAMEPAD_BUTTON_L2 = 'BTN_TL2'     # Left Trigger (Elbow)
GAMEPAD_BUTTON_R1 = 'BTN_TR'      # Right Bumper (Hand)
GAMEPAD_BUTTON_R2 = 'BTN_TR2'     # Right Trigger (Hand)
GAMEPAD_AXIS_DPAD_Y = 'ABS_HAT0Y' # D-Pad Up/Down (Shoulder)

GAMEPAD_DEADZONE = 0.5
GAMEPAD_TURN_EXPO = 2.0

#driver 1
MOTOR_LEFT_FRONT_FORWARD = 17 #IN1 forward
MOTOR_LEFT_FRONT_BACKWARD = 27 #IN2 backward
MOTOR_LEFT_FRONT_ENABLE = 16  #ENA speed

MOTOR_LEFT_REAR_FORWARD = 22 #IN3 forward
MOTOR_LEFT_REAR_BACKWARD = 5 #IN4 backward
MOTOR_LEFT_REAR_ENABLE = 19 #ENB speed

#driver 2
MOTOR_RIGHT_FRONT_FORWARD = 23 #IN1 forward
MOTOR_RIGHT_FRONT_BACKWARD = 24 #IN2 backward
MOTOR_RIGHT_FRONT_ENABLE = 20 #ENA speed

MOTOR_RIGHT_REAR_FORWARD = 6 #IN3 forward
MOTOR_RIGHT_REAR_BACKWARD = 13 #IN4 backward
MOTOR_RIGHT_REAR_ENABLE = 21 #ENB speed

#driver 3
MOTOR_ARM_SHOULDER_FORWARD = 30 #IN1 forward
MOTOR_ARM_SHOULDER_BACKWARD = 31 #IN2 backward
MOTOR_ARM_SHOULDER_ENABLE = 32 #ENB speed

#driver 4
MOTOR_ARM_ELBOW_FORWARD = 26 #IN1 forward
MOTOR_ARM_ELBOW_BACKWARD = 18 #IN2 backward
MOTOR_ARM_ELBOW_ENABLE = 29 #ENA speed

MOTOR_ARM_HAND_FORWARD = 8 #IN3 forward
MOTOR_ARM_HAND_BACKWARD = 7 #IN4 backward 
MOTOR_ARM_HAND_ENABLE = 15 #ENB speed

CAMERA_SERVO_PIN = 25 #kullanılmıyor kamera kepçeye bağlı 
ARM_BASE_SERVO_PIN = 12    

#IMU stabilizasyon değerleri, değişebilir
STABILIZE_KP = 0.8  # Proportional gain
STABILIZE_KI = 0.2  # Integral gain
ARM_BASE_ROTATION_SPEED = 2.0 # degrees per second
# DHT11 
DHT11_PIN = 4 

# MCP3008
SOIL_SENSOR_ADC_CHANNEL = 0

#adc değerini test edip belirle
SOIL_MOISTURE_DRY_VALUE = 800  #kuruyken
SOIL_MOISTURE_WET_VALUE = 400  #sudayken


#GPS
GPS_SERIAL_PORT = '/dev/serial0'
GPS_BAUD_RATE = 9600