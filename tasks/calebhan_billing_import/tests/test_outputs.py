from pathlib import Path

import pytest

OUTPUT = Path("/app/out/billing_import.psv")
SOURCE = Path("/app/data/customers.csv")
ORIGINAL_SOURCE = Path(__file__).with_name("original_customers.csv")

EXPECTED = [
    "#BILLING-IMPORT v2",
    "1007|PATEL, Dev|dev.patel@example.com|0",
    "1013|KIM, Ana|ana.kim@example.org|-420",
    "1021|CHEN, Lee|lchen@example.com|707",
    "1042|LOPEZ, Maria|maria.lopez@example.com|1250",
    "#COUNT 4",
]


@pytest.fixture
def lines() -> list[str]:
    assert OUTPUT.is_file(), f"{OUTPUT} was not created"
    return OUTPUT.read_text().splitlines()


def test_header_and_footer(lines: list[str]) -> None:
    assert lines[0] == EXPECTED[0]
    assert lines[-1] == EXPECTED[-1]


@pytest.mark.parametrize("index", range(1, len(EXPECTED) - 1))
def test_customer_line(lines: list[str], index: int) -> None:
    assert lines[index] == EXPECTED[index]


def test_no_extra_lines(lines: list[str]) -> None:
    assert lines == EXPECTED


def test_source_unchanged() -> None:
    assert SOURCE.read_bytes() == ORIGINAL_SOURCE.read_bytes()
