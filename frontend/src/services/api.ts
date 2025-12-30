/** API client for backend communication. */
import type {
  Feedback,
  FeedbackListResponse,
  SummarizeRequest,
  SummarizeResponse,
  StatsResponse,
  FeedbackFilters,
} from '../types/feedback';
import { API_BASE_URL } from '../constants';
import { handleApiError, ApiException } from '../utils/errorHandler';

class ApiClient {
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`;
    
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
      });

      if (!response.ok) {
        await handleApiError(response);
      }

      return response.json();
    } catch (error) {
      if (error instanceof ApiException) {
        throw error;
      }
      throw new ApiException(0, 'Network error occurred', 'network_error');
    }
  }

  async getFeedback(
    page: number = 1,
    pageSize: number = 20,
    filters?: FeedbackFilters
  ): Promise<FeedbackListResponse> {
    const params = new URLSearchParams({
      page: page.toString(),
      page_size: pageSize.toString(),
    });

    if (filters?.search) params.append('search', filters.search);
    if (filters?.source) params.append('source', filters.source);
    if (filters?.sentiment) params.append('sentiment', filters.sentiment);
    if (filters?.start_date) params.append('start_date', filters.start_date);
    if (filters?.end_date) params.append('end_date', filters.end_date);

    return this.request<FeedbackListResponse>(`/api/feedback?${params}`);
  }

  async getFeedbackById(id: number): Promise<Feedback> {
    return this.request<Feedback>(`/api/feedback/${id}`);
  }

  async createFeedback(
    text: string,
    source: string,
    metadata?: Record<string, any>
  ): Promise<Feedback> {
    return this.request<Feedback>('/api/feedback', {
      method: 'POST',
      body: JSON.stringify({ text, source, metadata }),
    });
  }

  async summarizeFeedback(request: SummarizeRequest): Promise<SummarizeResponse> {
    return this.request<SummarizeResponse>('/api/feedback/summarize', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  async getStats(): Promise<StatsResponse> {
    return this.request<StatsResponse>('/api/feedback/stats');
  }
}

export const apiClient = new ApiClient();

