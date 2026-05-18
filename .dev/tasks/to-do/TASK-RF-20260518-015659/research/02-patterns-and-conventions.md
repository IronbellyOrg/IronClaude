# Research 02 — Patterns & Conventions

- **Topic type:** Patterns & Conventions (idioms the new code must follow to look native)
- **Scope:** `src/superclaude/cli/sprint/` and `src/superclaude/cli/pipeline/`
- **Status:** Complete
- **Date:** 2026-05-18
- **Track goal:** Land 4 deterministic sprint-runner fixes (stall_timeout default + watchdog split; output-file collision; timeout reconciliation; phase_start JSONL emission).

---

## 1. Dataclass field defaults — `SprintConfig` structure

`SprintConfig` lives at `src/superclaude/cli/sprint/models.py:347-477` and **inherits from `PipelineConfig`**. The dataclass uses:
- Simple typed fields with literal defaults: `start_phase: int = 1` (`models.py:360`), `model: str = ""` (`models.py:363`), `permission_flag: str = "--dangerously-skip-permissions"` (`models.py:365`).
- Mutable defaults use `field(default_factory=...)`: `index_path: Path = field(default_factory=lambda: Path("."))` (`models.py:357`), `phases: list[Phase] = field(default_factory=list)` (`models.py:359`).
- `Literal[...]` for constrained string fields: `wiring_gate_mode: Literal["off", "shadow", "soft", "full"] = "soft"` (`models.py:376`), `checkpoint_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"` (`models.py:391`).

**Example 1 — diagnostic flag pattern (existing precedent for new flags):**
```python
# models.py:368-371 — pre-existing block where new diagnostic fields would fit
debug: bool = False
stall_timeout: int = 0  # 0 = disabled
stall_action: str = "warn"  # "warn" or "kill"
phase_timeout: int = 0  # 0 = disabled
```
A trailing inline `#` comment names the sentinel value (`0 = disabled`) — new fields should follow.

**Example 2 — Literal-typed mode field with comment block above:**
```python
# models.py:389-391
# Checkpoint enforcement gate mode (v3.7, Wave 2)
# off=disabled, shadow=log JSONL only, soft=log + stdout warning,
# full=log + downgrade PASS to PASS_MISSING_CHECKPOINT on missing files
checkpoint_gate_mode: Literal["off", "shadow", "soft", "full"] = "shadow"
```

**Backward-compat migration shim** lives in `__post_init__` (`models.py:398-444`). The pattern: a `_old_to_new` dict + `warnings.warn(..., DeprecationWarning, stacklevel=2)` + `object.__setattr__(self, new_name, old_val)` (`models.py:421-436`). New default changes that need a non-default-aware shim should land here.

**Wiring through to caller signature:** `load_sprint_config` (`config.py:275-287`) accepts the new field as a keyword arg with the same default, then passes it into the `SprintConfig(...)` constructor at `config.py:332-349`. The CLI `run` command in `commands.py:185-216` is the third place that names the field (Click option + pass-through). **Adding/changing a field requires touching all three sites in sync.**

---

## 2. Subprocess Popen + file-handle pattern

The canonical subprocess lifecycle lives in **`src/superclaude/cli/pipeline/process.py`** (the sprint base class).

**Open mode is unconditional `"w"` (write/truncate):**
```python
# pipeline/process.py:118-123
if self.tool_write_mode:
    self._stdout_fh = open(self.output_file.with_suffix(".log"), "w")
else:
    self._stdout_fh = open(self.output_file, "w")
self._stderr_fh = open(self.error_file, "w")
```
No `encoding=` kwarg on these two `open()` calls — they rely on locale default. Compare to the *debug* logger which is explicit: `_FlushHandler(str(log_path), mode="w", encoding="utf-8")` at `debug_logger.py:93,106`.

**Popen kwargs assembled in a dict, then `**` splatted:**
```python
# pipeline/process.py:125-134
popen_kwargs = {
    "stdin": subprocess.PIPE,
    "stdout": self._stdout_fh,
    "stderr": self._stderr_fh,
    "env": self.build_env(env_vars=self._extra_env_vars),
}
if hasattr(os, "setpgrp"):
    popen_kwargs["preexec_fn"] = os.setpgrp

self._process = subprocess.Popen(self.build_command(), **popen_kwargs)
```

