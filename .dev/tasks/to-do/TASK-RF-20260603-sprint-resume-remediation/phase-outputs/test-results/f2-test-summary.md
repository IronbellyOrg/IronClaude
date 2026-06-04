# F-2 Test Summary (Phase 3)

**Command:** `uv run pytest "tests/sprint/test_resume.py::TestInvariants" -v`
**Overall:** ✅ PASS — 4 passed in 0.19s (full output: `cg1-green.txt`)

## Per-test results

| Test | AC / Gap | Result | Note |
|------|----------|--------|------|
| `test_gate_hard_stops_on_last_completed_overclaim` | FR-2.4 (hard stop) | ✅ PASS | Gate still hard-STOPs on last-completed over-claim; `accept_suspect` override still flips passed. Non-regressed. |
| `test_boundary_quarantine_nondestructive` | FR-2.5 (CG-1 anchor) | ✅ PASS | `passed is True`, `quarantined == {}`, report-only non-destructive invariant intact — the `partial_paths` field add did NOT regress it. |
| `test_boundary_partial_paths_surfaced_in_report` | **CG-1 / F-2** | ✅ PASS (was RED) | `report.partial_paths` contains `phase-3-task-T03.02-output.txt` on the default report-only path. RED→GREEN. |
| `test_haiku_coherence_advisory_only` | DD-2 (NFR-3) | ✅ PASS | Advisory coherence read still advisory-only; `passed`/`validated_last` unchanged. |

## RED→GREEN evidence

- **RED:** `cg1-red.txt` — `test_boundary_partial_paths_surfaced_in_report` FAILED with `AttributeError: 'BoundaryReport' object has no attribute 'partial_paths'` (the F-2 gap: no report-only partial-paths field existed).
- **GREEN:** `cg1-green.txt` — same test PASSES; `report.partial_paths` now carries the half-written transcript path on the report-only path (Option A: field populated in `run()` independent of `cleanup_opted_in`).

## Non-regression confirmation

- **`test_boundary_quarantine_nondestructive` PASSES** — `passed is True` and `quarantined == {}` still hold; the new field is a pure report surface and never a term in `passed` (NFR-3).
- **FR-2.4 hard-stop test PASSES** — gate verdict logic unchanged.

## Verdict source

All rows reflect the actual pytest output above — no fabricated results.
