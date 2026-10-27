# D-0048 — FR-LC1 EvalRunner lifecycle spec

**Task:** T03.04 (Phase 3, Roadmap FR-LC1 / R-048)
**Module:** `src/superclaude/cli/eval/runner.py`
**Status:** Implemented 2026-05-20

## Scope

T03.04 lands the FR-LC1 *lifecycle skeleton*: a single entrypoint
`run_eval(spec, ...) -> EvalOutcome` that executes the seven-step per-eval
sequence and enforces the status-mapping rules. The runner *class* that
COMP-004 (T03.05) layers on top — per-eval JSONL logging, per-eval
timeout, parallel orchestration handoff — is explicitly out of scope here
(see §"Out of scope for T03.04" below).

The skeleton is fully testable without a real PTY: the spawn / inject /
observe trio is injected as a `LifecycleExecutor` protocol so unit tests
substitute stubs that return canned exit codes and transcripts. T03.05
plugs in the concrete `PtyDriver` + `ClaudeProcessAdapter` executor.

## 7-step lifecycle (FR-LC1)

The sequence below is executed verbatim by `run_eval`. Each step name
matches the design-spec diagram (`design-spec.md §6`) and the roadmap row
(R-048) so artefact lookups stay grepable.

| # | Step | Implementation site | Allowed exception → status |
|---|---|---|---|
| 1 | **build isolation** | `HomeIsolation.setup(config=...)` (T02.11 / D-0032). Atomic-setup wrapper (T02.13) is honoured — partial HOMEs stay on disk for forensics. | `HomeContainmentViolation` / `RuntimeError` / `OSError` → **ERRORED** (`teardown(keep=True)`). |
| 2 | **deploy hooks** | `deploy_hooks_to(home_path)` (T02.14 / D-0034). Caller-injectable so tests stub the deploy without a real `hooks.json`. | `HookDeployFailed` / `OSError` → **ERRORED** (`teardown(keep=True)`). |
| 3 | **spawn** | `executor.spawn(ctx)` — production wires `ClaudeProcessAdapter.spawn()` + `PtyDriver.spawn()` (T02.16 / T02.19). | Any `BaseException` other than `KeyboardInterrupt` / `SystemExit` → **ERRORED** (`teardown(keep=True)`). `KeyboardInterrupt` / `SystemExit` propagates so NFR-REL1 (T03.07) can mark **INTERRUPTED**. |
| 4 | **inject** | `executor.inject(ctx, prompts)` — production wires `PtyDriver.inject_prompt` and the manifest's `inputs[*]`. | Same propagation rule as step 3. |
| 5 | **observe** | `executor.observe(ctx) -> ObservedRun` — production drains `PtyDriver.read_stdout` until exit and captures `(stdout, stderr, exit_code, duration_sec, transcript_path)`. Per-eval JSONL log lives in T03.05; per-eval timeout lives in T03.07. | `TimeoutError` reserved for T03.07 → **TIMEOUT** (skeleton routes through `ERRORED` mapping today; T03.07 swaps the branch). Other exceptions → **ERRORED**. |
| 6 | **assert** | Each `ExpectCallable(ctx)` (FR-EXP1 / T04.01..T04.07 land later) is invoked. The runner builds an `EvalContext` via `EvalContext.from_runner_state(...)` (T03.03) once observe returns and passes it to every callable. | Any callable that raises → **ERRORED** with `error_class = "<fqcn>"`. Any callable that returns an `ExpectResult` with `passed=False` → **FAIL**. All `passed=True` → **PASS**. |
| 7 | **teardown** | `home.teardown(keep=...)`. `keep` is forced to `True` for any non-PASS outcome so failed/errored evals retain their HOME for post-mortem; PASS outcomes honour the caller's `keep_home_on_pass` (default `False`). Teardown failures are *swallowed* — they do not flip status from PASS to FAIL (the design-spec invariant: teardown is best-effort). | Logged via the optional `on_teardown_error` callback; never re-raised. |

