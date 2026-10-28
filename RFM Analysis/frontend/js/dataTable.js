/**
 * Data Table Component
 * Renders a table with all customer RFM data
 */

function renderDataTable(rfmData) {
    const tbody = document.querySelector('#rfm-table tbody');
    if (!tbody) {
        console.error('Data table not found');
        return;
    }
    
    tbody.innerHTML = '';
    
    rfmData.forEach(customer => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${customer.CustomerID}</td>
            <td>${customer.Recency}</td>
            <td>${customer.Frequency}</td>
            <td>£${customer.Monetary.toFixed(2)}</td>
            <td><strong>${customer.RFM_Score}</strong></td>
            <td><span class="segment-badge">${customer.Customer_Segment}</span></td>
        `;
        tbody.appendChild(row);
    });
}
