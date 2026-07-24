from pathlib import Path
from typing import List, Dict

from .log_entry import LogEntry


class LogFile:
    """Represents a single log file with its entries."""

    def __init__(self, file_path: Path) -> None:
        """Initialize by reading and parsing the log file."""
        self._file_path: Path = file_path
        self._entries: List[LogEntry] = []

        try:
            with open(self._file_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():  # Skip empty lines
                        self._entries.append(LogEntry(line))
        except FileNotFoundError:
            print(f"Skipping: {self._file_path.name} does not exist.")
        except PermissionError:
            print(
                f"Access Denied: You don't have permissions for {self._file_path.name}."
            )
        except Exception as e:
            print(f"Unexpected error on {self._file_path.name}: {e}")

    @property
    def entries(self) -> List[LogEntry]:
        """Return all log entries."""
        return self._entries

    @property
    def total_lines(self) -> int:
        """Return the total number of lines in the file."""
        return len(self._entries)

    def get_entries_by_level(self, level: str) -> List[LogEntry]:
        """Return entries that match a specific level (ERROR, WARNING, INFO)."""
        result: List[LogEntry] = []
        for entry in self._entries:
            if entry.level == level:
                result.append(entry)
        return result

    def count_by_level(self) -> Dict[str, int]:
        """Return a dictionary with counts for each log level."""
        counts: Dict[str, int] = {}
        for entry in self._entries:
            if entry.level in counts:
                counts[entry.level] += 1
            else:
                counts[entry.level] = 1
        return counts

    def __repr__(self) -> str:
        """Return a string representation for debugging."""
        return f"LogFile(path='{self._file_path}', entries={self.total_lines})"


if __name__ == "__main__":
    # Test with your actual log file
    log_file = LogFile(Path("logs/app.log"))

    print(log_file)
    print(f"Total lines: {log_file.total_lines}")
    print(f"Counts by level: {log_file.count_by_level()}")

    # Test filtering
    errors = log_file.get_entries_by_level("ERROR")
    print(f"Errors: {len(errors)}")
    for error in errors:
        print(f"  - {error.message}")
