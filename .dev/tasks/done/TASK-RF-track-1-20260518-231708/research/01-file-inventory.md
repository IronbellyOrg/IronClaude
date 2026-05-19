# Research: File Inventory

- **Topic type:** File Inventory
- **Scope:** `src/superclaude/cli/sprint/` (19 .py files) + tracked `.sprint-exitcode` files under `.dev/releases/**/`
- **Status:** Complete
- **Date:** 2026-05-18

---

## 1. Sprint module `.sprint-exitcode` references

Verified by direct `grep -rn '\.sprint-exitcode' src/superclaude/cli/sprint/`. Only two writers/readers exist in the sprint module itself.

| file:line | direction | context snippet | what it does |
|---|---|---|---|
| `src/superclaude/cli/sprint/executor.py:1754` | **W** (write) | `        (config.release_dir / ".sprint-exitcode").write_text(str(_exitcode))` — preceded by `# Write sentinel exit code file so tmux caller can read the outcome` and `_exitcode = 0 if sprint_result.outcome == SprintOutcome.SUCCESS else 1`; wrapped in `try/except OSError: pass` | Final write at end of `execute_sprint()` — emits the sentinel that the tmux outer-process layer reads after detach. This is the **primary bug site** (writes into the tracked archive path). |
| `src/superclaude/cli/sprint/tmux.py:166` | **R** (read) | `    sentinel = config.release_dir / ".sprint-exitcode"` followed by `exit_code = int(sentinel.read_text().strip())` — after `subprocess.run(["tmux", "attach-session", ...])` returns | Outer-process reader inside `launch_in_tmux()` — runs in the parent CLI after `tmux attach-session` detaches; needs to read the sentinel written by the inner `execute_sprint()` so it can `raise SystemExit(exit_code)` with the right code. |

Additional **non-source** references found (outside scope but relevant for downstream updates):

| file:line | direction | what it does |
|---|---|---|
| `tests/sprint/test_tmux.py:100` | **W** (test fixture) | Test writes `0\n` to `config.release_dir / ".sprint-exitcode"` to simulate a successful inner run so `launch_in_tmux` returns cleanly. Will need to follow whatever new path the writer/reader pair settles on. |
| `src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh:90,126` | R | Crash-recovery skill reads `$d/.sprint-exitcode` to surface stalled-sprint state to the user. Out of sprint scope but the path *must remain discoverable* (likely via `state_dir` adjacent to or instead of `release_dir`). |
| `src/superclaude/skills/sc-crash-recovery/SKILL.md` lines 65, 118, 127, 134, 137; `refs/pipelines.md:100,103`; `refs/investigators.md:18`; `refs/report-template.md:100` | R (doc) | Skill documentation referencing the sentinel for recovery flows. |
| `docs/generated/sprint-cli/03-execution-engine.md:99`, `06-artifacts-output.md:17,147`, `09-wiring-validation.md:85`, `00-overview.md:130` | doc | Generated documentation describing the sentinel location. |
| `docs/sprint-cli-deep-dive.md` lines 66, 276, 1287, 1291, 1322, 1622; `docs/developer-guide/sprint-tui-reference.md:148,194,516` | doc | Hand-authored docs describing the writer line. |

---

## 2. Sprint module `release_dir` references

Verified by direct `grep -rn 'release_dir' src/superclaude/cli/sprint/`. Captures every read, every pass-through, and the single definition site.

