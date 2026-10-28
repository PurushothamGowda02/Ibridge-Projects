"""Web search and content extraction for plagiarism detection"""
import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Tuple
from urllib.parse import quote_plus, urlparse
import time


def extract_key_phrases(text: str, num_phrases: int = 5) -> List[str]:
    """Extract key phrases from text for searching"""
    # Split into sentences
    sentences = re.split(r'[.!?]+', text)
    
    # Get longest sentences (likely to be unique)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 50]
    sentences.sort(key=len, reverse=True)
    
    # Take top phrases
    phrases = []
    for sentence in sentences[:num_phrases]:
        # Take first 10-15 words
        words = sentence.split()[:12]
        phrase = ' '.join(words)
        if len(phrase) > 30:  # Minimum length
            phrases.append(phrase)
    
    return phrases


def search_google_api(query: str, api_key: str, search_engine_id: str, num_results: int = 3) -> List[Dict]:
    """
    Search using Google Custom Search API (Reliable and Fast)
    Get API key from: https://console.cloud.google.com/
    Get Search Engine ID from: https://programmablesearchengine.google.com/
    """
    results = []
    
    try:
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': api_key,
            'cx': search_engine_id,
            'q': query,
            'num': num_results
        }
        
        print(f"    🔍 Searching Google API...")
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get('items', [])
            print(f"    ✅ Found {len(items)} results")
            
            for item in items:
                results.append({
                    'title': item.get('title', ''),
                    'url': item.get('link', ''),
                    'snippet': item.get('snippet', '')
                })
        elif response.status_code == 429:
            print(f"    ⚠️  API rate limit exceeded")
        else:
            print(f"    ❌ API error: {response.status_code}")
            error_data = response.json()
            if 'error' in error_data:
                print(f"       {error_data['error'].get('message', 'Unknown error')}")
        
    except Exception as e:
        print(f"    ❌ Google API error: {e}")
    
    return results


def search_bing(query: str, num_results: int = 3) -> List[Dict]:
    """
    Fallback: Search using Bing (Less reliable, may be blocked)
    """
    results = []
    
    try:
        search_url = f"https://www.bing.com/search?q={quote_plus(query)}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=3)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for result in soup.find_all('li', class_='b_algo')[:num_results]:
                title_elem = result.find('h2')
                link_elem = result.find('a')
                snippet_elem = result.find('p')
                
                if title_elem and link_elem:
                    title = title_elem.get_text(strip=True)
                    url = link_elem.get('href', '')
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ''
                    
                    if url and url.startswith('http'):
                        results.append({
                            'title': title,
                            'url': url,
                            'snippet': snippet
                        })
        
    except Exception as e:
        print(f"    ❌ Bing search error: {e}")
    
    return results


