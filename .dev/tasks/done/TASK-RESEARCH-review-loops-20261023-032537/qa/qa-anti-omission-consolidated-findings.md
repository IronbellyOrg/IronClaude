# QA Report: Phase 6 Anti-Omission Consolidated Findings

**Topic:** Repeated review failures after fixes in `/sc:workflow` plans and `/sc:implement` tasks
**Date:** 2026-10-24
**Task step:** Step 6.38, Consolidate exhaustive omission findings (`TASK-RESEARCH-review-loops-20261023-032537.md:525-527`)
**Phase:** Phase 6 anti-omission gate (Gate 5), consolidation
**Anti-omission cycle:** 0
**Fix cycle:** N/A (report-only consolidation)
**Report under review:** `RESEARCH-REPORT-review-loops.md`. I read all 1,313 lines. I re-measured its sha256 at the end of this step: `a10cef088fb1be687fc65a72553910a8a522b4ef8eccb8081e4e2e48972469c7`, which is unchanged.
**Path convention:** paths are relative to `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/`. "Report:N" means a line of the final report.
**Governing sources read:**
- `/config/.claude/skills/tech-research/SKILL.md`: Gate 5 at :411-415, and the Anti-Omission Agent Prompt and output format at :1196-1239.
- `/config/.claude/skills/task/SKILL.md`: Standard QA Report Output Format at :466-506.
- `BUILD-REQUEST.md`: lines 1-56.
- `phase-outputs/discovery/anti-omission-input-map.md`: lines 1-223.
- All four `qa/qa-anti-omission-report-{1,2,3,4}.md` reports, in full.

**Method:**
- Every proposed omission was re-read at its cited source lines.
- Absence from the report was confirmed by reading the full report and by a fixed-string search of the report for each omission's distinctive wording.
- Where Partition 3's own inputs restate content, they were read directly: `research/evidence-deck.md:424-578` and `:700-721`.
- Rubric clause differences were checked mechanically against `research/historical-review-rules.json` lines 11 and 19.
- Reviewer table rows were counted mechanically.
- No package file was edited, no Git command was run and no session `.jsonl` was opened.

## Overall Verdict

Verdict: FAIL

**Why it fails:**
- **Real omissions remain.** 34 verified omissions must be recovered into the report: 4 IMPORTANT and 30 MINOR. A further 2 proposed omissions are covered by an explicit, reasoned exclusion already in the report.
- **One reviewer pass is not valid.** The Partition 3 review does not meet the requirement to enumerate "EVERY distinct claim … no sampling":
  - its stated counts do not reconcile with its own table;
  - its PASS is contradicted by its own inputs.
- **Partition 3 has no valid exhaustive pass.** The gate's "no missing reviewer passes" condition is therefore not met.

## Coverage and Reconciliation

**Expected and actual reports: 4 of 4 present.**

| Partition | Assigned inputs (map) | Report file | Reviewer verdict | Stated enumeration | Rows counted mechanically | Represented | Covered-by-dedup | Omitted | Arithmetic | Consolidated verdict |
|---|---|---|---|---:|---:|---:|---:|---:|---|---|
| 1. Screening, rule map, recovered sources | 14 files, 2,062 lines (map:24-44) | `qa/qa-anti-omission-report-1.md` | FAIL | 224 | 224 (155/50/22 hits, less one summary header row each) | 154 | 49 | 21 (3 IMPORTANT, 18 MINOR) | 154+49+21=224; per-file table sums verified | FAIL. Adjudicated: R 154, D 51, O 19 (O-08 and O-14 reclassified to dedup) |
| 2. Six case reports and raw captures | 8 files, 4,188 lines (map:46-60) | `qa/qa-anti-omission-report-2.md` | FAIL | 295 | 295 (225 R, 56 C, 14 O) | 225 | 56 | 14 (1 IMPORTANT, 13 MINOR) | 225+56+14=295; per-case sums verified | FAIL |
| 3. Evidence deck and synth-01 to synth-03 | 5 files, 1,524 lines (map:62-73) | `qa/qa-anti-omission-report-3.md` | PASS | 72 families | 85 rows (A-H 56; I-L 29) | 65 stated; 78 by rows | 7 | 0 | Does NOT reconcile: 85 rows are listed, but the summary says 72 (Report-3:167-171) | FAIL. The PASS is not accepted (see Reviewer Exhaustiveness) |
| 4. Later synthesis, cards, debate results, gaps | 26 files, 6,737 lines (map:75-103) | `qa/qa-anti-omission-report-4.md` | FAIL | 406 | 406 (383 REP, 20 DEDUP, 3 OMIT) | 383 | 20 | 3 (1 IMPORTANT, 2 MINOR) | 383+20+3=406; section table verified | FAIL |

Inputs covered by the four partitions total 53 files. That matches map:181-186: none unassigned and none assigned twice. Every reviewer read the full report and re-verified its hash. Partition 2 also re-verified the hash at 17:12Z.

**Proposed omissions:**
- 38 omissions were proposed in total: 21 from P1, 14 from P2, 0 from P3 and 3 from P4.
- Merges across partitions:
  - P4 #2 merged into O-01 and O-02, whose origin is P1 #20 and #19.
  - P4 #3 merged into O-30, whose origin is P2 #9.
- That leaves 36 unique omissions:
  - 34 RECOVER, 2 DEDUP, 0 OUT-OF-SCOPE;
  - by severity, 4 IMPORTANT (O-01, O-02, O-04, O-05) and 32 MINOR.

