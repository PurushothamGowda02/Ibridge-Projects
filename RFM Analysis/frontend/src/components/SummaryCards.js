import React from 'react';

function SummaryCards({ rfmData, segmentSummary }) {
  const totalCustomers = rfmData.length;
  const topSegment = segmentSummary.reduce((max, current) =>
    current.count > max.count ? current : max
  );
  const avgMonetary = rfmData.reduce((sum, customer) => sum + customer.Monetary, 0) / totalCustomers;

  return (
    <section className="summary-cards">
      <div className="card">
        <h3>Total Customers</h3>
        <p className="card-value">{totalCustomers.toLocaleString()}</p>
      </div>
      <div className="card">
        <h3>Top Segment</h3>
        <p className="card-value">{topSegment.segment}</p>
      </div>
      <div className="card">
        <h3>Average Spend</h3>
        <p className="card-value">£{avgMonetary.toFixed(2)}</p>
      </div>
    </section>
  );
}

export default SummaryCards;
