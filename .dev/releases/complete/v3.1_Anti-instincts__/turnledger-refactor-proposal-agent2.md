# TurnLedger Integration Refactoring Proposal for Anti-Instincts Gate Spec

> **Author**: Agent 2 (Refactoring Expert)
> **Date**: 2026-03-20
> **Original Spec**: `anti-instincts-gate-unified.md` (hereafter "AIG")
> **Design Addendum**: `turnledger-integration/v3.1/design.md` (hereafter "TLD")
> **Scope**: Identify every place TLD proposes TurnLedger consumption that replaces, modifies, or supplements AIG pipeline definitions; produce a conflict-resolution refactoring plan.

---

## 1. Section-by-Section Diff Summary

### AIG Section 3: Architecture

| Aspect | AIG Current | TLD Impact | Verdict |
|--------|-------------|------------|---------|
| Pipeline flow diagram | Linear: `merge -> ANTI_INSTINCT_GATE -> test-strategy` | TLD inserts a `run_post_task_gate_hook()` step at [5] in the task loop (TLD Section 2.4) that evaluates trailing gates per-task, including gate-pass reimbursement via `ledger.credit()` | **Supplements**. AIG's pipeline is for the *roadmap* executor; TLD's is for the *sprint* executor. No direct conflict, but AIG Section 9 (Executor Integration) must clarify which executor it targets if both share `gates.py`. |
| Zero LLM calls property | AIG enforces 0 LLM calls for all anti-instinct checks | TLD does not add LLM calls; `gate_passed()` is pure Python | **Compatible**. No change needed. |
| Pipeline position | "between merge and test-strategy" | TLD places gate evaluation after every task subprocess in the sprint executor, not between named pipeline steps | **Different pipeline**. AIG addresses `roadmap/executor.py`; TLD addresses `sprint/executor.py`. The gate definitions in `gates.py` are shared infrastructure. |

### AIG Section 8: Gate Definition (`ANTI_INSTINCT_GATE`)

| Aspect | AIG Current | TLD Impact | Verdict |
|--------|-------------|------------|---------|
| Gate artifact | `anti-instinct-audit.md` with YAML frontmatter | TLD's `gate_passed()` function (gates.py line 20) evaluates any gate by checking: file exists, non-empty, min lines, frontmatter fields, semantic checks. AIG's `ANTI_INSTINCT_GATE` is consumed by this function. | **Compatible**. `gate_passed()` is the evaluation mechanism; `ANTI_INSTINCT_GATE` is the criteria. TLD does not redefine gate criteria. |
| `ALL_GATES` list position | `("anti-instinct", ANTI_INSTINCT_GATE)` between merge and test-strategy | TLD's `TrailingGateRunner.submit()` uses `gate_passed` as its `gate_check` parameter. It pulls gate criteria from the step definition, not from `ALL_GATES` ordering. | **Supplements**. `ALL_GATES` ordering matters for the roadmap executor's sequential pipeline. TLD's trailing gate runner uses step-level gate assignment, so both can coexist. |
| Enforcement tier | `STRICT` for all 3 semantic checks | TLD introduces a graduated rollout: shadow -> soft -> full (TLD Section 6.2). A `STRICT` gate in the roadmap pipeline could be `shadow` in the sprint pipeline. | **Conflict**. See Section 5 below. |
| Semantic check functions | `_no_undischarged_obligations`, `_integration_contracts_covered`, `_fingerprint_coverage_check` -- all read frontmatter from a single content string | TLD's `gate_passed()` already handles this pattern (frontmatter field check + semantic checks). No API mismatch. | **Compatible**. |

### AIG Section 8.1: Coexistence with D-03/D-04

| Aspect | AIG Current | TLD Impact | Verdict |
|--------|-------------|------------|---------|
| Dedup policy note | "D-03/D-04 should be conditional on ANTI_INSTINCT_GATE not being active, OR both coexist as defense-in-depth" | TLD does not mention D-03/D-04. TLD's `DeferredRemediationLog` replaces existing failure tracking (TLD Section 4.3), which could include D-03/D-04 outcomes. | **Risk**. If D-03/D-04 failures were previously tracked via `TaskResult.gate_outcome`, TLD's replacement mapping (Section 4.3) must also accommodate anti-instinct gate failures. |

### AIG Section 9: Executor Integration

