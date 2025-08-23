#!/bin/bash
echo "🔍 Starting deployment script..."
echo "📁 Current directory: $(pwd)"
echo "📋 Files in current directory:"
ls -la

echo "🔧 Installing Git LFS..."
git lfs install

echo "📥 Pulling LFS files..."
git lfs pull

echo "📊 Checking model file..."
if [ -f "final_model.h5" ]; then
    echo "✅ Model file found: $(ls -lh final_model.h5)"
else
    echo "❌ Model file not found!"
    echo "📂 All .h5 files:"
    find . -name "*.h5" -ls
fi

echo "🐍 Installing Python dependencies..."
python -m pip install -r requirements.txt

echo "🚀 Starting the application..."
gunicorn --bind 0.0.0.0:$PORT --timeout 120 --workers 1 app:app
