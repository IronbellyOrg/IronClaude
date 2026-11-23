# QA Report - Task Integrity (Lens: phase-structure)

**Topic:** observer visual parity tech-research task file
**Date:** 2026-11-18
**Phase:** task-integrity (lens: phase-structure)
**Fix cycle:** N/A (fix_authorization: false)

**Task file:** /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/TASK-RESEARCH-observer-visual-parity-20261117-184800.md (475 lines, 271 KB, read in full in ranged reads)
**Template:** /home/coder/.claude/templates/workflow/02_mdtm_template_complex_task.md (frontmatter lines 1-61 and Part 2 lines 1160-1520 read)
**Live TB-Add catalogue:** read from /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.claude/agents/rf-qa.md lines 337-377. It holds TB-Add-1, 3, 4, 5, 6, 7 and 8 (definition items 21-27), the same set as my brief. No extra items.

## Overall Verdict: FAIL (1 blocking finding, 12 notes)

## Structure Map (verified)

| Phase | Lines | Items | Purpose | Header claim | Match |
|---|---|---|---|---|---|
| 1 Preparation | 120-128 | 2 | status, folder check | none | n/a |
| 2 Deep Investigation | 130-152 | 5 | 5 parallel codebase agents | "five items" | yes |
| 3 Gate 1 | 154-190 | 13 | 3 gate agents, fix cycle 1, cycle 2 (conditional), verdict, gaps log | "3 agents" | yes |
| 4 Web Research | 192-202 | 2 | 2 parallel web agents | "two items" | yes |
| 5 Synthesis + Gate 2 | 204-266 | 18 | 6 synth, 3 gate agents, fix, verify, cycle 2, verdict | "six", "3 agents" | yes |
| 6 Assembly + Gates 3, 4, 5 | 268-364 | 37 | 1 assembler, 7 lens, 10 Gate-4 items, 10 Gate-5 items | "7", "2", "2" | yes |
| 7 Present and Complete | 366-384 | 5 | verify, present, summary, Done, non-blocking suggestion | none | n/a |
| Total | | 82 | | | `grep -c '^- \[ \]'` = 82, and 82 lines also match the well-formed pattern, so there are no malformed or nested checkboxes |

All 82 items end with "Once done, mark this item as complete." (82/82). 81/82 carry blocker or re-spawn fallback text. The one without it is the intentionally NON-BLOCKING item at line 384.

## Issues Found

### B-1 (Blocking) Step 5.6 (synth-06) is told to filter by the implementation plan, which it is forbidden to read

- Location: line 232 (Step 5.6 prompt) against line 206 (Phase 5 preamble) and the Step 5.5 / 5.6 ordering.
- Evidence: the Phase 5 preamble (line 206) says the six synthesis agents "read only research files and the gaps log (never each other's output)". The Step 5.6 prompt gives synth-06 only the gaps log and the "Gaps and Questions" / "Stale Documentation Found" sections of the research files. The same prompt also says Section 9 must include "every unresolved gap that is not closed by an implementation step; do not include questions answered elsewhere in the plan". The "plan" is synth-05 (Step 5.5), and the "implementation step" filter needs it. The agent cannot do this. It will either include every gap or guess.
- Consequence: Section 9 will predictably restate questions that Section 8 answers. That trips Gate 2 check 7 at line 240 ("Open Questions in Section 9 aren't answered elsewhere") and the crossref-chain and internal-consistency lenses at lines 278 and 290. This spends fix cycles against the 2-cycle cap on a defect the task file built in. Checklist items 11 and 15 (item-level data flow) apply.
- Required fix, either: (a) make Step 5.6 sequential after Step 5.5 and add `synthesis/synth-05-implementation-plan.md` (and `synth-02`/`synth-04`) to its read list, updating the Phase 5 preamble, or (b) delete the "not closed by an implementation step / answered elsewhere in the plan" clause from the Step 5.6 prompt and leave reconciliation to Gate 2.

### Carried from another lens (not counted again here)

