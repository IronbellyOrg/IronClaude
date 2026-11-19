# Redesign spec: observer visual parity (issue #606, sub-issue of #409)

Status: ready to claim. Date: 2026-11-18 (owner layout ruling applied). Source of every number and file reference below: the research report `.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/RESEARCH-REPORT-observer-visual-parity.md` (the evidence trail) and the merged review findings `.dev/issues/409/visual-parity/merged/FINDINGS.md` (finding ids M-01 to M-18). Where this spec and the report differ, the report's Section 8 text copied in Part B governs, except that the owner's 2026-11-18 layout ruling (section 10, D-1) overrides the report's earlier two-column questions screen.

Part C (space diet, owner rulings 2026-11-18) sits between the summary and Part B and governs where they differ. Short names used below: `OBS` = `src/superclaude/cli/observe/`; `T` = `tests/observe/`; `VP` = `.dev/issues/409/visual-parity/`; `RR` = `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md`.

## 1. What to build, in one paragraph

Bring `superclaude observe` to the visual language of the three design mockups (Signal Bridge, Attention Ledger, Decision Desk) at 160, 116 and 80 columns: colour and weight from one named theme, boxed and titled panes, a two-column Decision Desk at 160 and 116 (stacked at 80), a stacked questions screen at every width with a prominent `SEEN IS NOT RESOLVED` count strip and a `RETAIN CONTEXT` pane, plus five plain-text defects of today's layout. Replicate the theme, styling and layout techniques, not the images. Keep the observer read-only, real data only, question text on screen only (never in the record or the JSON snapshot), no blinking, no mouse, no animation.

## 2. Rules that cannot change

- Do not edit `OBS/export.py`. `record_text` and `snapshot_json` stay byte-identical (the records golden added in Phase 2 proves it).
- Question text appears on screen only. Both hash canaries (record and snapshot) must keep passing from Phase 0 onward.
- NO_COLOR output contains zero escape bytes and the same text as the coloured output after SGR removal. ASCII output is pure ASCII with `+ - |` borders and `#` for the block glyph, never a `?` where a border belongs (guard G-1).
- The 16-colour theme must keep eight distinct role colours (guard G-2): Rich's automatic downgrade of the mockup RGB collapses muted, green, red and violet onto index 7, so the 16-colour table uses named ANSI colours.
- Facts the screen does not have are not drawn: no owner, requester, mapped-tree, SIGNALS bars or affected-session list (accepted divergences AD-1 to AD-8, section 6).
- Existing tests that read the source text must keep passing: `QUESTION_GATE_PASSED` and `QUESTION_LINK_PASSED` (commands.py:67, 70), the words `release-gates.md` and `Task 18` in commands.py (`T/test_commands.py:747-772`), no `Console(`, `from_markup`, `sorted(`, `.sort(` or adapter, collector, parse import in `render.py`, and `len(group.renderables) == len(screen_lines(...))` (`T/test_render.py:399`).
- Nothing under `.claude/` is ever staged. `.dev/tasks` is staged. The PR goes to `IronbellyOrg/IronClaude` through `/sc:pr-submit --monitor 3`, never to `SuperClaude-Org`.

## 3. Decisions this spec makes

| Topic | Decision | Why (short) |
|---|---|---|
| Composition | Keep the line-based text model as the source of truth. A `Line` (plain text plus role spans) layer records roles at the builders; `render()` still returns one Rich `Text` per line. Frames and columns are hand-built from `GLYPHS`. No Rich `Panel`, `Table`, `Layout` or `Columns` in `render()`. | Keeps `T/test_render.py:399`, the source guards, the record and the NO_COLOR text untouched; a Rich Panel does not give ASCII borders (`safe_box` has no effect, probed on Rich 15.0.0). |
| Render harness | Offline scripted checks on `console.file.getvalue()` captures, plus a fresh reviewer who scores a fixed rubric against the mockup PNGs. No new dependency. PNG rasterising is a session-only extra through the Playwright MCP browser, proven once in step 0.4. | No PNG tool is installed (no PIL, cairosvg, browsers); `export_text(styles=True)` ignores NO_COLOR and the colour downgrade, so it is never the capture. |
| ANSI colour depth | Decision D2 in two steps. Floor: eight named 16-colour roles (works everywhere). Then detect depth: `NO_COLOR` or `TERM=dumb` gives none; `COLORTERM=truecolor` or `24bit` gives truecolor (the mockup palette exactly); `TERM` ending `256color` gives 256-colour; otherwise 16-colour. One role table per depth in a new `OBS/theme.py`. Default owner choice D-5: all three depths. | Today `make_console` pins `color_system="standard"` (terminal.py:121) and nothing reads COLORTERM or TERM, so a truecolor terminal never sees the mockup palette. |
| Zellij 0.44.2 | Go as an optional layout and manual check only (Option Z2). No-go as a dependency of the observer or of the render gate. | See section 5. |
| Hash fixture | Phase 0 adds a synthetic plan-ask with a 64-hex-character hash and file paths. Owner ruling 2026-11-18: the hash is never shown on screen (Part C, step 2.12); the tests assert it is absent and that both record canaries still pass. | PR #591 consideration 8, superseded by the ruling. |
| Layout (owner ruling 2026-11-18) | The Decision Desk is two columns at 160 and 116 and stacked at 80. The questions screen is stacked at every width. | Evidence: the stacked-vs-two-column comparison comment on issue #606 (rows used: questions 11 stacked vs 17 two-column at 160, 12 vs 17 at 116; desk 23 vs 14 at 160, 23 vs 18 at 116). |

## 4. Findings the work closes

Severity as in `merged/FINDINGS.md` (High, Medium, Low). DEFECT means the code or spec is wrong today; PARITY-GAP means the mockup shows something the screen lacks. OPEN-1 to OPEN-3 are severities the two reviewers could not settle; they are treated as Medium (they gate the phase) until the owner rules.

| ID | Finding | Severity | Closing phase | Rubric row |
|---|---|---|---|---|
| M-01 | No colour or weight on any screen | High | P1 (frame and tile colours re-scored in P3, P4, P6) | RB-01, RB-09 |
| M-02 | No boxed, titled panes | High | P3 (questions, desk), P6 (ledger) | RB-02 |
| M-03 | Questions screen has no two-column layout | High | none: closed by owner ruling (AD-8, stacked kept) | RB-03 (stacked order) |
| M-04 | Decision Desk stacked, not two-column (owner ruled yes) | High | P5 | RB-03 |
| M-05 | `SEEN IS NOT RESOLVED` count has no visual weight | High | P4 | RB-04 |
| M-06 | Ledger has no attention slot or observation pane | Medium | P6 | RB-18 |
| M-07 | Caveats outweigh question rows (OPEN-1) | Medium | P4 | RB-16 |
| M-08 | Absent values not muted (DEFECT: the spec says muted) | Medium | P1 | RB-11 |
| M-09 | State values not coloured | Medium | P1 (ledger rows), P5 (desk fields) | RB-10 |
| M-10 | No column heading at 116 and 80 (DEFECT, ruling R-1) | Medium | P2 | RB-12 |
| M-11 | 80-column key list cut (DEFECT) | Medium | P2 | RB-13 |
| M-12 | Desk emphasis and alignment | Medium | P5 | RB-14 |
| M-13 | Title bar and READ ONLY badge (OPEN-3) | Medium | P2 | RB-15 |
| M-14 | No RETAIN CONTEXT pane (OPEN-2) | Medium | P4 | RB-17 |
| M-15 | Footer key pair split, no rule above footer | Low | P2 | RB-20 |
| M-16 | 80-column counts cut inside a token (DEFECT) | Low | P2 | RB-21 |
| M-17 | Wide blank band after the id column (optional) | Low | P2 | RB-22 |
| M-18 | Selected question has a glyph only | Low | P1 | RB-23 |

Totals: 18 findings; M-03 is closed by owner ruling AD-8, so 17 are fixed by code (4 High, 9 Medium, 4 Low); 2 guards (G-1 ASCII panes, G-2 colour depth); 8 accepted divergences; 3 open severities; the layout decision (D-1) is ruled.

## 5. Zellij go or no-go, with evidence

Recommendation: **conditional go, as an optional layout and manual check; no-go as a dependency.**

Evidence:
- The owner confirmed Zellij is installed and working in every workspace. Binary: `/usr/local/bin/zellij`, version 0.44.2, with a shipped config, theme `aidev02` and layouts `agent.kdl` and `default.kdl`.
- The research read the binary's help text and the official documentation only: Zellij sets the `ZELLIJ` environment variable in its panes, supports floating panes and command panes in layouts, and has `zellij action dump-screen` (with an `--ansi` form in current docs). The online docs describe a newer release than 0.44.2 (0.46.0 was announced 2026-11-11), so every flag must be checked with `--help` on 0.44.2 first.
- The observer already adapts to any pane size on each draw, and it is a plain Rich program that runs without Zellij. Zellij only wraps its output, so NO_COLOR and ASCII modes are unaffected.
- Not yet exercised in this research: a live session test of colour pass-through (truecolor and 256), wide-glyph fidelity of the box and block characters inside a Zellij pane, and `dump-screen --ansi` output on 0.44.2.

Conditions that must hold if Zellij is used: the observer works unchanged outside Zellij; read-only; all three widths; NO_COLOR and ASCII unchanged. It may read `ZELLIJ` as a hint, never as a requirement. Action: step 7.4 runs one manual session test and records the result in `VP/zellij-note.md`. It is not a phase gate.

## 6. Accepted divergences (not fix requests)

| ID | Mockup element | Why it stays different |
|---|---|---|
| AD-1 | Header "8 owners / 80 sessions / 80 mapped trees" | No owner or mapped-tree data; the COUNTS strip is the real-data equivalent (only its styling is in scope). |
| AD-2 | SIGNALS bars; SETTLED, POLICY FROZEN, UNKNOWN, STALE tiles | RR line 20 ("no bars, no health name") and line 93 (no verified settled mapping); muted `unavailable (no source)` stays. |
| AD-3 | Two-line register rows and prose lifecycle words | The spec requires separate raw fields and a verbatim `nextAction.kind` (RR lines 30-31). |
| AD-4 | Requester, owner, `Affected:` list, scope count, `4 sessions shown` | No such source; a shared worktree must not be read as affected sessions (RR line 57). One linked session is shown as one. |
| AD-5 | Different key map, no `tab pane` focus, worker ledger stays under the desk | RR lines 13, 21 and 39. |
| AD-6 | No `workerState` column at 80 (optional at 116) | Compact forms are fixed by RR line 33. |
| AD-7 | 80-column sentence "Questions stay until explicit resolution." and a forced focused card | It would promise more than the observer keeps (RR line 42: in memory, this process only). The truthful retention text wins. |
| AD-8 | Two-column questions screen with a right-hand count tile and context pane (attention-ledger mockup at 160 and 116) | Owner ruling 2026-11-18 after the stacked-vs-two-column comparison on #606: two columns cost 5 to 6 more rows, wrapped the question text at 116 and added no fact. The count weight (M-05) and the RETAIN CONTEXT grouping (M-14) are delivered inside the stack instead. |

## 7. Phase list

Every phase leaves `uv run pytest tests/observe/ -q` green (baseline 766 passed on 2026-11-17, plus tests each phase adds) and ends with its render gate (section 8). Detailed step tables, files, test edits and golden changes for each phase are in Part B.

| Phase | Name | What changes | Goldens | Findings |
|---|---|---|---|---|
| P0 | Render-compare harness, rubric, baseline, pinning tests | New harness `VP/tools/render_compare.py`, rubric, baseline score, Q7 hash fixture and tests, height test. No `src/` change. | none | prepares the gate for all |
| P1 | Colour depth, theme, role spans, styled-capture gates | `TerminalPolicy.color_system`, new `OBS/theme.py`, `Line` layer in `render.py`, styled one-shot path, pty live test. Style only, no text change. | none regenerated | M-01, M-08, M-18, M-09 (ledger), G-2 |
| P2 | Text and budget defects on existing layouts | Heading at 116 and 80, key list never cut, footer rule, counts never cut mid-token, title bar and badge. First split off a never-regenerated records golden. Then the Part C space diet (steps 2.9 to 2.15): each fact once, reasons once, no hash, aligned desk labels, status badge, ledger diet. | both presentation goldens re-baselined | M-10, M-11, M-13, M-15, M-16, M-17 |
| P3 | Frame primitive and single-column titled panes (questions-on screens) | Box glyphs with ASCII forms, `_frame`, inner-width threading, frame-aware test helpers, Q7 re-pin. | link-off golden regenerated | M-02 (questions, desk), G-1, Q7 |
| P4 | Count strip and RETAIN CONTEXT pane on the stacked questions screen (160 and 116; 80 unchanged) | `_count_strip`, `_retain_pane`, 3-row block-glyph font, one render-only field `count_figure`. | link-off golden regenerated | M-05, M-07, M-14 (M-03 closed by AD-8) |
| P5 | Decision Desk as question pane plus evidence pane (two columns at 160 and 116, stacked at 80) | `_two_columns` composer, aligned field lines, evidence pane titled `LINKED SESSION` (D-8). | none | M-04, M-12, M-09 (desk) |
| P6 | Ledger panes (questions off) | Attention pane, observation pane, framed worker table. Needs D-2. | release-1 presentation golden regenerated | M-06, M-02 (ledger) |
| P7 | Spec reconciliation, final gate matrix, PR | Edit RR lines 17, 20, 25, 33, 41, 57, 61, 70 (RR 43 stays stacked); optional Zellij check; full checks; `/sc:pr-submit --monitor 3`. | none | records the spec changes |

If the owner later rules two columns for the questions screen too, restore the earlier two-column Phase 4 (count tile and RETAIN pane in a right column) and drop AD-8; if stacked for the Decision Desk too, skip P5 and M-04 stays open.

## 8. Render gate (the last step of every phase)

Each phase is closed by an automated loop, not by the author's opinion.

1. **Implement** the phase steps; `uv run pytest tests/observe/ -v` is green.
2. **Render** with `uv run python .dev/issues/409/visual-parity/tools/render_compare.py --out <out>/<phase>/iter-<n> --check --heights 44,40,24,12,8`: screens `ledger`, `questions`, `desk`, `desk-planask` at widths 160, 116, 80 (heights 48, 42, 42), in five passes (truecolor, 256, 16-colour, NO_COLOR, ASCII), plus the text-only height matrix. `--check` writes `checks.json` with the script-checked rubric rows. A run without all five passes or without `--check` is not valid.
3. **Rasterise** each truecolor and 16-colour HTML through the Playwright MCP browser to a PNG (route proven in step 0.4). If that fails, the reviewer compares the text and ANSI files with the mockup text and ANSI files and uses the mockup PNG as the visual reference.
4. **Score.** Spawn one fresh reviewer subagent per width, with no resume and no author context. It gets only the rubric file, the reviewer prompt, the mockup PNGs and text for that width, and the rendered PNG, text, ANSI and `checks.json`. It returns `scores.json`: PASS or FAIL plus one evidence line per in-scope row.
5. **Fix and repeat.** Fix every failing High or Medium row, re-render, score again with a new reviewer. At most 3 iterations per phase.
6. **Close or stop.** A phase closes only when every High and Medium row in scope passes in the last iteration; Low rows pass or are logged as deferred. Escalate to the owner and stop (write `VP/scores/<phase>/stop.md` with the failing rows and the iteration scores, do not start the next phase) when a row still fails after iteration 3, or when two consecutive iterations do not improve the number of passing rows.

The fixed rubric (rows RB-01 to RB-23, written once in P0 to `VP/rubric/rubric.md`, never edited between phases) is in Part B, section 8.4.

## 9. Risks

