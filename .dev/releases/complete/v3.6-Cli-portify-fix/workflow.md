# v3.6 CLI Portify Fix — Implementation Workflow

**Source:** `cli-portify-audit.md` (fully validated 2026-03-23)
**Scope:** 42 confirmed issues across `src/superclaude/cli/cli_portify/` (31 files)
**Execution:** `/sc:task-unified` per task
**Branch:** Create `feature/v3.6-cli-portify-fix` from `master`

---

## Phase 1: Make the Pipeline Run [P0]

> **Goal:** `superclaude cli-portify run <skill>` launches real Claude subprocesses, produces artifacts, validates config, and emits a complete return contract.
> **Resolves:** C-01, C-02, C-03, C-04, C-05, C-06, C-07, H-01, H-02, H-04, H-05, H-06
> **Checkpoint:** Run `superclaude cli-portify run sc-roadmap --dry-run --output /tmp/test-portify` — must exit 0 with `return-contract.yaml` containing 8 fields

### Task 1.1: Wire step dispatch into executor (AD-1)

**Fixes:** C-01, C-02, C-04, C-05
**Files:** `executor.py`, `steps/__init__.py`
**Tier:** complex

1. Create a step dispatch registry in `steps/__init__.py` mapping step IDs from `STEP_REGISTRY` to their `run_*()` functions
2. In `executor.py:_execute_step()`, replace the `self._step_runner` / no-op fallback with a direct call to the step dispatch registry
3. Remove the `step_runner` parameter from `PortifyExecutor.__init__()` — it's no longer needed
4. Each step module's `run()` function already uses `PortifyProcess` directly (System B pattern) — no changes needed in step files for this task

**Depends on:** nothing
**Verify:** `PortifyExecutor._execute_step()` calls into step modules; no more no-op fallback

### Task 1.2: Set output_file on PortifyStep construction

**Fixes:** C-06
**Files:** `executor.py` (around line 1454-1461)
**Tier:** simple

1. When building `PortifyStep` from `STEP_REGISTRY` entries, set `output_file` and `error_file` to the expected artifact paths in the workdir (derive from step ID + known artifact names)
2. Verify `_determine_status()` can now see a real `artifact_path`

**Depends on:** nothing
**Verify:** `step.output_file is not None` for every constructed step

### Task 1.3: Wire config validation

**Fixes:** C-03
**Files:** `commands.py`, `config.py`
**Tier:** simple

1. Import `validate_portify_config` from `config.py` into `commands.py`
2. Call `validate_portify_config(config)` before `run_portify(config)` at line 109
3. Ensure `PortifyValidationError` is raised for: missing workflow path, non-existent SKILL.md, non-writable output dir

**Depends on:** nothing
**Verify:** `superclaude cli-portify run sc-fake` produces clean error, exit code 1

### Task 1.4: Wire workdir creation

**Fixes:** H-04
**Files:** `commands.py` or `executor.py`, `workdir.py`
**Tier:** simple

1. Import `create_workdir` and `emit_portify_config_yaml` from `workdir.py`
2. Call `create_workdir(config)` before executor construction
3. Call `emit_portify_config_yaml(config, workdir)` to write `portify-config.yaml`

**Depends on:** Task 1.3 (validation must pass before workdir creation)
**Verify:** Output directory contains `portify-config.yaml` after run

### Task 1.5: Add resume_from field to PortifyConfig

**Fixes:** H-01
**Files:** `models.py`, `commands.py`
**Tier:** simple

1. Add `resume_from: str = ""` field to `PortifyConfig` dataclass
2. Remove the `# type: ignore[attr-defined]` dynamic attribute assignment in `commands.py:107`
3. Set `config.resume_from = resume_step` directly (now a valid field)

**Depends on:** nothing
**Verify:** `mypy` or type checker no longer needs the ignore comment

### Task 1.6: Wire resume validation

**Fixes:** H-02
**Files:** `commands.py` or `executor.py`, `resume.py`
**Tier:** simple

1. Import `validate_resume_entry` from `resume.py`
2. When `config.resume_from` is set, call `validate_resume_entry(config.resume_from, workdir)` before starting execution
3. Raise `PortifyValidationError` if resume prerequisites not met

