"""
FastAPI routes for CropGuard prediction API
Wraps existing ML pipeline from models/predict.py
"""
import os
import sys
import uuid
import numpy as np
from io import BytesIO
from fastapi import APIRouter, File, UploadFile, HTTPException
from PIL import Image

from app.config import MAX_UPLOAD_SIZE, ALLOWED_EXTENSIONS, DISEASE_CLASSES
from app.api.schemas import PredictionResponse, HealthResponse
from app.models.disease_database import get_disease_info

router = APIRouter(prefix="/api", tags=["prediction"])

# Import existing ML pipeline (preserve original code)
# Add parent directory to path to import root-level modules
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

try:
    from models.onnx_predictor import ONNXPredictor
    PREDICTOR_AVAILABLE = True
    predictor = None  # Lazy load
except ImportError as e:
    print(f"Warning: Could not import ONNXPredictor: {e}")
    print(f"This is critical. ONNX model must be available for predictions.")
    PREDICTOR_AVAILABLE = False


def get_predictor():
    """Lazy load the ONNX predictor on first use"""
    global predictor
    if predictor is None:
        if not PREDICTOR_AVAILABLE:
            raise HTTPException(
                status_code=500,
                detail="ONNX predictor module not available"
            )
        try:
            predictor = ONNXPredictor()
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to load ONNX model: {str(e)}"
            )
    return predictor


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="CropGuard backend is running"
    )


@router.post("/predict", response_model=PredictionResponse)
async def predict_disease(image: UploadFile = File(...)):
    """
    Main prediction endpoint.
    Accepts image upload and returns disease classification with confidence scores.
    
    Args:
        image: Uploaded image file (JPG, PNG, WebP)
        
    Returns:
        PredictionResponse with:
        - Primary disease prediction
        - Top 3 predictions with confidence
        - Detailed disease information (symptoms, treatment, prevention)
    """
    
    # Validate file
    if not image.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Check file extension
    file_ext = image.filename.split(".")[-1].lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Read file
    try:
        contents = await image.read()
        
        # Check file size
        if len(contents) > MAX_UPLOAD_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Max size: {MAX_UPLOAD_SIZE / 1024 / 1024}MB"
            )
        
        # Load image
        image_pil = Image.open(BytesIO(contents))
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid image file: {str(e)}"
        )
    
    # Run prediction using ONNX model
    try:
        predictor = get_predictor()
        prediction_result = predictor.predict(image_pil, top_k=3)
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )
    
    # Extract results
    primary_disease = prediction_result.get("disease_name", "Unknown")
    confidence = prediction_result.get("confidence", 0.0)
    top_3_raw = prediction_result.get("top_3_predictions", [])
    
    # Format top-3 predictions with colors
    top_3_formatted = []
    for idx, pred in enumerate(top_3_raw, 1):
        disease_name = pred.get("class_name", "Unknown")
        disease_info = get_disease_info(disease_name)
        
        top_3_formatted.append({
            "rank": idx,
            "disease_name": disease_name,
            "confidence": float(pred.get("confidence", 0.0)),
            "color": disease_info.get("color", "#6B7280")
        })
    
    # Get detailed disease information
    disease_details_raw = get_disease_info(primary_disease)
    disease_details = {
        "name": disease_details_raw.get("name", primary_disease),
        "scientific_name": disease_details_raw.get("scientific_name", "N/A"),
        "severity": disease_details_raw.get("severity", "unknown"),
        "symptoms": disease_details_raw.get("symptoms", []),
        "treatment": disease_details_raw.get("treatment", []),
        "prevention": disease_details_raw.get("prevention", []),
        "description": disease_details_raw.get("description", ""),
        "color": disease_details_raw.get("color", "#6B7280")
    }
    
    # Build response
    response_data = {
        "image_id": str(uuid.uuid4()),
        "prediction": {
            "primary_disease": primary_disease,
            "confidence": float(confidence),
            "model_version": "v1.0"
        },
        "top_3": top_3_formatted,
        "disease_details": disease_details
    }
    
    return PredictionResponse(success=True, data=response_data)


@router.get("/models")
async def get_models():
    """Get available model information"""
    try:
        predictor = get_predictor()
        model_info = predictor.get_model_info()
        return {
            "models": [
                {
                    "name": "ResNet50 + ONNX Runtime",
                    "version": "2.0",
                    "framework": "ONNX Runtime",
                    "input_size": [224, 224],
                    "num_classes": model_info["num_classes"],
                    "classes": model_info["class_names"],
                    "model_path": model_info["model_path"],
                    "runtime": model_info["runtime"]
                }
            ]
        }
    except Exception as e:
        return {
            "error": f"Could not retrieve model info: {str(e)}"
        }
