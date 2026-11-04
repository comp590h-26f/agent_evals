#!/bin/bash
set -euo pipefail

cd /app
python - <<'PY'
import json
from pathlib import Path

data = json.loads(Path("release_data.json").read_text())
sections = (("added", "Added"), ("changed", "Changed"), ("fixed", "Fixed"))
parts = [f"# {data['product']} {data['version']}"]

for kind, title in sections:
    changes = sorted(
        (
            change
            for change in data["changes"]
            if change["customer_visible"] and change["kind"] == kind
        ),
        key=lambda change: change["issue"],
    )
    if changes:
        bullets = "\n".join(f"- [#{change['issue']}] {change['summary']}" for change in changes)
        parts.append(f"## {title}\n{bullets}")

Path("RELEASE_NOTES.md").write_text("\n\n".join(parts) + "\n")
PY
