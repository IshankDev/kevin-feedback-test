"""Feedback service layer for business logic."""
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import logging

from ..models import Feedback
from ..core.exceptions import FeedbackNotFoundError, DatabaseError
from ..core.constants import VALID_SENTIMENTS, VALID_SOURCES
from .ai_service import ai_service

logger = logging.getLogger(__name__)


class FeedbackService:
    """Service for feedback business logic."""
    
    @staticmethod
    def get_feedback(
        db: Session,
        skip: int = 0,
        limit: int = 20,
        search: Optional[str] = None,
        source: Optional[str] = None,
        sentiment: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> tuple[List[Feedback], int]:
        """Get paginated feedback with filters."""
        query = db.query(Feedback)
        
        # Apply filters
        if search:
            query = query.filter(Feedback.text.ilike(f"%{search}%"))
        
        if source:
            query = query.filter(Feedback.source == source)
        
        if sentiment:
            query = query.filter(Feedback.sentiment == sentiment)
        
        if start_date:
            query = query.filter(Feedback.created_at >= start_date)
        
        if end_date:
            query = query.filter(Feedback.created_at <= end_date)
        
        # Get total count
        total = query.count()
        
        # Apply pagination and ordering
        feedback = query.order_by(Feedback.created_at.desc()).offset(skip).limit(limit).all()
        
        return feedback, total
    
    @staticmethod
    def get_feedback_by_ids(db: Session, feedback_ids: List[int]) -> List[Feedback]:
        """Get feedback items by their IDs."""
        if not feedback_ids:
            return []
        try:
            return db.query(Feedback).filter(Feedback.id.in_(feedback_ids)).all()
        except Exception as e:
            logger.error(f"Error fetching feedback by IDs: {str(e)}", exc_info=True)
            raise DatabaseError(f"Failed to fetch feedback by IDs: {str(e)}") from e
    
    @staticmethod
    def create_feedback(db: Session, text: str, source: str, metadata: Optional[Dict] = None) -> Feedback:
        """
        Create new feedback and analyze sentiment.
        
        Args:
            db: Database session
            text: Feedback text content
            source: Feedback source (must be in VALID_SOURCES)
            metadata: Optional metadata dictionary
            
        Returns:
            Created Feedback object
            
        Raises:
            ValueError: If source is invalid
            DatabaseError: If database operation fails
        """
        if source not in VALID_SOURCES:
            raise ValueError(f"Invalid source: {source}. Must be one of {VALID_SOURCES}")
        
        if not text or not text.strip():
            raise ValueError("Feedback text cannot be empty")
        
        try:
            # Analyze sentiment using AI
            sentiment = ai_service.analyze_sentiment(text)
            
            if sentiment not in VALID_SENTIMENTS:
                logger.warning(f"Invalid sentiment '{sentiment}' returned, using neutral")
                sentiment = 'neutral'
            
            feedback = Feedback(
                text=text.strip(),
                source=source,
                sentiment=sentiment,
                extra_data=metadata
            )
            
            db.add(feedback)
            db.commit()
            db.refresh(feedback)
            
            logger.info(f"Created feedback ID {feedback.id} with sentiment {sentiment}")
            return feedback
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating feedback: {str(e)}", exc_info=True)
            raise DatabaseError(f"Failed to create feedback: {str(e)}") from e
    
    @staticmethod
    def get_stats(db: Session) -> Dict[str, Any]:
        """Get feedback statistics."""
        total = db.query(Feedback).count()
        
        # Sentiment counts
        sentiment_counts = (
            db.query(Feedback.sentiment, func.count(Feedback.id))
            .group_by(Feedback.sentiment)
            .all()
        )
        sentiment_dict = {sent or 'unknown': count for sent, count in sentiment_counts}
        
        # Source counts
        source_counts = (
            db.query(Feedback.source, func.count(Feedback.id))
            .group_by(Feedback.source)
            .all()
        )
        source_dict = {source: count for source, count in source_counts}
        
        # Recent count (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_count = db.query(Feedback).filter(Feedback.created_at >= week_ago).count()
        
        return {
            'total_feedback': total,
            'sentiment_counts': sentiment_dict,
            'source_counts': source_dict,
            'recent_count': recent_count
        }
    
    @staticmethod
    def analyze_sentiment_for_feedback(db: Session, feedback_id: int) -> Feedback:
        """Re-analyze sentiment for a specific feedback item."""
        feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
        if feedback:
            feedback.sentiment = ai_service.analyze_sentiment(feedback.text)
            db.commit()
            db.refresh(feedback)
        return feedback

