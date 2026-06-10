"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class PredictionItem(BaseModel):
    """Single prediction result"""
    rank: int
    disease_name: str
    confidence: float
    color: str


class DiseaseDetails(BaseModel):
    """Disease information"""
    name: str
    scientific_name: str
    severity: str
    symptoms: List[str]
    treatment: List[str]
    prevention: List[str]
    description: str
    color: str


class PredictionResponse(BaseModel):
    """Full prediction response"""
    success: bool
    data: Optional[dict] = None
    error: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "image_id": "abc123",
                    "prediction": {
                        "primary_disease": "Early Blight",
                        "confidence": 0.94,
                        "model_version": "v1.0"
                    },
                    "top_3": [
                        {
                            "rank": 1,
                            "disease_name": "Early Blight",
                            "confidence": 0.94,
                            "color": "#FF6B6B"
                        },
                        {
                            "rank": 2,
                            "disease_name": "Septoria Leaf Spot",
                            "confidence": 0.05,
                            "color": "#FFA500"
                        },
                        {
                            "rank": 3,
                            "disease_name": "Healthy",
                            "confidence": 0.01,
                            "color": "#10B981"
                        }
                    ],
                    "disease_details": {
                        "name": "Early Blight",
                        "scientific_name": "Alternaria solani",
                        "severity": "medium",
                        "symptoms": [
                            "Brown, concentric rings on lower leaves",
                            "Yellow halo around lesions"
                        ],
                        "treatment": [
                            "Remove infected leaves",
                            "Apply fungicide"
                        ],
                        "prevention": [
                            "Plant resistant varieties",
                            "Practice crop rotation"
                        ],
                        "description": "Early blight is a fungal disease...",
                        "color": "#FF6B6B"
                    }
                }
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "message": "CropGuard backend is running"
            }
        }
