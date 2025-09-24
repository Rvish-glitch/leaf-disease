#!/usr/bin/env python3
"""
Script to upload the leaf disease detection model to Hugging Face Hub
"""

from huggingface_hub import HfApi, create_repo
import json
import os

def upload_model_to_hf():
    # You'll need to set your HF token
    # Get it from: https://huggingface.co/settings/tokens
    
    # Repository details
    repo_id = "rishabh914/leaf-disease-detection"  # Updated to your username
    
    api = HfApi()
    
    try:
        # Create repository (will skip if already exists)
        create_repo(repo_id, exist_ok=True, repo_type="model")
    print(f"Repository {repo_id} created/verified")
        
        # Upload the model file
        api.upload_file(
            path_or_fileobj="final_model.h5",
            path_in_repo="final_model.h5",
            repo_id=repo_id,
            commit_message="Upload leaf disease detection model"
        )
    print("Model file uploaded successfully")
        
        # Upload class indices
        api.upload_file(
            path_or_fileobj="class_indices.json",
            path_in_repo="class_indices.json", 
            repo_id=repo_id,
            commit_message="Upload class indices"
        )
    print("Class indices uploaded successfully")
        
        # Create a README for the model
        readme_content = """---
license: mit
tags:
- image-classification
- plant-disease
- tensorflow
- keras
library_name: tensorflow
---

# Leaf Disease Detection Model

This model can detect diseases in plant leaves using EfficientNetB3 architecture.

## Usage

```python
from huggingface_hub import hf_hub_download
import tensorflow as tf
import json

# Download model and class indices
model_path = hf_hub_download(repo_id="Rvish-glitch/leaf-disease-detection", filename="final_model.h5")
indices_path = hf_hub_download(repo_id="Rvish-glitch/leaf-disease-detection", filename="class_indices.json")

# Load model
model = tf.keras.models.load_model(model_path)

# Load class indices
with open(indices_path, 'r') as f:
    class_indices = json.load(f)
```

## Classes

The model can detect various plant diseases across different crops including tomato, potato, apple, and corn.
"""
        
        api.upload_file(
            path_or_fileobj=readme_content.encode(),
            path_in_repo="README.md",
            repo_id=repo_id,
            commit_message="Add model documentation"
        )
    print("README uploaded successfully")
        
    print(f"\nModel successfully uploaded to: https://huggingface.co/{repo_id}")
        
    except Exception as e:
    print(f"Error uploading to Hugging Face: {e}")
        print("Make sure you have:")
        print("1. Installed huggingface_hub: pip install huggingface_hub")
        print("2. Logged in: huggingface-cli login")

if __name__ == "__main__":
    upload_model_to_hf()
