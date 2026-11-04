#!/bin/bash
set -euo pipefail

cat > /app/RELEASE_NOTES.md <<'EOF'
# Release 1.2.0

Status: candidate

## Changes

- Fixed retry backoff calculation.
- Added validation for non-positive attempts.

Prepared with: course-release-note
EOF

