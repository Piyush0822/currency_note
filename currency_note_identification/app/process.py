import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from io import BytesIO

# Define the image dimensions and number of classes
img_width, img_height = 224, 224
num_classes = 9

# Load the saved model
model = tf.keras.models.load_model('trained_model/final_currency_model.h5')

def currency_prediction(img):

    # Use your model to predict the class of the uploaded image
    pred = model.predict(img)
    class_idx = np.argmax(pred[0])
    classes = {'10': 0, '100': 1, '20': 2, '200': 3, '2000': 4, '50': 5, '500': 6, 'Fake': 7, 'Not_Detected': 8}
    class_label = list(classes.keys())[list(classes.values()).index(class_idx)]

    return class_label

def currency_prediction_file(img_path):
    # Load and preprocess your uploaded image
    img_content = img_path.read()
    img = image.load_img(BytesIO(img_content), target_size=(img_width, img_height))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis=0)
    img /= 255.

    # Use your model to predict the class of the uploaded image
    pred = model.predict(img)
    class_idx = np.argmax(pred[0])
    classes = {'10': 0, '100': 1, '20': 2, '200': 3, '2000': 4, '50': 5, '500': 6, 'Fake': 7, 'Not_Detected': 8}
    class_label = list(classes.keys())[list(classes.values()).index(class_idx)]

    return class_label
