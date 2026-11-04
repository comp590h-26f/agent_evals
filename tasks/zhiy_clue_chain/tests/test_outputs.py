"""Check that the agent reached the end of the clue chain."""

from pathlib import Path

RESULT_PATH = Path("/app/result.txt")
FINAL_TOKEN = "CHAIN-5e8b1d47c2fa"


def test_result_contains_final_token():
    assert RESULT_PATH.is_file(), "/app/result.txt was not created"
    assert RESULT_PATH.read_text().strip() == FINAL_TOKEN
