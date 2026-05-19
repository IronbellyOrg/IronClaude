# Research: Patterns & Conventions — SprintConfig Construction

**Track**: 1 of 3
**Researcher**: 02-config-pattern
**Topic**: SprintConfig construction; where `release_dir` is set; where/how to introduce `state_dir` for `.sprint-exitcode`
**Status**: Complete
**Date**: 2026-05-18

## Scope

- `src/superclaude/cli/sprint/config.py` (full)
- `src/superclaude/cli/sprint/models.py` (full)
- `src/superclaude/cli/sprint/__init__.py`
- `src/superclaude/cli/sprint/commands.py` (SprintConfig instantiation sites)

## Track Hypothesis Context

`.sprint-exitcode` is currently written to `config.release_dir`
(`src/superclaude/cli/sprint/executor.py:1754`) and read back by the tmux
caller (`src/superclaude/cli/sprint/tmux.py:166`). The repo `.gitignore`
only excludes it at the **repo root** (`/.sprint-exitcode`,
`.gitignore:222`). Because `release_dir` typically resolves to a tracked
path like `.dev/releases/current/<release>/`, every sprint run causes a
transient file to appear inside a tracked directory. The hypothesis is
to migrate this write to a non-tracked transient `state_dir` defaulting
to `.dev/sprint-state/<tasklist-id>/`.

---

## 1. SprintConfig dataclass/class definition

Defined at `src/superclaude/cli/sprint/models.py:348-397`. It is a
`@dataclass` that inherits from
`superclaude.cli.pipeline.models.PipelineConfig`
(`src/superclaude/cli/pipeline/models.py:179-189`) which contributes
these inherited fields:

| Inherited field      | Type   | Default                              | Source                                  |
|----------------------|--------|--------------------------------------|-----------------------------------------|
| `work_dir`           | `Path` | `Path(".")`                          | `pipeline/models.py:183`                |
| `dry_run`            | `bool` | `False`                              | `pipeline/models.py:184`                |
| `max_turns`          | `int`  | `100`                                | `pipeline/models.py:185`                |
| `model`              | `str`  | `""`                                 | `pipeline/models.py:186`                |
| `permission_flag`    | `str`  | `"--dangerously-skip-permissions"`   | `pipeline/models.py:187`                |
| `debug`              | `bool` | `False`                              | `pipeline/models.py:188`                |
| `grace_period`       | `int`  | `0`                                  | `pipeline/models.py:189`                |

`SprintConfig` itself adds (file:line refers to `models.py`):

