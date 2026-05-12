# Research Notes: Roadmap & Tasklist Generation Architecture Overhaul

**Date:** 2026-04-04
**Scenario:** A (explicit request with detailed investigation areas, specific files, and output expectations)
**Depth Tier:** Deep

---

## EXISTING_FILES

### Roadmap CLI (`src/superclaude/cli/roadmap/`) — 5,470 lines total

| File | Lines | Purpose | Key Exports |
|------|-------|---------|-------------|
| `executor.py` | 2,897 | Pipeline orchestration — `_build_steps()`, `roadmap_run_step()`, `execute_roadmap()`, input routing, state management, convergence, deviation analysis, remediation | `execute_roadmap`, `detect_input_type`, `_route_input_files`, `_build_steps`, `roadmap_run_step`, `_run_convergence_spec_fidelity`, `_run_deviation_analysis`, `_run_remediate_step`, `apply_decomposition_pass` |
| `prompts.py` | 942 | ALL prompt-building functions for pipeline steps | `build_extract_prompt`, `build_extract_prompt_tdd`, `build_generate_prompt`, `build_diff_prompt`, `build_debate_prompt`, `build_score_prompt`, `build_merge_prompt`, `build_spec_fidelity_prompt`, `build_wiring_verification_prompt`, `build_test_strategy_prompt` |
| `commands.py` | 359 | CLI entry point — click commands, argument parsing | `roadmap_group` (click group) |
| `models.py` | 133 | Data models — `RoadmapConfig`, `AgentSpec`, `Finding`, `ValidateConfig` | `RoadmapConfig`, `AgentSpec`, `Finding`, `ValidateConfig` |
| `gates.py` | 1,139 | 15 gate constants + 31 checker functions | `EXTRACT_GATE`, `EXTRACT_TDD_GATE`, `GENERATE_A_GATE`, `GENERATE_B_GATE`, `DIFF_GATE`, `DEBATE_GATE`, `SCORE_GATE`, `MERGE_GATE`, `TEST_STRATEGY_GATE`, `SPEC_FIDELITY_GATE`, `REMEDIATE_GATE`, `CERTIFY_GATE`, `ANTI_INSTINCT_GATE`, `DEVIATION_ANALYSIS_GATE`, `ALL_GATES` |

