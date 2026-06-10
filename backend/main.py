"""
Uvicorn entry point for CropGuard backend
Run with: python -m uvicorn backend.main:app --reload
Or: python main.py
"""
import uvicorn
from app.main import app
from app.config import HOST, PORT, DEBUG

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        reload=DEBUG,
        log_level="info"
    )
