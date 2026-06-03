# Research: 03 - Sprint Execution Runtime
**Investigation type:** Code Tracer / Architecture Analyst
**Scope:** `src/superclaude/cli/sprint/` and generated sprint docs for comparison only
**Status:** Complete
**Date:** 2026-06-02
---

## Source Inventory

Initial file discovery found 19 Python source files in `/config/workspace/IronClaude/src/superclaude/cli/sprint/` (8,568 total lines). Runtime-heavy files are `executor.py` (2,148 lines), `models.py` (883), `tui.py` (629), `monitor.py` (571), `config.py` (509), `commands.py` (463), `checkpoints.py` (408), `process.py` (385), and `tmux.py` (323). Supporting files include `summarizer.py`, `retrospective.py`, `diagnostics.py`, `logging_.py`, `kpi.py`, `preflight.py`, `debug_logger.py`, `notify.py`, `classifiers.py`, and `__init__.py`.

Key discovery commands used: `find /config/workspace/IronClaude/src/superclaude/cli/sprint -maxdepth 3 -type f | sort`, `wc -l /config/workspace/IronClaude/src/superclaude/cli/sprint/*.py`, plus targeted grep for classes/functions and execution keywords.

**Key Takeaways:**
- Sprint runtime is concentrated in `commands.py` -> `config.py` -> `executor.py`, with process/session abstractions split into `process.py`, `monitor.py`, `tmux.py`, and presentation in `tui.py`.
- There is a dedicated state model layer in `models.py` for tasks, phase/sprint results, monitor state, TurnLedger, and shadow gate metrics.
- Generated sprint docs exist under `/config/workspace/IronClaude/docs/generated/sprint-cli/`; they are comparison-only and require code cross-validation before use.

## Section 2 Mapping — Sprint CLI Entry, Configuration, and Phase/Task Parsing

### CLI command surface

- `commands.py` defines the `sprint` Click group at `/config/workspace/IronClaude/src/superclaude/cli/sprint/commands.py:15-32`. The docstring advertises `run`, `attach`, `status`, `logs`, and `kill`; current code also defines `verify-checkpoints` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/commands.py:360-415`.
- `run(...)` is the active orchestration entry point at `/config/workspace/IronClaude/src/superclaude/cli/sprint/commands.py:189-207`. It imports `load_sprint_config`, `execute_sprint`, `is_tmux_available`, and `launch_in_tmux` lazily at `/config/workspace/IronClaude/src/superclaude/cli/sprint/commands.py:219-221`.
- `run(...)` supports phase slicing (`--start`, `--end`), Claude budget/model (`--max-turns`, `--model`), tmux vs foreground (`--no-tmux`, hidden `--tmux-session-name`), permission mode, debug logging, watchdog controls (`--stall-timeout`, `--startup-stall-timeout`, `--stall-action`), `--shadow-gates`, fidelity overrides, `--release-dir`, and `--state-dir`; see `/config/workspace/IronClaude/src/superclaude/cli/sprint/commands.py:71-188`.
- `run(...)` loads config at `/config/workspace/IronClaude/src/superclaude/cli/sprint/commands.py:229-243`, applies release-dir overrides at `/config/workspace/IronClaude/src/superclaude/cli/sprint/commands.py:249-268`, blocks on failed spec-fidelity unless forced at `/config/workspace/IronClaude/src/superclaude/cli/sprint/commands.py:270-280`, prints dry-run output at `/config/workspace/IronClaude/src/superclaude/cli/sprint/commands.py:282-284`, and dispatches to tmux or foreground execution at `/config/workspace/IronClaude/src/superclaude/cli/sprint/commands.py:286-290`.

### Phase discovery and config loading

- `config.py` imports `Phase`, `SprintConfig`, and `TaskEntry` from `.models` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/config.py:11`, making `models.py` the type backbone for parsing/config.
- `PHASE_FILE_PATTERN` accepts `phase-N-tasklist.md`, `pN-tasklist.md`, `phase_N_tasklist.md`, and `tasklist-pN.md` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/config.py:15-26`.
- `discover_phases(index_path)` parses the index markdown table for file names and optional `Execution Mode` values at `/config/workspace/IronClaude/src/superclaude/cli/sprint/config.py:52-140`. Allowed execution modes are `claude`, `python`, and `skip`; invalid values raise a Click exception at `/config/workspace/IronClaude/src/superclaude/cli/sprint/config.py:109-115`.
- `_resolve_release_dir(index_path)` treats an index inside `tasklist/`, `tasklists/`, or `tasks/` as part of a larger release directory only when the grandparent contains `.roadmap-state.json` or spec/requirements files; see `/config/workspace/IronClaude/src/superclaude/cli/sprint/config.py:236-272`.
- `load_sprint_config(...)` validates the index exists, discovers phases, enriches each `Phase` with a heading-derived name and prompt preview, auto-detects `end_phase`, validates gaps/missing files, pre-scans total active tasks, and builds `SprintConfig`; see `/config/workspace/IronClaude/src/superclaude/cli/sprint/config.py:275-367`.
- `count_tasks_in_file(phase_file)` counts only headings matching `### T<PP>.<TT>` via `_TASK_ID_HEADING_RE`; unreadable files return 0 instead of raising, which makes task-progress display best-effort (`/config/workspace/IronClaude/src/superclaude/cli/sprint/config.py:28-49`).

