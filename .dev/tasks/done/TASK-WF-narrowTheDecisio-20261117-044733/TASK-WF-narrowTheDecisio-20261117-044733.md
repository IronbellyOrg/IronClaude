---
schema: workflow-plan/1.2
source: ./source.md
strategy: systematic
depth: quick
slug: TASK-WF-narrowTheDecisio-20261117-044733
version: "1"
priority: Medium
created_date: "2026-11-17"
---

# Narrow the D2 amendment wording to a Ruling

Source: ./source.md
Goal: Two sentences stop saying the person never writes any approval into a file and say only that the person never has to write the Ruling line.

## Constraints

- Documents only. Do not edit `src/superclaude/skills/sc-implement-protocol/refs/qa.md`, any code, any test, any `.claude/` file, or any file under `.dev/` other than this package.
- Keep every other word of both sentences exactly: the chat confirmation rule, "executor-invented approval", and the references to `qa.md`.
- Other owner records (a pipeline issue's grant row, an observer pass record) stay written by the owner; the new wording must not contradict that.
- Do not push, open a PR or post to GitHub.

## Phase 1: Narrow the wording

## Task 1: Narrow the D2 phrase in the worker contract

In `src/superclaude/core/WORKER-CONTRACT.md` line 57, replace the parenthetical `(decision D2, amended 2026-11-17 by the owner: no approval is ever required to be written into a file by the person)` with `(decision D2, amended 2026-11-17 by the owner: the person is never required to write a Ruling line into a file; other owner records, such as a grant row or a pass record, are still written by the owner)`.

Acceptance criteria:
- `src/superclaude/core/WORKER-CONTRACT.md` line 57 contains the new parenthetical and the rest of the line is byte-identical to before (checked with `git diff`).
- `git grep -n "no approval is ever required" src docs` prints nothing.
- `uv run pytest tests/skills/test_worker_contract.py -q` passes.

## Task 2: Narrow the matching phrase in the technical reference

Depends on: Task 1

In `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` line 722 (table row for `WORKER-CONTRACT.md:57`), replace `(D2, amended 2026-11-17: the person never has to write a file)` with `(D2, amended 2026-11-17: the person never has to write the Ruling line themselves)`.

Acceptance criteria:
- Line 722 of `docs/architecture/SUPERVISED-ORCHESTRATION-TECHNICAL-REFERENCE.md` contains the new parenthetical and the rest of the row is byte-identical to before (checked with `git diff`).
- `git grep -n "the person never has to write a file" -- . ':!.dev'` prints nothing.
- `uv run pytest tests/docs tests/core -q` passes where those folders exist.
