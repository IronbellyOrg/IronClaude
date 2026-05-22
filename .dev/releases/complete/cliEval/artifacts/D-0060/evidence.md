# D-0060 Disk-Budget Poller — Verification Evidence

Captured 2026-05-20 on branch `fix/prd-path-resolution-and-templates`.

## 1. Files delivered

| Path | Role | State |
|---|---|---|
| `src/superclaude/cli/eval/disk_budget.py` | `DiskBudgetPoller` + `BreachDetail` + module constants | new |
| `src/superclaude/cli/eval/orchestrator.py` | `disk_budget_poller=` constructor param + breach-aware submission loop + `_disk_budget_skipped_outcome` helper | modified |
| `tests/cli/eval/test_disk_budget.py` | 33 tests across 8 classes covering constants, constructor guards, defaults, disabled mode, breach detection, side-car payload, symlink handling, `BreachDetail`, and orchestrator integration | new |
| `.dev/releases/current/cliEval/artifacts/D-0060/spec.md` | Contract documentation | new |
| `.dev/releases/current/cliEval/artifacts/D-0060/notes.md` | Design notes | new |
| `.dev/releases/current/cliEval/artifacts/D-0060/evidence.md` | This file | new |
| `.dev/releases/current/cliEval/evidence/T03.19/pytest-disk-budget.txt` | Verbatim pytest output (disk-budget suite) | new |
| `.dev/releases/current/cliEval/evidence/T03.19/pytest-orchestrator-regression.txt` | Verbatim pytest output (orchestrator regression) | new |

## 2. Unit test run — `test_disk_budget.py`

Command: `uv run pytest tests/cli/eval/test_disk_budget.py -v`

Result: **33 passed in 1.16s**

Per-class breakdown:

| Class | Tests | Result |
|---|---|---|
| `TestPublicConstants` | 5 | PASS |
| `TestConstructorGuards` | 6 | PASS |
| `TestDefaults` | 4 | PASS |
| `TestDisabledPoller` | 2 | PASS |
| `TestBreachDetection` | 6 | PASS |
| `TestSymlinkHandling` | 1 | PASS |
| `TestBreachDetail` | 1 | PASS |
| `TestOrchestratorIntegration` | 8 | PASS |

## 3. Regression run — `test_orchestrator.py`

Command: `uv run pytest tests/cli/eval/test_orchestrator.py -v`

Result: **20 passed in 0.49s** (unchanged from D-0057 baseline).

The disk-budget integration is fully backward-compatible: omitting
`disk_budget_poller=` leaves the orchestrator behaviour byte-identical
to the D-0057 contract.

## 4. Acceptance criteria → evidence mapping

| AC from T03.19 | Test(s) | Result |
|---|---|---|
| RunOrchestrator polls disk usage every 5s when `--max-disk-mb` is set (default 1024 MB) | `TestPublicConstants::test_default_budget_is_1024_mb`, `TestPublicConstants::test_default_tick_is_5_seconds`, `TestDefaults::test_default_budget_uses_module_constant`, `TestDefaults::test_default_tick_uses_module_constant` | PASS (4/4) |
| Filling the run dir past budget triggers `disk_budget_exceeded` artifact and exit-code constant `2` | `TestBreachDetection::test_breach_writes_side_car_with_payload`, `TestBreachDetection::test_breach_detail_matches_side_car`, `TestPublicConstants::test_breach_exit_code_is_2`, `TestPublicConstants::test_artifact_name_is_pinned` | PASS (4/4) |
| In-flight evals complete after breach | `TestOrchestratorIntegration::test_inflight_workers_complete_after_breach` | PASS |
| New evals are not scheduled after breach | `TestOrchestratorIntegration::test_breach_stops_scheduling_but_preserves_outcome_per_spec` | PASS |
| `--max-disk-mb 0` disables the poller (verified by writing past would-be-budget without interruption) | `TestDefaults::test_disabled_when_budget_zero`, `TestDisabledPoller::test_start_is_noop_when_disabled`, `TestDisabledPoller::test_breach_does_not_fire_when_disabled`, `TestOrchestratorIntegration::test_disabled_poller_does_not_change_behavior` | PASS (4/4) |
| TASKLIST_ROOT/artifacts/D-0060/spec.md documents the poller cadence and breach semantics | `.dev/releases/current/cliEval/artifacts/D-0060/spec.md` (8 sections, ~9 KB) | PASS |

