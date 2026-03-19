# CLI Portify — Full Structural Audit Report

**Date:** 2026-03-18
**Scope:** `src/superclaude/cli/cli_portify/` (31 Python files)
**Branch:** `v3.0-AuditGates`
**Method:** 3-agent parallel Pass 2 structural audit with grep-backed evidence

---

## Executive Summary

The `cli-portify` CLI runner is **fundamentally non-functional**. The pipeline's entry point (`superclaude cli-portify run`) silently exits with code 0 after doing nothing. This is not a single bug — it is a systemic disconnection: the package contains ~4,500 lines of implemented infrastructure (subprocess execution, monitoring, diagnostics, TUI, logging, gate checking, failure handling, resume validation) that is **never wired into the execution path**.

### Issue Counts by Severity

| Severity | Count | Description |
|----------|-------|-------------|
| CRITICAL | 7 | Pipeline completely non-functional; entire subsystems disconnected |
| HIGH | 14 | Missing validations, dead modules, broken contracts, gate bypasses |
| MEDIUM | 18 | Logic bugs, duplicate code, wrong defaults, artifact path mismatches |
| LOW | 8 | Dead variables, unused imports, style issues |
| **Total** | **47** | |

### The Core Problem

```
superclaude cli-portify run sc-tasklist
  → commands.py: load_portify_config() ✓ (no validation)
  → executor.py: run_portify(config)
    → PortifyExecutor(step_runner=None)  ← CRITICAL: no step runner
      → _execute_step() → no-op fallback → (0, "", False) for ALL steps
      → every step classified as PASS_NO_SIGNAL
      → pipeline returns SUCCESS
      → zero Claude subprocesses launched
      → zero artifacts produced
      → zero gates checked
```

---

## Scope & Definition of Done

### What's In Scope for v3.6

**P0 — Pipeline Must Function (Phases 1-2, issues C-01 through C-07, H-01 through H-14):**
All 21 CRITICAL and HIGH issues. After v3.6, `superclaude cli-portify run <workflow>` must launch real Claude subprocesses, produce artifacts, check gates, and emit a schema-complete return contract.

**P1 — Consolidate Duplicates (Phase 3, issues M-01 through M-04, H-03):**
Eliminate the 5 duplicate systems (gates, convergence state, step timing, event vocabulary, resumable-steps) to prevent future divergence.

**P2 — Fix Step-Level Bugs (Phase 4, issues M-08 through M-16):**
Fix the 9 logic bugs in step modules that would cause incorrect behavior once the pipeline is wired.

### What's Out of Scope

- LOW issues (L-01 through L-08): cosmetic; fix opportunistically during implementation
- M-05 (no-op test fallbacks): deferred until test strategy is established
- M-06, M-07 (dead PROMPT_BUILDERS class, maybe_split_prompt): delete during Phase 3 if untouched
- M-17, M-18 (regex flag, dead variable): minor; fix opportunistically
- New features (new steps, new CLI options beyond what cli.py already defines)

### NFR Prioritization

| NFR | Priority | Rationale |
|-----|----------|-----------|
| SC-011 (return contract) | P0 | Downstream consumers depend on contract schema |
| SC-012 (--dry-run) | P0 | Already implemented, just needs wiring |
| D-0003 (PortifyContract) | P0 | Replace inline YAML with proper builders |
| D-0008 (portify-config.yaml) | P0 | Workdir setup is prerequisite for all steps |
| NFR-007 (execution log) | P1 | Important for debugging but not blocking |
| NFR-008 (TUI dashboard) | P2 | Nice-to-have; pipeline works without it |
| NFR-009 (stall detection) | P1 | Needed for long-running Claude subprocesses |
| R-001 (progress telemetry) | P1 | Needed for stall detection |
| FR-042 (diagnostics) | P1 | Valuable on failure but not blocking basic operation |
| FR-030-033 (convergence) | P0 | Already implemented in convergence.py; just needs wiring from panel_review |

### Acceptance Criteria

The release is **done** when all of the following are true:

