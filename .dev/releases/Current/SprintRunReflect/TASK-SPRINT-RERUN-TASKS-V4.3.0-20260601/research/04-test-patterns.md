# Research 04: Test & Verification Patterns

**Status:** Complete
**Researcher:** #4
**Topic:** Test framework, patterns, and AC→test mapping for `superclaude sprint rerun-tasks` v4.3.0
**TDD source:** `/config/workspace/IronClaude/.dev/releases/backlog/SprintGranularResume/merged-requirements.md` §Acceptance criteria (lines 261-270)

---

## 1. Test Framework & Discovered Conventions

### 1.1 Framework
- **pytest** with `from __future__ import annotations` header in every sprint test file (evidence: `tests/sprint/test_checkpoints.py:11`, `test_e2e_success.py:7`, `test_cli_contract.py:7`).
- **Click testing** via `from click.testing import CliRunner` for CLI subcommand tests (`tests/sprint/test_cli_contract.py:9`, `test_checkpoints.py:18`).
- **Mocking style:** `from unittest.mock import patch` with multi-stacked `with` blocks for subprocess/notify isolation (`tests/sprint/test_e2e_success.py:11`, `:96-106`). No `pytest-mock`; pure stdlib.

### 1.2 conftest.py for sprint
- **No `tests/sprint/conftest.py` exists.** Sprint tests use only:
  - `tmp_path` (pytest built-in).
  - The repo-root `tests/conftest.py:28-79` session-scoped `_pollution_snapshot` and `tests/conftest.py:82-117` autouse `_redirect_reflexion_writes` fixtures (apply globally).
- A nested `tests/sprint/diagnostic/conftest.py` exists but is scoped to the `diagnostic/` subdirectory and not consumed by top-level sprint tests.
- **Implication:** new tests for `rerun-tasks` should rely on `tmp_path` + local helper functions (mirroring `_make_config`, `_seed_sprint`, `_build_phase` patterns) rather than a shared conftest. If shared helpers grow large, introduce `tests/sprint/conftest.py` as part of this work.

### 1.3 Naming conventions
- File: `test_<module_name>.py` directly mirrors `src/superclaude/cli/sprint/<module_name>.py` (`tests/sprint/test_checkpoints.py` ↔ `src/superclaude/cli/sprint/checkpoints.py`).
- **Class grouping:** `class TestXxxYyy:` per unit-under-test, where `XxxYyy` matches a function or behavior (e.g. `TestExtractCheckpointPaths`, `TestVerifyCheckpointFiles`, `TestVerifyCheckpointsGate`, `TestRecoverMissingCheckpoints`, `TestVerifyCheckpointsCLI` in `test_checkpoints.py:42, 128, 186, 402, 524`).
- **Function naming:** `test_<scenario>` snake_case (e.g. `test_zero_checkpoints`, `test_shadow_mode_emits_event_no_stdout`, `test_full_mode_downgrades_status_on_missing`).
- **Tests covering specific TDD/AC IDs:** module docstring opens with the task ID (e.g. `test_cli_contract.py:1` `"""T07.03 — CLI contract validation..."""`, `test_e2e_success.py:1` `"""T07.01 — E2E test: 3-phase sprint to completion."""`, `test_backward_compat_regression.py:1` `"""T09.02 — Backward compatibility regression..."""`).

### 1.4 Parametrize
- Used **sparingly**; `test_checkpoints.py` does NOT use `@pytest.mark.parametrize` — instead it uses one-method-per-scenario classes. Of the four files surveyed (`test_checkpoints.py`, `test_cli_contract.py`, `test_e2e_success.py`, `test_backward_compat_regression.py`), zero use `parametrize`.
- **Recommendation:** follow the same convention — separate test methods per AC scenario; reserve `parametrize` only for matrix expansions like "all 4 gate modes" (cf. `test_checkpoints.py:277-280` iterates inline with a `for` loop inside one test, not `parametrize`).

