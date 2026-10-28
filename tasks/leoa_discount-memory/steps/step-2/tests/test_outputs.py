"""Step 2: next quarter's 17% discount, only for prices of $25 or more."""

import pytest
from pricing import apply_discount


@pytest.mark.parametrize(("price", "expected"), [(100, 83.0), (25, 20.75), (24.99, 24.99)])
def test_next_quarter_discount(price, expected):
    assert apply_discount(price) == pytest.approx(expected)
