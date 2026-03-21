# Adversarial Compare: v3.1 Anti-Instincts Gate <- TurnLedger Integration

> **Date**: 2026-03-20
> **Plans compared**: Alpha (Design-First), Beta (Spec-First), Gamma (Interleaved)
> **Spec**: `anti-instincts-gate-unified.md`
> **Design**: `design.md` (v3.1 TurnLedger + TrailingGateRunner)

---

## Consensus (all 3 agree)

All three plans agree on the following findings with identical section targeting and change nature:

1. **Section 8 (Gate Definition) requires modification** -- All plans identify that `ANTI_INSTINCT_GATE` must document its relationship to `gate_rollout_mode` and `resolve_gate_mode()`. All agree the gate currently has no awareness of the TurnLedger/TrailingGateRunner infrastructure.

2. **Section 9 (Executor Integration) requires modification** -- All plans identify that `_run_anti_instinct_audit()` and its Step definition need documentation about TurnLedger interaction, `retry_limit=0` rationale, and the boundary between roadmap and sprint pipelines.

3. **Section 12 (File Change List) requires modification** -- All plans agree the file list must expand to address TurnLedger integration files and coordination/conflict analysis.

4. **Section 13 (Implementation Phases) requires modification** -- All plans agree the phasing must address TurnLedger integration ordering and rollout mode considerations.

5. **Section 14 (Assumptions) requires modification** -- All plans agree new assumptions (A-011+) are needed for TurnLedger availability, `gate_rollout_mode` defaults, and retry/budget interaction.

6. **Sections 1-7, 10, 11, 15, 16 are unchanged** -- All plans agree these sections (Problem Statement, Evidence, Architecture, Modules 1-4, Prompts, Contradictions, Subsumption, Rejected Alternatives) require no modification. All four detection modules are pure-Python functions with zero TurnLedger interaction.

7. **`gate_rollout_mode` defaults to `"off"`** -- All plans agree the default must be backward-compatible with no behavioral change for existing users.

8. **`TurnLedger` must be None-safe** -- All plans agree that when TurnLedger is absent (standalone roadmap run), all code paths must degrade gracefully.

9. **`retry_limit=0` is correct for the anti-instinct step** -- All plans agree deterministic checks should not retry, and all note this sidesteps budget concerns.

10. **No merge conflicts between Anti-Instincts and TurnLedger** -- All plans agree the two specs modify different executor files (`roadmap/executor.py` vs `sprint/executor.py`) with additive-only changes to shared `pipeline/gates.py`.

11. **TurnLedger migration to `pipeline/models.py` is a separate concern** -- All plans note the cross-release recommendation to move TurnLedger from `sprint/models.py` to `pipeline/models.py` but agree the anti-instinct spec should not own this.

---

## Majority Agreement (2 of 3 agree)

### 1. Anti-instinct gate should participate in sprint-level trailing gate pipeline (Beta + Gamma agree; Alpha dissents)

**Beta and Gamma** both recommend wiring the anti-instinct gate into `run_post_task_gate_hook()`, `TrailingGateRunner.submit()`, `DeferredRemediationLog`, and the reimbursement loop when running inside a sprint context. They propose new sections (9.5/9.6) for sprint executor integration and KPI report integration.

**Alpha dissents**: Alpha explicitly states the anti-instinct gate is a roadmap-pipeline gate, NOT a sprint-pipeline trailing gate, and is NOT governed by `gate_rollout_mode`. Alpha recommends a "TurnLedger Non-Applicability" section (8.5) that categorically excludes TurnLedger from the anti-instinct gate. Alpha's position is that roadmap gates are release-scoped and always blocking, so rollout semantics do not apply.

**Assessment**: This is the central architectural disagreement. Alpha's reading is more conservative and preserves the roadmap/sprint pipeline boundary. Beta and Gamma assume a nested execution model (roadmap invoked within sprint) that Alpha does not address. **Resolution**: see Contradictions section.

### 2. `gate_rollout_mode` applies to anti-instinct gate (Beta + Gamma agree; Alpha dissents)

Beta and Gamma both propose rollout mode behavior matrices showing how shadow/soft/full modes affect the anti-instinct gate. Alpha states rollout mode is irrelevant because roadmap gates are always blocking via `resolve_gate_mode()` returning BLOCKING for `GateScope.RELEASE`.

**Assessment**: Depends on the pipeline domain question above.

### 3. `SprintGatePolicy` activation is a cross-cutting dependency (Beta + Gamma agree; Alpha does not mention)

Beta and Gamma both identify that `SprintGatePolicy.build_remediation_step()` must be instantiated for gate remediation to work (analyze.md Finding F-3). Alpha does not mention `SprintGatePolicy` at all.