### Task parsing

- `parse_tasklist(content, execution_mode='claude')` scans phase markdown for `### T<PP>.<TT> -- Title` headings, dependencies, optional `**Command:**`, optional classifier table row, and deliverables-derived description at `/config/workspace/IronClaude/src/superclaude/cli/sprint/config.py:399-492`.
- The regexes driving task parsing are `_TASK_HEADING_RE`, `_DEPENDENCY_RE`, `_TASK_ID_REF_RE`, `_COMMAND_RE`, and `_CLASSIFIER_RE` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/config.py:374-396`.
- Python-mode phases are stricter: any parsed task without a `**Command:**` raises a Click exception at `/config/workspace/IronClaude/src/superclaude/cli/sprint/config.py:475-479`.
- `_parse_phase_tasks(phase, config)` in the executor reads the phase file and delegates to `parse_tasklist(...)`; it returns `None` for freeform phases without task headings, which sends them down the single phase-level subprocess path (`/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1118-1132`).

### Data models that matter for porting

- `TaskEntry` carries `task_id`, `title`, `description`, `dependencies`, `command`, and `classifier` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:24-37`.
- `TaskStatus`, `GateOutcome`, and `GateDisplayState` define task/gate lifecycle values and display labels at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:39-155`.
- `TaskResult` is runner-constructed, not agent-self-reported; fields include task status, turn count, exit code, timing, output bytes, gate outcome, reimbursement amount, and output path at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:158-209`.
- `PhaseStatus` marks `PASS`, `PASS_NO_SIGNAL`, `PASS_NO_REPORT`, `PASS_RECOVERED`, `PREFLIGHT_PASS`, `PASS_MISSING_CHECKPOINT`, `INCOMPLETE`, `HALT`, `TIMEOUT`, `ERROR`, and `SKIPPED`, with success/failure predicates at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:211-270`.
- `SprintConfig` extends `PipelineConfig` and owns paths, execution flags, gate modes, checkpoint mode, total task count, and transient `state_dir` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:347-510`.
- `SprintConfig.__post_init__` sets `work_dir = release_dir`, maps old wiring fields, derives `wiring_gate_mode`, and defaults `state_dir` to `.dev/sprint-state/<tasklist-id>` when not provided (`/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:415-471`).

**Port implications for Mastra + Backlog.md + Beads:**
- Reusable: markdown task parsing is deterministic and small enough to port or wrap directly; Backlog.md/Beads can model the parsed `TaskEntry` graph, but the current parser only stores dependencies and does not schedule by dependency order beyond preserving file order.
- Rebuild likely: Click-specific config loading and path override behavior would need an adapter around Mastra workflow inputs and whichever backlog/task graph store is chosen.
- Stress-test point: sprint's phase discovery depends on markdown filename conventions and optional execution-mode table columns, not an external issue database. A Beads port must decide whether Beads IDs replace `T<PP>.<TT>` IDs or map onto them.

**Key Takeaways:**
- The current runtime has two execution modes: phase-level Claude subprocesses for freeform phase files and task-level subprocesses for parsed `TaskEntry` inventories.
- `python` execution mode is a preflight subprocess path with explicit commands; `skip` records a skipped phase without Claude.
- The hardest parsing-port risk is not regex complexity; it is preserving sprint's implicit conventions: phase filenames, `Execution Mode` table, `T<PP>.<TT>` task IDs, checkpoint path declarations, and result-file sentinel semantics.

## Section 4 Mapping — Execution Runtime, Process Isolation, Tmux/TUI, Monitoring, and Stall Handling

### Main orchestration flow

- `execute_sprint(config)` is the core loop at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1135-1757`. It preflights the `claude` binary, installs signal handlers, creates logger/TUI/monitor objects, initializes `SprintResult`, starts a summary worker, constructs `TurnLedger`, `ShadowGateMetrics`, `DeferredRemediationLog`, and `SprintGatePolicy`, starts the TUI, cleans stale isolation dirs, executes python-mode preflight phases, then iterates active phases.
- Preflight python-mode phases are executed before the main Claude loop via `execute_preflight_phases(config)` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1228-1234`.
- In the main loop, python phases are skipped because preflight already handled them (`/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1241-1243`); skip-mode phases append a `PhaseResult(status=SKIPPED)` with no subprocess (`/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1245-1257`).
- Parsed task phases take Path A: `_parse_phase_tasks(...)` then `execute_phase_tasks(...)`, append task gate results, determine phase pass/error from task statuses, run post-phase wiring hook, log result, update TUI, and `continue` before the phase-level monitor block (`/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1259-1301`).
- Freeform phases take Path B: create an isolation directory, copy the phase file, start `OutputMonitor`, optionally retarget tmux tail pane, spawn `ClaudeProcess`, then poll the process while updating TUI and enforcing timeout/stall watchdogs (`/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1303-1457`).