1. **Subprocess execution**: `superclaude cli-portify run <valid-skill-dir>` launches Claude subprocesses via `PortifyProcess` for each pipeline step (verified by checking process spawn in execution log or return contract `step_timings`)
2. **Artifact production**: Each step that completes successfully writes its expected artifact to the workdir (e.g., `component-inventory.md`, `portify-analysis.md`, `portify-spec.md`)
3. **Gate enforcement**: `GATE_REGISTRY` gates are consulted after each step; a gate failure halts the pipeline with `GATE_FAILURE` status (not `PASS_NO_SIGNAL`)
4. **Return contract**: `return-contract.yaml` contains all 8 fields defined in `contract.py:PortifyContract` (including `phases`, `artifacts`, `step_timings`, `gate_results`)
5. **Config validation**: Invalid inputs (missing workflow path, non-existent SKILL.md, non-writable output dir) produce clean error messages before any subprocess is launched
6. **No duplicate systems**: Each concept (gates, resumable-steps, convergence state, step timing, event vocabulary) has exactly one canonical definition
7. **Step-level correctness**: All step modules pass their own gate checks when given valid Claude output (no bypassed gates, no inverted defaults, no wrong artifact paths)

### Target Scenarios

**Scenario 1 — Happy path:**
```
Given: A valid skill at ./src/superclaude/skills/sc-roadmap/ with SKILL.md
When:  superclaude cli-portify run sc-roadmap --output ./out
Then:  - workdir created at ./out/
       - Claude subprocess launched for each of 7+ steps
       - Artifacts written: component-inventory.md, portify-analysis.md, portify-spec.md, panel-report.md
       - Gates checked after each step (section counts, frontmatter, placeholder scan)
       - return-contract.yaml emitted with 8 fields, status=SUCCESS
       - Exit code 0
```

**Scenario 2 — Validation failure:**
```
Given: A non-existent path ./src/superclaude/skills/sc-fake/
When:  superclaude cli-portify run sc-fake --output ./out
Then:  - validate_portify_config() raises PortifyValidationError
       - Clean error message: "Workflow path does not exist: ..."
       - No subprocess launched, no workdir created
       - Exit code 1
```

**Scenario 3 — Gate failure mid-pipeline:**
```
Given: A valid skill, but Claude produces output missing required sections
When:  superclaude cli-portify run sc-roadmap --output ./out
Then:  - Steps 1-2 succeed, step 3 produces incomplete output
       - Gate SC-003 fails: "Missing required sections: ..."
       - Pipeline halts with GATE_FAILURE status
       - return-contract.yaml emitted with status=PARTIAL, failed_step identified
       - diagnostics.md emitted with failure context
       - Exit code 1
```

---

## Architectural Decisions

### AD-1: Step System — Hybrid approach (System A taxonomy + System B execution style)

**Decision**: Keep System A's 12-step `STEP_REGISTRY` taxonomy as the canonical pipeline model. Refactor System B's `steps/run_*()` modules to align with the registry step IDs and adopt their execution pattern (direct `PortifyProcess` usage, prerequisite checks, gate enforcement, artifact writing).

**Rationale**:

The codebase contains two competing step architectures:

| Dimension | System A (`executor.py execute_*_step()`) | System B (`steps/run_*()`) |
|-----------|------------------------------------------|---------------------------|
| Steps covered | 9 of 12 registry entries | 7 (different step vocabulary) |
| Step IDs | Match `STEP_REGISTRY` exactly | Different names (`analyze-workflow` vs `protocol-mapping`) |
| Subprocess | Optional `process_runner` param, no-op fallback | Direct `PortifyProcess` import and usage |
| Gates | None | Inline gate checks (SC-003, SC-004, SC-006) |
| Artifacts | Returns stdout; no file I/O | Writes artifacts, checks prerequisites |
| Error handling | Returns synthetic success tuple | Structured `PortifyStepResult` with failure classification |

Neither system is wired into `PortifyExecutor.run()` today. System A has the right taxonomy but stub implementations. System B has real execution behavior but a mismatched step vocabulary.

**Implementation plan**:
1. `PortifyExecutor._execute_step()` dispatches to step modules by step ID
2. Each step module exports a `run(config, workdir, process) -> PortifyStepResult` function
3. Step modules use `PortifyProcess` directly (System B pattern)
4. Step modules enforce gates from `GATE_REGISTRY` (not inline copies)
5. `execute_*_step()` free functions in executor.py are deleted (replaced by step modules)
6. New step modules are created for registry entries not covered by System B (`protocol-mapping`, `analysis-synthesis`, `step-graph-design`, `models-gates-design`, `prompts-executor-design`, `pipeline-spec-assembly`, `release-spec-synthesis`)

