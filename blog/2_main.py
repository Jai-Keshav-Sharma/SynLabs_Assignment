import feedparser
import requests
import re
import json
from collections import Counter

# ---------------- CONFIG ----------------
RSS_FEED_URL = "https://www.dealnews.com/c142/Electronics/?rss=1"
APIFY_TOKEN = os.getenv("APIFY_TOKEN")
APIFY_ACTOR_URL = (
    "https://api.apify.com/v2/acts/radeance~ubersuggest-scraper/run-sync?token=apify_api_ND4L1CHmhdXQeaj1X5ugaUb1Cpj2dt0KAxpo"
)

# ---------------------------------------


def fetch_latest_product():
    feed = feedparser.parse(RSS_FEED_URL)
    entry = feed.entries[0]

    title = entry.title
    description = re.sub("<.*?>", "", entry.get("summary", ""))

    return title, description


def extract_seed_keyword(title):
    title = title.lower()
    title = re.sub(r"[^a-zA-Z0-9\s]", "", title)

    words = title.split()
    common_words = {"with", "and", "for", "the", "off", "deal", "sale"}

    keywords = [w for w in words if w not in common_words]
    seed = " ".join(keywords[:3])

    return seed


def fetch_seo_keywords(seed_keyword):
    url = (
        "https://api.apify.com/v2/acts/"
        "radeance~ubersuggest-scraper/"
        "run-sync-get-dataset-items"
    )

    payload = {
        "keyword": seed_keyword,
        "country": "us",
        "language": "en"
    }

    response = requests.post(
        url,
        params={"token": APIFY_TOKEN},
        json=payload,
        timeout=120
    )

    # ✅ Apify returns 200 OR 201 on success
    if response.status_code not in (200, 201):
        raise RuntimeError(
            f"Apify failed {response.status_code}: {response.text}"
        )

    items = response.json()

    if not isinstance(items, list) or len(items) == 0:
        raise RuntimeError("Empty dataset returned by Apify")

    keywords = []

    for item in items:
        # from "search"
        for s in item.get("search", []):
            kw = s.get("keyword")
            if kw:
                keywords.append(kw)

        # from "suggestions"
        for s in item.get("suggestions", []):
            kw = s.get("keyword")
            if kw:
                keywords.append(kw)

    # remove duplicates
    keywords = list(dict.fromkeys(keywords))

    # keep only SEO-friendly phrases
    keywords = [
        kw for kw in keywords
        if any(x in kw.lower() for x in ["best", "buy", "price", "review", "wireless", "lamp", "charger"])
    ]

    # guarantee 3–4 keywords
    if len(keywords) < 3:
        keywords = [
            f"best {seed_keyword}",
            f"{seed_keyword} price",
            f"{seed_keyword} review",
            f"buy {seed_keyword}"
        ]

    return keywords[:4]





def generate_blog(title, description, keywords):
    keyword_text = ", ".join(keywords)

    blog = f"""
{title}

Looking for the best electronics deals right now? The {title} is currently gaining attention among tech enthusiasts thanks to its impressive features and competitive pricing.

This product stands out for its performance, reliability, and overall value, making it a smart choice for anyone searching for {keywords[0]}. Whether you're upgrading your setup or buying for the first time, this deal offers a balance of quality and affordability.

Shoppers comparing options often look for {keywords[1]} and {keywords[2]}, and this product checks those boxes with ease. Its growing popularity also makes it one of the most searched items under {keywords[3]}.

If you’re planning a purchase soon, now is a great time to act while availability and pricing remain favorable. Deals like these don’t last long, especially in the fast-moving electronics market.
"""
    return blog.strip()


def main():
    print("\nFetching latest product from RSS...")
    title, description = fetch_latest_product()

    print("Product:", title)

    seed_keyword = extract_seed_keyword(title)
    print("Seed keyword:", seed_keyword)

    print("\nFetching SEO keywords...")
    seo_keywords = fetch_seo_keywords(seed_keyword)

    print("Selected SEO keywords:", seo_keywords)

    print("\nGenerating SEO blog post...\n")
    blog = generate_blog(title, description, seo_keywords)

    print(blog)


if __name__ == "__main__":
    main()
