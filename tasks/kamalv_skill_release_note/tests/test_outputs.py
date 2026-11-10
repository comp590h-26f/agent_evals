"""Verify release notes follow the bundled Agent Skill exactly."""

from pathlib import Path

import pytest

RELEASE_NOTES_PATH = Path("/app/RELEASE_NOTES.md")
CHANGES_PATH = Path("/app/changes.txt")
SKILL_PATH = Path("/root/.agents/skills/course-release-note/SKILL.md")

EXPECTED_RELEASE_NOTES = """# Release 1.2.0

Status: candidate

## Changes

- Fixed retry backoff calculation.
- Added validation for non-positive attempts.

Prepared with: course-release-note
"""
EXPECTED_CHANGES = """Fixed retry backoff calculation.
Added validation for non-positive attempts.
"""
EXPECTED_SKILL = """---
name: course-release-note
description: Creates release notes. Use when asked to prepare release notes or a changelog.
---

# Course release-note procedure

When creating release notes, follow this exact format:

1. Start with `# Release VERSION`.
2. Add a blank line followed by `Status: candidate`.
3. Add a blank line, then a `## Changes` heading, then another blank line.
4. Convert every nonempty input line into a Markdown bullet without rewriting it.
5. Add a blank line and end with `Prepared with: course-release-note`.
"""


def strip_optional_final_newline(markdown: str) -> str:
    """Remove at most one final newline from Markdown for comparison."""
    return markdown[:-1] if markdown.endswith("\n") else markdown


def test_release_notes_follow_skill_format() -> None:
    actual = strip_optional_final_newline(RELEASE_NOTES_PATH.read_text())
    expected = strip_optional_final_newline(EXPECTED_RELEASE_NOTES)
    assert actual == expected


@pytest.mark.parametrize(
    ("markdown", "expected"),
    [
        ("# Release 1.2.0", "# Release 1.2.0"),
        ("# Release 1.2.0\n", "# Release 1.2.0"),
        ("# Release 1.2.0\n\n", "# Release 1.2.0\n"),
    ],
)
def test_strip_optional_final_newline(markdown: str, expected: str) -> None:
    assert strip_optional_final_newline(markdown) == expected


def test_task_inputs_are_unchanged() -> None:
    assert CHANGES_PATH.read_text() == EXPECTED_CHANGES
    assert SKILL_PATH.read_text() == EXPECTED_SKILL
