import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Optional
from toadman.models import Article

CACHE_DIR = Path.home() / ".toadman" / "cache"
CACHE_FILE = CACHE_DIR / "articles_cache.json"
CACHE_EXPIRY_HOURS = 1

def save_cache(articles: List[Article]) -> None:
    """Save articles to cache."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    cache_data = {
        "timestamp": datetime.now().isoformat(),
        "articles": [
            {
                "title": a.title,
                "url": a.url,
                "published_date": a.published_date.isoformat() if a.published_date else None,
                "source": a.source,
                "content_snippet": a.content_snippet,
                "category": a.category,
            }
            for a in articles
        ]
    }
    
    CACHE_FILE.write_text(json.dumps(cache_data, indent=2), encoding='utf-8')

def load_cache() -> Optional[List[Article]]:
    """Load articles from cache if not expired."""
    if not CACHE_FILE.exists():
        return None
    
    try:
        cache_data = json.loads(CACHE_FILE.read_text(encoding='utf-8'))
        
        # Check if cache is expired
        cache_time = datetime.fromisoformat(cache_data["timestamp"])
        if datetime.now() - cache_time > timedelta(hours=CACHE_EXPIRY_HOURS):
            return None
        
        # Reconstruct articles
        articles = []
        for item in cache_data["articles"]:
            published = None
            if item["published_date"]:
                published = datetime.fromisoformat(item["published_date"])
            
            article = Article(
                title=item["title"],
                url=item["url"],
                published_date=published,
                source=item["source"],
                content_snippet=item["content_snippet"],
                category=item["category"],
            )
            articles.append(article)
        
        return articles
    
    except Exception:
        return None

def clear_cache() -> None:
    """Clear the cache file."""
    if CACHE_FILE.exists():
        CACHE_FILE.unlink()
