import React, { useState, useEffect } from 'react';
import './App.css';
import TrainingDataTab from './components/TrainingDataTab';
import UnseenDataTab from './components/UnseenDataTab';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [activeTab, setActiveTab] = useState('training');
  const [error, setError] = useState(null);

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <h1>RFM Analysis Dashboard</h1>
        <p>Customer Segmentation by Recency, Frequency, and Monetary Value</p>
      </header>

      {/* Error Banner */}
      {error && (
        <div className="error-banner">
          <span>{error}</span>
          <button onClick={() => setError(null)}>×</button>
        </div>
      )}

      {/* Tab Navigation */}
      <div className="tabs">
        <button
          className={`tab-button ${activeTab === 'training' ? 'active' : ''}`}
          onClick={() => setActiveTab('training')}
        >
          Training Data
        </button>
        <button
          className={`tab-button ${activeTab === 'unseen' ? 'active' : ''}`}
          onClick={() => setActiveTab('unseen')}
        >
          Unseen Data Upload
        </button>
      </div>

      {/* Tab Content */}
      <div className="tab-content">
        {activeTab === 'training' && (
          <TrainingDataTab apiBaseUrl={API_BASE_URL} onError={setError} />
        )}
        {activeTab === 'unseen' && (
          <UnseenDataTab apiBaseUrl={API_BASE_URL} onError={setError} />
        )}
      </div>
    </div>
  );
}

export default App;
