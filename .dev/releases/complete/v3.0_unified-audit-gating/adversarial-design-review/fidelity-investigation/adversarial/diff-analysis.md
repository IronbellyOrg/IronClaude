# Diff Analysis: Fidelity Gate Convergence Investigation

## Metadata
- Generated: 2026-03-19
- Variants compared: 3
- Focus: fidelity-gate-effectiveness, severity-drift, attention-degradation, remediation-loops
- Variant A: Wiring Verification Gate v2.0 (merged-spec.md)
- Variant B: Anti-Instincts Gate (anti-instincts-gate-unified.md)
- Variant C: Wiring Verification Gate v1.0 (wiring-verification-gate-v1.0-release-spec.md)

---

## Catalog A: Gate Criteria, Pass/Fail Logic, and Severity Definitions

### Variant A (Wiring Gate v2.0)

| Section | Content | Relevance to Root Causes |
|---------|---------|-------------------------|
| §5.1 WiringFinding.severity | `Literal["critical", "major", "info"]` — 3-level severity with code-level definitions | **SEVERITY DRIFT**: Provides a fixed, code-enforced severity enum. LLM cannot reinterpret. |
| §5.1 WiringReport.blocking_for_mode() | Deterministic function: shadow→0, soft→critical_count, full→critical+major | **GOALPOST MOVEMENT**: Pass/fail logic is pure Python, not LLM prose. |
| §5.6 WIRING_GATE semantic checks | 5 checks, all pure functions over frontmatter strings | **SEVERITY DRIFT**: Checks are deterministic — `_finding_counts_consistent` and `_severity_summary_consistent` validate serialized form |
| §5.6 _zero_blocking_findings_for_mode | Reads rollout_mode from frontmatter, returns True/False deterministically | **GOALPOST MOVEMENT**: What constitutes "pass" is encoded in code, not prompt prose |
| §5.4 Report frontmatter | 16 required fields, all typed (int/string/bool) | **ATTENTION DEGRADATION**: Gate evaluates structured frontmatter, not free-text narrative |
| §3.3 Separate analysis from enforcement | "Deterministic wiring analysis — pure Python over source files (no LLM)" | **ALL ROOT CAUSES**: LLM is completely removed from the gate evaluation loop |

### Variant B (Anti-Instincts Gate)

| Section | Content | Relevance to Root Causes |
|---------|---------|-------------------------|
| §8 ANTI_INSTINCT_GATE | 3 semantic checks, all pure Python over frontmatter | **SEVERITY DRIFT**: Fixed criteria — `undischarged_obligations==0`, `uncovered_contracts==0`, `fingerprint_coverage>=0.7` |
| §8 _no_undischarged_obligations | `int(fm.get("undischarged_obligations", -1)) == 0` | **GOALPOST MOVEMENT**: Binary pass/fail, no severity grading to drift |
| §8 _fingerprint_coverage_check | `float(fm.get("fingerprint_coverage", 0.0)) >= 0.7` | **GOALPOST MOVEMENT**: Fixed numeric threshold, no LLM interpretation |
| §3 Architecture | "All four detection modules are pure Python with zero LLM calls" | **ALL ROOT CAUSES**: Deterministic floor, not bypassable by completion bias |
| §9 Executor Integration | Executor writes audit report with frontmatter, gate validates frontmatter | **DOCUMENT REGENERATION**: Gate validates a report artifact, not the roadmap itself |

### Variant C (Wiring Gate v1.0)

| Section | Content | Relevance to Root Causes |
|---------|---------|-------------------------|
| §4.1 WiringFinding.severity | `Literal["critical", "major"]` — only 2 levels | **SEVERITY DRIFT**: Fixed enum but less granular than v2.0 |
| §4.4 WIRING_GATE | 5 semantic checks: `analysis_complete_true`, `zero_unwired_*` (x3), `total_findings_consistent` | **GOALPOST MOVEMENT**: Hard zero-tolerance — all counts must be 0 for pass |
| §4.3 Report format | 10 required frontmatter fields (fewer than v2.0) | **ATTENTION DEGRADATION**: Simpler structure, less to evaluate |
| §4.5 Sprint integration | shadow/soft/full mode with `report.passed` boolean | **SEVERITY DRIFT**: `.passed` is a simple boolean (total_findings==0), no mode-aware blocking |

---

## Catalog B: Remediation Behavior and Retry/Loop Logic

### Variant A (Wiring Gate v2.0)

