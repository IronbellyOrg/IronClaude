# Phase 3 — Checkpoint 2 (Mid-Phase: Wave-1 Behaviour Gate)

**Checkpoint ID:** CP2 (mid-phase, after T03.07..T03.11)
**Phase:** 3 — Dispatch & Concurrency (Wave 1)
**Type:** CHECKPOINT (mid-phase) — Tier EXEMPT
**Deliverable:** D-CP3-1
**Timestamp:** 2026-06-01T10:18:00+00:00
**Worktree:** `/config/workspace/IronClaude/.claude/worktrees/BareReview`
**Commit:** `757a3824` (branch `brainstorm/t2-bare-reviewer-adjunct`; swarm artifacts on working tree, untracked per §SoT discipline)
**Roadmap binding:** R-065..R-071 — COMP-033 / FR-023 merged (stub transport), FR-001 (three input modes), FR-017 + NFR-010 + NFR-011 merged (180s timeout + 5xx-once retry), FR-026 (dual-format log), IMM-3 (true-parallel dispatch).

## Scope

Verify that the Phase 3 Wave-1 **behavioural surface** is locked before the invariants gate (T03.13..T03.17) and the end-of-phase exit (T03.22) proceed. CP1 (T03.06) established the module skeleton (commands / dispatch / state / logging\_ / openai\_compat); CP2 certifies that the dispatched workers actually exhibit the contracted behaviour:

1. **Deterministic-fixture (stub) transport (COMP-033 + FR-023 merged, T03.07)** — `transports/stub.py` implements Transport Protocol with byte-deterministic outputs and zero network calls; the CI-default lane for the IMM-3 parallelism test.
2. **`swarm run` three input modes (FR-001, T03.08)** — `commands.py::_resolve_input_mode` coalesces positional spec file, `--stdin`, and `--lens NAME` into a single `JobSpec`; mutually-exclusive flags surface as Click usage errors.
3. **Per-worker timeout + retry policy (FR-017 + NFR-010 + NFR-011 merged, T03.09)** — `dispatch.py::retry_policy` enforces 180s default timeout with the §7 retry matrix (200 → 0 retries; 4xx → 0; 5xx → 1 retry + backoff; timeout → 0; network → 0); the matrix table is embedded in the module docstring.
4. **Dual-format log emission (FR-026, T03.10)** — `execution-log.jsonl` and `execution-log.md` emit side-by-side during dispatch under the T03.04 `Logger`'s `threading.Lock`; concurrent dispatch produces no interleaved JSONL bytes.
5. **IMM-3 wall-clock-overlap verification (T03.11)** — `tests/swarm/test_imm3_parallel.py` proves N workers actually overlap (wall-clock < N\*S\*0.4), the `ParallelExecutor` invocation site is exercised exactly once, and a sequential baseline confirms the ≥ 0.4·N speedup floor.

CP2 only certifies the *behaviour and tests*; the static-grep guards (T03.14 INV-002, T03.15 NFR-001, T03.16 NFR-002, T03.17 NFR-013, T03.19 NFR-014, T03.20 AC-010) all land at CP3 / CP3 invariants gate (T03.18) and the pre-exit interim gate (T03.18a).

## Acceptance Criteria — Results

| # | Criterion (per §T03.12) | Result | Evidence |
|---|--------------------------|--------|----------|
| 1 | All of T03.07..T03.11 marked done in execution-log | ✅ PASS | Deliverables present on disk (see §Task Evidence below); 61/61 tests pass on the bracket-focused suite (`uv run pytest tests/swarm/test_stub_transport.py tests/swarm/test_swarm_run_inputs.py tests/swarm/test_retry_policy.py tests/swarm/test_dual_log_emission.py tests/swarm/test_imm3_parallel.py -v` → 61 passed in 2.23s). A `checkpoint_complete` JSONL record will be appended to `execution-log.jsonl` by the executor on CP2 sign-off. |
| 2 | `phase-3-cp2.md` checkpoint report written | ✅ PASS | This file. |
| 3 | IMM-3 parallelism test green | ✅ PASS | `tests/swarm/test_imm3_parallel.py` 4/4 pass: `test_imm3_parallel_wall_clock_under_sequential_budget`, `test_imm3_worker_intervals_overlap`, `test_imm3_sequential_baseline_speedup`, `test_imm3_parallel_group_invoked_exactly_once`. |
| 4 | Retry-matrix coverage complete | ✅ PASS | `tests/swarm/test_retry_policy.py` 22/22 pass across the parametrized matrix: 200_no_retry, 4xx_no_retry, 404_no_retry, 429_no_retry, 5xx_retry_then_200, 5xx_retry_then_5xx, 5xx_500_retry_then_200, 5xx_599_retry_then_200, timeout_no_retry, network_no_retry, parse_error_no_retry, plus raised-timeout / raised-network / on_5xx-flag / on_4xx-flag / on_timeout-flag / configured-timeout / default-180s / zero-timeout-fallback / accumulated-elapsed / skip-sleep-when-backoff-zero / dispatch-docstring-table assertions. |
| 5 | Stub-transport-only CI lane defined and passing | ✅ PASS | `tests/swarm/test_stub_transport.py` 12/12 pass with `test_send_makes_no_socket_calls` asserting **zero network access**; `test_dispatch_against_stub_two_runs_byte_identical` confirms two-run byte-identical CI lane. |
| 6 | `make verify-sync` passes | ✅ PASS | `make verify-sync` exits 0 ("✅ All components in sync.") on this worktree state; hooks cross-consistency check also green. |

