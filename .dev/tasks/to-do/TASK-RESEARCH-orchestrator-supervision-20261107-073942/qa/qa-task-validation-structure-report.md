# QA Report — Task Integrity (phase-structure / ordering lens)

**Topic:** Orchestrator mode research task, issue #339
**Date:** 2026-11-07
**Phase:** task-integrity
**Lens:** phase-structure
**Fix cycle:** N/A
**fix_authorization:** false
**Task file:** .dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/TASK-RESEARCH-orchestrator-supervision-20261107-073942.md (443 lines)
**Template:** ~/.claude/templates/workflow/02_mdtm_template_complex_task.md

---

## Overall Verdict: FAIL

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Frontmatter complete | FAIL (minor) | Lines 1-48 read. Has id, title, status, type, priority, dates, parent_doc, depends_on, reflect_pre/reflect_post, tags, template_schema_doc, estimation, task_type. Compared with template 02 it lacks `autogen_method`, `spec_path`, and reflect_pre `coverage_pct` / `depth` / `reviewed_at`; it adds `reflect_post_mode` and reflect_pre `skip_reason`. The rf-qa generic fields `created` / `template` / `tracks` do not exist in template 02, so that part does not apply. |
| 2 | Mandatory template sections | PASS (with note) | Present: Task Overview (l.52), Key Objectives (l.58), Prerequisites & Dependencies (l.68), Execution Context (l.88), Handoff File Convention (l.94), Frontmatter Update Protocol (l.98), Phases 1-7, Task Log (l.362+). Template Part 2 `## Post-Completion Actions` is absent, but its content sits in Phase 7, which the anti-orphaning rule allows. Execution Context uses bullets instead of `###` subsections (minor, I-7). |
| 3 | Phase dependencies logical | FAIL (blocking) | Phase-level order is correct (scope verify, research gate, web, synthesis, assembly plus gates, present). The item-level dependency inside Phase 5 is wrong, see B1/B2. |
| 4 | Phase ordering logical | PASS | `### Phase` headers 1-7 run in sequence, no gaps (awk count). |
| 5 | Completion items in final phase | PASS | Present, tech-reference suggestion, I17 validation, Task Summary, 7.5 reflect gate and 7.6 mark-Done are all in Phase 7 (l.342-360). 7.6 guards on an open HALT. |
| 6 | Task Log at bottom | PASS | l.362-443: Task Summary, Execution Log, Blocker format, Phase 1-7 Findings, Phase Gate Findings, Open Questions / Notes, Follow-Up Items, Deviations. |
| 7 | Item count reasonable | PASS | awk count of `- [ ]` per phase: P1 2, P2 6, P3 15, P4 2, P5 20, P6 28, P7 6, total 79, matching the stated 79. No `* [`, `- []` or nested checkboxes (grep empty). |
| 8 | Open Questions documented | PASS | Task Log Open Questions / Notes section is present; the 5.6 synthesis item owns report Section 9. |
| 9 | M3/M4 QA gate patterns | FAIL (blocking, B4) | M3: 11 lens agents in 6.2-6.4 (at least 6, PASS). Cycle control order is regression, then `[HALT-MONOTONICITY]`, then the 2-cycle cap (PASS). M4: the 6.7 fidelity gate has 4 agents but no cross-source-contradictions agent as in template PG.6. |
| 10 | TB-Add-1 placeholder scan | PASS | Grep for TODO/TBD/FIXME: 3 hits at l.270 and l.274. All three are inside search instructions in the assembler and lens prompts ("search for `[`, TODO, TBD, PLACEHOLDER", "no ... TODO markers anywhere"), so none is a placeholder. No item is title-only. |
| 11 | TB-Add-3 clarification adjacency | PASS (inactive) | No item is blocked on a numbered Open Question, so there is nothing to cross-reference. |
| 12 | TB-Add-4 DAG | PASS (with note) | The only backward edges are the bounded fix-cycle loop-backs (verify, then re-fix, capped at 2). No item reads output produced only by a later item, except the soft 5.4/5.5 coupling covered by B1. |
| 13 | TB-Add-5 granularity | FAIL (minor) | 6.7 and 6.7b each combine "consolidate + conditional fix spawn" in one item and "verify + cycle control" in another. Template 02 splits these. No justification comment is given. |
| 14 | TB-Add-6 format consistency | FAIL (minor) | `Verify:` prefix count is 0. Items use B2 prose ("Then confirm ... ensuring"), but 7.5 alone uses a `**Context:/Action:/Output:/Verification:/Completion gate:**` field layout (the only `**Verification:**` hit). The formats are mixed. |
| 15 | TB-Add-7 source areas reappear; no file:line in block | PASS (with note) | Each source area on l.91 (core/, sc-crash-recovery/, ccsession-tag/, cli/, commands/, the tests dirs, inventory/, the P1 task artifacts, .dev/issues/339, brainstorms) reappears in item Contexts (src/ hits at l.122-318). The block has no `path:NN` reference (grep -oE for `:[0-9]+` on l.88-101 returns nothing). The consumer-side regex `src/|/.*:[0-9]+` matches 1 line (l.91), but only on directory paths, so this is a minor note (I-9). |
| 16 | TB-Add-8 per-item evidence binding | FAIL (minor) | 72 of 79 items name code surfaces with no file:line (awk list: l.108, 112, 126, 130, 152-180, 196, 206-260, 274-338, 346-358). Examples: `src/superclaude/cli/main.py` and `tests/skills/test_worker_contract.py`. `evidence-absence` count is 0. Graded minor because this is a research task whose agents produce the citations. The check still fails as written. |
| 17 | HALT / Frontmatter Update Protocol consistency (lens addition) | FAIL (blocking, B3) | Read l.98-100 and the HALT items at l.180, 260, 310, 324, 338 and 7.5. See B3. |