**Depends on:** Task 1.4, Task 1.5
**Verify:** `--resume invalid-step` produces clean error

### Task 1.7: Merge cli.py into commands.py, delete cli.py (AD-3)

**Fixes:** C-07
**Files:** `commands.py`, `cli.py`
**Tier:** medium

1. Read `cli.py` and identify useful options not in `commands.py`: `--commands-dir`, `--skills-dir`, `--agents-dir`, `--include-agent`, `--save-manifest`, `--start`
2. Add these options to the click command in `commands.py`
3. Delete `cli.py`
4. Verify `main.py:370` still imports correctly (it already uses `commands.py`)

**Depends on:** nothing
**Verify:** `cli.py` deleted; `superclaude cli-portify --help` shows merged options

### Task 1.8: Broaden exception handling

**Fixes:** H-06
**Files:** `commands.py`
**Tier:** simple

1. Add catch blocks for `FileNotFoundError`, `PermissionError`, `OSError`, `yaml.YAMLError`
2. Add a final `except Exception` catch-all that logs traceback and exits cleanly
3. All error paths should `click.echo(str(exc), err=True)` and `sys.exit(1)`

**Depends on:** nothing
**Verify:** Trigger each error type; confirm clean messages, no raw tracebacks

### Task 1.9: Replace inline return contract with PortifyContract builders

**Fixes:** H-05
**Files:** `executor.py`, `contract.py`
**Tier:** medium

1. In `executor.py:_emit_return_contract()` (lines 276-309), replace raw dict + yaml.safe_dump with calls to `build_success_contract()`, `build_partial_contract()`, or `build_failed_contract()` from `contract.py`
2. Ensure all 8 PortifyContract fields are populated: `status`, `phases`, `artifacts`, `step_timings`, `gate_results`, `total_duration`, `error_message`, `resume_command`

**Depends on:** Task 1.1 (step dispatch must be wired to produce real step_timings and gate_results)
**Verify:** `return-contract.yaml` contains all 8 fields

### Task 1.10: Delete unreachable execute_*_step() free functions

**Fixes:** C-05, M-05
**Files:** `executor.py`
**Tier:** simple

1. Delete the 7 free functions (lines ~509-1230): `execute_protocol_mapping_step`, `execute_analysis_synthesis_step`, `execute_step_graph_design_step`, `execute_models_gates_design_step`, `execute_prompts_executor_design_step`, `execute_pipeline_spec_assembly_step`, `execute_release_spec_synthesis_step`
2. Remove any imports only used by those functions

**Depends on:** Task 1.1 (must confirm new dispatch is working before deleting old code)
**Verify:** `executor.py` reduced by ~700 lines; no import errors

---

## Phase 2: Wire Infrastructure [P0/P1]

> **Goal:** Gate enforcement, execution logging, stall detection, diagnostics, TUI, and review gates all active.
> **Resolves:** H-08, H-09, H-10, H-11, H-12, H-13, H-14
> **Checkpoint:** Run pipeline with intentionally bad Claude output — must see gate failure, diagnostics.md, execution log entries

### Task 2.1: Wire GATE_REGISTRY into executor [P0]

**Fixes:** H-13
**Files:** `executor.py`, `gates.py`
**Tier:** medium

1. Import `get_gate_criteria` from `gates.py` into `executor.py`
2. After each step completes in `_execute_step()`, call `get_gate_criteria(step.step_id)` and run the gate function against step output
3. If gate fails, set step status to `GATE_FAILURE` and halt pipeline (or continue based on gate severity)
4. Record gate results for inclusion in return contract

**Depends on:** Phase 1 (Task 1.1 specifically)
**Verify:** Bad step output triggers gate failure, not PASS_NO_SIGNAL

### Task 2.2: Wire ExecutionLog [P1]

**Fixes:** H-10
**Files:** `executor.py`, `logging_.py`
**Tier:** simple

1. Instantiate `ExecutionLog` in `PortifyExecutor.__init__()`
2. Call logging methods at step start, step complete, step fail, pipeline complete events
3. Ensure `execution-log.jsonl` and `execution-log.md` written to workdir

**Depends on:** Phase 1
**Verify:** Workdir contains `execution-log.jsonl` after run

