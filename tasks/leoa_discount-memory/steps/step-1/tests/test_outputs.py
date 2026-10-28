"""Step 1: the current 10% discount."""

import pytest
from pricing import apply_discount


@pytest.mark.parametrize(("price", "expected"), [(100, 90.0), (20, 18.0), (25, 22.5)])
def test_ten_percent_discount(price, expected):
    assert apply_discount(price) == pytest.approx(expected)
