# 03 — Swarm Dispatch Seam (`dispatch_wave1` + `WorkerResult`)

- **Topic:** The swarm dispatch seam that `ensemble.py` imports — `dispatch_wave1` call contract, `WorkerResult` shape, `ParallelExecutor` fan-out.
- **Investigation type:** API Surface Mapper
- **Scope:** `src/superclaude/cli/swarm/dispatch.py` (`dispatch_wave1`), `src/superclaude/cli/swarm/models.py` (`WorkerResult`).
- **Status:** Complete
- **Date:** 2026-06-19 (line numbers re-verified 2026-06-20)

---

## Orientation: where this seam sits `[CODE-VERIFIED]`

`ensemble.py` does **not yet exist** in `src/superclaude/cli/swarm/` — it is the NEW
component this TDD designs (the ReflectHardening / "RH" feature). It is the *caller*
that will import the dispatch seam below. Verified by:

- `find . -name ensemble.py` → no hit anywhere in the repo.
- `grep -rln dispatch_wave1 src/superclaude/` → only `dispatch.py` (def site),
  `commands.py`, `normalize.py`, `logging_.py` reference it today; no `ensemble.py`.

So this report documents the **existing, stable** dispatch contract that `ensemble.py`
will consume in-process, taken verbatim from code.

Source files (re-verified line numbers, 2026-06-20):

- `src/superclaude/cli/swarm/dispatch.py` — `dispatch_wave1` at **L334-508**
  (signature L334-343; docstring L344-407; body L409-508). `retry_policy` L195-276.
  Supporting `_send_once` L143-192, `_run_worker` L279-331, `_classify_http_code` L127-140.
- `src/superclaude/cli/swarm/models.py` — `WorkerResult` (DM-013) at **L1026-1136**
  (field block L1117-1128; `__post_init__` L1130-1136).
- `src/superclaude/execution/parallel.py` — `ParallelExecutor` at **L80-246**
  (`quiet` attr L100; `plan` L105; `execute` L173-212; `_execute_group` L214-246).

---

## 1. `dispatch_wave1` call contract `[CODE-VERIFIED]`

### 1.1 Full signature (every parameter + return type)

From `dispatch.py` L334-343, verbatim:

```python
def dispatch_wave1(
    preflight_result: PreflightResult,
    transport: Optional[Transport] = None,
    *,
    transport_for_slot: Optional[Callable[[int], Transport]] = None,
    prompt: str = "",
    parallel_executor: Optional[ParallelExecutor] = None,
    worker_spec: Optional[WorkerSpec] = None,
    logger: Optional[Logger] = None,
) -> list[WorkerResult]:
```

| Param | Type | Default | Role |
|---|---|---|---|
| `preflight_result` | `PreflightResult` | (required, positional) | Wave-0 output. Fan-out count = `preflight_result.manifest.preflight.workers_requested` (L412). |
| `transport` | `Optional[Transport]` | `None` | Single shared transport for all N slots (legacy single-model path). |
| `transport_for_slot` | `Optional[Callable[[int], Transport]]` | `None` (kw-only) | Per-slot transport factory `(slot_index) -> Transport`. **Takes precedence** over `transport` when supplied (L453-457) → enables heterogeneous per-worker model fan-out. |
| `prompt` | `str` | `""` (kw-only) | Fully-assembled prompt body. Passed verbatim to `transport.send` (transport MUST NOT re-normalize, COMP-031). |
| `parallel_executor` | `Optional[ParallelExecutor]` | `None` (kw-only) | Inject a pre-sized executor (tests use a small `max_workers` to force queueing). When `None`, a new one is built sized to `workers_requested` (L424). |
| `worker_spec` | `Optional[WorkerSpec]` | `None` (kw-only) | Carries `timeout_sec` (NFR-010) + `RetryPolicy` (FR-017/NFR-011). When `None`, defaults to `WorkerSpec()` = §7 matrix (L419). |
| `logger` | `Optional[Logger]` | `None` (kw-only) | When set, emits `wave_transition` (open), paired `worker_start`/`worker_done` per slot, and `wave_transition` (close). When `None`, dispatch is silent. |

