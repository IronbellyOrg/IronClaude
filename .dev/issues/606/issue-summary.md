# Summary: #606 [FEATURE] Observer visual parity: bring the dashboard theme, frames and layout up to the design mockups

- Issue: https://github.com/IronbellyOrg/IronClaude/issues/606
- Type: feature
- Complexity: complex (rubric: `refs/claim.md`)
- Effort estimate: 56 hours

## What the issue asks for

Make `superclaude observe` look like the three design mockups (Signal Bridge, Attention Ledger and Decision Desk) at 160, 116 and 80 columns, without changing its rules: read-only, real data only, and question text shown on screen only. The review and the phased spec are already done and posted on the issue: the merged findings, the spec in three comments (sha256 `a5fc4f9b...`, checked), and the owner rulings of 2026-11-18. Those rulings put the Decision Desk in two columns at 160 and 116, keep the questions screen stacked, never show the hash, and apply the "space diet". What remains is to implement phases P0 to P7: a render-compare harness; a colour theme with depth detection (truecolor, 256, 16); fixes for the plain-text defects; titled frames; a count strip and a RETAIN CONTEXT pane; the two-column desk; ledger panes; and spec reconciliation. Each phase must pass an automated render gate (at most 3 iterations) before the next starts. The claiming agent runs `/sc:workflow` on the spec, then `/sc:implement`, then `/sc:pr-submit --monitor 3`. One gap: the Phase 0 inputs (`VP/inputs/tools/render_current.py` and the baseline captures) and the evidence trail exist only untracked in a local checkout, so they must be pushed or rebuilt first (see the accuracy check).

## Relevant files and systems (cheatsheet)

| Path or system | Why it matters |
|---|---|
| `src/superclaude/cli/observe/render.py` | All layout. Plain-string builders feed `render()` (:524-531). This is where the role spans, frames, count strip, RETAIN pane and two-column desk go. Height budgeting is at :436-503. |
| `src/superclaude/cli/observe/terminal.py` | `GLYPHS` (:30-34), `TerminalPolicy`, `resolve_policy`, and `make_console`, which pins `"standard"` (:121). Colour depth and ASCII frame glyphs go here. It is the only module allowed to touch `Console` or `NO_COLOR`. |
| `src/superclaude/cli/observe/theme.py` (new) | Role-to-style tables for each colour depth, as the spec decides. |
| `src/superclaude/cli/observe/commands.py` | The `--once --width` path (`export_text()`, :238-242) and `LiveScreen` (:257-279). The `shape` key (:265) needs the colour depth. The gate constants at :67 and :70 must stay untouched. |
| `src/superclaude/cli/observe/view.py` | Display literals and values (:64-107, :843-853, :946-949), the render-only `count_figure`, and the Part C text changes. |
| `src/superclaude/cli/observe/export.py` | Must not change. `record_text` and `snapshot_json` stay byte-identical. |
| `tests/observe/test_render.py`, `test_terminal.py`, `test_commands.py`, `test_view.py`, `conftest.py` | Pins that the work changes on purpose (:250-259 byte equality, :399-404 source guards, `test_commands.py:121` no ESC in one-shot output, `test_terminal.py:181-198` source scan). |
| `tests/observe/golden_release1_surface.json`, `release1_surface.py`, `golden_questions_linkoff.json`, `test_linkoff_screen_reference.py` | Goldens. Split the records part off first; re-baseline the presentation goldens only in the commits that change them. |
| `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md` | The rendering contract. Lines 17, 20, 25, 33, 41, 57, 61 and 70 are edited in P7; line 43 stays stacked. |
| `.dev/issues/409/attachments/{signal-bridge,attention-ledger,decision-desk}.png`, `.dev/issues/409/orca-observer-design-package.zip` | Mockup references. The text and ANSI exports are inside the zip under `orca-observer-20261106/exports/<w>/` and `agent-focus/exports/<w>/`. |
| `.dev/issues/409/visual-parity/` (local only: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/`) | The spec's working folder: inputs, findings rounds, layout prototypes, and the harness and rubric to be written. It is not on GitHub today. |
| Issue #606 comments (REDESIGN-SPEC parts 1-3, owner rulings) | The plan of record. Assemble it with the body's `jq` command into `.dev/issues/409/visual-parity/REDESIGN-SPEC.md`. |
| Zellij 0.44.2 (`/usr/local/bin/zellij`, `~/.config/zellij/`) | An optional manual check only (step 7.4). It is not a dependency. |
| Playwright MCP browser | Optional PNG rasterising for the render gate. The fallback is a text and ANSI comparison. |
| `origin/integration` (6.0.0 removals) | 13 of the 21 recently merged pull requests landed there. None touch the observer, and `observe` stays registered in `main.py`. |

Estimate basis: 8 phases, each with a scripted render gate and up to 3 fix iterations. The work spans two areas (observer CLI code with its goldens, and the harness, rubric and spec documents) and adds a pty live test. That is well over 16 hours, so the issue rates `complex`.

## Analysis

- [analyze-observe.md](analysis/analyze-observe.md): `/sc:analyze --depth deep` of `src/superclaude/cli/observe/` and `tests/observe/` on `origin/master` 3fb35a5ae. It has 12 findings (3 High, 6 Medium, 3 Low), the blast radius and an order of work.
- [accuracy-check.md](accuracy-check.md): verdict `out_of_date`. All code claims still hold, but the evidence trail and the Phase 0 inputs are not on any branch on GitHub.
