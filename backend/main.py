"""
Uvicorn entry point for CropGuard backend
Run with: python -m uvicorn backend.main:app
Or: python main.py
"""
import os
import uvicorn
from app.main import app

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
