import os
import json
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.efficientnet import preprocess_input


class LeafDiseaseChecker:
    def __init__(self, model_path, idx_path=None, auto_dir=None):
        self.model = load_model(model_path)

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

    def predict(self, img_path, size=(256, 256), top_k=5, output_json='predictions.json'):
        if not os.path.exists(img_path):
            result = {"error": "file not found"}
        else:
            img = load_img(img_path, target_size=size)
            arr = preprocess_input(np.expand_dims(img_to_array(img), 0))
            preds = self.model.predict(arr)[0]
            top = sorted(enumerate(preds), key=lambda x: -x[1])[:top_k]

            result = {
                "predictions": [
                    {
                        "name": self.idx_to_class.get(i, str(i)),
                        "probability": round(float(p), 4)
                    }
                    for i, p in top
                ]
            }

        # Only write to file if a valid path is provided
        if output_json:
            with open(output_json, 'w') as f:
                json.dump(result, f, indent=2)

        return result

    def _viz(self, img, top):
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        axes[0].imshow(img)
        axes[0].axis('off')
        classes, vals = zip(*[(self.idx_to_class.get(i, i), p) for i, p in top])
        axes[1].barh(classes, vals)
        axes[1].invert_yaxis()
        axes[1].set_xlabel('Confidence')
        plt.tight_layout()
        plt.show()

    def batch(self, d, size=(256, 256)):
        res = {}
        for f in os.listdir(d):
            if f.lower().endswith(('.jpg', '.png', '.jpeg')):
                res[f] = self.predict(os.path.join(d, f), size, output_json=None)
        summary = {
            v['disease']: sum(1 for r in res.values() if r.get('disease') == v['disease'])
            for v in res.values()
        }
        print({'total': len(res), 'summary': summary})
        return res


if __name__ == '__main__':
    chk = LeafDiseaseChecker(
        'final_model.h5',
        idx_path='class_indices.json'
    )
    result = chk.predict(
        'test/test/AppleCedarRust3.JPG',
        output_json='/home/rvish/leaf-image-detec/frontend/public/predictions.json'
    )
    print(result)
