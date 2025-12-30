/** Custom hook for feedback operations. */
import { useState, useCallback } from 'react';
import { apiClient } from '../services/api';
import { getErrorMessage } from '../utils/errorHandler';
import type { Feedback, FeedbackListResponse, FeedbackFilters } from '../types/feedback';

interface UseFeedbackState {
  feedback: Feedback[];
  total: number;
  loading: boolean;
  error: string | null;
}

export function useFeedback() {
  const [state, setState] = useState<UseFeedbackState>({
    feedback: [],
    total: 0,
    loading: false,
    error: null,
  });

  const fetchFeedback = useCallback(
    async (page: number = 1, pageSize: number = 20, filters?: FeedbackFilters) => {
      setState((prev) => ({ ...prev, loading: true, error: null }));
      try {
        const response: FeedbackListResponse = await apiClient.getFeedback(page, pageSize, filters);
        setState({
          feedback: response.items,
          total: response.total,
          loading: false,
          error: null,
        });
      } catch (err) {
        setState((prev) => ({
          ...prev,
          loading: false,
          error: getErrorMessage(err),
        }));
      }
    },
    []
  );

  return {
    ...state,
    fetchFeedback,
  };
}

