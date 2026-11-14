---
schema: workflow-plan/1.2
---

# Fixture plan

## Constraints

- Keep `src/app/core.py` importable.

## Task 1: Add the guard module

Create `src/app/merge_guard.py` and `src/app/scripts/tool.sh`, and extend `src/app/core.py`.

Acceptance criteria:
- `grep -n "merge_guard" src/app/core.py` prints one line.

## Task 2: Update the docs

Edit `docs/guide.md` and `CHANGELOG.md`; model the helper on `scripts/old.sh` and call `scripts/tool.sh`.

Acceptance criteria:
- `grep -rl HOW-WE-WORK tests` prints nothing.

## Task 3: Tests

Add `tests/app/test_merge_guard.py`; keep `tests/app/test_core.py` green.

The guard keeps every retry visible to the operator, records each attempt with its reason and its outcome, refuses to hide a failed attempt behind a later success, and reports the full history of the cycle when the run ends so that nobody has to reconstruct it from scattered logs or from memory afterwards
