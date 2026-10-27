---
spec_source: merged-spec.md
generated: "2026-03-19T00:00:00Z"
generator: requirements-extraction-agent-opus-4.6
functional_requirements: 38
nonfunctional_requirements: 14
total_requirements: 52
complexity_score: 0.78
complexity_class: HIGH
domains_detected: [backend, static-analysis, pipeline-infrastructure, audit, testing]
risks_identified: 8
dependencies_identified: 15
success_criteria_count: 14
extraction_mode: standard
pipeline_diagnostics: {elapsed_seconds: 133.0, started_at: "2026-03-19T01:47:47.298905+00:00", finished_at: "2026-03-19T01:50:00.317469+00:00"}
---

## Functional Requirements

- **FR-001**: Detect unwired injectable dependencies — constructor parameters typed `Optional[Callable]` (or `Callable | None`) with default `None` that are never explicitly provided at any call site. *(G-001, SC-001)*
- **FR-002**: Detect orphan modules — Python files in provider directories whose exported functions are never imported by any consumer. *(G-002, SC-002)*
- **FR-003**: Detect unwired dispatch registries — registry dictionaries whose values reference non-importable functions. *(G-003, SC-003)*
- **FR-004**: Emit structured YAML+Markdown wiring verification report conforming to `GateCriteria`/`SemanticCheck` contracts. *(G-004, SC-004)*
- **FR-005**: Deploy wiring gate in shadow mode initially with a defined path to soft and full enforcement. *(G-005, SC-006)*
- **FR-006**: Integrate wiring verification as a post-merge step in the roadmap pipeline via `_build_steps()`. *(G-006, SC-005)*
- **FR-007**: Integrate with cleanup-audit protocol by extending audit-scanner, audit-analyzer, and audit-validator agents. *(G-007, SC-011, SC-012)*
- **FR-008**: Provide AST analyzer plugin for `ToolOrchestrator` injection seam to populate `FileAnalysis.references`. *(G-008, SC-013)*
- **FR-009**: Implement `WiringFinding` dataclass with fields: `finding_type`, `file_path`, `symbol_name`, `line_number`, `detail`, `severity`. *(Section 5.1)*
- **FR-010**: Implement `WiringReport` dataclass with `total_findings` property derived from list lengths and `blocking_for_mode()` method implementing shadow/soft/full semantics. *(Section 5.1)*
- **FR-011**: Implement `WiringConfig` dataclass with `registry_patterns`, `provider_dir_names`, `whitelist_path`, `exclude_patterns`. *(Section 4.2.1)*
- **FR-012**: Unwired callable analysis must AST-parse Python files, extract `Optional[Callable]` params with `None` default from `__init__`, search call sites for keyword provision, and flag zero-provider params. *(Section 5.2.1)*
- **FR-013**: Support whitelist via `wiring_whitelist.yaml` with `symbol` and `reason` fields; malformed entries logged as WARNING in Phase 1, raise `WiringConfigError` in Phase 2+. *(Section 5.2.1)*
- **FR-014**: Assign severity levels: critical (execution/dispatch depends on seam), major (dead seam with local fallback), info (whitelisted intentional optional). *(Section 5.2.1)*
- **FR-015**: Orphan module analysis must identify provider directories by convention (`config.provider_dir_names`), AST-parse files, extract public top-level defs, search for imports outside provider dir. *(Section 5.2.2)*
- **FR-016**: Exclude `__init__.py`, `conftest.py`, `test_*.py` from orphan analysis. *(Section 5.2.2)*
- **FR-017**: Apply dual evidence rule: symbol is orphaned only if direct analysis finds no import chain AND cleanup-audit evidence does not justify dynamic/deferred use. *(Section 5.2.2)*
- **FR-018**: Registry analysis must detect module-level dict assignments matching `REGISTRY_PATTERNS`, verify each entry resolves to importable function. *(Section 5.2.3)*
- **FR-019**: Registry analysis must classify three detection types: entry unresolved (critical), registry unused (major), explicit None handler (major). *(Section 5.2.3)*
- **FR-020**: Implement `ast_analyze_file()` as `ToolOrchestrator` plugin returning `FileAnalysis` with populated `references`, `imports`, `exports`, and metadata (`has_dispatch_registry`, `injectable_callables`). *(Section 5.3)*
- **FR-021**: Handle `SyntaxError` in AST parsing gracefully by returning empty `FileAnalysis`. *(Section 5.3)*
- **FR-022**: Report frontmatter must contain exactly 17 specified fields: `gate`, `target_dir`, `files_analyzed`, `files_skipped`, `rollout_mode`, `analysis_complete`, `audit_artifacts_used`, `unwired_callable_count`, `orphan_module_count`, `unwired_registry_count`, `critical_count`, `major_count`, `info_count`, `total_findings`, `blocking_findings`, `whitelist_entries_applied`. *(Section 5.4, 8.2)*
- **FR-023**: Report Markdown body must contain 7 sections in order: Summary, Unwired Optional Callable Injections, Orphan Modules/Symbols, Unregistered Dispatch Entries, Suppressions and Dynamic Retention, Recommended Remediation, Evidence and Limitations. *(Section 5.4.1)*
- **FR-024**: Implement `_extract_frontmatter_values()` private helper in `audit/wiring_gate.py` (~15 LOC) to extract frontmatter key-value pairs, duplicating `_FRONTMATTER_RE` from `pipeline/gates.py`. *(Section 5.5)*
- **FR-025**: Define `WIRING_GATE` as `GateCriteria` with `enforcement_tier="STRICT"`, `min_lines=10`, 17 required frontmatter fields, and 5 semantic checks. *(Section 5.6)*
- **FR-026**: Implement 5 semantic check functions: `_analysis_complete_true`, `_recognized_rollout_mode`, `_finding_counts_consistent`, `_severity_summary_consistent`, `_zero_blocking_findings_for_mode`. *(Section 5.6)*
- **FR-027**: `_zero_blocking_findings_for_mode` must return True unconditionally for shadow mode, check `blocking_findings == 0` for soft/full modes. *(Section 5.6)*
- **FR-028**: Report emitter must compute `blocking_findings` based on rollout mode: shadow=0, soft=critical_count, full=critical_count+major_count. *(Section 5.6)*
- **FR-029**: Add `build_wiring_verification_prompt()` to `roadmap/prompts.py` returning empty string (non-LLM step). *(Section 5.7)*
- **FR-030**: Add wiring-verification `Step` to `_build_steps()` after spec-fidelity with `gate_mode=GateMode.TRAILING`, `retry_limit=0`, `timeout_seconds=60`. *(Section 5.7)*
- **FR-031**: Executor must special-case `step.id == "wiring-verification"` to run `run_wiring_analysis()` and `emit_report()` instead of LLM execution. *(Section 5.7.1)*
- **FR-032**: Update `_get_all_step_ids()` to include `"wiring-verification"` after `"spec-fidelity"` and before `"remediate"`. *(Section 5.7)*
- **FR-033**: Update `ALL_GATES` in `roadmap/gates.py` to include `WIRING_GATE`. *(Section 5.7)*
- **FR-034**: Add `wiring_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"` to `SprintConfig` in `sprint/models.py`. *(Section 5.8)*
- **FR-035**: Implement sprint post-task wiring analysis hook with mode-dependent behavior (shadow: log, soft: warn, full: gate_passed + remediation). *(Section 5.8)*
- **FR-036**: Extend audit-scanner agent to add `REVIEW:wiring` classification signal for files with wiring indicators. *(Section 6.2)*
- **FR-037**: Extend audit-analyzer agent to add 9th mandatory field "Wiring path" (Declaration -> Registration -> Invocation chain) with `UNWIRED_DECLARATION` and `BROKEN_REGISTRATION` finding types. *(Section 6.3)*
- **FR-038**: Extend audit-validator agent to add Check 5 (Wiring Claim Verification) with critical fail on DELETE recommendation for files with live wiring paths. *(Section 6.4)*

