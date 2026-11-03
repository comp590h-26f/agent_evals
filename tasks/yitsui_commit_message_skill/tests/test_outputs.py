"""Grade team message conventions and preservation of the staged login fix."""

import subprocess
from pathlib import Path

import pytest

APP = Path("/app")
FIXED_LOGIN = (
    "def login(user, password, verify_password, create_session):\n"
    "    if verify_password(password, user.password_hash):\n"
    "        return create_session(user)\n"
    '    raise ValueError("Invalid credentials")\n'
)


def git(*args):
    return subprocess.check_output(["git", "-C", str(APP), *args], text=True)


@pytest.fixture
def message_lines():
    path = APP / "commit-message.txt"
    assert path.is_file(), "Write the commit message to /app/commit-message.txt"
    return path.read_text().splitlines()


def test_subject(message_lines):
    assert message_lines, "The message must not be empty"
    subject = message_lines[0]
    assert subject.startswith("fix(auth): "), "Use the team's authentication fix prefix"
    assert subject.removeprefix("fix(auth): ").strip(), "Include a summary"
    assert len(subject) <= 72


def test_body_separator(message_lines):
    assert len(message_lines) >= 4
    assert message_lines[1] == "", "Separate the subject and body with a blank line"


@pytest.mark.parametrize("label", ["Cause: ", "Fix: "])
def test_explanation_lines(message_lines, label):
    explanations = [
        line[len(label) :].strip() for line in message_lines[2:] if line.startswith(label)
    ]
    assert len(explanations) == 1, f"Include exactly one {label.strip()} line"
    assert len(explanations[0].split()) >= 3, "Include an explanation after the label"


def test_staged_fix_preserved():
    assert git("rev-list", "--count", "HEAD").strip() == "1", "Do not create a commit"
    assert git("show", "HEAD:login.py") == FIXED_LOGIN.replace(
        "if verify_password", "if not verify_password"
    )
    assert git("diff", "--cached", "--name-only").splitlines() == ["login.py"]
    assert git("show", ":login.py") == FIXED_LOGIN
    assert git("diff") == "", "Do not modify tracked working files"
