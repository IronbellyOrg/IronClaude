# Reviewer 2 brief (persona: qa)

Plan under review: `.dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/TASK-WF-phase2CodegraphI-20261029-192001.md`. Spec: `.dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/source.md`. Mode UC-1 (pre-execution): judge whether the plan fully and correctly implements the spec, and whether each task is independently executable and its acceptance criteria can pass as written (every acceptance block runs under `bash -euo pipefail`). Classify each divergence as Authorized expansion / Necessary deviation / Drift / Regression with a `file:line` citation you Read yourself. Read-only: do not run commands or edit files. Return findings as YAML: `findings: [{id, class, severity, plan_ref, spec_ref, claim, fix}]` plus `self_audit` if you find nothing.

Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.

## T1 card excerpt

(Coverage section of the T1 card, verbatim from `.dev/reflect/pre-phase2CodegraphI-20261029192356/t1-card.md`)

## Coverage

- Pass 1 (ID_REGEX) found 0 labeled ids; Pass 2 extracted 104 quote-pinned rows (`artifacts/inferred-requirements.yaml`). `coverage_degraded: parsed-sparse` (inferred 104 > parsed 0).
- Containment matching: 64/104 matched, `coverage_pct_union = 0.6154` (`artifacts/coverage-matrix.yaml`).
- Manual triage of the 40 unmatched rows (`artifacts/unmapped-triage.yaml`): 39 are covered by reference (the plan names the spec section or the test-id range, e.g. Task 4 "tests U1-U11, U20-U22 and U24"), 1 (INF-027, `source.md:212`, Coder `command -v` check) is Coder-owned by design. Real coverage gaps: 0.
- Every spec task T0-T12 maps to one plan task: T0→1, T0b→2, T2 step 0→3, T1→4, T2→5, T3→6, T3b→7, T4→8, T5→9, T6→10, T7→11, T8→12, T9→13, T10→14, T11→15, T12→16.
- Brief requirements: test command in every task's acceptance; commit point and issue-#323 comment at the end of every phase (G0-G6); decision rules in Constraints; final full verification (Task 14) and post-merge live verification (Task 16).


## Grounding hunks

### .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/source.md:1-24

Spec section range (Read it; the spec is 860 lines, so it is given as per-section ranges covering 100 percent).

### .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/source.md:25-54

Spec section range (Read it; the spec is 860 lines, so it is given as per-section ranges covering 100 percent).

### .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/source.md:55-215

Spec section range (Read it; the spec is 860 lines, so it is given as per-section ranges covering 100 percent).

### .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/source.md:216-273

Spec section range (Read it; the spec is 860 lines, so it is given as per-section ranges covering 100 percent).

### .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/source.md:274-419

Spec section range (Read it; the spec is 860 lines, so it is given as per-section ranges covering 100 percent).

### .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/source.md:420-722

Spec section range (Read it; the spec is 860 lines, so it is given as per-section ranges covering 100 percent).

### .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/source.md:723-807

Spec section range (Read it; the spec is 860 lines, so it is given as per-section ranges covering 100 percent).

### .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/source.md:808-860

Spec section range (Read it; the spec is 860 lines, so it is given as per-section ranges covering 100 percent).

### .dev/reflect/pre-phase2CodegraphI-20261029192356/artifacts/coverage-matrix.yaml

Containment matrix (104 rows).

### .dev/reflect/pre-phase2CodegraphI-20261029192356/artifacts/unmapped-triage.yaml

Orchestrator triage of the 40 unmatched rows; verify it.

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| 104 INF rows (inferred) | coverage | 64 containment + 39 by reference + 1 out of scope | artifacts/coverage-matrix.yaml |
| Brief must-keeps: test cmd per task, commit point + #323 comment per phase, decision rules, final verification | coverage | covered | plan Constraints, Tasks 2,5,8,9,13,15,16 |
