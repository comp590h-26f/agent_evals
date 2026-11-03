---
name: commit-messages
description: Write Git commit messages using this repository's conventions when preparing a message for a staged change.
---

# Commit messages

Review the staged diff before writing the message. For authentication bug fixes,
use these team conventions:

- Start the subject with `fix(auth): ` followed by an imperative summary.
- Keep the entire subject at most 72 characters.
- Separate the subject from the body with a blank line.
- Include a `Cause: ` line explaining the defect and a `Fix: ` line explaining
  the corrected behavior. Each line must contain an explanation, not just a label.
- Describe what the diff establishes. Do not claim tests passed unless you ran them.

Write the message to the destination requested by the user. Preparing a message
does not authorize creating a commit or changing the staged files.