### Process/session management

- Sprint's `ClaudeProcess` subclasses the generic pipeline process at `/config/workspace/IronClaude/src/superclaude/cli/sprint/process.py:88-121`; it builds a sprint prompt and delegates actual subprocess lifecycle to `superclaude.cli.pipeline.process.ClaudeProcess`.
- The base process builds `claude --print --verbose <permission-flag> --no-session-persistence --tools default --max-turns N --output-format <format>` at `/config/workspace/IronClaude/src/superclaude/cli/pipeline/process.py:73-95`.
- Prompt delivery is via stdin, not argv, to avoid Linux `MAX_ARG_STRLEN`; see `/config/workspace/IronClaude/src/superclaude/cli/pipeline/process.py:73-78` and `/config/workspace/IronClaude/src/superclaude/cli/pipeline/process.py:140-146`.
- The base process strips `CLAUDECODE` and `CLAUDE_CODE_ENTRYPOINT` and merges caller env vars at `/config/workspace/IronClaude/src/superclaude/cli/pipeline/process.py:97-112`.
- The base process uses `subprocess.Popen` with stdout/stderr redirected to files, optional `os.setpgrp` process groups, and no explicit `cwd` in `Popen`; see `/config/workspace/IronClaude/src/superclaude/cli/pipeline/process.py:114-157`.
- Termination is process-group aware: SIGTERM, wait 10 seconds, then SIGKILL at `/config/workspace/IronClaude/src/superclaude/cli/pipeline/process.py:173-214`.
- `SignalHandler` records `shutdown_requested` on SIGINT/SIGTERM and restores handlers on uninstall at `/config/workspace/IronClaude/src/superclaude/cli/sprint/process.py:219-250`.

### Isolation reality

- `IsolationLayers` and `setup_isolation(config)` exist and describe four layers (`CLAUDE_WORK_DIR`, `GIT_CEILING_DIRECTORIES`, `CLAUDE_PLUGIN_DIR`, `CLAUDE_SETTINGS_DIR`) at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:106-182`.
- Current `execute_sprint` does not call `setup_isolation(config)` in the main loop. Path B only creates `results/.isolation/phase-N`, copies the phase file into it, and passes `{'CLAUDE_WORK_DIR': str(isolation_dir)}` to `ClaudeProcess` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1303-1324`.
- Path A `_run_task_subprocess(...)` bypasses the sprint subclass constructor via `ClaudeProcess.__new__` and `_Base.__init__`, writes per-task output/error paths, and passes no extra env vars at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1076-1115`. There is no per-task isolation env in the current Path A implementation.
- **Port implication:** Do not treat the documented/commented “4-layer isolation” as an active runtime guarantee. Mastra porting should either implement it for real or explicitly scope the port to the currently active weaker isolation model.

### Path A task subprocesses and TurnLedger

- `execute_phase_tasks(...)` loops over parsed tasks, budget-checks `TurnLedger.can_launch()`, pre-debits `minimum_allocation`, runs a subprocess factory or `_run_task_subprocess`, maps exit code `0` to `PASS`, `124` to `INCOMPLETE`, and other non-zero exits to `FAIL`, reconciles budget, then runs wiring and anti-instinct hooks (`/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:927-1073`).
- `_run_task_subprocess(...)` builds only a minimal prompt with task ID/title, phase file, and description at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1086-1091`.
- Current Path A output files are task-specific: `config.task_output_file(phase, task)` and `config.task_error_file(phase, task)` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1098-1108`; those path helpers are defined at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:502-506`.
- `_run_task_subprocess(...)` currently returns `turns_consumed=0` with a comment that turn counting is wired separately at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1111-1115`. This limits TurnLedger accuracy for Path A.
- `TurnLedger` tracks `initial_budget`, `consumed`, `reimbursed`, reimbursement rate, minimum launch/remediation budgets, and wiring-specific budget counters at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:693-776`.
- `check_budget_guard(ledger)` exists at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:338-351`, but `execute_phase_tasks(...)` uses direct `ledger.can_launch()` checks instead at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:974-987`.

### Path B prompt/runtime

