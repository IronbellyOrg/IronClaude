# QA Report — Post-Completion Structural (Cycle 2)

**Topic:** `superclaude sprint rerun-tasks` (v4.3.0) — SHA-guard self-trip fix verification
**Date:** 2026-06-02
**Phase:** task-integrity / fix-cycle (structural)
**Fix cycle:** 2
**Fix authorization:** true
**Scope:** Verify the SHA-guard self-trip fix resolves the cycle-1 blocking defect, introduces no regression, does not defeat the guard, and the cycle-1 PASS verdict still holds.

---

## Overall Verdict: PASS

The cycle-1 blocking defect (SHA-guard self-trip) is resolved. The guard still catches real operator edits (NOT defeated / not always-pass). No regressions. No new issues found. No in-place fixes required.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Fix correctness — both sites use same stripped helper; helper strips only provenance block; `compute_tasklist_sha256` unaltered | PASS | Helper at `rerun_tasks.py:688-701` uses `_split_rerun_block(content)[1]` then `hashlib.sha256(...).hexdigest()`, OSError→`""`. Both sites (`:1292` step-4, `:1373` step-12) call it, both on `phase_obj.file`. `recovery.py:238-247` `compute_tasklist_sha256` unchanged (whole-file stream hash). `import hashlib` at `:26`. |
| 2 | Guard not defeated — real operator edit outside block still aborts | PASS | AC5 test `test_source_tasklist_sha_mismatch_aborts` (`test_rerun_tasks_failure_modes.py:288`) appends `"\nedited mid-flight\n"` (plain content, outside RERUN block) and asserts exit≠0 + byte-exact abort. PASSED. `test_force_merge_proceeds_with_warning` confirms `--force-merge` still bypasses. PASSED. |
| 3 | Happy path fixed — full merge-back without `--force-merge`, non-trivial | PASS | `test_merge_back_succeeds_without_force_merge` (`test_rerun_tasks_e2e.py:333`), class `@pytest.mark.integration` (`:320`). No `--force-merge`. Asserts exit 0, no abort, "Rerun merged", AND originals renamed `*.failed-<ts>`, provenance block written, `recovery_history` appended, `{T07.11,T07.12}` merged into result.json. PASSED. Genuinely exercises merge-back. |
| 4 | Blast radius — stored `source_tasklist_sha256` is audit-only, never re-compared vs whole-file hash | PASS | Grep: `source_tasklist_sha256` written to bundle (`:1393`) + audit JSON (`recovery.py:511`) only; never read back for comparison. `end_tasklist_sha256` (`recovery.py:675`) computed fresh whole-file, audit-only. Guard compares `source_sha`(`:1292`) vs `current_sha`(`:1373`) — both stripped, self-consistent. The two SHA families never cross-compared. |
| 5 | No regression — full suite + ruff | PASS | `uv run pytest` 7 sprint files: **233 passed**. `uv run ruff check` rerun_tasks.py + e2e test: **All checks passed!** |
| 6 | Cycle-1 PASS items intact (12 flags, classification, 7-step merge) | PASS | `git diff HEAD` on rerun_tasks.py = **+19/-2**: only `import hashlib`, the new helper, two call-site swaps. Flag surface (`commands.py` options), classification ladder, merge steps untouched. `compute_tasklist_sha256` import retained (still used `:175`). |

## Summary
- Checks passed: 6 / 6
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0

## Issues Found
None.

## Notable Observation (non-blocking, by design)
The bundle's `source_tasklist_sha256` (now the **stripped** hash, `:1393`) differs from the sub-tasklist frontmatter `source_tasklist_sha256` (the **whole-file** hash via `compute_tasklist_sha256` at `extract_phase_subset` `:175`). Both are audit-only and are never compared against each other or against the stripped guard hash (criterion 4), so the divergence is benign. Flagged for awareness only — not a defect.

## Actions Taken
None — fix verified correct as-applied; no in-place changes needed.

## Confidence Gate
- **Confidence:** Verified: 6/6 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 6 | Grep: 4 | Glob: 0 | Bash: 6 (2 pytest runs + ruff + greps + git diff)
- No UNCHECKED or UNVERIFIABLE items.
- No web research performed (purely local source-truth verification).

## QA Complete

VERDICT: PASS
