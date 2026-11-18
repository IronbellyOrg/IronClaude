# QA Report - Task Integrity (lens: phase-structure)

**Topic:** Review Panel run 2 research task file
**Date:** 2026-11-14
**Phase:** task-integrity
**Fix cycle:** N/A (fix_authorization: false)
**Task file:** /home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/tasks/to-do/TASK-RESEARCH-review-panel-run2-20261114-075454/TASK-RESEARCH-review-panel-run2-20261114-075454.md

**Lens:** phase-structure. **fix_authorization:** false (task file not modified).
**Scope read:** all 717 lines of the task file. Long single-paragraph items were read in full for Phase 1, the cycle-control logic of Phase 3, items 5.37-5.50, 6.01-6.02, 6.29-6.70, Phase 7 and Post-Completion; the repeated Phase 2/3/5/6 lens prompts were read at head and tail and compared programmatically. Also read: template 02 (frontmatter, Part 1 rules I6, I16, I17, I19, Part 2 skeleton) and BUILD-REQUEST.md gate requirements.

## Overall Verdict: FAIL (4 blocking IMPORTANT issues, 0 CRITICAL; 6 MINOR notes)

## Structural facts established (tool-verified)
| Fact | Evidence |
|---|---|
| Frontmatter parses (yq) and its top-level key set is IDENTICAL to template 02 (template 02 has `created_date` and no `created`/`template`/`tracks` keys); id/title/status/type/created_date/task_type non-empty; id equals the folder name | `yq -o=json` on lines 2-61; `diff` of key sets |
| 186 items, all `- [ ]`, none nested or indented. Per phase: P1 3, P2 24, P3 27, P4 4, P5 50, P6 70, P7 3 plus Post-Completion 5 | awk count over `^- \[ \]` |
| Item numbers 2.01-2.24, 3.01-3.26, 4.01-4.04, 5.01-5.50, 6.01-6.70 contiguous, no duplicates; cross-refs ("items 3.21-3.25", "5.38-5.40", "6.16-6.28", "Item 6.70") resolve | grep/awk |
| Placeholder scan `\bTBD\b|\bTODO\b|\bFIXME\b` = 0 hits. Every item has Context, Action, Output, an "Ensuring" clause (183/186; the 3 exceptions are two template-standard status items and the NON-BLOCKING item) and a blocker-logging clause (181/186) | grep/awk |
| Every spawn item embeds its full prompt (0 spawn items lack "AGENT PROMPT" or "with this prompt") | awk |
| Largest single spawn = 18 agents (items 2.01-2.18, one message); wave 2 = 6; Gate 1 = 15; Gate 2 = 15; Gate 3 instance a = 13 and instance b = 13 only after all a returned; Gate 4 = 4+1; Gate 5 = 4; Phase 5.1 = 10. No item spawns more than 20 | Steps 2.1, 2.2, 3.2, 5.2, 6.2, 6.3, 6.6, 6.9 |
| Execution Context block (lines 108-145): `grep -cE 'src/|/.*:[0-9]+'` = 0. Source areas: 7 areas, each reappears in at least 3 items (review package 16, reflect Tier 2 28, E2 branch 28, E1 evidence 3, installed-only 30, consumers 21, repository rules 21) | grep -c |
| Step 1.3 prerequisites hold now: both commits are `commit`, HEAD `50d4d2b9d`, branch `ironbelly/shadow-runs`, `ls-tree` of the E2 tip lists the workspace; `make sync-dev` and `verify-sync` targets exist | git cat-file/rev-parse/ls-tree, grep Makefile |
| Phase 2 items 2.01-2.24 each reference only their own `research/NN-*.md` output (no wave-internal dependency); output names match Gate 1 partitions A/B/C (01-08, 09-16, 17-24); Gate 1 and Gate 2 report names in the lens items equal the names in consolidation items 3.16 and 5.27 | awk over lines 171-219; Output path listing of 3.01-3.15 and 5.12-5.26 |

## Phase ordering (checklist 3, 4)
research (P2) -> Gate 1 (P3, halts before P4) -> web (P4) -> synthesis 5.01-5.10 -> Gate 2 -> enumeration 5.37 -> debates 5.38-5.49 plus dynamic block -> fold 5.50 -> assembly 6.01 -> sizing 6.02 -> Gate 3 (a, then b) -> fix/verify/control -> Gate 4 fidelity -> Gate 5 anti-omission -> final validation 6.68-6.70 -> Phase 7 -> Post-Completion. Each gate reads the previous gate's `gateN-cycle-control.md` before starting (3.26, 5.37, 6.39, 6.54, 6.68). No cycle in the item graph; "in parallel with items X" references are peer notes, not dependencies. PASS.