### 1.5 Fixture / setup conventions
- `CliRunner` instantiation via `setup_method` on a `class` (`test_cli_contract.py:17-18`), OR inline `runner = CliRunner()` per test (`test_checkpoints.py:530`).
- Helpers as **module-level functions** prefixed with `_` (e.g. `_make_config`, `_seed_sprint`, `_build_phase`, `_read_events`, `_popen_factory_all_pass`) — *not* fixtures.
- Subprocess mocking uses a custom `_FakePopenSuccess`/`_FakePopenExit1` class with `poll()`/`wait()` methods + a closure-based `_popen_factory(config)` returning the `side_effect` callable (`test_e2e_success.py:42-86`, `test_e2e_halt.py:44-93`).

### 1.6 Markers
- `@pytest.mark.integration` on integration tests (`test_execute_sprint_integration.py:89`).
- No `@pytest.mark.unit` is set explicitly; the repo-root `tests/conftest.py` and `src/superclaude/pytest_plugin.py` apply auto-markers by directory.
- For the new `rerun-tasks` work: mark E2E/round-trip tests with `@pytest.mark.integration` (AC2, AC3); leave unit tests unmarked.

### 1.7 Imports & target SoT
- All tests import from `superclaude.cli.sprint.*` (production code lives in `src/superclaude/cli/sprint/`). Examples:
  - `from superclaude.cli.sprint.checkpoints import (build_manifest, extract_checkpoint_paths, ...)` (`test_checkpoints.py:20-26`)
  - `from superclaude.cli.sprint.commands import sprint_group, verify_checkpoints` (`test_cli_contract.py:11`, `test_checkpoints.py:27`)
  - `from superclaude.cli.sprint.executor import execute_sprint, _verify_checkpoints` (`test_e2e_success.py:13`, `test_checkpoints.py:28`)
  - `from superclaude.cli.sprint.models import Phase, SprintConfig, PhaseStatus, CheckpointEntry` (`test_checkpoints.py:30-35`, `test_e2e_success.py:14-17`)
- **For rerun-tasks:** new imports will resolve to `superclaude.cli.sprint.recovery`, `superclaude.cli.sprint.rerun_tasks`.

---

## 2. The Canonical Mirror Pattern (recovery.py ↔ checkpoints.py)

`test_checkpoints.py` is the gold-standard mirror for `tests/sprint/test_recovery.py`. Structural template:

```
1. Module docstring: "Tests for sprint recovery bundle, audit log, and merge orchestration."
2. from __future__ import annotations
3. Stdlib + third-party imports (click.testing.CliRunner if needed)
4. Production imports from superclaude.cli.sprint.recovery
5. Section header banner comments separating unit-under-test groups:
   # ---------------------------------------------------------------------------
   # RecoveryBundle construction
   # ---------------------------------------------------------------------------
6. One TestXxx class per concept.
7. Module-level _helper functions for fixture-like setup (e.g., _seed_recovery_bundle).
```

Reference banner format: `test_checkpoints.py:37-39, 123-125, 150-152, 260-262, 283-285, 397-399, 519-521`.

---

## 3. CLI Contract Test Pattern (for the 9+ new flags)

`test_cli_contract.py` covers documented options by invoking `--help` and asserting flag tokens appear in `result.output`:

```python
def test_run_help(self):
    result = self.runner.invoke(sprint_group, ["run", "--help"])
    assert result.exit_code == 0
    assert "--start" in result.output
    assert "--end" in result.output
    ...
```
(evidence: `test_cli_contract.py:31-43`)

**For rerun-tasks**, mirror this pattern: a single `TestRerunTasksContract` class with one method per flag/help concern. Required flags from TDD §CLI shape (line 184):
- `--phase` (int, required when not using `--from-reflect-report`)
- `--tasks` (comma-separated T-IDs)
- `--merge-back / --no-merge-back` (default ON)
- `--dry-run`
- `--include-transitive` (default OFF)
- `--ignore-deps`
- `--force-merge`
- `--allow-loop`
- `--no-verify-checkpoints` (default OFF, i.e., verify runs)
- `--bundle-dir <path>`
- `--restore`
- `--from-reflect-report <path>` (mutually exclusive with `--phase --tasks`)

