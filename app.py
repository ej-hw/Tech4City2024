from flask import Flask, request, jsonify, send_file, render_template
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import io
import base64
import numpy as np
from skimage.metrics import structural_similarity as ssim
import torch
from model import load_model, make_prediction, create_image_with_bboxes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ImageModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)

def calculate_ssim(image1, image2):
    image1_gray = image1.convert('L')
    image2_gray = image2.convert('L')
    img1_array = np.array(image1_gray)
    img2_array = np.array(image2_gray)
    score, _ = ssim(img1_array, img2_array, full=True)
    return score

model = load_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    img = Image.open(file.stream).convert('RGB')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes = img_bytes.getvalue()

    new_image = ImageModel(name=file.filename, data=img_bytes)
    db.session.add(new_image)
    db.session.commit()

    last_image = ImageModel.query.order_by(ImageModel.id.desc()).first()
    if last_image:
        last_img = Image.open(io.BytesIO(last_image.data)).convert('RGB')
        similarity_score = calculate_ssim(img, last_img)
    else:
        similarity_score = 0.0

    prediction = make_prediction(model, img)
    img_with_bboxes_np = create_image_with_bboxes(np.array(img), prediction)

    img_bytes_detected = io.BytesIO()
    Image.fromarray(img_with_bboxes_np).save(img_bytes_detected, format='PNG')
    img_base64_detected = base64.b64encode(img_bytes_detected.getvalue()).decode('utf-8')

    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

    prediction_data = {
        "objects": [{"class": label, "box": box.tolist()} for label, box in zip(prediction["labels"], prediction["boxes"])],
        "confidence": similarity_score
    }

    return jsonify({
        "image": img_base64,
        "processed_image": img_base64_detected,
        "prediction": prediction_data
    })

@app.route('/display/<int:image_id>')
def display_image(image_id):
    image_data = ImageModel.query.filter_by(id=image_id).first()
    if image_data:
        img = Image.open(io.BytesIO(image_data.data)).convert('RGB')
        prediction = make_prediction(model, img)
        img_with_bboxes_np = create_image_with_bboxes(np.array(img), prediction)

        img_bytes = io.BytesIO()
        Image.fromarray(img_with_bboxes_np).save(img_bytes, format='PNG')
        img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

        return render_template('display.html', image=img_base64)
    else:
        return "Image not found"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)

#working with streamlit -----------------------------------------------------------------------------------------------
# import streamlit as st
# from PIL import Image
# import numpy as np
# import matplotlib.pyplot as plt
# from model import load_model, make_prediction, create_image_with_bboxes

# # Set page configuration
# st.set_page_config(page_title="Object Detection App", page_icon=":tada:", layout="wide")

# @st.cache(allow_output_mutation=True)
# def load_or_create_model():
#     return load_model()

# def main():
#     st.title('Object Detection Web App')
#     st.write('Upload an image to detect objects.')

#     # Dashboard
#     upload = st.file_uploader(label="Upload Image Here:", type=["png", "jpg", "jpeg"])

#     if upload:
#         try:
#             img = Image.open(upload)
#             st.image(img, caption='Uploaded Image', use_column_width=True)

#             model = load_or_create_model()
#             prediction = make_prediction(model, img)
#             img_with_bbox = create_image_with_bboxes(np.array(img), prediction)

#             fig = plt.figure(figsize=(12, 12))
#             ax = fig.add_subplot(111)
#             plt.imshow(img_with_bbox)
#             plt.xticks([], [])
#             plt.yticks([], [])
#             ax.spines["top"].set_visible(False)
#             ax.spines["bottom"].set_visible(False)
#             ax.spines["right"].set_visible(False)
#             ax.spines["left"].set_visible(False)

#             st.pyplot(fig, use_container_width=True)

#             del prediction["boxes"]
#             st.header("Predicted Objects")
#             st.write(prediction)

#         except Exception as e:
#             st.error(f"Error: {str(e)}")

# if __name__ == '__main__':
#     main()
#----------------------------------------------------------------------------------------------------------------------