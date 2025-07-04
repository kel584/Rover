# vision_controller.py

import cv2
from picamera2 import Picamera2
import time
import config
import numpy as np

class VisionController:
    def __init__(self):
        print("[VISION] Kamera başlatılıyor...")
        self.picam2 = Picamera2()
        cam_config = self.picam2.create_preview_configuration(main={"size": (640, 480)})
        self.picam2.configure(cam_config)
        self.picam2.start()
        time.sleep(1.0)
        
        print("[VISION] Aruco detector başlatılıyor...")
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(config.ARUCO_DICTIONARY)
        aruco_params = cv2.aruco.DetectorParameters()
        self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, aruco_params)
        print("[VISION] Görüş sistemi hazır.")

    def _get_border_color(self, frame, corners):
        """Analyzes the pixels around a tag to determine its border color."""
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = np.zeros(frame.shape[:2], dtype="uint8")

        #cornersu dönüştür
        pts_int = corners.astype(np.int32)
        
        #çizgiyi çiz
        cv2.polylines(mask, [pts_int], True, (255, 255, 255), thickness=20)
        cv2.fillPoly(mask, [pts_int], (0, 0, 0))

        detected_colors = {}
        for color_name, (lower, upper) in config.COLOR_RANGES.items():
           
            lower_np = np.array(lower, dtype=np.uint8)
            upper_np = np.array(upper, dtype=np.uint8)
            color_mask = cv2.inRange(hsv_frame, lower_np, upper_np)
            color_in_border = cv2.bitwise_and(color_mask, color_mask, mask=mask)
            detected_colors[color_name] = cv2.countNonZero(color_in_border)

        
        if max(detected_colors.values()) > 100:
            return max(detected_colors, key=lambda x: detected_colors[x])
        
        return "unknown"

    def detect_tags(self):
        """
        Captures a frame, detects ArUco tags, and their border colors.
        Returns a list of detected tag objects and the annotated frame.
        """
        frame = self.picam2.capture_array()
        
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        (corners_list, ids, rejected) = self.detector.detectMarkers(frame_bgr)
        
        detected_objects = []
        if ids is not None:
            for i, tag_id in enumerate(ids):
                tag_corners = corners_list[i]
                border_color = self._get_border_color(frame_bgr, tag_corners)
                
                detected_objects.append({
                    "id": tag_id[0],
                    "corners": tag_corners,
                    "color": border_color
                })
               
                cv2.putText(frame_bgr, border_color,
                            (int(tag_corners[0][0][0]), int(tag_corners[0][0][1]) - 15),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        
        if corners_list:
            cv2.aruco.drawDetectedMarkers(frame_bgr, corners_list, ids)

        return detected_objects, frame_bgr
        
    def stop(self):
        if self.picam2.started:
            self.picam2.stop()
            print("[VISION] Kamera durduruldu.")