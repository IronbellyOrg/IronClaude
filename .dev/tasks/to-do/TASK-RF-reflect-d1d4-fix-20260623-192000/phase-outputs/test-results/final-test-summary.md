# Final test regression summary

**Date:** 2026-06-24
**Command:** `env -u SUPERCLAUDE_REFLECT_WRAPPER_ACTIVE uv run pytest tests/cli/reflect/ -q`
**Raw:** `final-pytest.txt`

## Result: **145 passed, 1 xpassed** (0 failed)

## Comparison vs baseline

- Baseline (`baseline-summary.md`): 143 passed, 1 xpassed.
- Final: 145 passed, 1 xpassed.
- Delta = **+2 passing**, both in the NEW `test_reviewer_swarm_target_grounding.py`:
  - `test_snapshot_success_reports_children_only_not_full_snapshot` (the D1 falsifier — FAIL-before → PASS-after)
  - `test_disabled_path_unchanged_when_isolation_off` (default-OFF regression guard)
- The pre-existing `test_reviewer_isolation_gate.py::test_clean_committable_grounds_reviewers_in_snapshot` still passes with its sanctioned assertion update (`"snapshot"` → `"snapshot-children-only"`).
- **No previously-passing test regressed.** (The one transient `test_fix_loop` failure during the post-ruff re-run was flaky — passed 3/3 in isolation and in the final suite; documented in `../plans/d1-verify.md`.)
