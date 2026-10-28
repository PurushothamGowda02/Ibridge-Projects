/**
 * Unseen Data Handler
 * Manages file upload and analysis of new datasets
 */

const API_BASE_URL = 'http://localhost:8000';

// Tab switching
document.querySelectorAll('.tab-button').forEach(button => {
    button.addEventListener('click', () => {
        const tabName = button.getAttribute('data-tab');
        
        // Remove active class from all buttons and contents
        document.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
        
        // Add active class to clicked button and corresponding content
        button.classList.add('active');
        document.getElementById(tabName + '-tab').classList.add('active');
    });
});

// File upload handler
document.getElementById('upload-button').addEventListener('click', async () => {
    const fileInput = document.getElementById('file-input');
    const file = fileInput.files[0];
    
    if (!file) {
        showUploadStatus('Please select a CSV file', 'error');
        return;
    }
    
    if (!file.name.endsWith('.csv')) {
        showUploadStatus('Please select a CSV file', 'error');
        return;
    }
    
    await uploadAndAnalyze(file);
});

// Allow drag and drop
const uploadContainer = document.querySelector('.upload-container');
uploadContainer.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadContainer.style.backgroundColor = '#f0f0f0';
});

uploadContainer.addEventListener('dragleave', () => {
    uploadContainer.style.backgroundColor = 'transparent';
});

uploadContainer.addEventListener('drop', async (e) => {
    e.preventDefault();
    uploadContainer.style.backgroundColor = 'transparent';
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        document.getElementById('file-input').files = files;
        await uploadAndAnalyze(files[0]);
    }
});

async function uploadAndAnalyze(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    showUploadStatus('Analyzing dataset...', 'loading');
    document.getElementById('upload-button').disabled = true;
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/rfm/analyze-unseen`, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Upload failed');
        }
        
        const result = await response.json();
        
        showUploadStatus(`✓ ${result.message}`, 'success');
        displayUnseenResults(result);
        
    } catch (error) {
        console.error('Upload error:', error);
        showUploadStatus(`✗ Error: ${error.message}`, 'error');
    } finally {
        document.getElementById('upload-button').disabled = false;
    }
}

function showUploadStatus(message, type) {
    const statusDiv = document.getElementById('upload-status');
    statusDiv.textContent = message;
    statusDiv.className = `upload-status ${type}`;
}

function displayUnseenResults(result) {
    const rfmData = result.rfm_data;
    const segmentSummary = result.segments_summary;
    const stats = result.stats;
    
    // Show results section
    document.getElementById('unseen-results').style.display = 'block';
    
    // Update summary cards
    document.getElementById('unseen-total-customers').textContent = stats.total_customers.toLocaleString();
    
    const topSegment = segmentSummary.reduce((max, current) => 
        current.count > max.count ? current : max
    );
    document.getElementById('unseen-top-segment').textContent = topSegment.segment;
    document.getElementById('unseen-avg-monetary').textContent = '£' + stats.avg_monetary.toFixed(2);
    
    // Render charts
    renderUnseenBarChart(segmentSummary);
    renderUnseenScatterPlot(rfmData);
    
    // Render table
    renderUnseenDataTable(rfmData);
}

let unseenBarChartInstance = null;

function renderUnseenBarChart(segmentSummary) {
    const canvasElement = document.getElementById('unseen-bar-chart');
    if (!canvasElement) {
        console.error('Unseen bar chart canvas not found');
        return;
    }
    
    const ctx = canvasElement.getContext('2d');
    
    const labels = segmentSummary.map(s => s.segment);
    const data = segmentSummary.map(s => s.count);
    
    const segmentColors = {
        'Champions': '#667eea',
        'Loyal Customers': '#764ba2',
        'Potential Loyalists': '#f093fb',
        'New Customers': '#4facfe',
        'At Risk': '#fa709a',
        'Lost': '#fee140',
        'Others': '#a8edea'
    };
    
    const colors = labels.map(label => segmentColors[label] || '#999');
    
    if (unseenBarChartInstance) {
        unseenBarChartInstance.destroy();
    }
    
    unseenBarChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Number of Customers',
                data: data,
                backgroundColor: colors,
                borderColor: colors,
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}

let unseenScatterChartInstance = null;

function renderUnseenScatterPlot(rfmData) {
    const canvasElement = document.getElementById('unseen-scatter-plot');
    if (!canvasElement) {
        console.error('Unseen scatter plot canvas not found');
        return;
    }
    
    const ctx = canvasElement.getContext('2d');
    
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
        pointHoverRadius: 7
    }));
    
    if (unseenScatterChartInstance) {
        unseenScatterChartInstance.destroy();
    }
    
    unseenScatterChartInstance = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
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
        }
    });
}

function renderUnseenDataTable(rfmData) {
    const tbody = document.querySelector('#unseen-rfm-table tbody');
    if (!tbody) {
        console.error('Unseen data table not found');
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
