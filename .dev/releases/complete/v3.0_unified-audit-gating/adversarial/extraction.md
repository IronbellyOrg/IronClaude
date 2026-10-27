

---
spec_source: .dev/releases/current/v3.0_unified-audit-gating/adversarial/merged-spec.md
generated: "2026-03-18T00:00:00Z"
generator: requirements-extraction-agent-opus-4.6
functional_requirements: 42
nonfunctional_requirements: 18
total_requirements: 60
complexity_score: 0.82
complexity_class: HIGH
domains_detected: [backend, security, static-analysis, pipeline-infrastructure, agent-behavioral-specs, testing]
risks_identified: 8
dependencies_identified: 14
success_criteria_count: 14
extraction_mode: standard
---

## Functional Requirements

**FR-001**: Detect constructor parameters typed `Optional[Callable]` (or `Callable | None`) with default `None` that are never explicitly provided at any call site. (Section 5.2.1, G-001)

**FR-002**: AST-parse all Python files in target directory and extract injectable callable parameters from `__init__` methods. (Section 5.2.1)

**FR-003**: For each injectable callable, search all Python files for call sites constructing the class and check if any provides the parameter by keyword. Zero providers yields a `WiringFinding(unwired_callable)`. (Section 5.2.1)

**FR-004**: Support whitelist via `wiring_whitelist.yaml` with `symbol` and `reason` fields per entry. Malformed entries logged as WARNING in Phase 1, raise `WiringConfigError` in Phase 2+. (Section 5.2.1)

**FR-005**: Detect orphan modules — Python files in provider directories whose exported functions are never imported by any consumer. (Section 5.2.2, G-002)

**FR-006**: Identify provider directories by convention: names matching `config.provider_dir_names` or directories containing 3+ Python files with common function prefix. (Section 5.2.2)

**FR-007**: Exclude `__init__.py`, `conftest.py`, and `test_*.py` from orphan module analysis. (Section 5.2.2)

**FR-008**: Enforce dual evidence rule for orphan classification: symbol orphaned only if both direct analysis finds no import chain AND cleanup-audit evidence does not justify dynamic/deferred use. (Section 5.2.2)

**FR-009**: Detect unwired dispatch registry dictionaries whose values reference non-importable functions. (Section 5.2.3, G-003)

**FR-010**: Identify registries via module-level assignments where target name matches `DEFAULT_REGISTRY_PATTERNS` and value is a Dict literal. (Section 5.2.3)

**FR-011**: Classify registry findings into three types: entry unresolved (critical), registry unused (major), explicit None mapping (major). (Section 5.2.3)

**FR-012**: Emit structured YAML frontmatter + Markdown report conforming to `GateCriteria` validation with all 15 required frontmatter fields. (Section 5.4, G-004)

**FR-013**: Report body MUST contain 7 sections in order: Summary, Unwired Optional Callable Injections, Orphan Modules/Symbols, Unregistered Dispatch Entries, Suppressions and Dynamic Retention, Recommended Remediation, Evidence and Limitations. (Section 5.4.1)

**FR-014**: Implement `WiringFinding` dataclass with fields: `finding_type`, `file_path`, `symbol_name`, `line_number`, `detail`, `severity`. (Section 5.1)

**FR-015**: Implement `WiringReport` dataclass with `total_findings` property deriving counts from list lengths (single-source computation). (Section 5.1)

**FR-016**: Implement `WiringReport.blocking_for_mode()` returning 0 for shadow, critical-only count for soft, critical+major count for full. (Section 5.1)

**FR-017**: Implement `WiringConfig` dataclass with `registry_patterns`, `provider_dir_names`, `whitelist_path`, `exclude_patterns`. (Section 4.2.1)

**FR-018**: Define `WIRING_GATE` as a `GateCriteria` instance with 15 required frontmatter fields, `min_lines=10`, `enforcement_tier="STRICT"`, and 5 semantic checks. (Section 5.6)

**FR-019**: Implement semantic check `_analysis_complete_true`: verify `analysis_complete` frontmatter field is `true`. (Section 5.6)

**FR-020**: Implement semantic check `_recognized_rollout_mode`: verify `rollout_mode` is one of `shadow`, `soft`, or `full`. (Section 5.6)

