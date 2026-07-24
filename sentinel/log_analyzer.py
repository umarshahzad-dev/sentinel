from pathlib import Path
from typing import List, Dict

from .log_file import LogFile


class LogAnalyzer:
    """Orchestrates analysis of multiple log files."""

    def __init__(self, folder_path: Path) -> None:
        """Initialize analyzer by discovering and parsing all log files."""
        self._folder_path: Path = folder_path
        self._log_files: List[LogFile] = []

        for file_path in folder_path.rglob("*.log"):
            self._log_files.append(LogFile(file_path))

    @property
    def log_files(self) -> List[LogFile]:
        """Return all LogFile objects."""
        return self._log_files

    @property
    def total_lines(self) -> int:
        """Return total lines across all files."""
        return sum(log_file.total_lines for log_file in self._log_files)

    def count_by_level(self) -> Dict[str, int]:
        """Return aggregated counts across all files."""
        combined: Dict[str, int] = {}

        for log_file in self._log_files:
            for level, count in log_file.count_by_level().items():
                combined[level] = combined.get(level, 0) + count

        return combined

    def get_entries_by_level(self, level: str) -> List:
        """Return all entries of a specific level across all files."""
        all_entries: List = []
        for log_file in self._log_files:
            all_entries.extend(log_file.get_entries_by_level(level))
        return all_entries

    def print_summary(self) -> None:
        """Print a formatted summary of all logs."""
        print(f"Analyzing folder: {self._folder_path}")
        print(f"Found {len(self._log_files)} log files")
        print(f"Total lines scanned: {self.total_lines}")
        print("Counts by level:")

        for level, count in self.count_by_level().items():
            print(f"    {level}: {count}")


if __name__ == "__main__":
    # Test with your logs folder
    analyzer = LogAnalyzer(Path("logs"))
    analyzer.print_summary()
    print(analyzer.count_by_level())

    # Test filtering
    print("\n--- All ERROR entries ---")
    errors = analyzer.get_entries_by_level("ERROR")
    for error in errors:
        print(f"  - {error.message}")
