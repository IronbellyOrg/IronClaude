# D-0061 — Verification Evidence

## §1 — Primary suite (T03.20)

Command:

```
uv run pytest tests/cli/eval/test_no_shared_state.py -v
```

Raw output: `../../evidence/T03.20/pytest-no-shared-state.txt`

Summary:

```
============================== 10 passed in 0.33s ==============================
```

| Test | Result | AC coverage |
|---|---|---|
| `TestNoSharedStateAcrossTrials::test_three_trials_each_with_fifteen_evals_all_pass` | PASSED | AC1: 3 trials × 15 evals all PASS |
| `TestNoSharedStateAcrossTrials::test_home_paths_pairwise_distinct_across_all_trials` | PASSED | AC2: HOME paths pairwise distinct |
| `TestNoSharedStateAcrossTrials::test_home_paths_all_under_shared_scratch_root` | PASSED | AC2 (FR-ISO2 sanity): all HOMEs contained |
| `TestNoSharedStateAcrossTrials::test_session_ids_pairwise_distinct_across_all_trials` | PASSED | AC2: session_ids pairwise distinct (record + env views) |
| `TestNoSharedStateAcrossTrials::test_telemetry_paths_pairwise_distinct_across_all_trials` | PASSED | AC2: JSONL paths pairwise distinct |
| `TestNoSharedStateAcrossTrials::test_telemetry_contents_belong_to_owning_eval` | PASSED | AC2 (strengthening): no JSONL cross-talk |
| `TestNoSharedStateAcrossTrials::test_no_port_state_leaks_into_per_eval_env` | PASSED | AC3: no port-bearing env keys present |
| `TestNoSharedStateAcrossTrials::test_env_home_matches_recorded_home_path_for_every_eval` | PASSED | AC2 (env-drift guard): env HOME matches recorded HOME |
| `TestNoSharedStateWithinEachTrial::test_each_trial_yields_fifteen_unique_homes` | PASSED | Intra-trial sanity: 15 unique HOMEs per trial |
| `TestNoSharedStateWithinEachTrial::test_each_trial_yields_fifteen_unique_session_ids` | PASSED | Intra-trial sanity: 15 unique session_ids per trial |

## §2 — Regression (orchestrator + isolation + sibling FR-G2 integration)

Command:

```
uv run pytest tests/cli/eval/test_no_shared_state.py \
              tests/cli/eval/test_parallel_15.py \
              tests/cli/eval/test_orchestrator.py \
              tests/cli/eval/test_home_isolation.py
```

Raw output: `../../evidence/T03.20/pytest-regression.txt`

Summary:

```
============================== 64 passed in 2.85s ==============================
```

No regressions in:

- `tests/cli/eval/test_no_shared_state.py` — 10/10 (T03.20, new)
- `tests/cli/eval/test_parallel_15.py` — 7/7 (T03.16)
- `tests/cli/eval/test_orchestrator.py` — 20/20 (T03.15)
- `tests/cli/eval/test_home_isolation.py` — 27/27 (T02.11)

## §3 — Acceptance Criteria Closure

| AC | Status | Evidence |
|---|---|---|
| File `tests/cli/eval/test_no_shared_state.py` runs 3 trials of 15-eval parallel runs and exits 0 | ✅ | §1 row 1 (+ rows 9/10 confirming per-trial structure) |
| Across all trials, per-eval HOME paths, session_ids, and JSONL paths are pairwise distinct | ✅ | §1 rows 2 / 4 / 5 (+ rows 6 / 8 strengthening) |
| No port-collision errors are recorded | ✅ | §1 row 7 (structural assertion: no `PORT`-bearing env keys in any per-eval env) |
| `TASKLIST_ROOT/artifacts/D-0061/spec.md` documents the no-shared-state contract | ✅ | `spec.md` |

## §4 — File manifest

```
tests/cli/eval/test_no_shared_state.py                     — new, ~430 LOC, 10 tests
.dev/releases/current/cliEval/artifacts/D-0061/spec.md     — integration scenario
.dev/releases/current/cliEval/artifacts/D-0061/notes.md    — design notes
.dev/releases/current/cliEval/artifacts/D-0061/evidence.md — this file
.dev/releases/current/cliEval/evidence/T03.20/pytest-no-shared-state.txt — raw pytest
.dev/releases/current/cliEval/evidence/T03.20/pytest-regression.txt      — raw regression
```