**What this resolves**: C-01, C-02, C-04, C-05, M-05

### AD-2: Gate System — `gates.py` is canonical; `steps/gates.py` is deleted

**Decision**: `gates.py` (top-level) with `GATE_REGISTRY` is the single source of gate definitions. `steps/gates.py` (duplicate) is deleted. Step modules import gates from `gates.py`.

**Rationale**: `gates.py` has comprehensive coverage (G-000 through G-011) and a registry pattern. `steps/gates.py` only covers Steps 1-2 with different implementations. One source prevents divergence.

**What this resolves**: M-01, H-13

### AD-3: CLI Interface — `cli.py` features merge into `commands.py`

**Decision**: Merge the useful options from `cli.py` (`--commands-dir`, `--skills-dir`, `--agents-dir`, `--include-agent`, `--save-manifest`, `--start`) into `commands.py`. Delete `cli.py`.

**Rationale**: `commands.py` is the live entry point (imported by `main.py:370`). `cli.py` is dead code with a newer option set. Merging preserves the improvements without maintaining two interfaces.

**What this resolves**: C-07

---

## Test Strategy

### Existing Test State

The current test suite (if any) tests against a no-op pipeline — every step returns `(0, "", False)` and is classified as `PASS_NO_SIGNAL`. These tests verify the no-op behavior, not real pipeline execution. They must be updated or replaced.

### Test Approach by Phase

**Phase 1 — Pipeline Wiring (integration tests)**:
- **Smoke test**: `superclaude cli-portify run <test-fixture-skill> --dry-run` completes with exit code 0 and emits `return-contract.yaml` with all 8 fields
- **Subprocess verification**: Mock `PortifyProcess.run()` to return canned output; verify executor dispatches to correct step module for each step ID
- **Config validation**: Test `validate_portify_config()` with invalid paths, missing files, non-writable dirs — verify `PortifyValidationError` raised with descriptive message
- **Gate failure**: Mock step output missing required sections; verify `GATE_FAILURE` status in return contract

**Phase 2 — Infrastructure Wiring (unit tests)**:
- **ExecutionLog**: Verify NDJSON entries written for step start/complete/fail events
- **OutputMonitor**: Verify stall detection callback fires after configurable timeout
- **DiagnosticsCollector**: Verify `diagnostics.md` emitted when executor catches exception
- **PortifyContract builders**: Verify `build_success_contract()`, `build_partial_contract()`, `build_failed_contract()` produce schema-compliant YAML

**Phase 3 — Consolidation (regression tests)**:
- **Single gate source**: Verify no imports from `steps/gates.py` remain
- **Single resumable-steps source**: Verify `RESUMABILITY_MATRIX`, `_RESUMABLE_STEPS`, and `RESUMABLE_STEPS` are consolidated

**Phase 4 — Step-level fixes (unit tests per step)**:
- **brainstorm_gaps**: Verify `has_section_12_content()` is called and gate failure is classified correctly
- **design_pipeline**: Verify `skip_review` defaults to `False`, `dry_run` halts before synthesis, artifact name matches
- **discover_components**: Verify artifact written to `results_dir`, not `config.output_dir`
- **panel_review**: Verify no `AttributeError` on `config.results_dir`

### Test Fixtures

Create a minimal test skill fixture at `tests/fixtures/test-skill/` with:
- `SKILL.md` (minimal valid frontmatter)
- A simple workflow directory structure
- Canned Claude output files for each step (for mock-based testing)

---

## Wiring Map

### What Is Connected (live execution path)

```
main.py:370 ─── commands.py:cli_portify_group ─── config.py:load_portify_config()
                      │
                      └── executor.py:run_portify()
                            │
                            └── PortifyExecutor(step_runner=None) ← ALL STEPS NO-OP
                                  │
                                  └── _emit_return_contract() (minimal 5-field YAML)
```

### What Is Disconnected (implemented but never called)

