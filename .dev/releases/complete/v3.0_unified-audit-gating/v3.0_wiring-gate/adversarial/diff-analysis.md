---
title: Diff Analysis — Wiring Verification Gate Spec Variants
timestamp: 2026-03-18T00:00:00Z
variant_count: 3
total_differences_found: 67
category_counts:
  structural: 12
  content: 22
  contradictions: 11
  unique_contributions: 14
  shared_assumptions: 8
---

# Diff Analysis: Wiring Verification Gate — Three Spec Variants

## Metadata

| Field | Value |
|-------|-------|
| Analysis date | 2026-03-18 |
| Variants compared | 3 (Variant A, Variant B, Variant C) |
| Total differences found | 67 |
| Structural differences | 12 |
| Content differences | 22 |
| Contradictions | 11 |
| Unique contributions | 14 |
| Shared assumptions | 8 |
| Depth | deep |

---

## Structural Differences (S-NNN)

### S-001: Top-Level Section Count and Naming

**Severity: Medium**

| Variant | Section Count | Numbering Range |
|---------|--------------|-----------------|
| A | 15 sections | 1-15 |
| B | 14 sections + 3 appendices | 1-14 + Appendix A/B/C |
| C | 18 sections | 1-18 |

Variant A uses a flat 15-section layout. Variant B uses 14 numbered sections plus 3 appendices for reference material. Variant C uses 18 sections, the most granular decomposition. The additional sections in C come from separating Data Models (Section 6), Report Format (Section 7), and Gate Definition (Section 8) into standalone sections, whereas A and B embed these within larger architecture/design sections.

### S-002: Frontmatter Schema Divergence

**Severity: Medium**

| Variant | Frontmatter Fields |
|---------|-------------------|
| A | title, release, status, date, owner, inputs, scope |
| B | release, version, status, date, supersedes, branch, parent_analysis, priority, estimated_scope |
| C | release, version, status, date, parent_specs, phase1_findings, priority, estimated_scope |

Variant A uses `title` and `owner` fields absent from B and C. Variant B uniquely includes `supersedes` (listing two prior specs) and `branch`. Variant C uses `parent_specs` (singular reference) vs B's `parent_analysis` (multiple references). Only B and C include `version`, `priority`, and `estimated_scope`.

### S-003: Problem Statement Structure

**Severity: Low**

Variant A (Section 1) presents a prose problem statement with a bullet list of 5 representative findings. Variant B (Section 1) uses a table with 5 rows breaking findings into System/Pattern/Count columns, plus a "What changed from v1.0" subsection. Variant C (Section 1) uses a 3-row table with Category/Count/Example columns. B and C both cite "32 unwired symbols across 14 files"; A does not provide aggregate counts.

### S-004: Architecture Section Depth

**Severity: Medium**

Variant A splits architecture into "Current Architecture Reality" (Section 4) and "Proposed Architecture" (Section 5), with subsections 5.1-5.4. Variant B consolidates into a single "Architecture" section (Section 4) with subsections 4.1-4.3 plus "Detailed Design" (Section 5) with subsections 5.1-5.7. Variant C uses "Architecture" (Section 4) with subsections 4.1-4.4. B is the deepest, with 7 detailed design subsections providing code-level implementation guidance.

### S-005: Detection Design Heading Level

**Severity: Low**

Variant A uses `## 6. Detection Design` with sub-headings `## 6.1`, `## 6.2`, `## 6.3` (inconsistent: `##` for both parent and child). Variant B uses `## 5. Detailed Design` with `### 5.2` containing sub-headings `#### 5.2.1`, `#### 5.2.2`, `#### 5.2.3`. Variant C uses `## 5. Detection Design` with `### 5.1`, `### 5.2`, `### 5.3`. B's nesting is deepest (4 levels); C is cleanest (3 levels).

### S-006: Presence of Explicit Decision Table

**Severity: Low**

Variant A (Section 13) lists 5 decisions with "Adopt" dispositions but no rationale column. Variant B (Section 14) lists 7 decisions in a table with Decision/Rationale columns. Variant C has no standalone decision section; decisions are embedded contextually throughout the document (e.g., "Execution approach: Deterministic Python analysis... This avoids LLM-dependent detection" in Section 4.4.1).

### S-007: Appendix Usage

**Severity: Low**

Only Variant B includes appendices. Appendix A is a substrate reference table (15 symbols with exact line numbers). Appendix B is a forensic cross-reference mapping findings to spec sections and tasks. Appendix C is an explicit out-of-scope list. Variants A and C embed equivalent content inline or omit it.

