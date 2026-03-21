---
proposal: turnledger-refactor-for-wiring-gate
status: draft
date: 2026-03-20
original_spec: wiring-verification-gate-v1.0-release-spec.md
design_addendum: ../current/turnledger-integration/v3.2/design.md
---

# TurnLedger Refactoring Proposal -- Wiring Gate v3.2

## Overview

This proposal identifies every point where the TurnLedger integration design
(`design.md`) replaces, modifies, or supplements definitions in the original
wiring verification gate release spec (`wiring-verification-gate-v1.0-release-spec.md`).
The goal is a section-by-section accounting of what changes, what stays, what
is new, where conflicts exist, and how to resolve them.

---

## 1. Section-by-Section Diff Summary

### Section 1: Problem Statement

| Aspect | Status |
|--------|--------|
| Original text | **Unchanged** |
| TurnLedger impact | None |

The problem statement describes the "defined but not wired" pattern. The
TurnLedger design does not alter the problem framing. No changes required.

---

### Section 2: Goals and Non-Goals

| Aspect | Status |
|--------|--------|
| Goals 1-5 | **Unchanged** |
| Non-Goals | **Unchanged** |
| TurnLedger impact | None directly; budget accountability is an implicit new goal but is not listed |

**Recommendation**: Add a Goal 6: "Integrate wiring analysis cost into
TurnLedger budget accounting to provide per-task cost visibility." This makes
the TurnLedger integration an explicit deliverable rather than an undocumented
side effect.

---

### Section 3: Architecture

#### Section 3.1: System Context

| Aspect | Status |
|--------|--------|
| Original diagram | **Modified** |
| TurnLedger impact | New dependency arrows from `sprint/executor.py` to TurnLedger and from wiring hook to `trailing_gate.py:resolve_gate_mode()` |

The original diagram shows `sprint/executor.py -> SprintGatePolicy` and
`pipeline/trailing_gate.py -> resolve_gate_mode()`. The design adds:

- `sprint/executor.py -> TurnLedger (debit_wiring, credit_wiring)`
- `sprint/executor.py -> resolve_gate_mode()` (direct call, replacing mode string comparison)
- `sprint/executor.py -> attempt_remediation()` (new call path for BLOCKING failures)

The `SprintGatePolicy` relationship remains but is now invoked through
`attempt_remediation()` rather than directly from the mode switch.

#### Section 3.2: Module Architecture

| Aspect | Status |
|--------|--------|
| `audit/wiring_gate.py` | **Unchanged** |
| `audit/wiring_config.py` | **Unchanged** |
| `sprint/models.py` | **Modified** -- TurnLedger gains 3 fields + 3 methods; SprintConfig fields replaced |
| `sprint/executor.py` | **Modified** -- hook signature changes, mode dispatch rewritten |
| `sprint/kpi.py` | **New target** -- `GateKPIReport` extended with wiring fields |

#### Section 3.3: Data Flow

| Aspect | Status |
|--------|--------|
| Original flow | **Replaced** by design.md Section 3 budget flow |

The original flow is:

```
Task completes -> git diff -> run_wiring_analysis() -> emit_report() -> gate_passed() -> shadow/soft/full branch
```

The TurnLedger flow inserts budget checkpoints:

```
Task completes -> budget reconciliation -> can_run_wiring_gate()? -> debit_wiring() -> run_wiring_analysis() -> resolve_gate_mode() -> credit_wiring() or attempt_remediation()
```

Key structural differences:
1. Budget guard added before analysis (can skip entirely if budget exhausted)
2. `gate_passed()` call is now wrapped inside `resolve_gate_mode()` dispatch
3. Credit/debit accounting wraps the entire analysis lifecycle
4. Remediation path uses `attempt_remediation()` instead of inline policy invocation

---

### Section 4: Detailed Design

#### Section 4.1: Data Models (WiringFinding, WiringReport)

| Aspect | Status |
|--------|--------|
| WiringFinding | **Unchanged** |
| WiringReport | **Potentially modified** -- design references `report.scan_duration_seconds` (Section 4, line 268) which does not exist on the original WiringReport dataclass |

**Conflict C1**: The design references `report.scan_duration_seconds` in the
remediation path (`evaluation_ms=report.scan_duration_seconds * 1000`). The
original WiringReport has no such field. Either WiringReport must gain a
`scan_duration_seconds: float = 0.0` field, or the remediation code must
compute duration externally.

