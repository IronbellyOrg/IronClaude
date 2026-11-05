# Merge Log

## Metadata

- Base: Variant 1 (reviewer-1-card, analyzer), variant-1-original.md
- Executor: merge-executor agent
- Plan: refactor-plan.md (9 planned changes, 3 rejected; auto-approved 2026-11-02)
- Changes applied: 9 of 9
- Status: COMPLETE
- Date: 2026-11-02
- Output: merged-output.md

## Changes Applied

| Change | Target | Status | Before | After | Provenance tag |
|---|---|---|---|---|---|
| #1 | new row F13 | APPLIED | no after.txt finding | F13, Drift (wording), LOW: Task 4 AC says orca_close_repro.py writes after.txt but the script only prints; recommendation: run with `> after.txt`; citations tasklist:69; remediation-source.md:23; live-check/orca_close_repro.py:75-165 | Variant 2 — merged per Change #1 |
| #2 | F12 | APPLIED | category Refinement, LOW | category Drift, LOW; recommendation unchanged | Base (original, modified) — Change #2 |
| #3 | F2 | APPLIED | severity MEDIUM | severity LOW; baseline recommendation unchanged | Base (original, modified) — Change #3 |
| #4 | F5 | APPLIED | recommendation: verify by recorded pid (`kill -0`) or `pgrep -f` on the full per-test path only | recommendation: fixture runs SKILL_DIR's proxy (tests:595), so check the recorded pid by /proc/<pid>/stat state (zombie counts as gone) or by the port, not `kill -0`; never a generic pgrep/pkill; citation column gains tests:595 and INV-004 | Base (original, modified) — Change #4 |
| #5 | F3 | APPLIED | category "Regression (inherent to the goal, unplanned)", MEDIUM | category "Drift (unplanned consequence)", MEDIUM; INV-011 evidence added (ccsession:769-770, 782-784, 793-795: each update adds a permanent shim, 6 combinations later "no free shim port") | Base (original, modified) — Change #5 |
| #6 | new row F14 | APPLIED | no INV-001 finding | F14, Drift, MEDIUM: unconditional os.setsid lets a hand-started shim survive its terminal with a dead pty stderr; recommendation: setsid only when stderr is not a terminal; citations from INV-001 | invariant-probe — merged per Change #6 |
| #7 | new row F15 | APPLIED | no INV-002 finding | F15, Drift, MEDIUM: Test A greens with the subshell alone; recommendation: assert `os.getsid(shim_pid) != os.getsid(root_pid)` in Test A; citations Task 1 (plan:29); REPORT.md | invariant-probe — merged per Change #7 |
| #8 | new section "Residual risks (LOW)" | APPLIED | absent | four bullets: INV-003, INV-010, INV-013, inherited Orca descriptors (`/proc/2258510/fd`) | invariant-probe — merged per Change #8 |
| #9 | new section "Coverage and adherence" + F10 | APPLIED | absent; F10 without grep-equivalence note | section with spec-to-plan completeness (only INF-044 unmapped), QA-slice adherence 16/5/2/0, contingent grep equivalence; F10 rationale gains the Variant 2 note and citations tasklist:82; tests/unit/test_ccsession_tiers.py:30; tests/unit/test_ccsession_tag.py:28 | Variant 2 — merged per Change #9 |

Rejected items from the plan (X-003/C-005, X-001/C-004, C-002) were not applied; F1, the F2 baseline recommendation and F11 stay as in the base.

## Post-Merge Validation

- Structural integrity: PASS. One H1 (base title), findings table with 15 rows (F1-F15, contiguous ids, 6 columns on every row), the base "Checked and aligned" paragraph, then two new H2 sections. No numbered-list or checkbox lines. Provenance header comments present; a Source comment precedes every section and sits in the last cell of every changed or new row, so the table stays valid.
- Internal references resolve: PASS. F10 and F12 referenced from "Coverage and adherence" exist; INV-001, INV-002, INV-003, INV-004, INV-010, INV-011, INV-013 all exist in invariant-probe.md; every citation was copied from the base, Variant 2 or invariant-probe.md without new citations.
- New contradictions introduced: 0. The 2 Drift items in Variant 2's adherence counts (after.txt, HC5) match F13 and F12 now both labelled Drift; the base verdict ("no HIGH issues; several MEDIUM") still holds with F14 and F15 at MEDIUM; the new F5 recommendation applies to the `shim` fixture (Task 2) and does not conflict with F6's copy-path pgrep for Task 1 real-launch cleanup.

## Summary

| Planned | Applied | Failed | Skipped |
|---|---|---|---|
| 9 | 9 | 0 | 0 |
