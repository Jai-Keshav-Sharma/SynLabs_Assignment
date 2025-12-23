import feedparser
import requests
import re
import os
import base64
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ---------------- CONFIG ----------------
RSS_FEED_URL = "https://www.dealnews.com/c142/Electronics/?rss=1"

APIFY_ACTOR_URL = (
    "https://api.apify.com/v2/acts/"
    "radeance~ubersuggest-scraper/"
    "run-sync-get-dataset-items"
)

APIFY_TOKEN = os.getenv("APIFY_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

GITHUB_USERNAME = "Jai-Keshav-Sharma"
REPO_NAME = "seo-blog-automation"
BRANCH = "main"
BLOG_PATH = "_posts"  # root of repo

# --------------------------------------


def fetch_latest_product():
    feed = feedparser.parse(RSS_FEED_URL)
    entry = feed.entries[0]
    title = entry.title
    description = re.sub("<.*?>", "", entry.get("summary", ""))
    return title, description


def normalize_seed_keyword(title):
    title = title.lower()
    # remove prices like $15, 54-cent, etc.
    title = re.sub(r"\$?\d+(-cent)?", "", title)

    # remove shipping text
    title = re.sub(r"shipping.*", "", title)


    brands = [
        "geagood", "sennheiser", "apple", "sony", "anker",
        "samsung", "hp", "lenovo", "dell"
    ]
    for brand in brands:
        title = title.replace(brand, "")

    title = re.sub(r"[^a-z\s]", "", title)
    title = re.sub(r"\s+", " ", title).strip()

    stopwords = {
    "with", "for", "and", "w",
    "cent", "shipping", "order", "first"
    }

    tokens = [t for t in title.split() if t not in stopwords]

    return " ".join(tokens[:5])


def fetch_seo_keywords(seed_keyword):
    payload = {
        "keyword": seed_keyword,
        "country": "us",
        "language": "en"
    }

    response = requests.post(
        APIFY_ACTOR_URL,
        params={"token": APIFY_TOKEN},
        json=payload,
        timeout=120
    )

    if response.status_code not in (200, 201):
        raise RuntimeError(response.text)

    items = response.json()
    keywords = []

    for item in items:
        for s in item.get("search", []):
            if s.get("keyword"):
                keywords.append(s["keyword"])

        for s in item.get("suggestions", []):
            if s.get("keyword"):
                keywords.append(s["keyword"])

    keywords = list(dict.fromkeys(keywords))

    if len(keywords) < 3:
        keywords = [
            f"best {seed_keyword}",
            f"{seed_keyword} price",
            f"{seed_keyword} review",
            f"buy {seed_keyword}"
        ]

    return keywords[:4]


def generate_blog(title, keywords):
    return f"""
Looking for a smart electronics upgrade? The {title} is gaining attention among buyers searching for **{keywords[0]}** thanks to its practical design and strong value.
...
""".strip()



def publish_to_github(title, blog_content):
    def slugify(text):
        text = text.lower()
        text = re.sub(r"\$+", " dollar ", text)
        text = re.sub(r"\+", " plus ", text)
        text = re.sub(r"[^a-z0-9\s-]", "", text)
        text = re.sub(r"\s+", "-", text)
        return text.strip("-")[:60]


    date_prefix = datetime.utcnow().strftime("%Y-%m-%d")
    filename = f"{BLOG_PATH}/{date_prefix}-{slugify(title)}.md"


    content = f"""---
title: "{title}"
date: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S +0000')}
---

{blog_content}
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
            "message": f"Add blog post: {title}",
            "content": encoded,
            "branch": BRANCH
        }
    )

    if response.status_code not in (200, 201):
        raise RuntimeError(response.text)

    slug = slugify(title)
    year, month, day = date_prefix.split("-")

    return f"https://{GITHUB_USERNAME}.github.io/{REPO_NAME}/{year}/{month}/{day}/{slug}/"



def main():
    print("\nFetching latest product...")
    title, _ = fetch_latest_product()
    print("Product:", title)

    seed = normalize_seed_keyword(title)
    print("Normalized seed keyword:", seed)

    print("\nFetching SEO keywords...")
    seo_keywords = fetch_seo_keywords(seed)
    print("SEO keywords:", seo_keywords)

    print("\nGenerating blog...")
    blog = generate_blog(title, seo_keywords)

    print("\nPublishing blog...")
    url = publish_to_github(title, blog)

    print("\n✅ Blog published successfully!")
    print("🔗 Live URL:", url)


if __name__ == "__main__":
    main()
