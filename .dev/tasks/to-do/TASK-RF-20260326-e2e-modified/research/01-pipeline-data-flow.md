# Research: Data Flow Tracer — Pipeline Execution Flow

**Status**: Complete
**Researcher**: pipeline-data-flow
**Scope**: `src/superclaude/cli/roadmap/executor.py`, `commands.py`, `models.py`
**Focus**: How `superclaude roadmap run` processes input through all pipeline steps

---

## 1. CLI Invocation Syntax and Flags

**Source**: `src/superclaude/cli/roadmap/commands.py`, lines 32-218

### Basic syntax
```
superclaude roadmap run <SPEC_FILE> [OPTIONS]
```

`SPEC_FILE` is a positional argument: `click.Path(exists=True, path_type=Path)` — the file must exist.

### All flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--agents` | str (comma-sep) | `None` (model default: `opus:architect,haiku:architect`) | Agent specs `model[:persona]` |
| `--output` | Path | parent dir of `SPEC_FILE` | Output directory for all artifacts |
| `--depth` | Choice: quick/standard/deep | `None` (model default: `standard`) | Debate round depth |
| `--resume` | flag | False | Skip steps whose outputs already pass gates |
| `--dry-run` | flag | False | Print step plan and exit |
| `--model` | str | `""` | Override model for all steps |
| `--max-turns` | int | 100 | Max agent turns per subprocess |
| `--debug` | flag | False | Debug logging to `output_dir/roadmap-debug.log` |
| `--no-validate` | flag | False | Skip post-pipeline validation step |
| `--allow-regeneration` | flag | False | Allow patches exceeding diff-size threshold |
| `--retrospective` | Path | None | Path to retrospective file (missing file not an error) |
| `--input-type` | Choice: auto/tdd/spec | `auto` | Force input type detection |

### CLI-level auto-detection feedback (commands.py lines 193-210)
When `--input-type auto` (default), the CLI calls `detect_input_type()` and prints:
```
[roadmap] Auto-detected input type: {tdd|spec}
```
If TDD detected, a yellow warning is emitted:
```
NOTE: TDD input detected. The pipeline's deviation-analysis step (DEVIATION_ANALYSIS_GATE) is not yet TDD-compatible and may fail. All other steps (extract through spec-fidelity) will work correctly.
```

### Output directory resolution (commands.py line 152)
```python
resolved_output = output_dir if output_dir is not None else spec_file.parent
```
Both `output_dir` and `work_dir` in the config are set to the resolved output path.

---

## 2. RoadmapConfig Fields

**Source**: `src/superclaude/cli/roadmap/models.py`, lines 95-116
**Parent**: `PipelineConfig` at `src/superclaude/cli/pipeline/models.py`, lines 170-180

### PipelineConfig (parent) fields
| Field | Type | Default |
|-------|------|---------|
| `work_dir` | Path | `Path(".")` |
| `dry_run` | bool | `False` |
| `max_turns` | int | `100` |
| `model` | str | `""` |
| `permission_flag` | str | `"--dangerously-skip-permissions"` |
| `debug` | bool | `False` |
| `grace_period` | int | `0` |

### RoadmapConfig (child) additional fields
| Field | Type | Default |
|-------|------|---------|
| `spec_file` | Path | `Path(".")` |
| `agents` | list[AgentSpec] | `[AgentSpec("opus","architect"), AgentSpec("haiku","architect")]` |
| `depth` | Literal["quick","standard","deep"] | `"standard"` |
| `output_dir` | Path | `Path(".")` |
| `retrospective_file` | Path \| None | `None` |
| `convergence_enabled` | bool | `False` |
| `allow_regeneration` | bool | `False` |
| `input_type` | Literal["auto","tdd","spec"] | `"auto"` |
| `tdd_file` | Path \| None | `None` |

### AgentSpec (models.py lines 65-91)
- Parsed from `"model:persona"` or just `"model"` (defaults persona to `"architect"`)
- `.id` property returns `"{model}-{persona}"` (used in filenames, e.g. `opus-architect`)

---

## 3. `detect_input_type()` — 4-Signal Scoring

**Source**: `executor.py`, lines 59-108

Reads the spec file content and applies a scoring system. Threshold: `score >= 3` means TDD.

| Signal | What it checks | Points |
|--------|---------------|--------|
| **Signal 1**: Numbered headings | Count of `^## \d+\.` patterns. >=10 headings: +3; >=5: +2 | 0-3 |
| **Signal 2**: TDD frontmatter fields | Checks for `feature_id`, `parent_doc`, `authors`, `quality_scores`, `coordinator` at line start | +1 each (max 5) |
| **Signal 3**: TDD section names | Checks for 9 strings: "Data Models", "API Specifications", "Component Inventory", "Testing Strategy", "Operational Readiness", "Migration & Rollout", "State Management", "Performance Budgets", "Accessibility Requirements" | +1 each (max 9) |
| **Signal 4**: Frontmatter type | `"Technical Design Document"` in first 1000 chars | +2 |

