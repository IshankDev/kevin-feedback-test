/** Application constants. */

export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const DEFAULT_PAGE_SIZE = 20;
export const MAX_PAGE_SIZE = 100;

export const SENTIMENT_COLORS = {
  positive: '#28a745',
  negative: '#dc3545',
  neutral: '#6c757d',
} as const;

export const SOURCE_LABELS = {
  support_ticket: 'Support Ticket',
  survey: 'Survey',
  app_store: 'App Store',
} as const;

