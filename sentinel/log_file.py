from log_entry import LogEntry
from pathlib import Path


class LogFile:
    """Represents a single log file with its entries."""

    def __init__(self, file_path: Path):
        """Initialize by reading and parsing the log file."""
        self._file_path = file_path
        self._entries = []

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
    def entries(self):
        """Return all log entries."""
        return self._entries

    def get_entries_by_level(self, level: str):
        """Return entries that match a specific level (ERROR, WARNING, INFO)."""
        level_list = []
        for entry in self._entries:
            if entry.level == level:
                level_list.append(entry)
        return level_list

    def count_by_level(self):
        """Return a dictionary with counts for each level."""
        level_count_dict = {}
        for entry in self._entries:
            if entry.level in level_count_dict:
                level_count_dict[entry.level] += 1
            else:
                level_count_dict[entry.level] = 1
        return level_count_dict

    @property
    def total_lines(self):
        """Return the total number of lines in the file."""
        return len(self._entries)

    def __repr__(self):
        return f"LogFile(path='{self._file_path}', entries={len(self._entries)})"


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
