import toml
from pathlib import Path
from typing import Dict, List

CONFIG_FILE = Path.home() / ".toadman" / "config.toml"

DEFAULT_CONFIG = {
    "rss_feeds": {
        "OpenAI": "https://openai.com/blog/rss.xml",
        "MyClaw Newsletter": "https://newsletter.myclaw.ai/rss/",
        "The Neuron": "https://rss.beehiiv.com/feeds/N4eCstxvgX.xml",
    },
    "hacker_news": {
        "keywords": ["agentic", "Claude Code", "Codex", "OpenClaw"],
        "hits_per_keyword": 5,
    },
    "cache": {
        "expiry_hours": 1,
    },
}

def load_config() -> Dict:
    """Load configuration from file or create default."""
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG
    
    try:
        return toml.load(CONFIG_FILE)
    except Exception:
        return DEFAULT_CONFIG

def save_config(config: Dict) -> None:
    """Save configuration to file."""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        toml.dump(config, f)

def get_rss_feeds() -> Dict[str, str]:
    """Get RSS feeds from config."""
    config = load_config()
    return config.get("rss_feeds", DEFAULT_CONFIG["rss_feeds"])

def get_hn_keywords() -> List[str]:
    """Get Hacker News keywords from config."""
    config = load_config()
    return config.get("hacker_news", {}).get("keywords", DEFAULT_CONFIG["hacker_news"]["keywords"])

def get_cache_expiry_hours() -> int:
    """Get cache expiry hours from config."""
    config = load_config()
    return config.get("cache", {}).get("expiry_hours", DEFAULT_CONFIG["cache"]["expiry_hours"])
