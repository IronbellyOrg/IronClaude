# IronClaude Roadmap Pipeline -- Deep Trace

> Generated: 2026-04-03
> Source: `src/superclaude/cli/roadmap/` module tree
> Scope: Full step-by-step trace from CLI invocation through final validated output

---

## Section 1: Pipeline Overview

```
USER INVOCATION
       |
       v
[commands.py] -- CLI parsing, routing, config build
       |
       v
[executor.py::execute_roadmap()] -- orchestrator entry
       |
       +--[--dry-run?]-----> print plan, exit
       |
       +--[--resume?]------> _restore_from_state() --> _apply_resume()
       |
       v
[executor.py::_build_steps()] -- builds 12-step plan
       |
       v
[pipeline/executor.py::execute_pipeline()] -- generic sequencer
       |
       |   For each step:
       |     1. on_step_start callback
       |     2. roadmap_run_step() ----+
       |     3. gate_passed()          |
       |     4. retry if gate fails    |
       |     5. on_step_complete       |
       |     6. HALT if exhausted      |
       |                               |
       |   +---------------------------+
       |   |
       |   v
       |   Step dispatches by step.id:
       |
       |   PROGRAMMATIC (no Claude subprocess):
       |     anti-instinct  -> obligation_scanner + integration_contracts + fingerprint
       |     deviation-analysis -> deviation registry JSON aggregation
       |     remediate -> deviations_to_findings + generate_remediation_tasklist
       |     wiring-verification -> wiring_gate.run_wiring_analysis
       |     [convergence mode] spec-fidelity -> convergence engine
       |
       |   INFERENCE (Claude subprocess via ClaudeProcess):
       |     extract          -> claude -p "<extract prompt>"     -> extraction.md
       |     generate-{A}     -> claude -p "<generate prompt>"    -> roadmap-{A}.md
       |     generate-{B}     -> claude -p "<generate prompt>"    -> roadmap-{B}.md
       |     diff             -> claude -p "<diff prompt>"        -> diff-analysis.md
       |     debate           -> claude -p "<debate prompt>"      -> debate-transcript.md
       |     score            -> claude -p "<score prompt>"       -> base-selection.md
       |     merge            -> claude -p "<merge prompt>"       -> roadmap.md
       |     test-strategy    -> claude -p "<test-strat prompt>"  -> test-strategy.md
       |     spec-fidelity    -> claude -p "<fidelity prompt>"    -> spec-fidelity.md
       |     certify          -> claude -p "<certify prompt>"     -> certification-report.md
       |
       v
[executor.py::_save_state()] -- write .roadmap-state.json
       |
       +--[failures?]-----> _format_halt_output(), sys.exit(1)
       |
       +--[--no-validate?]-> skip validation, return
       |
       v
[executor.py::_auto_invoke_validate()]
       |
       v
[validate_executor.py::execute_validate()]
       |
       +-- single agent: reflect -> report
       +-- multi agent:  [reflect-A, reflect-B] parallel -> adversarial-merge -> report
       |
       v
DONE: validation-report.md written
```

---

## Section 2: Entry Point (commands.py)

**File**: `src/superclaude/cli/roadmap/commands.py`

### Subcommands

The `superclaude roadmap` command group exposes three subcommands:

| Subcommand | Line | Purpose |
|---|---|---|
| `run` | L32-256 | Execute the full roadmap generation pipeline |
| `validate` | L285-359 | Validate existing roadmap pipeline outputs |
| `accept-spec-change` | L259-282 | Update spec_hash after accepted deviation records |

### `run` Flags

| Flag | Type | Default | Purpose | Line |
|---|---|---|---|---|
| `INPUT_FILES` | positional, 1-3 paths | required | Spec, TDD, and/or PRD files | L33 |
| `--agents` | string | `None` (default: opus:architect,haiku:architect) | Comma-separated model:persona pairs | L35-40 |
| `--output` | path | parent dir of first input file | Output directory for artifacts | L42-48 |
| `--depth` | choice: quick/standard/deep | `None` (default: standard) | Debate round count | L49-54 |
| `--resume` | flag | false | Skip steps whose outputs already pass gates | L55-60 |
| `--dry-run` | flag | false | Print step plan without executing | L61-63 |
| `--model` | string | "" | Override model for all steps | L64-66 |
| `--max-turns` | int | 100 | Max turns per Claude subprocess | L67-69 |
| `--debug` | flag | false | Enable debug logging | L70-72 |
| `--no-validate` | flag | false | Skip post-pipeline validation | L73-76 |
| `--allow-regeneration` | flag | false | Allow patches exceeding diff-size threshold | L77-80 |
| `--retrospective` | path | None | Prior release cycle retrospective file | L81-93 |
| `--input-type` | choice: auto/tdd/spec | "auto" | Input file type override | L94-99 |
| `--tdd-file` | path | None | Supplementary TDD file | L100-110 |
| `--prd-file` | path | None | Supplementary PRD file | L111-122 |

### Invocation Flow (commands.py L134-256)

1. **Validate input count**: 1-3 files max (L162-166)
2. **Route input files**: `_route_input_files()` classifies each positional file as spec/tdd/prd via `detect_input_type()` and merges with explicit `--tdd-file` and `--prd-file` flags (L171-176)
3. **Detect CLI parameter sources**: checks whether `--agents` and `--depth` were explicitly provided vs defaulted (L179-185) -- this matters for `--resume` state restoration
4. **Parse agent specs**: `AgentSpec.parse()` splits "model:persona" strings (L188-191)
5. **Resolve output directory**: defaults to parent of first input file (L194)
6. **Resolve retrospective**: graceful missing-file handling (L198-206)
7. **Build RoadmapConfig**: all flags assembled into dataclass (L210-229)
8. **Call execute_roadmap()**: the main orchestration entry point (L250-256)

### `validate` Flags

| Flag | Type | Default | Purpose |
|---|---|---|---|
| `OUTPUT_DIR` | positional path | required | Directory containing pipeline outputs |
| `--agents` | string | "opus:architect" | Agent specs for validation |
| `--model` | string | "" | Override model |
| `--max-turns` | int | 100 | Max turns per subprocess |
| `--debug` | flag | false | Debug logging |

---

## Section 3: The `run` Pipeline (executor.py)

**File**: `src/superclaude/cli/roadmap/executor.py`

### Input File Routing (L63-316)

**`detect_input_type(spec_file)`** (L63-185):
- Reads file content and applies weighted scoring to classify as `prd`, `tdd`, or `spec`
- PRD scoring (checked first, threshold >= 5): frontmatter type field, 12 PRD-exclusive section headings, user story patterns, JTBD patterns, prd tags
- TDD scoring (checked second, threshold >= 5): numbered section headings count, TDD-exclusive frontmatter fields (`parent_doc`, `coordinator`), 8 TDD-specific section names, frontmatter type field
- Falls back to "spec" if neither threshold met
- Logs borderline warnings for scores 3-6

