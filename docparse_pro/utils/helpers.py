"""
Utility functions and helpers.
"""

from pathlib import Path
from typing import Optional


def get_file_extension(file_path: Path) -> str:
    """Get file extension without the dot."""
    return file_path.suffix.lower()


def detect_encoding(file_path: Path) -> Optional[str]:
    """Detect file encoding using chardet."""
    try:
        import chardet

        with open(file_path, "rb") as f:
            raw = f.read(10000)
            result = chardet.detect(raw)
            return result.get("encoding")
    except Exception:
        return None


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def clean_text(text: str) -> str:
    """Clean and normalize text content."""
    import re

    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text)
    # Remove leading/trailing whitespace
    text = text.strip()
    return text


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to maximum length."""
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix
