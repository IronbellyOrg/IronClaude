# Research: File Inventory
**Topic type:** File Inventory
**Scope:** src/superclaude/cli/sprint/*.py (19 files) + 2 new files (recovery.py, rerun_tasks.py)
**Status:** Complete
**Date:** 2026-06-01
---

## Section A: LOC Snapshot (existing files)

| File | LOC |
|------|-----|
| __init__.py | 5 |
| classifiers.py | 45 |
| notify.py | 62 |
| debug_logger.py | 138 |
| kpi.py | 218 |
| logging_.py | 235 |
| preflight.py | 245 |
| diagnostics.py | 291 |
| tmux.py | 323 |
| retrospective.py | 366 |
| process.py | 385 |
| checkpoints.py | 408 |
| commands.py | 463 |
| config.py | 509 |
| monitor.py | 571 |
| tui.py | 629 |
| summarizer.py | 644 |
| models.py | 883 |
| executor.py | 2148 |
| **TOTAL existing** | **8568** |

---

## Section B: Per-file inventory (existing 19 .py files)

### B.1 `__init__.py` (5 LOC)
- **Path:** `src/superclaude/cli/sprint/__init__.py`
- **Purpose:** Package entry — re-exports the Click `sprint_group`.
- **Exports:** `sprint_group` (from `.commands`)
- **Cross-file imports:** `from .commands import sprint_group`
- **rerun-tasks relevance:** none (no edit required)

### B.2 `classifiers.py` (45 LOC)
- **Path:** `src/superclaude/cli/sprint/classifiers.py`
- **Purpose:** Registry of subprocess-output classifiers used by preflight executor.
- **Exports:**
  - `CLASSIFIERS: dict[str, Callable[[int,str,str],str]]` (line 16)
  - `empirical_gate_v1(exit_code, stdout, stderr) -> str` (line 19)
  - `run_classifier(name, exit_code, stdout, stderr) -> str` (line 30)
- **Cross-file imports:** none (stdlib only)
- **rerun-tasks relevance:** none directly; but the TDD T6 "Classification heuristic" lives in `executor.py`, not here.

### B.3 `notify.py` (62 LOC)
- **Path:** `src/superclaude/cli/sprint/notify.py`
- **Purpose:** Best-effort cross-platform desktop notifications on phase / sprint completion.
- **Exports:**
  - `notify_phase_complete(result: PhaseResult)` (line 34)
  - `notify_sprint_complete(result: SprintResult)` (line 50)
  - private `_notify(title, message, urgent)` (line 12)
- **Cross-file imports:** `from .models import PhaseResult, SprintResult`
- **rerun-tasks relevance:** consider firing a `notify_rerun_complete` on merge-back success (optional polish; not in TDD).

### B.4 `debug_logger.py` (138 LOC)
- **Path:** `src/superclaude/cli/sprint/debug_logger.py`
- **Purpose:** Crash-safe flush-on-write structured debug logger; NullHandler when `config.debug=False`.
- **Exports:**
  - `DEBUG_LOG_VERSION = "1.0"`, `LOGGER_NAME = "superclaude.sprint.debug"`
  - `class _FlushHandler(logging.FileHandler)` (line 29)
  - `class _DebugFormatter(logging.Formatter)` (line 46)
  - `setup_debug_logger(config: SprintConfig) -> logging.Logger` (line 69)
  - `debug_log(logger, event, **kwargs) -> None` (line 117)
- **Cross-file imports (TYPE_CHECKING):** `from .models import SprintConfig`
- **rerun-tasks relevance:** `rerun_tasks.py` should use `debug_log()` for trace events (extraction, dep-walk, merge-back).

### B.5 `kpi.py` (218 LOC)
- **Path:** `src/superclaude/cli/sprint/kpi.py`
- **Purpose:** Gate KPI aggregation/reporting for trailing gates.
- **Exports:**
  - `@dataclass class GateKPIReport` (line 27)
  - `build_kpi_report(...)` (line 151)
- **rerun-tasks relevance:** none required by TDD.

### B.6 `logging_.py` (235 LOC)
- **Path:** `src/superclaude/cli/sprint/logging_.py`
- **Purpose:** Human-readable execution log writer + reader (`execution-log.jsonl` + readable tail).
- **Exports:**
  - `class SprintLogger` (line 13)
  - `read_status_from_log()` (line 224)
  - `tail_log(lines=50, follow=False)` (line 231)
- **rerun-tasks relevance:** TDD T5 step 5 specifies appending three new event types to `execution-log.jsonl`:
  - `phase_rerun_start`
  - `task_rerun_complete` (one per task)
  - `phase_rerun_complete`
  Plus mutate the original `phase_complete` event to add `superseded_by: <bundle-path>`. The append-events work belongs in `recovery.py` (engine) or `rerun_tasks.py` (orchestration) calling into `SprintLogger`.

### B.7 `preflight.py` (245 LOC)
- **Path:** `src/superclaude/cli/sprint/preflight.py`
- **Purpose:** Python/skip-mode phase execution path (non-Claude phases).
- **Exports:**
  - `execute_preflight_phases(config: SprintConfig) -> list[PhaseResult]` (line 90)
  - private helpers `_truncate`, `_write_evidence`, `_inject_source_field`
- **rerun-tasks relevance:** none — rerun-tasks targets the Claude execution path.

### B.8 `diagnostics.py` (291 LOC)
- **Path:** `src/superclaude/cli/sprint/diagnostics.py`
- **Purpose:** Failure diagnostic collection, classification, and report generation.
- **Exports:**
  - `class FailureCategory(Enum)` (line 19) — stall, timeout, crash, error, unknown
  - `@dataclass class DiagnosticBundle` (line 31)
  - `class DiagnosticCollector` (line 72)
  - `class FailureClassifier` (line 157)
  - `class ReportGenerator` (line 235)
- **rerun-tasks relevance:** T6 classification heuristic in TDD ("api_retry / ConnectionRefused / output_tokens==0") could optionally piggyback on `FailureClassifier`; TDD places the heuristic in `executor.py` post-task.

### B.9 `tmux.py` (323 LOC)
- **Path:** `src/superclaude/cli/sprint/tmux.py`
- **Purpose:** tmux session lifecycle (launch, attach, kill, pane updates).
- **Exports:** `is_tmux_available`, `session_name`, `find_running_session`, `launch_in_tmux`, `_build_foreground_command`, `update_tail_pane`, `update_summary_pane`, `attach_to_sprint`, `kill_sprint`
- **rerun-tasks relevance:** rerun-tasks is a short-lived foreground command; tmux launch likely skipped. No edit anticipated.

### B.10 `retrospective.py` (366 LOC)
- **Path:** `src/superclaude/cli/sprint/retrospective.py`
- **Purpose:** Release-level retrospective aggregation from phase summaries.
- **Exports:**
  - `@dataclass class ReleaseRetrospective` (line 45)
  - `class RetrospectiveGenerator` (line 310)
  - Aggregator helpers `_aggregate_phase_outcomes`, `_aggregate_files`, `_aggregate_validation_matrix`, `_aggregate_errors`, `_assess_validation_coverage`
- **rerun-tasks relevance:** none required by TDD (retro can later read `recovery_history` for narrative context).

### B.11 `process.py` (385 LOC)
- **Path:** `src/superclaude/cli/sprint/process.py`
- **Purpose:** Claude subprocess wrapper, signal handler, context builder.
- **Exports:**
  - `class ClaudeProcess(_PipelineClaudeProcess)` (line 88)
  - `class SignalHandler` (line 219)
  - `build_task_context(...)` (line 257)
  - `get_git_diff_context(start_commit) -> str` (line 322)
  - `compress_context_summary(...)` (line 347)
  - private spawn/signal/exit hook factories
- **rerun-tasks relevance:** the rerun executor invocation reuses `ClaudeProcess` indirectly via `execute_sprint(config_for_sub_index)`. No source changes required.

### B.12 `checkpoints.py` (408 LOC)
- **Path:** `src/superclaude/cli/sprint/checkpoints.py`
- **Purpose:** Canonical checkpoint-path parsing, manifest building, and auto-recovery from artifacts.
- **Exports:**
  - Regex constants `CHECKPOINT_PATH_PATTERN` (line 22) and `CHECKPOINT_HEADING_PATTERN` (line 30) — **the canonical mirror pattern that TDD T1 cites**
  - `extract_checkpoint_paths(phase_file, release_dir) -> list[tuple[str,Path]]` (line 36)
  - `verify_checkpoint_files(paths) -> list[tuple[str,Path,bool]]` (line 97) — **used by TDD T3 cross-phase dep check**
  - `_nearest_heading(headings, offset) -> str` (line 115)
  - `build_manifest(...)` (line 134)
  - `write_manifest(entries, output_path) -> None` (line 169)
  - `recover_missing_checkpoints(manifest, artifacts_dir, phase_tasklists) -> list[CheckpointEntry]` (line 209)
  - `_extract_verification_block(tasklist_path, checkpoint_name) -> str` (line 293)
  - `_discover_phase_artifacts(artifacts_dir, phase_number) -> list[Path]` (line 334)
  - `_render_recovered_checkpoint(...)` (line 367)
- **Cross-file imports:** `from .models import CheckpointEntry`
- **rerun-tasks relevance (HIGH):** TDD line 214 specifies `~30 LOC edit` here — wrap `recover_missing_checkpoints()` to optionally return a `RecoveryBundle` (forward-compat for v4.4.0 unified recovery). T9 specifies post-merge auto-invocation `verify-checkpoints --recover --phase N --quiet`.

### B.13 `commands.py` (463 LOC)
- **Path:** `src/superclaude/cli/sprint/commands.py`
- **Purpose:** Click command-group definition for `superclaude sprint <verb>`.
- **Exports:**
  - `@click.group("sprint") def sprint_group()` (line 16)
  - `_check_fidelity(index_path) -> tuple[bool,str]` (line 35)
  - `run(...)` (line 189) — the existing 18-option sprint runner
  - `attach()` (line 294)
  - `status()` (line 306)
  - `logs(lines, follow)` (line 331)
  - `kill(force)` (line 348)
  - `verify_checkpoints(output_dir, recover, as_json)` (line 376) — registered as `@sprint_group.command("verify-checkpoints")`
  - `_print_checkpoint_table(manifest, manifest_path)` (line 418)
  - `_print_dry_run(config)` (line 452)
- **Cross-file imports:** `from .config import load_sprint_config`, `from .executor import execute_sprint`, `from .tmux import is_tmux_available, launch_in_tmux` (lazy inside `run()`).
- **rerun-tasks relevance (HIGH):** TDD line 211 — **NEW `@sprint_group.command("rerun-tasks")` Click block, ~90 LOC**. Click options per TDD CLI shape:
  - argument: `INDEX_PATH` (Path, exists=True)
  - `--phase` (int, mutex group A)
  - `--tasks` (comma-list, mutex group A, requires `--phase`)
  - `--from-reflect-report` (Path, mutex group B)
  - `--merge-back / --no-merge-back` (default ON)
  - `--dry-run` (flag)
  - `--include-transitive` (flag)
  - `--ignore-deps` (flag)
  - `--force-merge` (flag)
  - `--allow-loop` (flag)
  - `--no-verify-checkpoints` (flag)
  - `--bundle-dir` (Path)
  - `--restore` (flag)
  - Mutually-exclusive enforcement via Click callback or pre-checks.

### B.14 `config.py` (509 LOC)
- **Path:** `src/superclaude/cli/sprint/config.py`
- **Purpose:** Sprint configuration loader + tasklist parsing.
- **Exports:**
  - `count_tasks_in_file(phase_file) -> int` (line 37)
  - `discover_phases(index_path) -> list[Phase]` (line 52)
  - `_extract_phase_name(phase_file) -> str` (line 143)
  - `_extract_phase_prompt_preview(phase_file, phase_name) -> str` (line 167)
  - `validate_phases(...)` (line 207)
  - `_resolve_release_dir(index_path) -> Path` (line 236)
  - `load_sprint_config(...)` (line 275)
  - `parse_tasklist(content, execution_mode="claude") -> list[TaskEntry]` (line 399) — **TDD T1 round-trip parser**
  - `parse_tasklist_file(path, execution_mode="claude") -> list[TaskEntry]` (line 495)
- **rerun-tasks relevance (HIGH):** `parse_tasklist()` is the parser used for the round-trip validation in TDD T1; `rerun_tasks.extract_phase_subset()` MUST invoke it before/after slicing.

### B.15 `monitor.py` (571 LOC)
- **Path:** `src/superclaude/cli/sprint/monitor.py`
- **Purpose:** Sidecar monitor thread: NDJSON parsing, turn counting, stall detection.
- **Exports:**
  - `detect_error_max_turns(output_path) -> bool` (line 37)
  - `detect_prompt_too_long(...) -> bool` (line 64)
  - `count_turns_from_output(output_path) -> int` (line 223)
  - `class OutputMonitor` (line 253)
  - private flatten/shorten/condense helpers
- **rerun-tasks relevance:** no direct edit; rerun execution reuses monitor.

### B.16 `tui.py` (629 LOC)
- **Path:** `src/superclaude/cli/sprint/tui.py`
- **Purpose:** Rich-based live TUI dashboard.
- **Exports:**
  - `class SprintTUI` (line 75)
  - Format helpers `_format_tokens`, `_format_bytes`, `_render_bar`, `_render_percent`, `_format_timestamp`, `_truncate`
- **rerun-tasks relevance:** none required by TDD v1.

### B.17 `summarizer.py` (644 LOC)
- **Path:** `src/superclaude/cli/sprint/summarizer.py`
- **Purpose:** Per-phase signal extraction + Sonnet-narrative summarization.
- **Exports:**
  - `@dataclass class PhaseSummary` (line 81)
  - `extract_phase_signals(output_path) -> dict` (line 165)
  - `invoke_sonnet(prompt, *, timeout)` (line 305)
  - `class PhaseSummarizer` (line 485)
  - `class SummaryWorker` (line 557)
  - Stream parsing / classification helpers
- **rerun-tasks relevance:** TDD T6 transcript-fallback path can reuse `extract_phase_signals()` to discover task `is_error` / `output_tokens` from per-task transcripts (`phase-N-task-T<PP>.<TT>-output.txt`).

### B.18 `models.py` (883 LOC)
- **Path:** `src/superclaude/cli/sprint/models.py`
- **Purpose:** All dataclasses + enums for sprint domain.
- **Exports (key):**
  - `@dataclass class TaskEntry` (line 25)
  - `class TaskStatus(Enum)` (line 39) — currently `PASS / FAIL / INCOMPLETE / SKIPPED`
  - `class GateOutcome(Enum)` (line 56), `class GateDisplayState(Enum)` (line 69)
  - `GATE_DISPLAY_TRANSITIONS` (line 106)
  - `is_valid_gate_transition(from_state, to_state) -> bool` (line 120)
  - `@dataclass class TaskResult` (line 159) — status, turns_consumed, exit_code, started_at, finished_at, output_bytes, gate_outcome, reimbursement_amount, output_path
  - `class PhaseStatus(Enum)` (line 211) — 11 members incl. PASS_RECOVERED, PREFLIGHT_PASS
  - `class SprintOutcome(Enum)` (line 272)
  - `@dataclass class Phase` (line 282) — number, file, name, execution_mode
  - `@dataclass class CheckpointEntry` (line 312)
  - `@dataclass class SprintConfig(PipelineConfig)` (line 348) — incl. `result_file(phase)` returning `<results_dir>/phase-N-result.md` (line 509)
  - `@dataclass class SprintStep(Step)` (line 513)
  - `@dataclass class PhaseResult(StepResult)` (line 523) — phase, status, exit_code, started_at, finished_at, output_bytes, error_bytes, last_task_id, files_changed, turns, tokens_in, tokens_out
  - `@dataclass class SprintResult` (line 559)
  - `@dataclass class MonitorState` (line 623)
  - `@dataclass class TurnLedger` (line 693)
  - `build_resume_output(...)` (line 779)
  - `@dataclass class ShadowGateMetrics` (line 837)
- **rerun-tasks relevance (HIGH):** TDD line 212 — `~70 LOC delta`. Specifically:
  - **T6**: Add `task_results: list[TaskResult] = field(default_factory=list)` to `PhaseResult` (line ~523)
  - **T6**: Add `recovery_history: list[RecoveryBundleRef] = field(default_factory=list)` to `PhaseResult`
  - **T6**: `TaskStatus` enum (line 39): rename `FAIL` -> `FAIL_TERMINAL` keeping serialized value `"fail"` for back-compat; add `FAIL_RECOVERABLE = "fail_recoverable"`. Update `is_failure` property accordingly.
  - **T5/T6**: Add `RecoveryStatus` enum (SUCCESS / PARTIAL / FAILED / DRYRUN) — could land here or in `recovery.py`; TDD line 209 places `RecoveryBundle` + `RecoveryStatus` in `recovery.py`.
  - **T6**: Add `RecoveryBundleRef` dataclass for the `recovery_history` field.
  - **JSON serialization**: TDD line 212 requires JSON ser/de for PhaseResult.task_results + recovery_history (current `phase-N-result.md` is markdown; new `phase-N-result.json` is a SIBLING file written at phase end).

### B.19 `executor.py` (2148 LOC)
- **Path:** `src/superclaude/cli/sprint/executor.py`
- **Purpose:** Phase execution engine — subprocess launch, monitor wiring, gate enforcement, result determination, sprint orchestration.
- **Exports (key):**
  - `class SprintGatePolicy` (line 56)
  - `class IsolationLayers` (line 107), `setup_isolation(config) -> IsolationLayers` (line 150)
  - `class AggregatedPhaseReport` (line 191) — already has `task_results: list[TaskResult]` field (line 209)
  - `aggregate_task_results(...)` (line 296)
  - `check_budget_guard(ledger) -> str | None` (line 338)
  - `run_wiring_safeguard_checks(...)` (line 354), `_resolve_wiring_mode(config) -> str` (line 427)
  - `run_post_task_wiring_hook(...)` (line 458), `run_post_phase_wiring_hook(...)` (line 748)
  - `_log_shadow_findings_to_remediation_log(...)` (line 632)
  - `_format_wiring_failure(...)` (line 666), `_recheck_wiring(...)` (line 717)
  - `run_post_task_anti_instinct_hook(...)` (line 803)
  - `execute_phase_tasks(...)` (line 927) — **returns `task_results, remaining, phase_gate_results`**
  - `_run_task_subprocess(...)` (line 1076)
  - `_parse_phase_tasks(phase, config) -> list[TaskEntry] | None` (line 1118)
  - `execute_sprint(config: SprintConfig)` (line 1135) — the main loop
  - `_write_exit_sentinel(config, exitcode) -> None` (line 1759)
  - `_classify_from_result_file(...)` (line 1774)
  - `_verify_checkpoints(...)` (line 1811)
  - `_check_checkpoint_pass(config, phase) -> bool` (line 1894)
  - `_check_contamination(config, phase) -> list[str]` (line 1908)
  - `_write_crash_recovery_log(...)` (line 1927)
  - `_write_preliminary_result(...)` (line 1954)
  - `_write_executor_result_file(...)` (line 2020) — writes `config.result_file(phase)` (`.md`)
  - `_determine_phase_status(...)` (line 2067)
- **Cross-file imports (line 19-41):** `.debug_logger`, `.diagnostics`, `.logging_`, `.models`, `.monitor`, `.notify`, `.process`, `.tmux`, `.tui`; plus pipeline-level `superclaude.cli.pipeline.{models, trailing_gate}`.
- **rerun-tasks relevance (HIGH):** TDD line 213 — `~40 LOC delta`:
  - **T6**: At phase end (after `_write_executor_result_file()` or alongside), write a NEW `<results_dir>/phase-N-result.json` containing serialized `PhaseResult` with `task_results` populated. Existing `task_results` already flow through `execute_phase_tasks()` return tuple (line 1267 in `execute_sprint`).
  - **T6 Classification heuristic**: post-task classification logic for `FAIL_RECOVERABLE` vs `FAIL_TERMINAL`:
    - `is_error: false` + `output_tokens > 0` -> PASS
    - `is_error: true` + (`api_retry` OR `ConnectionRefused` OR `output_tokens == 0`) -> FAIL_RECOVERABLE
    - `is_error: true` + none of the above -> FAIL_TERMINAL
    - process killed / truncated transcript -> INCOMPLETE
  - Likely site for heuristic: inside or right after `_run_task_subprocess()` (line 1076), feeding into `TaskResult.status`.

---

## Section C: New files (per TDD)

### C.1 `recovery.py` (NEW, ~250 LOC per TDD line 209)
- **Path:** `src/superclaude/cli/sprint/recovery.py`
- **Purpose:** Recovery-bundle abstraction + generic merge engine; pre-positioned for v4.4.0 `sprint repair` umbrella.
- **Required exports (from TDD sections T5, T7, T8, T9):**

  **Dataclasses / enums:**
  - `class RecoveryStatus(Enum)`: `SUCCESS | PARTIAL | FAILED | DRYRUN` (TDD line 82-84)
  - `@dataclass class RecoveryBundle` (TDD lines 71-84):
    - `bundle_id: str` (rerun-<isots>)
    - `verb: str` ("rerun-tasks")
    - `affected_phase: int`
    - `affected_tasks: list[str]`
    - `artifacts_produced: list[Path]`
    - `artifacts_replaced: dict[Path, Path]` (canonical -> preserved with .failed-<ts>)
    - `source_tasklist_sha256: str`
    - `end_tasklist_sha256: str | None`
    - `status: RecoveryStatus`
    - `rerun_attempt: int` (1..3, cap at 3)
  - `@dataclass class RecoveryBundleRef` (referenced by `PhaseResult.recovery_history` — short serialized reference: bundle_id + path + status + ts).

  **Protocols:**
  - `class Nominator(Protocol)` (TDD T7 line 147): `def nominate(self, context) -> list[TaskID]`. Future-compatible with `RfQaNominator`, `CiFailureNominator`.
  - `class ManualNominator(Nominator)` — wraps `--phase + --tasks`.
  - `class ReflectReportNominator(Nominator)` — reads YAML/JSON, filters `classification: regression|drift`.

  **Functions:**
  - `merge_recovery_bundle(bundle: RecoveryBundle, source_index: Path) -> None` (TDD T5 lines 86-99) performing the 7 merge steps:
    1. Rename transcripts -> `.failed-<orig-ts>.txt` + copy bundle's rerun transcripts to canonical paths
    2. Same for checkpoint reports
    3. Same for `-errors.txt`
    4. Write `results/phase-N-rerun-manifest.json`
    5. Append three new events to `execution-log.jsonl` (`phase_rerun_start`, `task_rerun_complete`, `phase_rerun_complete`)
    6. Mutate original `phase_complete` event to add `superseded_by: <bundle-path>` (append-only at event level + link record)
    7. Rewrite `phase-N-result.json` with updated `task_results` + append to `recovery_history`
  - `write_recovery_audit_log(bundle_dir: Path, event: dict) -> None` (TDD T4 line 66 — `<results_dir>/recovery-audit.log` shared with checkpoint mutations).
  - `compute_tasklist_sha256(path: Path) -> str` — SHA256 helper for INV-3.
  - Lock-file helpers: `acquire_recovery_lock(results_dir, phase: int) -> Path` (TDD T8.5 — `<results_dir>/.recovery-locks/phase-N.lock`, PID+timestamp, atexit + signal-handler auto-clear); `release_recovery_lock(lock_path: Path) -> None`.
  - `retry_count_for_task(phase_result: PhaseResult, task_id: str) -> int` — counts entries in `recovery_history` matching task_id; enforces TDD T8.2 retry cap of 3.

### C.2 `rerun_tasks.py` (NEW, ~280 LOC per TDD line 210)
- **Path:** `src/superclaude/cli/sprint/rerun_tasks.py`
- **Purpose:** Verb orchestration — extract subset, dep-walk, run, merge-back.
- **Required exports (from TDD T1, T2, T3, T4, T6, T8):**

  **Core functions:**
  - `extract_phase_subset(source_path: Path, target_task_ids: list[str], bundle_dir: Path) -> Path` (TDD T1 lines 21-28):
    1. Read `phase-N-tasklist.md` verbatim
    2. Apply regex `r'^### (T\d{2}\.\d{2})\b.*?(?=^### T\d{2}\.\d{2}|\Z)'` (MULTILINE|DOTALL)
    3. Preserve frontmatter, phase goal heading, dependencies section, narrative pre-first-task verbatim
    4. Slice target task blocks exactly (preserve original T-IDs, no renumbering)
    5. **Round-trip parse via `config.parse_tasklist()`**; abort if `parsed(slice) != parsed(original).filter(target_ids)` with message: `"Sub-tasklist extraction failed round-trip validation. Inspect <bundle>/phase-Nr-tasklist.md vs source."`
    6. Write to `<bundle_dir>/phase-Nr-tasklist.md` with frontmatter `rerun_of: phase-N`, `source_tasklist_sha256: <hex>`
  - `build_rerun_bundle_dir(results_dir: Path, override: Path | None) -> Path` (TDD T8.6 — auto-suffix `-1`..`-9` on collision; abort at `-9`).
  - `build_sub_index(bundle_dir: Path, sub_tasklist: Path) -> Path` (TDD T2 — writes `tasklist-index-Nr.md` enumerating only the rerun phase + sub-tasklist).
  - `walk_dependencies(phase_tasklist: Path, target_ids: list[str], *, include_transitive: bool, ignore_deps: bool) -> tuple[list[str], list[str]]` (TDD T3 lines 42-55) — returns `(resolved_target_ids, warnings)`:
    1. Read declared `depends_on` for each target
    2. In-rerun -> OK; `[x]` in source -> OK; `[ ]` in source -> WARN + ABORT (unless `--ignore-deps`)
    3. Cross-phase deps: call `checkpoints.verify_checkpoint_files()` for prerequisite phases
    4. `--include-transitive`: auto-include failed deps up to 50% cost ceiling; above -> ABORT
  - `discover_failed_tasks_from_transcripts(results_dir: Path, phase: int) -> list[tuple[str, TaskStatus]]` (TDD T6 line 130 legacy fallback) — when `phase-N-result.json` missing/empty: read each `results/phase-N-task-T<PP>.<TT>-output.txt`, parse final JSON line, apply classification heuristic.
  - `flip_target_checkboxes(phase_tasklist: Path, target_ids: list[str], bundle_dir: Path) -> dict` (TDD T4 lines 60-66) — `[x] -> [ ]`, prepend `rerun_in_progress:` frontmatter block; return restore-info for auto-restore.
  - `restore_checkboxes_on_abort(phase_tasklist: Path, restore_info: dict) -> None` (TDD T4 line 65) — auto-restore on pre-merge-back abort.
  - `finalize_checkboxes_on_success(phase_tasklist: Path, target_ids: list[str], bundle_dir: Path) -> None` (TDD T4 line 64) — flip back to `[x]`, move `rerun_in_progress` -> `rerun_history`.
  - `stash_and_restore_deliverables(target_ids: list[str], results_dir: Path, bundle_dir: Path) -> None` (TDD T8.4) — stash files at `<bundle>/preserved/<relative-path>`; `--restore` flag restores from most recent bundle.
  - `select_default_recoverable_tasks(phase_result_json: Path) -> list[str]` (TDD line 256 OQ#3) — when no explicit `--tasks`, pick all tasks where `status == FAIL_RECOVERABLE` within the named phase.

  **Orchestration entry-point (called from Click block in `commands.py`):**
  - `run_rerun_tasks(config, *, phase, tasks, from_reflect_report, merge_back, dry_run, include_transitive, ignore_deps, force_merge, allow_loop, no_verify_checkpoints, bundle_dir, restore) -> int`:
    1. Acquire lock (T8.5)
    2. Nominate task IDs via `Nominator` (manual or reflect-report)
    3. Print equivalent manual command if `from_reflect_report` (T7 line 145)
    4. Build bundle dir (T8.6) + capture `source_tasklist_sha256`
    5. `extract_phase_subset()` (T1) + `walk_dependencies()` (T3)
    6. If `dry_run`: print extraction plan, exit
    7. Retry-cap check (T8.2): abort if `retry_count_for_task() > 3` unless `--allow-loop`
    8. Stash deliverables (T8.4)
    9. `flip_target_checkboxes()` (T4)
    10. Build sub-index (T2); invoke `execute_sprint(sub_config)` via executor
    11. On rerun success + `--merge-back`: re-hash source (T8.1 SHA check, unless `--force-merge`); call `recovery.merge_recovery_bundle()` (T5); finalize checkboxes
    12. On rerun ABORT pre-merge: `restore_checkboxes_on_abort()`
    13. Auto-invoke `verify-checkpoints --recover --phase N --quiet` unless `--no-verify-checkpoints` (T9 line 170)
    14. Release lock
    15. Return exit code

---

## Section D: Secondary inventory — by-file x TDD-section matrix

This matrix lets the task-builder enumerate per-file checklist items granularly.

| TDD Section | Title | Primary file | Secondary file(s) | Specific symbols / state-machine elements |
|---|---|---|---|---|
| **T1** | Task extraction | `rerun_tasks.py` (NEW) | `config.py` (parser reuse) | `extract_phase_subset()`, regex `r'^### (T\d{2}\.\d{2})\b.*?(?=^### T\d{2}\.\d{2}|\Z)'`, round-trip via `parse_tasklist()`, frontmatter fields `rerun_of`, `source_tasklist_sha256` |
| **T2** | Index construction | `rerun_tasks.py` (NEW) | — | `build_rerun_bundle_dir()`, `build_sub_index()`, files `tasklist-index-Nr.md`, `phase-Nr-tasklist.md`, `recovery-bundle.json` |
| **T3** | Dependency handling | `rerun_tasks.py` (NEW) | `checkpoints.py` (`verify_checkpoint_files()`), `config.py` (depends_on parser) | `walk_dependencies()`, `--include-transitive` 50% cost ceiling, `--ignore-deps` |
| **T4** | Checkbox mutation | `rerun_tasks.py` (NEW) | `recovery.py` (audit log via `write_recovery_audit_log()`) | `flip_target_checkboxes()`, `restore_checkboxes_on_abort()`, `finalize_checkboxes_on_success()`, frontmatter blocks `rerun_in_progress:` / `rerun_history:`, audit at `<results_dir>/recovery-audit.log` |
| **T5** | Results merge-back | `recovery.py` (NEW) | `logging_.py` (event append), `models.py` (PhaseResult write) | `RecoveryBundle` dataclass, `RecoveryStatus` enum, `merge_recovery_bundle()` 7-step engine, new event types `phase_rerun_start` / `task_rerun_complete` / `phase_rerun_complete`, `superseded_by:` link on original `phase_complete` event, `phase-N-rerun-manifest.json` |
| **T6** | Per-task persistence | `models.py` (EDIT), `executor.py` (EDIT) | `rerun_tasks.py` (legacy fallback), `summarizer.py` (transcript parsing) | `PhaseResult.task_results: list[TaskResult]`, `PhaseResult.recovery_history: list[RecoveryBundleRef]`, `TaskStatus.FAIL_TERMINAL` (rename from `FAIL`, keep serialized `"fail"`), `TaskStatus.FAIL_RECOVERABLE = "fail_recoverable"`, classification heuristic in `executor._run_task_subprocess` / post-task, `phase-N-result.json` write at phase end (~20 LOC), `discover_failed_tasks_from_transcripts()` legacy fallback |
| **T7** | reflect integration | `recovery.py` (NEW) | `commands.py` (Click `--from-reflect-report`), `rerun_tasks.py` (resolution) | `class Nominator(Protocol)`, `class ManualNominator`, `class ReflectReportNominator`, `--nomination-source {manual|reflect-report}`, mutex flag enforcement |
| **T8** | Failure modes | `recovery.py` (NEW), `rerun_tasks.py` (NEW) | `models.py` (RecoveryBundle.rerun_attempt) | (1) SHA256 check via `compute_tasklist_sha256()` + `--force-merge`; (2) `retry_count_for_task()` cap-3 + `--allow-loop`; (3) `.failed-<ts>` rename in `merge_recovery_bundle`; (4) `stash_and_restore_deliverables()` + `--restore`; (5) `acquire_recovery_lock()` / `release_recovery_lock()` + atexit/signal handler; (6) bundle-dir collision auto-suffix `-1`..`-9`; (7) auto-restore on ABORT (see T4) |
| **T9** | verify-checkpoints composition | `commands.py` (EDIT — auto-invoke), `checkpoints.py` (EDIT — wrap to return RecoveryBundle) | `rerun_tasks.py` (post-merge call) | Auto-invoke `verify-checkpoints --recover --phase N --quiet` after merge-back; `--no-verify-checkpoints` opt-out; wrap `recover_missing_checkpoints()` to optionally produce a `RecoveryBundle` for v4.4.0 forward-compat |
| **CLI shape** | Click block | `commands.py` (EDIT) | — | New `@sprint_group.command("rerun-tasks")` Click block (~90 LOC), 12 options (see B.13), mutually-exclusive group via Click callback |
| **AC1-AC8** | Acceptance criteria | tests | all | See researcher-4 |

---

## Section E: LOC delta budget (from TDD line 207-217)

| File | Action | LOC delta | New file? |
|---|---|---|---|
| `recovery.py` | NEW | ~250 | yes |
| `rerun_tasks.py` | NEW | ~280 | yes |
| `commands.py` | EDIT | ~90 | no |
| `models.py` | EDIT | ~70 | no |
| `executor.py` | EDIT | ~40 | no |
| `checkpoints.py` | EDIT | ~30 | no |
| Tests | NEW | ~500 | yes (~25 unit + 2 integration) |
| **TOTAL** | | **~1260** | |

**Dependencies (per TDD line 219):** none new. Re-uses Click, dataclasses, json, hashlib (stdlib), and project MDTM parser (`config.parse_tasklist()`).

**`make sync-dev` impact:** zero — Python source, not skill/command/agent sync output (TDD line 221).

---

## Section F: Cross-file import map (existing edges relevant to rerun-tasks)

- `commands.py` -> `.config.load_sprint_config`, `.executor.execute_sprint`, `.tmux.launch_in_tmux` (lazy in `run()`); **NEW: -> `.rerun_tasks.run_rerun_tasks`**
- `executor.py` (line 19-41) -> `.debug_logger`, `.diagnostics`, `.logging_`, `.models`, `.monitor`, `.notify`, `.process`, `.tmux`, `.tui`; **NEW edge: writes `phase-N-result.json` via `models.PhaseResult.to_json()` or inline json.dumps**
- `checkpoints.py` -> `.models.CheckpointEntry`; **NEW edge: optionally returns `RecoveryBundle` from `recover_missing_checkpoints()`** (forward-compat)
- `notify.py` -> `.models.{PhaseResult, SprintResult}`
- `debug_logger.py` -> `.models.SprintConfig` (TYPE_CHECKING)
- **NEW `rerun_tasks.py`** -> `.config.parse_tasklist`, `.checkpoints.verify_checkpoint_files`, `.recovery.{RecoveryBundle, merge_recovery_bundle, acquire_recovery_lock, ...}`, `.executor.execute_sprint`, `.models.{SprintConfig, Phase, TaskStatus, TaskResult, PhaseResult}`, `.debug_logger.debug_log`, `.summarizer.extract_phase_signals` (legacy fallback)
- **NEW `recovery.py`** -> `.models.{PhaseResult, TaskResult, TaskStatus}`, `.logging_.SprintLogger` (event append), `.debug_logger.debug_log`

---

## Status: Complete

## Summary

- **19 existing .py files** inventoried with path, purpose, key exports + line numbers, LOC, and rerun-tasks relevance flag (HIGH on 5: `commands.py`, `models.py`, `executor.py`, `checkpoints.py`, `config.py`).
- **2 new files** specified from TDD T1/T2/T6/T9: `recovery.py` (~250 LOC, RecoveryBundle + merge engine + Nominator protocol + lock helpers + SHA helpers) and `rerun_tasks.py` (~280 LOC, extract + dep-walk + flip checkboxes + orchestration entry point).
- **5 EDIT targets** with LOC budget: `commands.py` +90 (new Click block), `models.py` +70 (FAIL_RECOVERABLE / task_results / recovery_history / JSON ser), `executor.py` +40 (phase-N-result.json + classification heuristic), `checkpoints.py` +30 (wrap to return RecoveryBundle).
- **Secondary by-file x TDD-section matrix** (Section D) maps every TDD section to its target file(s) and specific symbols/state-machine elements — directly usable by task-builder to enumerate per-file MDTM items.
- **Cross-file import map** (Section F) shows existing edges plus the NEW edges the two new files introduce.
- **Total delta:** ~760 source + ~500 tests = ~1260 LOC, zero new dependencies, zero `make sync-dev` impact.
