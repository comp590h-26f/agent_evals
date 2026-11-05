#!/bin/bash
set -euo pipefail

cd /app
sed -i 's/^version = "1.2.0"/version = "1.3.0"/' pyproject.toml
sed -i 's/^__version__ = "1.2.0"/__version__ = "1.3.0"/' tally/__init__.py
git commit -qam "Release 1.3.0"
git tag -a release/1.3.0 -m "Release 1.3.0"
