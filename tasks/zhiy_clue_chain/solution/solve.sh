#!/bin/bash
set -euo pipefail

ANSWERS=(
    56 cold 7 paris green 42 mars 8 went 25
    au 6 pacific 9 mice 32 january 60 down 81
    tokyo z def 7 12 ice commit earth 42 day
    8 pwd 720 rome iron i 999 4 ate lion
    121 portuguese 100 404 false 24 jupiter 45 spring madrid
    1024 honey ls 3 full 55 april for 6 blue
)

for answer in "${ANSWERS[@]}"; do
    output=$(python /app/next.py "$answer")
done

echo "${output##*Final token: }" > /app/result.txt