On read failure (OSError, UnicodeDecodeError), returns `"spec"` (fallback).

---

## 4. `_build_steps()` — Complete Step List

**Source**: `executor.py`, lines 832-1001

Returns `list[Step | list[Step]]` where inner lists are parallel groups.

### Input type resolution (line 841-843)
```python
effective_input_type = config.input_type
if effective_input_type == "auto":
    effective_input_type = detect_input_type(config.spec_file)
```

### Agent resolution (lines 847-848)
```python
agent_a = config.agents[0]
agent_b = config.agents[1] if len(config.agents) > 1 else config.agents[0]
```

### Step-by-step table

| # | Step ID | Prompt Function | Gate | Output File | Timeout | Inputs | Retry | Notes |
|---|---------|----------------|------|-------------|---------|--------|-------|-------|
| 1 | `extract` | `build_extract_prompt_tdd()` if TDD, else `build_extract_prompt()` | `EXTRACT_GATE` | `extraction.md` | 300s | `[spec_file]` | 1 | TDD/spec branching here |
| 2a | `generate-{agent_a.id}` | `build_generate_prompt(agent_a, extraction)` | `GENERATE_A_GATE` | `roadmap-{agent_a.id}.md` | 900s | `[extraction.md]` | 1 | model=agent_a.model |
| 2b | `generate-{agent_b.id}` | `build_generate_prompt(agent_b, extraction)` | `GENERATE_B_GATE` | `roadmap-{agent_b.id}.md` | 900s | `[extraction.md]` | 1 | model=agent_b.model; **parallel with 2a** |
| 3 | `diff` | `build_diff_prompt(roadmap_a, roadmap_b)` | `DIFF_GATE` | `diff-analysis.md` | 300s | `[roadmap_a, roadmap_b]` | 1 | |
| 4 | `debate` | `build_debate_prompt(diff, roadmap_a, roadmap_b, depth)` | `DEBATE_GATE` | `debate-transcript.md` | 600s | `[diff, roadmap_a, roadmap_b]` | 1 | |
| 5 | `score` | `build_score_prompt(debate, roadmap_a, roadmap_b)` | `SCORE_GATE` | `base-selection.md` | 300s | `[debate, roadmap_a, roadmap_b]` | 1 | |
| 6 | `merge` | `build_merge_prompt(score, roadmap_a, roadmap_b, debate)` | `MERGE_GATE` | `roadmap.md` | 600s | `[score, roadmap_a, roadmap_b, debate]` | 1 | |
| 7 | `anti-instinct` | `""` (no LLM) | `ANTI_INSTINCT_GATE` | `anti-instinct-audit.md` | 30s | `[spec_file, merge_file]` | 0 | Deterministic, no subprocess |
| 8 | `test-strategy` | `build_test_strategy_prompt(merge, extraction)` | `TEST_STRATEGY_GATE` | `test-strategy.md` | 300s | `[merge, extraction]` | 1 | |
| 9 | `spec-fidelity` | `build_spec_fidelity_prompt(spec_file, merge)` | `SPEC_FIDELITY_GATE` (or None if convergence) | `spec-fidelity.md` | 600s | `[spec_file, merge]` | 1 | |
| 10 | `wiring-verification` | `build_wiring_verification_prompt(merge, spec_file.name)` | `WIRING_GATE` | `wiring-verification.md` | 60s | `[merge, spec_fidelity]` | 0 | `gate_mode=GateMode.TRAILING` |

### Extract step TDD branching (lines 874-886)
```python
prompt=(
    build_extract_prompt_tdd(config.spec_file, retrospective_content=retrospective_content)
    if effective_input_type == "tdd"
    else build_extract_prompt(config.spec_file, retrospective_content=retrospective_content)
)
```
Both prompt builders are imported from `.prompts` (line 46-47).

---

## 5. Output Directory Structure

**Source**: `executor.py`, lines 850-859

All output files are written to `config.output_dir` (resolved from `--output` or spec file parent dir).

