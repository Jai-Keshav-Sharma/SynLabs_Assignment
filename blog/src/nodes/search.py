from serpapi import GoogleSearch
from src.models import BlogState
from src.config import SERPAPI_KEY, SERP_NUM_RESULTS


def search_product(state: BlogState) -> BlogState:
    """Node 5: Search product reviews + specs via SerpAPI"""
    print("\n[NODE 5] Searching product info via SerpAPI...")
    
    product_name = state["normalized_name"]
    
    print(f"Searching for: {product_name}")
    
    results_text = ""
    
    # Search 1: Reviews
    try:
        search_params_reviews = {
            "q": f"{product_name} review",
            "api_key": SERPAPI_KEY,
            "num": SERP_NUM_RESULTS,
            "engine": "google"
        }
        
        search_reviews = GoogleSearch(search_params_reviews)
        review_results = search_reviews.get_dict()
        
        if "organic_results" in review_results:
            results_text += "=== Reviews ===\n"
            for result in review_results["organic_results"][:SERP_NUM_RESULTS]:
                snippet = result.get('snippet', '')
                if snippet:
                    results_text += f"- {snippet}\n"
            print(f"Found {len(review_results['organic_results'])} review results")
        else:
            print(f"No review results found")
            
    except Exception as e:
        print(f"Review search error: {e}")
    
    # Search 2: Specifications
    try:
        search_params_specs = {
            "q": f"{product_name} specifications",
            "api_key": SERPAPI_KEY,
            "num": SERP_NUM_RESULTS,
            "engine": "google"
        }
        
        search_specs = GoogleSearch(search_params_specs)
        spec_results = search_specs.get_dict()
        
        if "organic_results" in spec_results:
            results_text += "\n=== Specifications ===\n"
            for result in spec_results["organic_results"][:SERP_NUM_RESULTS]:
                snippet = result.get('snippet', '')
                if snippet:
                    results_text += f"- {snippet}\n"
            print(f"Found {len(spec_results['organic_results'])} spec results")
        else:
            print(f"No spec results found")
            
    except Exception as e:
        print(f"Spec search error: {e}")
    
    # Fallback: Use product description if no search results
    if len(results_text) < 50:
        print("⚠️  No search results found, using product description")
        results_text = f"=== Product Information ===\n{state['product_description']}"
    
    state["search_results"] = results_text
    print(f"Gathered {len(results_text)} chars of search data")
    return state