**FR-021**: Implement semantic check `_finding_counts_consistent`: verify `total_findings == unwired_callable_count + orphan_module_count + unwired_registry_count`. (Section 5.6)

**FR-022**: Implement semantic check `_severity_summary_consistent`: verify `critical_count + major_count + info_count == total_findings`. (Section 5.6)

**FR-023**: Implement semantic check `_zero_blocking_findings_for_mode`: shadow always True, soft/full True only if `blocking_findings == 0`. (Section 5.6)

**FR-024**: Implement `_extract_frontmatter_values()` helper in `audit/wiring_gate.py` (not pipeline/), duplicating `_FRONTMATTER_RE` regex to preserve layering. (Section 5.5)

**FR-025**: Implement `emit_report()` that computes `blocking_findings` based on rollout mode: shadow=0, soft=critical_count, full=critical+major. (Section 5.6)

**FR-026**: All string-valued frontmatter fields MUST use `yaml.safe_dump()` to prevent YAML injection. (Section 5.4)

**FR-027**: `whitelist_entries_applied` field MUST always be present in report, zero if no whitelist configured. (Section 5.4)

**FR-028**: Deploy in shadow mode initially with `GateMode.TRAILING` for roadmap pipeline. (Section 5.7, G-005)

**FR-029**: Integrate wiring-verification as Step 9 in `_build_steps()` after `spec-fidelity`, with `retry_limit=0` and `gate_mode=GateMode.TRAILING`. (Section 5.7, G-006)

**FR-030**: Special-case `step.id == "wiring-verification"` in `roadmap_run_step()` to run deterministic analysis instead of LLM step. (Section 5.7.1)

**FR-031**: Update `_get_all_step_ids()` to include `"wiring-verification"` after `"spec-fidelity"` and before `"remediate"`. (Section 5.7)

**FR-032**: Update `ALL_GATES` in `roadmap/gates.py` to include `WIRING_GATE`. (Section 5.7)

**FR-033**: Add `build_wiring_verification_prompt()` to `roadmap/prompts.py` returning empty string (non-LLM step). (Section 5.7)

**FR-034**: Add `wiring_gate_mode: Literal["off", "shadow", "soft", "full"]` field to `SprintConfig` with default `"shadow"`. (Section 5.8)

**FR-035**: Implement sprint post-task wiring analysis hook: run analysis after task classification, emit per-task report, behavior varies by mode (shadow=log, soft=warn, full=gate). (Section 5.8)

**FR-036**: Implement `ast_analyze_file()` as ToolOrchestrator analyzer plugin populating `FileAnalysis.references` field. (Section 5.3, G-008)

**FR-037**: ToolOrchestrator AST plugin must populate `has_dispatch_registry` and `injectable_callables` metadata. (Section 5.3)

**FR-038**: Extend audit-scanner agent with `REVIEW:wiring` classification signal for files with wiring indicators. (Section 6.2, G-007)

**FR-039**: Extend audit-analyzer agent with 9th mandatory field "Wiring path" (Declaration -> Registration -> Invocation chain). (Section 6.3)

**FR-040**: Extend audit-validator with Check 5: Wiring Claim Verification (verify callable parameters, registry entries, wiring path completeness). (Section 6.4)

**FR-041**: Implement pre-activation checklist: confirm `provider_dir_names` matches real directory, first-run sanity check (>50 files must produce >0 findings). (Section 7, Phase 1)

**FR-042**: Implement public API: `run_wiring_analysis(target_dir, config?) -> WiringReport`, `emit_report(report, output_path, enforcement_mode)`, `ast_analyze_file(file_path, content) -> FileAnalysis`. (Section 8.1)

## Non-Functional Requirements

**NFR-001**: Analysis must complete in < 5 seconds for 50 files. (SC-008, Section 9 R4)

**NFR-002**: Analysis must be < 2 seconds for sprint post-task hook (AST-only, no subprocess). (Section 9, R4)

**NFR-003**: Analysis must be deterministic — same inputs always produce same outputs. (Section 7, Phase 2 rollback trigger)

