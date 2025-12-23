from langgraph.graph import StateGraph, END
from src.models import BlogState
from src.nodes import (
    fetch_product,
    normalize_keyword,
    fetch_seo_keywords,
    generate_keywords,
    search_product,
    generate_blog,
    publish_blog,
)


def create_workflow():
    """Create LangGraph workflow"""
    workflow = StateGraph(BlogState)
    
    # Add nodes
    workflow.add_node("fetch_product", fetch_product)
    workflow.add_node("normalize_keyword", normalize_keyword)
    workflow.add_node("fetch_seo_keywords", fetch_seo_keywords)
    workflow.add_node("generate_keywords", generate_keywords)
    workflow.add_node("search_product", search_product)
    workflow.add_node("generate_blog", generate_blog)
    workflow.add_node("publish_blog", publish_blog)
    
    # Define edges (linear flow)
    workflow.set_entry_point("fetch_product")
    workflow.add_edge("fetch_product", "normalize_keyword")
    workflow.add_edge("normalize_keyword", "fetch_seo_keywords")
    workflow.add_edge("fetch_seo_keywords", "generate_keywords")
    workflow.add_edge("generate_keywords", "search_product")
    workflow.add_edge("search_product", "generate_blog")
    workflow.add_edge("generate_blog", "publish_blog")
    workflow.add_edge("publish_blog", END)
    
    return workflow.compile()