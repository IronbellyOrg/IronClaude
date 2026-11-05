# Refactor Plan: merge into base V1 (reviewer-1 card)

Approval: auto (non-interactive). Target: `merged-review-card.md`, deduplicated as D-001..D-023.

## Integrations from non-base variants

| # | Source | Target in base | Rationale (debate) | Approach | Risk |
|---|---|---|---|---|---|
| R-01 | V2 R2-01, V3 R3-05 | R1-10 -> D-002 | C-009 converged blocking; V3 adds "no fix pass can repair it" and "AC names no saved file" | Merge claims; fix = baseline `git status --porcelain` saved at Task 1 start and cited by the AC | Low |
| R-02 | V2 R2-02, V3 R3-06 | new D-006 | C-010 settled should-fix | Add finding with the saved-output fix | Low |
| R-03 | V3 R3-04 | R1-04 -> D-003 | C-004 settled should-fix; keep V3's spec-departure and cross-run evidence (orca-capabilities.md:127) | Merge evidence; classify as Drift from spec:293 | Low |
| R-04 | V3 R3-08 | R1-03 -> D-004 | C-003 settled should-fix; V3 adds the failed-start branch (orca-capabilities.md:112) | Merge; rewrite the stop rule per A-004 | Medium |
| R-05 | V3 R3-09 | R1-09 -> D-007 | C-018 agreed | Merge evidence (plan:39 kept branch collision) | Low |
| R-06 | V3 R3-03 | R1-05 -> D-009 | X-001 converged on V3's run-time rule | Replace "correct before Task 2" with a pre-run help check plus V3's record-not-correct rule | Medium |
| R-07 | V2 R2-03 | new D-012 | C-013 settled should-fix | Add | Low |
| R-08 | V3 R3-07 | new D-013 | unique, sound | Add | Low |
| R-09 | V2 R2-04..R2-09, V3 R3-01, R3-03 | new D-015, D-017..D-022 | agreed minors and unique minors | Add | Low |
| R-10 | V2 R2-05 | R1-12 -> D-016 | C-012 agreed | Split the grep-exit part of R1-12 into D-016; rest stays D-023 | Low |

## Base weaknesses fixed

| Issue in base | Better source | Fix |
|---|---|---|
| R1-05 fix edits the plan after Task 1 starts | V3 R3-03 + managed-workspace.md:43 | Help check runs before `/sc:implement` starts; in-run usage errors are recorded FAIL |
| R1-03 fix stops a worker on non-null `agentWait` | orca-capabilities.md:114, :125, :129 | Stop only on Orca's positive stall proof (transcript final agent turn with no `worker_done`, `exited` liveness) or after the person explicitly says to stop; otherwise record FAIL and ask the person |
| R1-02 should-fix stands but leaves INV-007 open | invariant probe | State in D-005 that it should be applied with the blocking fixes |
| R1-06, R1-11 weak | calibration | Keep D-010 at should-fix (agreed with T1, cheap); downgrade R1-11 to minor D-014 |

## Changes not made

- F-016 (Depends-on line): rejected; plan:35 makes Task 4 depend on Task 2 (C-016).
- F-017 move of the procedure out of Constraints: not adopted; kept as minor D-019 with V3's rule.
- R3-03's claim that FINAL loses the procedure: dropped as wrong (qa.md:310 gives FINAL the full plan).
- `reviewer-2-calibration.md`'s note that Task 5's `git add .dev/tasks` stages the reflect folder: dropped as wrong (`.dev/reflect/` is outside `.dev/tasks/`).
- V2's blocking severity for D-006 and V3's blocking severity for D-003: not adopted (C-010, C-004).
- T1's blocking severity for D-004 and D-005: not adopted (C-003, C-002).
