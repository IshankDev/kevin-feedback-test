import { type Feedback } from '../types/feedback';

interface FeedbackCardProps {
  feedback: Feedback;
}

export function FeedbackCard({ feedback }: FeedbackCardProps) {
  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getSentimentColor = (sentiment: string | null) => {
    if (!sentiment) return 'neutral';
    return sentiment.toLowerCase();
  };

  return (
    <div className={`feedback-card ${getSentimentColor(feedback.sentiment)}`}>
      <div className="feedback-header">
        <span className="feedback-source">{feedback.source}</span>
        {feedback.sentiment && (
          <span className={`sentiment-badge ${feedback.sentiment.toLowerCase()}`}>
            {feedback.sentiment}
          </span>
        )}
        <span className="feedback-date">{formatDate(feedback.created_at)}</span>
      </div>
      <p className="feedback-text">{feedback.text}</p>
    </div>
  );
}