The runner returns an `EvalOutcome` (DM-001 / T03.01) reflecting the
classified status, the captured `expects` tuple, the `duration_sec` (from
the observe step, or `0.0` when the eval errored before observe ran), and
the `error_class` populated when status is `ERRORED`.

## Status mapping rules

Status is the single field every downstream consumer (Reporter, exit code
logic) keys off. The mapping is enforced by the private helper
`_classify_outcome(...)` so unit tests can pin the rules without
constructing a full EvalContext.

| Trigger | Status | `error_class` | `expects` | `duration_sec` |
|---|---|---|---|---|
| All `ExpectResult.passed == True` | **PASS** | `None` | observed tuple | observed value |
| At least one `ExpectResult.passed == False`, no harness exception | **FAIL** | `None` | observed tuple | observed value |
| Harness exception during steps 1-5 (setup, deploy, spawn, inject, observe) | **ERRORED** | fqcn of caught exception | `()` (no assertions ran) | `0.0` until observe completes, otherwise observed value |
| `ExpectCallable` itself raises during step 6 | **ERRORED** | fqcn of raising exception | partial tuple of results gathered before the raise | observed value |
| `KeyboardInterrupt` / `SystemExit` during any step | re-raised (NFR-REL1 / T03.07 marks **INTERRUPTED**) | n/a in T03.04 | n/a in T03.04 | n/a in T03.04 |
| Per-eval timeout (raised as `TimeoutError` by T03.07) | **TIMEOUT** in T03.07 — T03.04 routes through ERRORED today | fqcn `"builtins.TimeoutError"` | `()` | `0.0` |

### `PASS` precondition

`PASS` is only emitted when *every* applied `ExpectCallable` returned an
`ExpectResult` with `passed=True` and zero harness exceptions fired in
steps 1-6. An empty `expects` tuple (manifest with `expects: []`) is
treated as PASS by design — the eval ran cleanly and nothing was asked of
it. T04.x callable design owners can add a "must have at least one
Expect" loader-side guard if the suite contract requires it; the runner
does not police that here.

### Why `KeyboardInterrupt` / `SystemExit` propagate

The atomic-setup wrapper, the executor, and `ExpectCallable` bodies
intentionally do *not* swallow these two exception types. The runner
re-raises them after running `teardown(keep=True)` so NFR-REL1 (T03.07)
can install a signal handler that converts them into an **INTERRUPTED**
outcome at the orchestrator layer. Catching them inside the runner would
defeat the cooperative-cancellation contract.

## `LifecycleExecutor` protocol

```python
class LifecycleExecutor(Protocol):
    def spawn(self, ctx: ExecutorContext) -> None: ...
    def inject(self, ctx: ExecutorContext) -> None: ...
    def observe(self, ctx: ExecutorContext) -> ObservedRun: ...
```

`ExecutorContext` is a small dataclass carrying the post-isolation state
the executor needs (`home`, `home_path`, `run_dir`, `artifacts_dir`,
`stdout_path`, `stderr_path`, `transcript_path`, `env`, plus the original
`EvalSpec`). Tests substitute a `StubExecutor` that records the call
sequence and returns a canned `ObservedRun`. Production code (T03.05)
implements the protocol on top of `PtyDriver` + `ClaudeProcessAdapter`.

`ObservedRun` is a frozen dataclass carrying `(exit_code, stdout, stderr,
duration_sec, jsonl_paths, artifacts)` — i.e. exactly the fields the
runner needs to build the EvalContext that step 6 will see.

## Caller contract

`run_eval` is called by:

- **COMP-004 EvalRunner** (T03.05 / D-0049) — wraps `run_eval` in a
  class that owns the per-eval JSONL log (`home_path/.eval-logs/`) and
  the per-eval timeout enforcement.
- **Unit tests** (`tests/cli/eval/test_eval_lifecycle.py`) — supply
  stub executor + stub expect callables to pin the 7-step sequence and
  the status mapping in isolation.