- Path B prompt construction is in `process.py::ClaudeProcess.build_prompt()` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/process.py:123-216`. It invokes `/sc:task Execute all tasks in @<phase_file> --compliance strict --strategy systematic` and injects sprint context, execution rules, checkpoint instructions, scope boundary, and result-file contract.
- The prompt explicitly requires checkpoint files before result files at `/config/workspace/IronClaude/src/superclaude/cli/sprint/process.py:187-195` and instructs the phase to write `EXIT_RECOMMENDATION: CONTINUE` or `HALT` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/process.py:208-215`.
- **Port implication:** Mastra can model this as a workflow step prompt, but the strict result-file sentinel is a SuperClaude-specific control-plane contract. Backlog.md/Beads task state should not replace it unless `_determine_phase_status` is also redesigned.

### Tmux and terminal UX

- `is_tmux_available()` returns true only when `tmux` exists and the process is not already inside a tmux session (`/config/workspace/IronClaude/src/superclaude/cli/sprint/tmux.py:50-55`).
- `launch_in_tmux(config)` creates a deterministic `sc-sprint-<sha1>` session, runs the foreground `superclaude sprint run ... --no-tmux` command, creates a 3-pane layout, attaches, then reads `.sprint-exitcode` from `config.state_dir` to propagate failure to the outer process (`/config/workspace/IronClaude/src/superclaude/cli/sprint/tmux.py:81-173`).
- `_build_foreground_command(config)` forwards `--state-dir` so the inner no-tmux process writes the same sentinel the outer process reads (`/config/workspace/IronClaude/src/superclaude/cli/sprint/tmux.py:176-210`). It forwards `--debug`, `--stall-timeout`, and non-default `--stall-action`, but does not forward `--startup-stall-timeout`, `--shadow-gates`, `--release-dir`, or fidelity override flags.
- `update_tail_pane(...)` targets pane `0.2` and tails the current output file; `update_summary_pane(...)` targets pane `0.1` and displays the latest summary file; see `/config/workspace/IronClaude/src/superclaude/cli/sprint/tmux.py:213-252`.
- `attach_to_sprint()` and `kill_sprint(force)` operate on the first running `sc-sprint-*` session found by `find_running_session()`; non-force kill sends SIGTERM to pane `0.0`, waits 10 seconds, then SIGKILL/kills the tmux session at `/config/workspace/IronClaude/src/superclaude/cli/sprint/tmux.py:255-323`.
- `SprintTUI` is Rich-based and uses `Live(..., refresh_per_second=2, screen=False)` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/tui.py:98-108`. Rendering errors are caught and reported without aborting the sprint at `/config/workspace/IronClaude/src/superclaude/cli/sprint/tui.py:116-152`.
- The TUI renders header, phase table, dual phase/task progress bar, optional latest summary notification, optional error panel, and active panel at `/config/workspace/IronClaude/src/superclaude/cli/sprint/tui.py:154-197`. Phase rows show status, gate, duration, turns, and output bytes at `/config/workspace/IronClaude/src/superclaude/cli/sprint/tui.py:221-303`.

### Monitoring and stall handling

- `OutputMonitor` watches a stream-json output file in a daemon thread, reading incremental chunks and parsing complete NDJSON lines at `/config/workspace/IronClaude/src/superclaude/cli/sprint/monitor.py:253-396`.
- Monitor state tracks output bytes, growth/event timestamps, events received, last task/tool, files changed, growth rate, stall seconds, activity log, turns, errors, last assistant text, task progress estimate, and token counts; see `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:623-666`.
- `MonitorState.stall_status` is display-oriented and returns `waiting...`, `active`, `thinking...`, or `STALLED` based on hardcoded 30s/120s thresholds at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:667-681`.
- Runtime watchdogs use CLI-configured thresholds, not `stall_status`: startup-stall fires when `events_received == 0` and `stall_seconds > startup_stall_timeout`; mid-stall fires when events have been seen and `stall_seconds > stall_timeout`; see `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1366-1445`.
- `stall_action='kill'` sets `_timed_out = True`, terminates the process, and later maps the phase exit code to 124; `stall_action='warn'` prints a warning and continues (`/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1382-1403` and `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1421-1440`).
- `detect_error_max_turns(output_path)` and `detect_prompt_too_long(output_path, error_path=...)` inspect output/error tails for budget/context-exhaustion signals at `/config/workspace/IronClaude/src/superclaude/cli/sprint/monitor.py:37-107`.
- The monitor extracts structured assistant events, tool-use activity, token counts, tool-result errors, task IDs, tool names, and files-changed regex signals at `/config/workspace/IronClaude/src/superclaude/cli/sprint/monitor.py:398-571`.

