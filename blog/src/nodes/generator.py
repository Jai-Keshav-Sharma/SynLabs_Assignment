import json
from langchain_core.messages import HumanMessage
from src.models import BlogState
from src.llm import get_llm
from src.prompts import get_blog_generation_prompt


def generate_blog(state: BlogState) -> BlogState:
    """Node 6: LLM writes 200-word blog with SEO keywords"""
    print("\n[NODE 6] Generating blog with LLM...")
    
    llm = get_llm()
    prompt = get_blog_generation_prompt(
        state["product_title"],
        state["product_category"],
        state["product_description"],
        state["seo_keywords"],
        state["search_results"]
    )
    
    response = llm.invoke([HumanMessage(content=prompt)])
    
    # Debug: print raw response
    print(f"Raw LLM response: {response.content[:200]}...")
    
    try:
        blog = json.loads(response.content)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        # Fallback blog
        blog = {
            "title": f"{state['seo_keywords'][0]} - {state['product_title'][:50]}",
            "content": f"Discover the {state['product_title']}. {state['product_description'][:150]}"
        }
    
    state["blog_title"] = blog["title"]
    state["blog_content"] = blog["content"]
    
    print(f"Blog title: {blog['title']}")
    print(f"Blog length: {len(blog['content'].split())} words")
    return state