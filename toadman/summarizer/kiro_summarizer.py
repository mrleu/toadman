import subprocess
from toadman.models import Article

def summarize_article(article: Article, timeout: int = 60) -> str:
    """
    Summarize an article using Kiro CLI.
    
    Args:
        article: The article to summarize
        timeout: Timeout in seconds for the Kiro CLI call
    
    Returns:
        The summary text from Kiro
    """
    prompt = f"""Summarize this news article in 3-5 bullet points, focusing on key technical details and impact:

Title: {article.title}
Source: {article.source}
URL: {article.url}

Content:
{article.content_snippet}

Provide a concise summary highlighting:
- Main announcement or development
- Key technical details
- Impact on developers/users
"""
    
    try:
        # Call kiro-cli chat with the prompt via stdin
        result = subprocess.run(
            ['kiro-cli', 'chat'],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Error: Kiro CLI returned code {result.returncode}\n{result.stderr}"
    
    except subprocess.TimeoutExpired:
        return "Error: Kiro CLI timed out"
    except FileNotFoundError:
        return "Error: kiro-cli not found. Please ensure Kiro CLI is installed."
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Test with a sample article
    from toadman.fetchers.rss_fetcher import fetch_rss_feeds
    
    articles = fetch_rss_feeds()
    if articles:
        print(f"Summarizing: {articles[0].title}\n")
        summary = summarize_article(articles[0])
        print(summary)