**Port implications for Mastra + Backlog.md + Beads:**
- Reusable conceptually: process lifecycle, stream-json monitoring, stall watchdogs, sentinel exit propagation, and Rich/tmux UX are strong patterns.
- Rebuild likely: Mastra's agent/workflow runtime would need its own subprocess/session abstraction if it is orchestrating Claude Code CLI sessions; Mastra agent approval can suspend tool execution before sensitive/long operations per Tavily-extracted Mastra docs, but it does not replace this file-backed watchdog/process-group model by itself.
- Backlog.md/Beads fit better as task-state stores than as process runners. Beads' dependency graph/ready-work concept (Tavily result: docs.rs `rusty-beads` and Peter Warnock overview) aligns with sprint dependencies, but sprint currently executes tasks sequentially in markdown order and treats process outputs/checkpoints/result files as the authority.

**Key Takeaways:**
- Sprint is a hard porting stress test because it combines CLI parsing, markdown task contracts, subprocess control, TUI/tmux, file monitors, watchdogs, checkpoints, and recovery.
- The current runtime has real divergence between Path A and Path B: Path A has task-level subprocesses but weaker live monitoring and weaker isolation; Path B has richer monitoring/context/checkpoint prompting but coarser phase-level execution.
- Any Mastra port that only models “phases and tasks” will miss the real complexity: process lifecycle, output files, result sentinels, monitors, watchdogs, and tmux IPC.

## Section 6 Mapping — Checkpoints, Result Classification, Diagnostics, Summaries, and Recovery

### Result classification and recovery

- `_determine_phase_status(...)` is the authoritative phase status classifier at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:2067-2148`.
- Classification priority is: exit 124 -> `TIMEOUT`; non-zero + prompt-too-long -> valid result-file status or `INCOMPLETE`; non-zero + end checkpoint PASS and no contamination -> `PASS_RECOVERED`; other non-zero -> `ERROR`; exit 0 + result file HALT/CONTINUE/status markers -> `HALT`/`PASS`; exit 0 + no result file but output exists -> `PASS_NO_REPORT` unless `error_max_turns`, then `INCOMPLETE`; no output -> `ERROR` (`/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:2088-2148`).
- `_classify_from_result_file(...)` rejects missing/stale/unreadable result files, treats `EXIT_RECOMMENDATION: HALT` as `HALT`, `CONTINUE` or `status: PASS` as `PASS_RECOVERED`, `status: FAIL` as `HALT`, and `status: PARTIAL` as `INCOMPLETE` (`/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1774-1808`).
- `_write_preliminary_result(...)` writes `EXIT_RECOMMENDATION: CONTINUE` after an exit-0 subprocess if no fresh non-empty result file exists, so status determination does not fall through to `PASS_NO_REPORT` (`/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1954-2018`).
- `_write_executor_result_file(...)` overwrites the result file after classification with executor-authored frontmatter, table, source metadata, monitor metrics, and `EXIT_RECOMMENDATION` (`/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:2020-2064`).
- Crash recovery checks `checkpoints/CP-P<NN>-END.md` for PASS, scans artifacts for next-phase task IDs, logs recovery, and returns `PASS_RECOVERED` only when uncontaminated (`/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1894-1951` and `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:2101-2109`).

### Checkpoints

- `checkpoints.py` centralizes parsing, verification, manifest writing, and auto-recovery; see module summary at `/config/workspace/IronClaude/src/superclaude/cli/sprint/checkpoints.py:1-7`.
- `extract_checkpoint_paths(phase_file, release_dir)` parses `Checkpoint Report Path:` declarations, associates each with the nearest preceding checkpoint heading, resolves `TASKLIST_ROOT/` and relative paths, and returns absolute expected paths at `/config/workspace/IronClaude/src/superclaude/cli/sprint/checkpoints.py:36-94`.
- `verify_checkpoint_files(...)` returns existence status for each declared checkpoint at `/config/workspace/IronClaude/src/superclaude/cli/sprint/checkpoints.py:97-112`.
- `_verify_checkpoints(...)` runs only after PASS-like status, emits `checkpoint_verification` events, and respects `checkpoint_gate_mode`: `off`, `shadow` (default), `soft`, or `full`; full mode downgrades to `PASS_MISSING_CHECKPOINT` when files are missing (`/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1811-1891`).
- End-of-sprint manifest creation calls `build_manifest(config.index_path, config.release_dir)` and `write_manifest(...)`, writing `<release_dir>/manifest.json` and emitting a `checkpoint_manifest` JSONL event at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1702-1725`.
- `recover_missing_checkpoints(...)` can synthesize missing checkpoint reports from tasklist verification blocks and matching phase artifacts; the recovered report explicitly marks status as `UNKNOWN` and recommends rerun/manual inspection (`/config/workspace/IronClaude/src/superclaude/cli/sprint/checkpoints.py:209-408`).
- The CLI `verify-checkpoints` subcommand builds a manifest, optionally recovers missing reports, writes `manifest.json`, and prints a table or JSON at `/config/workspace/IronClaude/src/superclaude/cli/sprint/commands.py:360-415`.

### Diagnostics and logs

