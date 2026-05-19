# Research 03 — Integration Points (Caller Graph & Blast Radius)

**Status:** Complete
**Researcher:** R3 of 5
**Scope:** Trace callers and downstream consumers for the 6 fixes (C1–C6) in sprint-runner track.
**Method:** Grep + Glob + Read across `src/superclaude/`, `tests/`, `docs/`.

---

## IP-1 — `config.stall_timeout` / `config.stall_action`

**Target:** `src/superclaude/cli/sprint/models.py:369-370`

```python
stall_timeout: int = 0  # 0 = disabled
stall_action: str = "warn"  # "warn" or "kill"
```

**Sprint-CLI surface:**
- `src/superclaude/cli/sprint/commands.py:132-143` — Click flags `--stall-timeout` (int, default `0`) and `--stall-action` (Choice["warn","kill"], default `"warn"`). Forwarded into `build_sprint_config` at lines 215-216.
- `src/superclaude/cli/sprint/config.py:284-285,345-346` — `build_sprint_config()` kwargs.
- `src/superclaude/cli/sprint/tmux.py:200-203` — Forwards `--stall-timeout` / `--stall-action` to nested `tmux` sessions only when set non-default.
- `src/superclaude/cli/sprint/executor.py:1367-1398` — Sole watchdog consumer (per-phase path only).

**Tests (will break if defaults change):**
- `tests/sprint/diagnostic/test_debug_logger.py:321-365` — `test_default_stall_timeout_zero`, `test_default_stall_action_warn`, plus 2 more assertions on `0/"warn"` defaults.
- `tests/sprint/diagnostic/test_instrumentation.py:348-572` — 8 tests pinning forwarding behaviour at `0`/`120`/`"warn"`/`"kill"` boundaries (e.g. `test_stall_timeout_forwarded`, `test_stall_timeout_not_forwarded_when_zero`, `test_cli_help_shows_stall_timeout_option`).
- `tests/sprint/test_watchdog.py:50,125,191` — fixtures use `stall_timeout=10` so unaffected by default change, but verify both actions.
- `tests/roadmap/test_nfr_compliance.py:135-138` — `test_no_stall_timeout_field` asserts the **roadmap** spec does NOT mention `stall_timeout`. Roadmap-NFR unrelated; not impacted by sprint default change.

**Docs:**
- `docs/sprint-cli-deep-dive.md:131-132,527-532` — documents `int = 0` default explicitly.
- `docs/developer-guide/sprint-tui-reference.md:541-542` — same.
- `docs/generated/sprint-cli/02-data-models.md:249` — lists the fields.
- `docs/analysis/gsd-vs-superclaude-comparison.md:407` — references watchdog behavior.

**Other CLIs using same name (do NOT cross-contaminate):**
- `prd/models.py:130-131` (`int = 120, "warn"`), `cleanup_audit/models.py:76-77` (`int = 300, "kill"`), `cli_portify/models.py:581` (`int = 300`). Each has its own command surface — sprint changes do not affect them.

**Blast Radius:** **MEDIUM** for changing defaults (3 tests pin the literal `0`/`"warn"`, ~5 doc files need updating). **LOW** for adding watchdog logic that respects the existing fields.

**Mitigation:**
- If C1 changes default `stall_timeout` from `0`, update `test_default_stall_timeout_zero` + `test_default_stall_action_warn` + the `0 == zero` assertions in `test_instrumentation.py:556-557,571-572`, plus 3 doc files (`sprint-cli-deep-dive.md`, `sprint-tui-reference.md`, `02-data-models.md`).
- If C1 adds new watchdog behavior without changing defaults, only `tests/sprint/test_watchdog.py` may need new cases.

---

## IP-2 — `SprintConfig.output_file()` / `error_file()`

**Target:** `src/superclaude/cli/sprint/models.py:469-473`

```python
def output_file(self, phase: Phase) -> Path:
    return self.results_dir / f"phase-{phase.number}-output.txt"
def error_file(self, phase: Phase) -> Path:
    return self.results_dir / f"phase-{phase.number}-errors.txt"
```

