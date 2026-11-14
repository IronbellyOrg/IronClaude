# QA Report: Task Integrity, Structure and Phase Ordering (Partition p1)

**Task file:** .dev/tasks/to-do/TASK-RF-sweep-phase1-20261108-072653/TASK-RF-sweep-phase1-20261108-072653.md
**Scope:** frontmatter, front sections, Phases 1 to 7 (task file lines 1 to 1264)
**Date:** 2026-11-08
**Phase:** task-integrity
**Lens:** phase-structure
**Fix authorization:** false (report only)
**Fix cycle:** N/A

---

## Overall Verdict: FAIL

5 IMPORTANT (blocking) findings, 0 CRITICAL, 12 MINOR notes.

[PARTITION NOTE: this is partition p1 (lines 1 to 1264). Cross-file checks that need Phases 8 to 14 (TB-Add-7 source-area reappearance, template Task Log sections) were run against the whole file with Grep, and are marked where they fall outside the partition.]

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Frontmatter complete; `spec_path` and `reflect_post_mode: skill` present; no `start_commit` or `executor_model_class` | PASS (with notes) | Read lines 1-69: `spec_path: "docs/designs/orchestrator-mode.md"` (line 20), `reflect_post_mode: skill` (line 21). Grep `start_commit\|executor_model_class` hits only line 2366 (POST runner prompt body), none in frontmatter. Field set matches template 02 lines 2-60. Notes M10, M17. |
| 2 | Mandatory template sections present, including `## Execution Context` | PASS (with notes) | Headings grep: Task Overview (72), Key Objectives (78), Prerequisites (90, 92, 100), Execution Context (117) with References (119), Source Areas (142), Key Constraints (155), Handoff File Convention (167), Frontmatter Update Protocol (194), Detailed Task Instructions (204). Template 02 sections missing elsewhere in the file: see M11. |
| 3 | Phase dependencies logical | PASS | Phase 1 setup, 2 to 5 design fixes, 6 R5 HALT, 7 pre-implementation gates, 8 onward code (headings 206, 238, 419, 586, 760, 976, 1010, 1265). Each phase consumes only earlier outputs (for example 6.3 reads the 5.4 WC-16 text, 7.13 reads OQ-1 to OQ-7 files). |
| 4 | Ordering follows BUILD-REQUEST MANDATORY PHASE ORDER | PASS (with note) | BUILD-REQUEST:54-76. Task: R3-B1 (Phase 2), R3-B2 (3), R3-B3 (4), R4 (5), each with a gate; R5 HALT (6); 1.0b (7.1-7.13), 1.0a (7.14-7.18), 1.16a (7.19); first code item 8.2 (line 1276). 7.18 writes `tests/sweep/fixtures/` before Phase 8, but DESIGN line 876 makes that part of step 1.0a, so accepted. See M13. |
| 5 | Design-fix gates follow M3; agent counts at or above I19/I22 full floors; own `qa/<gate>/` folder | FAIL | R3-B1/B2/B3 and R4 gates: 9 agents each (4 rf-qa + 4 rf-qa-qualitative + 1 domain), meets research/09:193 (8 plus domain). Each writes 18 outputs into its own folder (`qa/r3-b1/`, `qa/r3-b2/`, `qa/r3-b3/`, `qa/r4/`). Failures: I-1 (R5 has no own gate), I-2 (decisions gate below floor), I-3 (regression PASS set not producible), I-4 (no parallel spawn). |
| 6 | Owner-decision items use the human-gate pattern (OQ-n, PENDING record, HALT to Blocked without tick) | PASS (with notes) | OQ-1 to OQ-8 in Open Questions (lines 2457-2464). Record items 6.1, 7.1, 7.3, 7.5, 7.7, 7.9, 7.11, 7.14 write `status: PENDING` files. HALT items 6.2, 7.2, 7.4, 7.6, 7.8, 7.10, 7.12, 7.15 use the HALT rule (line 192: sets "⚪ Blocked", fills `blocker_reason`, STOP, do not tick). GQ-63 states no recommendation (line 1074). Notes M12, M16. |
| 7 | TB-Add-1: no TBD/TODO/FIXME, no title-only items | PASS | Grep `TBD\|TODO\|FIXME`: every hit (285, 286, 293, 452, 453, 460, 627, 634, 843, 850, 1003) is a grep command or lens prompt that checks DESIGN for those tokens, not a placeholder. 144 items in lines 1-1264; 144 each of Context, Action, Output, Verification, Completion gate fields (Bash count). |
| 8 | TB-Add-3: blocked items cite their OQ-n in Context | PASS (with note) | Record and HALT items cite OQ in titles and Context. Gaps in dependent items: M7. |
| 9 | TB-Add-4: item dependencies form a DAG | PASS | Back-references only to earlier items; the only back-edges are bounded re-run loops (2.7 to 2.1-2.6, 6.4 to 6.3, 7.20 to owning item), which are retries, not dependency cycles. Forward mentions (7.1 "Blocks: item 9.1", 6.4 "reviewed by the decisions gate in Phase 7") are notes, not inputs. |
| 10 | TB-Add-5: XL or multi-file items split | PASS | R3 and R4 edits are one item per edit group (2.1-2.6, 3.1-3.4, 4.1-4.5, 5.1-5.11); one agent per item; 1.3 writes two small artifact files in one read-only step. |
| 11 | TB-Add-6: `Verify:` prefix throughout | PASS (with note) | Bash: 144 Verification lines, 143 start `Verify:`; item 6.3 (line 998) starts `Verify on branch (b):`. M6. |
| 12 | TB-Add-7: Source areas reappear in items; block has no `file:line` | FAIL | Grep of item Context lines across the whole file: `cli/recommend` 2, `cli/reflect` 2, `commands/issue.md` 2, `commands/graph.md` 2, `plugins/superclaude` 2, `developer-guide` 1, `tests/core` 4, `tests/recommend` 4; `cli/sprint` 0 and `cli/swarm` 0. I-5. Block lines 117-202 have `src/` hits (GOAL verbatim) and line references, M8. |
| 13 | TB-Add-8: Context citing code has `file:line` or evidence-absence | PASS (with note) | Most Contexts cite `file:line` (for example 1.2 `SKILL.md:204`, 6.1 `WORKER-CONTRACT.md:110`, 7.9 `pragmatic.md:22`). Gaps: M9. |

