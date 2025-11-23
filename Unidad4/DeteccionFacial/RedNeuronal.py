# Red Neuronal.py
import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow import keras

# Alias para capas
ImageDataGenerator = keras.preprocessing.image.ImageDataGenerator
Sequential = keras.models.Sequential
Conv2D = keras.layers.Conv2D
MaxPooling2D = keras.layers.MaxPooling2D
Flatten = keras.layers.Flatten
Dense = keras.layers.Dense
Dropout = keras.layers.Dropout
BatchNormalization = keras.layers.BatchNormalization
EarlyStopping = keras.callbacks.EarlyStopping
ModelCheckpoint = keras.callbacks.ModelCheckpoint
to_categorical = keras.utils.to_categorical


# CARGAR FER2013 DESDE CSV

ruta = r"IA\Unidad4\DeteccionFacial\dataset\fer2013.csv"

data = pd.read_csv(ruta)

# Convertir píxeles
imagenes = np.array([np.fromstring(pixels, dtype=np.uint8, sep=' ').reshape((48, 48)) 
                     for pixels in data['pixels']])

imagenes = imagenes.astype("float32") / 255.0
imagenes = np.expand_dims(imagenes, -1)  # (n,48,48,1)

# One-hot de las etiquetas
emociones = to_categorical(data['emotion'], num_classes=7)

# SEPARAR ENTRENAMIENTO / VALIDACIÓN

X_train, X_val, y_train, y_val = train_test_split(
    imagenes, emociones, test_size=0.2, random_state=42
)

# 3. AUMENTACIÓN DE DATOS

datagen = ImageDataGenerator(
    rotation_range=20,
    zoom_range=0.15,
    brightness_range=[0.9, 1.1],
    horizontal_flip=True,
    fill_mode='nearest'
)

datagen.fit(X_train)

# 4. DEFINIR MODELO CNN

modelo = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(48, 48, 1)),
    BatchNormalization(),
    MaxPooling2D(2, 2),

    Conv2D(96, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D(2, 2),

    Conv2D(128, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D(2, 2),

    Conv2D(256, (3, 3), activation='relu'),
    BatchNormalization(),
    MaxPooling2D(2, 2),

    Flatten(),
    Dense(256, activation='relu'),
    Dropout(0.4),

    Dense(7, activation='softmax')  # FER2013 tiene 7 emociones
])

modelo.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# 5. CALLBACKS
callbacks = [
    EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
    ModelCheckpoint("IA/Unidad4/DeteccionFacial/modelo/mejor_modelo.keras", monitor='val_loss', save_best_only=True)
]

# 6. ENTRENAR MODELO

modelo.fit(
    datagen.flow(X_train, y_train, batch_size=32),
    validation_data=(X_val, y_val),
    epochs=50,
    callbacks=callbacks
)
