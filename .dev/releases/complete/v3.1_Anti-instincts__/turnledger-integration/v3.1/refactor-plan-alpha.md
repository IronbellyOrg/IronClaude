# Refactoring Plan: Anti-Instincts Gate Unified Spec <- TurnLedger Integration

---
title: "Refactoring Plan Alpha: v3.1 Anti-Instincts Gate <- TurnLedger Integration"
status: DRAFT
date: 2026-03-20
spec: .dev/releases/backlog/v3.1_Anti-instincts__/anti-instincts-gate-unified.md
design: .dev/releases/current/turnledger-integration/v3.1/design.md
analysis: .dev/releases/current/turnledger-integration/v3.1/analyze.md
brainstorm: .dev/releases/current/turnledger-integration/v3.1/brainstorm.md
cross_release: .dev/releases/current/turnledger-integration/cross-release-summary.md
turnledger_source: src/superclaude/cli/sprint/models.py (lines 488-525)
---

## Context

The v3.1 Anti-Instincts Gate spec (`anti-instincts-gate-unified.md`) defines four deterministic detection modules for roadmap quality (obligation scanner, integration contracts, fingerprint coverage, spec structural audit) plus a gate definition and executor/prompt wiring. It targets `src/superclaude/cli/roadmap/` and adds zero LLM calls.

The TurnLedger integration design (`design.md`) specifies how `TurnLedger`, `TrailingGateRunner`, `DeferredRemediationLog`, and `GateKPIReport` wire into the **sprint executor pipeline** (`src/superclaude/cli/sprint/`). It activates the dormant `reimbursement_rate=0.8`, adds a `gate_rollout_mode` field, introduces `run_post_task_gate_hook()`, and defines a shadow/soft/full rollout.

**Critical observation**: These two specs operate in **different pipeline domains**:
- Anti-Instincts Gate: `roadmap/` pipeline (extraction -> generation -> merge -> gate)
- TurnLedger integration: `sprint/` pipeline (task loop -> subprocess -> gate -> reimbursement)

The overlap is narrow but real: the Anti-Instincts Gate uses `gate_passed()` and `GateCriteria` from the shared `pipeline/gates.py` substrate, and the TurnLedger integration's `TrailingGateRunner` also consumes `gate_passed()`. The design.md's rollout mechanism (`gate_rollout_mode`) and `ANTI_INSTINCT_GATE`'s enforcement tiers are parallel concepts that must coexist.

---

## Sections Requiring Modification

### Section 8: Gate Definition

- **Current content summary**: Defines `ANTI_INSTINCT_GATE` as a `GateCriteria` with 3 semantic checks, STRICT enforcement tier, position in `ALL_GATES` between merge and test-strategy. Notes coexistence with D-03/D-04 Unified Audit Gating.
- **Required change**: The design.md introduces `gate_rollout_mode` (off/shadow/soft/full) on `SprintConfig` and `run_post_task_gate_hook()` which dispatches gate evaluation through `TrailingGateRunner.submit()`. The `ANTI_INSTINCT_GATE` runs in the roadmap pipeline (not sprint), so it is NOT subject to `gate_rollout_mode` directly. However, Section 8's "Coexistence with Unified Audit Gating D-03/D-04" paragraph must be expanded to document:
  1. That `ANTI_INSTINCT_GATE` is a roadmap-pipeline gate, not a sprint-pipeline trailing gate, and therefore is NOT governed by `gate_rollout_mode`.
  2. That the `gate_passed()` function from `pipeline/gates.py` is now shared between: (a) the roadmap pipeline's synchronous gate checks, (b) the sprint pipeline's `TrailingGateRunner.submit(gate_check=gate_passed)` path, and (c) the new `run_post_task_gate_hook()`. The `ANTI_INSTINCT_GATE` criteria must remain compatible with the `gate_passed()` signature `(Path, GateCriteria) -> tuple[bool, str | None]`.
  3. That `resolve_gate_mode()` (trailing_gate.py line 614) always returns BLOCKING for `GateScope.RELEASE`; the Anti-Instinct gate at roadmap scope is inherently blocking and unaffected by rollout mode.