**NFR-004**: Graceful degradation on AST parse errors — log and skip unparseable files, do not crash. (Section 9, R2)

**NFR-005**: No signature changes to any existing pipeline substrate symbols (`SemanticCheck`, `GateCriteria`, `Step`, `GateMode`, `gate_passed()`, `TrailingGateRunner`, `DeferredRemediationLog`). (Section 3.1)

**NFR-006**: Semantic check functions must be pure — `check_fn: Callable[[str], bool]` with no I/O. (Section 3.1)

**NFR-007**: Preserve layering: `pipeline/*` MUST NOT import from `roadmap/*`, `audit/*`, or `sprint/*`. `audit/*` may import `pipeline/models.py`. (Section 3.2)

**NFR-008**: Separate analysis from enforcement — three distinct layers: deterministic analysis, artifact emission, gate enforcement. (Section 3.3)

**NFR-009**: Extend cleanup-audit, don't duplicate — reuse existing audit structural outputs, keep deterministic analysis authoritative. (Section 3.4)

**NFR-010**: Test coverage >= 90% on `wiring_gate.py` and `wiring_analyzer.py`. (Section 10.3)

**NFR-011**: Minimum 20 unit tests and 3 integration tests. (Section 10.1, 10.2)

**NFR-012**: Test fixtures limited to 50-80 LOC. (Section 10.3)

**NFR-013**: Phase 2 (soft) promotion requires FPR < 15%, TPR > 50%, p95 < 5s. (Section 7)

**NFR-014**: Phase 3 (full) promotion requires FPR < 5%, TPR > 80%, whitelist stable 5+ sprints. (Section 7)

**NFR-015**: Production code estimated at 480-580 lines; test code at 370-480 lines. (Frontmatter)

**NFR-016**: Agent extensions must be additive only — no existing tools or rules changed. (Section 6.1)

**NFR-017**: Resume behavior: wiring-verification step must be deterministic and reproducible for pipeline resume. (Section 5.7.2)

**NFR-018**: Wiring gate does not have its own override mechanism; overrides handled at lifecycle governance level. (Section 15.3)

## Complexity Assessment

**complexity_score**: 0.82
**complexity_class**: HIGH

**Scoring rationale**:

| Factor | Score | Weight | Rationale |
|--------|-------|--------|-----------|
| Component count | 0.85 | 0.20 | 7 new files, 7 modified files, 5 agent extensions |
| Integration surface | 0.90 | 0.25 | Touches roadmap executor, sprint executor, pipeline gate substrate, audit agents, ToolOrchestrator |
| Algorithm complexity | 0.75 | 0.20 | AST parsing with cross-file import resolution, registry analysis, multi-mode enforcement |
| Coordination risk | 0.80 | 0.15 | Merge conflict risk with anti-instincts and other v3.x branches; 3-phase rollout |
| Domain complexity | 0.75 | 0.10 | Static analysis domain with known FPR challenges (import aliases, re-exports) |
| Testing burden | 0.80 | 0.10 | 20+ unit tests, 3+ integration tests, fixture authoring, 90% coverage target |

**Weighted score**: 0.85×0.20 + 0.90×0.25 + 0.75×0.20 + 0.80×0.15 + 0.75×0.10 + 0.80×0.10 = 0.170 + 0.225 + 0.150 + 0.120 + 0.075 + 0.080 = **0.82**

## Architectural Constraints

1. **Preserve existing gate substrate**: No signature changes to `SemanticCheck`, `GateCriteria`, `Step`, `GateMode`, `gate_passed()`, `TrailingGateRunner`, or `DeferredRemediationLog`. (Section 3.1)

2. **Layering constraint (NFR-007)**: `pipeline/*` MUST NOT import from `roadmap/*`, `audit/*`, or `sprint/*`. Import direction is strictly one-way. (Section 3.2)

3. **Three-layer separation**: Deterministic wiring analysis (pure Python, no LLM) → artifact emission (Markdown + YAML) → gate enforcement (existing `gate_passed()`). (Section 3.3)

4. **Static gate wiring**: No dynamic gate registry exists. Gates are wired statically at `Step` construction in `_build_steps()`. (Section 5.7.1)