## 5. Breach semantics validation

| Path | Test | Result |
|---|---|---|
| Breach triggers when usage exceeds budget | `TestBreachDetection::test_breach_triggers_when_usage_exceeds_budget` | PASS |
| Side-car JSON contains `reason`, `output_dir`, `usage_bytes`, `budget_bytes`, `max_disk_mb`, `ticked_at` | `TestBreachDetection::test_breach_writes_side_car_with_payload` | PASS |
| `BreachDetail.to_dict()` matches side-car on-disk | `TestBreachDetection::test_breach_detail_matches_side_car` | PASS |
| Breach is one-shot (cleanup does not clear the flag) | `TestBreachDetection::test_breach_is_one_shot` | PASS |
| Usage under budget does not trigger breach | `TestBreachDetection::test_no_breach_when_usage_under_budget` | PASS |
| `artifact_path()` returns `None` before breach | `TestBreachDetection::test_artifact_path_returns_none_before_breach` | PASS |
| Symlinks are skipped (no double-counting via sibling tree) | `TestSymlinkHandling::test_symlinks_are_skipped` | PASS |

## 6. Orchestrator integration validation

| Path | Test | Result |
|---|---|---|
| `disk_budget_poller=None` is the no-op default | `TestOrchestratorIntegration::test_orchestrator_accepts_optional_poller` | PASS |
| `max_disk_mb=0` poller wired through orchestrator is a no-op | `TestOrchestratorIntegration::test_disabled_poller_does_not_change_behavior` | PASS |
| Pre-existing breach → all specs SKIPPED with pinned `skip_reason` + `skip_flag_triggered` | `TestOrchestratorIntegration::test_breach_stops_scheduling_but_preserves_outcome_per_spec` | PASS |
| Mid-run breach → in-flight workers run to completion | `TestOrchestratorIntegration::test_inflight_workers_complete_after_breach` | PASS |
| Outcome order preserved even with SKIPPED backfills | `TestOrchestratorIntegration::test_breach_outcome_order_matches_input_order` | PASS |
| Healthy poller → all PASS, no SKIPPED synthesis | `TestOrchestratorIntegration::test_no_breach_means_all_pass` | PASS |
| Poller thread joined when `run()` returns | `TestOrchestratorIntegration::test_breach_stops_poller_on_orchestrator_exit` | PASS |
| Cancellation dominates breach (operator intent overrides resource limit) | `TestOrchestratorIntegration::test_cancellation_takes_priority_over_disk_breach` | PASS |

## 7. Constructor guards

| Guard | Test | Result |
|---|---|---|
| `max_disk_mb < 0` → `ValueError` | `TestConstructorGuards::test_negative_budget_rejected` | PASS |
| `max_disk_mb` non-int → `TypeError` | `TestConstructorGuards::test_non_int_budget_rejected` | PASS |
| `max_disk_mb=True` → `TypeError` (booleans rejected) | `TestConstructorGuards::test_boolean_budget_rejected` | PASS |
| `tick_sec == 0` → `ValueError` | `TestConstructorGuards::test_zero_tick_rejected` | PASS |
| `tick_sec < 0` → `ValueError` | `TestConstructorGuards::test_negative_tick_rejected` | PASS |
| `artifact_name == ""` → `ValueError` | `TestConstructorGuards::test_empty_artifact_name_rejected` | PASS |

## 8. Out-of-scope confirmations

The following are intentionally NOT exercised by these tests (handled by
other phases/tasks):

- CLI flag wiring (`--max-disk-mb 0|1024|N`) — Phase 4 dispatcher.
- Reporter side-car surfacing into `RunSummary.artifacts["disk_budget_exceeded"]`
  — COMP-008 / T03.13.
- Disk-space pre-flight checks (doctor command) — separate roadmap row.
- Per-eval HOME / scratch reclamation on breach — out of scope; workers
  finish with whatever HOME they own.

## 9. Sign-off

All T03.19 acceptance criteria verified by automated tests. The disk-
budget primitive and orchestrator integration are ready for the Phase 4
CLI dispatcher to bind `--max-disk-mb` and translate
`DISK_BUDGET_EXCEEDED_EXIT_CODE = 2` into the process exit status.