**Signature:** Single positional `phase: Phase`. NO existing caller passes a task identifier.

**Production callers:**
| File:Line | Use |
|---|---|
| `executor.py:1101-1102` | `_run_task_subprocess` (PER-TASK path — collision source) |
| `executor.py:1112` | Re-reads phase output for size telemetry (per-task path) |
| `executor.py:1311` | Per-phase fallback — `monitor.reset` target |
| `executor.py:1465-1469` | `_determine_phase_status` inputs (per-phase fallback) |
| `executor.py:1506` | error_file size telemetry (per-phase fallback) |
| `tmux.py:137` | First active phase tail pane bootstrap |
| `diagnostics.py:118,123,195` | Post-sprint diagnostic dump |
| `summarizer.py:495` | Aggregated phase report generation |

**Test callers (would break on signature change):**
- `tests/sprint/test_integration_lifecycle.py:74`
- `tests/sprint/test_watchdog.py:75,149,215`
- `tests/sprint/test_multi_phase.py:74,135`
- `tests/sprint/test_summarizer.py:360,408,584-585`
- `tests/sprint/test_integration_signal.py:89,214,303`
- `tests/sprint/test_backward_compat_regression.py:171,281,469`

Total: **~17 production + ~13 test call sites.**

**Blast Radius for FIX-C2 (output-file collision):**
- **HIGH** if signature changes to `output_file(phase, task=None)` — all callers must be updated/audited.
- **MEDIUM** if a new method `task_output_file(phase, task)` is added and only `_run_task_subprocess` at lines 1101-1102 + 1112 is migrated. Per-phase callers untouched.

**Mitigation (recommended):**
- Add `task_output_file(phase, task)` / `task_error_file(phase, task)` ALONGSIDE existing methods. Update only `_run_task_subprocess` (executor.py:1101-1102, 1112). No existing tests break; one new test verifying per-task file isolation.

---

## IP-3 — `_run_task_subprocess` (executor.py:1076)

**Target:** `src/superclaude/cli/sprint/executor.py:1076-1115`

**Caller chain:**
1. `execute_phase_tasks` at `executor.py:1008` — the ONLY caller (per-task subprocess factory default).
2. `execute_phase_tasks` is dispatched from `execute_sprint` at `executor.py:1266`, gated by `tasks = _parse_phase_tasks(phase, config)` at `executor.py:1261`.

**Gate logic:**
```python
# executor.py:1261-1265
tasks = _parse_phase_tasks(phase, config)
if tasks:
    # per-task path → execute_phase_tasks → _run_task_subprocess (one subprocess per task)
else:
    # per-phase fallback at line 1302+ → single ClaudeProcess(config, phase) (one subprocess per phase)
```

**Per-task vs per-phase gate:** `_parse_phase_tasks` returns a list if the phase file contains `### T<PP>.<TT>` task headings, else `None`. So *every* tasklist-style phase enters `execute_phase_tasks`.

**Collision scope:**
- The `output_file` collision exists ONLY in the per-task path (multiple tasks share `phase-N-output.txt` — each overwrites the previous via the same path).
- The per-phase fallback at line 1311 has a single subprocess per phase, no collision.

**Test fixtures using `_subprocess_factory` (bypass `_run_task_subprocess`):**
- `tests/sprint/test_execute_sprint_integration.py` — uses fakes.
- `tests/sprint/test_phase8_halt_fix.py` — uses fakes.
- `tests/sprint/test_anti_instinct_*.py` — uses fakes.

**Blast Radius for FIX-C2:** **LOW** — only one production caller; tests use `_subprocess_factory` and won't run the real path.

**Mitigation:** Update `_run_task_subprocess` to use `config.task_output_file(phase, task)` (new method). Existing factory-based tests unaffected.

---

## IP-4 — `write_phase_start` / `write_phase_complete` / `write_phase_interrupt`

**Target:** `src/superclaude/cli/sprint/logging_.py:59-87, 89-157`

