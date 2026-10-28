import React, { useState, useEffect } from 'react';
import axios from 'axios';
import BarChart from './BarChart';
import ScatterPlot from './ScatterPlot';
import DataTable from './DataTable';
import SummaryCards from './SummaryCards';

function TrainingDataTab({ apiBaseUrl, onError }) {
  const [rfmData, setRfmData] = useState([]);
  const [segmentSummary, setSegmentSummary] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [rfmRes, summaryRes] = await Promise.all([
        axios.get(`${apiBaseUrl}/api/rfm`),
        axios.get(`${apiBaseUrl}/api/segments/summary`)
      ]);

      setRfmData(rfmRes.data);
      setSegmentSummary(summaryRes.data);
      onError(null);
    } catch (error) {
      onError(`Failed to load training data: ${error.message}`);
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
        <p>Loading training data...</p>
      </div>
    );
  }

  return (
    <div>
      <SummaryCards rfmData={rfmData} segmentSummary={segmentSummary} />

      <div className="charts-section">
        <div className="chart-container">
          <h2>Segment Distribution</h2>
          <BarChart segmentSummary={segmentSummary} />
        </div>

        <div className="chart-container">
          <h2>Recency vs Monetary Value</h2>
          <ScatterPlot rfmData={rfmData} />
        </div>
      </div>

      <div className="table-section">
        <h2>Customer RFM Data</h2>
        <DataTable rfmData={rfmData} />
      </div>
    </div>
  );
}

export default TrainingDataTab;