**Return type: `list[WorkerResult]`** — one `WorkerResult` per requested slot, sorted by
`index` 0..N-1 (positional correspondence with requested slots). All params after
`transport` are **keyword-only** (the bare `*` at L337).

### 1.2 How a caller invokes it in-process

Minimal real call (single shared transport):

```python
from superclaude.cli.swarm.dispatch import dispatch_wave1
results = dispatch_wave1(
    preflight_result,            # from run_preflight(...)
    transport=stub_or_openai_transport,
    prompt=assembled_prompt,
    worker_spec=WorkerSpec(...), # optional; else §7 defaults
)
```

Heterogeneous multi-model call (one model per slot) — the shape `ensemble.py` will use:

```python
results = dispatch_wave1(
    preflight_result,
    transport_for_slot=lambda i: transport_for_model(models[i]),
    prompt=assembled_prompt,
    worker_spec=worker_spec,
    logger=logger,
)
```

### 1.3 Early-exit / guard semantics `[CODE-VERIFIED]`

- **L409-410:** `if transport is None and transport_for_slot is None: return []`
  — the "wire-only" no-op path (both transport sources absent).
- **L412-414:** `if workers_requested <= 0: return []`.
- **L425:** `executor.quiet = True` — FR-1: dispatch path is silent on the worker
  thread; workers emit to files, not stdout. (Set on whatever executor was injected
  or freshly built.)

### 1.4 One `WorkerResult` per slot — the invariant `[CODE-VERIFIED]`

Body L444-490:

1. `_make_callable(slot_index)` (L444-462) builds a per-slot closure using
   default-arg binding to capture `slot_index` (avoids the late-binding closure trap).
   The closure picks `transport_for_slot(slot_index)` if a factory was supplied, else
   the shared `transport` (L453-457), then calls `_run_worker(...)`.
2. `tasks` (L464-472): one `Task(id=f"worker-{index:02d}", ...)` per
   `range(workers_requested)`.
3. `plan = executor.plan(tasks)` (L474); `raw_results = executor.execute(plan)` (L475)
   → `Dict[task.id -> WorkerResult | None]`.
4. **Re-key + invariant guard (L484-490):** for each `index in range(workers_requested)`,
   look up `raw_results.get(f"worker-{index:02d}")`. If it is a `WorkerResult`, append
   it; **otherwise** (a `None` — meaning an unexpected exception escaped `_run_worker`)
   synthesize `WorkerResult(index=index, status="proxy_error", attempts=1)`. This
   guarantees **exactly one `WorkerResult` per slot**, even under contract violation,
   and positional alignment with requested slots.

`_run_worker` (L279-331) is contractually non-raising: every terminal outcome
(success/timeout/parse_error/proxy_error) is encoded into the returned `WorkerResult`.
It stamps `result.index = index` (L310) and, when a logger is present, emits
`worker_start`/`worker_done` events including `model_id`/`model_label` so a failed slot
stays attributable (L321-327).

---

## 2. Timeout / retry matrix `[CODE-VERIFIED]`

The per-attempt + retry behavior is `retry_policy` (L195-276), which `_run_worker`
calls once per slot (L309). Module docstring matrix (L21-54) + code:

| Outcome | `http_code` | Default retry? | `attempts` |
|---|---|---|---|
| `success` | 200 | no | 1 |
| 4xx `proxy_error` | 400..499 | no (`on_4xx=False`) | 1 |
| 5xx `proxy_error` | 500..599 | **yes, once** (`on_5xx=True`) | 1 or 2 |
| `timeout` | `None` | no (`on_timeout=False`) | 1 |
| network/other | `None` | no (no flag exists) | 1 |
| `parse_error` | 200 (usually) | no | 1 |

Key code facts:

- **Timeout source:** `timeout_sec = spec.timeout_sec if spec.timeout_sec > 0 else
  _DEFAULT_TIMEOUT_SEC` (L244), `_DEFAULT_TIMEOUT_SEC = 180` (L124, NFR-010). Forwarded
  to `transport.send(prompt, timeout_sec)` (L170) so the transport's httpx timeout
  matches the dispatcher budget.
- **Retry decision (L249-259):** only `proxy_error` with a `5xx` bucket and
  `retry.on_5xx` (or `4xx`+`on_4xx`, or `timeout`+`on_timeout`) sets `should_retry`.
  `other`/`None` (network/connection failure) is **never** retried — there is no
  `on_network` flag.
- **`_classify_http_code` (L127-140):** `None → "other"`; 500-599 → `"5xx"`;
  400-499 → `"4xx"`; else `"other"`.
- **5xx retry branch (L264-276):** sleeps `max(0, retry.on_5xx_backoff_sec)` via the
  injectable `sleep_fn` (default `time.sleep`), issues a second `_send_once`, stamps
  `second.attempts = 2`, and sets `second.elapsed_ms = first.elapsed_ms +
  second.elapsed_ms` (cumulative transport wall-clock; **backoff sleep excluded** — it
  is policy overhead, not transport work).
- **`RetryPolicy` defaults** (`models.py` L149-152, encode §7): `on_5xx=True`,
  `on_5xx_backoff_sec=2`, `on_4xx=False`, `on_timeout=False`.
- **`_send_once` (L143-192)** normalizes the three transport terminal forms:
  returned `WorkerResult` passes through (`attempts=1`, `elapsed_ms` backfilled if 0);
  raised `TimeoutError` → synthetic `status="timeout"`, `http_code=None`; any other
  `Exception` → synthetic `status="proxy_error"`, `http_code=None`.

---

## 3. `WorkerResult` shape (DM-013) `[CODE-VERIFIED]`

`@dataclass` in `models.py` L1026; field block L1117-1128; `__post_init__` L1130-1136.
**Exact field set (12 fields), verbatim with types + defaults:**

| # | Field | Type | Default | Meaning |
|---|---|---|---|---|
| 1 | `index` | `int` | `0` | Worker slot index 0..N-1; drives `{index:02d}` filename substitution. |
| 2 | `path` | `str` | `""` | Canonical output path (post-normalize, or = `raw_path` for raw-only). |
| 3 | `raw_path` | `str` | `""` | Per-worker raw output (`*.raw.<ext>`); retained when `retain_raw=True`. |
| 4 | `meta_path` | `str` | `""` | Per-worker meta sidecar (`*.meta.json`) — transport/model/attempts/status. |
| 5 | `final_path` | `str` | `""` | Post-normalization file consumed by Wave 3 reduce/merge. |
| 6 | `model_id` | `str` | `""` | Transport-supplied model identifier (e.g. `gpt-5-codex`). |
| 7 | `model_label` | `str` | `""` | Human-facing model label for merge provenance/event log. |
| 8 | `bytes` | `int` | `0` | Worker output byte count. |
| 9 | `status` | `WorkerStatus` | `"success"` | One of the 4 enum values below; validated in `__post_init__`. |
| 10 | `http_code` | `Optional[int]` | `None` | DM-013 `http_code:int?`; `None` = no transport HTTP response recorded. |
| 11 | `attempts` | `int` | `1` | Attempt count: 1 (no retry) or 2 (5xx retried once). |
| 12 | `elapsed_ms` | `int` | `0` | Per-worker wall-clock elapsed (ms), cumulative across attempts. |

### 3.1 `status` enum — `WorkerStatus` `[CODE-VERIFIED]`

`models.py` L69: `WorkerStatus = Literal["success", "timeout", "parse_error", "proxy_error"]`.

`WorkerResult.__post_init__` (L1130-1136) raises `ValueError` if `status` is not one of
these four (`typing.get_args(WorkerStatus)`). The §7.4 salvage promotion
`parse_error → success` is a Wave-2 (normalize) concern, **not** applied in this
dataclass or in dispatch.