## Non-Functional Requirements

- **NFR-001**: Analysis must complete in < 5 seconds for 50 files. *(SC-008)*
- **NFR-002**: Analysis must be pure deterministic Python using AST — no LLM synthesis, no subprocess calls. *(Section 3.3, D2)*
- **NFR-003**: Test coverage must be >= 90% on `wiring_gate.py` and `wiring_analyzer.py`. *(Section 10.3)*
- **NFR-004**: Minimum 20 unit tests and 3 integration tests. *(Section 10.1, 10.2)*
- **NFR-005**: All string-valued frontmatter fields must use `yaml.safe_dump()` to prevent YAML injection. *(Section 5.4)*
- **NFR-006**: Zero signature changes to existing pipeline substrate symbols (`SemanticCheck`, `GateCriteria`, `Step`, `GateMode`, `gate_passed()`, `TrailingGateRunner`, `DeferredRemediationLog`). *(Section 3.1)*
- **NFR-007**: Strict dependency layering: `pipeline/*` must NOT import from `roadmap/*`, `audit/*`, or `sprint/*`. *(Section 3.2)*
- **NFR-008**: Phase 2 (soft mode) activation requires FPR < 15%, TPR > 50%, p95 < 5s. *(Section 7)*
- **NFR-009**: Phase 3 (full mode) activation requires FPR < 5%, TPR > 80%, whitelist stable for 5+ sprints. *(Section 7)*
- **NFR-010**: Total new production code estimated at 480-580 lines; total test code 370-480 lines. *(Section 12)*
- **NFR-011**: `retry_limit=0` — deterministic step executes exactly once; transient filesystem errors handled within analysis function. *(Section 5.7)*
- **NFR-012**: ToolOrchestrator AST plugin (T06) has explicit cut criteria: defer to v2.1 if not complete before T08 begins. *(Section 5.3.1)*
- **NFR-013**: Agent extensions must be additive only — no existing tools changed, no existing rules removed. *(Section 6.1)*
- **NFR-014**: FPR calibration for Phase 2 must use `measured_FPR + 2 sigma` above re-export noise floor; must not activate if unwired-callable FPR cannot be separated from noise. *(Section 7)*

