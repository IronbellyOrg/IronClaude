# Anti-Omission Report: Partition 2

Verdict: FAIL

**Report reviewed:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/RESEARCH-REPORT-review-loops.md`. I read all 1,313 lines. The sha256 is `a10cef088fb1be687fc65a72553910a8a522b4ef8eccb8081e4e2e48972469c7`, checked at the start of this run and again at 2026-10-24T17:12Z.
**Input files checked (Partition 2, all ranges, no sampling):**
- `research/01-session-ac2cd1fd.md` (1-442)
- `research/02-session-a9b88895.md` (1-314)
- `research/03-session-6f744b87.md` (1-362)
- `research/04-session-43582de1.md` (1-615)
- `research/05-session-e002bed2.md` (1-502)
- `research/06-session-0690ee9f.md` (1-387)
- `research/deep-handoffs-first-source.txt` (1-675)
- `research/deep-handoffs-remaining-source.txt` (1-891)

The raw captures were compared line by line with their case reports using `diff` on the mapped segments. Only substance that exists solely in the raw text was enumerated separately (rows 68, 107, 196, 254, 295).
**Total findings enumerated:** 295
**Date:** 2026-10-24
**Governing template:** `/config/.claude/skills/tech-research/SKILL.md:1196-1239` (Anti-Omission Agent Prompt and output format)
**Method:** Coverage was judged by meaning only, never by ID or citation. "Represented" means the substance appears in the report. "Covered-by-dedup" means the substance has an exact semantic equivalent, or falls under an explicit, reasoned exclusion in the report (Report:271, 274, 379, 382). Case recommendations to build remediation are out of scope under `BUILD-REQUEST.md:14,35` ("not another speculative remediation loop"; "research-only"). The known user-accepted defects J1, L1, L2 and L3 (`phase-outputs/discovery/anti-omission-input-map.md:17-21`) are not counted as new omissions.

## Full Enumeration

Key: R = REPRESENTED, C = COVERED-BY-DEDUP, O = OMITTED. "Report:N" means a line in the final report.

### Case 01: Orca planning (`research/01-session-ac2cd1fd.md`)

| # | Source finding (distinction) | Kind | Source | Class | Report location or equivalent |
|---|---|---|---|---|---|
| 1 | Mixed-cause loop: not twenty regressions after sixteen fixes | causal class | 01:14-21, :421 | R | Report:165, 271, 287 |
| 2 | Two full reflection runs plus one targeted review, not three full cycles: partial, partial, PARTIAL | transition | 01:23 | R | Report:129 |
| 3 | First review: sixteen findings, status partial, two citations dropped and no finding dropped | transition | 01:68 | R | Report:165 (sixteen findings) |
| 4 | User authorized applying all sixteen findings and rerunning the review | authority | 01:69 | R | Report:165 ("Authorized v2 rewrite") |
| 5 | v2 is a whole-file Write at 544, confirmed at 545 | transition | 01:70, :373 | R | Report:165, 846 |
| 6 | Second review: twenty items, partial, two high blockers, recommends a targeted review instead of a third full run | transition | 01:73 | R | Report:165 |
| 7 | User: "apply 01-20 as plan version 3", then Write 841 | authority/transition | 01:74-75 | R | Report:165 ("Authorized v3") |
| 8 | The structural gate at 843/849 checks shape only, not semantic correctness | validity | 01:76 | R | Report:530 |
| 9 | Orchestrator recommended narrowing (856); user authorized it (858); one reviewer checked the two blockers | authority | 01:77-79, :305 | R | Report:165, 271 |
| 10 | The targeted review returns PARTIAL for both items and finds further omissions | transition | 01:80 | R | Report:165 |
| 11 | The persisted targeted verdict (877) is condensed and omits per-site detail kept in the returned review at 874 | uncertainty | 01:81, :253, :356 | R | Report:350, 891 |
| 12 | Recommendation to edit "without another review" relying on per-task QA (885); user authorized it (889) | authority | 01:82-83, :307 | R | Report:165 |
| 13 | Fifteen edits produce v4; it passes the structural gate; "NOT CHECKED: v4 has had no review" (hidden final) | hidden final | 01:84-86, :311 | R | Report:165, 530, 949 |
| 14 | Elapsed wall-clock intervals are not token costs | uncertainty | 01:88 | C | Explicit exclusion at Report:271, 379 |
| 15 | Count correction: 14 fixed and 2 partial, not 13 and 3; the summary omitted the repository-self-check item | validity | 01:92-97, :393, :398 | R | Report:253, 350 |
| 16 | The twenty items include a duplicate (N-02) and an explicit non-defect note (N-16) | validity | 01:99-102 | R | Report:165, 349 |
| 17 | The user authorized every amendment and the scope reduction; termination was not a clean review result | authority | 01:106-108 | R | Report:165, 291 |
| 18 | 3.1: moving the four-asset check into early detection introduced a behavioral divergence, and the first review itself proposed that stronger predicate | causal + earlier miss | 01:114-128 | R | Report:550 |
| 19 | 3.1: the "pin equals current is forbidden" subclaim was withdrawn as a contradiction | validity | 01:124, :210 | C | Report:241, 349 (withdrawn or rejected claims); per-item inventory excluded at :271 |
| 20 | 3.2: the old lock-digest source substitution was introduced, while the other old-value gaps were incomplete (mixed) | causal | 01:132-144, :208 | R | Report:550, 344, 311 |
| 21 | The field-9 requirement (Requirements:302, recipe state) conflicts with rollback separating recipe and deployed package; provenance could be the better source if approved | validity / source tension | 01:208, :299 | **O** | See Omissions #2 |
| 22 | 3.3: the inventory test was scheduled before route registration (introduced) | causal | 01:148-160, :215 | R | Report:550 |
| 23 | 3.4: the renderer test boundary was introduced, and the original integration gap remained | causal | 01:164-176, :209 | R | Report:550 |
| 24 | 3.5: the wrongly named fetch remote was introduced while refining an underspecified step | causal | 01:180-192, :224 | R | Report:550 |
| 25 | The first review's proposed fixes were not checked against the whole specification | earlier miss | 01:198 | R | Report:349 ("defective proposed repairs") |
| 26 | N-01: validation after external calls is a pre-existing defect found later | causal | 01:206 | R | Report:523, 271 |
| 27 | N-06, N-07, N-09, N-11: pre-existing test and interface gaps found later | causal | 01:211-216 | C | Report:165 ("old omissions"); inventory excluded at :271 |
| 28 | N-08: old issue unresolved, with a stronger fixture demand | causal | 01:213 | C | Report:165, 241 |
| 29 | N-12: current pin versus "Noop"; a pre-existing omission made worse by contradictory source text | causal / source tension | 01:217, :296 | R | Report:255 |
| 30 | N-13: changed review precision; the proposed YAML assertion was rejected | validity | 01:218 | C | Report:241, 349 |
| 31 | N-14: old finding unresolved; v3 declares owner-run live acceptance as the only coverage | causal | 01:219, :382 | C | Report:253 (the M-04 partial) |
| 32 | N-15: incomplete renderer-test fix | causal | 01:220 | C | Report:165 ("incomplete repairs") |
| 33 | N-17: introduced acceptance-executability gap ("same result as base" with no baseline capture task) | causal | 01:222, :389 | **O** | See Omissions #4 |
| 34 | N-18: pre-existing hygiene risk; the citation validator rejected a proposed claim | validity | 01:223 | C | Report:349 |
| 35 | N-20: incomplete old fix plus source inconsistency; the validator narrowed it | causal | 01:225 | C | Report:165, 349 |
| 36 | Earlier-miss reason 1: the coverage matrix credited the up-to-date state without proving it | earlier miss | 01:231-232 | R | Report:523, 343 |
| 37 | Earlier-miss reason 2: the matrix omitted the security and ordering clauses; a check existing somewhere is not a check before the fetch | earlier miss | 01:234-235 | R | Report:523, 271 |
| 38 | Earlier-miss reason 3: the specification's own test table had holes; the QA self-audit only matched that list | earlier miss | 01:237-238, :301 | R | Report:271 (stated in the exclusion cell) |
| 39 | Earlier-miss reason 4: introduced text needs no earlier-miss explanation | earlier miss | 01:240-241 | R | Report:240 |
| 40 | The remaining miss reasons are unknown; no cognitive cause is inferred | uncertainty | 01:243, :350 | R | Report:288, 946 |
| 41 | Targeted review: secondary tag sources are unfiltered; pre-existing | causal | 01:257 | C | Report:165 ("old omissions") |
| 42 | Targeted review: unsafe bad-value wording introduced in v3 | causal | 01:258 | R | Report:550 |
| 43 | Targeted review: the annotated-tag URL instruction is inherited from Source:158 and conflicts with check-before-use at Source:469; the v4 response was not independently verified | causal / source tension | 01:259, :298 | **O** | See Omissions #1 |
| 44 | Targeted review: fetch-level malformed-rollback case and missing mutations are incomplete repairs | causal | 01:260-262 | C | Report:165 |
| 45 | Targeted review: the `needs: detect` remark is a documentation clarification, not faulty wiring | validity | 01:263 | C | Report:349 (overclaims) |
| 46 | Targeted review: ill-defined condition mutation introduced in v3 | causal | 01:264 | R | Report:550 |
| 47 | Targeted review: pin and rollback no-op state value unspecified | causal | 01:265 | C | Report:255 |
| 48 | No runtime positive-control proof for the up-to-date week | uncertainty | 01:266, :349 | R | Report:255 |
| 49 | The contradiction between self-check-before-upstream-call and prefetched input is unresolved | source tension | 01:267, :297, :348 | R | Report:256, 950 |
| 50 | Four overstatements in the targeted return were narrowed, not counted as bugs | validity | 01:269-278 | C | Report:349, 241 |
| 51 | Continuation mechanism: review passes answered different questions; newly concrete interfaces exposed defects that had been underspecified rather than wrong | causal | 01:290, :188 | **O** | See Omissions #3 |
| 52 | Continuation mechanism: local fixes crossed component boundaries | causal | 01:292 | R | Report:549 |
| 53 | Continuation mechanism: stronger test demands accumulated beyond Source:477-479 | causal | 01:301 | R | Report:271, 241 |
| 54 | Stop: authorized narrowing (the cited reason was cost and diminishing test-strength findings) and enforcement deferred to implementation | authority / stop | 01:305-313 | R | Report:165, 291 |
| 55 | No basis to call v4 approved; the structural gate passes all four versions | validity | 01:318-319 | R | Report:530, 949 |
| 56 | Reconstruction hashes: v1 and v2 match their review snapshots, v4 matches the live plan, v3 has no comparison target | uncertainty | 01:323 | R | Report:533, 846 |
| 57 | Both full reviews used the same driving-source hash | control | 01:340 | R | Report:165, 578 |
| 58 | No runtime regression; later implementation artifacts do not prove execution here | uncertainty | 01:344-345 | R | Report:165 |
| 59 | Current GitHub concurrency documentation not verified (N-16 note) | uncertainty | 01:351 | C | Report:165 (non-defect note) |
| 60 | No stale-architecture claim; the real issues are conflicting instructions, a wrong count and a condensed verdict | validity | 01:356 | R | Report:263 |
| 61 | Case table "All sixteen first-round repairs", including several successful non-recurring repairs | control / table | 01:375-394 | R | Report:312, 551; detail excluded at :271 |
| 62 | "Fixed" means the next reviewer accepted the amendment, not that runtime behavior was correct | validity | 01:402 | R | Report:253 |
| 63 | M-11 applied the narrower detailed recommendation, not the broader top-level list | validity | 01:389 | C | Inventory exclusion at Report:271 |
| 64 | Blocked Edit 150/151 did not apply; the retry at 163/164 did | transition | 01:404-417 | R | Report:559, 846 |
| 65 | Recommended classification: mixed-cause churn with an unreviewed final amendment | causal class | 01:423 | R | Report:165, 768 |
| 66 | Resume identifiers for six transitions | provenance | 01:425-442 | C | Report:165 (transition chain); UUID tables excluded at :271 |
| 67 | Persistence note: main transcribed the return; not producer-written | provenance | 01:10 | R | Report:110, 1245 |
| 68 | Raw-only text: DONE/NEXT status lines and the original grouped cleanup entry, later corrected | raw | deep-handoffs-first-source.txt:2-9 and original timeline row | C | Corrected account at Report:559, 846 |

### Case 02: claim-gate oracle (`research/02-session-a9b88895.md`)

| # | Source finding (distinction) | Kind | Source | Class | Report location or equivalent |
|---|---|---|---|---|---|
| 69 | Two failed reviews, then a pass after an authorized fixture correction | transition | 02:13 | R | Report:130, 166 |
| 70 | The second failure kept one known frozen defect; no new requirement and no regression | causal | 02:13, :27-28 | R | Report:166 |
| 71 | Not counted: repeated deliveries, Task 11 carryover, two local test failures, archive refusal | exclusion | 02:17-22, :281-290 | R | Report:272, 380, 130 |
| 72 | Builder freeze order: freeze bytes first; no tuning from acceptance results | control | 02:79-81 | R | Report:629 |
| 73 | First FAIL at 291 with four findings (a truncated relay; the full review is in the artifact) | transition | 02:84 | R | Report:166 |
| 74 | Repair authority at 383 covers findings 1-3 only; fixture, hash, digest and tokens stay frozen; no duplicate coverage to hide the omission | authority | 02:85, :208 | R | Report:166, 628, 876 |
| 75 | Corrections applied; corrected return at 398 | transition | 02:86-89 | R | Report:166 |
| 76 | Second FAIL at 450 confirms the three repairs | transition | 02:91 | R | Report:166, 628 |
| 77 | Task recorded blocked; orchestrator asked for authorization that would invalidate earlier evidence | authority | 02:92-93 | C | Report:166, 272 ("superseded prior results") |
| 78 | Authorization at 521, one boolean changed at 573, assertion added at 579, pins at 585-586, PASS at 668 | transition / authority | 02:94-99 | R | Report:166, 628 |
| 79 | Archive blocked by a missing operator archive ruling; not a review failure | exclusion / authority | 02:102, :281 | R | Report:130, 272 |
| 80 | 4.1: unverified evidence selected rejection rows; valid; repaired; did not recur | validity | 02:112-130 | R | Report:272 |
| 81 | Textual table constants are not the executable predicates | earlier miss | 02:126, :234 | R | Report:343 |
| 82 | 4.2: the contrast varied the wrong causal factor | validity | 02:140-154 | R | Report:272, 523 |
| 83 | 4.3: missing-abstraction case was another import-cycle record | validity | 02:160-174 | R | Report:272 |
| 84 | The second reviewer judged the added structural positive necessary, not extra scope | validity | 02:174 | C | Report:166 ("not a new demand") |
| 85 | 4.4 origin: shared default `default_path=False` that the security constructor did not override | causal | 02:192 | C | Report:630 ("Ordinary incomplete work explains the original omission"), 728 |
| 86 | 4.4 is valid and was not invented by the reviewer | validity | 02:206 | R | Report:166 |
| 87 | Why the first repair could not fix it: the prohibition at 383 | authority | 02:208 | R | Report:628 |
| 88 | All four findings valid; three repaired; the recurring one is a frozen input | causal | 02:218-220 | R | Report:166, 176 |
| 89 | Test counts 67/78, then 74/85, then 74/85 | uncertainty | 02:226-230 | R | Report:166, 238 |
| 90 | Coverage checked structure more strongly than meaning | earlier miss | 02:235 | R | Report:238, 523 |
| 91 | Security grading could pass without the default-path fact | earlier miss | 02:236 | C | Report:238, 523 |
| 92 | The correction strengthened an assertion without adding tests; not cosmetic | validity | 02:242, :248 | R | Report:238 |
| 93 | No inherent contradiction; the fixture was satisfiable before freezing; the requirement was not impossible | validity | 02:252-256 | R | Report:166, 629 |
| 94 | After authorization: fixture and hash preserved, earlier results superseded, exactly one field changed | authority | 02:260-265 | R | Report:166, 272 |
| 95 | Independent byte comparison: only the boolean changed | control | 02:267 | R | Report:380 |
| 96 | No full pre-authorization oracle snapshot | uncertainty | 02:269, :295 | R | Report:957 |
| 97 | Corrected evidence is labeled re-frozen, not untouched | validity | 02:275 | R | Report:166 |
| 98 | Integration passed 255 default and 85 acceptance tests | detail | 02:279 | C | Report:380 (test totals not used as completeness measures) |
| 99 | No live-model effectiveness claim | uncertainty | 02:294 | R | Report:956 |
| 100 | Task 11 carryover is not an independent observation | exclusion | 02:296 | R | Report:272 |
| 101 | Graph index excluded the worktree; direct reads used instead | method | 02:71, :297 | C | Report:109 |
| 102 | No stale documentation; the live fixture differs on purpose | validity | 02:302 | R | Report:263 |
| 103 | The second failure was predictable; the operator decision removed the blocker | causal | 02:106-108 | R | Report:166, 628 |
| 104 | Recommended class: retained frozen-input defect requiring authorization | causal class | 02:308 | R | Report:166 |
| 105 | Resume identifiers | provenance | 02:314 | C | Report:166 |
| 106 | Case table "Evidence register" (paths) | table | 02:30-72 | C | Report:534, 844 |
| 107 | Raw-only text: status lines, otherwise identical | raw | deep-handoffs-first-source.txt:367-374 | C | Same substance in rows 69-104 |

### Case 03: manual-page rendering and baseline (`research/03-session-6f744b87.md`, no raw capture exists)

| # | Source finding (distinction) | Kind | Source | Class | Report location or equivalent |
|---|---|---|---|---|---|
| 108 | A real execution and repeated-review case | scope | 03:32 | R | Report:167 |
| 109 | Task 6: environmental verification blocker; not a new bug and not an unsupported finding | causal class | 03:37 | R | Report:167, 628 |
| 110 | The render clause came from the generated plan, not the inline source | authority | 03:49 | R | Report:635 |
| 111 | Sequence 406-450: edits, checks, cannot-verify, static-only evidence, cannot-verify again | transition | 03:55-62 | R | Report:167, 628 |
| 112 | The reviewer named two exits (a real render or an acceptance ruling) and said it cannot grant the ruling | authority | 03:66-68 | R | Report:623 |
| 113 | `/usr/bin/man` is a notice script; no renderer present; 275-byte notice | causal | 03:72-86 | R | Report:628, 859 |
| 114 | The initial check looked successful because output was redirected and only `rc=0` was saved | earlier miss | 03:88 | R | Report:628 |
| 115 | Not untestable in principle; not executable here; weak guard; requirement not invented; no malformed-roff defect | validity | 03:92-96 | R | Report:347, 629-630 |
| 116 | The evidence-only patch did not satisfy the criterion | validity | 03:100-102 | R | Report:167 |
| 117 | Static slice 187-195 is narrower than the 11-line insertion 186-196; recorded ranges miss the first and last lines | uncertainty | 03:104, :142 | **O** | See Omissions #5 |
| 118 | Before and after blobs; 11 inserted lines; delivered hash | control | 03:121-137 | R | Report:8, 324, 167 |
| 119 | Ledger lines 14-18 sequence | hidden final | 03:150-156 | R | Report:860 |
| 120 | `head-moved` comes from a missing HEAD file the scripts never wrote; the guard treats missing as moved | validity | 03:160-169 | R | Report:260, 351 |
| 121 | At 496: no advisers ran and nothing was reverted | transition | 03:171 | R | Report:351 |
| 122 | Wrong-task consent refused; correct consent then given | authority | 03:175-177 | R | Report:167, 348 |
| 123 | Ruling keeps cannot-verify; FINAL told to check the gap; pass keeps the unmet clause; final response says unverified | accepted gap / hidden final | 03:178-182 | R | Report:131, 167, 860 |
| 124 | The loop ended through informed acceptance | stop | 03:186-188 | R | Report:167 |
| 125 | Task 2 baseline rebuilt from HEAD after editing | causal | 03:190-210 | R | Report:167, 346 |
| 126 | Independent check against the retained Git trees | control | 03:214-239 | R | Report:167, 604 |
| 127 | The reviewer at 234 relied on the executor's account | validity | 03:243-251 | R | Report:167 |
| 128 | The `extra` verdict was justified by the wrong diff but found no actual extra work | validity | 03:252 | R | Report:346 |
| 129 | Task 2 is separate from the Task 6 blocker | causal class | 03:258 | R | Report:167 |
| 130 | Other reviews and exclusions (later validator, later planning) | exclusion | 03:262-272 | R | Report:273 |
| 131 | Later finding: interactive PATH ordering can bypass the wrapper; a different issue | causal | 03:274 | R | Report:273 |
| 132 | Two repeated-review cases; no unlimited retry cycle | causal | 03:278-280 | C | Report:167, 273 |
| 133 | Gaps: no real render, no HEAD file, no CI render result | uncertainty | 03:298-300 | R | Report:953, 1068 |
| 134 | Reviewer child-session logs not inspected; older analysis used only for provenance | method | 03:301-302 | C | Report:98, 109 |
| 135 | No stale documentation | validity | 03:310 | R | Report:263 |
| 136 | Recommended: two separate mechanisms; the accepted gap is not a render | causal class | 03:318-320 | R | Report:167, 770 |
| 137 | Resume identifiers | provenance | 03:322-339 | C | Report:167 |
| 138 | Current location mapping: three hashes match; old path gone; nothing else re-verified; no reason inferred | uncertainty | 03:341-362 | R | Report:257, 638, 862 |

### Case 04: regenerated CI plan (`research/04-session-43582de1.md`)

| # | Source finding (distinction) | Kind | Source | Class | Report location or equivalent |
|---|---|---|---|---|---|
| 139 | Most problems fixed; partial repairs; tooling exemption added to status but not hash checking | causal | 04:14 | R | Report:168, 344 |
| 140 | Search filters specified but not verified; missed before and survived | causal | 04:14, :170-176 | R | Report:523, 872 |
| 141 | Four "new medium" findings are not four regressions; two were downgraded | validity | 04:16 | R | Report:551 |
| 142 | Graph defect is the strongest introduction; the sequential executor prevents runtime reordering | causal | 04:16, :210-229 | R | Report:168, 555 |
| 143 | No implementation or product regression observed | uncertainty | 04:20 | R | Report:168 |
| 144 | Original window: 03:41:52, 1,000 rows, probe still running | window | 04:66-87 | R | Report:143 |
| 145 | Eight skill invocations; the printed implementation command was marked "not run" | exclusion | 04:81 | C | Report:168 |
| 146 | 18 is a deduplicated count; the probe had 19 entries; 14 report sections are aggregation | counting | 04:110-112 | C | Report:102, 136 |
| 147 | Repeated debate statements are not new discoveries | counting | 04:116 | R | Report:102 |
| 148 | "16 fixed, 2 partial" was intermediate; the contradiction is preserved | validity | 04:117-121 | R | Report:254 |
| 149 | Case table of the original 18 dispositions | table | 04:127-146 | C | Report:274 exclusion; M-05 at :254; M-15 at :274 |
| 150 | Reviewer 1 read the whole-document concern too broadly and conceded | validity | 04:148, :182-190 | R | Report:168, 254 |
| 151 | Substantial repair, not wholesale failure | control | 04:152 | R | Report:274, 382 |
| 152 | 6.1: incomplete repair; hash exposure pre-existing; 48 reported entries are not a baseline | causal | 04:158-168 | R | Report:552 |
| 153 | 6.2 earlier miss: the recorded remedy covered only creation arguments; the reason is unknown | earlier miss | 04:180 | C | Report:288, 523 |
| 154 | 6.4: directory allowlist is an inherited source/check mismatch, downgraded | validity | 04:192-202 | R | Report:168 |
| 155 | "New" means newly detected, not newly introduced | validity | 04:206 | R | Report:241 |
| 156 | Original serial chain was safe; repointing advice; prose "number order" substitute | causal | 04:214-227 | R | Report:344, 555 |
| 157 | Renumbering repair was proposed, not applied | transition | 04:233 | R | Report:274 |
| 158 | Mechanism: requirements stronger than checks | causal | 04:239 | R | Report:343 |
| 159 | Mechanism: declared complete without item-by-item verification | causal | 04:243 | R | Report:168 |
| 160 | Mechanism: review findings needed correction | validity | 04:245 | R | Report:349 |
| 161 | Mechanism: "ready with notes" inconsistent with findings | validity | 04:247 | R | Report:168 |
| 162 | Not context exhaustion or reviewer count | uncertainty | 04:251 | R | Report:294 |
| 163 | Original specification intact; regenerated source is the original plus feedback | authority | 04:255 | C | Report:168 |
| 164 | Tooling-output exemption explicitly disclosed as a necessary deviation, not a concealed scope expansion | authority | 04:256 | **O** | See Omissions #6 |
| 165 | README contradictions outside the designated paragraph were accepted by the specification | accepted gap | 04:257, :275 | C | Report:349 (withdrawn objections), 263 |
| 166 | No extra workflow edit or scope violation observed | uncertainty | 04:258 | R | Report:168 |
| 167 | Gaps: no proof of real failures; external docs not re-researched; no later refactor inferred | uncertainty | 04:266-271 | R | Report:951, 274 |
| 168 | Completed review: not-ready, 5 medium, 11 low, no high; partial status from citation drops (hidden final) | hidden final | 04:286 | R | Report:143, 168 |
| 169 | Final response asks for a second refactor or acceptance; no user decision | authority | 04:288, :333 | R | Report:168 |
| 170 | "Partial" does not mean still running; two citations dropped and corrected | validity | 04:301-314 | R | Report:168, 382 |
| 171 | Draft at 03:46:28, final at 03:47:57 | detail | 04:337 | C | Report:143 |
| 172 | 16 merged final items are not 16 runtime bugs; probe entries not added | counting | 04:341, :362 | R | Report:136, 274 |
| 173 | D-002 also includes unchecked push-before-search sequencing | causal | 04:346 | C | Report:523 (same merged search finding) |
| 174 | D-004 confinement: pre-existing, forwarding made explicit, not introduced, no mutation | causal / validity | 04:348, :368-408 | C | Report:168 ("old acceptance weaknesses survive"), 951 |
| 175 | D-005 half-edited header: pre-existing weakness surviving an incomplete repair | causal | 04:349, :410-440 | R | Report:523 |
| 176 | D-006 rename: incomplete repair; the advised path order was wrong and corrected | causal / validity | 04:350, :522 | R | Report:254, 349 |
| 177 | D-007: immutability checked only by decision-line count; a verification gap on the repair's new promise | causal | 04:351, :524, :547-559 | **O** | See Omissions #7 |
| 178 | D-008: inherited over-strict job-name check; two card claims wrong | causal / validity | 04:352, :523, :535-545 | C | Report:168, 349 |
| 179 | D-009, D-014, D-015, D-016: retained pre-existing weaknesses | causal | 04:353-360, :602-605 | R | Report:168 |
| 180 | D-010: angle-bracket check wording ambiguity introduced while resolving placeholders | causal | 04:354, :525 | **O** | See Omissions #8 |
| 181 | D-011 and D-012 optional | validity | 04:355-356 | R | Report:168 |
| 182 | D-013 / R2-7: rejected literal-advisory claim | validity | 04:357, :526 | R | Report:349 |
| 183 | Final report repeats 16/2; must not reclassify optional hardening | validity | 04:366 | R | Report:254 |
| 184 | Probe hazards in proposed repairs; corrects the earlier debate; disclosed deviation | validity | 04:444-456 | R | Report:274 |
| 185 | Updated endpoint identities | window | 04:460-467 | R | Report:143 |
| 186 | Plan modification times unchanged; proposed fixes not applied | transition | 04:478 | R | Report:168, 274 |
| 187 | Return-contract input-tree hash; no input drift | provenance | 04:491 | C | Report:848 |
| 188 | Synthesis implication: regeneration did not fully repair; probe concerns are not regressions | causal | 04:495 | R | Report:168 |
| 189 | R2-1: the reviewer's proposed repair was itself incomplete | validity | 04:520 | R | Report:349 |
| 190 | R2-2: overclaimed | validity | 04:521 | R | Report:168 |
| 191 | R2-8: matrix bookkeeping, not a plan defect | validity | 04:527 | R | Report:349 |
| 192 | Counting and uncertainty; earlier misses unknown | uncertainty | 04:563-573 | R | Report:274, 288 |
| 193 | Summary and recommended action | causal class | 04:577-579 | R | Report:168 |
| 194 | Withdrawn R1-8 and R1-9 | validity | 04:609-610 | R | Report:349, 382 |
| 195 | Resume identifiers | provenance | 04:583-594 | C | Report:168 |
| 196 | Raw-only text: "review had not finished" endpoint and original recommendation | raw | deep-handoffs-remaining-source.txt:7, :263 | R | Report:143, 382 |

### Case 05: Orca monitor Task 12 (`research/05-session-e002bed2.md`)

| # | Source finding (distinction) | Kind | Source | Class | Report location or equivalent |
|---|---|---|---|---|---|
| 197 | One invocation; repeated reviews of the same task | causal class | 05:14, :50 | R | Report:383 |
| 198 | Rows 1-1247 boundary, separate from the 03:25:59 selection time | window | 05:16, :319-335 | R | Report:144, 147 |
| 199 | 7 verdicts; 5 repairs (1 automatic, 4 operator-authorized); 4 "fix" replies; reviewer and halt counts | counting / authority | 05:18-22 | R | Report:133, 169 |
| 200 | No Task 12 retry-ladder, adviser or revert records | uncertainty | 05:23 | R | Report:169, 292 |
| 201 | Most later findings pre-existed; one regression | causal | 05:25 | R | Report:169, 523 |
| 202 | Migration explains why the compliant result did not finish the task | causal | 05:27, :223-236 | R | Report:169, 577 |
| 203 | Task 12 combined many jobs; 640 lines | causal | 05:54-56 | R | Report:169, 962 |
| 204 | First three criteria structural; behavior tests deferred to Task 14 | validity | 05:58 | R | Report:237, 523 |
| 205 | Prompt rules widened acceptance: "any defect of any severity" and "judge every bullet directly"; findings mixed suggested-command exactness (rename overlap), cosmetics (vhex, punctuation, grammar) and stricter keyword matching | authority / validity | 05:58, :132, :135, :145-146, :156, :238-250 | **O** | See Omissions #9 |
| 206 | Structural checks passed; the log is structural, overwritten, not a cumulative suite | uncertainty | 05:62-71, :297 | R | Report:920 |
| 207 | About 5 h 24 min waiting on the operator; not repair work | counting | 05:107 | R | Report:275, 383 |
| 208 | The compliant result was followed by a protocol-mandated review that found old defects | transition | 05:111 | R | Report:730 |
| 209 | At 804: older-pin and equal-tag discovery histories differ | validity | 05:119 | R | Report:169, 890 |
| 210 | Failed PR listing is a retained member of the error-propagation family | causal | 05:120 | C | Report:169 |
| 211 | At 906: pre-existing missed defects (patch, blank notes, upper bound, reversed link) | causal | 05:128-133 | C | Report:169 |
| 212 | Carriage-return escape reasoned from formatting rules, not rendered on GitHub | uncertainty | 05:131, :294 | **O** | See Omissions #10 |
| 213 | Evidence-log gap is repair-era, not fabricated execution | validity | 05:134 | C | Report:343 |
| 214 | Fields 8 and 10 have no size cap: a design gap | validity | 05:136 | R | Report:577 |
| 215 | At 1021: early pin summary family | causal | 05:142 | C | Report:169, 344 |
| 216 | 89-tag argument failure reproduced; about 70 tags is a fixture-dependent figure | uncertainty | 05:143, :148 | R | Report:275, 955 |
| 217 | Electron callout missing from its field | causal | 05:144 | C | Report:169 |
| 218 | At 1143: detect checkout family; timeout claim unverified | causal / uncertainty | 05:154 | R | Report:407 |
| 219 | Patch and lock hashes unchecked: incomplete earlier hardening | causal | 05:155 | C | Report:169 |
| 220 | Security output exceeds the body limit; not a plan deviation | validity | 05:157 | R | Report:577, 733 |
| 221 | About 9,000 tags is a theoretical ceiling | validity | 05:158 | R | Report:275 |
| 222 | Blocked edits 1164-1170 are not repairs | transition | 05:160 | R | Report:559 |
| 223 | At 1240: outage mislabel, a cross-component defect missed by the accepted helper | causal | 05:166 | R | Report:177, 367 |
| 224 | At 1240: links-only fallback design gap | causal | 05:167 | R | Report:733 |
| 225 | At 1240: error-trap regression proven | causal | 05:168 | R | Report:169, 550 |
| 226 | At 1240 (one of the four accepted defects): newline validator is retained or incomplete hardening, not a new vulnerability; reachability caveat | causal / validity | 05:169-171 | **O** | See Omissions #11 |
| 227 | 5.1: the same requirement rediscovered across five boundaries | causal | 05:179-191 | R | Report:344, 275 |
| 228 | 5.2: trap mechanism; the detect guard was not mirrored in the pin step | causal | 05:193-210 | R | Report:552, 732 |
| 229 | 5.3: size repairs exposed later limits rather than creating them | causal | 05:212-221 | R | Report:239, 733 |
| 230 | Ledger halt numbers do not count the verdicts | counting | 05:236 | R | Report:259, 350 |
| 231 | Authorization does not retroactively make items original violations | authority | 05:250 | R | Report:890 |
| 232 | Only one mechanism introduced a defect | causal | 05:254 | R | Report:169 |
| 233 | Controls: Tasks 10 and 11; the Task 10 helper missed an integration case | control | 05:256-271 | R | Report:177 |
| 234 | Troubleshooting session not counted and not shown as a cause | exclusion | 05:267, :298 | C | Report:107 |
| 235 | Ledger at 1244: the initial and compliant verdicts are absent from it | hidden final | 05:277-285 | R | Report:259, 350 |
| 236 | Last verdict "misunderstood"; stop at 1247; historical endpoint | window | 05:287 | R | Report:169 |
| 237 | Reproductions seen only through returned results; nothing rerun | method | 05:291 | C | Report:8, 935 |
| 238 | Runner permissions, dispatch, cancellation, queue and timeout unverified | uncertainty | 05:292-293 | R | Report:407, 952 |
| 239 | Size thresholds depend on fixtures; body limit unverified | uncertainty | 05:295-296 | R | Report:955 |
| 240 | Reused reviewer's usage must not be summed | uncertainty | 05:299 | R | Report:275 |
| 241 | No stale documentation; these are evidence-version limits | validity | 05:308 | R | Report:263 |
| 242 | Membership freeze is not a content freeze | window | 05:319-335 | R | Report:98, 314 |
| 243 | Fingerprints; the retrospective prefix hash is not a snapshot | uncertainty | 05:337-371 | R | Report:147, 961 |
| 244 | The current ledger must not be projected backward | window | 05:373-385 | R | Report:352 |
| 245 | Acceptance at 1250-1301 of four defects, verdict unchanged, no eighth review (hidden final) | accepted gap / authority | 05:389-411 | R | Report:169, 736, 954 |
| 246 | Consistent with the ledger acceptance rule | authority | 05:403-407 | R | Report:197 |
| 247 | Task 13 reviews are separate; missing HEAD file | exclusion | 05:413-425 | R | Report:260, 383 |
| 248 | Task 13 accepted gap (phrase repair, test rerun declined, `missing` verdict unchanged, no re-review) and its wording-expansion evidence | accepted gap / authority | 05:429-433, :448 | **O** | See Omissions #12 |
| 249 | Later acceptance changes the status, not the causal classes; the trap was accepted, not repaired | causal | 05:442-449 | R | Report:954, 443 |
| 250 | Earlier-miss reasons unknown; the trap explains behavior, not reviewer reasoning | uncertainty | 05:453 | R | Report:288, 946 |
| 251 | Summary: progressive discovery in a large unit | causal class | 05:461 | R | Report:772 |
| 252 | Recommended regression matrix and output-budget decision (remediation) | recommendation | 05:463 | C | Out of scope (`BUILD-REQUEST.md:14,35`); research-only stance at Report:663-667; output-budget gaps at :577, :733 |
| 253 | Case table "Reviewer identity and verdict mapping" | table | 05:487-502 | R | Report:169 |
| 254 | Raw-only text: original older-pin label and ledger framing, both later corrected | raw | deep-handoffs-remaining-source.txt:279-566 | C | Corrected account at Report:169 |

### Case 06: credential FINAL gates (`research/06-session-0690ee9f.md`)

| # | Source finding (distinction) | Kind | Source | Class | Report location or equivalent |
|---|---|---|---|---|---|
| 255 | Two independent final-review incidents | causal class | 06:13-18 | R | Report:170 |
| 256 | Initial package: issues, evidence fix, pass; no delivery change | transition | 06:17 | R | Report:178, 604 |
| 257 | Follow-up package sequence; rubric changed | transition | 06:18 | R | Report:134, 170 |
| 258 | Second failure was not fix-introduced; the Task 10 citation was already wrong | causal | 06:20 | R | Report:170, 604 |
| 259 | Delivery digests unchanged | control | 06:22-27 | R | Report:170, 244 |
| 260 | One real line shift, several citations wrong from creation, one criterion accepted too early | causal | 06:31 | R | Report:276, 346 |
| 261 | Not a controlled retry | uncertainty | 06:32 | R | Report:404 |
| 262 | Archives exist; hashes match the `PLAN:` records | provenance | 06:45-62 | C | Report:849 |
| 263 | User explicitly reopened Task 3 evidence only (record 396) before the initial repair | authority | 06:76 | **O** | See Omissions #13 |
| 264 | Task 3 reviewer isolated from the ledger; temporary files; executor cited README line 161, a table separator | causal | 06:84-94 | R | Report:604, 346 |
| 265 | First final was valid under the rule then loaded; the lint criterion itself held | validity | 06:96-104 | R | Report:178, 524, 605 |
| 266 | Root cause: temporary proof lost at the ledger handoff | causal | 06:129 | R | Report:346 |
| 267 | First follow-up FINAL findings: Task 6 literal failure, Task 8 moved line, Task 7 wrong location, Task 17 weak pointers | validity | 06:143-148 | R | Report:276, 346 |
| 268 | Task 6 relaxation chain 1215, 1219, 1230, then the reviewer | causal / authority | 06:156-175 | R | Report:170, 577 |
| 269 | Owner acceptance at 1935/1938/1968 names Tasks 7, 8 and 17 only | authority | 06:177-187 | R | Report:348, 893 |
| 270 | Task 10 blank `:10` citation created at 1425, flagged at 2012; the reviewer had read the correct log | causal | 06:189-212 | R | Report:604 |
| 271 | Task 7 repair range omits row 57 | validity | 06:214 | R | Report:604 |
| 272 | The second failure was caused mainly by an existing evidence defect | causal | 06:216 | R | Report:170 |
| 273 | Fixes at 2015 and 2016 with the same digest; overreach admitted at 2028; no new permission | authority | 06:220-222 | R | Report:348, 747 |
| 274 | Ledger omits the second failed FINAL; the third prompt's "recorded" wording is wrong | hidden final | 06:224-236 | R | Report:259, 1069 |
| 275 | Rubric line 79 versus line 82; acceptance-recording rules also changed | causal | 06:242-258 | R | Report:229, 577 |
| 276 | The pass follows both changes; effects cannot be separated; the updater is unknown | uncertainty | 06:262-266 | R | Report:404, 947-948 |
| 277 | Eight observations; the task-body omission is valid, pre-existing and not a failure cause | validity | 06:270-279 | R | Report:170, 276 |
| 278 | Historical content checked against tree d9f262a; today's worktree has changed | control | 06:283 | R | Report:8 |
| 279 | Method controls, including read-only Git object inspection | method | 06:289-295 | R | Report:8 (case-06 Git scope narrowness is the known defect L2) |
| 280 | Count exclusions: expected negative test failures; initial Task 1 unrelated-red "extras" result; follow-up plan regeneration is not a retry | exclusion | 06:299-301 | **O** | See Omissions #14 |
| 281 | Cosmetic observations are not code defects | exclusion | 06:302 | R | Report:276 |
| 282 | Gaps: updater unknown; temporary files lost; nonblank is not semantic support; archive verified but universal compliance not | uncertainty | 06:306-309 | R | Report:170, 947, 959, 1067 |
| 283 | Follow-up list positions are historical, not current defects | validity | 06:313-319 | R | Report:261, 384 |
| 284 | Reviewer transcript hashes | provenance | 06:321-334 | C | Report:170 |
| 285 | Earlier miss unknown; no cognitive cause | uncertainty | 06:337-341 | R | Report:276 |
| 286 | Summary | causal class | 06:345 | R | Report:170, 773 |
| 287 | Recommended durable-evidence and pointer checks (remediation) | recommendation | 06:347 | C | Out of scope (`BUILD-REQUEST.md:14,35`); target-state equivalents at Report:345-346, 350 |
| 288 | Resume identifiers, including nested record 116 | provenance | 06:349-365 | R | Report:170 |
| 289 | Observations 1-2 are cosmetic | validity | 06:375-376 | R | Report:276, 384 |
| 290 | Observation 3 was authorized by Task 17 | authority | 06:377 | R | Report:276, 384 |
| 291 | Observations 4 and 6 use equivalent wording | validity | 06:378, :380 | R | Report:276, 384 |
| 292 | Observation 5: load-order omission | validity | 06:379 | R | Report:170, 276 |
| 293 | Observation 7: acceptance artifact exists but no ruling line; not missing consent; not re-litigated | accepted gap / authority | 06:381 | R | Report:348, 893 |
| 294 | Observation 8: retained restart remark is accurate | validity | 06:382 | R | Report:276, 384 |
| 295 | Raw-only text: "five final reviews" status line and the superseded 19:57:18.651Z timestamp | raw | deep-handoffs-remaining-source.txt:570, :205 | C | Counts at Report:134, 170, 178; corrected timestamp at :604 |

## Omissions Found

| # | Source finding | Source file | Status | If deduped, by which report item | Severity | Recovery |
|---|---|---|---|---|---|---|
| 1 | The Orca source tells the executor to follow an annotated tag's upstream URL (`object.url`, Source:158), which conflicts with the rule that upstream values are checked before use (Source:469). The targeted reviewer classed the resulting finding as pre-existing and inherited from the source, not a v3 regression. The v4 response (require a 40-hex object digest and a fixed tag-object endpoint) received no separate independent verification. The report lists only two Orca source contradictions and says "Retain both Orca source tensions" (Report:255-256, 901, 950), so this third tension disappears. | `research/01-session-ac2cd1fd.md:259,298` | OMITTED | n/a | IMPORTANT | Add a third Orca source-contradiction row to Section 2.5. Change "both" to name all preserved tensions in the Section 8 Constraints row (Report:901) and in Question 6 (Report:950). Record the pre-existing classification and the unverified v4 response. |
| 2 | The field-9 requirement (Requirements:302) takes the old lock digest from recipe state, although rollback can separate recipe and deployed-package state. The case says provenance could be the better engineering source if explicitly approved. The report presents the digest-source switch only as an introduced defect (Report:550, 344). | `research/01-session-ac2cd1fd.md:208,299` | OMITTED | n/a | MINOR | Qualify the Option B "Digest source" support item: the substitution changed the declared field contract, but the requirement itself is in tension with rollback. |
| 3 | Continuation mechanism: successive review passes answered different questions. Corrections made collectors, regions, checks and ordering concrete, and later reviewers found defects in interfaces that had been underspecified rather than wrong. | `research/01-session-ac2cd1fd.md:290,188` | OMITTED | n/a | MINOR | Add this mechanism to the Orca account in Section 2.2 or Option B Scope, kept separate from "introduced" and "old defect". |
| 4 | N-17: v2 added "same result as on the base commit" comparisons without any baseline-capture task. The case classes this as an introduced acceptance-executability gap (the M-11 qualification). The report's list of Orca introductions (Report:550, 344) leaves it out. | `research/01-session-ac2cd1fd.md:222,389` | OMITTED | n/a | MINOR | Add it to the Option B "Further introductions in the case report" list. |
| 5 | Documentation Task 6: the static evidence slice covered lines 187-195, narrower than the 11-line insertion at 186-196, and the recorded line ranges miss the first and last inserted lines. The case calls this a small limitation that is not the cause. | `research/03-session-6f744b87.md:104,142` | OMITTED | n/a | MINOR | Add one clause to the documentation row of Section 2.2 or the Option E Support row: the static evidence also covered less than its "added lines" description. |
| 6 | The CI tooling-output exemption changed the original checking boundary but was explicitly disclosed as a necessary deviation in the feedback and the regenerated constraints, so it was not a concealed scope expansion (authority condition). The report mentions the exemption only as an incomplete repair (Report:344, 552). | `research/04-session-43582de1.md:256` | OMITTED | n/a | MINOR | Note in the CI row of Section 2.2 or 2.6 that the exemption was an authorized, disclosed deviation whose defect was incomplete coverage of the hash check. |
| 7 | CI D-007 (R2-5): the repair moved the decision note and banned later edits to the research file, but checks immutability only by counting decision lines. The case classes this as a verification gap attached to the repair's new promise: neither a regression nor a pre-existing weakness. | `research/04-session-43582de1.md:351,524,547-559` | OMITTED | n/a | MINOR | Add it to the CI residuals in Section 2.2 as a repair-era verification gap distinct from the graph introduction and the retained weaknesses. |
| 8 | CI D-010 (R2-6): the "no `<` placeholder" check wording was introduced by the repair while it tried to resolve placeholders. The case classes it as a repair-era wording ambiguity and finds no runtime regression. | `research/04-session-43582de1.md:354,525` | OMITTED | n/a | MINOR | Add it alongside #7 as the second repair-era wording gap. |
| 9 | The monitor acceptance boundary was wider than literal compliance. Review prompts said "any defect of any severity means noncompliant" and told reviewers to judge every Task 12 bullet directly instead of waiting for the deferred tests. The findings mixed in: exactness problems in commands the requirements suggested (the rename overlap behind `git diff --name-only`), cosmetic output issues (unused `vhex()`, punctuation, grammar) and a stricter keyword-matching interpretation. The report keeps only broader hardening, output-budget gaps and the "not retroactive" rule (Report:577, 890). | `research/05-session-e002bed2.md:58,132,135,145-146,156,238-250` | OMITTED | n/a | MINOR | Add the prompt-level rules and the three finding sub-types to the monitor rows of Section 2.2 or 2.6, or to Option C Support as the source of added scope. |
| 10 | The monitor carriage-return quote-escape finding was reasoned from formatting rules and never rendered on GitHub. | `research/05-session-e002bed2.md:131,294` | OMITTED | n/a | MINOR | Add it to the monitor unverified-behavior list in Section 5.1 (Report:407) or Question 8. |
| 11 | The fourth accepted monitor defect: provenance validators accept a trailing newline. The case classes it as retained or incomplete hardening with a mixed validator history, not a vulnerability introduced by the repair, and warns that not every cited validator is reachable because command substitution strips newlines. The report names the four accepted defects only as a count (Report:736). | `research/05-session-e002bed2.md:169-171` | OMITTED | n/a | MINOR | Name the four accepted defects in the monitor row of Section 2.2 with their classes, including this one. |
| 12 | Monitor Task 13 continuation: verdicts "misunderstood" and then "missing" although the 72-row acceptance test passed. The human requested a phrase repair and explicitly declined a test rerun, the executor recorded acceptance with the `missing` verdict unchanged, and no fresh re-review followed. The case cites this as further evidence of review-driven wording expansion. The report uses Task 13 only for the head-moved identity and for count exclusion (Report:260, 383). | `research/05-session-e002bed2.md:413-433,448` | OMITTED | n/a | MINOR | Add a sentence to the Section 2.1 out-of-window note or the monitor row of Section 2.6 recording this separate accepted gap, without adding it to Task 12 counts. |
| 13 | Initial credential package: the user explicitly reopened Task 3 evidence only (record 396) before the durable-proof repair (authority condition). This contrasts with the later Task 10 overreach. | `research/06-session-0690ee9f.md:76` | OMITTED | n/a | MINOR | Add the authorization at record 396 to the initial-package description in Section 2.2 or the Option D Support row. |
| 14 | Credential count exclusions: expected negative test failures are not loop failures; the initial Task 1 unrelated-red "extras" result is not a failed spec review; the follow-up plan regeneration is not another execution retry. | `research/06-session-0690ee9f.md:299-301` | OMITTED | n/a | MINOR | Add these exclusions to the "Deliberately not repeated" cell of the credential row in Section 2.6 or Section 4 Key Takeaway Coverage. |

## Summary

- Findings enumerated: 295 (Case 01: 68; Case 02: 39; Case 03: 31; Case 04: 58; Case 05: 58; Case 06: 41).
- Represented: 225. Covered-by-dedup: 56. Omitted: 14.
- Reconciliation: 225 + 56 + 14 = 295.
  - Case 01: 46 + 18 + 4 = 68
  - Case 02: 30 + 9 + 0 = 39
  - Case 03: 27 + 3 + 1 = 31
  - Case 04: 43 + 12 + 3 = 58
  - Case 05: 44 + 10 + 4 = 58
  - Case 06: 35 + 4 + 2 = 41
- Omission severity: CRITICAL 0, IMPORTANT 1 (#1), MINOR 13 (#2-#14).
- Known user-accepted defects not counted: J1, L1, L2 (relevant to row 279), L3.
- Verdict: FAIL (14 omitted).

## Limitations

- **Partition scope.** Cross-file checks covered only Partition 2's inputs. Restatements of these case families in Partition 3 (evidence-deck D3-D8) and Partition 4 (hypothesis cards, synth-04) were not checked here. Step 6.38 deduplicates them.
- **Excluded reads.** No Git command was run and no session `.jsonl` was opened. Statements about original JSONL records rely on the case reports and raw captures.
- **Raw captures.** These were checked with `diff` against their mapped case segments. Raw-only text was status lines, superseded classifications, the original CI pending endpoint and one superseded timestamp (rows 68, 107, 196, 254, 295). No other substantive raw-only content was found.
- **Covered-by-dedup judgments.** For per-item inventories (the 20 Orca N-items, the 18 CI concerns, monitor per-review findings), these rely on the report's explicit, reasoned exclusions (Report:271, 274, 379, 382) together with the class-level statements cited. A stricter reader could count more individual items as omitted, especially rows 19, 27, 30, 50, 173, 174 and 178.
- **Out of scope.** The case-level remediation recommendations (rows 252, 287) are treated as out of scope under `BUILD-REQUEST.md:14,35`, not as omissions.
- **Report version.** Report line numbers refer to the hash checked at the start of this run (`a10cef08...`). The same hash was confirmed again at 17:12Z.

## Self-Audit

Not applicable: omissions were found. I checked:
- every Partition 2 range, with all six case tables included;
- every raw-capture segment, by diff;
- keyword-in-context searches of the full report for each candidate omission, to confirm absence, including "annotated", "object.url", "field 9", "underspecif", "baseline" (Orca context), "187", "necessary deviation", "immutab", "angle", "any severity", "carriage", "trailing", "Task 13", "396", "reopen" and "extras".

| Status | Result |
|---|---|
| DONE | Enumerated 295 distinct Partition 2 findings across six case reports and two raw captures, each classified against the full report (sha256 `a10cef08...`). |
| DONE | Found 14 omissions (1 IMPORTANT, 13 MINOR), each with a source path, line and recovery text. Verdict: FAIL. |
| NEXT | The parent persists this text verbatim at `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-anti-omission-report-2.md`, then consolidates it at Step 6.38. |