**Assessment**: Relevant only if the gate participates in the sprint pipeline. Consistent with the Beta/Gamma architectural view.

### 4. Explicit KPI reporting boundary (Alpha + Gamma agree; Beta assumes integration)

Alpha and Gamma both note the boundary between roadmap-pipeline gate results and sprint-level KPI reporting. Alpha says they do NOT feed into `build_kpi_report()`. Gamma says they feed in only when the roadmap runs inside a sprint.

Beta assumes anti-instinct results always feed into `build_kpi_report()` without distinguishing the execution context.

**Assessment**: Gamma's conditional approach (feed into KPI only when in sprint context) is the most nuanced and correct.

---

## Unique Findings (only 1 plan identified)

### Alpha-only findings:

1. **Coordination table for merge conflicts** (Section 12) -- Alpha provides a detailed file-by-file conflict risk table showing which files each spec touches. Neither Beta nor Gamma provide this granular analysis. **Value**: High -- prevents unnecessary sequencing of parallel work.

2. **`resolve_gate_mode()` invariant as defense-in-depth** -- Alpha documents that even though the roadmap pipeline does not call `resolve_gate_mode()`, the function would return BLOCKING for release-scoped gates. This is an invariant worth documenting. **Value**: Medium -- defense-in-depth documentation.

3. **Explicit dependency graph for assumptions** (A-011 <-> Section 8 coexistence) -- Alpha traces which assumptions support which section claims and notes they must stay paired. **Value**: Medium -- prevents orphaned invariants.

### Beta-only findings:

1. **Rollout mode behavior matrix** (Section 9.6) -- Beta provides a detailed table showing gate behavior across all four rollout modes (off/shadow/soft/full) with columns for logging, remediation, TaskResult mutation, and reimbursement. **Value**: High -- removes ambiguity about mode semantics if the gate participates in sprint pipeline.

2. **Enforcement tier vs rollout mode distinction** -- Beta explicitly separates `enforcement_tier="STRICT"` (criteria strictness: zero tolerance on semantic checks) from `gate_rollout_mode` (consequence of failure: log/warn/block). **Value**: High -- prevents semantic confusion.

3. **Scope creep warning** -- Beta explicitly warns that adding TurnLedger wiring roughly doubles the executor.py diff and recommends considering whether TurnLedger wiring is a separate PR. **Value**: High -- pragmatic implementation concern.

4. **Reimbursement applies to upstream merge step, not anti-instinct step** -- Beta clarifies that since the anti-instinct step consumes 0 LLM turns, reimbursement applies to the merge step's turn cost. **Value**: High -- prevents incorrect reimbursement accounting.

5. **Threading concern with TrailingGateRunner** -- Beta notes that `TrailingGateRunner.submit()` runs on a daemon thread, which is unnecessary overhead for a <1s synchronous operation. Suggests special-casing. **Value**: Medium -- performance consideration.

### Gamma-only findings:

1. **Dual execution context** (Effect 2) -- Gamma uniquely identifies that the anti-instinct step must work in two contexts: (a) standalone roadmap pipeline (no TurnLedger, legacy pass/fail) and (b) roadmap pipeline invoked from within a sprint (TurnLedger available, economics active). Both paths must be defined. **Value**: Critical -- this is the key architectural insight that resolves the Alpha vs Beta/Gamma disagreement.

2. **Structural audit budget impact** (Effect 5) -- Gamma identifies that the structural audit (Section 9 Change 1) has an indirect budget impact in sprint context: if it fails in STRICT mode, the sprint task fails and debits actual turns with no reimbursement. **Value**: Medium -- non-obvious interaction effect.

3. **DeferredRemediationLog x retry_limit=0 interaction** (Effect 4) -- Gamma traces the exact behavior: failure enters remediation path but immediately exits with `BUDGET_EXHAUSTED` since no retry budget is allocated. **Value**: Medium -- clarifies non-obvious edge case.

4. **Per-gate-type reimbursement rate** as future consideration (Effect 3) -- Gamma notes that all gates currently share a single `reimbursement_rate` but future gates may need type-specific rates. **Value**: Low -- future extensibility note only.

5. **Section 16.5: TurnLedger Integration Contract** -- Gamma proposes a standalone section that explicitly defines the credit/debit/remediation interaction. Neither Alpha nor Beta propose a dedicated integration contract section. **Value**: High -- centralizes the economic interaction model.

---

## Contradictions

### Contradiction 1: Pipeline Domain -- Is the anti-instinct gate a roadmap-only gate or a dual-context gate?