- **Specific edits**:
  - After the "Coexistence with Unified Audit Gating D-03/D-04" paragraph (spec lines 1077-1083), add:

    ```
    ### Coexistence with Sprint-Pipeline TurnLedger/TrailingGateRunner (v3.1)

    The `ANTI_INSTINCT_GATE` operates in the roadmap pipeline
    (`src/superclaude/cli/roadmap/executor.py`) and is evaluated synchronously
    by `gate_passed()` after the anti-instinct audit step writes its output.
    It is NOT a sprint-pipeline gate and is NOT governed by `SprintConfig.gate_rollout_mode`.

    The sprint pipeline's `TrailingGateRunner` (introduced by v3.1 TurnLedger
    integration) also consumes `gate_passed()` from `pipeline/gates.py` but
    operates on sprint task outputs, not roadmap artifacts. These are distinct
    gate evaluation paths sharing the same evaluation function.

    Key invariant: `ANTI_INSTINCT_GATE` is always BLOCKING. The
    `resolve_gate_mode()` function returns `GateMode.BLOCKING` for
    `GateScope.RELEASE`-scoped gates. Roadmap gates are release-scoped by
    definition and therefore immune to shadow/soft/full rollout semantics.
    ```

- **Cross-references**: Section 9 (Executor Integration) references the gate; Section 3 (Architecture) diagram shows gate position.
- **Risk**: If this clarification is omitted, implementers may attempt to wire `ANTI_INSTINCT_GATE` into `TrailingGateRunner` or apply `gate_rollout_mode` to roadmap gates, breaking the always-blocking invariant.

---

### Section 9: Executor Integration

- **Current content summary**: Specifies 4 changes to `src/superclaude/cli/roadmap/executor.py`: structural audit after extract, anti-instinct step after merge, anti-instinct audit runner function, and import/step-ID updates. References `retry_limit=0` on the anti-instinct step.
- **Required change**: The design.md identifies that `Step.retry_limit` in the pipeline executor has **no budget awareness** (analyze.md Finding F-4). The anti-instinct step already has `retry_limit=0` (deterministic, no retry needed), which is correct and budget-neutral. However, the spec should explicitly document why `retry_limit=0` is chosen and note that the pipeline executor's retry mechanism (`pipeline/executor.py:174-294`) operates independently of `TurnLedger` budget tracking. This is a documentation-only change to prevent future confusion when TurnLedger is wired into the sprint pipeline.

  Additionally, the `_run_anti_instinct_audit()` function reads `roadmap.md` from `output_dir`. The design.md's data flow diagram (Section 7) shows that sprint-level gate results feed into `build_kpi_report()`. The roadmap pipeline's anti-instinct audit results do NOT feed into the sprint KPI report -- they are a separate reporting chain. This separation should be documented.

- **Specific edits**:
  - In Change 2 (anti-instinct step definition, spec lines 1163-1175), add a comment to the Step definition:

    ```python
    Step(
        id="anti-instinct",
        prompt="",  # Non-LLM step; executor handles directly
        output_file=out / "anti-instinct-audit.md",
        gate=ANTI_INSTINCT_GATE,
        timeout_seconds=30,  # Pure Python, <1s expected
        inputs=[config.spec_file, extraction, merge_file],
        retry_limit=0,  # Deterministic; retry produces same result.
                        # Note: pipeline executor retry (pipeline/executor.py)
                        # has no TurnLedger budget awareness. This step is
                        # budget-neutral regardless because retry_limit=0.
    ),
    ```

  - After Change 3 (`_run_anti_instinct_audit()`, spec line 1278), add a note:

    ```
    **KPI Reporting Boundary**: The anti-instinct audit results are roadmap-pipeline
    artifacts. They do NOT feed into `build_kpi_report()` (sprint/kpi.py), which
    aggregates sprint-level `TrailingGateResult` objects from `TrailingGateRunner`.
    If roadmap-pipeline gate metrics are desired, they should feed into a separate
    roadmap-level reporting mechanism (future work, not in scope for v3.1).
    ```

