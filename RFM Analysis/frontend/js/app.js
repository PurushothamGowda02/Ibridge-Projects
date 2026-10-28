/**
 * Main Application Entry Point
 * Fetches data from the backend API and orchestrates all component rendering
 */

const API_BASE_URL = 'http://localhost:8000';

async function initializeApp() {
    try {
        console.log('Initializing app, fetching from:', API_BASE_URL);
        
        // Fetch data from all three endpoints in parallel
        const [rfmResponse, summaryResponse] = await Promise.all([
            fetch(`${API_BASE_URL}/api/rfm`),
            fetch(`${API_BASE_URL}/api/segments/summary`)
        ]);
        
        // Check for HTTP errors
        if (!rfmResponse.ok) {
            throw new Error(`RFM endpoint error: ${rfmResponse.status} ${rfmResponse.statusText}`);
        }
        if (!summaryResponse.ok) {
            throw new Error(`Summary endpoint error: ${summaryResponse.status} ${summaryResponse.statusText}`);
        }
        
        // Parse JSON responses
        const rfmData = await rfmResponse.json();
        const segmentSummary = await summaryResponse.json();
        
        console.log('Data loaded successfully:', rfmData.length, 'customers');
        console.log('Segment summary:', segmentSummary);
        
        // Wait a bit for DOM to be fully ready
        await new Promise(resolve => setTimeout(resolve, 100));
        
        // Render all components
        console.log('Rendering bar chart...');
        renderBarChart(segmentSummary);
        
        console.log('Rendering scatter plot...');
        renderScatterPlot(rfmData);
        
        console.log('Rendering data table...');
        renderDataTable(rfmData);
        
        console.log('Rendering summary cards...');
        renderSummaryCards(rfmData, segmentSummary);
        
        console.log('All components rendered successfully');
        
        // Hide error banner if it was shown
        hideErrorBanner();
        
    } catch (error) {
        console.error('Error loading data:', error);
        showErrorBanner(`Could not load data. Please ensure the backend server is running at ${API_BASE_URL}. Error: ${error.message}`);
    }
}

function showErrorBanner(message) {
    const banner = document.getElementById('error-banner');
    const messageEl = document.getElementById('error-message');
    if (banner && messageEl) {
        messageEl.textContent = message;
        banner.classList.add('visible');
    }
}

function hideErrorBanner() {
    const banner = document.getElementById('error-banner');
    if (banner) {
        banner.classList.remove('visible');
    }
}

// Initialize the app when the DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('DOM loaded, starting initialization...');
    initializeApp();
});
