# QA Report: Phase 6 Source-Fidelity Corrections

**Topic:** Repeated review failures after fixes in `/sc:workflow` plans and `/sc:implement` tasks (`R/RESEARCH-REPORT-review-loops.md`)
**Date:** 2026-10-24
**Phase:** Phase 6 fidelity gate, Step 6.29 (one serialized source-fidelity fixer)
**Fidelity fix cycle:** 1 of 2
**Package root (R):** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/`
**Mode:** `fix_authorization: true`, but the parent applies every write. I edited no package file. All patches were built and checked on private `/tmp` copies, and those copies have been deleted. I ran no Git command and did not open the parent session log `dfade920-…jsonl`. I read the other primary logs only by record number.
**Input:** `R/qa/qa-fidelity-consolidated-findings.md` (F-01 to F-10), the five fidelity reviews, the full report (1,310 lines, sha256 `9ac64f1353fb9a6ea228af727183d3434788807498219150a54275a84ad8e568`, re-measured before and after this work and unchanged on disk).
**User decisions applied (task log entry `[2026-10-24T06:32Z]`, task file :681):** F-05 "Keep, disclosed". F-02 "Disclosure only".
**Not fixed, by instruction:** J1, the stale status lines at Report:5, :1235 and :1287 (user-accepted, `phase-outputs/plans/report-gate-decision.md:116`).

---

## Overall Verdict

Verdict: FAIL

The input set fails: all 10 fidelity defects F-01 to F-10 are present in the current on-disk report. This step prepared a source-backed correction for every one of them. The patches are pending parent application. Steps 6.30 and 6.31 must then verify them independently. None of the corrections changes a rank, a ranked cause, the order V1 > V3 > V2 > V5 > V4 or any pair tally.

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | F-01 replay-row plan versions against the logged payloads | Defect confirmed; corrected | Orca log `ac2cd1fd…jsonl`, recomputed here: Write 141 alone hashes to `648c5578`. Write 141 plus Edit 163 hashes to `ebc03d45`, which is the v1 snapshot. Write 544 hashes to `d3a12ef9` and Write 841 to `cbfb606a`. `research/01-session-ac2cd1fd.md:323,330-332,410-413` |
| 2 | F-02 requested criterion against the delivered criterion | Defect confirmed; disclosure added | `BUILD-REQUEST.md:12,34`; task file :311, :379, :559 ("most-to-least likely"); `reviews/adversarial/adversarial/diff-analysis.md:64,69` |
| 3 | F-03 who decided the Phase 5 review skip | Defect confirmed; corrected | Task file :645 ("Parent judgment: … NOT run"); `phase-outputs/plans/synthesis-gate-decision.md:65` |
| 4 | F-04 coverage pointers in 2.6 and 7.7, and the authorized no-review edit | Defect confirmed; corrected | Orca records 858 ("have one fresh reviewer check only N-01 and N-12"), 885 ("without another review … per-task reviewer will hold each task to it") and 889 ("make the small edit"). `research/01-session-ac2cd1fd.md:237-238,301,303-313`. Grep shows "test table" and "Source:479" appear nowhere in the report, and "weaker source tests" appears only in the 2.6 claim |
| 5 | F-05 denial of the Coder Git object reads | Defect confirmed; disclosed per user decision | `research/03-session-6f744b87.md:121-131` ("I independently read both Git blobs"), `:212-250` ("using the earlier Git tree"); `report-gate-decision.md:115` |
| 6 | F-06 phantom "second reviewer" | Defect confirmed; corrected | Documentation log records 204, 222 and 234 all carry the same task id `a728a634771049499`; `screening-recovery-source.txt:76` ("Same reviewer returns `compliant`") |
| 7 | F-07 the CI "16 fixed, 2 partial" count survived debate | Defect confirmed; corrected and marked | Second-review `REPORT.md:21`; CI log 1052 (03:46:28.426Z) and 1084 (03:48:11.615Z) both carry the 16-of-18 text; `round2-v1.md:5,16,33`; `merged-verdict.yaml:8` and `consensus-summary.md:3` have no itemized cycle-0 list; case 04:117-118, :130, :143, :145, :294, :361 |
| 8 | F-08 monitor skill-load timestamp | Defect confirmed; corrected | Monitor log `e002bed2…jsonl`: record 14 at 19:29:17.282Z (user), 40 at 19:29:22.409Z, 42 at 19:29:22.708Z, 58 at 19:29:28.357Z |
| 9 | F-09 historical `ledger.md` bytes said to be "uncheckable" | Defect confirmed; corrected | Record 873 is a Read of the installed `ledger.md`. Record 874 (20:34:06.655Z) has startLine 1, numLines 243, totalLines 243 and content sha256 `bd66451d93910c97aac0b20a4d1c2f35b0452c96cbda24567cb731f09ceddeb8`. A diff against today's installed copy differs only at line 3 |
| 10 | F-10 provenance class of `scope-rules.md` and `scope-02.md`, plus the scope-04/05 residual | Defect confirmed; residual resolved; corrected | Rule-map record 79 (2026-10-23T03:31:40.642Z) is a 13,299-character status-table return. It has no `0b533765` hash and no "Recovered historical" section. `scope-rules.md:1,11,47,64-77`; `qa/qa-phase-2-fix-log.md:487-514`. `scope-02/04/05.md:8,11` each say "No producer-written report is claimed" and use their own title and sections, while the captures at `screening-handoffs-source.txt:214-232` (and the others) are status-table returns. All three are main-session summaries, not exact returns |
| 11 | Patch mechanics | PASS | 42 patches. Each `before` was asserted to occur exactly once at its turn, applied in array order. A fresh replay of the JSON on the live originals reproduced the `/tmp` after-hashes for all 6 files |
| 12 | Contradiction sweep on the patched copy | PASS after one round | Searched for "None was performed", "Steps 6.3-6.20", "likel", "intermediate", "corrected in debate", "corrected or changed", "skipped by", "second reviewer", "hash-check", "19:29:17Z", "Coder tree", "Git object", "16 fixed", "reconstructed from logged", "weaker source". The remaining hits are consistent with the corrections (details under Preservation Checks). Report:612 and the 10.9 synthesis-identity note were patched because the changes would otherwise contradict them |
| 13 | Table integrity | PASS | Every changed table row has the same cell count as its table header |

## Summary

- Findings in scope: 10 (F-01 to F-10). Resolved by a prepared patch: 10. Unresolved: 0.
- Severity of the input defects: IMPORTANT 5 (F-01, F-02, F-05, F-07, F-09), MINOR 5 (F-03, F-04, F-06, F-08, F-10), CRITICAL 0.
- Patches: 42 in total. The report has 25, synth-01 has 9, synth-02 has 3, synth-04 has 2, `gaps-and-questions.md` has 1 and `research/04-session-43582de1.md` has 2 (25 + 9 + 3 + 2 + 1 + 2 = 42). The two case-04 patches only add lines; no existing case text is changed.
- Corrections that change a rank or a ranked cause: 0.
- **Confidence:** Verified: 13/13 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. The Coder Git object contents were not re-read, because Git was not allowed. No correction depends on them: F-05 only discloses that they were read.
- **Tool engagement:** Read: 43 | Grep: 0 (searches ran inside Bash) | Glob: 0 | Bash: 17 (read-only `sed`, `grep`, `wc`, `sha256sum`, `cp` to `/tmp`, and `uv run --no-project python` record readers and patch builders on `/tmp` only). No web research.

## Issues Found

| ID | Old issue | Source evidence (path:line) | Resolution | Status | Rank impact |
|---|---|---|---|---|---|
| F-01 | Report:843 said v1/v2 were "reconstructed from logged Writes" and left out v3. v1 matches its snapshot only after Edit 163 is applied | `research/01-session-ac2cd1fd.md:323,330-332,410-413`; Orca records 141, 150/151, 163/164, 544, 841 (recomputed `648c5578`, `ebc03d45`, `d3a12ef9`, `cbfb606a`) | R-20: v1 = Write 141 + successful Edit 163 (the retry of blocked 150/151), `ebc03d45…`; v2 = Write 544, `d3a12ef9…`; v3 = Write 841, `cbfb606a…`; "Write and Edit payloads"; v3 has no comparison target. R-25 also records the Step 6.29 changes to synth-01/02/04 in 10.9 | RESOLVED | None |
| F-02 | The report never quoted the requested likelihood criterion or said that A-001 replaced it | `BUILD-REQUEST.md:12,34`; task file :311, :379, :559; `diff-analysis.md:64,69`; task log `[2026-10-24T06:32Z]` | R-03 / S1-01: new Section 1 bullet quoting the criterion, the debate's reason (no shared comparison rule), A-001, and the user's 2026-10-24 acceptance; Evidence line extended. R-18 / S4-01: new 7.3 row stating the order is not the requested likelihood ranking. No re-ranking | RESOLVED (disclosure only, per user) | None |
| F-03 | Report:10 attributed the Phase 5 review skip to a user decision | Task file :645; `synthesis-gate-decision.md:65` | R-02: the user authorized advancement (03:41Z) and said "if valuable" (03:45Z); the parent judged the review duplicative and did not run it; recorded as a user-authorized skip, not a pass | RESOLVED | None |
| F-04 | 2.6 and 7.7 claimed coverage that is not where they said; the authorized no-review v4 edit was not stated | Orca records 858, 885, 889; `research/01-session-ac2cd1fd.md:237-238,301,303-313` | R-04/R-05 and S1-02/S1-03: Orca row states the user-directed targeted review (858), the no-review recommendation (885) and the authorization (889). R-09 / S1-07: 2.6 now points to the real locations (Section 2.7, Option A Support, Gap row 1, Option B Risk). R-10 / S1-08: the source-test-table holes are listed as not repeated. R-19 / S4-02: 7.7 points to Section 2.2 and Section 4 | RESOLVED | None |
| F-05 | Report:901 denied the Coder Git reads; :8 and :322 did not disclose them | `research/03-session-6f744b87.md:121-131,212-250`; `report-gate-decision.md:115`; task log `[2026-10-24T06:32Z]` | R-01 (:8), R-12 (:322) and R-21 (:901): disclose that the case-03 analyst read two Coder blobs and three trees during Phase 2, as read-only object reads with no authorization on record, and that the user accepted keeping the evidence on 2026-10-24. The clause "(not the Coder trees named in Option D)" is removed. R-17 (:612): "reading them again" plus the disclosure. The evidence is kept | RESOLVED (keep, disclosed, per user) | None |
| F-06 | Report:166 said "the historical second reviewer" | Documentation log records 204/222/234 (same id `a728a634771049499`); `screening-recovery-source.txt:76`; `research/03-session-6f744b87.md:204,257` | R-06 / S1-04: "the same reviewer's second verdict (raw 234) relied on the executor's account" | RESOLVED | None |
| F-07 | Report:167, :272, :347 and :380 said the 16/2 count was corrected in debate; no contradiction marker existed | Second-review `REPORT.md:21`; CI log 1052, 1084; `round2-v1.md:5,16,33`; `merged-verdict.yaml:8`; `consensus-summary.md:3`; case 04:117-118, :130, :143, :145, :294, :361 | R-07/S1-05, R-11/S1-09, R-13/R-14/S2-01/S2-02 and R-15/S2-03: debate changed the verdict and narrowed the boundary-file reading, but the final review kept 16/2. R-08/S1-06: new Section 2.5 row with the exact `[CONTRADICTION: …]` marker. G-01: the same marker in `gaps-and-questions.md`. C-01/C-02: a dated, attributed erratum and marker added next to case 04:117-118 and :294, with existing text unchanged. The final partial pair is still marked unrecoverable | RESOLVED | None |
| F-08 | Report:578 gave "skill load was at 19:29:17Z" | Monitor records 14, 40, 42, 58; `research/05-session-e002bed2.md:83` | R-16: "19:29:22Z (records 40/42; the command was at 19:29:17Z, record 14)". Applied in the same patch as F-09 | RESOLVED | None |
| F-09 | Report:578 said the historical `ledger.md` bytes "cannot be hash-checked" | Monitor records 873/874; sha256 `bd66451d…`; line-3-only diff against the installed copy | R-16: the loaded bytes survive in full at record 874 (lines 1-243 of 243, sha256 given) and differ only at line 3. Whether the 20:29:54Z install wrote this file is still unproven, so the link stays timing evidence | RESOLVED | None; the V3 independence caveat and the user's existing rerun decision are unchanged |
| F-10 | 10.9 listed `scope-rules.md` and `scope-02.md` (and, unverified, scope-04/05) as exact returns | Record 79 of `agent-ascope-review-rules-0cb52ca63dfedc7b.jsonl`; `scope-rules.md:11,47,64-77`; `qa/qa-phase-2-fix-log.md:487-514`; `scope-02/04/05.md:8,11`; `screening-handoffs-source.txt:9-195,214-382,386-443` | R-22/R-23/R-24: all four moved to "Main-maintained or coordination records", with the preserved original returns cited and the reclassification noted in the label. Raw provenance is untouched | RESOLVED (residual checked: scope-04/05 are not exact returns) | None |

## Actions Taken

- I verified every finding against its primary source. Six JSONL logs were read by record number only: Orca planning, monitor, documentation, CI, and the rule-map subagent record 79. I recomputed the plan-version hashes and the record-874 ledger hash.
- I built all 42 patches on `/tmp` copies of six files. At each step I asserted that the `before` text occurred exactly once. I then replayed the JSON array on the live originals and got matching after-hashes. The `/tmp` workspace is deleted.
- I updated the synthesis wording wherever synth-01, synth-02 and synth-04 carried the same defective text. I did not patch `synth-02:31` or `synth-05:102`: the first is a prescriptive constraint and the second lists only replay, test and run items, and neither claims anything about Git reads. The Git disclosure exists only in the report, as it did after Step 6.18.
- I did not edit `fidelity-source-map.md:299,303` or the cross-source limitation line `:47`. They are review records, not report text (consolidation `:210`).

## Exact Patches If Direct Writes Are Prohibited

**(a) File hashes** (paths relative to R; after-hashes computed on the `/tmp` copies and reproduced by a fresh replay):

| `RESEARCH-REPORT-review-loops.md` | `9ac64f1353fb9a6ea228af727183d3434788807498219150a54275a84ad8e568` | `a94475caee954ae9942c4b4e8d609e4fc4bfb898fa134026045c78657f18ccf2` |
| `synthesis/synth-01-problem-current-state.md` | `f5c334dad15533ab8e7d70de6afdcc66c8493a741e14e06003a1d87580e9b14a` | `8d9c4db1a23877c84cc13efbd05bc95503fefd2c206256bbc26e345eb3b0d337` |
| `synthesis/synth-02-target-gaps.md` | `7b154d4b72327121f5c96b1a1503ea75b8f22bba6f3bba2265fda9b1e3ff4fa3` | `bcc1bdb3d8cedf536eb4eb1ebaaf5619ec6e58a5b2707c5a1db5c49d97775d13` |
| `synthesis/synth-04-options-recommendation.md` | `d85b9761b6fdb721a35fb3ce57552571aa31c088f25c0f3a3cb55925b7f79896` | `f0e20bd9362e13ee95ab8c0c0d24fbcc2c3413ab230fcd9810fc4fea606430b0` |
| `gaps-and-questions.md` | `0c4904e5bc83285a7d1502b14b877cea93c2ee59f32b4d964b934fd98c9019ed` | `9a688abf99e2db931a19b2170ad221c44be6d283524018b5b1fc576ecacdb890` |
| `research/04-session-43582de1.md` | `661d0604423bc9f68b38f1cf9e752c43b70968cf8d5701d928cf167a66cd0de7` | `b89b16d7886693300c3d4b244729342471e5c218693aeb9a46938764c63a99c6` |

**(b) Patch array.** Apply in array order. Each `before` occurs exactly once at its turn. Files are relative to R.

```json
[
 {
  "id": "R-01-F05-scope",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "and task log entry `[2026-10-24T05:35Z]` records the corrected range. From that decision on, no agent is to run any Git command; none was run in report-gate fix cycle 2 or by the cycle-3 fixer.",
  "after": "and task log entry `[2026-10-24T05:35Z]` records the corrected range. From that decision on, no agent is to run any Git command; none was run in report-gate fix cycle 2 or by the cycle-3 fixer. **Second disclosed departure (Coder Git objects, Phase 2):** during the Phase 2 documentation case analysis, the case-03 analyst read two Coder Git blobs (`62e217cd`, `0a01c9a4`) and three Coder Git trees (`f60d2c39727ec1c65b2a5fd475c0c9ebd2a0c894`, `3c5fdfacef70399481ed851f92d217d7b10011b0`, `00d8f4ae0d9a617eac6bf882e9c9ecf1c602e0a8`) in `/config/workspace/Coder/.git` and compared their manual-page and test-file contents (`research/03-session-6f744b87.md:121-131,212-250`). These were read-only object reads; no Git mutation is recorded, and the source does not record which tool performed them. No authorization for them is on record, and the acceptance above covers only the IronClaude reads at Task Steps 6.3-6.20 (`phase-outputs/plans/report-gate-decision.md:115`). The report relies on this evidence in Section 2.2 (documentation row) and Option D (Support, Evidence strength). On 2026-10-24 the user accepted keeping it, disclosed (\"Keep, disclosed\"; task log entry `[2026-10-24T06:32Z]`)."
 },
 {
  "id": "R-02-F03-header",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "The separate full Task Phase 5 phase-output review was skipped by user decision (2026-10-24T03:45Z) and is recorded as a skip, not a pass.",
  "after": "The separate full Task Phase 5 phase-output review was not run. The user authorized advancement at 03:41Z and at 03:45Z said to keep that review only \"if valuable\"; the parent then judged it duplicative of Phase 6 and did not run it. It is recorded as a user-authorized skip, not a pass."
 },
 {
  "id": "R-03-F02-section1",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "Sections 1-5 describe that evidence. The provisional, non-consensus comparative ranking of the five candidates is in Section 7.\n\n**Evidence:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/BUILD-REQUEST.md:12` (research question naming `sc:workflow` and `sc:implement`), `:14` (user-reported trigger);",
  "after": "Sections 1-5 describe that evidence. The provisional, non-consensus comparative ranking of the five candidates is in Section 7.\n- **Requested ranking criterion and the criterion delivered:** The build request asks for the five candidates to be \"ranked most to least likely\" and says: \"Use the result to rank the five by likelihood given this sample, not by artifact polish ... No fabricated probability percentages\" (`BUILD-REQUEST.md:12,34`). The debate's diff analysis recorded that the five cards \"await comparative likelihood ranking\" but that \"none supplies a common comparison rule that resolves breadth versus event-specific causal certainty\", and that \"existence, explanatory reach and expected recurrence are different questions\". It therefore promoted rule A-001, under which explanatory reach across contexts counts first and direct evidence for a particular transition counts second (`reviews/adversarial/adversarial/diff-analysis.md:64,69`; Section 6.0). Section 7 ranks explanatory support under A-001, not likelihood. No user authorization for that substitution was on record when the ranking was made; on 2026-10-24 the user accepted the explanatory-support order as the delivered answer, with no re-ranking (task log entry `[2026-10-24T06:32Z]`).\n\n**Evidence:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/BUILD-REQUEST.md:12` (research question naming `sc:workflow` and `sc:implement`; requested \"most to least likely\" ranking), `:14` (user-reported trigger), `:34` (requested likelihood criterion); `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/reviews/adversarial/adversarial/diff-analysis.md:64,69` (comparison rule A-001); task log entry `[2026-10-24T06:32Z]` (user acceptance of the explanatory-support order);"
 },
 {
  "id": "R-04-F04-orca-row",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "Authorized v3 receives a targeted review that remains partial. Fifteen successful edits then produce v4.",
  "after": "Authorized v3 receives a targeted review, narrowed at the user's instruction to two items (raw 858), that remains partial. The orchestrator then recommends a small edit “without another review”, saying the `/sc:implement` per-task reviewer will hold each task to it (raw 885), and the user authorizes it (“make the small edit”, raw 889). Fifteen successful edits then produce v4."
 },
 {
  "id": "R-05-F04-orca-transitions",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "targeted result 874 → edits 906-934 → disclosure 946.",
  "after": "targeted result 874 → no-review recommendation 885 → user authorization 889 → edits 906-934 → disclosure 946."
 },
 {
  "id": "R-06-F06-doc-row",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "the historical second reviewer had relied on the executor’s account",
  "after": "the same reviewer’s second verdict (raw 234) relied on the executor’s account"
 },
 {
  "id": "R-07-F07-ci-row",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "Reviewer 1’s “16 fixed, 2 partial” (810/821) was one intermediate assessment, whose interpretation of at least one partial item later debate corrected, and that reviewer initially returned “ready with notes” before debate changed the verdict. The second review ultimately finishes not-ready:",
  "after": "Reviewer 1 reported “16 fixed, 2 partial” (810/821) and initially returned “ready with notes”. Debate changed that verdict to not-ready and narrowed reviewer 1’s reading of the boundary-file partial to optional hardening, but the completed second review kept the same count: it “fixes 16 of the 18 cycle-0 findings in full and the other 2 in part” (final review report, written at 1052 and repeated to the user at 1084). Which two findings that final count treats as partial cannot be recovered (Section 2.5 contradiction marker). The second review ultimately finishes not-ready:"
 },
 {
  "id": "R-08-F07-marker-2.5",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/gaps-and-questions.md:29-35`. |\n| [CONTRADICTION: Orca source’s current-candidate diagram",
  "after": "`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/gaps-and-questions.md:29-35`. |\n| [CONTRADICTION: reviewer 1's \"16 fixed, 2 partial\" (CI log 821) vs the completed second review's own closure \"fixes 16 of the 18 cycle-0 findings in full and the other 2 in part\" (REPORT.md:21; CI log 1052, 1084); the merged verdict (:8) and consensus summary (:3) carry no itemized cycle-0 checklist, so the final partial pair is unrecoverable] | Preserve both statements. The research layer calls the count one reviewer's intermediate assessment that later debate corrected (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md:117-118`). The completed, debate-merged review keeps the same 16/2 count; debate changed the readiness verdict (`round2-v1.md:16,33`) and conceded only that the boundary-file part of one partial is optional hardening, not an M-10 requirement (`round2-v1.md:5`; `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md:145,361`). Do not choose which two findings the final count treats as partial: no surviving source itemizes them. Case 04's table (M-05 partial at `:130`, M-18 partly corrected at `:143`) fits a 16/2 count but does not prove it is the same pair. | Second CI review directory `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-specR1-20261023-031725-20261023032025/`: `REPORT.md:21`, `adversarial/merged-verdict.yaml:8`, `adversarial/consensus-summary.md:3`, `adversarial/round2-v1.md:5,16,33`; CI log `/config/.claude/projects/-config-workspace-IronClaude/43582de1-c41b-4b6a-806c-f19f1488095c.jsonl` records 821, 1052 and 1084; `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md:117-118,130,143,145,294,361`; `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/gaps-and-questions.md` (Unresolved Contradictions). |\n| [CONTRADICTION: Orca source’s current-candidate diagram"
 },
 {
  "id": "R-09-F04-2.6-represented",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "Sections 2.2, 2.4 and 2.5 preserve mixed causality, substantial successful repairs, corrected counts, source-hash stability, semantic/order interactions, validation timing versus presence, over-credited coverage, weaker source tests, authorized narrowing and unreviewed v4. Blocked cleanup attempts are not applied changes. |",
  "after": "Sections 2.2, 2.4 and 2.5 preserve mixed causality, substantial successful repairs, corrected counts, source-hash stability, semantic/order interactions and unreviewed v4. Section 2.2 (Orca row) also records the authorized narrowing: the user-directed two-item targeted review (raw 858), the recommendation to make the v4 edit without another review (raw 885) and the user's authorization (raw 889); Section 2.7 keeps authorized review narrowing as a distinct endpoint. Validation timing versus presence is carried outside Section 2, in Option A Support (Section 6), and over-credited coverage in Option A Support and Gap row 1 (Section 4). That blocked cleanup attempts are not applied changes is carried in Option B Risk (Section 6). |"
 },
 {
  "id": "R-10-F04-2.6-excluded",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "is not repeated in Section 2; it is represented with the inaccurate 13/3 closure summary as a stale-summary gap in Section 4. |",
  "after": "is not repeated in Section 2; it is represented with the inaccurate 13/3 closure summary as a stale-summary gap in Section 4. The case's finding that the Orca specification's own test table left holes, and that later rounds asked for stronger tests absent from it (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/01-session-ac2cd1fd.md:237-238,301`), is not repeated in the report. |"
 },
 {
  "id": "R-11-F07-2.6-ci",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "the intermediate “16 fixed, 2 partial” assessment and the initial “ready with notes” verdict that debate changed. |",
  "after": "reviewer 1’s “16 fixed, 2 partial” count, which the completed review kept (Section 2.5 contradiction marker), and the initial “ready with notes” verdict that debate changed. |"
 },
 {
  "id": "R-12-F05-constraints",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "and on 2026-10-24 the user accepted keeping that evidence (commands, purposes and the basis of that decision: header Scope line). Proposed investigations",
  "after": "and on 2026-10-24 the user accepted keeping that evidence (commands, purposes and the basis of that decision: header Scope line). Second disclosed departure: during the Phase 2 documentation case analysis, the case-03 analyst read two Coder Git blobs and three Coder Git trees in `/config/workspace/Coder/.git` (read-only object reads, no Git mutation recorded), with no authorization on record (`research/03-session-6f744b87.md:121-131,212-250`); on 2026-10-24 the user accepted keeping that evidence, disclosed (header Scope line). Proposed investigations"
 },
 {
  "id": "R-13-F07-gap-row",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": ", and reviewer 1’s intermediate “16 fixed, 2 partial” and initial “ready with notes” judgments were corrected or changed in debate. |",
  "after": "; debate changed reviewer 1’s initial “ready with notes” verdict to not-ready and narrowed its reading of the boundary-file partial to optional hardening, but the completed second review kept reviewer 1’s “16 fixed, 2 partial” count (Section 2.5 contradiction marker). |"
 },
 {
  "id": "R-14-F07-gap-row-cites",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md:102-104,114-118,240,244`. |",
  "after": "`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md:102-104,114-118,240,244,361`; second CI review `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-specR1-20261023-031725-20261023032025/REPORT.md:21`. |"
 },
 {
  "id": "R-15-F07-key-takeaway",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "the premature every-note-applied claim, the intermediate “16 fixed, 2 partial” assessment and the initial “ready with notes” verdict corrected in debate (reviewer-output gap row). |",
  "after": "the premature every-note-applied claim; the initial “ready with notes” verdict that debate changed; and reviewer 1’s “16 fixed, 2 partial” count, whose boundary-file partial reading debate narrowed but which the completed review kept (reviewer-output gap row; Section 2.5 contradiction marker). |"
 },
 {
  "id": "R-16-F08-F09-option-c-scope",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "while the monitor's skill load was at 19:29:17Z (`research/05-session-e002bed2.md:83`); the two credential FINAL loads bracket the write (Section 2.3). The two runs are therefore not independent support for V3. The installed `ledger.md` was rewritten on 2026-10-23, so its historical bytes cannot be hash-checked. |",
  "after": "while the monitor's skill load was at 19:29:22Z (records 40/42; the command was at 19:29:17Z, record 14; `research/05-session-e002bed2.md:83`); the two credential FINAL loads bracket the write (Section 2.3). The two runs are therefore not independent support for V3. The `ledger.md` bytes the monitor loaded survive in full in the record-874 Read result (lines 1-243 of 243, content SHA-256 `bd66451d93910c97aac0b20a4d1c2f35b0452c96cbda24567cb731f09ceddeb8`). They differ from the current installed copy only at line 3, the staging sentence changed on 2026-10-23 (Section 2.3). What those bytes cannot show without other history is whether this file was among the files the 20:29:54Z install wrote, so the link to that install stays timing evidence. |"
 },
 {
  "id": "R-17-F05-option-d-reuse",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "Loose object files with these IDs were present on 2026-10-24 but were not validated as tree objects; reading them is read-only Git object access that needs authorization (Section 8).",
  "after": "Loose object files with these IDs were present on 2026-10-24 but were not validated as tree objects; reading them again is read-only Git object access that needs authorization (Section 8). The case-03 analyst already read these trees during the Phase 2 case analysis, with no authorization on record; the user accepted keeping that evidence on 2026-10-24 (header Scope line; Section 8, Separate authorization)."
 },
 {
  "id": "R-18-F02-7.3",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "| The order ranks explanatory support for this selected, clustered sample under A-001 | Yes | `ADV/diff-analysis.md:69`; `ADV/refactor-plan.md:9` |",
  "after": "| The order ranks explanatory support for this selected, clustered sample under A-001 | Yes | `ADV/diff-analysis.md:69`; `ADV/refactor-plan.md:9` |\n| The order is the likelihood ranking the build request asked for (\"rank the five by likelihood given this sample\", `BUILD-REQUEST.md:34`; \"ranked most to least likely\", `:12`) | No. The debate adopted A-001's explanatory-reach rule instead, because the cards supplied no shared rule for comparing their likelihood (Section 1). The order ranks explanatory support. On 2026-10-24 the user accepted the explanatory-support order as the delivered answer; there is no re-ranking | `ADV/diff-analysis.md:64,69`; task log entry `[2026-10-24T06:32Z]` |"
 },
 {
  "id": "R-19-F04-7.7",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "| Mixed-cause planning loop: correction-induced defects, coverage over-credit, source contradictions; stopped by authorized narrowing; v4 unreviewed | Options A, B, C; 7.4 |",
  "after": "| Mixed-cause planning loop: correction-induced defects, coverage over-credit, source contradictions; stopped by authorized narrowing; v4 unreviewed | Options A, B, C; 7.4. The authorized narrowing and the authorized unreviewed v4 edit (raw 858, 885, 889) are in Section 2.2 (Orca row) and Section 4 (Key Takeaway Coverage, Orca planning row), not in Sections 6-7 |"
 },
 {
  "id": "R-20-F01-replay-row",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "| Plan v1 (first reviewed, raw 499) and v2 (Write 544/545), reconstructed from logged Writes; the first two reconstructed hashes match their review snapshots (`research/01-session-ac2cd1fd.md:323`) |",
  "after": "| Plan v1 (first reviewed, raw 499) = Write 141 plus the successful Edit 163, the retry of the blocked attempt 150/151, which did not apply (SHA-256 `ebc03d45…`); v2 = Write 544, confirmed at 545 (`d3a12ef9…`); v3 = Write 841, the version the targeted review at 874 checked (`cbfb606a…`). All three are reconstructed from logged Write and Edit payloads. The v1 and v2 reconstructions match their review snapshots; v3 has no independent comparison target (`research/01-session-ac2cd1fd.md:323,330-332,410-413`) |"
 },
 {
  "id": "R-21-F05-separate-authorization",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "None was performed here, except read-only Git reads of the IronClaude repository (not the Coder trees named in Option D), made at Task Steps 6.3-6.20 (recorded at Steps 6.3, 6.8, 6.9 and 6.17-6.20) by reviewer, consolidator, fixer and verifier agents spawned by the parent orchestrator, without user authorization at the time and with no Git mutation, and accepted by the user on 2026-10-24 (header Scope line). |",
  "after": "None was performed here, except two disclosed sets of read-only Git reads (header Scope line). First, read-only Git reads of the IronClaude repository made at Task Steps 6.3-6.20 (recorded at Steps 6.3, 6.8, 6.9 and 6.17-6.20) by reviewer, consolidator, fixer and verifier agents spawned by the parent orchestrator, without user authorization at the time and with no Git mutation, and accepted by the user on 2026-10-24. Second, during the Phase 2 documentation case analysis, the case-03 analyst read the Coder Git blobs `62e217cd` and `0a01c9a4` and the three Coder trees named in Option D (`research/03-session-6f744b87.md:121-131,212-250`), with no authorization on record and no recorded Git mutation; on 2026-10-24 the user accepted keeping that evidence, disclosed (task log entry `[2026-10-24T06:32Z]`). |"
 },
 {
  "id": "R-22-F10-label",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "**Raw recovered historical evidence versus main-persisted exact returns** (classification taken from the Agent Type column of 10.2-10.7):",
  "after": "**Raw recovered historical evidence versus main-persisted exact returns** (classification taken from the Agent Type column of 10.2-10.7, except that `research/scope-rules.md`, `research/scope-02.md`, `research/scope-04.md` and `research/scope-05.md` were reclassified at Task Step 6.29 after comparison with their original returns):"
 },
 {
  "id": "R-23-F10-exact-row",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "`research/evidence-deck.md`; `research/scope-rules.md`; `research/scope-02.md`, `research/scope-04.md`, `research/scope-05.md`; `research/web-01-gap-applicability.md`;",
  "after": "`research/evidence-deck.md`; `research/web-01-gap-applicability.md`;"
 },
 {
  "id": "R-24-F10-main-row",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "| Main-maintained or coordination records | `research/scope-01.md` and `research/scope-03.md` (main-maintained summaries with original material distinguished); `research/research-notes.md`;",
  "after": "| Main-maintained or coordination records | `research/scope-01.md` and `research/scope-03.md` (main-maintained summaries with original material distinguished); `research/scope-02.md`, `research/scope-04.md` and `research/scope-05.md` (main-session screening summaries that say \"No producer-written report is claimed\" and point to the screening returns preserved at `research/screening-handoffs-source.txt:9-195`, `:214-382` and `:386-443`, the last a provenance supplement; `scope-02.md:8,11`, `scope-04.md:8,11`, `scope-05.md:8,11`); `research/scope-rules.md` (a main-session rule map, not the analyst's exact return: that return, preserved at `/config/.claude/projects/-config-workspace-IronClaude/bbddbf85-99f2-4caf-a47f-a402da4f09de/subagents/agent-ascope-review-rules-0cb52ca63dfedc7b.jsonl` record 79, has a different title and structure; the main session also read the four sources directly (`scope-rules.md:11,47`), and the Phase 2 correction later inserted the recovered loaded-rule section at `:64-77` (`qa/qa-phase-2-fix-log.md:487-514`)); `research/research-notes.md`;"
 },
 {
  "id": "R-25-F01-F07-synth-identity-note",
  "file": "RESEARCH-REPORT-review-loops.md",
  "before": "Task Step 6.18 later changed synth-01, synth-04 and synth-05 (10.10, last row); the hashes above are the assembly-time identities.",
  "after": "Task Step 6.18 later changed synth-01, synth-04 and synth-05 (10.10, last row), and the Task Step 6.29 source-fidelity corrections later changed synth-01, synth-02 and synth-04 (`qa/qa-fidelity-fix-log.md`); the hashes above are the assembly-time identities."
 },
 {
  "id": "S1-01-F02-section1",
  "file": "synthesis/synth-01-problem-current-state.md",
  "before": "These sections describe the evidence, not the eventual ranking.\n\n**Evidence:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/BUILD-REQUEST.md:12` (research question naming `sc:workflow` and `sc:implement`), `:14` (user-reported trigger);",
  "after": "These sections describe the evidence, not the eventual ranking.\n- **Requested ranking criterion and the criterion delivered:** The build request asks for the five candidates to be \"ranked most to least likely\" and says: \"Use the result to rank the five by likelihood given this sample, not by artifact polish ... No fabricated probability percentages\" (`BUILD-REQUEST.md:12,34`). The debate's diff analysis recorded that the five cards \"await comparative likelihood ranking\" but that \"none supplies a common comparison rule that resolves breadth versus event-specific causal certainty\", and that \"existence, explanatory reach and expected recurrence are different questions\". It therefore promoted rule A-001, under which explanatory reach across contexts counts first and direct evidence for a particular transition counts second (`reviews/adversarial/adversarial/diff-analysis.md:64,69`; Section 6.0). Section 7 ranks explanatory support under A-001, not likelihood. No user authorization for that substitution was on record when the ranking was made; on 2026-10-24 the user accepted the explanatory-support order as the delivered answer, with no re-ranking (task log entry `[2026-10-24T06:32Z]`).\n\n**Evidence:** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/BUILD-REQUEST.md:12` (research question naming `sc:workflow` and `sc:implement`; requested \"most to least likely\" ranking), `:14` (user-reported trigger), `:34` (requested likelihood criterion); `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/reviews/adversarial/adversarial/diff-analysis.md:64,69` (comparison rule A-001); task log entry `[2026-10-24T06:32Z]` (user acceptance of the explanatory-support order);"
 },
 {
  "id": "S1-02-F04-orca-row",
  "file": "synthesis/synth-01-problem-current-state.md",
  "before": "Authorized v3 receives a targeted review that remains partial. Fifteen successful edits then produce v4.",
  "after": "Authorized v3 receives a targeted review, narrowed at the user's instruction to two items (raw 858), that remains partial. The orchestrator then recommends a small edit “without another review”, saying the `/sc:implement` per-task reviewer will hold each task to it (raw 885), and the user authorizes it (“make the small edit”, raw 889). Fifteen successful edits then produce v4."
 },
 {
  "id": "S1-03-F04-orca-transitions",
  "file": "synthesis/synth-01-problem-current-state.md",
  "before": "targeted result 874 → edits 906-934 → disclosure 946.",
  "after": "targeted result 874 → no-review recommendation 885 → user authorization 889 → edits 906-934 → disclosure 946."
 },
 {
  "id": "S1-04-F06-doc-row",
  "file": "synthesis/synth-01-problem-current-state.md",
  "before": "the historical second reviewer had relied on the executor’s account",
  "after": "the same reviewer’s second verdict (raw 234) relied on the executor’s account"
 },
 {
  "id": "S1-05-F07-ci-row",
  "file": "synthesis/synth-01-problem-current-state.md",
  "before": "Reviewer 1’s “16 fixed, 2 partial” (810/821) was one intermediate assessment, whose interpretation of at least one partial item later debate corrected, and that reviewer initially returned “ready with notes” before debate changed the verdict. The second review ultimately finishes not-ready:",
  "after": "Reviewer 1 reported “16 fixed, 2 partial” (810/821) and initially returned “ready with notes”. Debate changed that verdict to not-ready and narrowed reviewer 1’s reading of the boundary-file partial to optional hardening, but the completed second review kept the same count: it “fixes 16 of the 18 cycle-0 findings in full and the other 2 in part” (final review report, written at 1052 and repeated to the user at 1084). Which two findings that final count treats as partial cannot be recovered (Section 2.5 contradiction marker). The second review ultimately finishes not-ready:"
 },
 {
  "id": "S1-06-F07-marker-2.5",
  "file": "synthesis/synth-01-problem-current-state.md",
  "before": "`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/gaps-and-questions.md:29-35`. |\n| [CONTRADICTION: Orca source’s current-candidate diagram",
  "after": "`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/gaps-and-questions.md:29-35`. |\n| [CONTRADICTION: reviewer 1's \"16 fixed, 2 partial\" (CI log 821) vs the completed second review's own closure \"fixes 16 of the 18 cycle-0 findings in full and the other 2 in part\" (REPORT.md:21; CI log 1052, 1084); the merged verdict (:8) and consensus summary (:3) carry no itemized cycle-0 checklist, so the final partial pair is unrecoverable] | Preserve both statements. The research layer calls the count one reviewer's intermediate assessment that later debate corrected (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md:117-118`). The completed, debate-merged review keeps the same 16/2 count; debate changed the readiness verdict (`round2-v1.md:16,33`) and conceded only that the boundary-file part of one partial is optional hardening, not an M-10 requirement (`round2-v1.md:5`; `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md:145,361`). Do not choose which two findings the final count treats as partial: no surviving source itemizes them. Case 04's table (M-05 partial at `:130`, M-18 partly corrected at `:143`) fits a 16/2 count but does not prove it is the same pair. | Second CI review directory `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-specR1-20261023-031725-20261023032025/`: `REPORT.md:21`, `adversarial/merged-verdict.yaml:8`, `adversarial/consensus-summary.md:3`, `adversarial/round2-v1.md:5,16,33`; CI log `/config/.claude/projects/-config-workspace-IronClaude/43582de1-c41b-4b6a-806c-f19f1488095c.jsonl` records 821, 1052 and 1084; `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md:117-118,130,143,145,294,361`; `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/gaps-and-questions.md` (Unresolved Contradictions). |\n| [CONTRADICTION: Orca source’s current-candidate diagram"
 },
 {
  "id": "S1-07-F04-2.6-represented",
  "file": "synthesis/synth-01-problem-current-state.md",
  "before": "Sections 2.2, 2.4 and 2.5 preserve mixed causality, substantial successful repairs, corrected counts, source-hash stability, semantic/order interactions, validation timing versus presence, over-credited coverage, weaker source tests, authorized narrowing and unreviewed v4. Blocked cleanup attempts are not applied changes. |",
  "after": "Sections 2.2, 2.4 and 2.5 preserve mixed causality, substantial successful repairs, corrected counts, source-hash stability, semantic/order interactions and unreviewed v4. Section 2.2 (Orca row) also records the authorized narrowing: the user-directed two-item targeted review (raw 858), the recommendation to make the v4 edit without another review (raw 885) and the user's authorization (raw 889); Section 2.7 keeps authorized review narrowing as a distinct endpoint. Validation timing versus presence is carried outside Section 2, in Option A Support (Section 6), and over-credited coverage in Option A Support and Gap row 1 (Section 4). That blocked cleanup attempts are not applied changes is carried in Option B Risk (Section 6). |"
 },
 {
  "id": "S1-08-F04-2.6-excluded",
  "file": "synthesis/synth-01-problem-current-state.md",
  "before": "is not repeated in Section 2; it is represented with the inaccurate 13/3 closure summary as a stale-summary gap in Section 4. |",
  "after": "is not repeated in Section 2; it is represented with the inaccurate 13/3 closure summary as a stale-summary gap in Section 4. The case's finding that the Orca specification's own test table left holes, and that later rounds asked for stronger tests absent from it (`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/01-session-ac2cd1fd.md:237-238,301`), is not repeated in the report. |"
 },
 {
  "id": "S1-09-F07-2.6-ci",
  "file": "synthesis/synth-01-problem-current-state.md",
  "before": "the intermediate “16 fixed, 2 partial” assessment and the initial “ready with notes” verdict that debate changed. |",
  "after": "reviewer 1’s “16 fixed, 2 partial” count, which the completed review kept (Section 2.5 contradiction marker), and the initial “ready with notes” verdict that debate changed. |"
 },
 {
  "id": "S2-01-F07-gap-row",
  "file": "synthesis/synth-02-target-gaps.md",
  "before": ", and reviewer 1’s intermediate “16 fixed, 2 partial” and initial “ready with notes” judgments were corrected or changed in debate. |",
  "after": "; debate changed reviewer 1’s initial “ready with notes” verdict to not-ready and narrowed its reading of the boundary-file partial to optional hardening, but the completed second review kept reviewer 1’s “16 fixed, 2 partial” count (Section 2.5 contradiction marker). |"
 },
 {
  "id": "S2-02-F07-gap-row-cites",
  "file": "synthesis/synth-02-target-gaps.md",
  "before": "`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md:102-104,114-118,240,244`. |",
  "after": "`/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/04-session-43582de1.md:102-104,114-118,240,244,361`; second CI review `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-specR1-20261023-031725-20261023032025/REPORT.md:21`. |"
 },
 {
  "id": "S2-03-F07-key-takeaway",
  "file": "synthesis/synth-02-target-gaps.md",
  "before": "the premature every-note-applied claim, the intermediate “16 fixed, 2 partial” assessment and the initial “ready with notes” verdict corrected in debate (reviewer-output gap row). |",
  "after": "the premature every-note-applied claim; the initial “ready with notes” verdict that debate changed; and reviewer 1’s “16 fixed, 2 partial” count, whose boundary-file partial reading debate narrowed but which the completed review kept (reviewer-output gap row; Section 2.5 contradiction marker). |"
 },
 {
  "id": "S4-01-F02-7.3",
  "file": "synthesis/synth-04-options-recommendation.md",
  "before": "| The order ranks explanatory support for this selected, clustered sample under A-001 | Yes | `ADV/diff-analysis.md:69`; `refactor-plan.md:9` |",
  "after": "| The order ranks explanatory support for this selected, clustered sample under A-001 | Yes | `ADV/diff-analysis.md:69`; `refactor-plan.md:9` |\n| The order is the likelihood ranking the build request asked for (\"rank the five by likelihood given this sample\", `BUILD-REQUEST.md:34`; \"ranked most to least likely\", `:12`) | No. The debate adopted A-001's explanatory-reach rule instead, because the cards supplied no shared rule for comparing their likelihood (Section 1). The order ranks explanatory support. On 2026-10-24 the user accepted the explanatory-support order as the delivered answer; there is no re-ranking | `ADV/diff-analysis.md:64,69`; task log entry `[2026-10-24T06:32Z]` |"
 },
 {
  "id": "S4-02-F04-7.7",
  "file": "synthesis/synth-04-options-recommendation.md",
  "before": "| Mixed-cause planning loop: correction-induced defects, coverage over-credit, source contradictions; stopped by authorized narrowing; v4 unreviewed | Options A, B, C; 7.4 |",
  "after": "| Mixed-cause planning loop: correction-induced defects, coverage over-credit, source contradictions; stopped by authorized narrowing; v4 unreviewed | Options A, B, C; 7.4. The authorized narrowing and the authorized unreviewed v4 edit (raw 858, 885, 889) are in Section 2.2 (Orca row) and Section 4 (Key Takeaway Coverage, Orca planning row), not in Sections 6-7 |"
 },
 {
  "id": "G-01-F07-marker",
  "file": "gaps-and-questions.md",
  "before": "These are verified specification contradictions, not claims current runtime is definitely broken.\n",
  "after": "These are verified specification contradictions, not claims current runtime is definitely broken.\n\n[CONTRADICTION: reviewer 1's \"16 fixed, 2 partial\" (CI log 821) vs the completed second review's own closure \"fixes 16 of the 18 cycle-0 findings in full and the other 2 in part\" (REPORT.md:21; CI log 1052, 1084); the merged verdict (:8) and consensus summary (:3) carry no itemized cycle-0 checklist, so the final partial pair is unrecoverable] Added 2026-10-24 by the Task Step 6.29 source-fidelity fixer (finding F-07 in `qa/qa-fidelity-consolidated-findings.md`). Both statements are kept: `research/04-session-43582de1.md:117-118` calls the count one reviewer's intermediate assessment that later debate corrected, while the completed second review keeps the same count. Debate changed the readiness verdict and narrowed one partial's boundary-file reading to optional hardening; no surviving source names the final partial pair. Sources: `research/04-session-43582de1.md:117-118,145,294,361`; second CI review `/config/workspace/IronClaude/.dev/worktrees/ci-followup/.dev/reflect/pre-TASK-WF-specR1-20261023-031725-20261023032025/REPORT.md:21`, `adversarial/merged-verdict.yaml:8`, `adversarial/consensus-summary.md:3`, `adversarial/round2-v1.md:5,16,33`; CI log `/config/.claude/projects/-config-workspace-IronClaude/43582de1-c41b-4b6a-806c-f19f1488095c.jsonl` records 821, 1052 and 1084.\n"
 },
 {
  "id": "C-01-F07-marker-after-118",
  "file": "research/04-session-43582de1.md",
  "before": "- Later debate corrected that assessment’s interpretation of at least one “partial” item.\n",
  "after": "- Later debate corrected that assessment’s interpretation of at least one “partial” item.\n\n<!-- fidelity-erratum: 2026-10-24, Task Step 6.29, finding F-07 -->\n[CONTRADICTION: reviewer 1's \"16 fixed, 2 partial\" (CI log 821) vs the completed second review's own closure \"fixes 16 of the 18 cycle-0 findings in full and the other 2 in part\" (REPORT.md:21; CI log 1052, 1084); the merged verdict (:8) and consensus summary (:3) carry no itemized cycle-0 checklist, so the final partial pair is unrecoverable] Erratum added 2026-10-24 by the Task Step 6.29 source-fidelity fixer; the two takeaways above are unchanged. The completed second review kept the same count (final report line 21, CI log records 1052 and 1084; see the supplement's Section 3 Key Takeaways, \"The final report repeats ...\"). Debate changed the readiness verdict and narrowed the boundary-file partial to optional hardening.\n"
 },
 {
  "id": "C-02-F07-erratum-after-294",
  "file": "research/04-session-43582de1.md",
  "before": "The final report’s verdict and counts are at lines 21-25. The return contract records `overall_verdict: not_ready` and the counts at lines 71-75.\n",
  "after": "The final report’s verdict and counts are at lines 21-25. The return contract records `overall_verdict: not_ready` and the counts at lines 71-75.\n\nFidelity erratum (2026-10-24, Task Step 6.29, finding F-07; the sentence above is unchanged): final report line 21 also carries the closure count \"fixes 16 of the 18 cycle-0 findings in full and the other 2 in part\". See the [CONTRADICTION] marker added after the Section 4 Key takeaways.\n"
 }
]
```

## Preservation Checks

| Check | Result | Evidence |
|---|---|---|
| Ranks, displayed order and tallies unchanged | PASS | Counts before and after on the report and on synth-04: "V1 > V3 > V2 > V5 > V4" 5→5 and 3→3; "3 of 5" 6→6 and 4→4; "2 of 5" 5→5 and 4→4; "5 of 5" 4→4 and 3→3; rank-1 and rank-5 rows 1→1. No patch touches Sections 7.1 or 7.2 |
| J1 untouched | PASS | No patch targets Report:5, :1235 or :1287. R-25 is at :1256, an identity note, not a status line |
| No rewrite of empirical originals or debate history | PASS | Only addition-only patches touch a case file: C-01 and C-02 in `research/04`, each dated and attributed, and each `after` keeps its `before` text whole. No edits to `reviews/adversarial/**`, captures, cards, logs, plans, gate decisions, the source map or the task file |
| No invented evidence or false certainty | PASS | Every new fact traces to a record or line I read: hashes recomputed, record texts read. The final CI partial pair stays unrecoverable. Who ran the 20:29:54Z install, and whether it wrote `ledger.md`, stays unknown. The source tool for the Coder reads is stated as unrecorded |
| Remaining sweep hits are consistent | PASS | "None was performed" is now one occurrence, with both disclosures. "Steps 6.3-6.20" appears only in IronClaude-scoped statements. Every "likel" hit is a non-likelihood statement or the new disclosure. The leftover "intermediate" hits are the CI primary-transition label "intermediate claims 791/801/810-821" (a timing label), the case-04 quote inside the marker, "intermediate verdicts" (monitor ledger) and "intermediate evidence" (constraints). "second reviewer" now appears only in the oracle control row, where a different reviewer is meant. Report:850 "reading them needs authorized read-only Git object access" refers to future replay and agrees with R-17 |
| No Git, no parent-log read, no package writes | PASS | Every command was read-only or limited to `/tmp`. The live report hash is still `9ac64f13…e568` after cleanup |
| Monotonicity input for Step 6.32 | Recorded | \|F_0\| = 10. Expected \|F_1\| = 0 if the verifiers confirm the patches. No cycle-0 PASS identity is targeted. P2-V12 (synth-02 equal to its assembly hash) becomes historically true only, and R-25 records the change. Step 6.30 should re-check P2-V12 explicitly |

## QA Complete

**Verdict: FAIL** for the input set (10 open fidelity defects in the on-disk report). All 10 are RESOLVED by prepared patches, which are pending parent application. None changes a rank or a ranked cause.

| Status | Result |
|---|---|
| DONE | Verified F-01 to F-10 against primary records and lines, including recomputed Orca plan hashes and the record-874 `ledger.md` hash (`bd66451d…`, line-3-only difference). |
| DONE | Built 42 exact patches over 6 files. Each `before` occurs once, in order, and a fresh replay reproduced all after-hashes. The ranking is unchanged. |
| DONE | Resolved the scope-04/05 residual: both are main-session summaries, not exact returns, and are reclassified under F-10. |
| NEXT | Parent: confirm the six before-hashes, apply the JSON array in order, confirm the six after-hashes, and persist this text to `R/qa/qa-fidelity-fix-log.md`. |
| NEXT | Steps 6.30 and 6.31: independently verify every F-xx correction and all 84 cycle-0 PASS identities, including P2-V12. |
## Parent Application Record (2026-10-24)

| Item | Record |
|---|---|
| Persistence | The parent copied this report verbatim from the restricted fixer's final transcript text (record 258 of `subagents/agent-ap6-fid-fixer-*.jsonl`) into the prepared stub. The parent did not edit the fixer text above this section. |
| Application | `/tmp/apply_p6.py qa/qa-fidelity-fix-log.md` applied all 42 JSON patches in array order; each `before` occurred exactly once; all six start and end hashes matched before any write. |
| Files written | `RESEARCH-REPORT-review-loops.md` (1,310 to 1,313 lines, sha256 a94475ca...), `synthesis/synth-01`, `synth-02`, `synth-04`, `gaps-and-questions.md`, `research/04-session-43582de1.md`. |
| Case-file check | Both `research/04-session-43582de1.md` patches were checked to be insertion-only (dated, attributed F-07 contradiction marker and erratum); no existing case-file text was changed. |
| Not written | Cards, `reviews/adversarial/**`, raw captures, logs, plans, gate decisions, the task file. J1 not fixed, by user decision. |
| Git | None run. |
| Verification | Pending: `qa/qa-fidelity-verification-structural.md` and `qa/qa-fidelity-verification-content.md`. |

## Column Note (Phase 6 /task gate, 2026-10-24, finding G6-48)

**Attribution:** appended by the Phase 6 /task phase-gate fixer, applied by the parent. The fixer text above is unchanged.

The hash table under "(a) File hashes" has no header or separator row, so it does not render as a Markdown table. Its three columns are: file (path relative to the package root), SHA-256 before, SHA-256 after.