### Files created by pipeline steps
```
{output_dir}/
  extraction.md                    # Step 1
  roadmap-{agent_a.id}.md          # Step 2a  (e.g. roadmap-opus-architect.md)
  roadmap-{agent_b.id}.md          # Step 2b  (e.g. roadmap-haiku-architect.md)
  diff-analysis.md                 # Step 3
  debate-transcript.md             # Step 4
  base-selection.md                # Step 5
  roadmap.md                       # Step 6 (merged final)
  anti-instinct-audit.md           # Step 7
  test-strategy.md                 # Step 8
  spec-fidelity.md                 # Step 9
  wiring-verification.md           # Step 10
  .roadmap-state.json              # State file (written by _save_state)
```

### Additional files from error/subprocess paths
```
  {step_output}.err                # Error file per step (ClaudeProcess error_file)
  certification-report.md          # Certify step (post-pipeline)
  remediation-tasklist.md          # Remediate step (post-pipeline)
  deviation-registry.json          # Convergence mode only
  spec-deviations.md               # Deviation analysis
  dev-*-accepted-deviation.md      # Accepted deviation records
```

---

## 6. `execute_roadmap()` Orchestration

**Source**: `executor.py`, lines 1717-1843

### Full flow
1. `config.output_dir.mkdir(parents=True, exist_ok=True)` — ensure output dir exists
2. If `--resume`: call `_restore_from_state()` to restore agents/depth from `.roadmap-state.json`
3. Apply hardcoded defaults if agents/depth still empty
4. Capture `initial_spec_hash` (for spec-patch cycle detection)
5. Call `_build_steps(config)` to build step list
6. If `config.dry_run`: call `_dry_run_output(steps)` and return
7. If `resume`: call `_apply_resume(steps, config, gate_passed)` to skip already-passed steps
8. Call `execute_pipeline(steps, config, roadmap_run_step, on_step_start, on_step_complete)`
9. Call `_save_state(config, results)`
10. Check for failures:
    - If spec-fidelity failed: attempt spec-patch auto-resume cycle
    - If any failure: print `_format_halt_output()` to stderr, `sys.exit(1)`
11. If all passed: print `[roadmap] Pipeline complete: N steps passed`
12. Unless `--no-validate`: auto-invoke validation

### Key function signatures
```python
def execute_roadmap(
    config: RoadmapConfig,
    resume: bool = False,
    no_validate: bool = False,
    auto_accept: bool = False,
    agents_explicit: bool = True,
    depth_explicit: bool = True,
) -> None:
```

---

## 7. `--dry-run` Behavior

**Source**: `executor.py`, lines 1316-1347, 1769-1772

When `config.dry_run` is True:
1. `_build_steps()` is called normally to construct the full step list
2. `_dry_run_output(steps)` is called, which iterates over all steps
3. For each step, `_print_step_plan()` prints:
   ```
   Step N: {step.id}
     Output: {step.output_file}
     Timeout: {step.timeout_seconds}s
     Model: {step.model}                    # only if model is set
     Gate tier: {step.gate.enforcement_tier}
     Gate min_lines: {step.gate.min_lines}
     Gate frontmatter: field1, field2, ...   # only if gate has required fields
     Semantic checks: check1, check2, ...    # only if gate has semantic checks
   ```
4. Parallel steps are labeled `(parallel)`: `Step N (parallel): {step.id}`
5. Function returns immediately after printing — no subprocess execution

Additionally, in `roadmap_run_step()` (line 444-452), if `config.dry_run`, each step returns `StepResult(status=PASS)` immediately without launching a subprocess.

---

## 8. `--output` Flag Behavior

**Source**: `commands.py`, lines 48-49, 152

- CLI option name is `output_dir`, maps to `--output`
- Default: `None`
- Resolution: `resolved_output = output_dir if output_dir is not None else spec_file.parent`
- Both `config.output_dir` and `config.work_dir` are set to `resolved_output.resolve()` (absolute path)
- The directory is created in `execute_roadmap()` line 1745: `config.output_dir.mkdir(parents=True, exist_ok=True)`

---

## 9. Error Handling: Gate Failures

**Source**: `executor.py`, lines 1792-1820 and 1004-1060

### Step-level failure in `roadmap_run_step()`:
- Exit code 124 (timeout): returns `StepResult(status=StepStatus.TIMEOUT)`
- Non-zero exit code: returns `StepResult(status=StepStatus.FAIL, gate_failure_reason=...)`
- Gate evaluation happens in `execute_pipeline()` (separate module), not in `roadmap_run_step()`

