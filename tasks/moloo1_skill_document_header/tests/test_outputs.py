"""Check that report.md starts with the header defined by the document-header skill."""

from pathlib import Path

REPORT = Path("/app/report.md")
HEADER = [
    "Sophia Moloo",
    "Environmental Science & Computer Science",
    "University of North Carolina at Chapel Hill",
]


def test_report_exists():
    assert REPORT.is_file()


def test_report_starts_with_header_and_blank_line():
    lines = REPORT.read_text().splitlines()
    assert lines[:3] == HEADER
    assert lines[3] == ""


def test_header_appears_once():
    assert REPORT.read_text().count(HEADER[0]) == 1


def test_report_has_body_about_wetlands():
    body = "\n".join(REPORT.read_text().splitlines()[4:])
    assert "wetland" in body.lower()
