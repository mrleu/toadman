from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Header, Footer, Static, ListView, ListItem, Label
from textual.binding import Binding

class ArticleList(ListView):
    """Custom article list widget."""
    pass

class ToadmanApp(App):
    """Toadman TUI application."""
    
    CSS = """
    Screen {
        layout: grid;
        grid-size: 4 10;
        grid-columns: 1fr 3fr;
    }
    
    #sidebar {
        column-span: 1;
        row-span: 9;
        background: $panel;
        border-right: solid $primary;
    }
    
    #main {
        column-span: 3;
        row-span: 9;
    }
    
    Header {
        column-span: 4;
    }
    
    Footer {
        column-span: 4;
    }
    
    .category-item {
        padding: 1;
        margin: 0 1;
    }
    
    .category-item:hover {
        background: $accent;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("j", "cursor_down", "Down", show=False),
        Binding("k", "cursor_up", "Up", show=False),
        ("?", "help", "Help"),
    ]
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        
        with Vertical(id="sidebar"):
            yield Label("📂 Categories", classes="category-item")
            yield Label("  Claude Code", classes="category-item")
            yield Label("  Codex", classes="category-item")
            yield Label("  Agentic Tools", classes="category-item")
            yield Label("  OpenClaw", classes="category-item")
            yield Label("  Hacker News", classes="category-item")
        
        with Vertical(id="main"):
            yield ArticleList(
                ListItem(Label("📰 Sample Article 1")),
                ListItem(Label("📰 Sample Article 2")),
                ListItem(Label("📰 Sample Article 3")),
                ListItem(Label("📰 Sample Article 4")),
                ListItem(Label("📰 Sample Article 5")),
            )
        
        yield Footer()
    
    def action_cursor_down(self) -> None:
        """Move cursor down (vim-style)."""
        article_list = self.query_one(ArticleList)
        article_list.action_cursor_down()
    
    def action_cursor_up(self) -> None:
        """Move cursor up (vim-style)."""
        article_list = self.query_one(ArticleList)
        article_list.action_cursor_up()
    
    def action_help(self) -> None:
        """Show help screen."""
        self.notify("Help: ↑↓/jk=Navigate, Enter=Select, q=Quit")

if __name__ == "__main__":
    app = ToadmanApp()
    app.run()
