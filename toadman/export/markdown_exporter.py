from pathlib import Path
from datetime import datetime
from typing import List, Dict
from toadman.models import Article

def export_to_markdown(articles: List[Article], summaries: Dict[str, str] = None) -> Path:
    """
    Export articles and their summaries to a markdown file.
    
    Args:
        articles: List of articles to export
        summaries: Optional dict mapping article URLs to their summaries
    
    Returns:
        Path to the exported markdown file
    """
    if summaries is None:
        summaries = {}
    
    # Create exports directory
    export_dir = Path.home() / ".toadman" / "exports"
    export_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"toadman_export_{timestamp}.md"
    filepath = export_dir / filename
    
    # Build markdown content
    content = f"""# Toadman News Export
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

Total Articles: {len(articles)}

---

"""
    
    for article in articles:
        content += f"""## {article.title}

**Source:** {article.source}  
**Category:** {article.category}  
**Published:** {article.published_date or 'Unknown'}  
**URL:** [{article.url}]({article.url})

"""
        
        # Add summary if available
        if article.url in summaries:
            content += f"""### AI Summary

{summaries[article.url]}

"""
        
        # Add original content
        content += f"""### Content

{article.content_snippet}

---

"""
    
    # Write to file
    filepath.write_text(content, encoding='utf-8')
    
    return filepath

if __name__ == "__main__":
    # Test export
    from toadman.fetchers.rss_fetcher import fetch_rss_feeds
    
    articles = fetch_rss_feeds()[:5]
    filepath = export_to_markdown(articles)
    print(f"Exported to: {filepath}")