**Call sites in executor.py:**
| File:Line | Method | Path |
|---|---|---|
| `executor.py:1256` | `write_phase_result(skip_result)` | SKIPPED early-exit |
| `executor.py:1297` | `write_phase_result(phase_result)` | **per-task path** completion |
| `executor.py:1328` | `write_phase_start(phase, started_at)` | **per-phase fallback only** |
| `executor.py:1442` | `write_phase_interrupt(...)` | per-phase fallback only |
| `executor.py:1564` | `write_phase_result(phase_result)` | per-phase fallback completion |

**MISSING — per-task path lacks `write_phase_start`.** The per-task block (1262-1300) only emits `tui.update` at 1265 and `write_phase_result` at 1297. There is no `write_phase_start` call before `execute_phase_tasks`.

**JSONL truncation check:** `_jsonl()` at `logging_.py:210-212` uses `open(..., "a")` (append). Grepped all of `src/`: **NO** `.write_text(`, `.unlink()`, or `"w"` mode write against `execution_log_jsonl`. Append-only — missing events truly never written, not overwritten.

**Verified live evidence:**
```
$ awk -F'"event":' '{print $2}' .dev/releases/current/task-builder-merge/execution-log.jsonl \
    | awk -F'"' '{print $2}' | sort | uniq -c
      4 phase_complete
      1 sprint_start
```
ZERO `phase_start`, ZERO `phase_interrupt` events. Confirmed missing.

**Exception handling check:** `write_phase_start` body (logging_.py:59-69) is a single `_jsonl()` call. No try/except. The `_jsonl` itself has no try/except either. So no silent swallowing — the call site simply doesn't exist on the per-task path.

**Tests pinning event fields:**
- `tests/sprint/test_regression_gaps.py:497-514` — `test_write_phase_start_fields` invokes `logger.write_phase_start` directly and reads the JSONL. Will continue to pass after C4 (we add a call site, not change the method).
- `tests/sprint/test_e2e_success.py:137` — comments document that `write_phase_start` is "called when each phase begins RUNNING" (currently false for tasklist phases).
- `tests/sprint/test_preflight.py:1061-1129` — `write_phase_result` validation (unrelated to start event).

**Blast Radius for FIX-C4:** **LOW** — single-line addition before `execute_phase_tasks` invocation at `executor.py:1265`. No signature change.

**Mitigation:** Add `logger.write_phase_start(phase, started_at)` between line 1263 (`started_at = ...`) and 1264 (`tui.update`). New regression test asserting `phase_start` event count == phase count.

---

## IP-5 — Watchdog (executor.py:1336-1417)

**Target poll loop:** `executor.py:1339` (start `while proc_manager._process.poll() is None`) → `executor.py:1417` (`time.sleep(0.5)`, loop end).

**State variables (defined IN loop scope — fresh per phase):**
- `_timed_out = False` at `executor.py:1336`
- `_stall_acted = False` at `executor.py:1337`
- `_poll_start = time.monotonic()` at `executor.py:1338`

**Reset semantics:**
- `_timed_out`: set `True` at line 1345 (deadline) or 1389 (kill). Never reset within the phase loop. Naturally reset at start of next phase iteration.
- `_stall_acted`: set `True` at 1372. **Reset to `False` at 1403-1404 when `ms.stall_seconds == 0.0`** — single-fire guard with auto-rearm.

**Per-task path:** `execute_phase_tasks` and `_run_task_subprocess` (executor.py:1086-1115) have NO equivalent poll loop or watchdog. They use `proc.start(); proc.wait()` at line 1109-1110 — blocking, no watchdog, no stall_timeout enforcement.

**Recent watchdog history (`git log --oneline | head -5`):**
```
edd3ddd docs(task-builder): D-0067 T05.16 MIG-005 evidence + FF governance entry
db6166e feat(task-builder): MIG-005 land FR-CONV.5 Retry Monotonicity + Regression Halts (M5)
0dcc947 test(task-builder): D-0066 T05.15 TEST-024 sequencing inversion fixture
c9e2b12 test(task-builder): D-0065 T05.14 TEST-017 + TEST-022 fixtures
20b58f6 test(task-builder): D-0064 T05.13 TEST-015 + TEST-016 monotonicity fixtures
```
Recent work is task-builder/anti-instinct, not watchdog. The watchdog block is stable.