## Complexity Assessment

**complexity_score**: 0.78
**complexity_class**: HIGH

**Rationale**:
- **Integration breadth** (high): Touches 3 subsystems (roadmap, sprint, audit) plus 5 agent behavioral specs, while preserving strict layering constraints on a 4th subsystem (pipeline). The dual-mode operation (roadmap gate + sprint hook + audit extension) multiplies integration surface.
- **Algorithmic depth** (medium-high): Three distinct AST-based analysis algorithms (unwired callables, orphan modules, unwired registries), each with different traversal patterns, scope resolution, and severity classification logic.
- **Constraint density** (high): Zero changes to pipeline substrate, strict dependency direction enforcement, frontmatter invariants (three-way consistency), mode-aware enforcement semantics, and explicit cut criteria for optional components.
- **Rollout complexity** (medium): Three-phase shadow/soft/full rollout with statistical FPR calibration gates and `grace_period` interaction considerations.
- **Testing burden** (medium): 20+ unit tests, 3+ integration tests, 90% coverage target, test fixtures.

## Architectural Constraints

1. **Zero pipeline changes**: No modifications to `pipeline/models.py`, `pipeline/gates.py`, `pipeline/trailing_gate.py`, or any `pipeline/*` module. The wiring gate is a consumer of existing pipeline contracts.
2. **Dependency layering (NFR-007)**: `audit/*` may import `pipeline/models.py`; `roadmap/*` and `sprint/*` may import `audit/*` and `pipeline/*`; `pipeline/*` must NEVER import from `roadmap/*`, `audit/*`, or `sprint/*`.
3. **SemanticCheck contract preservation**: `check_fn: Callable[[str], bool]` — pure function, no I/O, receives report content string only.
4. **Artifact-based enforcement**: Gate evaluation operates on emitted report files, not repository state. Policy is encoded in the report frontmatter.
5. **Deterministic analysis only**: No LLM synthesis for wiring analysis. AST-only, no subprocess, no dynamic dispatch resolution.
6. **Static gate wiring**: Gates are wired at `Step` construction time in `_build_steps()` — no dynamic gate registry.
7. **Frontmatter regex duplication**: `_FRONTMATTER_RE` must be duplicated as private constant in `audit/wiring_gate.py` to preserve layering (cannot import from `pipeline/gates.py`).
8. **Extend, don't duplicate**: Cleanup-audit integration must extend existing agents, not create new agent types.
9. **Technology mandate**: Python 3.10+, `ast` stdlib module for parsing, `yaml.safe_dump()` for serialization.
10. **Merge coordination**: Modifications to `roadmap/gates.py` require coordination with Anti-Instincts and Unified Audit Gating concurrent work.

