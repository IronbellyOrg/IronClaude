# Research: Zellij and render harness environment
**Investigation type:** Integration Mapper
**Scope:** the files and commands listed above
**Status:** Complete
**Date:** 2026-11-17
---

## 1. Installed Zellij setup

### 1.1 Version and setup check
- `command -v zellij` -> `/usr/local/bin/zellij`; `zellij --version` -> `zellij 0.44.2` [CODE-VERIFIED]
- `zellij setup --check` (read-only): `[CONFIG FILE]: Well defined.`, `[CONFIG DIR]: "/home/coder/.config/zellij"`, `[LAYOUT DIR]: "/home/coder/.config/zellij/layouts"`, `[PLUGIN DIR]: "/home/coder/.local/share/zellij/plugins"`, `[FEATURES]: []`, `[DEFAULT EDITOR]: Not set` [CODE-VERIFIED]
- No session was started, attached or modified.

### 1.2 /home/coder/.config/zellij/config.kdl (53 lines, mostly comments)
- Active directives: line 35 `theme "aidev02"`, line 36 `show_release_notes false`, line 37 `default_shell "/bin/bash"`, lines 49-53 `plugins { welcome-screen location="zellij:session-manager" { welcome_screen false } }` [CODE-VERIFIED]
- No `keybinds` block, so stock keybindings. Header (lines 1-33) says the file exists to suppress first-run wizards in a CI contract test, not to style anything.
- Directory listing: config.kdl 3065 bytes, layouts/agent.kdl 11861 bytes (265 lines), layouts/default.kdl 2734 bytes (58 lines), themes/aidev02.kdl 12006 bytes (252 lines) [CODE-VERIFIED]. The headers say they are copied from `/etc/skel` (machine provisioning, not this repo).

### 1.3 layouts/default.kdl (58 lines)
- Lines 48-58: `layout { default_tab_template { pane size=1 borderless=true { plugin location="zellij:tab-bar" } children pane size=2 borderless=true { plugin location="zellij:status-bar" } } }`. Tab bar on top (1 row), status bar at the bottom (2 rows) [CODE-VERIFIED]
- Header: no keybinds, no border-colour override (theme decides), pure 7-bit ASCII.

### 1.4 layouts/agent.kdl (265 lines)
- Line 111 `theme "aidev02_agent"`; lines 113-120 `default_tab_template` holds only `pane size=2 borderless=true { plugin location="zellij:status-bar" }` then `children` (status bar on top, no tab bar) [CODE-VERIFIED]
- Line 122 onward: inline `themes { aidev02_agent { ... } }`. It differs from aidev02 in `frame_selected.base 5` (magenta, line 165) and `ribbon_selected.background 5` (line 153); aidev02 uses cyan 6 [CODE-VERIFIED]

### 1.5 themes/aidev02.kdl (252 lines)
- Lines 109-110 `themes { aidev02 {`; slots text_unselected, text_selected, ribbon_unselected, ribbon_selected, frame_selected (base 6 cyan, line 152), frame_unselected (base 7), frame_highlight, exit_code_success (base 2) [CODE-VERIFIED for lines 109-178; lines 179-252 not read]
- Every value is one ANSI-16 integer in [0,15] (no hex, no RGB); header lines 35-45 say so and lines 74-80+ forbid ANSI 4 (blue) and truecolor.
- Mapping from the header (lines 17-32): ACCENT_PRIMARY cyan 6, ACCENT_SECONDARY magenta 5, SUCCESS green 2, WARNING yellow 3, ERROR red 1, FG_DIM 8.

### 1.6 What Zellij 0.44.2 offers (help text only; anything needing a running session is UNVERIFIED)
- `zellij --help`: `-l/--layout`, `--layout-string` (raw KDL), `-n/--new-session-with-layout`, `-s/--session`, `--max-panes`, `-c/--config`, `--config-dir`. Subcommands include action, attach, convert-config/layout/theme, edit, list-sessions, kill-session, options [CODE-VERIFIED by help text]
- `zellij action --help` (first 120 lines only, so the list is partial): `dump-screen`, `dump-layout`, `list-panes`, `list-tabs`, `new-pane`, `new-tab`, `override-layout`, `hide-floating-panes`, `are-floating-panes-visible`, `change-floating-pane-coordinates`, `launch-plugin`, `launch-or-focus-plugin`, `pipe`, `paste`, `rename-pane`, `resize`, `save-session` [CODE-VERIFIED by help text]
- `zellij run --help`: `-f/--floating`, `--width/--height/-x/-y` (integer or percent), `--pinned`, `-n/--name`, `--cwd`, `-c/--close-on-exit`, `--borderless`, `--in-place`, `--stacked`, `--blocking`, `--block-until-exit[-success|-failure]` [CODE-VERIFIED by help text]. A floating Decision Desk pane could be opened from the CLI with fixed size and position.
- `zellij action dump-screen --help`: `-a/--ansi` keeps ANSI styling, `-f/--full` includes scrollback, `-p/--pane-id <terminal_N|plugin_N|N>`, `--path <file>` (stdout if omitted) [CODE-VERIFIED by help text]. It emits text or ANSI only, never an image. Whether the dump is faithful for colours, wide glyphs and box drawing is UNVERIFIED (needs a session).
- Tab bar and status bar are the plugins `zellij:tab-bar` and `zellij:status-bar` (default.kdl lines 51 and 55) [CODE-VERIFIED].
- Theme reuse: Zellij themes are ANSI-16 slots; the observer prints through Rich, so reuse means choosing the same ANSI-16 indices. Whether an application can read the active Zellij theme at runtime is UNVERIFIED (not in help).
- Starting `superclaude observe` in a pane: `zellij run -- <cmd>` exists per help; the layout-file syntax for a command pane is UNVERIFIED here because no installed layout uses it.

