# COMP590H/release-skill

The agent must cut release 1.3.0 by following a team release process that only an
agent skill documents. The skill is not installed in the task image, so an agent
passes only if it ships this skill with its own skills. Add it as
`release/SKILL.md` in the agent's skills directory:

````markdown
---
name: release
description: Cut a new release of a Python package in this team's repositories. Use whenever asked to release, cut, publish, or tag a new version.
---

# Releasing a package

Our deploy pipeline only picks up releases that follow these steps exactly.

1. Set the new version in both `pyproject.toml` (`[project] version`) and the
   package's `__version__`.
2. Commit the change with the message `Release X.Y.Z`.
3. Create an **annotated** tag named `release/X.Y.Z` on that commit, with the
   message `Release X.Y.Z`. Do not use `vX.Y.Z` tags; the pipeline ignores them.

   ```sh
   git tag -a release/X.Y.Z -m "Release X.Y.Z"
   ```

4. Do not push; CI pushes tags after review.
````
