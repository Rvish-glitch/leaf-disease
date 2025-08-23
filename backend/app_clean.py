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
    print("💡 Make sure you have internet connection and the repo ID is correct")
    checker = None

FRONTEND_JSON_PATH = 'predictions.json'

@app.route('/')
def health_check():
    if checker is None:
        return jsonify({
            'status': 'error',
            'message': 'Model not loaded - check Hugging Face connection',
            'hf_repo': HF_REPO_ID
        }), 500
    
    return jsonify({
        'status': 'healthy',
        'message': 'Leaf Disease Detection API is running',
        'model_source': 'Hugging Face',
        'hf_repo': HF_REPO_ID,
        'version': '2.0'
    })

@app.route('/health')
def health():
    return health_check()

@app.route('/predict', methods=['POST'])
def predict():
    if checker is None:
        return jsonify({
            'error': 'Model not loaded - check Hugging Face connection'
        }), 500
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    try:
        # Save uploaded file temporarily
        upload_path = os.path.join('uploads', file.filename)
        os.makedirs('uploads', exist_ok=True)
        file.save(upload_path)
        
        # Make prediction
        result = checker.predict(upload_path)
        
        # Save to JSON file
        import json
        with open(FRONTEND_JSON_PATH, 'w') as f:
            json.dump(result, f, indent=2)
        
        # Clean up uploaded file
        os.remove(upload_path)
        
        return jsonify({
            'success': True,
            'prediction': result,
            'model_source': 'Hugging Face',
            'hf_repo': HF_REPO_ID
        })
        
    except Exception as e:
        print(f"Prediction error: {e}")
        # Clean up uploaded file if it exists
        if os.path.exists(upload_path):
            os.remove(upload_path)
        return jsonify({
            'error': f'Prediction failed: {str(e)}'
        }), 500

@app.route('/predictions')
def get_predictions():
    """Get the latest predictions from JSON file"""
    try:
        if os.path.exists(FRONTEND_JSON_PATH):
            import json
            with open(FRONTEND_JSON_PATH, 'r') as f:
                predictions = json.load(f)
            return jsonify({
                'success': True,
                'predictions': predictions,
                'model_source': 'Hugging Face',
                'hf_repo': HF_REPO_ID
            })
        else:
            return jsonify({
                'success': False,
                'message': 'No predictions available yet'
            })
    except Exception as e:
        return jsonify({
            'error': f'Failed to load predictions: {str(e)}'
        }), 500

if __name__ == '__main__':
    # Get port from environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
