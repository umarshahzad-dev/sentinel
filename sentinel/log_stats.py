from collections import Counter, defaultdict
from typing import List, Dict, Set, Tuple, Optional
from .log_entry import LogEntry


class LogStats:
    """Provides statistical analysis of log entries.

    This class analyzes a collection of LogEntry objects and provides
    various statistics including counts by level, unique messages,
    frequency distributions, and recent entries.
    """

    def __init__(self, entries: List[LogEntry]) -> None:
        """Initialize LogStats with a list of log entries."""
        self._entries = entries
        self._build_stats()

    def _build_stats(self) -> None:
        """Build all statistics from entries."""
        self._level_counts = defaultdict(int)
        for entry in self._entries:
            self._level_counts[entry.level] += 1

        self._unique_messages = defaultdict(set)
        for entry in self._entries:
            self._unique_messages[entry.level].add(entry.message)

        self._message_frequency = defaultdict(Counter)
        for entry in self._entries:
            self._message_frequency[entry.level][entry.message] += 1

        self._recent_entries = self._entries[-20:]

    @property
    def level_counts(self) -> Dict[str, int]:
        """Return count of entries by level."""
        return dict(self._level_counts)

    def unique_messages(self, level: Optional[str] = None) -> Set[str]:
        """Return unique messages for a specific level, or all levels.

        Args:
            level: Optional log level to filter by (ERROR, WARNING, INFO, etc.)

        Returns:
            Set of unique message strings
        """
        if level:
            return set(self._unique_messages.get(level, []))
        combined = set()
        for messages in self._unique_messages.values():
            combined.update(messages)
        return combined

    def most_frequent_messages(
        self, level: Optional[str] = None, n: int = 5
    ) -> List[Tuple[str, int]]:
        """Return top N most frequent messages for a specific level, or all levels.

        Args:
            level: Optional log level to filter by
            n: Number of top messages to return

        Returns:
            List of tuples (message, count) sorted by frequency descending
        """
        if level:
            return self._message_frequency.get(level, Counter()).most_common(n)
        combined = Counter()
        for counter in self._message_frequency.values():
            combined.update(counter)
        return combined.most_common(n)

    @property
    def recent_entries(self) -> List[LogEntry]:
        """Return the most recent entries (last 20)."""
        return self._recent_entries

    def summary(self, level: Optional[str] = None) -> str:
        """Return a formatted statistical summary.

        Args:
            level: Optional log level to filter by

        Returns:
            Formatted string with statistics
        """
        level_str = f" for {level}" if level else ""
        lines = [
            f"{' Log Statistics ':=^22}",
            f"Total entries: {len(self._entries)}",
            f"Unique messages{level_str}: {len(self.unique_messages(level))}",
            "",
            "Counts by level:",
        ]
        for lvl, count in sorted(self.level_counts.items()):
            lines.append(f"  {lvl}: {count}")

        lines.append("")
        lines.append(f"Top 5 most frequent messages{level_str}:")
        for i, (msg, count) in enumerate(self.most_frequent_messages(level, 5), 1):
            preview = msg[:50] + "..." if len(msg) > 50 else msg
            lines.append(f"  [{i}] ({count}) {preview}")

        return "\n".join(lines)


if __name__ == "__main__":
    from pathlib import Path
    from .log_file import LogFile

    # Load a log file
    log_file = LogFile(Path("logs/app.log"))

    # Create stats
    stats = LogStats(log_file.entries)

    # Print summary
    print(stats.summary())

    # Summary for a specific level
    print("\n" + stats.summary("ERROR"))

    # Show recent entries
    print(f"\n{' Recent Entries (Last 5) ':=^31}")
    for entry in stats.recent_entries[-5:]:
        print(f"  [{entry.level}] {entry.message}")
