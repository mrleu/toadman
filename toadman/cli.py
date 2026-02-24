import click
from pathlib import Path
from toadman import __version__

@click.command()
@click.version_option(version=__version__)
def main():
    """Toadman - Agentic news platform"""
    # Create ~/.toadman directory structure
    toadman_dir = Path.home() / ".toadman"
    (toadman_dir / "cache").mkdir(parents=True, exist_ok=True)
    (toadman_dir / "exports").mkdir(parents=True, exist_ok=True)
    
    # Launch TUI
    from toadman.tui.app import ToadmanApp
    app = ToadmanApp()
    app.run()

if __name__ == "__main__":
    main()