### Task 2.3: Wire OutputMonitor with stall detection [P1]

**Fixes:** H-08
**Files:** `executor.py`, `monitor.py`
**Tier:** medium

1. Instantiate `OutputMonitor` in executor
2. Connect stall detection callback to step execution
3. Configure timeout from `config.stall_timeout`

**Depends on:** Phase 1
**Verify:** Long-running step triggers stall detection callback

### Task 2.4: Wire DiagnosticsCollector [P1]

**Fixes:** H-09
**Files:** `executor.py`, `diagnostics.py`
**Tier:** simple

1. Instantiate `DiagnosticsCollector` in executor
2. In the executor's `finally` block (or error handler), call `emit_diagnostics()` on failure
3. Ensure `diagnostics.md` written to workdir on pipeline failure

**Depends on:** Phase 1
**Verify:** Pipeline failure produces `diagnostics.md`

### Task 2.5: Wire failures.py handlers [P1]

**Fixes:** H-12
**Files:** `executor.py`, `failures.py`
**Tier:** simple

1. Import `FAILURE_HANDLERS` from `failures.py`
2. In error handling paths, dispatch to appropriate failure handler based on error type
3. Failure classification feeds into return contract and diagnostics

**Depends on:** Task 2.4
**Verify:** Different failure types produce different handler output

### Task 2.6: Wire review.py into step modules [P1]

**Fixes:** H-14
**Files:** `review.py`, `steps/design_pipeline.py`, `steps/panel_review.py`
**Tier:** medium

1. Replace inline review gate implementations in `design_pipeline.py` and `panel_review.py` with imports from canonical `review.py`
2. Wire `review_gate()` into steps that require user approval before proceeding
3. Use `REVIEW_GATE_STEPS` to determine which steps need review

**Depends on:** Phase 1
**Verify:** Steps in `REVIEW_GATE_STEPS` prompt for user review

### Task 2.7: Wire PortifyTUI [P2]

**Fixes:** H-11
**Files:** `executor.py`, `tui.py`
**Tier:** medium

1. Instantiate `PortifyTUI` in executor with TTY detection (only when stdout is a terminal)
2. Update TUI step list to match `STEP_REGISTRY` entries
3. Feed step progress events to TUI

**Depends on:** Task 2.2 (logging provides events TUI can display)
**Verify:** Pipeline run in terminal shows live dashboard; non-TTY runs skip TUI

---

## Phase 3: Consolidate Duplicates [P1]

> **Goal:** Each concept has exactly one canonical definition. No duplicate systems.
> **Resolves:** M-01, M-02, M-03, H-03
> **Checkpoint:** grep for duplicate class/constant names returns only the canonical definition

### Task 3.1: Delete steps/gates.py, canonicalize gates.py (AD-2)

**Fixes:** M-01
**Files:** `steps/gates.py`, `gates.py`, step modules that import from `steps/gates.py`
**Tier:** simple

1. Find all imports of `steps/gates.py` across step modules
2. Replace with imports from top-level `gates.py`
3. Delete `steps/gates.py`

**Depends on:** Task 2.1 (gates must be wired first)
**Verify:** `steps/gates.py` deleted; no import errors

### Task 3.2: Remove duplicate ConvergenceState from models.py

**Fixes:** M-02
**Files:** `models.py`
**Tier:** simple

1. Delete the `ConvergenceState` enum from `models.py:136` (the unused one)
2. Verify `convergence.py:ConvergenceState` is the only remaining definition
3. Check no code references the deleted enum

**Depends on:** nothing
**Verify:** Only one `ConvergenceState` definition in codebase

### Task 3.3: Consolidate 4 copies of resumable steps

**Fixes:** H-03
**Files:** `resume.py`, `failures.py`, `contract.py`, `steps/validate_config.py`
**Tier:** medium

1. Keep `resume.py:RESUMABILITY_MATRIX` as canonical source (richest data structure)
2. In `failures.py`, `contract.py`, and `steps/validate_config.py`: replace local `_RESUMABLE_STEPS` / `RESUMABLE_STEPS` with imports from `resume.py`
3. Add a helper function in `resume.py`: `get_resumable_step_names() -> frozenset[str]` for simple consumers