> Note: the broader job-level `ResultStatus` (L68 — `success`/`partial`/`failed`) is a
> *different* enum, used by `ResultContract` (DM-012) at reduce, not by `WorkerResult`.

### 3.2 Where `WorkerResult`s are aggregated `[CODE-VERIFIED]`

`ResultContract.output_files: list["WorkerResult"]` (`models.py` L1010) is the field
that collects them at Wave-3 reduce. The contract also carries the count triple
`workers_requested` / `workers_succeeded` / `workers_failed` (L1007-1009), with
INV-005: `workers_succeeded + workers_failed == workers_requested` (enforced at the
reduce emitter, not the dataclass).

---

## 4. `ParallelExecutor` fan-out behavior `[CODE-VERIFIED]`

`src/superclaude/execution/parallel.py`, class L80-246. Dispatch is **forbidden** from
instantiating `concurrent.futures.ThreadPoolExecutor` directly (AC-004); all swarm
parallelism routes through this single seam.

- **Construction:** `ParallelExecutor(max_workers=workers_requested)` (dispatch L424).
  `quiet: bool = False` class attribute (L100); dispatch flips it to `True` (L425) so
  the executor's own `print(...)` calls (all gated behind `if not self.quiet:`) stay
  silent on the worker thread — the FR-1 single-writer discipline.
- **`plan(tasks) -> ExecutionPlan` (L105):** groups tasks by `depends_on`; swarm tasks
  declare `depends_on=[]` (dispatch L469) so all N land in one parallel group.
- **`execute(plan) -> Dict[str, Any]` (L173-212):** returns `dict` of `task.id -> result`.
  Iterates groups, calling `_execute_group`.
- **`_execute_group` (L214-246):** opens a `ThreadPoolExecutor(max_workers=self.max_workers)`
  (L219), submits every task (L221-223), collects via `as_completed` (L226). On success
  → `results[task.id] = result` (L233). **On any exception → `results[task.id] = None`**
  (L238-241) — the task is marked FAILED and its slot value is `None`. This is exactly
  the `None` that dispatch's L487-490 guard converts into a synthetic `proxy_error`
  `WorkerResult`, preserving the one-result-per-slot invariant.

Because `_run_worker` is contractually non-raising, the `None`/exception branch is a
defensive backstop, not the normal path; normally every `task.id` maps to a real
`WorkerResult`.

---

## 5. Diversity / reviewer_count measured over SUCCEEDED workers M, not slots N

**EXPLICIT (per task brief, FR-RH2.4 / FR-RH2.9):** When `ensemble.py` (the new caller)
computes **diversity** and **reviewer_count**, it MUST measure over the set of
**succeeded** workers `M`, *not* the requested slot count `N`. Only a `WorkerResult`
whose `status == "success"` counts toward `M`. Workers with `status` of
`proxy_error`, `timeout`, or `parse_error` (the other three `WorkerStatus` values) do
**not** count toward `M`.

Code anchors that make this implementable directly off the returned list `[CODE-VERIFIED]`:

- `dispatch_wave1` returns `list[WorkerResult]` of length **N** (one per requested slot,
  including failed/synthetic slots) — so the caller cannot use `len(results)` as M.
- The success predicate is literally `r.status == "success"` — dispatch itself already
  uses exactly this to compute its closing-event `success_count`:
  `success_count = sum(1 for r in results if r.status == "success")` (dispatch L496).
  `ensemble.py` should reuse the same predicate to derive M (and then diversity over the
  distinct `model_id`/`model_label` of those M succeeded results).
- This aligns with the job-level IMM-5 status matrix in `StatusPolicy`
  (`models.py` L535-539), which is defined over M (succeeded) vs N (requested):
  `M==N → success`; `2 <= M < N → partial`; `M < 2 → failed`.

> Caveat `[UNVERIFIED]`: `ensemble.py` does not yet exist, so the *exact* place this M-vs-N
> rule is coded is a design obligation of this TDD, not an observable in the current
> tree. The dispatch surface gives the caller everything needed (per-slot `status`,
> `model_id`, `model_label`) to implement it correctly; the success predicate
> (`status == "success"`) is verified against dispatch L496.

