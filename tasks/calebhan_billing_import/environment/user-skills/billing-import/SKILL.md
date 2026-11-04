---
name: billing-import
description: Build the billing system's bulk import file from customer records. Use whenever asked to create, regenerate, or fix a billing import file.
---

# Billing import file

The billing system accepts one bulk import file at `/app/out/billing_import.psv`.
It rejects the whole file if any line deviates from this format.

1. First line: `#BILLING-IMPORT v2`
2. One line per customer, sorted by `customer_id` ascending:
   `customer_id|LAST, First|email|balance_cents`
   - Upper-case the last name; keep the first name as written.
   - Lower-case the email.
   - Write the balance as an integer number of cents (`12.50` -> `1250`,
     `-4.20` -> `-420`).
3. Skip customers whose `status` is `closed`.
4. Last line: `#COUNT <n>`, where `<n>` is the number of customer lines.

Do not modify the source CSV.
