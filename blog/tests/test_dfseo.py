"""Test DataForSEO API connection"""
import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

DATAFORSEO_LOGIN = os.getenv("DATAFORSEO_LOGIN")
DATAFORSEO_PASSWORD = os.getenv("DATAFORSEO_PASSWORD")

print("=" * 60)
print("Testing DataForSEO API")
print("=" * 60)

if not DATAFORSEO_LOGIN or not DATAFORSEO_PASSWORD:
    print("\n❌ ERROR: DataForSEO credentials not found in .env")
    print("\nPlease add to your .env file:")
    print("DATAFORSEO_LOGIN=your_login")
    print("DATAFORSEO_PASSWORD=your_password")
    print("\nSign up at: https://dataforseo.com/")
    exit(1)

print(f"\nLogin: {DATAFORSEO_LOGIN}")
print(f"Password: {'*' * len(DATAFORSEO_PASSWORD)}")

# Create base64 encoded credentials
creds = base64.b64encode(f"{DATAFORSEO_LOGIN}:{DATAFORSEO_PASSWORD}".encode()).decode()
print(f"\nEncoded credentials: {creds[:20]}...")

# Test 1: Check account status
print("\n" + "=" * 60)
print("Test 1: Checking Account Status")
print("=" * 60)

try:
    url = "https://api.dataforseo.com/v3/appendix/user_data"
    
    headers = {
        "Authorization": f"Basic {creds}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers, timeout=30)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        
        if "tasks" in data and data["tasks"]:
            task = data["tasks"][0]
            result = task.get("result", {})
            
            print("\n✅ Account Status:")
            print(f"  Login: {result.get('login')}")
            print(f"  Money: ${result.get('money', {}).get('balance', 0):.2f}")
            print(f"  Limit: {result.get('money', {}).get('limit', 0)} requests/day")
            print(f"  Used Today: {result.get('money', {}).get('daily_used', 0)}")
        else:
            print(f"\n⚠️  Unexpected response structure: {data}")
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
except Exception as e:
    print(f"\n❌ Exception: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Get keyword suggestions
print("\n" + "=" * 60)
print("Test 2: Getting Keyword Suggestions")
print("=" * 60)

test_keyword = "airpods pro"
print(f"Testing with keyword: '{test_keyword}'")

try:
    # Method 1: Keywords Suggestions
    url = "https://api.dataforseo.com/v3/keywords_data/google_ads/keywords_for_keywords/live"
    
    headers = {
        "Authorization": f"Basic {creds}",
        "Content-Type": "application/json"
    }
    
    payload = [{
        "keywords": [test_keyword],
        "location_code": 2840,  # USA
        "language_code": "en",
        "include_seed_keyword": True,
        "limit": 10
    }]
    
    print(f"\nRequest URL: {url}")
    print(f"Payload: {payload}")
    
    response = requests.post(url, headers=headers, json=payload, timeout=60)
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"Response keys: {data.keys()}")
        
        if "tasks" in data and data["tasks"]:
            task = data["tasks"][0]
            
            print(f"\nTask Status: {task.get('status_message')}")
            
            if task.get("result"):
                results = task["result"]
                
                print(f"\nFound {len(results)} keyword suggestions:")
                
                keywords = []
                for i, item in enumerate(results[:10], 1):
                    keyword = item.get("keyword", "N/A")
                    volume = item.get("search_volume", 0)
                    competition = item.get("competition", "N/A")
                    
                    print(f"\n  {i}. Keyword: {keyword}")
                    print(f"     Volume: {volume}")
                    print(f"     Competition: {competition}")
                    
                    keywords.append(keyword)
                
                print(f"\n✅ Extracted {len(keywords)} keywords:")
                for kw in keywords[:5]:
                    print(f"  - {kw}")
            else:
                print(f"\n⚠️  No results in task")
                print(f"Task data: {task}")
        else:
            print(f"\n⚠️  No tasks in response")
            print(f"Response: {data}")
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
except Exception as e:
    print(f"\n❌ Exception: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Search Volume
print("\n" + "=" * 60)
print("Test 3: Getting Search Volume")
print("=" * 60)

try:
    url = "https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live"
    
    headers = {
        "Authorization": f"Basic {creds}",
        "Content-Type": "application/json"
    }
    
    payload = [{
        "keywords": [test_keyword, "wireless earbuds", "best headphones"],
        "location_code": 2840,  # USA
        "language_code": "en"
    }]
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        
        if "tasks" in data and data["tasks"]:
            task = data["tasks"][0]
            
            if task.get("result"):
                results = task["result"]
                
                print(f"\n✅ Search Volume Results:")
                for item in results:
                    keyword = item.get("keyword", "N/A")
                    volume = item.get("search_volume", 0)
                    print(f"  '{keyword}': {volume:,} searches/month")
            else:
                print(f"\n⚠️  No results")
        else:
            print(f"\n⚠️  No tasks")
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        
except Exception as e:
    print(f"\n❌ Exception: {e}")

print("\n" + "=" * 60)
print("Test Complete")
print("=" * 60)