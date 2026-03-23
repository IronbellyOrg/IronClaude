# Major Issue M11 — Distinguish `skipped` from `not started` in pipeline manifests

## Problem

The current pipeline manifest design uses `status: skipped` for at least one failure mode, but it does not record why the phase was skipped.

That creates an ambiguity during `--pipeline-resume`:

1. **Dependency-blocked skip** — the phase was intentionally skipped because an upstream dependency failed.
2. **Not yet started** — the phase was never dispatched because execution halted or had not reached that phase yet.

Those two states require different resume behavior:

- A dependency-blocked phase should become eligible again if its dependency is now repaired/completed.
- A not-yet-started phase should just enter the normal scheduling flow when its turn arrives.

Without a reason field, resume logic cannot tell whether `skipped` means “do not run until dependency state changes” or merely reflects “execution never got here.”

## Root cause

The manifest currently overloads lifecycle state and causal state into a single field.

- **Lifecycle state** answers: what happened to this phase?
- **Causal state** answers: why did this happen?

`status` alone is insufficient because `skipped` is terminal-looking but not semantically self-contained.

## Proposal

Add a new optional manifest field:

```yaml
skipped_reason: <string|null>
```

Use it only when `status: skipped`.

### Recommended schema

For each phase entry:

```yaml
phases:
  phase-id:
    status: pending|running|completed|failed|skipped
    skipped_reason: null|dependency_failed|manual_exclusion|conditional_false|upstream_cancelled
    dependencies:
      - other-phase-id
    artifacts: []
    artifact_checksums: {}
    last_updated: "2026-03-23T12:00:00Z"
```

## Status model

### Keep `pending` as the only representation of “not started”

This is the most important semantic rule.

- `pending` = phase has not started yet
- `running` = phase is currently executing
- `completed` = phase finished successfully
- `failed` = phase ran and failed
- `skipped` = scheduler deliberately decided not to run it for a known reason

That means **not started must never be encoded as `skipped`**.

If a phase has not yet been evaluated by the scheduler, it stays `pending`.

## Allowed `skipped_reason` values

Start narrow. Avoid an open-ended free-text field as the only source of truth.

Recommended initial enum:

- `dependency_failed`
  - One or more required upstream phases failed, so this phase could not run.
- `upstream_cancelled`
  - One or more upstream phases were cancelled/aborted, so this phase could not run.
- `manual_exclusion`
  - Operator or configuration explicitly excluded this phase.
- `conditional_false`
  - Phase was valid in the graph, but runtime conditions evaluated false.

For M11 specifically, `dependency_failed` is the critical value.

### Optional companion detail field

If the implementation wants richer debugging without weakening machine semantics, add:

```yaml
skipped_details:
  blocked_by:
    - validate
    - analyze
  message: "Skipped because validate failed"
```

But the core fix should not depend on this. The minimum viable change is still `skipped_reason`.

## Resume semantics

## Rule 1: `pending` phases are normal candidates

On resume, any phase with `status: pending` should be considered not yet attempted.

Behavior:
- Evaluate dependencies normally.
- If dependencies are satisfied, dispatch it.
- If dependencies are still unsatisfied because an upstream phase is incomplete or failed, leave it pending until the scheduler reaches a stable decision point.

## Rule 2: `skipped` + `skipped_reason: dependency_failed` is re-evaluable

On resume, phases previously skipped due to failed dependencies should **not** be treated as permanently skipped.

Behavior:
1. Inspect the current manifest state of dependencies.
2. If blocking dependencies are still failed/not completed, keep the phase skipped.
3. If all required dependencies are now completed, convert the phase back to `pending` and allow dispatch.

This is the core behavioral change needed for M11.

## Rule 3: other skip reasons remain skipped unless explicitly invalidated

Examples:
- `manual_exclusion` should remain skipped on resume.
- `conditional_false` should remain skipped unless the condition is explicitly recomputed and now true.

This prevents resume from unexpectedly reviving phases that were intentionally suppressed.

## Proposed resume algorithm

### Phase 1 — Load and normalize manifest