#### Section 4.2: Analysis Functions

| Aspect | Status |
|--------|--------|
| 4.2.1 Unwired Callable Analysis | **Unchanged** |
| 4.2.2 Orphan Module Analysis | **Unchanged** |
| 4.2.3 Unwired Registry Analysis | **Unchanged** |

All three analyzers are internal to `audit/wiring_gate.py` and have no
TurnLedger dependency. The design does not alter their algorithms.

#### Section 4.3: Report Format

| Aspect | Status |
|--------|--------|
| Report structure | **Unchanged** |
| 4.3.1 Frontmatter serialization | **Unchanged** |
| 4.3.2 Whitelist audit visibility | **Unchanged** |

The TurnLedger design does not modify report output format.

#### Section 4.4: Gate Definition (WIRING_GATE)

| Aspect | Status |
|--------|--------|
| WIRING_GATE constant | **Unchanged** |
| Semantic checks | **Unchanged** |

The gate definition remains a pure `GateCriteria` consumer. TurnLedger
integration happens at the executor level, not at the gate definition level.

#### Section 4.5: Sprint Integration

| Aspect | Status |
|--------|--------|
| Original text | **Replaced entirely** by design.md Sections 2-4 |

This is the primary replacement target. Every element of Section 4.5 is
affected:

**4.5a: Hook point location** -- STAYS. The hook remains at the post-task
classification point in `sprint/executor.py`.

**4.5b: Shadow mode flow (code block)** -- REPLACED. The 3-branch
`if/elif/elif` on `config.wiring_gate_mode` is replaced by:
1. `config.wiring_gate_enabled` boolean guard
2. `ledger.can_run_wiring_gate()` budget guard
3. `ledger.debit_wiring()` / `ledger.credit_wiring()` accounting
4. `resolve_gate_mode()` dispatch (returns TRAILING or BLOCKING)
5. `attempt_remediation()` path for BLOCKING failures

**4.5c: SprintConfig field** -- REPLACED.

| Before (original spec) | After (design.md) |
|---|---|
| `wiring_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"` | `wiring_gate_enabled: bool = True` |
| | `wiring_gate_scope: GateScope = GateScope.TASK` |
| | `wiring_gate_grace_period: int = 0` |

**4.5d: Function signature** -- MODIFIED. The hook gains a `ledger` parameter:

| Before | After |
|---|---|
| (implicit, inline in executor) | `run_post_task_wiring_hook(task, config, task_result, ledger=None) -> TaskResult` |

#### Section 4.6: Deviation Count Reconciliation

| Aspect | Status |
|--------|--------|
| Original text | **Unchanged** |
| TurnLedger impact | None |

The deviation count reconciliation is an independent companion gate on
`roadmap/gates.py`. It has no TurnLedger dependency.

---

### Section 5: File Manifest

| File | Original Action | TurnLedger Change |
|------|----------------|-------------------|
| `audit/wiring_gate.py` | CREATE 250-300 LOC | **Possibly +1 field** (scan_duration_seconds on WiringReport; see C1) |
| `audit/wiring_config.py` | CREATE 40-60 LOC | **Unchanged** |
| `sprint/models.py` | MODIFY +5 LOC | **Modified**: +5 becomes +30-40 LOC (3 new TurnLedger fields, 3 new methods, SprintConfig field replacement) |
| `sprint/executor.py` | MODIFY +25 LOC | **Modified**: +25 becomes +60-80 LOC (run_post_task_wiring_hook with budget flow, attempt_remediation path, ledger threading) |
| `roadmap/gates.py` | MODIFY +40 LOC | **Unchanged** |
| `sprint/kpi.py` | Not in original manifest | **New**: MODIFY +20-30 LOC (GateKPIReport wiring fields, build_kpi_report parameter) |
| `tests/audit/test_wiring_gate.py` | CREATE 200-250 LOC | **Unchanged** (core analysis tests) |
| `tests/audit/test_deviation_recon.py` | CREATE 60-80 LOC | **Unchanged** |
| `tests/audit/fixtures/` | CREATE 50-80 LOC | **Unchanged** |
| `tests/pipeline/test_full_flow.py` | Not in original manifest | **New**: MODIFY +80-120 LOC (scenarios 5-8) |
| `tests/sprint/test_models.py` | Not in original manifest | **New**: MODIFY +30-40 LOC (debit_wiring, credit_wiring, can_run_wiring_gate tests) |

