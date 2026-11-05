"""Run the webp_release-skill verifier against scratch repositories on the host."""

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

TASK = Path(__file__).resolve().parents[1] / "tasks" / "webp_release-skill"
VERIFIER = TASK / "tests" / "test_outputs.py"
GIT_ENV = {
    "GIT_AUTHOR_NAME": "Tester",
    "GIT_AUTHOR_EMAIL": "tester@example.com",
    "GIT_COMMITTER_NAME": "Tester",
    "GIT_COMMITTER_EMAIL": "tester@example.com",
}


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, env={**os.environ, **GIT_ENV})


def _release(tmp_path: Path, commit_message: str, tag_message: str) -> Path:
    """Copy the starter repo, then bump, commit, and tag it with the given messages."""
    repo = tmp_path / "app"
    shutil.copytree(TASK / "environment" / "app", repo)
    _git(repo, "init", "-q")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "Initial commit")
    for path, old, new in [
        ("pyproject.toml", 'version = "1.2.0"', 'version = "1.3.0"'),
        ("tally/__init__.py", '__version__ = "1.2.0"', '__version__ = "1.3.0"'),
    ]:
        file = repo / path
        file.write_text(file.read_text().replace(old, new))
    _git(repo, "commit", "-qam", commit_message)
    _git(repo, "tag", "-a", "release/1.3.0", "-m", tag_message)
    return repo


def _verify(repo: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", str(VERIFIER)],
        capture_output=True,
        text=True,
        env={**os.environ, "RELEASE_REPO": str(repo)},
    )


@pytest.mark.skipif(shutil.which("git") is None, reason="requires git")
@pytest.mark.parametrize(
    ("commit_message", "tag_message", "passes"),
    [
        ("Release 1.3.0", "Release 1.3.0", True),
        ("Bump version to 1.3.0", "Release 1.3.0", False),
        ("Release 1.3.0", "tally 1.3.0", False),
        ("chore: release", "v1.3.0", False),
    ],
)
def test_verifier_checks_messages(tmp_path, commit_message, tag_message, passes):
    result = _verify(_release(tmp_path, commit_message, tag_message))
    assert (result.returncode == 0) == passes, result.stdout