### Pipeline-level failure handling in `execute_roadmap()`:
1. After `execute_pipeline()` returns, checks for any `FAIL` or `TIMEOUT` results
2. If spec-fidelity specifically failed: attempts a spec-patch auto-resume cycle (one-shot)
3. Otherwise: calls `_format_halt_output(results, config)` which produces:
   ```
   ERROR: Roadmap pipeline halted at step '{step_id}' (attempt N/2)
     Gate failure: {reason}
     Output file: {path}
     Output size: X bytes (Y lines)
     Step timeout: Xs | Elapsed: Ys

   Completed steps: step1 (PASS, attempt 1), step2 (PASS, attempt 1)
   Failed step:     stepN (FAIL, attempt 1)
   Skipped steps:   stepM, stepO

   To retry from this step:
     superclaude roadmap run {spec_file} --resume

   To inspect the failing output:
     cat {output_file}
   ```
4. Then calls `sys.exit(1)`

### Special step behaviors:
- **anti-instinct** (step 7): runs `_run_anti_instinct_audit()` deterministically (no subprocess). If it raises, the error propagates.
- **wiring-verification** (step 10): runs static analysis directly. `gate_mode=GateMode.TRAILING` means it does not block subsequent steps.
- **spec-fidelity** (step 9): if `convergence_enabled`, runs convergence engine instead of LLM subprocess.

---

## 10. `roadmap_run_step()` — Step Runner

**Source**: `executor.py`, lines 432-593

This is the `StepRunner` callback passed to `execute_pipeline()`.

### Execution flow per step:
1. Record `started_at`
2. If `dry_run`: return PASS immediately
3. If `anti-instinct`: run `_run_anti_instinct_audit()` directly (no subprocess)
4. If `spec-fidelity` with convergence: run `_run_convergence_spec_fidelity()`
5. If `wiring-verification`: run `run_wiring_analysis()` + `emit_report()` directly
6. Otherwise: embed inputs into prompt via `_embed_inputs()`, launch `ClaudeProcess`
7. Poll for cancellation while subprocess runs
8. On completion: sanitize output (strip preamble before YAML frontmatter)
9. Post-processing:
   - Extract step: inject `pipeline_diagnostics` into frontmatter + structural audit
   - Test-strategy step: inject provenance fields (`spec_source`, `generated`, `generator`)
10. Return `StepResult`

### State file `.roadmap-state.json` structure (lines 1410-1428)
```json
{
  "schema_version": 1,
  "spec_file": "<absolute path>",
  "spec_hash": "<sha256>",
  "agents": [{"model": "opus", "persona": "architect"}, ...],
  "depth": "standard",
  "last_run": "<ISO timestamp>",
  "steps": {
    "<step_id>": {
      "status": "PASS|FAIL|TIMEOUT",
      "attempt": 1,
      "output_file": "<path>",
      "started_at": "<ISO>",
      "completed_at": "<ISO>"
    }
  },
  "validation": {...},
  "fidelity_status": "pass|fail|skipped|degraded",
  "remediate": {...},
  "certify": {...}
}
```

---

## 11. Complete Step ID List (Pipeline Order)

**Source**: `executor.py`, `_get_all_step_ids()`, lines 1063-1081

```python
[
    "extract",
    "generate-{agent_a.id}",  # e.g. "generate-opus-architect"
    "generate-{agent_b.id}",  # e.g. "generate-haiku-architect"
    "diff",
    "debate",
    "score",
    "merge",
    "anti-instinct",
    "test-strategy",
    "spec-fidelity",
    "wiring-verification",
    "remediate",
    "certify",
]
```

Note: `remediate` and `certify` appear in the ID list but are not in `_build_steps()` — they are post-pipeline steps built separately via `build_certify_step()`.

---

## Summary

The `superclaude roadmap run` pipeline is a 10-step (11 with trailing wiring) orchestrated execution:

1. **CLI layer** (`commands.py`): parses flags, builds `RoadmapConfig`, calls `detect_input_type()` for user feedback, then delegates to `execute_roadmap()`
2. **Orchestrator** (`execute_roadmap()`): handles resume/state restoration, builds steps via `_build_steps()`, handles dry-run shortcut, delegates to `execute_pipeline()`, manages post-pipeline validation and spec-patch cycles
3. **Step builder** (`_build_steps()`): constructs 10 `Step` objects with prompt functions, gates, output paths, and timeouts. Steps 2a+2b are a parallel group (inner list). TDD/spec branching happens at step 1 (extract) via different prompt builders.
4. **Step runner** (`roadmap_run_step()`): executes each step either as a Claude subprocess or directly (anti-instinct, wiring-verification). Post-processes output (sanitize preamble, inject metadata).
5. **Error path**: gate failures cause pipeline halt with diagnostic output and `sys.exit(1)`. Spec-fidelity failures trigger a one-shot auto-resume cycle.

Key file naming convention: output files use agent `.id` property (`{model}-{persona}`) for generate steps, fixed names for all others. All files land in `config.output_dir`.
