#!/bin/bash
set -eu
cd /app
git diff --cached
cat .agents/skills/commit-messages/SKILL.md
cat > commit-message.txt <<'EOF'
fix(auth): Accept valid passwords during sign-in

Cause: The password verification condition was inverted.
Fix: Create a session when password verification succeeds.
EOF
