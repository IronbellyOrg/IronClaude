# D-0047 — EvalContext runtime record spec

**Task:** T03.03 (Phase 3, Roadmap DM-010 / R-047)
**Module:** `src/superclaude/cli/eval/models.py`
**Status:** Implemented 2026-05-20

## Field schema (15-field contract)

Field declaration order matches DM-010 verbatim so attribute traversal,
factory construction, and any future `to_dict()` consumer iterate in the
same canonical order the roadmap row enumerates.

| #  | Field             | Type                  | Default  | Purpose |
|----|-------------------|-----------------------|----------|---------|
| 1  | `eval_spec`       | `EvalSpec` (DM-002)   | required | Parsed manifest row. Stored by-reference; `EvalSpec` is itself frozen so the runner cannot mutate the spec after the context is built. |
| 2  | `home`            | `HomeIsolation` (DM-006) | required | Per-eval isolation record. Carries `eval_id`, `home_root`, `session_id`, `time_offset_sec` and the COMP-006 method surface; ExpectCallables that need `home.env()` / `home.state_path(...)` use it directly. |
| 3  | `home_path`       | `Path`                | required | The per-eval `HOME` directory created by `HomeIsolation.setup`. The factory keeps the `home.home_path == home_path` invariant so callers do not have to re-dereference the property. |
| 4  | `artifacts_dir`   | `Path`                | required | Directory the runner writes per-eval artifacts under (PTY transcripts, hook outputs, captured side-cars). Resolved beneath `home_path`. |
| 5  | `run_dir`         | `Path`                | required | The run-scoped scratch directory the orchestrator (FR-G2 / T03.16) created. One `run_dir` per `superclaude eval run` invocation. |
| 6  | `env`             | `Mapping[str, str]`   | required | Environment variables exported to the Claude subprocess. Wrapped in `types.MappingProxyType` so mutation raises `TypeError`. |
| 7  | `stdout_path`     | `Path`                | required | Path of the captured (PTY-stripped) stdout transcript. `Expect.stdout` opens this. |
| 8  | `stderr_path`     | `Path`                | required | Path of the captured stderr transcript. |
| 9  | `transcript_path` | `Path`                | required | Path to the raw PTY transcript (pre-strip, ANSI escapes preserved). |
| 10 | `jsonl_paths`     | `Mapping[str, Path]`  | required | Named JSONL log file paths (e.g. `{"hook_log": ..., "telemetry": ...}`). Wrapped in `MappingProxyType`. `Expect.jsonl(name=..., ...)` resolves through this mapping. |
| 11 | `exit_code`       | `int`                 | required | Captured exit code of the Claude subprocess after `wait()`. `Expect.exit_code` reads it. |
| 12 | `stdout`          | `str`                 | required | Full captured stdout. Mirrors `stdout_path` so primitives can read it in-memory. |
| 13 | `stderr`          | `str`                 | required | Full captured stderr. |
| 14 | `duration_sec`    | `float`               | required | Wall-clock seconds the eval body ran (spawn to exit). `Expect.duration` reads this verbatim. |
| 15 | `artifacts`       | `Mapping[str, str]`   | required | Artifact-name to absolute (or run-relative) path mapping. Mirrors `EvalOutcome.artifacts` (DM-001). Wrapped in `MappingProxyType`. |

## Invariants

- `@dataclass(frozen=True)` — attribute mutation raises `dataclasses.FrozenInstanceError` (covered by `test_eval_context_is_frozen` and the per-field `test_eval_context_every_field_is_frozen[*]` parametrisation).
- Field declaration order matches DM-010 verbatim (covered by `test_eval_context_has_required_fields` and `test_eval_context_field_order_constant_matches_dataclass`).
- Mapping fields (`env`, `jsonl_paths`, `artifacts`) are wrapped in `types.MappingProxyType` so the more subtle attack of mutating `ctx.env["HOME"]` raises `TypeError` (covered by `test_eval_context_env_is_mapping_proxy`, `test_eval_context_jsonl_paths_is_mapping_proxy`, `test_eval_context_artifacts_is_mapping_proxy`).
- Direct `EvalContext(...)` construction also wraps mapping fields via `__post_init__` (covered by `test_eval_context_direct_construction_also_wraps_mappings`).
- `from_runner_state(...)` is keyword-only so future field additions cannot silently re-bind positional callers (covered by `test_from_runner_state_keyword_only_arguments`).
- `home.home_path == ctx.home_path` invariant holds after factory construction (covered by `test_from_runner_state_resolves_home_path_from_home`).
- Factory propagates `HomeIsolation.home_path` `RuntimeError` when setup has not run, surfacing the failure at context construction rather than later when an ExpectCallable reads `ctx.home_path` (covered by `test_from_runner_state_raises_when_home_not_setup`).
- Factory shallow-copies caller mappings into new `MappingProxyType` wrappers so caller mutation after construction cannot bleed into the context (covered by `test_eval_context_factory_isolates_env_from_caller_mutation`).
- Two factory calls with identical arguments produce equal instances (covered by `test_from_runner_state_is_deterministic`).
- Every kwarg lands on the corresponding attribute verbatim modulo proxy wrapping (covered by `test_from_runner_state_field_values_round_trip`).

