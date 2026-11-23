---
source: codebase
quality_tier: fallback_1
method: Explore agent with codegraph, Glob, Grep and Read (auggie MCP not available in this session)
created: 2026-11-08T13:29:00Z
---

# Codebase Context: orca-observer-mvp

**Paths:** Repo is `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp`. Below, `cli/` means `src/superclaude/cli/` and `proto/` means `.dev/design/orca-observer-20261106/`.

## 1. Existing Rich TUIs and live displays

None of the four files reads keyboard input (a search for termios, tty, select, readchar found nothing). None handles NO_COLOR, `console.width` or `cell_len`; they rely on Rich defaults.

- **`cli/sprint/tui.py` (649 lines)**: imports `Console`, `Group`, `Live`, `Panel`, `Table`, `Text` (lines 9-14); no `Layout`. `SprintTUI.start()` builds `Live(..., refresh_per_second=2, screen=False)` (lines 119-126); stdout/stderr redirect on unless `SUPERCLAUDE_SPRINT_RENDER_DIAG=1` (line 118). Push-based refresh: executor calls `update()` -> `self._live.update(self._render())`; first render error sets `_live_failed` and prints one warning (lines 136-172). `_render()` returns one `Panel` around a `Group` (lines 174-217). Phase table `Table(box=None, pad_edge=False)` with fixed widths (lines 250-259). Helpers `_render_bar` (614), `_render_percent` (624), `_format_timestamp` (632), `_truncate` (640, `len()`-based, adds "...", not display width). Tests in `tests/sprint/`: `test_tui.py` (11), `test_tui_v2_wave1.py` (39), `test_tui_v2_wave2.py` (34), `test_tui_gate_column.py` (8), `test_tui_monitor.py` (5), `test_tui_redirect_gate.py` (3).
- **`cli/sprint/monitor.py` (761 lines)**: no Rich code; data side. `OutputMonitor` (line 443) runs a daemon thread "output-monitor" (470-475). `_poll_loop` waits on `_stop_event.wait(poll_interval)`, default 0.5 s (451, 502-505). Reads NDJSON incrementally with `_line_buffer`; `stop()` joins with 2 s timeout (477-481). Tests: `tests/sprint/test_monitor.py` (43).
- **`cli/prd/tui.py` (305 lines)**: Rich imported inside `try` with `_HAS_RICH=False` fallback (16-26). `Console(stderr=True)` only when interactive (130-131); `_is_interactive()` checks `sys.stderr.isatty()` (301-305). `start()` no-op when not interactive (143-153). Same `Live` settings; once-and-done failure guard (198-208). Docstring forbids `async` and sprint/roadmap imports (7-8). Tests: none found (UNVERIFIED that none exist elsewhere).
- **`cli/cleanup_audit/tui.py` (145 lines)**: `Console`, `Group`, `Live`, `Panel`, `Text` (12-16). Same `Live` settings (65-70); silent failure guard (79-91); `_render()` Panel around Group (93-105). Tests: none found.

**Shared convention:** class with `__init__(config, console=None)`, `start() -> Live`, `stop()`, push-style `update()`, `_render() -> Panel`; status styles/icons in dicts (sprint 42-77, prd 34-72).

## 2. Existing code that calls the `orca` CLI

- `cli/install_user_setup.py:35` `_ORCA_CLIS = ("orca-ide", "orca")`.
- `_find_orca()` (198-221): `shutil.which` each name, runs `[path, "skills", "list", "--json"]` with `capture_output=True, text=True, timeout=10, stdin=DEVNULL`, `json.loads`, accepts only if the `orca-cli` topic is present (guards against the GNOME screen reader also named `orca`, 199-202). Catches `OSError`, `SubprocessError`, `ValueError`, `AttributeError` (217).
- `_orca_timeout(deadline)` at 224 (body not read).
- Nothing mentions "orca orchestration" or "worker-list"; nothing parses orchestration JSON.

## 3. Existing ANSI sanitizers and width helpers in `src/`