| Field                          | Type                                    | Default                                       | Line | Notes                                                                                |
|--------------------------------|-----------------------------------------|-----------------------------------------------|------|--------------------------------------------------------------------------------------|
| `index_path`                   | `Path`                                  | `Path(".")`                                   | 358  | tasklist-index.md path.                                                              |
| `release_dir`                  | `Path`                                  | `Path(".")`                                   | 359  | Mirrored into `work_dir` by `__post_init__` (line 404).                              |
| `phases`                       | `list[Phase]`                           | `[]`                                          | 360  | Discovered phases.                                                                   |
| `start_phase`                  | `int`                                   | `1`                                           | 361  |                                                                                      |
| `end_phase`                    | `int`                                   | `0`                                           | 362  | `0` = auto-detect.                                                                   |
| `max_turns`                    | `int`                                   | `100`                                         | 363  | Re-declared on subclass.                                                             |
| `model`                        | `str`                                   | `""`                                          | 364  | Re-declared.                                                                         |
| `dry_run`                      | `bool`                                  | `False`                                       | 365  | Re-declared.                                                                         |
| `permission_flag`              | `str`                                   | `"--dangerously-skip-permissions"`            | 366  | Re-declared.                                                                         |
| `tmux_session_name`            | `str`                                   | `""`                                          | 367  | Threaded back by `launch_in_tmux`.                                                   |
| `debug`                        | `bool`                                  | `False`                                       | 369  | Re-declared.                                                                         |
| `stall_timeout`                | `int`                                   | `0`                                           | 370  | `0` = disabled.                                                                      |
| `stall_action`                 | `str`                                   | `"warn"`                                      | 371  | `"warn"` or `"kill"`.                                                                |
| `phase_timeout`                | `int`                                   | `0`                                           | 372  |                                                                                      |
| `shadow_gates`                 | `bool`                                  | `False`                                       | 374  |                                                                                      |
| `wiring_gate_mode`             | `Literal["off","shadow","soft","full"]` | `"soft"`                                      | 377  | Derived from `wiring_gate_enabled`/`grace_period` in `__post_init__` (lines 442-445).|
| `gate_rollout_mode`            | `Literal["off","shadow","soft","full"]` | `"off"`                                       | 381  |                                                                                      |
| `wiring_gate_scope`            | `str`                                   | `"task"`                                      | 383  |                                                                                      |
| `wiring_analysis_turns`        | `int`                                   | `1`                                           | 384  |                                                                                      |
| `remediation_cost`             | `int`                                   | `2`                                           | 385  |                                                                                      |
| `wiring_gate_enabled`          | `bool`                                  | `True`                                        | 387  |                                                                                      |
| `wiring_gate_grace_period`     | `int`                                   | `0`                                           | 388  |                                                                                      |
| `checkpoint_gate_mode`         | `Literal["off","shadow","soft","full"]` | `"shadow"`                                    | 392  |                                                                                      |
| `total_tasks`                  | `int`                                   | `0`                                           | 397  | Pre-scanned at load time; `0` is valid fallback.                                     |

Computed properties (file:line, all in `models.py`):
- `debug_log_path` (448-450): `self.results_dir / "debug.log"`
- `results_dir` (452-454): `self.release_dir / "results"`
- `execution_log_jsonl` (456-458): `self.release_dir / "execution-log.jsonl"`
- `execution_log_md` (460-462): `self.release_dir / "execution-log.md"`
- `active_phases` (464-468): phases in `[start_phase, end_phase]`.
- `output_file(phase)` / `error_file(phase)` / `result_file(phase)` (470-477): files under `results_dir`.

All current path-derived properties hang off `release_dir`. **No
existing field can serve as `state_dir`**; a new field is required.

### `__post_init__` behaviour (`models.py:399-445`)

- Line 404: `object.__setattr__(self, "work_dir", self.release_dir)` —
  ensures `PipelineConfig.work_dir` always mirrors `release_dir` so both
  access paths agree.
- Lines 422-437: backward-compat migration shim for renamed fields
  (`wiring_budget_turns` -> `wiring_analysis_turns`, etc.). Emits
  `DeprecationWarning`.
- Lines 442-445: derives `wiring_gate_mode` from
  `wiring_gate_enabled` / `wiring_gate_grace_period`.

A new `state_dir` field can piggy-back on this hook for default
resolution without breaking callers that omit it.

---

## 2. Where `release_dir` is set

Comprehensive list of all `release_dir` assignment sites (sprint module
only; full grep at end of section):

### Production path

1. `src/superclaude/cli/sprint/config.py:336` — `load_sprint_config()`
   sets `release_dir=_resolve_release_dir(index_path)` when constructing
   the canonical `SprintConfig` (lines 332-349).
2. `src/superclaude/cli/sprint/config.py:236-272` — `_resolve_release_dir`
   chooses between `index_path.parent` and its grandparent depending on
   whether the index is under a `tasklist/` subdirectory and whether the
   grandparent has `.roadmap-state.json` / `*spec*.md`. This is the only
   resolution logic in production.
3. `src/superclaude/cli/sprint/commands.py:234-237` — `run` subcommand,
   when `--release-dir` is provided, overwrites the loaded config via
   `object.__setattr__(config, "release_dir", resolved)` and likewise
   forces `work_dir` to the same path. The override is post-construction
   so `__post_init__` does NOT re-run.

### Test fixtures (every fixture / call site that sets `release_dir=`)

(Verified by grep `SprintConfig\(` across `tests/sprint/**`.)