| file:line | usage type | snippet / purpose |
|---|---|---|
| `src/superclaude/cli/sprint/models.py:354` | doc-string mentioning the field | "The ``release_dir`` field maps to ``work_dir``…" |
| `src/superclaude/cli/sprint/models.py:359` | **def** (canonical definition) | `release_dir: Path = field(default_factory=lambda: Path("."))` on `SprintConfig` (frozen-style dataclass via `object.__setattr__`) |
| `src/superclaude/cli/sprint/models.py:402` | comment | Sync release_dir to PipelineConfig.work_dir |
| `src/superclaude/cli/sprint/models.py:404` | **read+propagate** | `object.__setattr__(self, "work_dir", self.release_dir)` — binds `work_dir` (inherited from `PipelineConfig`) to `release_dir` in `__post_init__` |
| `src/superclaude/cli/sprint/models.py:454` | property derivation | `results_dir = self.release_dir / "results"` |
| `src/superclaude/cli/sprint/models.py:458` | property derivation | `execution_log_jsonl = self.release_dir / "execution-log.jsonl"` |
| `src/superclaude/cli/sprint/models.py:462` | property derivation | `execution_log_md = self.release_dir / "execution-log.md"` |
| `src/superclaude/cli/sprint/config.py:236` | def | `def _resolve_release_dir(index_path: Path) -> Path:` — derives release dir from tasklist-index location (with grandparent fallback) |
| `src/superclaude/cli/sprint/config.py:266` | log message | `"Resolved release_dir to grandparent: %s (index inside %s/)"` |
| `src/superclaude/cli/sprint/config.py:336` | construction | `release_dir=_resolve_release_dir(index_path)` inside `load_sprint_config()` — only construction site in the loader |
| `src/superclaude/cli/sprint/commands.py:42` | import | `from .config import _resolve_release_dir` |
| `src/superclaude/cli/sprint/commands.py:44` | call | `sprint_dir = _resolve_release_dir(index_path)` (used by `attach`/`status` subcommands) |
| `src/superclaude/cli/sprint/commands.py:176-177` | click option name | `"--release-dir"` / `"release_dir_override"` (variable name) |
| `src/superclaude/cli/sprint/commands.py:198` | param | `release_dir_override: Path | None,` in `run()` signature |
| `src/superclaude/cli/sprint/commands.py:234-237` | override write | `if release_dir_override is not None: ... object.__setattr__(config, "release_dir", resolved)` — only post-load mutation site |
| `src/superclaude/cli/sprint/tmux.py:58` | param | `def session_name(release_dir: Path) -> str:` |
| `src/superclaude/cli/sprint/tmux.py:60` | read | `h = hashlib.sha1(str(release_dir.resolve()).encode()).hexdigest()[:8]` — derives unique tmux session name |
| `src/superclaude/cli/sprint/tmux.py:87` | read | `name = session_name(config.release_dir)` |
| `src/superclaude/cli/sprint/tmux.py:166` | read | **sentinel reader** (see section 1) |
| `src/superclaude/cli/sprint/executor.py:178` | read | `scoped_work_dir=config.release_dir,` passed to `setup_isolation` |
| `src/superclaude/cli/sprint/executor.py:179` | read | `git_boundary=config.release_dir,` |
| `src/superclaude/cli/sprint/executor.py:389` | read | reference in setup/aggregation pathway |
| `src/superclaude/cli/sprint/executor.py:412` | read | `source_dir = config.release_dir` |
| `src/superclaude/cli/sprint/executor.py:504` | read | `source_dir = config.release_dir` |
| `src/superclaude/cli/sprint/executor.py:592` | read | passed positionally into helper |
| `src/superclaude/cli/sprint/executor.py:1708` | read | `_manifest = build_manifest(config.index_path, config.release_dir)` |
| `src/superclaude/cli/sprint/executor.py:1709` | read | `_manifest_path = config.release_dir / "manifest.json"` |
| `src/superclaude/cli/sprint/executor.py:1754` | **write target via release_dir** | **sentinel writer** (see section 1) |
| `src/superclaude/cli/sprint/executor.py:1829` | read | `declared = extract_checkpoint_paths(phase.file, config.release_dir)` |
| `src/superclaude/cli/sprint/executor.py:1885` | read | `config.release_dir / "checkpoints" / f"CP-P{phase.number:02d}-END.md"` |
| `src/superclaude/cli/sprint/executor.py:1901` | read | `artifacts_dir = config.release_dir / "artifacts"` |
| `src/superclaude/cli/sprint/executor.py:1909` | read | `contaminated.append(str(md_file.relative_to(config.release_dir)))` |
| `src/superclaude/cli/sprint/process.py:130` | read | `sprint_name = getattr(config, "release_name", None) or config.release_dir.name` |
| `src/superclaude/cli/sprint/process.py:132` | read | `artifact_root = config.release_dir / "artifacts"` |
| `src/superclaude/cli/sprint/process.py:144` | read | builds list of prior `phase-N` dirs under release_dir |
| `src/superclaude/cli/sprint/checkpoints.py:38` | param | `release_dir: Path` parameter on `extract_checkpoint_paths` |
| `src/superclaude/cli/sprint/checkpoints.py:46` | doc-string | refers to release_dir as sprint's work dir |
| `src/superclaude/cli/sprint/checkpoints.py:82` | read | `resolved = (release_dir / candidate).resolve()` |
| `src/superclaude/cli/sprint/checkpoints.py:128` | param | `release_dir: Path` on `verify_checkpoint_files` |
| `src/superclaude/cli/sprint/checkpoints.py:149` | read | `extract_checkpoint_paths(phase.file, release_dir)` |
| `src/superclaude/cli/sprint/tui.py:202` | doc-string | "Derived from ``SprintConfig.release_dir`` basename" |
| `src/superclaude/cli/sprint/tui.py:206` | read | `name = self.config.release_dir.name` (TUI title fallback) |

