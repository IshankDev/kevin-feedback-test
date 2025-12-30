import { useState, useEffect } from 'react';
import { type Feedback, type FeedbackFilters } from '../types/feedback';
import { apiClient } from '../services/api';
import { FeedbackCard } from './FeedbackCard';
import { SearchBar } from './SearchBar';
import { Filters } from './Filters';
import { SummaryPanel } from './SummaryPanel';

export function FeedbackList() {
  const [feedback, setFeedback] = useState<Feedback[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [page, setPage] = useState(1);
  const [total, setTotal] = useState(0);
  const [filters, setFilters] = useState<FeedbackFilters>({});
  const [stats, setStats] = useState<any>(null);
  const [summary, setSummary] = useState<string | null>(null);
  const [summaryLoading, setSummaryLoading] = useState(false);

  const pageSize = 20;

  const loadFeedback = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiClient.getFeedback(page, pageSize, filters);
      setFeedback(response.items);
      setTotal(response.total);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load feedback');
    } finally {
      setLoading(false);
    }
  };

  const loadStats = async () => {
    try {
      const statsData = await apiClient.getStats();
      setStats(statsData);
    } catch (err) {
      console.error('Failed to load stats:', err);
    }
  };

  useEffect(() => {
    loadFeedback();
  }, [page, filters]);

  useEffect(() => {
    loadStats();
  }, []);

  const handleSearch = (query: string) => {
    setFilters({ ...filters, search: query });
    setPage(1);
  };

  const handleFiltersChange = (newFilters: FeedbackFilters) => {
    setFilters(newFilters);
    setPage(1);
  };

  const handleSummarize = async () => {
    setSummaryLoading(true);
    try {
      const response = await apiClient.summarizeFeedback({ filters });
      setSummary(response.summary);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate summary');
    } finally {
      setSummaryLoading(false);
    }
  };

  const totalPages = Math.ceil(total / pageSize);

  return (
    <div className="feedback-list-container">
      <div className="main-content">
        <div className="header-section">
          <h1>Customer Feedback Explorer</h1>
          <SearchBar onSearch={handleSearch} />
        </div>

        <div className="content-grid">
          <div className="filters-section">
            <Filters
              filters={filters}
              onFiltersChange={handleFiltersChange}
              stats={stats}
            />
            <button
              onClick={handleSummarize}
              disabled={summaryLoading}
              className="summarize-button"
            >
              {summaryLoading ? 'Generating...' : 'Generate Summary'}
            </button>
          </div>

          <div className="feedback-section">
            {error && <div className="error-message">{error}</div>}
            
            {loading ? (
              <div className="loading">Loading feedback...</div>
            ) : feedback.length === 0 ? (
              <div className="empty-state">No feedback found. Try adjusting your filters.</div>
            ) : (
              <>
                <div className="feedback-stats">
                  Showing {feedback.length} of {total} feedback items
                </div>
                <div className="feedback-items">
                  {feedback.map((item) => (
                    <FeedbackCard key={item.id} feedback={item} />
                  ))}
                </div>
                <div className="pagination">
                  <button
                    onClick={() => setPage((p) => Math.max(1, p - 1))}
                    disabled={page === 1}
                  >
                    Previous
                  </button>
                  <span>
                    Page {page} of {totalPages}
                  </span>
                  <button
                    onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
                    disabled={page >= totalPages}
                  >
                    Next
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      </div>

      {summary && (
        <SummaryPanel summary={summary} onClose={() => setSummary(null)} />
      )}
    </div>
  );
}

