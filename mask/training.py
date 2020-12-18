"""
    Training de nuestro modelo de clasificación de rostros con mascarilla
"""

from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report
from util_training import *

# Lectura de la data
data, labels = load_images('data/with_mask/', 'data/without_mask/')

# One-Hot encoding de los labels
labels = encode_labels(labels)

# 80% training - 20% testing
X_train, X_test, Y_train, Y_test = train_test_split(data, labels, test_size = 0.15,
                                                    stratify = labels, random_state = 40)
# Construimos el modelo
model = build_model()

# Data Augmentation para considerar distintas transformaciones sobre las 
# imagenes de training (rotationces, zoom, flip, etc)
aug = ImageDataGenerator(rotation_range = 40, zoom_range = 0.3,
                         width_shift_range = 0.3, height_shift_range = 0.3,
                         shear_range = 0.3, horizontal_flip = True, fill_mode = 'nearest')

# Training
H = model.fit(aug.flow(X_train, Y_train, batch_size = BS),
              steps_per_epoch = len(X_train) // BS,
              validation_data = (X_test, Y_test),
	      validation_steps = len(X_test) // BS,
	      epochs = EPOCHS, 
              verbose = 1)

# Hacemos la predicción
predictions = model.predict(X_test, batch_size = BS)

# Imprimimos las métricas
print(classification_report(Y_test.argmax(axis = 1), predictions.argmax(axis = 1), target_names = lb.classes_))

# Guardamos el modelo
model.save('mask_detector.hdf5')

# Graficamos las métricas
draw_metrics(EPOCHS, H)
