import feedparser
import re
from src.config import RSS_FEED_URL
from src.models import BlogState


def fetch_product(state: BlogState) -> BlogState:
    """Node 1: Fetch latest product from RSS feed"""
    print("\n[NODE 1] Fetching latest product...")
    
    feed = feedparser.parse(RSS_FEED_URL)
    entry = feed.entries[0]
    title = entry.title
    description = re.sub("<.*?>", "", entry.get("summary", ""))
    
    print(f"Product: {title}")
    
    state["product_title"] = title
    state["product_description"] = description
    return state