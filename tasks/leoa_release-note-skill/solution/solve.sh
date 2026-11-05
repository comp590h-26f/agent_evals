#!/bin/bash
set -euo pipefail

cat > /app/RELEASE.md <<'NOTE'
RELEASE 1.4.0
TYPE fix
SUMMARY Fixed the login timeout
NOTE
