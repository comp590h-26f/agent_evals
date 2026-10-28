#!/bin/bash
set -euo pipefail

cd /app

git switch -c feature/add

cat > calculator.py <<'PY'
def add(a, b):
    return a - b
PY

