# QA Report — Task File Qualitative Review (operational-correctness lens)

**Topic:** observer-visual-parity tech-research task file
**Date:** 2026-11-18
**Phase:** task-qualitative (lens: operational-correctness)
**Fix cycle:** N/A (fix_authorization: false)

---

## Overall Verdict: FAIL (1 blocking finding, B-1; 13 notes)

Task file reviewed in full: 480 lines, 82 `- [ ]` items, 271,249 bytes (Phases 1-7, Task Log). Drift baseline: BUILD-REQUEST GOAL read verbatim (BUILD-REQUEST.md line 12), so AX-1 is active.

## Items Reviewed

| # | Check | axis | Result | Evidence |
|---|-------|------|--------|----------|
| 1 | Gate/command dry-run | none | PASS | Ran `uv run pytest tests/observe/ -q -p no:cacheprovider`: 766 passed in 26.67s, `git status --short -- src tests uv.lock pyproject.toml` empty afterwards. `zellij --version` = 0.44.2; `zellij setup --help` lists `--check` as "Checks the configuration ... displays currently used directories" (read-only); `zellij action --help` lists dump-screen, dump-layout, new-pane, toggle-floating-panes. Step 7.1 `git -C ... status --short -- src tests` is read-only. No item starts a Zellij session (Step 2.5 forbids it; only `--help`/`--check`/`--version`). |
| 2 | Project convention compliance | none | PASS | Docs-only: every write target is under the task folder (research/, synthesis/, qa/, gaps-and-questions.md, RESEARCH-REPORT-*.md). `uv run` used for every Python call; `render_current.py` and `record_golden*` are explicitly "do NOT run". See N-9 for the `.dev/tasks` staging rule. |
| 3 | Intra-phase execution order simulation | AX-3 | FAIL | Executing Steps 3.3, 5.9, 6.6, 6.7, 6.8 cycle 2: the fix-agent item has no prompt of its own (lines 180, 258, 310, 336, 360 say "same ... prompt as Step 3.2 / 5.8 / 6.5 / ... above"). At that point the executor does not have what it needs in the item. See B-1. All other ordering is sound: gaps-and-questions.md (Step 3.4) is created before Step 4.1/4.2 read it; web files (Phase 4) exist before synth 5.2-5.6 read them; synth files exist before 6.1; report exists before 6.2-6.8. |
| 4 | Function signature verification (adapted: every embedded value vs source) | none | PASS | wc -l matches for render 531, view 1204, terminal 160, sanitize 48, commands 500, export 274, collector 361, questions 142, keys 235. Grep: terminal.py:121 `color_system=None if policy.no_color else "standard"`; render.py:497 `width_class == "full"`; render.py:528 `Text(line, no_wrap=True, overflow="crop")`; commands.py:242 `console.export_text()`; commands.py:257 `class LiveScreen`; commands.py:67/70 gate constants; render.py defs at 62/155/246/304/311/329/359/390/524; terminal.py `clip` at 138 and `GLYPHS` (selected/truncate/hrule) at 30-34. |
| 5 | Module context analysis | none | PASS | `safe_box` is a Rich `Console` kwarg at terminal.py:123, not a function (prompt 2.1 lists it among names to document; agent will find it). `clip` lives in terminal.py, imported by render.py:21. `render_current.py` `emit()` (lines 68-75) uses `screen_lines` then `render` then `console.export_text(styles=True)` on a `record=True` console, matching Step 2.5(e). |
| 6 | Downstream consumer analysis | none | PASS | Synthesis map equals SKILL.md lines 1503-1508 (synth-01 = 1,2; 02 = 3,4; 03 = 5; 04 = 6,7; 05 = 8; 06 = 9,10). Report Structure (SKILL.md 1317-1493) has the same 10 headers the assembler prompt lists. File-name chain checked end to end: Gate 1 `qa-fix-verification-phase3*.md` (3.2) read by 3.4; Gate 2 `...-phase5*.md` (5.8) read by 5.10; Gate 3 `qa-fix-verification*.md` (6.6) read by the 6.6 gate item; Gate 4 `qa-fidelity-*` and Gate 5 `qa-anti-omission-*` consistent between producers and consumers. |
| 7 | Test validity (verification steps substantive) | none | PASS | Verification clauses are checkable: exact section headers, `Status: Complete`, file existence, counts, verdict strings. Weak spot only in Step 7.2 (not measurable), already noted by the B2 report (its N-6). |
| 8 | Coverage of primary use case / acceptance criteria | none | PASS | Q1-Q7 each have a research source (01/02/03/04/05 + web-01/02), a synth home (synth-04 section 7.2 table) and a plan home (synth-05). Gate counts match BUILD-REQUEST lines 32-37: 3 + 3 + 7 + 2 + 2 agents. |
| 9 | Error path coverage | none | PASS | Every item ends with "re-spawn once, then log blocker, mark complete"; every gate has a HALT to status Blocked after cycle 2. |
| 10 | Runtime failure path trace | none | PASS | Entry (BUILD-REQUEST) to exit (Phase 7) traced. Only operational friction found is the task-file size (N-1) and the halt-guard edge case (N-4); neither breaks the data flow. |
| 11 | Completion scope honesty | none | PASS | O-1 and OPEN-1..3 are deliberately left open and routed to Section 9 / 7.3 (Builder Notes line 411); the task completes the investigation, not the decisions. |
| 12 | Ambient dependency completeness | none | PASS | Agent types exist in the runtime list: general-purpose, rf-analyst, rf-qa, rf-qa-qualitative, rf-assembler. All referenced input paths exist (see Self-Audit). Minor: N-2 (heading names), N-10 (agent-file phase labels). |
| 13 | Kwarg/dependent-step sequencing | none | PASS | No step consumes an artifact before its producer; cycle-2 items are conditional on the cycle-2 consolidated file, which the first 3.3/5.9/6.6/6.7/6.8 item always writes (either "not needed" or the list). |
| 14 | Function/path existence claims | none | PASS | Glob/ls confirm: 28 `.py` + 2 goldens in tests/observe (22 `test_*.py`, see N-7), visual-parity `inputs/{mockups,current,tools}`, `merged/FINDINGS.md` (210 lines), `rendering-rules.md` (107 lines, so cited lines up to 93 exist), `pr-591-comment.md` (line 18 is consideration 8), attachments PNGs, `~/.config/zellij/{config.kdl,themes/aidev02.kdl,layouts/agent.kdl,layouts/default.kdl}`, `/usr/local/bin/zellij`. Absent tools (chromium, google-chrome, rsvg-convert, inkscape, convert, freeze, termshot, aha, ansi2html, unzip) match research-notes line 37. |
| 15 | Cross-reference accuracy for templates | none | PASS | Template 02 line 835 says "Partitioning: Only for >10 files (raised from 6)", so the Phase 3/5 "no partitioning" statements are right. SKILL.md lines 399-419 give 3/3/7/2/2 agents at standard. |

