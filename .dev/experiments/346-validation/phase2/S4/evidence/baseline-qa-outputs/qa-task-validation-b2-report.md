# QA Report - Task Integrity (Lens b2-self-containment)

**Topic:** BMAD first-use directory creation (TASK-RESEARCH-bmad-first-use-20261107-075901)
**Date:** 2026-11-07
**Phase:** task-integrity
**Fix cycle:** N/A (fix_authorization: false; task file not edited)
**Task file:** /home/coder/workspaces/worktrees/Coder/bmad-ponytail-global/.dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/TASK-RESEARCH-bmad-first-use-20261107-075901.md

---

## Method log (appended incrementally)

- Task file is 324KB (over the 256KB single-Read limit); read in full in line ranges (lines 1-591), plus Grep counts.
- Cross-read: BUILD-REQUEST.md, research/research-notes.md, SKILL.md prompt templates (lines 630-1240), Template 02 section B (lines 146-226).
- Pointers in the items were spot-checked against disk (Glob/Grep/Read/wc): Dockerfile.coder:133-144, test-57 lines 448-452, startup.sh:673-679, README.md:241 and 308, test hit counts (startup-boot 35, test-46 38, test-19 5), line counts (1863/1132/3061/1953/1262/610), BMAD package files, superclaude files, OD-1 / memlog / SPEC lines. All checked pointers are accurate.
- Item inventory: 89 checklist items (`- [ ]`), 44 embedded agent prompts (`BEGIN AGENT PROMPT`), 15 further agent-spawning items that embed NO prompt (see Issue 1). No nested or malformed checkboxes (Grep for indented, `* [ ]` and `- []` forms: 0).

---

## Items Reviewed (lens checklist)

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Every item has all B2 components (context, action, output, verification, completion gate) | FAIL (minor) | 81 of 89 items carry the "cannot be marked as done" gate sentence; the 8 that do not are lines 176, 180, 476, 480, 484, 488, 492, 496 (Phase 1 and Phase 7). Items 176, 488, 492, 496 also lack a failure-log clause or an "ensuring" clause. Issue 6. |
| 2 | No item relies on context from a prior item without restating it | FAIL | 15 items defer to "the full agent prompt embedded in Step X above" (Issue 1); 7 lens items rely on N defined in a paragraph outside any item (Issue 2); item 5.2 says "names as in Step 5.1" (Issue 9). |
| 3 | Agent-spawning items embed full prompts | FAIL | 44 of 59 agent-spawning items embed a full prompt. The 15 cycle-2 items (lines 250, 254, 258, 340, 344, 348, 401, 403, 405, 429, 431, 433, 457, 459, 461) do not. Nested spawn in 3.5 (line 230) has no embedded prompt (Issue 3). |
| 4 | File paths are specific | PASS with note | All cited repo, BMAD and superclaude paths exist (Glob). Output paths are specific per item. Note: 34 of 44 prompts give only relative paths (Issue 8). |
| 5 | Verification criteria measurable | PASS with note | Counts, Status lines, section names, BLOCKING_COUNT arithmetic, git status, spot-check minimums (2.4, 2.5, 3.1) are measurable. Several items rely on "no claim is fabricated" with no sample size (Issue 10). |
| 6 | No batch items; each agent/file has its own item | PASS | 5 research, 2 web, 4 synth, 3+3+3 gate-1/2 agents, 7 lens, 2 fidelity, 2 anti-omission each have their own item. Multiple items share one "Step" heading in 6.2-6.7b, which makes positional references ("next item", "previous item") necessary (see Issue 1). |
| 7 | No items based on CODE-CONTRADICTED / UNVERIFIED findings | PASS | The task contains no research results yet. The four known UNVERIFIED items are research targets, not premises. Line pointers inside prompts were verified true (see method log). `global_target_dir` Grep over the package excluding `*.yaml` returns no match, consistent with the research notes. |
| 8 | No Ponytail research items | PASS | Case-sensitive "Ponytail" appears only at line 130 (no-work statement) and line 579 (builder note). Every other case-insensitive hit is the worktree directory name `bmad-ponytail-global`. |
| 9 | Incremental File Writing Protocol in every agent prompt | PASS | All 44 embedded prompts carry it (Grep of `Incremental File Writing` hits every prompt line 189-205, 214-238, 275-279, 288-312, 320-328, 361-383, 389-395, 413-423, 441-451). |
| 10 | ADVERSARIAL STANCE in every QA/analyst review prompt | PASS with note | Present in 3.1-3.3, 3.6, 3.7, 5.5-5.7, 5.10, 5.11, 6.2-6.4 lens prompts, 6.6 verifications, 6.7 fidelity, 6.7b anti-omission. Absent from the five fix-agent prompts (rf-qa, fix_authorization true; lines 230, 320, 389, 419, 447). Issue 7. |
| 11 | Documentation Staleness Protocol in every research prompt | PASS with note | Present in 5 of 5 codebase research prompts (lines 189-205). Absent from web-01/web-02 (lines 275, 279); the SKILL.md Web template also omits it. Issue 7. |