| Aspect | AIG Current | TLD Impact | Verdict |
|--------|-------------|------------|---------|
| Target file | `src/superclaude/cli/roadmap/executor.py` | TLD targets `src/superclaude/cli/sprint/executor.py` | **Different files**. No merge conflict on the same file. However, if `ANTI_INSTINCT_GATE` is ever evaluated in the sprint pipeline (e.g., when a sprint task generates a roadmap), TLD's gate hook would need to know about it. |
| Change 1: Structural audit after extract | Executor-level hook in roadmap executor | TLD does not modify the roadmap executor | **No conflict**. |
| Change 2: Anti-instinct step definition | `Step(id="anti-instinct", ...)` with `retry_limit=0` | TLD's `TrailingGateRunner` assumes gate evaluation is retryable (via `attempt_remediation()`). A `retry_limit=0` step would bypass TLD's remediation flow. | **Conflict**. See Section 5 below. |
| Change 3: `_run_anti_instinct_audit()` | Writes `anti-instinct-audit.md` as gate artifact | TLD expects gate artifacts to exist at `step.output_file` for `gate_passed()` to evaluate. This is compatible if the audit report path matches. | **Compatible**. |
| Change 4: `_get_all_step_ids()` update | Adds `"anti-instinct"` between merge and test-strategy | TLD's sprint executor has its own step list; no conflict. | **No conflict**. |

### AIG Section 10: Prompt Modifications

| Aspect | AIG Current | TLD Impact | Verdict |
|--------|-------------|------------|---------|
| `INTEGRATION_ENUMERATION_BLOCK` | Added to `build_generate_prompt()` in `prompts.py` | TLD does not modify prompts | **No conflict**. |
| `INTEGRATION_WIRING_DIMENSION` | 6th dimension in `build_spec_fidelity_prompt()` | TLD does not modify prompts | **No conflict**. |

### AIG Section 12: File Change List

| Aspect | AIG Current | TLD Impact | Verdict |
|--------|-------------|------------|---------|
| `gates.py` modifications | AIG modifies `src/superclaude/cli/roadmap/gates.py` | TLD references `src/superclaude/cli/pipeline/gates.py` -- a different file (`pipeline/` vs `roadmap/`). | **Clarification needed**. If `gate_passed()` lives in `pipeline/gates.py` and `ANTI_INSTINCT_GATE` lives in `roadmap/gates.py`, they are in different modules. But TLD Section 3.1 says `gate_passed()` is the evaluation function for all gates. Either AIG's gate must be importable by TLD's evaluation path, or both gate files share a common interface. |
| `executor.py` modifications | AIG modifies `roadmap/executor.py` | TLD modifies `sprint/executor.py` | **No file-level conflict**, but interface expectations must align (see Section 5). |

### AIG Section 13: Implementation Phases

| Aspect | AIG Current | TLD Impact | Verdict |
|--------|-------------|------------|---------|
| Phase 1 enforcement | STRICT on all 3 checks immediately | TLD mandates shadow -> soft -> full graduated rollout (TLD Section 6.2) with explicit graduation criteria | **Conflict**. See Section 5 below. |
| Phase 2 deferred items | Negative-space prompting, coherence graph, obligation ledger, etc. | TLD does not reference AIG Phase 2 items | **No conflict**. |

---

## 2. Exact Section/Requirement IDs Affected

### AIG-S8: Gate Definition -- Enforcement Tier

**Before (AIG Section 8, line ~1026):**
```python
ANTI_INSTINCT_GATE = GateCriteria(
    ...
    enforcement_tier="STRICT",
    ...
)
```

**After (if TLD rollout pattern is adopted):**
The `enforcement_tier` field becomes insufficient. TLD's rollout model uses `gate_rollout_mode` (off/shadow/soft/full) which is runtime-configurable per-sprint, not a static property of the gate criteria. Two options:

1. Keep `enforcement_tier="STRICT"` as the gate's *intrinsic* tier, and let the sprint executor's `gate_rollout_mode` override behavior at runtime (shadow mode ignores tier, soft mode warns only, full mode enforces tier). This preserves AIG's intent while gaining TLD's graduated rollout.

2. Add an `enforcement_override` field to `GateCriteria` that the sprint executor can read.

### AIG-S9-C2: Anti-Instinct Step -- retry_limit=0

**Before (AIG Section 9, line ~1173):**
```python
Step(
    id="anti-instinct",
    ...
    retry_limit=0,  # Deterministic; retry would produce same result
    ...
)
```

**After (if TLD remediation pattern applies):**
The `retry_limit=0` is correct for the *roadmap* pipeline because the anti-instinct checks are deterministic -- re-running them on the same merged roadmap produces the same result. However, TLD's `attempt_remediation()` does not retry the gate; it retries the *task subprocess* that produced the failing artifact, then re-evaluates the gate. If the anti-instinct gate ever runs in the sprint pipeline, its `retry_limit` should be governed by TLD's remediation policy, not hardcoded to 0.