5. **Deterministic step, not LLM step**: Wiring verification must run as executor-special-cased deterministic Python, not LLM synthesis. (D2, D2a)

6. **Artifact-based enforcement**: Gate evaluates report content via `check_fn(content: str) -> bool`, not repository state. (D1)

7. **Python-only analysis**: Cross-language analysis explicitly out of scope. (Non-Goals)

8. **No dynamic dispatch resolution**: `**kwargs`, `getattr`, `importlib` patterns excluded. (Non-Goals)

9. **Frontmatter regex duplication**: `_FRONTMATTER_RE` duplicated in `audit/wiring_gate.py` as private constant (not imported from `pipeline/gates.py`) to preserve layering. (Section 5.5)

10. **ToolOrchestrator cut criteria**: T06 can be deferred to v3.1 if not complete before T08 begins. Core functionality does not depend on it. (Section 5.3.1)

11. **`retry_limit=0`**: Wiring step executes exactly once — deterministic analysis makes retries pointless. (Section 5.7)

12. **Naming constraint**: Existing `GateResult` and `TrailingGateResult` names preserved. Future lifecycle uses `TransitionGateResult`. (Section 8.4)

## Risk Inventory

**RISK-001** (HIGH likelihood, MEDIUM impact): False positives from intentional `Optional[Callable]` hooks.
*Mitigation*: Whitelist mechanism with `wiring_whitelist.yaml`; shadow-mode calibration before enforcement.

**RISK-002** (MEDIUM likelihood, LOW impact): AST parsing fails on complex Python patterns.
*Mitigation*: Graceful degradation — log and skip unparseable files; count in `files_skipped`.

**RISK-003** (LOW likelihood, MEDIUM impact): Shadow data insufficient to calibrate promotion thresholds.
*Mitigation*: Minimum 2-release shadow period before soft promotion.

**RISK-004** (LOW likelihood, MEDIUM impact): Sprint performance impact from post-task analysis.
*Mitigation*: AST-only analysis with no subprocesses; target < 2s execution.

**RISK-005** (HIGH likelihood, HIGH impact): `provider_dir_names` misconfiguration causing missed or false findings.
*Mitigation*: Pre-activation checklist with sanity check (>50 files → >0 findings); rollback if zero findings on known-unwired codebase.

**RISK-006** (HIGH likelihood, MEDIUM impact): Import re-export aliases cause elevated false positive rate.
*Mitigation*: Documented as known limitation; v3.1 alias pre-pass planned; FPR noise floor measured before soft promotion.

**RISK-007** (MEDIUM likelihood, MEDIUM impact): Agent behavioral extension regression.
*Mitigation*: Additive-only changes; no existing agent rules removed or tools changed.

**RISK-008** (LOW likelihood, LOW impact): `resolve_gate_mode()` forces BLOCKING when shadow intended.
*Mitigation*: Explicit `gate_mode` on Step construction; mode-aware semantic checks return True for shadow regardless.

## Dependency Inventory

| # | Dependency | Type | Location |
|---|-----------|------|----------|
| DEP-001 | `SemanticCheck` | Internal symbol | `pipeline/models.py:58-65` |
| DEP-002 | `GateCriteria` | Internal symbol | `pipeline/models.py:67-75` |
| DEP-003 | `Step` | Internal symbol | `pipeline/models.py:77-90` |
| DEP-004 | `GateMode` | Internal symbol | `pipeline/models.py:46-55` |
| DEP-005 | `gate_passed()` | Internal function | `pipeline/gates.py:20-74` |
| DEP-006 | `_FRONTMATTER_RE` | Internal regex (duplicated) | `pipeline/gates.py:77-80` |
| DEP-007 | `TrailingGateRunner` | Internal class | `pipeline/trailing_gate.py:88-213` |
| DEP-008 | `DeferredRemediationLog` | Internal class | `pipeline/trailing_gate.py:489-578` |
| DEP-009 | `resolve_gate_mode()` | Internal function | `pipeline/trailing_gate.py:593-628` |
| DEP-010 | `ToolOrchestrator` + `FileAnalysis` | Internal class | `audit/tool_orchestrator.py` |
| DEP-011 | `_build_steps()` | Internal function | `roadmap/executor.py:344-476` |
| DEP-012 | `SprintGatePolicy` | Internal class | `sprint/executor.py:50-93` |
| DEP-013 | Python `ast` module | Stdlib | Standard library |
| DEP-014 | Python `re` module | Stdlib | Standard library |