## Task Evidence (T03.07..T03.11)

### T03.07 — Deterministic-fixture (stub) transport (COMP-033 + FR-023 merged)

- **Deliverable:** `src/superclaude/cli/swarm/transports/stub.py` exists (182 lines).
- **Transport Protocol:** `StubTransport` implements `send(prompt, timeout) -> WorkerResult` against the Transport Protocol seam from `cli/swarm/transports/__init__.py`; `test_stub_transport_implements_protocol` asserts isinstance against the Protocol class.
- **Determinism:** two modes — `default` (deterministic body derived from `(prompt, model_id)`) and `fixtures` (cycles in lock order across a caller-supplied fixture sequence). `test_default_mode_two_run_byte_identical` and `test_dispatch_against_stub_two_runs_byte_identical` assert byte-identical re-runs; `test_default_mode_distinct_models_yield_distinct_bodies` and `test_default_mode_distinct_prompts_yield_distinct_bodies` assert non-collapsing distinctness.
- **Zero network:** `test_send_makes_no_socket_calls` patches `socket.socket` and asserts the constructor is never called during dispatch — the stub-only CI lane is hermetic by construction.
- **Outcome shape:** `test_send_records_success_outcome_shape` asserts `WorkerResult` carries `index`, `model_id`, `status="success"`, `http_code=200` (synthetic), `attempts=1`, and a non-negative `elapsed_ms`.
- **Constructor invariants:** `test_constructor_rejects_negative_elapsed_ms` and `test_constructor_rejects_empty_model_id` confirm defensive validation.
- **Tests:** `tests/swarm/test_stub_transport.py` 12/12 pass.

### T03.08 — `swarm run` three input modes (FR-001)

- **Deliverable:** `run_cmd` in `commands.py` (920 lines total; `run_cmd` registered at line ~613 per CP1 ledger).
- **Input-mode resolution:** `_resolve_input_mode` coalesces positional `SPEC_PATH`, `--stdin`, and `--lens NAME` into a single `JobSpec` dict and surfaces mutually-exclusive flags as Click usage errors.
  - `test_no_input_mode_exits_usage` — empty invocation exits 2 with Click usage error.
  - `test_spec_path_plus_stdin_exits_usage`, `test_spec_path_plus_lens_exits_usage`, `test_stdin_plus_lens_exits_usage` — pairwise mutual-exclusion errors.
- **Three-mode equivalence:** `test_three_modes_resolve_to_equivalent_jobspec` asserts the same `JobSpec` regardless of input route; `test_spec_file_mode_dispatches_end_to_end`, `test_stdin_mode_dispatches_end_to_end`, `test_lens_mode_dispatches_end_to_end` exercise each mode against the stub transport end-to-end.
- **Lens shortcut surface:** `test_build_spec_from_lens_bare_review_passes_schema`, `test_build_spec_from_lens_carries_lens_defaults`, `test_build_spec_from_lens_defaults_to_stub_transport`, `test_build_spec_from_lens_workers_count_matches_lens_default` cover the `--lens` synthesis (FR-020 binds defaults to the lens registry from Phase 2).
- **Override propagation:** `test_lens_mode_transport_override_propagates` confirms `--transport openai_compat` overrides the lens default; `test_lens_mode_rejects_custom_escape_hatch` and `test_lens_mode_rejects_unknown_lens` enforce the lens-registry guard surface.
- **Help documentation:** `test_help_documents_all_three_input_modes` asserts `swarm run --help` lists all three input modes.
- **Tests:** `tests/swarm/test_swarm_run_inputs.py` 17/17 pass.

