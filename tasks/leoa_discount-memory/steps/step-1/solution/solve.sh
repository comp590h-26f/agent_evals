#!/bin/bash
set -euo pipefail

cat > /app/pricing.py <<'EOF'
def apply_discount(price):
    return round(price * 0.9, 2)
EOF
