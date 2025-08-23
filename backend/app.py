from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from run import LeafDiseaseChecker

app = Flask(__name__)
CORS(app)

checker = LeafDiseaseChecker(
    model_path='final_model.h5',
    idx_path='class_indices.json'
)

FRONTEND_JSON_PATH = 'predictions.json'

@app.route('/predict', methods=['POST'])
def predict():
    print("🔥 Received POST /predict")

    if 'image' not in request.files:
        print("❌ No image uploaded!")
        return jsonify({'error': 'No image uploaded'}), 400

    img_file = request.files['image']
    print(f"📷 Image name: {img_file.filename}")

    os.makedirs('uploads', exist_ok=True)
    temp_path = os.path.join('uploads', img_file.filename)
    img_file.save(temp_path)
    print(f"✅ Image saved at {temp_path}")

    result = checker.predict(temp_path, output_json=FRONTEND_JSON_PATH)
    print("📊 Prediction complete")

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
