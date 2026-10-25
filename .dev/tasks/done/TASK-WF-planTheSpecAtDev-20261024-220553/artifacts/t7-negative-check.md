# Task 7 by-hand negative check

Test file: `tests/skills/test_implement_severity_static.py`. Command for each run:
`PYTHONDONTWRITEBYTECODE=1 uv run pytest -p no:cacheprovider tests/skills/test_implement_severity_static.py -q`

Baseline before edits: 17 passed. sha256 before:
- `refs/qa.md` 37a60f437b18794b7c88864c4af35c67920385a6376a935bb45da1a63f8bf8f1
- `refs/retry.md` 3af053a9f70aeb6a02731d2b8320fa1879c34db00b72b94846c3dc1fb7c0a728

Both files were copied to /tmp before editing and restored with `cp` afterwards.

## 1. Remove the blocking-only verdict-order sentence from `refs/qa.md`

Edit: removed the sentence "After the anchor Read-back, the origin fields and the inherited cap, the parent runs the closed order of "## Verdict (exactly one)" over the parent-confirmed blocking findings only and records the result as the verdict, once; nobody rewrites a recorded verdict." (one occurrence, Verdict owner section).

Result: `1 failed, 16 passed`.
`FAILED tests/skills/test_implement_severity_static.py::test_ac03_verdict_order_fed_by_blocking_findings_only`
(AssertionError: the sentence is not in the flattened qa.md text.)

## 2. Add an unlisted line containing `halts` to `refs/retry.md`

Edit: appended `This unlisted line halts nothing.` to the end of the file.

Result: `1 failed, 16 passed`.
`FAILED tests/skills/test_implement_severity_static.py::test_ac11_every_halt_stop_ruling_site_is_classified`
(AssertionError: `['refs/retry.md:454 matches 0 entries: This unlisted line halts nothing.']`)

## Restore

- sha256 of both files after restore equals the values above (`diff` of before/after sha lists: no difference).
- `git diff --stat` before and after the check is identical (15 files changed, 614 insertions(+), 57 deletions(-); the new test file is untracked).
- Re-run after restore: 17 passed.
