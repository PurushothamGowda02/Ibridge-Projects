import React from 'react';

function DataTable({ rfmData }) {
  return (
    <div className="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Customer ID</th>
            <th>Recency (days)</th>
            <th>Frequency</th>
            <th>Monetary (£)</th>
            <th>RFM Score</th>
            <th>Segment</th>
          </tr>
        </thead>
        <tbody>
          {rfmData.map((customer, index) => (
            <tr key={index}>
              <td>{customer.CustomerID}</td>
              <td>{customer.Recency}</td>
              <td>{customer.Frequency}</td>
              <td>£{customer.Monetary.toFixed(2)}</td>
              <td><strong>{customer.RFM_Score}</strong></td>
              <td>{customer.Customer_Segment}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default DataTable;
