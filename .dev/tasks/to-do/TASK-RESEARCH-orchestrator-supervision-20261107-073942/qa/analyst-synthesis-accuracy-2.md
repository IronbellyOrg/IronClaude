# Synthesis Accuracy Review (Partition 2 of 2)

**Analysis type:** Synthesis quality review, synthesis-accuracy lens (checklist items 1-5)
**Date:** 2026-11-07
**Task:** orchestrator mode Phase 1, issue #339
**Task directory:** `.dev/tasks/to-do/TASK-RESEARCH-orchestrator-supervision-20261107-073942/`
**Assigned synthesis files:** `synthesis/synth-04-options-recommendation.md` (275 lines), `synthesis/synth-05-implementation-plan.md` (309 lines), `synthesis/synth-06-questions-evidence.md` (231 lines)
**Sources read:** `gaps-and-questions.md` (all 359 lines), `research/scope-03-cli-patterns.md` (full), `qa/qa-nb4-fix-log.md`, the Report Structure template (`~/.claude/skills/tech-research/SKILL.md:1311-1487`); targeted line reads and greps of the other nine `research/*.md` files (line counts, cited lines, fallback notes); spot checks of cited repository code (`tests/skills/test_worker_contract.py:245-254`, `:545`; `src/superclaude/skills/sc-crash-recovery/scripts/bootstrap_scan.sh:70-84`). Coverage limit: research-notes, scope-02, scope-04, 05, 06, 07, web-01 and web-02 were not re-read end to end; claims sourced only from them were checked at their cited lines, not against the whole file.
**Fix authorization:** false. No synthesis file was edited. md5 of the three files before review: synth-04 `80717655259a0047bd8234a1e3b4fb04`, synth-05 `e4236cd49b616f17622fe88aa1191b22`, synth-06 `ccbb50b1a4dfc3c4ecf11ca976a89619`.
**Severity rule:** CRITICAL and IMPORTANT block; MINOR are notes.

[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file analysis requires merging all partition reports.]

---

## Per-File Review

### synth-04-options-recommendation.md

**Sections covered:** 6. Options Analysis, 7. Recommendation, plus unnumbered "Open Questions" and "Coverage and exclusions"
**Verdict:** FAIL (1 IMPORTANT, 5 MINOR)

| Check # | Check | Result | Evidence/Issue |
|---|---|---|---|
| 1 | Section headers match template | PASS with notes | `## 6. Options Analysis` (:24), `### Option A1..A4` (:37, :95, :122, :150), `### Options Comparison` (:176), `## 7. Recommendation` (:189). Notes: :191 says "Recommended option" where the template says "**Recommended approach:**"; extra unnumbered H2s at :248 and :263 (M1, M2) |
| 2 | Table column structure | PASS with notes | Aspect tables carry Effort, Risk, Reuse, Files/systems affected, Pros, Cons; comparison (:178) is Criterion x A1/A2/A3 with the five template rows plus one extra row. Notes: steps table :224 uses Step/Work/Files; OQ table :250 uses #/Question/Source/Blocks (M3, M4) |
| 3 | No fabrication | FAIL | X-6 (:220) states that `gaps-and-questions.md:125` "still says Open: 76. Resolved: 24"; the file now reads "Open: 75. Resolved: 25" (F1). R-3 (:159) says the scanner "skips" worktrees; the code reports them as not a repo (M5) |
| 4 | Actual paths and evidence cited | PASS | Every option row and R-1..R-4 cite file:line; spot checks held (`bootstrap_scan.sh:72-83`, NB-4 allowlist `scope-03:99`) |
| 5 | >=2 options with assessment tables; A4 only as rejected with [CODE-CONTRADICTED] reason | PASS | A1, A2, A3 each have an Aspect table and appear in the comparison; A4 is headed "(REJECTED, [CODE-CONTRADICTED])" (:150), excluded from the comparison (:172), with R-1/R-2 tagged [CODE-CONTRADICTED] (C3, C4). Note: :156 says every reason is a code fact, but R-4 is a design argument (M5) |

### synth-05-implementation-plan.md

**Sections covered:** 8. Implementation Plan (Phase 1 sub-tables 1A-1F, later phases, 8.1-8.5, Integration Checklist)
**Verdict:** FAIL (2 IMPORTANT)

| Check # | Check | Result | Evidence/Issue |
|---|---|---|---|
| 1 | Section headers match template | PASS | `## 8. Implementation Plan`, `### Phase 1` with Goal and Dependencies, Integration Checklist present |
| 2 | Table column structure | PASS | Steps 1.1-1.29 use Step/Action/Files/Details |
| 3 | No fabrication | FAIL | X-6 (:260) and the C2 rows (:172, :206) call the `gaps-and-questions.md:125` count stale and file it under C2; C2 is the test-file length (gaps :171), and :125 is now correct (F2). Step 1.17 (:104) and 8.1 (:158) state "GQ-11 decided as WC-14"; the gaps file marks GQ-11 an open owner decision (F5) |
| 4 | Actual paths and evidence cited | PASS | Spot checks held: `NEVER_AS_WORKER` has 8 entries and the test at `tests/skills/test_worker_contract.py:545` is named "all seven" (1.19 correct); Check 11 at `Makefile:467-476`; allowed-tools space form matches `scope-03:208-209` |
| 5 | Options | N/A | Plan file; follows A1 |

