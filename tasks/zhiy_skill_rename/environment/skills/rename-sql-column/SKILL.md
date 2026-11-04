---
name: rename-sql-column
description: Use when renaming a column in a SQL schema or query.
---

# Rename a SQL column

Our team generates new column names instead of choosing them by hand.

1. From this skill's directory, run `python scripts/new_name.py <current_name>`.
2. Use the printed name exactly as the new name.
3. Update every query that uses the column, and add a migration for the schema.