### S-008: Tasklist Structure Granularity

**Severity: Medium**

| Variant | Tasks | Columns | Parallel Tracks |
|---------|-------|---------|-----------------|
| A | 4 tracks (named, not numbered) | Description only | Critical path described in prose |
| B | 12 tasks (T01-T12) | Description, Deps, LOC | 1 critical path |
| C | 13 tasks (T01-T13) | Description, Deliverables, Deps | 1 critical path + 2 parallel tracks |

Variant A provides the least actionable tasklist: 4 named tracks without task-level decomposition. Variant C is most granular with 13 tasks, explicit deliverables, and named parallel tracks. Variant B sits between with 12 tasks and LOC estimates per task.

### S-009: Testing Strategy Organization

**Severity: Medium**

Variant A has no testing section. Variant B (Section 10) specifies minimum 20 unit tests and 3 integration tests in a table format. Variant C (Section 15) specifies minimum 14 unit tests and 2 integration tests, broken down per-function with numbered test cases and expected outcomes. C's per-test-case enumeration is more prescriptive; B's count is higher but descriptions are less specific.

### S-010: Success Criteria Formatting

**Severity: Low**

Variant A (Section 12) uses a numbered prose list (9 criteria). Variant B (Section 11) uses a table with SC-NNN IDs, Description, and Verification columns (14 criteria). Variant C (Section 17) uses a table with SC-NNN IDs, Description, and Verification columns (12 criteria). B has the most success criteria; A the fewest. B and C use formal IDs; A does not.

### S-011: Risk Assessment Presence and Format

**Severity: Medium**

Variant A has no risk assessment section. Variant B (Section 9) uses a table with Risk/L/I/Mitigation columns (8 risks, R1-R8). Variant C (Section 14) uses Risk/Likelihood/Impact/Mitigation columns (7 risks, R1-R7). Both B and C identify provider_dir_names misconfiguration as High/High risk.

### S-012: Interface Contracts Section

**Severity: Medium**

Variant A has no dedicated interface contracts section; public API is mentioned in Section 5.1 as "Suggested public surface." Variant B (Section 8) includes Public API, Gate Contract (table with 13 fields), and Dependency Direction subsections. Variant C (Section 13) includes Public API, Gate Contract (text), and Dependency Direction subsections. B's gate contract table is the most detailed, with explicit type and pass-condition columns.

---

## Content Differences (C-NNN)

### C-001: Version Identity and Lineage

**Severity: Medium**

Variant A labels itself as an unnamed draft under `v3.0_wiring-gate`. Variant B explicitly labels itself `v2.0.0` and lists what it supersedes: "wiring-verification-gate-v1.0" and "v3.0_wiring-gate spec.md (prior draft from roadmap pipeline)." Variant C labels itself `v1.0.0` with a `parent_specs` reference to the v1.0 release spec. The versioning is inconsistent: B claims to be v2.0 superseding both A and C's lineage, while C claims to be v1.0. This affects which document is considered authoritative.

### C-002: Scope — Sprint Integration

**Severity: High**

Variant A scopes the release to "roadmap post-merge wiring-verification gate" only (frontmatter `scope` field). Sprint integration is not mentioned anywhere in Variant A. Variant B includes full sprint integration: `SprintConfig.wiring_gate_mode`, post-task hook in `sprint/executor.py`, and "Mode B: Sprint Post-Task Check" as a first-class operation mode. Variant C also includes sprint integration with identical `wiring_gate_mode` field and post-task hook code. A's scope is strictly roadmap; B and C extend to sprint.

### C-003: Scope — Cleanup-Audit Agent Extension Depth

**Severity: High**

Variant A (Section 5.4) describes cleanup-audit reuse at a principle level: "extend audit-analyzer evidence collection" with 5 recommended field additions. Variant B (Section 6) provides detailed agent-by-agent extension tables for all 5 agents with specific field names, new finding types (`UNWIRED_DECLARATION`, `BROKEN_REGISTRATION`), and a new Check 5 for audit-validator. Variant C (Section 4.4.3) provides agent extension tables similar to B but with different field names (e.g., `wiring_surfaces`/`registry_symbols` vs `Wiring path`). B is most prescriptive with a dedicated 9th mandatory field; A is most abstract.

### C-004: ToolOrchestrator AST Analyzer Plugin

**Severity: High**

Variant A does not mention `ToolOrchestrator` at all. Variant B (Section 5.3) provides a full implementation of `ast_analyze_file()` as a `ToolOrchestrator` plugin in a dedicated `wiring_analyzer.py` module, with code showing `FileAnalysis` population. Variant C mentions the `ToolOrchestrator` extension (Section 4.4.3) at a design level: "Create an AST-aware analyzer that populates the currently-empty `references` field." B has implementation-level detail; C has design-level description; A omits entirely.

