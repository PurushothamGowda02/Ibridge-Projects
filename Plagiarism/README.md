# Plagiarism Detection System (BCA Final Year Project)

A comprehensive full-stack plagiarism detection system with **online source checking** capabilities.

## 🌟 Key Features

### Core Detection
- ✅ **Multi-Algorithm Detection**: TF-IDF, Jaccard Similarity, Word Overlap
- ✅ **Phrase Matching**: Detects 3-20 word exact matches
- ✅ **Smart Scoring**: Weighted combination for accurate results
- ✅ **Duplicate Prevention**: Automatic deduplication of documents

### 🌐 Online Plagiarism Detection (NEW!)
- ✅ **Google Custom Search API**: Reliable web search integration
- ✅ **Content Extraction**: Fetches and analyzes web pages
- ✅ **Source Links**: Direct links to original sources
- ✅ **Real-time Checking**: Finds plagiarism from Google, Wikipedia, etc.
- ⚡ **Optional Feature**: Unchecked by default for fast performance
- 🆓 **Free Tier**: 100 searches per day, then $5 per 1000 searches

### 📊 Advanced Features
- ✅ **Document Preview**: See snippets of matched content
- ✅ **Matching Context**: Highlights plagiarized phrases
- ✅ **Risk Categorization**: High/Moderate/Low risk grouping
- ✅ **Database Viewer**: Browse stored documents
- ✅ **File Upload**: Support for TXT, PDF, DOC, DOCX
- ✅ **Tooltips**: Explanations for all metrics

## Tech Stack

- **Backend**: Flask (Python 3.13)
- **Database**: SQLite
- **Detection**: TF-IDF, Jaccard, Word Overlap algorithms
- **Web Search**: Google Custom Search API (requires API key)
- **Content Extraction**: BeautifulSoup4
- **Frontend**: HTML5, CSS3, Vanilla JavaScript

## Project Structure

```text
Plagiarism/
├── backend/
│   ├── app.py                    # Flask API server
│   ├── database.py               # SQLite database management
│   ├── plagiarism_engine.py     # Core detection algorithms
│   ├── web_search.py             # Online plagiarism detection
│   ├── config.py                 # API configuration (Google API keys)
│   ├── db_utils.py               # Database utilities
│   ├── requirements.txt          # Python dependencies
│   ├── test_plagiarism.py        # Algorithm tests
│   ├── test_real_plagiarism.py   # Real-world tests
│   ├── test_performance.py       # Performance benchmarks
│   ├── check_db.py               # Database viewer
│   └── data/
│       └── plagiarism.db         # SQLite database
├── frontend/
│   ├── index.html                # Main UI
│   ├── styles.css                # Styling
│   └── script.js                 # Frontend logic
├── docs/
│   ├── BCA_Final_Year_Project_Report_Plagiarism_Detection.docx
│   └── images/                   # Diagrams and charts
├── README.md                     # This file
├── HOW_IT_WORKS.md              # User guide
├── PLAGIARISM_ALGORITHM.md      # Technical documentation
├── FEATURES.md                   # Feature list
├── GOOGLE_API_SETUP.md          # Google API setup guide (10 minutes)
├── ONLINE_CHECKING_GUIDE.md     # Online checking guide
└── SOLUTION_SUMMARY.md          # Quick reference

```

## 🚀 Setup and Run

### Prerequisites
- Python 3.13 or higher
- pip (Python package manager)
- Modern web browser

### Installation

1. **Clone or download the project**
   ```bash
   cd Plagiarism
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate virtual environment**
   - Windows (PowerShell):
     ```powershell
     .\.venv\Scripts\Activate.ps1
     ```
   - Windows (CMD):
     ```cmd
     .venv\Scripts\activate.bat
     ```
   - Linux/Mac:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```

5. **Run the backend server**
   ```bash
   python backend/app.py
   ```
   Server will start at `http://localhost:5000`

6. **Open the frontend**
   - Open `frontend/index.html` in your web browser
   - Or navigate to `http://localhost:5000` (if serving static files)

7. **[Optional] Configure Google API for Online Checking**
   - See `GOOGLE_API_SETUP.md` for detailed instructions (10 minutes)
   - Get free API key from Google Cloud Console
   - 100 free searches per day
   - Without API key: Database-only checking works perfectly

## 📖 Usage Guide

### Basic Plagiarism Check (Database Only - Fast!)

1. **Submit Reference Documents**
   - Go to "Text Input" tab
   - Enter title and paste content
   - **Leave "Check against online sources" UNCHECKED** ⚡
   - Click "Check Plagiarism"
   - Document is stored in database
   - **Results in < 1 second**

2. **Check for Plagiarism**
   - Submit another document
   - System compares against stored documents
   - View similarity scores and matching phrases
   - **Fast and reliable**

### 🌐 Online Plagiarism Check (Requires Google API Key)

**Setup Required**: Follow `GOOGLE_API_SETUP.md` to configure Google Custom Search API (10 minutes, free)