**`_route_input_files()`** (L188-316):
- Classifies each positional file via `detect_input_type()`
- Applies `--input-type` override for single-file mode only
- Validates no duplicate types (e.g., two specs)
- Requires at least one spec or TDD as primary input (PRD alone is rejected)
- Merges explicit `--tdd-file` and `--prd-file` flags with conflict detection
- Applies redundancy guard (ignores --tdd-file when primary is TDD)
- Applies same-file guard (rejects when two slots point to same file)

### execute_roadmap() (L2245-2391)

This is the main orchestration function. Step-by-step:

1. **Create output directory** (L2273)
2. **Resume state restoration** (L2276-2281): if `--resume`, calls `_restore_from_state()` to pull agents, depth, input_type, tdd_file, prd_file from `.roadmap-state.json`
3. **Apply default agents/depth** if still None (L2284-2287)
4. **Capture initial spec hash** for spec-patch cycle detection (L2293)
5. **Re-route input files** through centralized routing (L2296-2308)
6. **Build step list** via `_build_steps(config)` (L2314)
7. **--dry-run branch**: print step plan, exit (L2317-2319)
8. **--resume branch**: `_apply_resume()` checks each step's output against its gate, marks passing steps as SKIPPED (L2322-2325)
9. **Execute pipeline**: delegates to `execute_pipeline()` from `pipeline/executor.py` with `roadmap_run_step` as the step runner (L2328-2334)
10. **Save state**: writes `.roadmap-state.json` with all step results (L2337)
11. **Check failures** (L2340-2367):
    - If spec-fidelity failed: attempts spec-patch resume cycle (`_apply_resume_after_spec_patch`)
    - Otherwise: prints HALT diagnostic, exits with code 1
12. **Auto-invoke validation** unless `--no-validate` or resume already completed (L2372-2390)

### _build_steps() (L1299-1490)

Constructs the step list. Each Step has: id, prompt, output_file, gate, timeout_seconds, inputs, retry_limit, model, gate_mode.

**Step execution order** (sequential unless noted):

| # | Step ID | Type | Output File | Timeout |
|---|---|---|---|---|
| 1 | extract | Inference | extraction.md | 300s (1800s for TDD) |
| 2a | generate-{agent_a.id} | Inference (parallel) | roadmap-{agent_a.id}.md | 900s |
| 2b | generate-{agent_b.id} | Inference (parallel) | roadmap-{agent_b.id}.md | 900s |
| 3 | diff | Inference | diff-analysis.md | 300s |
| 4 | debate | Inference | debate-transcript.md | 600s |
| 5 | score | Inference | base-selection.md | 300s |
| 6 | merge | Inference | roadmap.md | 600s |
| 7 | anti-instinct | Programmatic | anti-instinct-audit.md | 30s |
| 8 | test-strategy | Inference | test-strategy.md | 300s |
| 9 | spec-fidelity | Inference (or convergence) | spec-fidelity.md | 600s |
| 10 | wiring-verification | Programmatic | wiring-verification.md | 60s |
| 11 | deviation-analysis | Programmatic | spec-deviations.md | 300s |
| 12 | remediate | Programmatic | remediation-tasklist.md | 600s |
| 13* | certify | Inference (dynamic) | certification-report.md | 300s |

*Step 13 (certify) is constructed dynamically after remediate completes, not in _build_steps().

### roadmap_run_step() (L649-828)

This is the StepRunner callback passed to `execute_pipeline()`. Dispatches by step.id:

**Programmatic dispatch (no subprocess)**:
- `anti-instinct` (L673-684): calls `_run_anti_instinct_audit(spec_file, merge_file, output_file)` directly
- `spec-fidelity` with convergence_enabled (L688-689): calls `_run_convergence_spec_fidelity()`
- `deviation-analysis` (L692-693): calls `_run_deviation_analysis()`
- `remediate` (L696-697): calls `_run_remediate_step()`
- `wiring-verification` (L699-717): calls `run_wiring_analysis()` + `emit_report()` from audit module

**Inference dispatch (Claude subprocess)** (L719-798):
1. Build semantic role labels for inline embedding (L723-731)
2. Embed all input files into prompt as fenced code blocks via `_embed_inputs()` (L732-747)
3. Create `ClaudeProcess` with composed prompt, output file, model, timeout (L749-759)
4. `proc.start()` launches subprocess (L761)
5. Poll for cancellation every 1s (L764-776)
6. `proc.wait()` collects exit code (L777)
7. Handle exit codes: 124 = timeout, non-zero = fail (L780-798)

**Post-subprocess processing** (L800-828):
- `_sanitize_output()`: strips conversational preamble before YAML frontmatter (L801)
- For extract step: `_inject_pipeline_diagnostics()` adds timing metadata + `_run_structural_audit()` warning-only hook (L804-812)
- For test-strategy step: `_inject_provenance_fields()` adds spec_source/generated/generator (L815-819)

### Inline Embedding (L330-352)

`_embed_inputs()` reads input files and returns their contents as labeled fenced code blocks. This is used instead of `--file` flags because the Claude CLI's `--file` is a cloud download mechanism, not a local file injector. Size limit is 120KB (_EMBED_SIZE_LIMIT, L324), derived from Linux MAX_ARG_STRLEN (128KB) minus template overhead (8KB).

---

## Section 4: Step Inventory

| Step # | Name | Type | Input Files | Output File | Gate | Prompt Source |
|---|---|---|---|---|---|---|
| 1 | extract | Inference | spec, [tdd], [prd] | extraction.md | EXTRACT_GATE (or EXTRACT_TDD_GATE for TDD) | `build_extract_prompt()` / `build_extract_prompt_tdd()` |
| 2a | generate-{A} | Inference (parallel) | extraction.md, [tdd], [prd] | roadmap-{A}.md | GENERATE_A_GATE | `build_generate_prompt(agent_a)` |
| 2b | generate-{B} | Inference (parallel) | extraction.md, [tdd], [prd] | roadmap-{B}.md | GENERATE_B_GATE | `build_generate_prompt(agent_b)` |
| 3 | diff | Inference | roadmap-{A}.md, roadmap-{B}.md | diff-analysis.md | DIFF_GATE | `build_diff_prompt()` |
| 4 | debate | Inference | diff-analysis.md, roadmap-{A}.md, roadmap-{B}.md | debate-transcript.md | DEBATE_GATE | `build_debate_prompt(depth)` |
| 5 | score | Inference | debate-transcript.md, roadmap-{A}.md, roadmap-{B}.md, [tdd], [prd] | base-selection.md | SCORE_GATE | `build_score_prompt()` |
| 6 | merge | Inference | base-selection.md, roadmap-{A}.md, roadmap-{B}.md, debate-transcript.md, [tdd], [prd] | roadmap.md | MERGE_GATE | `build_merge_prompt()` |
| 7 | anti-instinct | Programmatic | spec, roadmap.md | anti-instinct-audit.md | ANTI_INSTINCT_GATE | N/A (no LLM) |
| 8 | test-strategy | Inference | roadmap.md, extraction.md, [tdd], [prd] | test-strategy.md | TEST_STRATEGY_GATE | `build_test_strategy_prompt()` |
| 9 | spec-fidelity | Inference (or convergence) | spec, roadmap.md, [tdd], [prd] | spec-fidelity.md | SPEC_FIDELITY_GATE (None if convergence) | `build_spec_fidelity_prompt()` |
| 10 | wiring-verification | Programmatic | roadmap.md, spec-fidelity.md | wiring-verification.md | WIRING_GATE | N/A (no LLM, TRAILING mode) |
| 11 | deviation-analysis | Programmatic | spec-fidelity.md, roadmap.md | spec-deviations.md + .json | DEVIATION_ANALYSIS_GATE | N/A (no LLM) |
| 12 | remediate | Programmatic | spec-deviations.md, spec-fidelity.md, roadmap.md | remediation-tasklist.md + .json | REMEDIATE_GATE | N/A (no LLM) |
| 13 | certify | Inference (dynamic) | remediation-tasklist.md | certification-report.md | CERTIFY_GATE | `build_certification_prompt()` |