**Key observation for fix design:** `release_dir` is the canonical archive path used by ~30 call sites for legitimate archive content (results/, execution-log.*, checkpoints/, artifacts/, manifest.json). The bug is *only* that the sentinel exit code piggybacks on it. The fix should introduce a sibling `state_dir` field (covered by track 02) and update **exactly two source lines** (executor.py:1754 writer + tmux.py:166 reader) plus one test (`tests/sprint/test_tmux.py:100`).

**Note (gap-fill 2026-05-18):** Line numbers re-verified post PR-A landing (which grew `executor.py` by ~40 lines: 2096 → 2136). Drift summary: executor.py sentinel writer `1714 → 1754`; manifest build `1668→1708`, manifest path `1669→1709`; checkpoint extract `1789→1829`; checkpoint END path `1845→1885`; artifacts dir `1861→1901`; contaminated rel-path `1869→1909`. `models.py` SprintConfig def `347→348`; `__post_init__` body shifted by +1 line; field/property lines shifted by +1. `commands.py` `--release-dir` option block moved (170→176-177), `run()` param (189→198), override write (224-228→234-237). `tmux.py:166` and `config.py:236/266/336` unchanged.

**Scope decision needed — cross-skill dependency (`bootstrap_scan.sh`):** The crash-recovery skill at `src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh:90,126` reads `$d/.sprint-exitcode` relative to release roots. The FU-001 fix MUST choose ONE of:

- **(a) In-scope co-patch**: FU-001 also patches `bootstrap_scan.sh:90,126` to read from `state_dir` (or to look in both old + new locations during a migration window), AND copies the change into the dev-side `.claude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh` via `make sync-dev`. Both lines are simple shell variable updates; estimated ~10 lines of diff incl. fallback logic.
- **(b) Defer with explicit Open Question**: FU-001 ships sprint changes only and the generated task file MUST include an Open Question section flagging that crash-recovery alignment is deferred to a sibling follow-up (e.g. FU-003), AND that `bootstrap_scan.sh` will surface stalled-sprint state inaccurately for new releases until that follow-up lands. The Open Question must include a concrete recommendation on sibling timing.

**Builder must pick (a) or (b) explicitly — do not leave the cross-skill dependency unaddressed.**

---

## 3. Tracked `.sprint-exitcode` files (40 total)

All files are 1 byte. Content is a single digit `0` or `1` (no trailing newline observed). Listed in `git ls-files` order with age (`git log -1 --format=%ai`), content, and disposition recommendation.

Disposition legend:
- **rm-cached**: `git rm --cached` (untrack but keep working-copy if it exists; transient runtime sentinel, never belonged in version control)
- **rm**: `git rm` (no value to keep on disk; archived release; safe to delete entirely)