Five cycle-2 fix-agent items (lines 180, 258, 310, 336, 360) still say "using the same fix-agent prompt as Step X.Y" instead of embedding the prompt. This is blocking finding B-1 in /home/coder/workspaces/worktrees/IronClaude/issue-409-mvp/.dev/tasks/to-do/TASK-RESEARCH-observer-visual-parity-20261117-184800/qa/qa-task-validation-b2-report.md. I re-read all five lines in the task file just now and each still has that wording, so the finding is open. It also bears on checklist item 5.

### Notes (minor, do not fail the gate)

| # | Location | Note | Suggested fix |
|---|---|---|---|
| N-1 | Frontmatter, lines 1-49 | Definition item 1 lists `created`, `template` and `tracks` as required. The file has none of them; it uses `created_date`. I checked the source of truth: Template 02 frontmatter (template lines 1-61) has none of the three either, and the file matches the template field for field except `reflect_pre`, `reflect_post` and `reflect_post_mode`. The omitted reflect fields agree with the stated intent that the POST gate is absent. I read this as a stale checklist rather than a task-file defect. | Reconcile the rf-qa item 1 field list with Template 02, or add the three fields if you want a strict reading. |
| N-2 | Execution Context, lines 83-114 | TB-Add-7. The block has `### Source Areas`, not a `**Source areas:**` line, so the literal trigger is the degraded form (`tb-add-7-degraded-tolerated`). I cross-checked anyway: all 7 source areas reappear in item bodies (observe package: 2.1/2.2; tests/observe: 2.3; spec folder, visual-parity, attachments: 2.4; zellij config: 2.5; pyproject.toml and Makefile: 2.5). No `path.py:NN` citation in the block (`grep -nE '\.py:[0-9]+'` on lines 83-114 returned nothing). The optional consumer spot check `grep -cE "src/|/.*:[0-9]+"` returns 1, from the directory entry `.../src/superclaude/cli/observe/` at line 93. That is a directory path, which is what Source Areas is meant to hold. | None. Treat the spot-check hit as a false positive. |
| N-3 | Lines 272 and 278 | TB-Add-1. A Grep for `TBD`, `TODO`, `FIXME` hits 3 times: line 272 (`TODO`, `TBD`, in the assembler's "search for placeholders" rule) and line 278 (`TODO markers`, in the template-conformance lens prompt). These are search targets quoted for agents, not placeholder content. Every item has context, action, output, verification and a completion clause, so none is title-only. | Reword to "placeholder markers listed in the Content rules" if you want a clean mechanical scan. |
| N-4 | Whole file | TB-Add-6. No item uses a `Verify:` prefix (0 matches) and there is no Acceptance Criteria list. Verification is phrased as "verify that ..." / "ensuring ..." / "Confirm ...". That is the B2 single-paragraph pattern of Template 02, so the form is uniform within each item class (spawn items: "and verify that its output file ... exists"; read items: "ensuring ..."). The literal `Verify:` rule does not map onto this format. | None, or clarify TB-Add-6 for B2 paragraph items. |
| N-5 | Items 2.3 (line 144), 2.5 (152), 3.1 (160-164), 6.3 domain-accuracy (288), 6.7 (322, 324) | TB-Add-8. These items reference code surfaces (test files, `render_current.py emit()`, `render.py`/`terminal.py`/`commands.py`, the `observe/` folders) with no `file:line` and no `<!-- evidence-absence: ... -->` comment. There are zero `evidence-absence` comments in the file. Items 2.1 and 2.2 do carry approximate lines, and I verified them against code: header gate `render.py:497`, `render` 524, `make_console` `color_system` `terminal.py:121`, `export_text` `commands.py:242`, `LiveScreen` 257. These are investigation or review items whose line evidence is produced by the agent. This is a citation-format matter, so it is minor, but a mechanical TB-Add-8 run would flag them. | Add one evidence-absence HTML comment to each (for example "line evidence is produced by the agent"). |
| N-6 | Source Areas, line 94 | Prose count. "28 test modules plus the two goldens" is wrong. `tests/observe/` holds 28 `.py` files but only 22 `test_*.py` modules; the other 6 are `__init__.py`, `conftest.py`, `record_golden.py`, `record_golden_questions.py`, `release1_surface.py` and `spike_child.py`. The Step 2.3 prompt at line 144 says "28 .py files", which is correct. | Change line 94 to "28 .py files (22 test modules)". |
| N-7 | Gate verdict items at lines 188, 266, 316, 340, 364 | Each says the gate passes when "the last-run verification pair reports zero blocking findings". When cycle 1 passes, the cycle-2 files exist but are "not needed" stubs with no PASS or FAIL. "Last-run" is then ambiguous: the executor should read the cycle-1 pair. | Add "a 'not needed' stub is not a verification report; skip it". |
| N-8 | Gate 4, lines 322-324 | Coverage. The fidelity source sets cover code, tests, FINDINGS.md, rendering-rules.md, `render_current.py`, Zellij files, pyproject and Makefile. They leave out the mockup `.txt`/`.ansi`/`.png` files, `inputs/current/`, the three PNG attachments, and `test_linkoff_screen_reference.py`, `release1_surface.py`, `record_golden*.py`. Research file 04 (Q4 colour roles, pane geometry) and 03 depend on them. Template PG.6 also has a third `cross-source-contradictions` agent; this file has none and does not mention dropping it (the Task Log only records the 3-4 agent rule deviation). Gate 3 also has no completeness lens (the template has one), though Gate 5 covers the same ground. | Add the mockup and golden-helper files to the Gate 4 partitions, and log the dropped agent under Deviation 1. |
| N-9 | Lines 198, 202, 232 against 190 | Web research findings have no route into Open Questions. The gaps log (line 190) is built at the end of Phase 3, before the web files exist. The Step 5.6 prompt tells synth-06 to read the "Gaps and Questions and Stale Documentation Found sections of every file" including web-01 and web-02. The web prompts (4.1, 4.2) define only "Key External Findings" and "Recommendations from External Research" as closing sections, so those sections will not exist. Web discrepancies reach the report only through synth-03's supports/extends/contradicts marks and the Gate 5 enumeration. | Add a "Gaps and Questions" closing section to the web prompts, or fold the web files into the gaps log after Phase 4. |
| N-10 | Step 1.2 (line 128) | The check requires a `reviews/` folder. It exists on disk (verified with `ls`), but nothing writes to it; all gate reports go to `qa/`. Harmless orphan. | Drop `reviews/` from Step 1.2, or leave it. |
| N-11 | Lines 111, 178 and others | Status string "⚪ Blocked" matches Template 02's body (template lines 1232, 467) but not the options comment at template line 6, which lists "🔴 Blocked". This is a template-internal inconsistency. | None for this file. |
| N-12 | Lines 98, 152 | Source Areas says the Zellij binary is "read-only; CLI help only". The Step 2.5 prompt also runs `zellij setup --check` (diagnostic, not help). I did not run it, so any side effects are unverified. | Align the wording, or drop `setup --check`. |

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| L1 | Frontmatter complete and well-formed | PASS (N-1) | Lines 1-49 parse as YAML with a closing `---` at line 49; id, title, status, type, created_date, updated_date and task_type are non-empty. Matches Template 02 lines 1-61 except the reflect keys. `created`, `template`, `tracks` are absent from the file and from the template. |
| L2 | Mandatory template sections present | PASS | Task Overview (53), Key Objectives (59), Prerequisites & Dependencies (68), Execution Context (83), Detailed Task Instructions (116), Task Log / Notes (386). Template's Post-Completion Actions is replaced by Phase 7 (preface line 368 explains why). Handoff File Convention is replaced by a Key Constraints bullet (line 104). Both are recorded and consistent with BUILD-REQUEST line 58. |
| L3 | Phase dependencies logical | PASS at phase level | 1 to 2 to 3 (Gate 1) to 4 to 5 (Gate 2) to 6 to 7. Each gate has a HALT clause that blocks the next phase (lines 188, 266, 316, 340, 364). |
| L4 | Research, synthesis, assembly, QA ordering | PASS | Research (2, 4), gate on 01-05 (3), synthesis (5), gate (5.7-5.10), assembly (6.1), Gates 3, 4, 5 (6.2-6.8), present (7). |
| L5 | Task-completion items in final phase | PASS | 7.1 Glob and `git status` check, 7.3 Task Summary and status Done. Every output (research, gaps log, synth, report, qa) is consumed downstream or verified in 7.1. Only `reviews/` is orphaned (N-10). |
| L6 | Task Log at bottom | PASS | Line 386 onward: Task Summary, Builder Notes, Execution Log, per-phase findings, Phase Gate Findings, Follow-Up Items, Deviations from Process. |
| L7 | Item count reasonable | PASS | 82 items. 18 of them are conditional "not needed or run" cycle-2 items, which is the cost of the max-2-cycle design at 5 gates. |
| L8 | Open questions and gaps documented | PASS (N-9) | O-1 and OPEN-1 to OPEN-3 are in Builder Notes (line 411) and routed to Sections 7.3 and 9 (lines 190, 224, 232). Gaps log is built at Step 3.4. |
| L9 | M3, M4 gates and Step 6.7b anti-omission | PASS (N-8) | M3: aggregate, lens spawn, consolidate, single fix agent, 2-agent verify, cycle 2 (Gate 3 has 3 rf-qa + 4 rf-qa-qualitative = 7). M4: 2 fidelity agents, consolidate, fix, verify, cycle 2. Anti-omission is Step 6.8 (line 342), labelled "this is Step 6.7b of the tech-research skill", with enumeration by meaning, 2 rf-analyst agents, RECOVER or JUSTIFY disposition, and agent inputs split so all 7 research files, the gaps log and 6 synth files are covered. |
| L10 | TB-Add-1 placeholder scan | PASS (N-3) | Grep hits at 272 and 278 are quoted search terms, not placeholders. No title-only items (82/82 have the completion clause). |
| L11 | TB-Add-3 blocked items cite Open Question index | PASS (inactive) | The task has no Open Questions section and no item is blocked on a question. |
| L12 | TB-Add-4 dependencies form a DAG | PASS | I traced the file-name chains: 3.4 (gaps log) to 4.1/4.2 to 5.x to 6.1 to 6.2-6.4 to 6.5 to 6.6 to 6.7 to 6.8. All output and verification file names agree between producer and consumer for Gates 1-5 (for example `qa-fix-verification-phase3.md`, `...-phase3-cycle2.md`, `qa-fix-log-cycle2.md`, `qa-fidelity-verification-1-cycle2.md`). No back edges. |
| L13 | TB-Add-5 granularity | PASS | Each item produces one deliverable or spawns one agent. Conditional IF/ELSE items are the L-pattern. Oversize is inherent to embedded prompts (see closing note). |
| L14 | TB-Add-6 consistent Verify format | PASS (N-4) | No `Verify:` prefix anywhere; the B2 phrasing is consistent within each item class. |
| L15 | TB-Add-7 source areas reappear, no file:line in block | PASS (N-2) | 7 of 7 source areas reappear in items; no `.py:NN` in block. |
| L16 | TB-Add-8 per-item evidence binding | PASS with notes (N-5) | 2.1 and 2.2 cite lines and I confirmed them in code. Other code-surface items have neither lines nor an evidence-absence comment. |
| D2 | Checklist format `- [ ]` | PASS | 82 lines match `^- \[ \]`; the broader pattern for `- []`, `* [ ]` and indented boxes also returns 82, so none malformed. |
| D4 | No nested checkboxes | PASS | Same count equality; no indented checkbox. |
| D5 | Agent prompts embedded | FAIL | Five cycle-2 fix items say "same prompt as Step X.Y" (carried from the b2 report, B-1 there). All other spawn items embed the full prompt. |
| D6 | Parallel spawning indicated | PASS | Lines 132, 156, 194, 206, 236, 276, 292, 320, 344 (and the cycle-2 verification pair at 338 and 362). |
| D7, D18 | Phase structure and header counts | PASS | Counts above match every header claim. |
| D8 | Output paths specified | PASS | Every spawn item names its absolute output path. |
| D9 | No standalone context items | PASS | The Phase 3, 5 and 6 "Read ..." items each end in a created file or a gate decision. |
| D11, D15 | Item-level data flow within a phase | FAIL | B-1 (Step 5.6 against Step 5.5). The other Phase 5 and 6 items are in correct order. |
| D12 | Duplicate operations | PASS | The repeated gate pattern is per-gate with different files; no identical command repeated. |
| D13 | Verification durability | PASS (N/A) | Documentation-only; BUILD-REQUEST line 44 says TESTING_REQUIREMENTS N/A. |
| D14 | Completion honesty | PASS | No task-level Open Questions section. Owner decisions are report content, and 7.2 presents them to the user. Done is gated by Gates 1-5 PASS. |
| D16 | Execution-order simulation | PASS (N/A) | No kwarg or signature items. |
| D17 | Function, class, file existence | PASS | Verified in code: `screen_lines` render.py:390, `render` 524, `_columns` 155, `_header_lines` 246, `_help_lines` 304, `_question_line` 311, `_desk_lines` 329, `_panel_lines` 359, `build_view` view.py:894, `resolve_policy` terminal.py:73, `make_console` 110, `ascii_safe` 133, `clip` 138, `GLYPHS` 30 (keys selected, truncate, hrule), `TerminalPolicy` 38, `LiveScreen` commands.py:257, `QUESTION_GATE_PASSED` 67, `QUESTION_LINK_PASSED` 70, `DESK_*` and `QUESTIONS_LINK_KEYS_LINE` in view.py:83-94. `safe_box` is a Console kwarg at terminal.py:123, not a function. Line counts match `wc -l` for all 9 files (531, 1204, 160, 48, 500, 274, 361, 142, 235). All other cited files, the zellij files and `/usr/local/bin/zellij` exist. |
| D19 | Prose count accuracy | FAIL (minor) | N-6 (22 test modules, not 28). The other counts (5 agents, 2 web, 6 synth, 7/2/2 gate agents, 7 phases) are correct. |
| D20 | Template references | PASS | Rule IDs F2a, I16, I17, I19, I22 exist in Template 02 Part 1. The file has no `§N` references. |

## Summary

- Checks passed: 33 of 36 rows (D5, D11/D15 and D19 failed)
- Blocking issues: 1 new (B-1) plus 1 carried (b2 report B-1); notes: 12
- Issues fixed in place: 0 (fix_authorization false)
- D19 is graded minor (a count in prose), so it does not fail the gate.

## Recommendations

1. Fix B-1 before execution. The simplest edit is to delete the "not closed by an implementation step / answered elsewhere in the plan" clause from Step 5.6 and let Gate 2 reconcile Section 9 against Section 8.
2. Fix the b2 report's B-1 (embed the five cycle-2 fix prompts).
3. Optional: N-5 (evidence-absence comments), N-8 (Gate 4 source set and the dropped cross-source agent) and N-9 (web gaps routing) are the ones most likely to affect report quality.

## Confidence

Verified: 36/36 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0% (every row was checked with a tool call; the FAIL verdict comes from findings, not from gaps in checking).
Tool engagement: Read: 22 | Grep: 17 | Glob: 4 | Bash: 5 (all read-only). No web research was needed, so no Tavily calls.
Limits: I did not run `zellij setup --check` or any other tool from the task prompts (N-12). I did not review the content of the embedded prompts for domain accuracy, only their structure, ordering and dependencies.

Also noted and accepted: the items are very long single lines (some about 7 KB, because the full agent prompt is embedded as checklist item 5 requires), which conflicts with the "about 15 lines per item" test of item 10. The one-agent, one-output scope of each item is atomic, so I did not flag it separately.

VERDICT: FAIL

