# HIGH Issues — Synthesis Summary

> Generated: 2026-03-20
> Source: 7 parallel brainstorm agents, one per HIGH issue (ISS-004 through ISS-010)
> Input: issues-classified.md, CompatibilityReport-Merged.md, deterministic-fidelity-gate-requirements.md

## Overview

| ID | Issue | Selected Proposal | CRITICAL Dependency | Spec Sections |
|----|-------|-------------------|---------------------|---------------|
| ISS-004 | Diff-size threshold 30% vs 50% | B (defer to ISS-003) | ISS-003 | FR-9 |
| ISS-005 | Diff-size granularity per-patch vs per-file | B (replace AC bullet 5) | ISS-003 | FR-9 |
| ISS-006 | Rollback scope per-file vs all-or-nothing | C (per-file + coherence check) | ISS-003 | FR-9 |
| ISS-007 | MorphLLM vs ClaudeProcess remediation model | A (ClaudeProcess-primary, adapter) | ISS-003 | FR-9 |
| ISS-008 | DeviationRegistry location (own file vs convergence.py) | A (remove from manifest) | ISS-001 | FR-6 |
| ISS-009 | Severity rule tables — foundational, no code exists | A (inline with canonical keys) | None | FR-3 |
| ISS-010 | Remediation ownership — post-pipeline vs convergence loop | A (integration approach) | ISS-001, ISS-003 | FR-7, FR-9 |

---

## Per-Issue Decisions

### ISS-004: Diff-size threshold mismatch (30% vs 50%)

**Selected**: Proposal B — Defer to ISS-003 resolution

**Rationale**: ISS-003's recommended Proposal #1 already includes the threshold change as delta item 5: `MODIFY _DIFF_SIZE_THRESHOLD_PCT: 50 -> 30 (ISS-004)`. A standalone spec edit would be redundant and overwritten when ISS-003 is applied. The spec is internally consistent at 30% across six locations — the code at `remediate_executor.py:45` is the sole outlier.

**Fallback**: If ISS-003 is delayed or resolved with a proposal that omits the threshold, escalate to Proposal C (belt-and-suspenders: add 30% to FR-9 description + cross-reference ISS-003).

**CRITICAL dependency**: ISS-003 must be resolved first. Validation checklist in proposal file.

---

### ISS-005: Diff-size granularity mismatch (per-patch vs per-file)

**Selected**: Proposal B — Replace AC bullet 5 with implementation-ready contract

**Rationale**: The current one-line AC is too terse. Proposal B expands it to a multi-line contract that explicitly retires the v3.0 `_check_diff_size()` whole-file approach, specifies per-patch evaluation of `RemediationPatch` objects, and handles partial rejection. It avoids adding a new FR-9.2 sub-section (Proposal A) or prescribing full function signatures (Proposal C).

**Key finding**: The entire patch-based flow (RemediationPatch, apply_patches) does not exist yet — per-patch checking requires this infrastructure as a prerequisite.

**CRITICAL dependency**: ISS-003 must be applied first (establishes MODIFY framing for FR-9).

---

### ISS-006: Rollback scope mismatch (per-file vs all-or-nothing)

**Selected**: Proposal C — Per-file rollback with post-execution coherence check

**Rationale**: The snapshot primitives (`create_snapshots`, `restore_from_snapshots`) already operate per-file. The all-or-nothing behavior lives solely in the orchestration layer (`_handle_failure()`). Proposal C lets all agents complete in parallel, then evaluates each file independently, with a coherence pass that rolls back successful files sharing cross-file findings with failed files. This balances partial progress (critical for 3-run convergence budget) with correctness.

**Key finding**: `_handle_failure()` is the single point of change — it calls `restore_from_snapshots(all_target_files)` and `executor.shutdown()`. Per-file rollback requires replacing this with per-file evaluation + coherence check.

**CRITICAL dependency**: ISS-003 must be applied first. ISS-005 is tightly coupled (per-patch rejection determines per-file outcomes).

---

### ISS-007: MorphLLM vs ClaudeProcess remediation model

**Selected**: Proposal A — ClaudeProcess-primary with MorphLLM-compatible format (adapter pattern)

