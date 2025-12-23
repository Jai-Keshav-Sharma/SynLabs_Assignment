"""Test Apify Ubersuggest scraper connection"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
APIFY_ACTOR_URL = (
    "https://api.apify.com/v2/acts/"
    "radeance~ubersuggest-scraper/"
    "run-sync-get-dataset-items"
)

print(f"Testing Apify with token: {APIFY_TOKEN[:10]}...")

# Test with a simple keyword
test_keyword = "airpods pro"

payload = {
    "keyword": test_keyword,
    "country": "us",
    "language": "en"
}

print(f"\nSearching for keyword: '{test_keyword}'")
print(f"Request URL: {APIFY_ACTOR_URL}")
print(f"Payload: {payload}")

try:
    response = requests.post(
        APIFY_ACTOR_URL,
        params={"token": APIFY_TOKEN},
        json=payload,
        timeout=120
    )
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code in (200, 201):
        items = response.json()
        print(f"Response Type: {type(items)}")
        print(f"Number of items returned: {len(items)}")
        
        if items:
            print(f"\nFirst item keys: {items[0].keys()}")
            print(f"\nFirst item structure:")
            
            for key, value in items[0].items():
                if isinstance(value, list):
                    print(f"  {key}: [{len(value)} items]")
                    if value and len(value) > 0:
                        print(f"    First element: {value[0]}")
                else:
                    print(f"  {key}: {value}")
            
            # Extract keywords
            keywords = []
            for item in items:
                for s in item.get("search", []):
                    if s.get("keyword"):
                        keywords.append(s["keyword"])
                for s in item.get("suggestions", []):
                    if s.get("keyword"):
                        keywords.append(s["keyword"])
            
            keywords = list(dict.fromkeys(keywords))
            
            print(f"\n✅ Extracted Keywords ({len(keywords)} total):")
            for i, kw in enumerate(keywords[:10], 1):
                print(f"  {i}. {kw}")
            
            if len(keywords) > 10:
                print(f"  ... and {len(keywords) - 10} more")
                
        else:
            print("\n⚠️  Empty response from Apify")
            
    else:
        print(f"\n❌ Error Response:")
        print(response.text[:500])
        
except requests.exceptions.Timeout:
    print("\n❌ Request timed out after 120 seconds")
except Exception as e:
    print(f"\n❌ Exception: {e}")
    import traceback
    traceback.print_exc()