| # | path | size | age | content | disposition |
|---|---|---|---|---|---|
| 1 | `.dev/releases/archive/v3.66-tdd-skill-refactor-v2/.sprint-exitcode` | 1 | 2026-04-13 | `0` | rm |
| 2 | `.dev/releases/complete/cleanup-audit-v2-UNIFIED-SPEC/tasklist/.sprint-exitcode` | 1 | 2026-03-06 | `0` | rm |
| 3 | `.dev/releases/complete/cross-framework-deep-analysis/.sprint-exitcode` | 1 | 2026-03-16 | `0` | rm |
| 4 | `.dev/releases/complete/cross-framework-deep-analysis/v2.25-cli-portify-cli/.sprint-exitcode` | 1 | 2026-03-16 | `1` | rm |
| 5 | `.dev/releases/complete/release-split-workspace-rca/.sprint-exitcode` | 1 | 2026-05-13 | `0` | rm |
| 6 | `.dev/releases/complete/unified-audit-gating-v1.2.1/tasklist/.sprint-exitcode` | 1 | 2026-03-07 | `0` | rm |
| 7 | `.dev/releases/complete/unified-audit-gating-v1.2.1/test-evidence/live-sprint/.sprint-exitcode` | 1 | 2026-03-07 | `1` | rm |
| 8 | `.dev/releases/complete/unified-audit-gating-v2/.sprint-exitcode` | 1 | 2026-03-07 | `0` | rm |
| 9 | `.dev/releases/complete/v.2.11-roadmap-v4/tasklist/.sprint-exitcode` | 1 | 2026-03-06 | `0` | rm |
| 10 | `.dev/releases/complete/v.2.17-roadmap-reliability/.sprint-exitcode` | 1 | 2026-03-08 | `0` | rm |
| 11 | `.dev/releases/complete/v2.07-tasklist-v1/tasklist/.sprint-exitcode` | 1 | 2026-03-05 | `0` | rm |
| 12 | `.dev/releases/complete/v2.08-RoadmapCLI/tasklist/.sprint-exitcode` | 1 | 2026-03-06 | `0` | rm |
| 13 | `.dev/releases/complete/v2.09-adversarial-v2/tasklist/.sprint-exitcode` | 1 | 2026-03-07 | `0` | rm |
| 14 | `.dev/releases/complete/v2.10-spec-panel-v2/tasklist/.sprint-exitcode` | 1 | 2026-03-06 | `0` | rm |
| 15 | `.dev/releases/complete/v2.13-CLIRunner-PipelineUnification/smoke-test-sprint/.sprint-exitcode` | 1 | 2026-03-07 | `0` | rm |
| 16 | `.dev/releases/complete/v2.13-CLIRunner-PipelineUnification/tasklist/.sprint-exitcode` | 1 | 2026-03-06 | `0` | rm |
| 17 | `.dev/releases/complete/v2.18-cli-portify-v2/.sprint-exitcode` | 1 | 2026-03-08 | `0` | rm |
| 18 | `.dev/releases/complete/v2.19-roadmap-validate/.sprint-exitcode` | 1 | 2026-03-09 | `0` | rm |
| 19 | `.dev/releases/complete/v2.20-WorkflowEvolution/.sprint-exitcode` | 1 | 2026-03-09 | `0` | rm |
| 20 | `.dev/releases/complete/v2.22-RoadmapRemediate/.sprint-exitcode` | 1 | 2026-03-10 | `0` | rm |
| 21 | `.dev/releases/complete/v2.23-cli-portify-v3/.sprint-exitcode` | 1 | 2026-03-11 | `0` | rm |
| 22 | `.dev/releases/complete/v2.24-cli-portify-cli-v4/.sprint-exitcode` | 1 | 2026-03-14 | `0` | rm |
| 23 | `.dev/releases/complete/v2.24.1-cli-portify-cli-v5/.sprint-exitcode` | 1 | 2026-03-14 | `0` | rm |
| 24 | `.dev/releases/complete/v2.24.2-Accept-Spec-Change/.sprint-exitcode` | 1 | 2026-03-14 | `0` | rm |
| 25 | `.dev/releases/complete/v2.24.5-SpecFidelity/.sprint-exitcode` | 1 | 2026-03-15 | `0` | rm |
| 26 | `.dev/releases/complete/v2.25-cli-portify-cli/.sprint-exitcode` | 1 | 2026-03-16 | `0` | rm |
| 27 | `.dev/releases/complete/v2.25.5-PreFlightExecutor/.sprint-exitcode` | 1 | 2026-03-16 | `0` | rm |
| 28 | `.dev/releases/complete/v2.25.5-PreFlightExecutor/roadmap-pass-no-report-fix/.sprint-exitcode` | 1 | 2026-03-16 | `0` | rm |
| 29 | `.dev/releases/complete/v2.25.7-Phase8HaltFix/.sprint-exitcode` | 1 | 2026-03-16 | `0` | rm |
| 30 | `.dev/releases/complete/v2.26-roadmap-v5/.sprint-exitcode` | 1 | 2026-03-17 | `0` | rm |
| 31 | `.dev/releases/complete/v3.05_DeterministicFidelityGates/.sprint-exitcode` | 1 | 2026-03-21 | `0` | rm |
| 32 | `.dev/releases/complete/v3.0_unified-audit-gating/.sprint-exitcode` | 1 | 2026-03-19 | `0` | rm |
| 33 | `.dev/releases/complete/v3.1_Anti-instincts__/.sprint-exitcode` | 1 | 2026-03-21 | `0` | rm |
| 34 | `.dev/releases/complete/v3.2_fidelity-refactor___/.sprint-exitcode` | 1 | 2026-03-21 | `0` | rm |
| 35 | `.dev/releases/complete/v3.65-prd-refactor/.sprint-exitcode` | 1 | 2026-04-13 | `0` | rm |
| 36 | `.dev/releases/complete/v3.65-tdd-skill-refactor/.sprint-exitcode` | 1 | 2026-04-13 | `0` | rm |
| 37 | `.dev/releases/complete/v3.66-tdd-skill-refactor-v2/.sprint-exitcode` | 1 | 2026-05-13 | `0` | rm |
| 38 | `.dev/releases/complete/v3.67-prd-skill-portify/.sprint-exitcode` | 1 | 2026-05-13 | `0` | rm |
| 39 | `.dev/releases/complete/v3.7-turnledger-integration/v3.7-TurnLedger-Validation/tasklist/.sprint-exitcode` | 1 | 2026-03-23 | `0` | rm |
| 40 | `.dev/releases/current/task-sc-task-directional-merge/.sprint-exitcode` | 1 | 2026-05-15 | `0` | rm |