def fetch_webpage_content(url: str, max_length: int = 3000) -> str:
    """Fetch and extract text content from a webpage"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=3)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(['script', 'style', 'nav', 'footer', 'header', 'aside', 'form']):
                script.decompose()
            
            # Get text from main content areas
            main_content = soup.find('main') or soup.find('article') or soup.find('body')
            if main_content:
                text = main_content.get_text(separator=' ', strip=True)
            else:
                text = soup.get_text(separator=' ', strip=True)
            
            # Clean up whitespace
            text = re.sub(r'\s+', ' ', text)
            
            # Limit length
            if len(text) > max_length:
                text = text[:max_length]
            
            return text
        
    except Exception as e:
        print(f"    ⚠️  Fetch error for {url[:50]}: {e}")
    
    return ""


def check_online_plagiarism(text: str, num_searches: int = 2) -> List[Dict]:
    """
    Check if text appears online by searching key phrases
    Returns list of potential sources with similarity scores
    """
    from plagiarism_engine import final_similarity, find_plagiarized_words
    
    # Check if Google API is configured
    try:
        from config import GOOGLE_API_KEY, GOOGLE_SEARCH_ENGINE_ID, is_google_api_configured
        use_google_api = is_google_api_configured()
    except:
        use_google_api = False
        GOOGLE_API_KEY = ""
        GOOGLE_SEARCH_ENGINE_ID = ""
    
    results = []
    
    # Extract key phrases to search
    key_phrases = extract_key_phrases(text, num_phrases=num_searches)
    
    if not key_phrases:
        print("❌ No key phrases extracted")
        return results
    
    if use_google_api:
        print(f"🔍 Searching online using Google Custom Search API...")
    else:
        print(f"⚠️  Google API not configured, using fallback method (may not work)")
        print(f"   To enable: Add API key to backend/config.py")
    
    print(f"📝 Checking {len(key_phrases)} key phrases...")
    
    searched_urls = set()
    
    for i, phrase in enumerate(key_phrases):
        print(f"\n  📝 Phrase {i+1}: '{phrase[:60]}...'")
        
        # Try Google API first if configured
        if use_google_api:
            search_results = search_google_api(phrase, GOOGLE_API_KEY, GOOGLE_SEARCH_ENGINE_ID, num_results=2)
        else:
            # Fallback to Bing (may not work)
            print(f"    🔄 Trying Bing (fallback)...")
            search_results = search_bing(phrase, num_results=2)
        
        if not search_results:
            print(f"    ❌ No search results found")
            continue
        
        for search_result in search_results:
            url = search_result['url']
            
            # Skip if already checked
            if url in searched_urls:
                continue
            
            searched_urls.add(url)
            
            # Skip certain domains
            parsed = urlparse(url)
            skip_domains = ['youtube.com', 'facebook.com', 'twitter.com', 'instagram.com', 
                          'linkedin.com', 'reddit.com', 'pinterest.com', 'tiktok.com']
            if any(domain in parsed.netloc for domain in skip_domains):
                print(f"    ⏭️  Skipping {parsed.netloc}")
                continue
            
            print(f"    🌐 Checking: {url[:70]}...")
            
            # Fetch webpage content
            webpage_text = fetch_webpage_content(url, max_length=3000)
            
            if webpage_text and len(webpage_text) > 100:
                # Calculate similarity
                scores = final_similarity(text, webpage_text)
                
                print(f"       📊 Similarity: {scores['final_score']}%")
                
                # Only include if similarity is significant
                if scores['final_score'] > 15:
                    plagiarized = find_plagiarized_words(text, webpage_text)
                    
                    results.append({
                        'source': 'web',
                        'title': search_result['title'],
                        'url': url,
                        'final_score': scores['final_score'],
                        'tfidf_score': scores['tfidf_score'],
                        'jaccard_score': scores['jaccard_score'],
                        'verdict': get_verdict(scores['final_score']),
                        'plagiarized_words': plagiarized,
                        'snippet': search_result['snippet']
                    })
                    print(f"       ✅ Added to results (High similarity)")
                else:
                    print(f"       ⏭️  Skipped (Low similarity)")
            else:
                print(f"       ⚠️  Could not extract text")
            
            # Rate limiting
            time.sleep(0.5)
        
        # Rate limiting between searches
        time.sleep(1)
    
    # Sort by similarity score
    results.sort(key=lambda x: x['final_score'], reverse=True)
    
    print(f"\n✅ Found {len(results)} online sources with >15% similarity")
    
    return results[:3]


def get_verdict(score: float) -> str:
    """Get plagiarism verdict based on score"""
    if score >= 75:
        return "High plagiarism risk"
    if score >= 45:
        return "Moderate plagiarism risk"
    return "Low plagiarism risk"


if __name__ == "__main__":
    # Test
    test_text = """
    Machine learning is a method of data analysis that automates analytical model building. 
    It is a branch of artificial intelligence based on the idea that systems can learn from data, 
    identify patterns and make decisions with minimal human intervention.
    """
    
    print("="*80)
    print("Testing online plagiarism detection...")
    print("="*80)
    results = check_online_plagiarism(test_text, num_searches=2)
    
    print(f"\n{'='*80}")
    print(f"RESULTS: Found {len(results)} potential sources")
    print(f"{'='*80}")
    for result in results:
        print(f"\n  📄 Title: {result['title']}")
        print(f"  🔗 URL: {result['url']}")
        print(f"  📊 Similarity: {result['final_score']}%")
        print(f"  ⚖️  Verdict: {result['verdict']}")


