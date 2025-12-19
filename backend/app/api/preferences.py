"""
User Preferences API endpoints
Handles saving and retrieving user preferences
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime
import logging

from app.models.database import UserPreferences, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

router = APIRouter()
logger = logging.getLogger(__name__)


class PreferenceRequest(BaseModel):
    """Request model for saving preferences"""
    user_id: Optional[str] = Field(None, description="User ID")
    assist_mode: str = Field(..., description="Selected assist mode")
    source: str = Field(..., description="Source: 'camera_recommendation' or 'manual_selection'")
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0, description="Confidence score")
    preferences: Optional[Dict] = Field(None, description="Additional preferences")
    completed_onboarding: bool = Field(True, description="Onboarding completed")


class PreferenceResponse(BaseModel):
    """Response model for preferences"""
    user_id: str
    assist_mode: str
    source: str
    confidence: Optional[float]
    preferences: Optional[Dict]
    completed_onboarding: bool
    created_at: datetime
    updated_at: datetime


@router.post("", response_model=PreferenceResponse)
async def save_preferences(
    request: PreferenceRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Save user preferences
    
    Args:
        request: Preference request
        db: Database session
    
    Returns:
        Saved preferences
    """
    try:
        user_id = request.user_id or "anonymous"
        
        # Check if preferences exist
        result = await db.execute(
            select(UserPreferences).where(UserPreferences.user_id == user_id)
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            # Update existing
            existing.assist_mode = request.assist_mode
            existing.source = request.source
            existing.confidence = str(request.confidence) if request.confidence else None
            existing.preferences = request.preferences
            existing.completed_onboarding = request.completed_onboarding
            existing.updated_at = datetime.utcnow()
            await db.commit()
            await db.refresh(existing)
            
            return PreferenceResponse(
                user_id=existing.user_id,
                assist_mode=existing.assist_mode,
                source=existing.source,
                confidence=float(existing.confidence) if existing.confidence else None,
                preferences=existing.preferences,
                completed_onboarding=existing.completed_onboarding,
                created_at=existing.created_at,
                updated_at=existing.updated_at
            )
        else:
            # Create new
            new_pref = UserPreferences(
                user_id=user_id,
                assist_mode=request.assist_mode,
                source=request.source,
                confidence=str(request.confidence) if request.confidence else None,
                preferences=request.preferences,
                completed_onboarding=request.completed_onboarding
            )
            db.add(new_pref)
            await db.commit()
            await db.refresh(new_pref)
            
            return PreferenceResponse(
                user_id=new_pref.user_id,
                assist_mode=new_pref.assist_mode,
                source=new_pref.source,
                confidence=float(new_pref.confidence) if new_pref.confidence else None,
                preferences=new_pref.preferences,
                completed_onboarding=new_pref.completed_onboarding,
                created_at=new_pref.created_at,
                updated_at=new_pref.updated_at
            )
            
    except Exception as e:
        logger.error(f"Error saving preferences: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error saving preferences: {str(e)}"
        )


@router.get("/{user_id}", response_model=PreferenceResponse)
async def get_preferences(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Get user preferences
    
    Args:
        user_id: User ID
        db: Database session
    
    Returns:
        User preferences
    """
    try:
        result = await db.execute(
            select(UserPreferences).where(UserPreferences.user_id == user_id)
        )
        pref = result.scalar_one_or_none()
        
        if not pref:
            raise HTTPException(status_code=404, detail="Preferences not found")
        
        return PreferenceResponse(
            user_id=pref.user_id,
            assist_mode=pref.assist_mode,
            source=pref.source,
            confidence=float(pref.confidence) if pref.confidence else None,
            preferences=pref.preferences,
            completed_onboarding=pref.completed_onboarding,
            created_at=pref.created_at,
            updated_at=pref.updated_at
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting preferences: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting preferences: {str(e)}"
        )


@router.delete("/{user_id}")
async def delete_preferences(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete user preferences (privacy feature)
    
    Args:
        user_id: User ID
        db: Database session
    
    Returns:
        Success message
    """
    try:
        result = await db.execute(
            select(UserPreferences).where(UserPreferences.user_id == user_id)
        )
        pref = result.scalar_one_or_none()
        
        if pref:
            await db.delete(pref)
            await db.commit()
        
        return {"message": "Preferences deleted successfully"}
        
    except Exception as e:
        logger.error(f"Error deleting preferences: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting preferences: {str(e)}"
        )

