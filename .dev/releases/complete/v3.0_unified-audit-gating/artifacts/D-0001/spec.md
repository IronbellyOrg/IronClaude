---
deliverable: D-0001
phase: 1
task: T01.01
title: Architecture Decision Log — Open Questions OQ-1 through OQ-7
date: 2026-03-19
status: committed
constraint: Zero pipeline substrate modification (no signature changes to SemanticCheck, GateCriteria, Step, GateMode, gate_passed(), TrailingGateRunner, DeferredRemediationLog)
---

# Architecture Decision Log — Wiring Verification Gate v2.0

All 7 open questions resolved below. Each adopts the proposed default from the roadmap Phase 0 table unless noted. Rationale references the source architect (Opus/Haiku/Both) and validates against the zero-pipeline-modification constraint.

---

## OQ-1: How are `audit_artifacts_used` located/counted?

**Question**: When the wiring analyzer optionally consumes cleanup-audit evidence as a false-positive suppressor (Section 6.6 authority rule), how does it discover and count those artifacts?

**Committed Answer**: Glob for `*-audit-report.yaml` in the output directory. The count of matched files is recorded as `audit_artifacts_used` in report frontmatter.

**Rationale**: Glob-based discovery is deterministic and convention-aligned with existing audit output naming. No configuration needed — the output directory is already known from the pipeline context. If no audit artifacts exist, `audit_artifacts_used = 0` and the analyzer operates purely on direct AST analysis, which is the authoritative mode per Section 6.6.

**Source**: Opus

**Pipeline constraint check**: No pipeline substrate touched. The glob runs against output artifacts, not pipeline internals.

---

## OQ-2: Are `exclude_patterns` matches counted in `files_skipped`?

**Question**: When `WiringConfig.exclude_patterns` (e.g., `test_*.py`, `conftest.py`, `__init__.py`) causes files to be excluded from analysis, are those files counted in the `files_skipped` frontmatter field?

**Committed Answer**: Yes. Files matching `exclude_patterns` increment `files_skipped` for visibility. This means `files_analyzed + files_skipped` equals the total Python files discovered in `target_dir`.

**Rationale**: Counting excluded files in `files_skipped` provides transparency about analysis scope. An operator reviewing the report can see exactly how many files were considered vs. analyzed. This supports the auditability design constraint ("every enforcement decision must be explainable from report frontmatter and evidence sections alone"). The alternative — silently excluding files — would make scope gaps invisible.

**Source**: Opus

**Pipeline constraint check**: No pipeline changes. `files_skipped` is a frontmatter field in the emitted report, validated by `WIRING_GATE.required_frontmatter_fields` which is defined in `audit/wiring_gate.py`.

---

## OQ-3: Is whitelist strictness derived from `rollout_mode`?

**Question**: How strictly should malformed whitelist entries (missing `symbol` or `reason` fields) be handled? Should strictness vary by rollout mode?

**Committed Answer**: Yes, strictness is mode-dependent:
- **shadow**: Malformed entries are logged as WARNING and skipped. Analysis continues.
- **soft/full**: Malformed entries raise `WiringConfigError`, halting analysis.

**Rationale**: During shadow mode, the gate is non-blocking and the priority is data collection. Halting on a malformed whitelist entry would prevent shadow data gathering for no enforcement benefit. Once the gate is in soft or full mode, enforcement decisions depend on whitelist correctness — a malformed entry could silently suppress a real finding, so strict validation is warranted. This graduated approach matches the three-phase rollout philosophy.

**Source**: Opus

**Pipeline constraint check**: No pipeline changes. `WiringConfigError` is raised in `audit/wiring_config.py`. Whitelist loading is entirely within the new `audit/` modules.

**Interaction note**: This decision interacts with OQ-5 (comparator/consolidator scope) only at the behavioral level — both are additive. No technical coupling.

---

## OQ-4: Does `SprintConfig.source_dir` already exist?

**Question**: The sprint integration (Section 5.8) calls `run_wiring_analysis(target_dir=config.source_dir)`. Does `SprintConfig` already have a `source_dir` field, or does one need to be added?

**Committed Answer**: Verify before Phase 3b implementation. If `source_dir` does not exist on `SprintConfig`, add it as part of Phase 3b task 3b.1 alongside the `wiring_gate_mode` field addition.

**Rationale**: This is a factual question requiring code inspection at implementation time. The roadmap correctly defers verification to Phase 3b rather than Phase 0 because: (a) Phase 3b is when sprint integration begins, (b) the answer determines ~5 LOC of additional work at most, and (c) verifying now would add no value since the field could be added/renamed between now and Phase 3b.

**Source**: Opus

**Pipeline constraint check**: Any `source_dir` addition is to `sprint/models.py`, not `pipeline/*`.

---

## OQ-5: Comparator/consolidator extension scope?

