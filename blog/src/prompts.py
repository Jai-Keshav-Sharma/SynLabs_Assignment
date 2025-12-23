"""All LLM prompts for the workflow"""


def get_normalize_prompt(title: str) -> str:
    """Prompt for extracting product name and category"""
    return f"""You are a JSON-only assistant. Extract the core product name and product category from this title.

Title: {title}

Return ONLY a valid JSON object (no markdown, no explanation):
{{
    "name": "core product name (lowercase, include brand)",
    "category": "product category/type"
}}

NOTE: ALWAYS TRY TO KEEP THE PRODUCT NAME WITHIN 2 TO 4 WORDS

Example:
Title: "Apple AirPods Pro $199 with Free Shipping"
Output: {{"name": "apple airpods pro", "category": "wireless earbuds"}}"""


def get_keyword_generation_prompt(name: str, category: str, description: str) -> str:
    """Prompt for generating SEO keywords"""
    return f"""You are a JSON-only assistant. Generate 4 SEO-optimized keywords for this product.

Product Name: {name}
Category: {category}
Description: {description[:200]}

Return ONLY a valid JSON array (no markdown, no explanation):
["keyword1", "keyword2", "keyword3", "keyword4"]

Focus on: search volume, buyer intent, long-tail variations."""


def get_blog_generation_prompt(
    title: str,
    category: str,
    description: str,
    keywords: list,
    search_results: str
) -> str:
    """Prompt for generating blog post"""
    return f"""You are a JSON-only assistant. Write a 200-word SEO-optimized blog post about this product.

Product: {title}
Category: {category}
Description: {description}

SEO Keywords (MUST use all): {keywords}
Research Data:
{search_results}

Requirements:
1. Blog title MUST include one SEO keyword
2. All {len(keywords)} keywords must appear naturally in the body
3. Exactly 200 words
4. Structure: Introduction → Features/Benefits → Why it's trending → Conclusion
5. Engaging, conversational tone

Return ONLY valid JSON (no markdown, no explanation):
{{
    "title": "Blog title with SEO keyword",
    "content": "200-word blog content"
}}"""