1. **Enable Online Checking**
   - Go to "Text Input" tab
   - ✅ **Check "Check against online sources"**
   - Paste your document
   - Click "Check Plagiarism"

2. **Wait for Results** (20-30 seconds)
   - System searches the web for key phrases
   - Fetches and analyzes matching web pages
   - Shows results with source links

3. **Review Results**
   - 💾 Database matches (your documents)
   - 🌐 Online matches (web sources)
   - Click "View Source →" to see original

**Note**: Without API key, online checking will fail with 403 errors. Database checking works perfectly without any API key.

### File Upload

1. **Go to "Upload File" tab**
2. **Select file** (.txt, .pdf, .doc, .docx)
3. **Enter title and author**
4. **Click "Check Plagiarism"**
5. **System extracts text and checks for plagiarism**

### View Database

1. **Click "View Database" tab**
2. **See all stored documents**
3. **View previews and metadata**
4. **Click "🔄 Refresh" to update**

## 🎯 API Endpoints

### Health Check
```http
GET /api/health
```
Returns server status

### List Documents
```http
GET /api/documents
```
Returns all documents with previews

### Add Document
```http
POST /api/documents
Content-Type: application/json

{
  "title": "Document Title",
  "author": "Author Name",
  "raw_text": "Document content..."
}
```

### Check Plagiarism
```http
POST /api/check
Content-Type: application/json

{
  "title": "Document Title",
  "author": "Author Name",
  "raw_text": "Document content...",
  "check_online": true  // Optional: enable online checking
}
```

### Check File
```http
POST /api/check-file
Content-Type: multipart/form-data

file: [file upload]
title: "Document Title"
author: "Author Name"
```

### Get Report
```http
GET /api/reports/<doc_id>
```
Returns comparison report for a document

### Cleanup Duplicates
```http
POST /api/cleanup-duplicates
```
Removes duplicate documents from database

## 🧪 Testing

### Run Algorithm Tests
```bash
python backend/test_plagiarism.py
```

### Run Real-World Tests
```bash
python backend/test_real_plagiarism.py
```

### Check Database
```bash
python backend/check_db.py
```

### Test Online Detection
```bash
# Note: Requires Google API key configured in backend/config.py
python backend/web_search.py
```

### Test Performance
```bash
python backend/test_performance.py
```

## 📊 Detection Algorithms

### 1. TF-IDF Cosine Similarity (50% weight)
- Measures text similarity based on word importance
- Uses 1-3 word n-grams
- Best for detecting similar vocabulary

### 2. Jaccard Similarity (30% weight)
- Measures exact phrase overlap
- Uses 3, 4, and 5-word shingles
- Best for detecting copy-paste plagiarism

### 3. Word Overlap (20% weight)
- Calculates ratio of common words
- Helps detect topic similarity
- Best for paraphrased content

### Final Score
```
Final Score = (0.5 × TF-IDF) + (0.3 × Jaccard) + (0.2 × Word Overlap)
```

## 🎨 Verdict Thresholds

| Score | Verdict | Color | Meaning |
|-------|---------|-------|---------|
| ≥ 75% | High Risk | 🔴 Red | Likely plagiarism |
| 45-74% | Moderate Risk | 🟡 Orange | Possible plagiarism |
| 5-44% | Low Risk | 🟢 Green | Similar topics |
| < 5% | Original | ✅ Green | No plagiarism |

## 🌐 Online Detection Details

### How It Works
1. **Extracts 2-3 key phrases** from your document (most unique sentences)
2. **Searches Google** using Custom Search API
3. **Fetches top 2 results** per phrase
4. **Downloads webpage content** (up to 3000 characters)
5. **Analyzes similarity** using same algorithms as database checking
6. **Returns matches** with source links and snippets

### Requirements
- **Google Custom Search API Key** (free tier: 100 searches/day)
- **Search Engine ID** (created in Programmable Search Engine)
- **Setup Time**: ~10 minutes (see `GOOGLE_API_SETUP.md`)

### Performance
- **Speed**: 20-30 seconds (due to web requests and rate limiting)
- **Accuracy**: Same as database checking (TF-IDF + Jaccard + Word Overlap)
- **Coverage**: Checks 4-6 web sources per document
- **Cost**: Free for first 100 searches/day, then $5 per 1000 searches

### Limitations
- Takes 20-30 seconds (vs <1 second for database only)
- Requires API key configuration
- Limited to 100 free searches per day
- May not find all sources (depends on search results)
- Some websites may block content extraction

### Best Practices
- **Use database checking first** (fast and reliable)
- **Enable online checking** only for suspicious documents
- **Review source links manually** for verification
- **Combine with manual research** for thorough checking
- **Monitor API usage** to stay within free tier

## 🔧 Configuration

### Database Location
```python
# backend/database.py
DB_PATH = BASE_DIR / "data" / "plagiarism.db"
```

### File Upload Settings
```python
# backend/app.py
UPLOAD_FOLDER = 'backend/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
```

### Detection Parameters
```python
# backend/plagiarism_engine.py
min_phrase_length = 3    # Minimum words in phrase
max_phrase_length = 20   # Maximum words in phrase
shingle_sizes = [3, 4, 5]  # Word sequence lengths
```

