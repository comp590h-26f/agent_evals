# Article summary with repository source attribution

This task measures whether an agent discovers and follows
`/app/.agents/skills/source-attribution/SKILL.md` while summarizing the supplied
article. The task instruction asks only for a one-paragraph summary and does not
mention the skill or attribution. The original article includes a title and a
synthetic source URL; no browsing is needed.

The verifier has five tests: source article preservation, file existence and
nonempty content, exact attribution and spacing, one body paragraph, and topic
coverage. It compares `/app/article.md` byte for byte with `tests/original_article.md`,
a snapshot stored with the hidden tests. Content checks ignore attribution lines,
so an otherwise valid summary without attribution and an unchanged source passes
four tests and fails one. Reward is 1 only when all five tests pass.
The host regressions in `tests/test_skill_article_summary.py` exercise valid,
missing, incorrect, repeated, and misplaced attribution, paragraph formatting,
off-topic content, absent or empty output, and valid summaries paired with
unchanged, replaced, or missing source articles.

## Validation

Run from the repository root:

```sh
make check
make test
make oracle TASKS=yewons_skill_article_summary
make baseline TASKS=yewons_skill_article_summary
make agent AGENT=yewons_servant TASKS=yewons_skill_article_summary ENV_FILE=../590_agents/.env
```

Source preservation validation on November 5, 2026, in a fresh Ubuntu WSL
source snapshot:

| Validation | Result |
| --- | --- |
| `make check` | Passed Ruff lint, formatting, and Pyright. |
| `make test` | 52 passed, including 16 verifier regression cases. |
| Task oracle | Reward 1; all five verifier tests passed; zero exceptions. |
| Task baseline | Reward 0; source preservation passed and all four summary tests failed; zero exceptions. |

Logs for these task runs are under `jobs/source-integrity-validation/` (ignored
by Git).

Earlier results on November 3, 2026, before the source preservation check:

| Validation | Result |
| --- | --- |
| `make check` | Passed Ruff lint, formatting, and Pyright. |
| `make test` | 49 passed, including 13 verifier regression cases. |
| Task oracle | Reward 1; four verifier tests passed; zero exceptions. |
| Task baseline | Reward 0; all four verifier tests failed because no summary exists; zero exceptions. |
| One live `yewons_servant` run | Reward 0; three verifier tests passed and only the attribution test failed; zero exceptions. |

The live run's ATIF trace contains two shell calls: the first attempted to read
`AGENTS.md`, read `article.md`, and checked Git status; the second wrote and read
`summary.md` and checked Git status. It contains no skill discovery or skill read.
The written summary was one relevant paragraph without the required source
block. This run therefore failed specifically for omitted attribution; future
runs may behave differently. The agent implementation was not changed.

Windows did not have `make` on PATH, and the sandbox initially denied access to
Docker and the shared uv cache. The four required make targets ran successfully
in a fresh Ubuntu WSL source snapshot with a separate Linux virtual environment.
Direct Windows Harbor oracle, baseline, and live runs used escalated Docker/cache
access and also completed without execution exceptions. An initial Ruff format
check identified two formatting differences, which were fixed before validation.

Local logs are under `jobs/yewons-skill-validation/` (ignored by Git). The live
trace is at
`yewons-skill-live/yewons_skill_article_summary__MQtLKkr/agent/trajectory.json`,
and its verifier output is in the same trial's `verifier/test-stdout.txt`.