**Revised totals:**

| Category | Original estimate | After TurnLedger |
|----------|-------------------|------------------|
| New production code | 360-430 LOC | 440-550 LOC |
| New test code | 310-410 LOC | 420-570 LOC |

---

### Section 6: Interface Contracts

#### Section 6.1: Public API

| Aspect | Status |
|--------|--------|
| `run_wiring_analysis()` | **Unchanged** |
| `emit_report()` | **Unchanged** |
| `check_wiring_report()` | **Unchanged** |
| `run_post_task_wiring_hook()` | **New** -- not in original Section 6.1 but defined in design.md Section 3.1 |

**Recommendation**: Add `run_post_task_wiring_hook` to Section 6.1 as a public
API with its full signature and docstring.

#### Section 6.2: Configuration Contract

| Aspect | Status |
|--------|--------|
| WiringConfig dataclass | **Unchanged** |
| SprintConfig additions | **Replaced** (see Section 4.5c above) |

#### Section 6.3: Gate Contract

| Aspect | Status |
|--------|--------|
| WIRING_GATE constant | **Unchanged** |
| Frontmatter contract table | **Unchanged** |
| `enforcement_mode` frontmatter field | **Conflict C2** (see below) |

**Conflict C2**: The original report format includes `enforcement_mode: shadow`
in frontmatter (Section 4.3 example). The TurnLedger design replaces mode
strings with `GateScope` + `resolve_gate_mode()`. The frontmatter field
`enforcement_mode` would need to be either:
- Kept as a human-readable label derived from the effective GateMode, or
- Replaced with `gate_scope` and `effective_gate_mode` fields.

---

### Section 7: Risk Assessment

| Risk | Status |
|------|--------|
| R1-R6 | **Unchanged** |
| New risks from design.md Section 9 | **Additive** |

New risks introduced by TurnLedger integration:

| Risk | Source |
|------|--------|
| R7: `int(1 * 0.8) = 0` makes single-turn reimbursement a no-op | design.md Section 3.2 and Section 9 |
| R8: SprintConfig field rename breaks existing configs | design.md Section 9 |
| R9: Ledger=None path skips remediation entirely | design.md Section 9 |

These should be merged into the original Section 7 table.

---

### Section 8: Rollout Plan

| Aspect | Status |
|--------|--------|
| Phase 1 (Shadow) | **Modified** -- pre-activation checklist stays, but mode mechanism changes from `wiring_gate_mode="shadow"` to `wiring_gate_scope=GateScope.TASK` + `grace_period=999999` |
| Phase 2 (Soft) | **Modified** -- enforcement mechanism changes from mode string to `GateScope.MILESTONE` |
| Phase 3 (Full) | **Modified** -- enforcement mechanism changes from mode string to `GateScope.RELEASE` |
| Rollout Decision Criteria | **Supplemented** -- design.md Section 5.4 adds transition checklist showing config-only phase changes |
| Threshold calibration | **Unchanged** -- FPR analysis and decision rules remain valid |
| Rollout Framework Integration | **Strengthened** -- TurnLedger integration makes this concrete rather than aspirational |

**Key improvement**: Phase transitions become config-only changes (one field
update) rather than code changes. The design.md Section 5.4 transition
checklist makes this explicit.

---

### Section 9: Testing Strategy

#### Section 9.1: Unit Tests

| Aspect | Status |
|--------|--------|
| analyze_unwired_callables tests (4) | **Unchanged** |
| analyze_orphan_modules tests (5) | **Unchanged** |
| analyze_unwired_registries tests (2) | **Unchanged** |
| emit_report / gate tests (3) | **Unchanged** |
| TurnLedger model tests | **New** -- design.md Section 8 item 8: tests for debit_wiring, credit_wiring, can_run_wiring_gate |

#### Section 9.2: Integration Tests

| Aspect | Status |
|--------|--------|
| SC-010 (cli-portify fixture) | **Unchanged** |
| SC-006 (shadow mode non-interference) | **Modified** -- must now also assert budget accounting (debit applied, credit applied on pass) |
| Scenarios 5-8 (TurnLedger flow tests) | **New** -- design.md Section 7 |

