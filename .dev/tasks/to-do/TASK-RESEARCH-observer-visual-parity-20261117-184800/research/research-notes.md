# Research Notes: observer visual-parity redesign (issue #606)

**Status:** Complete
**Date:** 2026-11-17
**Scenario:** A (explicit request: goal, code locations, output type and seven questions are given)
**Depth Tier:** Standard (3-5 codebase agents, 1-2 web agents; QA intensity standard)
**Task directory:** `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/`
**Worktree root (all paths below are relative to it):** `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/`

**Goal:** research how to redesign the read-only Orca terminal observer (`superclaude observe`) presentation to reach theme, styling and layout parity with its design mockups, driven by the merged findings list `.dev/issues/409/visual-parity/merged/FINDINGS.md` (M-01 to M-18, guards G-1 and G-2, accepted divergences AD-1 to AD-7, open items OPEN-1 to OPEN-3, owner decision O-1).
**Why:** the report feeds a phased redesign spec with a render gate per phase (implement, render at 160/116/80, a fresh reviewer scores a fixed rubric against the mockup, fix, re-render; at most 3 iterations per phase). A later agent turns the spec into a tasklist with `/sc:workflow`.
**Output type:** options and an implementation plan (phased), with a Zellij go or no-go, an ANSI colour-depth decision and a render-harness choice.

---

## EXISTING_FILES

Line counts measured 2026-11-17 (`wc -l`).

| Path | Lines | Purpose (from scope discovery; agents must verify) |
|---|---|---|
| `src/superclaude/cli/observe/render.py` | 531 | Builds screen lines and the Rich renderable: `screen_lines`, `render`, `_panel_lines`, `_desk_lines`, `_question_line`, `_help_lines`, `_columns`, `_header_lines`, `wrap`, `clip`. Today every line becomes `Text(line, no_wrap=True, overflow="crop")` (line ~524-529). Header gate `width_class == "full"` at ~line 497. Desk and panel notes order at ~365-387. |
| `src/superclaude/cli/observe/view.py` | 1204 | View model: `build_view`, `Session`, `Key`, `apply_key`, `QuestionLine`, `DeskView`, `QuestionsPanel`, constants `DESK_*`, `QUESTIONS_LINK_KEYS_LINE`, ledger title, counts strip, help line. Decides which text lines exist. |
| `src/superclaude/cli/observe/terminal.py` | 160 | `TerminalPolicy`, `resolve_policy` (width class full/line/narrow, `no_color`, ascii), `GLYPHS` (selected, truncate, hrule), `ascii_safe` (`?` substitution), `safe_box`, `make_console` (`color_system=None if policy.no_color else "standard"`, line ~121). |
| `src/superclaude/cli/observe/commands.py` | 500 | Command entry, `LiveScreen` (line ~257, draws the renderable directly), one-shot width-bound output via `console.export_text()` (line ~242, no styles requested), `QUESTION_LINK_PASSED` gate constant. |
| `src/superclaude/cli/observe/collector.py` | 361 | `Collector` with `questions=` and `link=` parameters; produces the data the view reads. |
| `src/superclaude/cli/observe/export.py` | 274 | Text record and JSON snapshot writers; record suffix ` | dispatchId=<id> | link=<state>`; question text must never be written. |
| `src/superclaude/cli/observe/keys.py`, `parse.py`, `adapter.py`, `questions.py`, `sanitize.py` | 235, 835, 512, 142, 48 | Key input, parsing of Orca output, adapter, question rows, sanitising of untrusted text. Context only; not expected to change. |
| `tests/observe/` (28 .py files plus 2 goldens) | n/a | `test_render.py`, `test_terminal.py`, `test_commands.py`, `test_view.py`, `test_export.py`, `test_snapshot_schema.py`, `test_golden_contract.py`, `test_linkoff_screen_reference.py`, `release1_surface.py`, `record_golden*.py`, `conftest.py` (helpers `make_rows`, `make_question_rows`, `question_payload`, `make_envelope`, `FakeClock`, `FakeRunner`), goldens `golden_release1_surface.json` and `golden_questions_linkoff.json`. |
| `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md` | n/a | Current rendering contract (cited by line in the findings: 13, 17, 20, 21, 25, 30-33, 38-50, 57, 61, 70, 93). |
| `.dev/issues/409/visual-parity/inputs/` | n/a | `mockups/{160,116,80}/{signal-bridge,agent-focus-attention-ledger,decision-desk}.{txt,ansi,png}`; `current/{160,116,80}/{ledger,questions,desk,ansi-*}.txt`; `tools/render_current.py` (run `PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 uv run python <script>`). |
| `.dev/issues/409/attachments/` | n/a | `signal-bridge.png`, `attention-ledger.png`, `decision-desk.png`. |
| `.dev/issues/409/visual-parity/merged/FINDINGS.md` | n/a | The merged findings list (input to this research). |
| `~/.config/zellij/config.kdl`, `themes/aidev02.kdl`, `layouts/agent.kdl`, `layouts/default.kdl`; `/usr/local/bin/zellij` 0.44.2 | n/a | Installed Zellij setup, read-only; `zellij setup --check` reports the config well defined. |
| `.dev/issues/409/pr-591-comment.md` | n/a | PR #591 consideration 8: add one fixture question with a 64-character hex hash and file paths; check the 80-column desk frame wraps or cuts it cleanly. |

