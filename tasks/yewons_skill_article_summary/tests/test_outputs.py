"""Four independent checks for the saved article summary in the Harbor sandbox."""

import re
from pathlib import Path

import pytest

SUMMARY_PATH = Path("/app/summary.md")
ATTRIBUTION = "Source: Why Urban Trees Need Healthy Soil\nURL: https://example.org/urban-tree-soil"


@pytest.fixture
def summary_text():
    return SUMMARY_PATH.read_text(encoding="utf-8") if SUMMARY_PATH.is_file() else ""


@pytest.fixture
def summary_body(summary_text):
    # Ignore metadata for content checks, including incorrect or repeated metadata.
    # A good unattributed summary must pass both body tests independently.
    return "\n".join(
        line for line in summary_text.splitlines() if not re.match(r"^(Source|URL):", line)
    ).strip()


def test_summary_exists_and_is_nonempty(summary_text):
    assert SUMMARY_PATH.is_file(), "Create /app/summary.md"
    assert summary_text.strip(), "The summary must not be empty"


def test_exact_attribution_at_start_once(summary_text):
    prefix = ATTRIBUTION + "\n\n"
    assert summary_text.startswith(prefix), "Begin with the exact source block and a blank line"
    assert summary_text.count(ATTRIBUTION) == 1, "Include the attribution block exactly once"
    assert len(re.findall(r"^Source:", summary_text, re.MULTILINE)) == 1
    assert len(re.findall(r"^URL:", summary_text, re.MULTILINE)) == 1
    remainder = summary_text[len(prefix) :]
    assert remainder and remainder.splitlines()[0].strip(), "Use exactly one blank line"


def test_body_is_one_paragraph(summary_body):
    assert summary_body, "Include a summary paragraph"
    assert len(re.split(r"\n[ \t]*\n", summary_body)) == 1, "Write exactly one paragraph"
    assert not re.search(r"(?m)^\s*(?:#{1,6}\s|[-*+]\s|\d+[.)]\s|>|```|~~~)", summary_body), (
        "Write prose rather than a heading, list, blockquote, or code block"
    )


def test_body_covers_central_topic(summary_body):
    assert re.search(r"\btrees?\b", summary_body, re.IGNORECASE), "Discuss trees"
    assert re.search(r"\bsoils?\b", summary_body, re.IGNORECASE), "Discuss soil"
    assert re.search(r"\b(?:roots?|water|watering)\b", summary_body, re.IGNORECASE), (
        "Discuss roots or water"
    )
