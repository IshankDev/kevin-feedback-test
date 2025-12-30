export interface Feedback {
  id: number;
  text: string;
  source: string;
  sentiment: string | null;
  created_at: string;
  metadata?: Record<string, any>;
}

export interface FeedbackListResponse {
  items: Feedback[];
  total: number;
  page: number;
  page_size: number;
}

export interface SummarizeRequest {
  feedback_ids?: number[];
  filters?: {
    search?: string;
    source?: string;
    sentiment?: string;
    start_date?: string;
    end_date?: string;
  };
}

export interface SummarizeResponse {
  summary: string;
  feedback_count: number;
  sentiment_breakdown: Record<string, number>;
}

export interface StatsResponse {
  total_feedback: number;
  sentiment_counts: Record<string, number>;
  source_counts: Record<string, number>;
  recent_count: number;
}

export interface FeedbackFilters {
  search?: string;
  source?: string;
  sentiment?: string;
  start_date?: string;
  end_date?: string;
}
