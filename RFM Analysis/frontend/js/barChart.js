/**
 * Bar Chart Component
 * Renders a Chart.js bar chart showing segment distribution
 */

let barChartInstance = null;

function renderBarChart(segmentSummary) {
    const canvasElement = document.getElementById('bar-chart');
    if (!canvasElement) {
        console.error('Bar chart canvas not found');
        return;
    }
    
    const ctx = canvasElement.getContext('2d');
    
    const labels = segmentSummary.map(s => s.segment);
    const data = segmentSummary.map(s => s.count);
    
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
    
    const colors = labels.map(label => segmentColors[label] || '#999');
    
    // Destroy existing chart if it exists
    if (barChartInstance) {
        barChartInstance.destroy();
    }
    
    barChartInstance = new Chart(ctx, {
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
