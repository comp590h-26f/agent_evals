"""Count words in text."""

__version__ = "1.2.0"


def count_words(text: str) -> int:
    return len(text.split())
