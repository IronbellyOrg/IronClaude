# /sc:analyze: observer presentation layer (issue #606)

- Command: `/sc:analyze src/superclaude/cli/observe/ tests/observe/ --focus architecture --depth deep` (run by following `~/.claude/commands/sc/analyze.md`)
- Target revision: `origin/master` at 3fb35a5ae02c6e6950334c990e3c03878b80b5b8. Every file was read with `git show origin/master:<path>`. The current checkout (`docs/409-orca-dashboard-designs`) has no `src/superclaude/cli/observe/`, so the working tree was not used. `origin/integration` (ccd724c6b) has the same observer files (`git diff --stat origin/master origin/integration -- src/superclaude/cli/observe tests/observe` is empty).
- Scope: the presentation path that #606 changes (`render.py`, `terminal.py`, `commands.py` one-shot and live paths, `view.py` display literals, `export.py` as a do-not-touch boundary) and the tests and goldens that pin it.
- Method: static reading only. No tests were run, no screens were rendered, and no source was modified.

Codegraph: index_state=unavailable, checked_at=2026-11-18T04:26:00Z; degraded: graph:unavailable (this worker has no codegraph tools, and the checkout has no observer code to index; Glob, Grep, Read and `git show` were used instead)

## 1. Layout and metrics

| File (`src/superclaude/cli/observe/`) | Lines | Role in #606 |
|---|---|---|
| `render.py` | 531 | All layout. It turns a `View` into `list[str]` (`screen_lines`) and then into a Rich `Group` of plain `Text` (`render`, :524-531). Every builder returns plain strings: `counts_lines` :94, `_columns` :155, `_row_line` :233, `_header_lines` :246, `_inspector_lines` :255, `_help_lines` :304, `_question_line` :311, `_desk_lines` :329, `_panel_lines` :359, `screen_lines` :390. |
| `terminal.py` | 160 | The only module that builds a `Console` or reads terminal facts (docstring :1-6, enforced by `tests/observe/test_terminal.py:181-198`). It holds `GLYPHS` :30-34, `TerminalPolicy` :38-51, `resolve_policy` :73-92, `make_console` :110-125 (`color_system` :121, `safe_box=policy.ascii` :123), `ascii_safe` :133-135 and `clip` :138-160. |
| `commands.py` | 500 | The one-shot width-bound path (:238-242, `export_text()` without styles) and `LiveScreen` (:257-279, `Live(screen=True)`). Its rebuild key is `shape = (width, height, ascii, no_color)` at :265. |
| `view.py` | 1204 | Every screen literal and display value: the question-panel literals :64-83, the desk literals :85-99, `UNAVAILABLE` :100, `text_of` :377-385, row display :481-518, desk session fields :843-853 and the COUNTS tokens :946-949. |
| `export.py` | 274 | `record_text` and `snapshot_json`. The spec says this file must not change. |
| `parse.py` | 835 | `ASK_CAP` :475 and :503, and the link vocabulary :468-472. Read-only context for #606. |

Tests: 22 test modules in `tests/observe/` with 454 `def test_` functions before parametrisation. The spec's baseline, 766 passed, counts after parametrisation; it was not re-run here. The largest files touched by #606 are `test_view.py` (1383 lines), `test_render.py` (1022), `test_commands.py` (881), `conftest.py` (353) and `test_terminal.py` (198). Goldens: `golden_release1_surface.json` (546 lines; written by `release1_surface.py`) and `golden_questions_linkoff.json` (158 lines; read by `test_linkoff_screen_reference.py`).

## 2. How a screen is drawn today

1. `view.py` builds a `View`, which holds every literal and every display value.
2. `render.screen_lines(view, policy)` lays the screen out as plain strings. Height is budgeted by counting list lengths (`render.py:438-457` for the questions panel and desk, `:499-503` for the ledger).
3. `render.render()` wraps each string in `Text(line, no_wrap=True, overflow="crop")`. No string carries a style, a role or a span.
4. There are two output paths. The live screen (`LiveScreen.draw`, `commands.py:264-274`) prints the `Group` through `make_console(policy)`, which is where colour would appear. The `--once --width` path (`commands.py:238-242`) prints to a recording console and returns `export_text()`, which removes styles. The plain `--once` path returns `record_text(view)`.

Because nothing is styled today, the colour-enabled and NO_COLOR outputs are byte-identical. `tests/observe/test_render.py:250-259` asserts this, and `release1_surface.py:60` freezes the colour-enabled printed bytes in the golden.

## 3. Findings

Severity is the effect on the #606 work: how likely it is to break the work, or the work to break something, when it is not handled.