**Question**: How much should the audit-comparator and audit-consolidator agents be modified for wiring awareness? Should they be restructured to handle wiring data natively?

**Committed Answer**: Additive wiring sections only, no restructure. Specifically:
- **audit-comparator**: Add a cross-file wiring consistency check (Section 6.1, Table row 4).
- **audit-consolidator**: Add a "Wiring Health" section to the final report (Section 6.1, Table row 5).

No existing agent tools change. No existing agent rules are removed. No report format restructuring.

**Rationale**: The agents are behavioral specs (`.md` files). Restructuring their output format risks emergent regression in LLM-interpreted behavior (Risk R7, MEDIUM severity). Additive sections are testable independently and do not alter existing tool access or rule sets. This aligns with the Section 6.1 constraint: "All 5 agents are behavioral specs. Extensions are additive — no tools change, no existing rules removed."

**Source**: Haiku

**Pipeline constraint check**: Agent specs are in `src/superclaude/agents/`, completely outside `pipeline/*`.

---

## OQ-6: Rollout ownership for `grace_period`?

**Question**: Who owns the shadow metrics collection, FPR calibration, and the activation decision from shadow to soft to full enforcement? How does `grace_period` interact with shadow mode?

**Committed Answer**: Single accountable owner for shadow metrics and activation decisions. The owner is responsible for:
1. Monitoring shadow findings across release cycles (Phase 6a tasks 6a.1-6a.5)
2. Computing FPR/TPR/latency statistics
3. Producing the readiness report with explicit recommendation (Phase 6a task 6a.6)
4. Making the soft-mode and full-mode activation decisions (Phase 6b)

**`grace_period` interaction** (from Section 7, Phase 1 operational note): Roadmap configurations should set `grace_period > 0` during shadow rollout to enable `GateMode.TRAILING` behavior via `TrailingGateRunner`. If `grace_period = 0` forces BLOCKING, shadow mode still passes because `_zero_blocking_findings_for_mode` reads `rollout_mode=shadow` from frontmatter and returns True unconditionally, and the emitter sets `blocking_findings=0` in shadow mode. However, TRAILING mode provides cleaner operational semantics.

**Rationale**: Shadow-to-soft activation requires statistical judgment (FPR calibration formula: `measured_FPR + 2σ < 15%`). Distributing this across multiple people risks diffusion of responsibility and premature activation. A single owner can hold the line on "Phase 2 MUST NOT activate if unwired-callable FPR cannot be separated from noise" (Section 7 Phase 2).

**Source**: Haiku

**Pipeline constraint check**: `grace_period` is read from existing pipeline configuration, not modified. `TrailingGateRunner` is consumed as-is. No pipeline substrate changes.

---

## OQ-7: Merge sequencing with concurrent PRs?

**Question**: How should merge sequencing be handled given that `roadmap/gates.py` is a shared modification point with concurrent PRs (e.g., Anti-Instincts `ANTI_INSTINCT_GATE` in v3.05, Unified Audit Gating `SPEC_FIDELITY_GATE` extensions)?

**Committed Answer**: Complete Phases 1-2 before touching shared files. Specifically:
- Phases 1-2 create new files only (`audit/wiring_gate.py`, `audit/wiring_config.py`, `audit/wiring_analyzer.py`, test files) — no merge conflict risk.
- Phase 3a modifies `roadmap/executor.py`, `roadmap/gates.py`, and `roadmap/prompts.py` — these are the shared-file touchpoints requiring coordination.
- Preferred: single coordinated PR or sequenced PRs with explicit rebase points (Section 15).

**Rationale**: Phases 1-2 represent ~70% of the implementation work and touch zero shared files. By completing them first, the conflict-prone modifications (Phase 3a: ~35 LOC across 3 files) are isolated to a small, reviewable changeset that can be rebased against whatever concurrent changes have landed.

**Source**: Both (Opus + Haiku)

**Pipeline constraint check**: The shared files (`roadmap/gates.py`, `roadmap/executor.py`) are in `roadmap/*`, not `pipeline/*`. Zero pipeline substrate modifications in any phase.

---

## Summary Validation

| OQ | Answer Committed | Rationale Present | Source Cited | Pipeline Constraint Respected |
|----|-----------------|-------------------|-------------|-------------------------------|
| OQ-1 | Yes | Yes | Opus | Yes |
| OQ-2 | Yes | Yes | Opus | Yes |
| OQ-3 | Yes | Yes | Opus | Yes |
| OQ-4 | Yes (deferred verification) | Yes | Opus | Yes |
| OQ-5 | Yes | Yes | Haiku | Yes |
| OQ-6 | Yes | Yes | Haiku | Yes |
| OQ-7 | Yes | Yes | Both | Yes |

All 7 decisions are self-contained and do not require external documents to interpret. No decision contradicts the zero-pipeline-substrate-modification constraint.