---

## 4. E2E / Integration Test Pattern (AC1–AC8 round-trip)

The integration template is `test_e2e_success.py` + `test_e2e_halt.py` + `test_execute_sprint_integration.py`:

1. **Build `SprintConfig` with `tmp_path` as `release_dir`** and N synthetic phase tasklist files written via `pf.write_text(...)`. (`test_e2e_success.py:20-39`, `test_e2e_halt.py:22-41`).
2. **Mock `subprocess.Popen` via a closure factory** that writes the result + output files for each call (`test_e2e_success.py:59-86`, `test_e2e_halt.py:74-93`).
3. **Stack `patch()` blocks**: `shutil.which`, `subprocess.Popen`, `os.setpgrp`, `notify._notify` (`test_e2e_success.py:97-106`).
4. **Assert on JSONL stream:** parse `config.execution_log_jsonl`, filter by `event` key, count per-phase. (`test_e2e_success.py:131-163`, `test_e2e_halt.py:118-125`).
5. **Assert on Markdown log:** read `config.execution_log_md` and check `"**Outcome**: success"` / `"**Halted at**: Phase 2"` (`test_e2e_success.py:236-237`, `test_e2e_halt.py:181`).
6. **SystemExit assertion** for failure paths: `with pytest.raises(SystemExit) as exc: execute_sprint(config); assert exc.value.code == 1` (`test_e2e_halt.py:114-116`).

For round-trip (AC3), the pattern is: run the all-pass factory twice (different `tmp_path`s — once clean, once fail-then-rerun), diff the resulting directory trees with explicit filter for timestamps and `recovery_history` entries.

---

## 5. Backward-compat Regression Pattern (informs additive verification)

`test_backward_compat_regression.py:1-57` enforces the "new feature must not perturb existing surface" rule:
- Imports broad surface (`execute_pipeline`, `gate_passed`, `aggregate_task_results`, `execute_phase_tasks`).
- Asserts thread count delta is zero (`threading.active_count()` snapshot before/after).
- Asserts old fixture inputs produce byte-equivalent old behavior under default config.

For rerun-tasks, a regression test should assert: sprint without `rerun-tasks` invocation behaves identically pre/post — no new threads, no new JSONL event types fired, no new files written under canonical paths.

---

## 6. AC → Test Plan Mapping Table

Test file destinations:
- `tests/sprint/test_recovery.py` — NEW (mirrors `recovery.py`)
- `tests/sprint/test_rerun_tasks.py` — NEW (mirrors `rerun_tasks.py`)
- `tests/sprint/test_cli_contract.py` — EDIT (extend `TestRerunTasksContract`)
- `tests/sprint/test_models.py` — EDIT (FAIL_RECOVERABLE enum, PhaseResult fields)
- `tests/sprint/test_executor.py` — EDIT (phase-result-json write + FAIL classification)
- `tests/sprint/test_rerun_tasks_e2e.py` — NEW (AC2, AC3 integration)
- `tests/sprint/test_rerun_tasks_failure_modes.py` — NEW (AC4–AC8 negative paths)
- `tests/sprint/test_backward_compat_regression.py` — EDIT (rerun-tasks no-op regression)

### Mapping table