- `tests/sprint/test_models.py:180` — `_make_config` helper.
- `tests/sprint/test_models.py:1066` — direct call with `release_dir=tmp_path`.
- `tests/sprint/test_tmux.py:32` — fixture.
- `tests/sprint/test_tui_v2_wave2.py:71` — fixture.
- `tests/sprint/test_multi_phase.py:35` — fixture.
- `tests/sprint/test_integration_signal.py:34` — fixture.
- `tests/sprint/test_tui_monitor.py:41` — `**kwargs`-driven fixture.
- `tests/sprint/diagnostic/test_debug_logger.py:35,345` — two fixtures.
- `tests/sprint/test_tui.py:22` — fixture.
- `tests/sprint/test_wiring_budget_scenarios.py:42` — fixture.
- `tests/sprint/test_wiring_integration.py:39` — fixture.
- `tests/sprint/test_backward_compat_regression.py:74,124` — two fixtures.
- `tests/sprint/test_diagnostics.py:35` — fixture.
- `tests/sprint/test_preflight.py:491,591,928,1072,1108` — multiple per-test configs.
- `tests/sprint/diagnostic/test_diagnostics.py:33` — fixture.
- `tests/sprint/test_e2e_halt.py:34` — fixture.
- `tests/sprint/test_execute_sprint_integration.py:33` — fixture.
- `tests/sprint/test_phase8_halt_fix.py:37` — fixture.
- `tests/sprint/test_process.py:34` — `**kwargs`-driven fixture.
- `tests/sprint/test_e2e_trailing.py:77` — fixture.
- `tests/sprint/test_tui_task_updates.py:25` — fixture.
- `tests/sprint/test_checkpoints.py:174,274,279` — three constructions.
- `tests/sprint/test_resume_semantics.py:26,36,46,61,71,81,92,103,117` —
  9 inline `SprintConfig(index_path=...)` calls that **omit**
  `release_dir`, relying on the `Path(".")` default. These will likewise
  rely on the `state_dir` default.

### Read-only consumers (NOT assignment sites — for context)

`release_dir` is read at: `executor.py:178,179,389,412,504,592,1708,1709,1754,1829,1885,1901,1909`;
`tmux.py:60,87,166`; `process.py:130,132,144`; `checkpoints.py:38,82,128,149`;
and the properties on `SprintConfig` itself. The two sites the track
must migrate are **only**:

- `executor.py:1754` (writer)
- `tmux.py:166` (reader)

---

## 3. How env vars are read in `sprint/` (and adjacent CLI modules)

Exhaustive grep of `os.environ` / `os.getenv` under
`src/superclaude/cli/sprint/`, `src/superclaude/cli/pipeline/`, and
`src/superclaude/cli/main.py`:

| Site                                          | Pattern                                      | Purpose                                                        |
|-----------------------------------------------|----------------------------------------------|----------------------------------------------------------------|
| `sprint/tmux.py:55`                           | `"TMUX" not in os.environ`                   | Detect whether we are already inside tmux.                     |
| `sprint/commands.py:220`                      | `os.environ.get("CLAUDE_MODEL", "")`         | Model fallback when `--model` flag is empty (CLI-time default).|
| `sprint/summarizer.py:321`                    | `os.environ.items()` filtered by deny-list   | Subprocess env construction (strip helper).                    |
| `pipeline/process.py:104,107`                 | `os.environ.copy()`                          | Subprocess env construction.                                   |
| (none under `cli/main.py`)                    | —                                            | No env reads.                                                  |

### Project convention takeaways

1. **CLI-layer reads only.** The framework reads env vars in
   `commands.py` (CLI handler) and a couple of subprocess plumbing
   spots. Models and config-loader functions accept plain Python
   parameters; they do not read env directly.
2. **Pattern is `os.environ.get("<VAR>", "<default>")`** with a string
   fallback (see `commands.py:220` for `CLAUDE_MODEL`).
