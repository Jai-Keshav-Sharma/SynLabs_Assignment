import json
from langchain_core.messages import HumanMessage
from src.models import BlogState
from src.llm import get_llm
from src.prompts import get_normalize_prompt


def normalize_keyword(state: BlogState) -> BlogState:
    """Node 2: LLM extracts core product name + category"""
    print("\n[NODE 2] Normalizing keyword with LLM...")
    
    llm = get_llm()
    prompt = get_normalize_prompt(state["product_title"])
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    # Debug: print raw response
    print(f"Raw LLM response: {response.content}")
    
    try:
        result = json.loads(response.content)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Response content: {response.content}")
        # Fallback: extract manually
        result = {
            "name": state["product_title"].lower().split()[0],
            "category": "electronics"
        }
    
    state["normalized_name"] = result["name"]
    state["product_category"] = result["category"]
    
    print(f"Normalized: {result['name']} ({result['category']})")
    return state