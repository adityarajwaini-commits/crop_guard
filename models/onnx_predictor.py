"""
ONNX-based predictor for CropGuard disease classification.
Provides efficient inference using ONNX Runtime.
"""
import os
import numpy as np
from PIL import Image
import onnxruntime as ort
import json

class ONNXPredictor:
    def __init__(self, model_path: str = None, metadata_path: str = None):
        """
        Initialize ONNX Runtime predictor.
        
        Args:
            model_path: Path to ONNX model file. Defaults to saved_models/model.onnx
            metadata_path: Path to metadata JSON with class names. Defaults to saved_models/plantvillage_run/final_metrics.json
        """
        if model_path is None:
            model_path = os.path.join("saved_models", "model.onnx")
        
        if metadata_path is None:
            metadata_path = os.path.join("saved_models", "plantvillage_run", "final_metrics.json")
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"ONNX model not found at: {model_path}")
        
        if not os.path.exists(metadata_path):
            raise FileNotFoundError(f"Metadata not found at: {metadata_path}")
        
        # Load ONNX model
        self.session = ort.InferenceSession(model_path)
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name
        
        # Load metadata
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        self.class_names = metadata['class_names']
        self.num_classes = len(self.class_names)
        
        # Build preprocessing specs matching training configuration
        self.image_size = (224, 224)
        self.mean = np.array([0.485, 0.456, 0.406], dtype=np.float32).reshape(3, 1, 1)
        self.std = np.array([0.229, 0.224, 0.225], dtype=np.float32).reshape(3, 1, 1)
        
        self.model_path = model_path
        self.metadata_path = metadata_path

    def preprocess(self, image: Image.Image) -> np.ndarray:
        """
        Preprocess PIL Image to ONNX input format (batch_size=1, channels=3, height=224, width=224).
        
        Args:
            image: PIL Image object
            
        Returns:
            numpy array of shape (1, 3, 224, 224) in float32 format
        """
        # Ensure RGB
        if image.mode != "RGB":
            image = image.convert("RGB")
        
        # Resize using bilinear interpolation
        image_resized = image.resize(self.image_size, Image.Resampling.BILINEAR)
        
        # Convert to float32 numpy array and scale to [0, 1]
        array = np.array(image_resized, dtype=np.float32) / 255.0
        
        # Transpose from HWC to CHW
        array = np.transpose(array, (2, 0, 1))
        
        # Normalize
        array = (array - self.mean) / self.std
        
        # Add batch dimension and ensure float32 type
        return np.expand_dims(array, axis=0).astype(np.float32)

    def predict(self, image: Image.Image, top_k: int = 3) -> dict:
        """
        Run inference on image and return top-k predictions.
        
        Args:
            image: PIL Image object
            top_k: Number of top predictions to return
            
        Returns:
            dict with keys:
                - disease_name: primary predicted disease
                - confidence: confidence of primary prediction
                - top_3_predictions: list of top-k predictions with class_name and confidence
        """
        # Preprocess
        input_array = self.preprocess(image)
        
        # Run inference
        outputs = self.session.run([self.output_name], {self.input_name: input_array})
        logits = outputs[0][0]  # Shape: (num_classes,)
        
        # Convert logits to probabilities
        exp_logits = np.exp(logits - np.max(logits))  # Numerical stability
        probabilities = exp_logits / np.sum(exp_logits)
        
        # Get top-k predictions
        top_indices = np.argsort(probabilities)[::-1][:min(top_k, self.num_classes)]
        
        top_predictions = []
        for idx in top_indices:
            top_predictions.append({
                "class_name": self.class_names[idx],
                "confidence": float(probabilities[idx])
            })
        
        return {
            "disease_name": top_predictions[0]["class_name"],
            "confidence": top_predictions[0]["confidence"],
            "top_3_predictions": top_predictions
        }

    def predict_path(self, image_path: str, top_k: int = 3) -> dict:
        """
        Predict from image file path.
        
        Args:
            image_path: Path to image file
            top_k: Number of top predictions to return
            
        Returns:
            Same dict as predict()
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        image = Image.open(image_path)
        return self.predict(image, top_k=top_k)
    
    def get_model_info(self) -> dict:
        """Get information about the loaded model."""
        return {
            "model_path": self.model_path,
            "metadata_path": self.metadata_path,
            "num_classes": self.num_classes,
            "input_name": self.input_name,
            "output_name": self.output_name,
            "runtime": "ONNX Runtime",
            "class_names": self.class_names
        }