| ID | Severity | Domain | Finding | Evidence | Recommendation |
|---|---|---|---|---|---|
| A-1 | High | Architecture | The layout model holds plain strings only. Colour needs a role on each run of characters, and that role is lost at the first string join. About ten builders join cells, tokens and labels into one string (`_row_line` :243, `counts_lines` :111, `_question_line` :326, `_desk_lines` :348). | `render.py:233-243`, `:94-135`, `:311-326`, `:329-356`, `:524-531` | Follow the spec's `Line` layer (plain text plus role spans), built at each builder. `render()` must still return one `Text` per line, so that `test_render.py:399` (`len(group.renderables) == len(screen_lines(...))`) keeps holding. Do not use Rich `Panel`, `Table`, `Layout` or `Columns`: they change the renderable count, and the source scan at `test_render.py:400-404` forbids `Console(` and `from_markup` in `render.py`. |
| A-2 | High | Correctness | Height is budgeted by counting lines. Every frame adds two rows, and `Live(screen=True)` silently crops rows from the bottom, so the footer keys disappear first. The `spare` formula has three bare `+ 1` terms with no comment saying what each one counts. | `render.py:441-457` (`+ 1` at :453-455), `:499-503`, `commands.py:269-271` | Count every border row inside the builders whose output feeds `len(...)`. Add the height matrix test (8, 12, 24, 40, 44) before frames land (spec step 0.7). Assert the last row in a pty test. Read `render.py:444-445` before touching `spare`. |
| A-3 | High | Tests and goldens | Adding any style changes the colour-enabled bytes even when the text stays the same. A colour system is passed explicitly (`terminal.py:121`), so Rich writes SGR codes even to a `StringIO`; `test_terminal.py:47-51` relies on this. Three things break together: `test_render.py:256`, `golden_release1_surface.json` `printed_<w>`, and the T47 "byte-identical with release 1" meaning of that golden. The same golden also holds `record_text` and `snapshot_json`, which must not change. | `release1_surface.py:41-62`, `test_render.py:45-52`, `:250-259` | Split the records part (`record_text`, `snapshot_json`, headers) into its own golden that is never regenerated, before any style lands (spec step 2.1). After that, compare text after SGR removal instead of bytes, and regenerate the presentation goldens only in the commit that changes them. |
| A-4 | Medium | Correctness (ASCII) | `ascii_safe` maps every non-ASCII character to `?`, and `safe_box=policy.ascii` affects only Rich box objects, which this renderer does not use. A box character written as a string literal therefore becomes `?` in ASCII mode, breaking guard G-1. | `terminal.py:30-34`, `:123`, `:133-135`, `render.py:64-65` | Add each frame and block glyph to `GLYPHS` with its ASCII form (`+`, `-`, `\|`, `#`), and always draw them through `glyph()`. Add a test that the ASCII pass is pure ASCII and contains no `?` where a border belongs. |
| A-5 | Medium | Architecture (colour depth) | `TerminalPolicy` has no colour-depth field, and `make_console` pins `"standard"`. Depth detection (`COLORTERM`, `TERM`) must live in `terminal.py`, because `test_terminal.py:181-198` fails any other module that contains `Console(` or `NO_COLOR` as text, including in a docstring or comment. `LiveScreen` rebuilds its console only when `shape` changes, and `shape` holds no depth. | `terminal.py:38-43`, `:73-92`, `:121`, `commands.py:265`, `test_terminal.py:183-189` | Add `color_system` to `TerminalPolicy`, resolve it in `resolve_policy` from explicit `env` inputs (the function already takes `env`), and add it to the `shape` tuple. A new `theme.py` must hold only role-to-style tables and must not mention `NO_COLOR` or build a `Console`. Cache styles per `(role, depth)`. |
| A-6 | Medium | Output paths | The `--once --width` path calls `export_text()`, which removes styles, and `test_commands.py:121` asserts no escape byte. A styled one-shot capture therefore needs a separate path (`console.file.getvalue()`), and `export_text(styles=True)` must not be used as proof of colour: it ignores NO_COLOR and the depth downgrade. | `commands.py:238-242`, `test_commands.py:121`, `test_terminal.py:29-34` | Keep D-4's default: piped one-shot output stays plain. Prove colour on the live path with a pty test, using `pexpect>=4.9`, already declared at `pyproject.toml:41`; `tests/observe/spike_child.py` is a working `Live(screen=True)` child to copy from. |
| A-7 | Medium | Process | The spec's Phase 0 harness builds on `VP/inputs/tools/render_current.py` and the `VP/inputs/current/` captures. These files exist only untracked in `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/`, not on any branch on GitHub. | `accuracy-check.md` rows 1-5 | Before `/sc:workflow` runs, push `VP/inputs/` (and the research report, if it is wanted) to a branch, or plan to rebuild `render_current.py` from the fixtures in `src/superclaude/cli/observe/fixtures/`. The mockups themselves are on master inside `.dev/issues/409/orca-observer-design-package.zip`. |
| A-8 | Medium | Rendering defect (M-10) | Compact column headings exist but are not printed. `_columns` names `kind`, `dispatchId`, `liveness`, `age` and `flags` for the `line` and `short` classes, but the header is printed only at full width. | `render.py:193-230`, `:497-498` | Print a short heading at every width, and count it in `reserved` (`render.py:499-501`). |
| A-9 | Medium | Rendering defect (M-11) | With questions off, the key list is clipped, so `q quit` is lost at 80 columns. With questions on, it is wrapped. | `render.py:304-308` | Wrap between key groups in both cases. Keep the link-off keys literal pinned by `test_linkoff_screen_reference.py:34-37` and `:67-69`. |
| A-10 | Low | Rendering defect (M-16) | When the COUNTS strip runs out of room, the last low-priority token is cut mid-token with `>`. | `render.py:127-132` | Drop whole tokens and show a count of what is hidden. Protected tokens already wrap (:115-121). |
| A-11 | Low | Layout (M-17) | At 116 the id column takes up to 60 cells, and at 80 it takes the rest of the line, which leaves a wide blank band for short ids. | `render.py:195`, `:215` | This is optional. Column positions must not move between refreshes. |
| A-12 | Low | Data boundary | The desk cuts the question to 4 lines (`DESK_TEXT_LINES`), and the parser has already cut it at `ASK_CAP = 400`. A trailing hash can be lost in either place. The owner has since ruled that a hash is never shown on screen, so this only matters for the inspector. | `view.py:99`, `render.py:340-345`, `parse.py:475`, `:503` | Pin today's behaviour with a test (spec RB-27). Change neither cap without decision D-6. |