**Rationale**: All remediation uses ClaudeProcess (zero MorphLLM integration exists). Proposal A reframes FR-9 to make ClaudeProcess the primary engine while retaining the MorphLLM-compatible JSON patch schema as the data format. It introduces a three-tier applicator hierarchy: ClaudeProcess → deterministic fallback → future MorphLLM. This is honest about current state while preserving the migration path that was adversarial-reviewed (BF-5, Resolved Question #3).

**Rejected alternatives**: Proposal B (drop all MorphLLM refs) is most honest but discards context stakeholders already approved. Proposal C (Protocol interface) is over-engineering — YAGNI until MorphLLM integration is real.

**CRITICAL dependency**: ISS-003 must be applied first (rewrites FR-9 Description block).

---

### ISS-008: DeviationRegistry location (own file vs convergence.py)

**Selected**: Proposal A — Remove `deviation_registry.py` from manifest, accept current location

**Rationale**: DeviationRegistry (176 lines, 11 methods) is tightly coupled with `compute_stable_id()`, `_check_regression()`, and the convergence loop orchestrator (yet to be built). Co-location is the correct architecture. The spec's `relates_to` entry for `deviation_registry.py` is a phantom — no such file exists or should exist. FR-6 description is updated to reference the class's actual location in `convergence.py:50-225`.

**If ISS-001 Proposal #3 is adopted** (frontmatter disposition table), add: `deviation_registry.py: REMOVE_FROM_MANIFEST`.

**CRITICAL dependency**: ISS-001 must be applied first (governs convergence.py disposition).

---

### ISS-009: Severity rule tables — foundational, no code exists

**Selected**: Proposal A — Inline rule table with canonical machine keys, extend FR-3 in-place

**Rationale**: FR-3 is genuinely new infrastructure (zero code exists). The spec's rule table uses prose descriptions while the architecture design uses machine keys (`phantom_id`, `function_missing`, etc.) — this gap must be closed. Proposal A adds canonical keys, an implementation contract (`SEVERITY_RULES` dict, `get_severity()` function), a baseline statement, and surfaces the ISS-024 dependency (Finding field extension). It also adds 4 mismatch types from the architecture design that the original spec omitted.

**No CRITICAL dependency**: FR-3 is new code with no CREATE-vs-MODIFY conflict. Can be implemented immediately. Only prerequisite is ISS-024 (Finding field extension, LOW severity).

---

### ISS-010: Remediation ownership — post-pipeline vs convergence loop

**Selected**: Proposal A — Convergence loop wraps existing remediation (integration approach)

**Rationale**: The new `execute_fidelity_with_convergence()` function (identified by ISS-001) calls `execute_remediation()` between convergence runs. remediate_executor.py stays unchanged — it remains a pure execution engine. The convergence loop owns the budget (3 runs) and translates remediation results into DeviationRegistry updates. Legacy mode is completely untouched.

**Key insight**: Two different budget systems coexist — convergence has 3 runs, legacy has 2 remediation attempts. They must never overlap. In convergence mode, `_check_remediation_budget()` and `_print_terminal_halt()` are NOT invoked.

**CRITICAL dependency**: Both ISS-001 and ISS-003 must be applied first.

---

## Cross-Cutting Themes

### Theme 1: FR-9 Cluster (ISS-004, ISS-005, ISS-006, ISS-007)

Four of seven HIGH issues affect FR-9 (Edit-Only Remediation with Diff-Size Guard). All four depend on ISS-003 (CRITICAL) being resolved first. They form a coherent cluster:

- **ISS-003** (CRITICAL): Reclassify FR-9 from CREATE to MODIFY → establishes baseline/delta framing
- **ISS-007**: Reframe MorphLLM → ClaudeProcess-primary within that delta
- **ISS-005**: Replace per-file diff-size guard with per-patch evaluation
- **ISS-004**: Threshold value (subsumed by ISS-003 delta item 5)
- **ISS-006**: Rollback scope from all-or-nothing to per-file with coherence check

These four must be applied in sequence after ISS-003, since each modifies FR-9 text that the previous may have touched.

### Theme 2: Convergence Architecture (ISS-008, ISS-010)

Both issues relate to the convergence loop's relationship with other modules:

- **ISS-008**: DeviationRegistry stays in convergence.py (no extraction needed)
- **ISS-010**: Convergence loop wraps remediation (remediate_executor.py stays standalone)

Both depend on ISS-001 (CRITICAL) establishing convergence.py's MODIFY disposition. Together they confirm: convergence.py is the orchestration hub, other modules are execution engines called by it.

### Theme 3: Genuinely New Infrastructure (ISS-009)

ISS-009 stands alone — FR-3 severity rule tables are the only HIGH issue with zero existing code and no CRITICAL dependency. It's the foundational building block for FR-1 → FR-6 → FR-7 → FR-8 cascade.

---

## Recommended Execution Order

```
Phase 0: CRITICAL resolutions (prerequisite for most HIGH issues)
├── ISS-001: convergence.py CREATE → MODIFY
├── ISS-002: semantic_layer.py CREATE → MODIFY
└── ISS-003: remediate_executor.py CREATE → MODIFY

Phase 1: Independent HIGH (no CRITICAL dependency)
└── ISS-009: FR-3 severity rule tables (canonical keys + implementation contract)

Phase 2: FR-9 cluster (depends on ISS-003)
├── ISS-007: MorphLLM → ClaudeProcess-primary (modifies FR-9 Description)
├── ISS-005: Per-patch diff-size guard (modifies FR-9 AC bullet 5)
├── ISS-004: Threshold 30% (subsumed by ISS-003 — verify only)
└── ISS-006: Per-file rollback (modifies FR-9 AC bullets 9-10)

Phase 3: Convergence architecture (depends on ISS-001 + ISS-003)
├── ISS-008: Remove deviation_registry.py from manifest (modifies frontmatter + FR-6)
└── ISS-010: Intra-loop remediation (modifies FR-7 + FR-9 integration)
```

**Phase 1 can run in parallel with Phase 0.** Phases 2 and 3 are blocked on Phase 0 completion. Within Phase 2, ISS-007 should go first (modifies Description), then ISS-005 (modifies AC), then ISS-006 (extends AC). ISS-004 is a verification-only step.

**Phase 3 depends on both ISS-001 and ISS-003**, so it starts only after Phase 0 is fully complete. ISS-008 and ISS-010 are independent of each other and can run in parallel.
