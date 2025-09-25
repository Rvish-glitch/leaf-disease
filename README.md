# 🍃 Leaf Disease Detection System

A comprehensive machine learning application for detecting diseases in plant leaves using deep learning. The system identifies 38 different plant diseases and healthy conditions across various crops including Apple, Corn, Grape, Potato, Tomato, and more.

## 🌟 Features

- **Multi-Crop Disease Detection**: Supports 15+ plant types including Apple, Corn, Grape, Potato, Tomato, Cherry, Pepper, Strawberry, and more
- **38 Disease Classifications**: Detects various diseases like Apple Scab, Early Blight, Late Blight, Powdery Mildew, and healthy conditions
- **Real-time Predictions**: Upload leaf images and get instant disease classification results
- **Modern Web Interface**: Clean, responsive React frontend with Bootstrap styling
- **REST API**: Flask-based backend with comprehensive API endpoints
- **Docker Deployment**: Complete containerization for easy deployment
- **Cloud Integration**: Pre-configured for Railway (backend) and Vercel (frontend) deployment

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React App     │    │   Flask API     │    │  ML Model       │
│   (Frontend)    │◄──►│   (Backend)     │◄──►│ (Hugging Face)  │
│   Port 3000     │    │   Port 5000     │    │ TensorFlow      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Backend Stack
- **Framework**: Flask with CORS support
- **ML Framework**: TensorFlow 2.18.0 + Keras 3.5.0
- **Model Hosting**: Hugging Face Hub (`rishabh914/leaf-disease-detection`)
- **Server**: Gunicorn for production deployment
- **Image Processing**: OpenCV, Pillow, NumPy

### Frontend Stack
- **Framework**: React 19.1.0
- **UI Library**: React Bootstrap 2.10.10
- **HTTP Client**: Axios for API communication
- **Routing**: React Router DOM
- **Styling**: Bootstrap 5.3.6 + custom CSS

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Git
- Internet connection (for model download)

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/leaf-image-detec.git
cd leaf-image-detec
```

### 2. Local Development with Docker
```bash
# Build and start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:5000
```

### 3. Production Deployment
```bash
# Use production configuration
docker-compose -f docker-compose.prod.yml up --build -d

# Check service status
docker-compose -f docker-compose.prod.yml ps
```

## 📋 Supported Plant Diseases

The model can detect the following conditions:

### Apple
- Apple Scab
- Black Rot
- Cedar Apple Rust
- Healthy

### Corn (Maize)
- Cercospora Leaf Spot / Gray Leaf Spot
- Common Rust
- Northern Leaf Blight
- Healthy

### Potato
- Early Blight
- Late Blight
- Healthy

### Tomato
- Bacterial Spot
- Early Blight
- Late Blight
- Leaf Mold
- Septoria Leaf Spot
- Spider Mites (Two-spotted Spider Mite)
- Target Spot
- Tomato Yellow Leaf Curl Virus
- Tomato Mosaic Virus
- Healthy

### Other Crops
- **Grape**: Black Rot, Esca (Black Measles), Leaf Blight, Healthy
- **Cherry**: Powdery Mildew, Healthy
- **Pepper (Bell)**: Bacterial Spot, Healthy
- **Strawberry**: Leaf Scorch, Healthy
- **Peach**: Bacterial Spot, Healthy
- **Orange**: Huanglongbing (Citrus Greening)
- **Squash**: Powdery Mildew
- **Blueberry**: Healthy
- **Raspberry**: Healthy
- **Soybean**: Healthy



### Get All Predictions History
```http
GET /predictions
```

## 🐳 Docker Configuration

### Development Environment
- **Frontend**: React development server on port 3000
- **Backend**: Flask development server on port 5000
- **Hot Reloading**: Both services support live code changes

## 📁 Project Structure

```
leaf-image-detec/
├── backend/                 # Flask API server
│   ├── app.py              # Main Flask application
│   ├── requirements.txt    # Python dependencies
│   ├── class_indices.json  # Disease class mappings
│   ├── Dockerfile          # Backend container config
│   └── uploads/            # Uploaded images storage
├── frontend/               # React web application
│   ├── src/
│   │   ├── App.js          # Main React component
│   │   ├── UploadPage.js   # File upload interface
│   │   └── ResultPage.js   # Results display
│   ├── public/             # Static assets
│   ├── package.json        # Node.js dependencies
│   └── Dockerfile          # Frontend container config
├── docker-compose.yml      # Development orchestration
├── docker-compose.prod.yml # Production orchestration
├── Dockerfile              # Railway deployment config
├── railway.toml           # Railway platform settings
├── deploy.sh              # Deployment automation
└── test-deployment.sh     # Testing scripts
```

## 🧪 Testing

### Automated Testing
```bash
# Test local deployment
./test-deployment.sh

# Test individual services
docker-compose exec backend python -c "import app; print('Backend OK')"
docker-compose exec frontend npm test
```

### Manual Testing
1. Upload test images from `backend/test/test/` directory
2. Verify predictions match expected disease classifications
3. Check response times and accuracy


## 📊 Performance

- **Model Size**: ~100MB (loaded from Hugging Face)
- **Prediction Time**: <2 seconds per image
- **Supported Formats**: JPG, JPEG, PNG
- **Max Image Size**: 10MB
- **Accuracy**: >90% on validation dataset


## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.


