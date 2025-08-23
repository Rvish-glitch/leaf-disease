#!/bin/bash
echo "🔍 Starting deployment script..."
echo "📁 Current directory: $(pwd)"

# Default to Hugging Face unless explicitly disabled
USE_HUGGINGFACE=${USE_HUGGINGFACE:-true}

# Check if we should use Hugging Face
if [ "$USE_HUGGINGFACE" = "true" ]; then
    echo "🤗 Primary: Using Hugging Face for model hosting"
    echo "📝 Set USE_HUGGINGFACE=false to use local files instead"
else
    echo "📁 Using local files - checking Git LFS..."
    
    # Set up Git LFS if files are not present
    if [ ! -f "final_model.h5" ] || [ $(stat -c%s final_model.h5) -lt 1000000 ]; then
        echo "🔧 Setting up Git and Git LFS..."
        git config --global user.name "Railway Deploy" 
        git config --global user.email "deploy@railway.app"
        git lfs install --local
        
        echo "📥 Fetching LFS files..."
        git lfs fetch --all
        git lfs checkout
        
        echo "📊 Checking model file..."
        if [ -f "final_model.h5" ]; then
            filesize=$(stat -c%s final_model.h5)
            echo "✅ Model file found: $(ls -lh final_model.h5)"
            echo "📏 File size: $filesize bytes"
            
            if [ $filesize -lt 1000000 ]; then
                echo "⚠️  Model file is too small - trying direct LFS pull..."
                git lfs pull origin main
                git lfs checkout final_model.h5
            fi
        else
            echo "❌ Model file not found after LFS checkout!"
            echo "📂 Current directory contents:"
            ls -la
        fi
    else
        echo "✅ Local model file already present and valid"
    fi
fi

echo "📋 Current directory contents:"
ls -la

echo "🐍 Activating virtual environment and starting the application..."
. /opt/venv/bin/activate

echo "🚀 Starting the application..."
gunicorn --bind 0.0.0.0:$PORT --timeout 120 --workers 1 app:appcho "🔍 Starting deployment script..."
echo "📁 Current directory: $(pwd)"

echo "🤗 Using Hugging Face for model hosting - no Git LFS required!"
echo "� Current directory contents:"
ls -la

echo "🐍 Activating virtual environment and starting the application..."
. /opt/venv/bin/activate

echo "🚀 Starting the application..."
gunicorn --bind 0.0.0.0:$PORT --timeout 120 --workers 1 app:app
