# CLI Unwired Components Audit

**Target:** `src/superclaude/cli/`
**Date:** 2026-03-18
**Scope:** Call graph tracing, import chain analysis, dead-code detection
**Method:** Exhaustive grep + cross-reference across `src/superclaude/`

---

## Category 1: `Optional[Callable]=None` Params Never Populated

11 callable parameters exist that are **never passed a non-None value** at any call site in the entire `src/superclaude/` tree.

| # | File:Line | Parameter | Function/Method |
|---|---|---|---|
| 1 | `audit/spot_check.py:81` | `reclassify_fn` | `spot_check_validate()` |
| 2 | `roadmap/executor.py:723` | `halt_fn` | `_check_remediation_budget()` |
| 3 | `cli_portify/monitor.py:216` | `kill_fn` | `StallDetector.__init__()` |
| 4 | `cli_portify/executor.py:333` | `step_runner` | `PortifyExecutor.__init__()` |
| 5 | `cli_portify/executor.py:513` | `process_runner` | `execute_protocol_mapping_step()` |
| 6 | `cli_portify/executor.py:568` | `process_runner` | `execute_analysis_synthesis_step()` |
| 7 | `cli_portify/executor.py:729` | `process_runner` | `execute_step_graph_design_step()` |
| 8 | `cli_portify/executor.py:789` | `process_runner` | `execute_models_gates_design_step()` |
| 9 | `cli_portify/executor.py:844` | `process_runner` | `execute_prompts_executor_design_step()` |
| 10 | `cli_portify/executor.py:958` | `process_runner` | `execute_pipeline_spec_assembly_step()` |
| 11 | `cli_portify/executor.py:1207` | `process_runner` | `execute_release_spec_synthesis_step()` |

**Wired (for reference):** `pipeline/process.py:49-51` (`on_spawn`, `on_signal`, `on_exit`) — populated from `sprint/process.py:117-119`.

**Assessment:** Items 5–11 share the same `process_runner` pattern — a testing seam that was never connected. Item 4 (`step_runner`) is a broader executor injection that's similarly phantom. Items 1–3 are one-off hooks with no callers.

---

## Category 2: Dispatch Table Entries with No-Op/Stub Executors

### 2a. Explicit None entries in dispatch tables

| # | File:Line | Registry | Entry | Value |
|---|---|---|---|---|
| 1 | `cli_portify/failures.py:331` | `FAILURE_HANDLERS` | `USER_REJECTION` | `None` |
| 2 | `cli_portify/failures.py:333` | `FAILURE_HANDLERS` | `GATE_FAILURE` | `None` |

These are explicit `None` entries — documented as "handled elsewhere" but with no alternative handler wired. The accessor functions `has_handler()` (line 337) and `get_failure_handler_name()` (line 342) are also **never called** from outside their own module.

### 2b. Entire registries with zero external consumers

| # | File:Line | Registry | Accessor | External Callers |
|---|---|---|---|---|
| 3 | `cli_portify/prompts.py:347` | `PROMPT_BUILDERS` | `get_prompt_builder()` | **0** |
| 4 | `cli_portify/gates.py:447` | `GATE_REGISTRY` | `get_gate_criteria()` | **0** |
| 5 | `cli_portify/failures.py:324` | `FAILURE_HANDLERS` | `has_handler()`, `get_failure_handler_name()` | **0** |

All three registries define factory/accessor functions that are never invoked from outside their own file. The `PROMPT_BUILDERS` registry maps step names to `BasePromptBuilder` subclasses; `GATE_REGISTRY` maps step names to `GateCriteria`; `FAILURE_HANDLERS` maps `FailureClassification` enums to handler callables. Each has a well-defined API surface that nothing uses.

---

## Category 3: Gate Classes Instantiated but Never Registered with Enforcement

### 3a. Dead gate policy layer

| # | File:Line | Symbol | Status |
|---|---|---|---|
| 1 | `sprint/executor.py:50` | `SprintGatePolicy` | **Defined, never instantiated.** Implements `TrailingGatePolicy` protocol but no call site creates it. |
| 2 | `pipeline/trailing_gate.py:227` | `TrailingGatePolicy` | Protocol only — `SprintGatePolicy` is the sole implementor, which is itself dead. |
| 3 | `pipeline/trailing_gate.py:593` | `resolve_gate_mode()` | Exported in `__init__.py`, **never called** anywhere. |
| 4 | `pipeline/trailing_gate.py:585` | `GateScope` | Exported in `__init__.py`, **only used by `resolve_gate_mode()`** — transitively dead. |

### 3b. Dead audit gate modules

| # | File:Line | Symbol | Status |
|---|---|---|---|
| 5 | `audit/evidence_gate.py:71` | `evidence_gate()` | **Defined, zero callers.** |
| 6 | `audit/evidence_gate.py:20` | `GateResult` (evidence) | Only produced by `evidence_gate()` — transitively dead. |
| 7 | `audit/manifest_gate.py:102` | `check_manifest_completeness()` | **Defined, zero callers.** |
| 8 | `audit/manifest_gate.py:65` | `GateResult` (manifest) | Only produced by `check_manifest_completeness()` — transitively dead. |

