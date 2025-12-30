interface SummaryPanelProps {
  summary: string;
  onClose: () => void;
}

export function SummaryPanel({ summary, onClose }: SummaryPanelProps) {
  return (
    <div className="summary-panel-overlay" onClick={onClose}>
      <div className="summary-panel" onClick={(e) => e.stopPropagation()}>
        <div className="summary-header">
          <h2>AI Summary</h2>
          <button onClick={onClose} className="close-button">×</button>
        </div>
        <div className="summary-content">
          {summary.split('\n').map((paragraph, i) => (
            <p key={i}>{paragraph}</p>
          ))}
        </div>
      </div>
    </div>
  );
}

