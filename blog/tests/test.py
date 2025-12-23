"""Test SerpAPI connection"""
import os
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")

print(f"Testing SerpAPI with key: {SERPAPI_KEY[:10]}...")

params = {
    "q": "airpods pro review",
    "api_key": SERPAPI_KEY,
    "num": 3,
    "engine": "google"
}

try:
    search = GoogleSearch(params)
    results = search.get_dict()
    
    print(f"\nStatus: Success")
    print(f"Keys in response: {results.keys()}")
    
    if "organic_results" in results:
        print(f"Found {len(results['organic_results'])} results")
        for i, result in enumerate(results["organic_results"][:3], 1):
            print(f"\n{i}. {result.get('title')}")
            print(f"   {result.get('snippet', '')[:100]}...")
    elif "error" in results:
        print(f"\nError: {results['error']}")
    else:
        print("\nNo organic results found")
        print(f"Full response: {results}")
        
except Exception as e:
    print(f"\nException: {e}")