When `--pipeline-resume` starts:

1. Read the manifest.
2. For each phase:
   - If `status == skipped` and `skipped_reason` is absent, treat it as legacy data.
   - If `status == skipped` and `skipped_reason == dependency_failed`, mark it as re-evaluable.
   - If `status == pending`, treat it as not started.

### Phase 2 — Backward-compatibility normalization

To avoid breaking existing manifests:

- Legacy manifest with `status: skipped` and no `skipped_reason` should be interpreted conservatively.

Recommended policy:
1. If all dependencies are currently completed, downgrade legacy `skipped` to `pending`.
2. Otherwise leave it as `skipped` and annotate in memory/logging that the reason was inferred as dependency-related/unknown.

Alternative stricter policy:
- Require operator acknowledgement for legacy ambiguous entries.

Recommendation: use the first policy because it preserves resumability and minimizes operator friction.

### Phase 3 — Recompute eligibility

For every non-completed phase:

1. If `status == failed`, keep it eligible for retry according to existing retry/resume policy.
2. If `status == pending`, evaluate dependency satisfaction.
3. If `status == skipped` and `skipped_reason == dependency_failed`, re-check dependencies.
4. If dependencies are now satisfied, set:

```yaml
status: pending
skipped_reason: null
```

Then include the phase in the dispatchable set.

### Phase 4 — Dispatch by topological order

Run the normal scheduler over:
- all `pending` phases whose dependencies are satisfied
- any reactivated formerly-skipped phases

This keeps resume behavior aligned with fresh-run scheduling instead of inventing a second execution model.

## Write-time manifest rules

The scheduler should update the manifest with stricter invariants.

### When a phase is first created in the manifest

Set:

```yaml
status: pending
skipped_reason: null
```

### When a phase is skipped because dependency failed

Set:

```yaml
status: skipped
skipped_reason: dependency_failed
```

Optionally include which dependency blocked it.

### When a phase is dispatched

Set:

```yaml
status: running
skipped_reason: null
```

### When a phase completes successfully

Set:

```yaml
status: completed
skipped_reason: null
```

### When a phase fails during execution

Set:

```yaml
status: failed
skipped_reason: null
```

## Invariants

The implementation should enforce these invariants:

1. `status != skipped` => `skipped_reason == null`
2. `status == skipped` => `skipped_reason != null`
3. `pending` means no execution attempt has started
4. `completed` means artifact validation/checksum requirements passed
5. `skipped_reason: dependency_failed` means at least one dependency was non-completed at scheduling time

These invariants make the manifest machine-interpretable and testable.

## Why this is the right fix

This proposal is intentionally minimal.

It does not require:
- redesigning the scheduler
- inventing a separate resume-only state machine
- changing artifact checksum behavior
- changing topological execution rules

It only separates:
- **state** (`status`)
- **cause** (`skipped_reason`)

That is enough to make resume correct.

## Example scenarios

### Scenario A — Dependency failed, then later fixed

Initial run:

```yaml
phases:
  A:
    status: failed
    skipped_reason: null
  B:
    status: skipped
    skipped_reason: dependency_failed
    dependencies: [A]
```

Later, operator fixes A or reruns A and it becomes completed:

```yaml
phases:
  A:
    status: completed
    skipped_reason: null
  B:
    status: skipped
    skipped_reason: dependency_failed
    dependencies: [A]
```

On `--pipeline-resume`:
- Resume logic sees B was skipped because of dependency failure.
- It re-checks A.
- A is now completed.
- B is reset to `pending` and dispatched.

### Scenario B — Phase never reached

Initial run stopped early:

```yaml
phases:
  A:
    status: completed
  B:
    status: pending
  C:
    status: pending
```

On resume:
- B and C are simply normal pending phases.
- No special skip logic applies.

### Scenario C — Manual exclusion

```yaml
phases:
  security-review:
    status: skipped
    skipped_reason: manual_exclusion
```

On resume:
- It remains skipped.
- Resume does not silently reactivate it.

## Implementation steps

### 1. Extend manifest schema