- **Cross-references**: Section 8 (gate definition), Section 12 (file change list).
- **Risk**: Without the KPI boundary note, implementers may attempt to pipe roadmap gate results into the sprint KPI builder, producing nonsensical metrics (roadmap gates have no turn cost, no reimbursement, no remediation).

---

### Section 12: File Change List

- **Current content summary**: Lists 4 new source files, 4 new test files, and 3 modified files. Total impact: ~1,040 LOC, 0 LLM calls, <1s latency, 0 existing model changes.
- **Required change**: The design.md modifies files that overlap with or are adjacent to the anti-instincts spec's targets. The file change list should note potential merge conflicts and coordination requirements with the TurnLedger integration.

- **Specific edits**:
  - After the "Modified Files (3)" table (spec lines 1403-1408), add:

    ```
    ### Coordination with TurnLedger Integration (v3.1 Sprint Pipeline)

    The following files are modified by BOTH the Anti-Instincts Gate spec
    and the TurnLedger integration design:

    | File | Anti-Instincts Changes | TurnLedger Changes | Conflict Risk |
    |------|----------------------|-------------------|--------------|
    | `pipeline/gates.py` | Add `ANTI_INSTINCT_GATE`, 3 check functions, update `ALL_GATES` | `gate_passed()` consumed by `TrailingGateRunner.submit()` (no modification to gates.py itself) | None -- Anti-Instincts adds a new gate; TurnLedger reads existing `gate_passed()` |
    | `roadmap/executor.py` | Add anti-instinct step + audit runner | No changes (TurnLedger targets `sprint/executor.py`) | None -- different executor files |
    | `sprint/executor.py` | Not modified by Anti-Instincts | Add `run_post_task_gate_hook()`, `TrailingGateRunner` instantiation, `build_kpi_report()` call | None -- no overlap |
    | `sprint/models.py` | Not modified by Anti-Instincts | Add `gate_rollout_mode` field to `SprintConfig` | None -- no overlap |

    **Conclusion**: Zero merge conflicts expected. The two specs modify
    entirely different executor files (`roadmap/executor.py` vs
    `sprint/executor.py`). The shared substrate (`pipeline/gates.py`) is
    read-only for TurnLedger and additive-only for Anti-Instincts.
    ```

  - Update the "Total Impact" section to note:

    ```
    - **Existing model changes**: 0 (no changes to `SemanticCheck`, `GateCriteria`,
      `Step`, `PipelineConfig`, `SprintConfig`, or `TurnLedger`)
    ```

- **Cross-references**: Section 8 (coexistence notes), Section 9 (executor integration).
- **Risk**: Without this coordination table, parallel implementers may assume conflicts exist where none do, wasting effort on unnecessary sequencing.

---

### Section 13: Implementation Phases

- **Current content summary**: Phase 1 is the immediate spec (Sections 4-10), sequenced as: scanner -> contracts -> fingerprints -> structural audit -> gates -> executor -> prompts -> integration test. Phase 2 lists deferred items with adoption conditions.
- **Required change**: The cross-release summary (Section 4) recommends v3.1 TurnLedger integration as a **prerequisite** that should land BEFORE v3.2. The Anti-Instincts Gate is a roadmap-pipeline feature that is **independent** of the sprint-pipeline TurnLedger wiring. The implementation phases should clarify ordering:

  1. Anti-Instincts Gate (roadmap pipeline) can proceed **in parallel** with TurnLedger integration (sprint pipeline) -- no dependency in either direction.
  2. The cross-release summary's "v3.1 first" recommendation refers to TurnLedger wiring in the sprint pipeline, not the Anti-Instincts Gate.

