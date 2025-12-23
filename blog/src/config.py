import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

# DataForSEO (replaces Apify)
DATAFORSEO_LOGIN = os.getenv("DATAFORSEO_LOGIN")
DATAFORSEO_PASSWORD = os.getenv("DATAFORSEO_PASSWORD")

# LLM Provider: "openai" or "groq"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")

# RSS Feed
RSS_FEED_URL = "https://www.dealnews.com/c142/Electronics/?rss=1"

# GitHub
GITHUB_USERNAME = "Jai-Keshav-Sharma"
REPO_NAME = "seo-blog-automation"
BRANCH = "main"
BLOG_PATH = "_posts"

# SerpAPI
SERP_NUM_RESULTS = 3