Update the pipeline manifest schema/documentation so each phase entry supports:
- `status`
- `skipped_reason`

Document that `pending` is the only valid “not started” state.

### 2. Update manifest writers

Wherever the executor/scheduler marks downstream phases as skipped after dependency failure, write:

```yaml
status: skipped
skipped_reason: dependency_failed
```

Wherever phase entries are initialized, write:

```yaml
status: pending
skipped_reason: null
```

### 3. Update resume loader

When reading the manifest during `--pipeline-resume`:
- recognize `skipped_reason`
- treat `skipped/dependency_failed` as re-evaluable
- convert re-satisfied skipped phases back to `pending`

### 4. Add backward-compatibility handling

For old manifests without `skipped_reason`:
- detect ambiguous `skipped`
- infer eligibility conservatively
- write back normalized entries when safe

### 5. Improve operator visibility

Log decisions like:
- `phase B remains skipped: dependency A still failed`
- `phase B reactivated from skipped -> pending: dependency A now completed`
- `phase C remains skipped: manual_exclusion`

This makes resume behavior explainable.

## Test plan

### Unit tests

1. **Schema round-trip**
   - Manifest with `skipped_reason` serializes/deserializes correctly.

2. **Invariant enforcement**
   - `status=skipped` with null reason is rejected or normalized.
   - non-skipped status with non-null reason is rejected or normalized.

3. **Legacy manifest compatibility**
   - Old manifest lacking `skipped_reason` can still load.

### Resume behavior tests

4. **Pending starts normally**
   - `pending` phase with completed dependencies is dispatched on resume.

5. **Dependency-failed skip reactivates**
   - Phase skipped with `dependency_failed` becomes `pending` once dependencies are completed.

6. **Dependency-failed skip stays skipped when blocker remains**
   - If upstream phase is still failed, the skipped phase is not dispatched.

7. **Manual exclusion stays skipped**
   - `manual_exclusion` never auto-reactivates on resume.

8. **Mixed graph resume**
   - Completed phases remain skipped from execution.
   - Pending phases dispatch normally.
   - Reactivated skipped phases enter dispatch set only after dependencies are satisfied.

### Integration test

9. **End-to-end interrupted pipeline**
   - Run a graph where upstream phase fails.
   - Confirm downstream is written as `skipped + dependency_failed`.
   - Manually repair or update upstream manifest/state to completed.
   - Resume.
   - Confirm downstream phase is dispatched and eventually completed.

## Risks and mitigations

### Risk: legacy manifests remain ambiguous

Mitigation:
- add compatibility normalization on load
- emit clear logs when inference occurs

### Risk: too many skip reasons too early

Mitigation:
- start with a small enum
- only make `dependency_failed` special in resume logic initially

### Risk: scheduler writes inconsistent combinations

Mitigation:
- centralize manifest updates behind helper functions rather than ad hoc writes
- validate invariants before persisting

## Recommended acceptance criteria

1. Manifest schema includes `skipped_reason` for phase entries.
2. `pending` is the sole representation of “not started.”
3. Downstream phases skipped because an upstream dependency failed are persisted as:
   - `status: skipped`
   - `skipped_reason: dependency_failed`
4. On `--pipeline-resume`, a phase with `status: skipped` and `skipped_reason: dependency_failed` is re-evaluated against current dependency state.
5. If all blocking dependencies are now `completed`, that phase is reset to `pending` and becomes eligible for dispatch.
6. Phases skipped for other reasons do not auto-reactivate.
7. Legacy manifests without `skipped_reason` still resume without crashing.
8. Tests cover both dependency-blocked skip and genuine not-started cases.

## Final recommendation

Implement M11 as a schema-and-resume correction, not as a broad scheduler redesign.

The cleanest solution is:

- keep `pending` for not started
- keep `skipped` for deliberate scheduler decisions
- add `skipped_reason` to explain why skipping happened
- teach `--pipeline-resume` that `skipped + dependency_failed` is a re-checkable state, not a permanent terminal state

That change is small, explicit, backward-compatible, and directly solves the ambiguity called out in M11.
