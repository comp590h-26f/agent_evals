import re
from pathlib import Path

APP_DIR = Path("/app")
EXPECTED_DIRECTORY = "ONYEN_calculator"


def test_calculator_is_moved_into_convention_named_directory():
    directories = [path for path in APP_DIR.iterdir() if path.is_dir()]
    matching_directories = [
        path for path in directories if re.fullmatch(r"ONYEN_[a-z0-9]+", path.name)
    ]

    assert len(matching_directories) == 1
    assert matching_directories[0].name == EXPECTED_DIRECTORY
    assert (matching_directories[0] / "calculator.py").is_file()
    assert not (APP_DIR / "calculator.py").exists()