---

## Key Takeaways

1. **Signature is stable and kw-only after `transport`.** `dispatch_wave1(preflight_result,
   transport=None, *, transport_for_slot=None, prompt="", parallel_executor=None,
   worker_spec=None, logger=None) -> list[WorkerResult]`. `ensemble.py` passes
   `transport_for_slot` for heterogeneous per-model fan-out (it takes precedence over
   `transport`).
2. **One `WorkerResult` per requested slot, sorted by `index` 0..N-1**, guaranteed even
   when a worker callable raises (synthesized `proxy_error` backstop at L487-490). The
   returned list length is **N**, not M.
3. **`WorkerResult` has exactly 12 fields.** `status` is the 4-value `WorkerStatus`
   Literal (`success`/`timeout`/`parse_error`/`proxy_error`), guarded by `__post_init__`.
   `http_code` is `Optional[int]`; `attempts` is 1 or 2; `model_id`/`model_label` are
   stamped per slot for attribution.
4. **Retry matrix:** only 5xx is retried (once, with `on_5xx_backoff_sec` backoff);
   4xx / timeout / network are not. Timeout default 180s. `elapsed_ms` is cumulative
   transport wall-clock excluding backoff sleep.
5. **Fan-out routes through `ParallelExecutor` only** (AC-004). Dispatch sets
   `executor.quiet = True` (FR-1). `execute()` returns `dict[task.id -> WorkerResult|None]`.
6. **Diversity / reviewer_count are over M (succeeded), not N (requested).** The success
   predicate is `status == "success"` — already used by dispatch at L496 for its
   `success_count`. `ensemble.py` reuses this to derive M, then diversity over the
   distinct models of the M succeeded results.

## Gaps and Questions

- **`[UNVERIFIED]` `ensemble.py` does not exist yet.** It is the component this TDD
  designs. The M-vs-N diversity/reviewer_count rule (FR-RH2.4/2.9) is therefore a design
  obligation, not yet observable in code. The dispatch surface supplies everything needed
  to implement it (per-slot `status` + `model_id` + `model_label`); the success predicate
  is verified against `dispatch.py` L496.
- **`PreflightResult` / `Transport` internals not exhausted here.** This report treats
  `preflight_result.manifest.preflight.workers_requested` (the only field dispatch reads,
  L412) and the `Transport.send(prompt, timeout_sec) -> WorkerResult` shape as the
  boundary. Deeper preflight/transport surface is out of this report's scope (covered by
  the preflight/transport seam research files if needed).
- **No `partial`/`failed` job-level rollup in dispatch.** `dispatch_wave1` returns raw
  per-slot results only; the IMM-5 status reduction (M/N → success/partial/failed) happens
  later at Wave-3 reduce on `ResultContract`, not in this seam.

## Summary

`dispatch_wave1` (`dispatch.py` L334-508) is the in-process Wave-1 fan-out entrypoint the
new `ensemble.py` will call. It takes a `PreflightResult` plus a transport (shared
`transport` or per-slot `transport_for_slot` factory), fans `prompt` across
`workers_requested` (= N) slots strictly through `ParallelExecutor` (AC-004, `quiet=True`),
applies the §7 retry/timeout matrix per slot via `retry_policy` (5xx-retry-once, 180s
default timeout), and returns a `list[WorkerResult]` of length N sorted by `index`, with a
synthesized `proxy_error` backstop guaranteeing one result per slot. `WorkerResult`
(DM-013, `models.py` L1026-1136) carries 12 fields, the load-bearing ones being `status`
(the 4-value `WorkerStatus` Literal), `model_id`, `model_label`, `elapsed_ms`, and
`final_path`. The caller computes **diversity and reviewer_count over the succeeded subset
M** — `status == "success"` only — never over the requested N; `proxy_error` / `timeout` /
`parse_error` slots are excluded, matching the predicate dispatch already uses at L496.