**Recommendation**: Keep `retry_limit=0` for the roadmap pipeline step definition. Document that sprint-pipeline evaluation of this gate uses TLD's remediation loop instead of step-level retry.

### AIG-S9-C3: `_run_anti_instinct_audit()` -- No Reimbursement Awareness

**Before (AIG Section 9, line ~1184-1278):**
The audit runner writes the report and returns results. No interaction with `TurnLedger`.

**After (if TLD integration applies):**
When the anti-instinct audit runs in a pipeline that has a TurnLedger, a gate pass should trigger `ledger.credit(turns * reimbursement_rate)` per TLD Section 2.2. Since the anti-instinct step is pure Python with near-zero turn cost, the reimbursement would be negligible. But the *interface contract* should still be honored -- the step should participate in the debit/credit lifecycle.

**Recommendation**: No change to `_run_anti_instinct_audit()` itself. The reimbursement is handled by the executor's gate hook, not by the audit function. Document this in AIG Section 9 as a note.

### AIG-S8: Anti-Instinct Audit Report Format -- No KPI Fields

**Before (AIG Section 8, line ~1089-1103):**
The audit report frontmatter contains only anti-instinct-specific fields.

**After (if TLD KPI integration applies):**
TLD's `build_kpi_report()` (Section 5) aggregates gate results across all phases. The anti-instinct gate results would be included in `_all_gate_results` if evaluated via `TrailingGateRunner`. No change to the audit report format is needed because TLD reads `TrailingGateResult` objects (produced by `gate_passed()` evaluating the report), not the report frontmatter directly.

**Recommendation**: No change needed. The existing format is sufficient.

### AIG-S12: File Change List -- Missing `pipeline/gates.py` Coordination

**Before (AIG Section 12):**
Lists `roadmap/gates.py` as modified. Does not mention `pipeline/gates.py`.

**After:**
TLD's `gate_passed()` in `pipeline/gates.py` must be able to evaluate `ANTI_INSTINCT_GATE`. If `GateCriteria` and `SemanticCheck` are defined in `pipeline/gates.py` and imported by `roadmap/gates.py`, this works automatically. If they are defined separately, an import path must be established.

**Recommendation**: Add a note to AIG Section 12 confirming that `GateCriteria` and `SemanticCheck` are defined in or importable from `pipeline/gates.py`, ensuring TLD's `gate_passed()` can evaluate AIG's gate criteria.

---

## 3. New Sections Introduced by TurnLedger Integration

These sections would be **new additions** to AIG if the TLD integration is adopted:

### 3.1 New: Turn Budget Interaction (would follow AIG Section 9)

**Proposed Section 9.5: Turn Budget Interaction**

Content: Document that the anti-instinct step participates in the TurnLedger debit/credit lifecycle when running in a TurnLedger-aware pipeline. Specifically:
- The step debits `ledger.minimum_allocation` before execution (handled by executor, not by step code).
- Since the step is pure Python with <1s execution, actual turn consumption is near zero.
- The credit (reconciliation of pre-allocated minus actual) is handled by the executor's existing reconciliation logic.
- Gate-pass reimbursement via `ledger.credit(turns * reimbursement_rate)` is handled by TLD's `run_post_task_gate_hook()` if the step runs in the sprint pipeline.

### 3.2 New: Graduated Rollout Strategy (would supplement AIG Section 13)

**Proposed Section 13.1: Sprint Pipeline Rollout**

Content: When the anti-instinct gate is evaluated in the sprint pipeline (not just the roadmap pipeline), enforcement follows TLD's graduated rollout:
1. **Shadow**: Gate evaluates but results are metrics-only; no TaskResult impact.
2. **Soft**: Gate evaluates; failures logged as warnings; reimbursement active on pass; remediation attempted but non-blocking.
3. **Full**: Gate failures after exhausted remediation set TaskResult.status = FAIL.

This is distinct from AIG's Phase 1/Phase 2 (which governs the *roadmap* pipeline). The sprint pipeline rollout is controlled by `SprintConfig.gate_rollout_mode`.

### 3.3 New: Failure Tracking via DeferredRemediationLog (would supplement AIG Section 8)

**Proposed Section 8.5: Sprint Pipeline Failure Tracking**

Content: When the anti-instinct gate fails in the sprint pipeline, failures are tracked via `DeferredRemediationLog` (TLD Section 4), not via the roadmap pipeline's halt mechanism. The remediation log provides:
- Persistent, cross-phase failure journal
- Resume recovery via `--resume`
- KPI feed for `build_kpi_report()`

This replaces the roadmap pipeline's binary GATE FAIL / Proceed behavior with a richer failure lifecycle.

