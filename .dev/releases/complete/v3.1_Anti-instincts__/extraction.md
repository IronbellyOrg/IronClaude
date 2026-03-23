Now I have the complete spec. Let me produce the extraction document.

---
spec_source: anti-instincts-gate-unified.md
generated: "2026-03-20T00:00:00Z"
generator: claude-opus-4-6-requirements-extractor
functional_requirements: 28
nonfunctional_requirements: 10
total_requirements: 38
complexity_score: 0.72
complexity_class: HIGH
domains_detected: [backend, pipeline, testing, quality-assurance, sprint-infrastructure]
risks_identified: 12
dependencies_identified: 9
success_criteria_count: 8
extraction_mode: standard
---

## Functional Requirements

The spec does not use formal FR-NNN identifiers. Requirements are extracted by module/section and assigned FR-NNN IDs as fallback.

### Module 1: Obligation Scanner (V2-A)

**FR-001** — Implement `obligation_scanner.py` (~200 LOC) as a pure-Python, regex-based scanner that detects scaffolding terms in roadmap content and verifies each has a corresponding discharge task in a later phase.
- FR-001a — Scan for 11 scaffold term patterns: mock/mocked, stub/stubbed/stubs, skeleton, placeholder, scaffold/scaffolding/scaffolded, temporary, hardcoded, hardwired, no-op/noop, dummy, fake.
- FR-001b — Scan for 9 discharge term patterns: replace, wire up/in/into, integrate/integrating/integrated, connect, swap out/in, remove mock/stub/placeholder/scaffold, implement real, fill in, complete skeleton/scaffold.
- FR-001c — Parse content into phase-delimited sections by H2/H3 headings containing Phase/Step/Stage/Milestone patterns. Fallback to treating entire document as one section.
- FR-001d — For each scaffold term found, search all subsequent sections for a discharge term referencing the same component (component-context matching).
- FR-001e — Extract component context using a 60-char window around scaffold terms, preferring backtick-delimited terms, then capitalized multi-word terms, then full line context.
- FR-001f — Return `ObligationReport` dataclass with total_obligations, discharged, undischarged counts and full obligation list.

**FR-002** — Implement `# obligation-exempt` comment mechanism for legitimate scaffolding (e.g., test doubles) that should not trigger gate failure.

**FR-003** — Scaffold terms inside code blocks (backtick-fenced) MUST be flagged at MEDIUM severity rather than failing the gate. Separate `medium_severity_obligations` frontmatter field.

### Module 2: Integration Contract Extractor (V5-1)

**FR-004** — Implement `integration_contracts.py` (~250 LOC) that extracts integration contracts from spec text and verifies each has an explicit wiring task in the roadmap.
- FR-004a — Detect 7 categories of integration mechanisms via `DISPATCH_PATTERNS`: dict dispatch tables, plugin registries, callback/constructor injection, type-annotated dispatch (Dict[str, Callable]), strategy pattern, middleware chain, event binding, DI container.
- FR-004b — For each detected contract, extract surrounding context (3 lines before/after), classify mechanism, assign sequential IC-NNN ID.
- FR-004c — Deduplicate contracts by evidence string.

**FR-005** — Implement `check_roadmap_coverage()` that verifies each integration contract has explicit wiring task coverage in roadmap.
- FR-005a — Check roadmap against `WIRING_TASK_PATTERNS` (4 pattern categories: creation/population, wiring into mechanisms, specific named mechanisms, strategy/middleware/event setup).
- FR-005b — Fallback: extract UPPER_SNAKE_CASE and PascalCase identifiers from contract evidence and check for their presence in roadmap.
- FR-005c — Return `IntegrationAuditResult` with contracts, coverage list, uncovered_count, total_count.

**FR-006** — Implement `_classify_mechanism()` to categorize matched text into one of 10 mechanism types: dispatch_table, registry, dependency_injection, explicit_wiring, routing, strategy_pattern, middleware_chain, event_binding, di_container, integration_point.

### Module 3: Fingerprint Extraction (V4-2)