**Untracked sibling:** there is one more `.sprint-exitcode` visible from git status at `.dev/releases/current/task-builder-merge/.sprint-exitcode` — but it shows up as **untracked** (currently not in the 40-file tracked inventory). The fix's new state directory should swallow this file too going forward.

**Rationale for "rm" (not "rm-cached") across the board:**
- Every file is 1 byte (just `0` or `1`); contains no historical or evidentiary value beyond the boolean pass/fail signal already preserved in `execution-log.jsonl`/`manifest.json` in the same directory.
- `execution-log.jsonl` records per-phase `exit_code` and overall `status` — the sentinel is strictly redundant with authoritative log data.
- Keeping the file on disk after untracking still confuses future runs (would re-read stale 0/1) — better to remove cleanly and let the new transient `state_dir` own all post-fix sentinels.
- The single `archive/` entry (#1) is duplicated by `complete/v3.66-tdd-skill-refactor-v2` (#37) — neither is operationally needed.

If track 02 (state_dir composition) lands a migration shim that prefers `state_dir` but falls back to `release_dir`, the disposition could shift to **rm-cached** for the most recent (`current/`) entries — but `current/task-sc-task-directional-merge` is already a stale archived workspace, so **rm** is still safe.

---

## 4. Other sprint files inventory (full `src/superclaude/cli/sprint/*.py` overview)

Line counts via `wc -l`. Purpose and key exports captured by reading top-level `def`/`class`/`@click...` declarations.

| file | lines | 1-sentence purpose | key exports |
|---|---|---|---|
| `__init__.py` | 5 | Package re-export of the click sprint group | `sprint_group` |
| `checkpoints.py` | 400 | Extract checkpoint declarations from tasklists, verify on-disk presence, build/write `manifest.json`, recover missing checkpoints | `extract_checkpoint_paths`, `verify_checkpoint_files`, `build_manifest`, `write_manifest`, `recover_missing_checkpoints`, `CheckpointEntry` |
| `classifiers.py` | 45 | Map subprocess outcome + stdout/stderr to a phase status string ("empirical gate v1") | `empirical_gate_v1`, `run_classifier` |
| `commands.py` | 433 | Click CLI surface — `sprint run`, `sprint attach`, `sprint status`; only place `--release-dir` override is honored | `sprint_group`, `run`, `attach`, `status` |
| `config.py` | 503 | Load + validate a `SprintConfig`; discover phases; parse tasklists; resolve release directory from index path | `load_sprint_config`, `discover_phases`, `validate_phases`, `_resolve_release_dir`, `parse_tasklist`, `parse_tasklist_file`, `count_tasks_in_file` |
| `debug_logger.py` | 138 | Build per-sprint debug logger writing into `results_dir/debug.log` with auto-flush | `setup_debug_logger`, `debug_log`, `_FlushHandler`, `_DebugFormatter` |
| `diagnostics.py` | 291 | Failure classification + diagnostic bundle assembly + report generation for phase failures | `FailureCategory`, `DiagnosticBundle`, `DiagnosticCollector`, `FailureClassifier`, `ReportGenerator` |
| `executor.py` | 2136 | Sprint orchestration core — phase loop, gates, isolation, wiring/anti-instinct hooks, contamination check, **writes `.sprint-exitcode` sentinel** | `execute_sprint`, `execute_phase_tasks`, `aggregate_task_results`, `setup_isolation`, `IsolationLayers`, `SprintGatePolicy`, `AggregatedPhaseReport`, wiring/anti-instinct hook runners |
| `kpi.py` | 214 | Build a per-sprint `GateKPIReport` aggregating gate outcomes | `GateKPIReport`, `build_kpi_report` |
| `logging_.py` | 235 | Sprint structured logger writing to `execution-log.jsonl` + `execution-log.md`; status/tail helpers | `SprintLogger`, `read_status_from_log`, `tail_log` |
| `models.py` | 857 | All sprint dataclasses + enums; `SprintConfig` (the one that owns `release_dir`), `Phase`, `TaskEntry`, `TaskResult`, `PhaseResult`, `SprintResult`, `MonitorState`, status enums | `SprintConfig`, `Phase`, `TaskEntry`, `TaskResult`, `PhaseResult`, `SprintResult`, `MonitorState`, `TaskStatus`, `GateOutcome`, `GateDisplayState`, `PhaseStatus`, `SprintOutcome`, `CheckpointEntry`, `SprintStep`, `is_valid_gate_transition` |
| `monitor.py` | 571 | Stream-monitor of Claude Code output for stalls / max-turns / prompt-too-long / tool-use events | `OutputMonitor`, `detect_error_max_turns`, `detect_prompt_too_long`, `count_turns_from_output` |
| `notify.py` | 62 | Desktop notifications for phase/sprint completion | `notify_phase_complete`, `notify_sprint_complete` |
| `preflight.py` | 245 | Run optional preflight phases before main sprint, emit evidence files | `execute_preflight_phases` |
| `process.py` | 385 | Wrap `pipeline.ClaudeProcess` with sprint-specific spawn/signal/exit hooks; build per-task context | `ClaudeProcess`, `SignalHandler`, `build_task_context`, `get_git_diff_context`, `compress_context_summary` |
| `retrospective.py` | 366 | Aggregate phase summaries into release-level retrospective markdown | `ReleaseRetrospective`, `RetrospectiveGenerator` |
| `summarizer.py` | 644 | Per-phase signal extraction + haiku-narrative + markdown rendering; background `SummaryWorker` | `PhaseSummary`, `PhaseSummarizer`, `SummaryWorker`, `extract_phase_signals`, `invoke_haiku` |
| `tmux.py` | 317 | tmux session lifecycle (launch 3-pane layout, attach, kill) + **reads `.sprint-exitcode` sentinel** after detach | `launch_in_tmux`, `is_tmux_available`, `session_name`, `find_running_session`, `attach_to_sprint`, `kill_sprint`, `update_tail_pane`, `update_summary_pane` |
| `tui.py` | 629 | Live Rich-based terminal UI for the TUI pane | `SprintTUI` and formatters |
| **total** | **8464** | | |

---

## 5. Summary

- **Only two source-code touch points** for the FU-001 fix in the sprint module: `executor.py:1754` (writer) and `tmux.py:166` (reader). Both currently use `config.release_dir / ".sprint-exitcode"`. The 30-odd other `release_dir` references are all legitimate archive-path uses (results/, execution-log.*, checkpoints/, artifacts/, manifest.json) and must remain unchanged.
- **One test fixture** writes the sentinel (`tests/sprint/test_tmux.py:100`) and must follow whatever new path the writer/reader adopt.
- **`SprintConfig` is the cleanest place to add a `state_dir` field** (definition at `models.py:359`); construction happens in exactly one place (`config.py:336` inside `load_sprint_config`), and an override path already exists (`commands.py:236-237` mutates `release_dir`). Track 02 will own the field composition design.
- **All 40 tracked `.sprint-exitcode` files are 1-byte, in archived `complete/` or `archive/` releases**, and are redundant with `execution-log.jsonl`. Recommend a clean `git rm` (not `--cached`) for all 40, since the content is fully reconstructible from logs and the new `state_dir` will own all post-fix sentinels. One additional untracked sentinel exists at `.dev/releases/current/task-builder-merge/.sprint-exitcode` (already outside the inventory).
- **External readers** (crash-recovery skill scripts at `bootstrap_scan.sh:90,126`) must still be able to find the sentinel; track 02 should ensure `state_dir` is documented/discoverable (e.g., predictable sibling of `release_dir` or symlink) before this lands, or the recovery skill update must ship in the same release.