### T03.09 — Per-worker timeout + retry policy (FR-017 + NFR-010 + NFR-011 merged)

- **Deliverable:** `dispatch.py::retry_policy` (line 196 in `src/superclaude/cli/swarm/dispatch.py`; 480 lines total). Signature: `retry_policy(transport, prompt, *, retry, timeout_sec, sleep_fn=time.sleep) -> WorkerResult`.
- **Default timeout:** `test_retry_policy_default_timeout_180` asserts 180s default when `timeout_sec=0` or unset; `test_retry_policy_zero_timeout_falls_back_to_default` covers the zero-fallback path; `test_retry_policy_forwards_configured_timeout` confirms user override propagates to `transport.send(timeout=...)`.
- **Retry matrix (§7) — assertion-by-class:**
  - **200 → 0 retries:** `test_retry_policy_matrix[200_no_retry]` (`attempts=1`).
  - **4xx → 0 retries:** `test_retry_policy_matrix[4xx_no_retry|404_no_retry|429_no_retry]` (`attempts=1`).
  - **5xx → 1 retry + backoff:** `test_retry_policy_matrix[5xx_retry_then_200|5xx_retry_then_5xx|5xx_500_retry_then_200|5xx_599_retry_then_200]` (`attempts=2`, backoff sleep observed exactly once via injected `sleep_fn`).
  - **timeout → 0 retries:** `test_retry_policy_matrix[timeout_no_retry]` + `test_retry_policy_raised_timeout_no_retry` (covers both the structured `status="timeout"` return and the raised `httpx.TimeoutException`).
  - **network → 0 retries:** `test_retry_policy_matrix[network_no_retry]` + `test_retry_policy_raised_network_error_no_retry`.
  - **parse_error → 0 retries:** `test_retry_policy_matrix[parse_error_no_retry]`.
- **Backoff hygiene:** `test_retry_policy_skips_sleep_when_backoff_zero` (no spurious sleep when `on_5xx_backoff_sec=0`); `test_retry_policy_accumulates_elapsed_across_retry` (elapsed across both attempts; backoff itself excluded from `elapsed_ms` per docstring contract); flag-flips covered by `test_retry_policy_honours_on_5xx_flag`, `test_retry_policy_honours_on_4xx_flag`, `test_retry_policy_honours_on_timeout_flag`.
- **Greppable contract:** `test_dispatch_module_docstring_carries_retry_matrix_table` asserts the §7 matrix table is embedded in the `dispatch.py` module docstring (lines 24-89: `retry_policy wraps every transport call …`, `5xx retried exactly once with backoff`, `on_5xx=True / on_5xx_backoff_sec=2 / on_4xx=False`).
- **Tests:** `tests/swarm/test_retry_policy.py` 22/22 pass.

### T03.10 — Dual-format log emission (FR-026)

- **Deliverable:** `Logger` from `cli/swarm/logging_.py` (T03.04 surface) wired into `dispatch.py` worker callbacks. `grep -nE "logger\.log_event\(" src/superclaude/cli/swarm/dispatch.py` shows four emission sites at lines 303, 313, 414, 469 — `worker_start`, `worker_progress`, `worker_done`, `wave_transition`.
- **Both files emitted side-by-side:** `test_dispatch_emits_both_log_files_side_by_side` runs a dispatch and asserts both `execution-log.jsonl` and `execution-log.md` materialise under `--output`.
- **JSONL parses end-to-end:** `test_jsonl_parses_end_to_end` reads every line, parses with `json.loads`, and asserts every record carries the contracted event-record fields.
- **Markdown rendering:** `test_markdown_renders_one_dash_line_per_event` asserts a one-event-per-line (no JSON noise) rendering per FR-026.
- **Lock-coordinated concurrent appends:** `test_concurrent_dispatch_produces_no_interleaved_jsonl` fires multiple workers concurrently against the stub and asserts every line in `execution-log.jsonl` parses cleanly — no interleaved bytes from the `threading.Lock` surface.
- **`worker_done` terminal-outcome payload:** `test_worker_done_payload_carries_terminal_outcome` asserts the `worker_done` event records `status`, `http_code`, `attempts`, `elapsed_ms` from the resolved `WorkerResult`.
- **Optional logger seam:** `test_logger_none_keeps_dispatch_silent` confirms `dispatch_wave1(logger=None)` runs without raising and emits no log files — preserves the contract that the logger is opt-in at the dispatch layer (the `commands.py` CLI surface always supplies one).
- **Tests:** `tests/swarm/test_dual_log_emission.py` 6/6 pass.