**Dispositions by partition** (the full per-row dispositions and report locations are in each reviewer's enumeration table):

- **P1.** Enumeration is at Report-1:42-267 and omissions at :269-293.
  - Represented: items 001-224 marked R (154).
  - Dedup (49): the reviewer's D rows. Items 023, 042, 046, 189, 198, 201 and 205 rest on the report's disclosed exclusions at Report:277-278. I ratify those as valid.
  - Omitted: items 006, 026, 038, 067, 094-096, 107, 124, 127, 129, 130, 134, 139, 142, 179, 183, 184, 209, 210 and 223.
  - Adjudication: items 038 and 124 are reclassified to dedup as O-08 and O-14.
- **P2.** Enumeration is at Report-2:22-349 and omissions at :351-368.
  - Represented: 225. Dedup: 56.
  - Rows 252 and 287 (case-level remediation recommendations) are out of scope under `BUILD-REQUEST.md:14,35,50`. I ratify that.
  - Omitted: rows 21, 33, 43, 51, 117, 164, 177, 180, 205, 212, 226, 248, 263 and 280.
- **P3.** Enumeration is at Report-3:10-155.
  - 78 family rows are marked represented and 7 dedup (B1, E2, F2, F5, F6, F7 and G5).
  - The H5 REPRESENTED row and the F2, F5 and F6 DEDUP rows are contradicted by evidence-deck rows (see the Cycle-0 FAIL Set).
  - No P3 row is accepted for the cycle-0 PASS set.
- **P4.** Enumeration is at Report-4:25-526 and omissions at :528-534.
  - Represented: 383. Dedup: 20.
  - Omitted: D20, F08 and F11.
  - I ratify P4's stated judgment calls:
    - L08 dedup.
    - R06, R08, R11 and Q07 dedup under Report:279's reasoned exclusion of historical producer recovery errors.
    - A69, A95 and A96: deliberate Step 6.18 revisions recorded at Report:612 and 1290, treated as represented.

**Known user-accepted defects excluded:** J1 (Report:5, 1235, 1287), L1, L2 (P2 row 279) and L3 (Report:848), per map:17-21. None of O-01 to O-36 is one of them.

**Historical limitations preserved:**
- The recoveries add limitations and do not remove or weaken any. O-13, O-17, O-18, O-26, O-31 and O-33 are limitation or boundary recoveries.
- Every recovery targets the final report only. No historical ledger, log, fixture, capture or source file is to be changed (Report:906; `BUILD-REQUEST.md:35`).

## Reviewer Exhaustiveness

| Reviewer | Exhaustive item-level enumeration? | Evidence | Finding |
|---|---|---|---|
| P1 | Yes | 224 item rows across all 14 files. Raw captures were mapped by reading. Provenance-only ranges were declared (Report-1:29-33). Hashes were grouped one item per file, which was disclosed. | Valid pass. One inconsistency: the reviewer's own disclosed-exclusion rule (Report-1:35) was not applied to items 038 and 124. I resolve that as O-08 and O-14 below. That is not a defect, because the template says "when in doubt, FLAG". |
| P2 | Yes | 295 item rows. The raw captures were diffed against their mapped segments, and raw-only substance was enumerated (rows 68, 107, 196, 254, 295). Absence keyword searches were recorded (Report-2:396-399). | Valid pass. |
| P3 | **No** | See the process findings below. | **Process finding PF-01 (IMPORTANT) and PF-02 (MINOR). The pass is not valid; its PASS verdict is rejected.** |
| P4 | Yes | 406 item rows. Variants were confirmed verbatim against the cards (`grep -v -x -F`). Scores were cross-checked with jq. Absence greps were recorded (Report-4:583-588). | Valid pass. |

**PF-01: P3 does not meet "EVERY distinct claim … no sampling".** It fails on four counts:
1. **It enumerated families, not items.** It bundled tens of deck rows into seven dedup families (Report-3:167). The task requires item-level enumeration (Step 6.36; SKILL.md:1218 "list them, do not sample").
2. **Its counts do not reconcile.** The table lists 85 rows (A1-A8, B1-B4, C1-C4, D1-D12, E1-E4, F1-F8, G1-G5, H1-H11, I1-I9, J1-J6, K1-K6, L1-L8). Its own summary lists exactly these ranges but states 72, and states 65 represented against 78 by row count (Report-3:167-171).
3. **Its PASS is contradicted by its own inputs.**
   - It marked H5 REPRESENTED. But `research/evidence-deck.md:707-708` states the rubric clause content ("Missing, stale or unverifiable evidence is issues" versus "Moved line number alone is not issues … Acceptance-recording rules also change"), and the report never states it (O-01, O-02).
   - Its dedup bundles absorbed deck rows whose meaning the report lacks: deck:431 (O-23), :446 (O-25), :452 (O-05), :507 (O-28), :510 (O-29), :533 (O-31), :542 and :549 (O-30), and :548 (O-32).
4. **It misdescribes a finding.** F2 calls the annotated-tag item "withdrawn" (Report-3:74). Deck:452 classifies it as "Preexisting inherited source contradiction".

**PF-02: wrong date on the P3 report.** It is dated 2026-10-25 (Report-3:5). The task log records its completion and persistence at `[2026-10-24T17:18Z]` (task file :681). The other three reports and this gate are dated 2026-10-24.

**Consequence:** content found only in Partition 3 inputs (deck-only matrices, synth-01 to synth-03 and web-01) has no valid exhaustive review. The omissions above were caught only because other partitions restate the same families. A fresh item-level pass over Partition 3 is required before the gate can pass.

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | All four expected reports exist and match their map partitions | PASS | `qa/qa-anti-omission-report-{1,2,3,4}.md` were each read in full. The input lists match map:24-103. |
| 2 | Report identity unchanged across the gate | PASS | sha256 `a10cef08…` was re-measured at this step, equal to map:5 and to each report's header. |
| 3 | P1 enumeration exhaustive and counts reconcile | PASS | Mechanical row counts: 154/49/21. The per-file table sums to 224 (Report-1:302-317). |
| 4 | P2 enumeration exhaustive and counts reconcile | PASS | Mechanical row counts: 225/56/14. Per-case sums verified (Report-2:372-380). |
| 5 | P3 enumeration exhaustive and counts reconcile | FAIL | PF-01: 85 rows against 72 stated; family bundling; PASS contradicted by deck:431, 446, 452, 507, 510, 533, 542, 548, 549 and 707-708. |
| 6 | P3 report metadata accurate | FAIL | PF-02: dated 2026-10-25 against task log :681. |
| 7 | P4 enumeration exhaustive and counts reconcile | PASS | Mechanical row counts: 383/20/3. Section table verified (Report-4:542-563). |
| 8 | Each proposed omission confirmed against its cited source lines | PASS | All 38 were re-read at their cited source lines (research-notes:30; input-inventory:45,79,83; scope-01-recovered:58,62; screening-handoffs-source:94-196,378; scope-03-recovered:13,40-75,104,156-180; scope-rules:32,41,70-71; historical-review-rules.json:11,19; 01:208,222,259,290,298-299; 03:104,142; 04:256,351,354,524-525,547-559; 05:58,131,135,145-146,156,169-171,238-250,294,413-448; 06:76,299-301; hypothesis-01:142; hypothesis-03:57,59; merged-root-cause-analysis:73,77). Every source statement exists as described. |
| 9 | Each proposed omission confirmed absent from the report | PASS | Full report read, plus a fixed-string search. Each of these returned 0 hits: "task-research folder", "secret", "scratch-test", "204721", "leave every other step", "PR CI", "originating tests", "185406", "skipped on purpose", "1759", "11,215", "hash-pinned", "deletes only", "precedence", "operator-supplied", "stale evidence", "acceptance handling", "E-RESUME", "annotated", "object.url", "field 9", "underspecif", "same result as", "187-195", "necessary deviation", "angle", "any severity", "case-insensitive", "carriage", "trailing newline", "record 396", "extras" and "deferred or absent". The 4 hits for "immutab" are unrelated (Report:197, 484, 1089, 1198). |
| 10 | Rubric clause differences verified mechanically | PASS | Line 11 (earlier load): "Never 2+ reviewer agents per task" 1, "MUST NOT write" 1, "E-RESUME-NEEDED" 0, "subagent mode" 0, "troubleshoot" 0, "moved line number alone" 0. Line 19 (later load): "One reviewer per review; never 2+ reviewer agents for …", "E-RESUME-NEEDED" 1, "subagent mode" 1, "troubleshoot" 2, "moved line number alone" 1. |
| 11 | Cross-partition duplicates merged, keeping the originating partition and the higher severity | PASS | P4 #2 merged into O-01 and O-02 (origin P1, IMPORTANT). P4 #3 merged into O-30 (origin P2, MINOR). The P2 #14 regeneration clause is linked to O-04. |
| 12 | Every proposed omission has a recovery or an evidence-backed dedup or out-of-scope rationale | PASS | Issues Found table: 34 RECOVER with exact text, source and target; 2 DEDUP citing Report:279 and `BUILD-REQUEST.md:35`. |
| 13 | Out-of-scope decisions cite the authoritative request | PASS | P2 rows 252 and 287 cite `BUILD-REQUEST.md:14,35`, which this gate confirms. No new out-of-scope disposition was made here. |
| 14 | Known accepted defects J1 and L1-L3 not counted | PASS | None of O-01 to O-36 is J1 or L1-L3. P2 row 279 notes L2 without counting it. |
| 15 | No fabricated or quota findings | PASS | Every O-ID is a verified source statement absent from the report. No omission was invented to reach a count. P3's zero result was rejected on evidence, not on a quota. |
| 16 | Recoveries that could change a ranked cause or the ranking are flagged | PASS | See the Rank impact column. The debated variants already carry O-01, O-30 and O-36 content: `variant-3-original.md` "stale evidence as issues" 1 and "any defect of any severity" 1; `variant-1-original.md` "deferred or absent" 1. O-04, O-05, O-25, O-28 and O-29 would be undebated evidence if placed in Option Support rows, and are flagged. |
| 17 | Historical limitations preserved and no historical artifact edited | PASS | All recoveries target the report only. The recovered items add limits (O-13, O-17, O-18, O-26, O-31, O-33). |
| 18 | Final report free of genuine omissions | FAIL | 34 RECOVER items (4 IMPORTANT, 30 MINOR). |

## Summary

- Checks passed: 15 of 18
- Checks failed: 3 (checks 5, 6 and 18)
- Critical issues: 0
- Important issues: 5 (O-01, O-02, O-04, O-05 and process finding PF-01)
- Minor issues: 31 (30 RECOVER omissions plus PF-02)
- Adjudicated as covered by dedup: 2 (O-08, O-14)
- Issues fixed in-place: 0 (report-only; fix authorization false)

## Issues Found

| ID | Severity | Partitions | Source path:line | Omitted meaning | Disposition (RECOVER/DEDUP/OUT-OF-SCOPE) | Recovery text or rationale | Rank impact |
|---|---|---|---|---|---|---|---|
| O-01 | IMPORTANT | P1 #20 (originating), P4 #2; restated in the P3 input deck:707 | `research/scope-rules.md:70-71`; `research/historical-review-rules.json:11,19`; `synthesis/hypothesis-03.md:57`; `reviews/adversarial/merged-root-cause-analysis.md:73`; `research/evidence-deck.md:707-708` | What the FINAL evidence clause said in each load. The report says only that the rubrics are "materially different" (Report:229) and confounded (Report:134, 170, 948). | RECOVER | In Section 2.3 after "load materially different rubrics" (Report:229), and in Option C Support after "Two different rubric texts" (Report:577), add: "The two captured texts differ in substance. The earlier load (20:26:30.085Z, `0b533765…`, captured qa.md:79) makes missing, stale or unverifiable evidence an `issues` result. The later load (20:32:19.277Z, `faff03b7…`, captured :82) takes FINAL evidence from current files and `./artifacts/` logs rather than ledger citations, states that a moved line number alone is never `issues`, and checks user-accepted gaps against their recorded scope. The second FINAL, which rejected the blank Task 10 token, ran under the earlier text; the passing third FINAL ran under the later one (`research/scope-rules.md:70-71`; `research/historical-review-rules.json`; `research/evidence-deck.md:707-708`)." In Option D Evidence strength (Report:609), add one clause pointing to this contrast as the policy side of the confounding. | No rank change expected. `variant-3-original.md` already states this difference (verified), so the debate weighed it, and recovery restores card content. It changes assertions in 2.3 and Options C and D, so the affected prior report and fidelity checks must be rerun (Step 6.39). |
| O-02 | IMPORTANT | P1 #19 (originating), P4 #2 ("changes acceptance handling"); restated in the P3 input deck:708 | `research/scope-rules.md:70-71`; `research/historical-review-rules.json:11,19`; `research/evidence-deck.md:708` | Ruling authorship changed between the second and third FINAL. The report records only that the ruling record is missing (Report:170, 348, 893). | RECOVER | In Section 2.3 (Report:229), Option C Support (Report:577) and the Section 8 step 3.5 Details (Report:893), add: "The earlier load forbids the executor from writing a Ruling and requires an operator-supplied record (captured qa.md:65). The later load lets the executor record a clearly confirmed, scoped user acceptance with its provenance, keeping the noncompliant verdict (captured :66-68). The ruling-record requirement a reviewer applied therefore depends on which load it received (`research/scope-rules.md:70-71`; `research/evidence-deck.md:708`)." | No rank change. Same basis as O-01 (deck and card content). It changes an assertion in 2.3 and step 3.5, so affected checks need a rerun. |
| O-03 | MINOR | P1 #21 | `research/historical-review-rules.json:11,19` | Other clause differences between the two loads, absent from the report. | RECOVER | After the O-01 and O-02 text in Section 2.3, add: "The later load also changes 'never 2+ reviewer agents per task' to 'one reviewer per review', ties E-HALT-QA to the retry ladder's terminal halt, adds E-RESUME-NEEDED, keeps a run in subagent mode once it switches, always uses subagents for re-run and operator reviews, and bars reviewers from the retry and troubleshoot folders, with a citation into them yielding `cannot-verify`. The earlier load has none of these (`research/historical-review-rules.json` records.before and records.after; mechanically verified)." | None. Descriptive rubric history. |
| O-04 | IMPORTANT | P1 #11 (originating), P2 #14 third clause | `research/scope-03-recovered.md:71-75,92,131` (= `research/screening-recovery-source.txt:663-673`); `research/06-session-0690ee9f.md:301` | The selected credential follow-up incident executed a regenerated plan whose own pre-execution review was skipped on purpose, after the previous plan failed review. Report:1064 keeps only the missing-report fact. | RECOVER | In the 2.2 credential row (Report:170) and the 2.6 credential row's exclusion cell (Report:276), add: "The follow-up package executed a regenerated plan. The first follow-up plan `TASK-WF-issue358FollowUp-20261022-185406` failed its plan review (record 762: 'isn't safe to run'). The user said 'regenerate' (764). The replacement `…-193837` passed its format check, but 'its own review was skipped on purpose' (817) before implementation began (818). This is a planning observation, not another implementation retry (`research/scope-03-recovered.md:71-75,92,131`; `research/06-session-0690ee9f.md:301`)." | None if kept in 2.2 and 2.6. It is not in any debated card; adding it to an Option Support row would be undebated evidence and needs a user decision. |
| O-05 | IMPORTANT | P2 #1 (originating); restated in the P3 input deck:452 | `research/01-session-ac2cd1fd.md:259,298`; `research/evidence-deck.md:452` | A third Orca source tension: following the annotated-tag `object.url` (Source:158) against check-before-use (Source:469). The report says "both" tensions (Report:901, 950) and lists two (Report:255-256). | RECOVER | Add a Section 2.5 row after Report:256: "[CONTRADICTION: Orca source tells the executor to follow an annotated tag's upstream `object.url` (Source:158), while its rule requires upstream values to be checked before use (Source:469).] The targeted reviewer classed the resulting finding as pre-existing and inherited from the source, not a v3 regression. The v4 response (a 40-hex object digest and a fixed tag-object endpoint, Session:912) received no separate independent verification (`research/01-session-ac2cd1fd.md:259,298`; `research/evidence-deck.md:452`)." At Report:901 and Report:950, change "both" to name all three tensions. | Potential. This tension is absent from `synthesis/hypothesis-03.md:60` and the debated variant. Place it in 2.5, the Section 8 Constraints row and Q6 only, and state that it was not in the debated cards. Do not add it to Option C Support without a user decision. It changes the count assertion at Report:255-256, 901 and 950, so affected checks need a rerun. |
| O-06 | MINOR | P1 #1 | `research/research-notes.md:30` | No earlier task-research folder exists; retry-ladder designs are historical context only. | RECOVER | In the 10.2 research-notes row (Report:1043), add: "Scope discovery found no earlier task-research folder on this topic; existing retry-ladder designs are historical context, not a substitute for this investigation." | None |
| O-07 | MINOR | P1 #2 | `phase-outputs/discovery/input-inventory.md:45,79`; requirement `BUILD-REQUEST.md:50` | No excerpt exposes a secret value, which addresses the requested redaction. | RECOVER | In the 2.1 "Evidence delivery" row (Report:110), add: "No inventory excerpt exposes a secret value, and none was needed (`phase-outputs/discovery/input-inventory.md:45,79`)." | None |
| O-08 | MINOR | P1 #3 | `phase-outputs/discovery/input-inventory.md:83` | The first metadata-extraction command had a syntax error; the corrected command succeeded. | DEDUP | Intentional exclusion. This is a research-producer tool error recovered during discovery, not a review-loop finding. Report:279 explicitly excludes this class with a rationale ("Historical producer recovery errors and administrative gate narratives are not new empirical loop incidents"). The source file stays listed in the evidence trail (Report:1168) and on disk, which satisfies `BUILD-REQUEST.md:35` ("retain every intermediate"). This is consistent with P4's ratified dedup of the same class (R06, R08, R11, Q07). | None |
| O-09 | MINOR | P1 #4 | `research/scope-01-recovered.md:58,62` | Excluded session 02's interference context in the shared Orca worktree, during monitor Task 12. | RECOVER | In the 2.1 "Other controls" row (Report:107), add: "Excluded session 02 shares the Orca worktree with the monitor case: it records an accidental scratch-test commit into that worktree (record 460, traced to an inner heredoc at 1162) and another session changing `progress.md` at record 615 (2026-10-22T20:45:36Z), during the monitor Task 12 incident. This is interference context only, not a session-02 loop event; the monitor case analysis did not examine it." The last clause was verified: `research/05-session-e002bed2.md` has no match for "20:45:36" or "scratch-test". | None |
| O-10 | MINOR | P1 #5 | `research/screening-handoffs-source.txt:94,163,184,186,192` | Package lineage and overlap behind the Session 09 control. | RECOVER | In the 2.2 Session 09 control row (Report:182), add: "The overlapping writer was the documentation case's package `TASK-WF-issue358FollowUp-20261022-210638`, created in session 12; session 09 executed session 14's plan `TASK-WF-reviewAndPlanThe-20261022-204721`; session 11's overlap with session 10's package is the same overlap, counted once." | None |
| O-11 | MINOR | P1 #6 | `research/screening-handoffs-source.txt:120` | How Session 10 Task 4 converged: the measurable whole-file criterion outweighed "leave every other step unchanged". | RECOVER | In the Session 10 Task 4 control rows (Report:179, 782), add: "The first reviewer warned that the rewording could conflict with 'leave every other step unchanged'; the second accepted the one-comment change because the measurable whole-file criterion outweighs that general preservation wording." | None |
| O-12 | MINOR | P1 #7 | `research/screening-handoffs-source.txt:115-118,133`; `research/scope-02.md:18,28,44` | Session 10's separate Task 6 `cannot-verify` (needs PR CI), ruling and FINAL pass. | RECOVER | In the 2.2 Session 10 row (Report:179), add: "A separate CI-only Task 6 `cannot-verify` (record 1247) was stopped (1250), closed by a recorded ruling (1264) and a FINAL pass (1535); it is not joined to Task 4." | None |
| O-13 | MINOR | P1 #8 | `research/screening-handoffs-source.txt:378` | The originating tests of the mocked synthetic sessions were not traced. | RECOVER | In the 2.1 "Synthetic summaries" row (Report:106), add: "Their originating tests were not traced." | None |
| O-14 | MINOR | P1 #9 | `research/scope-03-recovered.md:13,176` (= `research/screening-recovery-source.txt:327,386`) | Two screening tool hiccups: wrong manifest location, then polluted extraction, both recovered. | DEDUP | Intentional exclusion, same class and rationale as O-08 (Report:279). The source itself records "no unresolved source-access blocker remains" (`research/scope-03-recovered.md:176`), and the file is listed at Report:1045. | None |
| O-15 | MINOR | P1 #10 | `research/scope-03-recovered.md:40-43,53`; `research/screening-recovery-source.txt:461,648-650` | Session 13's plan failed three acceptance checks, was corrected without semantic re-review, and became the initial credential package. | RECOVER | In the 7.7 Sessions 13/14 row (Report:785) and the initial-credential control rows (Report:178, 368), add: "The initial credential package's plan (`TASK-WF-issue358InTempla-20261022-151058`) first failed its plan review on three acceptance checks (one-key overwrite checks, any-one-name man-page check, missing README troubleshooting row); five changes were applied and only the format check reran." | None |
| O-16 | MINOR | P1 #12 | `research/scope-03-recovered.md:104`; `research/screening-recovery-source.txt:306` | Session 17's pre-second-FINAL fixes included making final review judge the current end state rather than moved line numbers alone. | RECOVER | In the Session 17 FINAL control rows (Report:181, 369), add: "Its repair also changed final review to judge the current end state rather than moved line numbers alone (record 1759). This is an observed event only." | None. Do not assert a link to the credential rubric change without load or commit evidence. |
| O-17 | MINOR | P1 #13 | `research/scope-03-recovered.md:156-162` | The archived roots and logs still existed at screening on 2026-10-23. | RECOVER | In the Option D Reuse row (Report:614), add: "On 2026-10-23 the historical archived roots still held `t3-markdownlint.log` (1,222 bytes), the retry-ladder `t8-test.log` (11,215 bytes) and the ledgers at their recorded lines; by 2026-10-24 the recorded worktree was gone. The candidate current log matches the earlier size only, not a hash." | None |
| O-18 | MINOR | P1 #14 | `research/scope-03-recovered.md:171` | The Sessions 13/14 and follow-up pre-review reports were linked, not fully read. | RECOVER | In the limit cell of the 7.7 Sessions 13/14 row (Report:785), add: "their workflow review reports and the follow-up pre-review were linked from actual events but not fully read at screening." | None |
| O-19 | MINOR | P1 #15 | `research/scope-03-recovered.md:180` | A naming paragraph was deliberately left hash-pinned after a fix (historical evidence staleness). | RECOVER | In the 2.5 historical-positions row (Report:261), add: "A source-design naming paragraph was intentionally left pinned to its old hash after a fix; this is historical evidence staleness, not a current documentation defect." | None |
| O-20 | MINOR | P1 #16 | `research/scope-rules.md:32` | `quality-gates.md:41`: a failed generation gate stops and deletes only its own draft. | RECOVER | In the 2.3 plan-generation row (Report:193), add: "A failed generation gate stops and deletes only its own draft (`quality-gates.md:41`); this grants this research no deletion authority." | None |
| O-21 | MINOR | P1 #17 | `research/scope-rules.md:41` | `qa.md:27-33`: concrete evidence citations are required, and an absent citation becomes `cannot-verify`. | RECOVER | In the 2.3 per-task QA row (Report:194), add: "Each verdict needs concrete evidence citations; an absent citation becomes `cannot-verify` (`qa.md:27-33`)." | None |
| O-22 | MINOR | P1 #18 | `research/scope-rules.md:41` | `qa.md:37-52`: a closed per-task verdict set with a precedence order. | RECOVER | In the same row (Report:194), add: "Per-task verdicts form a closed set with a defined precedence (`qa.md:37-52`)." | None |
| O-23 | MINOR | P2 #2; restated in the P3 input deck:431 | `research/01-session-ac2cd1fd.md:208,299`; `research/evidence-deck.md:431` | The field-9 requirement (Requirements:302) is itself in tension with rollback. Provenance could be a defensible source if approved, but no such change was declared. | RECOVER | In Option B Support "Digest source" (Report:550) and Gap row 2 (Report:344), add: "The substitution changed the declared field-9 contract; the requirement itself defines field 9 from recipe state even though rollback can separate recipe and deployed-package state, and provenance might be a defensible source if explicitly approved (no such approval was declared)." | Qualifies one V2 support item without reclassifying it (case and deck keep it introduced). No rank change. |
| O-24 | MINOR | P2 #3 | `research/01-session-ac2cd1fd.md:188,290` | Continuation mechanism: later passes answered different questions; newly concrete interfaces exposed defects that were underspecified rather than wrong. | RECOVER | In the 2.2 Orca row classification (Report:165), add: "Corrections made collectors, regions, checks and ordering concrete, and later reviewers found defects in interfaces that had been underspecified rather than concretely wrong; this is kept separate from 'introduced' and 'old defect'." | None |
| O-25 | MINOR | P2 #4; restated in the P3 input deck:446 | `research/01-session-ac2cd1fd.md:222,389`; `research/evidence-deck.md:446` | N-17: v2 added "same result as base" checks with no baseline-capture task, an introduced acceptance-executability gap. | RECOVER | In Option B "Further introductions in the case report, not in the card's table" (Report:550), add: "and the v2 'same result as on the base commit' comparisons with no baseline-capture task (N-17)." | Adds an introduction in the Orca context, which V2 already counts. A-001 reach is unchanged. Not debated evidence; label it as a case-report addition, as Report:550 already does. |
| O-26 | MINOR | P2 #5 | `research/03-session-6f744b87.md:104,142` | The static evidence slice (187-195) was narrower than the 11-line insertion (186-196). | RECOVER | In the 2.2 documentation row (Report:167) or Option E Support (Report:628), add: "The static slice covered lines 187-195 of an 11-line insertion at 186-196, so even the static evidence was narrower than its 'added lines' description; this limits the log, it is not the cause." | None |
| O-27 | MINOR | P2 #6 | `research/04-session-43582de1.md:256` | The CI tooling-output exemption was an explicitly disclosed necessary deviation, not concealed scope expansion. | RECOVER | In the 2.2 CI row (Report:168) or Gap row 2 Notes (Report:344), add: "The tooling-output exemption was explicitly disclosed as a necessary deviation in the feedback and regenerated constraints; its defect is incomplete hash coverage, not concealed scope expansion." | None |
| O-28 | MINOR | P2 #7; restated in the P3 input deck:507 | `research/04-session-43582de1.md:351,524,547-559`; `research/evidence-deck.md:507` | D-007: the repair's new immutability promise is checked only by a decision-line count. | RECOVER | In the 2.2 CI row residuals (Report:168), add: "D-007: the repair prohibited later edits to the research file but checks immutability only by counting decision lines, a verification gap attached to the repair's new promise, neither a regression nor a pre-existing weakness." | CI context is already counted for V2. No rank change. Not debated evidence. |
| O-29 | MINOR | P2 #8; restated in the P3 input deck:510 | `research/04-session-43582de1.md:354,525`; `research/evidence-deck.md:510` | D-010: the "no `<` placeholder" wording ambiguity was introduced by the repair. | RECOVER | Beside O-28 (Report:168), add: "D-010: the repair introduced an ambiguous 'no `<` placeholder' check while resolving placeholders, a repair-era wording ambiguity with no runtime regression established." | Same as O-28. |
| O-30 | MINOR | P2 #9 (originating), P4 #3; restated in the P3 input deck:542, 549 | `research/05-session-e002bed2.md:58,132,135,145-146,156,238-250`; `synthesis/hypothesis-03.md:59`; `reviews/adversarial/merged-root-cause-analysis.md:77`; `research/evidence-deck.md:542,549` | The monitor review prompts made "any defect of any severity" noncompliant and told reviewers to judge every bullet directly. Findings mixed suggested-command exactness, cosmetics and case-insensitive keyword matching. | RECOVER | In Option C Support after "uncapped fields absent from the plan (records 906, 1143)" (Report:577), and in the 2.6 monitor row (Report:275), add: "and case-insensitive security-keyword matching that the written pattern did not clearly require; the per-review prompts made any defect of any severity noncompliant and told reviewers to judge every Task 12 bullet directly, so findings mixed requirement violations with exactness problems in commands the requirements suggested (the `git diff --name-only` rename overlap) and cosmetic output (unused `vhex()`, punctuation, grammar)." | None. `variant-3-original.md` already carries the any-severity rule (verified), so this restores debated content. |
| O-31 | MINOR | P2 #10; restated in the P3 input deck:533 | `research/05-session-e002bed2.md:131,294`; `research/evidence-deck.md:533` | The carriage-return quote-escape finding was reasoned, never rendered on GitHub. | RECOVER | In the 5.1 monitor runner row (Report:407) or Q8 (Report:952), add: "The carriage-return quote-escape finding was reasoned from formatting rules, not rendered on GitHub." | None |
| O-32 | MINOR | P2 #11; restated in the P3 input deck:548 | `research/05-session-e002bed2.md:166-171,445`; `research/evidence-deck.md:545-548` | The four accepted monitor defects are named only as a count (Report:736). The fourth (newline validators) is retained hardening, not a new vulnerability, with a reachability caveat. | RECOVER | In the 2.2 monitor row (Report:169), add: "The four accepted defects are the record-1240 findings: selected-release failure mislabeled as outage (preexisting cross-component), links-only fallback over the body limit (preexisting design gap), the error-trap contamination (proven introduced regression) and provenance validators accepting a trailing newline (retained or incomplete hardening, not a new vulnerability; not every cited validator is reachable, because command substitution strips trailing newlines)." | None |
| O-33 | MINOR | P2 #12 | `research/05-session-e002bed2.md:413-433,448` | Monitor Task 13's accepted gap: test rerun declined, `missing` kept, no re-review. The case cites it as further wording-expansion evidence. | RECOVER | In the 2.1 out-of-window note (Report:149) or the 2.6 monitor row (Report:275), add: "Task 13 (separate from Task 12 counts): verdicts `misunderstood` then `missing` although its 72-row acceptance test passed; the human requested a phrase repair and explicitly declined a test rerun, and the executor recorded acceptance with `missing` unchanged and no fresh re-review (records 1293-1371)." | None. Excluded from counts and the ranking, consistent with Report:149. |
| O-34 | MINOR | P2 #13 | `research/06-session-0690ee9f.md:76` (also `research/scope-03-recovered.md:65`) | The user explicitly reopened Task 3 evidence only (record 396) before the initial repair. | RECOVER | In the 2.2 credential row (Report:170) or Option D Support (Report:604), add: "The initial repair followed the user's explicit reopening of Task 3 evidence only (record 396)." | None |
| O-35 | MINOR | P2 #14 | `research/06-session-0690ee9f.md:299-301` | Credential count exclusions: expected negative test failures; the initial Task 1 unrelated-red "extras"; regeneration is not a retry. | RECOVER | In the 2.6 credential exclusion cell (Report:276), add: "Expected negative test failures are not loop failures, and the initial Task 1 unrelated-red 'extras' result is not a failed spec review." The regeneration clause is recovered once, under O-04. | None |
| O-36 | MINOR | P4 #1 | `synthesis/hypothesis-01.md:142` (verbatim in `reviews/adversarial/adversarial/variant-1-original.md`); `reviews/adversarial/adversarial/base-selection.md:233,546` | The V1 discriminating test's separate step: verify whether the relevant behavior test was deferred or absent. | RECOVER | In Option A Falsification (Report:527), 7.6 order 1 (Report:757) and the step 2.1 Action (Report:872), add after "run the check actually used against it": "and separately verify whether the relevant behavior test was deferred or absent (`synthesis/hypothesis-01.md:142`)." | None. The debated variant already carries this step (verified). It changes falsification text only. |

## Cycle-0 PASS Set

These are items an accepted reviewer verified as represented or legitimately deduped, adjudicated here:

- **P1:** 154 REPRESENTED items plus 51 COVERED-BY-DEDUP, as listed at Report-1:42-267:
  - the reviewer's 49 D rows;
  - O-08 (item 038) and O-14 (item 124), adjudicated dedup under Report:279.
- **P2:** 225 REPRESENTED plus 56 COVERED-BY-DEDUP rows (Report-2:22-349). This includes the out-of-scope remediation rows 252 and 287 under `BUILD-REQUEST.md:14,35`.
- **P4:** 383 REPRESENTED plus 20 COVERED-BY-DEDUP rows (Report-4:25-526). This includes:
  - the ratified judgment calls L08, R06, R08, R11, Q07, A69, A95 and A96;
  - all five hypotheses' mechanisms, support, counterevidence, alternatives, scope, falsification and limits;
  - the actual debate outcomes: V1 first 5/5; V3 above V2 3/5; V4 above V5 3/5, with V5 above V4 displayed on the 2/5 side (Report:675-708).
- **P3:** none accepted for cycle 0. Its 85 family rows remain provisional until an exhaustive item-level pass replaces them (PF-01).

## Cycle-0 FAIL Set

- **Omissions to recover (34):**
  - IMPORTANT: O-01, O-02, O-04 and O-05.
  - MINOR: O-03, O-06, O-07, O-09, O-10, O-11, O-12, O-13, O-15, O-16, O-17, O-18, O-19, O-20, O-21, O-22, O-23, O-24, O-25, O-26, O-27, O-28, O-29, O-30, O-31, O-32, O-33, O-34, O-35 and O-36.
- **Process findings (2):**
  - PF-01 (IMPORTANT): no valid exhaustive Partition 3 pass.
  - PF-02 (MINOR): P3 report date wrong.
- **Rejected P3 dispositions** (all contradicted by deck rows):
  - H5 REPRESENTED is contradicted by deck:707-708 (O-01, O-02).
  - F2 DEDUP is contradicted by deck:431, 446 and 452 (O-23, O-25, O-05).
  - F5 DEDUP is contradicted by deck:507 and 510 (O-28, O-29).
  - F6 DEDUP is contradicted by deck:533, 542, 548 and 549 (O-31, O-30, O-32).
- **Assertion changes that require reruns** (Step 6.39 "changed … assertions invalidate affected prior gates"):
  - O-01, O-02 and O-03 (Section 2.3, Options C and D, step 3.5);
  - O-05 (the "two/both Orca source tensions" statements at Report:255-256, 901 and 950);
  - O-23 (Option B support qualification).
  - The affected prior report-gate and fidelity checks must be rerun on actual evidence, not carried as stale PASS.
- **Ranking:** no recovery is expected to change a ranked cause or the displayed order V1 > V3 > V2 > V5 > V4, provided:
  - O-04 and O-05 are kept out of Option Support rows;
  - O-25, O-28 and O-29 are labelled as case-report additions the debate did not weigh.
  - Any placement that adds undebated evidence to a candidate's support is a user decision about rerunning the debate.

## QA Complete

| Status | Result |
|---|---|
| DONE | Read all four anti-omission reports, the input map, the build request, the governing templates and the full report (sha256 `a10cef08…`, unchanged). Re-read every proposed omission at its cited source lines and confirmed its absence from the report. |
| DONE | Consolidated 38 proposed omissions into 36 unique IDs: 34 RECOVER (4 IMPORTANT, 30 MINOR) and 2 DEDUP under Report:279. Each has exact recovery text, source and target, or an evidence-backed rationale, plus a rank-impact flag. |
| DONE | Rejected Partition 3's PASS. It enumerated families rather than items, its counts do not reconcile (85 rows against 72 stated), its own deck rows contradict it, and it is misdated. Verdict: FAIL. |
| NEXT | Step 6.39: one serialized rf-qa fixer recovers O-01 to O-36 (except the DEDUP items O-08 and O-14) into the report, keeping O-04 and O-05 out of Option Support rows. The parent must also run a fresh item-level Partition 3 anti-omission pass and rerun the prior report and fidelity checks affected by O-01, O-02, O-03, O-05 and O-23 before the Step 6.40-6.42 verification and gate. |

## Addendum: Partition 3 Rerun Reconciliation (2026-10-24)

**Inputs:**
- `qa/qa-anti-omission-report-3-rerun.md`, read in full (lines 1-259).
- `research/evidence-deck.md` lines 68-371 (D2 screened inventory, D3 deduplication, D4 chronologies), lines 424-578 (D6 matrices) and lines 700-721 and 812-890 (D10, D12, D13, D14, D15, D16).
- The final report, sha256 `a10cef088fb1be687fc65a72553910a8a522b4ef8eccb8081e4e2e48972469c7`, re-measured at this step and unchanged.

No file was edited, no Git command was run and no session `.jsonl` was opened.

### Rerun validity verdict

**The rerun counts as the item-level pass, but nine of its dispositions are overturned here.**

**What it does correctly:**
- It enumerates 290 items and its counts reconcile: 256 represented + 33 covered-by-dedup + 1 omitted = 290, and the block sum 17+7+20+107+14+20+13+20+11+34+24+3 = 290 was re-checked.
- It covers deck sections D1, D3 and D5-D15 row by row, all of web-01, and synth-01 to synth-03 by line diff. That fixes the counting and family-bundling failures recorded in PF-01.

**Where it falls short:**
1. **It did not enumerate D2 (deck:68-111) or D4 (deck:168-368).** I read both in full. Every row restates Partition 1 inputs (the 30 slots, already enumerated as P1 items 001-224) or Partition 2 inputs (the six case chronologies, already enumerated as P2 rows 1-295). None of them carries anything that exists only in the deck. For example, the "396 user reopens evidence" entry at deck:349 is already covered as O-34. So skipping them loses nothing.
2. **It did not enumerate D12 Key Takeaways (deck:816-823) or D16 Summary (deck:886-890).** I checked them:
   - D12 is represented almost word for word in the Section 5.3 table (Report:440-446).
   - D16 is represented at Report:118-121, 309 and 168-170.
   - No new omission results.
3. **New process finding PF-03 (IMPORTANT): wrong block-level dedup.** The rerun marked whole matrix ranges as dedup (E46-E75, E97-E114, E117-E138) and marked E207 as dedup. Of these, nine items are wrong when checked against the deck and report text (mapping table below). Two of them hide content behind IMPORTANT omissions: E207 (part of O-01) and the annotated-tag row (O-05). I adjudicate each one here. The other rows in those ranges restate case items that Partition 2 already judged item by item (R or C), so P2's judgments stand for them.

**Updated PF-01 consequence:**
- A valid exhaustive Partition 3 pass now exists. It is the rerun's 290-item enumeration, with the nine dispositions corrected below and the D2, D4, D12 and D16 coverage confirmed above.
- PF-01 stays on record against the original `qa/qa-anti-omission-report-3.md`. Its PASS remains a rejected historical result and is not rewritten.
- The gate condition "no missing reviewer passes" is now met.
- These adjudications were made by this consolidation context. They must be re-verified by the fresh verifiers at Steps 6.40 and 6.41.

### Mapping table

| Rerun item | O-ID | My adjudication | Evidence |
|---|---|---|---|
| O1 / E209: the revised rubric's "Acceptance-recording rules also change" (deck:708) | O-02 | **Agree: OMITTED, IMPORTANT.** It is the same omission as O-02, which also comes from P1 #19 and P4 #2. The rerun's O1 is merged into O-02 and keeps its originating partitions plus P3. | deck:708; `research/scope-rules.md:70-71` (captured qa.md:65 against :66-68). The phrases "acceptance handling" and "operator-supplied" each appear 0 times in the report. Report:348 and :893 treat the missing ruling line only as a bookkeeping gap. |
| E207: the earlier rubric's "missing, stale or unverifiable evidence is issues" (deck:707), rerun D | O-01 | **Disagree: OMITTED (IMPORTANT, part of O-01).** The rerun's equivalent, Report:196, is the *current* rule at commit `2165ae25`. Per Report:229, that commit carries the *later* `faff03b7` bytes. Report:229 itself says "a current file is still not itself a historical load". So the earlier load's content, which points the opposite way, is stated nowhere. | deck:707; `research/scope-rules.md:70`. The phrase "stale evidence" appears 0 times in the report. |
| E208: the revised rubric's moved-line-alone rule (deck:708), rerun R | O-01 | **Partly agree.** The clause does appear, but only as a current rule (Report:196, 584, 744). The report never says it differed between the second and third FINAL. That before-and-after contrast is what O-01 recovers. | Report:196, 229, 584. |
| E46-E75 row "lock digest → deployed-package provenance" (deck:431), rerun D | O-23 | **Disagree: RECOVER, MINOR.** The deck's limit column qualifies it: "Provenance might be a defensible approved design change, but no such change was declared." Option B Support (Report:550) cites the digest switch as introduction evidence without that qualification. | deck:431; `research/01-session-ac2cd1fd.md:208,299`. "Field 9" appears 0 times in the report. |
| E46-E75 row "base-result comparison lacks recorded baseline" (deck:446), rerun D | O-25 | **Disagree: RECOVER, MINOR.** Report:550 lists the "Further introductions in the case report" by name and leaves this one out. A named list like that reads as complete, so the gap is an omission, not compression. | deck:446; `research/01-session-ac2cd1fd.md:222`. "Same result as" appears 0 times. |
| E46-E75 row "annotated-tag URL followed unchecked" (deck:452), rerun D | O-05 | **Disagree: RECOVER, IMPORTANT.** The deck classes it as a "Preexisting inherited source contradiction". The report states there are "both" Orca source tensions (Report:901, 950) and lists only two (Report:255-256). The rerun's anchor, Report:523, is a different item: the validation-after-fetch defect N-01 at deck:435. | deck:452; `research/01-session-ac2cd1fd.md:259,298`. "Annotated" and "object.url" each appear 0 times. |
| E97-E114 row "research-file immutability not proved" (deck:507), rerun D | O-28 | **Disagree: RECOVER, MINOR.** It is a distinct causal class: a gap in checking the repair's own new promise. The CI row's named list of residual weaknesses (Report:168: serialization, render-output, status-normalization, reference-frame) leaves it out. | deck:507; `research/04-session-43582de1.md:524,547-559`. |
| E97-E114 row "angle-bracket check ambiguous" (deck:510), rerun D | O-29 | **Disagree: RECOVER, MINOR.** It is wording ambiguity introduced during the repair. Report:168 names dependency repointing as the only introduction. | deck:510; `research/04-session-43582de1.md:525`. "Angle" appears 0 times. |
| E117-E138 rows "capitalized security term" (deck:542) and "cosmetics and uncapped fields" (deck:549), rerun D | O-30 | **Disagree: RECOVER, MINOR.** Option C Support (Report:577) lists its broader-hardening examples and names only the uncapped fields. The "any defect of any severity" prompt rule comes from P2 and P4 inputs (`research/05-session-e002bed2.md:240`; `synthesis/hypothesis-03.md:59`), not from the deck. | deck:542, 549. "Case-insensitive" and "any severity" each appear 0 times. |
| E117-E138 row "carriage-return quote escape" (deck:533), rerun D | O-31 | **Disagree: RECOVER, MINOR.** The row carries a limitation, "Initially reasoned, not rendered on GitHub". The report's list of unverified monitor behaviors (Report:407) leaves it out. | deck:533; `research/05-session-e002bed2.md:131,294`. "Carriage" appears 0 times. |
| E117-E138 row "validators accept newline-suffixed values" (deck:548), rerun D | O-32 | **Disagree: RECOVER, MINOR.** Report:736 gives only a count of four accepted defects. This row's classification ("retained or incomplete hardening") and its reachability limit appear nowhere in the report. | deck:545-548; `research/05-session-e002bed2.md:166-171`. "Trailing newline" appears 0 times. |
| All other E46-E75, E97-E114 and E117-E138 rows; E151, E168, E170 and E176-E178, rerun D | none | **Agree: D.** These restate Partition 2 case items that P2 judged one by one as R or C, for example P2 rows 19, 27, 30, 50, 173-176, 178, 182 and 289-294. The report's explicit deferral of the remaining detail (Report:271, 274, 277, 379, 382) is a reasoned exclusion. | P2 report lines 22-349 and the report lines cited. |
| E1-E45, E76-E96, E115-E116, E139-E150, E152-E206, E210-E290, rerun R or R/D | none | **Agree.** I re-read the D10-D16 rows and the Report:440-446 representation. | deck:700-721, 812-890. |
| D2, D4, D12, D16 (not enumerated by the rerun) | none | **No new omission.** D2 and D4 restate P1 and P2 inputs. D12 and D16 are represented. | deck:68-368, 816-823, 886-890; Report:118-121, 309, 440-446. |

### New O-IDs

None. The rerun's only omission maps to O-02. The nine overturned dispositions all map to existing IDs: O-01, O-05, O-23, O-25, O-28, O-29, O-30, O-31 and O-32. Their recovery text in the Issues Found table stands unchanged. O-02 now lists its originating partitions as P1 #19 (origin), P4 #2 and P3-rerun O1, and stays IMPORTANT.

### Final RECOVER list for the Step 6.39 fixer

There are 34 omissions to recover:
- **IMPORTANT (4):** O-01, O-02, O-04, O-05.
- **MINOR (30):** O-03, O-06, O-07, O-09, O-10, O-11, O-12, O-13, O-15, O-16, O-17, O-18, O-19, O-20, O-21, O-22, O-23, O-24, O-25, O-26, O-27, O-28, O-29, O-30, O-31, O-32, O-33, O-34, O-35, O-36.
- **Not to recover:** O-08 and O-14 stay DEDUP under Report:279.

**Conditions on the fixer:**
- **Undebated evidence stays out of the ranking rows.** Keep O-04 and O-05 out of the Option Support rows, and label O-25, O-28 and O-29 as case-report additions the debate never weighed.
- **Reruns triggered by changed wording.** O-01, O-02, O-03, O-05 and O-23 change what the report asserts. Under Step 6.39 that invalidates the affected prior report-gate and fidelity checks, which must actually be rerun.

### Updated overall verdict

Verdict: FAIL. The 34 verified omissions above remain in the report. The missing Partition 3 reviewer pass is now covered by the rerun plus this adjudication.

| Status | Result |
|---|---|
| DONE | Read the Partition 3 rerun in full and accepted it as the item-level pass. Its counts reconcile at 290. |
| DONE | Read deck D2, D4, D12 and D16 directly and found no new omission. Overturned 9 of the rerun's dedup dispositions against source and report text, and mapped its only omission to O-02. No new O-ID was needed. |
| NEXT | The Step 6.39 fixer recovers the 34 IDs listed above. Steps 6.40 and 6.41 must then re-verify this addendum's adjudications with fresh reviewers. |

_Parent persistence note (2026-10-24): addendum appended verbatim from the consolidator's final transcript text (record 233) at the parent's request; the original consolidation above is unchanged._

## Erratum: Partition 3 Rerun Counts (2026-10-24, anti-omission cycle 2)

**Attribution:** appended by the anti-omission fix cycle 2 worker (Task Step 6.42, group M7; `qa/qa-anti-omission-fix-log-cycle2.md`) from the structural verifier's finding AO-V7 (`qa/qa-anti-omission-verification-structural.md`, Issues Found). Everything above this heading is unchanged; this section corrects one statement and rewrites nothing.

**Statement corrected:** the addendum's rerun validity verdict (line 243 above) says the rerun's "counts reconcile: 256 represented + 33 covered-by-dedup + 1 omitted = 290". Only the 290 total and the block sum 17+7+20+107+14+20+13+20+11+34+24+3 reconcile. The 256/33/1 split is the rerun's own summary (`qa/qa-anti-omission-report-3-rerun.md:248-251`), and it does not match the rerun's own enumeration table. This is the same class of count failure recorded against the original Partition 3 report under PF-01.

**Recount from the rerun's own table** (`qa/qa-anti-omission-report-3-rerun.md:26-233`; every range row expanded to its item count, for example E46-E75 = 30; counted mechanically):

| Status in the rerun table | Items | Rows |
|---|---:|---|
| R (represented) | 210 | Block A 17, B 7, C 20, D 34 (E45, E76-E91, E92-E96, E116, E140-E150), E 14, F 15, G 13, H 18, I 11, J 34, K 24, L 3 |
| D (covered-by-dedup) | 76 | E46-E75 (30), E97-E114 (18), E117-E138 (22), E139, E151, E170, E177, E178, E207 |
| R/D | 3 | E115, E168, E176 |
| O (omitted) | 1 | E209 |
| **Total** | **290** | 210 + 76 + 3 + 1 |

**Related labelling slips, recorded and not rewritten:**
- The rerun's own prose (`qa/qa-anti-omission-report-3-rerun.md:254`) names the dedup ranges "E97-E116" and "E117-E139", but its table marks E115 R/D and E116 R.
- The addendum's mapping table groups E168 and E176 with the rerun's D rows (line 275 above), but the rerun marks them R/D. It groups E139 with the "rerun R or R/D" rows (line 276 above), but the rerun marks E139 D; its anchor, the five reviewer identities in the Section 2.2 monitor row, is present in the report.

**Effect:** none on the O-ID set, the RECOVER list or the ranking. The mapping table above (lines 262-277) still adjudicates every D range and every single D row, and the recount changes no adjudication. The rerun file and the earlier text of this consolidation are not edited.
