from pydantic import BaseModel, Field, field_serializer
from datetime import datetime
from typing import Optional, Dict, Any


class FeedbackBase(BaseModel):
    text: str
    source: str
    metadata: Optional[Dict[str, Any]] = Field(None, alias="extra_data", serialization_alias="metadata")
    
    class Config:
        from_attributes = True
        populate_by_name = True


class FeedbackCreate(FeedbackBase):
    pass


class FeedbackResponse(FeedbackBase):
    id: int
    sentiment: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class FeedbackListResponse(BaseModel):
    items: list[FeedbackResponse]
    total: int
    page: int
    page_size: int


class SummarizeRequest(BaseModel):
    feedback_ids: Optional[list[int]] = None
    filters: Optional[Dict[str, Any]] = None


class SummarizeResponse(BaseModel):
    summary: str
    feedback_count: int
    sentiment_breakdown: Dict[str, int]


class StatsResponse(BaseModel):
    total_feedback: int
    sentiment_counts: Dict[str, int]
    source_counts: Dict[str, int]
    recent_count: int  # Last 7 days

