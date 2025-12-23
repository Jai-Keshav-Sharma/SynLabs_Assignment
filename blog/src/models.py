from typing import TypedDict


class BlogState(TypedDict):
    """State schema for LangGraph workflow"""
    
    # From fetch_product
    product_title: str
    product_description: str
    
    # From normalize_keyword
    normalized_name: str
    product_category: str
    
    # From fetch_seo_keywords / generate_keywords
    seo_keywords: list
    
    # From search_product
    search_results: str
    
    # From generate_blog
    blog_title: str
    blog_content: str
    
    # From publish_blog
    publish_url: str