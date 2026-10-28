# 🌐 Online Plagiarism Checking Guide

## ⚠️ Why Automated Online Checking is Disabled

Search engines (Google, Bing, DuckDuckGo) actively block automated searches to prevent:
- Web scraping
- Bot traffic
- API abuse
- Server overload

**Result**: Automated online checking returns 0 results even though sources exist.

## ✅ Solution: Manual Online Checking

### Method 1: Manual Search + Database Addition

**Step 1: Extract Key Phrases**
```
From your document, copy 2-3 unique sentences:
Example: "Machine learning is a method of data analysis that automates analytical model building"
```

**Step 2: Search Google**
```
1. Open Google.com
2. Paste the phrase in quotes: "Machine learning is a method of data analysis"
3. Press Enter
4. Review results
```

**Step 3: Add Sources to Database**
```
1. Copy text from found webpage
2. Go to your plagiarism system
3. Submit as new document
4. Now your document will be compared against it!
```

### Method 2: Use Google Custom Search API (Recommended for Production)

**Setup:**
1. Go to https://developers.google.com/custom-search
2. Create a Custom Search Engine
3. Get API key
4. Add to system configuration

**Benefits:**
- ✅ Reliable
- ✅ Fast
- ✅ No blocking
- ✅ 100 free searches/day

**Cost:**
- Free: 100 searches/day
- Paid: $5 per 1000 searches

### Method 3: Use Plagiarism APIs

**Commercial Options:**
1. **Copyscape API** - $0.03 per search
2. **Turnitin API** - Enterprise pricing
3. **Grammarly API** - Subscription based
4. **Quetext API** - $10/month

## 🔧 How to Enable Google Custom Search

### Step 1: Get API Key

```bash
1. Visit: https://console.cloud.google.com/
2. Create new project
3. Enable "Custom Search API"
4. Create credentials (API key)
5. Copy your API key
```

### Step 2: Create Search Engine

```bash
1. Visit: https://programmablesearchengine.google.com/
2. Click "Add"
3. Search the entire web: Select "Search the entire web"
4. Create
5. Copy your Search Engine ID
```

### Step 3: Update Configuration

Create `backend/config.py`:
```python
# Google Custom Search Configuration
GOOGLE_API_KEY = "your_api_key_here"
GOOGLE_SEARCH_ENGINE_ID = "your_search_engine_id_here"
```

### Step 4: Update web_search.py

```python
import requests

def search_google_api(query: str, api_key: str, cx: str) -> List[Dict]:
    """Search using Google Custom Search API"""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'key': api_key,
        'cx': cx,
        'q': query,
        'num': 3
    }
    
    response = requests.get(url, params=params)
    results = []
    
    if response.status_code == 200:
        data = response.json()
        for item in data.get('items', []):
            results.append({
                'title': item.get('title'),
                'url': item.get('link'),
                'snippet': item.get('snippet')
            })
    
    return results
```

## 📊 Current System Capabilities

### ✅ What Works Now:
- Database plagiarism detection (fast, accurate)
- File upload (PDF, DOCX, TXT)
- Document preview
- Matching phrases
- Risk categorization
- Duplicate prevention

### ❌ What Doesn't Work:
- Automated web search (blocked by search engines)
- Real-time online checking
- Internet source detection

### 🔄 Workaround:
1. **Build your reference library**
   - Add common source materials
   - Add textbook excerpts
   - Add previous assignments
   - Add Wikipedia articles

2. **Manual verification**
   - Copy suspicious phrases
   - Search Google manually
   - Add found sources to database

3. **Use the system for**
   - Comparing student submissions
   - Checking against your database
   - Finding internal plagiarism

## 💡 Best Practices

### For Teachers:

**Build a Reference Library:**
```
1. Add course materials
2. Add textbook chapters
3. Add common online sources
4. Add previous year submissions
```

**Check Students Against Each Other:**
```
1. Collect all submissions
2. Submit to system
3. System compares all vs all
4. Find who copied from whom
```

**Manual Online Check for Suspicious Cases:**
```
1. If score is suspiciously low
2. Copy unique phrases
3. Google search manually
4. Verify sources
```

### For Students:

**Check Your Work:**
```
1. Add your source materials to database
2. Submit your draft
3. See similarity with sources
4. Ensure proper paraphrasing
```

**Avoid Plagiarism:**
```
1. Write in your own words
2. Cite all sources
3. Use quotation marks for direct quotes
4. Check similarity before submission
```

## 🎯 Realistic Expectations

### What This System IS:
- ✅ Internal plagiarism detector
- ✅ Document comparison tool
- ✅ Similarity analyzer
- ✅ Database-based checker

### What This System IS NOT:
- ❌ Internet-wide plagiarism detector
- ❌ Turnitin replacement
- ❌ Real-time web crawler
- ❌ AI content detector

## 🚀 Future Solutions

### Option 1: Google Custom Search API
- **Cost**: $5 per 1000 searches
- **Reliability**: High
- **Setup**: 30 minutes
- **Recommended**: Yes

### Option 2: Commercial API
- **Cost**: $10-100/month
- **Reliability**: Very High
- **Setup**: 10 minutes
- **Recommended**: For production

### Option 3: Proxy Rotation
- **Cost**: $20-50/month
- **Reliability**: Medium
- **Setup**: Complex
- **Recommended**: No (against ToS)

### Option 4: Manual Process
- **Cost**: Free
- **Reliability**: High
- **Setup**: None
- **Recommended**: For small scale

## 📝 Summary

**Current Status:**
- ✅ Database checking: **Working perfectly**
- ❌ Online checking: **Disabled (search engines block bots)**

**Recommended Approach:**
1. Use database checking for primary detection
2. Build comprehensive reference library
3. Manual Google search for verification
4. Consider Google Custom Search API for production

**Bottom Line:**
The system works excellently for comparing documents against your database. For online checking, either use manual search or implement Google Custom Search API ($5/1000 searches).