### synth-06-questions-evidence.md

**Sections covered:** 9. Open Questions (9.1-9.7), 10. Evidence Trail
**Verdict:** FAIL (2 IMPORTANT, 4 MINOR)

| Check # | Check | Result | Evidence/Issue |
|---|---|---|---|
| 1 | Section headers match template | PASS | `## 9. Open Questions` (:19), `## 10. Evidence Trail` (:189), `### Codebase Research` (:193), `### Web Research` (:206), `### Gaps Log` (:224) |
| 2 | Table column structure | PASS | 9.x tables use #/Question/Impact/Suggested Resolution; Codebase Research uses File/Topic/Agent Type; Web Research uses File/Topic |
| 3 | No fabrication | FAIL | Row 17 (:45) resolution "keep it off by default" for `--include-remote` contradicts the plan and the research (F3). Row 58 (:86) resolution "Apply rule 2 before rule 7" misstates GQ-84's resolution (F4) |
| 4 | Actual paths and evidence cited | PASS with notes | All ten research line counts match `wc -l` (05=206, 06=190, 07=94, notes=335, s01=152, s02=242, s03=215, s04=374, web-01=229, web-02=63). Fallback notes match web-01:8 and web-02:6. Note: :221 still calls synth-05 "not yet written" (M9) |
| 5 | Options | N/A | Questions and evidence file |

---

## NB-4 Re-check (corrected allowlist)

Result: **PASS.** No synthesis text uses the old allowlist. task-list, run-list, run-current and gate-list appear as allowed and `inbox` as forbidden at synth-04 :18, :34 (K-5), :62 and OQ-8 (:259); synth-05 :9 and step 1.4 (:62, citing "`scope-03:99` after NB-4"); synth-06 :11. This matches `research/scope-03-cli-patterns.md:99` and `qa/qa-nb4-fix-log.md`. The only NB-4 residue is the stale gap-count text handled in F1 and F2.

---

## Issues Requiring Fixes

### Blocking (IMPORTANT)

| # | Severity | File:location | Check | Issue | Required fix |
|---|---|---|---|---|---|
| F1 | IMPORTANT | synth-04 :220 (X-6) | 3 | States that `gaps-and-questions.md:125` "still says Open: 76. Resolved: 24" with GQ-03 open. The current line reads "Open: 75. Resolved: 25 (GQ-03, ...)" and "Open blocking QA finding: none". The claim was true when `qa/qa-nb4-fix-log.md:39` was written and is now false. | Delete X-6, or restate it as "gaps:125 was corrected to 75/25 after the NB-4 pass; no effect on the option choice". |
| F2 | IMPORTANT | synth-05 :260 (X-6), :172 (C2 row in 8.1), :206 (8.5), :282 | 3, 4 | Calls the gap count at `gaps-and-questions.md:125` stale and sends it to Open Questions "(C2)". The count is no longer stale (see F1), and C2 is a different claim: the length of `tests/core/test_how_we_work_routing_table.py`, 1202 lines (`gaps-and-questions.md:171`; synth-06 row 89 at :134 uses C2 correctly). | Remove the stale-count statement; take the C2 label off X-6 and the :282 row; keep C2 only for the test-file length. |
| F3 | IMPORTANT | synth-06 :45 (row 17, GQ-22) | 3 | Suggested resolution "Measure once; keep it off by default" for `--include-remote`. synth-04 :60 and synth-05 step 1.4 (:62) put `--include-remote` in the default worker-list argv, and the gaps row (`gaps-and-questions.md:45`) records that remote rows read `unverifiable` without it (05 `:163`). No research line supports "off by default". | Change the resolution to "Keep `--include-remote` on (remote rows read `unverifiable` without it, 05 :163); measure its cost once". |
| F4 | IMPORTANT | synth-06 :86 (row 58, GQ-84) | 3 | Suggested resolution "Apply rule 2 before rule 7" repeats the problem statement. The gaps row (`gaps-and-questions.md:107`) says the plan should state that rule 2 needs the transcript read, so an exited row with no `worker_done` and an unreadable transcript gives could not determine. synth-05 8.1 (:161) has this right. | Replace the resolution with "Rule 2 needs the transcript read; exited, no `worker_done`, unreadable transcript -> could not determine (synth-05 1.3)". |
| F5 | IMPORTANT | synth-05 :104 (step 1.17, "GQ-11 decided as WC-14, not a WC-1 clause"), :158 (8.1 row "GQ-11 WC-14"), :138 (G7/GQ-10 row) | 3 | Treats two owner decisions as settled. `gaps-and-questions.md:34` and :153 mark GQ-11 "open (owner decision); WC-14 is the working name"; :152 marks the report location (GQ-10, AMBIGUITY 3) an open owner decision. synth-06 rows 8-9 (:36-37) and 101-102 (:151-152) list both as owner decisions. The `.dev/` location has research support (`scope-01-contract.md:84` proposes it), but neither choice was made. | In 1.17, :158 and :138, say "working name WC-14 (GQ-11 open owner decision)" and "proposed location `.dev/` per scope-01:84 (GQ-10 open owner decision)", and list GQ-10 and GQ-11 in 8.2. |

