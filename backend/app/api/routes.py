"""API routes for feedback operations."""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
import logging

from ..database import get_db
from ..core.exceptions import FeedbackNotFoundError, AIServiceError
from ..core.constants import DEFAULT_PAGE, DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE, MAX_FEEDBACK_FOR_SUMMARY
from ..schemas import (
    FeedbackCreate, FeedbackResponse, FeedbackListResponse,
    SummarizeRequest, SummarizeResponse, StatsResponse
)
from ..services.feedback_service import FeedbackService
from ..services.ai_service import ai_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/feedback", response_model=FeedbackListResponse, tags=["Feedback"])
async def get_feedback(
    page: int = Query(DEFAULT_PAGE, ge=1, description="Page number"),
    page_size: int = Query(DEFAULT_PAGE_SIZE, ge=1, le=MAX_PAGE_SIZE, description="Items per page"),
    search: Optional[str] = Query(None, description="Search text in feedback content"),
    source: Optional[str] = Query(None, description="Filter by source"),
    sentiment: Optional[str] = Query(None, description="Filter by sentiment"),
    start_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format)"),
    db: Session = Depends(get_db)
):
    """
    Get paginated feedback with optional filters.
    
    Returns a list of feedback items with pagination support.
    """
    skip = (page - 1) * page_size
    
    # Parse date strings
    start_dt = None
    end_dt = None
    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        except ValueError as e:
            logger.warning(f"Invalid start_date format: {start_date}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid start_date format. Use ISO format (e.g., 2024-01-01T00:00:00Z)."
            ) from e
    
    if end_date:
        try:
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        except ValueError as e:
            logger.warning(f"Invalid end_date format: {end_date}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid end_date format. Use ISO format (e.g., 2024-01-01T00:00:00Z)."
            ) from e
    
    try:
        feedback, total = FeedbackService.get_feedback(
            db=db,
            skip=skip,
            limit=page_size,
            search=search,
            source=source,
            sentiment=sentiment,
            start_date=start_dt,
            end_date=end_dt
        )
        
        return FeedbackListResponse(
            items=[FeedbackResponse.model_validate(f) for f in feedback],
            total=total,
            page=page,
            page_size=page_size
        )
    except Exception as e:
        logger.error(f"Error fetching feedback: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch feedback"
        ) from e


@router.get("/feedback/stats", response_model=StatsResponse, tags=["Statistics"])
async def get_stats(db: Session = Depends(get_db)):
    """
    Get feedback statistics.
    
    Returns aggregated statistics including total count, sentiment distribution,
    source distribution, and recent feedback count.
    """
    try:
        stats = FeedbackService.get_stats(db)
        return StatsResponse(**stats)
    except Exception as e:
        logger.error(f"Error fetching stats: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch statistics"
        ) from e


@router.get("/feedback/{feedback_id}", response_model=FeedbackResponse, tags=["Feedback"])
async def get_feedback_by_id(feedback_id: int, db: Session = Depends(get_db)):
    """
    Get a single feedback item by ID.
    
    Args:
        feedback_id: The ID of the feedback item to retrieve
    """
    from ..models import Feedback
    
    feedback = db.query(Feedback).filter(Feedback.id == feedback_id).first()
    if not feedback:
        raise FeedbackNotFoundError(f"Feedback with ID {feedback_id} not found")
    
    return FeedbackResponse.model_validate(feedback)


@router.post("/feedback", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED, tags=["Feedback"])
async def create_feedback(feedback: FeedbackCreate, db: Session = Depends(get_db)):
    """
    Create new feedback. Sentiment will be automatically analyzed using AI.
    
    Args:
        feedback: Feedback data including text, source, and optional metadata
    """
    try:
        created = FeedbackService.create_feedback(
            db=db,
            text=feedback.text,
            source=feedback.source,
            metadata=feedback.metadata
        )
        logger.info(f"Created feedback with ID {created.id}")
        return FeedbackResponse.model_validate(created)
    except AIServiceError as e:
        logger.error(f"AI service error while creating feedback: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error creating feedback: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create feedback"
        ) from e


@router.post("/feedback/summarize", response_model=SummarizeResponse, tags=["AI"])
async def summarize_feedback(request: SummarizeRequest, db: Session = Depends(get_db)):
    """
    Generate AI summary for feedback items.
    
    Can summarize specific feedback by IDs or filtered feedback based on criteria.
    """
    feedback_items = []
    
    try:
        if request.feedback_ids:
            # Summarize specific feedback items
            feedback_items = FeedbackService.get_feedback_by_ids(db, request.feedback_ids)
            if not feedback_items:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No feedback found with the provided IDs"
                )
        elif request.filters:
            # Summarize based on filters
            filters = request.filters
            start_dt = None
            end_dt = None
            
            if filters.get('start_date'):
                try:
                    start_dt = datetime.fromisoformat(filters['start_date'].replace('Z', '+00:00'))
                except ValueError:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid start_date format in filters"
                    )
            if filters.get('end_date'):
                try:
                    end_dt = datetime.fromisoformat(filters['end_date'].replace('Z', '+00:00'))
                except ValueError:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Invalid end_date format in filters"
                    )
            
            feedback_items, _ = FeedbackService.get_feedback(
                db=db,
                skip=0,
                limit=MAX_FEEDBACK_FOR_SUMMARY,
                search=filters.get('search'),
                source=filters.get('source'),
                sentiment=filters.get('sentiment'),
                start_date=start_dt,
                end_date=end_dt
            )
        else:
            # Get recent feedback if no filters
            feedback_items, _ = FeedbackService.get_feedback(db=db, skip=0, limit=MAX_FEEDBACK_FOR_SUMMARY)
        
        if not feedback_items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No feedback found to summarize"
            )
        
        # Extract text from feedback items
        feedback_texts = [item.text for item in feedback_items]
        
        # Generate summary
        context = request.filters or {}
        summary = ai_service.summarize_feedback(feedback_texts, context=context)
        
        # Calculate sentiment breakdown
        sentiment_breakdown = {}
        for item in feedback_items:
            sentiment = item.sentiment or 'unknown'
            sentiment_breakdown[sentiment] = sentiment_breakdown.get(sentiment, 0) + 1
        
        logger.info(f"Generated summary for {len(feedback_items)} feedback items")
        return SummarizeResponse(
            summary=summary,
            feedback_count=len(feedback_items),
            sentiment_breakdown=sentiment_breakdown
        )
    except HTTPException:
        raise
    except AIServiceError as e:
        logger.error(f"AI service error during summarization: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate summary"
        ) from e