**Environment facts (measured):** no `PIL`, `cairosvg`, `pyte`, `playwright` or `fontTools` Python module in the project environment; none of chromium, google-chrome, rsvg-convert, inkscape, ImageMagick `convert` or `cairosvg` on PATH. A Playwright MCP browser tool exists in the Claude session but is not part of the repository. The Rich package has no `__version__` attribute (find its version through package metadata). `unzip` is not installed (use Python `zipfile`).

## PATTERNS_AND_CONVENTIONS

- One text line becomes one unstyled `Text`; the screen is produced by `screen_lines(view, policy)` and then `render(view, policy)`; `emit()` in `render_current.py` uses the same two calls.
- Gate constants with pinned-regex tests (`QUESTION_GATE_PASSED`, `QUESTION_LINK_PASSED`); a golden that pins exact screen lines (`golden_questions_linkoff.json`) and a release-1 golden holding screen lines, printed bytes, plain records and JSON snapshots (`golden_release1_surface.json`).
- Existing tests compare colour-enabled and NO_COLOR printed bytes for equality (to be changed deliberately when styling arrives; the text content must stay equal).
- ASCII mode and colour are independent policy decisions in `terminal.py`.
- Untrusted text passes through `sanitize.py` and `ascii_safe`.
- Tests run with `uv run pytest tests/observe/ -v`; Python via `uv run` only; installed-primitive path rules do not apply (this is package code).

## SOLUTION_RESEARCH

Approaches to evaluate (the codebase agents gather the facts; the synthesis writes the options):

| Id | Approach to the pane, tile and column composition | Notes to verify |
|---|---|---|
| A | Hand-built lines: extend `_panel_lines` and `_desk_lines` to draw box characters and composed columns as plain strings, then a separate styling pass that maps spans to Rich styles | Keeps `screen_lines` text identical for goldens; width maths by hand (`cell_len`); ASCII box mapping by hand. |
| B | Rich renderables (`Panel`, `Table`, `Columns`, `Layout`) assembled in `render()` | Rich handles width and box styles (`box.HEAVY`, `box.ROUNDED`, `box.ASCII`); but `screen_lines` (the text contract used by tests, goldens, records) must still be derivable; check how `Console.export_text` and a recorded console reproduce it. |
| C | Hybrid: line-based text model stays the source of truth; a style map (per line or per span) is produced alongside; Rich draws it | Smallest golden churn; single place for the theme. |

Questions: Q1 (composition inside the line pipeline), Q2 (tests and goldens per phase), Q3 (render-to-image harness and reviewer rubric), Q4 (ANSI colour depth), Q5 (live path vs one-shot path), Q6 (Zellij go or no-go), Q7 (the 64-hex-character fixture at 80 columns). Harness options for Q3: Rich `export_svg` or `export_html` rendered by a headless browser (the Playwright MCP tool in the session; nothing in the project environment), ANSI to PNG with a tool that must be installed (to verify and cost), or text and ANSI-escape assertions plus a model-judged rubric that views the mockup PNGs and a rendered image or the text and ANSI exports. Whatever is chosen must also work offline in CI or say so.

## RECOMMENDED_OUTPUTS

All under the task directory:

- Research: `research/01-render-view-terminal-pipeline.md`, `research/02-live-screen-commands-export.md`, `research/03-tests-goldens-fixtures.md`, `research/04-spec-mockups-and-findings.md`, `research/05-zellij-and-render-harness-environment.md`; web: `research/web-01-rich-composition-and-colour.md`, `research/web-02-zellij-and-terminal-capture.md`.
- Synthesis: `synthesis/synth-01-problem-current-state.md` (sections 1, 2), `synthesis/synth-02-target-gaps.md` (3, 4), `synthesis/synth-03-external-findings.md` (5), `synthesis/synth-04-options-recommendation.md` (6, 7), `synthesis/synth-05-implementation-plan.md` (8), `synthesis/synth-06-questions-evidence.md` (9, 10).
- Final: `RESEARCH-REPORT-observer-visual-parity.md`; gaps log `gaps-and-questions.md`.

