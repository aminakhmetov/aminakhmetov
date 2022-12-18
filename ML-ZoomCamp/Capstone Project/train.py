print('Importing libraries..')
import pandas as pd
import tensorflow as tf
import numpy as np
from tensorflow import keras
from tensorflow.keras.applications.xception import Xception
from tensorflow.keras.applications.xception import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# utility function for defining random seed
def set_seed():
    seed = 40
    np.random.seed(seed)
    tf.random.set_seed(seed)

# importing metadata
print('Importing training metadata..')
df_train_full = pd.read_csv('kitchenware-classification/train.csv', dtype={'Id': str})
df_train_full['filename'] = 'kitchenware-classification/images/' + df_train_full['Id'] + '.jpg'
val_cutoff = int(len(df_train_full) * 0.8)
df_train = df_train_full[:val_cutoff]
df_val = df_train_full[val_cutoff:]

# creating image generators
print('Creating image generators..')
image_format = 300
train_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
train_generator = train_datagen.flow_from_dataframe(df_train,x_col='filename',y_col='label',target_size=(image_format, image_format),batch_size=32)
val_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
val_generator = val_datagen.flow_from_dataframe(df_val,x_col='filename',y_col='label',target_size=(image_format, image_format),batch_size=32,)
set_seed()

# defining the model
print('Defining the model..')
# CNN input from Xception model
base_model = Xception(weights='imagenet',include_top=False,input_shape=(image_format, image_format, 3))
base_model.trainable = False
inputs = keras.Input(shape=(image_format, image_format, 3))
base = base_model(inputs, training=False)
vectors = keras.layers.GlobalAveragePooling2D()(base)
outputs = keras.layers.Dense(6)(vectors)
model = keras.Model(inputs, outputs)
model.summary()

# setting the hyperparameters
print('Setting hyperparameteres of the model..')
learning_rate = 0.01
optimizer = keras.optimizers.Adam(learning_rate=learning_rate)
loss = keras.losses.CategoricalCrossentropy(from_logits=True)
model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])

# training of the model
print('Training of the model..')
history = model.fit(train_generator,epochs=2,validation_data=val_generator)

# saving the model to tflite format
print('Saving model in tflite format')
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
with open('deployment/cutlery-prod.tflite', 'wb') as f_out:
    f_out.write(tflite_model)
