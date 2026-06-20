"""
Backend configuration for CropGuard FastAPI server
"""
import os
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_DIR = BASE_DIR.parent  # parent of backend

# FastAPI settings
DEBUG = os.getenv("DEBUG", "True") == "True"
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
API_PREFIX = "/api"

# CORS settings
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",  # Vite default
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "https://your-vercel-app.vercel.app",  # TODO: replace with your Vercel frontend URL
]

# File upload settings
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}

# ML Model settings
MODEL_PATH = os.path.join(PROJECT_DIR, "saved_models", "best_model.pth")
IMAGE_SIZE = (224, 224)
CONFIDENCE_THRESHOLD = 0.3

# Disease classification
DISEASE_CLASSES = [
    "Healthy",
    "Early Blight",
    "Late Blight",
    "Septoria Leaf Spot",
    "Yellow Leaf Curl Virus",
    "Bacterial Spot",
    "Target Spot",
]
