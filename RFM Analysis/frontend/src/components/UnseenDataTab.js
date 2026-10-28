import React, { useState } from 'react';
import axios from 'axios';
import BarChart from './BarChart';
import ScatterPlot from './ScatterPlot';
import DataTable from './DataTable';
import SummaryCards from './SummaryCards';

function UnseenDataTab({ apiBaseUrl, onError }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [results, setResults] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      onError('Please select a CSV file');
      return;
    }

    if (!file.name.endsWith('.csv')) {
      onError('Please select a CSV file');
      return;
    }

    try {
      setUploading(true);
      setUploadStatus('Analyzing dataset...');
      setResults(null); // Clear previous results

      console.log('Uploading file:', file.name, 'Size:', file.size, 'bytes');

      const formData = new FormData();
      formData.append('file', file);

      console.log('Sending request to:', `${apiBaseUrl}/api/rfm/analyze-unseen`);

      const response = await axios.post(
        `${apiBaseUrl}/api/rfm/analyze-unseen`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      );

      console.log('Upload successful:', response.data);

      setResults(response.data);
      setUploadStatus(`✓ ${response.data.message}`);
      onError(null);
    } catch (error) {
      console.error('Upload error:', error);
      const errorMsg = error.response?.data?.detail || error.message;
      onError(`Upload failed: ${errorMsg}`);
      setUploadStatus(`❌ Upload failed: ${errorMsg}`);
      setResults(null);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div>
      <div className="upload-section">
        <h2>Upload Unseen Dataset</h2>
        <p>Upload a CSV file with the same format as the training data to analyze new customers.</p>

        <div className="upload-container">
          <input
            type="file"
            accept=".csv"
            onChange={handleFileChange}
            disabled={uploading}
          />
          <button
            className="btn-primary"
            onClick={handleUpload}
            disabled={uploading}
          >
            {uploading ? 'Analyzing...' : 'Analyze Dataset'}
          </button>
        </div>

        {uploadStatus && (
          <div className={`upload-status ${uploadStatus.includes('✓') ? 'success' : uploadStatus.includes('Analyzing') ? 'loading' : 'error'}`}>
            {uploadStatus}
          </div>
        )}
      </div>

      {results && (
        <div>
          <SummaryCards rfmData={results.rfm_data} segmentSummary={results.segments_summary} />

          <div className="charts-section">
            <div className="chart-container">
              <h2>Segment Distribution (Unseen)</h2>
              <BarChart segmentSummary={results.segments_summary} />
            </div>

            <div className="chart-container">
              <h2>Recency vs Monetary (Unseen)</h2>
              <ScatterPlot rfmData={results.rfm_data} />
            </div>
          </div>

          <div className="table-section">
            <h2>Unseen Customer RFM Data</h2>
            <DataTable rfmData={results.rfm_data} />
          </div>
        </div>
      )}
    </div>
  );
}

export default UnseenDataTab;
