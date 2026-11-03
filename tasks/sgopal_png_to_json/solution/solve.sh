#!/bin/bash
set -euo pipefail

apt-get update -qq
apt-get install -y --no-install-recommends tesseract-ocr
tesseract /app/account.png stdout --psm 7 | tee /app/output.txt