- **Specific edits**:
  - After Phase 1's implementation sequence (spec lines 1439-1447), add:

    ```
    **Parallelism with TurnLedger Integration**: The Anti-Instincts Gate
    implementation (roadmap pipeline) has zero dependency on TurnLedger
    integration (sprint pipeline). These can be implemented in parallel by
    different agents/branches. The only shared artifact is `pipeline/gates.py`,
    where Anti-Instincts adds `ANTI_INSTINCT_GATE` (additive) and TurnLedger
    reads existing `gate_passed()` (read-only). No sequencing constraint.
    ```

  - In Phase 2 deferred items table (spec lines 1452-1458), add a row:

    ```
    | Sprint-pipeline gate reimbursement via TurnLedger | design.md | Separate v3.1 workstream; activates `reimbursement_rate` in `execute_phase_tasks()`. No dependency on Anti-Instincts Gate modules. |
    ```

- **Cross-references**: Section 12 (file change list coordination table).
- **Risk**: Without this clarification, project planning may serialize the two workstreams unnecessarily, doubling implementation time.

---

### Section 14: Shared Assumptions and Known Risks

- **Current content summary**: Lists 7 assumptions (A-001 through A-010, with gaps) covering extraction, regex, scaffolding, thresholds, and LLM correlation.
- **Required change**: The design.md introduces new risk vectors that the Anti-Instincts spec should acknowledge for completeness:

  1. The design.md's Key Invariant #5 states "Release gates are always blocking" -- the Anti-Instincts gate depends on this invariant. If `resolve_gate_mode()` behavior changes, the always-blocking assumption breaks.
  2. The analyze.md Finding F-4 notes pipeline executor retry has no budget awareness. The Anti-Instincts step uses `retry_limit=0` which sidesteps this, but the assumption that `retry_limit=0` is sufficient for deterministic steps should be documented.

- **Specific edits**:
  - Add two rows to the assumptions table:

    ```
    | A-011 | `resolve_gate_mode()` returns BLOCKING for release-scoped gates | Anti-Instinct gate treated as non-blocking; rollout mode applied incorrectly | Anti-Instinct gate is in roadmap pipeline which does not use `resolve_gate_mode()` at all; invariant is defense-in-depth |
    | A-012 | Deterministic steps need `retry_limit=0` because retry produces identical results | Wasted budget if retry_limit > 0 on deterministic steps | Already set correctly; pipeline executor retry has no budget awareness (F-4) so cost is invisible but real |
    ```

- **Cross-references**: Section 8 (gate definition), Section 9 (executor integration).
- **Risk**: Low. These are clarifying assumptions, not behavioral changes.

---

## New Sections Required

### New Section: TurnLedger Non-Applicability Statement (insert after Section 8.4 "Coexistence" or as Section 8.5)

The design.md establishes a detailed economic model (debit/credit/reimbursement) for sprint-pipeline gate evaluation. The Anti-Instincts Gate operates in the roadmap pipeline which has NO economic model -- roadmap steps are either subprocess (LLM) or pure-Python, with no TurnLedger tracking. A short section should make this explicit.

**Content**:

```markdown
### 8.5 TurnLedger Non-Applicability

The Anti-Instincts Gate is a roadmap-pipeline artifact. The roadmap pipeline
(`src/superclaude/cli/pipeline/executor.py` and `src/superclaude/cli/roadmap/executor.py`)
does not use `TurnLedger` for budget tracking. Roadmap steps consume subprocess
turns tracked by the pipeline executor's built-in retry mechanism (`Step.retry_limit`),
not by `TurnLedger.debit()`/`.credit()`.

Consequently:
- No `TurnLedger` instance is created for roadmap pipeline execution.
- No reimbursement occurs when the Anti-Instincts gate passes.
- No remediation budget is consumed when the Anti-Instincts gate fails (the step
  has `retry_limit=0`; failure halts the pipeline immediately).
- `DeferredRemediationLog` is not used for Anti-Instincts gate failures.
- `GateKPIReport` / `build_kpi_report()` does not aggregate Anti-Instincts results.

If TurnLedger budget tracking is desired for roadmap pipeline steps in the future,
that is a separate design decision requiring `TurnLedger` instantiation in
`pipeline/executor.py` or `roadmap/executor.py` -- outside the scope of both
the Anti-Instincts Gate and the v3.1 TurnLedger sprint integration.
```

