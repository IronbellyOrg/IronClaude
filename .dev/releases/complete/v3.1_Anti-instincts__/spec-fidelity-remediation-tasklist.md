# Spec-Fidelity Remediation Tasklist

## Scope
Align these documents before the next `spec-fidelity` rerun:
- `/config/workspace/IronClaude/.dev/releases/current/v3.1_Anti-instincts__/anti-instincts-gate-unified.md`
- `/config/workspace/IronClaude/.dev/releases/current/v3.1_Anti-instincts__/roadmap.md`

## Phase 1 — Canonical spec contradictions

### Task S1 — Normalize file inventory in spec
**Target:** `anti-instincts-gate-unified.md`

**Work**
- Replace the contradictory `New Files (4 source + 4 test)` section with a single authoritative 12-file inventory.
- Ensure the earlier file inventory, expanded test list, and total-impact counts all agree.

**Dependencies:** none

**Acceptance criteria**
- Every spec file-count reference agrees on `4 source + 8 test = 12 files`.
- No section in the spec still implies only 8 new files.
- The spec and roadmap file inventories can be compared without arithmetic ambiguity.

### Task S2 — Resolve sprint-file ownership contradiction in spec
**Target:** `anti-instincts-gate-unified.md`

**Work**
- Reconcile the spec’s modified-files table with the later coordination table.
- Decide whether `src/superclaude/cli/sprint/models.py` and `src/superclaude/cli/sprint/executor.py` are in scope for Anti-Instincts.
- Make both sections say the same thing.

**Dependencies:** none

**Acceptance criteria**
- The modified-files table and coordination table agree on sprint-file scope.
- A reader can tell whether sprint files are truly part of this release without cross-section conflict.

### Task S3 — Resolve D-03/D-04 coexistence policy in spec
**Target:** `anti-instincts-gate-unified.md`

**Work**
- Replace the unresolved `OR` branch with a single canonical policy.
- If defense-in-depth is the intended decision, state it explicitly and remove the alternative branch.

**Dependencies:** none

**Acceptance criteria**
- The spec no longer leaves D-03/D-04 coexistence unresolved.
- The roadmap’s chosen policy can be judged against a single source-of-truth rule.

### Task S4 — Reframe shadow validation placement in spec
**Target:** `anti-instincts-gate-unified.md`

**Work**
- Move or restate shadow validation so it clearly occurs after sprint integration, not inside an “immediate” phase.
- Align phase wording with the actual dependency chain.

**Dependencies:** S2

**Acceptance criteria**
- Shadow validation is described as post-sprint-integration rollout validation.
- Phase sequencing no longer conflicts with roadmap phase structure.

## Phase 2 — Roadmap internal contradictions

### Task R1 — Fix `off` mode contradiction in roadmap
**Target:** `roadmap.md`

**Work**
- Remove `no computation until explicitly enabled` style wording.
- Ensure all roadmap prose and tables agree that in `off` mode the gate still evaluates but the result is ignored by sprint infrastructure.

**Dependencies:** S3

**Acceptance criteria**
- Executive summary, rollout prose, and rollout table all describe `off` mode consistently.
- No roadmap text implies both “gate fires” and “no computation.”

### Task R2 — Reconcile requirement totals in roadmap
**Target:** `roadmap.md`

**Work**
- Recompute or restate the Executive Summary requirement totals.
- Make the top-line counts consistent with the requirement coverage matrix.
- If exact totals are intentionally approximate, remove the misleading numeric split.

**Dependencies:** none

**Acceptance criteria**
- Executive Summary counts reconcile with the roadmap’s own matrix.
- No arithmetic mismatch remains between summary and enumerated requirements.

## Phase 3 — Roadmap omissions from spec contract

### Task R3 — Complete Phase 2.1 gate-definition tasking
**Target:** `roadmap.md`

**Work**
- Add `min_lines=10` to the `ANTI_INSTINCT_GATE` definition task.
- Add `gate_scope=GateScope.TASK` to the gate-definition task, not just executor-step wiring.

**Dependencies:** S1, R1

**Acceptance criteria**
- Phase 2.1 explicitly captures all gate-definition fields required by the spec.
- A tasklist generator would not omit `min_lines` or `gate_scope`.

### Task R4 — Add explicit KPI integration task
**Target:** `roadmap.md`

**Work**
- Add a dedicated sprint-side task for KPI report integration.
- Mention `build_kpi_report()` / KPI aggregation behavior explicitly.

**Dependencies:** S2

**Acceptance criteria**
- Roadmap includes a discrete KPI integration task.
- Sprint-side implementation scope explicitly mentions KPI aggregation.

### Task R5 — Add explicit executor import/update task
**Target:** `roadmap.md`

**Work**
- Add a task for the executor import/update bundle tied to sprint integration.
- Explicitly cover the required import/update behavior instead of leaving it implicit.

**Dependencies:** S2

**Acceptance criteria**
- The roadmap contains a concrete task for the import/update bundle.
- Executor wiring scope is fully represented in planning text.

## Phase 4 — Low-priority traceability cleanup

### Task C1 — Normalize OQ/NFR traceability
**Targets:** `anti-instincts-gate-unified.md`, `roadmap.md`

**Work**
- Either add a canonical OQ/NFR registry to the spec, or replace roadmap OQ/NFR citations with direct section references.
- Prefer the minimum change that restores traceability without inventing new ambiguity.

**Dependencies:** S3, R2

**Acceptance criteria**
- OQ/NFR references are traceable to a defined source.
- The roadmap no longer depends on undefined identifiers.

### Task C2 — Normalize fingerprint helper naming
**Targets:** `anti-instincts-gate-unified.md`, `roadmap.md`

**Work**
- Make the helper/check naming consistent between roadmap task text and spec helper function naming.
- Keep semantic-check label and helper function intent unambiguous.

**Dependencies:** none

**Acceptance criteria**
- Roadmap and spec use one consistent naming scheme for the fingerprint coverage helper/check.
- No fidelity reviewer could reasonably flag a helper-name mismatch.

## Execution order
1. S1, S2, S3 in parallel if desired
2. S4 after S2
3. R1 after S3
4. R2 anytime
5. R3 after S1 and R1
6. R4 and R5 after S2
7. C1 after S3 and R2
8. C2 anytime

## Checkpoints

### Checkpoint A — Spec stabilized
Required complete:
- S1
- S2
- S3
- S4

### Checkpoint B — Roadmap stabilized
Required complete:
- R1
- R2
- R3
- R4
- R5

### Checkpoint C — Optional cleanup
Optional before rerun:
- C1
- C2

## Final verification

### Task V1 — Regenerate fidelity verdict
**Command**
```bash
superclaude roadmap run /config/workspace/IronClaude/.dev/releases/current/v3.1_Anti-instincts__/anti-instincts-gate-unified.md --resume
```

**Success criteria**
- `spec-fidelity` reruns against the corrected spec and roadmap.
- Previously stale findings do not recur.
- No HIGH-severity contradictions remain.

## Deliverable
This file is the execution tasklist for converging spec and roadmap before the next fidelity run.
