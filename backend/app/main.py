"""
CropGuard FastAPI Application
Main server entry point with CORS, middleware, and route registration
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
import os

from app.config import CORS_ORIGINS, API_PREFIX, DEBUG
from app.api import routes

# Create FastAPI app
app = FastAPI(
    title="CropGuard API",
    description="Professional plant disease detection API",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add GZIP compression middleware
app.add_middleware(GZipMiddleware, minimum_size=1000)


# Exception handlers
@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "Internal server error"}
    )


# Include routes
app.include_router(routes.router)


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "CropGuard API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/ping")
async def ping():
    """Simple ping endpoint"""
    return {"message": "pong"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=DEBUG
    )
