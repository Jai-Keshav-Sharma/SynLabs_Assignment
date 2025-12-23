import json
import requests
import base64
from langchain_core.messages import HumanMessage
from src.models import BlogState
from src.llm import get_llm
from src.prompts import get_keyword_generation_prompt
from src.config import DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD


def fetch_keywords_dataforseo(keyword):
    """Fetch keyword suggestions from DataForSEO API"""
    if not DATAFORSEO_LOGIN or not DATAFORSEO_PASSWORD:
        print("DataForSEO credentials not configured")
        return []
    
    try:
        # Create base64 encoded credentials
        creds = base64.b64encode(
            f"{DATAFORSEO_LOGIN}:{DATAFORSEO_PASSWORD}".encode()
        ).decode()
        
        url = "https://api.dataforseo.com/v3/keywords_data/google_ads/keywords_for_keywords/live"
        
        headers = {
            "Authorization": f"Basic {creds}",
            "Content-Type": "application/json"
        }
        
        payload = [{
            "keywords": [keyword],
            "location_code": 2840,  # USA
            "language_code": "en",
            "include_seed_keyword": True,
            "limit": 10
        }]
        
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            tasks = data.get("tasks", [])
            
            if tasks and tasks[0].get("result"):
                results = tasks[0]["result"]
                keywords = []
                
                for item in results:
                    kw = item.get("keyword")
                    if kw:
                        keywords.append(kw)
                
                return keywords[:4]
        else:
            print(f"DataForSEO API error: {response.status_code}")
            print(f"Response: {response.text[:200]}")
        
        return []
        
    except Exception as e:
        print(f"DataForSEO exception: {e}")
        return []


def fetch_seo_keywords(state: BlogState) -> BlogState:
    """Node 3: Fetch SEO keywords from DataForSEO"""
    print("\n[NODE 3] Fetching SEO keywords from DataForSEO...")
    
    keywords = []
    
    # Try DataForSEO
    if DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD:
        print(f"Searching for: {state['normalized_name']}")
        keywords = fetch_keywords_dataforseo(state["normalized_name"])
        print(f"DataForSEO returned {len(keywords)} keywords")
        
        if keywords:
            print(f"Keywords: {keywords}")
    else:
        print("DataForSEO not configured, will use LLM generation")
    
    state["seo_keywords"] = keywords
    return state


def generate_keywords(state: BlogState) -> BlogState:
    """Node 4: LLM generates SEO keywords if < 3 from DataForSEO"""
    if len(state.get("seo_keywords", [])) >= 3:
        print("\n[NODE 4] Skipping LLM keyword generation (enough keywords)")
        return state
    
    print("\n[NODE 4] Generating SEO keywords with LLM...")
    
    llm = get_llm()
    prompt = get_keyword_generation_prompt(
        state["normalized_name"],
        state["product_category"],
        state["product_description"]
    )
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    print(f"Raw LLM response: {response.content}")
    
    try:
        result = json.loads(response.content)
        # Handle both array and object formats
        if isinstance(result, dict) and "keywords" in result:
            keywords = result["keywords"]
        elif isinstance(result, list):
            keywords = result
        else:
            keywords = []
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Response content: {response.content}")
        # Fallback keywords
        keywords = [
            f"best {state['normalized_name']}",
            f"{state['normalized_name']} price",
            f"{state['normalized_name']} review",
            f"buy {state['normalized_name']}"
        ]
    
    state["seo_keywords"] = keywords
    print(f"Generated keywords: {keywords}")
    return state