## Summary
- Checks passed: 14 / 15
- Checks failed: 1
- Critical issues: 0 (1 IMPORTANT, blocking)
- Issues fixed in-place: 0 (fix_authorization: false)
- Axis lens status: AX-1 active (BUILD-REQUEST GOAL available verbatim); no `drift-axis-inactive`.

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| B-1 | IMPORTANT (blocking) | Task file lines 180 (Step 3.3), 258 (Step 5.9), 310 (Step 6.6), 336 (Step 6.7), 360 (Step 6.8) | The five cycle-2 fix-agent items spawn an `rf-qa` agent with `fix_authorization: true` but carry no prompt. Each says "using the same fix-agent prompt as Step 3.2 / 5.8 / 6.5" or "as in the cycle-1 fix item above" plus a parenthetical paraphrase. The paraphrase drops the role sentence, "Fix only blocking findings; leave minor findings as notes", "create it first with Write containing a header only", the per-fix log-line contents and, for Gates 1 and 2, the targeted-research-agent and Documentation Staleness rules. Line 118 promises every embedded prompt is "complete and must be passed ... verbatim". Cycle 2 is the last cycle before HALT, so a fix agent running on a rebuilt prompt (no log protocol, no self-check) feeds the monotonicity guard an incomplete log. I confirmed the wording at each line by reading them. Independent of, and in agreement with, B-1 of `qa-task-validation-b2-report.md`. | Write the full fix-agent prompt into each of the five items with the cycle-2 consolidated path and cycle-2 log path substituted (AX-3 omission). |

