# Final validation (item 10.2)

Date: 2026-09-20

## tests/troubleshoot/

`1 failed, 245 passed in 16.18s`
known-red e4 only.
new reds: 0

## Full suite

Reused item 8.2 capture (`pytest-full-output.txt`): `25 failed, 11536 passed, 139 skipped, 2 xpassed, 37 warnings, 1 error`. Failing set = baseline. Only T15/T19 changed after 8.2 (`ids=`, `FIX`); both still pass in the 10.2 troubleshoot run.
new reds: none

## verify-sync

`✅ All components in sync.` (re-run after item 8.4; src/tests only, make sync-dev already done)

## lint

Scoped ruff tests/troubleshoot All checks passed. Repo `make lint` E702 in `repro/boundary_fork_repro.py` pre-existing on origin/master.