**FR-007** — Implement `fingerprint.py` (~150 LOC) that extracts code-level identifiers from spec content and checks coverage ratio in roadmap.
- FR-007a — Extract backtick-delimited identifiers (minimum 4 chars, strip trailing parentheses).
- FR-007b — Extract function/class definitions from Python code blocks (`def`/`class` patterns).
- FR-007c — Extract ALL_CAPS constants (minimum 4 chars, `[A-Z][A-Z_]{3,}`), excluding common non-specific constants via `_EXCLUDED_CONSTANTS` frozenset (16 entries: TRUE, FALSE, NONE, TODO, NOTE, WARNING, HIGH, MEDIUM, LOW, YAML, JSON, STRICT, STANDARD, EXEMPT, LIGHT, PASS, FAIL, INFO, DEBUG, ERROR, CRITICAL).
- FR-007d — Deduplicate fingerprints by text.

**FR-008** — Implement `check_fingerprint_coverage()` with configurable `min_coverage_ratio` (default 0.7). Return tuple of (passed, coverage_ratio, all_fingerprints, missing_fingerprints). Gate passes when coverage ratio >= threshold.

### Module 4: Spec Structural Audit (V1-C)

**FR-009** — Implement `spec_structural_audit.py` (~80 LOC) that counts structural requirement indicators in raw spec text.
- FR-009a — Count: code blocks, MUST/SHALL/REQUIRED clauses, function signatures in code blocks, class definitions in code blocks, test_* name patterns, UPPERCASE_DICT = { registry patterns, pseudocode blocks (containing if/elif/else/for/while).
- FR-009b — Return `SpecStructuralAudit` dataclass with all counts plus `total_structural_indicators` sum.

**FR-010** — Implement `check_extraction_adequacy()` comparing extraction's `total_requirements` against spec structural indicator count with configurable threshold (default 0.5).
- FR-010a — Phase 1: warning-only (log but do not block pipeline).
- FR-010b — Phase 2: STRICT enforcement (re-trigger extraction or halt).

### Gate Definition

**FR-011** — Define `ANTI_INSTINCT_GATE` as a `GateCriteria` instance with:
- FR-011a — Required frontmatter fields: `undischarged_obligations` (int), `uncovered_contracts` (int), `fingerprint_coverage` (float 0.0-1.0).
- FR-011b — `min_lines=10`, `enforcement_tier="STRICT"`, `gate_scope=GateScope.TASK`.
- FR-011c — Three semantic checks: `no_undischarged_obligations`, `integration_contracts_covered`, `fingerprint_coverage_sufficient`.

**FR-012** — Implement three gate check functions that validate anti-instinct audit report frontmatter:
- FR-012a — `_no_undischarged_obligations()`: passes when `undischarged_obligations == 0`.
- FR-012b — `_integration_contracts_covered()`: passes when `uncovered_contracts == 0`.
- FR-012c — `_fingerprint_coverage_check()`: passes when `fingerprint_coverage >= 0.7`.

**FR-013** — Insert `("anti-instinct", ANTI_INSTINCT_GATE)` into `ALL_GATES` list between `("merge", MERGE_GATE)` and `("test-strategy", TEST_STRATEGY_GATE)`.

### Executor Integration

**FR-014** — Add `_run_structural_audit()` executor hook that runs after `EXTRACT_GATE` passes, before `generate-*` steps. This is executor-level logic (not a pipeline Step), following existing `_inject_pipeline_diagnostics` pattern.
- FR-014a — Parse extraction frontmatter for `total_requirements` via YAML.
- FR-014b — Phase 1: log warning if ratio below 0.5; do not block.

**FR-015** — Add `anti-instinct` Step to `_build_steps()` between `merge` and `test-strategy`.
- FR-015a — Non-LLM step (empty prompt); executor handles directly when `step.id == "anti-instinct"`.
- FR-015b — `output_file=out / "anti-instinct-audit.md"`, `gate=ANTI_INSTINCT_GATE`, `timeout_seconds=30`, `retry_limit=0`.
- FR-015c — Inputs: `[config.spec_file, extraction, merge_file]`.

**FR-016** — Implement `_run_anti_instinct_audit()` that orchestrates all three checks and writes `anti-instinct-audit.md`.
- FR-016a — Run obligation scanner on roadmap content.
- FR-016b — Run integration contract extraction on spec + roadmap.
- FR-016c — Run fingerprint coverage on spec + roadmap.
- FR-016d — Write YAML frontmatter with 9 fields: undischarged_obligations, uncovered_contracts, fingerprint_coverage, total_obligations, discharged_obligations, total_contracts, covered_contracts, total_fingerprints, matched_fingerprints, structural_audit_passed.
- FR-016e — Write markdown body with three sections: Obligation Scanner (V2-A) table, Integration Contracts (V5-1) table, Fingerprint Coverage (V4-2) with missing list.

**FR-017** — Add `"anti-instinct"` to `_get_all_step_ids()` between `"merge"` and `"test-strategy"`.

**FR-018** — Add imports: `from .gates import ANTI_INSTINCT_GATE` and `from ..sprint.models import TrailingGateResult, DeferredRemediationLog`.

### Prompt Modifications

**FR-019** — Add `INTEGRATION_ENUMERATION_BLOCK` constant to `prompts.py` and append it to `build_generate_prompt()` return value before `_OUTPUT_FORMAT_BLOCK`.
- FR-019a — Block MUST instruct LLM to enumerate all integration points before generating phases.
- FR-019b — Block MUST warn that implementing components does not automatically wire them.
- FR-019c — Block MUST require `## Integration Wiring Tasks` section in roadmap output.
- FR-019d — Block MUST list 4 integration point types: data structure mapping, constructor/factory injection, explicit wiring/binding, lookup/dispatch mechanisms.
- FR-019e — Block MUST list 4 common integration patterns requiring explicit tasks: dispatch tables, constructor injection, import chains, registration.

**FR-020** — Add `INTEGRATION_WIRING_DIMENSION` as 6th comparison dimension in `build_spec_fidelity_prompt()`, after dimension 5 ("NFRs").

### Sprint Executor Integration

**FR-021** — Implement sprint-level gate result propagation for anti-instinct gate:
- FR-021a — Wrap gate result in `TrailingGateResult(passed, evaluation_ms, gate_name)`.
- FR-021b — Submit to sprint-level `_all_gate_results` accumulator.
- FR-021c — On PASS in soft/full mode: `ledger.credit(int(upstream_merge_turns * ledger.reimbursement_rate))`.
- FR-021d — On FAIL: append to `remediation_log`; remediation re-runs upstream merge step; exits with `BUDGET_EXHAUSTED` (retry_limit=0).
- FR-021e — `ShadowGateMetrics.record(passed, evaluation_ms)` in shadow/soft/full modes.

**FR-022** — Add `gate_rollout_mode: Literal["off", "shadow", "soft", "full"] = "off"` to `SprintConfig`.

**FR-023** — Implement rollout mode behavior matrix:
- FR-023a — `off`: gate fires, result ignored.
- FR-023b — `shadow`: gate fires, result logged to ShadowGateMetrics, no pipeline effect.
- FR-023c — `soft`: gate fires, warning logged, remediation attempted, no TaskResult mutation, reimbursement on pass.
- FR-023d — `full`: gate fires, error logged, remediation attempted, TaskResult set to FAIL on exhaustion, reimbursement on pass.

**FR-024** — Implement `run_post_task_gate_hook()` in sprint executor.

### KPI Report Integration

**FR-025** — Anti-instinct gate results contribute to `GateKPIReport` via `build_kpi_report()`:
- FR-025a — Contribute to `gate_pass_rate` / `gate_fail_rate`.
- FR-025b — Contribute to `gate_latency_p50` / `gate_latency_p95`.
- FR-025c — Contribute to `turns_reimbursed_total` (soft/full mode on pass only).

### Test Files

**FR-026** — Create 8 test files:
- FR-026a — `tests/roadmap/test_obligation_scanner.py` (~100 LOC): scaffold/discharge detection, phase splitting, component context.
- FR-026b — `tests/roadmap/test_integration_contracts.py` (~100 LOC): contract extraction, coverage checking, mechanism classification.
- FR-026c — `tests/roadmap/test_fingerprint.py` (~100 LOC): fingerprint extraction, coverage ratio, threshold behavior.
- FR-026d — `tests/roadmap/test_spec_structural_audit.py` (~60 LOC): structural indicator counting, ratio comparison.
- FR-026e — `tests/sprint/test_shadow_mode.py` (~50-70 LOC): shadow mode integration.
- FR-026f — `tests/pipeline/test_full_flow.py` (~50-70 LOC): full flow with reimbursement path.
- FR-026g — `tests/roadmap/test_anti_instinct_integration.py` (~80-100 LOC): gate+executor+prompts integration.
- FR-026h — `tests/sprint/test_anti_instinct_sprint.py` (~60-80 LOC): sprint rollout mode scenarios.

### Contradiction Resolutions

**FR-027** — Implement all 8 contradiction resolutions (X-001 through X-008) as specified in Section 11.

### Shadow Validation Graduation

**FR-028** — Shadow-mode graduation criteria: `ShadowGateMetrics.pass_rate >= 0.90` over 5+ sprints before advancing from shadow to soft mode.

---

## Non-Functional Requirements

Requirements use the spec's verbatim NFR identifiers.

**NFR-001** — All detection is deterministic Python with zero LLM calls. No LLM-on-LLM review.

**NFR-002** — Combined anti-instinct gate latency < 1s (all checks are pure Python).

**NFR-004** — All modules are pure functions: content in, result out, no I/O. (Note: NFR-003 is unassigned per spec.)

**NFR-005** — `ANTI_INSTINCT_GATE` enforcement tier is STRICT (all 3 semantic checks must pass).

**NFR-006** — Ship with `gate_rollout_mode=off` default; shadow validation required before enforcement.

**NFR-007** — All TurnLedger calls guarded by `if ledger is not None` (None-safe). Standalone roadmap mode has `ledger=None`.

**NFR-008** — Anti-instinct modules have zero dependency on TurnLedger wiring. Can be implemented independently.

**NFR-009** — `gate_passed()` function signature unchanged. Backward compatible.

**NFR-010** — Anti-instinct and wiring-integrity gates evaluate independently (no ordering constraint).

**NFR-011** — Thresholds (0.7 fingerprint, 0.5 structural) calibrated via shadow-mode data before enforcement.

---

## Complexity Assessment

**Score: 0.72 — HIGH**

**Rationale:**

| Factor | Weight | Score | Justification |
|---|---|---|---|
| Module count | 0.15 | 0.8 | 4 new source modules + 8 test files + 5 modified files |
| Cross-cutting integration | 0.20 | 0.9 | Dual execution context (roadmap standalone vs sprint-invoked), gate propagation to TurnLedger/TrailingGateRunner/KPI |
| Regex complexity | 0.10 | 0.6 | 11 scaffold + 9 discharge + 8 dispatch + 4 wiring patterns; non-trivial but well-specified |
| Architectural constraints | 0.15 | 0.7 | Must be pure Python, zero LLM calls, stateless pipeline, SemanticCheck single-file workaround |
| Sprint infrastructure coupling | 0.15 | 0.8 | 4-mode rollout behavior matrix, reimbursement, remediation, KPI aggregation |
| Implementation sequencing | 0.10 | 0.5 | Clear dependency graph, parallelizable branches |
| Testing scope | 0.10 | 0.7 | 8 test files across roadmap/sprint/pipeline, integration tests required |
| Coordination risk | 0.05 | 0.7 | Merge conflicts with Wiring Verification, Unified Audit Gating, TurnLedger |

**Weighted total: 0.72**

The spec is large (~1,700 lines, ~1,200 new LOC) but extremely well-specified with inline code, clear interfaces, and resolved contradictions. The primary complexity driver is the dual execution context and rollout mode state machine.

---

## Architectural Constraints

1. **Zero LLM calls** — All four detection modules must be pure Python with deterministic execution. LLM-on-LLM review is explicitly prohibited as it shares the same blindspots.
2. **Pure functions** — All modules must be `content in, result out` with no I/O operations. File reading/writing is the executor's responsibility.
3. **Stateless pipeline** — V4-5's stateful registry approach is rejected. All checks operate on artifact content, not shared mutable state.
4. **SemanticCheck single-file limitation** — Gate semantic checks receive only a single content string. Multi-file checks use executor-level workaround: write audit report, validate frontmatter.
5. **Pipeline position** — Anti-instinct step runs between `merge` and `test-strategy`. Structural audit runs between `extract` and `generate` as executor-level hook.
6. **Target module** — All new files in `src/superclaude/cli/roadmap/`. Sprint modifications in `src/superclaude/cli/sprint/`.
7. **Backward compatibility** — `gate_passed()` signature unchanged. `gate_rollout_mode` defaults to `"off"`. Existing tests unmodified.
8. **Python version** — `from __future__ import annotations` used; `str | None` union syntax in dataclasses.
9. **TurnLedger None-safety** — All economic paths guarded by `if ledger is not None`.
10. **No retry on deterministic failure** — `retry_limit=0` on anti-instinct step; retry produces identical results.
11. **Defense-in-depth with D-03/D-04** — If both Anti-Instincts and Unified Audit Gating ship, they coexist independently.

---

## Risk Inventory

| # | Risk | Severity | Mitigation |
|---|---|---|---|
| 1 | Scaffold vocabulary misses non-standard deferral language | Medium | Component context extraction + `# obligation-exempt` escape hatch; expand vocabulary based on shadow-mode false negatives |
| 2 | Fingerprint 0.7 threshold produces false positives on specs with many illustrative examples | Medium | Shadow-mode calibration (NFR-011); threshold is configurable parameter |
| 3 | Structural audit 0.5 threshold is arbitrary without empirical data | Medium | Phase 1 is warning-only; graduate to STRICT after shadow validation |
| 4 | SemanticCheck single-file workaround may become limiting | Low | Phase 2 deferred item: model extension for multi-file access |
| 5 | Merge conflicts with Wiring Verification / Unified Audit Gating in `gates.py` | Medium | Changes are additive-only; coordinate insertion order in `ALL_GATES` |
| 6 | TurnLedger not instantiated before anti-instinct gates fire (A-011) | Medium | None-safe guards; anti-instinct degrades gracefully |
| 7 | 60-char context window insufficient for diverse roadmap structures (OQ-002) | Low | Validate in shadow mode; adjust window size if needed |
| 8 | "Mentioned is not planned" (A-009) — fingerprint presence check conflates mention with planning | Medium | V5-1 contract extractor provides verb-anchored wiring check; combined checks reduce risk |
| 9 | Sprint infrastructure (TrailingGateRunner, DeferredRemediationLog) not yet available | Medium | Staged implementation: anti-instinct modules first, sprint wiring second; zero dependency between branches |
| 10 | False positives from anti-instinct gate block sprints before validation (A-012) | High | Phase 1 ships with `gate_rollout_mode=off`; no behavioral change until shadow validation passes |
| 11 | Contract-specific vs global pattern matching may produce false positives (OQ-009) | Low | Phase 1 ships global matching; contract-specific matching deferred to Phase 2 |
| 12 | `SprintGatePolicy` instantiation is a cross-cutting dependency (A-014) | Medium | design.md Section 6.3 specifies instantiation; not anti-instinct-specific |

---

## Dependency Inventory

| # | Dependency | Type | Required By |
|---|---|---|---|
| 1 | `src/superclaude/cli/roadmap/gates.py` (existing) | Internal — modify | FR-011, FR-012, FR-013 — `GateCriteria`, `SemanticCheck`, `GateScope`, `ALL_GATES`, `_parse_frontmatter` |
| 2 | `src/superclaude/cli/roadmap/executor.py` (existing) | Internal — modify | FR-014, FR-015, FR-016, FR-017, FR-018 — `_build_steps()`, `_get_all_step_ids()`, Step class |
| 3 | `src/superclaude/cli/roadmap/prompts.py` (existing) | Internal — modify | FR-019, FR-020 — `build_generate_prompt()`, `build_spec_fidelity_prompt()` |
| 4 | `src/superclaude/cli/sprint/models.py` (existing) | Internal — modify | FR-022 — `SprintConfig`, `TrailingGateResult`, `DeferredRemediationLog` |
| 5 | `src/superclaude/cli/sprint/executor.py` (existing) | Internal — modify | FR-021, FR-024 — sprint executor loop, `_all_gate_results` |
| 6 | `src/superclaude/cli/sprint/kpi.py` (existing) | Internal — read-only | FR-025 — `build_kpi_report()`, `GateKPIReport` |
| 7 | Python `re` module | Stdlib | All modules — regex-based pattern matching |
| 8 | Python `dataclasses` module | Stdlib | All modules — data structures |
| 9 | Python `yaml` (PyYAML) | Third-party | FR-014 — extraction frontmatter parsing |

---

## Success Criteria

| # | Criterion | Threshold | Measurement |
|---|---|---|---|
| 1 | Obligation scanner detects undischarged scaffolding in cli-portify regression case | 100% — "mocked steps" detected with no discharge | Run scanner on historical cli-portify roadmap output |
| 2 | Integration contract extractor identifies `PROGRAMMATIC_RUNNERS` dispatch pattern | 100% — at least 1 contract extracted from cli-portify spec | Run extractor on v2.24/v2.24.1/v2.25 specs |
| 3 | Fingerprint coverage detects omission of `_run_programmatic_step`, `PROGRAMMATIC_RUNNERS`, `test_programmatic_step_routing` | Coverage ratio < 0.7 on historical broken roadmap | Run fingerprint check on cli-portify spec+roadmap pair |
| 4 | All 4 source modules pass unit tests | 100% test pass rate | `uv run pytest tests/roadmap/test_obligation_scanner.py tests/roadmap/test_integration_contracts.py tests/roadmap/test_fingerprint.py tests/roadmap/test_spec_structural_audit.py` |
| 5 | Combined anti-instinct gate latency < 1s | < 1000ms | Time `_run_anti_instinct_audit()` on representative spec+roadmap |
| 6 | Zero LLM calls in anti-instinct pipeline step | 0 LLM invocations | Code review + integration test verification |
| 7 | Existing tests pass without modification | 0 regressions | `uv run pytest` full suite |
| 8 | Shadow-mode graduation: pass rate >= 0.90 over 5+ sprints | >= 90% pass rate | `ShadowGateMetrics.pass_rate` aggregation |

---

## Open Questions

The spec provides a canonical registry of open questions (Section 14.5). Extracted verbatim:

| ID | Question | Current Resolution | Section |
|---|---|---|---|
| OQ-001 | Fingerprint extensibility (category weights, custom exclusions) | Deferred to Phase 2 | 6 |
| OQ-002 | Is 60-char context window sufficient for diverse roadmaps? | Validate in shadow mode; adjust if needed | 4 |
| OQ-003 | `# obligation-exempt` comment syntax and scope | Per-line scope on the scaffold term's line | 4 |
| OQ-004 | Should code-block scaffold terms block at MEDIUM or STRICT? | Separate `medium_severity_obligations` frontmatter field, excluded from gate blocking | 4 |
| OQ-005 | D-03/D-04 coexistence policy | Defense-in-depth: both gates evaluate independently | 8 |
| OQ-006 | When does structural audit transition from warning to STRICT? | Manual configuration after shadow-mode metrics confirm threshold adequacy | 7 |
| OQ-007 | Are TurnLedger design.md sections finalized? | Verify during Phase 4; reconcile any gaps | 9.5, 16.5 |
| OQ-008 | Multi-component false negatives in context extraction | Assess in shadow mode; expand context extraction if needed | 4 |
| OQ-009 | Contract-specific vs global pattern matching | Phase 1 ships global; contract-specific matching deferred | 5 |
| OQ-010 | Should `## Integration Wiring Tasks` heading be validated? | Add heading presence check to merge gate or structural audit indicator | 10 |
| OQ-011 | `_EXCLUDED_CONSTANTS` alignment with 4-char regex minimum | Aligned: frozenset entries excluded from ALL_CAPS extraction | 6 |

**Additional implicit questions identified:**

| ID | Question | Source |
|---|---|---|
| OQ-012 | What is the behavior when `_split_into_phases()` finds headings that don't follow Phase/Step/Stage/Milestone pattern? (e.g., "## 2.3 Executor") — the regex requires these keywords | Section 4 code |
| OQ-013 | How does the `medium_severity_obligations` field (OQ-004 resolution) interact with the gate — is it informational-only or does it affect downstream processing? | Section 4 / FR-003 |
| OQ-014 | The `_EXCLUDED_CONSTANTS` frozenset lists 20 entries but the spec text says "16 entries" — which is authoritative? (Code shows: TRUE, FALSE, NONE, TODO, NOTE, WARNING, HIGH, MEDIUM, LOW, YAML, JSON, STRICT, STANDARD, EXEMPT, LIGHT, PASS, FAIL, INFO, DEBUG, ERROR, CRITICAL = 21) | Section 6 code vs narrative |
| OQ-015 | The structural audit `_run_structural_audit` in Section 9 uses `import yaml` inline — should this be a top-level import or is lazy import intentional? | Section 9 code |