### Security and real-data rules

- Injection: text reaches `Text` as data. The console sets `markup=False`, `emoji=False` and `highlight=False` (`terminal.py:118-120`), and `render.py` may not contain `from_markup` (`test_render.py:401-402`). Styling must keep this property: apply styles as `Text` spans or `Style` objects, and never build markup strings from source text. The `injection` fixture and `test_sanitize.py` already cover control characters.
- Read-only: `render.py` imports neither the adapter nor the collector (`test_render.py:401-402`), and `export.py` is the only writer of records. The redesign adds no data path. The spec's `count_figure` field must not be read by `export.py`; add the source-scan test the spec names.

### Performance

Rendering is cheap: fewer than 200 lines per frame, with no I/O in `render.py`. The only real cost to manage is Rich `Style` parsing, so cache styles per `(role, depth)` (risk in spec section 9). Building two columns with `zip_longest` over lists of lines costs O(rows) per frame. Nothing here needs measuring before the work starts.

## 4. Recommendations, in order

1. Make the Phase 0 inputs reachable first (A-7). Without them the harness cannot be built as specified.
2. Split the golden before any change to its bytes (A-3). The records golden must never be regenerated.
3. Add colour depth in `terminal.py` with the source-scan rule in mind (A-5). Then add the `Line` and role-span layer to `render.py` with no text change (A-1). Prove colour on the live path with a pty test, not with `export_text(styles=True)` (A-6).
4. Fix the plain-text defects (A-8 to A-10) while the goldens are being re-baselined.
5. Add frames only after the height matrix test exists (A-2), and draw every glyph through `GLYPHS` (A-4).
6. Build the two-column desk last. It touches the most budgeting code (`render.py:436-479`).

## 5. Blast radius of the planned change

| Area | Files the redesign must reach |
|---|---|
| Source | `terminal.py` (policy depth, glyphs), new `theme.py`, `render.py` (all builders), `commands.py` (shape tuple; optional styled one-shot), `view.py` (render-only `count_figure`, Part C text changes). `export.py` and `parse.py`: no change. |
| Tests | `test_render.py` (byte equality :250-259, row-format pins :653 and :930-940), `test_terminal.py` (:40-51 and the source scan :181-198), `test_commands.py` (:121, :670-691 line-equality checks against framed output), `test_view.py`, `test_question_cap.py`, `test_inspector_scroll.py`, `conftest.py` (frame-aware helpers), plus new pty, theme, height and styled-capture tests. |
| Goldens | `golden_release1_surface.json` and its writer `release1_surface.py` (split, then presentation re-baseline). `golden_questions_linkoff.json` and its writer `capture()` in `test_linkoff_screen_reference.py:50-64` (re-baselined in P2 to P4). |
| Spec | `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md` lines 17, 20, 25, 33, 41, 57, 61 and 70 (P7). |
