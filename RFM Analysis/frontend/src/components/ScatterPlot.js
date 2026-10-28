import React from 'react';
import { Scatter } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LinearScale,
  PointElement,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(LinearScale, PointElement, Tooltip, Legend);

function ScatterPlot({ rfmData }) {
  const segmentColors = {
    'Champions': '#667eea',
    'Loyal Customers': '#764ba2',
    'Potential Loyalists': '#f093fb',
    'New Customers': '#4facfe',
    'At Risk': '#fa709a',
    'Lost': '#fee140',
    'Others': '#a8edea'
  };

  const segmentGroups = {};
  rfmData.forEach(customer => {
    const segment = customer.Customer_Segment;
    if (!segmentGroups[segment]) {
      segmentGroups[segment] = [];
    }
    segmentGroups[segment].push({
      x: customer.Recency,
      y: customer.Monetary,
      customerId: customer.CustomerID
    });
  });

  const datasets = Object.keys(segmentGroups).map(segment => ({
    label: segment,
    data: segmentGroups[segment],
    backgroundColor: segmentColors[segment] || '#999',
    borderColor: segmentColors[segment] || '#999',
    borderWidth: 1,
    pointRadius: 5,
    pointHoverRadius: 7,
  }));

  const chartData = {
    datasets,
  };

  const options = {
    responsive: true,
    maintainAspectRatio: true,
    plugins: {
      legend: {
        display: true,
        position: 'top',
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return `Customer: ${context.raw.customerId}, Recency: ${context.raw.x} days, Monetary: £${context.raw.y.toFixed(2)}`;
          }
        }
      }
    },
    scales: {
      x: {
        title: {
          display: true,
          text: 'Recency (days since last purchase)'
        },
        min: 0
      },
      y: {
        title: {
          display: true,
          text: 'Monetary Value (£)'
        },
        min: 0
      }
    }
  };

  return <Scatter data={chartData} options={options} />;
}

export default ScatterPlot;
