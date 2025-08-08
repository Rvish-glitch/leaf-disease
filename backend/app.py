
import json
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.efficientnet import preprocess_input

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from run import LeafDiseaseChecker

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Leaf Disease Detection API is running'})

checker = LeafDiseaseChecker(
    model_path='final_model.h5',
    idx_path='class_indices.json'
)

FRONTEND_JSON_PATH = 'predictions.json'

@app.route('/predict', methods=['POST'])
def predict():
    print("Received POST /predict")

    if 'image' not in request.files:
        print(" No image uploaded!")
        return jsonify({'error': 'No image uploaded'}), 400

    img_file = request.files['image']
    print(f" Image name: {img_file.filename}")

    os.makedirs('uploads', exist_ok=True)
    temp_path = os.path.join('uploads', img_file.filename)
    img_file.save(temp_path)
    print(f" Image saved at {temp_path}")

    result = checker.predict(temp_path, output_json=FRONTEND_JSON_PATH)
    print(" Prediction complete")

    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