**File handles stored on the instance** (`self._stdout_fh`, `self._stderr_fh`; `process.py:69-71`) and **closed in `_close_handles()` with broad except**:
```python
# pipeline/process.py:238-244
def _close_handles(self) -> None:
    for fh in (self._stdout_fh, self._stderr_fh):
        if fh is not None:
            try:
                fh.close()
            except Exception:
                pass
```

**Output-file path is computed by `SprintConfig.output_file(phase)` / `.error_file(phase)`** (`models.py:469-473`):
```python
def output_file(self, phase: Phase) -> Path:
    return self.results_dir / f"phase-{phase.number}-output.txt"
def error_file(self, phase: Phase) -> Path:
    return self.results_dir / f"phase-{phase.number}-errors.txt"
```
Phase-number-keyed only — no resume-attempt suffix today. Output-file-collision fix will need to either change these helpers or rename via the caller before `ClaudeProcess.start()` reaches `open(...,"w")`.

**Parent dir auto-created via mkdir:** `self.output_file.parent.mkdir(parents=True, exist_ok=True)` (`process.py:116`). Follow this `parents=True, exist_ok=True` form everywhere — also used in `logging_.py:26` (`config.results_dir.mkdir(parents=True, exist_ok=True)`) and `debug_logger.py:91`.

---

## 3. datetime / timezone usage

**Single canonical form across sprint/:** `datetime.now(timezone.utc)`. Imported as `from datetime import datetime, timezone` (`logging_.py:6`, `models.py:13`, `executor.py:1325`, `debug_logger.py:19`).

