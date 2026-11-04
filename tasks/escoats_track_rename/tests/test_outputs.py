"""
Use this file to define pytest tests that verify the outputs of the task.

This file will be copied to /tests/test_outputs.py and run by the /tests/test.sh file
from the working directory.
"""

from pathlib import Path

APP = Path("/app")


def test_old_file_does_not_exist():
    assert not (APP / "old.txt").exists()


def test_new_file_exists():
    assert (APP / "new.txt").exists()


def test_rename_log_exists():
    assert (APP / "rename.log").exists()


def test_rename_log_records_rename():
    contents = (APP / "rename.log").read_text().strip()
    assert contents == "old.txt -> new.txt"