**Tests pinning current watchdog behavior:**
- `tests/sprint/test_watchdog.py` — full coverage of "warn" / "kill" / single-fire / no-trigger-when-disabled (3 tests at lines 50, 125, 191).
- `tests/sprint/diagnostic/test_instrumentation.py:481-530` — simulates watchdog math via local variables (NOT the executor's loop).

**Blast Radius for FIX-C1 (stall_timeout default + watchdog):**
- **LOW** if the change is "add watchdog to per-task path" — copy lines 1365-1404 into `execute_phase_tasks`/`_run_task_subprocess`. No existing tests break.
- **MEDIUM** if default changes (already covered in IP-1).

**Mitigation:** New test verifying per-task path triggers watchdog on stalled task; reuse `tests/sprint/test_watchdog.py` patterns. Per-task watchdog must NOT use the blocking `proc.wait()` — needs a poll loop with `_process.poll() is None`.

---

## IP-6 — `--no-session-persistence` (DEFERRED for follow-up)

**Target:** `src/superclaude/cli/pipeline/process.py:84`

```python
cmd = ["claude", "--print", "--verbose", self.permission_flag,
       "--no-session-persistence", "--tools", "default", ...]
```

**Callers of `ClaudeProcess.build_command()` (production):**
- All sprint phases via `sprint/process.py:ClaudeProcess.__init__` → `pipeline/process.py:ClaudeProcess.__init__`.
- All sprint per-task subprocesses via `executor.py:1093-1110` (`_run_task_subprocess`).
- `cli_portify/executor.py` (pipeline runner).
- `prd/executor.py` (PRD runner).

**Tests pinning the flag's presence:**
- `tests/sprint/test_process.py:48` — `assert "--no-session-persistence" in cmd`.
- `tests/pipeline/test_process.py:44,140` — same assertions in pipeline tests.

**Docs referencing the flag:**
- `docs/guides/cli-portify-and-pipeline-runner-guide.md:196,206`
- `docs/guides/sprint-cli-tools-release-guide.md:231,239`
- `docs/guides/roadmap-cli-tools-release-guide.md:641,650`

**Session warmup / daemon infrastructure:**
- `grep -rn "warmup\|daemon\|session.*pool" src/` returns nothing relevant. **NO existing session warmup infrastructure.**
- The flag is currently hard-coded — no opt-out exists. Removing it would change the contract for every sprint/pipeline/portify run.

**Blast Radius for C5 removal:** **HIGH** — 3 tests + 3 doc files + behavior change across **all four** CLI pipelines (sprint, pipeline-runner, cli-portify, prd).

**Mitigation:** Defer (already C5). When tackling: introduce an opt-out flag `--allow-session-persistence` defaulting to False, leave existing tests intact, then build warmup separately.

---

## IP-7 — Remediation path (`SprintGatePolicy.build_remediation_step` at executor.py:66-87)

**Target:** `src/superclaude/cli/sprint/executor.py:66-87`

**Containing class:** `SprintGatePolicy` (executor.py:56-98). Implements the `TrailingGatePolicy` protocol from `pipeline/trailing_gate.py:250-254`.

**Instantiation sites:**
- `executor.py:1216` — `SprintGatePolicy(config)` — **constructed but NOT bound to a variable**. Comment at lines 1212-1215 explicitly states "intentionally not bound to a local — its construction is captured by tests via SprintGatePolicy.__init__ patching".
- `tests/pipeline/test_trailing_gate.py:556-610` — 4 tests construct and invoke `policy.build_remediation_step(...)` directly.
- `tests/sprint/test_execute_sprint_integration.py:4` — patches `SprintGatePolicy.__init__` to verify the construction wiring.

**Production invocations of `.build_remediation_step(...)`:**
- **NONE.** Grep across `src/` returns zero call sites. Only `evaluate(...)` is invoked in production (`cli_portify/executor.py:592` uses its own gate policy, not `SprintGatePolicy`).

**Status:** **Dead code in active sprints.** The class is wired only as a protocol satisfier and a test hook. The remediation flow it implements (gate failure → focused remediation step) is never executed by `execute_sprint`.

**Timeout formula:** Line 86 uses `self._config.max_turns * 60` — half of the per-phase formula at 1106/process.py:115 (`max_turns * 120`). If revived, this inconsistency must be reconciled.

**Blast Radius for FIX-C3 (timeout reconciliation):**
- **LOW** for changing line 86 because no production caller. 4 unit tests in `test_trailing_gate.py` may need their `timeout_seconds` expectation updated.
- **HIGH** if we instead choose to make line 86 the canonical formula and propagate (would touch process.py:115 and executor.py:1106).

**Mitigation:** Per the track plan, line 86 (`* 60`) should be updated to match the active sprint path (`* 120 + 300`) for consistency, even though dead. Touches 1 line in src + may need 1 assertion update in `test_trailing_gate.py:578`-ish region.

---

## IP-8 — Timeout formulas across CLI subsystems

**`max_turns * 120` (sprint canonical):**
- `src/superclaude/cli/sprint/process.py:115` — `timeout_seconds=config.max_turns * 120 + 300` (per-phase ClaudeProcess).
- `src/superclaude/cli/sprint/executor.py:1106` — `timeout_seconds=config.max_turns * 120 + 300` (per-task `_run_task_subprocess`).

**`max_turns * 60` (sprint outlier — dead):**
- `src/superclaude/cli/sprint/executor.py:86` — `SprintGatePolicy.build_remediation_step` (dead code, see IP-7).

**Other CLI subsystems (NOT touched by sprint fixes):**
- `prd/executor.py:499` — `timeout_seconds=self._config.stall_timeout * 30` (DIFFERENT formula entirely — derives from stall_timeout, not max_turns).
- `cli_portify` and `cleanup_audit` — no equivalent `max_turns * N` formula in their executors.
- `roadmap` — no comparable timeout.

**Blast Radius:** **LOW** — only 3 sites in sprint; reconciliation touches at most 1 (the outlier at executor.py:86). No cross-pipeline contamination.

**Mitigation:** Align line 86 to `* 120 + 300`. Or, conversely, document the `* 60` as remediation-specific (smaller subprocess scope) — but since the code is dead, the consistent-default choice is safer.

---

## Cross-Cutting Summary

| Fix | Touchpoint(s) | Blast Radius | Key Mitigation |
|---|---|---|---|
| **C1** stall_timeout + watchdog on per-task path | executor.py:1336-1417, _run_task_subprocess | LOW (new code) / MEDIUM (if default changes) | Add poll loop to per-task; do NOT change default unless tests + docs updated |
| **C2** output-file collision (per-task) | executor.py:1101-1102, 1112; models.py:469-473 | MEDIUM | Add `task_output_file(phase, task)`; do NOT change existing signature |
| **C3** timeout reconciliation | executor.py:86 | LOW (dead code) | Update line 86 only; check 4 trailing-gate unit tests |
| **C4** phase_start JSONL | executor.py:~1264 (per-task block) | LOW | One-line insertion of `logger.write_phase_start(phase, started_at)` |
| **C5** (deferred) --no-session-persistence | pipeline/process.py:84 | HIGH | Defer until warmup infrastructure exists |
| **C6** (deferred) fan-out | execute_phase_tasks loop | HIGH | Defer |

**Test files most exposed:**
1. `tests/sprint/test_watchdog.py` — primary watchdog regression coverage.
2. `tests/sprint/diagnostic/test_instrumentation.py` — 8 forwarding tests anchored on defaults `0`/`"warn"`.
3. `tests/sprint/diagnostic/test_debug_logger.py` — 4 default assertions.
4. `tests/sprint/test_regression_gaps.py:492-514` — `write_phase_start` event field validation (will PASS after C4 fix, no change needed).
5. `tests/pipeline/test_trailing_gate.py:556-610` — `SprintGatePolicy` direct tests (1 may need update for C3).

**Docs most exposed (if defaults change):**
- `docs/sprint-cli-deep-dive.md:131-132`
- `docs/developer-guide/sprint-tui-reference.md:541-542`
- `docs/generated/sprint-cli/02-data-models.md:249`
