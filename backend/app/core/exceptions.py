"""Custom exception classes."""


class FeedbackException(Exception):
    """Base exception for feedback-related errors."""
    pass


class FeedbackNotFoundError(FeedbackException):
    """Raised when feedback item is not found."""
    pass


class AIServiceError(FeedbackException):
    """Raised when AI service fails."""
    pass


class DatabaseError(FeedbackException):
    """Raised when database operation fails."""
    pass

