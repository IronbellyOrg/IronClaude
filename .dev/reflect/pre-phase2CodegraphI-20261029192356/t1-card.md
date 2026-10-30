# Tier 1 reflection card (UC-1, pre-execution)

Plan: `.dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/TASK-WF-phase2CodegraphI-20261029-192001.md` (16 tasks, 7 phases). Spec: `source.md` in the same package (860 lines, byte-exact snapshot of the Phase 2 spec).

## Coverage

- Pass 1 (ID_REGEX) found 0 labeled ids; Pass 2 extracted 104 quote-pinned rows (`artifacts/inferred-requirements.yaml`). `coverage_degraded: parsed-sparse` (inferred 104 > parsed 0).
- Containment matching: 64/104 matched, `coverage_pct_union = 0.6154` (`artifacts/coverage-matrix.yaml`).
- Manual triage of the 40 unmatched rows (`artifacts/unmapped-triage.yaml`): 39 are covered by reference (the plan names the spec section or the test-id range, e.g. Task 4 "tests U1-U11, U20-U22 and U24"), 1 (INF-027, `source.md:212`, Coder `command -v` check) is Coder-owned by design. Real coverage gaps: 0.
- Every spec task T0-T12 maps to one plan task: T0→1, T0b→2, T2 step 0→3, T1→4, T2→5, T3→6, T3b→7, T4→8, T5→9, T6→10, T7→11, T8→12, T9→13, T10→14, T11→15, T12→16.
- Brief requirements: test command in every task's acceptance; commit point and issue-#323 comment at the end of every phase (G0-G6); decision rules in Constraints; final full verification (Task 14) and post-merge live verification (Task 16).

## Deviations (UC-1: plan vs spec)

- **D-1 (Drift, plan defect).** Task 16's acceptance block (plan line 278) includes the local-scope `jq -e` check inside a block that "exits 0", while the next criterion (plan line 286) and `source.md` §2.12 say a local-scope failure is a user action, not a plan failure. As written, a workspace with a local-scope Serena entry fails Task 16 although the plan is satisfied. Fix: move the local-scope check out of the exit-0 block into its own reported criterion.
- **D-2 (Necessary, clarity).** Task 5 acceptance (plan line 107) uses `$E` without defining it in the task; it is defined in `source.md` T2 step 1. A reviewer that sees only the task cannot run it. Fix: state "with `$E` as built in `./source.md` T2 step 1".
- No other deviation: task order follows the spec order with step 0 pulled before T1 as the spec requires (`source.md` "runs first, before T1").

## Risks

- Task 3 Leg B needs a logged-in `claude`; without it the plan ships `status` (Phase 3 degrades to CLI). Stated in Task 3 and Constraints (human item 6). Accepted.
- Task 13 clones committed files only; depends on Tasks 4-9 being committed (stated).
- Task 16 runs after merge on the live workspace; read-only by its text.

## Recommendation

Apply D-1 and D-2 to the plan; no other change.