## Gate and halt-precedence check (checklist 9)
Agent counts match BUILD-REQUEST: Gate 1 5 types x 3 partitions = 15; Gate 2 the same; Gate 3 5 rf-qa + 5 rf-qa-qualitative + 3 domain = 13 per instance (inside the 9-13 range; builder note line 713 records the choice); Gate 4 4 fidelity + 1 cross-source; Gate 5 4 rf-analyst. Serialized fix (I20): lens agents `fix_authorization: false`, ONE fix agent per cycle, two verifiers. Halt order regression > monotonicity > hard cap with byte-exact messages in every control item (lines 272, 284, 378, 390, 518, 530, 554, 566, 588, 600). Structure PASS; one defect inside the regression clause (issue 3).

## Issues Found
| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| 1 | IMPORTANT | Builder note line 711; Post-Completion item line 631; vs Items 6.45 and 6.50 (lines 548, 560), 6.59 and 6.64 (lines 582, 594), 6.69 (line 606) | The I17 items 5 and 6 deviation (SHA-256 comparison instead of a final-state lens QA and fidelity gate) rests on the claim "Gates 3, 4 and 5 and the final validation ... already run on the final report, and the report is not edited after them" (line 711) and on the attestation text of line 631 ("which ran on the final report"). The task itself edits the report after Gate 3 passes (Gate 4 fix agent 6.45/6.50), after Gate 4 passes (Gate 5 fix agent 6.59/6.64) and after Gate 5 passes (final-validation fix agent 6.69). The compared hash is the LAST `FINAL_REPORT_SHA256` (one rf-qa agent, 6.68/6.70), so equality holds even when Gates 3 and 4 never saw the final text. The attestation is then false in exactly the case I17 item 5 exists for ("catching issues introduced by late-phase fixes"). Template 02 Part 2 requires the Post-Completion placeholders to be expanded into real lens and fidelity items. | Either (a) record the Gate 3 PASS hash and the Gate 4 PASS hash in `gate3-cycle-control.md` and `gate4-cycle-control.md`, and make the Post-Completion item run a reduced Gate 3 (at least 6 lenses) plus Gate 4 (at least 2 fidelity agents) cycle whenever the final hash differs from either; or (b) expand the template placeholders. At minimum make line 711 and the line-631 sentence conditional on "no fix agent edited the report after Gate N". |
| 2 | IMPORTANT | Item 5.10 (line 330: `### QA Reports` = "the Gate 1 reports present at this time"); Item 6.01 (line 448, rule 6: Evidence Trail "lists every research, web, scope, synthesis and QA file and every debate folder produced"); Item 6.68 checklist item 10 (line 604: "debate and QA file (verify against Glob counts)") | Unsatisfiable requirement. synth-10 is written at 5.10, before Gate 2 (5.12 onward). Gate 2 to Gate 5 reports, the gateN-cycle-control files, fix logs, `final-validation-checklist.md` and its fix log are created after assembly, and no item appends them to Section 10 (5.50 adds debate paths only). Item 6.68 item 10 will return a blocking FAIL at least once; Gate 3 lenses that check evidence-trail counts (6.04, 6.06) can raise the same finding, and every later gate creates new qa files so it can recur across cycles and trip the monotonicity or hard-cap HALT. Satisfying it means editing the report after Gates 3-5 (feeds issue 1). The tech-research skill checklist only requires research and synthesis files in the Evidence Trail. | Narrow Section 10, assembler rule 6 and checklist item 10 to research, scope, web, synthesis, gaps-log and debate files plus "QA reports present at assembly (Gate 1 and Gate 2)"; record later QA files in the Task Log (Phase Gate Findings). |
| 3 | IMPORTANT | Cycle-1 control items 3.20 (line 272), 5.31 (378), 6.33 (518), 6.48 (554), 6.62 (588) | The REGRESSION rule is widened to "or a finding reported FIXED (6.62: OK) by one report is reported open by the other". The two cycle-1 verifiers are deliberately different lenses (structural rf-qa vs content rf-qa-qualitative) and each re-judges EVERY blocking finding, so FIXED-vs-STILL-OPEN disagreement is normal. Under the clause it triggers an immediate HALT with the byte-exact message "Regression detected on Item X.Y, previously PASS at cycle 1, now FAIL" although the item was never PASS, and it pre-empts the designed outcome (union count F_1, then fix cycle 2). The template/PR-02 define regression only as an item that PASSed at cycle n and FAILs at n+1. The same items already define F_1 as the union of both reports, so a disagreement is already counted as open. The clause is absent from the cycle-2 controls (284, 390, 530, 566, 600), so the gates are also inconsistent with themselves. | Delete the "or a finding reported FIXED/OK by one report is reported open by the other" clause from the five control items (the union rule counts it), or demote it to a note in the decision file. |
| 4 | IMPORTANT | Step 7.2 (line 621) vs Post-Completion items (lines 631, 633, 635) | `git add .dev/tasks` runs in 7.2 and the 7.2 Execution Log entry is written after it; the final-state check, the Task Summary and the frontmatter `status: Done`/`completion_date` edits (lines 631-635) modify the task file afterwards. The staged snapshot therefore lacks the final task-file state, against the repo rule that `.dev/tasks/` is always staged. | Move the staging command after line 635, or add a final item "re-run `git add .dev/tasks > /dev/null` and repeat the three read-only checks" before the NON-BLOCKING suggestion. |
| 5 | MINOR | Items 2.18 (205), 4.02 (299), 4.04 (303), 6.39 (534), 6.40 (536), 6.42 (540), 6.43 (542) | TB-Add-8: Context names code surfaces (`Makefile`, `tests/skills/test_primitive_dual_surface_lookup.py`, `src/superclaude/agents/reflect-reviewer.md`, `src/superclaude/pr_submit/`, `scripts/reflect_*.py`, `src/superclaude/cli/review/`) with no file:line and no `<!-- evidence-absence: ... -->` comment. Other code-referencing items comply (anchors or the 11 evidence-absence markers). | Add an evidence-absence comment to those items. |
| 6 | MINOR | Item 5.50 (line 439) | TB-Add-5: one item edits five synthesis files (synth-05/06/07/09/10) with no single-item justification comment; its rule says "edit only the three or five synthesis files named above" (ambiguous). | Add a justification comment (one fold agent keeps ONE coherent design across files) and say "the five synthesis files". |
| 7 | MINOR | Post-Completion (lines 629-637) | I17 items 1 (all `- [ ]` marked) and 3 (every blocker entry has a resolution note) have no validation item (the Task Summary item 633 only partly covers 3). No N/A note for the code-test item (report-only task). | Add one validation item and a "tests not applicable: report only" note. |
| 8 | MINOR | Lines 159, 162, 228 | Steps 1.2 and 1.3 lack the template Completion Gate sentence; the Step 3.1 aggregation item and the Phase 7 and Post-Completion items carry no `(Item X.Y)` label though all other items do; the template Part 2 `### Task-Specific Context Files` placeholder section is absent (its content is covered by Previous Stage Outputs and References). | Cosmetic. |
| 9 | MINOR | Item 5.14 (line 342) | Typo "go no beyond their evidence". | "go no further than". |
| 10 | MINOR | Whole file | No explicit Open Questions section, so TB-Add-3 is inactive (no blocked item can reference an OQ index). The 13 [CODE-CONTRADICTED] rows and the [UNVERIFIED] list live in research-notes AMBIGUITIES_FOR_USER and reach the report via `gaps-and-questions.md` (3.26) and Section 9; owner decisions (commit and push, NOT ADJUDICATED conflicts) are in builder note line 716 and Step 7.3. Acceptable; note only. | None. |

