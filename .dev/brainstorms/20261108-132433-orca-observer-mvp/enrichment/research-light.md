---
source: research-light
quality_tier: fallback_1
method: deep-research agent with WebFetch and WebSearch (sc-research-protocol skill not installed; Tavily and Context7 not available in the agent session, fallback_reason tavily_missing)
created: 2026-11-08T13:31:00Z
---

# Light Research: production stack for the Orca observer

Dates come from GitHub, PyPI, pkg.go.dev and crates.io as of 2026-11-08. None of the frameworks were run here.

**Goal:** choose a read-only terminal dashboard stack for 5-10 orchestrators and 50-100 workers, inside an MIT Python repo that already uses Rich and click.

## 1. Charm: Bubble Tea v2, Lip Gloss v2, Bubbles v2 (Go)

- **License:** MIT for all three ("Copyright (c) 2020/2021-2026 Charmbracelet, Inc.").
- **Latest on pkg.go.dev:** Bubble Tea v2.1.1 (2026-10-28, module `charm.land/bubbletea/v2`); Lip Gloss v2.0.6 (2026-08-11); Bubbles v2.2.1 (2026-08-24). All newer than the TUIBBS-scp manifest pins (2.0.6 / 2.0.3 / 2.1.0).
- **Maintenance:** roughly monthly Bubble Tea releases in 2026, Charmbracelet org. Low risk.
- **Keyboard/list selection:** Bubbles list and table components; keys arrive as `tea.KeyPressMsg`.
- **Resize:** window-size messages; README advertises a cell-based renderer.
- **NO_COLOR:** honored by default, but read with `strconv.ParseBool` (colorprofile `env.go`), so `NO_COLOR=yes` is ignored, contrary to no-color.org (any non-empty value). When honored on a terminal, output drops to the ASCII profile; non-terminal output is plain.
- **Snapshot testing:** teatest/v2 (`WithInitialTermSize`, `Send`/`Type`, `FinalOutput`, golden files via `RequireEqualOutput`, `-update`). Lives under `x/exp`, no tagged release (latest untagged 2026-11-01); API can change.
- **Plain-text export:** Lip Gloss renders to strings; plain snapshot requires stripping escapes. No built-in export.
- **Wide/emoji width:** not described in READMEs. UNVERIFIED.
- **Distribution:** Go toolchain; one static binary per OS/CPU. Alongside the pipx CLI it needs a separate release download or platform-specific wheels, i.e. a cross-compile and release pipeline the repo does not have.

## 2. Textual (Python)

- **License:** MIT.
- **Latest:** 8.2.8 (2026-06-30); last five releases (April-June 2026) published by willmcgugan.
- **Maintenance:** Textualize company wound down May 2025 ("The future of Textualize"); Textual and Rich continue as community projects. No release for about 4 months; PR creation limited to collaborators. Medium risk.
- **Keyboard/list selection:** built-in focus and keys (ListView, DataTable). Detail UNVERIFIED.
- **Resize:** layout reflows.
- **NO_COLOR:** honored ("used internally to convert the application to monochrome, when the NO_COLOR env var is set", api/filter).
- **Testing:** best of the five: `App.run_test(size=(cols, rows))` headless (default 80x24), `Pilot` key presses, pytest-textual-snapshot SVG snapshots (`terminal_size=`, `--snapshot-update`).
- **Plain-text export:** none documented. UNVERIFIED.
- **Wide/emoji width:** Rich cell-width code.
- **Distribution:** one extra pure-Python dependency, no new toolchain.

## 3. Rich Live/Layout (Python, already a dependency)