### 3c. Dead cli_portify gate layer

| # | File:Line | Symbol | Status |
|---|---|---|---|
| 9 | `cli_portify/gates.py:479` | `gate_analyze_workflow()` | Zero callers |
| 10 | `cli_portify/gates.py:495` | `gate_design_pipeline()` | Zero callers |
| 11 | `cli_portify/gates.py:528` | `gate_synthesize_spec()` | Zero callers |
| 12 | `cli_portify/gates.py:544` | `gate_brainstorm_gaps()` | Zero callers |
| 13 | `cli_portify/gates.py:559` | `gate_panel_review()` | Zero callers |
| 14 | `cli_portify/gates.py:586` | `gate_step_graph_design()` | Zero callers |
| 15 | `cli_portify/gates.py:602` | `gate_models_gates_design()` | Zero callers |
| 16 | `cli_portify/gates.py:618` | `gate_prompts_executor_design()` | Zero callers |
| 17 | `cli_portify/gates.py:634` | `gate_pipeline_spec_assembly()` | Zero callers |
| 18 | `cli_portify/steps/gates.py:51` | `gate_validate_config()` | Zero callers |
| 19 | `cli_portify/steps/gates.py:82` | `gate_discover_components()` | Zero callers |
| 20 | `cli_portify/gates.py:43` | `GateFailure` | Type used in diagnostics, but **never instantiated** — no producer creates one. |

The executor (`cli_portify/executor.py`) implements bespoke inline checks rather than routing through `GATE_REGISTRY` → `get_gate_criteria()` → `gate_*()` functions. This entire abstraction layer is dead weight.

### 3d. Orphaned gate criteria

| # | File:Line | Symbol | Status |
|---|---|---|---|
| 21 | `roadmap/gates.py:885` | `DEVIATION_ANALYSIS_GATE` | Defined as `GateCriteria`, **never attached to any `Step`**. |

---

## Severity Summary

| Severity | Count | Symbols |
|---|---|---|
| **High** | 4 subsystems | `SprintGatePolicy` chain (4 symbols), `evidence_gate` module (2 symbols), `manifest_gate` module (2 symbols), `cli_portify` gate registry (12 symbols) |
| **Medium** | 11 | Never-populated `Optional[Callable]=None` params — testing seams with no tests using them |
| **Low** | 5 | Exported-but-unused: `resolve_gate_mode`, `GateScope`, `PROMPT_BUILDERS` accessor, `FAILURE_HANDLERS` accessors, `DEVIATION_ANALYSIS_GATE` |

**Total unwired components: 32 symbols across 14 files.**

---

## Actively Wired (for contrast)

These gate-related components are confirmed live:

| Symbol | Instantiation | Enforcement |
|---|---|---|
| `GateCriteria` | roadmap, tasklist, cleanup_audit, cli_portify gate modules | Attached to `Step.gate`, checked by `gate_passed()` |
| `gate_passed()` | — | Called from `pipeline/executor.py:214`, `cleanup_audit/executor.py:139`, roadmap resume paths |
| `TrailingGateRunner` | `pipeline/executor.py:85` | `.submit()` at `:201`, `.wait_for_pending()` at `:126` |
| `GateResultQueue` | Internal to `TrailingGateRunner` | `.put()` / `.drain()` used within runner |
| `ALL_GATES` (cleanup_audit) | `cleanup_audit/gates.py:148` | All 6 entries referenced in `cleanup_audit/executor.py` |
| `CLASSIFIERS` (sprint) | `sprint/classifiers.py:16` | `run_classifier()` called from `sprint/preflight.py:145` |
| `ClaudeProcess` callbacks | `on_spawn`, `on_signal`, `on_exit` | Populated from `sprint/process.py:117-119` |

---

## Recommended Actions

### Wire or remove the cli_portify gate layer
The `GATE_REGISTRY` + 10 `gate_*()` functions + `get_gate_criteria()` accessor form a complete but disconnected abstraction. Either:
- **Wire:** Refactor `cli_portify/executor.py` to call `get_gate_criteria()` → `gate_passed()` instead of inline checks
- **Remove:** Delete `cli_portify/gates.py:447-651` and `cli_portify/steps/gates.py:51-110`

### Wire or remove audit gate modules
`evidence_gate.py` and `manifest_gate.py` define gate functions with zero callers. Either integrate into the audit executor pipeline or remove.

### Wire or remove SprintGatePolicy
`SprintGatePolicy` implements `TrailingGatePolicy` but is never instantiated. Either wire it into sprint executor or remove along with the dead `resolve_gate_mode()` / `GateScope` chain.

### Clean up phantom callable params
The 7 `process_runner` params in `cli_portify/executor.py` and the `step_runner` param represent a testing injection pattern that was never used. Either add tests that use them or remove the params to reduce API surface noise.
