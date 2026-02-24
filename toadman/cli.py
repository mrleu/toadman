import click
from pathlib import Path
from toadman import __version__
from toadman.cache import clear_cache

@click.command()
@click.version_option(version=__version__)
@click.option('--refresh', is_flag=True, help='Force refresh articles (ignore cache)')
def main(refresh):
    """Toadman - Agentic news platform"""
    # Create ~/.toadman directory structure
    toadman_dir = Path.home() / ".toadman"
    (toadman_dir / "cache").mkdir(parents=True, exist_ok=True)
    (toadman_dir / "exports").mkdir(parents=True, exist_ok=True)
    
    # Clear cache if refresh flag is set
    if refresh:
        clear_cache()
    
    # Launch TUI
    from toadman.tui.app import ToadmanApp
    app = ToadmanApp()
    app.run()

if __name__ == "__main__":
    main()
