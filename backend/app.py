from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# Try to import the Hugging Face version first, fall back to local version
try:
    from run_hf import LeafDiseaseChecker
    USE_HUGGINGFACE = True
    print("🤗 Hugging Face version available")
except ImportError as e:
    print(f"⚠️  Hugging Face version not available: {e}")
    from run import LeafDiseaseChecker
    USE_HUGGINGFACE = False
    print("📁 Using local version of LeafDiseaseChecker")

app = Flask(__name__)
# CORS configuration - allow all origins for now
CORS(app)

# Configuration for Hugging Face model (ONLY)
HF_REPO_ID = os.environ.get('HF_REPO_ID', 'rishabh914/leaf-disease-detection')

print(f"🤗 Using ONLY Hugging Face model: {HF_REPO_ID}")
print(f"📁 Current directory: {os.getcwd()}")
print("⚠️ Local files will be ignored")

try:
    # Use ONLY Hugging Face model
    print(f"🤗 Loading model from Hugging Face: {HF_REPO_ID}")
    checker = LeafDiseaseChecker(
        use_huggingface=True,
        repo_id=HF_REPO_ID
    )
    print("✅ Hugging Face model loaded successfully")
except Exception as e:
    print(f"❌ Failed to load Hugging Face model: {e}")
    print("� Make sure you have internet connection and the repo ID is correct")
    checker = Nonest, jsonify
from flask_cors import CORS
import os

# Try to import the Hugging Face version first, fall back to local version
try:
    from run_hf import LeafDiseaseChecker
    USE_HUGGINGFACE = True
    print("🤗 Hugging Face version available")
except ImportError as e:
    print(f"⚠️  Hugging Face version not available: {e}")
    from run import LeafDiseaseChecker
    USE_HUGGINGFACE = False
    print("📁 Using local version of LeafDiseaseChecker")

app = Flask(__name__)
# CORS configuration - allow all origins for now
CORS(app)

# Configuration for Hugging Face model
HF_REPO_ID = os.environ.get('HF_REPO_ID', 'rishabh914/leaf-disease-detection')
USE_HF = os.environ.get('USE_HUGGINGFACE', 'false').lower() == 'true'

# Check if model file exists locally
model_path = 'final_model.h5'
idx_path = 'class_indices.json'

print(f"🔍 Checking for model file: {model_path}")
print(f"📁 Current directory: {os.getcwd()}")
print(f"📋 Files in current directory: {os.listdir('.')}")

if os.path.exists(model_path):
    print(f"✅ Model file found: {model_path} (size: {os.path.getsize(model_path)} bytes)")
    use_local = True
else:
    print(f"❌ Model file not found: {model_path}")
    use_local = False
    
if os.path.exists(idx_path):
    print(f"✅ Index file found: {idx_path}")
else:
    print(f"❌ Index file not found: {idx_path}")

try:
    if USE_HUGGINGFACE and USE_HF and not use_local:
        # Try to use Hugging Face only if explicitly enabled
        print(f"🤗 Attempting to download model from Hugging Face: {HF_REPO_ID}")
        checker = LeafDiseaseChecker(
            use_huggingface=True,
            repo_id=HF_REPO_ID
        )
    else:
        # Use local files (default behavior)
        print("📁 Using local model files")
        if USE_HUGGINGFACE:
            checker = LeafDiseaseChecker(
                model_path=model_path,
                idx_path=idx_path,
                use_huggingface=False
            )
        else:
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