| AC | Test file | Test class / function | Type | Fixtures | Mock approach |
|---|---|---|---|---|---|
| AC1 (`--dry-run` extraction plan) | `tests/sprint/test_rerun_tasks_e2e.py` | `class TestRerunTasksDryRun` → `test_dry_run_prints_plan_does_not_execute` | integration | `tmp_path`; helper `_seed_phase_with_tasks(tmp_path, phase=7, task_ids=["T07.11","T07.12"])` | `CliRunner.invoke(sprint_group, ["rerun-tasks", str(index), "--phase", "7", "--tasks", "T07.11,T07.12", "--dry-run"])`; assert no Popen called via `patch("...subprocess.Popen")` with `assert_not_called()` |
| AC2 (full re-execute + rename + flip + JSONL + verify-checkpoints) | `tests/sprint/test_rerun_tasks_e2e.py` | `class TestRerunTasksRoundTrip` → `test_rerun_renames_originals_flips_checkboxes_emits_event_runs_verify_checkpoints` | integration | `tmp_path`; `_seed_failed_phase(tmp_path, phase=7)` writes pre-existing `phase-7-result.json` with 2 FAIL_RECOVERABLE tasks; pre-existing `T07.11-transcript.jsonl` etc. | Stacked `patch()` on Popen factory (mirrors `_popen_factory_all_pass` in `test_e2e_success.py:59`); assert renamed files match `*.failed-<ts>` glob; parse `execution-log.jsonl`, filter `event=="phase_rerun_complete"`, assert exactly one; assert `phase-7-cp2.md` exists after run |
| AC3 (round-trip artifact equivalence) | `tests/sprint/test_rerun_tasks_e2e.py` | `class TestRerunTasksRoundTrip` → `test_artifact_set_equivalence_clean_vs_failed_then_rerun` | integration | Two `tmp_path` workspaces via `tmp_path_factory.mktemp`; `_seed_canonical_3phase_sprint` | Same Popen mocking pattern; `_diff_workspace_trees(a, b, ignore={"timestamps","recovery_history"})` helper compares relative path sets and file content modulo timestamps |
| AC4 (concurrent lock file) | `tests/sprint/test_rerun_tasks_failure_modes.py` | `class TestRerunTasksLocking` → `test_second_concurrent_invocation_aborts_with_lock_pid` | integration | `tmp_path`; manually pre-create `<release_dir>/.rerun-phase-7.lock` containing parent PID | `CliRunner.invoke(...)`; assert `result.exit_code != 0` and `"already running"` + str(pid) in `result.output` |
| AC5 (SHA256 mismatch + --force-merge) | `tests/sprint/test_rerun_tasks_failure_modes.py` | `class TestRerunTasksSHACheck` → `test_source_tasklist_sha_mismatch_aborts`, `test_force_merge_proceeds_with_warning` | integration | `tmp_path`; helper `_seed_sprint_with_recorded_sha(tmp_path, phase=7, original_sha="abc...")` then mutate file content post-record | `CliRunner.invoke(rerun-tasks, [..., "--phase", "7", "--tasks", "T07.11"])` asserts abort; rerun with `--force-merge` asserts exit 0 and `"WARN"` in output |
| AC6 (retry cap, --allow-loop override) | `tests/sprint/test_rerun_tasks_failure_modes.py` | `class TestRerunTasksRetryCap` → `test_fourth_attempt_aborts_with_cap_message`, `test_allow_loop_bypasses_cap` | integration | `tmp_path`; pre-seed `recovery_history` in `phase-7-result.json` with 3 prior attempts for `T07.11` | `CliRunner.invoke(...)`; assert `"retry-cap"` or `"3 prior attempts"` in stderr/output; second invocation adds `--allow-loop`, asserts exit 0 |
| AC7 (legacy fallback via transcript heuristic) | `tests/sprint/test_rerun_tasks_failure_modes.py` | `class TestRerunTasksLegacyFallback` → `test_missing_phase_result_json_falls_back_to_transcript_inspection`, `test_is_error_flag_triggers_failed_task_discovery`, `test_output_tokens_heuristic_discovers_truncated_tasks` | integration | `tmp_path`; `_seed_legacy_sprint(tmp_path, phase=7)` writes `T07.11-transcript.jsonl` with `is_error=true`, `T07.12-transcript.jsonl` with `output_tokens=0`, NO `phase-7-result.json` | Direct `rerun_tasks.discover_failed_tasks(phase=7, release_dir=tmp_path)` unit-style + CLI invoke; assert returned T-IDs == `["T07.11","T07.12"]` |
| AC8 (ABORT pre-merge auto-restore) | `tests/sprint/test_rerun_tasks_failure_modes.py` | `class TestRerunTasksAbortRestore` → `test_abort_before_merge_back_restores_source_tasklist`, `test_abort_clears_rerun_in_progress_flag` | integration | `tmp_path`; pre-seed `phase-7-tasklist.md` with pre-rerun checkbox state hashed; Popen mock raises mid-execution | Use `_FakePopenExit1` style (cf. `test_e2e_halt.py:59-71`); assert post-abort hash of `phase-7-tasklist.md` matches pre-state; assert no `rerun_in_progress: true` field remains in `phase-7-result.json` |