3. **Test fixtures construct `SprintConfig` directly** with keyword
   arguments and never go through `load_sprint_config`. Any new field
   must therefore have a sane `field(default_factory=...)` so all of the
   ~30 fixtures continue to work unchanged.

Conclusion: the cleanest project-aligned wiring is

- Add `SPRINT_STATE_DIR` env var resolution in
  `cli/sprint/commands.py::run` (alongside `CLAUDE_MODEL`), threaded
  through `load_sprint_config()` as a `state_dir: Path | None = None`
  parameter.
- `SprintConfig` gets a `state_dir: Path = field(default_factory=...)`
  whose default is derived deterministically from
  `release_dir`/`index_path` inside `__post_init__`, so direct
  constructors (tests, ad-hoc) still get a working value.

---

## 4. Recommended `state_dir` integration

### 4.1 Field

Add to `SprintConfig` (after `total_tasks`, around `models.py:398`):

```python
# Transient runtime state directory (e.g. .sprint-exitcode sentinel).
# Default resolved in __post_init__ to <repo>/.dev/sprint-state/<tasklist-id>/
# Override via SPRINT_STATE_DIR env var (handled at CLI layer in
# commands.py::run) or by passing state_dir= explicitly.
state_dir: Path = field(default_factory=lambda: Path(""))
```

Using `Path("")` (empty) as a sentinel lets `__post_init__` detect the
"not explicitly set" case and supply the derived default. (Using
`Path(".")` would collide with `release_dir`'s default and prevent
distinguishing user-supplied from implicit values; tests that pass
`release_dir=tmp_path` MUST get a derived `state_dir` not equal to
`tmp_path`.)

### 4.2 Default value derivation (in `__post_init__`)

Append to `SprintConfig.__post_init__` (after the existing
`wiring_gate_mode` derivation, around `models.py:445`):

```python
# Derive state_dir default if not explicitly provided.
if self.state_dir == Path(""):
    tasklist_id = self._derive_tasklist_id()
    derived = Path(".dev/sprint-state") / tasklist_id
    object.__setattr__(self, "state_dir", derived)
```

with a small private helper on the class:

```python
def _derive_tasklist_id(self) -> str:
    """Stable identifier for the current tasklist run.

    Prefers release_dir.name (matches the TUI panel title convention,
    tui.py:206); falls back to index_path.parent.name; final fallback
    is the index file stem.
    """
    if self.release_dir != Path(".") and self.release_dir.name not in ("", "."):
        return self.release_dir.name
    parent_name = self.index_path.parent.name
    if parent_name and parent_name != ".":
        return parent_name
    return self.index_path.stem or "default"
```

This mirrors the resolution already used by
`src/superclaude/cli/sprint/tui.py:202-206` so the `state_dir` slug
matches what users see in the TUI.

### 4.3 CLI loader changes

In `src/superclaude/cli/sprint/config.py`:

1. Add a new optional parameter to `load_sprint_config()` signature
   (around line 287):
   ```python
   state_dir: Path | None = None,
   ```
2. In the `SprintConfig(...)` constructor call (line 332-349), forward:
   ```python
   state_dir=state_dir if state_dir is not None else Path(""),
   ```
   The empty-Path sentinel triggers the `__post_init__` derivation.

In `src/superclaude/cli/sprint/commands.py::run`:

1. Add CLI option mirroring the env-var convention used for
   `CLAUDE_MODEL` (around line 220 / option block ending line 196):
   ```python
   @click.option(
       "--state-dir",
       "state_dir_override",
       type=click.Path(file_okay=False, path_type=Path),
       default=None,
       help="Transient state directory for .sprint-exitcode and other "
            "runtime artifacts (default: $SPRINT_STATE_DIR or "
            ".dev/sprint-state/<tasklist-id>/).",
   )
   ```
2. Thread it into `load_sprint_config()`:
   ```python
   state_dir = state_dir_override or (
       Path(os.environ["SPRINT_STATE_DIR"])
       if os.environ.get("SPRINT_STATE_DIR")
       else None
   )
   config = load_sprint_config(..., state_dir=state_dir)
   ```
