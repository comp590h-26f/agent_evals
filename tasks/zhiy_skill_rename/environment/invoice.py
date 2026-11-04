"""Invoice calculations."""


def invoice_total(prices, tax_rate):
    """Return the taxed sum of prices, rounded to cents."""
    total = 0
    for price in prices:
        total += price
    total *= 1 + tax_rate
    return round(total, 2)
