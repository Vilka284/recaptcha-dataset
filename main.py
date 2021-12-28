import keras
from keras import layers
from keras.models import Sequential, load_model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np


batch_size = 32
img_height = 180
img_width = 180

train_dg = keras.preprocessing.image.ImageDataGenerator(rescale=1./255, validation_split=0.2)
train_dg = keras.preprocessing.image.ImageDataGenerator(rescale=1./255)

train_generator = train_dg.flow_from_directory(
    'Large',
    class_mode='binary', seed=123)

validation_generator = train_dg.flow_from_directory(
    'Large',
    class_mode='binary', seed=123)

class_names = train_dg.class_names
normalization_layer = layers.experimental.preprocessing.Rescaling(1./255)
num_classes = len(class_names)

model = Sequential([
    layers.experimental.preprocessing.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
    layers.Conv2D(16, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(32, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(64, 3, padding='same', activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(num_classes)
])

model.compile(optimizer='adam',
              loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

epochs = 10

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs
)

with open('model.h5', 'w') as f:
    f.close()

model.save('model.h5')
