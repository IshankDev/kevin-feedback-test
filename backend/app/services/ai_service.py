"""AI service for sentiment analysis and summarization using Google Gemini."""
import google.generativeai as genai
from typing import List, Dict, Any, Optional
import logging

from ..config import settings
from ..core.exceptions import AIServiceError
from ..core.constants import VALID_SENTIMENTS, MAX_FEEDBACK_FOR_SUMMARY

logger = logging.getLogger(__name__)

# Configure Gemini API
try:
    genai.configure(api_key=settings.gemini_api_key)
except Exception as e:
    logger.error(f"Failed to configure Gemini API: {str(e)}")
    raise


class AIService:
    """Service for interacting with Google Gemini API."""
    
    def __init__(self):
        # Use gemini-2.5-flash for faster responses
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def analyze_sentiment(self, text: str) -> str:
        """
        Analyze sentiment of a single feedback text.
        
        Args:
            text: Feedback text to analyze
            
        Returns:
            'positive', 'negative', or 'neutral'
            
        Raises:
            AIServiceError: If AI service fails and fallback also fails
        """
        if not text or not text.strip():
            logger.warning("Empty text provided for sentiment analysis, returning neutral")
            return 'neutral'
        
        try:
            # Limit text length to avoid token limits
            text_snippet = text[:1000] if len(text) > 1000 else text
            
            prompt = f"""Analyze the sentiment of the following customer feedback. 
            Respond with ONLY one word: 'positive', 'negative', or 'neutral'.
            
            Feedback: {text_snippet}
            
            Sentiment:"""
            
            response = self.model.generate_content(prompt)
            sentiment = response.text.strip().lower().split()[0]  # Get first word only
            
            # Validate response
            if sentiment in VALID_SENTIMENTS:
                logger.debug(f"AI sentiment analysis: {sentiment}")
                return sentiment
            else:
                logger.warning(f"Invalid sentiment '{sentiment}' from AI, using fallback")
                return self._fallback_sentiment(text)
                
        except Exception as e:
            logger.error(f"Error analyzing sentiment with AI: {str(e)}", exc_info=True)
            # Use fallback instead of raising exception
            return self._fallback_sentiment(text)
    
    def summarize_feedback(self, feedback_texts: List[str], context: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate a summary of multiple feedback items.
        
        Args:
            feedback_texts: List of feedback text strings
            context: Optional context like date range, filters, etc.
            
        Returns:
            AI-generated summary string
            
        Raises:
            AIServiceError: If AI service fails
        """
        if not feedback_texts:
            return "No feedback available to summarize."
        
        try:
            # Limit to avoid token limits
            texts_to_summarize = feedback_texts[:MAX_FEEDBACK_FOR_SUMMARY]
            
            if len(feedback_texts) > MAX_FEEDBACK_FOR_SUMMARY:
                logger.warning(
                    f"Summarizing {MAX_FEEDBACK_FOR_SUMMARY} of {len(feedback_texts)} feedback items"
                )
            
            feedback_block = "\n\n---\n\n".join([
                f"Feedback {i+1}:\n{text}" 
                for i, text in enumerate(texts_to_summarize)
            ])
            
            context_str = ""
            if context:
                if context.get('date_range'):
                    context_str += f"Date range: {context['date_range']}\n"
                if context.get('source'):
                    context_str += f"Source filter: {context['source']}\n"
            
            prompt = f"""You are analyzing customer feedback for a product team. 
            Summarize the key themes, complaints, and positive feedback from the following customer feedback entries.
            Be concise but comprehensive. Focus on actionable insights.
            {context_str}
            
            Feedback entries:
            {feedback_block}
            
            Summary:"""
            
            response = self.model.generate_content(prompt)
            summary = response.text.strip()
            logger.info(f"Generated summary of {len(texts_to_summarize)} feedback items")
            return summary
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}", exc_info=True)
            raise AIServiceError(f"Failed to generate summary: {str(e)}") from e
    
    def _fallback_sentiment(self, text: str) -> str:
        """Fallback sentiment analysis using keyword matching."""
        text_lower = text.lower()
        negative_keywords = ['bad', 'terrible', 'awful', 'hate', 'disappointed', 'frustrated', 'broken', 'bug', 'error', 'crash', 'slow', 'worst']
        positive_keywords = ['love', 'great', 'excellent', 'amazing', 'perfect', 'wonderful', 'fantastic', 'best', 'happy', 'satisfied', 'good']
        
        negative_count = sum(1 for keyword in negative_keywords if keyword in text_lower)
        positive_count = sum(1 for keyword in positive_keywords if keyword in text_lower)
        
        if negative_count > positive_count:
            return 'negative'
        elif positive_count > negative_count:
            return 'positive'
        else:
            return 'neutral'


# Singleton instance
ai_service = AIService()