---

## Section 5: Gate Inventory

**File**: `src/superclaude/cli/roadmap/gates.py` (L765-1139), `src/superclaude/cli/pipeline/gates.py` (enforcement logic)

### Gate Enforcement Tiers (pipeline/gates.py L20-74)

| Tier | Checks Applied |
|---|---|
| EXEMPT | Always passes |
| LIGHT | File exists + non-empty |
| STANDARD | + min_lines + YAML frontmatter fields |
| STRICT | + semantic checks (pure Python functions on content) |

### Gate Definitions

| Gate Name | Required Frontmatter Fields | Min Lines | Tier | Semantic Checks | Defined At |
|---|---|---|---|---|---|
| EXTRACT_GATE | spec_source, generated, generator, functional_requirements, nonfunctional_requirements, total_requirements, complexity_score, complexity_class, domains_detected, risks_identified, dependencies_identified, success_criteria_count, extraction_mode | 50 | STRICT | complexity_class_valid, extraction_mode_valid | gates.py L765-795 |
| EXTRACT_TDD_GATE | (13 standard + 6 TDD: data_models_identified, api_surfaces_identified, components_identified, test_artifacts_identified, migration_items_identified, operational_items_identified) | 50 | STRICT | complexity_class_valid, extraction_mode_valid | gates.py L797-835 |
| GENERATE_A_GATE | spec_source, complexity_score, primary_persona | 100 | STRICT | frontmatter_values_non_empty, has_actionable_content | gates.py L837-853 |
| GENERATE_B_GATE | spec_source, complexity_score, primary_persona | 100 | STRICT | frontmatter_values_non_empty, has_actionable_content | gates.py L855-871 |
| DIFF_GATE | total_diff_points, shared_assumptions_count | 30 | STANDARD | (none) | gates.py L873-877 |
| DEBATE_GATE | convergence_score, rounds_completed | 50 | STRICT | convergence_score_valid (float in [0.0, 1.0]) | gates.py L879-890 |
| SCORE_GATE | base_variant, variant_scores | 20 | STANDARD | (none) | gates.py L892-896 |
| MERGE_GATE | spec_source, complexity_score, adversarial | 150 | STRICT | no_heading_gaps, cross_refs_resolve, no_duplicate_headings | gates.py L898-919 |
| TEST_STRATEGY_GATE | spec_source, generated, generator, complexity_class, validation_philosophy, validation_milestones, work_milestones, interleave_ratio, major_issue_policy | 40 | STRICT | complexity_class_valid, interleave_ratio_consistent, milestone_counts_positive, validation_philosophy_correct, major_issue_policy_correct | gates.py L921-961 |
| SPEC_FIDELITY_GATE | high_severity_count, medium_severity_count, low_severity_count, total_deviations, validation_complete, tasklist_ready | 20 | STRICT | high_severity_count_zero, tasklist_ready_consistent | gates.py L964-987 |
| ANTI_INSTINCT_GATE | undischarged_obligations, uncovered_contracts, fingerprint_coverage | 10 | STRICT | no_undischarged_obligations (==0), integration_contracts_covered (==0), fingerprint_coverage_check (>=0.7) | gates.py L1043-1068 |
| DEVIATION_ANALYSIS_GATE | schema_version, total_analyzed, slip_count, intentional_count, pre_approved_count, ambiguous_count, routing_fix_roadmap, routing_no_action, analysis_complete | 20 | STRICT | no_ambiguous_deviations (==0), validation_complete_true, routing_ids_valid (DEV-\\d+ pattern), slip_count_matches_routing, pre_approved_not_in_fix_roadmap, total_analyzed_consistent, deviation_counts_reconciled | gates.py L1070-1121 |
| REMEDIATE_GATE | type, source_report, source_report_hash, total_findings, actionable, skipped | 10 | STRICT | frontmatter_values_non_empty, all_actionable_have_status | gates.py L989-1012 |
| CERTIFY_GATE | findings_verified, findings_passed, findings_failed, certified, certification_date | 15 | STRICT | frontmatter_values_non_empty, per_finding_table_present, certified_is_true | gates.py L1014-1041 |
| WIRING_GATE | (defined in audit/wiring_gate.py) | varies | TRAILING mode | (defined in audit module) | audit/wiring_gate.py |

---

## Section 6: The `validate` Pipeline

**File**: `src/superclaude/cli/roadmap/validate_executor.py`

### Entry: execute_validate(config) (L369-end)

1. **Validate inputs exist** (L394): requires `roadmap.md`, `test-strategy.md`, `extraction.md` in output_dir
2. **Create validate/ subdirectory** (L397-398)
3. **Route by agent count** (L400+):
   - 1 agent: `_build_single_agent_steps()` -- single reflect step
   - 2+ agents: `_build_multi_agent_steps()` -- parallel reflect per agent, then adversarial merge

### Single-Agent Path (L192-215)

Produces one step:
- **reflect**: Claude subprocess validates roadmap across 7 dimensions (schema, structure, traceability, cross-file consistency, parseability, interleave, decomposition). Uses REFLECT_GATE.

### Multi-Agent Path (L218-266)

Produces two layers:
1. **Parallel reflect group**: one `reflect-{agent.id}` step per agent, all running concurrently. Each uses REFLECT_GATE.
2. **adversarial-merge**: merges all reflect reports into consolidated `validation-report.md`. Categorizes findings as BOTH_AGREE, ONLY_A, ONLY_B, CONFLICT. Uses ADVERSARIAL_MERGE_GATE.

### Validation Gates

| Gate | Required Fields | Min Lines | Tier | Semantic Checks |
|---|---|---|---|---|
| REFLECT_GATE | blocking_issues_count, warnings_count, tasklist_ready | 20 | STRICT | frontmatter_values_non_empty |
| ADVERSARIAL_MERGE_GATE | blocking_issues_count, warnings_count, tasklist_ready, validation_mode, validation_agents | 30 | STRICT | frontmatter_values_non_empty, agreement_table_present |

(Defined in `validate_gates.py` L30-69)

### validate_run_step() (L78-175)

Mirrors `roadmap_run_step()`: inline embedding of inputs, `ClaudeProcess` launch, poll for cancellation, sanitize output.

### Report Parsing (L269-315)

