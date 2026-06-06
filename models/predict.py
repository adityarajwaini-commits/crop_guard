import os
import torch
import torch.nn.functional as F
from PIL import Image
import torchvision.transforms as transforms

from config import Config
from models.train import build_model

class CropGuardPredictor:
    def __init__(self, model_path: str = None, device: str = None):
        """
        Loads the best model checkpoint and reconstructs the classifier state.
        
        Args:
            model_path (str, optional): Path to the saved checkpoint (.pth). 
                                        Defaults to saved_models/best_model.pth.
            device (str, optional): Target device ('cuda' or 'cpu').
        """
        self.device = torch.device(device if device else ("cuda" if torch.cuda.is_available() else "cpu"))
        
        # Determine best checkpoint path
        if model_path is None:
            model_path = os.path.join(Config.SAVED_MODELS_DIR, "best_model.pth")
            if not os.path.exists(model_path):
                model_path = os.path.join(Config.SAVED_MODELS_DIR, "best_head_model.pth")
                
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model checkpoint not found at: {model_path}. Train the model first.")

        # Load weights checkpoint
        checkpoint = torch.load(model_path, map_location=self.device)
        self.class_names = checkpoint['class_names']
        num_classes = len(self.class_names)

        # Build ResNet-50 model architecture
        self.model = build_model(num_classes=num_classes, freeze_backbone=False)
        self.model.load_state_dict(checkpoint['model_state_dict'])
        self.model = self.model.to(self.device)
        self.model.eval()

        # Build preprocessing transforms matching the validation transform specs
        self.transform = transforms.Compose([
            transforms.Resize(Config.IMAGE_SIZE),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def preprocess(self, image: Image.Image) -> torch.Tensor:
        """
        Preprocesses a PIL Image to a PyTorch float tensor.
        """
        # Ensure image is in RGB format
        if image.mode != "RGB":
            image = image.convert("RGB")
            
        tensor = self.transform(image)
        return tensor.unsqueeze(0) # Add batch dimension (1, C, H, W)

    def predict(self, image: Image.Image, top_k: int = 3) -> dict:
        """
        Evaluates leaf disease classes and returns prediction details.
        
        Args:
            image (PIL.Image.Image): Uploaded crop leaf PIL image.
            top_k (int): Number of top predictions to list in top_3_predictions.
            
        Returns:
            dict: Classification summary containing:
                  - disease_name (str)
                  - confidence (float)
                  - top_3_predictions (list of dicts)
        """
        # 1. Preprocess
        tensor = self.preprocess(image).to(self.device)

        # 2. Run model forward pass
        with torch.no_grad():
            outputs = self.model(tensor)
            
            # 3. Calculate probabilities using Softmax
            probabilities = F.softmax(outputs, dim=1).squeeze(0)

        # 4. Extract top probabilities and index mappings
        top_probs, top_indices = torch.topk(probabilities, k=min(top_k, len(self.class_names)))
        
        top_probs = top_probs.cpu().numpy()
        top_indices = top_indices.cpu().numpy()

        # Map to structured output format
        top_3 = []
        for i in range(len(top_probs)):
            label = self.class_names[top_indices[i]]
            conf = float(top_probs[i])
            top_3.append({
                "class_name": label,
                "confidence": conf
            })

        main_disease = self.class_names[top_indices[0]]
        main_confidence = float(top_probs[0])

        return {
            "disease_name": main_disease,
            "confidence": main_confidence,
            "top_3_predictions": top_3
        }

    def predict_path(self, image_path: str, top_k: int = 3) -> dict:
        """
        Wrapper to execute prediction from local file path.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image path not found: {image_path}")
            
        image = Image.open(image_path)
        return self.predict(image, top_k=top_k)