## SUGGESTED_PHASES

Phase 2 investigation agents (spawn in parallel; each writes incrementally):

| # | Type | Topic | Files | Output |
|---|---|---|---|---|
| 1 | Code Tracer | How the screen text is built and drawn today; where styles, panes, tiles and columns could be added; width and height budgets at 160/116/80; ASCII and NO_COLOR paths; colour system and glyph table (Q1, Q4, Q7 part, findings M-01 to M-18) | `src/superclaude/cli/observe/render.py`, `view.py`, `terminal.py`, `sanitize.py` | `research/01-render-view-terminal-pipeline.md` |
| 2 | Code Tracer | Live screen path versus one-shot path, `export_text`, `LiveScreen`, console construction, which console options keep styles; export record and JSON snapshot contract; collector link and question flow (Q5, screen-only question text) | `commands.py`, `export.py`, `collector.py`, `questions.py`, `keys.py` | `research/02-live-screen-commands-export.md` |
| 3 | Code Tracer | Tests and goldens: which tests assert screen text, printed bytes, records and snapshots; what must change per phase; how `release1_surface.py`, `record_golden*.py` and the two goldens are produced and pinned; the fixtures and helpers; where a 64-hex-character question fixture fits (Q2, Q7) | `tests/observe/**` (28 files, two goldens) | `research/03-tests-goldens-fixtures.md` |
| 4 | Doc Analyst | The rendering spec and what each merged finding needs from it (which spec lines change, which are guards, which conflict with O-1); decode the mockup `.ansi` colour roles and pane geometry at the three widths; map every finding M-01 to M-18 to the code location that must change | `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md` and other spec files in that folder, `.dev/issues/409/visual-parity/merged/FINDINGS.md`, `.dev/issues/409/visual-parity/inputs/**`, `.dev/issues/409/pr-591-comment.md` | `research/04-spec-mockups-and-findings.md` |
| 5 | Integration Mapper | Zellij and the render harness: read the installed Zellij config, theme and layouts; list what Zellij 0.44.2 offers (pane and layout composition, floating panes, tab and status bars, `zellij action dump-screen`, themes) from the CLI help and files; what tools exist offline for rendering ANSI or SVG to an image in this repo and environment; how `render_current.py` could become the Phase 0 harness (Q3, Q6) | `~/.config/zellij/**`, `/usr/local/bin/zellij` (CLI help only; do not start sessions that change user state), `.dev/issues/409/visual-parity/inputs/tools/render_current.py`, `pyproject.toml`, `Makefile` | `research/05-zellij-and-render-harness-environment.md` |

Web research agents (spawn in parallel; Tavily or Context7 first):

| # | Topic | Output |
|---|---|---|
| W1 | Rich composition and colour: `Panel`, `Table`, `Columns`, `Layout`, box styles including `box.ASCII`, `Text` span styles, `Console.color_system` auto-detection and the values (`standard`, `256`, `truecolor`), `COLORTERM`/`TERM` detection, `Console.export_svg`, `export_html`, `record=True`, `NO_COLOR` handling, `Live` and `screen=True` behaviour with styles | `research/web-01-rich-composition-and-colour.md` |
| W2 | Zellij: layout files (KDL), floating panes, `dump-screen`, run-from-layout commands, using a theme file; and offline ways to turn terminal output into an image for review (for example `freeze`, `termshot`, `ansi2html`, `aha`, headless-browser rendering of Rich SVG) with install cost and offline suitability | `research/web-02-zellij-and-terminal-capture.md` |

Synthesis mapping: standard table in the skill (six synth files).

## TEMPLATE_NOTES

Template 02 (complex task). QA intensity: standard. Gate 1 (research): 1 rf-analyst + 1 rf-qa + 1 rf-qa-qualitative. Gate 2 (synthesis): 1 rf-analyst + 1 rf-qa + 1 rf-qa-qualitative. Gate 3 (report): 3 structural + 3 content + 1 domain lens (finding-reproducibility). Gate 4 (fidelity): 2 agents. Gate 5 (anti-omission): 2 agents. Documentation is not verification: the merged findings list and the spec describe intent; every code claim needs a source-code read.

## AMBIGUITIES_FOR_USER

None. Intent is clear from the request and the codebase. Two items are left to the report as open questions, not asked now: O-1 (adopt two-column layouts, reversing the spec's stacked choice, owner decision recorded in the findings) and the three severity open items OPEN-1 to OPEN-3.