`_parse_report_counts()` extracts blocking/warning/info counts from the validation report frontmatter for CLI output.

---

## Section 7: Convergence Engine

**File**: `src/superclaude/cli/roadmap/convergence.py`

### Purpose

Implements deterministic fidelity convergence (FR-7) as an alternative to single-shot LLM spec-fidelity. Runs structural checkers + semantic layer + fidelity checker in a loop, with remediation between iterations, until HIGH findings reach zero or budget exhausts.

### Key Components

**Budget Constants** (L24-33):
- CHECKER_COST = 10
- REMEDIATION_COST = 8
- REGRESSION_VALIDATION_COST = 15
- CONVERGENCE_PASS_CREDIT = 5
- MAX_CONVERGENCE_BUDGET = 61 (3 full cycles)

**DeviationRegistry** (L88-200+):
- File-backed JSON registry at `deviation-registry.json`
- Tracks findings across runs with stable IDs (SHA-256 hash of dimension:rule_id:spec_location:mismatch_type)
- Status lifecycle: ACTIVE -> FIXED | FAILED | SKIPPED
- `merge_findings()`: new findings appended, known findings updated, missing findings marked FIXED
- Resets when spec_hash changes (new spec version)

**execute_fidelity_with_convergence()** (called from executor.py L955-964):
1. Initialize DeviationRegistry and TurnLedger
2. Loop up to max_runs=3:
   a. Run structural checkers (from `structural_checkers.py`)
   b. Run semantic layer (from `semantic_layer.py`)
   c. Run fidelity checker (from `fidelity_checker.py`)
   d. Merge findings into registry
   e. If HIGH count == 0: PASS, exit loop
   f. Run remediation on active HIGHs
   g. Debit budget
   h. Check for regression (handle_regression)
   i. Reimburse budget if structural HIGHs decreased
3. Write convergence report to spec-fidelity.md

### When It Runs

Only when `config.convergence_enabled = True` (currently defaults to False, L112 of models.py). Standard pipeline uses single-shot LLM spec-fidelity.

---

## Section 8: Fidelity Checking

**File**: `src/superclaude/cli/roadmap/fidelity_checker.py`

### Purpose

Verifies that spec functional requirements (FRs) have corresponding implementation evidence in the codebase. Uses exact name matching only (no NLP/fuzzy matching).

### Evidence Search Methods

1. **AST parse** of `.py` files: extracts top-level and nested function/class definitions
2. **String search fallback**: case-sensitive substring search of file contents for non-Python files or AST parse failures

### Ambiguity Policy

Fails open: ambiguous matches are reported as FOUND (not missing) to avoid false-positive gaps stalling the convergence engine.

### Integration

Called by `_run_checkers()` inside `_run_convergence_spec_fidelity()` (executor.py L906-917). Only runs in convergence mode. Returns `list[Finding]` for direct integration into the deviation registry.

### Key Classes

- **FRMapping**: maps FR ID to expected function/class names in codebase
- **FidelityResult**: per-FR check result (found/not-found/ambiguous)
- **FidelityChecker**: main class, takes source_dir and optional allowlist

---

## Section 9: Obligation Scanner

**File**: `src/superclaude/cli/roadmap/obligation_scanner.py`

### Purpose

Detects undischarged scaffolding obligations in roadmaps. A scaffolding obligation is created when the roadmap uses terms like "mock", "stub", "skeleton", "placeholder" etc. -- these create implicit promises that the temporary implementation will be replaced in a later phase.

### Algorithm (scan_obligations, L105+)

1. Pre-compute code block ranges for severity demotion
2. Split content into phase-delimited sections (H2/H3 headings)
3. For each section, find all scaffold terms (11 terms: mock, stub, skeleton, placeholder, scaffold, temporary, hardcoded, hardwired, no-op, dummy, fake)
4. For each scaffold term, extract component context (nearby text)
5. Search ALL subsequent sections for discharge terms (replace, wire up/in/into, integrate, connect, swap out/in, remove mock/stub, implement real, fill in, complete skeleton/scaffold)
6. Check for exempt comments (`# obligation-exempt`) and code-block severity demotion
7. Report undischarged obligations

### Output

`ObligationReport` dataclass:
- total_obligations: all detected
- discharged: matched with discharge term in later phase
- undischarged_count: undischarged, excluding MEDIUM severity and exempt items

### Gate Integration

Used by ANTI_INSTINCT_GATE semantic check `no_undischarged_obligations`: requires `undischarged_obligations == 0` in frontmatter.

---

## Section 10: Remediation Pipeline

### Overview

Remediation is a multi-step process triggered when spec-fidelity identifies deviations:

```
spec-fidelity.md -> deviation-analysis -> remediation-tasklist.md -> [certify]
```

### Step 11: Deviation Analysis (executor.py L1027-1174)

**`_run_deviation_analysis()`** -- programmatic, no LLM:
1. Reads `deviation-registry.json` from output directory
2. Aggregates findings by deviation_class: SLIP, INTENTIONAL, PRE_APPROVED, AMBIGUOUS
3. Builds routing lists (routing_fix_roadmap for SLIPs, routing_no_action for PRE_APPROVED)
4. Writes `spec-deviations.md` with YAML frontmatter and `spec-deviations.json` sidecar

### Step 12: Remediate (executor.py L1176-1256)

**`_run_remediate_step()`** -- programmatic, no LLM:
1. Reads `spec-deviations.json` sidecar
2. Converts to Finding objects via `deviations_to_findings()` (from remediate.py)
3. Generates remediation tasklist via `generate_remediation_tasklist()`
4. Writes `remediation-tasklist.md` and `remediation-tasklist.json` sidecar

### Remediate Module (remediate.py)

Pure functions:
- `format_validation_summary(findings)`: severity-grouped terminal summary
- `should_skip_prompt(findings)`: returns True when zero BLOCKING + WARNING
- `filter_findings(findings, scope)`: scope-based filtering with auto-SKIP logic
- `generate_remediation_tasklist(findings, source_report_path, content)`: produces checklist format with YAML frontmatter

### Remediation Budget (executor.py L1737-1775)

`_check_remediation_budget()`: reads `remediation_attempts` from `.roadmap-state.json`, max 2 attempts. When exhausted, calls `_print_terminal_halt()` with finding details and manual-fix instructions.

### Step 13: Certify (executor.py L1259-1296)

**`build_certify_step()`** -- constructs a dynamic Step:
- Prompt from `build_certification_prompt()` (certify_prompts.py)
- Inputs: remediation-tasklist.md
- Output: certification-report.md
- Gate: CERTIFY_GATE (requires `certified: true`)

The certification prompt instructs Claude to verify each remediation fix was applied correctly, outputting PASS/FAIL per finding with justification.

---

## Section 11: State Management

**File**: `src/superclaude/cli/roadmap/executor.py`

### .roadmap-state.json Structure

Written by `_save_state()` (L1834-1949) via atomic tmp + os.replace(). Schema:

```json
{
  "schema_version": 1,
  "spec_file": "/path/to/spec.md",
  "tdd_file": "/path/to/tdd.md",
  "prd_file": "/path/to/prd.md",
  "input_type": "spec",
  "spec_hash": "sha256...",
  "agents": [{"model": "opus", "persona": "architect"}, ...],
  "depth": "standard",
  "last_run": "2026-04-03T...",
  "steps": {
    "extract": {
      "status": "PASS",
      "attempt": 1,
      "output_file": "/path/to/extraction.md",
      "started_at": "...",
      "completed_at": "..."
    }
  },
  "validation": { "status": "pass" | "fail" },
  "fidelity_status": "pass" | "fail" | "skipped" | "degraded",
  "remediate": {
    "status": "...",
    "scope": "...",
    "findings_total": 0,
    "findings_actionable": 0,
    "findings_fixed": 0,
    "findings_failed": 0,
    "findings_skipped": 0,
    "agents_spawned": 0,
    "tasklist_file": "...",
    "timestamp": "..."
  },
  "certify": {
    "status": "...",
    "findings_verified": 0,
    "findings_passed": 0,
    "findings_failed": 0,
    "certified": true | false,
    "report_file": "...",
    "timestamp": "..."
  }
}
```

### Who Reads It

- `_restore_from_state()` (L2137-2242): restores agents, depth, input_type, tdd_file, prd_file on `--resume`
- `_apply_resume()`: checks gate pass status for each step to skip already-passing steps
- `_check_remediation_budget()`: reads remediation_attempts
- `_check_annotate_deviations_freshness()`: reads roadmap_hash from spec-deviations.md

### Who Writes It

- `_save_state()` (L1834-1949): writes after pipeline execution
- `write_state()` (L2099-2106): atomic write utility
- Merges with existing state: preserves validation, fidelity_status, remediate, certify keys

### Defense-in-Depth Guards

1. **No-progress guard**: skips write when no steps produced results (prevents corruption from broken resumes)
2. **Agent-mismatch guard**: preserves original agents when no generate steps ran (prevents overwriting correct agent config)

### Pipeline Status Derivation (L2068-2096)

`derive_pipeline_status(state)` maps state transitions:
- post-validate: `validated` | `validated-with-issues`
- post-remediate: `remediated`
- post-certify: `certified` | `certified-with-caveats`
- default: `pending`

---

## Section 12: Module Dependency Map

### Call Graph (who calls whom)

```
commands.py
  |-> executor._route_input_files()
  |-> executor.detect_input_type()
  |-> models.AgentSpec.parse()
  |-> models.RoadmapConfig()
  |-> executor.execute_roadmap()
        |-> executor._restore_from_state()
        |     |-> executor.read_state()
        |-> executor._build_steps()
        |     |-> prompts.build_extract_prompt() / build_extract_prompt_tdd()
        |     |-> prompts.build_generate_prompt()
        |     |-> prompts.build_diff_prompt()
        |     |-> prompts.build_debate_prompt()
        |     |-> prompts.build_score_prompt()
        |     |-> prompts.build_merge_prompt()
        |     |-> prompts.build_test_strategy_prompt()
        |     |-> prompts.build_spec_fidelity_prompt()
        |     |-> prompts.build_wiring_verification_prompt()
        |     |-> certify_prompts.build_certification_prompt()
        |     |-> gates.* (all gate constants)
        |     |-> audit.wiring_gate.WIRING_GATE
        |-> pipeline.executor.execute_pipeline()
        |     |-> executor.roadmap_run_step()  [for each step]
        |     |     |-> executor._embed_inputs()
        |     |     |-> pipeline.process.ClaudeProcess  [inference steps]
        |     |     |-> executor._run_anti_instinct_audit()
        |     |     |     |-> obligation_scanner.scan_obligations()
        |     |     |     |-> integration_contracts.extract_integration_contracts()
        |     |     |     |-> integration_contracts.check_roadmap_coverage()
        |     |     |     |-> fingerprint.check_fingerprint_coverage()
        |     |     |-> executor._run_convergence_spec_fidelity()
        |     |     |     |-> convergence.DeviationRegistry.load_or_create()
        |     |     |     |-> convergence.execute_fidelity_with_convergence()
        |     |     |     |     |-> structural_checkers.run_all_checkers()
        |     |     |     |     |-> semantic_layer.run_semantic_layer()
        |     |     |     |     |-> fidelity_checker.run_fidelity_check()
        |     |     |     |     |-> remediate_executor.execute_remediation()
        |     |     |-> executor._run_deviation_analysis()
        |     |     |-> executor._run_remediate_step()
        |     |     |     |-> remediate.deviations_to_findings()
        |     |     |     |-> remediate.generate_remediation_tasklist()
        |     |     |-> audit.wiring_gate.run_wiring_analysis()
        |     |     |-> executor._sanitize_output()
        |     |     |-> executor._inject_pipeline_diagnostics()
        |     |     |-> executor._inject_provenance_fields()
        |     |     |-> spec_structural_audit.check_extraction_adequacy()
        |     |-> pipeline.gates.gate_passed()  [for each step's gate]
        |-> executor._save_state()
        |     |-> executor.write_state()
        |-> executor._auto_invoke_validate()
              |-> validate_executor.execute_validate()
                    |-> validate_executor.validate_run_step()
                    |     |-> pipeline.process.ClaudeProcess
                    |-> pipeline.executor.execute_pipeline()
                    |-> validate_executor._parse_report_counts()
```

### Module Purpose Table

| Module | Purpose | Key Exports |
|---|---|---|
| `commands.py` | CLI entry point (Click commands) | `roadmap_group`, `run`, `validate`, `accept_spec_change` |
| `executor.py` | Pipeline orchestration, step dispatch, state management | `execute_roadmap`, `roadmap_run_step`, `_build_steps` |
| `models.py` | Data models: RoadmapConfig, AgentSpec, ValidateConfig, Finding | `RoadmapConfig`, `AgentSpec`, `ValidateConfig`, `Finding` |
| `prompts.py` | Prompt builders for inference steps (pure functions) | `build_extract_prompt`, `build_generate_prompt`, `build_diff_prompt`, `build_debate_prompt`, `build_score_prompt`, `build_merge_prompt`, `build_spec_fidelity_prompt`, `build_test_strategy_prompt`, `build_wiring_verification_prompt` |
| `gates.py` | Gate criteria constants + semantic check functions | All *_GATE constants, semantic check functions |
| `validate_executor.py` | Validation pipeline orchestration | `execute_validate`, `validate_run_step` |
| `validate_prompts.py` | Validation prompt builders | `build_reflect_prompt`, `build_merge_prompt` |
| `validate_gates.py` | Validation gate criteria | `REFLECT_GATE`, `ADVERSARIAL_MERGE_GATE` |
| `convergence.py` | Convergence engine, deviation registry | `DeviationRegistry`, `execute_fidelity_with_convergence`, `compute_stable_id` |
| `fidelity_checker.py` | Codebase evidence checking for spec FRs | `FidelityChecker`, `run_fidelity_check` |
| `obligation_scanner.py` | Scaffolding obligation detection | `scan_obligations`, `ObligationReport` |
| `fingerprint.py` | Code identifier coverage checking | `extract_code_fingerprints`, `check_fingerprint_coverage` |
| `integration_contracts.py` | Dispatch/wiring pattern detection | `extract_integration_contracts`, `check_roadmap_coverage` |
| `remediate.py` | Remediation filtering and tasklist generation | `deviations_to_findings`, `generate_remediation_tasklist`, `filter_findings` |
| `certify_prompts.py` | Certification prompt builder | `build_certification_prompt`, `extract_finding_context`, `generate_certification_report` |
| `spec_parser.py` | Spec document parsing (requirement ID extraction) | `parse_document`, `extract_requirement_ids` |
| `pipeline/executor.py` | Generic step sequencer with retry, gates, parallel dispatch | `execute_pipeline` |
| `pipeline/models.py` | Pipeline primitives: Step, StepResult, GateCriteria, etc. | `Step`, `StepResult`, `StepStatus`, `GateMode`, `GateCriteria`, `PipelineConfig` |
| `pipeline/gates.py` | Gate enforcement logic (tier-proportional) | `gate_passed` |
| `pipeline/process.py` | Claude subprocess wrapper | `ClaudeProcess` |
| `audit/wiring_gate.py` | Wiring analysis (dispatch table coverage) | `WIRING_GATE`, `run_wiring_analysis`, `emit_report` |