---

## 7. Unit Tests for New Modules

### 7.1 `tests/sprint/test_recovery.py` (mirrors `test_checkpoints.py` structure)

| Test class | Test function | Notes |
|---|---|---|
| `TestRecoveryBundle` | `test_construct_empty_bundle` | All-default constructor produces empty `entries`, `status=PENDING`. |
| `TestRecoveryBundle` | `test_add_entry_transitions_to_in_progress` | First `add_entry()` flips `status` IN_PROGRESS. |
| `TestRecoveryBundle` | `test_finalize_transitions_to_complete` | After `finalize()`, status COMPLETE; immutable post-finalize. |
| `TestRecoveryBundle` | `test_finalize_with_failures_transitions_to_partial` | Mixed-result bundle → `PARTIAL`. |
| `TestRecoveryBundle` | `test_serialize_to_json_includes_summary` | Mirrors `TestWriteManifest.test_writes_valid_json_with_summary` (`test_checkpoints.py:354-371`). |
| `TestRecoveryStatus` | `test_status_values_and_properties` | Mirrors `TestPassMissingCheckpointStatus.test_value_and_properties` (`test_checkpoints.py:266-271`). |
| `TestMergeRecoveryBundle` | `test_merge_writes_audit_log_entry` | `merge_recovery_bundle()` appends JSONL line to `<release_dir>/rerun-audit.log`. |
| `TestMergeRecoveryBundle` | `test_merge_is_idempotent` | Second merge of same bundle is a no-op. |
| `TestMergeRecoveryBundle` | `test_merge_failure_rolls_back_atomically` | Filesystem partial-failure simulated via `patch("pathlib.Path.write_text", side_effect=OSError)`. |
| `TestNominatorProtocol` | `test_manual_nominator_returns_explicit_task_ids` | Smoke test for protocol conformance. |
| `TestSharedAuditLogWriter` | `test_writer_appends_jsonl_line_with_timestamp` | Mirrors logger pattern from `test_checkpoints.py:179-183` `_read_events`. |
| `TestSharedAuditLogWriter` | `test_writer_creates_directory_if_missing` | Defensive mkdir behavior. |

### 7.2 `tests/sprint/test_rerun_tasks.py` (mirrors `test_checkpoints.py` structure)

