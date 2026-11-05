# Saved reviewer prompts of this package compared with the reviewer template

This note was added after the package was archived. It changes nothing else in the package: the prompts, the ledger and every other file are byte-unchanged.

## Result

The first-round prompt of each task (`artifacts/retries/T1/prompt-1-1.md` to `artifacts/retries/T9/prompt-1-1.md`) was compared with the reviewer template in `refs/qa.md` ("## Subagent prompt (when not inline)"). The check drops line 1 (the start sha, checked against the "Start sha:" slot), cuts out the seven slots and compares the rest with the template.

| Prompt | Result |
|---|---|
| T1 `prompt-1-1.md` | blank-line-only |
| T2 `prompt-1-1.md` | blank-line-only |
| T3 `prompt-1-1.md` | blank-line-only |
| T4 `prompt-1-1.md` | blank-line-only |
| T5 `prompt-1-1.md` | blank-line-only |
| T6 `prompt-1-1.md` | blank-line-only |
| T7 `prompt-1-1.md` | blank-line-only |
| T8 `prompt-1-1.md` | blank-line-only |
| T9 `prompt-1-1.md` | blank-line-only |

All nine match the template outside the slots on every non-blank line. They differ only in blank lines: each has blank lines between the slot labels where the template has none, and the blank line before "Do not trust the implementer's report." is missing.

## What this means

Under rule A (`refs/qa.md`, "## FINAL derived test"), a difference only in blank lines or trailing whitespace is a note, not `issues`. No non-blank line of any of the nine prompts differs from the template.

## Evidence

The evidence is in the package `TASK-WF-implementSavedPr-20261105-034852`. That package lives under `.dev/tasks/to-do/` until it is archived and under `.dev/tasks/done/` afterwards:

- `artifacts/prompt-check.py`: the comparison script.
- `artifacts/t6-prompt-check.txt`: its output for the nine prompts above.
- `artifacts/t6-selftest.txt`: its output for four self-test prompts (`match`, `blank-line-only`, `differs`, `differs`), which show that the script tells these cases apart.