| Section | Content | Relevance to Root Causes |
|---------|---------|-------------------------|
| §5.7 retry_limit=0 | "Deterministic; retry won't help" — step executes exactly once | **REMEDIATION LOOPS**: Explicitly prevents retry loops for deterministic steps |
| §5.7 Step definition | `retry_limit=0` with documented semantics from `pipeline/executor.py:158` | **NO CONVERGENCE**: Eliminates convergence problem entirely — one execution, pass or fail |
| §5.7.1 Executor special-casing | `if step.id == "wiring-verification": run_wiring_analysis()` — bypasses LLM entirely | **DOCUMENT REGENERATION**: No LLM generates the report, so no regeneration possible |
| §5.7.2 Resume behavior | "deterministic (same inputs produce same output)" — resume skips if gate passes | **REMEDIATION LOOPS**: Resume is idempotent; re-evaluation produces identical results |
| §5.8 Sprint soft mode | `if not report.clean: tui.warn(...)` — no remediation triggered | **REMEDIATION LOOPS**: Soft mode warns but never triggers a fix loop |

### Variant B (Anti-Instincts Gate)

| Section | Content | Relevance to Root Causes |
|---------|---------|-------------------------|
| §9 Step definition | `retry_limit=0` — "Deterministic; retry would produce same result" | **REMEDIATION LOOPS**: Same pattern as Variant A — no retry |
| §9 _run_anti_instinct_audit | Runs 3 deterministic checks, writes report, returns | **DOCUMENT REGENERATION**: Report is emitted by code, not LLM |
| §7 Structural audit | Phase 1: "warning-only...does not block the pipeline" | **REMEDIATION LOOPS**: Warning doesn't trigger remediation |
| No remediation section | Spec has no remediation/retry logic at all | **NO CONVERGENCE**: N/A — gate either passes or fails with no retry mechanism |

### Variant C (Wiring Gate v1.0)

| Section | Content | Relevance to Root Causes |
|---------|---------|-------------------------|
| §4.5 Sprint full mode | "Trigger remediation via SprintGatePolicy.build_remediation_step()" | **REMEDIATION LOOPS**: References remediation but does not define convergence criteria |
| No retry_limit field | Step definition not included in spec (sprint-only focus) | **NO CONVERGENCE**: No roadmap pipeline integration means no retry semantics defined |
| §4.5 Shadow mode | "Log result but do not affect task status" | **REMEDIATION LOOPS**: Shadow mode is observation-only |

---

## Catalog C: Attention, Systematic Coverage, and Drift Mitigation

### Variant A (Wiring Gate v2.0)

| Section | Content | Relevance to Root Causes |
|---------|---------|-------------------------|
| §3.3 Deterministic analysis | "pure Python over source files (no LLM)" | **ATTENTION DEGRADATION**: Eliminates LLM attention entirely — uses AST parsing |
| §5.2.1-5.2.3 Algorithm specs | Precise AST-based algorithms with explicit search patterns | **ATTENTION DEGRADATION**: Algorithms are deterministic — same files produce same findings every run |
| §5.5 _extract_frontmatter_values | Helper for all semantic checks to parse frontmatter consistently | **ATTENTION DEGRADATION**: Single parsing path for all checks — no per-check variation |
| §5.4 Report body sections | "7 sections in order" — structural contract for report body | **ATTENTION DEGRADATION**: Fixed structure means reviewers and gates always know where to look |
| §5.1 WiringReport.total_findings | Single-source computation from list lengths | **SEVERITY DRIFT**: Cannot drift because it's computed, not judged |

### Variant B (Anti-Instincts Gate)

| Section | Content | Relevance to Root Causes |
|---------|---------|-------------------------|
| §4 Obligation Scanner | Regex-based scanning with fixed vocabulary lists | **ATTENTION DEGRADATION**: Pattern matching is exhaustive within vocabulary — no attention dropout |
| §5 Contract Extractor | 7-category taxonomy with fixed regex patterns | **ATTENTION DEGRADATION**: Fixed pattern set means same spec always produces same contracts |
| §6 Fingerprint Extraction | Backtick + code block + ALL_CAPS extraction | **ATTENTION DEGRADATION**: Deterministic extraction — no LLM judgment |
| §7 Structural Audit | Counting structural indicators (code blocks, MUST/SHALL, signatures) | **ATTENTION DEGRADATION**: Pure counting — immune to attention effects |

### Variant C (Wiring Gate v1.0)

