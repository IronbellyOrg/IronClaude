# Refactoring Plan

## Overview
- Base: Variant 1 (reviewer-1-card, analyzer)
- Incorporated: Variant 2 (reviewer-2-card, qa); invariant-probe.md findings
- Planned changes: 9; rejected: 3
- Overall risk: Low (additive rows and wording; no finding removed)

## Planned Changes

| # | Change | Source | Target in base | Approach | Rationale | Risk |
|---|---|---|---|---|---|---|
| 1 | Add finding V2-after.txt: Task 4 AC says the live-check script "writes its output to .../after.txt" but it only prints; the runner must redirect stdout (category Drift (wording), severity LOW; recommendation: run with `> after.txt`) | V2 row 1, calibrated LOW | findings table, new row F13 | append | C-006 won by V2 unanimously; calibrator lowered to LOW | Low |
| 2 | Re-categorize F12 (HC5 missing) from Refinement to Drift (LOW); recommendation unchanged | V2 row 2 | F12 | replace | X-002/C-001 won by V2 unanimously; remediation-source.md:35 says "required" | Low |
| 3 | F2 severity MEDIUM -> LOW; keep the baseline recommendation | V1 concession; calibrator borderline | F2 | replace | X-001: V1 wins the point but concedes severity | Low |
| 4 | F5 recommendation: the `shim` fixture runs SKILL_DIR's proxy (tests:595), so check the recorded pid by /proc/<pid>/stat state (zombie counts as gone) or by the port, not `kill -0`; never a generic pgrep/pkill | V1 concession + INV-004 | F5 | replace | debate concession; zombie case | Low |
| 5 | F3 category "Regression (inherent...)" -> "Drift (unplanned consequence)", MEDIUM; add INV-011 evidence that every update adds a permanent shim and 6 combinations later "no free shim port" | V2 critique + INV-011 | F3 | replace | hedged label (calibrator 0.80 clarity) | Low |
| 6 | Add finding F14 (INV-001, MEDIUM, Drift): unconditional os.setsid lets a shim started by hand through a wrapper survive its terminal with a dead pty stderr, failing every request; recommendation: call setsid only when stderr is not a terminal (ccsession path has stderr /dev/null) | invariant-probe INV-001 | findings table | append | sufficiency challenge, unaddressed by both cards | Low |
| 7 | Add finding F15 (INV-002, MEDIUM, Drift): Test A only signals ppid descendants, so it greens with the subshell alone; recommendation: also assert `os.getsid(shim_pid) != os.getsid(root_pid)` in Test A | invariant-probe INV-002 | findings table | append | sufficiency challenge | Low |
| 8 | Add a "Residual risks (LOW)" block: INV-003 (Orca may match by ORCA_TERMINAL_HANDLE/cgroup), INV-010 (orphaned test shims on hard pytest interrupt), INV-013 (errno 48 vs 98, pre-existing), inherited Orca descriptors (`/proc/2258510/fd`) | invariant-probe + orchestrator note | new section | append | transparency | Low |
| 9 | Add "Coverage and adherence" block from V2: spec-to-plan completeness (every requirement span mapped except INF-044), QA-slice adherence 16/5/2/0, contingent grep equivalence (F10 gains the V2 note) | V2 C-014, U-010, C-003 | new section + F10 | append | C-014 won by V2 | Low |

## Changes NOT Being Made

| Diff point | Non-base approach | Why base kept |
|---|---|---|
| X-003 / C-005 | V2 row 5: AC5 "Constraints-only", LOW | V1's F1 names a concrete write path (ccsession:832); kept as MEDIUM |
| X-001 / C-004 | V2 row 6: pid check is a pure strength | V1's false-failure path holds (severity lowered per change 3) |
| C-002 | V2 row 3 Refinement | identical to F11 (TIE); F11 kept |

## Risk Summary
All changes are additive or re-labels inside a review card; rollback = use variant-1-original.md.

## Review Status
Auto-approved (non-interactive), 2026-11-02.
