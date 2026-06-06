import os
import json
import numpy as np
import onnxruntime as ort
from PIL import Image
from config import Config

class ONNXCropGuardPredictor:
    def __init__(self, onnx_model_path: str = None, class_names: list = None):
        """
        Lightweight predictor executing crop disease classification via ONNX Runtime.
        Avoids loading PyTorch weights.
        
        Args:
            onnx_model_path (str, optional): Path to exported ONNX model.
            class_names (list, optional): List of class names. If None, it attempts 
                                          to load them from saved_models/evaluation_report.txt.
        """
        self.model_path = onnx_model_path or os.path.join(Config.SAVED_MODELS_DIR, "model.onnx")
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"ONNX model file not found at: {self.model_path}. Run export_onnx.py first.")

        # Load session
        self.session = ort.InferenceSession(self.model_path, providers=['CPUExecutionProvider'])
        self.input_name = self.session.get_inputs()[0].name
        
        # Load classes from config, parameters, or evaluation reports
        if class_names is not None:
            self.class_names = class_names
        else:
            # Fallback placeholder if no dataset configuration is loaded
            self.class_names = Config.CLASSES

    def preprocess(self, image: Image.Image) -> np.ndarray:
        """
        Performs RGB conversion, resizing, float scaling, mean/std normalizations,
        and transposes image dimensions using NumPy. Matches PyTorch transforms.
        """
        if image.mode != "RGB":
            image = image.convert("RGB")
            
        # 1. Resize to target size (224x224)
        image = image.resize(Config.IMAGE_SIZE, Image.BILINEAR)
        
        # 2. Convert to numpy array and scale to [0, 1]
        img_arr = np.array(image).astype(np.float32) / 255.0
        
        # 3. Normalize with ImageNet mean and std constants
        mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
        std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
        img_arr = (img_arr - mean) / std
        
        # 4. Transpose dimensions: (H, W, C) -> (C, H, W)
        img_arr = img_arr.transpose(2, 0, 1)
        
        # 5. Expand batch dimensions: (1, C, H, W)
        img_arr = np.expand_dims(img_arr, axis=0)
        return img_arr

    def softmax(self, x: np.ndarray) -> np.ndarray:
        """
        Computes stable softmax probabilities.
        """
        e_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return e_x / np.sum(e_x, axis=-1, keepdims=True)

    def predict(self, image: Image.Image, top_k: int = 3) -> dict:
        """
        Runs model inference using ONNX Runtime.
        
        Args:
            image (PIL.Image.Image): Input leaf image.
            top_k (int): Number of top predictions to return.
            
        Returns:
            dict: Structured results matching PyTorch output layout.
        """
        # 1. Preprocess using NumPy pipeline
        img_tensor = self.preprocess(image)
        
        # 2. Run ONNX Session prediction
        ort_inputs = {self.input_name: img_tensor}
        logits = self.session.run(None, ort_inputs)[0][0]
        
        # 3. Calculate class probabilities
        probs = self.softmax(logits)
        
        # 4. Extract Top-k indices
        top_indices = np.argsort(probs)[::-1][:top_k]
        
        top_3 = []
        for idx in top_indices:
            label = self.class_names[idx] if idx < len(self.class_names) else f"Class_{idx}"
            top_3.append({
                "class_name": label,
                "confidence": float(probs[idx])
            })
            
        main_label = self.class_names[top_indices[0]] if top_indices[0] < len(self.class_names) else f"Class_{top_indices[0]}"
        
        return {
            "disease_name": main_label,
            "confidence": float(probs[top_indices[0]]),
            "top_3_predictions": top_3
        }

    def predict_path(self, image_path: str, top_k: int = 3) -> dict:
        """
        Wrapper to load image from path and perform prediction.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image path not found: {image_path}")
        image = Image.open(image_path)
        return self.predict(image, top_k=top_k)
