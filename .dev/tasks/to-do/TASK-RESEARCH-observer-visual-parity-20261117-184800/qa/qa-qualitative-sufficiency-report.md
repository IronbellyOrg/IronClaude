# QA Report — task-qualitative (lens: qa-gate-sufficiency)

**Topic:** observer-visual-parity tech-research task file
**Date:** 2026-11-18
**Phase:** task-qualitative
**Fix cycle:** N/A (first review)
**fix_authorization:** false

**Lens:** qa-gate-sufficiency (BUILD-REQUEST QA_INTENSITY: standard; full-intensity floors not applied)
**Task file reviewed:** /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/TASK-RESEARCH-observer-visual-parity-20261117-184800.md (475 lines, 82 `- [ ]` items)
**BUILD_REQUEST.GOAL baseline:** captured (BUILD-REQUEST.md line 12), so the AX-1 drift axis is active.

---

## Overall Verdict: FAIL

3 blocking findings (all IMPORTANT), 5 notes. Gate counts, lens split, serialization and the 2-cycle cap are correct. The failures are in what the gates are allowed to see (Gate 4 source set), one byte-exact wire string, and batch items that breach the BUILD-REQUEST granularity rule.

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Agent counts match BUILD-REQUEST per gate | none | PASS | Counted `- [ ] Spawn` gate items: Gate 1 = 3 (L160, L162, L164: rf-analyst, rf-qa, rf-qa-qualitative); Gate 2 = 3 (L238, L240, L242); Gate 3 = 7 (L278, L280, L282 rf-qa; L286, L288, L290 rf-qa-qualitative; L294 domain lens finding-reproducibility); Gate 4 = 2 (L322, L324 rf-qa); Gate 5 = 2 (L346, L348 rf-analyst). Matches BUILD-REQUEST L32-37 and SKILL.md L399-419. |
| 2 | Each gate agent is its own `- [ ]` item (BUILD-REQUEST L54-55 "Do NOT create batch items") | AX-3 | FAIL | Gate agents are individual items. The conditional cycle-2 verification pairs for Gate 4 (L338) and Gate 5 (L362) each spawn TWO agents (rf-qa and rf-qa-qualitative) inside ONE checkbox with one shared prompt. Gates 1, 2, 3 split the same pair into separate items (L182/L184, L260/L262, L312/L314). See B-3. |
| 3 | Lens-specific embedded prompts | none | PASS | Each of the 7 Gate 3 prompts names its own lens, checklist a-d and output file (L278-L294). Gate 1/2 prompts carry distinct lens checklists (8-item completeness, 10-item evidence, depth questions; accuracy, 12-item structure, coherence). Fidelity agents split by code area (L322, L324); anti-omission agents split by file halves (L346, L348). QA phase labels match SKILL.md L864-1211. |
| 4 | Fix agent is single and serialized, gate agents report-only | none | PASS | `fix_authorization: true` appears exactly 10 times (L170, 180, 248, 258, 300, 310, 328, 336, 352, 360) = 5 gates x 2 cycles, each "ONE Agent subagent" `rf-qa`, each after a consolidation item. Every gate/verification prompt states fix authorization false. |
| 5 | Verification round exists per fix cycle | none | PASS | Gate 1 L172/L174; Gate 2 L250/L252; Gate 3 L304/L306; Gate 4 L330/L332; Gate 5 L354/L356; cycle-2 equivalents present. Verification is unconditional (runs even when the fix log says "no fix agent needed"). |
| 6 | Monotonicity and regression guards encoded in the exact order, with byte-exact wire strings (task-builder SKILL.md L1290-1315, API-004) | AX-2 | FAIL | Guards present at L178, L256, L308, L334, L358 in the right order (regression, then monotonicity, then cycle-2 fix). But the regression string is written `Regression detected on Item X.Y, previously PASS at cycle N, now FAIL. ...` and called "byte-exact". SKILL.md L1295 pins `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. ...` (em dash). See B-1. Monotonicity string `[HALT-MONOTONICITY] |F|=<n>` is exact. |
| 7 | 2-cycle cap and HALT-and-escalate encoded per gate | none | PASS | Gate decision items L188, L266, L316, L340, L364 read the last-run verification pair, HALT with status "Blocked" plus blocker_reason if blocking findings remain after cycle 2, and name the phase not to execute (Phase 4, 6, Step 6.7, Step 6.8, Phase 7). |
| 8 | Fidelity gate agents read source files AND the full report, and the source set is sufficient | AX-3 | FAIL | Both prompts say "Read your assigned source files first, then read the FULL report" (L322, L324). But the static source lists omit files the report must describe (mockup .ansi/.txt/.png, test_linkoff_screen_reference.py, release1_surface.py, record_golden*.py, parse.py, adapter.py), while L320 claims "the whole source set is covered". See B-2. |
| 9 | Anti-omission: exhaustive, by meaning not ID | none | PASS | L344 and both prompts (L346, L348): "ENUMERATE every distinct finding... do not sample", "do NOT use ID or reference citation as your coverage test", "when in doubt FLAG". Output table with OMITTED / COVERED-BY-DEDUP, severity, enumeration counts. |
| 10 | Every omission recovered or justified, never dropped | none | PASS | Consolidation L350 requires a Disposition RECOVER or JUSTIFY column with a defensible-by-meaning justification; fix agent L352 must end every row as recovered or justified and log each; verification L354/L356 re-checks recovery and honesty of dedups. |
| 11 | Report has all 10 sections, assembled by a single rf-assembler | none | PASS | Assembly prompt L272 lists the 10 sections in order; synthesis mapping L212-L232 (S1-2, S3-4, S5, S6-7, S8, S9-10) matches SKILL.md L1508; template-conformance lens L278 checks all 10 plus order and TOC. |
| 12 | Research and synthesis artifacts preserved | none | PASS | No item deletes, moves or overwrites research/ or synthesis/ files; fix agents are told "do not modify research or synthesis files"; Step 7.1 (L372) globs all 15 named deliverables plus qa/ reports and runs `git status --short -- src tests`. |
| 13 | Gate 3 domain lens is the single standard-intensity lens | none | PASS | finding-reproducibility only (L294), type rf-qa-qualitative, as in SKILL.md L409. |
| 14 | A failed gate blocks the next phase | none | PASS | See check 7. Gate 1 -> Phase 4, Gate 2 -> Phase 6, Gate 3 -> Step 6.7, Gate 4 -> Step 6.8, Gate 5 -> Phase 7. |

