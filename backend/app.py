from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from run import LeafDiseaseChecker

app = Flask(__name__)
# CORS configuration - allow all origins for now
CORS(app)

# Check if model file exists
model_path = 'final_model.h5'
idx_path = 'class_indices.json'

print(f"🔍 Checking for model file: {model_path}")
print(f"📁 Current directory: {os.getcwd()}")
print(f"📋 Files in current directory: {os.listdir('.')}")

if os.path.exists(model_path):
    print(f"✅ Model file found: {model_path} (size: {os.path.getsize(model_path)} bytes)")
else:
    print(f"❌ Model file not found: {model_path}")
    
if os.path.exists(idx_path):
    print(f"✅ Index file found: {idx_path}")
else:
    print(f"❌ Index file not found: {idx_path}")

try:
    checker = LeafDiseaseChecker(
        model_path=model_path,
        idx_path=idx_path
    )
    print("✅ LeafDiseaseChecker initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize LeafDiseaseChecker: {e}")
    checker = None

FRONTEND_JSON_PATH = 'predictions.json'

@app.route('/')
def health_check():
    """Health check endpoint"""
    status = {
        'status': 'healthy' if checker is not None else 'unhealthy',
        'model_loaded': checker is not None,
        'model_file_exists': os.path.exists(model_path),
        'index_file_exists': os.path.exists(idx_path)
    }
    return jsonify(status)

@app.route('/predict', methods=['POST'])
def predict():
    print("🔥 Received POST /predict")
    
    if checker is None:
        print("❌ Model not initialized!")
        return jsonify({'error': 'Model not available - deployment issue'}), 500

    if 'image' not in request.files:
        print("❌ No image uploaded!")
        return jsonify({'error': 'No image uploaded'}), 400

    img_file = request.files['image']
    print(f"📷 Image name: {img_file.filename}")

    os.makedirs('uploads', exist_ok=True)
    temp_path = os.path.join('uploads', img_file.filename)
    img_file.save(temp_path)
    print(f"✅ Image saved at {temp_path}")

    try:
        result = checker.predict(temp_path, output_json=FRONTEND_JSON_PATH)
        print("📊 Prediction complete")
        return jsonify(result)
    except Exception as e:
        print(f"❌ Prediction failed: {e}")
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
