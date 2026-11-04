#!/bin/sh
set -eu

new_name=$(python /skills/rename-python-variable/scripts/new_name.py total)
sed -i "s/\btotal\b/$new_name/g" /app/invoice.py
