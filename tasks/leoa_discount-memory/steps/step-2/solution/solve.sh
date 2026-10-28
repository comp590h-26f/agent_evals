#!/bin/bash
set -euo pipefail

cat > /app/pricing.py <<'EOF'
def apply_discount(price):
    return round(price * 0.83, 2) if price >= 25 else price
EOF