### Online Search Settings
```python
# backend/web_search.py
num_searches = 2         # Number of phrases to search
num_results = 2          # Results per search
max_content_length = 3000  # Max webpage text length
timeout = 5              # Request timeout in seconds
```

### Google API Configuration
```python
# backend/config.py
GOOGLE_API_KEY = ""              # Add your API key here
GOOGLE_SEARCH_ENGINE_ID = ""     # Add your Search Engine ID here
```

See `GOOGLE_API_SETUP.md` for detailed setup instructions.

## 📚 Documentation

- **[README.md](README.md)** - Complete setup and usage guide (this file)
- **[GOOGLE_API_SETUP.md](GOOGLE_API_SETUP.md)** - Google API setup guide (10 minutes)
- **[ONLINE_CHECKING_GUIDE.md](ONLINE_CHECKING_GUIDE.md)** - Online checking guide
- **[HOW_IT_WORKS.md](HOW_IT_WORKS.md)** - Complete user guide
- **[PLAGIARISM_ALGORITHM.md](PLAGIARISM_ALGORITHM.md)** - Technical details
- **[FEATURES.md](FEATURES.md)** - Feature list and improvements
- **[SOLUTION_SUMMARY.md](SOLUTION_SUMMARY.md)** - Quick reference

## 🎓 Use Cases

### For Teachers
- Check student assignments against each other
- Detect copying between students
- Build reference library of sources
- Track plagiarism over time

### For Students
- Check your work before submission
- Ensure proper paraphrasing
- Avoid accidental plagiarism
- Verify citations

### For Researchers
- Check paper originality
- Find similar published work
- Detect self-plagiarism
- Verify proper attribution

## ⚠️ Important Notes

### What It CAN Detect
✅ Copy-paste plagiarism  
✅ Minor word changes  
✅ Sentence reordering  
✅ Online sources (with online check enabled)  
✅ Similar vocabulary usage  

### What It CANNOT Detect
❌ Heavy paraphrasing with different words  
❌ Translated plagiarism  
❌ Idea plagiarism (same concept, different words)  
❌ Structural plagiarism  
❌ AI-generated content (without training)  

### Ethical Use
- Use as ONE tool among many
- Always review results manually
- Consider context and citations
- Respect privacy and data protection
- Follow academic integrity policies

## 🚀 Future Enhancements

- [ ] Semantic similarity using BERT/Word2Vec
- [ ] Citation detection and exclusion
- [ ] Multi-language support
- [ ] Structural analysis
- [ ] AI-generated content detection
- [ ] Batch processing
- [ ] Export reports as PDF
- [ ] User authentication
- [ ] Faculty dashboard
- [ ] API rate limiting and caching
- [ ] Improved Google API error handling
- [ ] Alternative search providers (Bing API, etc.)

## 🐛 Troubleshooting

### Server won't start
```bash
# Check if port 5000 is in use
netstat -ano | findstr :5000

# Kill process if needed
taskkill /F /PID <process_id>
```

### Database errors
```bash
# Clean and rebuild database
python backend/db_utils.py
```

### Online check not working
- **Check if API key is configured** in `backend/config.py`
- **Follow setup guide**: `GOOGLE_API_SETUP.md`
- **Enable Custom Search API** in Google Cloud Console
- **Link billing account** (required even for free tier)
- **Wait 2-5 minutes** for changes to propagate
- **Check server logs** for specific error messages
- **Alternative**: Use database-only checking (works perfectly)

### Low similarity scores
- Ensure documents are in database
- **For online checking**: Configure Google API key
- Check document length (min 100 words)
- Verify text extraction from files
- **Tip**: Database checking is fast and reliable for stored documents

### Slow performance
- **Uncheck "Check against online sources"** for fast results (<1 second)
- Online checking takes 20-30 seconds (normal)
- Database-only checking is very fast
- Check `test_performance.py` to benchmark your system

## 📄 License

This project is created for educational purposes as a BCA Final Year Project.

## 👥 Contributors

- BCA Final Year Students
- Project Guide: [Name]
- Institution: [College Name]

## 📞 Support

For issues or questions:
1. Check documentation files
2. Review test scripts
3. Check database with `check_db.py`
4. Verify algorithm with test files

## 🎉 Acknowledgments

- Flask framework
- scikit-learn library
- BeautifulSoup4
- Google Custom Search API
- Open source community

---

**Note**: This system is designed for educational purposes. Always combine automated detection with human review for final plagiarism decisions.

## 🔑 Quick Start Summary

1. **Install**: `pip install -r backend/requirements.txt`
2. **Run**: `python backend/app.py`
3. **Open**: `frontend/index.html`
4. **Use**: Submit documents and check plagiarism (fast, database-only)
5. **Optional**: Configure Google API for online checking (see `GOOGLE_API_SETUP.md`)

**Default Mode**: Fast database checking (<1 second)  
**Optional Mode**: Online checking with Google API (20-30 seconds, requires setup)