- **Alpha**: The anti-instinct gate is exclusively a roadmap-pipeline artifact. TurnLedger does not apply. A "Non-Applicability" section should make this explicit. No sprint wiring needed.
- **Beta**: The anti-instinct gate must participate in the sprint trailing gate pipeline. The executor integration must wire into `run_post_task_gate_hook()`, `TrailingGateRunner.submit()`, `DeferredRemediationLog`, and reimbursement.
- **Gamma**: The anti-instinct gate operates in both contexts. In standalone roadmap runs, it operates in legacy pass/fail mode. When the roadmap pipeline is invoked from within a sprint, it participates in TurnLedger economics.

**Resolution**: Gamma's dual-context model is the most evidence-backed. The cross-release summary states that roadmap pipelines can be invoked as sprint tasks (`superclaude sprint run` with a tasklist including roadmap generation). Alpha is correct that the gate lives in the roadmap pipeline, but wrong that it never encounters TurnLedger. Beta is correct that sprint-level wiring is needed, but overstates it by implying the gate always participates in trailing evaluation. **Gamma wins**: define both paths explicitly.

### Contradiction 2: `GateScope` assignment

- **Alpha**: The anti-instinct gate is `GateScope.RELEASE` (roadmap gates are release-scoped by definition). `resolve_gate_mode()` returns BLOCKING.
- **Beta**: Proposes `GateScope.TASK` for trailing evaluation, `GateScope.RELEASE` for blocking. Implies dual scope.
- **Gamma**: Proposes `GateScope.TASK` as default.

**Resolution**: `GateScope.TASK` is correct for the trailing gate evaluation path (when invoked in sprint context). The roadmap pipeline's synchronous gate evaluation does not use `resolve_gate_mode()` at all (Alpha is correct about this). The gate scope field is consumed only by `resolve_gate_mode()`, which is sprint-pipeline infrastructure. **Gamma wins**: `GateScope.TASK` with documentation that roadmap-pipeline evaluation bypasses scope resolution entirely.

### Contradiction 3: New sections -- Non-Applicability vs Integration Contract

- **Alpha**: New section 8.5 "TurnLedger Non-Applicability" -- categorically excludes TurnLedger.
- **Beta**: New sections 9.5 (TurnLedger Interaction Model) + 9.6 (Rollout Mode Behavior Matrix) -- full integration.
- **Gamma**: New sections 9.5 (Sprint Executor Integration) + 9.6 (KPI Report Integration) + 16.5 (TurnLedger Integration Contract).

**Resolution**: Alpha's non-applicability section is incorrect given the dual-context model. Beta's rollout mode behavior matrix is valuable. Gamma's integration contract is the most complete. **Merged**: use Gamma's section structure (9.5, 9.6, 16.5) with Beta's rollout mode matrix included in 9.5 and Alpha's invariant documentation retained as a subsection.

---

## Completeness Assessment

### Which plan was most thorough?

**Alpha** was most thorough on the "unchanged" sections -- providing line-number references and explicit reasoning for each section's non-modification. Alpha also provided the most detailed cross-reference tracking and interaction effect analysis between its own proposed changes.

**Beta** was most thorough on the sprint-pipeline integration mechanics -- providing the most detailed edit specifications for executor wiring, rollout mode behavior, and reimbursement accounting.

**Gamma** was most thorough on interaction effects -- identifying 5 distinct cross-cutting effects where Alpha found 3 and Beta found 4. Gamma's dual-context insight was the key differentiating finding.

### Which plan identified the most cross-cutting concerns?

**Gamma** (5 interaction effects), followed by **Beta** (4 interaction effects), then **Alpha** (3 interaction effects). Gamma uniquely identified the structural audit budget impact and the DeferredRemediationLog x retry_limit=0 edge case.

### Were any spec sections missed by ALL plans?

No spec sections were missed by all three plans. All plans correctly identified the same set of unchanged sections (1-7, 10, 11, 15, 16) and the same set of modified sections (8, 9, 12, 13, 14). The differences are in the nature and extent of the modifications, not in which sections are targeted.

**However**: No plan addressed whether Section 3 (Architecture) should include a diagram note about the dual execution context (standalone vs sprint-invoked roadmap pipeline). This is a minor gap -- the architecture diagram shows the roadmap pipeline flow, which is correct, but does not indicate the optional TurnLedger overlay when invoked from sprint context.

---

## Merged Refactoring Plan

### Section 3: Architecture (minor addition)

- **Change**: Add a note to the pipeline position diagram indicating that when the roadmap pipeline is invoked as a sprint task, TurnLedger economics overlay the gate evaluation path. The diagram itself is unchanged.
- **Edits**: After the architecture diagram, add: "When the roadmap pipeline executes within a sprint task context, gate results propagate to the sprint-level `TrailingGateRunner` and `TurnLedger` for economic tracking. In standalone mode, gate evaluation is synchronous pass/fail with no budget interaction."
- **Cross-refs**: Section 9.5 (new), Section 16.5 (new).
- **Risk**: None -- documentation-only addition.