| Test class | Test function | Notes |
|---|---|---|
| `TestExtractPhaseSubset` | `test_single_task_id_returns_one_entry` | Mirrors `TestExtractCheckpointPaths.test_single_checkpoint_backticks` (`test_checkpoints.py:48-58`). |
| `TestExtractPhaseSubset` | `test_multiple_task_ids_preserves_order` | T07.11,T07.12 → list maintains comma-separated order. |
| `TestExtractPhaseSubset` | `test_unknown_task_id_raises_or_returns_empty` | Per TDD §T1 (line 19) parser semantics. |
| `TestExtractPhaseSubset` | `test_task_id_with_dependencies_returns_only_named_when_ignore_deps` | `--ignore-deps` skips dep walker. |
| `TestExtractPhaseSubset` | `test_include_transitive_expands_closure` | `--include-transitive` pulls in downstream tasks. |
| `TestExtractPhaseSubset` | `test_missing_tasklist_file_returns_empty` | Mirrors `test_missing_phase_file_returns_empty` (`test_checkpoints.py:89-90`). |
| `TestDependencyWalker` | `test_linear_chain_returns_full_chain` | T1→T2→T3 walker correctness. |
| `TestDependencyWalker` | `test_cycle_does_not_loop_infinitely` | Defensive cycle break. |
| `TestDependencyWalker` | `test_diamond_dep_resolved_once` | Convergent deps deduplicated. |
| `TestTransitiveClosure` | `test_closure_includes_all_descendants` | |
| `TestTransitiveClosure` | `test_closure_excludes_completed_tasks` | PASS-status tasks pruned. |
| `TestTranscriptFallback` | `test_discover_failed_tasks_via_is_error` | `is_error: true` in jsonl → task flagged. |
| `TestTranscriptFallback` | `test_discover_failed_tasks_via_output_tokens_heuristic` | `output_tokens == 0` → flagged. |
| `TestTranscriptFallback` | `test_transcript_directory_missing_returns_empty` | |
| `TestRunOrchestration` | `test_orchestrate_writes_failed_suffix_to_originals` | Rename to `*.failed-<ts>` validated via glob. |
| `TestRunOrchestration` | `test_orchestrate_emits_phase_rerun_complete_event` | JSONL parse mirrors `_read_events` (`test_checkpoints.py:179-183`). |
| `TestRunOrchestration` | `test_orchestrate_skips_verify_checkpoints_when_flag_set` | `--no-verify-checkpoints` |
| `TestRunOrchestration` | `test_orchestrate_calls_verify_checkpoints_with_recover_by_default` | |

### 7.3 `tests/sprint/test_models.py` (EDIT)

| Test class (new) | Test function | Notes |
|---|---|---|
| `TestFailRecoverableStatus` | `test_fail_recoverable_value_and_properties` | Mirrors `TestPassMissingCheckpointStatus` (`test_checkpoints.py:266-271`); `value == "fail_recoverable"`, `is_failure is True`, `is_terminal is False`. |
| `TestFailRecoverableStatus` | `test_fail_recoverable_in_taskstatus_enum_iteration` | Ensures inclusion in `list(TaskStatus)`. |
| `TestPhaseResultExtensions` | `test_task_results_field_default_empty_list` | New field `task_results: list[TaskResult] = field(default_factory=list)`. |
| `TestPhaseResultExtensions` | `test_recovery_history_field_default_empty_list` | |
| `TestPhaseResultExtensions` | `test_json_serialization_round_trip_with_task_results` | `json.dumps(asdict(...))` then `from_dict()` re-parse equality. |
| `TestPhaseResultExtensions` | `test_json_serialization_with_recovery_history_entries` | |

### 7.4 `tests/sprint/test_executor.py` (EDIT)

| Test class (new) | Test function | Notes |
|---|---|---|
| `TestPhaseResultJsonWrite` | `test_phase_result_json_written_at_phase_end` | After `execute_phase_tasks(...)`, `<release_dir>/phase-N-result.json` exists. |
| `TestPhaseResultJsonWrite` | `test_phase_result_json_includes_task_results_and_status` | |
| `TestFailClassificationHeuristic` | `test_transient_proxy_error_classified_fail_recoverable` | Mock task output containing `"proxy error"` → status FAIL_RECOVERABLE. |
| `TestFailClassificationHeuristic` | `test_api_retry_exhaustion_classified_fail_recoverable` | |
| `TestFailClassificationHeuristic` | `test_assertion_error_classified_plain_fail` | Non-transient errors remain FAIL. |
| `TestFailClassificationHeuristic` | `test_user_abort_classified_error_not_recoverable` | |

