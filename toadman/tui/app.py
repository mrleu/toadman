from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal, VerticalScroll
from textual.widgets import Header, Footer, Static, ListView, ListItem, Label, LoadingIndicator
from textual.binding import Binding
from textual.reactive import reactive
from textual.message import Message
from typing import List, Optional, Dict
from datetime import datetime
from toadman.models import Article
from toadman.fetchers.rss_fetcher import fetch_rss_feeds
from toadman.fetchers.hn_fetcher import fetch_hn_articles
from toadman.summarizer.kiro_summarizer import summarize_article
from toadman.export.markdown_exporter import export_to_markdown
from toadman.cache import load_cache, save_cache, clear_cache

class CategoryItem(Static):
    """A clickable category item."""
    
    class CategorySelected(Message):
        def __init__(self, category: str):
            super().__init__()
            self.category = category
    
    def __init__(self, category_name: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category_name = category_name
        self.selected = False
    
    def on_mount(self) -> None:
        self.update(f"  {self.category_name}")
    
    def on_click(self) -> None:
        self.post_message(self.CategorySelected(self.category_name))

class ArticleItem(ListItem):
    """A list item for an article."""
    
    def __init__(self, article: Article):
        label = Label(f"🐸 {article.title[:60]}...")
        super().__init__(label)
        self.article = article

class ArticleDetail(Static):
    """Article detail view."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.article = None
    
    def show_article(self, article: Article):
        self.article = article
        content = f"""[bold]{article.title}[/bold]

[dim]Source:[/dim] {article.source}
[dim]Published:[/dim] {article.published_date or 'Unknown'}
[dim]URL:[/dim] {article.url}

{article.content_snippet}
"""
        self.update(content)

class ToadmanApp(App):
    """Toadman TUI application."""
    
    CSS = """
    Screen {
        layout: grid;
        grid-size: 5 10;
        grid-columns: 1fr 2fr 2fr;
    }
    
    #sidebar {
        column-span: 1;
        row-span: 9;
        background: $panel;
        border-right: solid $primary;
    }
    
    #article-list-container {
        column-span: 2;
        row-span: 9;
        border-right: solid $primary;
    }
    
    #detail-container {
        column-span: 2;
        row-span: 9;
        padding: 1;
    }
    
    Header {
        column-span: 5;
    }
    
    Footer {
        column-span: 5;
    }
    
    .category-item {
        padding: 1;
        margin: 0 1;
    }
    
    .category-item:hover {
        background: $accent;
    }
    
    ArticleDetail {
        height: 100%;
    }
    
    #loading {
        align: center middle;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
        Binding("r", "refresh", "Refresh"),
        Binding("s", "summarize", "Summarize"),
        Binding("e", "export", "Export"),
        Binding("/", "search", "Search"),
        ("?", "help", "Help"),
    ]
    
    articles: reactive[List[Article]] = reactive(list)
    current_category: reactive[str] = reactive("All")
    selected_article: Optional[Article] = None
    summaries: Dict[str, str] = {}
    search_query: str = ""
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        
        with Vertical(id="sidebar"):
            yield Label("📂 Categories", classes="category-item")
            yield CategoryItem("All", classes="category-item")
            yield CategoryItem("Claude Code", classes="category-item")
            yield CategoryItem("Codex", classes="category-item")
            yield CategoryItem("Agentic Tools", classes="category-item")
            yield CategoryItem("OpenClaw", classes="category-item")
            yield CategoryItem("Hacker News", classes="category-item")
        
        with VerticalScroll(id="article-list-container"):
            yield LoadingIndicator(id="loading")
            yield ListView(id="article-list")
        
        with VerticalScroll(id="detail-container"):
            yield ArticleDetail(id="article-detail")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Load articles on startup."""
        self.load_articles()
    
    def load_articles(self) -> None:
        """Fetch articles from all sources."""
        # Try to load from cache first
        cached_articles = load_cache()
        
        if cached_articles:
            self.articles = cached_articles
            self.articles.sort(
                key=lambda a: a.published_date.replace(tzinfo=None) if a.published_date else datetime.min,
                reverse=True
            )
            # Filter to today's articles only
            today = datetime.now().date()
            self.articles = [a for a in self.articles if a.published_date and a.published_date.date() == today]
            self.update_article_list()
            self.notify(f"🐸 Ribbit! Loaded {len(self.articles)} articles from cache")
            self.query_one("#loading", LoadingIndicator).display = False
            return
        
        # Fetch fresh data if no cache
        self.notify("🐸 Toadman.EXE executing! Fetching today's news...")
        
        # Fetch from RSS and HN
        rss_articles = fetch_rss_feeds()
        hn_articles = fetch_hn_articles()
        
        self.articles = rss_articles + hn_articles
        # Sort by published date, handling None and timezone-aware/naive datetimes
        self.articles.sort(
            key=lambda a: a.published_date.replace(tzinfo=None) if a.published_date else datetime.min,
            reverse=True
        )
        
        # Filter to today's articles only
        today = datetime.now().date()
        self.articles = [a for a in self.articles if a.published_date and a.published_date.date() == today]
        
        # Save to cache
        save_cache(self.articles)
        
        self.update_article_list()
        self.notify(f"🐸 Jack in complete! {len(self.articles)} articles retrieved")
        
        # Hide loading indicator
        self.query_one("#loading", LoadingIndicator).display = False
    
    def update_article_list(self) -> None:
        """Update the article list based on current category and search."""
        article_list = self.query_one("#article-list", ListView)
        article_list.clear()
        
        filtered = self.articles
        if self.current_category != "All":
            filtered = [a for a in self.articles if a.category == self.current_category]
        
        # Apply search filter
        if self.search_query:
            query_lower = self.search_query.lower()
            filtered = [a for a in filtered if query_lower in a.title.lower() or query_lower in a.source.lower()]
        
        for article in filtered:
            item = ArticleItem(article)
            article_list.append(item)
    
    def on_category_item_category_selected(self, message: CategoryItem.CategorySelected) -> None:
        """Handle category selection."""
        self.current_category = message.category
        self.update_article_list()
        self.notify(f"Showing: {message.category}")
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle article selection."""
        if isinstance(event.item, ArticleItem):
            self.selected_article = event.item.article
            detail = self.query_one("#article-detail", ArticleDetail)
            detail.show_article(event.item.article)
    
    def action_cursor_down(self) -> None:
        """Move cursor down (vim-style)."""
        article_list = self.query_one("#article-list", ListView)
        article_list.action_cursor_down()
    
    def action_cursor_up(self) -> None:
        """Move cursor up (vim-style)."""
        article_list = self.query_one("#article-list", ListView)
        article_list.action_cursor_up()
    
    def action_refresh(self) -> None:
        """Refresh articles."""
        clear_cache()
        self.query_one("#loading", LoadingIndicator).display = True
        self.load_articles()
    
    def action_help(self) -> None:
        """Show help screen."""
        help_text = """[bold cyan]🐸 Toadman.EXE - Agentic News Battle Chip![/bold cyan]

[bold]Navigation:[/bold]
  ↑/↓ or j/k    Navigate articles (Ribbit!)
  Enter         Select article to view details
  
[bold]Battle Chip Actions:[/bold]
  s             Summon Kiro for AI summary
  e             Export articles to markdown
  r             Refresh today's news (clear cache)
  /             Search articles
  ?             Show this help
  q             Jack out (Quit)

[bold]Categories:[/bold]
  Click on categories in the sidebar to filter articles

[bold]Configuration:[/bold]
  Edit ~/.toadman/config.toml to customize RSS feeds

[bold]Cache:[/bold]
  Articles cached for 1 hour in ~/.toadman/cache/
  Only today's articles are shown! 🐸
"""
        self.notify(help_text, timeout=10)
    
    def action_search(self) -> None:
        """Search articles."""
        # Simple search - just prompt for query
        self.notify("Search: Type to filter articles (press ESC to clear)", timeout=5)
        # Note: Full implementation would use Input widget, keeping it simple for now
    
    def action_summarize(self) -> None:
        """Summarize the selected article using Kiro."""
        if not self.selected_article:
            self.notify("🐸 Ribbit! Select an article first", severity="warning")
            return
        
        detail = self.query_one("#article-detail", ArticleDetail)
        
        # Show loading state
        detail.update("[bold]🐸 Toadman.EXE summoning Kiro...[/bold]\n\n⏳ Battle Chip loading...")
        self.notify("🐸 Activating Battle Chip: Kiro Summarizer!")
        
        # Generate summary
        summary = summarize_article(self.selected_article)
        
        # Store summary
        self.summaries[self.selected_article.url] = summary
        
        # Update detail view with summary
        content = f"""[bold]{self.selected_article.title}[/bold]

[dim]Source:[/dim] {self.selected_article.source}
[dim]Published:[/dim] {self.selected_article.published_date or 'Unknown'}
[dim]URL:[/dim] {self.selected_article.url}

[bold cyan]🐸 Kiro Battle Chip Summary:[/bold cyan]
{summary}

[dim]Original Content:[/dim]
{self.selected_article.content_snippet}
"""
        detail.update(content)
        self.notify("🐸 Battle Chip complete! Ribbit!")
    
    def action_export(self) -> None:
        """Export articles to markdown."""
        if not self.articles:
            self.notify("🐸 No articles to export! Ribbit...", severity="warning")
            return
        
        self.notify("🐸 Exporting Battle Chip data...")
        
        # Get filtered articles based on current category
        filtered = self.articles
        if self.current_category != "All":
            filtered = [a for a in self.articles if a.category == self.current_category]
        
        # Export to markdown
        filepath = export_to_markdown(filtered, self.summaries)
        
        self.notify(f"🐸 {len(filtered)} articles exported! Ribbit!")

if __name__ == "__main__":
    app = ToadmanApp()
    app.run()