- `SprintLogger` writes both JSONL and Markdown logs; paths come from `SprintConfig.execution_log_jsonl` and `.execution_log_md` (`/config/workspace/IronClaude/src/superclaude/cli/sprint/logging_.py:13-27` and `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:482-488`).
- `write_header(...)`, `write_phase_start(...)`, `write_phase_interrupt(...)`, `write_phase_result(...)`, `write_checkpoint_verification(...)`, and `write_summary(...)` provide the runtime log contract at `/config/workspace/IronClaude/src/superclaude/cli/sprint/logging_.py:28-213`.
- `read_status_from_log()` and `tail_log(...)` are stubs that print “not yet connected” at `/config/workspace/IronClaude/src/superclaude/cli/sprint/logging_.py:224-235`; the Click `status` and `logs` commands therefore do not currently report live status/log tails.
- On failed phase status, executor collects diagnostics with `DiagnosticCollector`, classifies with `FailureClassifier`, writes a diagnostic markdown report via `ReportGenerator`, then sets sprint outcome to `HALTED` and records halt phase (`/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1609-1639`).
- `DiagnosticCollector.collect(...)` snapshots monitor state and tails output/error/debug logs at `/config/workspace/IronClaude/src/superclaude/cli/sprint/diagnostics.py:72-127`.
- `FailureClassifier.classify(...)` prioritizes watchdog stall, timeout, context exhaustion, crash, error, and unknown at `/config/workspace/IronClaude/src/superclaude/cli/sprint/diagnostics.py:157-232`.

### Summaries and retrospectives

- The executor creates `SummaryWorker(PhaseSummarizer(config), on_summary_ready=...)` and fans summary paths out to either tmux summary pane or the foreground TUI notification line at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1168-1196`.
- Summary submission for Path B happens after checkpoint verification and before phase logging/notification at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1578-1592`. Path A currently does not submit summaries in the per-task branch before `continue` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1259-1301`.
- `summarizer.py` describes a daemon-thread summary pipeline that extracts signals from stream-json, optionally invokes `claude --print --model claude-sonnet-4-5` with 30s timeout, and writes `results/phase-<N>-summary.md`; see `/config/workspace/IronClaude/src/superclaude/cli/sprint/summarizer.py:1-25`.
- `extract_phase_signals(output_path)` is NDJSON-file based, yielding tasks, files changed, validations, reasoning excerpts, and errors at `/config/workspace/IronClaude/src/superclaude/cli/sprint/summarizer.py:165-240` and following lines in the same file.
- End-of-sprint wrap-up waits up to 90s for summaries, then attempts `RetrospectiveGenerator(config).generate(...)`; failures are logged but do not abort sprint wrap-up (`/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1661-1688`).

**Port implications for Mastra + Backlog.md + Beads:**
- Backlog.md/Beads can track task/phase state, dependencies, and recovery todos, but checkpoint/result-file contracts are more like execution evidence than backlog metadata.
- Mastra workflow state could represent checkpoint stages, but the current implementation relies on filesystem manifests and JSONL events. A faithful port needs explicit filesystem artifact handling or a migration plan for those artifacts.
- Recovery semantics are conservative and evidence-based. Porting to Beads “ready work” should preserve halted phase/task, remaining tasks, diagnostic path, and missing checkpoint state rather than simply marking tasks failed.

**Key Takeaways:**
- Sprint status is not just subprocess exit code; it is exit code + result file freshness + prompt-too-long detection + checkpoint inference + checkpoint gate mode.
- Checkpoints are currently a filesystem protocol embedded in markdown tasklists; a task-graph backend would need a first-class checkpoint artifact model.
- Logging is partially complete: JSONL/Markdown writes are real, but `status` and `logs` subcommands are stubs.

## Section 8 Mapping — Port Feasibility, Reuse/Rebuild Split, and Hardest Stress-Test Findings

### External solution research provenance

`SOLUTION_RESEARCH` used Tavily as provider. Sources consulted:

- Mastra docs/search: `https://mastra.ai/docs/agents/agent-approval`, `https://mastra.ai`, plus Tavily search result for Mastra TypeScript agent framework/workflows.
- Backlog.md docs/search: `https://github.com/MrLesk/Backlog.md`, plus Tavily results describing Backlog.md as a Git-native markdown project board/CLI.
- Beads docs/search: `https://docs.rs/rusty-beads`, `https://peterwarnock.com/tools/beads-distributed-task-management-for-agents`, and `https://betterstack.com/community/guides/ai/beads-issue-tracker-ai-agents` describing Git-backed graph/dependency issue tracking for AI agents.

### Reusable assets