- **License:** MIT.
- **Latest:** 15.0.0 (2026-04-12); 14.3.4 (2026-04-11), 14.3.3 (2026-02-19).
- **Maintenance:** same maintainer and community status as Textual; very widely used.
- **Keyboard:** output only; no input handling. Keyboard focus needs hand-written raw-terminal key reading.
- **Resize:** Live re-reads console size each refresh; no resize event, enough for 80/116/160.
- **NO_COLOR:** honored; removes colors, keeps bold/italic, wins over FORCE_COLOR.
- **Plain-text export:** strongest: `Console(record=True)` with `export_text()` / `export_svg()`; `Console(file=StringIO(), width=N)` is the documented unit-test route.
- **Wide/emoji width:** `rich.cells`; 14.3.3 fixed an endless loop in `split_graphemes`.
- **Distribution:** zero added cost.

## 4. Ratatui (Rust)

- **License:** MIT.
- **Latest:** 0.30.2 (2026-06-19); 0.30.1 (2026-06-05); 0.30.0 (2025-12-26).
- **Maintenance:** community org; pre-1.0, expect breaking changes. Low-medium risk.
- **Keyboard/list:** List widget with selection state; crossterm events.
- **NO_COLOR:** default crossterm backend skips color when non-empty (inferred from `colored.rs` source, not tested); termion UNVERIFIED.
- **Snapshot testing:** `TestBackend::new(80, 20)` + `insta`, plain-text rows; colors not compared.
- **Wide/emoji width:** unicode-width, unicode-segmentation, unicode-truncate.
- **Distribution:** Rust toolchain; per-platform binary; maturin bin wheels (as ruff/uv do) could fit pipx (general knowledge, not checked against maturin docs).

## 5. TUIBBS (AGPL)

AGPL code must not be copied into this MIT repository. Not researched further.

## Comparison

| Stack | License | Toolchain | Fit | Maintenance risk |
|---|---|---|---|---|
| Bubble Tea/Lip Gloss/Bubbles v2 | MIT | Go plus per-platform binary pipeline | Strong widgets and focus. NO_COLOR read as true/false. Test helper untagged | Low (monthly 2026 releases, company-backed) |
| Textual 8.2.8 | MIT | None (pip dependency) | Strong focus, layout, headless SVG snapshots. Plain text UNVERIFIED | Medium (company closed 2025, last release June 2026) |
| Rich 15.0.0 Live/Layout | MIT | None (already installed) | Best plain-text export and width tests. No keyboard input | Medium (same maintainer, very widely used) |
| Ratatui 0.30.2 | MIT | Rust plus maturin or separate binary | Strong list, plain-text snapshots, NO_COLOR via crossterm | Low-medium (pre-1.0) |
| TUIBBS | AGPL | n/a | Do not copy code | n/a |

**Not checked:** Bubble Tea/Lip Gloss wide-character measurement; Textual plain-text export; NO_COLOR on Ratatui termion backend.

## Sources

- Bubble Tea: https://github.com/charmbracelet/bubbletea/releases, https://github.com/charmbracelet/bubbletea/blob/main/LICENSE, https://github.com/charmbracelet/bubbletea/blob/main/UPGRADE_GUIDE_V2.md, https://pkg.go.dev/charm.land/bubbletea/v2?tab=versions
- Lip Gloss: https://github.com/charmbracelet/lipgloss/releases, https://pkg.go.dev/charm.land/lipgloss/v2?tab=versions
- Bubbles: https://github.com/charmbracelet/bubbles/releases, https://pkg.go.dev/charm.land/bubbles/v2?tab=versions
- colorprofile: https://raw.githubusercontent.com/charmbracelet/colorprofile/main/env.go; teatest v2: https://pkg.go.dev/github.com/charmbracelet/x/exp/teatest/v2
- Textual: https://pypi.org/pypi/textual/json, https://textual.textualize.io/guide/testing/, https://textual.textualize.io/api/filter/, https://textual.textualize.io/blog/2025/05/07/the-future-of-textualize/
- Rich: https://pypi.org/pypi/rich/json, https://rich.readthedocs.io/en/stable/console.html
- Ratatui: https://crates.io/api/v1/crates/ratatui, https://ratatui.rs/recipes/testing/snapshots/, https://raw.githubusercontent.com/crossterm-rs/crossterm/master/src/style/types/colored.rs
- https://no-color.org/
