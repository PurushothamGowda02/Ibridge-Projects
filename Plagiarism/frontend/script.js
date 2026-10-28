const API_BASE = "http://localhost:5000/api";

const form = document.getElementById("checkForm");
const fileForm = document.getElementById("fileForm");
const summary = document.getElementById("summary");
const results = document.getElementById("results");
const fileUpload = document.getElementById("file_upload");
const fileName = document.querySelector(".file-name");
const refreshDbBtn = document.getElementById("refreshDb");
const databaseList = document.getElementById("databaseList");

// Tab switching functionality
document.querySelectorAll(".tab-button").forEach(button => {
  button.addEventListener("click", () => {
    const tabName = button.dataset.tab;
    
    // Update active button
    document.querySelectorAll(".tab-button").forEach(btn => btn.classList.remove("active"));
    button.classList.add("active");
    
    // Update active pane
    document.querySelectorAll(".tab-pane").forEach(pane => pane.classList.remove("active"));
    document.querySelector(`[data-pane="${tabName}"]`).classList.add("active");

    // Load database when database tab is clicked
    if (tabName === "database") {
      loadDatabase();
    }
  });
});

// Load database documents
async function loadDatabase() {
  databaseList.innerHTML = '<p class="loading">Loading documents...</p>';
  
  try {
    const response = await fetch(`${API_BASE}/documents`);
    const documents = await response.json();
    
    if (documents.length === 0) {
      databaseList.innerHTML = `
        <div class="empty-database">
          <p>⚠️ <strong>Database is empty!</strong></p>
          <p>The system can only detect plagiarism against documents already in the database.</p>
          <p><strong>How it works:</strong></p>
          <ol>
            <li>Submit your first document (becomes reference)</li>
            <li>Submit another document to compare against it</li>
            <li>System shows similarity percentage</li>
          </ol>
        </div>
      `;
      return;
    }
    
    databaseList.innerHTML = `
      <div class="db-stats">
        <strong>${documents.length}</strong> document${documents.length !== 1 ? 's' : ''} in database
      </div>
      ${documents.map(doc => `
        <div class="db-document">
          <div class="db-doc-header">
            <h4>${doc.title}</h4>
            <span class="db-doc-id">ID: ${doc.id}</span>
          </div>
          <div class="db-doc-meta">
            <span>👤 ${doc.author || 'Unknown'}</span>
            <span>📝 ${doc.text_length} characters</span>
            <span>📅 ${new Date(doc.created_at).toLocaleDateString()}</span>
          </div>
          ${doc.preview ? `<div class="db-doc-preview">${doc.preview}</div>` : ''}
        </div>
      `).join('')}
    `;
  } catch (error) {
    databaseList.innerHTML = `<p class="error">Error loading database: ${error.message}</p>`;
  }
}

// Refresh database button
refreshDbBtn.addEventListener("click", loadDatabase);

// Check API status on load
async function checkAPIStatus() {
  try {
    const response = await fetch(`${API_BASE}/health`);
    const data = await response.json();
    
    const statusEl = document.getElementById('api_status');
    if (statusEl && data.online_checking) {
      if (data.online_checking.google_api_configured) {
        statusEl.innerHTML = '✅ Google API configured - Online checking available';
        statusEl.style.color = '#2e7d32';
      } else {
        statusEl.innerHTML = '⚠️ Google API not configured - Using fallback (may not work). <a href="ONLINE_CHECKING_GUIDE.md" target="_blank">Setup Guide</a>';
        statusEl.style.color = '#ef6c00';
      }
    }
  } catch (error) {
    console.error('Failed to check API status:', error);
  }
}

// Check API status when page loads
checkAPIStatus();

// File upload display
fileUpload.addEventListener("change", (e) => {
  if (e.target.files.length > 0) {
    fileName.textContent = e.target.files[0].name;
    fileName.classList.add("show");
  } else {
    fileName.textContent = "";
    fileName.classList.remove("show");
  }
});

function riskClass(verdict) {
  if (verdict.includes("High")) return "risk-high";
  if (verdict.includes("Moderate")) return "risk-mid";
  return "risk-low";
}

