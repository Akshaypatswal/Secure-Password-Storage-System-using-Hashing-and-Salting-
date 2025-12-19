"""
InclusiveAI Backend - FastAPI Application
Main entry point for the backend API
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from app.api import assist_scan, preferences, auth, reports
from app.models.database import init_db

load_dotenv()

# CORS origins
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events"""
    # Startup
    await init_db()
    yield
    # Shutdown
    pass


app = FastAPI(
    title="InclusiveAI API",
    description="Smart Assistive Platform for People with Disabilities",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(assist_scan.router, prefix="/api/assist-scan", tags=["Assist Scan"])
app.include_router(preferences.router, prefix="/api/preferences", tags=["Preferences"])
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(reports.router, prefix="/api/reports", tags=["Reports"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "InclusiveAI API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "operational"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "InclusiveAI Backend"
    }


@app.get("/api/assist-preview")
async def get_assist_preview(mode: str):
    """
    Get assist mode preview/demo information
    
    Args:
        mode: Assist mode name (voice, sign, text, gesture, motor)
    
    Returns:
        Preview information for the requested mode
    """
    mode_info = {
        "voice": {
            "name": "Voice-First Interface",
            "description": "Optimized for low-vision and blind users",
            "features": ["Voice commands", "Screen reader", "Audio feedback"],
            "demo_url": "/demo/voice"
        },
        "sign": {
            "name": "Sign Language Interface",
            "description": "Optimized for deaf and hard-of-hearing users",
            "features": ["Sign language avatar", "Text chat", "Visual alerts"],
            "demo_url": "/demo/sign"
        },
        "text": {
            "name": "Text-Based Interface",
            "description": "Optimized for hearing-impaired users",
            "features": ["Large text", "Visual indicators", "Text-to-speech"],
            "demo_url": "/demo/text"
        },
        "gesture": {
            "name": "Gesture Interface",
            "description": "Optimized for motor-impaired users",
            "features": ["Hand gestures", "Touch controls", "Adaptive UI"],
            "demo_url": "/demo/gesture"
        },
        "motor": {
            "name": "Motor-Adapted Interface",
            "description": "Large buttons and switch mode support",
            "features": ["Large buttons", "Switch mode", "Simplified navigation"],
            "demo_url": "/demo/motor"
        }
    }
    
    if mode not in mode_info:
        raise HTTPException(status_code=404, detail=f"Mode '{mode}' not found")
    
    return {
        "mode": mode,
        **mode_info[mode]
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "path": str(request.url)
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

