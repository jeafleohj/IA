import os
from os import listdir
from os.path import isfile, join
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelBinarizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Input, AveragePooling2D, Flatten, Dropout, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import SGD

INIT_LR = 1e-4   # Learning rate
EPOCHS = 50      # Número de epochs
BS = 2          # Batch size

def load_images (route1, route2):
    data, labels = [], []
    for route in [route1, route2]:
        paths_list = list(join(route, f) for f in listdir(route) if isfile(join(route, f)))
        label = route.split(os.path.sep)[-2]
        for path in paths_list:
            # Redimencionamos la imagen a 224x224 y le damos el formato
            # que necesitará nuestra red MobileNetV2 mediante la función
            # que este modelo nos proporciona
            # Referencia: https://arxiv.org/abs/1801.04381
            image = load_img(path, target_size = (224, 224))
            image = img_to_array(image)
            image = preprocess_input(image)
            data.append(image)
            labels.append(label)
    data = np.array(data, dtype = 'float32')
    labels = np.array(labels)
    return data, labels

def encode_labels (labels):
    # Usaremos one-hot encoding para codificar los labels
    lb = LabelBinarizer()
    labels = lb.fit_transform(labels)
    return lb, to_categorical(labels)

def build_model ():
    # Construimos la red MobileNetV2 pero sin incluir la capa top
    # pues aplicaremos fine-tuning
    base_model = MobileNetV2(weights="imagenet",
                            include_top=False,
                            input_tensor = Input(shape = (224, 224, 3)))
    # construct the head of the model that will be placed on top of the
    # Construimos el fine-tuning model a partir del modelo anterior
    tuning_model = base_model.output
    # https://software.intel.com/sites/products/documentation/doclib/daal/daal-user-and-reference-guides/daal_prog_guide/GUID-9B434D4F-C723-4191-9A88-69148C75A3F1.htm
    tuning_model = AveragePooling2D(pool_size = (7, 7))(tuning_model)
    tuning_model = Flatten(name = 'flatten')(tuning_model)
    tuning_model = Dense(128, activation='relu')(tuning_model)
    tuning_model = Dropout(0.5)(tuning_model)
    tuning_model = Dense(2, activation='softmax')(tuning_model)
    model = Model(inputs = base_model.input, outputs = tuning_model)
    # Ahora apagamos los labels del base_model para no actualizarlos durante
    # el backpropagation
    for layer in base_model.layers:
        layer.trainable = False
    # Usaremos SGD como optimizar del modelo y tomaremos como metrica el accuracy
    # Además, como solo tenemos 2 clases, nos conviene utilizar 'binary_crossentropy'
    # en vez de un 'categorical_crossentropy'
    opt = SGD(lr = INIT_LR)
    model.compile(loss = 'binary_crossentropy', optimizer = opt, metrics = ['accuracy'])
    return model

def draw_metrics (EPOCHS, H):
    # Graficamos las métricas calculadas
    plt.style.use("ggplot")
    plt.figure(figsize=(24, 12))
    plt.plot(np.arange(0, EPOCHS), H.history['loss'], label='entrenamiento:loss')
    plt.plot(np.arange(0, EPOCHS), H.history['val_loss'], label='validación:loss')
    plt.plot(np.arange(0, EPOCHS), H.history['accuracy'], label='entrenamiento:accuracy')
    plt.plot(np.arange(0, EPOCHS), H.history['val_accuracy'], label='validación:accuracy')
    plt.title('Modelo MobileNetV2 con fine-tuning')
    plt.xlabel('# épocas')
    plt.ylabel('Loss / Accuracy')
    plt.legend()
    plt.savefig('metrics.png')