function displayResults(data) {
  const dbCount = data.database_matches || 0;
  const onlineCount = data.online_matches || 0;
  
  summary.innerHTML = `
    <div class="summary-card">
      <div class="summary-item">
        <span class="summary-label">Document ID:</span>
        <span class="summary-value">${data.submitted_document_id}</span>
      </div>
      <div class="summary-item">
        <span class="summary-label">Overall Verdict:</span>
        <span class="summary-value ${riskClass(data.overall_verdict)}">${data.overall_verdict}</span>
      </div>
      <div class="summary-item">
        <span class="summary-label">Sources Checked:</span>
        <span class="summary-value">${dbCount} database + ${onlineCount} online</span>
      </div>
    </div>
  `;

  if (!data.matches || data.matches.length === 0) {
    results.innerHTML = "<p class='no-results'>✅ No documents in corpus yet. Your submission has been stored.</p>";
    return;
  }

  // Separate database and online matches
  const dbMatches = data.matches.filter(m => !m.source || m.source === 'database');
  const webMatches = data.matches.filter(m => m.source === 'web');

  // Filter and group matches
  const highRisk = data.matches.filter(m => m.final_score >= 75);
  const moderateRisk = data.matches.filter(m => m.final_score >= 45 && m.final_score < 75);
  const lowRisk = data.matches.filter(m => m.final_score >= 5 && m.final_score < 45);

  let output = '';

  // Helper function to render matches
  const renderMatches = (matches, categoryTitle, categoryClass) => {
    if (matches.length === 0) return '';
    
    return `
      <div class="match-category ${categoryClass}">
        <h3 class="category-title">${categoryTitle} (${matches.length})</h3>
        ${matches.map(match => renderMatch(match)).join('')}
      </div>
    `;
  };

  output += renderMatches(highRisk, '🔴 High Risk Matches', 'high-risk-category');
  output += renderMatches(moderateRisk, '🟡 Moderate Risk Matches', 'moderate-risk-category');
  output += renderMatches(lowRisk, '🟢 Low Risk Matches', 'low-risk-category');

  if (highRisk.length === 0 && moderateRisk.length === 0 && lowRisk.length === 0) {
    output = "<p class='no-results'>✅ No significant plagiarism detected. Your document appears to be original.</p>";
  }

  results.innerHTML = output;
}

