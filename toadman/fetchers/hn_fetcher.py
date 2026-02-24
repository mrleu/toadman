import httpx
from datetime import datetime
from typing import List
from toadman.models import Article

HN_SEARCH_API = "https://hn.algolia.com/api/v1/search"
KEYWORDS = ["agentic", "Claude Code", "Codex", "OpenClaw"]

def fetch_hn_articles() -> List[Article]:
    """Fetch articles from Hacker News using Algolia search API."""
    articles = []
    
    for keyword in KEYWORDS:
        try:
            params = {
                "query": keyword,
                "tags": "story",
                "hitsPerPage": 5,
            }
            
            response = httpx.get(HN_SEARCH_API, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            for hit in data.get("hits", []):
                published = None
                if hit.get("created_at"):
                    published = datetime.fromisoformat(hit["created_at"].replace("Z", "+00:00"))
                
                article = Article(
                    title=hit.get("title", "No title"),
                    url=hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}",
                    published_date=published,
                    source="Hacker News",
                    content_snippet=hit.get("story_text", "")[:300],
                    category="Hacker News"
                )
                articles.append(article)
        except Exception as e:
            print(f"Error fetching HN for '{keyword}': {e}")
    
    # Remove duplicates by URL
    seen = set()
    unique_articles = []
    for article in articles:
        if article.url not in seen:
            seen.add(article.url)
            unique_articles.append(article)
    
    return unique_articles

if __name__ == "__main__":
    articles = fetch_hn_articles()
    print(f"Fetched {len(articles)} unique HN articles:")
    for article in articles[:5]:
        print(f"\n{article.source}")
        print(f"  {article.title}")
        print(f"  {article.url}")
        print(f"  {article.published_date}")
