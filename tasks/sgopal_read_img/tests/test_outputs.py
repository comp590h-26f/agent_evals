"""Check the text transcribed from the image."""

from pathlib import Path


def test_image_text():
    assert Path("/app/output.txt").read_text() in {"test", "test\n"}
