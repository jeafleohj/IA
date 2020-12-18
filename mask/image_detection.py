"""
    Reconoce el rostro en una imagen y determina si se está usando mascarilla
"""

import argparse
import cv2
import imutils
from util_detection import *

# Parsear argumentos
ap = argparse.ArgumentParser()
ap.add_argument('-i', '--input', required=True, help='Path de la imagen a procesar')
args = ap.parse_args()

face_model, mask_model = load_models()
image = cv2.imread(args.input)
image = imutils.resize(image, height = 600, width = 800)
detections = detect_faces(image, face_model)
locs, labels = detect_masks(image, detections, mask_model)
draw_rectangles(image, locs, labels)
cv2.imwrite(OUTPUT_FILE, image)
