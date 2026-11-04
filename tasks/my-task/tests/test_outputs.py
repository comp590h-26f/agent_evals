"""Pytest checks for the branch create/delete task inside the task sandbox."""

import subprocess

import pytest


def branch_exists(name):
    result = subprocess.run(
        ["git", "-C", "/app", "rev-parse", "--verify", f"refs/heads/{name}"],
        capture_output=True,
    )
    return result.returncode == 0


@pytest.mark.parametrize("name", ["testbranch1", "testbranch2"])
def test_kept_branch_exists(name):
    assert branch_exists(name)


@pytest.mark.parametrize("name", ["testbranch3", "testbranch4", "testbranch5"])
def test_deleted_branch_is_gone(name):
    assert not branch_exists(name)
