/**
 * Summary Cards Component
 * Renders summary statistics: total customers, top segment, average monetary
 */

function renderSummaryCards(rfmData, segmentSummary) {
    console.log('renderSummaryCards called with', rfmData.length, 'customers');
    
    // Total customers
    const totalCustomers = rfmData.length;
    const totalEl = document.getElementById('total-customers');
    if (totalEl) {
        totalEl.textContent = totalCustomers.toLocaleString();
        console.log('Set total customers to:', totalCustomers);
    } else {
        console.error('total-customers element not found');
    }
    
    // Top segment (highest count)
    const topSegment = segmentSummary.reduce((max, current) => 
        current.count > max.count ? current : max
    );
    const topSegmentEl = document.getElementById('top-segment');
    if (topSegmentEl) {
        topSegmentEl.textContent = topSegment.segment;
        console.log('Set top segment to:', topSegment.segment);
    } else {
        console.error('top-segment element not found');
    }
    
    // Average monetary value
    const avgMonetary = rfmData.reduce((sum, customer) => sum + customer.Monetary, 0) / totalCustomers;
    const avgMonetaryEl = document.getElementById('avg-monetary');
    if (avgMonetaryEl) {
        avgMonetaryEl.textContent = '£' + avgMonetary.toFixed(2);
        console.log('Set avg monetary to:', avgMonetary.toFixed(2));
    } else {
        console.error('avg-monetary element not found');
    }
}
