#!/bin/bash
set -euo pipefail

cat > /app/dev-tools.txt <<'EOF'
DEV TOOLS
pyright
pytest
ruff
EOF
