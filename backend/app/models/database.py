"""
Database models and initialization
"""

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DateTime, JSON, Boolean, Integer
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./inclusiveai.db")

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


class UserPreferences(Base):
    """User preferences model"""
    __tablename__ = "user_preferences"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True)
    assist_mode = Column(String, nullable=False)
    source = Column(String)  # 'camera_recommendation' or 'manual_selection'
    confidence = Column(String)  # JSON string of confidence scores
    preferences = Column(JSON)  # Additional preferences
    completed_onboarding = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ConsentRecord(Base):
    """Consent records model"""
    __tablename__ = "consent_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    consent_type = Column(String)  # 'camera_usage', etc.
    granted = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    version = Column(String)


class ScanRecord(Base):
    """Camera scan records (anonymized)"""
    __tablename__ = "scan_records"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    features = Column(JSON)  # Anonymized feature summaries
    recommendation = Column(JSON)  # Recommendation result
    timestamp = Column(DateTime, default=datetime.utcnow)
    deleted = Column(Boolean, default=False)


async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    """Dependency for getting database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

