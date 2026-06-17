# QA Report — Structural Verification (Phase Gate 2 fix re-check)

**Topic:** WS-0 bare-review inline run path — verify PG2 consolidated findings C1–C4 outcomes
**Date:** 2026-06-16
**Phase:** fix-cycle (structural re-verification, independent PG2.5 round)
**Fix authorization:** false (REPORT ONLY)
**Fix cycle:** PG2.5 verification (1)

---

## Overall Verdict: PASS

All four consolidated issues are correctly resolved per their stated outcomes. C1/C3/C4 are
verified FIXED with live + static evidence; C2 is verified as a DOCUMENTED, correctly-REVERTED
Phase-4 deferral (acceptable per the gate rule). No new structural issues were introduced by the
fixes. The full swarm suite is green and path-scoped ruff shows exactly the two pre-existing
errors with no new findings.

---

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| C1-code | `commands.py` builds `recommended_next_command_substitutions` from succeeded workers' `final_path`s before inline `reduce_wave3` | PASS | `commands.py:1844-1882`: `succeeded_final_paths = [w.final_path for w in normalized_workers if w.status=="success" and w.final_path]`; `next_cmd_subs.setdefault("suspect_files", ",".join(...) or "<no-bare-files>")`; `setdefault("compare_files", ",".join(["<existing-review>", *succeeded_final_paths]))`; passed as `recommended_next_command_substitutions=next_cmd_subs` into `reduce_wave3(... resume=False)`. Mirrors legacy comma-join. |
| C1-test | Presence test strengthened to assert `"{suspect_files}" not in contract` + `".final.md" in contract` | PASS | `test_e2e_user_guide.py:156-158`: `assert "{suspect_files}" not in contract`; `assert "{compare_files}" not in contract`; `assert ".final.md" in contract`. |
| C1-live | Live `swarm run --lens bare-review --target <200B file> --output /tmp/pg2verif --transport stub` → contract has NO unsubstituted `{suspect_files}` | PASS | `return-contract.yaml:64-65` emits `recommended_next_command: /sc:adversarial --compare <existing-review>,/tmp/pg2verif/bare-review-00-…final.md,… --suspect-source /tmp/…final.md,…`. `grep -c "{suspect_files}\|{compare_files}"` = **0** (ABSENT). |
| C2-revert | `normalize.py` `_normalize_one` REVERTED to verbatim recipe_args forwarding (no per-worker injection) | PASS | `normalize.py:440` `result = recipe.normalize(raw, args)` — `args` forwarded unchanged; `normalize_wave2:548` `args = recipe_args or {}`; docstring L526-528 "forwarded verbatim to every recipe call". `git diff --stat HEAD` shows `normalize.py` is **NOT in the diff** (zero changes vs committed) → clean revert, no orphaned partial change. |
| C2-test | `test_normalize.py::test_recipe_args_forwarded` green | PASS | `uv run pytest tests/swarm/test_normalize.py::test_recipe_args_forwarded -q` → 1 passed. |
| C2-doc | Deferral documented with rationale in consolidated findings | PASS | `qa-consolidated-findings-pg2.md:64-74` "C2 — DEFERRED to Phase 4 (WS-B), not fixed in WS-0" with full rationale (broke shared-helper contract, broader than WS-0 mandate, WS-B byte-parity gate is correct venue) + "Recorded as accepted deferral, not an unresolved blocker." Deferral is ACCEPTABLE — not a FAIL. |
| C3 | `ws0-gate-summary.md` labels `normalize.py:73` as I001 (not F821) | PASS | `ws0-gate-summary.md:37`: "`normalize.py:73` — `I001` (import block un-sorted/un-formatted). Present pre-WS-0 … [Corrected per PG2 C3 — this was mislabeled as `F821 Logger` in an earlier draft; the real code is `I001`.]". `uv run ruff check normalize.py` confirms real code = `I001` at `normalize.py:73:1`. Matches raw `ws0-gate.txt:149-150`. |
| C4-tests-exist | New e2e tests exist | PASS | `test_e2e_user_guide.py:161` `test_label_flag_stamps_caller_label_frontmatter`; `:176` `test_reviewers_flag_rejects_below_range`; `:186` `test_target_line_cap_and_timeout_flags_accepted`. |
| C4-tests-pass | New tests pass | PASS | Covered by full-suite run (2218 passed, 0 failed); each maps to: B-4 label frontmatter stamp, B-1 `--reviewers 1` → EXIT_USAGE, B-2/B-3 flag acceptance + contract present. |
| Suite | `uv run pytest tests/swarm/ -q` = 0 failed | PASS | **2218 passed, 26 skipped, 0 failed in 11.24s** — matches claimed counts exactly. |
| Ruff-scoped | Path-scoped ruff on the 3 files shows only 2 pre-existing errors, no new | PASS | `commands.py`: 1 error `F821 Undefined name 'Logger'` at `:1712` (pre-existing forward-ref). `normalize.py`: 1 error `I001` at `:73` (pre-existing import-sort). `test_e2e_user_guide.py`: "All checks passed!". No new errors. |
| No-regression | Fixes introduced no new structural issues | PASS | git diff scoped to `commands.py` (+343, C1) and `test_e2e_user_guide.py` (+130, C4); `normalize.py` untouched (C2 revert clean). Suite green; ruff delta = 0 new. |

## Summary

- Checks passed: 12 / 12
- Checks failed: 0
- Critical issues: 0
- Issues fixed in-place: 0 (report-only)

## Issues Found

None. (No new structural issues introduced; all four consolidated findings correctly addressed.)

## Observations (non-blocking, not gate issues)

| # | Severity | Location | Observation | Note |
|---|----------|----------|-------------|------|
| O1 | INFO | `TASK-RF-…045915.md:717` | The TASK-file execution log still carries the older "`normalize.py:73` F821 Logger" mislabel and the older `2215 passed` count. | OUT-OF-SCOPE for C3, which targets `ws0-gate-summary.md` (correctly fixed). This is a historical execution log entry, not the gate-summary doc; left as-is is reasonable, but a one-line corrective note there would reduce future confusion. Does NOT affect the verdict. |

## Actions Taken

None — report-only (`fix_authorization: false`).

## Recommendations

- PASS the structural re-verification. Proceed.
- (Optional, non-blocking) Add a corrective note at `TASK-RF-…045915.md:717` for the stale F821 label / test count to keep the execution log consistent with the corrected gate-summary. Not required to pass.

---

## Confidence Gate

- **Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 4 | Grep: 4 | Glob: 0 | Bash: 6
- Every checklist item maps to a specific static read, grep, or executed command (ruff/pytest/live swarm run) cited in the Items Reviewed table.
- No UNCHECKED items. No UNVERIFIABLE items. No web research required (all claims are local-source / executable).

## QA Complete
