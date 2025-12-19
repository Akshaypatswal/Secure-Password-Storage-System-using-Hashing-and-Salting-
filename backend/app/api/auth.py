"""
Authentication API endpoints
Simple authentication for demo purposes
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


class AuthRequest(BaseModel):
    """Request model for authentication"""
    username: Optional[str] = Field(None, description="Username")
    password: Optional[str] = Field(None, description="Password")


class AuthResponse(BaseModel):
    """Response model for authentication"""
    user_id: str
    token: Optional[str] = None
    message: str


@router.post("/login", response_model=AuthResponse)
async def login(request: AuthRequest):
    """
    Simple login endpoint (demo purposes)
    
    In production, implement proper JWT authentication
    """
    # Demo: Accept any credentials
    user_id = request.username or "anonymous"
    
    return AuthResponse(
        user_id=user_id,
        token="demo_token",
        message="Login successful (demo mode)"
    )


@router.post("/register", response_model=AuthResponse)
async def register(request: AuthRequest):
    """
    Simple registration endpoint (demo purposes)
    """
    user_id = request.username or "anonymous"
    
    return AuthResponse(
        user_id=user_id,
        token="demo_token",
        message="Registration successful (demo mode)"
    )


@router.get("/me")
async def get_current_user():
    """
    Get current user info (demo purposes)
    """
    return {
        "user_id": "anonymous",
        "message": "Demo mode - no authentication required"
    }