The function signature is:

```python
def run_eval(
    spec: EvalSpec,
    *,
    home: HomeIsolation,
    config: EvalConfig,
    run_dir: Path,
    artifacts_dir: Path,
    stdout_path: Path,
    stderr_path: Path,
    transcript_path: Path,
    executor: LifecycleExecutor,
    expect_callables: Sequence[ExpectCallable] = (),
    deploy_hooks: Callable[[Path], None] = deploy_hooks_to,
    on_teardown_error: Callable[[BaseException], None] | None = None,
    keep_home_on_pass: bool = False,
) -> EvalOutcome: ...
```

All keyword-only arguments after `spec` so future field additions cannot
silently re-bind positional callers (mirrors the convention established
by `EvalContext.from_runner_state` in T03.03).

## Acceptance criteria → implementation map

| AC bullet (T03.04) | Implementation site |
|---|---|
| `run_eval(spec)` executes the 7-step lifecycle and returns an `EvalOutcome`. | `run_eval` in `runner.py` — steps 1-7 land in declaration order; covered by `test_run_eval_executes_all_seven_steps_in_order`. |
| Harness exceptions during the lifecycle produce status `ERRORED`. | `_classify_outcome` + `_run_with_classification` wrappers; covered by `test_run_eval_setup_exception_yields_errored`, `test_run_eval_deploy_hooks_exception_yields_errored`, `test_run_eval_spawn_exception_yields_errored`, `test_run_eval_expect_raise_yields_errored`. |
| Assertion failures produce status `FAIL`. | `_classify_outcome`; covered by `test_run_eval_failing_expect_yields_fail`. |
| `PASS` only emitted when all Expects pass. | `_classify_outcome` requires all-True over `expects`; covered by `test_run_eval_passes_when_all_expects_pass`, `test_run_eval_mixed_results_yields_fail`. |
| `artifacts/D-0048/spec.md` documents the lifecycle and status mapping. | This file. |

## Teardown `keep` semantics

| Outcome | `keep` flag passed to `home.teardown` | Rationale |
|---|---|---|
| PASS | `keep_home_on_pass` (default `False`) | Clean runs reclaim disk by default; `--keep-home` plumbs True from CLI in T03.18. |
| FAIL | `True` | Failed assertions need their HOME for forensic diffing. |
| ERRORED | `True` | Harness failures preserve HOME so the runner author can reproduce. |
| TIMEOUT (T03.07) | `True` | Same forensic motivation as ERRORED. |
| INTERRUPTED (T03.07) | `True` | Same. |
| SKIPPED | n/a (skip path bypasses `run_eval`) | Capability gating runs upstream in the orchestrator; SKIPPED never reaches the lifecycle. |

## Module symbol re-exports

`run_eval`, `LifecycleExecutor`, `ExecutorContext`, and `ObservedRun` are
exported from `superclaude.cli.eval` so the T03.05 class wrapper and the
unit tests can import them without reaching into `runner`.

## Out of scope for T03.04

- **COMP-004 EvalRunner class** (T03.05 / D-0049) — wraps `run_eval`
  with per-eval JSONL log + timeout enforcement.
- **NFR-REL1 signal handling + per-eval timeout** (T03.07 / D-0050) —
  installs SIGINT/SIGTERM handlers and wires the `TimeoutError` →
  TIMEOUT mapping the table above reserves.
- **NFR-REL2 retry policy** (T03.08 / D-0051) — `retry_count=0` default
  lives on the orchestrator, not the lifecycle.
- **FR-EXP1 ExpectCallable primitives** (T04.01..T04.07) — `run_eval`
  takes them as a `Sequence[ExpectCallable]` today; loader → callable
  resolution lands in T04.x.
- **Skip-flag plumbing** — SKIPPED is the orchestrator's responsibility
  (capability gating runs before `run_eval` is called).