## Summary
- Checks passed: 10 / 17 (including 3 passes with notes)
- Checks failed: 7. Blocking: 3 (checks 3, 9 and 17, carrying B1-B4). Minor only: 4 (checks 1, 13, 14, 16).
- Issues fixed in-place: 0 (fix_authorization false)

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| B1 | IMPORTANT (blocking, ordering) | Phase 5 note l.202; Step 5.4 l.216; Step 5.5 l.220 | 5.5 (Implementation Plan, Section 8) runs in parallel with 5.4 (Options and Recommendation, Sections 6-7). 5.4 says "Do not assume A1 wins: follow the evidence", yet 5.5 hard-codes the A1 shape (a CLI registration in main.py plus a command file). If 5.4 recommends A2 or A3, Section 8 contradicts Section 7, and only the 5.7 coherence agent would catch it, after the work is done. | Take 5.5 out of the parallel batch. Run it after 5.4, have it read `synthesis/synth-04-*.md`, and plan the option that 5.4 recommends. Update the l.202 "all six independent" note to match. |
| B2 | IMPORTANT (blocking, missing input) | Step 5.5 l.220-222 | 5.5 reads only scope-01, scope-03, scope-04, web-01 and web-02. It does not read `gaps-and-questions.md`, scope-02, `05-orca-row-schema.md`, `06-orca-open-questions.md` or synth-02 (the Gap Analysis). Three gates require every Section 4 gap to map to a Section 8 step or a Section 9 entry: 5.7 tracing-2, assembler rule 5 and the lens cross-reference. The Orca read path (gaps G-A and G-B) is central to the sweep design. As written, 5.5 cannot meet those gates. | Add the missing files to 5.5's input list, together with synth-02 and synth-04 (this follows from the B1 fix). |
| B3 | IMPORTANT (blocking, protocol contradiction) | Frontmatter Update Protocol l.98-100; HALT paths l.180, 260, 310, 324, 338, 7.5 | Every HALT sets `blocker_reason` but never sets `status` to Blocked. The template's mandatory checkpoint says "If Blocked: update status ... and populate blocker_reason". The task's own protocol allows status edits only in 1.1 and 7.6, and does not list `blocker_reason` as an allowed field. So a halted task stays in status "Doing", and every HALT item breaks the task's own protocol by writing `blocker_reason`. | Extend the Frontmatter Update Protocol so that any HALT item may set `status: "Blocked"` and `blocker_reason`. Add the status set to each HALT path. |
| B4 | IMPORTANT (blocking, M4 pattern) | Step 6.7 l.312-324 | The fidelity gate has 4 agents but no cross-source-contradictions agent, and it does not follow the separate fidelity-gate item split of template PG.6. Phase 3 cross-validation covers contradictions between research files only. Contradictions between the assembled report and BUILD-REQUEST, the brainstorm or the issue sources go unchecked. | Add a cross-source-contradictions agent to 6.7 (template PG.6), or state in the item why Phase 3 already covers that lens. |
| M1 | MINOR | Frontmatter l.1-48 | Template fields `autogen_method` and `spec_path`, and reflect_pre `coverage_pct` / `depth` / `reviewed_at`, are missing. reflect_pre `skip_reason` and `reflect_post_mode` are not in the template. `related_docs` is a list of plain strings rather than path/description objects. | Align the fields with the template 02 schema (task-builder A.10.7 populates reflect_pre). |
| M2 | MINOR | Handoff File Convention l.94 | `gaps-and-questions.md` (at the task root) and `reviews/` (used at l.112) are not listed. | Add both to the convention. |
| M3 | MINOR | Phase 7 l.344-358; 3.1, 5.7, 6.2-6.4 | Phase 7 items 7.1-7.4 and 7.6 have no `**Step 7.x:**` labels, but the protocol cites "7.5" and "7.6" and 7.5 uses a different "**7.5 - ...**" label. Several Step headers (3.1, 5.7, 6.2-6.4) cover multiple items, so an item-ID reference cannot be resolved to a single item. | Give every Phase 7 item a `**Step 7.N:**` label and use one ID scheme throughout. |
| M4 | MINOR | 6.7, 6.7b (l.322-338) | Consolidation and the conditional fix are merged into one item, and verification and cycle control into another (granularity). | Split them as in 6.5/6.6, or add a justification comment. |
| M5 | MINOR | Whole file; 7.5 l.354 | There is no `Verify:` prefix anywhere, and 7.5 uses a field layout that no other item uses. | Pick one verification format and apply it to every item. |
| M6 | MINOR | 72 items (list in check 16) | Item Contexts name code surfaces with no file:line and no `<!-- evidence-absence -->` comment. | Add file:line citations or evidence-absence comments (for example "research agent will locate"). |
| I-7 | MINOR | Execution Context l.88-92 | It uses 3 bullets instead of the template's `### References` / `### Source Areas` / `### Key Constraints` subsections. | Convert the bullets to the template subsections. |
| I-9 | MINOR | Execution Context l.91 | The TB-Add-7 consumer-side regex matches directory paths (`src/...`). The line has no file:line, so it does not violate the rule, but strict tooling would flag it. | Optional: name areas by component rather than by path. |

## Confidence
- **Confidence:** Verified: 17/17 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%
- **Tool engagement:** Read: 11 | Grep: 1 | Glob: 0 | Bash: 4
- Note: Read + Grep + Glob = 12, which is below the 17 checklist items. The task file was read in full in chunks, and several checks (1, 2, 4-8, 11-13) were verified from those reads plus the awk/grep Bash runs. Per the Tool Engagement Minimum, flag this review as process-suspect. The findings themselves rest on line-cited evidence.

## Recommendations
- Fix B1-B4 in the task file before execution. B1 and B2 are fixed together by making 5.5 sequential after 5.4 with a complete input list.
- Minor items M1-M6, I-7 and I-9 are notes only.

## QA Complete

VERDICT: FAIL

Blocking issues: B1 (5.5 runs parallel to 5.4, so the plan can contradict the recommendation), B2 (5.5 is missing the gap and Orca inputs it needs to satisfy the gates), B3 (the HALT paths never set Blocked status and break the task's own Frontmatter Update Protocol), B4 (the 6.7 fidelity gate lacks the template PG.6 cross-source-contradictions agent).