## Checklist results
| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Frontmatter complete and well-formed | PASS | yq parse; key set identical to template 02 (the generic `created/template/tracks` keys are not in template 02) |
| 2 | Mandatory template sections | PASS (minor 7, 8) | Task Overview, Key Objectives, Prerequisites & Dependencies, Execution Context (References, Source Areas, Key Constraints), Handoff File Convention, Frontmatter Update Protocol, Detailed Task Instructions, Post-Completion Actions, Task Log |
| 3 | Phase dependencies logical | PASS | ordering section |
| 4 | Phase ordering | PASS | ordering section |
| 5 | Completion items / anti-orphaning | PASS with note | completion items sit in the template-position `## Post-Completion Actions` after Phase 7, gated by the Phase 7 precondition; content defects in issues 1 and 4 |
| 6 | Task Log at bottom | PASS | line 639; Phase 1-7 Findings, Phase Gate Findings, Follow-Up, Deviations |
| 7 | Item count reasonable | PASS | 186 items for 24 research + 4 web, 10 synthesis, 12 debate slots, 5 gates |
| 8 | Open Questions documented | PASS (note, issue 10) | |
| 9 | M3 / M4 / I20 / halt precedence | PASS structurally; defect in issue 3 | |
| 10 | TB-Add-1 | PASS | 0 placeholders; no title-only item |
| 11 | TB-Add-3 | INACTIVE | no OQ index |
| 12 | TB-Add-4 DAG | PASS | no cycles |
| 13 | TB-Add-5 | MINOR (issue 6) | |
| 14 | TB-Add-6 | PASS | template 02 requires an "ensuring..." clause, not a `Verify:` prefix or `- [x]` Acceptance Criteria; the clause is uniform |
| 15 | TB-Add-7 | PASS | 0 file:line refs in the block; all 7 source areas reappear |
| 16 | TB-Add-8 | MINOR (issue 5) | |

Confidence: Verified: 16/16 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
Tool engagement: Read: 9 | Grep (dedicated tool): 0 | Glob: 0 | Bash: 22 (grep, awk, yq and read-only git over the single-line items). Read+Grep+Glob (9) is below the 16 checks, flagged as the spec requires; the checks were done with Bash grep/awk because the items are 2-7 KB single lines, and each result is cited above.

## Recommendations
- Fix issues 1-4 before running `/task`: edits to Post-Completion, Step 7.2, five cycle-1 control items, and the 5.10/6.01/6.68 evidence-trail wording.
- Issues 5-10 are minor notes; no fix pass needed.

VERDICT: FAIL