```
SUBPROCESS LAYER (never imported by executor):
  process.py ─── PortifyProcess (the actual Claude subprocess launcher)

INFRASTRUCTURE (never instantiated):
  monitor.py ─── OutputMonitor, EventLogger, TimingCapture
  diagnostics.py ─── DiagnosticsCollector
  logging_.py ─── ExecutionLog (NDJSON + Markdown)
  tui.py ─── PortifyTUI (Rich live dashboard)
  workdir.py ─── create_workdir(), emit_portify_config_yaml()
  failures.py ─── 7 typed failure handlers, FAILURE_HANDLERS registry
  resume.py ─── validate_resume_entry(), RESUMABILITY_MATRIX

STEP IMPLEMENTATIONS (never called from main loop):
  steps/validate_config.py ─── run_validate_config()
  steps/discover_components.py ─── run_discover_components()
  steps/analyze_workflow.py ─── run_analyze_workflow()
  steps/design_pipeline.py ─── run_design_pipeline()
  steps/synthesize_spec.py ─── run_synthesize_spec()
  steps/brainstorm_gaps.py ─── run_brainstorm_gaps()
  steps/panel_review.py ─── run_panel_review()

GATES (never consulted by executor):
  gates.py ─── GATE_REGISTRY, all semantic gate functions (G-000 through G-011)
  steps/gates.py ─── duplicate gate definitions for Steps 1-2

OTHER DEAD MODULES:
  cli.py ─── v2.24.1 entry point (never registered in main.py)
  review.py ─── ReviewDecision, review_gate() (duplicated inline in steps)
  resolution.py ─── resolve_target() (duplicated by config.py)
  registry.py ─── MANDATED_STEP_ORDER (code-gen metadata, not runtime)
  prompts.py ─── PROMPT_BUILDERS class registry, get_prompt_builder() factory
```

### Partial Connections (used but only from dead paths)

```
prompts.py standalone functions ── called by executor.py execute_*_step() functions
  BUT: execute_*_step() functions are never called by PortifyExecutor.run()

convergence.py ── called by steps/panel_review.py
  BUT: steps/panel_review.py is never called from main loop

utils.py (parse_frontmatter, count_lines, etc.) ── called by step modules
  BUT: step modules are never called from main loop

contract.py:build_dry_run_contract() ── called by steps/design_pipeline.py
  BUT: steps/design_pipeline.py is never called from main loop
```

---

## CRITICAL Issues (7)

### C-01: No step runner wired — entire pipeline is a no-op
- **File:** `executor.py:1463`
- **Evidence:** `PortifyExecutor(steps=steps, workdir=workdir, ...)` — `step_runner=` parameter absent
- **Impact:** `_execute_step()` (line 408-410) falls through to `exit_code, stdout, timed_out = 0, "", False` for every step. Zero Claude subprocesses launched, zero artifacts produced.
- **Root cause:** `process.py:PortifyProcess` exists and is fully implemented but never imported by `executor.py`

### C-02: process.py completely unwired
- **File:** `process.py` (entire file)
- **Evidence:** Grep for `from .process import` and `from superclaude.cli.cli_portify.process import` — only `steps/panel_review.py:34` imports it; `executor.py` has zero references
- **Impact:** The subprocess launcher (`PortifyProcess.run()`) that should back `step_runner` is never used

### C-03: No config validation before execution
- **File:** `commands.py:109`
- **Evidence:** `run_portify(config)` called directly; `validate_portify_config()` exists in `config.py:127` but is never imported or called by `commands.py`
- **Impact:** Invalid workflow paths, missing SKILL.md files, name collisions, and non-writable output dirs reach the executor instead of failing early with clean errors

### C-04: All 7 step implementations disconnected
- **Files:** `steps/validate_config.py`, `steps/discover_components.py`, `steps/analyze_workflow.py`, `steps/design_pipeline.py`, `steps/synthesize_spec.py`, `steps/brainstorm_gaps.py`, `steps/panel_review.py`
- **Evidence:** Grep for `run_validate_config`, `run_discover_components`, `run_analyze_workflow`, `run_design_pipeline`, `run_synthesize_spec`, `run_brainstorm_gaps`, `run_panel_review` — zero callers for each
- **Impact:** All step logic (subprocess invocation, artifact writing, gate checking) is bypassed

### C-05: 7 execute_*_step() functions in executor.py are unreachable
- **File:** `executor.py:509-1230`
- **Evidence:** `PortifyExecutor.run()` calls `_execute_step()` which checks `self._step_runner`; the `execute_*_step()` free functions are never dispatched to
- **Impact:** The Phase 5-8 step implementations (protocol-mapping, analysis-synthesis, step-graph-design, models-gates-design, prompts-executor-design, pipeline-spec-assembly, release-spec-synthesis) exist but are never called

