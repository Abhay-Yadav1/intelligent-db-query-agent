import React, { useState } from 'react';
import './QueryInput.css';

function QueryInput({ onSubmit, loading }) {
  const [question, setQuestion] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (question.trim()) {
      onSubmit(question);
      setQuestion('');
    }
  };

  const exampleQuestions = [
    "Show all customers",
    "Count total orders",
    "Show customer names with order count",
    "Delete all customers"
  ];

  return (
    <div className="query-input-container">
      <form onSubmit={handleSubmit} className="query-form">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about your database..."
          className="query-input"
          disabled={loading}
        />
        <button 
          type="submit" 
          className="submit-button"
          disabled={loading || !question.trim()}
        >
          {loading ? '🔄 Processing...' : '🚀 Query'}
        </button>
      </form>
      
      <div className="example-questions">
        <p>Try these examples:</p>
        <div className="examples-grid">
          {exampleQuestions.map((example, index) => (
            <button
              key={index}
              onClick={() => setQuestion(example)}
              className="example-button"
              disabled={loading}
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default QueryInput;