**Risk if omitted**: Implementers may assume the TurnLedger integration design applies to all gates including roadmap gates, leading to incorrect wiring attempts.

---

## Sections Unchanged

### Section 1: Problem Statement (lines 1-13)
**Unchanged.** The problem statement describes LLM failure modes in roadmap generation. TurnLedger integration is a sprint-pipeline concern and does not alter the problem being solved. No edits needed.

### Section 2: Evidence -- The cli-portify Bug (lines 40-71)
**Unchanged.** This is historical evidence for the Anti-Instincts Gate. TurnLedger has no bearing on the cli-portify bug analysis. No edits needed.

### Section 3: Architecture (lines 74-103)
**Unchanged.** The architecture diagram shows the roadmap pipeline flow (spec -> extraction -> generation -> merge -> anti-instinct -> spec-fidelity). TurnLedger operates in the sprint pipeline, a different execution path. The diagram is accurate as-is. No edits needed.

### Section 4: Module 1 -- Obligation Scanner (lines 105-358)
**Unchanged.** The obligation scanner is a pure-Python function (`scan_obligations(content) -> ObligationReport`). It has no interaction with TurnLedger, TrailingGateRunner, DeferredRemediationLog, or any sprint-pipeline component. The implementation code, vocabulary tables, and false-positive mitigation are all roadmap-domain logic. No edits needed.

### Section 5: Module 2 -- Integration Contract Extractor (lines 361-668)
**Unchanged.** The integration contract extractor is a pure-Python function pair (`extract_integration_contracts()` + `check_roadmap_coverage()`). It scans spec text for integration patterns and verifies roadmap coverage. No sprint-pipeline interaction. No edits needed.

### Section 6: Module 3 -- Fingerprint Extraction (lines 671-818)
**Unchanged.** The fingerprint module is a pure-Python function (`check_fingerprint_coverage()`). It operates on spec and roadmap text content. No sprint-pipeline interaction. No edits needed.

### Section 7: Module 4 -- Spec Structural Audit (lines 821-955)
**Unchanged.** The spec structural audit is an upstream guard between extraction and generation. It is executor-level logic in the roadmap pipeline. No sprint-pipeline interaction. No edits needed.

### Section 10: Prompt Modifications (lines 1292-1363)
**Unchanged.** The prompt modifications add an integration enumeration block and a wiring dimension to roadmap generation prompts. These are roadmap-pipeline prompt templates with no sprint-pipeline interaction. No edits needed.

### Section 11: Contradiction Resolutions (lines 1366-1382)
**Unchanged.** The contradiction resolutions (X-001 through X-008) address conflicts between adversarial design review variants for the Anti-Instincts Gate. TurnLedger integration does not introduce new contradictions with any of these. No edits needed.

### Section 15: V5-3 AP-001 Subsumption by V2-A (lines 1478-1489)
**Unchanged.** This is an internal rationale for choosing V2-A over V5-3. No TurnLedger interaction. No edits needed.

### Section 16: Rejected Alternatives (lines 1493-1509)
**Unchanged.** The rejected alternatives are all roadmap-pipeline detection strategies. TurnLedger integration does not change the rationale for rejecting any of them. No edits needed.

---

## Interaction Effects