3. Mirror the `--release-dir` post-construction override pattern
   (commands.py:234-237) if `--state-dir` is allowed to override after
   `__post_init__`.

### 4.4 Ergonomics for the two callers that matter

Both call sites already access `config.release_dir / ".sprint-exitcode"`
without any helper. The minimal-touch migration is:

- `executor.py:1754`:
  ```python
  state_dir = config.state_dir
  state_dir.mkdir(parents=True, exist_ok=True)
  (state_dir / ".sprint-exitcode").write_text(str(_exitcode))
  ```
- `tmux.py:166`:
  ```python
  sentinel = config.state_dir / ".sprint-exitcode"
  ```

Optionally, add a property on `SprintConfig` for symmetry with
`execution_log_jsonl` etc. (e.g. `exitcode_path -> self.state_dir /
".sprint-exitcode"`), but that's a polish item, not required for the
migration.

### 4.5 `.gitignore` follow-up

Replace the repo-root-only anchored line at `.gitignore:222`:
```
/.sprint-exitcode
```
with a directory-scope rule that covers the new state dir, e.g.:
```
.dev/sprint-state/
```
(Repo-root `/.sprint-exitcode` can be kept for safety against legacy
runs.) Out of strict scope for this track, but the writer-side fix
without the .gitignore companion change leaves orphan files behind on
the first run.

### 4.6 Backward compatibility

- `__post_init__` derivation means **every existing test fixture that
  omits `state_dir=` still works**: they get an auto-derived path
  derived from their `release_dir` (or `tmp_path`).
- The 9 `test_resume_semantics.py` calls that pass only `index_path=`
  fall through to `index_path.parent.name` / `index_path.stem`.
- The `--release-dir` override at `commands.py:234-237` uses
  `object.__setattr__` post-construction and therefore does **not**
  re-run `__post_init__`. If the override should also re-derive
  `state_dir`, the override block must also reset
  `state_dir = Path("")` and call `_derive_tasklist_id` (or just bypass
  re-derivation since users overriding release_dir typically pin
  output paths explicitly).

---

## 5. Sprint config tests inventory (tests that need updating or new coverage)

### Tests that MUST pass unchanged (acceptance criterion)

All ~30 fixtures listed in section 2 should pass without edits because
`state_dir` defaults via factory. Acceptance check:
```
uv run pytest tests/sprint/ -v
```

### Tests that likely need new assertions / new cases in `tests/sprint/test_config.py`

`tests/sprint/test_config.py` currently has zero references to
`release_dir` or `state_dir` (verified by grep). The minimum-needed
additions inside `TestLoadSprintConfig` (line 197):

1. **`test_state_dir_default_derives_from_release_dir`** — load a
   config and assert `config.state_dir ==
   Path(".dev/sprint-state") / config.release_dir.name`.
2. **`test_state_dir_explicit_override_via_load_arg`** — call
   `load_sprint_config(..., state_dir=tmp_path / "custom")` and assert
   the override is preserved.
3. **`test_state_dir_env_var_resolution`** — set
   `SPRINT_STATE_DIR=/tmp/foo` via `monkeypatch.setenv` and invoke the
   Click command (via `CliRunner`) to assert env-var resolution at the
   CLI layer. (May live in `tests/sprint/test_commands.py` if one
   exists; otherwise inline here.)
