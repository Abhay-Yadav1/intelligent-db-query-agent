import React, { useState } from 'react';
import QueryInput from './components/QueryInput';
import ResultsDisplay from './components/ResultsDisplay';
import { queryDatabase } from './services/api';
import './App.css';

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleQuery = async (question) => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await queryDatabase(question);
      setResult(data);
    } catch (err) {
      setError('Failed to process query. Make sure the backend is running.');
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🤖 Intelligent Database Query Agent</h1>
        <p>Ask questions about your database in natural language</p>
      </header>

      <main className="app-main">
        <QueryInput onSubmit={handleQuery} loading={loading} />
        
        {error && (
          <div className="error-banner">
            ⚠️ {error}
          </div>
        )}
        
        <ResultsDisplay result={result} loading={loading} />
      </main>

      <footer className="app-footer">
        <p>Built with ❤️ using LangGraph, FastAPI & React</p>
        <p>
          <a href="https://github.com/Abhay-Yadav1/intelligent-db-query-agent" target="_blank" rel="noopener noreferrer">
            View on GitHub
          </a>
        </p>
      </footer>
    </div>
  );
}

export default App;