#!/bin/bash
echo "🔍 Starting deployment script..."
echo "📁 Current directory: $(pwd)"

echo "🤗 Using Hugging Face for model hosting - no Git LFS required!"
echo "� Current directory contents:"
ls -la

echo "🐍 Activating virtual environment and starting the application..."
. /opt/venv/bin/activate

echo "🚀 Starting the application..."
gunicorn --bind 0.0.0.0:$PORT --timeout 120 --workers 1 app:app
