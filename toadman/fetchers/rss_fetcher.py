import feedparser
from datetime import datetime
from typing import List
from toadman.models import Article
from toadman.config import get_rss_feeds

def fetch_rss_feeds() -> List[Article]:
    """Fetch articles from all configured RSS feeds."""
    articles = []
    RSS_FEEDS = get_rss_feeds()
    
    for source, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:  # Limit to 10 most recent
                published = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6])
                
                content = ""
                if hasattr(entry, 'summary'):
                    content = entry.summary[:300]
                elif hasattr(entry, 'description'):
                    content = entry.description[:300]
                
                article = Article(
                    title=entry.get('title', 'No title'),
                    url=entry.get('link', ''),
                    published_date=published,
                    source=source,
                    content_snippet=content,
                    category=_categorize(source, entry.get('title', ''))
                )
                articles.append(article)
        except Exception as e:
            print(f"Error fetching {source}: {e}")
    
    return articles

def _categorize(source: str, title: str) -> str:
    """Categorize article based on source and title."""
    title_lower = title.lower()
    
    if 'claude code' in title_lower or source == "Claude Log":
        return "Claude Code"
    elif 'codex' in title_lower:
        return "Codex"
    elif 'openclaw' in title_lower or source == "OpenClaw":
        return "OpenClaw"
    elif source == "Anthropic":
        return "Claude Code"
    elif source == "OpenAI":
        return "Codex"
    else:
        return "Agentic Tools"

if __name__ == "__main__":
    articles = fetch_rss_feeds()
    print(f"Fetched {len(articles)} articles:")
    for article in articles[:5]:
        print(f"\n{article.category} | {article.source}")
        print(f"  {article.title}")
        print(f"  {article.url}")
        print(f"  {article.published_date}")