| Section | Content | Relevance to Root Causes |
|---------|---------|-------------------------|
| §4.2.1-4.2.3 Algorithms | AST-based algorithms (same as v2.0 core) | **ATTENTION DEGRADATION**: Deterministic by design |
| No explicit coverage mechanism | Spec doesn't discuss systematic coverage or drift | **ATTENTION DEGRADATION**: Not explicitly addressed, but inherently solved by deterministic approach |

---

## Catalog D: Architectural Decisions Affecting Root Causes

### Variant A (Wiring Gate v2.0)

| Decision | Effect on Root Causes |
|----------|----------------------|
| D2: Deterministic Python, not LLM | **MITIGATES ALL 5**: Removes LLM from the gate evaluation loop entirely |
| D1: Artifact-based enforcement | **MITIGATES #2, #3**: Report is a stable artifact; gate evaluates content, not live state |
| D5: Rollout mode in frontmatter | **MITIGATES #4**: Policy is data, not code-path branching that could be reinterpreted |
| D6: GateMode.TRAILING for shadow | **MITIGATES #5**: No convergence needed — shadow mode always passes |
| retry_limit=0 for deterministic steps | **MITIGATES #1, #5**: No re-evaluation means no drift and no convergence problem |
| Mode-aware blocking_findings | **MITIGATES #4**: What blocks is encoded in the emitter, not judged per-run |
| WiringReport.clean vs blocking_for_mode() | **MITIGATES #4**: Separates analysis truth from enforcement policy |

### Variant B (Anti-Instincts Gate)

| Decision | Effect on Root Causes |
|----------|----------------------|
| All checks pure Python | **MITIGATES ALL 5**: Same deterministic advantage as Variant A |
| Separate gate (not extending SPEC_FIDELITY_GATE) | **MITIGATES #3, #4**: Isolated concern — doesn't bloat the spec-fidelity prompt |
| Executor writes report, gate validates | **MITIGATES #2**: No LLM regenerates the document |
| Binary pass/fail (0 undischarged, 0 uncovered) | **MITIGATES #1, #4**: No severity grading to drift; no threshold interpretation |
| Upstream guard (spec_structural_audit) | **PARTIALLY MITIGATES #3**: Catches extraction-stage attention loss, but is itself a ratio check |

### Variant C (Wiring Gate v1.0)

| Decision | Effect on Root Causes |
|----------|----------------------|
| AST-based analysis | **MITIGATES #1, #3**: Deterministic — no LLM judgment to drift |
| Zero-tolerance semantic checks | **MITIGATES #4**: All counts must be 0 — no threshold interpretation |
| No roadmap pipeline integration | **NEUTRAL**: Doesn't address roadmap fidelity loop (sprint-only focus) |
| `.passed` as simple boolean | **MITIGATES #4**: But loses mode-aware nuance of v2.0 |
| Deviation count reconciliation companion | **DIRECTLY ADDRESSES SPEC-FIDELITY**: Validates frontmatter counts match body counts |

---

## Shared Assumptions

| A-NNN | Assumption | Classification | Impact |
|-------|------------|---------------|--------|
| A-001 | The spec-fidelity gate's infinite loop is caused by LLM involvement in evaluation, not by the gate infrastructure itself | UNSTATED | If the gate infrastructure (not LLM) is buggy, none of these specs help |
| A-002 | Deterministic Python checks are sufficient replacements for LLM-based fidelity assessment | UNSTATED | Deterministic checks can only catch structural/mechanical issues, not semantic fidelity |
| A-003 | The existing `SemanticCheck` interface (`check_fn(content: str) -> bool`) is adequate for all needed checks | STATED | All three specs explicitly design around this constraint |
| A-004 | The spec-fidelity gate's remediation loop is the only convergence problem in the pipeline | UNSTATED | Other gates (MERGE_GATE, TEST_STRATEGY_GATE) may have similar issues |
| A-005 | None of these specs modify the existing SPEC_FIDELITY_GATE or its remediation behavior | STATED | They add new gates but don't fix the existing fidelity gate's convergence problem |

---

## Critical Observation

**None of the three specs directly address the spec-fidelity gate's infinite remediation loop.** All three specs introduce NEW gates (WIRING_GATE, ANTI_INSTINCT_GATE) that are deliberately deterministic. They avoid the convergence problem by design — but they do not fix the existing spec-fidelity gate that is stuck in the loop.

The existing SPEC_FIDELITY_GATE uses LLM-generated severity assessments, which is where root causes #1 (severity drift), #3 (attention degradation), and #4 (goalpost movement) manifest. Only Variant C's companion feature (deviation count reconciliation) directly touches the spec-fidelity gate, and even that only validates frontmatter/body consistency — it doesn't address severity drift.