Variants observed (all in sprint/):
- **Wall-clock for log timestamps and dataclass `started_at`/`finished_at`:** `datetime.now(timezone.utc)` — `executor.py:972, 984, 1012, 1247, 1263, 1284, 1325, 1427, 1615, 1884`; `models.py:170, 171, 500, 501, 532, 538`; `logging_.py:186`.
- **Serialization is always `.isoformat()`** when writing JSONL — `logging_.py:34, 48, 49, 64, 80-85, 100-101, 186`.
- **No naive `datetime.utcnow()` anywhere in sprint/** — all timestamps carry tz.
- **Conversion from `time.time()` epoch to dt:** `datetime.fromtimestamp(record.created, tz=timezone.utc)` (`debug_logger.py:56`). Logging-record timestamps are the only place epoch→dt conversion happens.

**Duration:** `(finished_at - started_at).total_seconds()` (`models.py:179, 515, 539`; `executor.py:1428`; `logging_.py:84`). Never subtract `time.monotonic()` deltas and report as duration in dataclass fields — those use wall-clock dt.

---

## 4. `time.monotonic` vs `time.time`

**Rule observed across sprint/executor.py:** `time.monotonic()` is used **for any deadline/elapsed comparison**; `time.time()` is essentially absent from the sprint code path.

The explicit comment at the watchdog block sets the convention:
```python
# executor.py:1326-1327
# Use monotonic clock for deadline enforcement to be immune to NTP adjustments
deadline = time.monotonic() + proc_manager.timeout_seconds
```

**`time.monotonic()` call sites in sprint/:**
- `executor.py:840, 847` — gate evaluation latency (imported locally as `_time`).
- `executor.py:997, 1069` — TUI state `last_event_time` updates.
- `executor.py:1327, 1338, 1343, 1350` — poll-loop deadline and elapsed.
- `models.py:607-609` — `MonitorState.last_growth_time`, `last_event_time`, `phase_started_at` all `field(default_factory=time.monotonic)`.
- `models.py:636` — `MonitorState.stall_status` uses `time.monotonic()` as `now`.

**`time.time()`:** appears in sprint/ only as `.timestamp()` conversions of an existing `datetime` object (e.g. `executor.py:1453, 1468 — started_at.timestamp()`), never as a fresh `time.time()` call for measuring elapsed.

**New code rule:** any deadline/elapsed/stall-window comparison must use `time.monotonic()`; any timestamp written to JSONL or stored on a dataclass field must use `datetime.now(timezone.utc)`. Never mix the two clocks in a single comparison.

---

## 5. JSONL event-emission pattern — `_jsonl()`

The sink is `SprintLogger._jsonl()` (`logging_.py:210-212`):
```python
def _jsonl(self, data: dict):
    with open(self.config.execution_log_jsonl, "a") as f:
        f.write(json.dumps(data, default=str) + "\n")
```
- Open mode **`"a"` (append)**, no `encoding=`.
- `default=str` so `Path` / `datetime` fall through to `str(...)` rather than raising.

**Every existing event passes a single dict literal with `"event"` as the first key**, followed by event-specific fields (`logging_.py`):

| Event | Line | Fields (in literal order) |
|---|---|---|
| `sprint_start` | 31-41 | `event, timestamp, index, phases, max_turns, model` |
| `phase_start` | 61-69 | `event, phase, phase_name, phase_file, timestamp` |
| `phase_interrupt` | 77-87 | `event, phase, phase_name, started_at, interrupted_at, duration_seconds, exit_code` |
| `phase_complete` | 92-107 | `event, phase, phase_name, status, exit_code, started_at, finished_at, duration_seconds, output_bytes, error_bytes, last_task_id, files_changed` |
| `checkpoint_verification` | 179-188 | `event, phase, expected, found, missing, timestamp` |
| `sprint_complete` | 192-201 | `event, outcome, duration_seconds, phases_passed, phases_failed, halt_phase` |

**Field naming conventions:**
- Event name is **`snake_case`** verb-or-noun phrase.
- `phase` (int) precedes `phase_name` (str). When a path is also included it's `phase_file` (str of full path).
- Timestamps emitted as **ISO 8601 strings** via `.isoformat()`. Naming is split: a single "start" event uses `"timestamp"`, paired open/close events use `"started_at"` + `"finished_at"` (or `"interrupted_at"`).
- Durations are **`duration_seconds`** as float.
- Byte counters: `output_bytes`, `error_bytes`.
- Exit code is **`exit_code`**.
- Lists are written as `list(seq)` literally (`logging_.py:183-185`) so generators get materialized.

**Method naming:** the `write_*` helper that emits the event is named for the event semantic (`write_phase_start`, `write_phase_interrupt`, `write_phase_result`, `write_checkpoint_verification`). It accepts the domain objects (phase, datetimes, ints) and constructs the dict inline — **callers do not construct the dict**.

**Fix-track relevance:** the new `phase_start` emission point already exists at `logging_.py:59-69` and is wired through `executor.py:1328` (`logger.write_phase_start(phase, started_at)`). If the fix is that `phase_start` is not consistently emitted in some path, audit the per-phase loop branches in `executor.py` around lines 1247-1330 (per-task branch ends at 1300 with `continue`; the per-phase branch starts at 1302) — only the per-phase branch currently calls `write_phase_start`.

---

## 6. Debug-logging pattern — `debug_log(_dbg, ...)`

**Logger acquisition** is a module-level `_dbg = logging.getLogger("superclaude.sprint.debug.<module>")` (e.g. `executor.py` uses `_dbg`; `process.py:27` uses `_dbg = logging.getLogger("superclaude.sprint.debug.process")`).

**`debug_log()` signature** (`debug_logger.py:117-138`):
```python
debug_log(logger, event, **kwargs)
```
- `event` is a **snake_case** string OR a **MACRO_CASE** lifecycle marker (`PHASE_BEGIN`, `PHASE_END`).
- kwargs are sorted alphabetically by key when rendered to the log line (`debug_logger.py:135`).
- Short-circuit guard: `if not logger.isEnabledFor(logging.DEBUG): return` — zero overhead when debug is off (`debug_logger.py:131-132`).

**Three examples around the watchdog block (executor.py:1330-1435):**

```python
# executor.py:1330 — phase lifecycle marker (MACRO_CASE)
debug_log(_dbg, "PHASE_BEGIN", phase=phase.number, file=str(phase.file))

# executor.py:1352-1363 — per-tick monitoring (snake_case event, many kwargs)
debug_log(
    _dbg,
    "poll_tick",
    phase=phase.number,
    pid=proc_manager._process.pid,
    poll_result="running",
    elapsed=round(_elapsed, 1),
    output_bytes=ms.output_bytes,
    growth_rate=round(ms.growth_rate_bps, 1),
    stall_seconds=round(ms.stall_seconds, 1),
    stall_status=ms.stall_status,
)

# executor.py:1373-1380 — branch event inside the watchdog
debug_log(
    _dbg,
    "watchdog_triggered",
    phase=phase.number,
    action=config.stall_action,
    stall_seconds=round(ms.stall_seconds, 1),
    pid=proc_manager._process.pid,
)
```

**Conventions to copy in new debug_log calls:**
- Multi-arg calls use vertical formatting (one kwarg per line) — see `executor.py:1352-1363`. Single-arg or short calls stay one-line (`executor.py:1330`).
- Floats are **`round(value, 1)`** before logging (so the log line stays narrow).
- Identifiers always passed by name: `phase=phase.number`, `pid=proc_manager._process.pid`.
- Counters are bare ints, not pre-formatted strings.
- Path values are coerced with `str(path)` (e.g. `file=str(phase.file)`).
- The dict-style log line `event k1=v1 k2=v2 ...` does **not** carry timestamps — the formatter adds those (`debug_logger.py:54-66`).

**Lifecycle markers (MACRO_CASE) reserved for boundaries** — `PHASE_BEGIN` (`executor.py:1330`), `PHASE_END` (`executor.py:1431`). Per-tick or branch events use `snake_case`.

---

## 7. Poll-loop / sleep pattern

**Only two `time.sleep` call sites exist across sprint/ + pipeline/:**
- `executor.py:1417` — `time.sleep(0.5)` at the bottom of the per-phase poll loop, comment two lines above: `# Update TUI at ~2 Hz (monitor thread handles data extraction)` (`executor.py:1406`).
- `tmux.py:300` — `time.sleep(10)` (tmux session settle).

**There is no module-level `POLL_INTERVAL_S` or similar constant** — the value is a magic literal inline at `executor.py:1417`. The comment at `executor.py:1406` is the only documentation of the rate. If the fix needs to expose or split the poll rate (e.g. for the watchdog), introducing a named module-level constant near the top of `executor.py` would be a small refactor — but the existing code intentionally uses the bare literal, so matching that style (and just leaving a comment) is also native.

**Poll-loop structure** (`executor.py:1336-1417`):
1. `_timed_out = False; _stall_acted = False; _poll_start = time.monotonic()` — boolean flags + monotonic anchor before the loop.
2. `while proc_manager._process.poll() is None:` — Popen.poll() drives the loop.
3. Shutdown check → break.
4. Deadline check (`time.monotonic() > deadline`) → set `_timed_out = True`, terminate, break.
5. Read `monitor.state` once into `ms`, compute `_elapsed`.
6. `debug_log("poll_tick", ...)`.
7. Watchdog block (currently *inside* the loop body, lines 1366-1404).
8. TUI update inside `try/except` so display glitches do not abort sprint (`executor.py:1408-1416`).
9. `time.sleep(0.5)` at end of iteration.

**Single-fire guards** use the pattern `if condition and not _flag: _flag = True; ...; if recovery: _flag = False` — see `_stall_acted` at `executor.py:1337, 1370, 1372, 1402-1404`. New watchdog guards should follow.

---

## 8. Stderr printing convention

**Sprint/ does not use a dedicated logger for human-facing stderr in the executor poll loop — it uses `print(..., file=sys.stderr)`.** Three call sites all live in the watchdog/TUI block at `executor.py:1382-1416`:

```python
# executor.py:1381-1388 (kill branch)
if config.stall_action == "kill":
    import sys

    print(
        f"[WATCHDOG] Stall detected ({ms.stall_seconds:.0f}s > "
        f"{config.stall_timeout}s) — killing phase {phase.number}",
        file=sys.stderr,
    )
```

```python
# executor.py:1392-1400 (warn branch)
else:
    # warn action: log and continue
    import sys

    print(
        f"[WATCHDOG] Stall detected ({ms.stall_seconds:.0f}s > "
        f"{config.stall_timeout}s) — warning for phase {phase.number}",
        file=sys.stderr,
    )
```

```python
# executor.py:1410-1416 (TUI display-error swallow)
except Exception as _tui_exc:
    import sys

    print(
        f"[TUI] Display error (continuing sprint): {_tui_exc}",
        file=sys.stderr,
    )
```

**Conventions:**
- Bracketed prefix tag: `[WATCHDOG]`, `[TUI]` — **uppercase, square-bracketed, terse subsystem name.**
- **`import sys` is local inside the branch**, not at module top (presumably to keep `sys` out of the global namespace given how rarely the code paths fire). New stderr prints in the same vicinity should follow.
- Numeric formatting uses inline `:.0f` (`stall_seconds:.0f`); no rounding helper.
- An alternate convention for human stderr exists elsewhere in the codebase: `click.echo(msg, err=True)` (used in `config.py:316`, `commands.py`). The poll-loop intentionally uses `print()` instead because Click context may not be active in every spawn path — match `print(..., file=sys.stderr)` for anything that fires inside the executor poll loop.
- The Rich-styled `SprintLogger._screen_warn` / `_screen_error` (`logging_.py:217-221`) emit to a `Console(stderr=True)` but are reserved for **phase-level result reporting**, not for the per-tick watchdog. Do not call `logger._screen_warn(...)` from inside the poll loop.

---

## 9. CLAUDE.md project rules that apply

From **`/config/workspace/IronClaude/CLAUDE.md`** (project root) — load-bearing rules for new code:

1. **UV-only Python ops** — `uv run pytest`, `uv pip install`. Never `python -m pytest` or `pip install`. Applies to the test commands you'd put in the task's verification section. Reference: CLAUDE.md "🐍 Python Environment Rules".
2. **`make sync-dev` → `make verify-sync`** — code lives in `src/superclaude/`; any sibling copy under `.claude/` is a generated mirror. The 4-fix track only touches `src/superclaude/cli/sprint/*` so no sync step is required for those edits, but if the task also edits `.claude/skills/`, `.claude/commands/`, or `.claude/agents/`, run `make sync-dev` then `make verify-sync` before commit. Reference: CLAUDE.md "🔄 Component Sync".
3. **Slash-command skill invocation** — irrelevant to this code track (no `/sc:<command>` is being added).
4. **Plugin override — `.dev/eval-workspaces/<skill-name>/`** — irrelevant to this code track.
5. **Tests use markers** — `@pytest.mark.unit`, `@pytest.mark.integration` (auto-applied by path), `@pytest.mark.confidence_check`, etc. New tests for sprint fixes will be picked up by pytest auto-discovery (`pyproject.toml:99-103`: `testpaths=["tests"]`, `python_files=["test_*.py"]`, `python_classes=["Test*"]`, `python_functions=["test_*"]`).
6. **Token budget by complexity** — informational only; not a hard rule for code style.
7. **Confidence-first** — protocol rule for the *builder*, not for the code itself.

From **`/config/workspace/IronClaude/.claude/skills/task-builder/SKILL.md`** (this skill's spec — checked the path exists in the standard skill location): not re-read here as it is the parent harness; the SKILL has already injected this researcher's scope. No additional code-style rules to surface from it.

**No additional rules** in `KNOWLEDGE.md`, `PLANNING.md`, or `RULES.md` were sampled — Researcher 1's inventory covers structural files; Researcher 4 covers the MDTM template. This researcher's responsibility ends at the conventions enumerated above.

---

## 10. Lint / format rules

From **`/config/workspace/IronClaude/pyproject.toml`**:

- **No standalone `ruff.toml` or `.ruff.toml` at the repo root** — ruff config is fully inline in `pyproject.toml`.
- **`[tool.ruff]`** (`pyproject.toml:175-181`): `line-length = 88`, `target-version = "py310"`, `exclude = ["docs/"]`, plus `tests/audit/fixtures/syntax_error.py` extend-excluded.
- **`[tool.ruff.lint]`** (`pyproject.toml:183-185`): `select = ["E", "F", "I", "N", "W"]` (pycodestyle errors+warnings, pyflakes, isort, pep8-naming), `ignore = ["E501"]` (line-too-long delegated to black).
- **`[tool.black]`** (`pyproject.toml:158-173`): `line-length = 88`, `target-version = ["py310", "py311", "py312"]`.
- **`[tool.mypy]`** (`pyproject.toml:187-195`): `python_version = "3.10"`, `disallow_untyped_defs = false` (gradual typing), `check_untyped_defs = true`, `no_implicit_optional = true`.

**Rules new code must follow:**
- **88-char line limit** (ruff's E501 is ignored but black enforces; existing wraps in `executor.py:1382-1388` use trailing-comma-on-own-line and string concatenation across lines — match that idiom).
- **Import order** (ruff "I"): stdlib → third-party → local (`from .models import ...` last). See `executor.py` top, `logging_.py:1-10`, `process.py:11-25`.
- **PEP8 naming** (ruff "N"): `snake_case` functions, `CapWords` classes, `_underscore_private`. Lifecycle markers `PHASE_BEGIN`/`PHASE_END` are debug-log *event strings*, not Python identifiers — they don't trip ruff.
- **`from __future__ import annotations`** is at the top of every module in sprint/ and pipeline/ (`config.py:3`, `models.py:8`, `process.py:12`, `logging_.py:3`, `debug_logger.py:16`). Required for new modules and idiomatic for edits.
- **Type hints:** modern syntax (`list[Phase]`, `dict[str, str]`, `int | None`) — see `models.py:380`, `process.py:51`. Pre-3.10 `Optional[...]` and `Tuple[...]` are NOT in use except where `from typing import Optional` is explicitly imported (`process.py:19`, `models.py:15`). New code should prefer PEP 604 `X | None` where possible.
- **Logger names:** dotted hierarchy under `superclaude.sprint.*` or `superclaude.pipeline.*` — see `config.py:13` (`superclaude.sprint.config`), `process.py:27` (`superclaude.sprint.debug.process`), `logging_.py` (the Console is named separately; module logger is omitted there).

**No coverage gate or required minimum** in `[tool.coverage.report]` (`pyproject.toml:144-156`); `show_missing = true` is the only display config.

---

## Summary

The new code for the 4 deterministic sprint-runner fixes should look native by matching these idioms:

- **Config:** add fields to `SprintConfig` (`models.py`) with literal defaults + inline `#` comment for sentinels; wire the field through `load_sprint_config` in `config.py:275-349` and the Click signature in `commands.py:185-216`; backward-compat-incompatible defaults use the migration shim in `SprintConfig.__post_init__`.
- **Subprocess:** all stdout/stderr open with mode `"w"` (no encoding kwarg); parents auto-created via `parents=True, exist_ok=True`; output paths come from `config.output_file(phase)` / `config.error_file(phase)` — change here if the collision fix renames per-attempt.
- **Time:** `time.monotonic()` for any elapsed/deadline (anchor comment at `executor.py:1326-1327`); `datetime.now(timezone.utc)` for any value stored on a dataclass or written to JSONL; never mix the two clocks.
- **JSONL:** dict literal with `"event": "<snake_case>"` first key, ISO timestamps via `.isoformat()`, append-mode write via `SprintLogger._jsonl()`; add a `write_<event_name>` method on `SprintLogger` rather than constructing the dict at the call site.
- **Debug logs:** `debug_log(_dbg, "event_name", **kwargs)` with floats `round(v, 1)`, multi-arg calls vertical, `PHASE_BEGIN`/`PHASE_END` only for true lifecycle boundaries.
- **Poll loop:** mirror the watchdog single-fire-guard pattern (`_acted` boolean reset when condition clears); `time.sleep(0.5)` cadence; wrap any display update in `try/except` and stderr-print on failure.
- **Stderr:** `print(f"[SUBSYSTEM] ...", file=sys.stderr)` with local `import sys`; bracketed uppercase subsystem prefix; do NOT route through `logger._screen_warn` from inside the poll loop.
- **Style:** 88-char wrap, `from __future__ import annotations`, modern `X | None` hints, ruff E+F+I+N+W with E501 ignored.

**File path of this research artifact:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RF-20260518-015659/research/02-patterns-and-conventions.md`
