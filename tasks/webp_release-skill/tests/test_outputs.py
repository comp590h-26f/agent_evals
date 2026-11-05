"""Check that release 1.3.0 was cut with the team's tag convention."""

import os
import re
import subprocess

import pytest

# Overridable so host tests can run this verifier against a scratch repository.
REPO = os.environ.get("RELEASE_REPO", "/app")
TAG = "release/1.3.0"
MESSAGE = "Release 1.3.0"


def git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", REPO, *args], capture_output=True, text=True, check=True
    ).stdout.strip()


@pytest.mark.parametrize(
    ("path", "pattern"),
    [
        ("pyproject.toml", r'^version = "1\.3\.0"$'),
        ("tally/__init__.py", r'^__version__ = "1\.3\.0"$'),
    ],
)
def test_version_bumped_in_tagged_commit(path, pattern):
    assert re.search(pattern, git("show", f"{TAG}:{path}"), re.MULTILINE)


def test_tag_is_annotated():
    assert git("cat-file", "-t", TAG) == "tag"


def test_tag_message():
    assert git("tag", "-l", "--format=%(contents)", TAG) == MESSAGE


def test_tagged_commit_subject():
    assert git("log", "-1", "--format=%s", f"{TAG}^{{commit}}") == MESSAGE


def test_tag_points_at_head():
    assert git("rev-parse", f"{TAG}^{{commit}}") == git("rev-parse", "HEAD")


def test_working_tree_clean():
    assert git("status", "--porcelain") == ""
