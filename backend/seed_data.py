"""Script to seed the database with sample feedback data."""
import sys
from datetime import datetime, timedelta, timezone
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add parent directory to path
sys.path.insert(0, '.')

from app.database import Base, get_db
from app.models import Feedback
from app.config import settings

# Sample feedback data
SAMPLE_FEEDBACK = [
    {
        "text": "The app crashes every time I try to upload a photo. This is really frustrating and I've lost several important images.",
        "source": "app_store",
    },
    {
        "text": "Love the new dark mode feature! It's much easier on the eyes during night time use.",
        "source": "survey",
    },
    {
        "text": "I've been waiting for customer support response for 3 days now. The ticket #12345 is still unresolved.",
        "source": "support_ticket",
    },
    {
        "text": "The search functionality is broken. When I search for 'settings', nothing comes up even though I know it exists.",
        "source": "app_store",
    },
    {
        "text": "Great update! The performance improvements are noticeable. The app feels much faster now.",
        "source": "survey",
    },
    {
        "text": "I can't log in to my account. I've reset my password three times but still getting authentication errors.",
        "source": "support_ticket",
    },
    {
        "text": "The UI is clean and intuitive. Really enjoying the user experience so far.",
        "source": "app_store",
    },
    {
        "text": "Battery drain is terrible after the latest update. My phone battery used to last all day, now it's dead by 2pm.",
        "source": "app_store",
    },
    {
        "text": "The onboarding process was smooth and helpful. I understood all the features quickly.",
        "source": "survey",
    },
    {
        "text": "Feature request: Can we add the ability to export data to CSV? This would be really helpful for my workflow.",
        "source": "support_ticket",
    },
    {
        "text": "The app freezes when I try to sync my data. I have to force close and restart multiple times.",
        "source": "app_store",
    },
    {
        "text": "Excellent customer service! The support team resolved my issue within hours.",
        "source": "survey",
    },
    {
        "text": "Notifications are not working. I'm not receiving any alerts even though they're enabled in settings.",
        "source": "support_ticket",
    },
    {
        "text": "The new design is beautiful! Much more modern and professional looking.",
        "source": "app_store",
    },
    {
        "text": "I'm experiencing data loss. Some of my saved items disappeared after the update. This is unacceptable.",
        "source": "support_ticket",
    },
    {
        "text": "The tutorial videos are very helpful. They made it easy to get started with the app.",
        "source": "survey",
    },
    {
        "text": "The app takes forever to load. Sometimes I wait 30 seconds just to see the home screen.",
        "source": "app_store",
    },
    {
        "text": "I love how customizable the dashboard is. I can arrange everything exactly how I want it.",
        "source": "survey",
    },
    {
        "text": "The payment processing failed multiple times. I tried different cards but none worked. Very frustrating.",
        "source": "support_ticket",
    },
    {
        "text": "The offline mode works perfectly! I can access my data even without internet connection.",
        "source": "app_store",
    },
    {
        "text": "The app is too complicated. There are too many features and I can't find what I need.",
        "source": "survey",
    },
    {
        "text": "Privacy concerns: I noticed the app is requesting location access even when not needed. Why?",
        "source": "support_ticket",
    },
    {
        "text": "The collaboration features are amazing! My team can work together seamlessly now.",
        "source": "app_store",
    },
    {
        "text": "The app keeps logging me out. I have to sign in every single time I open it.",
        "source": "support_ticket",
    },
    {
        "text": "The price is too high for what you get. There are free alternatives that do the same thing.",
        "source": "survey",
    },
    {
        "text": "The integration with other tools is seamless. It saved me hours of manual work.",
        "source": "app_store",
    },
    {
        "text": "I'm getting spam notifications. Please add an option to filter or disable certain types of alerts.",
        "source": "support_ticket",
    },
    {
        "text": "The documentation is comprehensive and well-written. I found answers to all my questions.",
        "source": "survey",
    },
    {
        "text": "The app is slow and laggy on my older device. Please optimize for lower-end phones.",
        "source": "app_store",
    },
    {
        "text": "The new feature you added is exactly what I needed! Thank you for listening to user feedback.",
        "source": "survey",
    },
]


def seed_database():
    """Seed the database with sample feedback."""
    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        existing_count = db.query(Feedback).count()
        if existing_count > 0:
            print(f"Database already contains {existing_count} feedback items. Skipping seed.")
            return
        
    # Generate feedback with varied timestamps (last 30 days)
    now = datetime.now(timezone.utc)
        feedback_items = []
        
        for i, item in enumerate(SAMPLE_FEEDBACK):
            # Create feedback with random dates in the last 30 days
            days_ago = random.randint(0, 30)
            created_at = now - timedelta(days=days_ago, hours=random.randint(0, 23))
            
            feedback = Feedback(
                text=item["text"],
                source=item["source"],
                created_at=created_at,
                extra_data={"seeded": True}
            )
            feedback_items.append(feedback)
        
        db.add_all(feedback_items)
        db.commit()
        
        print(f"Successfully seeded {len(feedback_items)} feedback items.")
        
        # Now analyze sentiment for all items
        print("Analyzing sentiment for all feedback items...")
        from app.services.ai_service import ai_service
        
        for feedback in feedback_items:
            try:
                feedback.sentiment = ai_service.analyze_sentiment(feedback.text)
            except Exception as e:
                print(f"Error analyzing sentiment for feedback {feedback.id}: {e}")
                # Use fallback
                feedback.sentiment = 'neutral'
        
        db.commit()
        print("Sentiment analysis complete!")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Seeding database with sample feedback...")
    seed_database()