### Notes (non-blocking)

| # | Axis | Where | Observation | Suggested action |
|---|------|-------|-------------|------------------|
| N-1 | AX-3 | Whole file (271,249 bytes = 264.9 KiB) | The file is larger than the Read tool's 256 KB single-read cap. My own full `Read` failed with "File content (264.9KB) exceeds maximum allowed size"; a 24-line range of Phase 3 also exceeded the 25,000-token cap. `/home/coder/.claude/skills/task/SKILL.md` line 91 ("READ: Read the task file from disk. ALWAYS") and line 113 ("You MUST re-read the task file before each action") assume a whole-file read. An executor will have to fall back to `Grep '^- \[ \]'` plus ranged reads. It works, but only if the executor adapts; adding the five full fix prompts for B-1 grows the file further. | Add a short note in "Detailed Task Instructions": locate the next item with `Grep` for `^- \[ \]` (line numbers) and Read by `offset`/`limit`; Step 7.1's "confirm every `- [ ]` is `- [x]`" can be a `Grep` count. |
| N-2 | AX-1 | Lines 124-128 and 80 other references | Items say "log ... in the `### Phase 1 Findings` section" (also Phase 2 to 7 Findings, 80 references by my `grep`). The real headings are `### Phase 1 - Preparation Findings`, `### Phase 2 - Deep Investigation Findings`, ... `### Phase 7 - Presentation and Completion Findings` (lines 428-455). No heading named `### Phase N Findings` exists. Mappable by a reader, but not literal. | Use the real heading names or rename the headings. |
| N-3 | AX-2 | Lines 178, 256, 308, 334, 358 | The "byte-exact" regression halt string uses a comma: `Regression detected on Item X.Y, previously PASS at cycle N, now FAIL. ...`. `~/.claude/skills/task-builder/SKILL.md` lines 1280 and 1295 and `~/.claude/skills/sc-tasklist-protocol/SKILL.md` line 1610 give it with an em-dash (`X.Y — previously`); `~/.claude/agents/rf-task-builder.md` line 419 and `~/.claude/agents/rf-qa.md` line 413 use the comma. Installed docs disagree with each other; the task follows the agent files. Only matters if a consumer string-matches the halt line (`tests/audit/_halt_emitter.py` exists in the repo for the em-dash tasklist form). | Pick one and note which source it follows; low risk for this research task. |
| N-4 | AX-4 | Lines 178, 256, 308, 334, 358 | The monotonicity guard reads "if \|F_2\| >= \|F_1\| HALT". The skill form (`task-builder/SKILL.md` line 1311, `sc-tasklist-protocol` line 1611) is "if \|F_n\| > 0 AND \|F_{n+1}\| >= \|F_n\|". With zero blocking findings at review 1 (no fix agent ran) but a cycle-1 verification FAIL from a fresh reviewer, the task HALTs where the skill would proceed to cycle 2. Also, in that zero-finding case the two cycle-1 verification agents still run (steps say "the agent still runs"), which is wasted work. Safe direction (halts early), so non-blocking. | Add the `> 0` guard, or state the stricter behaviour is intended. |
| N-5 | AX-3 | Step 3.1 qualitative prompt (line 164) | Gate 1 runs before the web files exist. The qualitative agent is asked whether each of Q1 to Q7 has enough raw evidence "that a synthesis agent can answer without re-researching" and to grade "a question that cannot be answered from the files" as blocking. Q4 (Rich detection via COLORTERM/TERM) and parts of Q3 and Q6 depend on Phase 4 web files. The prompt says the web files do not exist yet but never says those question parts are expected to be filled by Phase 4, so a strict reviewer could raise a spurious blocking gap and start a fix cycle that the Phase 4 work would have closed. | Add one sentence: Q-parts that need external sources are graded against what the code and local environment can show, not against web evidence. |
| N-6 | AX-3 | Step 6.2 evidence-quality lens (line 282, item a) | "Every factual claim cites a specific file path and line number." Environment facts (tool absent, Zellij 0.44.2, Rich version, `zellij --help` contents) are proven by commands, not file:line. The reproducibility lens (line 294) accepts "the command that proved them", so the two lenses disagree. Risk is a spurious finding and an avoidable fix cycle. | Let item a accept "command + output" for environment facts. |
| N-7 | AX-1 | Source Areas line 94; Key Objectives context | "28 test modules plus the two goldens". The 28 `.py` files in `tests/observe` are 22 `test_*.py` modules plus `__init__.py`, `conftest.py`, `record_golden.py`, `record_golden_questions.py`, `release1_surface.py`, `spike_child.py`. Step 2.3's own prompt words it correctly ("28 .py files"). | Reword to "28 .py files (22 test modules)". |
| N-8 | AX-2 | Line 118 vs lines 198 and 202 | "passed to the agent verbatim after substituting nothing" conflicts with the `[paste your 5-10 line summary here]` slot in Steps 4.1 and 4.2 (the items do say to substitute it). Same as B2 note N-1. | Say "substituting only the stated slots". |
| N-9 | AX-3 | Phase 7 | Project rule (`~/.claude/CLAUDE.md` core rule 4): `.dev/tasks/` "is always staged (`git add .dev/tasks`) ... never leave it untracked". The task creates about 60 files under its folder and never stages them (git status at session start shows this folder untracked). Staging is not committing, so this is a one-line, reversible final step; but Key Constraints line 103 also says no file outside the task folder is touched, so the executor needs an explicit instruction either way. | Add a non-gating last item `git add .dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800` (no commit), or state that staging is left to the owner. |
| N-10 | AX-1 | Lines 164, 238-242, 278-294, 322-324, 346-348 | Phase labels in the prompts (`research-gate-qualitative`, `synthesis-gate-qualitative`, `source-fidelity`, `report-lens-*`, `anti-omission`; rf-analyst `synthesis-quality-review`) are not phases/types defined in the installed agent files (`rf-qa.md` line 47 lists research-gate, synthesis-gate, report-validation, task-integrity, fix-cycle; `rf-analyst.md` line 40 lists completeness-verification, cross-validation, synthesis-review, gap-analysis, coverage-audit). They come from the SKILL.md prompt templates (lines 864-1207), and each prompt embeds its own checklist and output format, so the agents can follow them. | None required; expect the agents to follow the embedded checklist. |
| N-11 | AX-4 | Step 5.2 (line 216) | The C8 control is worded "must link a remediation need". `tech-research/SKILL.md` line 1380 says an unwired in-scope capability "MUST carry (or link) an MDTM remediation task under `.dev/tasks/to-do/`". Softer in the task. Probably moot here (the gaps are visual-parity gaps, not unwired capabilities). | Use the skill wording. |
| N-12 | AX-3 | Step 5.6 (line 232) vs Steps 4.1/4.2 | synth-06 is told to read "the Gaps and Questions and Stale Documentation Found sections of every file" including web-01 and web-02, but the web prompts produce only "Key External Findings" and "Recommendations from External Research". `gaps-and-questions.md` is built at Step 3.4, before the web files exist, so web-derived gaps (a web claim that contradicts the code) have no path into Section 9 except by the synth agent's judgment. Gate 5 anti-omission would catch a drop. | Tell synth-06 to also read the two closing sections of each web file. |
| N-13 | AX-5 | `.dev/issues/409/visual-parity/inputs/tools/render_questions_screen.py` | A second harness script (CLI width and height arguments, prints `screen_lines` for the questions screen) sits beside `render_current.py` and is not mentioned in the task, Step 2.4/2.5 or research notes. It is relevant to Phase 0 harness options and Q7. Reading `inputs/**` in Step 2.4 will likely surface it. | Name it in Step 2.5(e). |

