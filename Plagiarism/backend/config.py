"""Configuration file for API keys and settings"""

# Google Custom Search API Configuration
# Get your API key from: https://console.cloud.google.com/
# Get your Search Engine ID from: https://programmablesearchengine.google.com/
GOOGLE_API_KEY = "AIzaSyBlTsZkvDpIq2grfCvYTtD8YJLggTsnfag"  # Add your API key here
GOOGLE_SEARCH_ENGINE_ID = "a16ad90a07bea41b7"  # Add your Search Engine ID here

# Alternative: Set as environment variables
import os
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', GOOGLE_API_KEY)
GOOGLE_SEARCH_ENGINE_ID = os.getenv('GOOGLE_SEARCH_ENGINE_ID', GOOGLE_SEARCH_ENGINE_ID)

# Check if API is configured
def is_google_api_configured():
    return bool(GOOGLE_API_KEY and GOOGLE_SEARCH_ENGINE_ID)
