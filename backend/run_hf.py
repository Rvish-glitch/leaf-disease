import os
import json
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.efficientnet import preprocess_input
from huggingface_hub import hf_hub_download
import tempfile


class LeafDiseaseChecker:
    def __init__(self, model_path=None, idx_path=None, auto_dir=None, use_huggingface=True, repo_id="your-username/leaf-disease-detection"):
        """
        Initialize the LeafDiseaseChecker
        
        Args:
            model_path: Local path to model file (if use_huggingface=False)
            idx_path: Local path to class indices file (if use_huggingface=False) 
            auto_dir: Directory to auto-generate indices from
            use_huggingface: Whether to download model from Hugging Face
            repo_id: Hugging Face repository ID
        """
        self.use_huggingface = use_huggingface
        self.repo_id = repo_id
        
        if use_huggingface:
            # Download model and indices from Hugging Face
            print("Downloading model from Hugging Face...")
            try:
                model_path = hf_hub_download(
                    repo_id=repo_id,
                    filename="final_model.h5",
                    cache_dir=tempfile.gettempdir()
                )
                idx_path = hf_hub_download(
                    repo_id=repo_id,
                    filename="class_indices.json",
                    cache_dir=tempfile.gettempdir()
                )
                print("Model and indices downloaded successfully")
            except Exception as e:
                print(f"Failed to download from Hugging Face: {e}")
                print("Falling back to local files...")
                # Fallback to local files
                model_path = model_path or "final_model.h5"
                idx_path = idx_path or "class_indices.json"
        
        # Load model
        self.model = load_model(model_path)

        # Load class indices
        if idx_path and os.path.exists(idx_path):
            mapping = json.load(open(idx_path))
        elif auto_dir:
            mapping = self._make_indices(auto_dir)
            json.dump(mapping, open(idx_path or 'class_indices.json', 'w'))
        else:
            mapping = {}

        self.idx_to_class = {v: k for k, v in mapping.items()}

    def _make_indices(self, data_dir):
        classes = sorted([
            d for d in os.listdir(data_dir)
            if os.path.isdir(os.path.join(data_dir, d))
        ])
        return {c: i for i, c in enumerate(classes)}

    def predict(self, img_path):
        img = load_img(img_path, target_size=(256, 256))  # Changed from 224 to 256
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        pred = self.model.predict(img_array)
        pred_idx = np.argmax(pred)
        pred_prob = np.max(pred)

        pred_class = self.idx_to_class.get(pred_idx, f"class_{pred_idx}")

        return {
            'predicted_class': pred_class,
            'confidence': float(pred_prob),
            'all_predictions': {
                self.idx_to_class.get(i, f"class_{i}"): float(prob)
                for i, prob in enumerate(pred[0])
            }
        }

    def predict_top_k(self, img_path, k=3):
        img = load_img(img_path, target_size=(256, 256))  # Changed from 224 to 256
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        pred = self.model.predict(img_array)
        top_k_idx = np.argsort(pred[0])[::-1][:k]

        results = []
        for idx in top_k_idx:
            class_name = self.idx_to_class.get(idx, f"class_{idx}")
            confidence = float(pred[0][idx])
            results.append({
                'class': class_name,
                'confidence': confidence
            })

        return results

    def visualize_prediction(self, img_path, save_path=None):
        results = self.predict_top_k(img_path, k=5)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Display image
        img = load_img(img_path)
        ax1.imshow(img)
        ax1.set_title('Input Image')
        ax1.axis('off')
        
        # Display predictions
        classes = [r['class'] for r in results]
        confidences = [r['confidence'] for r in results]
        
        y_pos = np.arange(len(classes))
        bars = ax2.barh(y_pos, confidences)
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(classes)
        ax2.set_xlabel('Confidence')
        ax2.set_title('Top 5 Predictions')
        ax2.set_xlim(0, 1)
        
        # Add confidence values on bars
        for i, (bar, conf) in enumerate(zip(bars, confidences)):
            ax2.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2, 
                    f'{conf:.3f}', va='center')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
        
        return fig