### C-06: PortifyStep.output_file never set
- **File:** `executor.py:1454-1461`
- **Evidence:** Steps built from `STEP_REGISTRY` entries; `output_file` defaults to `None` (confirmed in `models.py:PortifyStep`)
- **Impact:** Even if `step_runner` were wired, `_determine_status()` would always see `artifact_path=None`, classifying every step as `PASS_NO_REPORT` instead of `PASS`

### C-07: cli.py (v2.24.1 interface) is dead code
- **File:** `cli.py` (entire file)
- **Evidence:** `main.py:370` imports from `commands.py`, not `cli.py`; grep for `from superclaude.cli.cli_portify.cli import` returns zero results
- **Impact:** The newer 11-option interface (`--commands-dir`, `--skills-dir`, `--agents-dir`, `--include-agent`, `--save-manifest`, `--start`) is unreachable; users run the older 7-option `commands.py` interface

---

## HIGH Issues (14)

### H-01: resume_from is an undeclared dynamic attribute
- **File:** `commands.py:107`, `models.py`
- **Evidence:** `config.resume_from = resume_step` with `# type: ignore[attr-defined]`; `PortifyConfig` dataclass has no `resume_from` field
- **Impact:** Fragile — any future `__slots__` or stricter model breaks resume silently

### H-02: validate_resume_entry() never called
- **File:** `resume.py` (entire file)
- **Evidence:** Grep for `validate_resume_entry` — zero callers outside resume.py
- **Impact:** `--resume <step>` proceeds without checking artifact prerequisites; missing artifacts cause runtime failures deep in the pipeline

### H-03: Three disjoint copies of resumable steps
- **Files:** `resume.py:RESUMABILITY_MATRIX`, `failures.py:28:_RESUMABLE_STEPS`, `contract.py:43:RESUMABLE_STEPS`
- **Impact:** Will diverge when pipeline steps change

### H-04: workdir.py never called — workdir not created
- **File:** `workdir.py`
- **Evidence:** Grep for `create_workdir` and `emit_portify_config_yaml` — zero callers
- **Impact:** D-0008 (`portify-config.yaml` emission) unimplemented; workdir existence not guaranteed before step execution

### H-05: Executor's return contract is schema-incomplete
- **File:** `executor.py:276-309`
- **Evidence:** `_emit_return_contract()` emits 5 fields via raw `yaml.safe_dump`; `contract.py:PortifyContract` specifies 8 fields (phases, artifacts, step_timings, gate_results missing)
- **Impact:** SC-011 nominally met but output schema wrong; `build_success_contract`, `build_partial_contract`, `build_failed_contract` are dead code

### H-06: Exception handling misses common error types
- **File:** `commands.py:111-116`
- **Evidence:** Only catches `PortifyValidationError` and `KeyboardInterrupt`; `RuntimeError`, `yaml.YAMLError`, `OSError`, `ImportError` all produce raw tracebacks

### H-07: process.py import chain may be broken
- **File:** `process.py`
- **Evidence:** Inherits from `ClaudeProcess` (`superclaude.cli.pipeline.process`); failure hidden because process.py is never imported by live path

### H-08: monitor.py completely unwired — NFR-009/R-001 unimplemented
- **File:** `monitor.py`
- **Evidence:** Grep for `OutputMonitor`, `EventLogger`, `TimingCapture` — zero callers
- **Impact:** Stall detection not running; no progress telemetry

### H-09: diagnostics.py completely unwired — FR-042 unimplemented
- **File:** `diagnostics.py`
- **Evidence:** Grep for `DiagnosticsCollector`, `emit_diagnostics` — zero callers
- **Impact:** No `diagnostics.md` on pipeline failure

### H-10: logging_.py completely unwired — NFR-007 unimplemented
- **File:** `logging_.py`
- **Evidence:** Grep for `ExecutionLog` — zero callers
- **Impact:** No `execution-log.jsonl` or `execution-log.md` produced

### H-11: tui.py completely unwired — NFR-008 unimplemented
- **File:** `tui.py`
- **Evidence:** Grep for `PortifyTUI`, `TuiDashboard` — zero callers
- **Impact:** No live dashboard; also step list in TUI doesn't match STEP_REGISTRY

### H-12: failures.py completely unwired — failure handlers dead
- **File:** `failures.py`
- **Evidence:** Grep for `FAILURE_HANDLERS`, `handle_missing_template` etc. — zero callers
- **Impact:** Fine-grained failure classification never applied

