# QA Report - Synthesis Gate (Structure Lens)

**Topic:** Observer visual-parity investigation (issue #606)
**Date:** 2026-11-17
**Phase:** synthesis-gate
**Fix cycle:** N/A
**Status:** Complete (verdict FAIL: 2 blocking, 8 minor)

---

**Scope:** six synth files in `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/synthesis/` (synth-01 to synth-06), each read in full; checked against the research files, the code under `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/`, the tests under `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/`, the mockups and the Report Structure in `/home/coder/.claude/skills/tech-research/SKILL.md` (lines 1317-1493). Fix authorization: false. No synthesis or research file was modified.

## Items Reviewed (12-item checklist)

### Item 1: Section headers match the Report Structure template - PASS
- Glob found exactly six files `synth-01` to `synth-06`. Headers seen: `## 1. Problem Statement` and `## 2. Current State Analysis` (synth-01), `## 3. Target State` and `## 4. Gap Analysis` (synth-02), `## 5. External Research Findings` (synth-03), `## 6. Options Analysis` and `## 7. Recommendation` (synth-04), `## 8. Implementation Plan` (synth-05), `## 9. Open Questions` and `## 10. Evidence Trail` (synth-06). Matches the template at SKILL.md:1336-1477 and the mapping table at SKILL.md:1501-1508.
- Subsections 2.N Current State Summary (synth-01 line 384) and 5.N External Research Summary (synth-03 line 114) are present.
- MINOR (m7): synth-05 puts the eight `### Phase N` blocks between `### 8.7` and `### 8.8`, with no 8.x numbering; synth-02 opens with a `#` title line while the others open at `##`. Assembly should normalise.

### Item 2: Table column structures - PASS
- Gap Analysis tables (synth-02 4.1a, 4.1b, 4.1c) use `Gap | Current State | Target State | Severity | Notes` exactly (lines 149, 172, 188).
- Options Comparison tables (synth-04 lines 96, 174, 245, 302) use `Criterion | Option ...`; per-option tables use `Aspect | Assessment` (template at SKILL.md:1405).
- Implementation tables (synth-05) use `Step | Action | Files | Details` in every phase.
- Open Questions use `# | Question | Impact | Suggested Resolution` (synth-06 lines 11, 20, 36, 48, 68). Evidence Trail uses `File | Topic | Agent Type` and `File | Topic`.

### Item 3: No fabrication (every claim traced) - PASS, with the limit stated below
Verified by my own tool calls (not by reading other QA reports):
- Code line cites checked by Read: render.py 12-14, 62-80, 94-135, 141-230 (`_columns` arithmetic: 2+114+10+22+12 = 160 at 160 columns), 233-243, 246-249, 255-287, 304-308, 311-326, 329-356, 359-387, 390-521, 524-531; terminal.py 21-24, 30-34, 37-51, 63-70, 73-92, 110-125, 133-160; view.py 48-113 (all constants named in synth-05 exist), 225-270, 377-385, 761, 836-860, 938-958; commands.py 58-70, 200-279; export.py 18-22, 96-112, 156-182; parse.py 468-475, 496-506; collector.py 150-155.
- Test line cites checked: test_render.py 22-77, 140-175, 177-185, 245-265, 396-404, 475-482, 544-549, 608-678, 744-760, 850-900, 936-1000; test_terminal.py 105-116, 181-198; test_commands.py 283-298, 664-692, 747-772, 828-842; test_export.py 236-244; test_linkoff_screen_reference.py 28-76; release1_surface.py 38-64; test_golden_contract.py 40-60; test_question_cap.py 75-78, 119-122; test_inspector_scroll.py 34-40; conftest.py 205-235.
- Measured claims reproduced: `uv run pytest tests/observe/ -q -p no:cacheprovider` printed `766 passed in 22.78s`; golden shape is 5 variants x 14 keys (30 `lines_*`, 15 `printed_*`), no ESC byte, no trailing newline in the release-1 golden and a trailing newline in the link-off golden; link-off scenarios `five` 24/24/25 and `long_subject` 22/22/23 lines. Rich 15.0.0: `safe_box` True and False print the same rounded border; `export_text(styles=True)` returns SGR under NO_COLOR while the stream is plain; `auto` on a StringIO prints no colour; the 16-colour and 256-colour downgrade of the eight mockup roles matches the table (15/7/8/11/14/7/7/7 and 189/145/60/214/80/115/210/147); `box.HEAVY` and `box.ASCII` exist; `Live(screen=True)` with 8 lines at height 5 wrote L0 to L4, no ellipsis; a non-terminal console wrote nothing; `cell_len` of the 16-character escape example in research 01 line 61 is 16 by the same rule (a shorter SGR string I tried gave 14, consistent with ESC counting 0). Mockups: 48/42/42 line frames, minimum line width equals the width, bold counts 3 to 16 per `.ansi`, 48 ESC lines in `160/signal-bridge.ansi`, 0 ESC in `current/160/ansi-ledger.txt`; pane borders in 160/signal-bridge, 160/116/80 decision-desk and 80 attention-ledger match the geometry in synth-01 2.4. Q7: a reproduction with a 211-character ask put the 64-hex hash whole on its own desk line at 160, 116 and 80 and out of the list line.
- Research cites spot-checked (R01:61, 85, 125-126, 208-215; R02:197-198; R03:36, 204, 220; R04:63-76; R05:76-77): all exist and say what the synthesis says.
- No fabricated fact found. Cite drift is listed as MINOR m6.
- Limit: URLs in synth-03 and the external-context notes elsewhere were traced to `research/web-01-*` and `research/web-02-*` and cross-checked only where a local probe could test them (items above). I did not fetch the remaining web pages; those statements are reliance, not verification.

### Item 4: Evidence citations use actual file paths - PASS
Every claim in synth-01, synth-02, synth-04 and synth-05 carries a path with line numbers or a function name; paths are relative with a stated base or absolute. No "the system handles X" style claims found.

### Item 5: Options analysis quality - PASS
synth-04 gives three options for each of Q1 (A, B, C), Q3 (H1, H2, H3), Q4 (D1, D2, D3) and Q6 (Z1, Z2, Z3), each with description, mechanism, effort, risk, reuse, files and pros and cons, plus a comparison table.

### Item 6: Implementation plan specificity - PASS
synth-05 names files, functions, signatures, line ranges, test names and commands in every step (for example 1.1 `TerminalPolicy.color_system` at terminal.py 37-51 / 73-92 / 121; 3.2 `_frame(title, body, width, policy, *, weight)`; 4.2 `_two_columns(...)`). No generic "create a service" steps. One logic gap in a step is recorded under Item 7 (B2).

### Item 7: Cross-section consistency - FAIL (2 blocking findings)

Passed parts: every gap in Section 4 has a closing step in Section 8 or an owner decision (synth-05 8.10 maps M-01 to M-18; G-1 to P3, G-2 to P1, Q5 to 1.5/1.6, G-F to 1.6(g), G-G to 0.7/3.8, G-A to 2.1/2.7, G-H and stale spec lines to 7.1, Zellij to 7.4, O-1 and OPEN-1 to OPEN-3 to D-1 and D-3); Section 6 options cite Section 2 evidence; the plan's width arithmetic is consistent (1+114+2+42+1 = 160; 1+70+2+42+1 = 116; 1+76+2+80+1 = 160; 1+66+2+46+1 = 116; inner width = pane - 4 gives 154/110/74 at the panes of 3.7).

**B1 (blocking, IMPORTANT): the phase labels and the order of work contradict each other across Sections 3.8, 7 and 8.**
- synth-02 3.8 Q2 row (line 132): P3 "width-gated 160 layout", P4 "boxed panes", P5 "optional Rich renderables".
- synth-04 7.1 recommended sequence (lines 321-329) and 7.2 Q2 row (line 354): P3 = additive two-column layouts behind O-1 (160 then 116), P4 = boxed panes and the count tile. Columns come before panes.
- synth-05 8.1 Q2 row (line 10) and the phase blocks (lines 208, 237, 278, 317): P3 = single-column frames, P4 and P5 = two-column questions screen and Decision Desk, P6 = ledger panes, P7 = spec and PR. Panes come before columns, and P5 means a different thing than in 3.8.
- Section 8 does not say it supersedes the Section 7 sequence, so the assembled report gives the developer two orders and three meanings for "P3", "P4" and "P5". The "Recommended sequence" in Section 7 is the thing Section 8 is meant to detail.
- Required fix: in synth-04 rewrite the 7.1 sequence and the 7.2 Q2 row to the P0 to P7 scheme of synth-05 (P3 frames, P4 questions two-column, P5 desk two-column, P6 ledger, P7 reconcile and PR), keeping the "160 then 116" split as a note inside P4 and P5; in synth-02 3.8 relabel the Q2 row as "research 03 grouping P0 to P5; the report plan is P0 to P7 in Section 8", or replace it with the P0 to P7 summary.

**B2 (blocking, IMPORTANT): Phase 4 step 4.5 drops required facts at small heights while claiming "no fact disappears".**
- synth-05 step 4.4 (line 263) removes `run_line`, `caveat_line` and `retention_line` from the left body at 160 and 116 and puts them only in the RETAIN CONTEXT pane.
- Step 4.5 (line 264) then says: if the right column is taller than the left budget, "drop the RETAIN pane first, then the tile; the tile's text then reappears as a line in the left body, so no fact disappears". Only the tile text is relocated. Dropping the RETAIN pane removes `one Run only: <runId>`, `no read marker in source: answered questions stay listed` and `retention reset at HH:MM; questions observed before this start are not retained`.
- Those lines are required: the retention sentence and the caveat are checked as required text (synth-02 SC-8, synth-05 RB-05 and the T19 phrase checks at test_render.py:437-453 named in 4.7), and the right column is the taller one in ordinary cases (tile frame + 5-row figure + counts text + RETAIN frame is roughly 18 rows against a left body of roughly 11 rows with 5 questions), so the drop rule would fire at the short heights the questions-win decision (render.py:444-445) is about.
- Required fix: in 4.5 state that when the RETAIN pane is dropped its three lines return to the left body (counted in the budget), or compute the left budget so the pane is never dropped without relocation; add a test at heights 24 and 26 at 116 that the retention sentence, the caveat and the run line are present.

### Item 8: Doc-only claims excluded from Sections 2, 6, 7, 8 - PASS
Spec and mockup facts (RR, FINDINGS, mockups) appear only as design target or spec-versus-code comparison and are tagged. Section 2 architecture statements are code-traced or probe-measured. Section 8 steps rest on code reads and say so (synth-05 line 3). No architecture claim rests on a document alone.

### Item 9: Stale docs surfaced - PASS
synth-02 4.3a and 4.3b list every CODE-CONTRADICTED and STALE DOC finding (width classes, `safe_box`, styled export route, `FROZEN` token, M-10 location, 153 cells, RR 61 versus RR 42, gate state, line drift); synth-06 9.5 repeats them with the corrected-claims table C1 to C8. I confirmed RR line 20 (`FROZEN unavailable`) against view.py:948 (`POLICY FROZEN ...`), RR line 43 against render.py:359-387, and the missing `READ ONLY` text by grep.

### Item 10: Content rules compliance - PASS
Tables used for multi-item data, ASCII diagrams present (synth-01 2.8, synth-03 5.1 and 5.3, synth-05 8.1, Phase 4 and 5), no full source reproductions (the two one-line regeneration commands in 2.7 are commands, not code). The project rule for `uv run` holds: the only `python` hit in the synthesis is a venv path. MINOR (m2): the C8 rule in SKILL.md:1380 asks that an unwired in-scope capability carry or link a remediation task; RN-1 to RN-3 (synth-02 4.2) carry specific changes but are not tied to the plan steps that implement them.

### Item 11: Completeness - PASS
All ten sections have content; grep for `TBD|TODO|FIXME|XXX|lorem|placeholder` over the six files returned no match. Command templates with `<phase>` and `<n>` are intentional.

### Item 12: No hallucinated file paths - PASS
Checked by `ls`/Glob: every existing path cited exists (`.dev/reviews/orchestrator-tui-alignment-20261113/05-observe-built-state.md`, `.dev/issues/409/ponytail-review-20261116/{tests-and-fixtures,design-docs-and-gates}.md`, `.dev/issues/409/pr-591-comment.md`, `.dev/issues/409/attachments`, `.dev/issues/409/owner-pass-record-20261112.md`, `.dev/issues/606/issue-body.md` (line 84 names the four golden and reference files), the spec folder with `rendering-rules.md` (107 lines) and `release-gates.md`, `.dev/issues/409/visual-parity/{inputs,merged}/...`, `src/superclaude/cli/observe/{fixtures,snapshot.schema.json,theme.py parent}`, `tests/observe/*` including `spike_child.py`, `/usr/local/bin/zellij` 0.44.2, the four `~/.config/zellij` files at 53/58/265/252 lines, DejaVuSansMono.ttf, `Makefile`). New files named in the plan (`OBS/theme.py`, `T/test_theme.py`, `T/test_styled_capture.py`, `T/test_height_budget.py`, `T/live_child.py`, `T/test_live_screen_pty.py`, `T/golden_release1_records.json`, `VP/tools/render_compare.py`, `VP/rubric/*`, `VP/scores/*`, `VP/png-route.md`, `VP/zellij-note.md`) have existing parent directories (`VP/tools/` and `VP/rubric/` are new subdirectories of the existing `.dev/issues/409/visual-parity/`).

## Overall Verdict: FAIL

Two blocking findings (B1, B2), both under Item 7. Eight minor findings are notes and do not fail the gate on their own.

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| B1 | IMPORTANT (blocking) | synth-02 line 132 (3.8 Q2 row); synth-04 lines 321-329 (7.1 sequence) and 354 (7.2 Q2 row); synth-05 lines 10, 208, 237, 278, 317 | The same labels P3, P4, P5 mean different work in Sections 3.8, 7 and 8, and Section 7 puts two-column layouts before boxed panes while Section 8 puts panes first. No note says which governs. | Make Section 7.1 and 7.2 use the P0 to P7 scheme of Section 8 and relabel the 3.8 row as research 03's own grouping (details under Item 7). |
| B2 | IMPORTANT (blocking) | synth-05 lines 263-264 (steps 4.4 and 4.5) | The degrade rule drops the RETAIN CONTEXT pane under height pressure, which removes the run line, the caveat and the retention sentence (required text), while saying "no fact disappears". | Relocate those three lines to the left body when the pane is dropped, or never drop the pane without relocation; add a test at heights 24 and 26 at 116 (details under Item 7). |
| m1 | MINOR | synth-05 step 3.8 (line 225) and Integration Checklist row 11 (line 417) | Height 8 is labelled "(diagnostic)". `too_small` is `height < MIN_ROWS` (terminal.py:49-52), so 8 rows draw the normal screen; test_render.py:990 loops `range(8, 61)` over normal screens. The "or `policy.too_small`" clause is harmless, the label is wrong. | Say "8 (the minimum drawn screen; the diagnostic starts at 7)". |
| m2 | MINOR | synth-02 4.2 (lines 197-205) | RN-1 to RN-3 do not point at the plan steps that implement them, and no `.dev/tasks/to-do/` remediation task is named (SKILL.md:1380). | Add a "Plan step" column: RN-1 to 1.4, RN-2 to 2.2, RN-3 to 2.3 and 2.3; note that the MDTM task is created from Section 8 by the workflow step. |
| m3 | MINOR | synth-02 rows M-08, M-10, M-11 (lines 158, 160, 161) versus synth-05 8.4 RB-11, RB-12, RB-13 (lines 72-74) and 8.10 (lines 436, 438, 439) | Section 4 rates them Critical as C8 defects "not downgraded"; the rubric and the map call them Medium. Gating is unchanged (High and Medium rows must pass), so only the labels disagree. | Align the severity words or state in 8.4 that the rubric uses the FINDINGS scale. |
| m4 | MINOR | synth-05 step 4.1 and 4.3 (lines 260, 262) | `count_figure` is defined as "the exact figure text already used inside `counts_line`". The text used there (view.py:706-719) is words as well as digits (`unknown (no question read yet)`, `100+ (window full)`, `0 (source window only; ...)`). The block font only has digits and `+`, and the width test `inner >= 4 * len(figure)` would pass for a 7-letter `unknown`. | Define `count_figure` as digits (and `+`) only when `open_total` is an integer, else empty so the tile falls back to the bold text line. |
| m5 | MINOR | synth-06 line 71 (row 39) | Says the guard test is "now :747-760"; Sections 2 and 4 correctly say 747-756 and 762-772 (test_commands.py:747-756 and 762-772). | Use 747-756. |
| m6 | MINOR | synth-02 lines 160 and 174; synth-01 line 351 and 204 | Cite drift: `_columns` names of the `line` layout are at render.py:198-203, not 203-204; test_terminal.py:109 asserts `safe_box is False` (the `is True` assertion is :115); `render_current.py` has 93 lines (wc), not 94. | Correct the cites. |
| m7 | MINOR | synth-05 headings; synth-02 line 1 | Phase blocks have no 8.x numbers and sit between 8.7 and 8.8; synth-02 starts with a `#` title. | Normalise heading levels at assembly. |
| m8 | MINOR | synth-04 7.1 Q3 row (line 317) versus synth-05 8.5 G3 and G4 (lines 94-95) | Section 7 says image-to-image comparison "is not part of the gate" and the H1 route is an optional extra; the Section 8 gate has a rasterise and PNG-scoring step (with a text fallback). | Add to 8.5 G3 that the PNG step is session-only and optional, with the text and ANSI tier as the gate, to match 7.1. |

## Summary
- Checks passed: 11 / 12
- Checks failed: 1 (Item 7), containing 2 blocking findings
- Blocking issues: 2 (CRITICAL: 0, IMPORTANT: 2)
- Minor issues (notes only): 8
- Issues fixed in-place: 0 (fix_authorization: false; no file modified)

**Confidence:** Verified: 12/12 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% for the 12 checklist items against the codebase and local probes. Stated limit: external web pages cited in synth-03 were not re-fetched (see Item 3); that part of Item 3 is reliance on `research/web-01-*` and `research/web-02-*`, plus the local probes listed.
**Tool engagement:** Read: 29 | Grep: 12 | Glob: 5 | Bash: 12 (probes, `sed -n` ranges, `ls`, one test run). No Tavily or web calls (`tavily_search: 0 | tavily_extract: 0 | web_search_fallback: 0 | web_fetch_fallback: 0`). Read + Grep + Glob = 46, above the 12 checklist items.

## Actions Taken
None to synthesis or research files (report-only). Probes ran in `/tmp` private directories that were removed; `uv run pytest ... -p no:cacheprovider` was run once for the baseline count.

## Recommendations
- Fix B1 and B2 in synth-04, synth-02 and synth-05 before assembly, then re-review only those two points (fix cycle 1).
- Fold m1 to m8 into the same pass where cheap (m1, m5, m6 are one-line edits); they do not need a re-review.

## QA Complete
