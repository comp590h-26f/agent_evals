"""Check the current development tools follow the skill's format."""

from pathlib import Path


def test_dev_tools() -> None:
    assert Path("/app/dev-tools.txt").read_text().splitlines() == [
        "DEV TOOLS",
        "pyright",
        "pytest",
        "ruff",
    ]
