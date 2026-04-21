# Research: Pipeline Step Map

**Investigation type:** Code Tracer
**Scope:** executor.py, commands.py, pipeline/executor.py
**Status:** Complete
**Date:** 2026-04-04

---

## 1. CLI Entry Point: `commands.py`

**File:** `src/superclaude/cli/roadmap/commands.py`

### `roadmap_group` (line 14)
Click group `@click.group("roadmap")` defining `superclaude roadmap` command family.

### `run` command (line 32)
Click command `@roadmap_group.command()` — the primary entry point.

**Arguments:**
- `input_files` — 1-3 positional Path arguments (spec, TDD, PRD in any order)

**Options (all optional):**
| Option | Type | Default | Purpose |
|---|---|---|---|
| `--agents` | str | None | Comma-separated `model[:persona]` specs |
| `--output` | Path | input_files[0].parent | Output directory |
| `--depth` | Choice[quick,standard,deep] | None (defaults in config) | Debate round depth |
| `--resume` | flag | False | Skip steps whose outputs pass gates |
| `--dry-run` | flag | False | Print plan, exit |
| `--model` | str | "" | Override model for all steps |
| `--max-turns` | int | 100 | Max agent turns per subprocess |
| `--debug` | flag | False | Enable debug logging |
| `--no-validate` | flag | False | Skip post-pipeline validation |
| `--allow-regeneration` | flag | False | Allow patches exceeding diff-size threshold |
| `--retrospective` | Path | None | Prior release cycle retrospective file |
| `--input-type` | Choice[auto,tdd,spec] | "auto" | Force input file type detection |
| `--tdd-file` | Path | None | Supplementary TDD for technical context |
| `--prd-file` | Path | None | Supplementary PRD for business context |

