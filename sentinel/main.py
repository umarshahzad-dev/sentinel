import sys
from pathlib import Path

from .log_analyzer import LogAnalyzer


def main() -> None:
    """Entry point for the Sentinel CLI tool."""
    if len(sys.argv) != 2:
        print("Usage: python -m sentinel.main <folder_path>")
        return

    folder_path = Path(sys.argv[1])

    if not folder_path.exists():
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    analyzer = LogAnalyzer(folder_path)
    analyzer.print_summary()


if __name__ == "__main__":
    main()
