/**
 * Scatter Plot Component
 * Renders a Chart.js scatter plot with Recency vs Monetary, colored by segment
 */

let scatterChartInstance = null;

function renderScatterPlot(rfmData) {
    const canvasElement = document.getElementById('scatter-plot');
    if (!canvasElement) {
        console.error('Scatter plot canvas not found');
        return;
    }
    
    const ctx = canvasElement.getContext('2d');
    
    // Define colors for each segment
    const segmentColors = {
        'Champions': '#667eea',
        'Loyal Customers': '#764ba2',
        'Potential Loyalists': '#f093fb',
        'New Customers': '#4facfe',
        'At Risk': '#fa709a',
        'Lost': '#fee140',
        'Others': '#a8edea'
    };
    
    // Group data by segment
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
    
    // Create datasets for each segment
    const datasets = Object.keys(segmentGroups).map(segment => ({
        label: segment,
        data: segmentGroups[segment],
        backgroundColor: segmentColors[segment] || '#999',
        borderColor: segmentColors[segment] || '#999',
        borderWidth: 1,
        pointRadius: 5,
        pointHoverRadius: 7
    }));
    
    // Destroy existing chart if it exists
    if (scatterChartInstance) {
        scatterChartInstance.destroy();
    }
    
    scatterChartInstance = new Chart(ctx, {
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