### 7.5 `tests/sprint/test_checkpoints.py` (EDIT)

| Test class (new) | Test function | Notes |
|---|---|---|
| `TestRecoverMissingReturnsRecoveryBundle` | `test_recover_missing_checkpoints_returns_bundle_type` | Forward-compat wrapper returns `RecoveryBundle`, not raw list. |
| `TestRecoverMissingReturnsRecoveryBundle` | `test_bundle_status_complete_when_all_recovered` | |
| `TestRecoverMissingReturnsRecoveryBundle` | `test_bundle_status_partial_when_some_skipped` | |
| `TestRecoverMissingReturnsRecoveryBundle` | `test_legacy_list_protocol_still_iterable_for_v4_3_callers` | Backward-compat: bundle remains iterable like the v4.2.x list. |

### 7.6 `tests/sprint/test_cli_contract.py` (EDIT)

| Test class (new) | Test function | Notes |
|---|---|---|
| `TestRerunTasksContract` | `test_rerun_tasks_subcommand_registered` | `sprint --help` lists `rerun-tasks` (mirrors `test_sprint_group_help`, `test_cli_contract.py:20-29`). |
| `TestRerunTasksContract` | `test_rerun_tasks_help_lists_all_flags` | Asserts `--phase`, `--tasks`, `--merge-back`, `--no-merge-back`, `--dry-run`, `--include-transitive`, `--ignore-deps`, `--force-merge`, `--allow-loop`, `--no-verify-checkpoints`, `--bundle-dir`, `--restore`, `--from-reflect-report` all present in `result.output`. Mirrors `test_run_help` (`test_cli_contract.py:31-43`). |
| `TestRerunTasksContract` | `test_rerun_tasks_help_documents_default_merge_back_on` | |
| `TestRerunTasksContract` | `test_phase_tasks_mutually_exclusive_with_from_reflect_report` | Invoke with both → exit non-zero; output mentions mutually-exclusive. |
| `TestRerunTasksContract` | `test_phase_required_when_no_from_reflect_report` | Missing `--phase` → click usage error. |
| `TestRerunTasksContract` | `test_tasks_required_when_no_from_reflect_report` | Missing `--tasks` → click usage error. |
| `TestRerunTasksContract` | `test_exits_cleanly_on_help` | `--help` returns exit 0 (mirrors `test_all_subcommands_exit_cleanly`, `test_cli_contract.py:82-86`). |

### 7.7 `tests/sprint/test_backward_compat_regression.py` (EDIT)

| Test class (new) | Test function | Notes |
|---|---|---|
| `TestRerunTasksNoRegressionWhenUnused` | `test_sprint_without_rerun_invocation_emits_no_new_event_types` | Baseline + post-feature event-type sets equal. |
| `TestRerunTasksNoRegressionWhenUnused` | `test_sprint_without_rerun_invocation_adds_zero_threads` | `threading.active_count()` snapshot before/after (mirrors regression doc lines `test_backward_compat_regression.py:21,46`). |
| `TestRerunTasksNoRegressionWhenUnused` | `test_phase_result_json_write_does_not_break_existing_e2e_paths` | Re-run `test_e2e_success.TestE2ESuccess::test_all_phases_pass` semantics inline against post-feature executor. |

---

## 8. Cross-cutting concerns (lock file, SHA256, FAIL_RECOVERABLE)

### 8.1 Lock file behavior — covered in `TestRerunTasksLocking` (AC4 §6)
- Additional unit: `tests/sprint/test_rerun_tasks.py::TestLockFile`
  - `test_lock_acquire_creates_file_with_pid` — file body == `str(os.getpid())`.
  - `test_lock_release_removes_file` — finally-clause cleanup.
  - `test_lock_stale_lock_with_dead_pid_is_reclaimed` — PID check via `os.kill(pid, 0)` raising `ProcessLookupError`.
  - `test_lock_file_path_namespaces_by_phase` — `.rerun-phase-7.lock` vs `.rerun-phase-8.lock` independent.

