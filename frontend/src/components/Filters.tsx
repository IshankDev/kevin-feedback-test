import { type FeedbackFilters } from '../types/feedback';

interface FiltersProps {
  filters: FeedbackFilters;
  onFiltersChange: (filters: FeedbackFilters) => void;
  stats?: {
    source_counts: Record<string, number>;
    sentiment_counts: Record<string, number>;
  };
}

export function Filters({ filters, onFiltersChange, stats }: FiltersProps) {
  const handleChange = (key: keyof FeedbackFilters, value: string) => {
    onFiltersChange({
      ...filters,
      [key]: value || undefined,
    });
  };

  const clearFilters = () => {
    onFiltersChange({});
  };

  const hasActiveFilters = Object.keys(filters).length > 0;

  return (
    <div className="filters">
      <h3>Filters</h3>
      
      <div className="filter-group">
        <label>Source</label>
        <select
          value={filters.source || ''}
          onChange={(e) => handleChange('source', e.target.value)}
        >
          <option value="">All Sources</option>
          {stats?.source_counts && Object.keys(stats.source_counts).map((source) => (
            <option key={source} value={source}>
              {source} ({stats.source_counts[source]})
            </option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <label>Sentiment</label>
        <select
          value={filters.sentiment || ''}
          onChange={(e) => handleChange('sentiment', e.target.value)}
        >
          <option value="">All Sentiments</option>
          {stats?.sentiment_counts && Object.keys(stats.sentiment_counts).map((sentiment) => (
            <option key={sentiment} value={sentiment}>
              {sentiment} ({stats.sentiment_counts[sentiment]})
            </option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <label>Start Date</label>
        <input
          type="date"
          value={filters.start_date || ''}
          onChange={(e) => handleChange('start_date', e.target.value)}
        />
      </div>

      <div className="filter-group">
        <label>End Date</label>
        <input
          type="date"
          value={filters.end_date || ''}
          onChange={(e) => handleChange('end_date', e.target.value)}
        />
      </div>

      {hasActiveFilters && (
        <button onClick={clearFilters} className="clear-filters">
          Clear Filters
        </button>
      )}
    </div>
  );
}

