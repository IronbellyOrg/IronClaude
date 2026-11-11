# Stack

**Recorded owner decision 2 (CONFIRMED 2026-11-08):** Python + Rich, as a `superclaude observe`-style subcommand in the IronClaude repository. R1 also writes the versioned, additive-only JSON snapshot (`snapshot-export-schema.md`). This supersedes issue 409's stated preference for Go with Bubble Tea v2, Lip Gloss v2 and Bubbles v2.

## Comparison (seed brief stack table, 2026-11-08, primary sources, nothing run: UNVERIFIED as run facts)

| Criterion | Go Bubble Tea v2 / Lip Gloss v2 / Bubbles v2 | Python Rich 15 (installed) | Textual 8.2.8 | Ratatui 0.30.2 |
|---|---|---|---|---|
| License | MIT | MIT | MIT | MIT |
| Toolchain added | Go toolchain plus per-platform binary release pipeline | None | One pure-Python dependency | Rust toolchain plus maturin or a binary |
| Keyboard and focus | Strong, built in | None; needs a hand-written POSIX key reader (`termios`, `tty`, `select`; stdlib) | Built in | Strong |
| Text export (required) | Not built in | `Console(record=True)` + `export_text()` | UNVERIFIED | Plain-text snapshots |
| NO_COLOR | Parsed as boolean (`NO_COLOR=yes` ignored, contrary to no-color.org); needs own check | Must be handled explicitly (no house TUI does it today) | UNVERIFIED | UNVERIFIED |
| Cell width | Wide-char width UNVERIFIED | `rich.cells.cell_len` | Via Rich | Built in |
| Headless tests | teatest/v2 untagged under `x/exp` | Fixed-width `Console(width=W)`, no TTY | `run_test(size=...)` | Snapshots |
| Maintenance | Low risk, monthly releases | Medium, same maintainer, very widely used | Medium; company wound down May 2025, community-maintained | Low-medium, pre-1.0 |
| Fit with repo | Second language, separate CI and release; cannot ship via `pipx install` | House pattern (`sprint/tui.py` `Live(...)`, `_render() -> Panel`); `click` registration in `cli/main.py` | New dependency to vet | Third language |

## Rules

- **Why Rich:** the two hardest MVP requirements, text export and cell-width truncation, are tested headlessly and Rich does both. Its one gap is keyboard input.
- **Key reader:** a small POSIX stdlib reader (`termios`/`tty`/`select`) for the navigation keys and `/ h m e q`. It is new non-trivial code with its own tests. It uses cbreak mode (`tty.setcbreak`, ISIG kept), not raw mode, so Ctrl-C still raises SIGINT. It restores the terminal in `finally` and on SIGINT, SIGTERM, SIGHUP and SIGTSTP (before suspending), and re-enters cbreak mode on SIGCONT.
- **Spike first (R0):** Rich Live with the cbreak key reader. If the spike fails, switch to Textual. Never build both. Textual is not first because of its maintenance risk and UNVERIFIED plain-text export.
- **One view model, two renderers:** the collector produces a snapshot; a pure function builds one view model; `render(view, W)` draws the width-bounded screen, `export_text(view)` writes the `e`/`--once` record form, lossless for every value the export permission allows, with full IDs, and `export(view)` writes the versioned, additive-only JSON snapshot (recorded owner decision 2, owner-decisions-20261108.md item 5; `snapshot-export-schema.md`). Tests assert on the view model and each renderer separately. A later Go port re-implements this small, test-pinned surface.
- **Terminal rules:** the screen truncates by cells with one visible `>`, which survives ASCII; `--ascii` selects the ASCII path for non-UTF-8 terminals; the record export never truncates. NO_COLOR is honoured for both `1` and `yes`.
- **Platform:** interactive mode is POSIX only; `--once` (text export) works everywhere, including Windows.
- **Placement:** a `click` subcommand registered like the others in `cli/main.py` (deferred import, then `add_command`). Recommended name `superclaude observe`; final name is open owner decision 3. Registering it in the shipped CLI is production integration under reading 1 (`release-gates.md`).
- **Licensing and reuse:** TUIBBS-scp is AGPL-3.0; no code is copied from it. The sanitizer is written in the observer package. The design prototype `canvas.py` is never imported by production code.