**Conflict C3**: The original SC-006 defines shadow mode non-interference as
"task status unchanged, no exception propagated, logger.info emitted." The
TurnLedger design adds budget side effects (debit_wiring always, credit_wiring
on pass) which are state changes on the ledger even in shadow mode. The SC-006
contract must be updated to either:
- Exclude ledger state from the "unchanged" assertion, or
- Explicitly assert the expected ledger mutations as part of the contract.

#### Section 9.3: Test Infrastructure

| Aspect | Status |
|--------|--------|
| Fixture directory | **Unchanged** |
| Coverage target | **Expanded** -- must now include coverage on TurnLedger wiring methods |

---

### Section 10: Success Criteria

| SC | Status |
|----|--------|
| SC-001 through SC-005 | **Unchanged** |
| SC-006 | **Modified** -- shadow mode contract now includes budget accounting assertions |
| SC-007 through SC-011 | **Unchanged** |
| SC-012 (new) | **New**: Budget integration -- `debit_wiring` and `credit_wiring` correctly track wiring analysis costs |
| SC-013 (new) | **New**: `reimbursement_rate` consumed in production -- `credit_wiring()` uses `self.reimbursement_rate` |
| SC-014 (new) | **New**: Backward compatibility -- `run_post_task_wiring_hook` works with `ledger=None` |
| SC-015 (new) | **New**: Remediation integration -- wiring failures in BLOCKING mode trigger `attempt_remediation()` |

---

### Section 11: Dependency Map

| Aspect | Status |
|--------|--------|
| Original diagram | **Modified** -- new edges added |

New dependency edges:

```
sprint/executor.py -> TurnLedger (debit_wiring, credit_wiring)  [NEW]
sprint/executor.py -> resolve_gate_mode()                        [NEW direct call]
sprint/executor.py -> attempt_remediation()                      [NEW]
sprint/kpi.py -> TurnLedger (wiring fields)                      [NEW]
```

The original claim "Zero changes to existing gate infrastructure" remains true.
TurnLedger extensions are on the sprint/models side, not on pipeline/models.

---

### Section 12: Tasklist Index

| Task | Status |
|------|--------|
| T01: Data models | **Modified** -- now includes TurnLedger field additions and SprintConfig field replacement |
| T02-T04: Analyzers | **Unchanged** |
| T05: Report emitter + WIRING_GATE | **Unchanged** |
| T06: Unit tests for analyzers | **Unchanged** |
| T07: Sprint integration | **Replaced** -- much larger scope; includes ledger threading, resolve_gate_mode() dispatch, attempt_remediation() path, null-ledger handling |
| T08-T09: Deviation reconciliation | **Unchanged** |
| T10: Integration test | **Modified** -- must include TurnLedger scenarios |
| T11: Retrospective | **Unchanged** |

New tasks introduced by TurnLedger integration:

| Task | Description | Deps |
|------|-------------|------|
| T01b | TurnLedger wiring extensions (3 fields, 3 methods) | -- |
| T01c | SprintConfig field migration (mode -> enabled + scope + grace) | -- |
| T06b | Unit tests for TurnLedger wiring methods | T01b |
| T07b | KPI report extension (`GateKPIReport` wiring fields, `build_kpi_report` param) | T01b |
| T10b | Integration tests: scenarios 5-8 (budget flow, remediation, null ledger, shadow deferred) | T07, T07b |

**Revised critical path**:

```
T01 + T01b + T01c (parallel) -> T02/T03/T04 (parallel) -> T05 -> T06 + T06b (parallel)
    -> T07 -> T07b -> T10 + T10b (parallel) -> T11
```

---

## 2. Exact Section/Requirement IDs Affected

### REQ-4.5: Sprint Integration (REPLACED)

**Before** (original spec Section 4.5):
```python
wiring_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"
```

With inline `if/elif/elif` dispatch on mode strings.

**After** (design.md Section 2.3):
```python
wiring_gate_enabled: bool = True
wiring_gate_scope: GateScope = GateScope.TASK
wiring_gate_grace_period: int = 0
```

With `resolve_gate_mode()` dispatch and TurnLedger budget accounting.

### REQ-6.2: Configuration Contract -- SprintConfig (REPLACED)

**Before**: Single field `wiring_gate_mode` added to SprintConfig.

**After**: Three fields (`wiring_gate_enabled`, `wiring_gate_scope`,
`wiring_gate_grace_period`) replace the single field.