**Flow (lines 162-256):**
1. Validates input_files count (max 3)
2. Calls `_route_input_files()` to classify positional files + explicit flags into spec/tdd/prd slots
3. Detects whether `--agents` and `--depth` were explicitly provided via `ctx.get_parameter_source()`
4. Parses `AgentSpec` list from `--agents` string (if provided)
5. Resolves output directory (explicit or input file's parent)
6. Resolves retrospective file (missing = warning, not error)
7. Builds `config_kwargs` dict — only includes agents/depth when explicitly provided
8. Constructs `RoadmapConfig(**config_kwargs)`
9. Prints routing info to stderr
10. Warns about TDD deviation-analysis incompatibility
11. Calls `execute_roadmap(config, resume, no_validate, agents_explicit, depth_explicit)`

### `validate` command (line 311)
Separate subcommand `superclaude roadmap validate OUTPUT_DIR` — runs validation on existing pipeline outputs. Not part of the main pipeline trace.

### `accept-spec-change` command (line 259)
Updates spec_hash in state after accepted deviation records. Utility command.

---

## 2. Input Routing: `_route_input_files()`

**File:** `src/superclaude/cli/roadmap/executor.py`, lines 188-316

Routes N positional files + explicit `--tdd-file`/`--prd-file` flags into pipeline slots.

**Algorithm:**
1. Validate count (1-3 files)
2. Classify each file via `detect_input_type()` (returns "prd", "tdd", or "spec")
3. Apply `--input-type` override for single-file mode only
4. Validate no duplicate types
5. Validate at least one spec or TDD as primary input (PRD alone is rejected)
6. Assign slots: spec_file, tdd_file, prd_file
7. Merge explicit `--tdd-file`/`--prd-file` (conflict detection)
8. Determine resolved `input_type` ("spec" or "tdd")
9. Redundancy guard: if primary is TDD, supplementary tdd_file is nulled
10. Same-file guard: no two slots can reference the same file

**Returns:** `{"spec_file": Path, "tdd_file": Path|None, "prd_file": Path|None, "input_type": str}`

### `detect_input_type()` (lines 63-185)
Multi-signal weighted scoring detector:
- **PRD** (threshold >= 5): frontmatter type field (+3), 12 section headings (+1 each), user story pattern (+2), JTBD pattern (+2), prd tag (+2)
- **TDD** (threshold >= 5): numbered headings count, exclusive frontmatter fields, TDD-specific sections, type field
- **Default:** "spec"

---

## 3. Orchestrator: `execute_roadmap()`

**File:** `src/superclaude/cli/roadmap/executor.py`, lines 2245-2391

### Flow:
1. `config.output_dir.mkdir(parents=True, exist_ok=True)` — ensure output dir
2. **Resume restore:** If `--resume`, calls `_restore_from_state()` to restore agents/depth/input_type/tdd_file/prd_file from `.roadmap-state.json`
3. **Apply defaults:** If agents still None: `[opus:architect, haiku:architect]`. If depth still None: `"standard"`
4. Capture `initial_spec_hash` for spec-patch cycle detection
5. Re-route input files through `_route_input_files()` (ensures consistent routing)
6. **Build steps:** `steps = _build_steps(config)` — returns list of Step/list[Step]
7. **Dry-run check:** If `config.dry_run`, calls `_dry_run_output(steps)` and returns
8. **Resume filter:** If `--resume`, calls `_apply_resume(steps, config, gate_passed)` to prune passing steps
9. **Execute:** `results = execute_pipeline(steps, config, roadmap_run_step, ...)`
10. **Save state:** `_save_state(config, results)`
11. **Failure handling:** If any FAIL/TIMEOUT:
    - If spec-fidelity failed: attempt `_apply_resume_after_spec_patch()` (single cycle)
    - Otherwise: format halt output, `sys.exit(1)`
12. **Success path:** Print completion, then auto-invoke validation unless `--no-validate`

---

## 4. Step Builder: `_build_steps()`

**File:** `src/superclaude/cli/roadmap/executor.py`, lines 1299-1490

Returns `list[Step | list[Step]]` — 12 steps (13 with dynamic certify), including one parallel group.

**Agent resolution:**
- `agent_a = config.agents[0]`
- `agent_b = config.agents[1] if len > 1 else config.agents[0]` (single-agent mode = same agent twice)

**Output file naming:**
All outputs under `config.output_dir`:
- `extraction.md`, `roadmap-{agent_a.id}.md`, `roadmap-{agent_b.id}.md`
- `diff-analysis.md`, `debate-transcript.md`, `base-selection.md`
- `roadmap.md` (merged), `test-strategy.md`, `spec-fidelity.md`
- `anti-instinct-audit.md`, `wiring-verification.md`
- `spec-deviations.md`, `remediation-tasklist.md`, `certification-report.md`

**Retrospective loading:** If `config.retrospective_file` exists and is a file, its content is read and passed to `build_extract_prompt()`.

---

## 5. Complete Pipeline Step Table

| # | Step ID | Prompt Function | Inputs | Output File | Gate | Tier | Timeout | Retries | Parallel Group | Seq/Par | Execution Type |
|---|---------|----------------|--------|-------------|------|------|---------|---------|----------------|---------|----------------|
| 1 | `extract` | `build_extract_prompt()` or `build_extract_prompt_tdd()` (based on input_type) | spec_file [+ tdd_file] [+ prd_file] | `extraction.md` | `EXTRACT_GATE` or `EXTRACT_TDD_GATE` | STRICT | 300s (spec) / 1800s (tdd) | 1 | — | Sequential | Claude subprocess |
| 2a | `generate-{agent_a.id}` | `build_generate_prompt(agent_a, extraction)` | extraction.md [+ tdd_file] [+ prd_file] | `roadmap-{agent_a.id}.md` | `GENERATE_A_GATE` | STRICT | 900s | 1 | Group 1 | Parallel | Claude subprocess |
| 2b | `generate-{agent_b.id}` | `build_generate_prompt(agent_b, extraction)` | extraction.md [+ tdd_file] [+ prd_file] | `roadmap-{agent_b.id}.md` | `GENERATE_B_GATE` | STRICT | 900s | 1 | Group 1 | Parallel | Claude subprocess |
| 3 | `diff` | `build_diff_prompt(roadmap_a, roadmap_b)` | roadmap_a, roadmap_b | `diff-analysis.md` | `DIFF_GATE` | STANDARD | 300s | 1 | — | Sequential | Claude subprocess |
| 4 | `debate` | `build_debate_prompt(diff, roadmap_a, roadmap_b, depth)` | diff, roadmap_a, roadmap_b | `debate-transcript.md` | `DEBATE_GATE` | STRICT | 600s | 1 | — | Sequential | Claude subprocess |
| 5 | `score` | `build_score_prompt(debate, roadmap_a, roadmap_b)` | debate, roadmap_a, roadmap_b [+ tdd_file] [+ prd_file] | `base-selection.md` | `SCORE_GATE` | STANDARD | 300s | 1 | — | Sequential | Claude subprocess |
| 6 | `merge` | `build_merge_prompt(score, roadmap_a, roadmap_b, debate)` | score, roadmap_a, roadmap_b, debate [+ tdd_file] [+ prd_file] | `roadmap.md` | `MERGE_GATE` | STRICT | 600s | 1 | — | Sequential | Claude subprocess |
| 7 | `anti-instinct` | (none — prompt is empty string) | spec_file, roadmap.md | `anti-instinct-audit.md` | `ANTI_INSTINCT_GATE` | STRICT | 30s | 0 | — | Sequential | **Deterministic** (obligation scanner + integration contracts + fingerprint) |
| 8 | `test-strategy` | `build_test_strategy_prompt(merge, extraction)` | merge, extraction [+ tdd_file] [+ prd_file] | `test-strategy.md` | `TEST_STRATEGY_GATE` | STRICT | 300s | 1 | — | Sequential | Claude subprocess |
| 9 | `spec-fidelity` | `build_spec_fidelity_prompt(spec_file, merge)` | spec_file, merge [+ tdd_file] [+ prd_file] | `spec-fidelity.md` | `SPEC_FIDELITY_GATE` (None if convergence_enabled) | STRICT | 600s | 1 | — | Sequential | Claude subprocess (or convergence engine if enabled) |
| 10 | `wiring-verification` | `build_wiring_verification_prompt(merge, spec_name)` | merge, spec-fidelity.md | `wiring-verification.md` | `WIRING_GATE` | (imported from audit) | 60s | 0 | — | Sequential | **Deterministic** (static analysis), **TRAILING** gate mode |
| 11 | `deviation-analysis` | (none — prompt is empty string) | spec-fidelity.md, merge | `spec-deviations.md` | `DEVIATION_ANALYSIS_GATE` | STRICT | 300s | 0 | — | Sequential | **Deterministic** (reads deviation-registry.json) |
| 12 | `remediate` | (none — prompt is empty string) | deviation file, spec-fidelity.md, merge | `remediation-tasklist.md` | `REMEDIATE_GATE` | STRICT | 600s | 0 | — | Sequential | **Deterministic** (deviations_to_findings + generate_remediation_tasklist) |
| 13* | `certify` | `build_certification_prompt(findings, context_sections)` | remediation-tasklist.md | `certification-report.md` | `CERTIFY_GATE` | STRICT | 300s | 1 | — | Sequential | Claude subprocess (dynamic, built by `build_certify_step()`) |

**Note on step 13 (certify):** This step is NOT in `_build_steps()`. It is described as "constructed dynamically by roadmap_run_step after remediate" (comment at line 1487). The `build_certify_step()` function (line 1259) exists to construct it, but the dynamic injection mechanism in the main pipeline flow was not found in `execute_roadmap()` — this may be invoked externally or deferred to a future version.

---

## 6. Step Runner: `roadmap_run_step()`

**File:** `src/superclaude/cli/roadmap/executor.py`, lines 649-828

Implements the `StepRunner` protocol. Called by `execute_pipeline()` for each step.

### Special-case dispatch (non-LLM steps):
Before launching a Claude subprocess, the runner checks `step.id` for special handling:

1. **`step.id == "anti-instinct"`** (line 673): Runs `_run_anti_instinct_audit()` directly. Three deterministic modules: obligation scanner, integration contract checker, fingerprint coverage. No subprocess.

2. **`step.id == "spec-fidelity"` with `config.convergence_enabled`** (line 688): Runs `_run_convergence_spec_fidelity()` — structural checkers + semantic layer + convergence engine.

3. **`step.id == "deviation-analysis"`** (line 692): Runs `_run_deviation_analysis()` — reads `deviation-registry.json`, aggregates by deviation_class, writes gate-compliant output.

4. **`step.id == "remediate"`** (line 696): Runs `_run_remediate_step()` — reads `spec-deviations.json`, converts to findings, generates remediation tasklist.

5. **`step.id == "wiring-verification"`** (line 702): Runs `run_wiring_analysis()` + `emit_report()` — static code analysis. Returns PASS unconditionally; gate evaluation is TRAILING.

### Standard Claude subprocess path (lines 719-828):
1. Build semantic role labels for input files (C-25)
2. Embed input files into prompt via `_embed_inputs()` (inline, not `--file`)
3. Check composed prompt size against `_EMBED_SIZE_LIMIT` (120KB) — warns but proceeds
4. Construct `ClaudeProcess` with: prompt, output_file, error_file (.err), max_turns, model, permission_flag, timeout, output_format="text"
5. `proc.start()` — launches subprocess
6. Poll loop: check cancel_check every 1 second while process runs
7. `proc.wait()` — get exit code
8. Exit code 124 = TIMEOUT, non-zero = FAIL
9. **Post-processing on success:**
   - `_sanitize_output()` — strips conversational preamble before YAML frontmatter
   - If `step.id == "extract"`: inject pipeline_diagnostics (FR-033) + run structural audit
   - If `step.id == "test-strategy"`: inject provenance fields
10. Return StepResult with PASS status (gate check happens in `execute_pipeline`)

---

## 7. Generic Pipeline Executor: `execute_pipeline()`

**File:** `src/superclaude/cli/pipeline/executor.py`, lines 46-171

### Signature:
```python
def execute_pipeline(
    steps: list[Step | list[Step]],
    config: PipelineConfig,
    run_step: StepRunner,
    on_step_start, on_step_complete, on_state_update,
    cancel_check, trailing_runner,
) -> list[StepResult]
```

### Algorithm:
1. Create `TrailingGateRunner` if `config.grace_period > 0`
2. Iterate over `steps` list:
   - **If `list[Step]`** (parallel group): call `_run_parallel_steps()`, halt if any FAIL
   - **If `Step`** (sequential): call `_execute_single_step()`, halt if not PASS
3. **Deferred execution:** After main loop (even on halt), find TRAILING-mode steps not yet executed and run them
4. **Sync point:** Collect trailing gate results, log warnings for failures
5. Return all `StepResult`s (flattened)

### `_execute_single_step()` (lines 174-294):
1. Call `on_step_start(step)`
2. Determine effective gate mode: TRAILING demoted to BLOCKING if `grace_period == 0`
3. Retry loop (retry_limit + 1 attempts):
   - Check cancel signal
   - Call `run_step(step, config, cancel_check)` — the injected `roadmap_run_step`
   - If no gate: trust runner's status
   - If TIMEOUT/CANCELLED: return immediately
   - **TRAILING mode:** submit to TrailingGateRunner, return PASS immediately
   - **BLOCKING mode:** call `gate_passed(output_file, gate)` synchronously
     - PASS: return PASS
     - FAIL: log, retry if attempts remain, else return FAIL

### `_run_parallel_steps()` (lines 297-347):
- Spawns one thread per step (daemon threads)
- Uses shared `cancel_event` — if any step fails, remaining get cancelled
- Waits for all threads to join
- Returns list of results, substituting CANCELLED for any None entries

---

## 8. Gate Evaluation Details

**File:** `src/superclaude/cli/roadmap/gates.py` (gate definitions), `src/superclaude/cli/pipeline/gates.py` (enforcement logic)

### Gate Criteria per Step:

| Gate | Required Frontmatter | Min Lines | Tier | Semantic Checks |
|------|---------------------|-----------|------|-----------------|
| EXTRACT_GATE | spec_source, generated, generator, functional_requirements, nonfunctional_requirements, total_requirements, complexity_score, complexity_class, domains_detected, risks_identified, dependencies_identified, success_criteria_count, extraction_mode | 50 | STRICT | complexity_class_valid, extraction_mode_valid |
| EXTRACT_TDD_GATE | (all of EXTRACT_GATE) + data_models_identified, api_surfaces_identified, components_identified, test_artifacts_identified, migration_items_identified, operational_items_identified | 50 | STRICT | complexity_class_valid, extraction_mode_valid |
| GENERATE_A/B_GATE | spec_source, complexity_score, primary_persona | 100 | STRICT | frontmatter_values_non_empty, has_actionable_content |
| DIFF_GATE | total_diff_points, shared_assumptions_count | 30 | STANDARD | (none) |
| DEBATE_GATE | convergence_score, rounds_completed | 50 | STRICT | convergence_score_valid (float in [0.0, 1.0]) |
| SCORE_GATE | base_variant, variant_scores | 20 | STANDARD | (none) |
| MERGE_GATE | spec_source, complexity_score, adversarial | 150 | STRICT | no_heading_gaps, cross_refs_resolve, no_duplicate_headings |
| ANTI_INSTINCT_GATE | undischarged_obligations, uncovered_contracts, fingerprint_coverage | 10 | STRICT | no_undischarged_obligations, integration_contracts_covered, fingerprint_coverage_check (>=0.7) |
| TEST_STRATEGY_GATE | spec_source, generated, generator, complexity_class, validation_philosophy, validation_milestones, work_milestones, interleave_ratio, major_issue_policy | 40 | STRICT | complexity_class_valid, interleave_ratio_consistent, milestone_counts_positive, validation_philosophy_correct, major_issue_policy_correct |
| SPEC_FIDELITY_GATE | high_severity_count, medium_severity_count, low_severity_count, total_deviations, validation_complete, tasklist_ready | 20 | STRICT | high_severity_count_zero, tasklist_ready_consistent |
| WIRING_GATE | (imported from audit module) | — | — | — |
| DEVIATION_ANALYSIS_GATE | schema_version, total_analyzed, slip_count, intentional_count, pre_approved_count, ambiguous_count, routing_fix_roadmap, routing_no_action, analysis_complete | 20 | STRICT | no_ambiguous_deviations, validation_complete_true, routing_ids_valid, slip_count_matches_routing, pre_approved_not_in_fix_roadmap, total_analyzed_consistent, deviation_counts_reconciled |
| REMEDIATE_GATE | type, source_report, source_report_hash, total_findings, actionable, skipped | 10 | STRICT | frontmatter_values_non_empty, all_actionable_have_status |
| CERTIFY_GATE | findings_verified, findings_passed, findings_failed, certified, certification_date | 15 | STRICT | frontmatter_values_non_empty, per_finding_table_present, certified_is_true |

---

## 9. Data Flow Summary

```
CLI (commands.py)
  |
  v
_route_input_files() -- classify spec/tdd/prd
  |
  v
execute_roadmap()
  |-- _restore_from_state() [if --resume]
  |-- _build_steps(config)
  |-- [dry-run check]
  |-- _apply_resume() [if --resume, prune passing steps]
  |
  v
execute_pipeline(steps, config, roadmap_run_step, ...)
  |
  |-- for each Step/list[Step]:
  |     |
  |     v
  |   _execute_single_step() or _run_parallel_steps()
  |     |
  |     v
  |   roadmap_run_step(step, config, cancel_check)
  |     |-- [special dispatch: anti-instinct, deviation-analysis, remediate, wiring, convergence]
  |     |-- [standard path: _embed_inputs() -> ClaudeProcess -> poll -> _sanitize_output()]
  |     |
  |     v
  |   gate_passed(output_file, gate)  [BLOCKING mode]
  |     |
  |     v
  |   [retry if fail, halt if exhausted]
  |
  v
_save_state(config, results)
  |
  v
[failure: _apply_resume_after_spec_patch() or sys.exit(1)]
[success: _auto_invoke_validate() unless --no-validate]
```

---

## 10. Key Architectural Patterns

1. **Composition-via-callable:** `execute_pipeline()` is generic — consumers inject their own `StepRunner` and callbacks. No roadmap/sprint imports in pipeline module (NFR-007).

2. **Inline embedding over `--file`:** All input files are embedded directly into the prompt string. The `--file` flag is explicitly avoided as it's a cloud download mechanism, not a local file injector.

3. **File-on-disk gates:** Each step writes output to a file, then gate criteria are evaluated against that file's YAML frontmatter and content. This is the inter-step communication mechanism.

4. **Deterministic steps mixed with LLM steps:** Steps 7 (anti-instinct), 10 (wiring), 11 (deviation-analysis), 12 (remediate) bypass Claude entirely and use pure Python logic.

5. **Parallel-then-sequential:** Only one parallel group exists (generate-A + generate-B). All other steps are sequential with explicit input dependencies.

6. **Trailing gates:** The wiring-verification step uses `GateMode.TRAILING` — its gate is non-blocking and evaluated asynchronously after the main pipeline completes.

7. **Atomic file writes:** State and output files use `tmp + os.replace()` for crash safety.

8. **Output sanitization:** After every Claude subprocess, `_sanitize_output()` strips conversational preamble before YAML frontmatter.

9. **Spec-patch auto-resume:** On spec-fidelity failure, a single auto-resume cycle can detect subprocess-written deviation records and re-run from the failing step.

---

## 11. Gaps and Questions

1. **Certify step (step 13) is confirmed dead code:** `build_certify_step()` is defined at executor.py:1259 but grep confirms it is never called anywhere in the `src/superclaude/cli/roadmap/` directory — not from `execute_roadmap()`, `_build_steps()`, `roadmap_run_step()`, or any other function. It exists only as a function definition with no callers.

2. **Step numbering inconsistency in comments:** Code comments label test-strategy as "Step 8" and spec-fidelity as "Step 8" (duplicate). The actual ordering is test-strategy=8, spec-fidelity=9 in execution order.

3. **Convergence mode (`convergence_enabled`):** Defaults to False. When enabled, spec-fidelity bypasses LLM entirely and uses a multi-round structural checker + semantic layer + remediation loop. No CLI flag to enable it — must be set programmatically.

4. **`_auto_invoke_validate()`** is called on success but was not defined in the sections read. It likely invokes the `validate` subcommand's executor.

5. **Single-agent mode:** When only one agent is provided, both generate steps use the same agent (different Step IDs but identical model/persona). The diff/debate/score steps still run but will compare identical outputs.

6. **`_EMBED_SIZE_LIMIT` = 120KB:** If the composed prompt exceeds this, it warns but proceeds anyway. On Linux, `MAX_ARG_STRLEN` is 128KB for a single argument. This could cause E2BIG errors on large specs.

7. **TDD deviation-analysis incompatibility:** Explicitly noted in commands.py (line 239-248) and gates.py comments. The `DEVIATION_ANALYSIS_GATE` is not TDD-compatible.

8. **No dynamic step injection:** The pipeline is built entirely by `_build_steps()` upfront. There is no mechanism to add or modify steps during execution based on intermediate results (except the spec-patch auto-resume path).

## 12. Stale Documentation Found

- The docstring for `roadmap_group` (line 16) says "8-step pipeline" but there are 12+ steps.
- The docstring for `executor.py` module (line 1) says "9-step roadmap pipeline" but there are 12+ steps.
- Comment at line 1444 says "Step 8: Spec Fidelity" — should be Step 9.

## 13. Summary

The roadmap pipeline is a 12-step sequential-with-one-parallel-group pipeline:

1. **Entry:** `commands.py::run()` parses CLI args, routes input files, builds `RoadmapConfig`, calls `execute_roadmap()`
2. **Orchestration:** `execute_roadmap()` handles resume/dry-run, builds steps via `_build_steps()`, delegates to generic `execute_pipeline()`
3. **Execution:** `execute_pipeline()` iterates steps, calling `roadmap_run_step()` for each, with retry and gate logic
4. **Step runner:** `roadmap_run_step()` dispatches to either deterministic Python logic (4 steps) or a Claude subprocess (8 steps), with post-processing (sanitization, field injection)
5. **Gates:** Each step's output file is validated against `GateCriteria` — frontmatter fields, min lines, semantic checks. 11 of 14 gates are STRICT tier.
6. **State:** `.roadmap-state.json` persists results for `--resume` support

**Key finding for overhaul:** All inter-step communication is via file-on-disk with YAML frontmatter. The extraction step is the single bottleneck that must capture all spec content — everything downstream depends on it. There is no incremental or template-driven writing mechanism; each step generates its full output from scratch via a single LLM call.