4. **`test_state_dir_distinct_from_release_dir_in_default_case`** —
   guard against accidental aliasing (the core bug we're fixing).

### Tests in `tests/sprint/test_models.py` that need new coverage

`tests/sprint/test_models.py` already has `TestSprintConfig` (line 187).
Add cases in that class:

1. **`test_state_dir_default_when_omitted`** — construct with
   `release_dir=Path("/tmp/release")` and assert `state_dir` resolves
   to `Path(".dev/sprint-state/release")` (i.e. `release_dir.name`).
2. **`test_state_dir_explicit_value_preserved`** — construct with
   `state_dir=Path("/tmp/explicit")` and assert it survives
   `__post_init__`.
3. **`test_state_dir_when_release_dir_default`** — construct only with
   `index_path=Path("/tmp/foo/tasklist-index.md")`; assert
   `state_dir == Path(".dev/sprint-state/foo")` (falls through to
   `index_path.parent.name`).
4. **`test_state_dir_falls_back_to_index_stem_when_no_parent`** —
   construct with only `index_path=Path("tasklist-index.md")`; assert
   it uses the stem.

### Other tests that may need light update (to remain green)

- `tests/sprint/test_tmux.py:32` — if the fixture asserts on a sentinel
  file location, switch the assertion from `config.release_dir /
  ".sprint-exitcode"` to `config.state_dir / ".sprint-exitcode"`. (Quick
  grep confirms whether the assertion exists — see Track 1
  `01-file-inventory` report.)
- `tests/sprint/test_execute_sprint_integration.py:33` and
  `test_e2e_*.py` fixtures — if any test reads the exit-code sentinel,
  same path update.

---

## Summary (3 lines)

- `SprintConfig` (models.py:348-397, dataclass extending `PipelineConfig` pipeline/models.py:179-189) currently anchors every path-derived property on `release_dir`; that field is set in two production sites (`config.py:336` and `commands.py:234-237`) plus ~30 test fixtures across `tests/sprint/**`.
- Project env-var convention is **CLI-layer only** (`commands.py:220` reads `CLAUDE_MODEL` via `os.environ.get`); no env reads in models/loader. Recommendation: add `state_dir: Path` field with empty-Path sentinel + `__post_init__` derivation to `.dev/sprint-state/<release_dir.name | index_path.parent.name | index_path.stem>/`; add `--state-dir` CLI flag and `SPRINT_STATE_DIR` env-var resolver in `commands.py::run`; thread optional `state_dir=` kwarg through `load_sprint_config()`.
- Two writer/reader sites flip (`executor.py:1754`, `tmux.py:166`); existing ~30 fixtures pass unchanged via factory default; companion `.gitignore` update from `/.sprint-exitcode` (`.gitignore:222`) to `.dev/sprint-state/` is needed but out-of-strict-scope for the config track.

---

## Gaps and Questions (gap-fill 2026-05-18)

Open Questions surfaced during research re-verification — flagged for the builder to resolve in the generated task file, not blocking research handoff:

1. **OQ-1 (load-bearing): Should `--release-dir` override re-derive `state_dir`?**
   - Context: The `run` subcommand at `commands.py:234-237` mutates `release_dir` post-construction via `object.__setattr__` — bypassing `__post_init__`. If the user passes only `--release-dir` (no `--state-dir`), the `state_dir` derived during `__post_init__` will reflect the ORIGINAL (loader-resolved) `release_dir`, NOT the override.
   - Recommendation (default): YES, re-derive. Add immediately after the existing `object.__setattr__(config, "release_dir", resolved)`:
     ```python
     # Re-derive state_dir if it was auto-derived from release_dir
     if config.state_dir == Path(".dev/sprint-state") / original_release_dir.name:
         object.__setattr__(config, "state_dir", Path(".dev/sprint-state") / resolved.name)
     ```
   - Alternative: leave alone and document the gotcha. Picks up `release_dir.name` mismatch but matches the override-is-explicit philosophy.
   - **Builder must choose one and document the rationale in the task file's Open Questions section.**

2. **OQ-2: Should `SPRINT_STATE_DIR` env-var also trigger `__post_init__` re-derivation?**
   - Same shape as OQ-1 but env-var driven. Recommendation: route via the loader (so `__post_init__` sees the explicit value) rather than via post-construction mutation.

3. **OQ-3 (drift-tracking): Line numbers will continue to drift.**
   - All `executor.py:NNNN` references in this doc reflect master HEAD at 2026-05-18 (`executor.py` = 2136 lines). The builder should re-grep `\.sprint-exitcode` and `release_dir` immediately before the FU-001 implementation phase if more than ~3 days elapse between research handoff and Phase 1 start.