## Risk Inventory

1. **R1** (severity: high) — False positives from intentional `Optional[Callable]` hooks. *Mitigation*: Whitelist mechanism; shadow-mode calibration period; expected 30-70% FPR contribution from import aliases (planned fix in v2.1).
2. **R2** (severity: low) — AST parsing fails on complex patterns (decorators, metaclasses, dynamic construction). *Mitigation*: Graceful degradation — log SyntaxError, skip file, continue analysis.
3. **R3** (severity: medium) — Shadow data insufficient to calibrate FPR/TPR thresholds for Phase 2 activation. *Mitigation*: Minimum 2-release shadow period before soft-mode activation.
4. **R4** (severity: medium) — Sprint performance impact from per-task wiring analysis. *Mitigation*: AST-only (no subprocess); < 2s target; < 5s budget for 50 files.
5. **R5** (severity: high) — `provider_dir_names` misconfiguration causes orphan analysis to scan wrong directories or miss real providers. *Mitigation*: Pre-activation checklist; first-run sanity check (>50 files must produce >0 findings).
6. **R6** (severity: high) — Re-export aliases and `__init__.py` chains cause false positives in unwired callable and orphan detection. *Mitigation*: Documented as known limitation; alias pre-pass planned for v2.1; noise floor documented.
7. **R7** (severity: medium) — Agent behavioral spec extensions cause regression in existing audit functionality. *Mitigation*: Extensions are strictly additive; no existing tools changed, no existing rules removed.
8. **R8** (severity: low) — `resolve_gate_mode()` forces BLOCKING, overriding shadow TRAILING intent. *Mitigation*: Explicit `gate_mode` on Step definition; mode-aware semantic checks return True for shadow regardless of GateMode.

## Dependency Inventory

1. **`pipeline/models.py`** — `SemanticCheck`, `GateCriteria`, `Step`, `GateMode` (existing, zero changes)
2. **`pipeline/gates.py`** — `gate_passed()` function (existing, zero changes)
3. **`pipeline/trailing_gate.py`** — `TrailingGateRunner`, `DeferredRemediationLog`, `resolve_gate_mode()` (existing, zero changes)
4. **`audit/tool_orchestrator.py`** — `ToolOrchestrator`, `FileAnalysis` (existing, zero changes)
5. **`roadmap/executor.py`** — `_build_steps()`, `_get_all_step_ids()`, `roadmap_run_step()` (existing, modified)
6. **`roadmap/gates.py`** — `ALL_GATES` list (existing, modified)
7. **`roadmap/prompts.py`** — prompt builder module (existing, modified)
8. **`sprint/executor.py`** — sprint task execution loop (existing, modified)
9. **`sprint/models.py`** — `SprintConfig` (existing, modified)
10. **Python `ast` module** — stdlib, AST parsing
11. **Python `re` module** — stdlib, registry pattern matching
12. **Python `yaml` module** — `yaml.safe_dump()` for YAML serialization
13. **`wiring_whitelist.yaml`** — optional external configuration file for suppression entries
14. **5 audit agent behavioral specs** (`audit-scanner.md`, `audit-analyzer.md`, `audit-comparator.md`, `audit-validator.md`, `audit-consolidator.md`) — agent markdown files modified
15. **`cli-unwired-components-audit.md`** — forensic evidence document (input context, not runtime dependency)

## Success Criteria