## Success Criteria

| ID | Criterion | Threshold | Verification Method |
|----|-----------|-----------|-------------------|
| SC-001 | Detects `Optional[Callable]=None` never provided | 100% detection on test fixtures | Unit test |
| SC-002 | Detects orphan modules in provider directories | 100% detection on test fixtures | Unit test |
| SC-003 | Detects unresolvable registry entries | 100% detection on test fixtures | Unit test |
| SC-004 | Report conforms to GateCriteria validation | `gate_passed()` returns True on valid report | Unit test |
| SC-005 | `gate_passed()` evaluates WIRING_GATE without modification | Existing function processes new gate | Integration test |
| SC-006 | Shadow mode logs without affecting task status | Sprint task status unchanged with shadow active | Integration test |
| SC-007 | Whitelist excludes findings and reports suppression count | `whitelist_entries_applied` matches applied count | Unit test |
| SC-008 | Analysis completes in < 5s for 50 files | p95 < 5000ms | Benchmark |
| SC-009 | Catches cli-portify executor no-op bug | At least 1 finding on cli-portify fixture | Retrospective |
| SC-010 | Pre-activation warns on zero matches | Warning emitted when >50 files yield 0 findings | Integration test |
| SC-011 | audit-scanner flags `REVIEW:wiring` | Files with wiring indicators classified correctly | Agent test |
| SC-012 | audit-analyzer produces 9-field profile with Wiring path | 9th field present and populated | Agent test |
| SC-013 | ToolOrchestrator AST plugin populates references | `FileAnalysis.references` non-empty for files with imports | Unit test |
| SC-014 | Mode-aware enforcement: shadow passes, full blocks on findings | Shadow returns True with findings; full returns False | Unit test |

## Open Questions

1. **`provider_dir_names` configuration**: What is the definitive set of directory names that should be treated as provider directories? Current default (`steps`, `handlers`, `validators`, `checks`) is assumed but unconfirmed. Owner and deadline TBD. (Section 15.4)

2. **FPR threshold for soft activation**: What specific FPR threshold should gate soft-mode promotion? Spec says < 15% but notes it must be separated from re-export noise floor. Requires shadow data. (Section 15.4)

3. **Whitelist governance**: Who is authorized to add whitelist entries? What is the review cadence? No process defined. (Section 15.4)

4. **Shadow window duration**: How many sprints must shadow mode run before soft promotion is permitted? Spec says "min 2-release" but this needs a concrete number. (Section 15.4)

5. **Merge conflict coordination**: How will modifications to `roadmap/gates.py` be sequenced with Anti-Instincts (v3.05) and other v3.x branches? Single coordinated PR or sequenced rebases? (Section 15.1)

6. **Known 30-70% FPR from import aliases**: The spec acknowledges a potentially very high false positive rate from unresolved import aliases and re-exports. Is this acceptable for shadow mode, or should alias resolution be prioritized before initial deployment? (Section 5.2.1)

7. **ToolOrchestrator `analyzer` parameter**: Does `ToolOrchestrator.__init__()` currently accept an `analyzer` parameter, or does this injection seam need to be created? The spec assumes it exists. (Section 5.3)

8. **`grace_period` configuration**: The spec notes that `grace_period > 0` should be set for TRAILING behavior during shadow rollout, but doesn't specify who controls this or what the default is. (Section 7, Phase 1)

9. **Cleanup of existing 32 unwired symbols**: The gate detects but does not remediate. The spec references v3.6-Cli-portify-fix for cleanup — is there a dependency or ordering constraint? (Section 15.2)

10. **Severity classification criteria**: The spec defines severity levels (critical/major/info) per finding type but the boundary between "execution/dispatch/enforcement behavior depends on the seam" (critical) and "seam is dead but local fallback exists" (major) requires human judgment. How will initial severity assignments be validated? (Section 5.2.1)
