<!-- /sc:issue feature template (simple). Copy to <D>/issue-body.md and fill every placeholder in place. Keep every heading. Write "Not known yet" under a heading when the description and the codebase pass give nothing; never invent a fact. -->

## Feature Summary

Bring the theme, styling and layout of `superclaude observe` up to the Signal Bridge, Attention Ledger and Decision Desk design references, without changing its read-only or real-data rules. This is a sub-issue of [#409](https://github.com/IronbellyOrg/IronClaude/issues/409), covering a joint visual review, a phased redesign specification with render gates, and implementation by the claiming agent.

## Problem Statement

The read-only observer has shipped R1, R2 and R3 Decision Desk, including the decision to keep question text on screen only, but its presentation falls short of the mockups. The 2026-11-17 audit of real renders found:

- No colour styling, including no implementation of the spec's muted unknown values; a styled export held no escape bytes.
- No boxed, titled panes.
- No two-column Decision Desk: the reference puts the question card on the left and affected-session evidence on the right; the implementation stacks the content.
- No large `SEEN IS NOT RESOLVED` count tile.
- No `RETAIN CONTEXT` panel; the current spec labels it a design reference.

Operators need the mockups' visual hierarchy without misleading claims about unavailable data. **Replicate the theme, styling and layout techniques, not the images exactly.** Missing owners, mapped trees, requester details or multi-session Affected lists, and standing constraints, are accepted reasons for divergence—not reasons to invent values or add sources.

## User Story

As an operator monitoring Orca orchestration, I want clearly framed, styled questions and session evidence, so that I can distinguish what needs attention, what is known and what remains unknown without changing Orca state.

## Proposed Solution

Complete these deliverables in order:

1. **Concurrent review and merged findings.** Run two concurrent reviewer sessions, GPT 6 Astra and Claude Opus 5.5. Each analyzes the actual renders against the three mockups and their 160-, 116- and 80-column text references. Have the reviewers debate the differences and produce one merged findings list, posted to this issue. Separate actionable visual gaps from accepted divergences caused by missing data or constraints.
2. **Phased redesign specification.** Use the merged findings to write and post a phased redesign spec in this issue body. It must cover colour and muted unknowns, framed titled panes, a prominent `SEEN IS NOT RESOLVED` count, the two-column Decision Desk at 160 and 116 columns with a stacked 80-column fallback, and the treatment of the `RETAIN CONTEXT` reference using only available evidence and explicit unknown/unavailable labels. Define measurable criteria, capture dimensions, accepted divergences and a render gate for every phase. The final phase breakdown and detailed visual spec are **Not known yet**; producing them is a deliverable, not work already completed by this draft.
3. **Implementation by the claiming agent.** Include instructions with the spec that the claiming agent runs `/sc:workflow` on it, then implements the resulting plan. Implement one phase, generate its updated renders, compare them with the mockups, and automatically iterate on that phase until its render gate passes before starting the next. The spec must define the automated capture/compare/fix/recheck loop and its stop/escalation conditions. Do not advance with an open High or Medium criterion. Submit PRs to `IronbellyOrg/IronClaude` through `/sc:pr-submit --monitor 3`.

Design references:

- `.dev/issues/409/attachments/attention-ledger.png`
- `.dev/issues/409/attachments/decision-desk.png`
- `.dev/issues/409/attachments/signal-bridge.png`
- `.dev/issues/409/orca-observer-design-package.zip` — text exports of each at 160, 116 and 80 columns.
- `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md` — current rendering rules, including the existing stacked layout and design-reference qualifications.

Keep the observer read-only, use real data only, and keep question text on screen only—not in its persisted record or snapshot. Preserve NO_COLOR, ASCII mode and all three supported widths. No blinking, mouse interaction or animation.

**Output modes (owner direction, 2026-11-17).** The redesign is not limited to ASCII. Full ANSI-styled output (colour, bold, dim and similar attributes, as in the `.ansi` exports of the design package) is the primary rich mode and is designed first-class. ASCII and NO_COLOR stay as fallbacks that must remain readable and escape-free. The spec must say which colour depth it targets (the console uses the `standard` colour system today) and whether richer depths (256 colour, truecolor) are worth detecting; that is a decision for the spec, not settled here.

**Zellij exploration (owner direction, 2026-11-17).** Zellij 0.44.2 is installed (`/usr/local/bin/zellij`) with a shipped config, theme and layouts (`~/.config/zellij/config.kdl`, `themes/aidev02.kdl`, `layouts/agent.kdl` and `default.kdl`), and the owner has confirmed it is present in all workspaces. The planning phase must evaluate, with evidence, whether Zellij adds value as a component of the dashboard, for example for pane and layout composition, floating panes for the Decision Desk, a status or tab bar, theme reuse, or capturing screens for the render gate. The result is a go or no-go recommendation with reasons in the spec. Conditions: the observer must keep working on its own without Zellij (a terminal that is not inside Zellij is supported), it stays read-only, and nothing Zellij-specific may break the three widths, NO_COLOR or ASCII.
Implementation and verification considerations from the codebase pass:

- The console already supports the `standard` colour system. ASCII and colour are currently independent policy decisions, so adding styling must explicitly preserve the required escape-free ASCII fallback. ANSI styling is the primary mode and ASCII is a fallback, not the design limit (see "Output modes").
- Use styled screen captures for the colour gate: width-bound one-shot output calls `console.export_text()` without requesting styles, whereas `LiveScreen` draws the renderable directly. Plain one-shot output alone is not proof that screen colour works.
- Existing tests compare colour-enabled and NO_COLOR printed bytes for equality. Update that expectation deliberately for styling while retaining equal text content and deterministic renders.
- The release-1 golden surface includes screen lines, printed bytes, plain records and JSON snapshots; the link-off golden pins exact screen lines. Separate deliberate presentation updates from unintended export changes.

## Acceptance Criteria

- [x] GPT 6 Astra and Claude Opus 5.5 have completed concurrent reviews and a debate; one merged findings list is posted on this issue, identifying accepted divergences separately.
- [x] A phased redesign spec is posted in this issue body, with observable criteria and a render gate per phase, the automated iteration loop and stop/escalation rules, and instructions for the claiming agent to run `/sc:workflow` on the spec and then implement its plan.
- [ ] After implementation, every phase has recorded render-gate evidence and no High or Medium criterion remains open; each phase passed before the next phase started.
- [ ] Colour styling, framed titled panes and a two-column Decision Desk are visible at 160 and 116 columns; at 80 columns the layout falls back to a readable stacked form. The question card and available linked-session evidence occupy the intended sides at wider widths, without inventing an affected-session list.
- [ ] The prominent `SEEN IS NOT RESOLVED` count and the spec's agreed treatment of `RETAIN CONTEXT` are demonstrated using only available evidence or explicit unknown/unavailable labels.
- [ ] The spec states the targeted ANSI colour depth and its fallbacks, and ANSI-styled output is verified on the live screen path with captures that keep their styling.
- [ ] The spec contains a Zellij go or no-go recommendation with evidence, and the observer still works unchanged outside Zellij.
- [ ] NO_COLOR rendered output contains no escape codes. ASCII rendered output contains neither escape codes nor non-ASCII characters. All three widths remain usable; no blinking, mouse interaction or animation is introduced.
- [ ] Golden files change only deliberately, with reviewed explanations of presentation changes; record/snapshot changes are not accepted as incidental layout changes, and question text remains screen-only.
- [ ] The observer retains its read-only and real-data rules: no write path to Orca, no new data feeds and no invented owners, requester details, mapped trees or multi-session affected scope.
- [ ] Side-by-side captures of Signal Bridge, Attention Ledger and Decision Desk against their mockups at 160, 116 and 80 columns are attached to the closing PR, documenting accepted divergences.

## Out of Scope

- Remote fleet support, tracked by [#604](https://github.com/IronbellyOrg/IronClaude/issues/604).
- New data feeds or capabilities for summaries, issue/PR links, named steps or opening a session.
- Write-back to Orca or any operational controls.
- Mouse interaction, animation or blinking.
- Pixel-for-pixel image replication, fabricated data, or reproducing reference controls that violate the standing constraints.

## Components Affected (from `/sc:analyze`)

Static codebase pass followed `/sc:analyze` with no depth flag, scoped to the observer presentation files and `tests/observe/`, with the rendering spec as context. Codegraph MCP lookup tools and Auggie were unavailable; the pass used Glob, Grep and Read after the CLI readiness check. No tests or runtime renders were executed for this draft; the supplied audit remains the runtime evidence.

Codegraph: index_state=fresh, checked_at=2026-11-17T17:51:00Z; degraded: none. Access: cli; analysis lookups used the file-tool fallback.

- `src/superclaude/cli/observe/render.py` — `screen_lines`, `render`, `_panel_lines` and `_desk_lines`: styling, framing, count presentation, responsive composition and render comparisons.
- `src/superclaude/cli/observe/view.py` — display values for questions, counts and Decision Desk evidence; preserve real-data and unknown-scope semantics.
- `src/superclaude/cli/observe/terminal.py` — `make_console`, `resolve_policy`, `color_system`, ASCII handling and width policy.
- `src/superclaude/cli/observe/commands.py` — `LiveScreen` and width-bound one-shot output; verify the actual styled screen path as well as plain output.
- `tests/observe/test_render.py`, `tests/observe/test_terminal.py`, `tests/observe/test_commands.py` — render widths, styling/fallback expectations and command integration.
- `tests/observe/release1_surface.py`, `tests/observe/test_linkoff_screen_reference.py`, `tests/observe/golden_release1_surface.json`, `tests/observe/golden_questions_linkoff.json` — deliberate updates to presentation references.
- `tests/observe/test_export.py`, `tests/observe/test_snapshot_schema.py`, `tests/observe/test_golden_contract.py` and the remaining `tests/observe/` regression suite — protect screen-only question text, data contracts and standing constraints.
- `~/.config/zellij/config.kdl`, `themes/aidev02.kdl`, `layouts/agent.kdl`, `layouts/default.kdl` — the installed Zellij setup the planning phase evaluates (read-only; not part of the repository).
- `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md` — align the phased redesign spec with the current rendering contract and explicitly record intentional layout changes.

## Related Issues/PRs

- Parent: [#409 — TUI Dashboard to Manage Orchestration at Scale](https://github.com/IronbellyOrg/IronClaude/issues/409).
- Separate backlog: [#604 — R4 remote fleet](https://github.com/IronbellyOrg/IronClaude/issues/604).
- Shipped observer work: [#503 — R1](https://github.com/IronbellyOrg/IronClaude/pull/503); [#514](https://github.com/IronbellyOrg/IronClaude/pull/514) and [#577](https://github.com/IronbellyOrg/IronClaude/pull/577) — R2; [#592 — R3 Decision Desk](https://github.com/IronbellyOrg/IronClaude/pull/592); [#598 — question text stays on screen only](https://github.com/IronbellyOrg/IronClaude/pull/598).

<!-- sc:issue:create template=issue-feature-simple -->

## Redesign spec

**Instructions for the agent that claims this issue.** The spec below (sections 1 to 12) is the plan of record. The step-by-step tables (files, golden changes, tests, rubric, gate protocol) are too long for an issue body, so the same spec is also posted as three comments on this issue (`<!-- REDESIGN-SPEC part i/3 -->`) that together are the whole file.

1. Save the whole spec to `.dev/issues/409/visual-parity/REDESIGN-SPEC.md`, unless that file already exists on your branch:

```bash
mkdir -p .dev/issues/409/visual-parity
gh issue view 606 --repo IronbellyOrg/IronClaude --json comments \
  --jq '[.comments[] | select(.body|startswith("<!-- REDESIGN-SPEC part")) | .body | sub("^[^\n]*\n";"")] | join("\n")' \
  > .dev/issues/409/visual-parity/REDESIGN-SPEC.md
sha256sum .dev/issues/409/visual-parity/REDESIGN-SPEC.md   # must equal the sha256 in the comment marker lines
```

2. Run `/sc:workflow @.dev/issues/409/visual-parity/REDESIGN-SPEC.md --depth standard --handoff none`.
3. Read the plan it prints, then run `/sc:implement <the plan path it printed>`. Every phase ends with its render gate; do not start a phase before the previous gate closes.
4. Rebase on `origin/master` before pushing. Open the PR only with `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."` (it targets `IronbellyOrg/IronClaude`).
5. Stop and ask the owner when a gate reaches the 3-iteration cap or two iterations in a row do not improve, or when an owner decision in section 10 is needed and its default does not fit.

Evidence trail (kept on the research branch, not needed to implement): `.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/RESEARCH-REPORT-observer-visual-parity.md`; merged findings: https://github.com/IronbellyOrg/IronClaude/issues/606#issuecomment-6957531081.

Status: ready to claim. Date: 2026-11-18 (owner layout ruling applied). Source of every number and file reference below: the research report `.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/RESEARCH-REPORT-observer-visual-parity.md` (the evidence trail) and the merged review findings `.dev/issues/409/visual-parity/merged/FINDINGS.md` (finding ids M-01 to M-18). Where this spec and the report differ, the report's Section 8 text copied in Part B governs, except that the owner's 2026-11-18 layout ruling (section 10, D-1) overrides the report's earlier two-column questions screen.

Part C (space diet, owner rulings 2026-11-18) sits between the summary and Part B and governs where they differ. Short names used below: `OBS` = `src/superclaude/cli/observe/`; `T` = `tests/observe/`; `VP` = `.dev/issues/409/visual-parity/`; `RR` = `.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md`.

### 1. What to build, in one paragraph

Bring `superclaude observe` to the visual language of the three design mockups (Signal Bridge, Attention Ledger, Decision Desk) at 160, 116 and 80 columns: colour and weight from one named theme, boxed and titled panes, a two-column Decision Desk at 160 and 116 (stacked at 80), a stacked questions screen at every width with a prominent `SEEN IS NOT RESOLVED` count strip and a `RETAIN CONTEXT` pane, plus five plain-text defects of today's layout. Replicate the theme, styling and layout techniques, not the images. Keep the observer read-only, real data only, question text on screen only (never in the record or the JSON snapshot), no blinking, no mouse, no animation.

### 2. Rules that cannot change

- Do not edit `OBS/export.py`. `record_text` and `snapshot_json` stay byte-identical (the records golden added in Phase 2 proves it).
- Question text appears on screen only. Both hash canaries (record and snapshot) must keep passing from Phase 0 onward.
- NO_COLOR output contains zero escape bytes and the same text as the coloured output after SGR removal. ASCII output is pure ASCII with `+ - |` borders and `#` for the block glyph, never a `?` where a border belongs (guard G-1).
- The 16-colour theme must keep eight distinct role colours (guard G-2): Rich's automatic downgrade of the mockup RGB collapses muted, green, red and violet onto index 7, so the 16-colour table uses named ANSI colours.
- Facts the screen does not have are not drawn: no owner, requester, mapped-tree, SIGNALS bars or affected-session list (accepted divergences AD-1 to AD-8, section 6).
- Existing tests that read the source text must keep passing: `QUESTION_GATE_PASSED` and `QUESTION_LINK_PASSED` (commands.py:67, 70), the words `release-gates.md` and `Task 18` in commands.py (`T/test_commands.py:747-772`), no `Console(`, `from_markup`, `sorted(`, `.sort(` or adapter, collector, parse import in `render.py`, and `len(group.renderables) == len(screen_lines(...))` (`T/test_render.py:399`).
- Nothing under `.claude/` is ever staged. `.dev/tasks` is staged. The PR goes to `IronbellyOrg/IronClaude` through `/sc:pr-submit --monitor 3`, never to `SuperClaude-Org`.

### 3. Decisions this spec makes

| Topic | Decision | Why (short) |
|---|---|---|
| Composition | Keep the line-based text model as the source of truth. A `Line` (plain text plus role spans) layer records roles at the builders; `render()` still returns one Rich `Text` per line. Frames and columns are hand-built from `GLYPHS`. No Rich `Panel`, `Table`, `Layout` or `Columns` in `render()`. | Keeps `T/test_render.py:399`, the source guards, the record and the NO_COLOR text untouched; a Rich Panel does not give ASCII borders (`safe_box` has no effect, probed on Rich 15.0.0). |
| Render harness | Offline scripted checks on `console.file.getvalue()` captures, plus a fresh reviewer who scores a fixed rubric against the mockup PNGs. No new dependency. PNG rasterising is a session-only extra through the Playwright MCP browser, proven once in step 0.4. | No PNG tool is installed (no PIL, cairosvg, browsers); `export_text(styles=True)` ignores NO_COLOR and the colour downgrade, so it is never the capture. |
| ANSI colour depth | Decision D2 in two steps. Floor: eight named 16-colour roles (works everywhere). Then detect depth: `NO_COLOR` or `TERM=dumb` gives none; `COLORTERM=truecolor` or `24bit` gives truecolor (the mockup palette exactly); `TERM` ending `256color` gives 256-colour; otherwise 16-colour. One role table per depth in a new `OBS/theme.py`. Default owner choice D-5: all three depths. | Today `make_console` pins `color_system="standard"` (terminal.py:121) and nothing reads COLORTERM or TERM, so a truecolor terminal never sees the mockup palette. |
| Zellij 0.44.2 | Go as an optional layout and manual check only (Option Z2). No-go as a dependency of the observer or of the render gate. | See section 5. |
| Hash fixture | Phase 0 adds a synthetic plan-ask with a 64-hex-character hash and file paths. Owner ruling 2026-11-18: the hash is never shown on screen (Part C, step 2.12); the tests assert it is absent and that both record canaries still pass. | PR #591 consideration 8, superseded by the ruling. |
| Layout (owner ruling 2026-11-18) | The Decision Desk is two columns at 160 and 116 and stacked at 80. The questions screen is stacked at every width. | Evidence: the stacked-vs-two-column comparison comment on issue #606 (rows used: questions 11 stacked vs 17 two-column at 160, 12 vs 17 at 116; desk 23 vs 14 at 160, 23 vs 18 at 116). |

### 4. Findings the work closes

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

### 5. Zellij go or no-go, with evidence

Recommendation: **conditional go, as an optional layout and manual check; no-go as a dependency.**

Evidence:
- The owner confirmed Zellij is installed and working in every workspace. Binary: `/usr/local/bin/zellij`, version 0.44.2, with a shipped config, theme `aidev02` and layouts `agent.kdl` and `default.kdl`.
- The research read the binary's help text and the official documentation only: Zellij sets the `ZELLIJ` environment variable in its panes, supports floating panes and command panes in layouts, and has `zellij action dump-screen` (with an `--ansi` form in current docs). The online docs describe a newer release than 0.44.2 (0.46.0 was announced 2026-11-11), so every flag must be checked with `--help` on 0.44.2 first.
- The observer already adapts to any pane size on each draw, and it is a plain Rich program that runs without Zellij. Zellij only wraps its output, so NO_COLOR and ASCII modes are unaffected.
- Not yet exercised in this research: a live session test of colour pass-through (truecolor and 256), wide-glyph fidelity of the box and block characters inside a Zellij pane, and `dump-screen --ansi` output on 0.44.2.

Conditions that must hold if Zellij is used: the observer works unchanged outside Zellij; read-only; all three widths; NO_COLOR and ASCII unchanged. It may read `ZELLIJ` as a hint, never as a requirement. Action: step 7.4 runs one manual session test and records the result in `VP/zellij-note.md`. It is not a phase gate.

### 6. Accepted divergences (not fix requests)

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

### 7. Phase list

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

### 8. Render gate (the last step of every phase)

Each phase is closed by an automated loop, not by the author's opinion.

1. **Implement** the phase steps; `uv run pytest tests/observe/ -v` is green.
2. **Render** with `uv run python .dev/issues/409/visual-parity/tools/render_compare.py --out <out>/<phase>/iter-<n> --check --heights 44,40,24,12,8`: screens `ledger`, `questions`, `desk`, `desk-planask` at widths 160, 116, 80 (heights 48, 42, 42), in five passes (truecolor, 256, 16-colour, NO_COLOR, ASCII), plus the text-only height matrix. `--check` writes `checks.json` with the script-checked rubric rows. A run without all five passes or without `--check` is not valid.
3. **Rasterise** each truecolor and 16-colour HTML through the Playwright MCP browser to a PNG (route proven in step 0.4). If that fails, the reviewer compares the text and ANSI files with the mockup text and ANSI files and uses the mockup PNG as the visual reference.
4. **Score.** Spawn one fresh reviewer subagent per width, with no resume and no author context. It gets only the rubric file, the reviewer prompt, the mockup PNGs and text for that width, and the rendered PNG, text, ANSI and `checks.json`. It returns `scores.json`: PASS or FAIL plus one evidence line per in-scope row.
5. **Fix and repeat.** Fix every failing High or Medium row, re-render, score again with a new reviewer. At most 3 iterations per phase.
6. **Close or stop.** A phase closes only when every High and Medium row in scope passes in the last iteration; Low rows pass or are logged as deferred. Escalate to the owner and stop (write `VP/scores/<phase>/stop.md` with the failing rows and the iteration scores, do not start the next phase) when a row still fails after iteration 3, or when two consecutive iterations do not improve the number of passing rows.

The fixed rubric (rows RB-01 to RB-23, written once in P0 to `VP/rubric/rubric.md`, never edited between phases) is in Part B, section 8.4.

### 9. Risks

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

### 10. Owner decisions

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

### 11. Definition of done

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

### 12. How the claiming agent starts

1. Save this spec to `.dev/issues/409/visual-parity/REDESIGN-SPEC.md` (the issue explains how to assemble it from the comments when it is not already on your branch).
2. Run `/sc:workflow @.dev/issues/409/visual-parity/REDESIGN-SPEC.md --depth standard --handoff none`.
3. Read the plan it prints. Then run `/sc:implement <the plan path it printed>`. Each phase ends with its render gate (section 8); do not start a phase before the previous gate closes.
4. Before pushing, rebase on `origin/master`. Open the PR only with `/sc:pr-submit --monitor 3 --head <branch> --title "..." --body "..."`.
5. Stop and ask the owner when a gate hits the 3-iteration cap or two non-improving iterations, or when a decision in section 10 is needed and its default does not fit.

