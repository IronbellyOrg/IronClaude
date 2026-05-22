# D-0061 — No-Shared-State Cross-Trial Integration Test (NFR-ISO1)

**Roadmap entry**: R-061
**Task**: T03.20
**Component(s) under test**: COMP-003 `RunOrchestrator` × COMP-006 `HomeIsolation`
**Source**: `tests/cli/eval/test_no_shared_state.py`
**Non-functional requirement**: NFR-ISO1 — "No shared HOMEs, no shared file
handles (e.g. `auggie-first.jsonl`), and no port collisions at
`--parallel 15`. Tests run N×15 trials."

## Purpose

T03.16 (D-0058) already proves that a *single* parallel run of 15 evals
yields per-eval isolated HOMEs, session_ids, and telemetry namespaces.
What T03.16 cannot detect is a class of regressions that only surface
*across* runs:

- A module-level dict that caches `mkdtemp` outputs by `eval_id` and
  returns the stale path on the next trial.
- A UUID generator seeded once per process so trial 1's session_ids
  re-appear in trial 2.
- A JSONL writer that holds a file handle open across runs and fans new
  writes into the previous trial's file.
- A future port allocator that binds at `setup` time and re-binds the
  same port in the next trial because the registry is never cleared.

T03.20 closes that gap by iterating the same composition `N=3` times
against a **single shared scratch root** and asserting cross-trial
uniqueness pairwise across all `3 × 15 = 45` evals.

## Integration scenario

### Wiring

```
trial in 0..N-1:
    spec list (15)
        │
        └─→ RunOrchestrator(run_one=isolation_worker_t{trial}, cancellation_token=None)
                  │
                  └─→ ThreadPoolExecutor(max_workers=clamp(parallel=8, [1,15]))
                          │
                          └─→ isolation_worker(spec):
                                  HomeIsolation(eval_id=spec.id,
                                                home_root=SHARED_scratch_root,
                                                session_id=f"sess-t{trial}-{spec.id}")
                                      │
                                      ├─ setup(config=permissive_config)
                                      │     → mkdtemp({eval_id}-…) under home_root
                                      ├─ env()
                                      │     → {HOME, CLAUDE_SESSION_ID}
                                      ├─ <write telemetry.jsonl in home_path/.eval-logs/>
                                      └─ teardown(keep=True)   ← directory survives
                                  return EvalOutcome(status="PASS", …,
                                                     artifacts={"telemetry": …})
        ↓
        records list (thread-safe append) capturing per-eval state
```

The `records` list is the join surface: every worker appends a single
dict with `trial`, `eval_id`, `home_path`, `session_id`, `env`, and
`telemetry_path`. After all 3 trials finish, the test reads back the
45 records and performs the cross-trial assertions.

### Parameters

| Symbol | Value | Source |
|---|---|---|
| `N_TRIALS` | 3 | Phase 3 task: "running 3 trials" (T03.20 AC1). |
| `EVALS_PER_TRIAL` | 15 | Phase 3 task: "15-eval parallel runs" (T03.20 AC1). |
| `PARALLEL` | 8 | Mirrors `DEFAULT_PARALLEL` in `orchestrator.py` and T03.16's choice. |
| `scratch_root` | `tmp_path / "eval-runs"` | Shared **across all 3 trials**, by design. |
| Spec id pattern | `E000…E014` | FR-SCH2 regex-safe, re-used across trials so a regression that keys cached state off `eval_id` surfaces. |
| Session id pattern | `sess-t{trial}-{spec.id}` | Trial number baked in so a per-trial canonical view stays unique even when env / JSONL views drift. |

### Telemetry payload (per eval)

```json
{
  "event": "eval_started",
  "trial": 1,
  "eval_id": "E007",
  "home_path": "/tmp/.../scratch_root/E007-XXXX",
  "session_id": "sess-t1-E007",
  "env_home": "/tmp/.../scratch_root/E007-XXXX",
  "env_session_id": "sess-t1-E007",
  "telemetry_namespace": "/tmp/.../scratch_root/E007-XXXX/.eval-logs/telemetry.jsonl"
}
```

## Test inventory