### H-13: GATE_REGISTRY and all semantic gates bypassed
- **File:** `gates.py`
- **Evidence:** Grep for `GATE_REGISTRY`, `get_gate_criteria` in executor.py — zero hits
- **Impact:** Section-count checks, frontmatter validation, placeholder scanning never run

### H-14: review.py completely disconnected
- **File:** `review.py`
- **Evidence:** Grep for `review_gate`, `ReviewDecision`, `REVIEW_GATE_STEPS` — zero callers
- **Impact:** Canonical review abstraction unused; duplicated inline in steps/design_pipeline.py and steps/panel_review.py

---

## MEDIUM Issues (18)

### M-01: Duplicate gate systems — steps/gates.py vs gates.py
- **Files:** `steps/gates.py`, `gates.py`
- **Evidence:** Both define `VALIDATE_CONFIG_GATE`, `DISCOVER_COMPONENTS_GATE`, `gate_validate_config()`, `gate_discover_components()` with different implementations

### M-02: Duplicate ConvergenceState enums
- **Files:** `convergence.py`, `models.py:136`
- **Evidence:** `models.py` defines a parallel `ConvergenceState` that is never used by panel_review (which imports from convergence.py)

### M-03: Duplicate StepTiming dataclasses
- **Files:** `contract.py:79`, `monitor.py:134`
- **Evidence:** Two `StepTiming` dataclasses with overlapping fields

### M-04: Three overlapping event vocabulary sets
- **Files:** `logging_.py`, `monitor.py`, `utils.py`
- **Evidence:** Each defines its own event-type constants with different names for the same concepts

### M-05: executor.py execute_*_step() no-op fallbacks fabricate success
- **File:** `executor.py:536-543`
- **Evidence:** Each returns `(0, EXIT_RECOMMENDATION_MARKER + " CONTINUE", False)` when `process_runner=None`
- **Impact:** Tests using these functions verify nothing real

### M-06: PROMPT_BUILDERS class registry is dead code
- **File:** `prompts.py`
- **Evidence:** `get_prompt_builder()` factory never called; 5 class builders unreferenced

### M-07: maybe_split_prompt() never called
- **File:** `prompts.py`
- **Evidence:** Defined but zero callers found

### M-08: brainstorm_gaps.py SC-006 gate bypassed
- **File:** `steps/brainstorm_gaps.py`
- **Evidence:** `has_section_12_content()` defined but never called by `run_brainstorm_gaps()` — artifact written and PASS returned without gate check

### M-09: brainstorm_gaps.py wrong failure classification
- **File:** `steps/brainstorm_gaps.py:191`
- **Evidence:** Subprocess failure classified as `MISSING_ARTIFACT` instead of `GATE_FAILURE`

### M-10: design_pipeline.py skip_review default inverted
- **File:** `steps/design_pipeline.py:158`
- **Evidence:** `getattr(config, "skip_review", True)` — default `True` means review is always skipped

### M-11: design_pipeline.py dry_run checked post-gate
- **File:** `steps/design_pipeline.py:136-155`
- **Evidence:** Artifact written and gate checked before dry_run halt; spec says dry_run should halt before synthesis

### M-12: design_pipeline.py artifact name mismatch
- **File:** `steps/design_pipeline.py:33`
- **Evidence:** `ARTIFACT_NAME = "portify-spec.md"` but docstring says `portify-pipeline-design.md`

### M-13: design_pipeline.py SC-004 gate checks unrequested field
- **File:** `steps/design_pipeline.py:209`
- **Evidence:** Checks `pipeline_steps` in frontmatter but prompt never instructs Claude to produce it

### M-14: discover_components.py writes artifact to wrong path
- **File:** `steps/discover_components.py:553`
- **Evidence:** Writes to `config.output_dir` not `results_dir`; downstream step expects `results_dir / "component-inventory.md"`

### M-15: discover_components.py _build_simple_tree result unused
- **File:** `steps/discover_components.py:557-558`
- **Evidence:** `tree = _build_simple_tree(workflow_dir, config)` assigned but never passed to render function

### M-16: panel_review.py config.results_dir would raise AttributeError
- **File:** `steps/panel_review.py:285`
- **Evidence:** `config.results_dir` is not a field on `PortifyConfig`; no `getattr` guard