### REQ-SC-006: Shadow Mode Non-Interference (MODIFIED)

**Before**: "Task status fields unchanged, no exception propagated, logger.info
emitted."

**After**: Same constraints, plus: "ledger.wiring_gate_cost incremented by
WIRING_ANALYSIS_TURNS; if analysis passed, ledger.wiring_gate_credits
incremented by credit amount."

### REQ-5: File Manifest (EXPANDED)

**Before**: 8 files, 360-430 production LOC.

**After**: 11 files, 440-550 production LOC. Three new file targets added
(`sprint/kpi.py`, `tests/pipeline/test_full_flow.py`,
`tests/sprint/test_models.py`).

### REQ-12: Tasklist (EXPANDED)

**Before**: 11 tasks (T01-T11).

**After**: 16 tasks (T01-T11 + T01b, T01c, T06b, T07b, T10b).

---

## 3. New Sections Introduced by TurnLedger Integration

### NEW-1: TurnLedger Budget Flow (design.md Section 3)

Complete budget lifecycle diagram showing debit-before-analysis,
credit-on-pass, remediation-on-blocking-fail. No equivalent exists in the
original spec. This becomes a new subsection under Section 4.5 (or a new
Section 4.5a).

### NEW-2: Remediation Path via attempt_remediation() (design.md Section 4)