### C-005: Gate Naming Convention

**Severity: Low**

Variant A uses `WIRING_VERIFICATION_GATE` as the gate constant name (Sections 5.2, 5.3, 7.4). Variant B uses `WIRING_GATE` (Section 5.5). Variant C uses `WIRING_GATE` (Section 8). Two variants agree on the shorter name; one uses the longer form.

### C-006: Semantic Check Design Philosophy

**Severity: High**

Variant A (Section 5.2) and Variant B (Section 5.5) use a **mode-aware enforcement** approach: a single `_zero_blocking_findings_for_mode` check that reads `rollout_mode` from frontmatter and interprets `blocking_findings` accordingly. Shadow always passes; soft blocks on critical; full blocks on critical+major.

Variant C (Section 8) uses **per-category zero checks**: `_zero_unwired_callables`, `_zero_orphan_modules`, `_zero_unwired_registries`, plus `_total_findings_consistent`. There is no mode-aware check. The gate always requires all counts to be zero for a pass.

This is a fundamental design divergence. A and B encode rollout policy into the report artifact (via `blocking_findings` computed per mode). C's gate definition always requires zero findings, meaning rollout control must happen external to the semantic checks (presumably via `GateMode.TRAILING` making the whole gate non-blocking in shadow).

### C-007: Frontmatter Field Set

**Severity: Medium**

| Field | A | B | C |
|-------|---|---|---|
| `gate` | Yes | Yes | Yes |
| `target_dir` / `analysis_scope` | `analysis_scope` | `target_dir` | `target_dir` |
| `files_analyzed` | Yes | Yes | Yes |
| `rollout_mode` / `enforcement_mode` | `rollout_mode` | `rollout_mode` | `enforcement_mode` |
| `analysis_complete` | Yes | Yes | Yes |
| `audit_artifacts_used` | int | int | bool |
| `unwired_callable_count` / `unwired_count` | `unwired_callable_count` | `unwired_callable_count` | `unwired_count` |
| `orphan_symbol_count` / `orphan_module_count` / `orphan_count` | `orphan_symbol_count` | `orphan_module_count` | `orphan_count` |
| `unregistered_dispatch_count` / `unwired_registry_count` / `registry_count` | `unregistered_dispatch_count` | `unwired_registry_count` | `registry_count` |
| `critical_count` | Yes | Yes | No |
| `major_count` | Yes | Yes | No |
| `info_count` | Yes | No | No |
| `total_findings` | Yes | Yes | Yes |
| `blocking_findings` | Yes | Yes | No |
| `severity_summary` (nested) | Yes | Yes (flat) | No |
| `whitelist_entries_applied` | No | Yes | Yes |

Key divergence: C omits severity-level counts (`critical_count`, `major_count`) and `blocking_findings`. A includes a nested `severity_summary` YAML block. B flattens severity into top-level fields. C uses `audit_artifacts_used` as boolean; A and B use integer.

### C-008: Rollout Mode Naming

**Severity: Low**

Variant A uses `rollout_mode` in frontmatter. Variant B uses `rollout_mode`. Variant C uses `enforcement_mode`. The semantic meaning is identical, but the field name differs in C.

### C-009: Report Body Section Requirements

**Severity: Medium**

Variant A (Section 7.3) specifies 7 required body sections: Summary, Unwired Optional Callable Injections, Orphan Modules/Symbols, Unregistered Dispatch Entries, Suppressions and Dynamic Retention, Recommended Remediation, Evidence and Limitations.

Variant B specifies frontmatter and gate definition but does not enumerate required body sections explicitly.

Variant C does not specify required body sections.

Only A prescribes report body structure.

### C-010: Step Timeout Configuration

**Severity: Low**

| Variant | timeout_seconds | retry_limit |
|---------|----------------|-------------|
| A | 60 | 0 |
| B | 60 | 0 |
| C | 120 | 1 |

