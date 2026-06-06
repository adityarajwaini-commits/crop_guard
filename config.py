import os

class Config:
    """
    Central configuration settings for CropGuard.
    All parameters are placeholders to be customized during implementation.
    """
    # Directory Configurations
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    ASSETS_DIR = os.path.join(BASE_DIR, "assets")
    SAVED_MODELS_DIR = os.path.join(BASE_DIR, "saved_models")
    
    # Model Configurations
    MODEL_NAME = "resnet50"
    IMAGE_SIZE = (224, 224)
    BATCH_SIZE = 32
    LEARNING_RATE = 0.001
    EPOCHS = 10
    
    # Output classes placeholder
    CLASSES = ["Healthy", "Diseased_Type_A", "Diseased_Type_B"]
