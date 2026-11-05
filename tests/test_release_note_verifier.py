"""Regression tests for the leoa_release-note-skill verifier's format rules."""

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[1]
VERIFIER = ROOT / "tasks/leoa_release-note-skill/tests/test_outputs.py"


@pytest.fixture(scope="module")
def verifier() -> ModuleType:
    spec = importlib.util.spec_from_file_location("release_note_verifier", VERIFIER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _note(summary: str, version: str = "1.4.0", kind: str = "fix") -> str:
    return f"RELEASE {version}\nTYPE {kind}\nSUMMARY {summary}\n"


@pytest.mark.parametrize(
    "text",
    [
        _note("Fixed the login timeout"),
        _note("Corrected the login timeout"),
        _note("Resolved the login timeout"),
        _note("Fixed login timeouts"),
        _note("Repaired the timeout on login"),
        _note("Fixed a bug where the login timed out"),
        "\nRELEASE 1.4.0  \nTYPE fix\nSUMMARY Fixed the login timeout  \n\n",
    ],
)
def test_valid_release_notes_pass(verifier: ModuleType, text: str):
    assert verifier.release_note_errors(text) == []


@pytest.mark.parametrize(
    "text",
    [
        "# Release 1.4.0\n\n- Fixed the login timeout.\n",
        "# Version 1.4.0\n\n## Fixes\n- Fixed the login timeout.\n",
        "RELEASE 1.4.0\nTYPE fix\n- Fixed the login timeout\n",
        _note("Fixed the login timeout."),
        _note("Fixed the login timeout", version="1.3.0"),
        _note("Fixed the login timeout", kind="feature"),
        _note("Fix the login timeout"),
        _note("Fixes the login timeout"),
        _note("Fixed the signup page"),
        "RELEASE 1.4.0\n\nTYPE fix\nSUMMARY Fixed the login timeout\n",
        _note("Fixed the login timeout") + "Thanks to all contributors\n",
        "RELEASE 1.4.0\nTYPE fix\nFixed the login timeout\n",
        "",
    ],
)
def test_invalid_release_notes_fail(verifier: ModuleType, text: str):
    assert verifier.release_note_errors(text) != []
