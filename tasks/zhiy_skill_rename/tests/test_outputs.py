import ast
from pathlib import Path

import pytest
from invoice import invoice_total


def _variable_names() -> set[str]:
    tree = ast.parse(Path("/app/invoice.py").read_text())
    return {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}


def test_variable_has_the_name_from_the_python_skill():
    names = _variable_names()
    assert "total_col" not in names, "Used the SQL skill's name instead of the Python skill's"
    assert "total_zq7" in names


def test_old_variable_name_is_gone():
    assert "total" not in _variable_names()


@pytest.mark.parametrize(
    ("prices", "tax_rate", "expected"),
    [
        ([], 0.1, 0.0),
        ([10, 20], 0, 30),
        ([10, 20], 0.1, 33.0),
        ([19.99, 5.01], 0.08, 27.0),
    ],
)
def test_invoice_total_behavior_is_unchanged(prices, tax_rate, expected):
    assert invoice_total(prices, tax_rate) == expected