---

## 4. Risks and Conflicts

### CONFLICT-01: Enforcement Tier vs. Graduated Rollout

**AIG says**: `ANTI_INSTINCT_GATE` has `enforcement_tier="STRICT"` (Section 8, line ~1026). Section 13 says Phase 1 is immediate STRICT enforcement.

**TLD says**: All gates should follow a shadow -> soft -> full rollout (Section 6.2) with explicit graduation criteria before enforcement activates.

**Impact**: If AIG ships with STRICT enforcement and TLD ships with graduated rollout, the anti-instinct gate would be STRICT in the roadmap pipeline but potentially "off" or "shadow" in the sprint pipeline. This is not inherently contradictory (different pipelines can have different policies), but it creates confusion about the gate's actual enforcement status.

### CONFLICT-02: retry_limit=0 vs. Remediation Loop

**AIG says**: The anti-instinct step has `retry_limit=0` because "Deterministic; retry would produce same result" (Section 9, line ~1173).

**TLD says**: Gate failures trigger `attempt_remediation()`, which re-runs the *task subprocess* and re-evaluates the gate (Section 6.3). This is meaningful even for deterministic gates because the *input artifact* (merged roadmap) could be regenerated.

**Impact**: If the anti-instinct gate is evaluated in the sprint pipeline via TLD's hook, the `retry_limit=0` field on the Step definition is irrelevant (TLD's remediation loop does not read `retry_limit`). But the conceptual mismatch should be documented.

### CONFLICT-03: Gate Artifact Location Assumptions

**AIG says**: The audit report is written to `output_dir / "anti-instinct-audit.md"` (Section 8, line ~1275).

**TLD says**: `gate_passed()` evaluates the file at `step.output_file` (Section 3.1). In TLD's sprint pipeline, this would be `config.results_dir / <step_output>`, which may differ from AIG's `output_dir`.

**Impact**: If the same gate criteria are used in both pipelines, the artifact path must be resolved consistently. The roadmap executor writes to `output_dir`; the sprint executor writes to `config.results_dir`.

### CONFLICT-04: `gates.py` Module Location Ambiguity

**AIG says**: Modify `src/superclaude/cli/roadmap/gates.py` (Section 8).

**TLD says**: `gate_passed()` lives in `src/superclaude/cli/pipeline/gates.py` (Section 3.1, document frontmatter).

**Impact**: Two different `gates.py` files. AIG's `ANTI_INSTINCT_GATE` must be evaluable by TLD's `gate_passed()`. If `GateCriteria` is defined in `pipeline/gates.py`, then `roadmap/gates.py` imports from it. If both define their own `GateCriteria`, there is a type mismatch.

### RISK-01: DeferredRemediationLog as Sole Failure Journal

**TLD says**: `DeferredRemediationLog` is the "single source" for gate failures (Section 4.2), replacing `TaskResult.gate_outcome = FAIL`.

**AIG says**: The anti-instinct gate communicates failure via the gate mechanism (GATE FAIL halts pipeline, Section 3).

**Impact**: In the roadmap pipeline, failure is binary (halt or proceed). In the sprint pipeline, failure enters the remediation lifecycle. If both pipelines are active simultaneously (e.g., a sprint task that generates a roadmap), the failure tracking paths diverge. This is acceptable but should be documented.

---

## 5. Recommended Resolutions

### RESOLUTION for CONFLICT-01: Dual-Mode Enforcement

**Recommendation**: Keep `enforcement_tier="STRICT"` as the gate's intrinsic property. Add a comment in AIG Section 8 stating:

> When evaluated in the sprint pipeline, enforcement behavior is governed by `SprintConfig.gate_rollout_mode` (shadow/soft/full), which may override the intrinsic enforcement tier during graduated rollout. The STRICT tier applies unconditionally in the roadmap pipeline.

No code change to `GateCriteria`. The sprint executor's `run_post_task_gate_hook()` already handles mode dispatch without reading `enforcement_tier`.

### RESOLUTION for CONFLICT-02: Document Scope of retry_limit

**Recommendation**: Add a note to AIG Section 9, Change 2:

> `retry_limit=0` applies to the roadmap pipeline's step-level retry mechanism. In the sprint pipeline, gate failure remediation is governed by `attempt_remediation()` (TLD Section 6.3), which re-runs the upstream task subprocess rather than retrying the deterministic gate check. The retry_limit field is not read by the sprint pipeline's remediation loop.

No code change needed.

### RESOLUTION for CONFLICT-03: Parameterize Artifact Path