- Markdown parser rules: phase filename discovery and task parsing from `config.py` can be ported into a Mastra/TypeScript adapter or kept as a Python subprocess library.
- State models: `TaskEntry`, `TaskResult`, `PhaseResult`, `SprintResult`, `MonitorState`, `TurnLedger`, and `CheckpointEntry` provide a concrete schema baseline for Backlog.md/Beads issue/task metadata.
- Process runner contract: generic `pipeline.process.ClaudeProcess` is reusable as a Python subprocess runner if the port remains hybrid; otherwise it becomes a TypeScript process-runner spec.
- Output monitoring: `OutputMonitor` is reusable algorithmically for stream-json parsing and TUI telemetry.
- Checkpoint utilities: `extract_checkpoint_paths`, `verify_checkpoint_files`, `build_manifest`, and `recover_missing_checkpoints` are cohesive enough to wrap or port.
- Tmux layout: `tmux.py` is self-contained, but Mastra/web orchestration may replace it with web/observability dashboards instead of porting pane management.

### Rebuild or redesign areas

- Mastra workflows would need explicit subprocess, timeout, signal, and file-monitor primitives; Mastra agent approval/human-in-loop features do not directly replace process groups, tmux IPC, or output-file watchdogs.
- Backlog.md is markdown/git-native task storage, but sprint's tasks are nested phase/task/checkpoint execution contracts, not ordinary backlog cards. A direct one-card-per-task import loses phase result, checkpoint, sentinel, and output-file context unless custom fields/conventions are added.
- Beads is a stronger conceptual fit for dependencies and ready-work detection, but sprint currently does not execute ready tasks by DAG; it executes file order with budget/stall control. A Beads port must choose between preserving sequential semantics or introducing DAG scheduling as a behavior change.
- The current code has active Path A/Path B divergence. A port should normalize or consciously preserve that split before adding a new orchestration framework.

### Hardest stress-test findings supported by code

- Sprint is the hardest current porting stress test where code evidence supports it because the runtime spans CLI config (`commands.py`, `config.py`), models (`models.py`), two process paths (`executor.py`, `process.py`, `pipeline/process.py`), file monitors (`monitor.py`), tmux/TUI (`tmux.py`, `tui.py`), ledgers/gates (`executor.py`, `models.py`, pipeline trailing gates), checkpoints (`checkpoints.py`), diagnostics (`diagnostics.py`), and summarization/retrospective (`summarizer.py`, `retrospective.py`).
- The largest mismatch with Backlog.md/Beads is that sprint has evidence artifacts and control files that are authoritative. Task state alone is insufficient.
- The largest mismatch with Mastra is subprocess/session management. Mastra is well-aligned for agent/workflow composition and approvals, but the sprint runner's current value is largely in OS/process/file/TUI control around Claude Code CLI.

**Key Takeaways:**
- Recommended port posture: hybrid first. Keep Python sprint runner for execution while experimenting with Backlog.md/Beads as task-state mirrors and Mastra as a supervisory/workflow layer.
- Do not use sprint as the first full rewrite candidate. Use it as an acceptance stress test after smaller CLI orchestration surfaces are ported.
- If sprint must be ported, preserve these invariants first: deterministic phase/task discovery, result-file freshness, checkpoint manifest, process-group termination, stream-json telemetry, stall watchdogs, and tmux/foreground exit-code propagation.

## Documentation Cross-Validation and Staleness Notes

### Generated sprint docs checked

1. `/config/workspace/IronClaude/docs/generated/sprint-cli/v3.7-refactor/chunk-02-sprint-tui-v2.md`
2. `/config/workspace/IronClaude/docs/generated/sprint-cli/debates/debate-sprint-context.md`

### Cross-validated claims

- Claim: Path A does not start `OutputMonitor`. **[CODE-VERIFIED]** Current Path A branches from `tasks = _parse_phase_tasks(...)` through `execute_phase_tasks(...)` and `continue`, skipping the monitor start block at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1259-1301`; monitor reset/start is in Path B at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1309-1315`.
- Claim: Path A constructs ad-hoc `MonitorState` objects for TUI updates. **[CODE-VERIFIED]** See `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:993-1000` and `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1065-1071`.
- Claim: Path A task prompt is minimal while Path B has sprint context. **[CODE-VERIFIED]** Path A prompt is three core lines at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1086-1091`; Path B builds a sprint context section at `/config/workspace/IronClaude/src/superclaude/cli/sprint/process.py:147-167`.
- Claim: Path A per-task subprocesses all write to the same `phase-N-output.txt`. **[CODE-CONTRADICTED]** Current code writes task-specific output/error files via `config.task_output_file(phase, task)` and `config.task_error_file(phase, task)` at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1098-1108`; helpers render `phase-N-task-TXX.YY-output.txt` and errors at `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:502-506`. This makes the generated v3.7 doc stale on that specific point.
- Claim: Path A `turns_consumed` is always 0. **[CODE-VERIFIED]** `_run_task_subprocess(...)` returns `(exit_code, 0, output_bytes)` with a turn-counting TODO-style comment at `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1111-1115`.
- Claim: Tmux has a summary pane and a tail pane. **[CODE-VERIFIED]** Pane constants and 3-pane layout are in `/config/workspace/IronClaude/src/superclaude/cli/sprint/tmux.py:39-48` and `/config/workspace/IronClaude/src/superclaude/cli/sprint/tmux.py:111-156`.
- Claim: Worker cwd is not guaranteed. **[CODE-VERIFIED]** Base `Popen` has no `cwd` argument at `/config/workspace/IronClaude/src/superclaude/cli/pipeline/process.py:125-134`; current callers rely on env vars such as `CLAUDE_WORK_DIR` for Path B (`/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1320-1324`) and pass no such env for Path A (`/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1098-1108`).