## Summary
- Checks passed: 11 / 14
- Checks failed: 3
- Critical issues: 0
- Blocking (IMPORTANT) issues: 3
- Issues fixed in-place: 0 (fix_authorization false)

## Issues Found

| # | Severity | Blocking | Location | Issue | Required Fix |
|---|----------|----------|----------|-------|-------------|
| B-1 | IMPORTANT | yes | Task file L178, L256, L308, L334, L358 (regression halt string, 5 gates) | Each halt guard says to emit the "byte-exact message" `Regression detected on Item X.Y, previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.`. The wire string pinned by API-004 at `/home/coder/.claude/skills/task-builder/SKILL.md` L1280 and L1295 is `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check.` (em dash after X.Y, not a comma). The task file silently changed the ABI string while calling it byte-exact. Any fixture that asserts the full string fails; the prefix grep at SKILL.md L1317 would still match, so the practical risk is low but the claim is false. | Replace `X.Y, previously` with `X.Y — previously` in the five guard items, or drop the words "byte-exact" and record the deliberate deviation in the Task Log. |
| B-2 | IMPORTANT | yes | Task file L320, L322, L324 (Gate 4 source partition); also L162 (Gate 1 spot-read scope) | The Gate 4 source lists are hard-coded, not "from research file paths" as SKILL.md L558 requires, and L320 asserts "the whole source set is covered". Not assigned to either fidelity agent: (a) the mockup sources `/home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/issues/409/visual-parity/inputs/mockups/{160,116,80}/*.ansi, *.txt, *.png` (verified present with `ls`), the attachments PNGs and `inputs/current/`; (b) `tests/observe/test_linkoff_screen_reference.py` (75 lines), `tests/observe/release1_surface.py` (62), `record_golden.py`, `record_golden_questions.py`, all named in research-notes.md L29 as core to Q2; (c) `parse.py` (835) and `adapter.py` (512), listed in the task's own Source Areas (L93). Section 3 (Target State), the colour roles and the pane geometry of the report come from the mockups, and the Gate 1 evidence-quality prompt (L162) only spot-reads `src/.../observe/` and `tests/observe/`. No gate in the plan checks mockup-derived claims against the mockup files, and those claims drive Q1, Q4 and the render rubric. | Add the mockup `.ansi` and `.txt` files (and `inputs/current/` renders) to fidelity agent 2, and the three test helpers to agent 1 (or add the clause "plus every other file path cited in research files 01 to 05"). Extend L162 spot-read scope to `.dev/issues/409/visual-parity/inputs/` and the Zellij paths. Correct the L320 coverage sentence. |
| B-3 | IMPORTANT | yes | Task file L338 and L362 (Gate 4 and Gate 5 cycle-2 verification) | Each of the two items spawns two agents (rf-qa and rf-qa-qualitative) under one checkbox with one shared prompt and a parenthetical lens split. BUILD-REQUEST L54-55 forbids batch items and requires an individual item for every validation step. Gates 1, 2 and 3 split the same pair into separate items (L182/L184, L260/L262, L312/L314), and cycle 1 of Gates 4 and 5 does too (L330/L332, L354/L356), so this is an inconsistency inside the file. A half-finished item cannot be resumed or marked per agent. | Split L338 into two items (rf-qa to `qa-fidelity-verification-1-cycle2.md`, rf-qa-qualitative to `qa-fidelity-verification-2-cycle2.md`) and L362 likewise, each with its own lens-specific embedded prompt and its own "not needed" branch. |

