# Researcher R1 — File Inventory (Current Pipeline)

**Task:** TASK-RF-20260531-042405 — Roadmap pipeline brittleness-elimination refactor + rewrite (R0+R1)
**Date:** 2026-05-31
**Scope:** All files under `src/superclaude/cli/roadmap/`, `tests/roadmap/`, and `src/superclaude/skills/sc-roadmap-protocol/`. Includes also the upstream substrate (`src/superclaude/cli/pipeline/models.py`) because R1.2/R1.3 land additions there.

**Method:** `wc -l` for LOC, `grep` for top-level `def`/`class`/`@dataclass` exports, targeted `Read` for signatures and the file:line markers the BUILD-REQUEST already cites. No re-derivation of the retrospective — purely current file state.

**Notable correction vs research-notes.md:** the working directory contains **25** Python files under `src/superclaude/cli/roadmap/` (not 24). The notes omit `validate_gates.py` (70 LOC). LOC totals: **16,698** matches the notes (the additional file is the smallest and the count includes `__init__.py` at 10 LOC).

---

## SECTION A — `src/superclaude/cli/roadmap/` per-file inventory (25 files, 16,698 LOC)

### A.1 Orchestrator / executor

#### `executor.py` (3,701 LOC) — central pipeline orchestrator
- **Role:** assembles the step list, runs the pipeline, dispatches gates, persists state.
- **Key exports:**
  - `roadmap_run_step(...)` L955 — single-step execution
  - `class _ClaudeRunner` L1253 — LLM invocation wrapper
  - `_run_convergence_spec_fidelity(...)` L1290 — convergence wrapper invocation
  - `_run_deviation_analysis(...)` L1592 — deterministic deviation step
  - `_run_remediate_step(...)` L1804 — remediate step entry
  - `build_certify_step(...)` L1899 — certify-step factory (**R1.3 wiring target** for `GateCriteria.code_assertions`)
  - `_build_steps(config: RoadmapConfig) -> list[Step | list[Step]]` L1947 — the full step list (steps 1-14)
  - `execute_roadmap(...)` L2985 — top-level entrypoint
  - `_save_state(...)` L2567 / `write_state(...)` L2832 / `read_state(...)` L2842 — state persistence (per-release `.roadmap-state.json`)
  - `derive_pipeline_status(...)` L2801, `_derive_fidelity_status(...)` L2685 — status derivation
  - `generate_degraded_report(...)` L2704, `build_remediate_metadata(...)` L2749, `build_certify_metadata(...)` L2778
  - `_restore_from_state(...)` L2870, `_apply_resume_after_spec_patch(...)` L3237, `check_remediate_resume(...)` L3449
  - `_auto_invoke_validate(...)` L3409
  - Pre-pipeline helpers: `_route_input_files` L214, `_compress_pipeline_input` L383, `_llm_inputs_for` L411, `_ensure_sidecars_present` L450, `_embed_inputs` L531, `_sanitize_output` L555, `_inject_pipeline_diagnostics` L612, `_inject_provenance_fields` L649
  - Audit helpers: `_run_structural_audit` L689, `_run_anti_instinct_audit` L734, `_validate_merge_completeness` L856
  - Halt/print: `_format_halt_output` L2211, `_print_terminal_halt` L2305, `_dry_run_output` L2531
- **Imports from sibling pipeline modules:** `gates.*` (all `*_GATE` constants), `prompts.*` (all `build_*_prompt`), `models.*` (`RoadmapConfig`, `Finding`), `convergence.*`, `fidelity_checker.*`, `obligation_scanner.*`, `structural_checkers.*`, `semantic_layer.*`, `remediate*`, `validate_executor.*`, `spec_*`, `templates.*`.
- **R0/R1 touch points:**
  - **R1.2** — `_save_state`/`read_state` L2832/L2842 become `PipelineEnvelope` writers (sidecar JSON keyed to step id).
  - **R1.3** — `build_certify_step` L1899 wires the first `CodeAssertion`.
  - **R1.5** — `_build_steps` L1947 gains a terminal `verify-implementation` step (and its `_run_*` wrapper added here).
  - **R1.6** — L2167 `gate=None if config.convergence_enabled else SPEC_FIDELITY_GATE` (the spec-fidelity bypass cited verbatim in BUILD-REQUEST §Brittleness Contract item 4) is deleted; the gate must always be present.
  - **R1.4** — `roadmap_run_step` L955 and `_ClaudeRunner` L1253 are the dispatch sites that flip to tool-write mode per step.

