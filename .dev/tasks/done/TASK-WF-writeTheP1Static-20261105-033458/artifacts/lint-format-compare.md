# Lint and format compare

- make lint: baseline rc=0, current rc=0; ruff 'All checks passed!' = True
- New ERROR lines: 0
- New WARN lines (a warning for a file that had none in the baseline; recorded, do not fail): 0
- Existing WARN lines whose size grew (recorded, do not fail): 1
  - brainstorm.md: 201 lines in the baseline, 217 lines now
- Warning count baseline: Warnings: 5; current: Warnings: 5
- LINT verdict: PASS

- ruff format --check (five test files): baseline rc=0, current rc=0
- Current output: 5 files already formatted
- FORMAT verdict: PASS
