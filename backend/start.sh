#!/bin/bash
echo "🔍 Starting deployment script..."
echo "📁 Current directory: $(pwd)"

echo "🔧 Setting up Git and Git LFS..."
git config --global user.name "Railway Deploy" 
git config --global user.email "deploy@railway.app"
git lfs install --local

echo "📥 Fetching LFS files with multiple attempts..."
git lfs fetch --all
git lfs checkout

echo "📊 Checking model file..."
if [ -f "final_model.h5" ]; then
    filesize=$(stat -c%s final_model.h5)
    echo "✅ Model file found: $(ls -lh final_model.h5)"
    echo "📏 File size: $filesize bytes"
    
    if [ $filesize -lt 1000000 ]; then  # Less than 1MB means it's probably just the pointer
        echo "⚠️  Model file is too small - trying direct LFS pull..."
        git lfs pull origin main
        git lfs checkout final_model.h5
        
        # Check again
        filesize=$(stat -c%s final_model.h5)
        echo "📏 New file size: $filesize bytes"
        
        if [ $filesize -lt 1000000 ]; then
            echo "❌ Still too small - LFS download failed"
            exit 1
        fi
    fi
else
    echo "❌ Model file not found!"
    echo "📂 Current directory contents:"
    ls -la
    exit 1
fi

echo "🐍 Installing Python dependencies..."
python -m pip install -r requirements.txt

echo "🚀 Starting the application..."
gunicorn --bind 0.0.0.0:$PORT --timeout 120 --workers 1 app:app