### Section 8 changes -> Section 9 consistency
The new coexistence paragraph in Section 8 references `resolve_gate_mode()` and `GateScope.RELEASE`. Section 9's executor integration must be consistent: the roadmap executor does NOT call `resolve_gate_mode()` -- it evaluates gates synchronously via `gate_passed()`. If Section 8 implies the roadmap executor knows about `resolve_gate_mode()`, Section 9 would need an import that doesn't belong there. The coexistence paragraph is carefully worded as an invariant statement ("roadmap gates are release-scoped by definition"), not an implementation directive.

### Section 12 coordination table -> Section 13 parallelism note
The coordination table in Section 12 establishes "zero merge conflicts." Section 13's parallelism note depends on this conclusion. If the coordination analysis were wrong (e.g., both specs modify `pipeline/gates.py` in conflicting ways), the parallelism note would be invalid. The analysis is correct: Anti-Instincts adds to gates.py; TurnLedger reads from it.

### Section 14 new assumptions -> Section 8 coexistence
A-011 (resolve_gate_mode returns BLOCKING for release scope) is referenced by the Section 8 coexistence paragraph. If A-011 is removed, the coexistence paragraph loses its supporting invariant. These must stay paired.

---

## Migration / Backward Compatibility Notes

1. **No behavioral changes to existing Anti-Instincts Gate spec.** All modifications are documentation/clarification additions. The four detection modules, gate definition, executor wiring, and prompt modifications are unchanged in behavior.

2. **No new dependencies introduced.** The Anti-Instincts Gate does not import from `sprint/models.py`, `sprint/executor.py`, `sprint/kpi.py`, `pipeline/trailing_gate.py`, or any TurnLedger-related module. The dependency graph remains: `roadmap/{obligation_scanner,integration_contracts,fingerprint,spec_structural_audit}.py` -> `roadmap/gates.py` -> `roadmap/executor.py`.

3. **`pipeline/gates.py` additive change is safe.** Adding `ANTI_INSTINCT_GATE` to `ALL_GATES` is purely additive. The `gate_passed()` function signature `(Path, GateCriteria) -> tuple[bool, str | None]` is not modified. `TrailingGateRunner.submit(gate_check=gate_passed)` continues to work because the function is not changed, only the registry of gate criteria grows.

4. **Execution order between Anti-Instincts and TurnLedger is unconstrained.** Either can land first. If TurnLedger lands first, `gate_rollout_mode` exists on `SprintConfig` but is irrelevant to roadmap pipeline. If Anti-Instincts lands first, `ANTI_INSTINCT_GATE` exists in `ALL_GATES` but is never encountered by `TrailingGateRunner` (which operates on sprint task outputs, not roadmap steps).

5. **Future consideration: TurnLedger migration to `pipeline/models.py`.** The cross-release summary (Section 2.3) recommends migrating `TurnLedger` from `sprint/models.py` to `pipeline/models.py` as a shared economic primitive. If this migration happens, the Anti-Instincts Gate spec is unaffected (it does not import or reference TurnLedger). However, if a future roadmap-pipeline budget mechanism is added, it could import TurnLedger from its new shared location.

---

## Summary of Changes

| Change Type | Count | Sections |
|-------------|-------|----------|
| Sections modified (documentation additions) | 5 | 8, 9, 12, 13, 14 |
| New sections required | 1 | 8.5 (TurnLedger Non-Applicability) |
| Sections verified unchanged | 12 | 1, 2, 3, 4, 5, 6, 7, 10, 11, 15, 16 (plus header/metadata) |
| Behavioral changes | 0 | -- |
| New dependencies | 0 | -- |
| New code | 0 | All changes are markdown documentation |
| Merge conflict risk | None | Different executor files, additive-only shared file |

**Total effort estimate**: Small. All changes are documentation additions to clarify the boundary between roadmap-pipeline and sprint-pipeline gate evaluation. No code changes, no new modules, no behavioral modifications.