| ID | Criterion | Threshold | Verification Method |
|----|-----------|-----------|---------------------|
| SC-001 | Detects `Optional[Callable]=None` never provided | At least 1 finding from known fixture | Unit test |
| SC-002 | Detects orphan modules in provider directories | At least 1 finding from fixture with zero importers | Unit test |
| SC-003 | Detects unresolvable registry entries | At least 1 finding from fixture with bad reference | Unit test |
| SC-004 | Report conforms to GateCriteria validation | `gate_passed()` returns True on well-formed report | Unit test |
| SC-005 | `gate_passed()` evaluates WIRING_GATE without modification | Existing `gate_passed()` function processes WIRING_GATE correctly | Integration test |
| SC-006 | Shadow mode logs without affecting task status | Sprint task status unchanged when wiring findings exist in shadow | Integration test |
| SC-007 | Whitelist excludes findings and reports suppression count | `whitelist_entries_applied > 0` when whitelist matches | Unit test |
| SC-008 | Analysis completes within time budget | < 5 seconds for 50 Python files | Benchmark test |
| SC-009 | Catches cli-portify executor no-op bug | Retrospective run detects known unwired `step_runner` | Retrospective validation |
| SC-010 | Pre-activation warns on zero matches | Warning emitted when `provider_dir_names` finds no matching directories | Integration test |
| SC-011 | audit-scanner flags `REVIEW:wiring` | Files with wiring indicators classified as `REVIEW:wiring` | Agent test |
| SC-012 | audit-analyzer produces 9-field profile with Wiring path | Wiring path field present with chain links or "MISSING" | Agent test |
| SC-013 | ToolOrchestrator AST plugin populates references | `FileAnalysis.references` non-empty for files with imports | Unit test |
| SC-014 | Mode-aware enforcement: shadow passes, full blocks | Shadow mode returns gate pass; full mode blocks on findings | Unit test |

## Open Questions

1. **`audit_artifacts_used` frontmatter field**: Listed in required fields but no algorithm specifies how cleanup-audit artifacts are located, loaded, or counted. How are prior audit artifacts discovered at runtime? Is there a convention for artifact paths?

2. **`files_skipped` semantics**: The `WiringReport` includes `files_skipped` and the frontmatter requires it, but the analysis algorithms don't specify when files are skipped vs. excluded. Are `exclude_patterns` matches counted as "skipped" or silently omitted?

3. **Whitelist validation strictness boundary**: Phase 1 logs malformed entries as WARNING; Phase 2+ raises `WiringConfigError`. How is the current phase determined at runtime? Is it derived from `rollout_mode` or configured separately?

4. **Sprint `source_dir` configuration**: `run_wiring_analysis(target_dir=config.source_dir)` references `config.source_dir` but `SprintConfig` only adds `wiring_gate_mode`. Does `source_dir` already exist on the config, or does it need to be added?

5. **`audit_artifacts_used` computation**: The field appears in required frontmatter but the report emitter's `enforcement_mode` parameter doesn't indicate how audit artifacts contribute. What triggers the count increment?

6. **`audit-comparator` and `audit-consolidator` extensions**: Section 6.1 mentions all 5 agents get extensions, but Sections 6.2-6.4 only detail scanner, analyzer, and validator. What specific behavioral rules are added to comparator ("cross-file wiring consistency check") and consolidator ("Wiring Health section")?

7. **`grace_period` configuration source**: Section 7 notes that `grace_period > 0` is needed for clean TRAILING semantics. Is `grace_period` set per-step, per-pipeline, or globally? Who is responsible for ensuring this configuration during shadow rollout?

8. **Import alias false positive rate**: Known limitation states 30-70% FPR contribution from import aliases. With this range, is shadow mode data collection meaningful for Phase 2 calibration if the noise floor is this high?

9. **Concurrent modification coordination**: Section 15 identifies merge conflict risk with Anti-Instincts and Unified Audit Gating PRs. Is there an established sequencing plan, or is this left to implementer judgment?

10. **`WiringConfig.registry_patterns` default type**: The dataclass specifies `re.Pattern` as the type with `DEFAULT_REGISTRY_PATTERNS` as default, but dataclass fields with mutable defaults typically need `field(default_factory=...)`. Is `re.Pattern` treated as immutable here, or does this need a factory?