### Section 8: Gate Definition (ANTI_INSTINCT_GATE)

- **Change**: (1) Add `gate_scope: GateScope = GateScope.TASK` to `ANTI_INSTINCT_GATE` so `resolve_gate_mode()` can dispatch correctly when the gate runs in sprint context. (2) Document the distinction between `enforcement_tier="STRICT"` (criteria strictness) and `gate_rollout_mode` (consequence of failure). (3) Expand "Coexistence with Unified Audit Gating" to cover TurnLedger/TrailingGateRunner coexistence with dual-context semantics.
- **Edits**:
  - Add `gate_scope` field to the `ANTI_INSTINCT_GATE` definition.
  - After the "Coexistence with Unified Audit Gating D-03/D-04" paragraph (spec lines 1077-1083), add:

    ```markdown
    ### Coexistence with Sprint-Pipeline TurnLedger/TrailingGateRunner (v3.1)

    The `ANTI_INSTINCT_GATE` operates in the roadmap pipeline
    (`src/superclaude/cli/roadmap/executor.py`) and is evaluated synchronously
    by `gate_passed()` after the anti-instinct audit step writes its output.

    **Dual execution context**:
    - **Standalone roadmap** (`superclaude roadmap run`): Gate evaluates in
      synchronous pass/fail mode. No TurnLedger, no reimbursement, no
      DeferredRemediationLog. Failure halts the pipeline (retry_limit=0).
    - **Sprint-invoked roadmap** (`superclaude sprint run` with roadmap task):
      Gate result propagates to the sprint-level TrailingGateRunner. Behavior
      is governed by `SprintConfig.gate_rollout_mode` (off/shadow/soft/full).

    **Enforcement tier vs rollout mode**: `enforcement_tier="STRICT"` means
    the semantic checks have zero tolerance (all 3 must pass). `gate_rollout_mode`
    governs the *consequence* of failure:
    - `off`: gate fires, result ignored by sprint infrastructure
    - `shadow`: gate fires, result logged to ShadowGateMetrics, no pipeline effect
    - `soft`: gate fires, failure logged as warning, remediation attempted, no TaskResult mutation
    - `full`: gate fires, failure blocks, remediation attempted, TaskResult set to FAIL on exhaustion

    The `gate_passed()` function from `pipeline/gates.py` is shared between
    roadmap-pipeline synchronous checks and sprint-pipeline trailing gate
    evaluation. The function signature is unchanged.
    ```

- **Cross-refs**: Section 9 (Executor Integration), Section 9.5 (new Sprint Executor Integration), Section 11 (X-007 enforcement tier).
- **Risk**: If `gate_scope` is omitted, `resolve_gate_mode()` cannot dispatch correctly in sprint context. If enforcement_tier vs rollout_mode is not clarified, implementers will conflate criteria strictness with failure consequence.

### Section 9: Executor Integration

- **Change**: (1) Add `gate_scope=GateScope.TASK` to the Step definition in Change 2. (2) Document `retry_limit=0` rationale and its interaction with TurnLedger budget. (3) Add KPI reporting boundary note. (4) Document that remediation path for anti-instinct failure re-runs the upstream merge step, not the anti-instinct check itself. (5) Add imports for `TrailingGateResult` and `DeferredRemediationLog` in Change 4.
- **Edits**:
  - In Change 2 (Step definition), add `gate_scope=GateScope.TASK` and annotate:

    ```python
    Step(
        id="anti-instinct",
        prompt="",  # Non-LLM step; executor handles directly
        output_file=out / "anti-instinct-audit.md",
        gate=ANTI_INSTINCT_GATE,
        gate_scope=GateScope.TASK,
        timeout_seconds=30,  # Pure Python, <1s expected
        inputs=[config.spec_file, extraction, merge_file],
        retry_limit=0,  # Deterministic; retry produces same result.
                        # Remediation (if available) re-runs the upstream
                        # merge step, not this check. DeferredRemediationLog
                        # records the failure but exits with BUDGET_EXHAUSTED
                        # immediately (no retry budget allocated).
    ),
    ```

  - After Change 3 (`_run_anti_instinct_audit()`), add:

    ```markdown
    **KPI Reporting Boundary**: In standalone roadmap mode, anti-instinct
    audit results are self-contained roadmap-pipeline artifacts. They do NOT
    feed into `build_kpi_report()` (sprint/kpi.py). In sprint-invoked mode,
    gate results are wrapped in `TrailingGateResult` and accumulated into
    the sprint-level `_all_gate_results` list for KPI aggregation.
    ```

  - In Change 4, add imports: `TrailingGateResult`, `DeferredRemediationLog`.

