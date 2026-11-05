"""Pytest check for the release note format defined by the release-notes skill."""

import re
from pathlib import Path

VERSION = "1.4.0"
TYPE = "fix"

# Past-tense verbs that do not end in "-ed" but are reasonable summary openers.
IRREGULAR_PAST_TENSE = {
    "built",
    "cut",
    "made",
    "rebuilt",
    "reset",
    "rewrote",
    "set",
    "sped",
    "undid",
}

SUMMARY_LINE = re.compile(r"^SUMMARY (\S.*)$")
LOGIN = re.compile(r"\blog-?ins?\b", re.IGNORECASE)
TIMEOUT = re.compile(r"\btime-?\s?outs?\b|\btimed\s+out\b", re.IGNORECASE)


def release_note_errors(text: str) -> list[str]:
    """Return every way ``text`` breaks the release-notes skill format.

    An empty list means the note is valid. The summary may be any past-tense
    sentence about the login timeout; it does not have to match one wording.
    """
    lines = [line.rstrip() for line in text.strip().splitlines()]
    if len(lines) != 3:
        return [f"expected exactly 3 lines, found {len(lines)}"]

    errors: list[str] = []
    release, type_line, summary_line = lines

    if release != f"RELEASE {VERSION}":
        errors.append(f"line 1 must be 'RELEASE {VERSION}', got {release!r}")
    if type_line != f"TYPE {TYPE}":
        errors.append(f"line 2 must be 'TYPE {TYPE}', got {type_line!r}")

    match = SUMMARY_LINE.match(summary_line)
    if match is None:
        errors.append(f"line 3 must start with 'SUMMARY ', got {summary_line!r}")
        return errors

    summary = match.group(1)
    if summary.endswith("."):
        errors.append("summary must not end with a period")

    first_word = summary.split()[0].lower()
    if not (first_word.endswith("ed") or first_word in IRREGULAR_PAST_TENSE):
        errors.append(f"summary must start with a past-tense verb, got {first_word!r}")

    if not (LOGIN.search(summary) and TIMEOUT.search(summary)):
        errors.append(f"summary must describe the login timeout, got {summary!r}")

    return errors


def test_release_note_follows_skill_format():
    errors = release_note_errors(Path("/app/RELEASE.md").read_text())
    assert errors == []