### M-17: has_criticals_addressed() regex single-line only
- **File:** `gates.py:236`
- **Evidence:** Negative lookahead without `re.DOTALL`; multi-line findings incorrectly flagged

### M-18: resolution.py dead local variable
- **File:** `resolution.py:261`
- **Evidence:** `resolved = ...` assigned in `_find_command_for_skill()` but never used

---

## LOW Issues (8)

### L-01: __init__.py unfilled `<skill_name>` template placeholder
### L-02: config.py import ordering in _find_cli_root()
### L-03: models.py lazy `import re` inside function body
### L-04: discover_components.py unused `shutil` import
### L-05: synthesize_spec.py unused `MAX_RETRIES = 1` constant
### L-06: steps/validate_config.py dead `_classify_warnings()` function
### L-07: utils.py dead `SIGNAL_VOCABULARY` constants and `verify_additive_only()`
### L-08: convergence.py `SimpleBudgetGuard` never passed to engine

---

## NFR/Spec Compliance Gap

| Requirement | Status | Module | Issue |
|-------------|--------|--------|-------|
| SC-011 (return contract on all exits) | PARTIAL | executor.py, contract.py | Contract emitted but schema incomplete (5/8 fields) |
| SC-012 (--dry-run phase filtering) | DEAD | executor.py | Filtering logic exists but steps no-op anyway |
| D-0003 (PortifyContract schema) | DEAD | contract.py | Builder functions never called by executor |
| D-0008 (portify-config.yaml) | DEAD | workdir.py | `emit_portify_config_yaml()` never called |
| FR-042 (diagnostics on failure) | DEAD | diagnostics.py | `DiagnosticsCollector` never instantiated |
| NFR-007 (execution log) | DEAD | logging_.py | `ExecutionLog` never instantiated |
| NFR-008 (TUI dashboard) | DEAD | tui.py | `PortifyTUI` never instantiated |
| NFR-009 (stall detection) | DEAD | monitor.py | `OutputMonitor` never instantiated |
| R-001 (progress telemetry) | DEAD | monitor.py | `TimingCapture` never instantiated |
| FR-030-033 (convergence loop) | DEAD | convergence.py | Implemented but only reachable from dead step |

---

## Per-File Classification

| File | Status | Severity | Notes |
|------|--------|----------|-------|
| `__init__.py` | KEEP | LOW | Template placeholder unfilled |
| `commands.py` | KEEP+FIX | CRITICAL | Missing validation, limited exception handling |
| `config.py` | KEEP | OK | validate_portify_config() correct but uncalled |
| `executor.py` | KEEP+FIX | CRITICAL | No step_runner, no output_file, unreachable execute_*_step() |
| `process.py` | KEEP+WIRE | CRITICAL | Fully implemented, completely unwired |
| `models.py` | KEEP+FIX | HIGH | Missing resume_from field |
| `cli.py` | CONSOLIDATE | CRITICAL | Dead v2.24.1 entry point; merge into commands.py or replace |
| `monitor.py` | KEEP+WIRE | HIGH | Implemented, unwired |
| `diagnostics.py` | KEEP+WIRE | HIGH | Implemented, unwired |
| `convergence.py` | KEEP | OK | Used by panel_review (itself dead from main loop) |
| `resume.py` | KEEP+WIRE | HIGH | Implemented, unwired; 3 copies of resumable-steps |
| `contract.py` | KEEP+WIRE | HIGH | Builders unused; executor uses inline version |
| `logging_.py` | KEEP+WIRE | HIGH | Implemented, unwired |
| `workdir.py` | KEEP+WIRE | HIGH | Implemented, unwired |
| `failures.py` | KEEP+WIRE | HIGH | Implemented, unwired |
| `utils.py` | KEEP | LOW | Some dead constants; active functions used by steps |
| `tui.py` | KEEP+WIRE | HIGH | Implemented, unwired; step list stale |
| `review.py` | CONSOLIDATE | HIGH | Duplicated inline by step modules |
| `resolution.py` | CONSOLIDATE | MEDIUM | Duplicated by config.py path resolution |
| `registry.py` | REVIEW | HIGH | Misleading name; may be deletable |
| `prompts.py` | KEEP | MEDIUM | Standalone functions live; class registry dead |
| `gates.py` | KEEP+WIRE | HIGH | Comprehensive gates, never consulted by executor |
| `steps/__init__.py` | KEEP | OK | Package marker |
| `steps/validate_config.py` | KEEP+WIRE | CRITICAL | Implemented, disconnected |
| `steps/discover_components.py` | KEEP+FIX | CRITICAL+MEDIUM | Disconnected, artifact path wrong |
| `steps/analyze_workflow.py` | KEEP+WIRE | CRITICAL | Implemented, disconnected |
| `steps/design_pipeline.py` | KEEP+FIX | CRITICAL+HIGH | Disconnected, multiple logic bugs |
| `steps/synthesize_spec.py` | KEEP+WIRE | CRITICAL | Implemented, disconnected |
| `steps/brainstorm_gaps.py` | KEEP+FIX | CRITICAL+HIGH | Disconnected, gate bypassed |
| `steps/panel_review.py` | KEEP+FIX | CRITICAL+HIGH | Disconnected, AttributeError risk |
| `steps/gates.py` | CONSOLIDATE | MEDIUM | Duplicates top-level gates.py |

