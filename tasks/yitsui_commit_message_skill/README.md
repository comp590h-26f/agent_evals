# Commit message skill discovery

Write a commit message for a staged, one-line login fix. The team's message
conventions live only in the task repository's
`.agents/skills/commit-messages/SKILL.md`. The image includes that skill; no host
skills or credentials are copied into the task.

The binary pytest verifier checks the subject prefix and length, blank separator,
nonempty Cause/Fix explanations, and preservation of the staged change and tracked
working files. It accepts varied wording. It does not automatically judge whether
the summary is imperative, the explanations are factually correct, or test claims
are supported; review the trajectory for those qualitative requirements.

Validate and evaluate from the repository root:

```sh
make oracle TASKS=yitsui_commit_message_skill
make baseline TASKS=yitsui_commit_message_skill
make agent AGENT=yitsui_starter TASKS=yitsui_commit_message_skill ENV_FILE=../590_agents/.env
```

Expect oracle reward 1 and no-op baseline reward 0. The current agent may miss the
skill and fail the conventions, but shell access allows independent discovery, so
failure is not guaranteed. A passing output alone does not prove skill activation;
inspect the trajectory for a skill read. Compare discovery disabled/enabled with
the same model and inputs when skill support is implemented in `../590_agents`.

## Initial trial (2026-11-03)

Oracle earned 1 and no-op baseline earned 0. `yitsui_starter`, using the configured
`gpt-5.6-luna` model, wrote only `Fix password verification in login handler`.
It failed all four message-format checks and passed repository preservation.
Its trajectory inspected the diff, recent commits, and commit configuration,
but never read the skill. This single trial demonstrates the intended failure;
it does not establish a failure rate or the effect of adding skill support.
