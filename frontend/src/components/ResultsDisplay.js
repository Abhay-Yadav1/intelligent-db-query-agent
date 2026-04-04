import React from 'react';
import './ResultsDisplay.css';

function ResultsDisplay({ result, loading }) {
  if (loading) {
    return (
      <div className="results-container">
        <div className="loading">
          <div className="spinner"></div>
          <p>Processing your query...</p>
        </div>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="results-container">
        <div className="no-results">
          <p>💡 Ask a question to see results</p>
        </div>
      </div>
    );
  }

  const { question, sql, status, results, message, error } = result;

  return (
    <div className="results-container">
      <div className="result-section">
        <h3>📝 Question</h3>
        <p className="question-text">{question}</p>
      </div>

      <div className="result-section">
        <h3>🔍 Generated SQL</h3>
        <div className="sql-box">
          <code>{sql}</code>
          <button 
            className="copy-button"
            onClick={() => navigator.clipboard.writeText(sql)}
          >
            📋 Copy
          </button>
        </div>
      </div>

      <div className="result-section">
        <h3>📊 Status</h3>
        <span className={`status-badge ${status}`}>
          {status === 'success' ? '✅' : status === 'rejected' ? '❌' : '⚠️'} {status.toUpperCase()}
        </span>
      </div>

      {message && (
        <div className="result-section">
          <h3>💬 Message</h3>
          <p className="message-text">{message}</p>
        </div>
      )}

      {error && (
        <div className="result-section error-section">
          <h3>❌ Error</h3>
          <p className="error-text">{error}</p>
        </div>
      )}

      {results && results.length > 0 && (
        <div className="result-section">
          <h3>📋 Results ({results.length} rows)</h3>
          <div className="table-wrapper">
            <table className="results-table">
              <tbody>
                {results.map((row, index) => (
                  <tr key={index}>
                    {row.map((cell, cellIndex) => (
                      <td key={cellIndex}>{cell}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}

export default ResultsDisplay;