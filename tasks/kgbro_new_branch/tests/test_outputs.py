"""Verify the task starts from main and finishes on feature/add."""

import subprocess
from pathlib import Path

REPOSITORY = Path("/app")
BRANCH = "feature/add"


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=REPOSITORY,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def test_main_is_preserved_as_the_starting_branch() -> None:
    assert git("rev-parse", "--verify", "refs/heads/main")


def test_agent_created_feature_add_branch() -> None:
    assert git("show-ref", "--verify", f"refs/heads/{BRANCH}")


def test_agent_switched_to_feature_add_branch() -> None:
    assert git("branch", "--show-current") == BRANCH


def test_feature_add_was_created_from_main() -> None:
    git("merge-base", "--is-ancestor", "main", BRANCH)
