# 🔑 Google Custom Search API Setup Guide

## Why You Need This

To enable **online plagiarism checking**, you need a Google Custom Search API key. This allows the system to search the web reliably.

**Benefits:**
- ✅ Reliable web search
- ✅ Fast results (< 1 second per search)
- ✅ No blocking or rate limiting
- ✅ 100 FREE searches per day
- ✅ $5 per 1000 additional searches

## 📝 Step-by-Step Setup (10 minutes)

### Step 1: Get Google API Key

1. **Go to Google Cloud Console**
   ```
   https://console.cloud.google.com/
   ```

2. **Create a New Project** (if you don't have one)
   - Click "Select a project" → "New Project"
   - Name: "Plagiarism Detector"
   - Click "Create"

3. **Enable Custom Search API**
   - Go to: https://console.cloud.google.com/apis/library
   - Search for "Custom Search API"
   - Click on it
   - Click "Enable"

4. **Create API Key**
   - Go to: https://console.cloud.google.com/apis/credentials
   - Click "Create Credentials" → "API Key"
   - Copy your API key (looks like: `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`)
   - Click "Restrict Key" (recommended)
   - Under "API restrictions", select "Custom Search API"
   - Click "Save"

### Step 2: Create Search Engine

1. **Go to Programmable Search Engine**
   ```
   https://programmablesearchengine.google.com/
   ```

2. **Create New Search Engine**
   - Click "Add" or "Get Started"
   - Name: "Plagiarism Checker"

3. **Configure Search**
   - **Search the entire web**: Select "Search the entire web"
   - **Image search**: OFF
   - **Safe search**: ON (recommended)
   - Click "Create"

4. **Get Search Engine ID**
   - After creation, click on your search engine
   - Click "Setup" or "Control Panel"
   - Find "Search engine ID" (looks like: `0123456789abcdefg:xxxxxxxx`)
   - Copy this ID

### Step 3: Add to Your System

1. **Open the config file**
   ```
   backend/config.py
   ```

2. **Add your credentials**
   ```python
   # Google Custom Search API Configuration
   GOOGLE_API_KEY = "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"  # Your API key here
   GOOGLE_SEARCH_ENGINE_ID = "0123456789abcdefg:xxxxxxxx"  # Your Search Engine ID here
   ```

3. **Save the file**

4. **Restart the server**
   ```bash
   # Stop the current server (Ctrl+C)
   # Start again
   python backend/app.py
   ```

### Step 4: Test It!

1. **Open the frontend**
2. **Paste some text** (e.g., copy from Wikipedia)
3. **✅ Check "Check against online sources"**
4. **Click "Check Plagiarism"**
5. **Wait 20-30 seconds**
6. **See results** with links to online sources!

## 💰 Pricing

### Free Tier
- **100 searches per day** - FREE
- Perfect for testing and small-scale use
- Resets daily

### Paid Tier
- **$5 per 1000 searches**
- Only charged after 100 free searches
- Very affordable for production use

### Example Costs:
- **10 documents/day** (2 searches each) = 20 searches = FREE
- **100 documents/day** = 200 searches = $0.50/day = $15/month
- **1000 documents/day** = 2000 searches = $10/day = $300/month

## 🔒 Security Best Practices

### 1. Restrict Your API Key
```
In Google Cloud Console:
- Go to Credentials
- Click on your API key
- Under "API restrictions", select "Custom Search API"
- Under "Application restrictions", add your domain
- Click "Save"
```

### 2. Use Environment Variables (Optional)
```bash
# Windows
set GOOGLE_API_KEY=your_key_here
set GOOGLE_SEARCH_ENGINE_ID=your_id_here

# Linux/Mac
export GOOGLE_API_KEY=your_key_here
export GOOGLE_SEARCH_ENGINE_ID=your_id_here
```

### 3. Don't Commit API Keys to Git
```bash
# Add to .gitignore
echo "backend/config.py" >> .gitignore
```

## 🧪 Testing Your Setup

### Test 1: Check API Status
```bash
curl http://localhost:5000/api/health
```

Should return:
```json
{
  "status": "ok",
  "online_checking": {
    "google_api_configured": true,
    "method": "Google Custom Search API"
  }
}
```

### Test 2: Run Test Script
```bash
cd backend
python web_search.py
```

Should find online sources and show similarity scores.

### Test 3: Use the UI
1. Open frontend
2. Check the status message under the checkbox
3. Should say: "✅ Google API configured"

## ❌ Troubleshooting

### "API key not valid"
- Check if you copied the full API key
- Make sure Custom Search API is enabled
- Check if API key restrictions are correct

### "Search engine ID not found"
- Verify you copied the correct Search Engine ID
- Make sure the search engine is set to "Search the entire web"

### "Quota exceeded"
- You've used 100 free searches today
- Wait until tomorrow for reset
- Or enable billing for paid searches

### "No results found"
- API is working but no matches found
- Try with text copied from Wikipedia
- Check if search phrases are being extracted

## 🎯 Alternative: Without API Key

If you don't want to set up Google API, you can:

1. **Use Database Only**
   - Fast and reliable
   - Compare against your own documents
   - Build a reference library

2. **Manual Online Checking**
   - Copy suspicious phrases
   - Search Google manually
   - Add found sources to database

3. **Use Commercial APIs**
   - Copyscape: $0.03/search
   - Turnitin: Enterprise pricing
   - Quetext: $10/month

## 📚 Additional Resources

- **Google Custom Search API Docs**: https://developers.google.com/custom-search/v1/overview
- **Pricing Details**: https://developers.google.com/custom-search/v1/overview#pricing
- **API Key Best Practices**: https://cloud.google.com/docs/authentication/api-keys

## ✅ Summary

1. **Get API Key** from Google Cloud Console (5 min)
2. **Create Search Engine** on Programmable Search (3 min)
3. **Add to config.py** (1 min)
4. **Restart server** (1 min)
5. **Test it!** (1 min)

**Total Time: ~10 minutes**
**Cost: FREE (100 searches/day)**

Once set up, online plagiarism checking will work reliably and fast! 🚀
