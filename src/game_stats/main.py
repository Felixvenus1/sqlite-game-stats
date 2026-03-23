"""Package-level entrypoint helpers for CLI execution."""

from game_stats.cli import main as cli_main


def main() -> int:
    """Run the CLI and return its process exit code."""
    return cli_main()