**Key Takeaways**
- Zellij 0.44.2 is installed with a minimal config; the theme is ANSI-16 only (cyan primary; magenta in the agent layout).
- Floating panes, `dump-screen --ansi`, `--layout-string` and `zellij run` exist per help text; none was exercised.
- Neither installed layout defines an observer pane or a floating pane; all runtime behaviour is UNVERIFIED.

## 2. Offline render tools

Working directory `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp`; `uv run python --version` -> `Python 3.10.20`; `uv --version` -> `uv 0.11.8`.

| Tool | Check | Result |
|---|---|---|
| Rich | `uv run python -c "import importlib.metadata as m; print(m.version('rich'))"` | `15.0.0` [CODE-VERIFIED] |
| PIL | `uv run python -c "import PIL"` | `ModuleNotFoundError` |
| cairosvg | import | `ModuleNotFoundError` |
| pyte | import | `ModuleNotFoundError` |
| playwright | import | `ModuleNotFoundError` |
| fontTools | import | `ModuleNotFoundError` |
| chromium, chromium-browser, google-chrome | `command -v` | MISSING |
| rsvg-convert, inkscape, convert, magick | `command -v` | MISSING |
| freeze, termshot, aha, ansi2html | `command -v` | MISSING |
| unzip | `command -v` | MISSING |
| node / npx | `command -v` | `/usr/local/bin/node` (v24.22.2), `/usr/local/bin/npx` |

- All five Python modules are absent from the project environment, matching the scope notes [CODE-VERIFIED]. No render-to-image tool is installed.
- Rich 15.0.0 `Console` has `export_html`, `export_svg`, `export_text`, `save_html`, `save_svg`, `save_text` (`dir(Console)` output) [CODE-VERIFIED]. SVG or HTML export is therefore available offline with no new dependency, but turning it into a PNG needs a rasteriser, and none is installed.
- `~/.cache/ms-playwright` does not exist, so no Playwright browser binaries are cached. Fonts: `fc-list` shows DejaVu Sans Mono among the system fonts (`/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf`). Whether it covers every glyph the mockups use is UNVERIFIED.
- `uv pip list | grep -iE 'rich|pillow|pytest '` showed `rich 15.0.0` and `pytest 9.2.0` and no Pillow [CODE-VERIFIED].

**Key Takeaways**
- Offline in this environment: Rich text/ANSI/SVG/HTML export, node 24. Nothing can rasterise SVG or HTML to PNG.
- Every PNG route needs a new dependency or a browser the repo does not ship.

## 3. Dev dependencies and Makefile targets

- `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/pyproject.toml` lines 34-43: runtime dependencies pytest, click, rich>=13.0.0 (line 37), pyyaml, jsonschema, jinja2, pexpect>=4.9, httpx>=0.27. Lines 45-56 `dev`: pytest-cov, pytest-benchmark, scipy, `ruff==0.15.20`, mypy. Lines 57-61 `test` extra. No image, SVG, terminal-emulator or browser package is declared [CODE-VERIFIED]. `pexpect` (line 41) is declared; `pyte` is not. `pexpect` 4.9.0 is the route for capturing the live screen's styled bytes through a pty (measured with a stand-in child in `02-live-screen-commands-export.md` section 9.3, route B).
- `Makefile` line 1 `.PHONY` list and targets: install (line 5, `uv pip install -e ".[dev]"`), test (line 13, `uv run pytest`), lint (line 48, `lint-architecture` then `uv run ruff check .`), format (line 53), sync-dev (109), verify-sync (166), verify-deps (356), lint-architecture (362), eval-skill (497), reflect-eval (508). No render, screenshot or observe target [CODE-VERIFIED via grep for `render|svg|png|observe`, which matched no target].
- A Phase 0 harness would need either a new dev extra in `pyproject.toml` lines 46-56 or a standalone script, plus a new Makefile target.