The original spec mentions remediation only in passing ("Trigger remediation
via SprintGatePolicy" with `...` ellipsis). The design provides a complete
remediation flow including budget guards, retry semantics, and credit-on-
successful-remediation. This becomes a new Section 4.5b.

### NEW-3: Backward Compatibility Contract (design.md Section 6)

The `ledger=None` handling is entirely new. The original spec assumes a ledger
is always present (implicitly, by not mentioning it). This becomes a new
Section 6.4 or an addendum to Section 6.1.

### NEW-4: KPI Report Extension (design.md Section 7.3)

Wiring-specific KPI fields (`wiring_gates_evaluated`, `wiring_gates_passed`,
`wiring_total_debit`, etc.) and `build_kpi_report()` parameter extension. No
equivalent in the original spec. This becomes a new Section 4.7 or an addendum
to Section 4.3.

### NEW-5: reimbursement_rate Production Wiring Audit (design.md Section 10)

Audit trail showing `reimbursement_rate` was dead code and is now live. This is
documentation/justification, not a requirement. Include as Appendix C.

---

## 4. Risks and Conflicts

### Conflict C1: Missing scan_duration_seconds on WiringReport

**Source**: design.md Section 4 references `report.scan_duration_seconds` in
the `TrailingGateResult` construction for remediation.

**Original spec**: WiringReport (Section 4.1) has no `scan_duration_seconds`
field.

**Impact**: The remediation path cannot construct a `TrailingGateResult` with
`evaluation_ms` without this field.

**Severity**: Medium -- blocks remediation path implementation (T07 in BLOCKING
mode).

### Conflict C2: enforcement_mode Frontmatter Field Semantics

**Source**: Original Section 4.3 report example includes
`enforcement_mode: shadow`. The TurnLedger design eliminates mode strings
in favor of `GateScope` + `resolve_gate_mode()`.

**Original spec**: `enforcement_mode` is a required frontmatter field in
`WIRING_GATE.required_frontmatter_fields` (Section 4.4).

**Impact**: The field name and possible values may need updating.

**Severity**: Low -- the field can remain as a human-readable label derived
from the effective GateMode without changing gate evaluation logic.

### Conflict C3: SC-006 Shadow Mode Contract vs. Budget Side Effects

**Source**: Original SC-006 asserts "task status fields unchanged" in shadow
mode. TurnLedger design mutates ledger state (debit_wiring, credit_wiring) in
shadow mode.

**Impact**: Test assertion scope must be clarified -- is the contract about
TaskResult immutability (still holds) or about zero observable side effects
(no longer holds with ledger mutations)?

**Severity**: Low -- the intent of SC-006 is clearly about TaskResult
immutability and pipeline non-interference, not about ledger bookkeeping.

### Conflict C4: int(1 * 0.8) = 0 Renders Single-Turn Credits Meaningless

**Source**: design.md Section 3.2 acknowledges that with
`WIRING_ANALYSIS_TURNS=1` and `reimbursement_rate=0.8`, credit rounds to 0.

**Impact**: The core value proposition ("clean code is cheap") does not hold
at the default configuration. Every wiring check costs exactly 1 turn
regardless of outcome.

**Severity**: Medium -- undermines the incentive design. The mitigation
("set reimbursement_rate=1.0") shifts the default expectation.

### Conflict C5: SprintConfig Migration Burden

**Source**: design.md replaces `wiring_gate_mode` with three fields. However,
the original spec field `wiring_gate_mode` does not yet exist in production --
it is part of this release.

**Impact**: If the original spec is implemented first and the TurnLedger design
is applied later, a migration is needed. If both are implemented together, no
migration exists -- the three-field form is the initial implementation.

**Severity**: Low if implemented together; Medium if sequenced.

---

## 5. Recommended Resolutions

### Resolution for C1 (scan_duration_seconds)

Add `scan_duration_seconds: float = 0.0` to `WiringReport` in Section 4.1.
Populate it in `run_wiring_analysis()` using `time.monotonic()` around the
analysis calls. This is a minimal, non-breaking addition that supports both
the KPI reporting and remediation path needs.

### Resolution for C2 (enforcement_mode frontmatter)

Keep `enforcement_mode` as a required frontmatter field. Derive its value from
the effective `GateMode` returned by `resolve_gate_mode()`:

```python
enforcement_mode_label = {
    GateMode.TRAILING: "shadow",
    GateMode.BLOCKING: "full",
}
```

This preserves backward compatibility with report consumers and maintains
human-readable reports while eliminating mode strings from executor logic.

### Resolution for C3 (SC-006 contract)

Clarify SC-006 to state: "Task status fields (state, assignee, priority) in
the sprint manifest are unchanged. TurnLedger budget mutations (debit_wiring,
credit_wiring) are expected side effects and are not covered by this
non-interference contract."

### Resolution for C4 (int rounding)

Change `WIRING_ANALYSIS_TURNS` default to 0 (free analysis) with a 1-turn
penalty on failure. Alternatively, accept the cost as documented and rely on
accumulation across tasks for the rate to matter. The simplest fix: use
`reimbursement_rate=1.0` as the default for wiring-specific credits, separate
from the general TurnLedger rate. This avoids changing the shared rate semantics.

A second option: track wiring credits as fractional internally and floor only
on final reporting. This preserves incentive semantics without changing the
public API.

**Recommended**: Accept the 1-turn cost at default settings. Document it
clearly. The reimbursement rate becomes meaningful at higher analysis costs
(large packages) or accumulated over many tasks. Do not introduce fractional
accounting complexity for a v1.0 shadow-mode release.

### Resolution for C5 (SprintConfig migration)

Implement the three-field form (`wiring_gate_enabled`, `wiring_gate_scope`,
`wiring_gate_grace_period`) directly, skipping the intermediate
`wiring_gate_mode` field entirely. Since `wiring_gate_mode` does not yet exist
in production, there is no migration burden. The original spec's Section 4.5
should be updated to use the three-field form from the start.

If sequencing requires the original spec to land first, add a `__post_init__`
migration path as the design.md suggests (Section 9, risk row 2), but this
is the less desirable path.

---

## 6. Implementation Order Recommendation

The cleanest approach is to treat the TurnLedger design as a modification of
the original spec rather than a post-hoc addition. Concretely:

1. **Update Section 4.5 in the original spec** to use the TurnLedger-based
   sprint integration (design.md Sections 2-4, 6).
2. **Update Section 5 (File Manifest)** with revised LOC estimates and new
   file targets.
3. **Update Section 6 (Interface Contracts)** with `run_post_task_wiring_hook`
   API and SprintConfig three-field form.
4. **Update Section 9 (Testing)** with TurnLedger scenarios and revised SC-006.
5. **Update Section 10 (Success Criteria)** with SC-012 through SC-015.
6. **Update Section 12 (Tasklist)** with new tasks T01b, T01c, T06b, T07b, T10b.
7. **Add Appendix C** with the reimbursement_rate production wiring audit.

All other sections (1, 2, 3.2 module arch for audit/, 4.1-4.4, 4.6, 7, 8
rollout phases, 11 dependency map, Appendix A, Appendix B) require only minor
annotation or no changes.

The critical path does not change in structure, but T01 and T07 grow in scope.
The parallel track (T08/T09 deviation reconciliation) remains fully independent.
