# Reviewer 2 brief (persona: qa)

## T1 card excerpt

## Coverage and acceptance (qa slice)
- Scope decision. The tasklist plans Phase P0 only and defers P1-P4 to their own plans (`TL:19`). The spec states "Each phase is one written plan" (`SRC:238`) and "Later phases do not start until the earlier phase's checks in section 7 pass" (`SRC:216`). Classification: Authorized scope limit, stated in the tasklist's Constraints with the source rule cited; the low union coverage is mostly P1-P4 rows the source itself assigns to later plans.
- P0 gap G1: AC-C5 (`SRC:271-274`) is never run or recorded; `SRC:241` says a phase passes only when every common check passes. In P0 no command file is edited, so the check is vacuous, but the tasklist does not record that.
- P0 gap G2: 7.2 step 5 requires each phase report to name at least one checked run longer than the heartbeat cadence (`SRC:291`); Task 8 (`TL:118-128`) does not require it.
- P0 gap G3: if AC-0.6 finds transcripts do not name tool calls, step 5 uses `--source terminal` instead (`SRC:291`, `SRC:303`); Task 8 does not carry that fallback.
- Ordering: AC-C1 and AC-C2 run only in Task 4 (`TL:77-79`), before Tasks 5-9 add or change files; they are not re-run at the end of the phase.


## Grounding hunks

codegraph run state: index_state=unknown checked_at=n/a worktree_root=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs projectPath=/home/coder/workspaces/worktrees/IronClaude/OrcaCLICommandRefactor-Specs (use Read/Grep/Glob only)

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:1-135
The full tasklist under review (Read it whole).

### .dev/reflect/pre-TASK-WF-orcaWorkerContra-20261102-231950-20261102232329/artifacts/coverage-matrix.yaml
Wave 1B coverage matrix (101 inferred rows, p0_gaps, observations_not_counted_as_gaps).

Audit the coverage matrix AGAINST the spec body in your grounding hunks; surface any requirement-bearing span absent from the matrix (parsed or inferred) as a finding.

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:1-16
Spec body section (Read these lines).

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:17-50
Spec body section (Read these lines).

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:51-130
Spec body section (Read these lines).

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:131-186
Spec body section (Read these lines).

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:187-202
Spec body section (Read these lines).

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:203-214
Spec body section (Read these lines).

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:215-239
Spec body section (Read these lines).

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:240-372
Spec body section (Read these lines).

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:373-384
Spec body section (Read these lines).

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:385-397
Spec body section (Read these lines).

### .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/source.md:398-452
Spec body section (Read these lines).

## Coverage slice

| Requirement / Task | Status | Grounding |
|---|---|---|
| P0 scope (spec section 6 P0 row, 7.1, 7.3 P0 rows, 2.1-2.3 contract content) | see coverage-matrix.yaml rows with phase P0/all and p0_gaps | coverage-matrix.yaml |
| P1-P4 rows | deferred by tasklist Constraints | .dev/tasks/to-do/TASK-WF-orcaWorkerContra-20261102-231950/TASK-WF-orcaWorkerContra-20261102-231950.md:19 |