**Key Takeaways**
- Nothing in pyproject.toml or the Makefile supports image rendering today; adding a dev extra and a `make render-gate` style target is new work.

## 4. render_current.py

File: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/tools/render_current.py` (94 lines, read only, not run).
- Header lines 1-11: run as `PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 uv run python .dev/issues/409/visual-parity/inputs/tools/render_current.py` from the repo root. It writes `inputs/current/<width>/{ledger,questions,desk}.txt` plus `ansi-<name>.txt`, from synthetic data built with test helpers (imports from `tests.observe.conftest`, lines 24-35).
- Constants: `OUT` (line 37), `HEIGHT = 50` (line 38), `WIDTHS = (160, 116, 80)` (line 39).
- `emit(view, width, name)` (lines 68-75): `resolve_policy({}, "utf-8", {"ascii": False}, width, HEIGHT)` (69), writes `"\n".join(screen_lines(view, policy))` to `<name>.txt` (72), then `make_console(policy, file=io.StringIO(), record=True)`, `console.print(render(view, policy))` and `console.export_text(styles=True)` to `ansi-<name>.txt` (73-75).
- `main()` (78-90) builds three views: `ledger` from `FixtureSource("base")`, `plain` (questions) and `desk` (after `apply_key(session, Key("text", "n"), ...)`) and calls `emit` for each width. Line 93 calls `main()` at import time (no `if __name__` guard).
- The recorded console is already on hand at line 73, so extending `emit` with `console.export_svg(...)` or `export_html(...)` per width and screen is a few lines, with no new dependency. A PNG step is the only new piece.
- Existing output: `current/160/ansi-ledger.txt` contains 0 ESC bytes (`grep -c $'\x1b'` -> 0), while the mockup `mockups/160/signal-bridge.ansi` has 48 lines containing ESC [CODE-VERIFIED]. The docstring (lines 8-9) says the same: no styles are applied by the current screen.
- Mockup inputs: `inputs/mockups/{160,116,80}/` each hold `agent-focus-attention-ledger`, `decision-desk` and `signal-bridge` as `.png`, `.ansi` and `.txt` (listing for 160 and 80 seen; 160 PNGs are 79851, 91078 and 171981 bytes). The mockup `.txt` files are plain text of the same screens.
- Because the mockups exist as .ansi and .txt as well as .png, a text and ANSI comparison needs no image tool.

**Key Takeaways**
- `render_current.py` already produces per-width text and ANSI for three screens; adding SVG/HTML export is trivial; PNG needs a new tool.
- Today's ANSI output has no styling, so ANSI diffing is meaningful only after styling lands.

## 5. Harness options: CI offline versus Claude session only

| Option | Works in CI offline today | Install cost | Notes |
|---|---|---|---|
| Text + ANSI assertions (existing `render_current.py` output, compare with mockup .txt/.ansi) | Yes | None | Model-judged rubric or script diff; can parse SGR codes to check colours without any image [CODE-VERIFIED that both file kinds exist] |
| Rich `export_svg` / `export_html` | Yes (Rich 15.0.0 API present) | None | Produces SVG/HTML text, not PNG |
| SVG to PNG via cairosvg or PIL + font | No (modules and rsvg-convert missing) | New dev dependency plus system libcairo (the cairo system library was not checked: UNVERIFIED) | Font and glyph fidelity depends on installed fonts (DejaVu Sans Mono present) |
| Headless browser (Playwright python or chromium) | No (no binaries, no `~/.cache/ms-playwright`) | Package plus a browser download (size and network access UNVERIFIED, not tested) | Best fidelity for HTML export |
| pyte terminal emulation | No | One pure-Python dev dependency (not tested) | Feeds ANSI into a screen model; still no PNG |
| Playwright MCP browser tool (`mcp__plugin_playwright_playwright__*`) | No: exists only in the Claude session, not in the repository | None in session | Could open an exported HTML or SVG file and screenshot it; tool availability was seen in this session's tool list, not exercised |
| Zellij `dump-screen --ansi` | No (needs a Zellij session) | None; binary installed | Text only, UNVERIFIED fidelity |

## 6. Fresh reviewer subagent scoring against mockup PNGs

- Inputs the reviewer needs: the mockup PNG (`inputs/mockups/<width>/<screen>.png`), the rendered output for the same width and screen (text, ANSI, and a PNG if available), and a fixed rubric file listing criteria and a score scale. Reading `.png` files is possible with the Read tool (it presents images visually per its description); this agent did not exercise it.
- Tools needed: Read only for text and PNG inputs; a Bash tool is not needed if the render step ran beforehand. A reviewer using only the ANSI/text exports can compare colour and layout by reading escape codes and text, but cannot see what the mockup PNG shows without an image.
- Because the rendered side would otherwise be text, a PNG render of the new output is what lets a reviewer compare image to image; without a rasteriser the reviewer would compare mockup PNG (image) against rendered text/ANSI (text), which is weaker.
- Whether a subagent's Read reliably shows a PNG is UNVERIFIED here (not tested).

**Key Takeaways**
- Text and ANSI scoring works offline now. Image-to-image scoring needs a PNG renderer, which does not exist in the repo or CI environment.

## 7. Q6 Zellij go or no-go (evidence only)

- Evidence for go: floating panes with size and position (`zellij run -f --width --height -x -y`), `dump-screen --ansi`, `--layout-string`, ANSI-16 theme files already installed (sections 1.6, 1.5).
- Evidence against or open: no session was started, so floating-pane behaviour, `dump-screen` fidelity and observer command panes are UNVERIFIED; `dump-screen` gives text, so it does not solve PNG rendering; the install on this machine is provisioned from `/etc/skel`, not from this repo, so CI cannot assume it exists (CI presence of zellij not checked: UNVERIFIED).
- Requirement that the observer works on its own outside Zellij, read-only, at all widths, with NO_COLOR and ASCII: nothing found in Zellij's config or help requires or prevents this; the observer is a Rich program run by `render_current.py` without Zellij.
- Evidence-based recommendation: no-go for Zellij as the Phase 0 render harness or a dependency of the observer (it adds no image output and its behaviour is unverified here); treat Zellij as an optional presentation environment to test manually after a verified session experiment.

**Key Takeaways**
- Zellij does not remove the need for a PNG renderer; its useful features are unverified without a live session.

## Gaps and Questions

- [UNVERIFIED] Floating-pane behaviour, `dump-screen --ansi` fidelity (colours, wide glyphs, box drawing), and command panes in a layout: all need a live Zellij session, which this task forbids.
- [UNVERIFIED] Whether an application can read the active Zellij theme at runtime.
- [UNVERIFIED] Layout-file syntax for starting `superclaude observe` in a pane (no installed layout uses a command pane).
- [UNVERIFIED] `zellij action --help` was read only to line 120, so the subcommand list is partial; lines 179-252 of `aidev02.kdl` and lines 180-265 of `agent.kdl` were not read.
- [UNVERIFIED] Whether Zellij exists in CI (the install here is provisioned from `/etc/skel`).
- [UNVERIFIED] Whether `pip`/`uv` can install Pillow, cairosvg, pyte or a Playwright browser here (network not tested); whether the cairo system library is present; whether DejaVu Sans Mono covers every glyph in the mockups.
- [UNVERIFIED] Whether a subagent's Read of a PNG works in the review setting (not tested).
- Question: Is a PNG-capable renderer worth a new dev dependency, or is a text/ANSI rubric plus mockup PNG viewing enough for the render gate?
- [CODE-CONTRADICTED] None found; all five scope-note claims about missing modules were confirmed.

## Stale Documentation Found

- [STALE DOC] `render_current.py` header (lines 8-9) says the ANSI files are "empty of escapes today"; confirmed accurate for `current/160/ansi-ledger.txt` (0 ESC bytes), but it will go stale as soon as styling lands.
- [STALE DOC] The Zellij layout/theme headers cite phase-tasklist task IDs and a CI validation gate "deferred to CI"; these concern the machine provisioning project, not this repo, and were not verified.
- `config.kdl` lines 30-31 cite `default.kdl:511` and lines 47-48 cite `default.kdl:236-238` of the upstream Zellij v0.44.2 source; not verified (the upstream file was not read).

## Summary

Zellij 0.44.2 is installed at `/usr/local/bin/zellij` with a minimal ANSI-16 theme and two layouts; floating panes, `dump-screen --ansi` and `--layout-string` appear in help text, but no behaviour was exercised. The project environment has Rich 15.0.0 (with `export_svg`/`export_html`) but no PIL, cairosvg, pyte, playwright, fontTools, browser, rsvg-convert, ImageMagick or other rasteriser, and pyproject.toml and the Makefile declare nothing for image rendering. `render_current.py` already writes per-width text and ANSI for three screens and could add SVG/HTML export with a few lines; PNG output needs a new dependency, and the Playwright MCP tool exists only in the Claude session. Text and ANSI comparison against the mockup `.txt`/`.ansi` files works offline today, while image-to-image scoring needs a new renderer. The Zellij evidence supports no-go as a harness dependency pending a live session test.
