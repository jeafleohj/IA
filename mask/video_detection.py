"""
    Reconoce el rostro usando la cámara de la laptop y determina si se está usando mascarilla
"""

import cv2
import imutils
from util_detection import *

FRAME_RESOLUTION = 3
WINDOWS_TITLE = 'Detector de mascarillas'

face_model, mask_model = load_models()
cap = cv2.VideoCapture(0)
cv2.startWindowThread()
frame_cnt = FRAME_RESOLUTION - 1

while True:
    # Resize frame a como máximo un cuadrado de 600x600
    ret, frame = cap.read()
    frame = imutils.resize(frame, height = 800, width = 600)
    
    frame_cnt += 1
    if frame_cnt == FRAME_RESOLUTION:
        frame_cnt = 0
        detections = detect_faces(frame, face_model)
        locs, labels = detect_masks(frame, detections, mask_model)

    draw_rectangles(frame, locs, labels)
    cv2.namedWindow(WINDOWS_TITLE)
    cv2.moveWindow(WINDOWS_TITLE, 100, 100)
    cv2.imshow(WINDOWS_TITLE, frame)

    # Terminar cuando se presiona la letra q
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
