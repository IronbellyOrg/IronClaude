# D-0058 — Parallel 15-Eval Integration Scenario (FR-G2)

**Roadmap entry**: R-058
**Task**: T03.16
**Component(s) under test**: COMP-003 `RunOrchestrator` × COMP-006 `HomeIsolation`
**Source**: `tests/cli/eval/test_parallel_15.py`
**Functional requirement**: FR-G2 — "Run all 15 evals in parallel (default
concurrency=8, max=15) with strict isolation: each eval owns its own HOME
directory, its own session_id, and its own state/telemetry namespace."

## Purpose

Verify the orchestrator + isolation composition behaves correctly at the
scale and concurrency the cliEval harness must support in production:

1. **Throughput** — 15 evals submitted at `--parallel 8` complete cleanly
   and produce one PASS outcome per spec.
2. **Per-eval HOME isolation** — every eval runs under a unique HOME
   directory (mkdtemp under the scratch root, prefixed `{eval_id}-`).
3. **Per-eval session_id** — every eval's `CLAUDE_SESSION_ID` is distinct,
   visible in three independent views: the worker's recorded snapshot,
   the per-eval JSONL telemetry, and the live `env()` mapping.
4. **Per-eval telemetry namespace** — each eval writes its own
   `home_path/.eval-logs/telemetry.jsonl`, contained strictly under that
   eval's HOME, never cross-talking with siblings.
5. **NFR-PERF2 clamp** — `parallel=16` saturates at `MAX_PARALLEL=15`;
   `parallel=15` actually admits 15 simultaneous workers.

## Integration scenario

### Wiring

```
spec list (15)
    │
    └─→ RunOrchestrator(run_one=isolation_worker, cancellation_token=None)
              │
              └─→ ThreadPoolExecutor(max_workers=clamp(parallel, [1,15]))
                      │
                      └─→ isolation_worker(spec):
                              HomeIsolation(eval_id=spec.id,
                                            home_root=scratch_root,
                                            session_id=f"sess-{spec.id}")
                                  │
                                  ├─ setup(config=permissive_config)
                                  │     → mkdtemp({eval_id}-…) under home_root
                                  ├─ env()
                                  │     → {HOME, CLAUDE_SESSION_ID, …}
                                  ├─ <write telemetry.jsonl in home_path/.eval-logs/>
                                  └─ teardown(keep=True)   ← directory survives
                              return EvalOutcome(status="PASS", …,
                                                 artifacts={"telemetry": …})
```

The worker substitutes for the Phase 4 spawn/inject/observe pipeline; FR-G2
is verified at the orchestrator + isolation composition layer, which is
exactly what T03.16 is scoped to.

### Specs

15 frozen `EvalSpec` rows with `id ∈ {eval-00, …, eval-14}`,
`category="smoke"`, `timeout_sec=60.0`, `requires=()`.

### Configuration

`EvalConfig` built with `allowed_scratch_roots=(scratch_root,)` so the
`containment_guard` invoked inside `HomeIsolation.setup` accepts the
test's tmpdir without granting blanket allowlist exemptions.

### Telemetry payload (per eval)

```json
{
  "event": "telemetry.smoke",
  "eval_id": "eval-07",
  "home_path": "/tmp/.../scratch_root/eval-07-XXXX",
  "session_id": "sess-eval-07",
  "env_home": "/tmp/.../scratch_root/eval-07-XXXX",
  "env_session_id": "sess-eval-07",
  "telemetry_namespace": "/tmp/.../scratch_root/eval-07-XXXX/.eval-logs"
}
```

## Test inventory

| # | Class.test | Verifies |
|---|---|---|
| 1 | `TestParallel15.test_runs_fifteen_evals_at_parallel_eight_exits_clean` | 15/15 PASS, observed concurrency ∈ [1, 8], duration well under suite timeout. |
| 2 | `TestParallel15.test_each_eval_receives_unique_home_path` | All 15 `home_path`s distinct, all under `scratch_root`. |
| 3 | `TestParallel15.test_each_eval_receives_unique_session_id` | `session_id` distinct in record, JSONL, and live `env()` views. |
| 4 | `TestParallel15.test_each_eval_has_isolated_telemetry_namespace` | All 15 `.eval-logs` namespaces distinct, each strictly inside its own HOME. |
| 5 | `TestParallel15.test_per_eval_jsonl_contents_are_self_consistent` | No cross-talk: JSONL `eval_id`/`home_path`/`session_id` match the spec they belong to. |
| 6 | `TestParallelClampAtFifteen.test_parallel_sixteen_clamps_to_fifteen` | `parallel=16` over 20 specs ⇒ peak concurrency ≤ 15. |
| 7 | `TestParallelClampAtFifteen.test_parallel_at_max_admits_fifteen_concurrent_workers` | `parallel=15` ⇒ exactly 15 concurrent (proves the clamp is not over-restrictive). |

## Acceptance Criteria Mapping (FR-G2 / Phase 3 T03.16)

| AC (verbatim) | Test(s) | Evidence line |
|---|---|---|
| File `tests/cli/eval/test_parallel_15.py` runs a 15-eval fixture suite at `--parallel 8` and exits 0 | T1 | `evidence.md` §1 |
| Each eval receives its own HOME, session_id, and telemetry namespace (verified by per-eval JSONL inspection) | T2, T3, T4, T5 | `evidence.md` §1 |
| `parallel=16` clamps to 15; recorded in test assertions | T6 | `evidence.md` §1 |
| `TASKLIST_ROOT/artifacts/D-0058/spec.md` documents the integration scenario | (this file) | — |

## Out of scope

- Real `ClaudeProcessAdapter` / `PtyDriver` integration. Phase 4 wires
  those into the worker; D-0058 verifies the scheduler+isolation layer.
- Hook deploy under each isolated HOME. T03.04 owns deploy; the worker
  here writes telemetry directly to exercise the namespace path.
- Cancellation under load. T03.15's `TestCancellation` covers the cancel
  semantics; T03.16 verifies the happy-path 15-wide composition.

## Dependencies

- **T02.11** (HomeIsolation) — `setup`/`env`/`teardown` methods and the
  `containment_guard` integration consumed by the worker.
- **T03.15** (RunOrchestrator) — `RunOrchestrator(run_one, cancellation_token)`
  scheduling primitive consumed by every test.

## References

- Functional requirement: `design-spec.md` line 19 (FR-G2).
- Clamp constants: `src/superclaude/cli/eval/orchestrator.py`
  (`DEFAULT_PARALLEL=8`, `MIN_PARALLEL=1`, `MAX_PARALLEL=15`).
- Isolation contract: `.dev/releases/current/cliEval/artifacts/D-0050/spec.md`
  (COMP-006 / DM-006).
- Sibling deliverable: `.dev/releases/current/cliEval/artifacts/D-0057/spec.md`
  (the orchestrator primitive this test composes with).
