# QA Report — Report Qualitative (Fidelity Fix Verification)

**Topic:** Orchestrator mode Phase 1 (issue #339) research report — source-fidelity fix verification
**Date:** 2026-11-08
**Phase:** report-qualitative (fix-cycle verification of fidelity findings F0-01..F0-21)
**Fix cycle:** 1
**Fix authorization:** false (report only; the report was not edited)

---

## Overall Verdict: FAIL

Four blocking findings are open (N1-N4, all IMPORTANT). Two are contradictions left by incomplete fixes (F0-01, F0-17). Two are omissions the fixes introduced: the data-loss guard from the CRITICAL fix F0-11 (and F0-19) has no test case, and the rollback does not cover the F0-20 edit. Seventeen of the 21 fidelity findings are fully resolved. All five orchestrator checks pass except "no contradiction between sections".

## Per-finding status (F0-01 to F0-21)

| ID | Severity (consolidated) | Status | Evidence (report line) |
|----|------|--------|------------------------|
| F0-01 | IMPORTANT | **OPEN** (see N1) | Rule 1 now skips a live blocked contract under `ask the coordinator` (:1219, :113, diagram :371-374), but step 1.3 rule 4a and 4b-contract in the same row still match that contract, and the GQ-96 sentence and the step 1.8 fixture (:1229) contradict each other. |
| F0-02 | IMPORTANT | RESOLVED | `partial` = finished, "partial: usable not yet judged": :64, :118, :385, :438, step 1.3 rule 6 (:1219), step 1.8 rule 6 fixture (:1229). |
| F0-03 | IMPORTANT | RESOLVED | :196. |
| F0-04 | IMPORTANT | RESOLVED | :451, :967, :1077, :1164, :1444. |
| F0-05 | IMPORTANT | RESOLVED | Step 1.6 (:1222): option types, exit codes, JSON keys always present, `--output` rejection. |
| F0-06 | IMPORTANT | RESOLVED | :267, :314-315, :326, :411; 9.4 row 98c (:1642) records the #409 design choice as an owner decision with a working default. |
| F0-07 | IMPORTANT | RESOLVED | :281, :326. |
| F0-08 | IMPORTANT | RESOLVED | :278, :431, :587, :614; 5.8 :825; K-6 :910. |
| F0-09 | IMPORTANT | RESOLVED | :273. |
| F0-10 | IMPORTANT | RESOLVED | :277, :283, :444; 9.4 row 98b (:1641) records DESIGN-CONTRACT rule 5 versus the seed brief as an owner decision. |
| F0-11 | CRITICAL | RESOLVED in text; test gap open as new finding N3 | :363, :406-407, :480-481; step 1.2 `WorktreeState.unpushed` (:1218); step 1.3 `git status --branch --porcelain` (:1219). Step 1.9 does not test it (N3). |
| F0-12 | IMPORTANT | RESOLVED | :37; Later phases table :1297-1306 (Blockers column, [CONTRADICTION] note). |
| F0-13 | IMPORTANT | RESOLVED | Same locations as F0-12; phases recorded, not designed. |
| F0-14 | IMPORTANT | RESOLVED | :163, :377-378. |
| F0-15 | IMPORTANT | RESOLVED | :174, :555. |
| F0-16 | IMPORTANT | RESOLVED | :167, :538, 7.1 row 15, 9.1 row 15. |
| F0-17 | IMPORTANT | **OPEN** (see N2) | GQ-09 is settled at §7 :1071, step 1.0b :1211, 8.1 :1319 and :1389, 9.1 row 7 :1520, 9.2 row 66 :1591 and 9.5 row 106 :1655, but the 8.2 row at :1409 still lists G6 as an owner decision and says "asks for all six". |
| F0-18 | IMPORTANT | RESOLVED | :560, :1343, :1388, row 57 :1571, 9.5 row 109 :1658. |
| F0-19 | IMPORTANT | RESOLVED in text; test gap open as new finding N3 | :408 (`git status --porcelain -- .dev/tasks`), step 1.2 `dev_tasks_unsaved` (:1218), step 1.3 (:1219). Not tested (N3). |
| F0-20 | IMPORTANT | RESOLVED; rollback gap open as new finding N4 | Steps 1.21(b) and 1.23; Rollback "Four registries" row (:1287) omits the 1.21(b) bullet (N4). |
| F0-21 | IMPORTANT | RESOLVED | :410, :776. |

Count: 17 fully resolved, 2 open (F0-01, F0-17), 2 resolved in text with a new blocking test gap (F0-11, F0-19), 1 resolved with a new blocking rollback gap (F0-20).

## Orchestrator's five checks

| Check | Result | Evidence |
|-------|--------|----------|
| No fix introduced a contradiction between sections | **FAIL** | N1 (step 1.3 rule 1 versus rule 4 and the step 1.8 fixture), N2 (8.2 :1409 versus §7 :1071, step 1.0b :1211, 9.1 row 7 :1520). |
| Section 8 plans only A1, which Section 7 recommends | PASS | §7 recommends A1; the 8.x steps build `superclaude sweep` + `/sc:sweep` (A1 shape); A2/A3 appear only as alternatives. |
| WC-10 intact (absent signal never proof of death) | PASS | Step 1.3 rule 2 needs Orca `exited` or an Orca-observed exit; `unverifiable`, late heartbeat, stale `liveStatus` and a missing row give could not determine (:1219); :832-846; 9.2 row 68 (:1593), row 70 (:1595); 9.4 rows 95 and 98 (:1636, :1639). |
| A4 never recommended | PASS | :848, :1028, :1166, :1564, 9.3 row 84 (:1620), 9.4 row 90 (:1631): A4 rejected throughout. |
| Later phases recorded, not designed | PASS | Later phases table :1297-1306 lists each phase with blockers only; the "Not a source phase: bounded automatic recovery" row records the OTP item without design. |

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Problem statement matches findings | PASS | §1-2 still frame Phase 1 as a read-only sweep with a static report; no fix moved scope to a later phase (:37, Later phases table :1297-1306). |
| 2 | Current state analysis is current | PASS | F0-14, F0-15 and F0-16 fixes keep code facts tagged by source (:163, :174, :555, :538); 9.3 stale-doc rows (:1618-1623) route stale docs to current captures. |
| 3 | Options are genuinely distinct | PASS | A1-A4 unchanged by the fixes; A4 still rejected on code evidence (:848, :1166). |
| 4 | Recommendation follows from analysis | PASS | §7 A1, Section 8 builds A1 only (five-check table above). |
| 5 | Implementation plan is actionable | **FAIL** | N1: a developer building `classify` from step 1.3 gets two incompatible outcomes for a live blocked contract under `ask the coordinator`. N3: the safe-to-close data-loss guard has no test. N4: rollback misses one edit. |
| 6 | Gaps are honest | PASS | 9.2 rows 81a-81d (:1607-1610) and 9.4 rows 98a-98c (:1640-1642) name what is not captured and give working defaults; step 1.3 prints "could not determine" where evidence is missing. |
| 7 | External research is relevant | PASS | 9.4 rows 94-98 (:1635-1639): external sources resolved as "codebase wins"; Grafana no-data rejected against WC-10. |
| 8 | Scale claims are substantiated | PASS | Step 1.4 bounds (50 `worker-show` calls, 90 s) are labelled proposed values, open until one measured sweep (9.1 row 63 :1577); `--include-remote` cost left open until measured (:1220). |
| 9 | Risk assessment is complete | **FAIL** | N3 (data-loss guard untested) and N4 (rollback incomplete) are risk-coverage gaps created by the F0-11/F0-19 and F0-20 fixes. |
| 10 | Evidence trail is complete | PASS (report-internal) | New fix text cites sources (`WORKER-CONTRACT.md:54-55`, `:108`, `:125`, `:133-136`; `seed-brief.md:60`, `:68`; `495eb96d:.../DESIGN-CONTRACT.md:11`). Tracing each cited research file to code was the fidelity reviewer's job and was not repeated here. |
| 11 | No circular reasoning | PASS | Owner-decision rows (98a-98c) state working defaults as plan choices, not as evidence; resolutions cite source files, not the report's own synthesis (for example the [CONTRADICTION] resolution P6-01 at :1584 cites `sc-swarm-wizard-protocol/SKILL.md:7`). |
| 12 | Conclusion is proportionate | PASS | Recommendation stays conditional on owner decisions (step 1.0b, 9.1, 9.4); `exited` and fencing rules are built against synthetic fixtures and labelled [UNVERIFIED] (:1219). |

## Summary

- Checks passed: 10 / 12
- Checks failed: 2 (items 5 and 9)
- Critical issues: 0 new (F0-11, the only CRITICAL, is resolved in text; its test gap is N3, graded IMPORTANT)
- Important issues open: 4 (N1, N2, N3, N4)
- Minor notes: 6
- Issues fixed in-place: 0 (fix authorization false)
- Issue count versus the previous cycle: 21 blocking before, 4 blocking now (decreasing).

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|-------------|
| N1 | IMPORTANT (contradiction; F0-01 incomplete) | Report step 1.3 (:1219), step 1.8 (:1229), :113, diagram :371-374 | The F0-01 fix makes rule 1 skip a blocked contract on a live, unsettled row whose brief says `ask the coordinator` ("working (rule 5) or could not determine (rule 7)"). In the same step, rule 4 still catches that row: (4a) "`return-contract.yaml` `worker_status: blocked` with `blocked_question`" gives waiting on a person (a), with no "no earlier match" qualifier; (4b-contract) "frozen when the latest implement `return-contract.yaml` has `worker_status: blocked`" gives (b). The GQ-96 sentence says without condition "a blocked implement contract gets class waiting on a person (a) from rule 1", and the step 1.8 fixture asserts the same for every blocked implement contract, while the rule 1 fixture in the same row asserts "not waiting on a person" for the live `ask the coordinator` case. Rules 1, 4 and the two fixtures cannot all hold. | In step 1.3, state that the `ask the coordinator` skip covers the contract half of 4a and 4b-contract as well (or that rule 4's contract sub-cases apply only when rule 1 would have applied). Make the GQ-96 sentence and the step 1.8 implement-contract fixture conditional on a settled row or `report blocked`. Align :113 and :371-374 with the same wording. |
| N2 | IMPORTANT (contradiction; F0-17 incomplete) | Report 8.2 row "S9 rows 7, 8, 9, 30, 51, 53" (:1409) | The row still lists "report person-started sessions (G6)" as an owner decision, says "step 1.0b asks for all six" and lists "WC-14 G6 wording" among what it blocks. §7 (:1071) says five owner decisions with GQ-09 settled; step 1.0b (:1211) says GQ-09 "is not asked"; 8.1 (:1319, :1389), 9.1 row 7 (:1520), 9.2 row 66 (:1591) and 9.5 row 106 (:1655) all say GQ-09 is settled by the sources. | Drop row 7 and G6 from the :1409 row (row label "S9 rows 8, 9, 30, 51, 53"), change "all six" to "all five", and remove "WC-14 G6 wording" from its Blocks column. |
| N3 | IMPORTANT (omission introduced by the F0-11/F0-19 fix; data-loss guard untested) | Report step 1.9 (:1230), step 1.8 (:1229) | The CRITICAL fix F0-11 and the F0-19 fix add two worktree-removable conditions (unpushed commits from `git status --branch --porcelain`; untracked or unstaged `.dev/tasks/` path from `git status --porcelain -- .dev/tasks`), and step 1.2 adds `unpushed` and `dev_tasks_unsaved`. Step 1.9 tests safe-to-close only "for each of the five `:108` conditions and the `:133-136` freeze"; step 1.8 adds no `patch_git` fixture for either new condition. The guard that prevents losing unpushed work and `.dev/tasks/` content has no test. | Add to step 1.8 `patch_git` fixtures: a branch with no upstream, a branch ahead of upstream, an untracked path under `.dev/tasks/` and an unstaged path under `.dev/tasks/`. Add to step 1.9 one safe-to-close case per fixture, each asserting "worktree removable: no" with the condition named, plus a `None` (could not determine) case when the git call fails. |
| N4 | IMPORTANT (omission introduced by the F0-20 fix) | Report Rollback table, "Four registries" row (:1287); rationale :1279 | The F0-20 fix adds step 1.21(b), an "Orca coordination" bullet in HOW-WE-WORK saying the coordinator runs `/sc:sweep` (and the never-as-worker bullet, :403). The rollback row reverts only the "Other commands" row, `_POST_REFRESH_ADDITIONS`, `_OTHER_COMMANDS` and the plugin byte copy. A rollback would leave the guide telling coordinators to run a removed command, which the rollback rationale at :1279 says is wrong. | Add the step 1.21(b) "Orca coordination" bullet (and the never-as-worker bullet if it names `/sc:sweep`) to the "Four registries" rollback row, and note that the plugin byte copy is re-copied after that revert too. |
| M1 | MINOR | :283 | A dangling "It" after the F0-10 [CONTRADICTION] insertion now has no clear antecedent. | Name the subject ("The seed brief ..."). |
| M2 | MINOR | :903 | The K-1 note says "the K-4 tests prove read-only"; the read-only proofs are steps 1.10/1.11 (K-1). | Change K-4 to K-1 or to steps 1.10-1.11. |
| M3 | MINOR | :908 | A prose line splits the constraints table, so K-5 and K-6 render outside it. | Move the prose line below K-6. |
| M4 | MINOR | :336 versus :167, :538 | :336 marks the reuse judgements [UNVERIFIED] while :167 and K2 (:538) state them as fact; 7.1, 8.2 and 9.1 row 15 agree with each other. | Use one label for the reuse judgement in all three places. |
| M5 | MINOR | :440 | The WC-14 G7 "under `.dev/`" note from the consolidated findings is unchanged (not rechecked; minor). | None required. |
| M6 | MINOR | :1343 | Cites `CR-01:12-21`; the fix log cited `:3`; row 57 cites both. | None required; both ranges are consistent. |

## Actions Taken

None. Fix authorization is false; the report was not edited.

## Self-Audit

**(a) Reliance list (rf-qa PASS items skipped for structural re-check):**
- No `## Inherited Structural Verdict` block was supplied. I relied on the fix log's statement that each F0 edit was applied and on `qa-fidelity-consolidated-findings.md` for each finding's original severity and required fix. I re-read every claimed fix location in the report myself and did not take the fix log's FIXED status as proof.
- I did not repeat the fidelity reviewer's tracing from research files to code (item 10). The source line citations in the new text were checked only for internal consistency.

**(b) Independent semantic checks (at least 1 required, INV-019):**
- Rule 1 versus rule 4 cross-read inside step 1.3: Read of report :1218-1230 this pass. Rule 1 has the `ask the coordinator` skip, rule 4a's contract half and 4b-contract do not, and the step 1.8 implement-contract fixture contradicts the rule 1 fixture in the same row. This gives N1. The fix log reported F0-01 as FIXED.
- 8.2 owner-decision row versus step 1.0b and §7: Read of :1409, compared with :1071, :1211, :1520 and 9.2 row 66 / 9.5 row 106 (Read :1576-1735). This gives N2.
- F0-11/F0-19 fix text versus the test plan: Grep for `five \`:108\` conditions|--branch --porcelain|git status --porcelain -- .dev/tasks` found the conditions at :407-408 and :1219 but only the five `:108` conditions at :1230. This gives N3.
- F0-20 edit versus the rollback table: Grep `Four registries` found :1287. Compared with steps 1.21(b) and 1.23 and the rationale at :1279. This gives N4.
- WC-10 sweep across the remaining window: 9.2 rows 68, 70, 80, 81; 9.4 rows 95-98 (:1593-1639). Every absent signal maps to could not determine. PASS.
- Second [CONTRADICTION] pair located at :1580-1584 (allowed-tools colon form versus space form). It is kept for the record with resolution P6-01 citing precedents. PASS.

**Questions:**
1. Factual claims checked independently: about 60 report locations, cross-read for consistency against each other and against the fix log's stated edits. No source code was read: the review is report-internal coherence by design, and code fidelity belongs to the fidelity reviewer.
2. Files read: the report (windows 1-664, 766-1735, plus targeted re-reads at :1218-1230 and :1409), `qa/qa-fidelity-consolidated-findings.md`, `qa/qa-fidelity-fix-log.md`.
3. Not applicable: 4 blocking and 6 minor findings were found.
4. No web research was performed. Tavily was not attempted and no fallback was used.

**Limitation:** report lines about 664-766 (Sections 5.1-5.4, external findings) were not read in this pass. The fix log lists no F0 edit there; the nearest fixed locations, :776 (F0-21) and :825 (F0-08), were read. A contradiction between 5.1-5.4 and a fixed section cannot be fully excluded.

## Confidence

- **Confidence:** Verified: 11/12 | Unverifiable: 1 | Unchecked: 0 | Confidence: 100.0%
  - Unverifiable: item 10, tracing research files to code. It is outside this review's scope (report-internal coherence), the report was not to be edited, and it belongs to the source-fidelity reviewer. The report-internal half of item 10 was checked.
- **Tool engagement:** Read: 19 | Grep: 3 | Glob: 0 | Bash: 0
  - The total (22) is above the checklist total (12).

## Recommendations

- Apply the fixes for N1-N4 (all report-text edits), then run one more qualitative verification. Under the fix-cycle limit that is the last review (cycle 2) before the open blocking findings go to the user.
- N1 is the most important: it decides the class a live blocked worker gets, and the plan currently gives two answers.

## Verdict: FAIL

Open blocking: 4 (N1, N2, N3, N4).

## QA Complete