---

## Appendix A: Prompt Architecture

All prompts follow a consistent structure:
1. **Role assignment**: "You are a [specialist type]"
2. **Task instruction**: what to read and produce
3. **Frontmatter specification**: exact YAML fields required (these must match gate criteria)
4. **Body section requirements**: numbered markdown sections
5. **Supplementary context blocks**: TDD/PRD enrichment (conditional)
6. **Output format block**: `_OUTPUT_FORMAT_BLOCK` appended to every prompt, requiring response start with `---` frontmatter

The `_OUTPUT_FORMAT_BLOCK` (prompts.py L62-79) explicitly forbids conversational preamble before frontmatter. Despite this, `_sanitize_output()` in the executor strips any preamble that LLMs emit anyway.

## Appendix B: Parallel Execution

Steps 2a and 2b (generate-{A} and generate-{B}) run in parallel via `_run_parallel_steps()` in `pipeline/executor.py`. The parallel group is represented as a `list[Step]` within the steps list. The pipeline executor:
1. Starts all steps in the group concurrently via threads
2. If any step fails, remaining steps are cancelled
3. All results must be PASS before the next sequential step begins

## Appendix C: Resume Logic

When `--resume` is passed:
1. `_restore_from_state()` loads agents, depth, input_type, tdd_file, prd_file from `.roadmap-state.json`
2. `_apply_resume()` iterates through each step, checking if its output file passes its gate via `gate_passed()`
3. Steps whose outputs already pass are marked SKIPPED
4. Execution starts from the first step that does NOT pass its gate
5. Spec hash comparison detects spec file changes (triggers cascade re-run)
6. Agent mismatch detection preserves original agents when no generate steps ran

---

## Section 13: The 12-Step Build Plan (What `_build_steps()` Constructs)

`_build_steps()` at `executor.py:1299` constructs a list of `Step` objects that define the entire pipeline. Each step is either sequential (one Step) or parallel (a list[Step]). The pipeline executor (`pipeline/executor.py:execute_pipeline`) processes them in order.

**The 12 steps in order:**

| # | Step ID | Type | What It Does | Input | Output File | Gate |
|---|---------|------|-------------|-------|-------------|------|
| 1 | `extract` | Inference | Reads the spec/TDD/PRD and extracts structured requirements, features, constraints, risks, and open questions into a normalized extraction document | spec file (+ optional TDD, PRD) | `extraction.md` | `EXTRACT_GATE` (or `EXTRACT_TDD_GATE` for TDD input) |
| 2a | `generate-{agent_a.id}` | Inference (parallel) | Agent A (default: opus:architect) reads the extraction and produces a full roadmap variant | `extraction.md` (+ optional TDD, PRD) | `roadmap-opus-architect.md` | `GENERATE_A_GATE` |
| 2b | `generate-{agent_b.id}` | Inference (parallel) | Agent B (default: haiku:architect) reads the extraction and produces a second roadmap variant independently | `extraction.md` (+ optional TDD, PRD) | `roadmap-haiku-architect.md` | `GENERATE_B_GATE` |
| 3 | `diff` | Inference | Compares both roadmap variants and produces a structured diff analysis | both roadmap variants | `diff-analysis.md` | `DIFF_GATE` |
| 4 | `debate` | Inference | Adversarial debate over the diff — argues for/against each variant's choices, with depth controlling debate rounds (quick=1, standard=2, deep=3) | diff + both variants | `debate-transcript.md` | `DEBATE_GATE` |
| 5 | `score` | Inference | Scores the debate outcomes and selects a base variant (the "winner") with justification | debate + both variants (+ optional TDD, PRD) | `base-selection.md` | `SCORE_GATE` |
| 6 | `merge` | Inference | Produces the final merged roadmap — uses the selected base variant as foundation and incorporates best elements from the other per the debate | base selection + both variants + debate (+ optional TDD, PRD) | `roadmap.md` | `MERGE_GATE` |
| 7 | `anti-instinct` | **Programmatic** | Deterministic audit — obligation scanner checks for undischarged scaffold terms, uncovered contracts, fingerprint coverage. No LLM. | spec + merged roadmap | `anti-instinct-audit.md` | `ANTI_INSTINCT_GATE` |
| 8 | `test-strategy` | Inference | Generates a test strategy document derived from the merged roadmap and extraction | merged roadmap + extraction (+ optional TDD, PRD) | `test-strategy.md` | `TEST_STRATEGY_GATE` |
| 9 | `spec-fidelity` | Inference | Compares the spec against the merged roadmap to find deviations — severity-classified (HIGH/MEDIUM/LOW) with quoted evidence from both documents | spec + merged roadmap (+ optional TDD, PRD) | `spec-fidelity.md` | `SPEC_FIDELITY_GATE` (disabled if convergence enabled) |
| 10 | `deviation-analysis` | **Programmatic** | Deterministic aggregation of deviations from spec-fidelity. No LLM. Parses the fidelity report and structures deviations for remediation. | spec-fidelity + merged roadmap | `spec-deviations.md` | `DEVIATION_ANALYSIS_GATE` |
| 11 | `remediate` | **Programmatic** | Deterministic tasklist generation from deviations. No LLM. Produces a remediation tasklist for HIGH/MEDIUM deviations. | deviations + spec-fidelity + merged roadmap | `remediation-tasklist.md` | `REMEDIATE_GATE` |
| 12 | `certify` | Inference | Dynamically constructed after remediate. Certification report validating that remediation was applied. | remediation output + merged roadmap | `certification-report.md` | (dynamic) |

**Key design: adversarial by default.** Steps 2a/2b generate two independent roadmaps from two different LLM personas. Steps 3-5 force them into structured debate. Step 6 merges the best of both. This prevents single-model blind spots.

**3 programmatic steps** (7, 10, 11) have `prompt=""` — they are Python code, not Claude subprocesses. The executor's `roadmap_run_step()` dispatches them to Python functions instead of `ClaudeProcess`.