| # | Class.test | Verifies |
|---|---|---|
| 1 | `TestNoSharedStateAcrossTrials.test_three_trials_each_with_fifteen_evals_all_pass` | Pre-condition: every trial returns 15 PASS outcomes. |
| 2 | `TestNoSharedStateAcrossTrials.test_home_paths_pairwise_distinct_across_all_trials` | All 45 `home_path` values are pairwise distinct. |
| 3 | `TestNoSharedStateAcrossTrials.test_home_paths_all_under_shared_scratch_root` | Every HOME resolves under the shared scratch root (FR-ISO2 sanity). |
| 4 | `TestNoSharedStateAcrossTrials.test_session_ids_pairwise_distinct_across_all_trials` | All 45 `CLAUDE_SESSION_ID` values are unique in both the canonical record and the env dict views. |
| 5 | `TestNoSharedStateAcrossTrials.test_telemetry_paths_pairwise_distinct_across_all_trials` | All 45 JSONL paths are pairwise distinct (proxy for "no shared file handles"). |
| 6 | `TestNoSharedStateAcrossTrials.test_telemetry_contents_belong_to_owning_eval` | Each JSONL's embedded `trial`/`eval_id`/`session_id` matches the eval that wrote it. |
| 7 | `TestNoSharedStateAcrossTrials.test_no_port_state_leaks_into_per_eval_env` | No env key carries `PORT` in its name; structural defense against future port-bound state. |
| 8 | `TestNoSharedStateAcrossTrials.test_env_home_matches_recorded_home_path_for_every_eval` | `env()['HOME']` agrees with the recorded `home_path`; catches stale env-dict leaks across trials. |
| 9 | `TestNoSharedStateWithinEachTrial.test_each_trial_yields_fifteen_unique_homes` | Intra-trial regression guard: 15 unique HOMEs per trial. |
| 10 | `TestNoSharedStateWithinEachTrial.test_each_trial_yields_fifteen_unique_session_ids` | Intra-trial regression guard: 15 unique session_ids per trial. |

## Acceptance Criteria Mapping (T03.20)

| AC (verbatim) | Test(s) | Evidence line |
|---|---|---|
| File `tests/cli/eval/test_no_shared_state.py` runs 3 trials of 15-eval parallel runs and exits 0 | T1 (+T9/T10 sanity) | `evidence.md` §1 |
| Across all trials, per-eval HOME paths, session_ids, and JSONL paths are pairwise distinct | T2, T4, T5 (T6 strengthens, T8 closes env drift) | `evidence.md` §1 |
| No port-collision errors are recorded | T7 (structural — no port-bearing env keys present) | `evidence.md` §1 |
| `TASKLIST_ROOT/artifacts/D-0061/spec.md` documents the no-shared-state contract | (this file) | — |

## Out of scope

- Real `ClaudeProcessAdapter` / `PtyDriver` integration. The Phase 4
  PTY layer is exercised by T03.22 (`test_pty_lifecycle.py`); T03.20
  verifies the orchestrator + isolation composition across trials.
- Cancellation under load. T03.15's `TestCancellation` and the
  signal-handler suite (T03.07) cover that surface; mixing it into the
  cross-trial integration would dilute both signals.
- Real port binding. `HomeIsolation` does not bind ports today; T7
  asserts the structural pre-condition (no port-named env keys) so a
  future regression that introduces port state is caught at the same
  layer.
- Disk-budget breach mid-trial. T03.19's `test_disk_budget.py` owns
  that surface; T03.20 runs under the default unbounded budget.

## Dependencies

- **T02.11** (HomeIsolation) — `setup`/`env`/`teardown` and the
  `containment_guard` integration consumed by the worker.
- **T03.15** (RunOrchestrator) — `RunOrchestrator(run_one)` scheduling
  primitive consumed by every trial.
- **T03.16** (FR-G2 parallel-15 integration) — pattern reference for
  the isolation-worker factory and the JSONL telemetry shape; T03.20
  is the cross-trial sibling test.

## References

- Non-functional requirement: NFR-ISO1 in `design-spec.md`.
- Sibling deliverable: `.dev/releases/current/cliEval/artifacts/D-0058/spec.md`
  (T03.16 — the single-trial 15-eval integration this test extends).
- Orchestrator clamp constants: `src/superclaude/cli/eval/orchestrator.py`
  (`DEFAULT_PARALLEL=8`, `MAX_PARALLEL=15`).
- Isolation contract: `.dev/releases/current/cliEval/artifacts/D-0029/spec.md`
  (COMP-006 / DM-006 / FR-ISO1).
