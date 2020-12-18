import os
import numpy as np
import cv2
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

MIN_SIZE = 10
THRESHOLD = 0.90
BATCH_SIZE = 32
MASK_TEXT, MASK_COLOR = 'Con mascarilla (:', (0, 255, 0)
NO_MASK_TEXT, NO_MASK_COLOR = 'Sin marcarilla :(', (0, 0, 255)
OUTPUT_FILE = 'salida.jpg'

def load_models ():
    # Cargando el modelo de detección de rostros
    proto_path = os.path.sep.join(['face_detector', 'deploy.prototxt'])
    weight_path = os.path.sep.join(['face_detector', 'res10_300x300_ssd_iter_140000.caffemodel'])
    face_model = cv2.dnn.readNet(proto_path, weight_path)
    # Cargando el modelo de detección de mascarillas
    mask_model = load_model('mask_detector.model')
    return face_model, mask_model

def detect_faces (frame, face_model):
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), (104, 177, 123))
    face_model.setInput(blob)
    return face_model.forward()

def detect_masks (frame, detections, mask_model):
    faces, locs, labels = [], [], []
    h, w = frame.shape[:2]
    for k in range(0, detections.shape[2]):
        prob = detections[0, 0, k, 2]
        if prob <= THRESHOLD: continue
        box = detections[0, 0, k, 3:7] * np.array([w, h, w, h])
        x1, y1, x2, y2 = box.astype('int')
        # Asegurar que 'box' no se salga de la imagen
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w - 1, x2), min(h - 1, y2)
        # Obtener la ROI
        if min(y2 - y1, x2 - x1) < MIN_SIZE: continue
        face = frame[y1:y2, x1:x2]
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        face = cv2.resize(face, (224, 224))
        face = img_to_array(face)
        face = preprocess_input(face)
        faces.append(face)
        locs.append((x1, y1, x2, y2))
        
    if len(faces) > 0:
        faces = np.array(faces, dtype='float32')
        labels = mask_model.predict(faces, batch_size=BATCH_SIZE)
    return (np.array(locs), np.array(labels))

def draw_rectangles (frame, locs, labels):
    for loc, label in zip(locs, labels):
        x1, y1, x2, y2 = loc
        mask, no_mask = label
        tag = MASK_TEXT if mask > no_mask else NO_MASK_TEXT
        color = MASK_COLOR if mask > no_mask else NO_MASK_COLOR
        text = '%s => %.2f%%' % (tag, max(mask, no_mask) * 100)
        cv2.putText(frame, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