**Depends on:** nothing
**Verify:** grep for `RESUMABLE_STEPS` and `_RESUMABLE_STEPS` returns only resume.py definitions + imports

### Task 3.4: Consolidate StepTiming into contract.py

**Fixes:** M-03
**Files:** `contract.py`, `monitor.py`
**Tier:** simple

1. Keep `contract.py:StepTiming` as canonical (used in return contract)
2. Refactor `monitor.py` to import and use `contract.py:StepTiming` instead of its own
3. Adapt fields if needed (monitor may need start_time/end_time; consider adding to canonical)

**Depends on:** Task 2.2, Task 2.3 (monitor/logging must be wired first)
**Verify:** Only one `StepTiming` class definition

---

## Phase 4: Fix Step-Level Bugs [P2]

> **Goal:** All step modules produce correct behavior when given valid Claude output.
> **Resolves:** M-08, M-09, M-11, M-12, M-13, M-14, M-15
> **Checkpoint:** Each step module's gate check passes with known-good test input

### Task 4.1: Fix brainstorm_gaps.py gate bypass + failure classification

**Fixes:** M-08, M-09
**Files:** `steps/brainstorm_gaps.py`
**Tier:** simple

1. Call `has_section_12_content()` on Claude output before returning PASS in `run_brainstorm_gaps()`
2. If gate fails, return `GATE_FAILURE` status (not PASS)
3. Change failure classification at line 191 from `MISSING_ARTIFACT` to appropriate classification for subprocess failure

**Depends on:** Phase 1 (step must be wired to test)
**Verify:** Missing Section 12 content triggers gate failure

### Task 4.2: Fix design_pipeline.py bugs (dry_run, artifact name, gate)

**Fixes:** M-11, M-12, M-13
**Files:** `steps/design_pipeline.py`
**Tier:** medium

1. **M-11:** Move dry_run check before gate check and artifact writing (halt before synthesis)
2. **M-12:** Align `ARTIFACT_NAME` with docstring/prompt — decide canonical name (`portify-spec.md` or `portify-pipeline-design.md`) and update all references
3. **M-13:** Either add `pipeline_steps` to the Claude prompt so the gate can check it, or remove the unrequested frontmatter check from `_check_gate`

**Depends on:** Phase 1
**Verify:** `--dry-run` halts before synthesis; artifact name consistent throughout

### Task 4.3: Fix discover_components.py artifact path + unused tree

**Fixes:** M-14, M-15
**Files:** `steps/discover_components.py`
**Tier:** simple

1. **M-14:** Change line 553 from `config.output_dir` to `config.results_dir` so artifact is written where downstream steps expect it
2. **M-15:** Either pass `tree` to `_render_simple_inventory()` (add parameter) or remove the `_build_simple_tree` call if the tree is not needed

**Depends on:** Phase 1
**Verify:** `component-inventory.md` written to `results_dir`, not `output_dir`

---

## Phase 5: Opportunistic Cleanup [LOW — fix during implementation]

> **Goal:** Clean up cosmetic issues encountered while working on Phases 1-4.
> **Resolves:** L-01, L-02, L-03, L-05, L-06, L-07, L-08, M-06, M-07, M-10 (code smell), M-17, M-18
> **Note:** These are not blocking. Fix when touching the relevant file.

| Item | File | Fix |
|------|------|-----|
| L-01 | `__init__.py` | Replace `<skill_name>` placeholder with actual name |
| L-02 | `config.py` | Fix import ordering in `_find_cli_root()`; remove dead `import superclaude.cli` |
| L-03 | `models.py` | Move `import re` to module level |
| L-05 | `synthesize_spec.py` | Delete unused `MAX_RETRIES = 1` |
| L-06 | `steps/validate_config.py` | Delete dead `_classify_warnings()` function |
| L-07 | `utils.py` | Delete dead `SIGNAL_VOCABULARY` constants and `verify_additive_only()` |
| L-08 | `convergence.py` | Either instantiate `SimpleBudgetGuard` in panel_review or delete the class |
| M-06 | `prompts.py` | Delete dead `PROMPT_BUILDERS` class registry and `get_prompt_builder()` |
| M-07 | `prompts.py` | Delete dead `maybe_split_prompt()` |
| M-10 | `design_pipeline.py` | Replace `getattr(config, "skip_review", True)` with `config.skip_review` |
| M-17 | `gates.py` | Add `re.DOTALL` flag to `has_criticals_addressed()` regex |
| M-18 | `resolution.py` | Delete dead `resolved` variable in `_find_command_for_skill()` |

