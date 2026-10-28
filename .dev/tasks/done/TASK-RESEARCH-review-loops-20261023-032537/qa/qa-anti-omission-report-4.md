# Anti-Omission Report: Partition 4

Verdict: FAIL

**Report reviewed:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/RESEARCH-REPORT-review-loops.md`. All 1,313 lines were read. The sha256 was re-measured at `a10cef088fb1be687fc65a72553910a8a522b4ef8eccb8081e4e2e48972469c7`, which matches the assigned identity.
**QA phase:** anti-omission, Task Step 6.37. Report-only, fix authorization false.
**Input map:** `phase-outputs/discovery/anti-omission-input-map.md`, Partition 4 (lines 75-103). Method rules (10-22) and known defects J1, L1, L2 and L3 were applied.
**Input files checked:** all 26 files in Partition 4, read in full with no sampling: synth-04, synth-05, synth-06, hypothesis-01 to -05, run-evidence, return-contract, input-manifest, merged-root-cause-analysis, diff-analysis, debate-transcript (1-489), invariant-probe, base-selection (1-577), score-source-manifest (1-2298), refactor-plan, plan-review-evidence, merge-log, variant-1 to -5-original and gaps-and-questions. **Total distinct findings enumerated: 406.**
**Date:** 2026-10-24
**Governing template:** `/config/.claude/skills/tech-research/SKILL.md:1196-1239`, Anti-Omission Agent Prompt and output format.

**Path key.** Package-relative paths:
- S4, S5, S6 = `synthesis/synth-04-options-recommendation.md`, `synth-05-implementation-plan.md`, `synth-06-questions-evidence.md`
- H1-H5 = `synthesis/hypothesis-01.md` to `-05.md`
- RE, RC, IM, MR = `reviews/adversarial/run-evidence.md`, `return-contract.md`, `input-manifest.json`, `merged-root-cause-analysis.md`
- DA, DT, IP, BS, SM, RP, PR, ML, VA1-VA5 = `reviews/adversarial/adversarial/diff-analysis.md`, `debate-transcript.md`, `invariant-probe.md`, `base-selection.md`, `score-source-manifest.json`, `refactor-plan.md`, `plan-review-evidence.md`, `merge-log.md`, `variant-1-original.md` to `variant-5-original.md`
- GQ = `gaps-and-questions.md`
- R = the final report

Status values:
- **REP:** REPRESENTED.
- **DEDUP:** COVERED-BY-DEDUP.
- **OMIT:** OMITTED.

## Full Enumeration

### A. synth-04, Sections 6-7 (99 items)

| ID | Source | Distinct item (family) | Status | Report location or equivalent |
|---|---|---|---|---|
| A01 | S4:16 | Five options are the five debated cards; variants immutable; cards preserve bodies verbatim (provenance claim) | REP | R:484 |
| A02 | S4:18 | Options follow card order, not rank (rank) | REP | R:486 |
| A03 | S4:22 | Ten-point writing convergence is not causal agreement (debate) | REP | R:490 |
| A04 | S4:23 | unresolved_conflicts 0 counts diff points; two causal pairs disputed (debate) | REP | R:491 |
| A05 | S4:24 | V4 writing base by tiebreak, not most likely cause (rank) | REP | R:492 |
| A06 | S4:25 | Final orders are judgments, not independent observations, majority or probability (rank) | REP | R:493 |
| A07 | S4:26 | Round 2.5 PASS is not causal consensus (invariant) | REP | R:494 |
| A08 | S4:27 | Process-confidence label is not causal probability (debate) | REP | R:495 |
| A09 | S4:28 | Post-merge PASS 13/13 is fidelity, not replay or consensus (limit) | REP | R:496 |
| A10 | S4:30-34 | A-001: target; reach first; direct evidence second; no independent votes; event override (rank) | REP | R:498-502 |
| A11 | S4:35 | A-001 Round 1 vector ACCEPT/QUALIFY/ACCEPT/ACCEPT/QUALIFY; Round 2 V1 ACCEPT, V2-V5 QUALIFY (debate) | REP | R:503 |
| A12 | S4:37-40 | Sample: 6 of 30 by modification time, clustered; 3 strict/1 blocker/2 planning; Orca pair and credential pair not independent (limit) | REP | R:505-508 |
| A13 | S4:44,54 | V1 description and mechanism: weaker predicate, later old counterexample (cause) | REP | R:512,522 |
| A14 | S4:46-50 | V1 four-step how-it-works (cause) | REP | R:514-518 |
| A15 | S4:55 | V1 support, oracle: labels/counts pass, 67/78 tests, four defects, record 291 truncated relay (support) | REP | R:523 |
| A16 | S4:55 | V1 support, monitor: 640-line workflow, structural checks, tests deferred to Task 14, most findings preexisting (support) | REP | R:523 |
| A17 | S4:55 | V1 support, Orca coverage credits up-to-date state; validation after fetch (support) | REP | R:523 |
| A18 | S4:55 | V1 support, CI: search stub ignores filters; blacklist admits half-edited header (support) | REP | R:523 |
| A19 | S4:56 | V1 opposition: oracle repairs, frozen authority, Tasks 10/11, introductions, credential proof-only (disconf) | REP | R:524 |
| A20 | S4:56 | V1 opposition: screened controls Session 10 Task 4 and Session 17 Task 8 with limits (disconf) | REP | R:524 |
| A21 | S4:57 | V1 alternatives V2-V5 coexist; size and deferred tests are amplifiers (alt) | REP | R:525 |
| A22 | S4:58 | V1 scope exclusions (scope) | REP | R:526 |
| A23 | S4:59 | V1 falsification, strengthen and weaken rule (falsif) | REP | R:527 |
| A24 | S4:60 | V1 strength; observational; miss reasons unknown (limit) | REP | R:528 |
| A25 | S4:61 | V1 debate: first in all orders, C-004, critiques at :128/:167/:208, accepted at :256-257 (debate) | REP | R:529 |
| A26 | S4:62 | V1 historical (499, 843/849, v4 unreviewed at 946) versus current quality-gates rule; drift (limit) | REP | R:530 |
| A27 | S4:63-64 | V1 effort M (reasoned); risk Medium with replay constraints (check) | REP | R:531-532 |
| A28 | S4:65-66 | V1 reuse and files: oracle artifacts, record 585, Orca v1-v4, v3 with no comparison target, CI plans (check) | REP | R:533-534 |
| A29 | S4:67-68 | V1 pros and cons: unanimous position; cognition and task size not isolated; monitor reconstruction (check) | REP | R:535-536 |
| A30 | S4:72,81 | V2 description and mechanism; introduction kept separate from sibling (cause) | REP | R:540,549 |
| A31 | S4:74-77 | V2 how-it-works (cause) | REP | R:542-545 |
| A32 | S4:82 | V2 support, Orca: inventory test, four-asset predicate, digest source, further case introductions (support) | REP | R:550 |
| A33 | S4:82 | V2 support: monitor trap 759-762/1240; CI lost ancestors (support) | REP | R:550 |
| A34 | S4:83 | V2 opposition: 14/2; 20 is not 20; monitor preexisting; oracle and credential; 2 of 4 CI mediums downgraded (disconf) | REP | R:551 |
| A35 | S4:83 | V2 opposition: Sessions 10/17 controls; Sessions 13/14 unreviewed corrections (disconf) | REP | R:551 |
| A36 | S4:84 | V2 alternatives: S-002 versus C-003; CI exemption; pin-trap sibling; V1 precedes; V3 (alt) | REP | R:552 |
| A37 | S4:85 | V2 scope: C-003 definition; sibling never introduction; plan is not runtime; trap accepted, not repaired (scope) | REP | R:553 |
| A38 | S4:86 | V2 falsification (falsif) | REP | R:554 |
| A39 | S4:87 | V2 strength; CI is plan nonconformance only (limit) | REP | R:555 |
| A40 | S4:88 | V2 debate 2,2,3,3,3 with reasons; V2 concessions; C-003 (debate) | REP | R:556 |
| A41 | S4:89 | V2 current rule: no weakness established (limit) | REP | R:557 |
| A42 | S4:90-91 | V2 effort M; risk Low-Medium; blocked attempts 150/151 and 1164-1170 not applied (check) | REP | R:558-559 |
| A43 | S4:92-95 | V2 reuse, files, pros, cons (check) | REP | R:560-563 |
| A44 | S4:99,108 | V3 description and four subtypes (cause) | REP | R:567,576 |
| A45 | S4:101-104 | V3 how-it-works (cause) | REP | R:569-572 |
| A46 | S4:109 | V3 support: lint relaxation chain 1215/1230/nested reviewer; FINAL reapplies (support) | REP | R:577 |
| A47 | S4:109 | V3 support: two rubric texts loaded from the same path (support) | REP | R:577 |
| A48 | S4:109 | V3 support: migration records; uncapped fields; Orca contradictions; CI boundary file (support) | REP | R:577 |
| A49 | S4:110 | V3 opposition: oracle, render, genuine monitor defects, same driving-source hash (disconf) | REP | R:578 |
| A50 | S4:111 | V3 alternatives: V1/V2 explain artifact state; V4 confound (alt) | REP | R:579 |
| A51 | S4:112 | V3 scope; "proven amplifier in two runs" (scope) | REP | R:580 |
| A52 | S4:113 | V3 falsification: paired adjudication (falsif) | REP | R:581 |
| A53 | S4:114 | V3 strength; installer identity and policy-only effect unknown (limit) | REP | R:582 |
| A54 | S4:115 | V3 debate 3,3,2,2,2 with reasons; concessions; C-002 (debate) | REP | R:583 |
| A55 | S4:116 | V3 historical versus current: moved-line rule; no registry (limit) | REP | R:584 |
| A56 | S4:117-118 | V3 effort M; risk Medium constraints (check) | REP | R:585-586 |
| A57 | S4:119-122 | V3 reuse, files, pros, cons (proof fixed; reviewer variance) (check) | REP | R:587-590 |
| A58 | S4:126-135 | V4 description, three forms, mechanism; head-moved is not proof (cause) | REP | R:594-603 |
| A59 | S4:136 | V4 support: initial credential proof became README citation; pass with no delivery change (support) | REP | R:604 |
| A60 | S4:136 | V4 support: Task 10 blank line-10 pointer; repair missed a row (support) | REP | R:604 |
| A61 | S4:136 | V4 support: documentation Task 2 post-edit HEAD baseline; tree f60d2c3 (support) | REP | R:604 |
| A62 | S4:137 | V4 opposition, including Session 17 FINAL (disconf) | REP | R:605 |
| A63 | S4:138 | V4 alternatives (alt) | REP | R:606 |
| A64 | S4:139 | V4 scope: two sessions, three contexts, clustered (scope) | REP | R:607 |
| A65 | S4:140 | V4 falsification (falsif) | REP | R:608 |
| A66 | S4:141 | V4 strength; digests exclude evidence and policy (limit) | REP | R:609 |
| A67 | S4:142 | V4 debate 4,4,4,5,5; V4 reversal reason; V5 agreed; C-007; writing base by tiebreak (debate) | REP | R:610 |
| A68 | S4:143 | V4 historical versus current (limit) | REP | R:611 |
| A69 | S4:144-149 | V4 effort S, risk Low, reuse, files, pros "Cheap", cons (check) | REP | R:612-617. Deliberately re-rated to M at Task Step 6.18 (R:612,653); "Cheap" removed to match the re-rating; all other content kept |
| A70 | S4:153-159 | V5 description, how-it-works, mechanism (cause) | REP | R:621-627 |
| A71 | S4:160 | V5 support: oracle exclusion, three repairs, PASS (support) | REP | R:628 |
| A72 | S4:160 | V5 support: `/usr/bin/man` notice script; static retry; same clause (support) | REP | R:628 |
| A73 | S4:161 | V5 opposition (disconf) | REP | R:629 |
| A74 | S4:162 | V5 alternatives (alt) | REP | R:630 |
| A75 | S4:163 | V5 scope: two incidents, different endpoints (scope) | REP | R:631 |
| A76 | S4:164 | V5 falsification (falsif) | REP | R:632 |
| A77 | S4:165 | V5 strength strong, moderate in general (limit) | REP | R:633 |
| A78 | S4:166 | V5 debate 5,5,5,4,4; concessions; C-005 (debate) | REP | R:634 |
| A79 | S4:167 | V5 historical versus current pin rule (limit) | REP | R:635 |
| A80 | S4:168-173 | V5 effort, risk, reuse, files, pros, cons (check) | REP | R:636-641 |
| A81 | S4:177-189 | Options comparison table, all criteria rows (overlap/rank) | REP | R:645-657 |
| A82 | S4:195-199 | Recommended approach (rank) | REP | R:663-667 |
| A83 | S4:201-203 | Rationale (rank) | REP | R:669-671 |
| A84 | S4:207-213 | 7.1 ranking rows: reasons, holders, dispute status, overrides (rank) | REP | R:675-681 |
| A85 | S4:217-225 | 7.2 five final orders (debate) | REP | R:685-693 |
| A86 | S4:227-234 | Pair tallies, including derived V1/V2/V3 above V4/V5 (debate) | REP | R:695-702 |
| A87 | S4:237-238 | Middle pair on larger side; bottom pair on smaller side; refactor-plan judgment; plan review passed; V4 reversal (debate) | REP | R:705-706 |
| A88 | S4:239 | No majority holds the full order (debate) | REP | R:707 |
| A89 | S4:240 | Weakest step is V5/V4 (rank) | REP | R:708 |
| A90 | S4:241 | Status partial; Round 3 not run (debate) | REP | R:709 |
| A91 | S4:245-254 | 7.3 eight statements, including user acceptance and numeric writing order (rank) | REP | R:713-722 |
| A92 | S4:258-268 | 7.4 overlap cautions (overlap) | REP | R:726-736, extended with shared deployment |
| A93 | S4:272-279 | 7.5 per-candidate current versus historical, including Task 10 authority event (limit) | REP | R:740-747 |
| A94 | S4:281 | Dated layer observation, 3 equal and 4 different pairs (limit) | REP | R:749 |
| A95 | S4:285-292 | 7.6 orders 1-4: checks, reasons, ranking effect (check/rank) | REP | R:753-760. Decision rules deliberately revised (S4:289 "V1 loses its lead" became a reach-input rule needing a debate rerun); the falsification direction survives |
| A96 | S4:294 | Trade-offs (check) | REP | R:762, revised |
| A97 | S4:298-308 | 7.7 key-finding coverage (provenance claim) | REP | R:766-776 |
| A98 | S4:310-319 | Screened-control placement table (disconf) | REP | R:778-787 |
| A99 | S4:321-340 | Sources read and limits (limit) | REP | R:1292-1313 (moved to 10.11) |

### B. synth-05, Section 8 (25 items)

| ID | Source | Distinct item | Status | Report location |
|---|---|---|---|---|
| B01 | S5:9-11 | Research-only scope; five comparisons plus order 4 plus two Phase 3 checks; not a tasklist | REP | R:797-799 |
| B02 | S5:13 | Different mechanisms; separate checked from required and introduced from old | REP | R:801 |
| B03 | S5:17-21 | Phase 1 goal and dependencies; missing bytes are a limitation | REP | R:805-809 |
| B04 | S5:23-41 | Verified input targets | REP | R:811-829 |
| B05 | S5:45 | Step 1.1, comparison identity; unknown rather than current bytes | REP | R:833 |
| B06 | S5:46 | Step 1.2, source layers distinct | REP | R:834 |
| B07 | S5:50-60 | Rendering-evidence mapping, three targets with limits | REP | R:852-862 |
| B08 | S5:62-66 | Phase 2 goal and dependencies | REP | R:864-868 |
| B09 | S5:70 | Step 2.1, what acceptance proves | REP | R:872 |
| B10 | S5:71 | Step 2.2, connected effects | REP | R:873 |
| B11 | S5:72 | Step 2.3, contract held constant | REP | R:874 |
| B12 | S5:73 | Step 2.4, proof versus delivery | REP | R:875 |
| B13 | S5:74 | Step 2.5, feasibility and authority | REP | R:876 |
| B14 | S5:75 | Step 2.6, reach on new sessions (user scope) | REP | R:877 |
| B15 | S5:77 | Source bindings | REP | R:879 |
| B16 | S5:79-83 | Phase 3 goal and dependencies | REP | R:881-885 |
| B17 | S5:87 | Step 3.1, successful-repair controls | REP | R:889 |
| B18 | S5:88 | Step 3.2, adjudicate first; older-pin versus equal-tag | REP | R:890 |
| B19 | S5:89 | Step 3.3, denominators; condensed summaries | REP | R:891 |
| B20 | S5:90 | Step 3.4, evidence boundary | REP | R:892 |
| B21 | S5:91 | Step 3.5, consent, scope, ruling | REP | R:893 |
| B22 | S5:92 | Step 3.6, checkpoint guard versus HEAD movement | REP | R:894 |
| B23 | S5:96-108 | Constraints and approval boundaries | REP | R:896-910 |
| B24 | S5:112-123 | Required-input coverage | REP | R:912-925 |
| B25 | S5:127-134 | Integration checklist | REP | R:927-935; the component-review pointer moved to R:1259 |

### C. synth-06, Sections 9-10.8 (35 items)

| ID | Source | Distinct item | Status | Report location |
|---|---|---|---|---|
| C01 | S6:9 | Questions are not permission | REP | R:941 |
| C02 | S6:13 | Question 1, breadth outside sample | REP | R:945 |
| C03 | S6:14 | Question 2, reviewer misses | REP | R:946 |
| C04 | S6:15 | Question 3, rubric authorship and uncaptured versions | REP | R:947 (revised to installer identity) |
| C05 | S6:16 | Question 4, evidence under earlier rubric | REP | R:948 |
| C06 | S6:17 | Question 5, Orca v4 quality | REP | R:949 |
| C07 | S6:18 | Question 6, Orca source contradictions | REP | R:950 |
| C08 | S6:19 | Question 7, CI weaknesses at implementation | REP | R:951 (adds post-window ledger) |
| C09 | S6:20 | Question 8, runner behavior | REP | R:952 |
| C10 | S6:21 | Question 9, rendering | REP | R:953 |
| C11 | S6:22 | Question 10, monitor defects repaired? | REP | R:954 |
| C12 | S6:23 | Question 11, size thresholds | REP | R:955 |
| C13 | S6:24 | Question 12, live-model effectiveness | REP | R:956 |
| C14 | S6:25 | Question 13, oracle byte comparison | REP | R:957 |
| C15 | S6:26 | Question 14, excluded sessions' nested activity | REP | R:958 |
| C16 | S6:27 | Question 15, pointer semantic support | REP | R:959 |
| C17 | S6:28 | Question 16, helper enforcement | REP | R:960 |
| C18 | S6:29 | Question 17, live bytes | REP | R:961 |
| C19 | S6:30 | Question 18, task size | REP | R:962 |
| C20 | S6:31 | Question 19, causal-order disagreements | REP | R:963 |
| C21 | S6:32 | Question 20, governing layer | REP | R:964 |
| C22 | S6:34 | Question sources | REP | R:966 |
| C23 | S6:36 | Zero queries, sources and findings; provider not tested | REP | R:968 |
| C24 | S6:40-56 | Codebase, web and gaps-log listings | REP | R:976-992 |
| C25 | S6:60-84 | 10.1 snapshot and superseding rows | REP | R:994-1020 |
| C26 | S6:86 | 16/1/6 header accounting | REP | R:1022 |
| C27 | S6:88 | 30 slots, six incidents, three strict, denominators | REP | R:1024 |
| C28 | S6:90-109 | 10.2 research provenance | REP | R:1026-1045 |
| C29 | S6:111-120 | 10.3 captures | REP | R:1047-1056 |
| C30 | S6:122-135 | Recorded earlier attempts (8 rows) | REP | R:1058-1071 |
| C31 | S6:137-159 | 10.4 components; card format unresolved; synth-04 absent at snapshot | REP | R:1073-1095 |
| C32 | S6:161-181 | 10.5 adversarial artifacts; record 71; PASS scope | REP | R:1097-1117 |
| C33 | S6:183-226 | 10.6 QA inventory 191/204 | REP | R:1119-1162 |
| C34 | S6:228-243 | 10.7 gates and dispatches | REP | R:1164-1179 |
| C35 | S6:245-267 | 10.8 historical FAILs, closures, refresh requirement | REP | R:1181-1203 |

### D. hypothesis-01, V1 card (25 items)

| ID | Source | Distinct item (family) | Status | Report location or equivalent |
|---|---|---|---|---|
| D01 | H1:33 | Checks prove format, labels or presence, not behavior (cause) | REP | R:512 |
| D02 | H1:33 | Large units and deferred tests amplify; not proven universal causes (overlap) | REP | R:525,528 |
| D03 | H1:43-46 | Four-step mechanism (cause) | REP | R:514-518 |
| D04 | H1:50 | Examples within one incident are not independent (limit) | REP | R:501 |
| D05 | H1:56 | Oracle semantics row (support) | REP | R:523 |
| D06 | H1:57 | Monitor row: three jobs, many behaviors; range, summary and size defects originally present (support) | REP | R:523; R:169; "large unit" R:772 |
| D07 | H1:58 | Orca coverage row: presence mistaken for wiring or timing (support) | REP | R:523 |
| D08 | H1:59 | CI search and advisory row (support) | REP | R:523 |
| D09 | H1:101 | Oracle: weak checks explain escape, not the authorization barrier (disconf) | REP | R:524,728 |
| D10 | H1:102 | Tasks 10/11 converged; size is an amplifier only (disconf) | REP | R:524 |
| D11 | H1:103 | Plan defects and trap are real introductions (disconf) | REP | R:524 |
| D12 | H1:107 | V2/V3 explain different events (overlap) | REP | R:525 |
| D13 | H1:108 | Frozen fixture, render tools and pointers are competing blockers that coexist (alt) | REP | R:525 |
| D14 | H1:118-119 | Strength; observational; clustered; no rate or probability; not every finding missed initially (limit) | REP | R:528,717,524 |
| D15 | H1:123 | Genuine but too-weak check; presence is not timing; labels are not meaning (support) | REP | R:441,769 |
| D16 | H1:124 | An old counterexample is not a repair introduction (disconf) | REP | R:239 |
| D17 | H1:130 | Summary: progressive discovery when tests are deferred (cause) | REP | R:512-518,523 |
| D18 | H1:140 | Test uses preserved versions, fixed criteria and policy (falsif) | REP | R:527,532 |
| D19 | H1:141-142 | Counterexample on first-passing version; run the check used (falsif) | REP | R:527 |
| D20 | H1:142 | Test also separately verifies whether the relevant behavior test was deferred or absent (check) | **OMIT** | See omissions table, row 1 |
| D21 | H1:143 | Weaken and strengthen rule (falsif) | REP | R:527 |
| D22 | H1:144 | Not run; must not relax criteria or replace final review (check) | REP | R:527,532 |
| D23 | H1:154 | Miss reasons unknown; size versus paths not isolated; tests inspected, not rerun (question) | REP | R:946,962,935 |
| D24 | H1:158 | Coverage rows over-credit; test inventories omit requirements; not current-doc staleness (limit) | REP | R:343; R:271 states the test-table holes; R:263 |
| D25 | H1:7,128 | Post-debate format-only; pre-debate summary wording is historical (provenance claim) | REP | R:484,1089 |

### E. hypothesis-02, V2 card (20 items)

| ID | Source | Distinct item | Status | Report location |
|---|---|---|---|---|
| E01 | H2:33 | Hypothesis demonstrated in selected changes, not every failure | REP | R:540 |
| E02 | H2:43-46 | Mechanism and boundary types | REP | R:542-545,549 |
| E03 | H2:50 | Interactions from one plan are not independent | REP | R:563,735 |
| E04 | H2:52 | Plan defects differ from runtime; only successful edits count | REP | R:553,559 |
| E05 | H2:56 | Inventory-test row | REP | R:550 |
| E06 | H2:57 | Four-asset predicate changes which job rejects | REP | R:550; "release-predicate" R:344 |
| E07 | H2:58 | Digest provenance crosses contract | REP | R:550; "old-value-source" R:344 |
| E08 | H2:59 | Pin-job trap is a proven regression | REP | R:550 |
| E09 | H2:60 | CI ancestors; sequential safeguard does not repair conformance | REP | R:550,555 |
| E10 | H2:102 | 14/2; 20 items are not 20 regressions | REP | R:551 |
| E11 | H2:103 | Monitor defects preexist; size repair exposes limits | REP | R:551,733 |
| E12 | H2:104 | Oracle and credential failures need other explanations | REP | R:551 |
| E13 | H2:108 | Two outcomes; sibling evidence alone is not regression | REP | R:553 |
| E14 | H2:109 | V1 can precede; V3 separate; not reviewer cognition | REP | R:552,729,946 |
| E15 | H2:119-120 | Strength; not most monitor findings; no claims about every repair, context limits or model | REP | R:555,294 |
| E16 | H2:124-125 | Takeaways: introductions real; siblings are not new damage | REP | R:550,553 |
| E17 | H2:131 | Summary | REP | R:540,555 |
| E18 | H2:141-146 | Replay test; neighbor checks; reclassify; newly phrased is insufficient; smaller diffs are not a cure | REP | R:554,344,962 |
| E19 | H2:156 | No controlled experiment; proposals unapplied; trap accepted, not repaired | REP | R:962,349,553 |
| E20 | H2:160 | Reviewed proposals violate distinctions; historical, not current | REP | R:349 |

### F. hypothesis-03, V3 card (20 items)

| ID | Source | Distinct item (family) | Status | Report location or equivalent |
|---|---|---|---|---|
| F01 | H3:33 | Hypothesis (cause) | REP | R:567 |
| F02 | H3:43-45 | Mechanism steps 1-3 (cause) | REP | R:569-572 |
| F03 | H3:46 | Without exact criteria and loaded rules, correction and changed acceptance are indistinguishable (cause) | REP | R:579,834 |
| F04 | H3:50 | Contract mechanisms in one run are not independent (limit) | REP | R:501 |
| F05 | H3:52 | No row shows all later findings invented (disconf) | REP | R:578,890 |
| F06 | H3:56 | Lint relaxation; owner acceptance only later (support) | REP | R:577,170,345 |
| F07 | H3:57 | Rubric changed between reviewers; pass follows both changes; effects not isolated (support) | REP | R:229,577,582 |
| F08 | H3:57; MR:73 | Content and direction of the rubric change: old text treats stale evidence as issues; later text says a moved line alone is not an issue and changes acceptance handling (support) | **OMIT** | See omissions table, row 2 |
| F09 | H3:58 | Migration adds fresh review; no adviser or revert ladder (support) | REP | R:577,169 |
| F10 | H3:59 | Uncapped fields absent from plan; later fixes are not retroactive criteria (support) | REP | R:577,890 |
| F11 | H3:59; MR:77 | Case-insensitive matching not clearly required; per-review prompts made any defect of any severity noncompliant (support) | **OMIT** | See omissions table, row 3 |
| F12 | H3:60 | Orca prose versus diagram; CI boundary-file conceded optional (support) | REP | R:577,254-256 |
| F13 | H3:102-104 | Three counterevidence bullets (disconf) | REP | R:578 |
| F14 | H3:108-109 | Family, not invention; individual attribution; amplifier in two runs (scope) | REP | R:576,580 |
| F15 | H3:119-120 | Strength; actor unknown; hardening validity varies (limit) | REP | R:582,241 |
| F16 | H3:124-125 | Record original and loaded contract; changed verdict is not controlled proof (check) | REP | R:345,579,948 |
| F17 | H3:131 | Summary: amplifies, does not invalidate all findings (cause) | REP | R:580 |
| F18 | H3:141-145 | Paired test; no waiver; accepted gap is not compliant (falsif) | REP | R:581,586 |
| F19 | H3:155 | Confounded; stable counterexamples; reviewer counts not shown as cause (question) | REP | R:582,578,294 |
| F20 | H3:159 | Same path, different contents; captured, not current (limit) | REP | R:229 |

### G. hypothesis-04, V4 card (20 items)

| ID | Source | Distinct item | Status | Report location |
|---|---|---|---|---|
| G01 | H4:33-34 | Hypothesis; does not explain every semantic defect | REP | R:594,607 |
| G02 | H4:35 | Proof can fail independently of delivery | REP | R:594 |
| G03 | H4:45-48 | Four mechanism bullets | REP | R:596-603 |
| G04 | H4:49 | Invalid claim-evidence-state link, not just a line number | REP | R:603 |
| G05 | H4:59 | Initial credential incident | REP | R:604 |
| G06 | H4:60 | Follow-up incident | REP | R:604 |
| G07 | H4:61 | Dirty baseline; render task lacked its start-HEAD file | REP | R:604,734 |
| G08 | H4:63 | Controls are digests and before/after evidence, not verdict order | REP | R:609,616 |
| G09 | H4:105 | Valid rejection; proof repair was real work; genuine lint failure | REP | R:605 |
| G10 | H4:106 | Confounded third pass; current qa.md:82 | REP | R:605,611 |
| G11 | H4:107 | Not permission to ignore evidence | REP | R:613,745 |
| G12 | H4:111 | Concentrated; overlaps policy, first-pass checks, records | REP | R:607,731 |
| G13 | H4:112 | Checkpoint halt is not a cause | REP | R:605 |
| G14 | H4:116 | Competing explanations | REP | R:606 |
| G15 | H4:126 | Strength; no frequency, probability or version effect | REP | R:609,717 |
| G16 | H4:132 | Summary: mechanisms must not be conflated | REP | R:603,605 |
| G17 | H4:142-143 | Falsification | REP | R:608,613 |
| G18 | H4:153 | Actor and miss unknown; t10 log missing at old path; transcript preserves it | REP | R:947,606,614 |
| G19 | H4:157 | README separator, blank line, later line shift | REP | R:346,611 |
| G20 | H4:174,261 | Writing-base role is quality, not likelihood | REP | R:492 |

### H. hypothesis-05, V5 card (17 items)

| ID | Source | Distinct item | Status | Report location |
|---|---|---|---|---|
| H01 | H5:33-34 | Hypothesis; not a universal inability | REP | R:621 |
| H02 | H5:35 | Rechecking an unchanged blocker cannot show resolution | REP | R:621-623 |
| H03 | H5:45 | Fixture frozen before its property was checked; authority excluded the fix | REP | R:628,166,728 |
| H04 | H5:46 | man prints a notice; static evidence cannot show rendering | REP | R:628 |
| H05 | H5:47 | Neither blocker changed; scoped decision needed | REP | R:623 |
| H06 | H5:48 | Unchanged state, not a new break | REP | R:166,347 |
| H07 | H5:58-59 | Incident rows | REP | R:628 |
| H08 | H5:61 | Repeats predictable from a documented blocker | REP | R:633,627 |
| H09 | H5:103-104 | Feasible; renderer could satisfy; re-review legitimate | REP | R:629 |
| H10 | H5:105 | Late blocker handling, not an impossible specification | REP | R:629,347 |
| H11 | H5:109-110 | Scope two incidents; overlaps; monitor acceptance needs other explanations | REP | R:630-631,736 |
| H12 | H5:114 | Competing explanations | REP | R:629-630 |
| H13 | H5:124 | Strength strong and moderate; no impossibility | REP | R:633 |
| H14 | H5:130 | Summary: two endpoints; no weakening of requirements | REP | R:631,637 |
| H15 | H5:140-141 | Falsification | REP | R:632,637 |
| H16 | H5:151 | No rendering; t6 log missing at old path; record 450 | REP | R:953,638,1066 |
| H17 | H5:155 | No stale-doc cause; re-frozen input is authorized; guard inadequate | REP | R:166,635,263 |

### I. run-evidence, return-contract, input-manifest (15 items)

| ID | Source | Distinct item | Status | Report location or equivalent |
|---|---|---|---|---|
| I01 | RE:7-8 | Actual Mode A deep invocation of five cards | REP | R:8,1101 |
| I02 | RE:11 | Zero strict inter-card factual contradictions | DEDUP | R:664 "distinct mechanisms that can coexist"; R:525 |
| I03 | RE:14 | Round 3 skipped at 1.0 against 0.80; no HIGH unaddressed | REP | R:709,494 |
| I04 | RE:16 | V4 base by tiebreak | REP | R:492 |
| I05 | RE:16 | Provisional order; only V1 unanimous; both pairs 3/5 | REP | R:675-702; phrasing reconciled at R:1289 |
| I06 | RE:18 | Plan review; canonical FAIL then PASS kept | REP | R:1111-1113 |
| I07 | RE:21; RC:28-29 | Merge recovered from record 71; no new merge or debate | REP | R:1115 |
| I08 | RE:23 | Validator PASS 13/13 and its scope | REP | R:496,1117,1156 |
| I09 | RC:10-20 | Contract: partial, 1.0, V4, 0 conflicts, no unaddressed invariants | REP | R:490-492,709 |
| I10 | RC:17-19 | fallback_mode false, failure_stage null, skill-direct | DEDUP | R:1101 "Actual invocation, completed debate/scoring"; R:1115 |
| I11 | RE:26,32; RC:26 | Partial is the honest final status; no completion claimed | REP | R:474,1104,1191 |
| I12 | RC:26 | Schema integer-versus-list note; disputes kept as warnings | DEDUP | R:491 states what the 0 counts and that two pairs remain disputed |
| I13 | RC:26 | V4 base is not the top causal explanation | REP | R:492,718 |
| I14 | RC:29-31 | Recovery hashes matched; no new debate or Git | REP | R:1113,1115 |
| I15 | IM:6-32 | Five debated input identities | REP | R:484,1089,1102 |

### J. merged-root-cause-analysis (17 items; MR:73 and MR:77 content are counted under F08 and F11)

| ID | Source | Distinct item | Status | Report location |
|---|---|---|---|---|
| J01 | MR:8-10 | Weak checks broadest but not the whole; five coexist; one sequence can traverse several | REP | R:664,525,732 |
| J02 | MR:15-17 | Target includes policy-driven reopening; comparison rule | REP | R:478,499-502 |
| J03 | MR:19 | No prevalence, probability, model or version effect | REP | R:506,717,722 |
| J04 | MR:21 | Writing base and writing agreement are not causal | REP | R:490-492 |
| J05 | MR:28-34 | Ordering table with conditional fit | REP | R:675-681 |
| J06 | MR:37-41 | Three advocate orders | REP | R:685-693 |
| J07 | MR:43 | Only V1 unanimous; not the majority's order | REP | R:707 |
| J08 | MR:47-138 | Five accounts: mechanism, support, opposition, limits, comparison (excluding MR:73 and MR:77) | REP | R:510-641 |
| J09 | MR:143-151 | Event-to-mechanism table, 7 rows | REP | R:647-650,728-736 |
| J10 | MR:153 | Newly phrased is not newly created; broader is not invalid | REP | R:239,241,349 |
| J11 | MR:158-165 | Six endpoint types are not interchangeable | REP | R:736,291,582,603,604,628 |
| J12 | MR:170-178 | Seven-step evidence path | REP | R:801,833-894 |
| J13 | MR:180 | No single check sufficient; fixture check is not authority; static is not render; smaller tasks are not a cure | REP | R:728,347,962,892 |
| J14 | MR:185-194 | Card directory, 29 links, anchors not replayed | REP | R:480,1112 |
| J15 | MR:196 | Failed fresh reads of t10 and t6 logs | REP | R:614,1066 |
| J16 | MR:201-207 | Seven limits | REP | R:946,962,947-948,241,953,349,553,722 |
| J17 | MR:212-214 | Summary; no safeguard shown to eliminate repeats | REP | R:670,801,892 |

### K. diff-analysis (21 items)

| ID | Source | Distinct item | Status | Report location or equivalent |
|---|---|---|---|---|
| K01 | DA:7-8,75 | Ten debate points; unique rows are not votes | REP | R:490,503 |
| K02 | DA:6 | Variants coexist; not exclusive designs | REP | R:664 |
| K03 | DA:16 | S-001: presentation earns no causal weight | DEDUP | R:492,718 (writing base and scores are not cause) |
| K04 | DA:17 | S-002 granularity of subtypes | REP | R:549,553,576,603,623 |
| K05 | DA:24 | C-001: what changes between submissions | REP | R:647,760 |
| K06 | DA:25 | C-002: state under examination | REP | R:652,874 |
| K07 | DA:26 | C-003: what evidence distinguishes | REP | R:652,553 |
| K08 | DA:27 | C-004: breadth | REP | R:648,652 |
| K09 | DA:28 | C-005: termination interpretation | REP | R:652,736 |
| K10 | DA:29 | C-006: discriminators | REP | R:527,554,581,608,632 |
| K11 | DA:30 | C-007: survival when live files change | REP | R:652,614,1066 |
| K12 | DA:33 | Rows not independent; tests unexecuted | REP | R:508,721 |
| K13 | DA:35-38 | Interpretation guards | REP | R:677-681,348,664 |
| K14 | DA:41-43 | Zero strict contradictions; differences are debate questions | DEDUP | R:664,525 (same as I02) |
| K15 | DA:48-52 | Unique contributions U-001 to U-005 | REP | R:523,550,577,604,629 |
| K16 | DA:60-63 | Four stated shared preconditions | REP | R:506,239,664,721 |
| K17 | DA:64,69 | A-001: existence, reach and recurrence differ | REP | R:88 |
| K18 | DA:71 | No independence assumption attributed | REP | R:506-508 |
| K19 | DA:76,78 | Severity and scores are not probabilities | REP | R:495,717 |
| K20 | DA:79 | V4/V5 missing archived logs | REP | R:1066 |
| K21 | DA:77 | Step 1 selects no winner | REP | R:88 |

### L. debate-transcript (20 items)

| ID | Source | Distinct item | Status | Report location or equivalent |
|---|---|---|---|---|
| L01 | DT:5,7 | Two advocate rounds plus probe; not three rounds | REP | R:494,709 |
| L02 | DT:19-49 | Round 1 V1: position, steelmen, critiques, concessions | REP | R:526,529,962 |
| L03 | DT:64-100 | Round 1 V2: position, critiques, overrides | REP | R:551,556 |
| L04 | DT:113-146 | Round 1 V3: why review happened versus why findings are valid | REP | R:529,730 |
| L05 | DT:152-185 | Round 1 V4: order V1>V3>V2>V4>V5; concessions | REP | R:610 |
| L06 | DT:195-223 | Round 1 V5: order; two barriers; do not bypass freeze | REP | R:623,634,637 |
| L07 | DT:243 | Round 1 A-001 vector | REP | R:503 |
| L08 | DT:231-242,475 | Round 1 writing labels were heterogeneous, not normalized votes | DEDUP | R:490 and R:652 (final Round 2 writing outcome); the source asserts no Round 1 consensus |
| L09 | DT:251-280 | Round 2 V1: accepted criticisms; V2>V3 and V4>V5 reasons | REP | R:529,556,610,634 |
| L10 | DT:289-319 | Round 2 V2: re-entry strengthens V3 but V2 not demoted | REP | R:556,583,634 |
| L11 | DT:328-359 | Round 2 V3: concessions; hardening not automatically invalid; V3 second | REP | R:583,679,730,890 |
| L12 | DT:368-400 | Round 2 V4: concessions; V5>V4 reversal reasons | REP | R:610,706 |
| L13 | DT:409-441 | Round 2 V5: concessions; V5>V4 held independently | REP | R:634,610 |
| L14 | DT:268-277 et seq. | Round 2 writing nominations | REP | R:652 |
| L15 | DT:279,318,358,399,440 | Conditional causal overrides | REP | R:677-681 |
| L16 | DT:449-450 | Round 3 not executed | REP | R:709 |
| L17 | DT:453 | 95% is process confidence, not causal | REP | R:495 |
| L18 | DT:469-475 | Convergence only for writing; causal not achieved | REP | R:490-491,709 |
| L19 | DT:478-486 | Final orders, tallies, four-of-five, qualified display | REP | R:685-708 |
| L20 | DT:49 | Task size is an amplifier remark | REP | R:962,966 |

### M. invariant-probe (9 items)

| ID | Source | Distinct item | Status | Report location |
|---|---|---|---|---|
| M01 | IP:6,29-32 | INV-001: delivery or PASS does not fix acceptance conditions | REP | R:244 |
| M02 | IP:7,34-37 | INV-002: nominal command or acceptance does not clear a blocker | REP | R:243,628 |
| M03 | IP:8,39-44 | INV-003: writing 10/10 is not causal; pairs 3/5 | REP | R:493,702 |
| M04 | IP:9,46-49 | INV-004: breadth is not prevalence; missing logs do not erase evidence | REP | R:493,1066 |
| M05 | IP:10,51-54 | INV-005: no sole cause | REP | R:720 |
| M06 | IP:11,56-63 | INV-006: safeguards not shown sufficient | REP | R:728,892,962 |
| M07 | IP:18-20,72 | PASS applies to writing synthesis only | REP | R:494 |
| M08 | IP:65 | Self-audit unknowns | REP | R:946-948 |
| M09 | IP:66 | Carry forward contested; no Round 3 | REP | R:709 |

### N. base-selection and score-source-manifest (12 items)

| ID | Source | Distinct item | Status | Report location or equivalent |
|---|---|---|---|---|
| N01 | BS:5 | Writing base only; not likelihood | REP | R:492,718 |
| N02 | BS:7-34 | Quantitative writing metrics and scores | DEDUP | R:718 numeric writing order |
| N03 | BS:36-123 | Qualitative 30-criterion totals 24/25/25/25/26 | DEDUP | R:718; mechanically matched to SM forward and reverse counts |
| N04 | BS:125-137 | 150/150 forward and reverse agreement | REP | R:1305 |
| N05 | BS:139-150 | Combined scores; order V4,V5,V2,V3,V1; V1 lowest | REP | R:718 |
| N06 | BS:150,155 | Tiebreak path | REP | R:492 |
| N07 | BS:153 | V4 is not the most likely cause | REP | R:492 |
| N08 | BS:157-168 | Strengths to preserve and incorporate | REP | R:522,549,576,603-609,627 |
| N09 | BS:170-171 | Separate causal comparison; disputes; coexisting; no cure | REP | R:675-702,717 |
| N10 | BS:173-562; SM:105-2247 | 300 claim-evidence-verdict writing records | DEDUP | Restate card content in D-H; summary at R:718,1305; no differing conclusion |
| N11 | BS:123,577 | Correctness MET is within supplied cards; agreement is not causal truth | REP | R:495-496,718 |
| N12 | SM:2,27,2248-2285 | Purpose; Round 2 A-001 vector; contested pairs; scores do not drive ranking | REP | R:492,503,702 |

### O. refactor-plan (8 items)

| ID | Source | Distinct item | Status | Report location or equivalent |
|---|---|---|---|---|
| O01 | RP:3-10 | Overview: target, rule, 10/10 not causal | REP | R:478,490,499-502,664 |
| O02 | RP:24 | User asked for likelihood; records support evidence-weighted judgment | REP | R:88,716 |
| O03 | RP:27-33 | Ordering table; V5 directness breaks narrow tie provisionally | REP | R:675-681,706 |
| O04 | RP:35 | Dissent; two-thirds threshold; display is not consensus | REP | R:685-707 |
| O05 | RP:38-78 | Change obligations, including that a safeguard is not a demonstrated cure | REP | R:510-641,736,892,962,1112 |
| O06 | RP:80-88 | Changes not made | REP | R:717-720,736,1056 |
| O07 | RP:90-100 | Risk summary | REP | R:474,707,962 |
| O08 | RP:102-107 | Plan auto-approved, not user-approved | DEDUP | R:88,716 record the user's later acceptance of the order |

### P. plan-review-evidence (4 items)

| ID | Source | Distinct item | Status | Report location |
|---|---|---|---|---|
| P01 | PR:9-19 | Independent review PASS; order and dissent retained | REP | R:706,1112 |
| P02 | PR:4 | Raw versus normalized hash-label correction | REP | R:1112 |
| P03 | PR:27-36 | Source-directory guard; 29 links | REP | R:1112 |
| P04 | PR:70-74 | Transcript-input review, not a new analytical review | REP | R:1112 |

### Q. merge-log (8 items)

| ID | Source | Distinct item | Status | Report location or equivalent |
|---|---|---|---|---|
| Q01 | ML:9-14 | Eight changes composed; executor wrote no file | REP | R:1113,1115 |
| Q02 | ML:26-96 | Change validations | REP | R:549-553,576,603,623,736 |
| Q03 | ML:102-109 | Post-merge validation details | REP | R:496,1117,1156 |
| Q04 | ML:130-144 | Contradiction re-scan zero | REP | R:1117,1156 |
| Q05 | ML:161-163 | Canonical FAIL then PASS | REP | R:1113,1000 |
| Q06 | ML:176 | Approval was not user approval | DEDUP | R:88,716 (same as O08) |
| Q07 | ML:180-184 | Executor verification hiccups with no content effect | DEDUP | R:279, Section 2.6 class exclusion of producer recovery errors |
| Q08 | ML:188-196 | Real artifacts; partial; no completion claimed | REP | R:1191,474 |

### R. gaps-and-questions (26 items)

| ID | Source | Distinct item | Status | Report location or equivalent |
|---|---|---|---|---|
| R01 | GQ:11 | Population and selection; no prevalence | REP | R:116-121,309,945 |
| R02 | GQ:12 | Historical edits and fixtures partly reconstructable | REP | R:957,902 |
| R03 | GQ:13 | Historical loads versus installed copies | REP | R:229,326,834,964 |
| R04 | GQ:19 | Text-only screening agents; main persists | REP | R:110 |
| R05 | GQ:20 | Skeleton overwrite and recovery | REP | R:1062 |
| R06 | GQ:21 | Read offset failure on a 73-line file | DEDUP | R:279 class exclusion |
| R07 | GQ:22 | Recovered files absent before recovery | REP | R:1044,1062 |
| R08 | GQ:23 | BUILD-REQUEST freshness-hook block | DEDUP | R:279 class exclusion |
| R09 | GQ:24 | Graph coverage unavailable; direct reads | REP | R:1311 |
| R10 | GQ:25 | Replay assertion; four placeholders kept | REP | R:1044 |
| R11 | GQ:26 | 5 of 15 spawns failed on lock contention | DEDUP | R:279 class exclusion |
| R12 | GQ:27 | Logs grew after observation | REP | R:147,352,961 |
| R13 | GQ:31 | 13/3 versus 14/2; duplicate and non-defect | REP | R:253,165 |
| R14 | GQ:33 | No-op versus patch-check contradiction | REP | R:255 |
| R15 | GQ:35 | Pre-fetched versus before-upstream contradiction | REP | R:256 |
| R16 | GQ:43 | CI endpoint update | REP | R:143,168 |
| R17 | GQ:44 | Monitor endpoint update | REP | R:144,169,954 |
| R18 | GQ:45 | Earlier misses unknown | REP | R:946 |
| R19 | GQ:47 | All 16 Orca repairs traced | REP | R:1030,271 |
| R20 | GQ:55 | Documentation navigation | REP | R:257 |
| R21 | GQ:56 | 7 equal, then 3 equal and 4 different | REP | R:258,327 |
| R22 | GQ:57 | Misses and updater unknown; confounding | REP | R:946-948 |
| R23 | GQ:58 | Runtime and platform not established | REP | R:952-956 |
| R24 | GQ:59 | Orca contradictions unresolved; v4 unreviewed | REP | R:949-950 |
| R25 | GQ:63 | Limits disclosed; nothing authorized | REP | R:295,324 |
| R26 | GQ:69 | CI 16/2 contradiction | REP | R:254 |

### V. Raw duplicate variants (5 items)

| ID | Source | Distinct item | Status | Equivalent |
|---|---|---|---|---|
| V1 | VA1:1-61 | Debated V1 body | DEDUP | hypothesis-01 (D01-D25); zero unmatched non-heading lines by `grep -v -x -F` |
| V2 | VA2:1-63 | Debated V2 body | DEDUP | hypothesis-02 (E01-E20); zero unmatched |
| V3 | VA3:1-62 | Debated V3 body | DEDUP | hypothesis-03 (F01-F20); zero unmatched |
| V4 | VA4:1-62 | Debated V4 body | DEDUP | hypothesis-04 (G01-G20); zero unmatched |
| V5 | VA5:1-60 | Debated V5 body | DEDUP | hypothesis-05 (H01-H17); zero unmatched |

## Omissions Found

| # | Source finding | Source file | Status | If deduped, by which report item | Severity | Recovery |
|---|---|---|---|---|---|---|
| 1 | The V1 discriminating test has a separate step: for each later finding, verify whether the relevant behavior test was deferred or absent. This step tests the deferred-test amplifier. | `synthesis/hypothesis-01.md:142` (verbatim from `reviews/adversarial/adversarial/variant-1-original.md:42`); identified as part of the test at `reviews/adversarial/adversarial/base-selection.md:233,546` | OMITTED | n/a | MINOR | In Option A Falsification (R:527), and in Section 8 step 2.1 Action (R:872), add after "run the check actually used against it": "and separately verify whether the relevant behavior test was deferred or absent." The report keeps steps a, b, d and e of the test but not this one. |
| 2 | What the credential rubric change was: "Old rule treats stale evidence as issues; later rule says moved line alone is not issues and changes acceptance handling." The report keeps that two rubric texts were loaded, their hashes, timing, provenance and the confounding. It never says what changed, so a reader cannot see that the change, made before the final pass, bears on stale or moved evidence citations and on acceptance handling. | `synthesis/hypothesis-03.md:57`; `reviews/adversarial/merged-root-cause-analysis.md:73`. The originating family is Partition 1, `research/scope-rules.md:70-71` (earlier rubric :65 and :79; later rubric :66-68 and :82). | OMITTED | n/a | IMPORTANT | In Section 2.3 (R:229, after "consecutive credential FINAL reviewers load materially different rubrics") and in Option C Support (R:577, after "Two different rubric texts"), add: "The two captured texts differ in substance: the earlier rubric (loaded 20:26:30.085Z, `0b533765…`) treats stale evidence as issues, while the later rubric (loaded 20:32:19.277Z, `faff03b7…`) says a moved line alone is not an issue and changes acceptance handling (`synthesis/hypothesis-03.md:57`; `reviews/adversarial/merged-root-cause-analysis.md:73`)." For clause-level detail, Step 6.38 should merge with Partition 1's ownership of `research/scope-rules.md:70-71`. |
| 3 | The broader-hardening contract mechanism in the monitor reviews. Besides uncapped fields, some findings concerned case-insensitive matching that was not clearly required, and the per-review prompts required any defect of any severity to be returned noncompliant. The report keeps only "uncapped fields absent from the plan". | `synthesis/hypothesis-03.md:59`; case-insensitive example also at `reviews/adversarial/merged-root-cause-analysis.md:77`. The originating family is Partition 2 (monitor case, sections 4-5). | OMITTED | n/a | MINOR | In Option C Support (R:577), after "uncapped fields absent from the plan (records 906, 1143)", add: "and case-insensitive matching not clearly required; the per-review prompts required any defect of any severity to be noncompliant (`synthesis/hypothesis-03.md:59`)." |

## Summary

- Findings enumerated: 406, all from Partition 4 inputs, with no sampling.
- Represented: 383. Covered-by-dedup: 20. Omitted: 3 (1 IMPORTANT, 2 MINOR).
- Reconciliation: 383 + 20 + 3 = 406. By section:

| Section | Represented | Dedup | Omitted | Total |
|---|---:|---:|---:|---:|
| A | 99 | 0 | 0 | 99 |
| B | 25 | 0 | 0 | 25 |
| C | 35 | 0 | 0 | 35 |
| D | 24 | 0 | 1 | 25 |
| E | 20 | 0 | 0 | 20 |
| F | 18 | 0 | 2 | 20 |
| G | 20 | 0 | 0 | 20 |
| H | 17 | 0 | 0 | 17 |
| I | 12 | 3 | 0 | 15 |
| J | 17 | 0 | 0 | 17 |
| K | 19 | 2 | 0 | 21 |
| L | 19 | 1 | 0 | 20 |
| M | 9 | 0 | 0 | 9 |
| N | 9 | 3 | 0 | 12 |
| O | 7 | 1 | 0 | 8 |
| P | 4 | 0 | 0 | 4 |
| Q | 6 | 2 | 0 | 8 |
| R | 23 | 3 | 0 | 26 |
| V | 0 | 5 | 0 | 5 |
| **Total** | **383** | **20** | **3** | **406** |

- Mandatory survivals confirmed:
  - All five hypotheses' mechanisms, support, counterevidence, alternatives, scope, falsification and limits are present in Options A-E (R:510-641).
  - The actual debate outcomes are present: order V1 > V3 > V2 > V5 > V4 labeled non-consensus (R:665,675-681); V1 first 5/5; V3 above V2 3/5; V4 above V5 3/5, with the displayed V5 above V4 on the 2-of-5 side (R:695-708; R:1285).
- **Verdict: FAIL (3 omitted).**

## Limitations

- **Process metadata not enumerated as findings,** because it carries no cause, support, disconfirmation, ranking reason, check or question:
  - Debate execution details: roster rejection of named calls and no N-1 fallback (DT:11; SM:27); Round 1 parallel and Round 2 sequential order (DT:6); current-model-default advocates (DT:10; RC:26; RP:4; ML:5; BS:153).
  - Identifiers: extraction paths, UUIDs, hashes and byte counts.
  - Card presentation material: chapters 3-5 and sections 10.3-10.5 (format-only N/A notes, read inventories, persistence receipts).
  - The provenance ranges S4:342-368, S5:136-162 and S6:269-289 named by the input map.
- **Judgment calls for Step 6.38:**
  - L08: Round 1 writing-label diversity is treated as dedup into the final Round 2 writing outcome.
  - R06, R08, R11 and Q07: research-process hiccups are treated as covered by the report's class-level exclusion of producer recovery errors (R:279).
  - A69, A95 and A96: deliberate revisions between synth-04 and the report (Option D effort S to M, the "Cheap" Pros wording, the 7.6 decision rules) are treated as represented, not omitted.
- **Cross-partition ownership:** omission 2 originates in Partition 1 (`research/scope-rules.md:70-71`, `research/historical-review-rules.json`), and omission 3 originates in Partition 2 (monitor case). Under the input map's Method rule 2, they are reported here because Partition 4 inputs restate them; Step 6.38 should deduplicate them and keep the originating partition.
- **Known defects not recounted:** J1, L1, L2 and L3.
- **Checks performed:**
  - Full Reads of all inputs and the report.
  - Report sha256 re-verified.
  - Every variant body line confirmed verbatim in its card (`grep -v -x -F`, zero unmatched).
  - score-source-manifest forward and reverse MET counts confirmed equal to base-selection (jq).
  - Absence greps on the report for each omission's wording ("stale evidence", "acceptance handling", "any severity", "case-insensitive", "deferred or absent", "absent or deferred"): no match.
- No file was edited, no Git command was run and no session `.jsonl` was opened.

| Status | Result |
|---|---|
| DONE | Enumerated all 406 distinct Partition 4 findings and classified each by meaning: 383 represented, 20 covered by dedup, 3 omitted. Counts reconcile. |
| DONE | Found 3 genuine omissions with recovery text and source lines: what the credential rubric change was (IMPORTANT); the V1 test's deferred-or-absent step (MINOR); the monitor any-severity prompt rule and case-insensitive example (MINOR). |
| NEXT | Parent persists this text verbatim at `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-anti-omission-report-4.md`; Step 6.38 consolidates it with Partition 1 and 2 ownership for omissions 2 and 3. |