import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

function BarChart({ segmentSummary }) {
  const segmentColors = {
    'Champions': '#667eea',
    'Loyal Customers': '#764ba2',
    'Potential Loyalists': '#f093fb',
    'New Customers': '#4facfe',
    'At Risk': '#fa709a',
    'Lost': '#fee140',
    'Others': '#a8edea'
  };

  const labels = segmentSummary.map(s => s.segment);
  const data = segmentSummary.map(s => s.count);
  const colors = labels.map(label => segmentColors[label] || '#999');

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Number of Customers',
        data,
        backgroundColor: colors,
        borderColor: colors,
        borderWidth: 1,
        borderRadius: 4,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        display: false,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 1,
        },
      },
    },
  };

  return <Bar data={chartData} options={options} />;
}

export default BarChart;