- **Cross-refs**: Section 8 (gate definition), Section 9.5 (new), Section 12 (file change list).
- **Risk**: Without the KPI boundary note, implementers may attempt to pipe roadmap gate results into sprint KPI in standalone mode. Without the remediation note, implementers may try to retry the anti-instinct check itself (pointless for deterministic checks).

### Section 9.5 (New): Sprint Executor Integration

- **Change**: New section defining how anti-instinct gate results flow through the sprint pipeline when the roadmap is invoked as a sprint task.
- **Content**:

  ```markdown
  ### 9.5 Sprint Executor Integration

  When the roadmap pipeline executes within a sprint task (via `superclaude sprint run`),
  the anti-instinct gate result participates in the sprint-level gate evaluation lifecycle:

  1. `_run_anti_instinct_audit()` executes as normal (roadmap pipeline)
  2. Gate result is wrapped in `TrailingGateResult(passed, evaluation_ms, gate_name)`
  3. Result submitted to sprint-level `_all_gate_results` accumulator
  4. On PASS (when `gate_rollout_mode` is "soft" or "full"):
     `ledger.credit(int(upstream_merge_turns * ledger.reimbursement_rate))`
     Note: reimbursement applies to the upstream merge step's turn cost,
     not the anti-instinct step (which consumes 0 LLM turns).
  5. On FAIL:
     `remediation_log.append(gate_result)` -- failure recorded
     Remediation re-runs the upstream merge step, not the anti-instinct check
     `DeferredRemediationLog` entry exits with BUDGET_EXHAUSTED (retry_limit=0)
  6. `ShadowGateMetrics.record(passed, evaluation_ms)` called in all modes

  **TurnLedger None-safety**: All credit/debit calls are guarded by
  `if ledger is not None`. In standalone roadmap mode, `ledger` is `None`
  and all economic paths are no-ops.

  **Threading note**: The anti-instinct check is a <1s synchronous operation.
  Rather than submitting through `TrailingGateRunner.submit()` (which runs on
  a daemon thread), consider running synchronously and feeding the result into
  the trailing gate infrastructure for bookkeeping only.

  #### Rollout Mode Behavior Matrix

  | `gate_rollout_mode` | Gate fires? | Failure logged? | Remediation attempted? | TaskResult mutated? | Reimbursement on pass? |
  |---------------------|------------|----------------|----------------------|--------------------|-----------------------|
  | off                 | Yes        | No             | No                   | No                 | No                    |
  | shadow              | Yes        | Yes (metrics)  | No                   | No                 | No                    |
  | soft                | Yes        | Yes (warning)  | Yes                  | No                 | Yes                   |
  | full                | Yes        | Yes (error)    | Yes                  | Yes (FAIL)         | Yes                   |
  ```