- `cli/eval/pty_stream.py:94-101` `ANSI_ESCAPE_RE`: strips CSI, OSC (BEL or ST), DCS/SOS/PM/APC, ESC + one printable. Exported (72), reused by `cli/eval/expect.py:42` (`_strip_ansi` 94-103). Gaps: no 8-bit C1 (`\x9b`, `\x9d`); no bare control chars or Unicode `Cf` (bidi overrides); unterminated OSC not matched.
- `cli/pipeline/validation_text.py:25` `sanitize_output(output_file, logger)` works on files; fit for terminal display UNVERIFIED (not read).
- No `wcwidth`, `rich.cells` or `cell_len` usage in `src/`. Only truncation helper is `sprint/tui.py:640` (`len()`).
- NO_COLOR handling in `src/` exists only in a shell script, `skills/ccsession-tag/ccsession:1567-1569`.

## 4. How a `superclaude <subcommand>` group is registered

- Root group `cli/main.py:18-20` (`@click.group()` + `@click.version_option`, function `main`).
- Each group lives in its package, e.g. `cli/sprint/commands.py:16-17` (`@click.group("sprint") def sprint_group()`), commands via `@sprint_group.command(...)` (72, 684), re-exported at `cli/sprint/__init__.py:3,5`.
- Registration: deferred import in `main.py` after all definitions, then `main.add_command(...)` (519-561):

```python
from superclaude.cli.sprint import sprint_group  # noqa: E402,I001  # intentional: deferred subcommand registration to avoid circular imports
main.add_command(sprint_group, name="sprint")
```

## 5. Offline design prototype `proto/` (synthetic, not production code)

- `canvas.py` imports `wcwidth`, `wcswidth` (5). `ASCII_MAP` (8). `sanitize(value)` (10-17) removes OSC, DCS/PM/APC, CSI (7-bit and 8-bit), ESC Fe, then drops Unicode Cc, Cf, Cs. `clip(text, width, ascii_mode=False)` (19-29) sanitizes then truncates by display width with `…` or `~`. `class Canvas` (31); `selected_summary` (117).
- `fixtures.py` header: "Synthetic observation records. No Orca adapter, environment reads or network I/O" (1). Functions `fixture(owners, count, variant)` (11), `normalize_events` (90), `metrics` (98), `write_fixtures` (114). Variants: base, uneven, shared-unmapped, historical, long-identifiers, source-loss, missing-fields, duplicate-out-of-order, empty, injection (24-85, 117).
- `render.py`: `designs`, `screen`, `image(no_color=...)`, `exports`, `build_gallery`. Layouts in `layouts/group_a.py`, `layouts/group_b.py`, `layouts/agent_focus.py`.
- `tests/test_designs.py`: 19 unittest tests (`Semantics` 10, `SafeText` 5: control_injection, width, ascii, no_color, html_escape; `Layouts` 4). JS test `tests/test_gallery.cjs` (not read).
- `requirements.txt`: `Pillow==13.0.0`, `wcwidth==0.9.4`; neither is a project dependency.

## 6. Textual and Go

- `pyproject.toml:37` `"rich>=13.0.0"`. Textual and wcwidth absent from `pyproject.toml`; `uv.lock` not checked.
- No `*.go` or `go.mod` in the repo.

## Reuse candidates

- **TUI class:** `SprintTUI` / `CleanupAuditTUI` structure (`Live(refresh_per_second=2, screen=False)`, `_render() -> Panel`, `_live_failed` guard).
- **Non-interactive fallback:** PRD TUI `_is_interactive()` + `Console(stderr=True)` (`prd/tui.py:130,143-146,301-305`).
- **Polling thread:** `OutputMonitor` (`sprint/monitor.py:443-505`).
- **Finding the binary:** `_find_orca()` (`install_user_setup.py:198-221`); reuse or move to a shared module rather than probing a bare `orca`.
- **Sanitizer:** `ANSI_ESCAPE_RE` (`eval/pty_stream.py:94`) as base, plus C1 and Cc/Cf filtering (proto `canvas.py:10-17` shows the stricter version).
- **Width truncation:** `rich.cells.cell_len` (Rich already a dependency, wcwidth is not), following proto `clip` logic (`canvas.py:19-29`).
- **Test scenarios:** proto `fixtures.py` variants (injection, long-identifiers, empty, source-loss) seed observer tests.
- **CLI registration:** deferred-import `main.add_command` pattern (`main.py:519-561`).

## Not checked

Tests for the PRD and cleanup-audit TUIs outside `tests/`; `validation_text.sanitize_output`; `_orca_timeout`; `uv.lock`; `test_gallery.cjs`.