**Step 12 is dynamic** — constructed at runtime by `roadmap_run_step()` after step 11 completes, based on remediation output.

---

## Section 14: Roadmap Output Structure (What `roadmap.md` Contains)

The merged roadmap (`roadmap.md`) is the primary output. Its structure is defined by the merge prompt (`prompts.py:619`) and enforced by the `MERGE_GATE`. Based on actual generated roadmaps (e.g., `.dev/releases/complete/v3.1_Anti-instincts__/roadmap.md`):

### YAML Frontmatter
```yaml
---
spec_source: <original spec filename>
complexity_score: <float from extraction>
adversarial: true
---
```

### Required Sections (from merge prompt, lines 641-646)

1. **Executive Summary** — synthesized from both variants. Scope, objectives, approach, key deliverables, timeline.

2. **Phased Implementation Plan** — the core of the roadmap. Multiple phases (typically 3-6), each containing:
   - Phase goal and scope description
   - Numbered tasks (`### N.M Task Title`) with:
     - What to implement
     - Why (rationale)
     - Dependencies
     - Acceptance criteria
   - Validation gates / checkpoints at phase boundaries

3. **Risk Assessment** — merged from both variants:
   - HIGH / MEDIUM / LOW classified risks
   - Each with probability, impact, mitigation, contingency

4. **Resource Requirements** — engineering resources, new files to create, files to modify, external dependencies

5. **Success Criteria and Validation Approach** — measurable criteria, validation checkpoints, cross-cutting validation taxonomy

6. **Timeline Estimates** — phase durations, critical path, parallel opportunities

### Additional Sections (from TDD/PRD enrichment)
When `--tdd` or `--prd` is provided, the merge prompt adds instructions to:
- Preserve exact technical identifiers from the TDD (interface names, endpoint paths, component names)
- Maintain alignment with PRD personas and success metric targets
- Ensure compliance requirements are not weakened during merge

### Full Artifact Set (all files in the output directory)
| File | Step | Purpose |
|------|------|---------|
| `extraction.md` | 1 | Normalized requirements extraction |
| `roadmap-opus-architect.md` | 2a | Variant A roadmap |
| `roadmap-haiku-architect.md` | 2b | Variant B roadmap |
| `diff-analysis.md` | 3 | Structured diff between variants |
| `debate-transcript.md` | 4 | Adversarial debate |
| `base-selection.md` | 5 | Winner selection with scoring |
| `roadmap.md` | 6 | **Final merged roadmap** (primary output) |
| `anti-instinct-audit.md` | 7 | Obligation/contract coverage audit |
| `test-strategy.md` | 8 | Test strategy derived from roadmap |
| `spec-fidelity.md` | 9 | Spec-vs-roadmap deviation report |
| `spec-deviations.md` | 10 | Structured deviation records |
| `remediation-tasklist.md` | 11 | Fix tasks for deviations |
| `certification-report.md` | 12 | Remediation verification |
| `wiring-verification.md` | (trailing) | Cross-reference integrity check |
| `.roadmap-state.json` | (state) | Pipeline progress and file references |

---

## Section 15: What Happens After Roadmap — The Downstream Pipeline

The roadmap is not the end. It feeds into tasklist generation, which feeds into sprint execution. Here is the full downstream flow:

### Step A: Roadmap Validates → `.roadmap-state.json` Updated

After `execute_roadmap()` completes all 12 steps, it auto-invokes validation (`_auto_invoke_validate` at `executor.py:2390`) unless `--no-validate` is set. Validation runs the `validate` subcommand which spawns reflection + adversarial merge agents to verify the roadmap against the spec.

`.roadmap-state.json` is updated with:
- `pipeline_status`: "complete" or "failed"
- `fidelity_status`: "pass" or "fail" (from spec-fidelity step)
- File paths for spec, TDD, PRD (auto-wired for downstream consumption)
- Per-step completion timestamps and status

### Step B: Tasklist Generation (`/sc:tasklist`)

**Entry:** User runs `/sc:tasklist @roadmap.md` — this is the `sc-tasklist-protocol` inference skill. It is NOT a programmatic Python pipeline like the roadmap executor. The entire tasklist generation runs inside a single Claude session following a deterministic algorithm defined in the skill protocol (`src/superclaude/skills/sc-tasklist-protocol/SKILL.md`).

**The algorithm (Sections 4.1 through 4.8 of the protocol):**

1. **Parse roadmap items (4.1)** — splits the roadmap text at headings, bullets, numbered items. Assigns deterministic `R-NNN` IDs in appearance order (top-to-bottom). Each parsed item retains its original text and position.

2. **Determine phase buckets (4.2)** — three strategies, tried in order:
   - If the roadmap explicitly labels phases/milestones (`Phase 1`, `v2.0`, `Milestone A`): each label becomes a phase bucket in appearance order
   - Otherwise: `##` headings become phase buckets
   - If no headings: 3 defaults (Foundations, Build, Stabilize)

3. **Fix phase numbering (4.3)** — renumber sequentially with no gaps. Roadmap phases 1, 3, 5 become output phases 1, 2, 3.

4. **Convert roadmap items to tasks (4.4)** — 1 task per roadmap item by default. Split into multiple tasks ONLY for compound deliverables (component + migration, feature + test strategy, API + UI, pipeline change + app change).

5. **TDD enrichment (4.4a, conditional)** — if `--spec` flag or auto-wired from `.roadmap-state.json`: appends component implementation tasks, migration stage tasks, test suite tasks, observability metric/alert tasks, DoD verification tasks. Enriches with specific class names, endpoint paths, test case names from the TDD.

6. **PRD enrichment (4.4b, conditional)** — if `--prd-file` flag or auto-wired: enriches task descriptions with persona annotations, success metric links, priority ordering from stakeholder priorities.

7. **Task ID and ordering (4.5)**:
   - IDs: `T<PP>.<TT>` — zero-padded phase number + task number within phase
   - **Ordering rule: roadmap's top-to-bottom order is preserved within each phase**
   - **Dependency reordering: ONLY within the same phase** — if task B depends on task A and both are in Phase 2, reorder so A appears before B
   - **Cross-phase dependencies: NOT reordered** — kept in phase order. The dependency is declared in the task's `**Dependencies:** T01.03` field but the phase assignment doesn't change. This works because phases execute sequentially (Phase 1 completes entirely before Phase 2 starts).

8. **Tier classification (5.3)** — keyword matching with confidence scoring. Priority: STRICT > EXEMPT > LIGHT > STANDARD. Each task gets a tier, confidence score, and visual confidence bar.

9. **Acceptance criteria (4.7)** — 4 bullets per task with Near-Field Completion Criterion (must name a specific verifiable artifact). 1-5 deliverables. 3-8 steps with PLANNING/EXECUTION/VERIFICATION/COMPLETION phase markers.

10. **Checkpoints (4.8)** — inserted after every 5 tasks plus end-of-phase.

**What the output looks like:**

Phase files ARE the task files. There is no separate "task file" per individual task. Each `phase-N-tasklist.md` is a self-contained execution unit containing ALL tasks for that phase:

```
TASKLIST_ROOT/
  tasklist-index.md          ← metadata, traceability matrix, phase file table
  phase-1-tasklist.md        ← Phase 1 heading + goal + tasks T01.01-T01.NN + checkpoints
  phase-2-tasklist.md        ← Phase 2 heading + goal + tasks T02.01-T02.NN + checkpoints
  ...
  phase-N-tasklist.md
```

Each task within a phase file contains:
- Task heading (`### T01.02 -- Implement session-scoped audit_trail fixture`)
- Metadata table (Roadmap Item IDs, Why, Effort, Risk, Tier, Confidence, Verification Method, MCP Requirements, Dependencies, Deliverable IDs)
- Artifact paths (`TASKLIST_ROOT/artifacts/D-NNNN/`)
- Deliverables (1-5 concrete outputs)
- Steps (numbered, with `[PLANNING]`/`[EXECUTION]`/`[VERIFICATION]`/`[COMPLETION]` phase markers)
- Acceptance criteria (4 bullets)
- Validation (specific commands or checks)
- Dependencies (task IDs this task depends on)
- Rollback instructions

**Dependencies are declared, not enforced.** The `**Dependencies:** T01.01` field on a task is metadata for the reader. The sprint executor does NOT check or enforce dependencies — it iterates tasks in list order. Dependencies are respected because the generator placed them in the correct order at generation time, not because the executor validates the dependency graph at runtime.

**Auto-wiring from `.roadmap-state.json` (4.1c):** If the state file exists, the tasklist generator auto-reads `tdd_file` and `prd_file` paths from it, so the user doesn't have to re-pass `--spec` and `--prd-file` flags.
5. **Generate acceptance criteria** — 4 bullets per task with Near-Field Completion Criterion.
6. **Insert checkpoints** — every 5 tasks + end-of-phase.
7. **Auto-wire from `.roadmap-state.json`** — reads `tdd_file` and `prd_file` paths so the user doesn't re-pass flags.
8. **Enrich from TDD** (if `--spec` flag or auto-wired) — adds component-level tasks, migration tasks, test suite tasks, observability tasks.
9. **Enrich from PRD** (if `--prd-file` flag or auto-wired) — adds user story tasks, metric validation tasks, acceptance scenario tasks.

**Output:** A bundle of files:
```
TASKLIST_ROOT/
  tasklist-index.md          ← metadata, traceability matrix, phase file table
  phase-1-tasklist.md        ← Phase 1 tasks + checkpoints
  phase-2-tasklist.md        ← Phase 2 tasks + checkpoints
  ...
  phase-N-tasklist.md
```

**Validation:** The tasklist skill auto-validates against the source roadmap after generation (Stages 7-10 of the protocol). `superclaude tasklist validate` can also run standalone, producing a `tasklist-fidelity.md` report.

### Step C: Sprint Execution (`superclaude sprint run`)

**Entry:** `superclaude sprint run <tasklist-index.md>` — this IS the programmatic Python executor (`src/superclaude/cli/sprint/executor.py`).

**Yes, the sprint executor executes the phase files.** Each `phase-N-tasklist.md` IS the input unit. The executor reads each phase file, parses it into tasks, and runs them.

**Execution flow:**

1. **Phase discovery** (`config.py:discover_phases`) — regex scans the index file for `phase-N-tasklist.md` filenames. Also reads the optional "Execution Mode" column from the index's phase table (`claude`, `python`, or `skip`).

2. **Fidelity gate** — reads `.roadmap-state.json` for `fidelity_status`. If `"fail"`, blocks execution unless `--force-fidelity-fail` is passed.

3. **Per-phase loop** (`executor.py:execute_sprint`, line 1178) — iterates phases in numerical order (Phase 1 → Phase 2 → ... → Phase N):
   - **Parse the phase file** — `_parse_phase_tasks()` reads the file, regex matches `### T<PP>.<TT>` headings, extracts `TaskEntry` structs (task_id, title, description from Deliverables, dependencies, tier)
   - **Per-task subprocess loop** (`execute_phase_tasks`, line 912) — iterates tasks in **list order** (the order they appear in the file). For each task:
     - Budget check (TurnLedger)
     - Spawn `claude -p` subprocess with a 3-line prompt (task ID, title, description, phase file path)
     - Block until subprocess exits
     - Map exit code: 0→PASS, 124→INCOMPLETE, other→FAIL
     - Run wiring hook (structural code analysis)
     - Run anti-instinct hook (format validation)
   - **Phase pass/fail** = `all(r.status == TaskStatus.PASS for r in task_results)`

4. **Phase failure = sprint halt** — diagnostics collected (`DiagnosticCollector`), sprint outcome set to HALTED. Resume via `--start N` to skip completed phases.

5. **Post-sprint** — KPI report (`gate-kpi-report.md`), execution log, desktop notification.

**Critical: dependencies are NOT enforced at runtime.** The executor iterates tasks in list order. If the tasklist generator ordered T01.01 before T01.02 because T01.02 depends on T01.01, that ordering is respected — but only because the file has them in that order, not because the executor checks the `**Dependencies:**` field. The executor doesn't read the dependency field at all (it's parsed into `TaskEntry.dependencies` but never consulted during execution).

**Cross-phase dependencies are inherently satisfied** because Phase N completes entirely before Phase N+1 starts. If T02.03 depends on T01.05, T01.05 will have already executed (and passed, or the sprint would have halted).

(See the sprint task execution research report at `.dev/tasks/to-do/TASK-RESEARCH-20260403-sprint-task-exec/RESEARCH-REPORT-sprint-task-execution.md` for the detailed per-task execution trace and known gaps.)

### Step D: Feedback Loop — Roadmap Update After Sprint Progress

**This loop does not currently exist as a programmatic pipeline.** There is no `superclaude roadmap update` command. The designed feedback mechanisms are:

1. **Retrospective file** — `execute_roadmap()` accepts `--retrospective <file>` (via `config.retrospective_file`). If provided, the extraction step receives it as additional context. This is the intended mechanism for feeding sprint outcomes back into a roadmap regeneration. But it requires manual creation of the retrospective file.

2. **`.roadmap-state.json` as state bridge** — the state file tracks which pipeline steps completed and links to spec/TDD/PRD files. The tasklist generator reads from it (auto-wiring). But the sprint executor does NOT write back to it — sprint outcomes don't update the roadmap state.

3. **`--resume` for incremental update** — if the spec changes after a roadmap was generated, `superclaude roadmap run --resume` detects the spec hash change and re-runs from the first invalidated step. But this is triggered by spec changes, not sprint outcomes.

**The gap:** There is no automated loop from sprint completion → roadmap update. To close this loop, you would need:
- Sprint executor writes a completion report (phases completed, tasks passed/failed, deviations found)
- A new command or step consumes this report as a retrospective
- `superclaude roadmap run --resume --retrospective <sprint-report>` regenerates the roadmap incorporating lessons learned
- The updated roadmap feeds into a new tasklist generation cycle

This is the "continuous refinement" loop that the pipeline architecture supports structurally but does not implement end-to-end.