---

## Recommended Fix Order

### Phase 1: Make the pipeline actually run (fixes C-01 through C-07, H-01 through H-06) [P0]
1. Implement AD-1: Refactor `_execute_step()` to dispatch to step modules by step ID via `PortifyProcess` (fixes C-01, C-02, C-04, C-05)
2. Set `output_file` and `error_file` on each `PortifyStep` built from `STEP_REGISTRY` (fixes C-06)
3. Call `validate_portify_config()` before `run_portify()` in `commands.py` (fixes C-03)
4. Call `create_workdir()` before executor construction (fixes H-04)
5. Add `resume_from` field to `PortifyConfig` dataclass (fixes H-01)
6. Wire `validate_resume_entry()` into resume path (fixes H-02)
7. Implement AD-3: Merge `cli.py` options into `commands.py`, delete `cli.py` (fixes C-07)
8. Broaden exception handling in `commands.py` (fixes H-06)
9. Verify `process.py` import chain for `ClaudeProcess` (fixes H-07)
10. Replace inline YAML in `_emit_return_contract()` with `PortifyContract` builders (fixes H-05)
11. Delete `execute_*_step()` free functions from executor.py (per AD-1)

### Phase 2: Wire infrastructure (fixes H-08 through H-14) [P0/P1]
12. Wire `GATE_REGISTRY` into step dispatch post-completion checks (fixes H-13) [P0]
13. Instantiate `ExecutionLog` in executor, call logging methods in step loop (fixes H-10) [P1]
14. Instantiate `OutputMonitor` with stall detection callback (fixes H-08) [P1]
15. Wire `DiagnosticsCollector` into executor's `finally` block (fixes H-09) [P1]
16. Wire `PortifyTUI` into executor with TTY detection (fixes H-11) [P2]
17. Wire canonical `review.py` into step modules, remove inline duplicates (fixes H-14) [P1]

### Phase 3: Consolidate duplicates (fixes M-01 through M-04, H-03) [P1]
18. Implement AD-2: Delete `steps/gates.py`, use `gates.py` exclusively (fixes M-01)
19. Remove duplicate `ConvergenceState` from `models.py` (fixes M-02)
20. Consolidate 3 copies of resumable-steps into single source in `resume.py` (fixes H-03)
21. Consolidate `StepTiming` into single definition in `contract.py` (fixes M-03)
22. Consolidate event vocabulary into single module (fixes M-04)

### Phase 4: Fix step-level bugs (fixes M-08 through M-16) [P2]
23. Fix gate bypass in brainstorm_gaps.py — call `has_section_12_content()` (fixes M-08)
24. Fix wrong failure classification in brainstorm_gaps.py (fixes M-09)
25. Fix inverted `skip_review` default in design_pipeline.py (fixes M-10)
26. Fix dry_run ordering in design_pipeline.py — halt before synthesis (fixes M-11)
27. Fix artifact name mismatch in design_pipeline.py (fixes M-12)
28. Remove unrequested frontmatter check in design_pipeline.py (fixes M-13)
29. Fix artifact path in discover_components.py — use `results_dir` (fixes M-14)
30. Fix unused `_build_simple_tree` result in discover_components.py (fixes M-15)
31. Fix `config.results_dir` AttributeError in panel_review.py (fixes M-16)

---

*Generated by 3-agent parallel structural audit — 2026-03-18*
