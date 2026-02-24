# Toadman

**Agentic news platform** - A terminal-based news aggregator for Claude Code, Codex, agentic development tools, and OpenClaw news.

## Features

- 📰 **RSS Feed Aggregation** - Fetches news from Anthropic, OpenAI, Claude Log, and OpenClaw
- 🔍 **Hacker News Integration** - Searches HN for agentic development discussions
- 🤖 **AI Summarization** - On-demand article summarization using Kiro CLI
- 🎨 **Rich TUI** - Beautiful terminal interface built with Textual
- 💾 **Smart Caching** - 1-hour cache to minimize API calls
- 📤 **Markdown Export** - Export articles and summaries to markdown
- ⚙️ **Configurable** - Customize RSS feeds and settings via config file

## Installation

```bash
# Clone the repository
git clone https://github.com/mrleu/toadman.git
cd toadman

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .
```

## Usage

```bash
# Launch Toadman
python -m toadman.cli

# Force refresh (ignore cache)
python -m toadman.cli --refresh
```

## Keyboard Shortcuts

- **↑/↓ or j/k** - Navigate articles
- **Enter** - Select article to view details
- **s** - Summarize selected article with Kiro
- **e** - Export articles to markdown
- **r** - Refresh articles (clear cache)
- **/** - Search articles
- **?** - Show help
- **q** - Quit

## Configuration

Edit `~/.toadman/config.toml` to customize:

```toml
[rss_feeds]
Anthropic = "https://www.anthropic.com/news/rss.xml"
OpenAI = "https://openai.com/blog/rss.xml"
"Claude Log" = "https://claudelog.com/feed.xml"
OpenClaw = "https://openclaw-ai.dev/feed.xml"

[hacker_news]
keywords = ["agentic", "Claude Code", "Codex", "OpenClaw"]
hits_per_keyword = 5

[cache]
expiry_hours = 1
```

## File Structure

```
~/.toadman/
├── cache/              # Cached articles
├── exports/            # Exported markdown files
└── config.toml         # Configuration file
```

## Requirements

- Python 3.9+
- Kiro CLI (for AI summarization)

## License

MIT