| Risk | Effect | Handling |
|---|---|---|
| Frames add 2 rows each and `Live(screen=True)` crops silently from the bottom | The footer keys and the `shown x/y` line vanish with no warning | Every frame row is counted in the height budget; height test at 8, 12, 24, 40, 44 and the pty test asserts the last row (steps 0.7, 3.8) |
| Release-1 byte-identical golden meaning ends (T47) | Reviewers may think export changed | Records golden split off first and never regenerated (step 2.1); both presentation goldens regenerated only from the current tree in the same commit as the change |
| The Decision Desk two-column layout reverses RR 57 (stacked desk) | Spec and code disagree | RR 57 edited in P7; RR 43 (questions stacked) stays as written |
| 16-colour collapse | State colours indistinguishable on 16-colour terminals | Named ANSI roles, test of eight distinct roles, state word always printed (G-2, RB-09, RB-10) |
| Rich caches ANSI codes on a `Style` | A later depth in the same test process shows stale codes | Styles cached per `(role, depth)` in `theme.py` |
| Box and block glyphs may be two cells wide in some terminals (East-Asian ambiguous width) | Frames misalign | Rich's `cell_len` counts them as one; carried as a caveat; ASCII mode is the fallback |
| The 160-column table already uses all 160 cells | A border needs 2 cells from `flags` | Measure first (step 6.1); fallback keeps the 160-column table unframed under a titled rule |
| 4-line desk cap and 400-character ask cap | A hash that trails a long path is cut | Pinned as today's behaviour with a test; changing the caps is owner decision D-6 |
| PNG route and the live `LiveScreen` under a pty have not been run | Gate falls back to text and ANSI | Proven once in steps 0.4 and 1.6(g); fallbacks written into the steps |
| Reviewer subjectivity | Gate noise | Fixed rubric, script checks for every row they can cover, fresh reviewer each iteration, 3-iteration cap |
| `STATE_ROLE` colours are a display choice with no spec meaning (RR 93) | A colour could be read as a health verdict | Only the minimum table is coloured, the word is always printed, owner confirms in D-7 |

## 10. Owner decisions

The full table with defaults and the effect of each alternative is Part B, section 8.2. The defaults below apply unless the owner rules otherwise; none of them blocks starting P0 and P1.