---

## Issues Found

| # | Severity | Location (task file line) | Issue | Required Fix |
|---|----------|---------------------------|-------|-------------|
| 1 | IMPORTANT | 250, 254, 258 (Steps 3.10-3.12); 340, 344, 348 (5.14-5.16); 401, 403, 405 (6.6 cycle 2); 429, 431, 433 (6.7 cycle 2); 457, 459, 461 (6.7b cycle 2) | 15 agent-spawning items contain no prompt. Each says "using EXACTLY the full agent prompt embedded in Step 3.5 / 3.6 / 3.7 / 5.9 / 5.10 / 5.11 above (or 'the cycle-1 ... item above'), changing only ..." This is the "see above" pattern that B2 and the lens forbid. It also contradicts the task's own rule at line 165 ("Every item below is a self-contained prompt: do not rely on anything read in an earlier item") and Template 02 B1 (batches lose earlier context at session rollover). Builder note 3 (line 581) knowingly justifies it ("the executor re-reads this file on every loop"), which does not satisfy B2. In 6.6, 6.7 and 6.7b several items share one Step heading, so the pointers are positional ("the cycle-1 rf-qa verification item of this Step 6.6 above", "the previous item"), which is ambiguous when 8-14 items sit under one heading. | Paste the complete prompt, with the cycle-2 substitutions already applied and the "LAST fix cycle" sentence included, into each of the 15 items (about 15 x 3-5 KB). Give every item in Steps 6.5-6.7b its own step label (for example 6.6a-6.6h) and delete the relative "next/previous item" pointers. Remove or correct builder note 3. |
| 2 | IMPORTANT | 365 (paragraph under Step 6.2) used by 367, 369, 371, 375, 377, 379, 383 | Every Gate 3 lens prompt says "Assume this document has at least N errors", but N is defined and the formula given only in the unnumbered paragraph at line 365, outside any checklist item. Items 6.3 (375-379) and 6.4 (383) sit under different step headings and never restate it. Template 02 B5 forbids separate reminder blocks between items, and the lens agent receives an undefined N. | In each of the 7 items, add the sentence: "Compute N first: Grep pattern `^` with output_mode `count` on `.dev/tasks/to-do/TASK-RESEARCH-bmad-first-use-20261107-075901/RESEARCH-REPORT-bmad-first-use.md`, then N = the larger of 5 and the line count divided by 100 rounded up; write that number in place of N in the prompt below." Delete line 365 or keep it as informational. |
| 3 | IMPORTANT | 230 (Step 3.5), inherited by 250 | The fix-agent prompt tells the agent to "spawn one targeted `rf-task-researcher` subagent per gap (give it the full Incremental File Writing Protocol and Documentation Staleness Protocol and this same scope guard)". The prompt contains neither a research-agent prompt nor the Staleness Protocol text (the agent's own prompt only has the Incremental protocol, and the scope guard). The nested agent prompt is therefore improvised from a reference, the only agent-spawning instruction in the task with no embedded prompt body. | Embed in 3.5 the full Codebase Research Agent prompt skeleton (Incremental protocol, Research Protocol, Documentation Staleness Protocol, output format, scope guard) with placeholders for gap, target file and addendum heading, or remove the spawn permission and require gaps to be marked UNVERIFIED instead. |
| 4 | IMPORTANT (outside the B2 lens; reported because it breaks a project rule) | 480 (Step 7.2) vs 484, 488, 492 | Step 7.2 stages `.dev/tasks` and says staging is the rule, but Step 7.3 afterwards creates `reviews/user-summary.md` (new untracked file), and 7.4 and 7.5 edit the task file. After 7.5 the tree has an untracked file and unstaged modifications under `.dev/tasks/`, which CLAUDE.md (project and global) says must never happen ("never leave it untracked"). | Move the staging item to after Step 7.5 (before the non-blocking 7.6), or add a second `git add .dev/tasks` plus the same `status --porcelain` check at that point. |
| 5 | MINOR | 185, 210, 271, 284, 357, 411, 439, 472 (phase intro paragraphs) | Executable rules live only in non-item paragraphs: "Phase 4 starts only after Step 3.13 recorded GATE1_FINAL: PASS" (271), "Phase 6 only after GATE2_FINAL: PASS" (357), Gate 4 after GATE3_FINAL (411), Gate 5 after GATE4_FINAL (439), parallel-spawn rules, "5.4 only after 5.3". Items 4.1, 4.2, 5.1, 6.1 and the first item of 6.7 and 6.7b do not restate their start condition. Mitigated: each Gate-final item says STOP on FAIL, so later items are not reached. | Add a one-clause start check to the first item of each phase (read the previous GATEn_FINAL line; if it is not PASS, stop). |
| 6 | MINOR | 176, 180, 476, 480, 484, 488, 492, 496 | These 8 items omit the B2 sentence "This item cannot be marked as done until the actions are completed in their entirety exactly as described" (they end with "Once done, mark this item as complete"). Items 176, 488, 492 and 496 also have no failure-log clause; 176 and 492 have no "ensuring" verification clause; 488 ends "Once the summary is complete" instead of the standard sentence. | Append the standard gate sentence to all 8; add a failure-log clause to 176, 488, 492; add one-line "ensuring" checks to 176 and 492 (for example "ensuring frontmatter status reads exactly 🟠 Doing"). |
| 7 | MINOR | 230, 320, 389, 419, 447 (fix agents); 275, 279 (web agents) | The five fix-agent prompts are rf-qa agents and carry no ADVERSARIAL STANCE although they "re-verify the claim" before editing. The two web research prompts carry no Documentation Staleness Protocol (consistent with the SKILL.md Web template, but the lens asks that research prompts carry it). | Add one adversarial sentence to the fix prompts ("assume the finding may be wrong or incomplete; re-read the source before editing"). For the web prompts add a short staleness clause: every doc-sourced claim about Claude Code or BMAD behaviour is tagged official / unofficial and checked against the dates of the page. |
| 8 | MINOR | 34 of 44 embedded prompts (lines 214-238, 275-279, 288-328, 361, 367-369, 375, 379, 389-395, 419-423, 441-451) | Output and input paths in these prompts are relative (`.dev/tasks/to-do/...`); only 10 prompts (189-205, 371, 377, 383, 413, 415) spell out the absolute worktree root. The relative-path anchor lives only in line 167. The Write and Edit tools take absolute paths, and the prompts themselves say "absolute paths". Works today because spawned agents start in the worktree, but it is not self-contained. | Prefix each prompt with "Worktree root: /home/coder/workspaces/worktrees/Coder/bmad-ponytail-global; all relative paths below are relative to it; pass absolute paths to Read, Write and Edit." |
| 9 | MINOR | 292 (Step 5.2), 300 (Step 5.4) | 5.2 says research files "(names as in Step 5.1)" (a pointer to another item). 5.4 reads synth-01 and synth-02 "if they exist", although 5.1 and 5.2 are spawned in the same message as 5.3 and 5.4 is only ordered after 5.3; a still-running 5.1 or 5.2 makes the clause skip silently, which defeats the stated aim of using the same gap wording as Section 4. | Write the seven research file globs out in 5.2. In 5.4 require that 5.1, 5.2 and 5.3 have all returned and delete "if they exist". |
| 10 | MINOR | Steps 2.1-2.3 (189-197), 4.1-4.2 (275, 279), 5.1-5.4 (288-300) | Verification clauses end with unmeasurable phrases ("no claim is fabricated", "traces to a research file", "ensuring the report was produced by the agent and not by you"), with no sample size. Steps 2.4 and 2.5 do set measurable minimums ("spot-check at least five rows with Grep"). | Add a minimum spot-check count (for example "re-open at least 5 cited file:line references with Read and confirm the cited line says what the file claims") to 2.1-2.3, 4.1-4.2, 5.1-5.4. |
| 11 | MINOR | 189, 193, 197, 201, 205, 296 | Candidate options A-F are re-described differently per prompt: Option B is "under ~/.claude/skills" (2.1, 2.3), "written from image-baked content" (2.2, 5.3) or "written by the bmad slug's install.sh" (2.4, research-notes line 82); Option C adds "or a new wrapper command" only in 2.2 and 5.3. Agents can therefore research different variants and the Section 6 comparison would not line up. | Use one canonical sentence per option (copy research-notes lines 79-86) in all seven prompts that list them. |
| 12 | MINOR | 189 (Step 2.1), 161 (Open Questions item 3) | Step 2.1 authorises a `bmad install` run in `/tmp` scratch directories while BUILD-REQUEST's binding scope guard says "read and research only". The decision is left to the orchestrator in a non-item section ("strike that clause if ..."); an executor cannot resolve it from the item. | The orchestrator should decide before execution and either keep or delete the "OBSERVED RUN" clause; record the decision in the Task Log. |
| 13 | MINOR (note) | frontmatter lines 1-62 | The rf-qa task-integrity checklist item 1 asks for `created`, `template`, `tracks`; Template 02 itself defines `created_date` and has no `template` or `tracks` key (Grep of the template), and this file follows the template. The checklist and the template disagree; the task file is not at fault. | None for the task file; fix the QA checklist or the template. |

---

## What passed (so the next cycle does not re-check it)

- Granularity: one item per research agent (5), web topic (2), synthesis file (4), gate agent and fix/verify step; no "spawn all five" batch item.
- Every one of the 44 embedded prompts carries the Incremental File Writing Protocol, the BINDING SCOPE GUARD and a "final message under 1500 characters" clause; all 5 codebase research prompts carry the Documentation Staleness Protocol with the three tags; 27 review/analyst/verification prompts carry ADVERSARIAL STANCE.
- The embedded QA, analyst, lens, fidelity and anti-omission prompts match the SKILL.md templates (checklists, severity grading, verdict wording, output formats); the N formula matches SKILL.md line 1057 (document_lines / 100, minimum 5).
- Ponytail: no research item, no agent, no evidence row. Only the two no-work statements at lines 130 and 579.
- Item shape: all 89 items are single-paragraph `- [ ]` lines; no nested boxes; each phase header count is not claimed, so there is nothing to miscount.
- The input slices of the two anti-omission agents together cover all 5 codebase files, both web files, all 4 synth files and the gaps log; the two fidelity agents cover files 01-05.

## Summary

- Checks passed: 8 of 11 (checks 4, 5, 6, 7, 8, 9, 10, 11; checks 4, 5, 10, 11 carry notes). Checks failed: 3 (checks 1, 2, 3).
- Issues: 13 total. CRITICAL: 0. IMPORTANT: 4 (Issues 1, 2, 3, 4). MINOR: 9 (Issues 5-13).
- Blocking: Issues 1, 2, 3 (B2 self-containment, the lens target) and Issue 4 (project staging rule). Issues 5-13 are notes.
- Issues fixed in place: 0 (fix_authorization: false; the task file was not edited).

## Confidence (computed)

- Verified: 11/11 checks (7 lens checks + 4 extra checks) | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- Tool engagement: Read: 18 | Grep: 34 | Glob: 5 | Bash: 1 (one read-only `wc -l` over the cited files). Tool calls (57) exceed checklist items (11).
- Limit of this review: the task file has no executed output yet, so "does the embedded prompt actually produce the file" cannot be tested; only the text of the items was verified. The accuracy of the research conclusions (for example `global_target_dir` has no reader) is for the research gates, not this lens; one Grep over the package outside `*.yaml` found none, which agrees with the research notes.
- Housekeeping note: one Bash call used `cd <worktree> && wc -l ...` against the project's "do not cd" rule; it was read-only and the shell does not persist.

## Recommendations

1. Rewrite the 15 reference items (Issue 1) with full embedded prompts and unique step labels, and drop builder note 3.
2. Embed the N computation in the 7 lens items (Issue 2) and the gap-researcher prompt in Step 3.5 (Issue 3).
3. Move the `.dev/tasks` staging to after Step 7.5 (Issue 4).
4. Apply the nine MINOR fixes in the same edit pass (Issues 5-13), then re-run this lens for fix cycle 1.

VERDICT: FAIL

## QA Complete
