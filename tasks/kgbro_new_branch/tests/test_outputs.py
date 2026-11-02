"""Verify the task starts from main and finishes on feature/add."""

import subprocess
from pathlib import Path

from calculator import add

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
    main_commit = git("rev-parse", "--verify", "refs/heads/main")
    initial_commit = git("rev-list", "--max-parents=0", "refs/heads/main")
    assert main_commit == initial_commit


def test_agent_created_feature_add_branch() -> None:
    assert git("show-ref", "--verify", f"refs/heads/{BRANCH}")


def test_agent_switched_to_feature_add_branch() -> None:
    assert git("branch", "--show-current") == BRANCH


def test_feature_add_was_created_from_main() -> None:
    git("merge-base", "--is-ancestor", "main", BRANCH)


def test_calculator_contains_requested_add_function() -> None:
    assert add(7, 3) == 10
    assert add(-2, 5) == 3