## Summary

- Checks passed: 11 / 13 (7 of them with notes)
- Checks failed: 2 (checks 5 and 12)
- Critical issues: 0
- Important issues: 5
- Minor issues: 12
- Issues fixed in-place: 0 (`fix_authorization: false`)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| I-1 | IMPORTANT | Phase 6 (lines 976-1008); item 1.2 (line 217); Key Constraints (line 156) | R5 edits DESIGN (item 6.3 adds a section 8 sentence and a `### Fix cycle 3` row) but has no QA gate of its own and no `qa/r5/` folder. BUILD-REQUEST:56 says each required design-fix item "edits DESIGN and is closed by its own QA gate". Item 6.4 Context (line 1002) hands the review to the Phase 7 decisions gate, which runs only after six more owner HALTs and the live step 1.0a capture, with lenses aimed at decision records (only 7.22, line 1174, touches the R5 sentence). The R5 DESIGN edit gets no template-conformance, consistency or SPEC-fidelity review. | Add an R5 gate after 6.4 (report-only lenses on the R5 DESIGN edit, one fix agent, two verifiers, at most 2 cycles), add `qa/r5` to the 1.2 mkdir and the 1.2 folder count (12), and add `qa/r5/` to the Key Constraints folder list. |
| I-2 | IMPORTANT | Item 7.21 Context (line 1166); items 7.21-7.25 | The decisions gate uses 5 agents (2 rf-qa, 2 rf-qa-qualitative, 1 rf-analyst), the intermediate task-integrity mix. task-builder SKILL.md:1009 sets the full-intensity floor at "6+ agents minimum (3 rf-qa + 3 rf-qa-qualitative per I19, plus domain lenses)" and says gates below it are "PROHIBITED"; SKILL.md:1041-1046 says not to apply the intermediate 5-agent mix to phase gates. This gate is a phase gate whose outputs feed code (and, per I-1, it is the only review of the R5 DESIGN edit). | Raise the decisions gate to at least 3 rf-qa + 3 rf-qa-qualitative plus a domain lens (keep the rf-analyst cross-source lens as the extra), and update the "1 of 5" titles, the 7.26 report count and the item 7.21 sizing sentence. |
| I-3 | IMPORTANT | QA Gate Protocol report-only preamble (line 188); item 2.17 (line 356); item 2.21 (line 384); mirrored by 3.15, 4.16, 5.22, 7.26, 7.30 | The regression guard compares against a "cycle-0 PASS set listing every check id each agent passed" (2.17), but the report-only preamble asks agents only for findings, a verdict and a blocking count; it never asks them to list the checks they passed. The cycle-0 PASS set cannot be built from the reports, so the first-precedence regression halt at cycle 1 has no defined input in all five gates. | Add to the report-only preamble: "List every check you ran by check id with PASS or FAIL." (the verifier preamble at line 190 already does this), so 2.17 can build the PASS set. |
| I-4 | IMPORTANT | All report-only lens batches: 2.8-2.16, 3.6-3.14, 4.7-4.15, 5.13-5.21, 7.21-7.25; verifier pairs 2.19/2.20 and peers | M3 (task-builder SKILL.md:1016-1018) says "spawn all lens agents in parallel with fix_authorization: false"; template 02 marks PG.2, PG.3 and PG.5 as PARALLEL (template lines 1376, 1384, 1394). Grep of lines 1-1264 for "parallel" returns 0 hits, and the Spawn rule (line 191) says "one agent per item" with no parallel batch instruction, so the executor will run 9 lens agents one after another per gate. | Add a parallel-batch note before each lens batch and each verifier pair (for example "Items 2.8 to 2.16 are independent and report-only; spawn them in one parallel batch, then tick each item when its report exists"). |
| I-5 | IMPORTANT | Execution Context Source Areas (line 146) | TB-Add-7 drift. The source area "`superclaude.cli.sprint` / `superclaude.cli.swarm` (the link-and-fsync publish pattern)" appears in no item Context anywhere in the file (Grep of Context lines: 0 hits for `cli/sprint` and `cli/swarm`; the `sprint` hits are `.dev/sprint-state/` and `/sc:swarm-wizard`). Item 9.1 (line 1477), which implements `_publish`, cites only DESIGN sections 3.2 and 7.1. The header claims an input no item reads. | Either cite the sprint and swarm publish code with `file:line` in item 9.1 Context, or drop that Source Areas bullet. |
| M6 | MINOR | Item 6.3 Verification (line 998) | Prefix is `Verify on branch (b):`, not `Verify:` (TB-Add-6). | Change to `Verify: on branch (b), ...`. |
| M7 | MINOR | Items 6.3 (line 995), 7.16 (line 1122), 7.17 (line 1138), 7.18 (line 1145); items after Phase 6 generally | TB-Add-3 and research/06:103 ask every dependent item's Context to cite its gating OQ. 6.3 cites "item 6.2", not OQ-1; 7.16-7.18 cite item 7.15 or the probe file, not OQ-8. Earlier HALT items prevent harm. | Add "Blocked by OQ-1" / "Blocked by OQ-8" to those Context fields. |
| M8 | MINOR | Execution Context lines 121-132, 138, 160, 164 | The block contains `src/` paths and line references (`after line 565`, "REPORT line 1247", "REPORT line 1238"), which the TB-Add-7 consumer grep would count. The GOAL text is verbatim by BUILD-REQUEST:45, so this is the mandated form. | Optional: move the two REPORT line citations into the items that use them. |
| M9 | MINOR | Item 2.15 Context (line 341); item 7.11 Context (line 1087) | TB-Add-8: 2.15 states "`pyproject.toml` requires Python >=3.10" with no `file:line` (the line is `pyproject.toml:16`); 7.11 cites "DESIGN section 13 D9" with no line. | Add `pyproject.toml:16`; add the D9 line or an evidence-absence comment. |
| M10 | MINOR | Frontmatter line 55 | `template_schema_doc: ".claude/templates/workflow/02_mdtm_template_complex_task.md"` does not exist in this checkout (repo `.claude/` holds only `agent-memory`, `cache`, `settings.json`); the installed copy at `~/.claude/templates/workflow/` exists, and References line 140 names it. | Point the field at `~/.claude/templates/workflow/02_mdtm_template_complex_task.md`. |
| M11 | MINOR (outside partition except the first point) | Whole-file headings | Template 02 sections missing: `### Task-Specific Context Files` (template 1332), `## Post-Completion Actions` (1427), and in the Task Log `### Task Summary` (1449), `### Phase Gate Findings` (1502), `### Follow-Up Items Identified` (1506), `### Deviations from Process` (1512). Phases are H2 (`## Phase N`) siblings of `## Detailed Task Instructions`, where the template uses H3. Partition p2 should confirm whether Phase 14 covers the Post-Completion items. | Add the missing Task Log subsections; add Post-Completion Actions or note that Phase 14 replaces it. |
| M12 | MINOR | Phase 7 items 7.1-7.15 | Each record item is written only after the previous HALT resolves, so the owner faces up to seven separate stop-and-resume cycles (OQ-2 to OQ-8) and cannot answer them together from the files. | Write all seven PENDING records first, then a single HALT item that checks all seven files. |
| M13 | MINOR | Phase 5 (items 5.1-5.3) and items 7.3-7.4 | R4 renumbers DESIGN to WC-16 before the owner answers GQ-11 (WC-16 or amend WC-1). If the owner picks (b), 7.4 HALTs and the R4 work is redone. BUILD-REQUEST:60 mandates the R4 renumber, so this is a known ordering cost. | Note it in Phase 5 intro, or ask GQ-11 at Phase 1. |
| M14 | MINOR | Item 7.18 Verification (line 1148) | `grep -rn '/home/coder\|coder' tests/sweep/fixtures/` also matches `encoder` and `decoder`, which can give a false failure. | Use `grep -rnw 'coder'` plus the `/home/coder` pattern. |
| M15 | MINOR | Item 1.1 (lines 208-213) | Template 02 Step 1.1 (template line 1327) also appends a "Task started" line to `### Execution Log`; item 1.1 does not. | Add the Execution Log entry. |
| M16 | MINOR | Open Questions (lines 2455-2470) | research/06:97 asks for OQ entries tagged `needs_human_decision`; entries say "OWNER DECISION PENDING" instead, and sit under the Task Log, not Execution Context. | Add the tag (location is acceptable). |
| M17 | MINOR | Frontmatter | The generic rf-qa check 1 lists `created`, `template`, `tracks`; template 02 uses `created_date` and `template_schema_doc` and has no `tracks`. The task matches its template, so this is a note only. | None needed. |

## Actions Taken

None. `fix_authorization: false`; the task file was not edited.

## Recommendations

- Fix I-1 to I-5 in the task file, then re-run this lens on Phases 1 to 7.
- I-3 is the cheapest and most important: one sentence in the report-only preamble restores the regression halt in all five gates.

## Confidence

- **Confidence:** Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 11 | Grep: 11 | Glob: 0 | Bash: 6

## QA Complete

VERDICT: FAIL


