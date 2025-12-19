"""
Reports API endpoints
Handles usage reports and analytics (privacy-compliant)
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime
import logging

from app.models.database import UserPreferences, ScanRecord, get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/usage")
async def get_usage_stats(
    db: AsyncSession = Depends(get_db)
):
    """
    Get anonymized usage statistics
    
    Returns:
        Aggregated usage statistics (no personal data)
    """
    try:
        # Count total users
        result = await db.execute(
            select(func.count(UserPreferences.id))
        )
        total_users = result.scalar() or 0
        
        # Count by assist mode
        result = await db.execute(
            select(
                UserPreferences.assist_mode,
                func.count(UserPreferences.id)
            ).group_by(UserPreferences.assist_mode)
        )
        mode_counts = {row[0]: row[1] for row in result.all()}
        
        # Count scans (non-deleted)
        result = await db.execute(
            select(func.count(ScanRecord.id)).where(ScanRecord.deleted == False)
        )
        total_scans = result.scalar() or 0
        
        return {
            "total_users": total_users,
            "mode_distribution": mode_counts,
            "total_scans": total_scans,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting usage stats: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error getting usage stats: {str(e)}"
        )


@router.get("/health")
async def reports_health():
    """Health check for reports service"""
    return {
        "status": "healthy",
        "service": "reports"
    }

