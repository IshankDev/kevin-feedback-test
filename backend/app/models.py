from sqlalchemy import Column, Integer, String, DateTime, JSON, Index, Text
from sqlalchemy.sql import func
from .database import Base


class Feedback(Base):
    """Feedback model for storing user feedback."""
    
    __tablename__ = "feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    source = Column(String(50), nullable=False, index=True)  # support_ticket, survey, app_store
    sentiment = Column(String(20), nullable=True, index=True)  # positive, negative, neutral
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)
    extra_data = Column(JSON, nullable=True)  # Additional structured data (metadata is reserved in SQLAlchemy)
    
    __table_args__ = (
        Index('idx_created_at', 'created_at'),
        Index('idx_sentiment', 'sentiment'),
        Index('idx_source', 'source'),
    )