## Notes (minor, no fix cycle, not rechecked)

| # | Location | Note |
|---|----------|------|
| N-1 | L170, L180, L248, L258, L300, L310, L328, L336, L352, L360 | The fix-agent quoted prompts never say "Fix authorization: true" inside the quoted text; the flag is only in the instruction before the quote. Gate agents carry "Fix authorization: false" inside their prompts, so the convention is inconsistent. An executor that forwards only the quoted text hands rf-qa no write authorization and the fix cycle does nothing. Embed the line in each fix prompt. |
| N-2 | L178 (and the four copies) | The regression guard needs the set of items that PASSED at the first review, but no item records that set; the consolidated file lists failures only. The executor must re-derive it from the first-review reports. Add a "PASS set" line to the consolidated file template. |
| N-3 | L192-L202, L238 | web-01 and web-02 get no pre-synthesis gate (Gate 1 reads files 01 to 05 only, L156). This matches SKILL.md L476-493, and Gate 2 reads all seven research files, so it is a documented design choice, not a defect. |
| N-4 | L346, L348 | The anti-omission inputs are research and synthesis files only. Findings M-01 to M-18, G, AD, OPEN and O-1 are enumerated through research/04 alone, never from FINDINGS.md directly. Acceptable per SKILL.md L565, but a drop inside research/04 itself would not be caught. |
| N-5 | L124-L128, many "log the blocker in the ### Phase N Findings section" references | Headings are `### Phase 2 - Deep Investigation Findings` etc. (L438-L455); the references use a shorter name. Cosmetic. |

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)

No `## Inherited Structural Verdict` section was in the spawn prompt (only the BUILD-REQUEST and a rf-qa structural pass ran earlier, per the sibling reports in qa/), so this review ran standalone and relied on no inherited PASS items.

## Self-Audit

**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- None. No inherited verdict table was supplied; I did not read the sibling reports `qa-task-validation-structure-report.md`, `qa-task-validation-b2-report.md`, `qa-task-research-alignment-report.md` or `qa-qualitative-operational-report.md`, so nothing here rests on them.

**(b) Independent semantic checks (>=1 required, INV-019):**
- Gate agent counts per gate - verified by Grep of `- [ ] ` (82 items) and Read of L154-L364; counted 3/3/7/2/2 and compared with BUILD-REQUEST L32-37 and SKILL.md L399-419.
- Regression wire string - verified by Grep for `HALT-MONOTONICITY|Regression detected on Item` in `/home/coder/.claude/skills`, then Read of task-builder SKILL.md L1268-1319; found the em dash vs comma difference (B-1).
- Fidelity source coverage - verified by Bash existence and line-count loop over every assigned path (all exist; agent 1 about 5,250 lines, agent 2 about 5,540 lines), `ls` of `tests/observe/` and `inputs/mockups/`, and Grep of research-notes.md L16-L32; found the unassigned mockup, test-helper and parser files (B-2).
- Single fix agent - verified by Grep for `fix_authorization: true` (10 hits = 5 gates x 2 cycles).
- Batch items - verified by reading L338 and L362 against L182-L184 and L260-L262 (B-3).
- Report sections - verified by Grep of "Report sections to produce" (L212-L232) against SKILL.md L1508.

**Confidence:** Verified: 14/14 checklist items with tool evidence | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (verdict FAIL on findings, not on missing verification)
**Tool engagement:** Read: 15 | Grep: 10 | Glob: 0 | Bash: 2 (read-only existence/line-count and `ls`)
**Web research:** none performed; Tavily not needed (all claims are local-file claims).

## Recommendations
- Fix B-1, B-2 and B-3 (all are small edits to existing items), then re-review; only blocking findings are rechecked.
- Optionally apply N-1 and N-2 in the same pass; they cost one line each.

## QA Complete

VERDICT: FAIL