---

## Dependency Graph

```
Phase 1 (P0 — pipeline runs)
  ├── Task 1.1 (step dispatch)  ─┐
  ├── Task 1.2 (output_file)    │
  ├── Task 1.3 (config valid)   │   ← all independent, can parallelize
  ├── Task 1.5 (resume_from)    │
  ├── Task 1.7 (merge cli.py)   │
  ├── Task 1.8 (exception hdl)  │
  │                              │
  ├── Task 1.4 (workdir)        ← depends on 1.3
  ├── Task 1.6 (resume valid)   ← depends on 1.4, 1.5
  ├── Task 1.9 (contract)       ← depends on 1.1
  └── Task 1.10 (delete stubs)  ← depends on 1.1
                │
Phase 2 (P0/P1 — infrastructure)
  ├── Task 2.1 (gates)          ← depends on Phase 1
  ├── Task 2.2 (logging)        ← depends on Phase 1
  ├── Task 2.3 (monitor)        ← depends on Phase 1
  ├── Task 2.4 (diagnostics)    ← depends on Phase 1
  ├── Task 2.5 (failures)       ← depends on 2.4
  ├── Task 2.6 (review)         ← depends on Phase 1
  └── Task 2.7 (TUI)            ← depends on 2.2
                │
Phase 3 (P1 — consolidation)
  ├── Task 3.1 (gates dedup)    ← depends on 2.1
  ├── Task 3.2 (convergence)    ← independent
  ├── Task 3.3 (resumable)      ← independent
  └── Task 3.4 (StepTiming)     ← depends on 2.2, 2.3
                │
Phase 4 (P2 — step bugs)
  ├── Task 4.1 (brainstorm)     ← depends on Phase 1
  ├── Task 4.2 (design_pipeline)← depends on Phase 1
  └── Task 4.3 (discover_comp)  ← depends on Phase 1

Phase 5 (LOW — opportunistic, no dependencies)
```

---

## Execution Strategy

**Recommended parallelization for `/sc:task-unified`:**

| Wave | Tasks | Rationale |
|------|-------|-----------|
| Wave 1 | 1.1, 1.2, 1.3, 1.5, 1.7, 1.8 | All independent P0 work |
| Wave 2 | 1.4, 1.6, 1.9, 1.10 | Depend on Wave 1 outputs |
| **Checkpoint** | **Run dry-run scenario** | **Verify pipeline executes** |
| Wave 3 | 2.1, 2.2, 2.3, 2.4, 2.6 | Independent infrastructure wiring |
| Wave 4 | 2.5, 2.7, 3.2, 3.3 | Depend on Wave 3 + independent consolidation |
| Wave 5 | 3.1, 3.4 | Depend on Wave 3 gate/logging wiring |
| **Checkpoint** | **Run gate failure scenario** | **Verify gates, logging, diagnostics** |
| Wave 6 | 4.1, 4.2, 4.3 | All independent step fixes |
| Wave 7 | Phase 5 (all) | Opportunistic cleanup |
| **Final** | **Run all 3 target scenarios** | **Acceptance criteria validation** |

---

## Acceptance Verification

After all phases complete, verify against audit acceptance criteria:

- [ ] AC-1: `superclaude cli-portify run <skill>` launches Claude subprocesses via PortifyProcess
- [ ] AC-2: Each successful step writes expected artifact to workdir
- [ ] AC-3: GATE_REGISTRY gates consulted after each step; failure halts pipeline
- [ ] AC-4: return-contract.yaml contains all 8 PortifyContract fields
- [ ] AC-5: Invalid inputs produce clean errors before subprocess launch
- [ ] AC-6: Each concept (gates, resumable-steps, convergence, step timing) has one canonical definition
- [ ] AC-7: Step modules pass gate checks with valid Claude output

---

*Generated from validated audit — 2026-03-23*