## Gaps and Questions

- **[CODE-CONTRADICTED] Generated TUI v2 doc says Path A task subprocesses write to the same phase output file.** Current code uses per-task output/error files. Question: was the generated doc written before the per-task path change, and do downstream summary/TUI docs need regeneration?
- **[UNVERIFIED] Mastra exact workflow primitives for long-running subprocess supervision.** Tavily confirmed Mastra agent approval/human-in-loop and framework positioning, but this research did not extract a Mastra API that directly matches process-group lifecycle, file-tail monitoring, tmux IPC, and kill escalation.
- **[UNVERIFIED] Backlog.md custom-field suitability.** Public docs/search confirm Git-native markdown task storage, but this research did not verify whether Backlog.md can natively encode sprint fields like phase number, checkpoint manifest path, result-file freshness, `TurnLedger`, or monitor telemetry without custom markdown conventions.
- **[UNVERIFIED] Beads exact CLI/schema support for checkpoint/evidence artifacts.** Public docs/search confirm Git-backed DAG/ready-work/context-store themes, but this research did not verify first-class artifact/checkpoint fields. Treat Beads as a likely task graph fit, not yet a proven execution-evidence fit.
- `setup_isolation(config)` appears unused in `execute_sprint`; only Path B sets `CLAUDE_WORK_DIR`, and Path A does not pass isolation env vars. Question: is this intentional rollback/debt, or should port planning treat four-layer isolation as a desired future invariant rather than current behavior?
- `status` and `logs` commands are stubs despite being advertised in the sprint group docstring. Question: should a port implement these as real views over `execution-log.jsonl`, or preserve current behavior?
- Tmux foreground command does not forward every run flag (`--startup-stall-timeout`, `--shadow-gates`, `--release-dir`, fidelity overrides). Question: are those omissions accepted constraints or bugs to fix before porting?
- Path A does not submit `SummaryWorker` summaries before continuing, while Path B does. Question: should summaries be normalized before any port feasibility decision?

## Stale Documentation Found

- **[STALE DOC]** `/config/workspace/IronClaude/docs/generated/sprint-cli/v3.7-refactor/chunk-02-sprint-tui-v2.md:19` says all Path A per-task subprocesses write to the same `phase-N-output.txt`. Current code contradicts this: `/config/workspace/IronClaude/src/superclaude/cli/sprint/executor.py:1098-1108` uses task-specific output/error files and `/config/workspace/IronClaude/src/superclaude/cli/sprint/models.py:502-506` defines task-specific filenames.
- **[STALE DOC]** Several line-number citations in `/config/workspace/IronClaude/docs/generated/sprint-cli/v3.7-refactor/chunk-02-sprint-tui-v2.md` and `/config/workspace/IronClaude/docs/generated/sprint-cli/debates/debate-sprint-context.md` no longer match current `executor.py` line numbers. Some structural claims remain true after line-number remapping (Path A no `OutputMonitor`, minimal Path A prompt), but the docs should not be used for direct file:line citations.
- **[STALE DOC]** `/config/workspace/IronClaude/docs/generated/sprint-cli/v3.7-refactor/chunk-02-sprint-tui-v2.md:145-167` recommends per-task output-file separation as a future prerequisite. Current code has already implemented task-specific output files, but summary/TUI code has not fully consumed that capability.

## Summary

Sprint run is a high-complexity orchestration surface with two runtime paths. The current code executes parsed task inventories through Path A (`execute_phase_tasks` plus one Claude subprocess per `TaskEntry`) and freeform phase files through Path B (`ClaudeProcess` plus `OutputMonitor`). The port feasibility conclusion is hybrid-first: keep the Python runner as execution authority while evaluating Mastra as a supervisory workflow layer and Backlog.md/Beads as task-state/dependency mirrors.

The primary reusable pieces are the parsing rules, data schemas, checkpoint utilities, monitor algorithm, and process-runner contract. The primary rebuild areas are Mastra subprocess supervision, task graph mapping, checkpoint/evidence artifact modeling, and terminal/session UX. The biggest code-backed risks are Path A/Path B divergence, partial/unused isolation infrastructure, stubbed `status`/`logs`, file-based result/checkpoint contracts, and the need to preserve stall/recovery semantics.
