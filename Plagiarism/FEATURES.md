# Plagiarism Detection System - Features Guide

## ✅ All Improvements Implemented

### 1. 🚫 Duplicate Prevention
- **Automatic Detection**: System checks for existing documents with same title (case-insensitive)
- **Smart Update**: If document exists, it updates instead of creating duplicate
- **Database Cleanup**: Removed 12 duplicate documents from database
- **API Endpoint**: `/api/cleanup-duplicates` for manual cleanup

### 2. 📄 Document Preview
- **Preview Snippet**: Shows first 200 characters of matched document
- **Matching Context**: Displays the context around plagiarized phrases
- **Visual Indicators**: 📄 for preview, 🎯 for matching content

### 3. 💡 Tooltips & Explanations
- **TF-IDF Tooltip**: "Measures text similarity based on word importance and frequency"
- **Jaccard Tooltip**: "Measures exact phrase overlap between documents"
- **Hover to Learn**: Hover over any metric badge to see explanation

### 4. 🗑️ Database Cleanup
- **Utility Script**: `backend/db_utils.py` for database management
- **Statistics**: Shows total documents and duplicate count
- **Safe Removal**: Keeps oldest document, removes duplicates
- **Cascade Delete**: Properly removes related comparisons

### 5. 📊 Better Grouping
- **Risk Categories**: 
  - 🔴 High Risk (≥75%)
  - 🟡 Moderate Risk (45-74%)
  - 🟢 Low Risk (5-44%)
- **Category Headers**: Clear visual separation
- **Smart Display**: Only shows relevant information per category

## 🎨 UI Improvements

### Summary Card
- Beautiful gradient header
- Shows: Document ID, Overall Verdict, Documents Checked
- Color-coded verdicts

### Match Display
- **High Risk**: Shows phrases + sequences + context
- **Moderate Risk**: Shows phrases + context
- **Low Risk**: Shows common keywords only
- **Insignificant (<5%)**: Hidden completely

### Tooltips
- Hover over TF-IDF or Jaccard badges
- Dark theme with smooth animation
- Positioned above the badge

## 🔧 Technical Details

### Backend Changes
1. **plagiarism_engine.py**:
   - Added `get_text_snippet()` for previews
   - Added `find_matching_context()` for phrase context
   - Updated `top_matches()` to prevent duplicates
   - Reduced noise: 4-word minimum phrases, more stop words

2. **app.py**:
   - Check for existing documents before insert
   - Update instead of duplicate
   - Exclude same-title documents from corpus
   - New `/api/cleanup-duplicates` endpoint

3. **db_utils.py** (NEW):
   - `remove_duplicate_documents()` - Clean database
   - `get_document_stats()` - Database statistics

### Frontend Changes
1. **script.js**:
   - New `displayResults()` with grouping
   - New `renderMatch()` for individual matches
   - Smart filtering by risk level
   - Preview and context display

2. **styles.css**:
   - Summary card styling
   - Category headers with colors
   - Tooltip implementation
   - Document preview boxes
   - Matching context highlighting

## 📝 Usage Examples

### Check for Duplicates
```bash
python backend/db_utils.py
```

### API Cleanup
```bash
curl -X POST http://localhost:5000/api/cleanup-duplicates
```

### Submit Document
- Text input or file upload
- System automatically checks for duplicates
- Updates existing document if title matches

## 🎯 Result Interpretation

### High Similarity (75%+)
- **Red Alert**: Likely plagiarism
- Shows: Exact matching phrases, sequences, context
- Action: Review and rewrite

### Moderate Similarity (45-74%)
- **Yellow Warning**: Possible plagiarism
- Shows: Matching phrases and context
- Action: Check citations and paraphrasing

### Low Similarity (5-44%)
- **Green OK**: Similar topics
- Shows: Common keywords only
- Action: Normal similarity for same subject

### Very Low (<5%)
- **Hidden**: Not shown in results
- Considered insignificant

## 🚀 Performance Optimizations

1. **Reduced Data**: 
   - 5 phrases (was 10)
   - 3 sequences (was 10)
   - 10 keywords (was 20)

2. **Smart Filtering**:
   - 60+ stop words
   - 4-word minimum phrases
   - Score-based display logic

3. **Database Efficiency**:
   - Case-insensitive title matching
   - Indexed queries
   - Cascade deletes

## 📱 Responsive Design
- Mobile-friendly tooltips
- Flexible grid layouts
- Touch-friendly badges
- Readable on all devices