function renderMatch(match) {
  const plagiarizedWords = match.plagiarized_words || {};
  const phrases = plagiarizedWords.matching_phrases || [];
  const shingles = plagiarizedWords.common_shingles || [];
  const words = plagiarizedWords.common_words || [];
  const isWebSource = match.source === 'web';
  
  let plagiarismDetails = '';
  
  // Show source type
  if (isWebSource) {
    plagiarismDetails += `
      <div class="source-badge web-source">
        🌐 Online Source
        ${match.url ? `<a href="${match.url}" target="_blank" class="source-link">View Source →</a>` : ''}
      </div>
    `;
  } else {
    plagiarismDetails += `
      <div class="source-badge db-source">
        💾 Database Document
      </div>
    `;
  }
  
  // Document preview or snippet
  if (match.snippet && isWebSource) {
    plagiarismDetails += `
      <div class="document-preview">
        <h5>📄 Search Result:</h5>
        <p class="preview-text">${match.snippet}</p>
      </div>
    `;
  } else if (match.document_preview) {
    plagiarismDetails += `
      <div class="document-preview">
        <h5>📄 Document Preview:</h5>
        <p class="preview-text">${match.document_preview}</p>
      </div>
    `;
  }

  // Matching context
  if (match.matching_context && match.final_score > 15) {
    plagiarismDetails += `
      <div class="matching-context">
        <h5>🎯 Matching Content:</h5>
        <p class="context-text">${match.matching_context}</p>
      </div>
    `;
  }
  
  // Only show phrases if there are any and score is high enough
  if (phrases.length > 0 && match.final_score > 15) {
    plagiarismDetails += `
      <div class="plagiarism-section">
        <h4>🔴 Matching Phrases${plagiarizedWords.total_matching_phrases > phrases.length ? ` (showing ${phrases.length} of ${plagiarizedWords.total_matching_phrases})` : ''}:</h4>
        <ul class="plagiarism-list">
          ${phrases.map(phrase => `<li class="plagiarized-phrase">"${phrase}"</li>`).join('')}
        </ul>
      </div>
    `;
  }
  
  // Only show shingles if score is moderate to high
  if (shingles.length > 0 && match.final_score > 25) {
    plagiarismDetails += `
      <div class="plagiarism-section">
        <h4>🟡 Common Sequences:</h4>
        <ul class="plagiarism-list">
          ${shingles.map(shingle => `<li class="plagiarized-shingle">"${shingle}"</li>`).join('')}
        </ul>
      </div>
    `;
  }
  
  // Only show common words if score is low (to show what's similar)
  if (words.length > 0 && match.final_score <= 25 && match.final_score > 5) {
    plagiarismDetails += `
      <div class="plagiarism-section">
        <h4>🟢 Common Keywords:</h4>
        <div class="word-cloud">
          ${words.map(word => `<span class="common-word">${word}</span>`).join(' ')}
        </div>
      </div>
    `;
  }
  
  return `
    <article class="match">
      <div class="match-header">
        <h3>${match.title}</h3>
        <p class="score ${riskClass(match.verdict)}">${match.final_score}%</p>
      </div>
      <div class="match-details">
        <span class="detail-badge tooltip" data-tooltip="Measures text similarity based on word importance and frequency">
          TF-IDF: ${match.tfidf_score}%
        </span>
        <span class="detail-badge tooltip" data-tooltip="Measures exact phrase overlap between documents">
          Jaccard: ${match.jaccard_score}%
        </span>
        <span class="verdict-badge ${riskClass(match.verdict)}">${match.verdict}</span>
      </div>
      ${plagiarismDetails}
    </article>
  `;
}

// Text form submission
form.addEventListener("submit", async (event) => {
  event.preventDefault();
  
  const checkOnline = document.getElementById("check_online").checked;
  
  if (checkOnline) {
    summary.innerHTML = "<p>🌐 Checking plagiarism against database AND online sources... This may take 30-60 seconds.</p>";
  } else {
    summary.innerHTML = "<p>Checking plagiarism against database...</p>";
  }
  
  results.innerHTML = "";

  const payload = {
    title: document.getElementById("title").value.trim(),
    author: document.getElementById("author").value.trim(),
    raw_text: document.getElementById("raw_text").value.trim(),
    check_online: checkOnline
  };

  try {
    const response = await fetch(`${API_BASE}/check`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();
    if (!response.ok) {
      summary.innerHTML = `<p class="risk-high">${data.error || "Failed to check plagiarism."}</p>`;
      return;
    }

    displayResults(data);
  } catch (error) {
    summary.innerHTML = `<p class="risk-high">Server error: ${error.message}</p>`;
  }
});

// File form submission
fileForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  
  const checkOnline = document.getElementById("check_online_file").checked;
  
  if (checkOnline) {
    summary.innerHTML = "<p>🌐 Processing file and checking against database AND online sources... This may take 30-60 seconds.</p>";
  } else {
    summary.innerHTML = "<p>Processing file and checking plagiarism against database...</p>";
  }
  
  results.innerHTML = "";

  const file = fileUpload.files[0];
  if (!file) {
    summary.innerHTML = '<p class="risk-high">Please select a file.</p>';
    return;
  }

  const formData = new FormData();
  formData.append("file", file);
  formData.append("title", document.getElementById("file_title").value.trim());
  formData.append("author", document.getElementById("file_author").value.trim());
  formData.append("check_online", checkOnline);

  try {
    const response = await fetch(`${API_BASE}/check-file`, {
      method: "POST",
      body: formData,
    });
    const data = await response.json();
    if (!response.ok) {
      summary.innerHTML = `<p class="risk-high">${data.error || "Failed to check plagiarism."}</p>`;
      return;
    }

    displayResults(data);
  } catch (error) {
    summary.innerHTML = `<p class="risk-high">Server error: ${error.message}</p>`;
  }
});

