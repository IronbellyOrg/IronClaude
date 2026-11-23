# QA Report - Synthesis Qualitative Review (coherence lens)

**Topic:** Observer visual-parity investigation (issue #606)
**Date:** 2026-11-17
**Phase:** synthesis-gate-qualitative (coherence lens)
**Fix cycle:** N/A
**Status:** Complete (verdict FAIL; 3 blocking, 10 minor)

---

Scope: six files under `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/synthesis/` (synth-01 to synth-06), read in full. Fix authorization: false; no synthesis or research file was modified. Spot checks against code and tests are cited per question.

## Q-A. Do findings build from current state to gaps to options to recommendation to plan?

Result: PASS with one structural break (see Q-G, finding B-1).
- synth-01 (state) to synth-02 (target and gaps) to synth-03 (external) to synth-04 (options, recommendation) to synth-05 (plan) to synth-06 (open questions): each section reuses the previous one's facts (160-cell table, 16-colour collapse, `export_text(styles=True)` hazard). Geometry agrees: 1+114+2+42+1=160 in synth-05 8.3, synth-01 2.4 and synth-02 3.3.
- The break: the phase breakdown is stated three different ways (synth-02 3.8, synth-04 7.1 and 7.2, synth-05 section 8). See B-1.

## Q-B. Are conclusions proportionate to the evidence?

Result: mostly yes; two over-claims.
- Strong claims have probes behind them: `safe_box` does not ASCII-ize a Panel, `export_text(styles=True)` ignores NO_COLOR, silent bottom crop under `Screen`, 16-colour collapse of muted/green/red/violet to index 7. Weak items are tagged [UNVERIFIED] (Zellij runtime, PNG route, flags column fit, `+1` terms) and the plan routes around them (step 0.4 fallback, step 6.1 measure-first).
- Verified: `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/terminal.py:121` is `color_system=None if policy.no_color else "standard"`; `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/test_terminal.py:105-116` pins `width`, `safe_box` and no-ESC only, so the plan claim that step 1.1 leaves that test passing is correct.
- Over-claim 1 (minor M-2): synth-05 P1 and 8.10 say "Closes M-09" and RB-10 requires state words "coloured by the D-7 table". `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/bmad/spec-orca-observer/rendering-rules.md:93` says there is no verified mapping from `workerState`/`outcome` to "settled", and synth-05 8.8 itself tags the mapping [UNVERIFIED]. With an empty or tiny `STATE_ROLE` table the gate row passes vacuously while the finding stays open.
- Over-claim 2 (minor M-6): the same fact carries different tags across files. synth-03 5.1.3 and 5.2.6 mark the `safe_box` probe and the 16-colour mapping "[UNVERIFIED in this synthesis]", while synth-01 2.1, synth-02 3.2 and synth-04 6.0 mark them [CODE-VERIFIED] (probe in research 01 and 04). Cause: synth-03's input list excluded 01 and 04. A reader of the assembled report sees both.

## Q-C. Are contradictions between research files resolved or surfaced?

Result: PASS. synth-01 2.6, synth-02 4.3a, synth-03 5.3 and 5.6, synth-04 6.0 and synth-05 8.6 each list the same set (16-colour collapse, styled export route, 157 vs 160 slack, 153 vs 160 ledger, four width classes, `safe_box`, Zellij go vs no-go, gate-test line ranges) and name the stronger evidence. The resolutions agree across files. Residual cosmetic drift: source-guard line range is cited as 396-403 (synth-01 2.3), 396-404 (synth-02 SC-17) and 400-404 (synth-05); minor, no decision depends on it (part of M-6).

## Q-D. Are the three composition options genuinely distinct?

Result: partly (minor M-1).
- B (Rich renderables) is genuinely distinct from A and C.
- A (hand-built lines plus a string-recovery styling pass) and C (hand-built lines plus roles recorded at build time) share the same frame helper, the same `zip_longest` columns, the same height accounting and the same test impact. synth-04 6.1 comparison table shows identical cells for A and C in 7 of 9 rows; only role assignment and risk text differ. The recommendation (C over A) rests entirely on that one axis, which is a valid axis, but the report presents "three options" when the real choice is two families plus one implementation detail. Also the option taxonomy changes between sections: synth-02 4.1b lists five composition options, synth-04 lists three, synth-01 cites seven from research 01.

## Q-E. Does the recommendation follow from the comparison table?

Result: PASS for Q1 (C), Q3 (H3), Q6 (Z2). Minor drift for Q4.
- Q1: C keeps `test_render.py:399` and the source guard, and avoids regex role recovery; table supports it.
- Q3: H3 is the only offline, dependency-free option that checks bytes; table supports it. The plan then adds an in-session PNG step (G3, Playwright MCP) as part of every gate; synth-04 7.2 says image-to-image is "not part of the gate". Fallback in G3 makes this consistent enough (note only).
- Q4 (minor M-8): synth-04 7.1 recommends D2 "in two steps" (named 16-colour roles first, then COLORTERM/TERM detection); synth-05 P1 step 1.1 to 1.2 delivers detection and all three tables in one phase, and synth-04 7.1 step 3 describes P1 as "theme table ... roles on the per-line Text" with no detection.
- Q6 (minor M-3): the headline answer is worded "Conditional go" (synth-04 7.2), "No-go as a render-harness dependency or observer dependency" (synth-05 8.1), "no-go ... optional presentation environment" (synth-01 2.5, synth-06 row 16). The substance agrees (never a dependency; optional manual check) but the plan has no Z2 layout deliverable at all, only a P7 manual note, so "conditional go as an optional layout" is not planned.

## Q-F. Does the phased plan leave the suite green at each phase, end each phase with a render gate, and respect the standing constraints?

Result: FAIL (blocking B-2); constraints respected.
- Constraints: read-only (no collector or write path added), real data only (AD-1 to AD-4 guarded by the P4 and P6 "no invented content" checks), question text screen-only (hash canaries in P0, `count_figure` source scan in P4.1), NO_COLOR (`color_system=None` kept, RB-06), ASCII (glyph pairs in step 3.1, RB-07), widths 160/116/80 (RB-08, 8.3). No blink or mouse (RB-08, pty test 1.6g). PASS.
- Render gate: every phase from P1 to P7 ends with the G1 to G6 protocol (P7.3 final matrix). P0 uses the baseline run instead (stated, minor M-9: P0 produces no gate verdict, only a baseline).
- BLOCKING B-2 (suite not green after P2 as written). Evidence:
  - `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/release1_surface.py:30-38,60` builds `printed_{width}` by printing `render(view, policy)` through `make_console` with `resolve_policy({}, ...)`.
  - After P1 step 1.1 an empty env resolves to `"standard"`, so `surface()["printed_*"]` contains SGR bytes. P1 step 1.6(c) therefore compares `strip_sgr(current[...])` against the unchanged plain golden. Consistent so far.
  - P2 step 2.7 (and 6.6) regenerates `golden_release1_surface.json` with `json.dumps(surface(), ...)` from the current tree. That writes the SGR-bearing `printed_*` strings into the golden. T47 as rewritten in 1.6(c) then compares stripped current output with an SGR-bearing golden and fails.
  - No step changes `surface()` to strip SGR, or T47 to strip both sides after regeneration. The plan's rollback and "byte-identical" claims for later phases rest on a state that does not exist.
  - Fix direction (not applied): decide once whether `printed_*` in the golden is raw or SGR-stripped, make `surface()` and T47 agree, and state it in 1.6(c) and 2.7. synth-04 7.1 step 3 says "regenerate the 15 `printed_*` values (or relax)"; synth-05 picked "relax" in P1 and "regenerate raw" in P2.
- Verified non-issues: no test in `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/test_render.py` compares `lines[0]` to `header1` outside the too-small diagnostic (lines 224, 241, 557), so the P2 badge does not break a header-equality test. `test_glyph_table_maps_to_ascii` (test_terminal.py:97-102) accepts new `GLYPHS` with ASCII forms.
- Minor M-10: P5 evidence pane at 116 has inner width 62, so a 64-character `resource.worktreeId` is hard-split (step 5.5 pins it). Acceptable, but synth-01 2.3 and synth-04 Q7 present the hash as whole at all widths; that holds only for the question pane.

## Q-G. Are the answers to Q1 to Q7 consistent with the plan and with each other?

Result: FAIL (blocking B-1 and B-3).
- Colour depth vs harness vs styled-capture gate: consistent. Q4 (depth by COLORTERM/TERM, named 16-colour roles), Q5 (`console.file.getvalue()`, piped `--once --width` stays plain per D-4) and Q3 (harness captures `getvalue()` through `make_console`, passes truecolor/16/NO_COLOR/ASCII) agree, and the pty test covers the live path. Only the two-step vs one-phase wording differs (M-8).
- BLOCKING B-1 (Q2 answer contradicts the plan). Three phase schemes appear:
  - synth-02 3.8: P0 tests; P1 style; P2 text; P3 width-gated 160 layout; P4 boxed panes; P5 optional Rich renderables.
  - synth-04 7.1 sequence and 7.2 Q2 answer: P3 two-column layouts (160 then 116) before P4 boxed panes and count tile; P4 touches "both goldens".
  - synth-05 section 8 (stated as "Decided", seven phases): P3 single-column frames first, P4 two-column questions and tile, P5 desk, P6 ledger, P7 spec and PR; golden changes land in P2 (both), P3 and P4 (link-off), P6 (release-1).
  The order of frames and columns is reversed between 7.1 and 8, 7.1 splits 160 and 116 into two phases while P4 does both together, and the golden-impact answer to Q2 does not match the plan. The report's own Q2 answer and its plan cannot both be followed. Fix direction: make 7.1 and 7.2 Q2 point to the section 8 phases (or drop the phase list from 7.1), and align 3.8.
- BLOCKING B-3 (Q7 answer contradicts the plan). synth-04 7.2 Q7 recommends "wrap, never cut, the hash"; synth-05 8.2 D-6 default is "Show in full when it fits; no cut hash". But synth-05 8.1 Q7 keeps "the 4-line desk cap still ends with `...`" and step 0.6 adds a test "pinning today's `...` cut (rule D-6)" for a hash that trails a long path and file list; step 5.4 notes the cap is reached sooner at 160 because the question pane inner width is 72. `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/src/superclaude/cli/observe/view.py:99` sets `DESK_TEXT_LINES = 4`. A hash that falls past line 4 is cut, so "never cut" is not delivered by any step and the pinned test asserts the opposite. Fix direction: either state that the default accepts a cut hash when the ask exceeds four lines (and take it to the owner as D-6), or add a step that exempts a hash token from the cap.
- Q1 vs plan: consistent (line model, `Line` plus spans, one `Text` per line, hand-built frames from `GLYPHS`; `safe_box` not relied on). Minor: synth-04 says P1 starts with line-level roles and grows to segments; synth-05 step 1.4 builds segments in P1.
- Q5 vs Q4 vs Q3 closure of Q-7 (minor M-7): synth-04 7.2 says the PNG-dependency decision is "closed here as 'no' for the gate"; synth-06 row 15 and synth-04 7.3 keep it as owner decision Q-7. Plan adds no dependency, so behaviour is safe, but the status wording differs.

## Q-H. Are O-1 and OPEN-1 to OPEN-3 honestly left open?

Result: PASS with one minor gap (M-4).
- O-1 is listed as open in synth-01 1.3, synth-02 4.1c, synth-04 7.3, synth-05 D-1 and synth-06 row 1. The plan assumes "yes" only as a stated default with the effect if "no" (P4 and P5 skipped, P3 stays) and P4 and P5 list D-1 as a dependency. Not silently decided.
- OPEN-1 and OPEN-3 are carried as "Medium (gated)", with RB-15 and RB-16 labelled "gating until ruled" and D-3 stating the effect of a Low ruling.
- Minor M-4: OPEN-2 is two questions (severity and whether RETAIN CONTEXT is built; synth-06 row 3, synth-02 4.1c). D-3 covers severity only. P4 step 4.4 builds the pane unconditionally, and 8.2 does not say what happens to P4, RB-17 and M-14 if the owner decides not to build it.
- Minor M-5: severity labels differ by section for the C8 defects. synth-02 4.1a rates M-08, M-10 and M-11 Critical; synth-05 8.10 and the rubric rate them Medium ("Severity per FINDINGS"). The header of 8.10 says which scale it uses, and the gate treats High and Medium alike, so no decision changes.

## Issues Found

| # | Severity | Blocking | Location | Issue | Required Fix |
|---|----------|----------|----------|-------|--------------|
| B-1 | IMPORTANT | yes | synth-02 3.8; synth-04 7.1 sequence and 7.2 Q2; synth-05 section 8 | Three different phase schemes; Q2 answer (P3 columns before P4 boxes, golden impact per phase) contradicts the "Decided" seven-phase plan | Make 7.1 and 7.2 Q2 refer to the section 8 phases; align 3.8 |
| B-2 | IMPORTANT | yes | synth-05 steps 1.6(c), 2.7, 3.9, 6.6; `tests/observe/release1_surface.py:30-38,60` | Regenerating the release-1 golden from the styled tree writes SGR into `printed_*`; T47 as rewritten in 1.6(c) strips only the current side, so it fails after P2 | Decide raw vs SGR-stripped `printed_*`, make `surface()` and T47 agree, state it in 1.6(c) and 2.7 |
| B-3 | IMPORTANT | yes | synth-04 7.2 Q7; synth-05 8.1 Q7, D-6, step 0.6, step 5.4; `view.py:99` | "Never cut the hash" and D-6 "no cut hash" vs the retained 4-line cap and a P0 test that pins the `...` cut | Either accept and state a cut hash as the default (owner D-6) or add a cap exemption step |
| M-1 | MINOR | no | synth-04 6.1 | Options A and C differ only in role assignment | Say so, or add a genuinely different third option |
| M-2 | MINOR | no | synth-05 P1, 8.10, RB-10; RR line 93 | "Closes M-09" and RB-10 can pass vacuously when `STATE_ROLE` is empty | Reword to "closes for values with a stated meaning" |
| M-3 | MINOR | no | synth-04 7.2 Q6 vs synth-05 8.1 | "Conditional go" vs "No-go"; no layout deliverable planned | Use one wording |
| M-4 | MINOR | no | synth-05 8.2 D-3, step 4.4 | OPEN-2 build-or-not has no "if otherwise" effect | Add the effect row |
| M-5 | MINOR | no | synth-02 4.1a vs synth-05 8.10 | M-08/M-10/M-11 Critical vs Medium | Add a scale note in 8.10 |
| M-6 | MINOR | no | synth-03 5.1.3, 5.2.6 vs synth-01/02/04; test line ranges | Same fact tagged [UNVERIFIED] and [CODE-VERIFIED]; cite ranges drift | Align tags and ranges at assembly |
| M-7 | MINOR | no | synth-04 7.2 Q3 vs synth-06 row 15 | Q-7 "closed as no" vs open | Say "recommended no, owner open" |
| M-8 | MINOR | no | synth-04 7.1 D2 "two steps" vs synth-05 P1 | Depth detection delivered in one phase | State the plan's choice in 7.1 |
| M-9 | MINOR | no | synth-05 P0 | No gate verdict for P0, baseline only | Note in the phase list |
| M-10 | MINOR | no | synth-05 step 5.5; synth-01 2.3 | Hash whole only in the question pane; split in the 116 evidence pane | State the scope of the claim |

## Summary
- Checks passed: 5 / 8 (Q-A to Q-H; Q-F and Q-G failed, Q-D partly)
- Checks failed: 2 (Q-F, Q-G)
- Blocking findings: 3 (B-1, B-2, B-3)
- Minor findings: 10 (M-1 to M-10)
- Critical issues: 0
- Issues fixed in-place: 0 (fix_authorization false)

## Self-Audit

**(a) Reliance list:** no Inherited Structural Verdict was supplied; standalone behaviour. Nothing relied on.

**(b) Independent semantic checks:**
- Source-guard and header-equality risk of the P2 badge: Grep of `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/tests/observe/test_render.py` for `header1|lines[0]` found no header-equality test (lines 224, 241, 557 are diagnostics).
- `test_terminal.py:105-116` read in full: it does not pin `color_system`, so step 1.1 is safe.
- `release1_surface.py:20-62` read in full: confirmed `printed_*` is produced by the styled console, which grounds B-2.
- `view.py:99` (`DESK_TEXT_LINES = 4`) and `rendering-rules.md:93` (no verified settled mapping) checked by Grep for B-3 and M-2.
- Factual claims independently verified against code: 6. Files read: 6 synthesis files (synth-05 in two pages), 2 code/test files. Not independently re-probed (relied on research files): Rich probes, Zellij help text, mockup geometry. Research files themselves were not re-read, so claims about their content are checked only for internal consistency across the synthesis files.
- No web research performed; no Tavily or fallback call made.

**Confidence:** Verified: 8/8 lens questions | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (lens questions answered with cited evidence; individual research-file facts not re-probed)
**Tool engagement:** Read: 11 | Grep: 6 | Glob: 1 | Bash: 0

## Recommendations
- Fix B-1, B-2, B-3 in the synthesis files, then re-review (fix cycle 1 of at most 2). Minor findings are notes and are not rechecked.

## Overall Verdict: FAIL

**Status:** Complete
**QA Complete**

