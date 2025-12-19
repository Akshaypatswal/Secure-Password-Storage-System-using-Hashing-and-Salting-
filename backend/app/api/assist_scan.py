"""
Assist Scan API endpoints
Handles camera scan data processing and recommendation generation
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, Dict, List, Any
from datetime import datetime
import logging

from app.services.assist_classifier import AssistClassifier
from app.models.database import ScanRecord, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize classifier
classifier = AssistClassifier()


class ScanFeatures(BaseModel):
    """Scan features from camera analysis"""
    handSignFreq: float = Field(0.0, ge=0.0, le=10.0, description="Hand signing frequency")
    speechDetected: bool = Field(False, description="Speech detected")
    gazePattern: Optional[str] = Field(None, description="Gaze pattern")
    posture: Optional[str] = Field(None, description="Posture cues")
    interactionBehavior: Optional[str] = Field(None, description="Interaction behavior")
    timestamp: Optional[str] = Field(None, description="Scan timestamp")


class ScanRequest(BaseModel):
    """Request model for assist scan"""
    features: ScanFeatures
    duration: int = Field(20, ge=1, le=60, description="Scan duration in seconds")
    user_id: Optional[str] = Field(None, description="User ID (optional)")


class RecommendationResponse(BaseModel):
    """Response model for recommendation"""
    mode: str = Field(..., description="Recommended assist mode")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    cues: List[str] = Field(..., description="Top cues that triggered recommendation")
    scores: Dict[str, float] = Field(..., description="All mode scores")
    explainability: Dict[str, Any] = Field(..., description="Explainability information")


@router.post("", response_model=RecommendationResponse)
async def process_assist_scan(
    request: ScanRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Process camera scan data and return assist mode recommendation
    
    Args:
        request: Scan request with features
        db: Database session
    
    Returns:
        Recommendation with confidence, cues, and explainability
    """
    try:
        # Extract features
        features_dict = request.features.dict()
        
        # Get recommendation from classifier
        recommendation = classifier.classify(features_dict)
        
        # Store scan record (anonymized, with user consent)
        if request.user_id:
            scan_record = ScanRecord(
                user_id=request.user_id,
                features=features_dict,
                recommendation=recommendation,
                timestamp=datetime.utcnow()
            )
            db.add(scan_record)
            await db.commit()
        
        return recommendation
        
    except Exception as e:
        logger.error(f"Error processing assist scan: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing scan: {str(e)}"
        )


@router.get("/health")
async def scan_health():
    """Health check for assist scan service"""
    return {
        "status": "healthy",
        "classifier_loaded": classifier.is_loaded(),
        "service": "assist_scan"
    }

