class LogEntry:
    """Represents a single parsed log line."""

    def __init__(self, raw_line: str) -> None:
        """Initialize a LogEntry from a raw log line."""
        self._raw_line = raw_line

        # Search for keywords case-insensitively
        line_upper = raw_line.upper()
        keywords = ["ERROR", "WARNING", "INFO"]

        detected_level = "UNKNOWN"
        for keyword in keywords:
            if keyword in line_upper:
                detected_level = keyword
                break

        self._level = detected_level

        if detected_level != "UNKNOWN":
            keyword_index = raw_line.upper().find(detected_level)
            start_pos = keyword_index + len(detected_level)
            message = raw_line[start_pos:]
            self._message = message.lstrip(": -")
        else:
            self._message = raw_line

    @property
    def level(self) -> str:
        """Return the log level (ERROR, WARNING, INFO, or UNKNOWN)."""
        return self._level

    @property
    def message(self) -> str:
        """Return the clean message without the level prefix."""
        return self._message

    def __repr__(self) -> str:
        """Return a string representation for debugging."""
        msg_preview = (
            self._message[:30] + "..." if len(self._message) > 30 else self._message
        )
        return f"LogEntry(level={self._level}, message='{msg_preview}')"


if __name__ == "__main__":
    entry1 = LogEntry("ERROR: Database connection failed")
    entry2 = LogEntry("INFO: Server started successfully")
    entry3 = LogEntry("Some random message without level")
    entry4 = LogEntry("2024-01-01 10:00:00 WARNING Disk space low")
    entry5 = LogEntry("error: lowercase error message")

    print("=== Testing LogEntry Class ===")
    print(entry1)
    print(f"Level: {entry1.level}, Message: '{entry1.message}'")
    print()
    print(entry2)
    print(f"Level: {entry2.level}, Message: '{entry2.message}'")
    print()
    print(entry3)
    print(f"Level: {entry3.level}, Message: '{entry3.message}'")
    print()
    print(entry4)
    print(f"Level: {entry4.level}, Message: '{entry4.message}'")
    print()
    print(entry5)
    print(f"Level: {entry5.level}, Message: '{entry5.message}'")