| ID | Decision | Default |
|---|---|---|
| D-1 (O-1) | Two columns for the Decision Desk at 160 and 116; questions screen stays stacked | RULED 2026-11-18 (the split, owner, issue #606) |
| D-2 | Re-baseline questions-off and link-off goldens | Yes (records golden split off first) |
| D-3 | Severity of M-07, M-14, M-13 (OPEN-1 to OPEN-3) | Medium, gating |
| D-4 | Piped `--once --width` carries ANSI | No (keeps `T/test_commands.py:121`) |
| D-5 | Target colour depths | Truecolor, 256 and 16 with detection |
| D-6 | Show a plan hash | RULED 2026-11-18: never shown on screen (Part C). D-13 to D-16 also ruled yes (Part C, C.1) |
| D-7 | State word to colour table | Minimum table of step 1.4 |
| D-8 | Evidence pane title | `LINKED SESSION` |
| D-9 | Frame lines in `--once --width` output | Yes |
| D-10 | PNG renderer as a new dev dependency | No |
| D-11 | Reword RR line 61 against RR line 42 and AD-7 | Reword in P7 |
| D-12 | Keep bold and dim under NO_COLOR | No (keep `color_system=None`) |

## 11. Definition of done

The work is done when all of these hold; each is checked, not asserted.

1. Every phase P0 to P7 (P5 only while D-1 stays yes) has a render-gate record under `VP/scores/<phase>/` showing all High and Medium rows passing in the last iteration, within 3 iterations, or a stop log the owner has answered.
2. Finding map (all closed unless noted; Low rows may be logged as deferred):
   - M-01, M-08, M-18: colour, muted absent values and selected-row role are visible in the truecolor, 256 and 16-colour passes (RB-01, RB-09, RB-11, RB-23).
   - M-02: titled borders on the questions list, the Decision Desk and the ledger panes (RB-02); borders are `+ - |` in the ASCII pass (RB-07).
   - M-04: Decision Desk in two columns at 160 and 116, stacked at 80 (RB-03). M-03: not fixed by owner ruling; the questions screen is stacked at every width (AD-8).
   - M-05: count strip at 160 and 116 with the exact text form still in the plain pass (RB-04).
   - M-06: attention and observation panes on the ledger screen with no invented content (RB-18).
   - M-07, M-14: the question rows lead; run, caveat and retention lines are muted and grouped in the RETAIN CONTEXT pane, or relocated into the list pane when height forces the pane out (RB-16, RB-17).
   - M-09: ledger-row and desk-field state words carry the table role (RB-10).
   - M-10, M-11, M-13, M-15, M-16, M-17: heading at 116 and 80, key list uncut, badge, footer rule and pair intact, counts not cut mid-token, no wide blank band (RB-12, RB-13, RB-15, RB-20, RB-21, RB-22).
   - G-1: ASCII pass is pure ASCII with `+ - |` borders in every gate. G-2: eight distinct role colours at 16 colours (RB-09).
3. **Colour depth:** the spec's decision D2 is implemented and tested for NO_COLOR, `TERM=dumb`, COLORTERM truecolor, TERM 256color and none; ANSI-styled output is verified on the live screen path by the pty test and on the one-shot path by `_screen_text(styled=True)`, and the captures keep their styling.
4. **Hash (PR #591 consideration 8, as ruled):** a plan-ask with a 64-hex-character hash and file paths is rendered at 160, 116 and 80 columns on the questions screen and the Decision Desk (RB-27): no run of 32 or more hex characters appears, the rest of the ask is intact, no line exceeds the width. Both hash canaries (record and snapshot) pass.
5. **Zellij:** `VP/zellij-note.md` records one manual session test on 0.44.2, or records that the owner declined it; the observer runs unchanged outside Zellij.
6. `record_text`, `snapshot_json` and `OBS/export.py` are unchanged (`git diff --stat` shows no `export.py` change); the records golden passes; `count_figure` is not read by `export.py`.
7. Both presentation goldens were regenerated from the current tree only in the commits that moved them; neither golden contains an escape byte.
8. `uv run pytest tests/observe/ -v`, `make test` and `make lint` pass; no `.claude/` path is staged; `.dev/tasks` is staged.
9. RR lines 17, 20, 25, 33, 41, 57, 61 and 70 match the built screens (P7), with the D-8 title and the pane titles `OBSERVATION WINDOW` and `RETAIN CONTEXT` recorded. RR 43 (stacked questions screen) stays as written.
10. The PR was opened only by `/sc:pr-submit --monitor 3` against `IronbellyOrg/IronClaude`, rebased on `origin/master`, and the returned URL starts `https://github.com/IronbellyOrg/IronClaude/pull/`.

## 12. How the claiming agent starts

1. Save this spec to `.dev/issues/409/visual-parity/REDESIGN-SPEC.md` (the issue explains how to assemble it from the comments when it is not already on your branch).
2. Run `/sc:workflow @.dev/issues/409/visual-parity/REDESIGN-SPEC.md --depth standard --handoff none`.
3. Read the plan it prints. Then run `/sc:implement <the plan path it printed>`. Each phase ends with its render gate (section 8); do not start a phase before the previous gate closes.
4. Before pushing, rebase on `origin/master`. Open the PR only with `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."`.
5. Stop and ask the owner when a gate hits the 3-iteration cap or two non-improving iterations, or when a decision in section 10 is needed and its default does not fit.

---

# Part C: space diet (owner rulings 2026-11-18; governs over Part B where they differ)

Source: the two screen-space audits (`.dev/issues/409/visual-parity/layout-compare/space-audit.md` and `space-audit-2.md`, the second read the rendered images). Owner rule: visual flair may cost a little screen space; repeated, redundant or badly presented information may not. Owner answers: (1) never show the hash on screen; (2) to (5) accepted as recommended.

Conflicts: where Part B says the hash is shown whole (decision D-6, rubric row RB-19, steps 0.6, 3.7 and 5.5, the Q7 notes), Part C step 2.12 replaces it. Where Part B says the three status fields and `reason unknown` are printed per row, Part C replaces that. Part B step numbers are unchanged; Part C steps are added to Phase 2 and run after step 2.8's text fixes and before its render gate.

## C.1 Decisions

| ID | Decision | Ruling |
|---|---|---|
| D-6 (replaced) | The 64-hex hash | Never shown on the questions screen or the Decision Desk. Any run of 32 or more hexadecimal characters in on-screen question text is removed. No marker is left. |
| D-13 | Per-row `reason unknown` | Replaced by one title note `reasons: none in source`. A row shows a reason only when the source gave one. Yes. |
| D-14 | Status badge | One `ACTIVE` badge when dispatchStatus is `active`, terminalState is `active` and outcome is `none`; any other combination (including an absent value, shown as `unknown`) expands to three separate rows with raw values. Yes. |
| D-15 | Liveness dot | `●` coloured by state with one legend; any value that is not alive is spelled out; under NO_COLOR the word is printed. Yes. |
| D-16 | Rarely used fields | `source counts` (when unknown), `runs seen`, and the `msg_` id move to the inspector. Yes. |

Open point for the owner (default shown): does the inspector (Enter) and the export keep the full question text including the hash? Default: the inspector keeps the full text (it is on-demand and on screen only); the record and snapshot never contain question text (unchanged rule). Say "hide it everywhere on screen" to strip the inspector too.

Known cost, accepted by the ruling: two plan-approval questions that differ only by hash look the same on screen. The age and the linked session still tell them apart.

## C.2 Steps (added to Phase 2)

| Step | Action | Files | Details |
|---|---|---|---|
| 2.9 | Show each fact once | `OBS/render.py`, `OBS/view.py` | (a) Decision Desk: the full question text appears only in the desk pane; the selected list row for the same question is one line cut with `>` (RR 50, 57). (b) Run id appears once: in the count strip title area (Phase 4) or, before Phase 4, in the panel title row; the freshness header cell for the questions source becomes `questions OK 0s` without the Run (RR 44, 45, 54); the panel keeps its own first state line (RR 45). (c) The count appears once: figure, `seen, not resolved` and `closed by evidence: unavailable` in one tile or strip; the separate counts row and the tile title echo are removed; `(no source)` is dropped from `closed by evidence: unavailable` (RR 47; `record_text` still writes `counts_line` unchanged, so only the screen builder changes). (d) The `msg_` id leaves the desk pane (it stays in the inspector). (e) The second copy of the retention and `worker-reported, not questions` lines under the desk is dropped. |
| 2.10 | Questions first, caveats under | `OBS/render.py` | In the list pane the question rows come first, then the disclosure (verbatim, RR 49, never shortened, wraps at 80). `no read marker in source: answered questions stay listed` and the retention sentence stay verbatim (RR 48, 53) and are adjacent in one RETAIN CONTEXT pane (Phase 4) or, before it, adjacent lines. |
| 2.11 | Reasons once | `OBS/view.py`, `OBS/render.py`, `T/test_render.py` | Title note `reasons: none in source` (D-13). The row suffix `reason unknown` is printed only when the source gave a reason. The `^\s*\d+[smh]  ` row checks and the `reason unknown` counting checks (`T/test_render.py:453, 930-948`) are rewritten to the new form; `T/golden_questions_linkoff.json` is regenerated in the Phase 2 commit. If a reason is absent but cannot be told from "not given", the title states the unknown (the rule "unknown is not none" holds because the word `none in source` is a statement about the source, not about the world). RR 50 is edited. |
| 2.12 | No hash on screen | `OBS/view.py` (display text only), `T/test_render.py`, `T/conftest.py` | Add `strip_hex(text) -> str` used where `shown` and `DeskView.ask` are built: remove every run of 32 or more `[0-9a-fA-F]` characters and collapse the double space left behind. It runs on the display strings only; `ask`, `text` and everything the record or snapshot reads are untouched. Rewrite the Q7 tests of steps 0.6, 3.7 and 5.5: the 64-hex fixture asserts the hash is absent from every screen line at 160, 116 and 80 in the plain pass, the rest of the ask is intact, the screen still fits, and the hash canaries (record and snapshot) still pass. The trailing-hash fixture keeps its 4-line cut with `...`. RB-19 is replaced by RB-27 below. |
| 2.13 | Aligned labels, one status badge, plain words | `OBS/render.py` (`_field_lines`, step 5.2) | Desk and ledger status per D-14: aligned label column (about 9 cells), label words `session`, `state`, `alive`, `next`, `status`, `worktree` instead of raw field names; `alive` shows one value built from verdict, source and evidence age (for example `yes (terminal), 3s ago`); `worktree` reads `wt-1  (this session only)` (the full note moves to the inspector, RR 57). Absent values stay `unknown`, muted. The three raw rows keep their raw field names when expanded. RR 57 and 71 are edited. |
| 2.14 | Ledger diet | `OBS/render.py` (`_columns`, `_row_segments`, footer) | Merge dispatchStatus, terminalState and outcome into one `status` cell with the badge rule (RR 30). Replace the `alive (terminal)` text column with the dot and one legend line (D-15), spelling out any non-alive value in amber and under NO_COLOR. Drop the `flags` column and show the changed marker `*` in the first cell (RR 65). Drop the separator rule row and the `+N more` row above a footer that already says `shown n/N` (RR 76). Put the gap notice and `26 historical hidden (h)` on one row (RR 23). Header and footer: drop `mode=` and `as of` (RR 17), the second `scope=all`, and `collected` from the footer (RR 22); one dim token `no source: settled, frozen, cost` replaces the three `unavailable (no source)` tokens (RR 20, 81, 82); footer keys become `j/k move  Enter detail  / filter  n/p question  h history  e export  q quit` (the dropped keys still work). `source counts` (when unknown) and `runs seen` leave the screen for the inspector (D-16). |
| 2.15 | Re-run goldens and the gate | as step 2.7 | Regenerate both presentation goldens in the same commit; the records golden (step 2.1) stays untouched. Score rubric rows RB-24 to RB-29. |

Order inside Phase 2: 2.1 first, then 2.2 to 2.8, then 2.9 to 2.14, then 2.15 and the render gate. If this is too large for one phase, split it into Phase 2a (2.1 to 2.8) and Phase 2b (2.9 to 2.15), each with its own gate.

## C.3 Rubric rows added (same fixed-rubric rules as Part B 8.4)

| ID | Criterion | Severity | Checked by | In scope from |
|---|---|---|---|---|
| RB-24 | No fact is printed twice on a screen: for the `desk` and `questions` fixtures at each width, the question text, the Run id, the count words and the freshness state of a source each occur once (header and panel state line excepted as RR 45 requires). | Medium | Script (string census) | Phase 2 |
| RB-25 | Reasons: no `reason unknown` suffix on any question row when no reason is given; the title carries `reasons: none in source`; a row with a reason shows it. | Medium | Script | Phase 2 |
| RB-26 | Status: dispatch, terminal and outcome show as one `ACTIVE` badge only when they are `active`, `active`, `none`; any other combination, including an absent value (`unknown`), shows three separate raw rows. | High (safety: unknown is not none) | Script | Phase 2 |
| RB-27 | Hash: no run of 32 or more hexadecimal characters appears on the questions screen or the Decision Desk at any width; the rest of the ask is intact; both canaries pass. (Replaces RB-19.) | High | Script | Phase 2 |
| RB-28 | Ledger: no `flags` column, no rule row, no `+N more` row above a `shown n/N` footer; liveness is a dot with a legend, and any non-alive value is spelled out, also under NO_COLOR. | Medium | Script plus Reviewer | Phase 2 |
| RB-29 | Order and labels: question rows lead the list pane; desk labels are plain words with one aligned value column; no internal `msg_` id and no raw field name on the desk except in an expanded status row. | Medium | Reviewer | Phase 2 |

## C.4 Spec lines to edit in Phase 7 (added to step 7.1)

RR 17 (`mode=`, `as of`), 20, 81, 82 (the `no source` token), 22 (footer), 23, 30, 44, 45, 47, 48 and 53 (order and merge only, wording kept), 50 (reasons once), 57 (desk fields, note moved to the inspector), 65 (flags), 71 (status badge), 76 (`+N more`). Verbatim safety wording that stays: the disclosure (RR 49), `no read marker in source: answered questions stay listed`, the retention sentence, `worker-reported, not questions`, `collected n / reported T` and PARTIAL (RR 20), `seen, not resolved`, `closed by evidence: unavailable`.

## C.5 Not cut (all three audits agree)

`collected n / reported T` and PARTIAL, the `seen, not resolved` headline with `closed by evidence: unavailable`, `worker-reported, not questions` with the verbatim `nextAction.kind`, the question age and `[no longer in source window]`, and the Human questions gap notice.

---

# Part B: detailed plan (copied from the research report, Section 8)

The sections below are copied from `RESEARCH-REPORT-observer-visual-parity.md`, Section 8 (8.1 to 8.10), at the time this spec was written. They hold the step tables, files, golden and test changes, rubric, gate protocol and the finding-to-phase map. Read the report for the evidence behind each step (research files 01 to 05, web-01, web-02 and the synthesis files are listed in its Section 10). Mentions of "this plan" mean this spec. Owner ruling 2026-11-18: Phase 4 below is the stacked count strip and RETAIN pane (the earlier two-column questions layout is dropped, AD-8) and the two-column composer moved to step 5.0. All paths are relative to the repository root.

### 8.1 Planning decisions (answers to Q1 to Q7 that every phase relies on)

| Q | Decision used by this plan | Evidence | Status |
|---|---|---|---|
| Q1 composition | Keep the line model. Introduce a `Line` (plain string plus role spans) layer in `OBS/render.py`; `screen_lines()` becomes `[l.plain for l in _compose(...)]` so every plain-string test and golden keeps its meaning. Frames and two columns are hand-built from `Line` objects using new `GLYPHS` entries. `render()` still returns one `Text` per line. No Rich `Panel`, `Table`, `Layout` or `Columns` in `render()`. | `render()` is one `Text(no_wrap=True, overflow="crop")` per string (render.py:524-531); `T/test_render.py:399` pins `len(group.renderables) == len(screen_lines(...))`; `wrap`/`clip` own the `>` and `...` markers; height budgets count `list[str]` lengths (render.py:438-457, 499-503); `safe_box` does not ASCII-ize a Panel (probe, Rich 15.0.0). [CODE-VERIFIED] | Decided |
| Q2 phases | Seven phases, ordered by golden impact: P0 tests and harness only; P1 style only; P2 text and budget fixes; P3 single-column frames; P4 stacked count strip and RETAIN pane on the questions screen, P5 two-column Decision Desk (owner ruling D-1: questions stay stacked); P6 ledger frames; P7 spec reconciliation and final gate. | 03 section 6 (P0 to P5 grouping), with P2 and P6 added for the findings it does not cover. | Decided |
| Q3 harness | Standalone script `VP/tools/render_compare.py` built on `render_current.py`; no new dependency. Text and ANSI tier is machine-checked; PNG tier is made in the Claude session by opening Rich `export_html` output in the Playwright MCP browser; a fresh reviewer subagent scores a fixed rubric (8.4) against the mockup PNGs. | 05 sections 2, 4, 5, 6; web-02 B1, B2, B7 (external context). PNG route is untested. | Decided; PNG route [UNVERIFIED] until step 0.4 |
| Q4 colour depth | Add `TerminalPolicy.color_system` resolved in `resolve_policy` (`NO_COLOR` gives `None`; `COLORTERM` truecolor or 24bit gives `"truecolor"`; `TERM` ending `256color` gives `"256"`; otherwise `"standard"`). A new `OBS/theme.py` holds one explicit role table per depth; the 16-colour table uses named ANSI colours, not downgraded RGB. | `make_console` pins `"standard"` (terminal.py:121); the downgrade measured in 04 section 3 collapses muted, green, red and violet to index 7. [CODE-VERIFIED + probe] | Default; owner confirms target depths (8.2 table, D-5) |
| Q5 styled capture | One-shot path: replace `export_text()` (commands.py:242) with a helper that returns `console.file.getvalue()` when styled output is allowed, else `export_text()`. Live path: a pty test through `pexpect`. Gate tests in P1. | `export_text(styles=True)` bypasses NO_COLOR and the colour downgrade (probe, 02 section 2); a `StringIO` console writes nothing under `Live(screen=True)` (02 section 9.2). [CODE-VERIFIED] | Default; owner rules D-4 |
| Q6 Zellij | No-go as a render-harness dependency or observer dependency. The observer stays standalone. Zellij is an optional manual check in P7 only. | 05 section 7 (help text only, nothing exercised); web-02 A2, A5 (external context: Zellij sets `ZELLIJ`; docs are newer than the 0.44.2 binary). | Decided; runtime behaviour [UNVERIFIED] |
| Q7 hash fixture | Add the 64-hex plan-ask fixture in P0 (pins today's wrap), re-pin it in P3 for the framed 80-column desk. Rule, per surface: (1) in the desk question text, a token that fits the pane's inner width (64 or more cells at every planned width: 154/110/74 single column, 72/110/74 in P5) stays whole on its own wrapped line, but only if it falls inside the first four wrapped lines (`DESK_TEXT_LINES = 4`, view.py:99; render.py:341-345), where the fourth line is cut with `...`; a hash after that point is not shown, and the ask is already cut by `ASK_CAP = 400` at parse.py:503. So the hash is never split by wrap, and it is not guaranteed to appear. (2) In an evidence field a value wider than the pane's inner width minus 2 is hard-split with nothing lost and no marker (62 at 116 in P5, so a 64-cell `resource.worktreeId` splits there; whole at 160 and 80). | Probe: hash whole at 160, 116, 80; paths over the width hard-split mid-word (01 section 4.9; 03 section 5c); `_desk_lines` render.py:339-353 re-read. [CODE-VERIFIED] | Pinned as today's behaviour; owner rules D-6 on whether a cut hash is acceptable |

Data flow after the plan (text authority stays at the bottom; styles never feed the record or snapshot):

```
build_view -> View (plain strings only; adds one render-only field, P4)
                |-- record_text(view)   (export.py)  unchanged bytes
                |-- snapshot_json(view) (export.py)  unchanged bytes
                v
          _compose(view, policy, message) -> list[Line]   Line = plain str + role spans
                |-- screen_lines()  = [l.plain ...]       goldens, tests, --once without styles
                v
          render() -> Group(one Text per Line, spans -> theme.style_for(role, depth))
                v
          make_console(policy)  color_system = None | standard | 256 | truecolor
```

### 8.2 Owner decisions the plan depends on (defaults assumed, effect if different)

| ID | Decision | Default assumed | If the owner rules otherwise |
|---|---|---|---|
| D-1 (O-1) | Layout: two columns for the Decision Desk at 160 and 116; the questions screen stays stacked at every width | RULED 2026-11-18 (owner, issue #606): the split. Evidence: the stacked-vs-two-column comparison comment on #606 | If the owner later rules two columns for the questions screen too: restore the earlier P4 (two-column questions screen with count tile and RETAIN pane) and drop AD-8. If stacked for the Decision Desk too: skip P5, keep P3's stacked desk frames, M-04 stays open |
| D-2 (G-A) | Re-baseline the questions-off and link-off goldens | Yes, regenerate from the current tree; `.dev/issues/606/issue-body.md:84` lists the four files as deliberate presentation updates. [CODE-VERIFIED line] Record and snapshot keys are split into a never-regenerated golden first (step 2.1) | "Freeze questions-off": P2 and P6 apply only to questions-on screens; M-06, M-10, M-11, M-13 stay open for the questions-off screens |
| D-3 (OPEN-1 to OPEN-3) | Severity of M-07, M-14, M-13 | Treated as Medium (gating) until ruled | A Low ruling removes the item from the gate |
| D-4 (Q5) | Should a piped `--once --width` carry ANSI | No: styled bytes only when stdout is a tty and colour is allowed (keeps `T/test_commands.py:121` true) | A styled-by-default ruling changes `T/test_commands.py:121` in P1 |
| D-5 (Q4/G-2) | Target colour depths | Truecolor, 256 and 16 with detection | "16 only": steps 1.1 detection and the two higher tables are dropped |
| D-6 (Q7) | Show a plan hash in full | Keep today's rule: the hash is whole (never split by wrap) when it lies inside the first four wrapped lines of the question text; a hash beyond the 4-line cap or the 400-character ask cap is cut with `...` and is not shown. The plan changes no cap | "Never show a cut hash" needs a raised `DESK_TEXT_LINES` or a hash-aware cap (view.py:99, render.py:341-345, parse.py:503), a changed pinned test (step 0.6, second test) and a spec edit; a "cut with a visible mark" rule needs a new test and a view-level rule |
| D-7 | Mapping from real state words to colour roles (M-09) | The minimum fixed `STATE_ROLE` table in step 1.4: workerState `running`, liveness `alive` and `live` are running; workerState `succeeded` and dispatchStatus `completed` are settled; workerState `failed` and dispatchStatus `failed` are failed; the `FROZEN` flag is frozen; every other value uses the body role; the state word is always printed. The code and spec state no meaning for these words (RR 93), so this is a display default for the owner to confirm | Owner supplies the table; the step 1.4 table is replaced and RB-10 is scored against the owner's table (it must stay non-empty) |
| D-8 | Title of the Decision Desk evidence pane (the mockups say `AFFECTED SESSION EVIDENCE` and `AFFECTED SESSIONS`, which claim an affected-session list the code does not have, AD-4) | `LINKED SESSION` (reuses the existing link vocabulary, parse.py:468-472); step 5.1 | Any other title that does not claim an affected list needs only the `DESK_EVIDENCE_TITLE` constant and the tests that name it changed; a title that claims an affected list needs new view data first (AD-4) and a spec edit to RR line 57 |
| D-9 | May `--once --width` output include frame (box-drawing) lines? (OPEN in 4.1b, 7.3 and 9.2 row 8) | Yes: the one-shot prints the same framed lines as the live screen. Step 3.6 therefore rewrites `T/test_commands.py:672-675` and `:690` to read framed output through `title_of` and `unframe` | No: add a `frames: bool` switch to `_compose` that `run_once` (commands.py:238-242) sets false, selecting the P2 unframed stacked layout for `--once --width` (and none of the P4 and P5 two-column layouts there); `T/test_commands.py:672-675` and `:690` then stay unchanged, step 3.6 drops those two edits, and tests are parametrised over `frames` for the one-shot path; the live screen still frames |
| D-10 | PNG renderer as a new dev dependency (Q-7) | No dependency: the gate is the text and ANSI tier plus the reviewer reading the mockup PNG; the image tier is session-only through the Playwright MCP browser (step 0.4) | Name one tool (for example `freeze`, or `playwright install chromium`), add a dev extra in `pyproject.toml` and a Makefile target, and make gate step G3 a script step; the licence and install checks of 9.3 row 21 come first |
| D-11 | Reword RR line 61 (the 80-column invariant lines) against RR line 42 and AD-7 (G-H) | Reword RR 61 in the P7 spec edit (step 7.1) so it no longer requires "Questions stay until explicit resolution."; RR 42 keeps the retention wording; the plan builds neither invariant line | The owner instead requires the lines on the 80-column screen: a text step is added to P4 (new literal in view.py, both goldens re-baselined) and the RB-05 literal list gains them; or RR 42 is reworded and AD-7 is withdrawn |
| D-12 | Keep bold and dim under NO_COLOR? (9.2 row 7) | No: keep `color_system=None`, which drops bold and dim with colour (G-2); hierarchy lives in text and glyphs | Use `no_color=True` with a colour system so bold and dim survive: rewrite `T/test_terminal.py:40-51` and `T/test_render.py:985-987`, and RB-06 changes from "zero ESC bytes" to "no colour SGR" |

### 8.3 Geometry and height budgets (design target from 04 section 4, checked against code arithmetic from 01)

| Screen | 160 | 116 | 80 |
|---|---|---|---|
| Questions screen | stacked at every width (owner ruling D-1, AD-8): panes `width - 2` wide with margin 1; at 160 and 116 three panes (count strip, list, RETAIN CONTEXT) | same | one column, panes 78 wide, no strip and no RETAIN pane |
| Decision Desk | left 76 (question over list), right 80 (session evidence) (1+76+2+80+1=160) | question 114 full width over 66 + 46 (1+66+2+46+1=116) | three stacked panes 78 wide |
| Ledger | table keeps all 160 cells today (render.py:159-192); a border-only frame needs `flags` to give 2 cells | `line` layout, frame 114 | `short` layout, frame 78 |
| Inner width of a framed pane | pane width minus 4 (border plus one cell padding each side) | same | same |
| Frame row cost | 2 rows per frame (top and bottom border) | 2 | 2 |
| Harness height for scoring | 48 (mockup frame height) | 42 | 42 |
| Extra height matrix (text only) | 44, 40, 24, 12, 8 | same | same |

Height rule: every added row must be counted inside `screen_lines` (`top`, `body`, `footer_height`), because on `Live(screen=True)` rows past `policy.height` are dropped from the bottom, which are the footer keys and `shown x/y` (02 section 9). [CODE-VERIFIED] `base` and `len(desk)` at render.py:441-457 are measured from returned lists, so frame rows are counted automatically once `_panel_lines` and `_desk_lines` return framed lines; the three `+1` terms stay as they are (which `+1` is which is [UNVERIFIED]; read the comment at render.py:444-445 before editing).

### 8.4 Fixed rubric for every render gate (written once in P0 to `VP/rubric/rubric.md`; the wording is not edited between phases)

| ID | Criterion | Severity | Findings | Checked by | In scope from |
|---|---|---|---|---|---|
| RB-01 | Colour roles, measured on the truecolour `.ansi` by mapping each SGR foreground RGB to a role (palette: base 225,233,238; muted 165,182,194; slate 82,108,128; amber 250,178,25; cyan 112,205,226; green 139,215,175; red 240,141,150; violet 194,173,242; 04 section 2). Pass only if all hold: (a) every foreground colour in the file is one of the eight triples; (b) the `header1` title text is cyan and bold; (c) every question age (in the list and in the desk) is amber and bold, and every question-text line in the desk is amber and bold; in the list the question subject text is base colour and bold (`body_bold`, step 1.4, RB-16(a); 04 line 57: amber question text in the desks, base bold in the 160 ledger), never amber; the one selected list row is scored under the `selected` role (marker and line bold amber, step 1.4; an unverified design choice, no mockup shows a selected row) and is exempt from the base-colour subject rule but not from the amber-age rule; (d) the `header2` freshness line, the keys hint and the footer text are muted; (e) every secondary-pane border glyph and the footer rule is slate (not applicable before P3, when no border exists); (f) ledger cells that carry no state or absent value are base. One counter-example, quoted with its line number, fails the row | High | M-01 | Script (`checks.json` role census for (a)) plus Reviewer for (b) to (f) | P1 |
| RB-02 | Every pane the mockup frames has a titled border with the title inset in the top border: heavy amber for the attention pane, rounded slate for secondary panes, cyan for the count strip | High | M-02 | Reviewer | P3 (questions, desk), P6 (ledger) |
| RB-03 | Layout structure matches 8.3: the Decision Desk is two columns at 160 and 116 and stacked at 80; the questions screen is stacked at every width (strip, list, RETAIN CONTEXT in that order at 160 and 116; list only at 80) | High | M-04 (desk); M-03 is closed by AD-8 | Reviewer | P4 (questions order), P5 (desk) |
| RB-04 | Count strip, at 160 and 116 only (none at 80). Pass only if all hold: (a) the strip frame's border glyphs carry the cyan role and its top border holds the title `QUESTIONS_COUNT_LABEL.upper()`; (b) when the figure is drawable (digits or `+`) and fits, the figure occupies 3 consecutive rows made of the block glyph (`█`, ASCII `#`), otherwise it is one bold amber figure; either way the figure is the tallest text on the screen; (c) the plain pass contains `seen, not resolved: N \| closed by evidence: unavailable (no source)` whole on one line, with N equal to the figure; (d) at 80 columns no strip frame exists and (c) still holds | High | M-05 | Script for (a) border role, (c) and (d); Reviewer for (b) | P4 |
| RB-05 | Required literals intact and uncut: gap notice, counts tokens without a mid-token cut, `PARTIAL (...)` text, the disclosure, `reason unknown`, desk title, retention line, `nextAction.kind` verbatim | High | guards RR 20, 31, 32, 47, 49 | Script (substring list) | every phase |
| RB-06 | NO_COLOR pass: zero ESC bytes; text equals the coloured pass after SGR removal; hierarchy is carried by text and glyphs | High | G-1 | Script | every phase |
| RB-07 | ASCII pass: output is pure ASCII; borders are `+ - |`; no `?` where a border should be | High | G-1 | Script | P3, and every phase for the ASCII text part |
| RB-08 | Fit: every line at most the width in cells; rows at most the height; the footer keys are the last lines; no SGR 5 or 6 (blink); no mouse sequences | High | AD-5, standing constraints | Script | every phase |
| RB-09 | 16-colour pass: the eight roles map to eight distinct ANSI colours (no two roles share an index) | High | G-2 | Script (theme table test plus SGR read) | P1 |
| RB-10 | State words follow the fixed `STATE_ROLE` table of step 1.4 (D-7 default). Pass only if all hold: (a) every `workerState`, `dispatchStatus` or liveness cell, desk field or flags cell whose raw value is in the table carries exactly the table's role in the `.ansi`; (b) every other value (and `terminalState`, `nextAction.kind`) carries the `body` role, never a state role; (c) the word is printed in the plain pass in every case; (d) the table is non-empty: `T/test_theme.py` asserts that the tuple keys `("workerState", "running")`, `("workerState", "succeeded")`, `("workerState", "failed")`, `("dispatchStatus", "completed")` and `("liveness", "alive")` are in `STATE_ROLE` and that `FROZEN_ROLE == "state_frozen"`, so the row cannot pass on an empty table; (e) at the `standard` depth the four state roles have four different SGR codes | Medium | M-09 | Script (`.ansi` census against the table, `T/test_theme.py`) | P1 (desk fields P5) |
| RB-11 | Absent values (`unknown`, `unavailable (no source)`, `reason unknown`) are muted; plain under NO_COLOR | Medium | M-08 | Reviewer | P1 |
| RB-12 | A column heading and rule appear at 116 and 80 whenever rows are visible | Medium | M-10 | Reviewer plus script | P2 |
| RB-13 | The 80-column key list is not cut and no key pair is split across lines | Medium | M-11 | Script | P2 |
| RB-14 | Desk, measured on the plain and `.ansi` passes of `desk` and `desk-planask`. Pass only if all hold: (a) the question text leads: the first body line of the first pane after `DESK_TITLE` is `qid  age`, and all question-text lines (at most `DESK_TEXT_LINES`) come before any `label: value` line; (b) question-text lines carry the amber role and bold; (c) in the evidence pane every one-line field starts its value at the same cell offset (`label_width` = longest label plus its colon), measured as the column of the first character after the label on each such line; (d) a value that does not fit beside its label sits on the next line indented two cells, and no line exceeds the width | Medium | M-12 | Script for (a), (c), (d); Reviewer for (b) | P5 |
| RB-15 | Title bar: the left title and a right `READ ONLY` badge (OPEN-3, gating until ruled) | Medium | M-13 | Reviewer | P2 |
| RB-16 | Question list hierarchy (OPEN-1, gating until ruled). Pass only if all hold in the `.ansi`: (a) every question row line is bold, and its subject text carries the `body_bold` role (base colour); the one selected row is accepted with its marker and line in the bold amber `selected` role (step 1.4) and is not counted against this clause; (b) every run, state, caveat and retention line carries the `muted` role and no bold; (c) at 160 and 116 the first line inside the list pane after the disclosure is a question row (the caveat lines sit in the RETAIN CONTEXT pane, step 4.4), and at 80 the row lines carry strictly more bold characters than the caveat lines (0) | Medium | M-07 | Script (role census per line class) | P4 |
| RB-17 | RETAIN CONTEXT grouping at 160 and 116 (OPEN-2, gating until ruled). Pass only if all hold: (a) when a frame whose top border contains `RETAIN CONTEXT` is drawn, it is slate-bordered, full pane width, below the list pane, and its body contains each of `run_line`, `caveat_line` and `retention_line` exactly once; (b) none of those three strings occurs anywhere else on the screen; (c) when the degrade rule of step 4.5 dropped the pane (small height), no such frame exists and each of the three strings still occurs exactly once, in the list pane; (d) at 80 columns no RETAIN CONTEXT frame exists | Medium | M-14 | Script (string census on the plain pass) | P4 |
| RB-18 | Ledger screen: observation and attention content is in titled panes, with no invented owner, requester, mapped-tree or SIGNALS content (AD-1 to AD-4) | Medium | M-06 | Reviewer | P6 |
| RB-19 | Q7: for the `PLAN_ASK` fixture (hash inside the first four wrapped lines) the 64-hex hash is whole on one line in the 80-column desk, nothing is lost, no line exceeds 80 cells; the trailing-hash fixture still ends its fourth line with `...` (D-6) | Medium | Q7 | Script | P3 |
| RB-20 | A rule line precedes the footer and the key pair `n/p question` is intact | Low | M-15 | Script | P2 |
| RB-21 | The 80-column counts strip is not cut inside a token | Low | M-16 | Script | P2 |
| RB-22 | No wide blank band after the id column at 116 and 80: the longest run of consecutive spaces between two non-space characters inside a ledger row line, on the `base` fixture, is at most N, where N is the same measure on the 160-column rows of the same fixture, recorded in `VP/scores/baseline.md` in step 0.8 (a number measured at the current commit, not assumed) | Low | M-17 | Script | P2 |
| RB-23 | The selected question has a role style in addition to the glyph | Low | M-18 | Reviewer | P1 |

A phase closes only when every High and Medium row that is in scope for it passes; Low rows are recorded and may be deferred with a log line. A reviewer scores only the rows in scope for the phase, and marks later rows `N/A (scheduled P<n>)`.

### 8.5 Render gate protocol (the last step of every phase, written once)

| Step | Action | Details |
|---|---|---|
| G1 | Implement | Phase steps are done; `uv run pytest tests/observe/ -v` is green (baseline 766 passed in 25.70 s on 2026-11-17, plus tests added by earlier phases). |
| G2 | Render | `uv run python .dev/issues/409/visual-parity/tools/render_compare.py --out <out>/<phase>/iter-<n> --check --heights 44,40,24,12,8` runs the harness contract of step 0.3: widths 160, 116 and 80 for screens `ledger`, `questions`, `desk` and `desk-planask`, in the five passes truecolor, 256-colour, 16-colour, NO_COLOR and ASCII, plus the text-only height matrix, with the file names listed in 0.3. `--check` writes `checks.json` with the script-checked rows listed in 0.3 (RB-01(a), RB-04, RB-05 to RB-10, RB-13, RB-14, RB-16, RB-17, RB-19 to RB-22 for the parts marked Script in 8.4). |
| G3 | Rasterise | In the Claude session, open each truecolor and 16-colour `<screen>.<depth>.html` (step 0.3) through the Playwright MCP browser at a fixed viewport and save `.png` next to it (route proven in step 0.4). If 0.4 fails, the text and ANSI tier is used and the reviewer compares `.txt`/`.ansi` files with the mockup `.txt`/`.ansi` files, with the mockup PNG as the visual reference. |
| G4 | Score | Spawn one fresh reviewer subagent per width (no resume, no author context). Its inputs are only `VP/rubric/rubric.md`, the reviewer prompt, the mockup PNGs and `.txt` for that width, and the rendered `.png`, `.txt`, `.ansi`, `checks.json`. It returns `scores.json` with PASS or FAIL and one evidence line per in-scope row. |
| G5 | Fix and repeat | Fix every failing High or Medium row, re-render, and score again with a new reviewer. At most 3 iterations per phase. |
| G6 | Close or stop | Close the phase only if all in-scope High and Medium rows pass in the last iteration. If any still fails after iteration 3, stop, log the failing rows and the iteration scores in `VP/scores/<phase>/stop.md`, and ask the owner; do not start the next phase. |

All gates include the NO_COLOR and ASCII pass (guard G-1) as G2 outputs; a gate with a missing pass is not valid.

### 8.6 Contradictions between research files and which finding wins

| Topic | Conflicting statements | Used here | Why |
|---|---|---|---|
| Width classes | Task prompt (g): full, line, narrow; code: full, line, short, narrow | Four classes | `OBS/terminal.py:63-70` [CODE-VERIFIED] |
| `safe_box` and Rich boxes | Earlier 03 and 04 text: `safe_box=policy.ascii` gives ASCII panes; 01 probe: Panel prints identical Unicode borders with `safe_box` True or False | Hand-built `+ - |` glyphs through `GLYPHS` | Probe on Rich 15.0.0 (01 section 1; 03 section 6 rule 3); corrected in Gate 1 |
| Full ledger width | FINDINGS M-06: 153 cells; 01: exactly 160 | 160 | Arithmetic from `_columns` render.py:159-192 |
| 16-colour collapse | 01 section 7: slate and muted collapse; 04 section 3: muted, green, red, violet all index 7, slate 8 | 04 table | Measured with Rich's own downgrade, reproduced by two reviewers |
| Styled one-shot export | 01 and 05 and `render_current.py`: `export_text(styles=True)`; 02 probe: it ignores NO_COLOR and the downgrade | `console.file.getvalue()` | 02 probe |
| NO_COLOR and bold | web-01: Rich NO_COLOR keeps bold and dim; code: `color_system=None` drops them | Code behaviour kept | Project choice, probe in 01 section 7 |
| Live overflow | web-01 (Rich docs): `Live` shows an ellipsis; 02 section 9 measurement: `Screen` crops silently | Silent crop | Measured |
| Right-column slack | 01: 114+1+42=157 of 160; 04: 1+114+2+42+1=160 | 04 numbers | Measured from the mockup files |
| Zellij | web-02: go, conditional; 05: no-go as a harness dependency | Not a dependency; optional manual check | Both agree the observer must stay standalone; neither ran a session |
| Gate test line ranges | 03: test_commands.py:747-760 and 762-777; 02: 747-756 and 762-772 | 02 ranges | Gate 1 log row 43 |

### 8.7 External context (web research, not code facts)

| Claim used | Source |
|---|---|
| `color_system` values and auto detection read `COLORTERM` then `TERM` | https://rich.readthedocs.io/en/stable/console.html ; https://github.com/Textualize/rich/blob/v15.0.0/rich/console.py |
| Rich `export_html`, `export_svg` need `record=True`; SVG output depends on a browser (`rsvg-convert` and ImageMagick failed) | https://rich.readthedocs.io/en/stable/reference/console.html ; https://github.com/Textualize/rich/issues/2153 |
| `Text` spans and `cell_len` rules (ambiguous width counted as 1) | https://github.com/Textualize/rich/blob/v15.0.0/rich/text.py ; https://github.com/Textualize/rich/blob/v15.0.0/rich/cells.py |
| Zellij sets `ZELLIJ` in panes; `dump-screen --ansi`; floating panes in layouts | https://zellij.dev/documentation/nested-sessions.html ; https://zellij.dev/documentation/cli-actions.html ; https://zellij.dev/documentation/creating-a-layout.html |
| Playwright screenshots at a set viewport | https://snapshotflow.com/blog/playwright-screenshot |

### Phase 0: Render-compare harness, rubric, baseline and pinning tests (no `src/` change)

**Goal:** make the visual gap measurable and pin today's behaviour before any code changes: a harness that writes per-width, per-screen outputs; a fixed rubric; a baseline score; the Q7 hash fixture; and tests that document the style contract.

**Dependencies:** none. Owner decision D-10 (no new PNG dependency by default). Baseline run: `uv run pytest tests/observe/ -q` gives 766 passed.

**Closes:** no finding. It prepares the gate for all of M-01 to M-18.

| Step | Action | Files | Details |
|---|---|---|---|
| 0.1 | Make `render_current.py` importable | `VP/inputs/tools/render_current.py` | Line 93 calls `main()` at import time with no guard. Wrap it in `if __name__ == "__main__":`. Outputs of a direct run stay identical. |
| 0.2 | Add the harness | `VP/tools/render_compare.py` (new) | Loads `render_current.py` by path (`importlib.util.spec_from_file_location`) to reuse its view builders (`questions_result`, `QUESTIONS`, the three views). Interface: `render_case(view, width: int, height: int, *, env: dict, ascii: bool, depth: str = "16") -> CaseOutput` where `CaseOutput` holds `plain` (`screen_lines`), `stream` (the string written by `make_console(policy, file=io.StringIO(), record=True)` printing `render(view, policy)`, read with `console.file.getvalue()`), and `html` (`console.export_html(inline_styles=True)`). Policy comes from `resolve_policy(env, "utf-8", {"ascii": ascii}, width, height)`. It must not use `export_text(styles=True)`. |
| 0.3 | Define the harness contract (the one definition; G2 in 8.5 and step 7.3 refer to it) | `VP/tools/render_compare.py` | **Command:** `uv run python .dev/issues/409/visual-parity/tools/render_compare.py --out <dir> [--depth 16,256,truecolor] [--heights 44,40,24,12,8] [--check]`. **Screens:** `ledger`, `questions`, `desk`, `desk-planask` (Q7 fixture, built in 0.6). **Widths:** 160, 116, 80, at heights 48, 42, 42 (mockup frame heights, 04 section 4; `render_current.py:38` uses 50, which is not like for like). **Five render passes** per width and screen: (1) truecolor, (2) 256-colour, (3) 16-colour, (4) NO_COLOR, (5) ASCII. **Depth selector:** `--depth` takes a comma list of `16`, `256`, `truecolor` (default all three), mapped to the Rich `color_system` values `standard`, `256`, `truecolor`; before step 1.1 adds `TerminalPolicy.color_system` the harness can only produce `16` (`make_console` pins `"standard"`, terminal.py:121), writes the other two as copies marked `not-available-before-P1` in `manifest.json`, and the baseline run has no ESC in any file anyway. **Output files** in `<dir>/<width>/`: `<screen>.txt` (plain `screen_lines`), `<screen>.<depth>.ansi` and `<screen>.<depth>.html` for each selected depth, `<screen>.nocolor.txt` (env `{"NO_COLOR": "1"}`), `<screen>.ascii.txt` (`ascii=True`, plain) and `<screen>.ascii.ansi` (`ascii=True`, 16-colour stream); plus `manifest.json` per width with line counts and cell widths. `--heights` adds a text-only matrix (`<screen>.h<height>.txt`). **`--check`** writes `<dir>/checks.json` with one entry per script-checked row: RB-01(a), RB-04(a, c, d), RB-05 to RB-10 (RB-10(a), (b), (d) from the `.ansi` census), RB-13, RB-14(a, c, d), RB-16, RB-17, RB-19 to RB-22; the checks are width fit by `rich.cells.cell_len`, no ESC in the NO_COLOR file, `isascii()` on both ASCII files, SGR 5 and 6 absent, mouse sequences absent, the required literal list present, `strip_sgr(stream) == plain + newlines`, and the role census of 8.4. Gates run with `--check`; a run without it is not valid. |
| 0.4 | Prove the PNG route once | `VP/png-route.md` (new) | In the Claude session, open one `.html` via `mcp__plugin_playwright_playwright__browser_navigate` (`file://`), set the page to `font-family: "DejaVu Sans Mono"` and a width of `<cols>ch`, take a screenshot with `browser_take_screenshot`, and Read the PNG back. Record viewport, font and result. [UNVERIFIED until run; DejaVu Sans Mono is the only mono font confirmed installed, and its coverage of the mockup glyphs is untested.] If it fails, record that the text and ANSI tier is the gate and that a PNG tool (freeze or Playwright) needs a separate owner approval; no dependency is added by this plan. |
| 0.5 | Write the rubric and reviewer prompt | `VP/rubric/rubric.md`, `VP/rubric/reviewer-prompt.md` (new) | `rubric.md` is the 8.4 table verbatim plus the palette from 04 section 2 and the geometry from 8.3. The reviewer prompt names the inputs (mockup `.png`/`.txt`/`.ansi` for the width, rendered `.png`/`.txt`/`.ansi`, `checks.json`), the pairing ledger to signal-bridge, questions to attention-ledger, desk to decision-desk, the PASS or FAIL JSON shape, and forbids edits. The screen pairing and the mockup titles that the spec retires (`OPEN HUMAN QUESTIONS`) are noted so the reviewer does not score the title text. |
| 0.6 | Add the Q7 fixture and tests | `T/test_render.py` (R3 block, after line 967, the last line of the test that starts at :958) | New `PLAN_ASK` constant: a synthetic ask with a plan path, two file paths and `"0123456789abcdef" * 4`, under `ASK_CAP = 400` characters (parse.py:475) and under four desk lines at 80 columns. Test `test_r3_a_plan_ask_with_a_64_hex_hash_and_paths_wraps_cleanly_in_the_desk(width)` over `WIDTHS`: built with `r3_rows([("w-001", PLAN_ASK)])` and `r3_screen(fake_clock, rows, 0, width, height=70)`; asserts every line `cell_len <= width`; the hash is whole on one desk line; the ask with spaces removed equals the desk text with spaces removed when not cut. Second test with a hash after a long path and file list that fills the four-line cap, pinning today's `...` cut: the hash is not shown, and this is the one stated exception to "the hash is whole" (rule D-6). The first test's fixture keeps the hash inside the first four lines. Third test: a worker with a 120-character `resource.worktreeId` (pattern from `T/test_view.py` `r3_workers(worktree=...)`) pins the 2-cell continuation indent at render.py:347-353. Canary: `HASH not in record_text(view)` and `HASH not in snapshot_json(view)`. |
| 0.7 | Add helpers and a height test | `T/conftest.py`, `T/test_height_budget.py` (new) | `strip_sgr(text) -> str` using `re.sub(r"\x1b\[[0-9;]*m", "", text)` and `sgr_params(text) -> set[str]`, with a self-test. `test_questions_on_screen_fits_the_height(width, height)` for heights 24, 40, 44. Run it first: if a height fails on today's code, record the failing heights in `VP/scores/baseline.md` and pin only the passing set (the forced single ledger row at render.py:502 can overflow; 02 section 9.4). |
| 0.8 | Baseline score | `VP/scores/baseline.json` (new) | Run the harness at the current commit, rasterise per 0.4, spawn one fresh reviewer per width (8.5 G4), store the scores, and write the measured threshold N of RB-22 (longest interior blank run in the 160-column rows of the `base` fixture) to `VP/scores/baseline.md`. Expected: RB-01 to RB-04 and RB-09 to RB-18 FAIL (the plain-text rows RB-05 to RB-08 are expected to pass, since the current screens are plain text); script rows that check text pass. A baseline that passes any High rubric row is a sign the rubric is not discriminating; revise `rubric.md` once, then freeze. |

**Tests and goldens that change:** none change; tests are added. Golden files and `printed_*` bytes are untouched.

**Byte-identical in this phase:** everything under `src/`; `record_text`; `snapshot_json`; both goldens.

**Rubric rows scored (baseline only):** all, as a baseline; no pass is required.

**Migration or rollback:** delete the new files; no source depends on them. If 0.7 shows an existing overflow, it is a finding for P3, not a P0 fix.

**Render gate:** the baseline run in step 0.8 replaces the gate for this phase; the phase closes when `uv run pytest tests/observe/ -v` is green with the new tests and the baseline file exists.

### Phase 1: Colour depth, theme, role spans and the styled-capture gates (style only, no text change)

**Goal:** add colour and weight to every existing screen without changing one plain character; fix colour depth (Q4, G-2); make styled output capturable and tested on the one-shot path and the live path (Q5).

**Dependencies:** Phase 0 (harness, helpers `strip_sgr`, rubric, baseline). Owner decisions D-4, D-5, D-7, D-12 (defaults in 8.2 apply if not ruled).

**Closes:** M-01 (colour and weight on the current screens; frame and strip colours follow in P3 and P4), M-08, M-18; M-09 on the ledger rows (desk fields complete it in P5); guard G-2.

| Step | Action | Files | Details |
|---|---|---|---|
| 1.1 | Resolve the colour system in the policy | `OBS/terminal.py` (`TerminalPolicy` 37-51, `resolve_policy` 73-92, `make_console` 110-125) | Add field `color_system: str \| None = "standard"` last in the frozen dataclass so existing constructions keep working. In `resolve_policy`: `None` when `no_color`; `None` when `env.get("TERM")` is `dumb` or `unknown`; `"truecolor"` when `env.get("COLORTERM", "").lower()` is `truecolor` or `24bit`; `"256"` when `env.get("TERM", "")` ends with `256color`; otherwise `"standard"`. In `make_console` replace line 121 with `color_system=policy.color_system`; keep `no_color=policy.no_color`. NO_COLOR therefore still gives `color_system=None` and drops bold as well as colour (project behaviour, 01 section 7). `NO_COLOR` literal stays only in terminal.py (source scan `T/test_terminal.py:181-198`). Tests call `resolve_policy({}, ...)` with an empty env, so they stay at `"standard"`. |
| 1.2 | Add the theme module | `OBS/theme.py` (new) | `ROLES: tuple[str, ...]` (semantic roles: `title`, `attention`, `attention_title`, `identity`, `secondary`, `body`, `body_bold`, `muted`, `selected`, `border_attention`, `border_secondary`, `border_count`, `state_running`, `state_settled`, `state_failed`, `state_frozen`); `style_for(role: str, depth: str) -> rich.style.Style \| None` (returns `None` for depth `None`); one table per depth. Truecolor RGB from the mockups: base 225,233,238; muted 165,182,194; slate 82,108,128; amber 250,178,25; cyan 112,205,226; green 139,215,175; red 240,141,150; violet 194,173,242 (04 section 2). 256-colour indexes: base 189, slate 60, cyan 80, muted 145, amber 214, green 115, red 210, violet 147. 16-colour table with named colours: base `bright_white`, muted `white`, slate `bright_black`, cyan `bright_cyan`, amber `bright_yellow`, green `green`, red `red`, violet `magenta`. No role sets blink, dim or reverse. `Style` objects are cached per `(role, depth)` so an earlier depth in the same process cannot leave stale codes on a later one (Rich caches ANSI codes on a Style, 01 section 7). The file must not contain the literals `Console(`, `NO_COLOR`, `COLUMNS`, `stdout.encoding` or `getpreferredencoding` (also not in comments). |
| 1.3 | Add the `Line` layer | `OBS/render.py` (imports 12-14, `render` 524-531, `screen_lines` 390-521) | New frozen `Span(start: int, end: int, role: str)` (character offsets) and `Line(plain: str, spans: tuple[Span, ...] = ())` with construction helpers `seg(text, role=None) -> Line` and `join(*parts: Line) -> Line` that build in order, so offsets never come from cell widths (wide characters are 2 cells but 1 character, 01 section 8.2). `Line.clipped(width, policy) -> Line` calls `clip()` on `plain` and trims spans to the new length; `ascii_safe` replaces one character with one `?`, so offsets stay valid. `_roled(strings: list[str], role: str) -> list[Line]` wraps existing `wrap(...)` output with one whole-line role. Rename the body of `screen_lines` to `_compose(view, policy, message=None) -> list[Line]` and define `screen_lines(...) = [l.plain for l in _compose(...)]`, so the public signature and every string result are unchanged. `render()` builds `Text(l.plain, no_wrap=True, overflow="crop")` per line and calls `text.stylize(style, span.start, span.end)` only when `policy.color_system` is not `None`. Keep render.py free of `Console(`, `from_markup`, `sorted(`, `.sort(` and of `observe.adapter\|collector\|parse` (`T/test_render.py:400-404`). |
| 1.4 | Assign roles at the builders (no text edits) | `OBS/render.py` (`counts_lines` 94-135, `_row_line` 233-243, `_header_lines` 246-249, `_inspector_lines` 255-287, `_question_line` 311-326, `_desk_lines` 329-356, `_panel_lines` 359-387, footer 514-521) | `header1` `title`; `header2`, `changes_line`, `gap_notice`, `_notes`, `ledger_empty` text and the footer `muted` (the mockups draw the clock and freshness line and the keys hint in muted, 04 section 2); counts tokens: protected tokens `identity`, and the suffix span of a token ending in `UNAVAILABLE` (view.py:100) `muted`; panel title `attention_title`; run, state, disclosure, caveat and retention lines `muted`; `counts_line` `identity`; ledger title `secondary` bold; the question line is built as segments: age `attention` bold, subject `body_bold`, `QUESTIONS_REASON` tail `muted`, and the selected question marker and line `selected` (bold amber, the only list-row text that is amber besides the age; M-18; the glyph stays `glyph("selected")`, RR line 50); `DESK_TITLE` `attention_title`, the desk `qid  age` line (qid and age) `attention` bold, desk question text `attention` bold, field labels `muted`, values `body`. `_row_line` is rebuilt as `_row_segments(row, columns, policy) -> Line`: it appends each `_cell(...)` in order and tags cells; the `nextAction.kind` cell stays `body` (RR line 31, never classified); a cell whose stripped text equals the bare `unknown` is `muted` (a real value `"unknown"` is quoted by `text_of`, view.py:377-385, so the bare word means absent); `workerState`, `dispatchStatus` (full layout only, `_columns` 166-191) and the liveness verdict (`_verdict`, all layouts) take the D-7 mapping `STATE_ROLE: dict[tuple[str, str], str]` in theme.py, keyed by `(field, exact raw value)` (exact string equality on the raw `RowView` value, never a regex and never a substring; for liveness the value is `row.raw.liveness_verdict`, render.py:151-152, and in the `full` layout the cell text is `<verdict> (<source>)`, view.py:509, so only the verdict characters take the role); a flags cell containing `FROZEN_MARKER` (view.py:106) is `state_frozen`. **Minimum fixed table (the D-7 default; values taken from the fixtures under `OBS/fixtures/`, where `workerState` shows running, idle, blocked, exited, succeeded, failed, ready, stopped, abandoned, `dispatchStatus` shows active, blocked, completed, failed, dispatched, and the liveness verdict shows alive, live, ended, exited, unverifiable):** `("workerState", "running")` and `("liveness", "alive")` and `("liveness", "live")` map to `state_running`; `("workerState", "succeeded")` and `("dispatchStatus", "completed")` map to `state_settled`; `("workerState", "failed")` and `("dispatchStatus", "failed")` map to `state_failed`; a flags cell containing `FROZEN_MARKER` is not a tuple key: theme.py holds it as the separate constant `FROZEN_ROLE = "state_frozen"`. Every other value (idle, blocked, exited, ready, stopped, abandoned, active, dispatched, ended, unverifiable, any unseen value) and every `terminalState` and `nextAction.kind` value stays `body`; `terminalState=released` is never styled as done (RR 71). The table is a display choice, not a count mapping, so it does not contradict RR 93 (which records that no verified mapping from `workerState` or outcome to "settled" exists for the SIGNALS bars, AD-2); it is owner decision D-7 and the owner may replace it, but the minimum list above must stay non-empty so RB-10 cannot pass on an empty table. The state word is always printed; before coding, re-read `RowView` construction (view.py:481-518) and the parse.py value sets to confirm the key names. No regex runs over worker-controlled text; roles are attached where the builder already knows the field. |
| 1.5 | Make the one-shot path styled-capable | `OBS/commands.py` (`run_once` 225-247, `LiveScreen` 257-279) | Add `_screen_text(view, policy, *, styled: bool) -> str` that builds `make_console(policy, file=io.StringIO(), record=True)`, prints `render(view, policy)` and returns `console.file.getvalue()` when `styled`, else `console.export_text()`. `run_once` sets `styled = (policy.color_system is not None) and stdout_is_tty`, taking stdout from the same dependency object that `_emit` (200-210) uses. Default per D-4: a piped `--once --width` stays plain. Add `policy.color_system` to the `LiveScreen` shape tuple at line 265, so a depth change rebuilds the `Live`. Do not touch lines 67 and 70 (`QUESTION_GATE_PASSED`, `QUESTION_LINK_PASSED`) and keep the words `release-gates.md` and `Task 18` in the file (`T/test_commands.py:747-772` read the source text). |
| 1.6 | Update tests and goldens | `T/test_render.py`, `T/release1_surface.py`, `T/test_terminal.py`, `T/test_theme.py` (new), `T/test_styled_capture.py` (new), `T/live_child.py` (new), `T/test_live_screen_pty.py` (new), `T/conftest.py` | (a) `test_rendering_twice_is_byte_identical_and_no_color_changes_no_text` (test_render.py:250-259): keep determinism and the `screen_lines` equality (:257); replace :256 with `strip_sgr(colour) == nocolor`, and assert that the colour print contains ESC at 160 for the base variant and that the NO_COLOR print contains none. (b) Audit every `printed(` call (:76, :161, :181, :255-256, :277, :605, :977, :987): any that applies `cell_len` or `bad_chars` to colour output first applies `strip_sgr`. (c) `T/release1_surface.py` (`_printed`, lines 34-38, which builds `printed_*` through `make_console` and `render()` and therefore gains SGR bytes once P1 styles `render()`, since an explicit `color_system` makes Rich write SGR even to a `StringIO`): make `_printed` return `strip_sgr(buffer.getvalue())`, importing `strip_sgr` from `tests.observe.conftest` as the module already imports `FakeClock` from there, and add a docstring line that `printed_*` holds the printed text with SGR removed (release 1 wrote none, so the strip changes nothing there). Every `printed_*` value in `surface()` is then plain text, equal to the plain golden bytes, so `test_t47_...` (:611-624) is not edited, no side of the comparison is stripped asymmetrically in any phase, and the golden file bytes do not change in P1. Styled bytes are never stored in a golden; they are pinned by (a), (f) and (g). (d) `test_terminal.py`: depth cases (NO_COLOR, TERM=dumb, COLORTERM truecolor, TERM xterm-256color, none) and `make_console(...).color_system` for each; the literal-options test at :105-116 still passes. (e) `test_theme.py`: every role exists at every depth; the eight palette roles are distinct at `"standard"` (RB-09); the four state roles have four different SGR codes at `"standard"` (RB-10(e)); `STATE_ROLE` contains the tuple keys `("workerState", "running")`, `("workerState", "succeeded")`, `("workerState", "failed")`, `("dispatchStatus", "completed")` and `("liveness", "alive")`, and `FROZEN_ROLE == "state_frozen"` (RB-10(d)); no style has blink; `style_for` returns distinct objects per depth. (f) `test_styled_capture.py`: `_screen_text(styled=True)` at 160, 116, 80 contains SGR and `strip_sgr(...)` equals the `export_text()` text; NO_COLOR gives zero ESC; ASCII stays ASCII; the one-shot CLI path with a non-tty stdout still satisfies `T/test_commands.py:121`. (g) Live gate: `live_child.py` builds the fixture view, calls the real `LiveScreen` (constructor and `draw` signature to be read at commands.py:257-279 when implementing) under `pexpect.spawn` with a fixed pty size (pattern at `T/spike_child.py:64`; `pexpect` is a declared dependency, pyproject.toml:41). `test_live_screen_pty.py` asserts the stream contains `\x1b[?1049h`, SGR bytes with `38;2` when `COLORTERM=truecolor`, only 16-colour codes otherwise, no SGR under `NO_COLOR=1`, no SGR 5 or 6, and no mouse mode sequences (`\x1b[?1000h`, `?1002h`, `?1003h`, `?1006h`). If Rich emits a bare reset under `NO_COLOR`, adjust the assertion with the measured bytes and note it. |
| 1.7 | Render gate | `VP/tools/render_compare.py` | Run G1 to G6 (8.5) with the rubric rows in scope for this phase. |

**Tests and goldens that change:** `T/test_render.py` (lines 250-259, plus `strip_sgr` at the audited `printed(` calls; `test_t47_...` at 611-624 is not edited); `T/release1_surface.py` (`_printed` strips SGR); `T/test_terminal.py` (added cases). New: `T/test_theme.py`, `T/test_styled_capture.py`, `T/live_child.py`, `T/test_live_screen_pty.py`. `T/golden_release1_surface.json` and `T/golden_questions_linkoff.json` do not change.

**Byte-identical in this phase:** `record_text`, `snapshot_json`, every `screen_lines` string (so `lines_*` in both goldens and all whole-line tests), `--once` without `--width`, the gate constant lines in commands.py.

**Rubric rows scored:** RB-01, RB-05 to RB-11, RB-23 (High and Medium must pass).

**Migration or rollback:** revert the phase commit. `color_system` defaults to `"standard"`, so a partial revert of render.py leaves unstyled output. If the `Line` refactor is too wide for one commit, land 1.1 and 1.2 first (no behaviour change), then 1.3 with `_roled` wrapping every existing builder as a single `body` line, then 1.4 builder by builder; each step keeps the suite green.

### Phase 2: Text and budget defects on the existing layouts (headings, keys, counts, title bar)

**Goal:** fix the five findings that are plain-text defects of today's layout and need no frame: missing column heading at 116 and 80, the cut 80-column key list, the split key pair and missing footer rule, the counts strip cut inside a token, and the title bar with a `READ ONLY` badge. Separate the record and snapshot guarantee from the presentation goldens before any golden is regenerated.

**Dependencies:** Phase 1. Owner decision D-2 (re-baseline the goldens; under "freeze questions-off" this phase applies to questions-on screens only) and D-3 for M-13.

**Closes:** M-10, M-11, M-13, M-15, M-16, M-17 (M-17 is optional, Low).

| Step | Action | Files | Details |
|---|---|---|---|
| 2.1 | Split the record guarantee from the presentation golden (do this first) | `T/golden_release1_records.json` (new), `T/release1_surface.py`, `T/test_render.py` | From the current `T/golden_release1_surface.json` keep, per variant (`base`, `empty`, `source-loss`, `injection`, `missing-fields`), only `header1`, `header2`, `gap_notice`, `record_text`, `snapshot_json`, and write them with `json.dumps(..., indent=1, sort_keys=True, ensure_ascii=False)` and no trailing newline (the serialisation measured in 03 section 4a). Add `test_release1_records_are_byte_identical_to_the_recorded_surface` that compares those keys from `surface()`. This file is never regenerated; it keeps "records and JSON snapshot byte-identical" enforced after the presentation golden is re-baselined. |
| 2.2 | Column heading at every width | `OBS/render.py` (`_header_lines` 246-249, gate 497, `ledger_fixed` 438-440; `reserved` 499-501 is read only, no edit) | Add `_heading_rows(view, policy) -> int` returning 2 when `view.visible_rows` else 0, and use it at the two places that today test `policy.width_class == "full"`: the `ledger_fixed` term (line 439) and the gate that appends the heading to `body` (line 497). Do not add the heading rows to `reserved` (lines 499-501): it reads `len(body)`, and the heading rows are already in `body` when it is computed, so a separate addition would count them twice and show one ledger row too few. `_columns` already names the `line` columns (203-204) and the `short` columns (218-221), so `_header_lines(columns, policy)` works for every class. The condition lives in `screen_lines`, not `render()` (FINDINGS cites the wrong function; behaviour confirmed). |
| 2.3 | Key list never cut, key pairs never split, rule above the footer | `OBS/render.py` (`_help_lines` 304-308, footer probe 423-431, footer 514-521) | Add `wrap_groups(text, width, policy) -> list[str]` next to `wrap`: split the help line on two-space separators, pack groups greedily into lines joined by two spaces, and fall back to `wrap` only for a single group wider than the width. `_help_lines` uses it in both branches, removing the `clip(...)` branch for `view.questions is None` (the cause of `e exp>` at 80, measured). Add one rule line `glyph("hrule") * width` before the footer lines and count it in `footer_height` at 423-431 and in the footer branch at 514-521. |
| 2.4 | Counts strip never cut inside a token | `OBS/render.py` (`counts_lines` 94-135, cut path 127-132) | Remove the branch that clips an unprotected token into the remaining room (127-129). A token that does not fit is dropped whole and the line ends with the existing ` >` marker (131), as RR line 20 allows for low-priority tokens; protected tokens keep their wrap path (115-121). Measured defect: `runs seen>` at 80 columns. |
| 2.5 | Title bar with a badge | `OBS/view.py` (constants near 44-114), `OBS/render.py` (head 409-414) | Add the literal `READ_ONLY_BADGE = "READ ONLY"` to view.py so render.py decides no literal (the test name at `T/test_render.py:396` says render never decides literals). In render.py add `_title_bar(lines: list[str], policy) -> list[Line]`: after `wrap(view.header1, width)`, append the badge right-aligned on the first wrapped line if `cell_len(line) + 2 + cell_len(badge) <= width`, else on the last wrapped line by the same test, else on its own right-aligned line. `view.header1` is not edited, so `record_text` (export.py:76) and `header1` in the golden are unchanged. Badge role `attention`. |
| 2.6 | Wide blank band (optional, Low) | `OBS/render.py` (`_columns` 195-196, 215) | Design choice not taken from research: give `line` and `short` the same id rule the `full` class uses (`22 + min(extra, 26)`, render.py:159-192) and let the last, elastic `flags` column take the remainder, so widths stay static (FINDINGS M-17 forbids widths that shift between refreshes). Skip if RB-22 already passes and log the skip. |
| 2.7 | Tests and goldens | `T/test_render.py`, `T/golden_release1_surface.json`, `T/golden_questions_linkoff.json` | Regenerate both presentation goldens from the current tree in the same commit. Link-off golden (command shape from 03 section 4b): `uv run python -I -c "import json,sys; sys.path.insert(0,'.'); from pathlib import Path; from tests.observe.test_linkoff_screen_reference import capture; from tests.observe.conftest import FakeClock; Path('tests/observe/golden_questions_linkoff.json').write_text(json.dumps(capture(FakeClock()), indent=1, ensure_ascii=False)+'\n', encoding='utf-8')"`. Release-1 golden (derived from 03 section 4a, not an approved procedure): the same shape with `from tests.observe.release1_surface import surface` and `json.dumps(surface(), indent=1, sort_keys=True, ensure_ascii=False)` written with no trailing newline, run from the current tree (not from `git archive 9e2608b03`). The `printed_*` values written this way are SGR-free because `_printed` strips SGR (step 1.6(c)), so the regenerated golden holds plain text and `test_t47_...` still compares like with like with no per-key stripping; add `test_presentation_goldens_hold_no_escape_bytes` (neither golden file contains `\x1b`), so a styled capture can never be written into a golden. Retitle the docstring of `test_t47_questions_off_is_byte_identical_to_the_recorded_release_1_surface` (:611) to say it pins the recorded presentation, since 2.1 now holds the release-1 record guarantee. Re-run and adjust, with evidence, the tests that depend on row counts and line positions: `test_matrix_lines_fit...` (`len(lines) <= 30`, :83), `test_decision_2...` (ledger rows between 1 and 3, :660), `test_line_and_short_forms_follow_kind_id_verdict_age` (:314-326; if it searches the whole screen it must be restricted to row lines now that headings exist at 116 and 80), `test_f08` (:748; passes by construction), `T/test_inspector_scroll.py` (inspector returns earlier, no heading). Add tests: heading present at 116 and 80 when rows are visible and absent when empty; no `>` at the end of the key line at 80; `n/p question` never split across lines; no counts line ends inside a token; `READ ONLY` appears once and every line fits; footer rule precedes the footer. |
| 2.8 | Render gate | `VP/tools/render_compare.py` | Run G1 to G6 (8.5). |

**Tests and goldens that change:** `T/golden_release1_surface.json` (lines and printed keys; regenerated), `T/golden_questions_linkoff.json` (the `116` and `80` lists gain headings, all widths gain the badge; regenerated), `T/test_render.py` (docstring and the position-sensitive tests above). New: `T/golden_release1_records.json` and its test; `test_presentation_goldens_hold_no_escape_bytes`.

**Byte-identical in this phase:** `record_text`, `snapshot_json`, `header1`, `header2`, `gap_notice` (now enforced by `golden_release1_records.json`), the gate lines in commands.py, `--once` without `--width`.

**Rubric rows scored:** RB-12, RB-13, RB-15, RB-20, RB-21, RB-22, plus every earlier row as regression.

**Migration or rollback:** step 2.1 is safe to land alone. After 2.7, rollback is a revert of the commit together with both regenerated goldens. If D-2 is "freeze questions-off", gate 2.2 to 2.6 on `view.questions is not None` and keep the release-1 golden untouched; M-10, M-11, M-13 then stay open for the questions-off screens.

### Phase 3: Frame primitive and single-column titled panes on the questions-on screens (ASCII-safe)

**Goal:** add the frame helper and box glyphs (G-1), then frame the COORDINATOR QUESTIONS list and the DECISION DESK as titled, coloured panes at every width, still one column, with every row counted in the height budget. Re-pin the Q7 hash fixture inside the 80-column frame.

**Dependencies:** Phase 2 (re-baselined goldens), Phase 1 (roles `border_*`). Owner decision D-9 (framed lines in `--once --width` output; step 3.6 assumes the default yes). Questions-off screens are not framed in this phase, so `golden_release1_surface.json` does not change here.

**Closes:** M-02 for the questions list and the desk (the ledger frame closes it in P6); Q7 fixture re-pinned (RB-19).

| Step | Action | Files | Details |
|---|---|---|---|
| 3.1 | Box glyphs with ASCII forms | `OBS/terminal.py` (`GLYPHS` 30-34) | Add, in the same unicode-and-ASCII pair shape as the existing `selected`, `truncate`, `hrule`: rounded `box_tl ╭`, `box_tr ╮`, `box_bl ╰`, `box_br ╯`, `box_h ─`, `box_v │`; heavy `hbox_tl ┏`, `hbox_tr ┓`, `hbox_bl ┗`, `hbox_br ┛`, `hbox_h ━`, `hbox_v ┃`. ASCII forms: corners `+`, horizontals `-`, verticals `\|` (RR line 25). All candidates measured one cell in Rich 15. Never write a box character as a literal in a string: `ascii_safe` (terminal.py:133-135) turns any non-ASCII character into `?`; always go through `glyph()`. |
| 3.2 | Frame helper | `OBS/render.py` (next to `_pad` 83-84) | `MARGIN = 1`, `FRAME_ROWS = 2`, `INNER_PAD = 1`. `_frame(title: str, body: list[Line], width: int, policy: TerminalPolicy, *, weight: str = "round") -> list[Line]` returns lines exactly `width` cells wide: top `tl + h + " " + title + " " + h*fill + tr`, body rows `v + " " + Line.padded(inner) + " " + v` with `inner = width - 4`, bottom `bl + h*(width-2) + br`. The title is clipped to `inner - 2` with `clip()`, so a long title cannot squeeze required body text. Border spans use `border_attention` for `weight="heavy"` and `border_secondary` for `"round"`; the title span is bold in the same colour. `Line.padded(width, policy) -> Line` pads with spaces by `cell_len`. Callers add the one-cell margin with `_indent(lines, MARGIN)`. |
| 3.3 | Thread the inner width | `OBS/render.py` (`_panel_lines` 359-387, `_question_line` 311-326, `_desk_lines` 329-356) | `pane = policy.width - 2*MARGIN`, `inner = pane - 4`. `_question_line(q, policy, inner)` and `_desk_lines(desk, policy, inner)` take the inner width in place of `policy.width`; every `wrap`, `clip` and the `room` arithmetic at lines 320-325 use `inner`. `_panel_lines` builds the body (run line, state, disclosure, counts line, caveat, question rows, cut text, `DESK_SELECTED_HIDDEN`, empty and window-full text, notes, retention) without the title and returns `_frame(panel.title, body, pane, policy, weight=...)`. Weight rule from the mockups: the list pane is heavy when there is no desk, round when a desk is shown; the desk pane is heavy. The desk is a separate frame in this phase (`DESK_TITLE` in its border). |
| 3.4 | Keep the budget exact | `OBS/render.py` (sizing 433-481, `base` 441-443, `spare` 447-457) | `base` is `len(_panel_lines(replace(panel, lines=(), empty_text=None), policy, None))` and `len(desk)` is the length of the returned list, so both include the frame rows with no new term. Keep the three `+1` terms as they are. Where the desk does not fit and `DESK_HIDDEN` replaces it, the notice goes inside the list frame body. The forced single ledger row at render.py:502 is unchanged. |
| 3.5 | Test helpers | `T/conftest.py` | `unframe(line: str) -> str` strips the margin, the left and right border glyph (rounded, heavy and ASCII forms) and one padding cell; `title_of(lines) -> list[str]` returns the text inset in top borders. Both are used only by tests. |
| 3.6 | Update tests (depends on owner decision D-9, default yes: framed lines in `--once --width` output; if D-9 is no, skip the two `T/test_commands.py` edits below and add the `frames` switch described in 8.2) | `T/test_render.py`, `T/test_commands.py`, `T/test_question_cap.py` | Whole-line checks become frame-aware: `DESK_TITLE in lines` (:900, :924, :997) becomes `DESK_TITLE in title_of(lines)`; `startswith("▸ ")` (:897), `startswith("dispatchId:")` (:964 and the desk slice :951-966), `endswith("reason unknown")` (:938, :948), `startswith("questions shown ")` (:479, :646), the exact `window full: older questions may be missing` (:547, `T/test_question_cap.py:77` and `:121`) use `unframe(l)`; `T/test_commands.py:672-675` and `:690` (`COORDINATOR QUESTIONS` and `seen, not resolved: 4 \| closed by evidence: unavailable (no source)` as whole lines of `--once --width` output) use `title_of` and `unframe`. `test_inspector...` at :118-132 is not framed and does not change. `test_decision_2` (:660-676, 8 `reason unknown` lines at height 26): two frame rows now come out of the same budget; re-pin the count from the measured value and record in the commit message that the owner's rule "the questions win on a short terminal" (comment at render.py:444-445) still holds while two fewer questions fit. `test_r3_the_desk_gives_way...` (:990, heights 8 to 60 at 116) keeps passing if every state is still reached; adjust only the height range if a state disappears. |
| 3.7 | Re-pin the Q7 fixture | `T/test_render.py` | The three tests from step 0.6 now read through `unframe`. Expected values (single column): inner width is `width - 6` (154 at 160, 110 at 116, 74 at 80). Ask text: the 64-cell hash stays whole on its own line when words precede it; the fourth desk line still ends in `...` when the ask exceeds four lines. Evidence field `resource.worktreeId` with the 64-cell hash: `label:` on one line, the value on the next line indented two cells (inner minus 2 is 72 at 80, so it fits whole); a value wider than the inner width is hard-split by `wrap()` with nothing lost and no marker (render.py:62-80). All lines at most the width. Both hash canaries (record, snapshot) stay. |
| 3.8 | Height and live checks | `T/test_height_budget.py`, `T/test_live_screen_pty.py` | Extend the height test to the framed questions-on screens at 8 (diagnostic), 12, 24, 40, 44 and the three widths: `len(lines) <= policy.height` or `policy.too_small`. In the pty test at height 24 and 40 assert the last stream row holds the `shown x/y` footer text, so a frame row that overflows (and drops the footer from the bottom, 02 section 9.2) fails the build. |
| 3.9 | Goldens | `T/golden_questions_linkoff.json` | Regenerate with the link-off command from step 2.7 (the link-off questions screen now has frames at all three widths). `T/golden_release1_surface.json` and `T/golden_release1_records.json` are untouched. |
| 3.10 | Render gate | `VP/tools/render_compare.py` | G1 to G6 with the NO_COLOR and ASCII passes mandatory (guard G-1): the ASCII pass must show `+---+` and `\|`, never `?`. |

**Tests and goldens that change:** `T/test_render.py`, `T/test_commands.py` (lines 672-690), `T/test_question_cap.py` (lines 77, 121), `T/conftest.py`, `T/test_height_budget.py`, `T/test_live_screen_pty.py`; `T/golden_questions_linkoff.json` regenerated.

**Byte-identical in this phase:** `record_text`, `snapshot_json`, all questions-off `screen_lines` and `printed_*` (so the release-1 presentation golden), the inspector screen, the too-narrow and too-small diagnostics.

**Rubric rows scored:** RB-02 (questions, desk), RB-07, RB-19, plus all earlier rows.

**Migration or rollback:** revert the commit and the regenerated link-off golden. Frames exist only through `_frame`; the `_panel_lines` and `_desk_lines` changes are reachable only when `view.questions` is set.

### Phase 4: Count strip and RETAIN CONTEXT pane on the stacked questions screen (160 and 116; 80 unchanged)

**Owner ruling (2026-11-18, issue #606): the questions screen stays stacked at every width.** This phase replaces the two-column questions layout of the earlier plan. The evidence is the stacked-vs-two-column comparison posted on #606 (two columns cost 6 more rows at 160 and 5 more at 116, wrapped the question text at 116, and added no fact). Finding M-03 (no two-column questions screen) is therefore not fixed; it is recorded as accepted divergence AD-8.

**Goal:** at 160 and 116 columns the questions screen is one stack of three panes: a full-width cyan count strip with a block-glyph figure, the amber question list (question rows lead), and a slate RETAIN CONTEXT pane that groups the run line, the caveat and the retention sentence. At 80 columns the screen stays exactly as Phase 3 left it. All content comes from facts the view already holds.

**Dependencies:** Phase 3 (`_frame`, helpers). Owner decision D-3 rules the severity of M-07 and M-14 (treated as Medium until then). The Decision Desk decision (two columns) does not affect this phase.

**Closes:** M-05, M-07, M-14. M-03 is closed by owner ruling AD-8, not by code.

Target layout (character grid; panes are `width - 2` wide with margin 1; the strip body is 3 rows):

```
 160 / 116 (stacked, three panes)                         80 (as Phase 3, no strip, no RETAIN pane)
 +-- SEEN IS NOT RESOLVED (cyan) -----------------+       +-- COORDINATOR QUESTIONS ---+
 | figure (3-row block font)  seen, not resolved:.|       | run, state, disclosure     |
 +-----------------------------------------------+       | counts line, caveat        |
 +-- COORDINATOR QUESTIONS (heavy, amber) --------+       | question rows              |
 | disclosure (muted)                             |       | retention line             |
 | > 1h  subject ...  reason unknown              |       +----------------------------+
 |   2h  subject ...  reason unknown              |
 | questions shown ...                            |
 +-----------------------------------------------+
 +-- RETAIN CONTEXT (slate) ----------------------+
 | run line, caveat, retention (muted)            |
 +-----------------------------------------------+
```

| Step | Action | Files | Details |
|---|---|---|---|
| 4.1 | One render-only field for the figure | `OBS/view.py` (panel dataclass at 246-266, `counts_line` built near 761), `T/test_view.py` | Add `count_figure: str = ""` to the panel view, set to the exact figure text already used inside `counts_line` (for example the `100+` form when the window is full), at the same place that builds `counts_line`, so the number logic has one source. The default keeps every existing construction valid. `counts_line`, `run_line` (794), `caveat_line` (798) and `retention_line` (804) are not edited. `OBS/export.py` must not read the new field; add a source-scan test next to `T/test_export.py:238-243` that `count_figure` does not appear in export.py. Read view.py:746-766 before editing. |
| 4.2 | Block glyph and a 3-row figure font | `OBS/terminal.py` (`GLYPHS`), `OBS/render.py` | Add glyph `block` (`█`, ASCII `#`). Add `_BIG`, a font of digits and `+`, each 3 cells wide and 3 rows tall, built only from the `block` glyph and spaces (design the shapes so 0 to 9 are distinguishable; check them in the render gate). A figure that contains any other character (for example `unknown`) is not drawn in the font. |
| 4.3 | Count strip | `OBS/render.py` | `_count_strip(panel, width, policy) -> list[Line]`: a frame with `border_count` (cyan), title `QUESTIONS_COUNT_LABEL.upper()` (view.py:70-72, no new literal), full pane width. Body of three rows when the figure is drawable and `figure_width + 2 + cell_len(panel.counts_line) <= inner`: the figure in the 3-row font in the `attention` role at the left, and `panel.counts_line` in `identity` on the middle row, two cells to the right of the figure, so the plain pass keeps `seen, not resolved: N \| closed by evidence: unavailable (no source)` whole on one line. Otherwise the body is one row: the figure bold in `attention`, two spaces, `panel.counts_line` wrapped to the inner width (the NO_COLOR, ASCII and 80-column text form). |
| 4.4 | RETAIN CONTEXT pane | `OBS/view.py` (constants), `OBS/render.py` | Add `RETAIN_TITLE = "RETAIN CONTEXT"` to view.py. `_retain_pane(panel, width, policy) -> list[Line]`: a round slate frame at full pane width whose body is `panel.run_line`, `panel.caveat_line` and `panel.retention_line` wrapped to the inner width in `muted`. At 160 and 116 these three lines are removed from the list body (they were scattered in three places, M-14) while the pane is drawn, and are put back there if step 4.5 drops the pane under height pressure; at 80 they stay where Phase 3 left them. |
| 4.5 | Compose the questions screen and degrade under height | `OBS/render.py` (`_panel_lines` 359-387, sizing 433-481) | At `width_class` `full` and `line`: the panel is `strip + list frame + retain pane` in that order (strip first, so the count leads; list frame body: disclosure, rows, cut text, `DESK_SELECTED_HIDDEN`, empty and window-full text, notes; row roles from Phase 1, caveats `muted`). Height rule: the panes are drawn only if at least `MIN_QUESTION_ROWS = 3` question rows (or all of them, when fewer exist) still fit; if not, drop the RETAIN pane first, then the strip, and relocate what each held in the same step: dropping the RETAIN pane puts `panel.run_line`, `panel.caveat_line` and `panel.retention_line` back in the list body in the Phase 3 order (run line near the top, caveat before the rows, retention sentence last); dropping the strip puts `panel.counts_line` back as a plain list-body line. The run line, the caveat and the retention sentence are required text (RR lines 42, 44 and 48; view.py:67, 73, 794), so a pane is never dropped without its lines being relocated and no fact disappears. The relocated lines are fixed rows of the list body: recompute `base` and `capacity` once with the relocated layout (a single retry, not a loop; the relocated layout is the Phase 3 layout, which already fits), so the owner's rule "the questions win on a short terminal" (render.py:444-445) still applies through the unchanged `spare` formula at 447-457. The value 3 is a design choice; measure the real trigger heights at 160 and 116 when implementing and record them. The question line format `<age>  <subject>  reason unknown` and its two-space separator are not changed (`T/test_render.py:653` and the `^\s*\d+[smh]  ` checks at :930-948 pin them). |
| 4.6 | Update tests | `T/test_render.py`, `T/test_view.py`, `T/test_export.py` | Phase 3 helpers (`unframe`, `title_of`) are enough. Phrase checks that read the counts line use `in` on the unframed text (the figure shares its row, so the row no longer starts with the phrase): `test_t19...` (:437-453), `test_decision_3_and_4` (:679-700), `test_f17_f15` (:786-805). Row checks (the exactly-5 `reason unknown` lines :453, `questions shown` :479, :646, `▸ ` :897) read the list pane through `pane_body(lines, QUESTIONS_TITLE, policy)`, a Phase 4 helper in `T/conftest.py` that returns the unframed body of the frame whose top border contains the title. Add tests: figure and `counts_line` present in the plain pass at 160 and 116, absent as a frame at 80; strip, list and retain panes appear in that order at 160 and 116; each pane is exactly `width - 2` wide; at heights 24 and 26 at 116 columns (also 160) the plain screen still contains the run line (`one Run only: <runId>`), the caveat (`no read marker in source: answered questions stay listed`) and the retention sentence (`retention reset at HH:MM; questions observed before this start are not retained`) whether the pane is drawn or dropped, with every line at most the width and at most the height (heights 24 and 26 are chosen to straddle the degrade point; measure the real trigger heights and add them); degrade order at small heights is RETAIN first, then the strip; `#` block font in ASCII mode and no `?`; `count_figure` is not read by export.py. |
| 4.7 | Golden | `T/golden_questions_linkoff.json` | Regenerate with the Phase 2 step 2.7 command. |
| 4.8 | Render gate | `VP/tools/render_compare.py` | G1 to G6; the reviewer checks the strip, the pane titles and the pane order at 160 and 116 against the stacked option in the layout comparison on #606 and the attention-ledger mockup for colour and weight only, and that no invented content (owner, requester, mapped trees) appears (AD-1 to AD-4). |

**Tests and goldens that change:** `T/test_render.py` (phrase and row checks above), `T/test_view.py` (default field only), `T/test_export.py` (source scan), `T/conftest.py` (`pane_body`); `T/golden_questions_linkoff.json` regenerated.

**Byte-identical in this phase:** `record_text` (it still writes `counts_line`), `snapshot_json`, questions-off screens and both release-1 goldens, the question line text, the whole 80-column questions screen.

**Rubric rows scored:** RB-03 (questions: stacked order), RB-04, RB-16, RB-17, plus all earlier rows.

**Migration or rollback:** revert the commit and the golden. `count_figure` is a defaulted field and can stay.

### Phase 5: Decision Desk as question pane plus session-evidence pane (two columns at 160 and 116, three stacked panes at 80)

**Goal:** the question text leads in its own emphasised pane, the linked-session evidence is an aligned `label: value` pane, and the question list sits in its own pane, laid out as in the desk mockups. Show only the one linked session the view already holds.

**Dependencies:** Phase 3 (`_frame`, `unframe`, `title_of`). Owner decision D-1 is ruled (Decision Desk in two columns at 160 and 116) and D-8 (the evidence pane title, below). Step 5.0 builds the two-column composer and its test helpers; Phase 4 no longer does.

**Closes:** M-04, M-12; completes M-09 on the desk fields.

Target layout (widths from 8.3):

```
 160: +-- DECISION DESK (heavy) ----+  +-- <evidence title> ------------------+
      | qid  age ... / question    |  | dispatchId:           w-002          |
      +-- COORDINATOR QUESTIONS ---+  | workerState:          ...            |
      | rows ...                   |  | resource.worktreeId:  ...            |
      +----------------------------+  | notes (DESK_WORKTREE_NOTE ...)       |
        left 76                          right 80
 116: DECISION DESK (full width 114) over  [<evidence> 66] [COORDINATOR QUESTIONS 46]
  80: DECISION DESK (78) / <evidence> (78) / COORDINATOR QUESTIONS (78), stacked
```

| Step | Action | Files | Details |
|---|---|---|---|
| 5.0 | Two-column composer and test helpers | `OBS/render.py`, `T/conftest.py` | `_two_columns(left: list[Line], right: list[Line], wl: int, wr: int, gap: int = 2) -> list[Line]`: rows from `zip_longest(left, right, fillvalue=blank)`, each side padded by `cell_len` to its width, right-side span offsets shifted by the character length of the padded left side plus the gap (character offsets, never cell widths). Test helpers in `T/conftest.py`: `split_columns(line, left_width, gap) -> tuple[str, str]` slices by cell width (write it with `cell_len` if the `rich.cells` chop helper differs in 15.0.0); `panes_flat(lines, policy) -> str` returns the whitespace-collapsed left text then the right text, so phrase checks do not read across the gap; `pane_body(lines, title, policy) -> list[str]` returns the unframed body of the frame whose top border contains the title (also used by Phase 4 for the stacked questions screen, where it is defined first). |
| 5.1 | Evidence pane title | `OBS/view.py` (constants near 85-99) | Add `DESK_EVIDENCE_TITLE`. The mockup titles are `AFFECTED SESSION EVIDENCE` and `AFFECTED SESSIONS`, which claim more than the code knows (AD-4: one linked session, no requester, owner or affected list; `DESK_WORKTREE_NOTE` view.py:87-90). The default wording is `LINKED SESSION`, reusing the existing link vocabulary (`linked`, parse.py:468-472); wording is decision D-8 and a spec edit to RR line 57. The render gate accepts any title that does not claim an affected list. `DESK_TITLE` (view.py:85) stays the desk question pane title, so tests that look for it keep one literal. |
| 5.2 | Aligned field lines | `OBS/render.py` (replaces the field loop at 347-353) | `_field_lines(label: str, value: str, inner: int, label_width: int, policy) -> list[Line]`. If `cell_len(value) <= inner - label_width - 1`: one line, label `muted` padded to `label_width`, value in its role. Otherwise the label line, then the value wrapped to `inner - 2` with a two-cell indent (today's behaviour, render.py:347-353). `label_width` is the longest label plus its colon across `desk.session_fields` (`resource.worktreeId:` is 20 cells). Values of `workerState`, `dispatchStatus` and the liveness verdict use `STATE_ROLE` from P1; `nextAction.kind` stays `body` (RR line 31). Field order is the order of `session_fields` (view.py:843-853), unchanged. |
| 5.3 | Pane builders | `OBS/render.py` (`_desk_lines` 329-356) | `_desk_question_pane(desk, width, policy) -> list[Line]`: heavy frame titled `DESK_TITLE`; first body line `qid  age <age>` (age `attention` bold, as the list ages and RB-01(c) require; `attention` bold qid), then `wrap(desk.ask, inner)` limited to `DESK_TEXT_LINES` (view.py:99) with the last line cut by `...` as today, in `attention` bold. `_desk_evidence_pane(desk, width, policy)`: round slate frame titled `DESK_EVIDENCE_TITLE`, the field lines from 5.2, then `desk.notes` wrapped in `muted`. Both are pure functions of `DeskView` and never read `View` record fields; the question text is read only here and in `_question_line` (screen-only rule). |
| 5.4 | Compose and budget | `OBS/render.py` (`_panel_lines` 359-387, sizing 458-479) | At `full`: left = question pane over the list frame (round, P3 rule), right = evidence pane, joined by `_two_columns` with `RIGHT_DESK = 80` and `left = width - 4 - 80` (76 at 160). At `line`: question pane at full width, then `_two_columns(evidence, list, wl = width - 4 - 46, wr = 46)` (66 and 46 at 116). At `short`: three stacked frames. The panel height is `max(left, right)` at `full` and the sum of the parts elsewhere. When the available rows are fewer than the question pane plus one list row, or fewer than the evidence pane, use the existing `DESK_HIDDEN` notice path (view.py:97, render.py:458-471) instead of a partial desk, so a half-drawn desk never reaches the screen. `DESK_TEXT_LINES` stays 4; note that at 160 the question pane inner width is 72, so a long ask reaches the `...` cut sooner than the old full-width text (decision D-6 covers any change to the cap). |
| 5.5 | Tests | `T/test_render.py`, `T/conftest.py` | Use `pane_body(lines, title, policy) -> list[str]` (defined in step 5.0), which returns the unframed body of the frame whose top border contains the title. Rework the R3 tests on it: `:891` (`▸ ` row in the list pane, `DESK_TITLE` in `title_of`, flat `dispatchId: w-002` through `panes_flat`), `:919` (unlinked reasons in the evidence pane, `dispatchId:` absent), `:930` (age and `reason unknown` per row in the list pane), `:943` and `:958` (desk text bounded to four lines with `...` at 80 columns: now `pane_body(lines, DESK_TITLE)`), `:970` (hostile text inert), `:985`, `:990` (desk gives way by height at 116), `:1009`, `:1017`. New tests: the 64-hex hash of the plan-ask question in the 46-cell list pane at 116 is hard-split across lines with nothing lost (the layout comparison on #606 showed Rich cutting it with an ellipsis, so the product `wrap` path must be tested); label column is aligned across all fields; a value that does not fit beside its label moves to its own indented line and a value wider than the inner width is hard-split with nothing lost; the Q7 hash (RB-19) is whole in the question pane at 160 (inner 72), 116 (inner 110) and 80 (inner 74); a 64-character `resource.worktreeId` at 116 (evidence inner 62) is hard-split with nothing lost; a desk screen is never taller than `policy.height` at 8, 12, 24, 40, 44. |
| 5.6 | Golden | `T/golden_questions_linkoff.json` | Unchanged by this phase (the link-off screen has no desk). `T/golden_release1_surface.json` unchanged. |
| 5.7 | Render gate | `VP/tools/render_compare.py` | G1 to G6 with screens `desk` and `desk-planask`; the reviewer scores RB-03 (desk), RB-14, RB-10 on the desk fields, RB-19 and the earlier rows. |

**Tests and goldens that change:** `T/test_render.py` (R3 block), `T/conftest.py`. No golden changes.

**Byte-identical in this phase:** `record_text` (question lines still `q.text`, never `q.shown` or `q.ask`), `snapshot_json`, questions-off and link-off screens.

**Rubric rows scored:** RB-03 (desk), RB-10 (desk fields), RB-14, RB-19, plus all earlier rows.

**Migration or rollback:** revert the commit. `DESK_EVIDENCE_TITLE` is an unused constant after a revert. If D-8 changes the wording, only the constant and the golden-free tests that name it change.

### Phase 6: Ledger screen panes (attention slot, observation window, framed table)

**Goal:** the ledger screen (questions off) gets the same pane vocabulary: the existing gap notice in an amber attention pane, the existing freshness, counts and changes lines in an observation pane, and the worker table in a titled pane, using only data already on the screen. No owner, requester, mapped-tree or SIGNALS content (AD-1 to AD-4).

**Dependencies:** Phase 3 (`_frame`), Phase 2 (headings at every width), owner decision D-2. Under "freeze questions-off" this phase is blocked for the questions-off screens and M-06 stays open.

**Closes:** M-06; completes M-02 (all panes titled and boxed).

| Step | Action | Files | Details |
|---|---|---|---|
| 6.1 | Measure before choosing the 160-column frame | `OBS/render.py` (`_flags_text` 141, `_columns` 155-230) | The full table uses all 160 cells (render.py:159-192: 2 + 114 + 22 + 12 + 10), so a border needs 2 cells from the elastic `flags` column. Measure the longest `_flags_text` over the fixtures (`base`, `empty`, `source-loss`, `injection`, `missing-fields`, `long-identifiers`) and the `FROZEN` marker case. [UNVERIFIED: this was not measured.] If `flags` at 10 cells does not clip, use a border-only frame (no padding, no margin, inner width `width - 2`) for the table at every width; otherwise keep the 160-column table unframed under a titled rule and frame it only at 116 and 80. Record the result in the commit message. |
| 6.2 | Parameterise the columns | `OBS/render.py` (`_columns` 155-230, `_row_segments`, `_header_lines`) | `_columns(policy, avail: int)` uses `avail` instead of `policy.width` in every width sum; callers pass the pane inner width. The three layouts keep their column sets (AD-3, AD-6). Rows and heading clip to `avail`. |
| 6.3 | Compose the head | `OBS/render.py` (head 409-414, gap part 482-485, `_notes` 290-301) | Order: title bar (P2), attention pane (heavy amber, title `QUESTIONS_TITLE`, body `view.gap_notice`, or `panel.summary` when questions are on and nothing is read yet, as render.py:482-485 does today), observation pane (round slate, title `OBSERVATION WINDOW`, body `header2`, the counts lines and `changes_line`; `counts_lines` is called with the inner width, so M-16 still holds), then the ledger pane (round slate, title `view.ledger_title`, body heading and rule, rows, and the overflow line `window.text  window.more_text`). `QUESTIONS_TITLE` reuses the panel title because the gap notice is what the questions panel replaces (`panel.replaces_gap`). `OBSERVATION WINDOW` is the mockup pane title for the per-source freshness line that `header2` already carries; any other wording is a spec edit. The `/filter` input line, the one-off message and the footer stay outside the frames. |
| 6.4 | Small-height fallback | `OBS/render.py` (`_compose`) | Build the framed head; if the framed screen would leave fewer than three ledger rows at `policy.height`, use the P2 plain head instead (the height matrix includes 12, where `golden` keys `lines_*x12` must stay plain). Threshold chosen from measured row counts at heights 12, 24 and 40, and recorded; the forced single row (render.py:502) remains the last resort. Every frame row is in `top` or `body`, so `reserved` and `capacity` (499-503) account for it. |
| 6.5 | Tests | `T/test_render.py`, `T/test_commands.py`, `T/test_golden_contract.py`, `T/test_question_cap.py` | Frame-aware versions of the whole-line checks on the ledger screen: `GAP_NOTICE in lines` (:242, :490, :494, :509 and `T/test_commands.py:121`) becomes `GAP_NOTICE in [unframe(l) for l in lines]`; `no successful worker-list read yet` and the two `no observed items` lines (:352-356); `^\d+/80 shown\s+\+\d+ more` (:94, :337); row `startswith` checks (:373-375, `▸`, ` *`) through `unframe`; the header and row checks at :287-326; `collected 100 / reported 428` stays on one line (`T/test_golden_contract.py:43-58`). `T/test_inspector_scroll.py` is unaffected (the inspector returns earlier, render.py:488-493). New: at heights 12 and 8 the screen falls back to the plain head; at 24, 40, 44 the framed screen has at most `policy.height` rows; no pane holds invented content (a source scan that the pane bodies are built from `view.gap_notice`, `header2`, counts, `changes_line`, the ledger rows). |
| 6.6 | Goldens | `T/golden_release1_surface.json` | Regenerate (step 2.7 command; `printed_*` stays SGR-free through `_printed`, step 1.6(c), and the no-escape test of step 2.7 must still pass). Expected diff: `lines_{160,116,80}x40` and `printed_*` for the five variants; `lines_*x12` unchanged if 6.4 keeps the plain head at 12. `T/golden_release1_records.json` and `T/golden_questions_linkoff.json` unchanged. |
| 6.7 | Render gate | `VP/tools/render_compare.py` | G1 to G6; RB-02 (ledger), RB-18, and all earlier rows. |

**Tests and goldens that change:** the tests above; `T/golden_release1_surface.json` regenerated.

**Byte-identical in this phase:** `record_text`, `snapshot_json`, `header1`, `header2`, `gap_notice` (enforced by `golden_release1_records.json`), the link-off golden, the inspector screen.

**Rubric rows scored:** RB-02 (ledger), RB-18, plus all earlier rows.

**Migration or rollback:** revert the commit and the regenerated golden. The fallback in 6.4 means a revert is also possible per height without touching the pane code.

### Phase 7: Spec reconciliation, final gate matrix and PR

**Goal:** make the written spec match the built screens, run the complete gate matrix once, and open the PR as the repository requires.

**Dependencies:** Phases 1 to 6 closed (or P5 skipped if D-1 is later changed). Owner decision D-11 (RR 61 wording) for step 7.1.

**Closes:** no finding on its own; it records the spec changes the closed findings require.

| Step | Action | Files | Details |
|---|---|---|---|
| 7.1 | Spec edits | `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md` | Lines 17 (title bar and badge), 25 (box glyph ASCII forms), 41 (RETAIN CONTEXT built), 57 (Decision Desk in two columns; RR 43 stays stacked, AD-8), 61 (reconcile with RR 42: the two 80-column invariant lines and "reachable only through the inspector"; the owner chooses the wording, G-H), 70 (muting implemented), 20 (token reads `POLICY FROZEN unavailable (no source)`, view.py:948), 33 (the `flags` column exists at 116 and 80). Pane titles `OBSERVATION WINDOW`, `RETAIN CONTEXT` and the D-8 desk evidence title are recorded there. |
| 7.2 | Keep the baseline capture honest | `VP/inputs/tools/render_current.py` | Update its docstring (lines 6-9 say the ANSI captures are empty of escapes). Keep `VP/inputs/current/` as the pre-fix baseline; write the post-fix harness output under the gate output directory, not over it. |
| 7.3 | Final gate matrix | `VP/tools/render_compare.py`, `T/test_live_screen_pty.py` | `render_compare.py --check --heights 44,40,24,12,8` exactly as defined in step 0.3: widths 160, 116, 80 at the mockup heights (48, 42, 42) and the text matrix at heights 44, 40, 24, 12, 8; the five passes truecolor, 256, 16-colour, NO_COLOR, ASCII; a pty run at each width; one fresh reviewer per width scores every rubric row. Every High and Medium row must pass; Low rows pass or are logged as deferred. |
| 7.4 | Optional Zellij manual check (not a gate) | `VP/zellij-note.md` (new) | Q6 is no-go as a dependency. If the owner wants it, run in a live Zellij 0.44.2 session: `zellij action dump-screen --help` first (the online docs describe a newer release, web-02 A7), then the observer in a pane and `zellij action dump-screen --ansi`; record colour, box and wide-glyph fidelity. The observer may read `ZELLIJ` as a hint, never as a requirement (web-02 A5, external context). [UNVERIFIED until run.] |
| 7.5 | Full checks | repo root | `uv run pytest tests/observe/ -v`, `make test`, `make lint`; confirm `T/test_commands.py:747-772` pass (gate lines intact); confirm `git diff` has no change to `src/superclaude/cli/observe/export.py` and no staged `.claude/` path; stage `.dev/tasks` as the repository rule requires. |
| 7.6 | Open the PR | branch | Verify `git remote get-url origin` and `gh repo view IronbellyOrg/IronClaude --json nameWithOwner -q .nameWithOwner` both name `IronbellyOrg/IronClaude`; `git fetch origin` and rebase onto `origin/master` before pushing; then run `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."` and check that the returned URL is `https://github.com/IronbellyOrg/IronClaude/pull/N`. Never a bare `gh pr create`, never the upstream repository. |

**Tests and goldens that change:** none in code; spec and docstring only.

**Rubric rows scored:** all rows, final.

**Migration or rollback:** documentation only; revert the commit.

### 8.8 Open items, [UNVERIFIED] claims and research findings excluded from plan steps

Items below are not asserted as fact in any step. Where a step depends on one, the step says so.

| Item | Tag | Where it bites | Handling |
|---|---|---|---|
| Playwright MCP can turn Rich `export_html` into a faithful PNG offline; DejaVu Sans Mono covers the mockup glyphs | [UNVERIFIED] | Step 0.4, gate G3 | Proven once in 0.4; fallback is the text and ANSI tier |
| A reviewer subagent has no Playwright tool, only Read | assumption | G3, G4 | The session rasterises; the reviewer only Reads PNGs (both Gate 1 QA reviewers read mockup PNGs successfully) |
| Constructor and `draw` signature of the real `LiveScreen` under a pty; whether `run_interactive` accepts `--fixture` | [UNVERIFIED] | Step 1.6(g) | Read commands.py:257-279 at implementation time; the child builds `LiveScreen` itself |
| Whether Rich emits a bare reset under NO_COLOR with `Live` | [UNVERIFIED] | Step 1.6(g) | Measure, then fix the assertion |
| Mapping from real `workerState`, `dispatchStatus` and liveness words to the four state colours | [UNVERIFIED], RR 93 says no verified settled mapping | Step 1.4 | Only the minimum fixed `STATE_ROLE` table of step 1.4 is coloured (owner decision D-7, default stated); every other value is `body`; the word is always printed |
| Longest `_flags_text` versus the 10-cell `flags` column | [UNVERIFIED] | Step 6.1 | Measure first; fallback is an unframed 160-column table |
| Which of the three `+1` terms in `spare` is which (render.py:454-456) | [UNVERIFIED] | Steps 3.4, 5.4 | Read the comment at render.py:444-445 first; the terms are not edited |
| Exact `PYTHONPATH` layout and approval for regenerating the release-1 golden | [UNVERIFIED] | Step 2.7 | The plan regenerates from the current tree, not from release 1 source |
| Whether East-Asian-ambiguous box and block glyphs are one cell in the owner's terminals | [UNVERIFIED] | All frames | Rich's `cell_len` says one; carry as a caveat |
| Mockup background (dark navy) and light-terminal behaviour of the palette | [UNVERIFIED] | RB-01 | Background is not scored |
| Selected-question look (M-18) | [UNVERIFIED] (no selected row in any mockup) | Step 1.4 | Scored against RR line 50 (glyph kept) plus a bold amber role, not against a mockup |
| Plan-approval ask content (path, file list, 64-hex hash) stored as question rows | [UNVERIFIED] (`pr-591-comment.md` lines 26-31) | Q7 fixture | Fixture is synthetic; confirm with the plan-ask source |
| Zellij: floating panes, `dump-screen --ansi` fidelity, command panes, theme read at runtime, presence in CI | [UNVERIFIED] | Step 7.4 only | Not a dependency (Q6) |
| Interaction of fixtures `injection` and `long-identifiers` with styling | [UNVERIFIED] | Phase 1 gate | Include both in the harness matrix |
| Owner rulings D-1 to D-12 and OPEN-1 to OPEN-3 | open | see 8.2 | Defaults stated; effect if different stated |

Research findings that are deliberately not in a plan step:

| Finding | Rationale for exclusion |
|---|---|
| Rich `Panel`, `Table`, `Layout`, `Columns` returned from `render()` (03 option P5, 01 option 4) | Breaks `T/test_render.py:399`, adds height uncertainty, and `safe_box` does not give ASCII borders; rejected in 8.1 Q1 |
| Block digit font as a hard requirement | FINDINGS does not require it (01 section 8.2 item 6); the plan uses it when the strip is wide enough and falls back to a bold figure |
| Age gutter (fixed-width age column) from M-07 | The `<age>  <text>` two-space form is pinned (`T/test_render.py:653`, :930-948) and RR line 50 fixes the age format; not changed |
| SIGNALS bars and tiles, "8 owners / 80 sessions / 80 mapped trees", two-line register rows, requester, owner, Affected lines | Accepted divergences AD-1 to AD-4: no real data behind them |
| Three-column signal-bridge layout at 160 | The full table needs all 160 cells (render.py:159-192); AD-3 |
| `export_text(styles=True)` as the styled capture | Ignores NO_COLOR and the colour downgrade (probe, 02 section 2) |
| cairosvg, `rsvg-convert`, freeze, pyte, aha, ansi2html, Pillow | Not installed; Rich SVG needs a browser engine (external: https://github.com/Textualize/rich/issues/2153); each is a new dependency or binary needing owner approval; the plan adds none |
| Reading the Zellij theme at runtime; Zellij chrome row arithmetic | Unverified, and Zellij is not a dependency |
| Making a styled piped `--once --width` the default | Open decision D-4; the default keeps `T/test_commands.py:121` |
| Rich's own NO_COLOR (keeps bold and dim) | The project keeps `color_system=None` under NO_COLOR (G-2); changing it is a separate owner decision |

### 8.9 Integration Checklist

| # | Check | Evidence to attach | Phase |
|---|---|---|---|
| 1 | `uv run pytest tests/observe/ -v` is green at the end of every phase (baseline 766 passed; count grows with added tests) | pytest summary line | all |
| 2 | `T/golden_release1_records.json` exists, is never regenerated, and passes | test result | P2 onward |
| 3 | `record_text`, `snapshot_json` and `export.py` are untouched; `count_figure` is not read by export.py | `git diff --stat` shows no `export.py` change; source-scan test | all |
| 4 | Question text appears only on screen: both hash canaries pass (record and snapshot) | test result | P0 onward |
| 5 | Gate lines `QUESTION_GATE_PASSED` and `QUESTION_LINK_PASSED` (commands.py:67, 70) unchanged; `release-gates.md` and `Task 18` still in commands.py | `T/test_commands.py:747-772` | P1 onward |
| 6 | No `Console(`, `from_markup`, `sorted(`, `.sort(` or adapter, collector, parse import in render.py; no `Console(`, `NO_COLOR`, `COLUMNS` literal outside terminal.py (also not in `theme.py` comments) | `T/test_render.py:400-404`, `T/test_terminal.py:181-198` | P1 onward |
| 7 | `len(group.renderables) == len(screen_lines(...))` still holds | `T/test_render.py:399` | all |
| 8 | NO_COLOR pass has zero ESC bytes and the same text as the coloured pass after SGR removal, at 160, 116, 80 | `checks.json` | all |
| 9 | ASCII pass is pure ASCII with `+ - \|` borders and `#` block glyph; no `?` where a border or glyph belongs | `checks.json` | P3 onward |
| 10 | No SGR 5 or 6 and no mouse mode sequence in any pass or in the live pty stream | `checks.json`, pty test | all |
| 11 | Every line at most the width in cells and at most the height in rows at 8 (diagnostic), 12, 24, 40, 44, 48; the footer is the last live row | height test, pty test | P0 onward |
| 12 | The 16-colour theme has eight distinct role colours | `T/test_theme.py` | P1 |
| 13 | Both presentation goldens regenerated from the current tree with the recorded command, in the same commit as the change that moved them | commit diff | P2, P3, P4, P6 |
| 14 | One fresh reviewer per width scored the in-scope rubric rows; at most 3 iterations; all High and Medium rows pass; stop log written if not | `VP/scores/<phase>/` | all |
| 15 | OPEN-1, OPEN-2, OPEN-3 treated as Medium until the owner rules; D-1 to D-12 recorded with the owner's answer | decision record in the PR body | P2, P4, P5 |
| 16 | `make lint` and `make test` pass; no `.claude/` path staged; `.dev/tasks` staged | command output, `git status` | P7 |
| 17 | PR opened only by `/sc:pr-submit --monitor 3` against `IronbellyOrg/IronClaude`; branch rebased on `origin/master`; returned URL checked | PR URL | P7 |

### 8.10 Finding-to-phase map (M-01 to M-18)

The Severity column quotes FIND (High, Med, Low); in the Section 4 scale High = Critical, Med = Important, Low = Minor.

| ID | Finding (short) | Severity per FINDINGS | Closing phase | Steps | Rubric row |
|---|---|---|---|---|---|
| M-01 | No colour or weight | High | P1 (frame and strip colours added in P3, P4, P6 and re-scored) | 1.1 to 1.6 | RB-01, RB-09 |
| M-02 | No boxed titled panes | High | P6 (questions and desk panes in P3) | 3.1 to 3.3, 6.3 | RB-02 |
| M-03 | Questions screen has no two columns | High | none: closed by owner ruling AD-8 (stacked kept, 2026-11-18) | n/a | RB-03 (stacked order) |
| M-04 | Decision Desk stacked | High | P5 | 5.3, 5.4 | RB-03 |
| M-05 | Count has no weight | High | P4 | 4.1 to 4.3 | RB-04 |
| M-06 | Ledger lacks attention slot, observation pane | Medium | P6 | 6.1 to 6.4 | RB-18 |
| M-07 | Caveats outweigh question rows (OPEN-1) | Medium | P4 | 4.4, 4.5 | RB-16 |
| M-08 | Absent values not muted | Medium | P1 | 1.4 | RB-11 |
| M-09 | State values uncoloured | Medium | P5 (ledger rows in P1, desk fields in P5) | 1.4, 5.2 | RB-10 |
| M-10 | No column heading at 116 and 80 | Medium | P2 | 2.2 | RB-12 |
| M-11 | 80-column key list cut | Medium | P2 | 2.3 | RB-13 |
| M-12 | Desk emphasis and alignment | Medium | P5 | 5.2, 5.3 | RB-14 |
| M-13 | Title bar and READ ONLY badge (OPEN-3) | Medium | P2 | 2.5 | RB-15 |
| M-14 | No RETAIN CONTEXT (OPEN-2) | Medium | P4 | 4.4, 4.5 | RB-17 |
| M-15 | Footer pair split, no rule | Low | P2 | 2.3 | RB-20 |
| M-16 | 80-column counts cut inside a token | Low | P2 | 2.4 | RB-21 |
| M-17 | Wide blank band after id | Low (optional) | P2 | 2.6 | RB-22 |
| M-18 | Selected question glyph only | Low | P1 | 1.4 | RB-23 |

Guards, questions and accepted items: G-1 is enforced from P3 (steps 3.1, 3.2, 3.10 and RB-07, re-run in every later gate); G-2 closes in P1 (steps 1.1, 1.2, RB-09); Q4 P1; Q5 P1 (steps 1.5, 1.6); Q7 P0 (0.6) and P3 (3.7), re-pinned in P5 (5.5); Q6 P7 step 7.4 (not a gate); AD-1 to AD-7 are respected by the "no invented content" check in the P4 and P6 gates; the spec lines changed by the closed findings (RR 17, 20, 25, 33, 41, 43, 57, 61, 70) are edited in P7.
