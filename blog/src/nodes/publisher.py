import re
import base64
import requests
from datetime import datetime
from src.models import BlogState
from src.config import GITHUB_TOKEN, GITHUB_USERNAME, REPO_NAME, BRANCH, BLOG_PATH


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug"""
    text = text.lower()
    text = re.sub(r"\$+", " dollar ", text)
    text = re.sub(r"\+", " plus ", text)
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"\s+", "-", text)
    return text.strip("-")[:60]


def publish_blog(state: BlogState) -> BlogState:
    """Node 7: Publish to GitHub Pages"""
    print("\n[NODE 7] Publishing to GitHub...")
    
    date_prefix = datetime.utcnow().strftime("%Y-%m-%d")
    filename = f"{BLOG_PATH}/{date_prefix}-{slugify(state['blog_title'])}.md"
    
    content = f"""---
title: "{state['blog_title']}"
date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S +0000')}
---

{state['blog_content']}
"""
    
    encoded = base64.b64encode(content.encode()).decode()
    
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{filename}"
    
    response = requests.put(
        url,
        headers={
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        },
        json={
            "message": f"Add blog post: {state['blog_title']}",
            "content": encoded,
            "branch": BRANCH
        }
    )
    
    if response.status_code not in (200, 201):
        raise RuntimeError(response.text)
    
    slug = slugify(state['blog_title'])
    year, month, day = date_prefix.split("-")
    
    publish_url = f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/{year}/{month}/{day}/{slug}/"
    state["publish_url"] = publish_url
    
    print(f"Published: {publish_url}")
    return state