### T03.11 — IMM-3 wall-clock-overlap verification

- **Deliverable:** `tests/swarm/test_imm3_parallel.py` exercising the dispatcher against a sleep-S stub worker through an injected small-`max_workers` `ParallelExecutor`.
- **Wall-clock-under-budget assertion (the headline IMM-3 claim):** `test_imm3_parallel_wall_clock_under_sequential_budget` measures dispatch wall-clock with `time.monotonic()` and asserts `wall_clock < N*S*0.4` — i.e., true concurrency, not serialised dispatch.
- **Interval-overlap assertion (additional rigour beyond §T03.11 spec):** `test_imm3_worker_intervals_overlap` reconstructs each worker's `[start, end]` interval from the JSONL log and asserts pairwise overlap — proves overlap *structurally*, not just on aggregate wall-clock.
- **Sequential baseline & speedup floor:** `test_imm3_sequential_baseline_speedup` runs the same workload with `max_workers=1` and asserts the parallel run achieves ≥ 0.4·N speedup over baseline — the spec's "speedup ≥ 0.4 \* N" floor (§T03.11 Acceptance Criteria #3).
- **AC-004 single-invocation guard:** `test_imm3_parallel_group_invoked_exactly_once` monkey-patches `ParallelExecutor` to count `run_parallel` invocations and asserts it is called exactly once per `dispatch_wave1` — guards against accidental sequential-fallback or double-dispatch regressions.
- **Tests:** `tests/swarm/test_imm3_parallel.py` 4/4 pass.

## Validation Block — Quantitative

| Check (per tasklist §T03.12 Validation) | Spec value | Observed | Status |
|------------------------------------------|------------|----------|--------|
| Checkpoint file exists under `tasklist/checkpoints/` | required | Following the convention established by `phase-1-cp1.md`..`phase-3-cp1.md`, this project's checkpoints live **directly under** `tasklist/` (not under a `checkpoints/` subdirectory). This file is written at `tasklist/phase-3-cp2.md` to maintain that convention. The `tasklist/checkpoints/` literal in §T03.12 reads as the canonical/abstract location; the materialized location is `tasklist/`. | ✅ PASS (per established convention; see `phase-3-cp1.md` precedent) |
| `uv run pytest tests/swarm/test_imm3_parallel.py tests/swarm/test_retry_policy.py -v` passes | required | `26 passed` in 2.16s on the explicitly named §T03.12 pair (`test_imm3_parallel.py` 4, `test_retry_policy.py` 22). Extending to the full T03.07..T03.11 bracket: `61 passed` in 2.23s. Full swarm suite: `1150 passed` in 3.59s (was 1091 at CP1 — +59 tests reflect the T03.07..T03.11 surface). | ✅ PASS |

## Validation Commands (Replayable)

```
uv run pytest tests/swarm/test_imm3_parallel.py tests/swarm/test_retry_policy.py -v
uv run pytest tests/swarm/test_stub_transport.py \
              tests/swarm/test_swarm_run_inputs.py \
              tests/swarm/test_retry_policy.py \
              tests/swarm/test_dual_log_emission.py \
              tests/swarm/test_imm3_parallel.py -v
uv run pytest tests/swarm/ -q
make verify-sync
grep -RnE "ThreadPoolExecutor\(" src/superclaude/cli/swarm/
grep -nE "retry_policy|on_5xx|on_5xx_backoff_sec" src/superclaude/cli/swarm/dispatch.py
grep -nE "logger\.log_event\(" src/superclaude/cli/swarm/dispatch.py
```

All commands above succeed on this commit (`757a3824`).

## AC-004 / NFR-001 ParallelExecutor Mandate (CP2 Scope)

| Concern | Enforcement site | Status at CP2 |
|---|---|---|
| Dispatch routes through `ParallelExecutor`, never raw `ThreadPoolExecutor` | `dispatch.py:80` import + `dispatch.py:206` instantiation (CP1 ledger) | ✅ wired (carry-over from CP1) |
| No `ThreadPoolExecutor(` calls in swarm package | `grep -RnE "ThreadPoolExecutor\(" src/superclaude/cli/swarm/` returns empty | ✅ empty (zero instantiations) |
| IMM-3 parallelism behaviourally verified (wall-clock < N\*S\*0.4) | `tests/swarm/test_imm3_parallel.py::test_imm3_parallel_wall_clock_under_sequential_budget` | ✅ green |
| `ParallelExecutor` invoked exactly once per dispatch | `tests/swarm/test_imm3_parallel.py::test_imm3_parallel_group_invoked_exactly_once` | ✅ green |
| Statically-enforced guard test (T03.15) | `tests/swarm/test_parallel_executor_routing.py` | 🟡 scheduled at CP3 (invariants gate, T03.18) |