## Factory

`EvalContext.from_runner_state(*, eval_spec, home, run_dir, artifacts_dir, stdout_path, stderr_path, transcript_path, jsonl_paths, env, exit_code, stdout, stderr, duration_sec, artifacts)` centralises three concerns the runner would otherwise have to repeat per emitted context:

1. **Resolves `home_path` off the `HomeIsolation` instance** so the runner does not duplicate `home.home_path` at the call site. The property accessor raises `RuntimeError` if `HomeIsolation.setup` has not run — exactly the failure the factory wants surfaced at context construction.
2. **Wraps the three mapping arguments** (`env`, `jsonl_paths`, `artifacts`) in `MappingProxyType(dict(...))` so the context's mapping fields are read-only views *and* isolated from caller mutation.
3. **Produces a deterministic instance**: every `EvalContext` built from the same arguments compares equal (the `@dataclass`-generated `__eq__` covers the 15 fields; mapping proxies compare equal when their underlying dicts do).

Keyword-only arguments are required so future field additions (e.g. when DM-010 grows a 16th field) do not silently re-order positional callers.

## Module symbol re-exports

`EvalContext` is re-exported from `superclaude.cli.eval` (`__init__.py`) so consumers (ExpectCallables, EvalRunner, RunOrchestrator) can import it without reaching into `models` (covered by `test_eval_context_reexported_from_package`).

## Caller contract (downstream consumers)

- **FR-EXP1 ExpectCallables** (T04.01..T04.07) — every `Expect.*` primitive accepts an `EvalContext` and returns an `ExpectResult`. The 15-field contract is the only surface they see.
- **COMP-004 EvalRunner** (T03.04 / T03.05) — construction site for `EvalContext` after the lifecycle's `observe` step has captured stdout/stderr/exit_code. The runner threads the assertion phase through `EvalContext.from_runner_state(...)`.
- **COMP-008 Reporter** (T03.13) — does *not* consume `EvalContext` directly. It consumes `EvalOutcome` + `EvalResult`; the assertion-phase data flows through `ExpectResult` records on the outcome.

## Acceptance criteria → implementation map

| AC bullet (T03.03)                                                                                          | Implementation site                                                                                                                                                |
|-------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Class `EvalContext` is frozen and exposes the 15 fields named in DM-010.                                    | `models.py` — `@dataclass(frozen=True) class EvalContext` (covered by `test_eval_context_has_required_fields`, `test_eval_context_is_frozen`).                     |
| `EvalContext` instances reject mutation (FrozenInstanceError on attempted set).                             | Frozen-dataclass `__setattr__` block (covered by `test_eval_context_every_field_is_frozen[*]`).                                                                    |
| `from_runner_state()` constructs an EvalContext from EvalSpec + HomeIsolation + run outputs deterministically. | `EvalContext.from_runner_state` keyword-only classmethod (covered by `test_from_runner_state_is_deterministic`, `test_from_runner_state_field_values_round_trip`). |
| `TASKLIST_ROOT/artifacts/D-0047/spec.md` records the contract.                                              | This file.                                                                                                                                                         |

## Out of scope for T03.03

- FR-LC1 lifecycle skeleton (T03.04) — the runner construction site for `EvalContext`.
- COMP-004 EvalRunner class (T03.05) — wraps FR-LC1 with per-eval JSONL logging.
- FR-EXP1 primitives (T04.01..T04.07) — backing implementations of `Expect.file` / `Expect.jsonl` / etc. that actually consume the context.
- Per-eval JSONL log format (T03.05) — the schema for the files `jsonl_paths` refers to.
- `to_dict()` for `EvalContext` — none of the planned consumers (ExpectCallables, runner) serialise the context; the field-order constant is in place for future need.
