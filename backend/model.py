import os
import base64
import sqlite3
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions

# Load the ResNet50 model
model = ResNet50(weights='imagenet')

def save_image(file, upload_folder):
    filepath = os.path.join(upload_folder, file.filename)
    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())
    return filepath

def classify_image(filepath):
    # Load and preprocess the image
    img = load_img(filepath, target_size=(224, 224))
    img_array = img_to_array(img)
    img_array = img_array.reshape((1, 224, 224, 3))
    img_array = preprocess_input(img_array)

    # Make prediction
    yhat = model.predict(img_array)
    label = decode_predictions(yhat)
    label = label[0][0]

    prediction = '%s (%.2f%%)' % (label[1], label[2] * 100)
    return prediction

def insert_image_info(filename, filepath, prediction):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO images (name, path, prediction) VALUES (?, ?, ?)', (filename, filepath, prediction))
    conn.commit()
    conn.close()

def convert_image_to_base64(filepath):
    with open(filepath, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
    return image_data