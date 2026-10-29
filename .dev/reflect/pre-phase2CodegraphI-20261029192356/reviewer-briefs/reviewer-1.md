# Reviewer 1 brief (persona: analyzer)

Plan under review: `.dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/TASK-WF-phase2CodegraphI-20261029-192001.md`. Spec: `.dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/source.md`. Mode UC-1 (pre-execution): judge whether the plan fully and correctly implements the spec, and whether each task is independently executable and its acceptance criteria can pass as written (every acceptance block runs under `bash -euo pipefail`). Classify each divergence as Authorized expansion / Necessary deviation / Drift / Regression with a `file:line` citation you Read yourself. Read-only: do not run commands or edit files. Return findings as YAML: `findings: [{id, class, severity, plan_ref, spec_ref, claim, fix}]` plus `self_audit` if you find nothing.

## T1 card excerpt

(Deviation section (D-1, D-2) and risk section of the T1 card, verbatim from `.dev/reflect/pre-phase2CodegraphI-20261029192356/t1-card.md`)

## Deviations (UC-1: plan vs spec)

- **D-1 (Drift, plan defect).** Task 16's acceptance block (plan line 278) includes the local-scope `jq -e` check inside a block that "exits 0", while the next criterion (plan line 286) and `source.md` §2.12 say a local-scope failure is a user action, not a plan failure. As written, a workspace with a local-scope Serena entry fails Task 16 although the plan is satisfied. Fix: move the local-scope check out of the exit-0 block into its own reported criterion.
- **D-2 (Necessary, clarity).** Task 5 acceptance (plan line 107) uses `$E` without defining it in the task; it is defined in `source.md` T2 step 1. A reviewer that sees only the task cannot run it. Fix: state "with `$E` as built in `./source.md` T2 step 1".
- No other deviation: task order follows the spec order with step 0 pulled before T1 as the spec requires (`source.md` "runs first, before T1").

## Risks

- Task 3 Leg B needs a logged-in `claude`; without it the plan ships `status` (Phase 3 degrades to CLI). Stated in Task 3 and Constraints (human item 6). Accepted.
- Task 13 clones committed files only; depends on Tasks 4-9 being committed (stated).
- Task 16 runs after merge on the live workspace; read-only by its text.


## Grounding hunks

### .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/TASK-WF-phase2CodegraphI-20261029-192001.md:1-287

Read the whole plan file (287 lines); cite by line.

### .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/source.md:420-722

Spec §5 task breakdown (T0-T12): Read this range; each plan task must match its spec task.

### .dev/tasks/to-do/TASK-WF-phase2CodegraphI-20261029-192001/source.md:723-786

Spec §6 progress reporting, §7 autonomy rules, §8 release order.

## Coverage slice

| Requirement / Task | Card ID | Status | Grounding |
|---|---|---|---|
| Task 16 acceptance block vs §2.12 local-scope rule | D-1 | drift | plan:278, plan:286 |
| Task 5 `$E` variable | D-2 | necessary | plan:107 |
| Spec T0-T12 → plan Tasks 1-16 order and dependencies | T1 coverage | covered | source.md:420-722 |