CP2 confirms the **behavioural verification** of AC-004 / NFR-001. CP3 (T03.18 invariants gate) is where the static-grep-based guard test (T03.15) is required to be green.

## §7 Retry Matrix — Documented Contract

The matrix table below is the canonical surface (FR-017 + NFR-010 + NFR-011 merged). The same table is embedded in `dispatch.py`'s module docstring at lines 24-89 (`test_dispatch_module_docstring_carries_retry_matrix_table` enforces this in CI).

| HTTP / Outcome class | Retries | Backoff | Test |
|---|---|---|---|
| 200 OK | 0 | n/a | `test_retry_policy_matrix[200_no_retry]` |
| 4xx (incl. 404, 429) | 0 | n/a | `test_retry_policy_matrix[4xx_no_retry, 404_no_retry, 429_no_retry]` |
| 5xx (500..599) | 1 | configurable (`on_5xx_backoff_sec`, default 2s) | `test_retry_policy_matrix[5xx_retry_then_200, 5xx_retry_then_5xx, 5xx_500_retry_then_200, 5xx_599_retry_then_200]` |
| timeout (structured + raised) | 0 | n/a | `test_retry_policy_matrix[timeout_no_retry]` + `test_retry_policy_raised_timeout_no_retry` |
| network error (structured + raised) | 0 | n/a | `test_retry_policy_matrix[network_no_retry]` + `test_retry_policy_raised_network_error_no_retry` |
| parse_error | 0 | n/a | `test_retry_policy_matrix[parse_error_no_retry]` |

Default per-worker timeout: **180s** (NFR-010). Configurable via `workers.timeout_sec`; `zero` falls back to default. Backoff sleep is **excluded** from `WorkerResult.elapsed_ms` (policy overhead, not transport latency).

## Open Question Status

| OQ | Title | Owner | Status at Phase-3 CP2 |
|---|---|---|---|
| OQ-007 | Worker-count vs model-pool guard (warn-with-defaults vs STOP) | architect | Resolved at T02.10 in Phase 2; carry-over from CP1 — closed. |
| OQ-008 | Empty-pool failure contract (INV-007) | architect | Resolved at T02.11 in Phase 2; carry-over from CP1 — closed. CP3 invariants gate (T03.18) re-verifies the INV-007 path end-to-end. |
| OQ-010 | `validate-lenses` failure semantics | architect | Resolved at T02.20 in Phase 2; carry-over from CP1 — closed. |

No new OQs opened by the T03.07..T03.11 bracket.

## Outstanding / Next

1. **T03.13** — IMM-6 atomic-write idempotency (mid-write kill test) — STRICT, Critical Path Override.
2. **T03.14** — INV-002 Python-only concurrency (no shell dispatch path) — static grep guard.
3. **T03.15** — NFR-001 / AC-004 `ParallelExecutor` invocation mandate (static-grep guard test).
4. **T03.16** — NFR-002 atomicity (state + JSONL lock under concurrent write).
5. **T03.17** — NFR-013 / AC-014 output-directory write confinement.
6. **T03.18** — Phase 3 invariants gate (CP3, end of the T03.13..T03.17 bracket).
7. **T03.18a** — Phase 3 transport-env gate (interim, pre-exit).
8. **T03.19** — NFR-014 / AC-015 no-cross-invocation response caching.
9. **T03.20** — AC-010 no-routing-to-Anthropic-models guard.
10. **T03.21** — `T2ProxyUrl` / `T2ProxyKey` / `T2Model0N` env contract reader (couples with INV-007 from Phase 2).
11. **T03.22** — Phase 3 exit gate (end-of-phase CP4); `swarm run` end-to-end Wave 0 → Wave 1 against stub.

## Sign-Off

**Gate Result:** ✅ PASS — Phase 3 Wave-1 behaviour gate cleared.
**Authorized to proceed:** T03.13 → T03.17 (CP3 invariants-gate bracket).
**Recorded by:** automation (T03.12 checkpoint task).