### 8.2 SHA256 mismatch — covered in `TestRerunTasksSHACheck` (AC5 §6)
- Additional unit: `tests/sprint/test_rerun_tasks.py::TestSourceTasklistShaCheck`
  - `test_compute_sha256_of_tasklist_deterministic` — same content → same hash.
  - `test_recorded_sha_matches_returns_true` — happy path.
  - `test_recorded_sha_mismatch_returns_false` — mutated file detected.
  - `test_no_recorded_sha_returns_neutral_pass` — first-run case.

### 8.3 FAIL_RECOVERABLE classification — covered in `TestFailClassificationHeuristic` (§7.4)
- Plus enum-level unit: `tests/sprint/test_models.py::TestFailRecoverableStatus` (§7.3).
- Plus integration: `tests/sprint/test_rerun_tasks.py::TestNominateFailRecoverableTasksByDefault`
  - `test_default_nomination_picks_only_fail_recoverable_within_phase` — without `--tasks`, defaults per TDD line 256.

---

## 9. Test count summary

| File | New tests | Edited tests |
|---|---|---|
| `tests/sprint/test_recovery.py` (NEW) | 12 | — |
| `tests/sprint/test_rerun_tasks.py` (NEW) | 22 | — |
| `tests/sprint/test_rerun_tasks_e2e.py` (NEW) | 3 (AC1, AC2, AC3) | — |
| `tests/sprint/test_rerun_tasks_failure_modes.py` (NEW) | 10 (AC4x1, AC5x2, AC6x2, AC7x3, AC8x2) | — |
| `tests/sprint/test_cli_contract.py` (EDIT) | — | 7 |
| `tests/sprint/test_models.py` (EDIT) | — | 6 |
| `tests/sprint/test_executor.py` (EDIT) | — | 6 |
| `tests/sprint/test_checkpoints.py` (EDIT) | — | 4 |
| `tests/sprint/test_backward_compat_regression.py` (EDIT) | — | 3 |
| **Total** | **47** | **26** = **73 tests** |

TDD §Implementation cost line 215 budgets "~25 unit tests + 2 integration tests = ~500 LOC". This plan is more thorough (73 tests); recommend either:
1. Trim §7.1/§7.2 to highest-value paths to stay near budget, OR
2. Revise TDD test count estimate upward to ~70 tests / ~1000 LOC.

---

## 10. Key file:line references

- Mirror template: `tests/sprint/test_checkpoints.py:42-148` (extract → verify → integrate progression).
- Gate-mode loop pattern: `tests/sprint/test_checkpoints.py:277-280`.
- `_read_events` JSONL helper: `tests/sprint/test_checkpoints.py:179-183`.
- CLI flag-presence assertion: `tests/sprint/test_cli_contract.py:31-43`.
- Stacked patch + Popen factory: `tests/sprint/test_e2e_success.py:96-108`.
- SystemExit assertion for failure paths: `tests/sprint/test_e2e_halt.py:114-116`.
- Thread-count regression snapshot: `tests/sprint/test_backward_compat_regression.py:21,46`.
- `@pytest.mark.integration` exemplar: `tests/sprint/test_execute_sprint_integration.py:89`.
- Repo-root autouse fixtures: `tests/conftest.py:28-117`.
- TDD AC1-AC8 source: `/config/workspace/IronClaude/.dev/releases/backlog/SprintGranularResume/merged-requirements.md:263-270`.
- TDD CLI shape: `/config/workspace/IronClaude/.dev/releases/backlog/SprintGranularResume/merged-requirements.md:184`.
- TDD module-by-module LOC budget: `/config/workspace/IronClaude/.dev/releases/backlog/SprintGranularResume/merged-requirements.md:209-217`.

---

**End of research 04.**