### Notes (MINOR)

| # | Severity | File:location | Check | Issue | Required fix |
|---|---|---|---|---|---|
| M1 | MINOR | synth-04 :191 | 1 | "**Recommended option: A1.**"; the template opens Section 7 with "**Recommended approach:**". | Use the template label. |
| M2 | MINOR | synth-04 :248, :263 | 1 | Unnumbered H2s "## Open Questions" and "## Coverage and exclusions" will collide with Section 9 and the Evidence Trail at assembly. | Demote them to H3 under Section 7, or fold OQ-1..OQ-10 into synth-06 Section 9. |
| M3 | MINOR | synth-04 :224 | 2 | Steps table uses Step/Work/Files, not Step/Action/Files/Details. | Rename the columns, or replace the table with a pointer to synth-05 Section 8. |
| M4 | MINOR | synth-04 :250 | 2 | OQ table uses #/Question/Source/Blocks, not #/Question/Impact/Suggested Resolution. | Use the template columns, or merge into Section 9. |
| M5 | MINOR | synth-04 :156, :159, :160, :174 | 3 | :156 says "Each reason below is a code fact", but R-4 (:160) is a design argument. R-3 (:159) says the scanner "skips worktrees whose `.git` is a file"; `bootstrap_scan.sh:72-83` prints `{"is_repo":false}` for them, which is what synth-04's own :174 says. | Reword :156 ("R-1 to R-3 are code facts; R-4 is a design reason") and R-3 ("reports them as not a repo"). |
| M6 | MINOR | synth-06 :49 (row 21, GQ-26) | 3 | Pins the colon form `Bash(superclaude sweep:*)`; synth-05 and the B-19 decision at `scope-03-cli-patterns.md:208-209` use the space form `Bash(superclaude sweep *)`. scope-03 has both forms, so this is a consistency defect, not a fabrication. | Use the space form. |
| M7 | MINOR | synth-06 :55 (row 27, GQ-32) | 3 | "Print the window and the Run ids"; synth-05 step 1.5 (:63) prints "Scope:" with the root path. GQ-32 is an open plan decision (`gaps-and-questions.md:55`), so the two files disagree. | Align with synth-05 or mark it open. |
| M8 | MINOR | synth-06 :61 (row 33) | 3 | Merges GQ-38 (worker-list paging, `page.hasMore`, `gaps-and-questions.md:61`) with GQ-48 (message listing capped at 100, :71); the resolution text belongs to GQ-48 only. GQ-38's handling is paging on `page.nextCursor`. | Split the row. |
| M9 | MINOR | synth-06 :221 | 4 | Lists synth-05 as "planned; not yet written"; synth-05 exists (309 lines). | Drop the parenthetical. |
| M10 | MINOR | synth-04 :218 vs synth-05 :258 (X-4) | 3 | synth-04 calls the guide's reading of null `agentWait` "the safer one"; synth-05 says "Follow the help reading". The resulting rule (null is not stall proof; absent = could not determine) is the same. | Use one wording. |
| M11 | MINOR | synth-04 :3, synth-06 :3 vs synth-05 :10 | 3 | synth-04 and synth-06 list six classes without "fenced"; synth-05 lists seven, including fenced (WC-12, step 1.3 rule 3). | Add "fenced" to synth-04 :3 and synth-06 :3. |

### Verified as correct (not findings)

- A4 appears only as rejected, with C3/C4 [CODE-CONTRADICTED] reasons (synth-04 :150-174).
- `NEVER_AS_WORKER` has 8 entries and the test name says "all seven" (`tests/skills/test_worker_contract.py:245-254`, `:545`), as synth-05 1.19 states.
- The research line counts and web fallback notes in synth-06 Section 10 match the files.
- The md5 of all three synthesis files after review equals the pre-review values: synth-04 `80717655259a0047bd8234a1e3b4fb04`, synth-05 `e4236cd49b616f17622fe88aa1191b22`, synth-06 `ccbb50b1a4dfc3c4ecf11ca976a89619`.

---

## Summary

- Files reviewed: 3. Passed: 0. Failed: 3.
- Issues: 16 (0 CRITICAL, 5 IMPORTANT, 11 MINOR).
- Blocking: 5 (F1-F5).
- NB-4 allowlist: carried correctly in all three files.

## Verdict: FAIL

