"""One-time setup script for GitHub Pages"""
import os
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_USERNAME = "Jai-Keshav-Sharma"
REPO_NAME = "seo-blog-automation"
BRANCH = "main"


def get_file_sha(filepath):
    """Get the SHA of an existing file"""
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{filepath}"
    
    response = requests.get(
        url,
        headers={
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        },
        params={"ref": BRANCH}
    )
    
    if response.status_code == 200:
        return response.json().get("sha")
    return None


def create_or_update_file(filepath, content):
    """Create or update a file in GitHub repo"""
    encoded = base64.b64encode(content.encode()).decode()
    
    url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}/contents/{filepath}"
    
    # Check if file exists
    sha = get_file_sha(filepath)
    
    payload = {
        "message": f"Update {filepath}" if sha else f"Add {filepath}",
        "content": encoded,
        "branch": BRANCH
    }
    
    # Include SHA if file exists (for update)
    if sha:
        payload["sha"] = sha
    
    response = requests.put(
        url,
        headers={
            "Authorization": f"token {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json"
        },
        json=payload
    )
    
    if response.status_code in (200, 201):
        action = "Updated" if sha else "Created"
        print(f"✓ {action} {filepath}")
    else:
        print(f"✗ Error with {filepath}: {response.text}")


def main():
    print("Setting up GitHub Pages configuration...\n")
    
    # _config.yml
    config_yml = """title: SEO Blog Automation
description: Automated electronics deal blog posts
baseurl: "/seo-blog-automation"
url: "https://Jai-Keshav-Sharma.github.io"

theme: minima

markdown: kramdown
plugins:
  - jekyll-feed
  - jekyll-seo-tag

collections:
  posts:
    output: true
    permalink: /:year/:month/:day/:title/
"""
    create_or_update_file("_config.yml", config_yml)
    
    # index.md
    index_md = """---
layout: home
title: Home
---

# Latest Electronics Deals & Reviews

Automated blog posts about trending electronics products.
"""
    create_or_update_file("index.md", index_md)
    
    # .gitignore
    gitignore = """_site/
.sass-cache/
.jekyll-cache/
.jekyll-metadata
.env
*.pyc
__pycache__/
.venv/
"""
    create_or_update_file(".gitignore", gitignore)
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("1. Go to https://github.com/Jai-Keshav-Sharma/seo-blog-automation/settings/pages")
    print("2. Enable GitHub Pages:")
    print("   - Source: Deploy from a branch")
    print("   - Branch: main")
    print("   - Folder: / (root)")
    print("3. Wait 1-2 minutes for the site to build")
    print("4. Check https://Jai-Keshav-Sharma.github.io/seo-blog-automation/")
    print("5. Run: python main.py")


if __name__ == "__main__":
    main()