#### `commands.py` (401 LOC) — Click CLI surface — **PRESERVE per MVR**
- **Role:** `superclaude roadmap run|validate|accept-spec-change` Click commands.
- **Key exports:** `roadmap_group()` L15, `run(...)` L175 (the long `--flag` list), `accept_spec_change(...)` L303, `validate(...)` L353.
- **Imports:** click, plus `executor.execute_roadmap`, `validate_executor.execute_validate`, `spec_patch.prompt_accept_spec_change`.
- **R0/R1 touch points:** **none** — Vector A explicit. The CLI surface and `--flag` shape are frozen.

### A.2 Gate registry + frontmatter machinery

#### `gates.py` (1,441 LOC) — gate criteria + semantic-check functions
- **Role:** defines all `*_GATE: GateCriteria` constants and the pure-Python `_*` semantic check functions that the gates reference.
- **Imports `GateCriteria, SemanticCheck` from `superclaude.cli.pipeline.models`** (L25) — the substrate dataclass lives upstream in `cli/pipeline/models.py`, not here.
- **Key exports:**
  - 35 pure semantic-check functions (`_no_heading_gaps` L30 → `_template_sections_present` L927); see Section D for the contract-relevant subset.
  - `_parse_frontmatter(content: str) -> dict[str, str] | None` L168 — **one of two disagreeing frontmatter parsers (Contract #6 target)**.
  - `_strip_yaml_quotes` L150 — frontmatter value normalizer.
  - All `*_GATE` constants (constructed `GateCriteria(...)` calls; see L1039+, L1079+, L1101+, L1106+, L1111+, L1116+, L1121+ for `SemanticCheck` instantiation sites) and the master `ALL_GATES = [...]` registry at L1426-1441 (14 entries, one per pipeline step).
- **R0/R1 touch points:**
  - **R0.3** — module-level constant names (`GATE_FIELD_NAMES` etc.) get re-exported from `superclaude.contracts`.
  - **R1.3** — `GateCriteria.code_assertions: list[CodeAssertion]` slot is added to the upstream dataclass (`cli/pipeline/models.py:91`), not here; gates.py picks up the new slot by re-import.
  - **R1.6** — `_cross_refs_resolve` L48 is a "warning-only" stub that always returns `True` (L88-91) — **Contract #5 return-True-stub target**; delete or make fail-closed.
  - **R1.6** — `_parse_frontmatter` L168 must be canonicalized against the second parser (`cli/pipeline/gates.py:_check_frontmatter` — see Cross-substrate note below).

#### `validate_gates.py` (70 LOC) — `validate` subcommand semantic checks
- **Role:** light second gate file used only by the `validate` Click subcommand path.
- **Key exports:** `_has_agreement_table(content: str) -> bool` L16 (the only function).
- **R0/R1 touch points:** none direct; affected only insofar as Contract #6 (parser consistency) and Contract #8 (threshold registry) ripple here.

### A.3 Determinism & preserved subsystems

#### `structural_checkers.py` (1,069 LOC) — **PRESERVE per MVR** (v3.05 deterministic structural-check layer)
- **Role:** spec-vs-roadmap structural diff for signatures, data-models, gates, CLI, NFRs.
- **Key exports:**
  - `get_severity(dimension, mismatch_type)` L60, `_route_findings(...)` L186, `_make_finding(...)` L261
  - `_canonicalize_requirement_id(...)` L295, `_classify_nfr_severity(...)` L356, `_get_sections_for_dimension(...)` L377, `_section_text(...)` L391
  - Five structural checkers: `check_signatures(...)` L402, `check_data_models(...)` L538, `check_gates(...)` L651, `check_cli(...)` L755, `check_nfrs(...)` L842
  - `run_all_checkers(spec_path, roadmap_path) -> list[Finding]` L1057 — aggregator
  - Local dataclasses `RegressionResult` L227, `RemediationPatch` L242 (shadow the ones in `convergence.py`/`remediate_executor.py` — possible Contract #6 ripple)
- **R0/R1 touch points:** **none** — MVR §3 explicit "preserve".

#### `convergence.py` (778 LOC) — **PRESERVE per MVR** (convergence wrapper)
- **Role:** wraps spec-fidelity step in convergence ladder; deviation registry; regression detection.
- **Key exports:**
  - `_get_turnledger_class()` L37, `reimburse_for_progress(...)` L44, `compute_stable_id(...)` L63
  - `class RunMetadata` L75 (dataclass), `class DeviationRegistry` L91, `class ConvergenceResult` L321, `class RegressionResult` L334 (shadow of structural_checkers')
  - `_check_regression(...)` L343, `_create_validation_dirs(...)` L384, `_cleanup_validation_dirs(...)` L408, `_atexit_cleanup()` L422
  - `execute_fidelity_with_convergence(...)` L434 — primary entrypoint
  - `handle_regression(...)` L671
- **R0/R1 touch points:** envelope migration only (R1.2 sidecar JSON consumers). No semantics changes.

### A.4 Anti-instinct + fidelity + integration

#### `obligation_scanner.py` (825 LOC) — anti-instinct scanner (Layer 1-5)
- **Role:** detects undischarged "feature obligations" in generated roadmaps. Per master report §Recurrence#6, direct ancestor of the MultiModelSwarm false-positive class.
- **Key exports:**
  - `class Obligation` L166, `class ObligationReport` L182 (dataclasses)
  - `scan_obligations(content: str) -> ObligationReport` L208 — primary API
  - Tail/phase helpers: `_find_tail_section_start` L418, `_split_into_phases` L436
  - Context helpers: `_extract_component_context` L526, `_get_context_line` L599, `_is_descriptive_context` L608, `_normalize_h3_for_match` L629, `_build_h3_index` L650, `_is_demoted_h3` L694, `_is_meta_context` L712
  - Discharge logic: `_has_discharge` L749, `_get_code_block_ranges` L771, `_is_inside_code_block` L776, `_is_discharge_intent_line` L784
  - Severity / position: `_determine_severity` L802, `_get_absolute_position` L813
- **`return True` stubs (Contract #5 audit targets):** L719, L722, L725, L729, L733, L737, L741, L760 — these sit inside the heuristic-skip helpers (`_is_demoted_h3` and `_is_meta_context`); they are early-exit short circuits, not gate stubs, so each requires individual classification before deletion.
- **R0/R1 touch points:**
  - **R0.2** — vocab-lint allowlist additions land in this module's term list (search for the term-table near `scan_obligations`).
  - **R1.4** — candidate for tool-write rewrite of detector reports.

#### `fidelity_checker.py` (417 LOC) — spec-fidelity checker
- **Role:** maps spec FRs to codebase function/class names and reports coverage.
- **Key exports:**
  - `class FRMapping` L123, `class FidelityResult` L132 (dataclasses)
  - `class FidelityChecker` L143 — primary class with `check(spec_path) -> list[FidelityResult]` (the loop visible at L287-303)
  - `run_fidelity_check(...)` L401 — top-level callable
- **R0/R1 touch points:**
  - **L287-303 — fail-open default cited verbatim in BUILD-REQUEST §Flaw 4.** The `if not mapping.expected_names: ... found=True, ambiguous=True` branch (L287-303) is the "no extractable names → fail-open per R-3" stub. **R1.6** deletes this and makes the default fail-closed.
  - **R0.1** — `FidelityChecker._extract_fr_mappings` (called L283) becomes the consumer of the `ID_PATTERNS` registry in `superclaude.contracts`.
  - **R1.5** — `verify-implementation` terminal step reuses `FidelityChecker._scan_codebase` (L284) via AST link.

#### `integration_contracts.py` (477 LOC) — integration-contract checking
- **Role:** extracts integration contracts from spec and verifies roadmap coverage.
- **Key exports:**
  - `class IntegrationContract` L122, `class WiringCoverage` L137, `class IntegrationAuditResult` L147 (dataclasses)
  - `extract_integration_contracts(spec_text)` L164, `check_roadmap_coverage(...)` L221
  - `_classify_mechanism(...)` L387, `_extract_identifiers(...)` L417, `_signature_subsumed(...)` L429, `_canonicalize_identifiers(...)` L449
- **R0/R1 touch points:**
  - **R0.3** — identifier extraction shares vocabulary with `obligation_scanner`; both must read the new `superclaude.contracts.GATE_FIELD_NAMES` registry.
  - **R1.1** — contract registry extension (return-type contracts for `check_roadmap_coverage`).

#### `fingerprint.py` (216 LOC) — fingerprint extraction + coverage gate
- **Role:** extracts code-like fingerprints from spec and roadmap, reports coverage.
- **Key exports:**
  - `class Fingerprint` L20 (dataclass)
  - `_is_code_like(text)` L90, `extract_code_fingerprints(content)` L104
  - `check_fingerprint_coverage(...)` L168, `fingerprint_gate_passed(...)` L202
- **`return True` stubs:** L97, L100 — inside `_is_code_like`, short-circuit returns (likely OK heuristics; classify in R1.6 audit).
- **R0/R1 touch points:** **R0.2** — vocab-lint extensions extend the fingerprint vocabulary.

### A.5 Prompt builders (R1.4 tool-write targets)

#### `prompts.py` (1,367 LOC) — all generator/merge/fidelity/wiring prompt strings
- **Role:** central LLM prompt assembly for the 9 LLM steps.
- **Key exports:** `wrap_for_incremental_write(...)` L115, `build_extract_prompt(...)` L181, `build_extract_prompt_tdd(...)` L329, `build_generate_prompt(...)` L533, `build_diff_prompt(...)` L854, `build_debate_prompt(...)` L879, `build_score_prompt(...)` L906, `build_merge_prompt(...)` L964, `build_spec_fidelity_prompt(...)` L1085, `build_wiring_verification_prompt(...)` L1220, `build_test_strategy_prompt(...)` L1278.
- **R0/R1 touch points:** **R1.4 primary target** — each `build_*_prompt` is replaced by a Jinja template under a new `templates/` tree (one phase per builder in the MDTM file). Side-by-side validation per Vector A.

#### `certify_prompts.py` (337 LOC) — certify-step prompts
- **Role:** certification prompt assembly + parsing.
- **Key exports:** `build_certification_prompt(...)` L21, `extract_finding_context(...)` L120, `_extract_by_lines(...)` L156, `_extract_by_section(...)` L172, `generate_certification_report(...)` L202, `parse_certification_output(...)` L278, `route_certification_outcome(...)` L303.
- **R0/R1 touch points:** **R1.4** — per master report §Recurrence#2 evidence indicates this module has dead-code branches; tool-write rewrite resolves it.

#### `validate_prompts.py` (197 LOC) — validate-subcommand prompts
- **Role:** `validate` Click command prompt builders.
- **Key exports:** `build_reflect_prompt(...)` L16, `build_merge_prompt(...)` L149.
- **R0/R1 touch points:** **R1.4** — separate sub-phase (validate is a distinct CLI command path).

#### `remediate_prompts.py` (134 LOC) — remediate prompts
- **Key exports:** `build_remediation_prompt(...)` L17, `group_findings_by_file(...)` L84, `build_cross_file_fragment(...)` L113.
- **R0/R1 touch points:** **R1.4** — Jinja migration.

### A.6 Remediate subsystem

#### `remediate.py` (433 LOC) — remediate orchestration + scoping
- **Key exports:** `class RemediationScope(enum.Enum)` L45, `format_validation_summary(...)` L63, `should_skip_prompt(...)` L111, `filter_findings(...)` L124, `generate_remediation_tasklist(...)` L177, `generate_stub_tasklist(...)` L291, `_parse_routing_list(...)` L324, `deviations_to_findings(...)` L361.
- **R0/R1 touch points:** **R1.2** (envelope consumer), **R1.4** (prompt builders move to Jinja).

#### `remediate_executor.py` (859 LOC) — remediate-step execution
- **Key exports:** `class RemediationPatch` L62, `create_snapshots(...)` L99, `restore_from_snapshots(...)` L127, `cleanup_snapshots(...)` L141, `enforce_allowlist(...)` L155, `_basename(...)` L197, `_run_agent_for_file(...)` L207, `_run_agent_with_retry(...)` L264, `check_patch_diff_size(...)` L309, `_check_diff_size(...)` L365, `_handle_file_rollback(...)` L431, `_check_cross_file_coherence(...)` L453, `_handle_failure(...)` L486, `_handle_success(...)` L529, `update_remediation_tasklist(...)` L563, `_update_frontmatter_counts(...)` L594, `_update_finding_entries(...)` L614, `fallback_apply(...)` L643, `check_morphllm_available(...)` L714, `execute_remediation(...)` L735.
- **`return True` stubs:** L326, L345, L362, L397, L412, L423, L706 — most are inside diff-size helpers (`_check_diff_size`, `_handle_file_rollback`) as "all checks passed → True" returns; classify before deletion.
- **R0/R1 touch points:** **R1.2** envelope migration; potentially **R1.4** tool-write for `_run_agent_for_file`.

#### `remediate_parser.py` (391 LOC) — remediate output parser
- **Key exports:** `parse_validation_report(text)` L18, `parse_individual_reports(...)` L50, `_parse_consolidated_findings(...)` L78, `_parse_flat_findings(...)` L94, `_extract_finding_blocks(...)` L108, `_extract_field(...)` L176, `_extract_agreement_keyword(...)` L203, `_extract_files_from_location(...)` L214, `_validate_required_fields(...)` L231, `_overlay_agreement_categories(...)` L250, `_overlay_remediation_status(...)` L272, `_deduplicate_findings(...)` L297, `_is_location_match(...)` L327, `_extract_line_numbers(...)` L352, `_merge_findings(...)` L364.
- **R0/R1 touch points:** **R1.4** — tool-write rewrite collapses this parser entirely (deterministic write means no parser needed). Major delta.

### A.7 Spec / parsing / patching

#### `spec_parser.py` (639 LOC) — spec markdown parser
- **Key exports:**
  - Dataclasses: `ParseWarning` L19, `CodeBlock` L28, `TableRow` L38, `MarkdownTable` L45, `FunctionSignature` L56, `ThresholdExpression` L65, `SpecSection` L76, `ParseResult` L91
  - `parse_frontmatter(text, warnings)` L109 — **third frontmatter parser variant** (Contract #6 ripple — needs canonicalization with `gates.py:_parse_frontmatter` L168 and `cli/pipeline/gates.py:_check_frontmatter` L91)
  - `extract_tables(...)` L183, `_parse_table_row(...)` L260, `extract_code_blocks(...)` L273
  - `extract_requirement_ids(text) -> dict[str, list[str]]` L333 — **R0.1 primary site for `ID_PATTERNS` consumer**
  - `extract_function_signatures(...)` L352, `extract_literal_values(...)` L376, `extract_thresholds(text)` L400 — **R0.3 `CONVERGENCE_THRESHOLDS` consumer site**
  - `_looks_like_file_path(...)` L437, `extract_file_paths(text)` L471, `extract_file_paths_from_tables(...)` L481
  - `split_into_sections(text)` L499, `parse_document(text) -> ParseResult` L608
- **`return True` stubs:** L468 — inside `_looks_like_file_path` early-exit (likely OK heuristic).
- **R0/R1 touch points:** **R0.1** (ID extraction registry), **R0.3** (threshold extraction registry), **R1.4** (deterministic parser becomes part of tool-write pipeline).

#### `spec_patch.py` (304 LOC) — spec-patch helpers
- **Key exports:** `class DeviationRecord` L40, `scan_accepted_deviation_records(output_dir)` L58, `update_spec_hash(...)` L146, `prompt_accept_spec_change(...)` L162, `_extract_frontmatter(text)` L285 (**fourth frontmatter parser** — Contract #6).
- **R0/R1 touch points:** **R1.2** envelope migration (spec-hash + accepted records become envelope fields).

#### `spec_structural_audit.py` (111 LOC) — spec structural audit
- **Key exports:** `class SpecStructuralAudit` L24, `audit_spec_structure(spec_text)` L37, `check_extraction_adequacy(...)` L88.
- **R0/R1 touch points:** **R0.1** consumer.

### A.8 Semantic / cosmetic / models / misc

#### `semantic_layer.py` (692 LOC) — semantic-check helpers
- **Key exports:**
  - `class RubricScores` L51, `class SemanticCheckRequest` L140, `class SemanticLayerResult` L404 (dataclasses)
  - `_truncate_to_budget(...)` L153, `build_semantic_prompt(request)` L182, `score_argument(...)` L272, `judge_verdict(...)` L326, `wire_debate_verdict(...)` L356
  - `run_semantic_layer(...)` L413, `_execute_semantic_check(...)` L494, `validate_semantic_high(...)` L570
- **R0/R1 touch points:** envelope migration only.

#### `cosmetic_remediator.py` (1,096 LOC) — post-merge cosmetic fix layer
- **Key exports:** `class CosmeticViolation` L160, `class Classification` L170, ~16 detector and apply helpers (`_detect_*`, `_apply_*`), `classify_gate_failure(...)` L682, `apply_cosmetic_remediations(...)` L1020.
- **R0/R1 touch points:** **R1.4 passthrough** — cosmetic remediator runs over tool-write output; only behavioral verification needed (does the renamed-template output still tickle the same fixes).

#### `models.py` (143 LOC) — pipeline dataclasses (local subset)
- **Key exports:**
  - `class Finding` L21 (`@dataclass`) — generic finding type
  - `class AgentSpec` L63 (`@dataclass`) — agent invocation spec
  - `class RoadmapConfig(PipelineConfig)` L93 (`@dataclass`) — **the central config that R1.2 extends** (holds only inputs/flags, no cross-step state per BUILD-REQUEST)
  - `class ValidateConfig(PipelineConfig)` L129 (`@dataclass`)
- **R0/R1 touch points:** **R1.2** — `PipelineEnvelope` is added here (alternative: new `envelope.py` per gap question #3); R1.2 also expands `RoadmapConfig` to hold the envelope path.

#### `templates.py` (71 LOC) — markdown templates
- **Key exports:** `get_template_path(name)` L21 (the only function).
- **R0/R1 touch points:** **R1.4** — gains Jinja template renderer for the tool-write output of each of the 9 LLM steps.

#### `__init__.py` (10 LOC) — package marker
- No exports of note.

---

## SECTION B — Cross-substrate dependency: `src/superclaude/cli/pipeline/models.py` (234 LOC)

Not in the assigned scope, but **R1.3 and R1.2 land additions here**, so flagged for the task builder:

- `class GateMode(Enum)` L73-78 — `BLOCKING` / `TRAILING`
- `class SemanticCheck` L82 — `name: str`, `check_fn: Callable[[str], bool | str]`, `failure_message: str` (the BUILD-REQUEST's "inherent flaw — signature is `(str) -> bool` only" cites this dataclass)
- `class GateCriteria` L91 — currently has `required_frontmatter_fields`, `min_lines`, `enforcement_tier`, `semantic_checks`. **R1.3 adds `code_assertions: list[CodeAssertion]` slot here.**
- `class Step` L109 — fields include `tool_write_mode: bool` L121 (**already exists** — flag is wired but tool-write code path is what R1.4 actually fills in), `template_path: Optional[Path]` L122 (**already exists**).
- `class StepResult` L126

**Also flagged — second frontmatter parser:** `src/superclaude/cli/pipeline/gates.py:_check_frontmatter` L91. With `cli/roadmap/gates.py:_parse_frontmatter` L168 and `cli/roadmap/spec_parser.py:parse_frontmatter` L109 plus `cli/roadmap/spec_patch.py:_extract_frontmatter` L285 plus `cli/cli_portify/utils.py:parse_frontmatter` L11 plus `cli/audit/wiring_gate.py:_extract_frontmatter_values` L931, there are **6 frontmatter-handling variants in the tree**. Contract #6 (parser consistency) must enumerate and canonicalize all of them.

---

## SECTION C — `tests/roadmap/` (64 test files, 28,036 LOC)

Test coverage map (which existing test file maps to which Brittleness Contract item):

| Contract # | Topic | Existing test files (current coverage) | New test file (per BUILD-REQUEST) |
|---|---|---|---|
| 1 | Recurrence regression | partial: `test_phase7_hardening.py`, `test_retrospective.py` | `test_recurrence_regression.py` (NEW) + `fixtures/recurrence/` tree (NEW) |
| 2 | Dispatch reachability | none directly | `test_dispatch_reachability.py` (NEW) |
| 3 | Anti-instinct (general) | `test_anti_instinct_integration.py`, `test_obligation_scanner.py` (1,205 LOC heavy), `test_obligation_scanner_meta_context.py`, `test_obligation_scanner_extract_component_context.py` | reused — Contract #10 adds `test_anti_instinct_recurrence.py` |
| 4 | Gate empty-target | `test_eval_gate_rejection.py`, `test_eval_gate_ordering.py`, `test_certify_gates.py`, `test_validate_gates.py`, `test_gates_data.py` (2,256 LOC) | `test_gate_empty_target.py` (NEW) |
| 5 | No fragility stubs | none — this is a CI lint | `test_no_fragility_stubs.py` (NEW; CI lint) |
| 6 | Parser consistency | `test_spec_parser.py`, `test_remediate_parser.py` | `test_parser_consistency.py` (NEW — enumerates the 6 frontmatter variants) |
| 7 | Retry contract | `test_resume.py`, `test_resume_restore.py`, `test_resume_pipeline_states.py`, `test_validate_resume_failure.py` | `test_retry_contract.py` (NEW) |
| 8 | Threshold registry | `test_models.py`, `test_nfr_compliance.py` | `test_threshold_registry.py` (NEW) |
| 9 | Spec/roadmap ID containment | `test_spec_fidelity.py` (570 LOC), `test_validate_sc001_sc003.py` | `test_spec_roadmap_id_containment.py` (NEW) |
| 10 | Anti-instinct recurrence | see #3 | `test_anti_instinct_recurrence.py` (NEW; seeded from MultiModelSwarm FP) |

**Other contract-relevant existing tests (do NOT delete):**

- `test_convergence.py` (2,049 LOC), `test_convergence_e2e.py`, `test_convergence_smoke.py`, `test_convergence_wiring.py`, `test_eval_convergence_multirun.py` — convergence preservation evidence per MVR
- `test_structural_checkers.py` (1,056 LOC), `test_structural_checkers_properties.py` — preserved-subsystem regression
- `test_executor.py` (1,898 LOC), `test_pipeline_integration.py`, `test_integration_v5_pipeline.py` — orchestrator + e2e
- `test_remediate*.py` (4 files: parser, executor, prompts, top-level) — remediate subsystem
- `test_cosmetic_remediator.py` (1,148 LOC) — cosmetic layer
- `test_certify_prompts.py`, `test_certify_gates.py` — certify subsystem
- `test_fingerprint.py`, `test_inline_fallback.py`, `test_dry_run.py`, `test_progress.py`, `test_parallel.py` — utility coverage
- `test_validate_*.py` (8 files) — validate subcommand
- `test_cli_contract.py`, `test_prd_cli.py`, `test_prd_prompts.py`, `test_halt.py`, `test_state.py`, `test_models.py`, `test_embed_inputs.py`, `test_backward_compat.py`, `test_accept_spec_change.py`, `test_spec_patch_cycle.py`, `test_compression_integration.py`, `test_file_passing.py`, `test_merge_completeness.py`, `test_nfr_compliance.py`, `test_semantic_layer.py`, `test_spec_structural_audit.py`, `test_vocabulary.py`, `test_prompts.py`, `test_remediation.py`, `test_eval_finding_lifecycle.py` — assorted

**Infrastructure:**
- `tests/roadmap/conftest.py` (60 LOC) — fixtures (R1.2 envelope-fixture extension target)
- `tests/roadmap/__init__.py` (empty)

---

## SECTION D — `src/superclaude/skills/sc-roadmap-protocol/` (skill protocol files)

| File | LOC | 1-sentence content summary |
|---|---|---|
| `SKILL.md` | 1,094 | Top-level skill prose for `/sc:roadmap` — orchestration narrative, flag reference, MVR-alignment summary; **R1 alignment target per master §Flaw 5** (must reflect new envelope/registry vocabulary once R1 lands). |
| `__init__.py` | 1 | Empty package marker. |
| `refs/extraction-pipeline.md` | 700 | Extract-step prose — how `build_extract_prompt` is structured, FR-extraction rules; **R1.4 alignment target** (Jinja templates replace the embedded examples). |
| `refs/templates.md` | 519 | Output-template prose — frontmatter shapes, OR-group aliases (`spec_source` vs `spec_sources`), section conventions; **R0.3 / R1.2 alignment target** (envelope shape + contract registry referenced here). |
| `refs/adversarial-integration.md` | 692 | Adversarial-debate prose for `diff`/`debate`/`score`/`merge` stages — **PRESERVE per MVR**. |
| `refs/scoring.md` | 322 | Scoring rubric prose for the adversarial layer — preserve; possible threshold-registry cross-link (Contract #8). |
| `refs/validation.md` | 474 | Validation-gate prose — describes the current `validate` subcommand pipeline; **R0.3 / R1.6 alignment target** (return-contract registry referenced here; fail-open/fail-closed semantics documented here). |

**Total skill LOC:** 3,802 LOC of prose. Phase 12 ("Skill protocol alignment") in research-notes.md targets all 6 of these `.md` files plus `SKILL.md`. Re-skim each after R1.6 lands to catch any stale "currently the gate is bypassed" type prose.

---

## SECTION E — Files NOT in scope but cross-referenced

These are not under the assigned directories but the BUILD-REQUEST or R0/R1 phases touch them:

- `src/superclaude/contracts/` — **DOES NOT EXIST.** R0.3 creates it with `__init__.py` exporting `ID_PATTERNS`, `CONVERGENCE_THRESHOLDS`, `GATE_FIELD_NAMES`; R1.1 extends with `RETURN_CONTRACTS`.
- `src/superclaude/cli/pipeline/models.py` — Section B above; R1.3 adds `code_assertions` slot, R1.2 may add `PipelineEnvelope` here vs in `cli/roadmap/models.py`.
- `src/superclaude/cli/pipeline/gates.py:_check_frontmatter` L91 — Contract #6 ripple.
- `src/superclaude/cli/audit/wiring_gate.py` (`WIRING_GATE` constant imported by `cli/roadmap/gates.py:24` and `_extract_frontmatter_values` L931) — Contract #6 ripple.
- `src/superclaude/cli/cli_portify/utils.py:parse_frontmatter` L11 — Contract #6 ripple (outside roadmap pipeline, but listed for completeness in the parser-consistency lint).

---

## SECTION F — File-by-file R0/R1 touch matrix (quick reference for task builder)

| File | R0.1 ID-set | R0.2 vocab-lint | R0.3 contracts | R1.1 contracts-ext | R1.2 envelope | R1.3 code-assert | R1.4 tool-write | R1.5 verify-impl | R1.6 cleanup |
|---|---|---|---|---|---|---|---|---|---|
| `executor.py` | | | | | X | X (build_certify_step) | X (dispatch) | X (new step) | X (L2167 gate=None) |
| `gates.py` | | | X | | | X (via GateCriteria) | | | X (_cross_refs_resolve L48) |
| `validate_gates.py` | | | X | X | | | | | |
| `structural_checkers.py` | | | | | | | | | (preserve) |
| `convergence.py` | | | | | X | | | | (preserve) |
| `obligation_scanner.py` | | X | | | | | (candidate) | | X (return-True audit) |
| `fidelity_checker.py` | X | | | | | | | X | X (L287-303 fail-open) |
| `integration_contracts.py` | | | X | X | | | | | |
| `fingerprint.py` | | X | | | | | | | (return-True audit) |
| `prompts.py` | | | | | | | X (9 builders) | | |
| `certify_prompts.py` | | | | | | | X | | X (dead code) |
| `validate_prompts.py` | | | | | | | X | | |
| `remediate_prompts.py` | | | | | | | X | | |
| `remediate.py` | | | | | X | | X | | |
| `remediate_executor.py` | | | | | X | | (candidate) | | X (return-True audit) |
| `remediate_parser.py` | | | | | | | X (collapsed by tool-write) | | |
| `spec_parser.py` | X | | X | | | | X | | |
| `spec_patch.py` | | | | | X | | | | X (parser canonicalization) |
| `spec_structural_audit.py` | X | | | | | | | | |
| `semantic_layer.py` | | | | | X | | | | |
| `cosmetic_remediator.py` | | | | | | | (passthrough) | | |
| `models.py` | | | | | X (envelope dc) | | | | |
| `templates.py` | | | | | | | X (Jinja renderer) | | |
| `commands.py` | | | | | | | | | (preserve) |
| `__init__.py` | | | | | | | | | |
| `cli/pipeline/models.py` | | | | | (X) | X (slot add) | | | |

**Coverage:** 6 files completely untouched by R0/R1 (`structural_checkers`, `convergence`, `commands`, `__init__`, cosmetic-as-passthrough; semantic_layer envelope-only).

---

**End R1 report.** Task builder should consult this file for per-file checklist-item granularity; cross-reference Section F for which phases must list which files in their Output/Verification.
