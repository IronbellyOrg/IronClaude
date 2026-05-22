# D-0046 — EvalResult implementation notes

## Design decisions

### Frozen dataclass

T03.02 only says "EvalResult dataclass" (T03.01 explicitly says "frozen", T03.03 explicitly says "frozen"). We chose **frozen** anyway to match the rest of the eval-models surface: every record the Reporter consumes is immutable so consumers cannot mutate cached state mid-render. `__post_init__` uses `object.__setattr__` to overwrite `duration_sec`, which is the documented escape hatch for frozen dataclasses.

### Timestamp representation

DM-003 enumerates `start` / `end` without prescribing a Python type. The task **Steps** explicitly choose ISO 8601 strings (Step 2: "Choose datetime representation (ISO 8601 strings)"). Rationale:

- The values round-trip through `json.dumps` with no custom encoder.
- The Reporter forwards them verbatim into `summary.json`.
- We still need duration arithmetic, which is handled by `datetime.fromisoformat(...)` at `__post_init__` time. Python 3.11+ `fromisoformat` accepts all reasonable ISO 8601 variants; the project targets `>=3.10` and uses 3.12 in CI.

### `duration_sec` overwrite vs. validate

We considered three options for keeping `duration_sec` consistent with timestamps:

1. **Validate** (raise `ValueError` if `duration != end - start`). Rejected — too strict for the partial-summary path on SIGINT, where the runner may not have written `end` yet.
2. **Overwrite unconditionally**. Rejected — destroys the partial-summary use case entirely.
3. **Overwrite when both timestamps are non-empty, otherwise honour the caller's value** (chosen). This satisfies the "consistently" wording in the AC for happy-path runs, while keeping the partial summary path constructible. Both behaviours are explicitly tested (`test_eval_result_duration_sec_caller_value_is_overwritten` and `test_eval_result_duration_sec_kept_when_timestamps_missing`).

### `error` serialisation shape

DM-003 types `error` as `Optional[Exception]`. Live `BaseException` instances do not pass through `json.dumps`, so `to_dict()` must lower them into a JSON-safe shape. We chose `{"type": "<fully.qualified.ClassName>", "message": str(error)}` over the alternatives:

- **`str(error)` only.** Rejected — loses the exception class, which the Reporter uses to group identical harness failures across runs (mirroring the `error_class` rationale in DM-001).
- **`repr(error)`.** Rejected — repr formatting drifts across Python versions and exception subclasses.
- **Include the full traceback.** Rejected — the per-eval JSONL log (T03.05) is the authoritative traceback source; DM-003's `error` is the Reporter-facing summary handle, not a forensics record.

The implementation lives in `_render_error()`; `dataclasses.asdict` is intentionally **not** used because it would attempt to recurse into the exception instance.

### Why both `EvalOutcome` *and* `EvalResult` exist

DM-001 (EvalOutcome) and DM-003 (EvalResult) intentionally separate two concerns:

- **EvalOutcome** — the *assertions-and-status* record the runner emits. Drives exit-code logic and the N′-vs-K invariant guard (FR-RPT1 / T03.11).
- **EvalResult** — the *stdout/stderr-and-timing* envelope the Reporter consumes. Carries the captured streams, lifecycle timestamps, and harness-level error.

The pair travels together: a runner finishes its lifecycle, builds an `EvalOutcome`, then wraps it in an `EvalResult` with the captured I/O and timing. The Reporter never reads them independently.

## Future work touchpoints

- **T03.04 / T03.05 (EvalRunner)** — will be the construction site for `EvalResult`. The runner must capture monotonic timestamps in ISO 8601 and feed them in.
- **T03.13 (Reporter)** — will consume `EvalResult.to_dict()` per row of `evals[]` in `summary.json` (DM-012 / T03.10 defines the surrounding schema).
- **T03.15 (RunOrchestrator)** — will collect one `EvalResult` per expanded spec from the worker pool and forward them to the Reporter alongside the `RunSummary` (DM-004 / T03.09).
