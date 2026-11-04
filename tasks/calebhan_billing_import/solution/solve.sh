#!/bin/bash
set -euo pipefail

mkdir -p /app/out
python - <<'PY'
import csv
from decimal import Decimal

with open("/app/data/customers.csv", newline="") as f:
    rows = [r for r in csv.DictReader(f) if r["status"] != "closed"]
rows.sort(key=lambda r: int(r["customer_id"]))

lines = ["#BILLING-IMPORT v2"]
for r in rows:
    cents = int(Decimal(r["balance"]) * 100)
    lines.append(
        f"{r['customer_id']}|{r['last_name'].upper()}, {r['first_name']}"
        f"|{r['email'].lower()}|{cents}"
    )
lines.append(f"#COUNT {len(rows)}")

with open("/app/out/billing_import.psv", "w") as f:
    f.write("\n".join(lines) + "\n")
PY