## Actions Taken
None (fix_authorization: false). The only state changes during this review: the test run used `-p no:cacheprovider` with `PYTHONDONTWRITEBYTECODE=1`; `git status` for src, tests, uv.lock and pyproject.toml was empty afterwards. This report file was written under the task `qa/` folder as instructed.

## Inherited Structural Verdict — Reliance Audit (PR-04, INV-019)
The spawn prompt carried no `## Inherited Structural Verdict` block, so I ran standalone and re-checked structure myself. See Self-Audit.

## Self-Audit

**(a) Reliance list — rf-qa PASS items skipped for structural re-check:**
- None relied on. The sibling reports in `qa/` (`qa-task-validation-b2-report.md`, and the near-empty structure/alignment/sufficiency stubs) were read only after my own pass to avoid duplicate findings. From the B2 report I took nothing as verified; B-1 here is my own reading of lines 180, 258, 310, 336, 360 and happens to agree with its B-1.

**(b) Independent semantic checks (>=1 required, INV-019):**
- Prompt-embedded code anchors are true -- verified by Grep/Read: terminal.py:121, render.py:497 and 528, commands.py:242 and 257, view/render/terminal function and class names, `wc -l` counts for 9 source files.
- Baseline is runnable and green -- ran `uv run pytest tests/observe/ -q -p no:cacheprovider` (766 passed, 26.67s), so the Step 2.3 "run once for a baseline" instruction works and leaves no tracked change.
- Zellij steps are read-only -- ran `zellij --version` (0.44.2), `zellij setup --help` (`--check` only displays config/dirs), `zellij action --help`; no session started.
- Offline-tool premise -- `command -v` for chromium, google-chrome, rsvg-convert, inkscape, convert, freeze, termshot, aha, ansi2html, unzip: all absent, matching research-notes line 37.
- Skill conformance -- compared synthesis mapping, Report Structure, gate counts (SKILL.md 399-419, 1317-1508) and the partition threshold (template 02 line 835) with the task; all agree.
- Gate loop mechanics -- traced all five gates: file names produced = file names consumed, two fix cycles then HALT, regression check before monotonicity; compared the halt strings with four installed documents (N-3) and the `|F_n| > 0` guard with two skill files (N-4).
- Task-file executability -- reproduced the Read-cap failure on the task file (N-1) and quoted `/task` skill lines 91 and 113.
- Anti-orphaning -- Phase 7 order is validate (7.1), present (7.2), summary (7.3), set status Done, then the NON-BLOCKING downstream suggestion last, as required by `task-builder/SKILL.md` rule 15 (line 2363).

**Confidence:** Verified: 15/15 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
**Tool engagement:** Read: ~30 | Grep: ~25 | Glob: 4 | Bash: 7 (counts approximate; every call mapped to a check above)

## Recommendations
1. Before execution, apply B-1: embed the full fix-agent prompt in the five cycle-2 items (lines 180, 258, 310, 336, 360), substituting the cycle-2 consolidated and log paths.
2. In the same edit pass, add the execution note from N-1 (the file is over the Read cap) and fix the heading references (N-2); these are cheap and reduce executor friction.
3. Optional, in priority order: N-5 and N-6 (they can cause spurious gate failures), N-9 (staging rule), N-4, N-3, then N-7 to N-13.
4. After the fix, a re-review needs only to confirm the five items carry a full prompt (cycle 1 of 2 allowed).

## QA Complete

VERDICT: FAIL


