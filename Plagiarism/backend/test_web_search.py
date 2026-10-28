"""Test web search functionality"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

# Test 1: Simple search
query = "machine learning artificial intelligence"
search_url = f"https://html.duckduckgo.com/html/?q={quote_plus(query)}"

print("Testing DuckDuckGo search...")
print(f"URL: {search_url}")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

try:
    response = requests.get(search_url, headers=headers, timeout=10)
    print(f"Status Code: {response.status_code}")
    print(f"Response Length: {len(response.text)}")
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try different selectors
        results1 = soup.find_all('div', class_='result')
        results2 = soup.find_all('div', class_='results_links')
        results3 = soup.find_all('a', class_='result__a')
        
        print(f"\nResults found:")
        print(f"  div.result: {len(results1)}")
        print(f"  div.results_links: {len(results2)}")
        print(f"  a.result__a: {len(results3)}")
        
        # Print first few divs to see structure
        print("\nFirst 3 result divs:")
        for i, result in enumerate(results1[:3]):
            print(f"\n--- Result {i+1} ---")
            print(result.prettify()[:500])
        
        # Try alternative: Google search (just to test)
        print("\n\nTrying alternative search method...")
        google_url = f"https://www.google.com/search?q={quote_plus(query)}"
        response2 = requests.get(google_url, headers=headers, timeout=10)
        print(f"Google Status: {response2.status_code}")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