Variant C allows 120 seconds and 1 retry. A and B allow 60 seconds and 0 retries. For a deterministic step, retries are arguably unnecessary (A and B's position), but C's allowance could handle transient filesystem issues.

### C-011: Gate Mode for Shadow Phase

**Severity: Medium**

All three variants use `GateMode.TRAILING` for shadow mode in the roadmap pipeline. However, Variant B additionally specifies that `resolve_gate_mode()` forces release-scope gates to BLOCKING, and explicitly sets `gate_mode=GateMode.TRAILING` on the Step definition to override this. Variant A notes this constraint in Section 4.3 but does not show the Step-level override. Variant C sets `gate_mode=GateMode.TRAILING` on the Step without discussing the `resolve_gate_mode()` interaction.

### C-012: Number of New Files

**Severity: Medium**

| Variant | New Production Files | New Test Files |
|---------|---------------------|----------------|
| A | 1 (`wiring_gate.py`) | 2 |
| B | 3 (`wiring_gate.py`, `wiring_config.py`, `wiring_analyzer.py`) | 3 + fixtures |
| C | 2 (`wiring_gate.py`, `wiring_config.py`) | 2 + fixtures |

Variant B creates the most files due to the dedicated `wiring_analyzer.py` for ToolOrchestrator integration. Variant A consolidates everything into a single production file. Variant C splits config out but does not create the analyzer module.

### C-013: LOC Estimates

**Severity: Low**

| Variant | Production LOC | Test LOC |
|---------|---------------|----------|
| A | Not specified | Not specified |
| B | 480-580 | 370-480 |
| C | 360-430 | 310-410 |

Variant A provides no LOC estimates. B estimates 25-35% more production code than C, largely due to the `wiring_analyzer.py` module (140-180 LOC).

### C-014: WiringFinding Severity Enum Values

**Severity: Medium**

Variant A (Section 5.1): `severity` field not shown in dataclass but severity policy defines critical/major/info. Variant B (Section 5.1): `severity: Literal["critical", "major", "info"] = "critical"`. Variant C (Section 6): `severity: Literal["critical", "major"] = "critical"`. C omits `info` as a valid severity level, which means whitelisted intentional optionals cannot be represented as info-level findings in C's model.

### C-015: Orphan Detection Scope

**Severity: Medium**

Variant A (Section 6.2) targets "top-level helpers in `gates.py`", "provider modules in `steps/`, `handlers/`, `validators/`, `checks/`", "gate policy classes", and "modules whose only references are local or documentary." Variant B (Section 5.2.2) targets "Python files in provider directories" identified by convention with configurable `provider_dir_names`. Variant C (Section 5.2) uses the same configurable `provider_dir_names` approach as B. A's scope is broader (includes gate policy classes and locally-referenced-only modules); B and C limit to provider directories.

### C-016: Registry Pattern Set

**Severity: Low**

All three variants define similar registry patterns. Variant A (Section 6.3) lists: `*_REGISTRY`, `*_DISPATCH`, `*_HANDLERS`, `*_ROUTER`, `*_BUILDERS`, `*_MATRIX`. Variant B (Section 5.2.3) lists: `STEP_REGISTRY`, `STEP_DISPATCH`, `PROGRAMMATIC_RUNNERS`, `*_REGISTRY`, `*_DISPATCH`, `*_HANDLERS`, `*_ROUTER`, `*_BUILDERS`. Variant C (Section 5.3) matches B exactly. Only A includes `*_MATRIX`. Only B and C include specific named registries (`STEP_REGISTRY`, `STEP_DISPATCH`, `PROGRAMMATIC_RUNNERS`).

### C-017: Suppression File Format

**Severity: Low**

Variant A (Section 10.2) requires each suppression to include "target symbol or file", "reason", and "optional expiry/revalidation note." Variants B and C specify a YAML whitelist format with `symbol` (dotted path) and `reason` (non-empty string) as required fields. A's format is less specific but includes an expiry concept absent from B and C.

### C-018: Resume Behavior Documentation

**Severity: Low**

Variant A (Section 9.3) explicitly addresses resume behavior: "roadmap already resumes by gate-passing existing artifacts" and notes that `_get_all_step_ids()` must be updated. Variant B (Section 5.6, Step 5) mentions updating `_get_all_step_ids()` but does not discuss resume semantics. Variant C does not mention resume behavior at all.

### C-019: Configuration Approach

**Severity: Medium**

Variant A (Section 9.2) specifies 5 config parameters: source subtree, rollout mode, thresholds, suppression path, cleanup-audit directory. It explicitly states "Keep config minimal. Do not introduce a new framework-level config subsystem."

Variant B (Section 5.4) mentions `WiringConfig` passed to `run_wiring_analysis()` and separately stores `wiring_rollout_mode` on roadmap config.

Variant C (Section 6) defines a full `WiringConfig` dataclass with `registry_patterns`, `provider_dir_names`, `whitelist_path`, and `exclude_patterns`.

C is most concrete; A is most explicit about constraint ("no new config subsystem"); B distributes config across modules.

### C-020: Rollout Phase Transition Criteria

**Severity: Medium**

| Metric | Variant A | Variant B | Variant C |
|--------|-----------|-----------|-----------|
| FPR for shadow->soft | Not specified | < 15% | < 15% |
| TPR for shadow->soft | Not specified | > 50% | > 50% |
| p95 latency | Not specified | < 5s | < 5s |
| Whitelist stability for shadow->soft | Not specified | 2+ releases | 2+ sprints |
| FPR for soft->full | Not specified | < 5% | < 5% |
| TPR for soft->full | Not specified | > 80% | > 80% |
| p95 latency for soft->full | Not specified | < 3s | Not specified |
| Whitelist stability for soft->full | Not specified | 5+ sprints | 5+ sprints |

Variant A provides no quantitative transition criteria. B and C largely agree. B specifies a tighter p95 latency target for soft->full (< 3s vs unspecified in C). C uses "sprints" as stability unit for both transitions; B uses "releases" for the first and "sprints" for the second.

### C-021: Dual-Mode vs Single-Mode Operation

**Severity: High**

Variant B (Section 4.3) explicitly defines three operation modes: Mode A (Roadmap Pipeline Gate), Mode B (Sprint Post-Task Check), Mode C (Cleanup-Audit Pass Extension). Each mode has a named subsection with specific integration points.

Variant C defines similar scope but without the named mode taxonomy. Sprint and roadmap integrations appear in Section 4.4.1 and 4.4.2.

Variant A defines only roadmap pipeline integration. There is no sprint mode and no cleanup-audit pass extension mode.

### C-022: Soft Mode Enforcement Tier

**Severity: Medium**

Variant C (Section 9, Phase 2) specifies that soft mode uses `GateMode.BLOCKING` with `enforcement_tier="STANDARD"`. Full mode uses `enforcement_tier="STRICT"`. Variants A and B define `WIRING_GATE` with `enforcement_tier="STRICT"` always and use mode-aware semantic checks to control blocking behavior. C uses the enforcement tier system for rollout graduation; A and B use frontmatter-encoded policy.

---

## Contradictions (X-NNN)

### X-001: Gate Constant Location

**Severity: High**

Variant A (Section 5.2) places `WIRING_VERIFICATION_GATE` in `roadmap/gates.py`. Variant B (Section 5.5, Module Map 4.2) places `WIRING_GATE` in `audit/wiring_gate.py`. Variant C (Section 4.2, 8) places `WIRING_GATE` in `audit/wiring_gate.py` (per module architecture diagram showing `WIRING_GATE GateCriteria constant` under `audit/wiring_gate.py`).

This is an architectural disagreement. A's placement in `roadmap/gates.py` follows the existing pattern where all roadmap gate constants live together. B and C's placement in `audit/wiring_gate.py` co-locates the gate with its analysis engine. B and C's approach arguably violates the existing convention but improves cohesion.

### X-002: Semantic Check Set — Mutually Exclusive Approaches

**Severity: High**

Variant A and B use 5 semantic checks: `analysis_complete_true`, `recognized_rollout_mode`, `finding_counts_consistent`, `severity_summary_consistent`, `zero_blocking_findings_for_mode`. The key check is `zero_blocking_findings_for_mode` which is mode-aware.

Variant C uses 5 semantic checks: `analysis_complete_true`, `zero_unwired_callables`, `zero_orphan_modules`, `zero_unwired_registries`, `total_findings_consistent`. These are per-category zero checks with no mode awareness.

These two approaches are incompatible. Under C's design, shadow mode cannot work through semantic checks alone (the checks always require zero findings). Under A/B's design, category-level zero checks are absent and replaced by a single mode-aware aggregate check. Implementing both simultaneously would create conflicting pass/fail semantics.

### X-003: `audit_artifacts_used` Type

**Severity: Low**

Variant A: `audit_artifacts_used: <int>` (integer count). Variant B: `audit_artifacts_used: <int>` (integer count, value 0 in example). Variant C: `audit_artifacts_used: bool` (boolean). Int-vs-bool for the same field would cause frontmatter validation failures if one variant's gate definition is applied to another's report output.

### X-004: Output File Name

**Severity: Low**

Variant A (Section 7.1): `wiring-verification.md`. Variant B (Section 5.6): `wiring-verification.md`. Variant C (Section 4.4.1): `wiring-report.md`. Different output filenames affect resume detection, `_get_all_step_ids()` wiring, and any downstream consumers that reference the artifact by name.

### X-005: Step Retry Policy

**Severity: Low**

Variants A and B: `retry_limit=0` with explicit rationale "Deterministic; retry won't help." Variant C: `retry_limit=1` with no rationale. For a truly deterministic step, retries produce identical results, making C's retry a no-op that wastes time.

### X-006: `WiringReport.passed` Semantics

**Severity: Medium**

Variant B (Section 5.1): `passed` property returns `True` when `total_findings == 0`. Variant C (Section 6): identical definition. However, B's mode-aware gate design means `passed` on the report object is not the same as "gate passes" (shadow mode always passes the gate even with findings). C's gate definition requires zero findings to pass, making `WiringReport.passed` and gate pass equivalent. This creates a semantic mismatch in B where the report says "not passed" but the gate says "passed" in shadow mode.

### X-007: Modification of `roadmap/gates.py`

**Severity: Medium**

Variant A (Section 5.2): Creates new `WIRING_VERIFICATION_GATE` constant in `roadmap/gates.py`. Variant B (Section 4.2): Modifies `roadmap/gates.py` only to "Import WIRING_GATE, add to ALL_GATES" (gate defined elsewhere). Variant C (Section 12): Modifies `roadmap/gates.py` to add "+40 LOC" for "Deviation count reconciliation check" but does not define the wiring gate there.

Only Variant C includes a deviation count reconciliation check in `roadmap/gates.py`. Variant A puts the wiring gate definition there. Variant B only adds an import.

### X-008: Agent Extension Specificity — audit-analyzer Fields

**Severity: Medium**

Variant A (Section 5.4) recommends adding 5 fields to audit-analyzer Pass 2 output: `wiring_surfaces`, `registry_symbols`, `effective_references`, `dynamic_loading_notes`, `wiring_assessment`.

Variant B (Section 6.3) adds 1 new mandatory field: "Wiring path" (Declaration -> Registration -> Invocation chain), plus 2 new finding types.

Variant C (Section 4.4.3) adds 4 fields matching A's set: `wiring_surfaces`, `registry_symbols`, `effective_references`, `wiring_notes`.

A and C agree on field names (with minor variation: `dynamic_loading_notes`/`wiring_assessment` vs `wiring_notes`). B takes a fundamentally different approach with a single chain-oriented "Wiring path" field instead of multiple structured fields. These produce incompatible audit-analyzer output schemas.

### X-009: Sprint Output Path

**Severity: Low**

Variant B (Section 5.7): Sprint wiring reports go to `work_dir / f"{task_id}-wiring-report.md"`. Variant C (Section 9, Phase 1): Sprint results logged to `.sprint-state/wiring/`. Different output paths with no reconciliation. Variant A does not specify sprint output.

### X-010: Minimum Unit Test Count

**Severity: Low**

Variant B (Section 10.1): "minimum 20" unit tests. Variant C (Section 15): "minimum 14" unit tests. A 43% difference in minimum test coverage expectations.

### X-011: Deviation Count Reconciliation Inclusion

**Severity: Medium**

Variant C (Section 10) includes a "Companion: Deviation Count Reconciliation" feature adding a `_deviation_counts_reconciled` check to `SPEC_FIDELITY_GATE`. Estimated 35-50 LOC, with its own task (T08) and test file. Variants A and B do not include this feature. C's file manifest shows +40 LOC to `roadmap/gates.py` for this, which conflicts with B's +5 LOC delta for the same file (import only). This companion feature is bundled into C's release scope but out of scope for A and B.

---

## Unique Contributions (U-NNN)

### U-001: Variant A — Explicit "Why `_build_steps()` Is the Correct Insertion Point" Rationale

**Value: Medium**

Variant A (Section 5.3) includes a dedicated subsection explaining why `_build_steps()` is the correct integration point: "The codebase has no dynamic gate registry for roadmap execution. Gates are wired statically at `Step` construction time." This architectural rationale is absent from B and C, which simply state the insertion point without justifying why alternatives were rejected.

### U-002: Variant A — Report Body Section Requirements

**Value: Medium**

Only Variant A (Section 7.3) specifies 7 required body sections for the `wiring-verification.md` report: Summary, Unwired Optional Callable Injections, Orphan Modules/Symbols, Unregistered Dispatch Entries, Suppressions and Dynamic Retention, Recommended Remediation, Evidence and Limitations. This prescribes the human-readable report structure.

### U-003: Variant A — Explicit "Rejected Option" Documentation

**Value: Low**

Variant A (Section 9.1) documents "LLM-only report generation" as a rejected option with the reason: "too weak for wiring assurance and too dependent on narrative interpretation." B and C state the chosen approach but do not document what was rejected.

### U-004: Variant A — Suppression Expiry Concept

**Value: Low**

Variant A (Section 10.2) includes "optional expiry / revalidation note" in suppression entries. B and C require only `symbol` and `reason`. The expiry concept supports suppression hygiene over time.

### U-005: Variant A — Follow-on Tasklist as Named Tracks

**Value: Low**

Variant A (Section 15) organizes implementation into 4 named tracks: Analyzer, Roadmap integration, Audit reuse, Rollout. This provides a higher-level planning view than B and C's task-level decomposition.

### U-006: Variant B — "What Changed from v1.0" Section

**Value: High**

Variant B (Section 1) includes a "What changed from v1.0" subsection enumerating 6 specific improvements over the prior spec version. This provides traceability and justification for why this variant exists. Neither A nor C document their relationship to prior versions in this way.

### U-007: Variant B — ToolOrchestrator AST Analyzer Implementation

**Value: High**

Variant B (Section 5.3) provides a complete `ast_analyze_file()` implementation with code, describing how it populates `FileAnalysis.references` and `metadata` fields. This is the only variant that provides implementation-level code for the ToolOrchestrator integration, including the downstream improvements to `dependency_graph.py`, `dead_code.py`, and `profile_generator.py`.

### U-008: Variant B — YAML Injection Prevention

**Value: Medium**

Variant B (Section 5.4) specifies: "All string-valued frontmatter fields MUST use `yaml.safe_dump()` to prevent YAML injection. Integer/boolean gate-evaluated fields are exempt." This security consideration is mentioned in C ("yaml.safe_dump for string fields" in data flow diagram) but not elevated to a MUST-level requirement. A does not mention it.

### U-009: Variant B — Pre-Activation Checklist

**Value: Medium**

Variant B (Section 7, Phase 1) defines a "Pre-activation checklist (blocking)" with 2 items: provider directory validation and zero-findings sanity check. Variant C (Section 9, Phase 1) has the same checklist. Variant A does not include a pre-activation checklist.

### U-010: Variant B — `blocking_findings` Computation Logic

**Value: High**

Variant B (Section 5.5) explicitly defines how `blocking_findings` is computed per rollout mode: shadow=0 always, soft=critical_count, full=critical_count+major_count. This is the crucial mapping between rollout policy and gate enforcement. A describes the concept abstractly but does not specify the computation. C does not use `blocking_findings` at all.

### U-011: Variant B — Forensic Cross-Reference Appendix

**Value: Medium**

Variant B (Appendix B) maps each known finding from the forensic analysis to its spec section and implementation task. This creates a traceability matrix from problem evidence to solution design.

### U-012: Variant C — Deviation Count Reconciliation Companion Feature

**Value: Medium**

Only Variant C (Section 10) includes the `_deviation_counts_reconciled` function as a companion feature for `SPEC_FIDELITY_GATE`. This addresses a related but distinct gap in spec-fidelity validation. Estimated at 35-50 LOC with its own test suite.

### U-013: Variant C — Coordination Notes Section

**Value: Medium**

Only Variant C (Section 18) includes explicit merge-conflict risk identification and coordination guidance: "coordinate with Anti-Instincts (`ANTI_INSTINCT_GATE` in v3.05) and Unified Audit Gating." This operational awareness is absent from A and B.

### U-014: Variant C — FPR Calibration Formula

**Value: Medium**

Variant C (Section 9, Phase 2) specifies: "Set thresholds at `measured_FPR + 2 sigma` above re-export noise floor. Phase 2 MUST NOT activate if unwired-callable FPR cannot be separated from noise." This statistical criterion for phase transition is unique and more rigorous than B's simple percentage thresholds.

---

## Shared Assumptions (A-NNN)

### A-001: STATED — SemanticCheck Interface Is Immutable

**Classification: STATED**

All three variants explicitly state that `SemanticCheck.check_fn: Callable[[str], bool]` must not be modified. Evidence: A Section 3.1 ("No signature changes to `SemanticCheck` are allowed"), B Section 3.1 (table: "No signature changes to any of these"), C Section 3.1 ("Zero changes to... `SemanticCheck`").

### A-002: STATED — Pipeline Module Must Not Import Domain Modules

**Classification: STATED**

All three variants state that `pipeline/*` must not import `roadmap/*`, `audit/*`, or `sprint/*`. Evidence: A Section 3.2, B Section 3.2, C Section 3.2.

### A-003: STATED — Deterministic Python Over LLM Synthesis

**Classification: STATED**

All three variants specify that wiring analysis must be deterministic Python (AST-based), not LLM-generated. Evidence: A Section 9.1, B Section 3.3, C Section 4.4.1.

### A-004: UNSTATED — AST Parsing Is Sufficient for Wiring Detection

**Classification: UNSTATED [SHARED-ASSUMPTION]**

All three variants assume that Python's `ast` module provides sufficient capability to detect all three wiring failure classes. None discuss limitations of AST-only analysis for patterns such as: dynamic attribute access (`setattr`/`getattr`), metaclass-generated methods, decorator-transformed signatures, or conditional imports behind `TYPE_CHECKING` guards. The assumption is that static AST parsing covers the target patterns, but the coverage boundary is never explicitly defined.

### A-005: UNSTATED — Single-Repository Scope

**Classification: UNSTATED [SHARED-ASSUMPTION]**

All three variants assume wiring analysis operates within a single repository (`src/superclaude/cli/`). None discuss cross-repository wiring (e.g., plugin packages that might provide callable implementations). This assumption is reasonable for v1 but constrains future extensibility.

### A-006: UNSTATED — `_build_steps()` Will Not Be Refactored Before This Release

**Classification: UNSTATED [SHARED-ASSUMPTION]**

All three variants depend on inserting a new `Step` at a specific position in `_build_steps()` (after `spec-fidelity`, around line 473). None consider the possibility that concurrent work might restructure `_build_steps()` or change the post-merge step ordering. The assumption that this insertion point is stable is critical to all three designs but never stated as a precondition.

### A-007: UNSTATED — Cleanup-Audit May Not Have Run

**Classification: UNSTATED [SHARED-ASSUMPTION]**

All three variants design for hybrid mode where cleanup-audit evidence is optional/advisory. However, none explicitly state what happens to detection accuracy when audit evidence is absent. The implicit assumption is that deterministic AST analysis alone produces acceptable results. This is reasonable but the accuracy delta between "with audit evidence" and "without" is never quantified.

### A-008: UNSTATED — Python Files Are Syntactically Valid

**Classification: UNSTATED [SHARED-ASSUMPTION]**

All three variants mention graceful degradation on `SyntaxError` (skip the file). However, none discuss the impact of widespread syntax errors (e.g., during a partially-complete merge) on analysis completeness. The assumption is that the vast majority of files in the analysis scope are parseable Python, which may not hold during certain pipeline states.

---

## Summary

### Counts Per Category

| Category | Count |
|----------|-------|
| Structural Differences (S-NNN) | 12 |
| Content Differences (C-NNN) | 22 |
| Contradictions (X-NNN) | 11 |
| Unique Contributions (U-NNN) | 14 |
| Shared Assumptions (A-NNN) | 8 (3 STATED, 5 UNSTATED) |
| **Total** | **67** |

### Highest-Severity Items

| ID | Category | Severity | Summary |
|----|----------|----------|---------|
| **X-001** | Contradiction | High | Gate constant location: `roadmap/gates.py` (A) vs `audit/wiring_gate.py` (B, C) |
| **X-002** | Contradiction | High | Mutually exclusive semantic check designs: mode-aware aggregate (A, B) vs per-category zero (C) |
| **C-002** | Content | High | Scope disagreement: roadmap-only (A) vs roadmap+sprint+audit (B, C) |
| **C-004** | Content | High | ToolOrchestrator AST plugin: absent (A), full implementation (B), design-level (C) |
| **C-006** | Content | High | Mode-aware enforcement (A, B) vs always-zero checks (C) -- fundamentally different rollout mechanism |
| **C-021** | Content | High | Triple-mode named taxonomy (B) vs unnamed dual-scope (C) vs single-scope (A) |
| **U-006** | Unique | High | B's "What changed from v1.0" provides lineage traceability |
| **U-007** | Unique | High | B's ToolOrchestrator implementation is the only code-level AST plugin design |
| **U-010** | Unique | High | B's `blocking_findings` computation is the crucial rollout-to-enforcement mapping |

### Key Architectural Decision Points Requiring Resolution

1. **Gate constant location** (X-001): Cohesion (audit/) vs convention (roadmap/gates.py)
2. **Semantic check philosophy** (X-002, C-006): Mode-aware aggregate check vs per-category zero checks. This is the single most impactful design divergence.
3. **Release scope** (C-002): Roadmap-only vs roadmap+sprint. Determines file manifest and LOC.
4. **ToolOrchestrator integration** (C-004): Include in v1 scope or defer?
5. **Deviation count reconciliation** (X-011): Bundle with wiring gate release or separate?
6. **`blocking_findings` computation model** (U-010): Explicit per-mode computation vs external gate mode control