- **Cross-refs**: Section 8 (gate definition), Section 9 (roadmap executor), Section 16.5 (integration contract), design.md Sections 3.3, 6.3.
- **Risk**: If this section is omitted, the dual-context execution model is undefined and implementers will either skip sprint integration entirely (Alpha's view) or wire it incorrectly.

### Section 9.6 (New): KPI Report Integration

- **Change**: New section defining how anti-instinct gate metrics feed into `build_kpi_report()`.
- **Content**:

  ```markdown
  ### 9.6 KPI Report Integration

  `GateKPIReport` (sprint/kpi.py) receives anti-instinct gate results
  alongside all other gate results at sprint completion via `build_kpi_report()`.

  The anti-instinct gate contributes to:
  - `gate_pass_rate` / `gate_fail_rate` (aggregate across all gate types)
  - `gate_latency_p50` / `gate_latency_p95` (expected <1s for anti-instinct)
  - `turns_reimbursed_total` (only in soft/full mode on pass)

  The audit report's frontmatter fields (`undischarged_obligations`,
  `uncovered_contracts`, `fingerprint_coverage`) are gate-specific detail.
  The KPI report consumes `TrailingGateResult.passed` and
  `TrailingGateResult.evaluation_ms`, not the audit report content.

  KPI aggregation occurs only in sprint context. Standalone roadmap runs
  do not produce a `GateKPIReport`.
  ```

- **Cross-refs**: Section 9.5, design.md Section 5.
- **Risk**: Without this section, the KPI report integration is undefined and implementers must reverse-engineer from design.md.

### Section 12: File Change List

- **Change**: (1) Add coordination table showing which files each spec modifies and conflict risk. (2) Add sprint-side files to the change list. (3) Update LOC estimate.
- **Edits**:
  - After the "Modified Files (3)" table, add:

    ```markdown
    ### Coordination with TurnLedger Integration (v3.1 Sprint Pipeline)

    | File | Anti-Instincts Changes | TurnLedger Changes | Conflict Risk |
    |------|----------------------|-------------------|--------------|
    | `pipeline/gates.py` | Add `ANTI_INSTINCT_GATE`, 3 check functions, update `ALL_GATES` | `gate_passed()` consumed by `TrailingGateRunner.submit()` (no modification) | None -- additive vs read-only |
    | `roadmap/executor.py` | Add anti-instinct step + audit runner | No changes (TurnLedger targets `sprint/executor.py`) | None -- different files |
    | `sprint/executor.py` | Not modified by Anti-Instincts | Add `run_post_task_gate_hook()`, `TrailingGateRunner`, `build_kpi_report()` | None -- no overlap |
    | `sprint/models.py` | Not modified by Anti-Instincts | Add `gate_rollout_mode` field to `SprintConfig` | None -- no overlap |

    **Conclusion**: Zero merge conflicts expected. The two specs modify
    entirely different executor files. The shared substrate (`pipeline/gates.py`)
    is read-only for TurnLedger and additive-only for Anti-Instincts.
    ```

  - Add to modified files list:
    - `src/superclaude/cli/sprint/models.py` -- add `gate_rollout_mode: Literal["off", "shadow", "soft", "full"] = "off"` on `SprintConfig`
    - `src/superclaude/cli/sprint/executor.py` -- add `run_post_task_gate_hook()`, `TrailingGateRunner`/`DeferredRemediationLog` instantiation, `build_kpi_report()` call

  - Add to new test files:
    - `tests/sprint/test_shadow_mode.py` -- shadow mode integration test
    - `tests/pipeline/test_full_flow.py` -- add scenario for reimbursement path

  - Update total impact: ~1,190-1,240 LOC (up from ~1,040). Existing model changes: 1 (`SprintConfig` gains `gate_rollout_mode`).

- **Cross-refs**: Section 8 (coexistence notes), Section 9.5 (sprint executor integration).
- **Risk**: Without the coordination table, parallel implementers may assume conflicts exist where none do. Without the expanded file list, sprint-side integration files are missed.

### Section 13: Implementation Phases

- **Change**: (1) Add parallelism note -- Anti-Instincts Gate (roadmap) can proceed in parallel with TurnLedger wiring (sprint). (2) Split task 6 into roadmap executor (6a) and sprint executor (6b). (3) Add task 9: shadow-mode validation. (4) Default to `gate_rollout_mode="off"` for Phase 1. (5) Add graduation criteria from design.md.
- **Edits**:
  - After Phase 1's implementation sequence, add:

    ```markdown
    **Parallelism with TurnLedger Integration**: The Anti-Instincts Gate
    modules (Sections 4-7, roadmap pipeline) have zero dependency on TurnLedger
    wiring (sprint pipeline). These can be implemented in parallel:
    - Branch A: Anti-instinct modules + roadmap executor wiring (tasks 1-6a, 7-8)
    - Branch B: Sprint executor wiring + TurnLedger instantiation (task 6b)
    The only shared artifact is `pipeline/gates.py` (additive vs read-only).
    ```

  - Split task 6: "6a: Roadmap executor -- anti-instinct step + structural audit hook" and "6b: Sprint executor -- `run_post_task_gate_hook()`, TurnLedger instantiation, KPI report call"
  - Add task 9: "Shadow-mode validation run. Graduation criteria: `ShadowGateMetrics.pass_rate >= 0.90` over 5+ sprints before advancing to soft mode."
  - Phase 1 ships with `gate_rollout_mode` defaulting to `"off"` -- no behavioral change until shadow validation passes.
  - Add to Phase 2 deferred items: "Sprint-pipeline gate reimbursement via TurnLedger | design.md | Separate v3.1 workstream; activates `reimbursement_rate`. No dependency on Anti-Instincts Gate modules."

- **Cross-refs**: Section 12 (file change list coordination table), design.md Section 6.2.
- **Risk**: Without the parallelism note, project planning may serialize workstreams unnecessarily. Without task splitting, implementers face scope confusion between roadmap and sprint executor changes.

### Section 14: Shared Assumptions and Known Risks

- **Change**: Add assumptions A-011 through A-014 covering TurnLedger availability, rollout mode defaults, reimbursement rate, and `SprintGatePolicy` instantiation.
- **Edits**: Add rows to the assumptions table:

    ```
    | A-011 | `execute_sprint()` will be modified to instantiate TurnLedger before anti-instinct gates fire | Reimbursement is a no-op; gate failures are never budget-tracked | v3.1 TurnLedger wiring is a prerequisite; anti-instinct gate degrades gracefully (None-safe) when TurnLedger is absent |
    | A-012 | `gate_rollout_mode` defaults to `"off"` | False positives from anti-instinct gate block sprints before shadow validation | Phase 1 ships with "off" default; shadow validation required before advancing |
    | A-013 | Reimbursement rate of 0.8 is shared across all gate types | Per-gate-type rates may be needed in future | Single rate sufficient for v3.1; extensibility noted as future consideration |
    | A-014 | `SprintGatePolicy` is instantiated in the sprint loop | Gate failures have no remediation path | design.md Section 6.3 specifies instantiation; this is a cross-cutting dependency, not anti-instinct-specific |
    ```

- **Cross-refs**: Section 8 (gate definition), Section 9.5 (sprint executor integration), design.md Section 10.
- **Risk**: Without A-011, implementers may assume the anti-instinct gate is self-contained in the roadmap pipeline and skip sprint integration. Without A-014, `SprintGatePolicy` (currently dead code per analyze.md F-3) remains uninstantiated.

### Section 16.5 (New): TurnLedger Integration Contract

- **Change**: New section explicitly defining the economic interaction model.
- **Content**:

  ```markdown
  ### 16.5 TurnLedger Integration Contract

  This section defines how the anti-instinct gate interacts with TurnLedger
  economics. All paths are None-safe (no TurnLedger in standalone roadmap mode).

  **On gate PASS** (soft/full mode):
  `ledger.credit(int(upstream_merge_turns * ledger.reimbursement_rate))`
  Reimbursement applies to the upstream merge step's LLM turn cost.
  The anti-instinct step itself consumes 0 LLM turns (pure Python).

  **On gate FAIL**:
  `remediation_log.append(gate_result)` -- failure recorded for KPI and --resume
  Remediation re-runs the upstream merge step (not the anti-instinct check).
  With `retry_limit=0`, the remediation path enters but immediately exits
  with `BUDGET_EXHAUSTED` -- no retry budget consumed.

  **On FAIL + `gate_rollout_mode="full"`**:
  `TaskResult.status = FAIL` -- sprint task marked as failed.

  **On `gate_rollout_mode="off"` or standalone roadmap**:
  Gate fires normally. Result is not submitted to sprint infrastructure.
  No credit, no debit, no remediation log entry. Backward compatible
  with pre-v3.1 behavior.

  **Invariant**: The anti-instinct gate's TurnLedger cost is always 0
  (pure Python, no LLM calls). Budget impact comes only from the
  reimbursement of upstream steps on pass, or the failure of upstream
  steps to earn reimbursement on fail.
  ```

- **Cross-refs**: Section 8 (gate scope), Section 9.5 (sprint executor integration), design.md Section 2.2.
- **Risk**: Without this contract, the economic interaction model must be inferred from scattered references across design.md, brainstorm.md, and the spec itself.

---

## New Sections Required (merged)

| Section | Purpose | Source Plans |
|---------|---------|-------------|
| 9.5: Sprint Executor Integration | Define sprint-side gate result flow, TurnLedger interaction, rollout mode behavior matrix | Beta + Gamma (Alpha's 8.5 Non-Applicability replaced) |
| 9.6: KPI Report Integration | Define anti-instinct gate metrics in `build_kpi_report()` | Gamma (Beta partially covered) |
| 16.5: TurnLedger Integration Contract | Explicit economic interaction model (credit/debit/remediation) | Gamma |

---

## Sections Unchanged (merged, verified by majority)

All three plans agree these sections require no modification:

| Section | Verification |
|---------|-------------|
| 1. Problem Statement | 3/3 agree -- LLM failure modes unchanged by TurnLedger |
| 2. Evidence: cli-portify Bug | 3/3 agree -- historical evidence, no TurnLedger relevance |
| 3. Architecture | 2/3 agree unchanged, merged plan adds minor diagram note (documentation-only) |
| 4. Module 1: Obligation Scanner | 3/3 agree -- pure-function, no budget interaction |
| 5. Module 2: Integration Contract Extractor | 3/3 agree -- pure-function, no budget interaction |
| 6. Module 3: Fingerprint Extraction | 3/3 agree -- pure-function, no budget interaction |
| 7. Module 4: Spec Structural Audit | 3/3 agree -- pure-function, no budget interaction |
| 10. Prompt Modifications | 3/3 agree -- generation-time, not gate-evaluation-time |
| 11. Contradiction Resolutions | 3/3 agree -- X-001 through X-008 remain valid (cross-ref X-007 from Section 9.5) |
| 15. V5-3 AP-001 Subsumption | 3/3 agree -- design decision unaffected |
| 16. Rejected Alternatives | 3/3 agree -- no alternative becomes viable due to TurnLedger |

---

## Interaction Effects (merged)

| # | Effect | Source Plans | Confidence |
|---|--------|-------------|------------|
| 1 | **Enforcement tier x rollout mode**: STRICT governs criteria; rollout mode governs consequence. Independent axes. | Alpha + Beta + Gamma | High |
| 2 | **Dual execution context**: Roadmap pipeline runs standalone (no TurnLedger) or within sprint (TurnLedger available). Both paths must be defined. | Gamma (unique) | High -- resolves central architectural disagreement |
| 3 | **Anti-instinct x wiring gate (v3.0)**: Both run post-task sequentially. Wiring hook fires first, then gate hook. Shared `DeferredRemediationLog` and `ledger`. | Beta | Medium |
| 4 | **Anti-instinct x spec-fidelity gate ordering**: Anti-instinct runs before spec-fidelity in `ALL_GATES`. Full-mode failure halts before spec-fidelity. Correct behavior. | Beta | High |
| 5 | **Reimbursement x pre-allocation reconciliation**: design.md replaces reconciliation with debit/credit model. Must not double-credit. Reconciliation refactor is a v3.1 prerequisite, not anti-instinct responsibility. | Beta | Medium |
| 6 | **DeferredRemediationLog x retry_limit=0**: Failure enters remediation path but exits immediately with BUDGET_EXHAUSTED. Correct but non-obvious. | Gamma | Medium |
| 7 | **Structural audit budget impact**: Phase 2 STRICT enforcement failure in sprint context debits turns with no reimbursement. Indirect but real. | Gamma | Medium |
| 8 | **Per-gate-type reimbursement rate**: Single rate sufficient for v3.1. Future extensibility consideration. | Gamma | Low |
| 9 | **Section 8 <-> Section 14 assumption pairing**: A-011 (resolve_gate_mode invariant) supports Section 8 coexistence paragraph. Must stay paired. | Alpha | Medium |
| 10 | **Section 12 coordination <-> Section 13 parallelism**: Zero-conflict conclusion enables parallel workstream recommendation. If coordination analysis is wrong, parallelism note is invalid. | Alpha | High |

---

## Migration / Backward Compatibility Notes (merged)

1. **`gate_rollout_mode` defaults to `"off"`**: No behavioral change for existing users. The anti-instinct gate fires and writes its audit report, but sprint-level economics (reimbursement, remediation, KPI) are inactive until explicitly opted in. (All 3 plans agree.)

2. **`TurnLedger` is None-safe throughout**: All new code paths guard on `if ledger is not None`. Standalone `superclaude roadmap run` works identically to pre-integration behavior. (All 3 plans agree.)

3. **No model changes to existing dataclasses**: `TurnLedger`, `SemanticCheck`, `GateCriteria`, `Step`, and `PipelineConfig` retain current fields. Only addition: `gate_rollout_mode` on `SprintConfig` and `gate_scope` on `ANTI_INSTINCT_GATE` definition. (Majority agree.)

4. **Implementation can be staged**: Ship anti-instinct modules (Sections 4-7) and gate definition (Section 8) first with `gate_rollout_mode="off"`. Sprint executor wiring (Section 9.5) ships as a follow-up when TurnLedger instantiation lands. (Beta + Gamma agree; Alpha considers staging unnecessary since it views TurnLedger as non-applicable.)

5. **Execution order unconstrained**: Either Anti-Instincts or TurnLedger wiring can land first. If TurnLedger lands first, `gate_rollout_mode` exists but is irrelevant to standalone roadmap runs. If Anti-Instincts lands first, `ANTI_INSTINCT_GATE` exists in `ALL_GATES` but is never encountered by `TrailingGateRunner` until sprint wiring is added. (Alpha + Gamma agree.)

6. **`SprintGatePolicy` activation**: `SprintGatePolicy.build_remediation_step()` must be instantiated for gate remediation to work (currently dead code per analyze.md F-3). This is a cross-cutting v3.1 dependency, not anti-instinct-specific. (Beta + Gamma agree; Alpha does not mention.)

7. **`pipeline/gates.py` additive change is safe**: Adding `ANTI_INSTINCT_GATE` to `ALL_GATES` does not modify `gate_passed()` signature. `TrailingGateRunner.submit(gate_check=gate_passed)` continues to work. (All 3 plans agree.)

8. **TurnLedger migration to `pipeline/models.py`**: Cross-release summary recommends this migration. It is a separate refactor that should land before or alongside v3.1 but is not owned by the anti-instinct gate spec. (All 3 plans agree.)

9. **Test backward compatibility**: Existing tests pass without modification. New test scenarios (shadow mode, reimbursement path, dual-context execution) are additive. (Beta + Gamma agree.)