**Recommendation**: AIG's `_run_anti_instinct_audit()` already writes to `output_dir / "anti-instinct-audit.md"`, and the Step definition sets `output_file=out / "anti-instinct-audit.md"`. In the sprint pipeline, `out` would resolve to `config.results_dir`. No code change needed as long as the Step's `output_file` field is set by the executor at construction time (which it is).

Add a note to AIG Section 9:

> The `output_file` path is resolved by the executor at step construction time. In the roadmap pipeline, this is `output_dir / "anti-instinct-audit.md"`. In the sprint pipeline, this would be `config.results_dir / "anti-instinct-audit.md"` if the gate is registered as a sprint step.

### RESOLUTION for CONFLICT-04: Establish Import Path

**Recommendation**: Confirm that `GateCriteria`, `SemanticCheck`, and `gate_passed()` are defined in `src/superclaude/cli/pipeline/gates.py` as the canonical location. AIG's `roadmap/gates.py` imports these types and defines gate *instances* (like `ANTI_INSTINCT_GATE`) that use them. Add to AIG Section 12:

> **Dependency**: `roadmap/gates.py` imports `GateCriteria`, `SemanticCheck` from `pipeline/gates.py`. The `gate_passed()` function in `pipeline/gates.py` can evaluate any `GateCriteria` instance regardless of which module defines it.

### RESOLUTION for RISK-01: Document Failure Path Divergence

**Recommendation**: Add a note to AIG Section 8 under "Why a Separate Gate":

> In the sprint pipeline, anti-instinct gate failures are recorded in `DeferredRemediationLog` and follow the remediation lifecycle (TLD Section 4). In the roadmap pipeline, gate failure halts the pipeline. Both paths produce the same audit report artifact; the divergence is in the failure *handling*, not the failure *detection*.

---

## 6. Summary of Required Changes to AIG

| AIG Section | Change Type | Description |
|-------------|-------------|-------------|
| Section 8 (Gate Definition) | Add note | Clarify that `enforcement_tier="STRICT"` is intrinsic; sprint pipeline honors `gate_rollout_mode` instead |
| Section 8 (Why a Separate Gate) | Add note | Document failure path divergence between roadmap and sprint pipelines |
| Section 9, Change 2 | Add note | Document that `retry_limit=0` applies to roadmap pipeline only; sprint uses remediation loop |
| Section 9 | Add subsection 9.5 | Turn Budget Interaction: document debit/credit lifecycle participation |
| Section 12 (File Change List) | Add dependency note | Confirm `GateCriteria`/`SemanticCheck` import path from `pipeline/gates.py` |
| Section 13 | Add subsection 13.1 | Sprint Pipeline Rollout: graduated rollout strategy for sprint execution |

**No existing AIG code or gate definitions need to be modified.** All changes are documentation additions that ensure the two specifications are compatible without contradiction.

---

## 7. Items in TLD That Do NOT Affect AIG

The following TLD sections are entirely sprint-pipeline-scoped and have no bearing on AIG:

| TLD Section | Reason for Non-Impact |
|-------------|----------------------|
| Section 2.1-2.3 (Debit/Credit call sites) | Sprint executor only; AIG's roadmap executor has no TurnLedger |
| Section 4 (DeferredRemediationLog) | Sprint failure tracking; does not modify gate definitions |
| Section 5 (GateKPIReport) | Post-sprint aggregation; does not change gate evaluation logic |
| Section 6.4 (SprintConfig field addition) | Sprint config only; roadmap config unaffected |
| Section 7 (Data flow diagram) | Sprint executor flow; roadmap executor has its own flow (AIG Section 3) |
| Section 8 (Key invariants) | Sprint-scoped invariants about TurnLedger monotonicity, shadow mode |

---

## 8. Implementation Sequence (if both AIG and TLD ship)

```
1. AIG Phase 1 (roadmap pipeline)
   - Implement 4 detection modules (obligation, contracts, fingerprint, structural audit)
   - Add ANTI_INSTINCT_GATE to roadmap/gates.py
   - Wire into roadmap/executor.py
   - Add documentation notes from Section 6 above

2. TLD Integration (sprint pipeline)
   - Add gate_rollout_mode to SprintConfig
   - Implement run_post_task_gate_hook() in sprint/executor.py
   - Wire TurnLedger reimbursement
   - Wire DeferredRemediationLog

3. Cross-Pipeline Registration (optional, after both ship)
   - Register ANTI_INSTINCT_GATE as evaluable by sprint pipeline
   - Map anti-instinct audit to sprint step if roadmap-generation tasks exist in sprints
```

AIG can ship first without any TLD dependencies. TLD can ship first without AIG's gate definitions. Neither blocks the other. The cross-pipeline integration is additive.