Additional roadmap files (not directly in the research prompt's scope but relevant):
| File | Lines | Purpose |
|------|-------|---------|
| `convergence.py` | ? | Convergence logic for spec fidelity |
| `fingerprint.py` | ? | Roadmap fingerprinting |
| `remediate.py` | ? | Remediation step logic |
| `remediate_executor.py` | ? | Remediation execution |
| `remediate_parser.py` | ? | Remediation output parsing |
| `remediate_prompts.py` | ? | Remediation prompt building |
| `semantic_layer.py` | ? | Semantic analysis |
| `spec_parser.py` | ? | Spec parsing |
| `spec_patch.py` | ? | Spec patching |
| `spec_structural_audit.py` | ? | Structural auditing |
| `structural_checkers.py` | ? | Structural validation |
| `validate_executor.py` | ? | Validation pipeline executor |
| `validate_gates.py` | ? | Validation-specific gates |
| `validate_prompts.py` | ? | Validation prompt building |
| `fidelity_checker.py` | ? | Fidelity checking |
| `obligation_scanner.py` | ? | Obligation scanning |
| `integration_contracts.py` | ? | Integration contract checking |
| `certify_prompts.py` | ? | Certification prompt building |

### Pipeline Framework (`src/superclaude/cli/pipeline/`) — 861 lines (core files)

| File | Lines | Purpose | Key Exports |
|------|-------|---------|-------------|
| `executor.py` | 364 | Generic pipeline executor — `execute_pipeline()`, parallel step support | `execute_pipeline`, `_execute_single_step`, `_run_parallel_steps`, `StepRunner` |
| `process.py` | 202 | `ClaudeProcess` subprocess wrapper — builds `claude` CLI commands, captures stdout | `ClaudeProcess` (with `build_command`, `build_env`, `start`, `wait`, `terminate`) |
| `models.py` | 179 | Core data models | `StepStatus`, `GateMode`, `SemanticCheck`, `GateCriteria`, `Step`, `StepResult`, `DeliverableKind`, `Deliverable`, `PipelineConfig` |
| `gates.py` | 116 | Generic gate checker — `gate_passed()`, frontmatter regex | `gate_passed`, `_check_frontmatter` |
| `trailing_gate.py` | 633 | Trailing gate implementation | (detailed trailing gate logic) |

Additional pipeline files (not core but potentially relevant):
- `combined_m2_pass.py`, `conflict_detector.py`, `contract_extractor.py`, `dataflow_graph.py`, `dataflow_pass.py`, `deliverables.py`, `diagnostic_chain.py`, `fmea_classifier.py`, `fmea_domains.py`, `fmea_promotion.py`, `guard_analyzer.py`, `guard_pass.py`, `guard_resolution.py`, `invariant_pass.py`, `invariants.py`, `mutation_inventory.py`, `state_detector.py`, `verification_emitter.py`

### Tasklist CLI (`src/superclaude/cli/tasklist/`) — 738 lines total

| File | Lines | Purpose | Key Exports |
|------|-------|---------|-------------|
| `executor.py` | 273 | Tasklist validation executor | `execute_tasklist_validate`, `_build_steps`, `tasklist_run_step` |
| `prompts.py` | 237 | Tasklist prompt builders | `build_tasklist_generate_prompt`, `build_tasklist_fidelity_prompt` |
| `commands.py` | 185 | CLI entry point | `tasklist_group`, `validate` |
| `gates.py` | 43 | Tasklist gate | `TASKLIST_FIDELITY_GATE` |
| `models.py` | ? | Tasklist models | ? |

### Reference Templates

| File | Purpose |
|------|---------|
| `src/superclaude/examples/tdd_template.md` | TDD template (~1300 lines, 28 sections) — reference for output template design |
| `src/superclaude/examples/release-spec-template.md` | Spec template — reference |
| `src/superclaude/examples/prd_template.md` | PRD template — reference |
| `.claude/templates/workflow/02_mdtm_template_complex_task.md` | MDTM complex task template (PART 1/PART 2 pattern) |

### Prior Research (from `TASK-RESEARCH-20260403-tasklist-quality`)

| File | Purpose |
|------|---------|
| `RESEARCH-REPORT-tasklist-quality.md` | Full research report on task count regression |
| `reviews/pipeline-trace-investigation.md` | Pipeline trace showing where granularity is lost |
| `reviews/r-item-collapse-investigation.md` | R-item investigation showing 1:1 mapping |
| `research/01-protocol-diff.md` through `06-context-analysis.md` | 6 codebase research files |
| `synthesis/synth-01` through `synth-03` | 3 synthesis files |

### Issue Documentation

| File | Purpose |
|------|---------|
| `.dev/tasks/to-do/ISSUE-pipeline-one-shot-output.md` | Issue doc on one-shot architecture problem |

---

## PATTERNS_AND_CONVENTIONS

1. **Pipeline step pattern**: Steps are defined as `Step` dataclass instances in `_build_steps()`, each with: `id`, `prompt_fn`, `inputs`, `output`, `gate`, `timeout`, `max_retries`, `parallel_group` (optional).

2. **Prompt function pattern**: Each step has a corresponding `build_X_prompt()` function in `prompts.py` that takes input file contents and returns a prompt string.

3. **Gate pattern**: Each step has a `GateCriteria` object defining frontmatter fields to check and semantic checks (custom functions) to run. Gates are defined as module-level constants in `gates.py`.

4. **Execution pattern**: `execute_roadmap()` → `_build_steps()` → `execute_pipeline()` → per-step: `roadmap_run_step()` → `ClaudeProcess` subprocess.

5. **ClaudeProcess pattern**: Wraps `claude --print --output-format text` subprocess calls. Output is captured from stdout to the step's output file.

6. **Input routing pattern**: `detect_input_type()` and `_route_input_files()` classify input files and build a `RoadmapConfig` with typed input paths.

7. **Parallel execution**: Some steps can run in parallel via `parallel_group` field on `Step`. The pipeline executor handles this via `_run_parallel_steps()`.

8. **State management**: `_save_state()` / `read_state()` persist pipeline state to a JSON file for resume capability.

9. **Convergence pattern**: `_run_convergence_spec_fidelity()` runs structural checkers + obligation scanner + fidelity checker as a compound step.

---

## SOLUTION_RESEARCH

The research prompt identifies three structural failures requiring architectural changes:

1. **Extraction destroys granularity** → Solution: bypass extraction for structured inputs (TDD/PRD), feed document directly to generate step
2. **One-shot output architecture** → Solution: incremental writing mechanism (subprocess writes to disk section-by-section)
3. **No output templates** → Solution: template files that define output structure

Approaches to evaluate:
- **Template-driven generation**: Create roadmap and tasklist output template files (similar to TDD/PRD templates) that define the expected structure
- **Incremental writing**: Explore `claude --print` limitations vs tool-use mode where the subprocess can use Write/Edit tools
- **Direct input consumption**: Modify the pipeline to skip extraction for TDD/PRD inputs and pass the full document to generate
- **Hybrid approach**: Keep extraction for unstructured specs, bypass for structured TDD/PRD

External research needed:
- Claude CLI `--output-format` options and behavior (stream-json, text, etc.)
- Claude model output token limits by model tier
- Whether `claude --print` supports continuation or multi-turn output

---

## RECOMMENDED_OUTPUTS

### Research Files (Phase 2)
| File | Topic | Agent Type |
|------|-------|-----------|
| `research/01-pipeline-step-map.md` | Complete pipeline step trace from CLI to output | Code Tracer |
| `research/02-input-routing.md` | Input routing, auto-detection, type propagation | Code Tracer |
| `research/03-prompt-architecture.md` | Every prompt function — format, granularity impact | Code Tracer |
| `research/04-claude-process-output.md` | ClaudeProcess, output capture, token limits, incremental options | Code Tracer + Architecture Analyst |
| `research/05-gate-architecture.md` | All gates, what they check, what needs to change | Code Tracer |
| `research/06-tasklist-pipeline.md` | Tasklist generation from CLI to output, skill relationship | Code Tracer |
| `research/07-template-patterns.md` | Existing template patterns (TDD, PRD, MDTM) for output template design | Pattern Investigator |
| `research/08-prior-research-context.md` | Key findings from prior tasklist-quality research | Doc Analyst |

### Web Research Files (Phase 4)
| File | Topic |
|------|-------|
| `research/web-01-claude-cli-output.md` | Claude CLI output modes, streaming, tool-use, token limits |
| `research/web-02-incremental-generation.md` | Patterns for incremental LLM output to disk |

### Synthesis Files (Phase 5)
| File | Report Sections | Source Research |
|------|----------------|----------------|
| `synthesis/synth-01-problem-current-state.md` | S1 Problem Statement, S2 Current State Analysis | 01, 02, 03, 04, 05, 06, 08 |
| `synthesis/synth-02-target-gaps.md` | S3 Target State, S4 Gap Analysis | All research files |
| `synthesis/synth-03-external-findings.md` | S5 External Research Findings | web-01, web-02 |
| `synthesis/synth-04-options-recommendation.md` | S6 Options Analysis, S7 Recommendation | All research + web files |
| `synthesis/synth-05-implementation-plan.md` | S8 Implementation Plan | All research files (especially 01-06) |
| `synthesis/synth-06-questions-evidence.md` | S9 Open Questions, S10 Evidence Trail | All gaps, all file paths |

### Final Report
`RESEARCH-REPORT-roadmap-tasklist-overhaul.md`

---

## SUGGESTED_PHASES

### Phase 2: Deep Investigation (8 parallel agents)

**Agent 1 — Pipeline Step Map (Code Tracer)**
- Topic: Complete pipeline step trace from CLI invocation to output
- Files: `executor.py` (focus on `_build_steps()`, `roadmap_run_step()`, `execute_roadmap()`), `commands.py`, `pipeline/executor.py`
- Output: `research/01-pipeline-step-map.md`
- Deliverable: Table of all 13+ pipeline steps with: id, prompt function, inputs, output file, gate, timeout, retries, parallel group, sequential/parallel

**Agent 2 — Input Routing (Code Tracer)**
- Topic: Input routing and auto-detection mechanics
- Files: `executor.py` (focus on `detect_input_type()`, `_route_input_files()`, `_embed_inputs()`), `commands.py`, `models.py`
- Output: `research/02-input-routing.md`
- Deliverable: How files get classified, what changes per input_type, how type propagates through steps

**Agent 3 — Prompt Architecture (Code Tracer)**
- Topic: Every prompt-building function's format, granularity impact, template usage
- Files: `prompts.py` (ALL functions), constants `_DEPTH_INSTRUCTIONS`, `_INTEGRATION_ENUMERATION_BLOCK`, `_INTEGRATION_WIRING_DIMENSION`, `_OUTPUT_FORMAT_BLOCK`
- Output: `research/03-prompt-architecture.md`
- Deliverable: Per-prompt: what format it requests, tables vs prose, minimum counts, template references, granularity preservation/destruction

**Agent 4 — ClaudeProcess and Output Mechanism (Code Tracer + Architecture Analyst)**
- Topic: How each step executes and captures output, token limits, incremental options
- Files: `pipeline/process.py` (full `ClaudeProcess` class), `pipeline/executor.py` (`_execute_single_step`)
- Output: `research/04-claude-process-output.md`
- Deliverable: Output capture mechanism, --output-format behavior, --max-turns, token limit handling, incremental writing feasibility

**Agent 5 — Gate Architecture (Code Tracer)**
- Topic: All gate definitions, what they check, change requirements
- Files: `roadmap/gates.py` (all 15 constants + 31 functions), `pipeline/gates.py`, `pipeline/models.py` (GateMode, GateCriteria), `pipeline/trailing_gate.py`
- Output: `research/05-gate-architecture.md`
- Deliverable: Per-gate: what it checks, GateMode (BLOCKING vs TRAILING), which gates break if output format changes

**Agent 6 — Tasklist Pipeline (Code Tracer)**
- Topic: Tasklist generation end-to-end, CLI vs skill, R-item parsing
- Files: `tasklist/executor.py`, `tasklist/prompts.py`, `tasklist/commands.py`, `tasklist/gates.py`
- Output: `research/06-tasklist-pipeline.md`
- Deliverable: Full tasklist pipeline trace, relationship between CLI and skill, how R-items are parsed

**Agent 7 — Template Patterns (Pattern Investigator)**
- Topic: Existing template patterns for output template design
- Files: `src/superclaude/examples/tdd_template.md`, `src/superclaude/examples/release-spec-template.md`, `src/superclaude/examples/prd_template.md`, `.claude/templates/workflow/02_mdtm_template_complex_task.md`
- Output: `research/07-template-patterns.md`
- Deliverable: Template structure patterns, PART 1/PART 2 pattern analysis, what roadmap/tasklist templates should contain

**Agent 8 — Prior Research Context (Doc Analyst)**
- Topic: Key findings from prior tasklist-quality research
- Files: `.dev/tasks/to-do/TASK-RESEARCH-20260403-tasklist-quality/RESEARCH-REPORT-tasklist-quality.md`, `reviews/pipeline-trace-investigation.md`, `reviews/r-item-collapse-investigation.md`
- Output: `research/08-prior-research-context.md`
- Deliverable: Distilled findings from prior research, confirmed granularity loss points, validated root causes. ALL architectural claims must be tagged [CODE-VERIFIED/CODE-CONTRADICTED/UNVERIFIED].

### Phase 3: Research Completeness Verification (2 parallel agents)
- rf-analyst (completeness-verification) → `qa/analyst-completeness-report.md`
- rf-qa (research-gate) → `qa/qa-research-gate-report.md`

### Phase 4: Web Research (2 parallel agents)

**Web Agent 1 — Claude CLI Output Modes**
- Topic: Claude CLI `--output-format` options (text, json, stream-json), tool-use mode, `--max-turns`, output token limits by model
- Context: Our pipeline uses `claude --print --output-format text`. We need to understand if incremental writing is possible.
- Output: `research/web-01-claude-cli-output.md`

**Web Agent 2 — Incremental LLM Generation Patterns**
- Topic: Patterns for LLM-based incremental file writing, template-driven generation, multi-turn output
- Context: We have a pipeline where each step produces a large markdown output. Currently one-shot. Need incremental.
- Output: `research/web-02-incremental-generation.md`

### Phase 5: Synthesis (6 parallel synth agents)
See RECOMMENDED_OUTPUTS above for synth file mapping.

### Phase 6: Assembly & Validation
- rf-assembler → `RESEARCH-REPORT-roadmap-tasklist-overhaul.md`
- rf-qa (report-validation) → `qa/qa-report-validation.md`
- rf-qa-qualitative (report-qualitative) → `qa/qa-qualitative-review.md`

---

## TEMPLATE_NOTES

Use Template 02 (Complex Task). This investigation involves:
- Discovery phase (Phase 2) with 8 parallel agents
- QA gates (Phases 3 and 5)
- Web research (Phase 4)
- Synthesis (Phase 5)
- Assembly with validation (Phase 6)

Template file: `.claude/templates/workflow/02_mdtm_template_complex_task.md`

---

## AMBIGUITIES_FOR_USER

None — intent is clear from the request and codebase context. The research prompt provides explicit investigation areas, specific files, and desired output format. The "WHY" section clearly explains the three structural failures motivating this investigation. The output section specifies exactly what the report should contain.
