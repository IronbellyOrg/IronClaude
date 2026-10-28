# QA Report: Phase 6 Source-Fidelity Consolidated Findings

**Topic:** Repeated review failures after fixes in `/sc:workflow` plans and `/sc:implement` tasks (`R/RESEARCH-REPORT-review-loops.md`)
**Date:** 2026-10-24
**Task step:** 6.28 (consolidate fidelity findings)
**Phase:** fidelity
**Lens:** source-fidelity consolidation (four partition reviews plus the cross-source contradiction review)
**Fidelity cycle:** 0
**Package root (R):** `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/`
**Report under review:** `R/RESEARCH-REPORT-review-loops.md`. It has 1,310 lines and sha256 `9ac64f1353fb9a6ea228af727183d3434788807498219150a54275a84ad8e568`, re-measured at the start of this step. All five fidelity reviews state the same hash.
**Mode:** report-only. No package file was edited and no Git command was run. The 10.9 MB parent session log was not opened. The primary sources were read only by record or line range.
**Governing instructions read:** `/config/.claude/skills/tech-research/SKILL.md:407-410` (Gate 4: 2 fidelity agents, partitioned into 3-4 when the sources exceed 1,000 lines, at most 2 fix cycles, HALT when the cycles are used up) and `:1153-1194` (fidelity prompt and report format); `/config/.claude/skills/task/SKILL.md:466-506` (Standard QA Report Output Format); task file Step 6.28 (`R/TASK-RESEARCH-review-loops-20261023-032537.md:487`).
**Known defect J1:** the stale status lines at Report:5, :1235 and :1287. This defect is known and the user accepted it (`R/phase-outputs/plans/report-gate-decision.md:116`). It is not a fidelity finding and is not counted here.

---

## Overall Verdict

Verdict: FAIL

All five fidelity reviews returned FAIL. After deduplication, 10 distinct fidelity defects remain open: 5 IMPORTANT, 5 MINOR and 0 CRITICAL. Each one is a case where the report misrepresents its sources, so each fails the gate whatever its severity. Two of them also need a user decision (see User Decisions Required).

## Coverage

| Expected review | Path | Present | Literal verdict | Real issues | Source scope (from the review header) |
|---|---|---|---|---|---|
| Partition 1: Orca planning, slots 19-24, debate, gate and task records | `R/qa/qa-source-fidelity-report-1.md` | Yes | FAIL (`:9`) | 4 (2 IMPORTANT, 2 MINOR) + J1 known | 46 sources or ranges, about 6,100 text lines, 7 JSONL logs by record; full report read |
| Partition 2: oracle, documentation and render case, cards, synthesis, QA records | `R/qa/qa-source-fidelity-report-2.md` | Yes | FAIL (`:10`) | 2 (1 IMPORTANT, 1 MINOR) + J1 known | 41 paths, about 4,900 text lines, 73 JSONL records; full report read |
| Partition 3: CI plan and Orca monitor | `R/qa/qa-source-fidelity-report-3.md` | Yes | FAIL (`:9`) | 2 (0 IMPORTANT, 2 MINOR) + J1 known | 24 files, about 4,400 text lines, about 85 JSONL records; full report read |
| Partition 4: credential finals, negatives and controls, current rules, cross-case layer | `R/qa/qa-source-fidelity-report-4.md` | Yes | FAIL (`:9`) | 2 (1 IMPORTANT, 1 MINOR) + J1 known | 41 sources, about 4,600 text lines, about 2,900 JSONL records; full report read |
| Cross-source contradiction check | `R/qa/qa-cross-source-contradictions-report.md` | Yes | FAIL (`:3`) | 1 (IMPORTANT) | 13 source-to-source conflict sets across all four partitions |

- **Expected 5, actual 5. No partition is missing.** The partition plan is `R/phase-outputs/discovery/fidelity-source-map.md:26-273`. Each source has exactly one owner (`:360`). Assigned reading load is 7,397 to 7,622 lines per partition (`:366-370`). That is far above the 1,000-line threshold, so four agents were required (`:372`).
- **Coverage gap carried forward (not counted as a finding).** Partition 4's Finding 2 says that `research/scope-04.md` and `research/scope-05.md` sit in the same 10.9 provenance row (Report:1242), and that Partitions 1 and 2 own them and should check them (`qa-source-fidelity-report-4.md:16`). Neither Partition 1 nor Partition 2 checked their provenance class. I read their headers. Both use the same pattern as `scope-02.md`: "Main session persists its returned evidence ... No producer-written report is claimed". Both point to a separate exact capture: `scope-04.md:8,11` points to `screening-handoffs-source.txt:214-382`, and `scope-05.md:8,11` points to `:386-443`. No fidelity reviewer compared either file with its capture, so whether each is an exact return has not been verified. This is an unverified residual, not a finding. The Step 6.29 fixer must check both files while correcting F-10, and Steps 6.30-6.31 must verify them.

## Items Reviewed

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | All four partitions and the cross-source review are present, with binary verdicts | PASS | Coverage table above. Each file carries a literal `Verdict: FAIL`. |
| 2 | Every review read the same report bytes | PASS | All five state sha256 `9ac64f13…e568`. Re-measured now: identical, 1,310 lines. |
| 3 | J1 recorded as known and not counted by every review | PASS | P1 `:19`, P2 `:19`, P3 `:18`, P4 `:18`, cross-source `:10`. Agrees with `report-gate-decision.md:116`. |
| 4 | Deduplication across reviews | PASS | 11 raw issues reduced to 10. Partition 3 Finding 1 and cross-source row `:25` are the same CI "16 fixed, 2 partial" defect, merged as F-07. Partition 3 Finding 2 and Partition 4 Finding 1 both touch Report:578 but are different defects, so they stay separate (F-08, F-09). |
| 5 | Severity on merge keeps the higher rating | PASS | F-07 is IMPORTANT (cross-source) over MINOR (Partition 3). |
| 6 | Each finding spot-checked against primary text by this consolidator | PASS, all 10 confirmed | F-01: `research/01-session-ac2cd1fd.md:323` ("Write and Edit payloads") against Report:843 ("reconstructed from logged Writes"). F-02: `BUILD-REQUEST.md:12,34`; task file `:311,:379,:559`; `diff-analysis.md:64,69`; Report:358 ("which is not a likelihood"). F-03: task file `:645`; `synthesis-gate-decision.md:65`. F-04: search for "150/151", "over-credit", "weaker source" and "validation timing" finds them only at Report:269, :557, :765, none in Sections 2.1-2.5. F-05: `research/03-session-6f744b87.md:125,212-250` against Report:901. F-06: `screening-recovery-source.txt:76` ("Same reviewer returns `compliant`"). F-07: CI second review `REPORT.md:21` and `round2-v1.md:5`; `research/04-session-43582de1.md:117-118,361`. F-08: `research/05-session-e002bed2.md:83`. F-09: monitor log record 874 (details under F-09). F-10: `scope-rules.md:8,11`; `scope-02.md:8,11`. |
| 7 | Disagreements between reviewers or with the map, resolved from primary evidence | PASS | Whether the installed `ledger.md` bytes the monitor loaded are available: the map (`fidelity-source-map.md:299`) and the cross-source limitations (`qa-cross-source-contradictions-report.md:47`) say unavailable. Partition 4 says preserved. I re-ran the check: record 874 is a full Read result (`filePath` = installed `ledger.md`, `startLine` 1, `numLines` 243, `totalLines` 243, timestamp 2026-10-22T20:34:06.655Z). Its exact content hashes to `bd66451d93910c97aac0b20a4d1c2f35b0452c96cbda24567cb731f09ceddeb8`, the value Partition 4 gives, and it differs from today's installed copy only at line 3. Partition 4 is correct. The map row and the cross-source limitation line are wrong; neither changes a cross-source row verdict. |
| 8 | Source contradictions resolved or honestly bounded, none silently chosen | PASS | See Unresolved Source Contradictions. |
| 9 | No defect quota, no invented finding | PASS | Every issue below traces to a reviewer row plus a primary line. The consolidator added no issue. The scope-04/05 residual is labelled unverified, not a finding. |
| 10 | Unavailable historical bytes stay unknown | PASS | Coder Git object contents, the identity of whoever ran the 20:29:54Z install, the final CI partial pair and the historical assembly hashes all remain unknown (see Unresolved Source Contradictions). |
| 11 | User-dependent corrections separated | PASS | F-02 and F-05 (see User Decisions Required). |

## Summary

- Reviews merged: 5 of 5 expected (4 partitions + 1 cross-source). All FAIL.
- Raw issues across reviews: 11 (P1 4, P2 2, P3 2, P4 2, cross-source 1). After deduplication: **10**.
- By merged severity: **CRITICAL 0, IMPORTANT 5 (F-01, F-02, F-05, F-07, F-09), MINOR 5 (F-03, F-04, F-06, F-08, F-10)**.
- Merges: 1. F-07 combines Partition 3 Finding 1 (MINOR) and cross-source row `:25` (IMPORTANT). Kept at IMPORTANT, the higher rating.
- Corrections that need a user decision: 2 (F-05, F-02). In both, the disclosure correction is required and is not optional.
- Corrections that could change a rank or a ranked cause: none of the required corrections does. Two optional user-chosen actions could: removing the Coder Git evidence (F-05) and re-ranking by likelihood (F-02). F-09 bears on a caveat the report already discloses but does not reorder anything.
- Verified-PASS identities frozen at cycle 0: 84 (P1 14, P2 12, P3 25, P4 7, cross-source 12, with 14 ranges inside P1). See Cycle-0 PASS Set.

## Issues Found

| ID | Severity | Sources (report, row; lens) | Location | Issue | Required correction | Rank impact |
|---|---|---|---|---|---|---|
| F-01 | IMPORTANT | P1 Finding 1 (`qa-source-fidelity-report-1.md:15`); lens: detail preservation / distortion | Report:843 (Section 8 replay table, Orca planning row); inputs for Section 7.6 order 2 and step 2.2 | **Distortion:** the row says v1 and v2 were "reconstructed from logged Writes" and that "the first two reconstructed hashes match their review snapshots". v1 only matches its snapshot after the successful Edit at record 163 is applied: Write 141 alone hashes to `648c5578…`, while the snapshot is `ebc03d45…` (P1 recomputation). The case file says "Write and Edit payloads" (`research/01-session-ac2cd1fd.md:323`). Report:531 also says "Writes/Edits", so the report contradicts itself. **Missing detail:** v3 (Write 841, reviewed at 874) is left out, although Option B Effort (Report:556) needs it as the second reviewed repair transition. | In Report:843, set "Version to use" to: v1 = Write 141 plus successful Edit 163 (not blocked attempt 150/151), hash `ebc03d45…`; v2 = Write 544, hash `d3a12ef9…`; v3 = Write 841, hash `cbfb606a…` (hashes at `research/01-session-ac2cd1fd.md:330-332`). Keep Report:531's statement that v3 has no independent comparison target. | None. This is a replay-input row, not ranking evidence. |
| F-02 | IMPORTANT | P1 Finding 2 (`:16`); lens: criteria validity / missing | Report:87-89 (Section 1), Section 6.0 comparison rule (Report:496-501), Report:663, :671 (7.1 heading), :713 (7.3) | **Missing / distorted governing criterion:** the request asks for the five causes to be "ranked most to least likely" and to "rank the five by likelihood given this sample ... No fabricated probability percentages" (`BUILD-REQUEST.md:12,34`). The task file repeats "most-to-least likely" at `:311`, `:379` and `:559`. The debate promoted A-001 because the cards only "await comparative likelihood ranking" and "existence, explanatory reach and expected recurrence are different questions" (`reviews/adversarial/adversarial/diff-analysis.md:64,69`). The report delivers an explanatory-support order (Report:671, :713) and even says the ranking "is not a likelihood" (Report:358). It never quotes the requested criterion and never says the debate replaced it. Section 1 cites `BUILD-REQUEST.md:12` only for the question wording (Report:89). No user authorization for the substitution is on record. | Required now: in Section 1 and 7.3, quote the requested criterion (`BUILD-REQUEST.md:12,34`), state that rule A-001 replaced likelihood with explanatory support, cite `diff-analysis.md:64,69`, and say that accepting the substitution is the user's decision. Anything beyond that disclosure waits for the user (see User Decisions Required, item 2). | Disclosure only: none. Re-ranking by likelihood: changes the governing criterion and therefore the ranking (see User Decisions Required). |
| F-03 | MINOR | P1 Finding 3 (`:17`); lens: semantic accuracy (who decided) | Report:10 (header "Gate qualification") | **Distortion:** says the separate full Task Phase 5 review "was skipped by user decision (2026-10-24T03:45Z)". The user said "keep the phase 5 review if valuable", and the parent judged it duplicative and did not run it (task file `:645`; `phase-outputs/plans/synthesis-gate-decision.md:65`). Report:1233 states this correctly, so the header contradicts both the sources and 10.9. | Reword Report:10 to say the parent judged the review duplicative and did not run it, under the user's 03:41Z authorization to advance and the 03:45Z "if valuable" clarification. Recorded as a skip, not a pass. Cite task file `:645` and `synthesis-gate-decision.md:65`. | None |
| F-04 | MINOR | P1 Finding 4 (`:18`); lens: phantom coverage / missing detail | Report:269 (Section 2.6 Orca row); Report:765 (Section 7.7, `research/01` row) | **Phantom coverage claims:** (a) Report:269 says Sections 2.2, 2.4 and 2.5 preserve "validation timing versus presence, over-credited coverage, weaker source tests, authorized narrowing" and that "Blocked cleanup attempts are not applied changes". None of these appears in Sections 2.1-2.5. The concepts appear only in Option A Support (Report:521), Option B Risk (Report:557) and Gap row 1 (Report:341). (b) Report:765 says "stopped by authorized narrowing" is represented in Options A-C and 7.4. It is not. (c) **Missing:** at Orca records 885 and 889, the orchestrator recommended the v4 edit "without another review", leaving enforcement to per-task implementation review, and the user authorized it (P1 record read; `research/01-session-ac2cd1fd.md:404-417`). The report says only that v4 is unreviewed (Report:164, :528, :946). | Make Report:269 and :765 point to where the content actually is (Option A Support, Option B Risk, Gap row 1), or add it to the cited sections. State once, citing records 885 and 889, that skipping review of the v4 edit was recommended and then authorized by the user. | None |
| F-05 | IMPORTANT | P2 Finding 1 (`qa-source-fidelity-report-2.md:16`); lens: accuracy / undisclosed evidence provenance | Report:901 (Section 8, Separate authorization row); Report:8 (Scope line); Report:322 (Section 3 Constraints); Report:612 (Option D Reuse). Evidence that depends on it: Report:166, :602, :607 | **Inaccurate denial:** Report:901 says that apart from the IronClaude Git reads, "None was performed here ... (not the Coder trees named in Option D)". The case-03 analyst read Coder blobs `62e217cd` and `0a01c9a4` and trees `f60d2c3…`, `3c5fdfa…` and `00d8f4a…` during the Phase 2 case analysis ("I independently read both Git blobs", `research/03-session-6f744b87.md:125`; tree comparison `:212-239`; "This investigation independently establishes it using the earlier Git tree", `:250`). The report relies on those reads at Report:166 ("Retained earlier Git objects independently establish the genuine delta"), :602 and :607 ("recovered Git trees"). The user's recorded acceptance covers only the IronClaude reads at Steps 6.3-6.20 (`report-gate-decision.md:115`). By the report's own definition at Report:612, reading these objects is Git object access that needs authorization. | Required now: at Report:8, :322 and :901, disclose that the case-03 analyst read these Coder blobs and trees during Phase 2 (cite `research/03-session-6f744b87.md:121-131,212-250`), and state that no authorization for those reads is on record. Delete the clause "(not the Coder trees named in Option D)" from Report:901. Do not silently delete the Coder-tree evidence: keeping or removing it is the user's decision (see User Decisions Required, item 1). | Disclosure: none. Removing the evidence: changes the support for ranked cause V4 (see User Decisions Required). |
| F-06 | MINOR | P2 Finding 2 (`:17`); lens: distortion (reviewer identity) | Report:166 (Section 2.2, documentation row) | **Phantom reviewer:** "the historical second reviewer had relied on the executor's account". Records 204, 222 and 234 involve one reviewer (task id `a728a634771049499`). The screening capture says "Same reviewer returns `compliant`" (`research/screening-recovery-source.txt:76`), and the case agrees (`research/03-session-6f744b87.md:204,257`). The report treats reviewer identity as a counting unit (Report:135). Report:344 and :379 phrase it correctly. | At Report:166, write "the same reviewer's second verdict (raw 234) relied on the executor's account". | None |
| F-07 | IMPORTANT (merged; MINOR in P3, IMPORTANT in cross-source; higher kept) | P3 Finding 1 (`qa-source-fidelity-report-3.md:15`; lens: distorted transition); cross-source row (`qa-cross-source-contradictions-report.md:25`; lens: unmarked source-to-source contradiction) | Report:167 (Section 2.2 CI row), :272 (Section 2.6 CI row), :347 (Section 4 reviewer-overclaim gap row), :380 (Section 4 Key Takeaway CI row). Source components: synth-01 (Sections 1-2) and synth-02 (Sections 3-4) | **Distortion, and the report takes one side without saying so:** the report calls reviewer 1's "16 fixed, 2 partial" an intermediate assessment that was "corrected or changed in debate" (:347) and "corrected in debate" (:380). The completed, debate-merged second review keeps the same tally: "fixes 16 of the 18 cycle-0 findings in full and the other 2 in part" (CI `.../pre-TASK-WF-specR1-20261023-031725-20261023032025/REPORT.md:21`; written at CI log record 1052, 03:46:28.426Z). It is repeated to the user at record 1084. Debate changed the readiness verdict (`round2-v1.md:16,33`) and conceded only that the boundary-file part is optional hardening, not an M-10 requirement (`round2-v1.md:5`). Case 04 holds both statements without a marker: "intermediate ... corrected" at `research/04-session-43582de1.md:117-118`, and "The final report repeats '16 original findings fixed, two partly fixed'" at `:361`. Case 04:294 cites "lines 21-25" but leaves out line 21's tally. No surviving source names the final partial pair. | (1) Rewrite Report:347 and :380, and qualify :167 and :272, to say that debate changed the readiness verdict and narrowed the reading of the boundary-file partial, but the final review and record 1084 kept the 16-fixed/2-partial count. Keep the existing statement that "ready with notes" changed. (2) Add a searchable marker in the report: `[CONTRADICTION: reviewer 1's "16 fixed, 2 partial" (CI log 821) vs the completed second review's own closure "fixes 16 of the 18 cycle-0 findings in full and the other 2 in part" (REPORT.md:21; CI log 1052, 1084); the merged verdict (:8) and consensus summary (:3) carry no itemized cycle-0 checklist, so the final partial pair is unrecoverable]`. (3) The cross-source review also asks for the same marker in `R/gaps-and-questions.md` and next to `research/04-session-43582de1.md:117-118,294`. Step 6.29 forbids rewriting empirical originals, so the fixer decides whether case 04 is in its edit scope; if it is not, the fixer logs that and places the marker in the report and the gap register. Apply the matching wording to synth-01 and synth-02 if they still carry it. | None. The 16/2 count is not used in Sections 6-7 (it appears only at Report:167, :272, :347, :380). |
| F-08 | MINOR | P3 Finding 2 (`qa-source-fidelity-report-3.md:16`); lens: inaccurate timestamp attribution | Report:578 (Option C Scope row, shared-deployment paragraph) | **Inaccurate:** "the monitor's skill load was at 19:29:17Z". 19:29:17.282Z is the user's `/sc:implement` command (record 14). The skill call and its loaded text are at 19:29:22.409Z and 19:29:22.708Z (records 40, 42), and `qa.md` loaded at 19:29:28.357Z (record 58). The case lists both times (`research/05-session-e002bed2.md:83`). All of these precede the 20:29:54Z install, so the conclusion stands. | Change it to "the monitor's skill load was at 19:29:22Z (records 40/42; the command was at 19:29:17Z)". Apply it in the same serialized edit as F-09, which touches the same paragraph. | None (P3 confirms the conclusion is unchanged) |
| F-09 | IMPORTANT | P4 Finding 1 (`qa-source-fidelity-report-4.md:15`); lens: inaccurate limitation (the source contradicts it) | Report:578 (Option C Scope row, last sentence). The same limitation underlies the Option C Evidence strength note (Report:580), the Options Comparison "not independent" cell (Report:646) and 7.4 Shared clusters (Report:732) | **Inaccurate limitation:** "The installed `ledger.md` was rewritten on 2026-10-23, so its historical bytes cannot be hash-checked." Monitor record 873 is a Read of the installed `ledger.md`, and record 874 (2026-10-22T20:34:06.655Z) holds the whole file: `startLine` 1, `numLines` 243, `totalLines` 243, content sha256 `bd66451d…` (re-verified by this consolidator). It differs from today's installed copy only at line 3 ("Do not `git add` the ledger." became the `.dev/tasks/` staging sentence). That matches the report's own Section 2.3 row (Report:207). This repeats the error class of prior finding P6-03 (local provenance treated as unavailable), and it sits on the shared-deployment caveat flagged as P6-04. | Replace the sentence: the loaded `ledger.md` survives in full at monitor record 874 (sha256 `bd66451d…`) and differs from the current installed copy only at line 3. Keep the "timing evidence" label. If the link to the 20:29:54Z install is still unproven (it cannot be tested without Git), say exactly that instead of calling the bytes uncheckable. Do not edit the source map (out of scope); this report records that `fidelity-source-map.md:299` is wrong. | No direct rank change. It bears on the V3 independence caveat the report already discloses (Report:578, :580, :646, :732), whose consequence the report already leaves to the user (debate rerun, Report:581, :732). If the restatement changes how strong the shared-deployment dependency is, that feeds the user's existing decision; it does not reorder anything automatically. |
| F-10 | MINOR | P4 Finding 2 (`:16`); lens: distorted provenance class | Report:1242 (10.9 "Main-persisted exact returns of restricted workers" row) | **Wrong provenance class:** `research/scope-rules.md` and `research/scope-02.md` are listed as exact returns. `scope-rules.md` has a different title and structure from the analyst's actual return (rule-map transcript record 79, 2026-10-23T03:31:40.642Z). It says the main session "additionally directly read the four sources" (`scope-rules.md:11`), and its section at `:64-77` was inserted later by the Phase 2 correction (`qa/qa-phase-2-fix-log.md:487-514`). `scope-02.md` is a 44-line main-session summary that points to the exact handoff at `screening-handoffs-source.txt:9-195` (`scope-02.md:11`). 10.9 gives the case reports a mixed-authorship note and puts `scope-01.md` and `scope-03.md` under "Main-maintained" (Report:1243), but applies neither treatment to these two files. | Move `scope-rules.md` and `scope-02.md` to the "Main-maintained or coordination records" class (Report:1243), or annotate them as main-authored, with the analyst return preserved elsewhere and later correction edits noted. Then compare `scope-04.md` and `scope-05.md` with their captures (Coverage residual) and classify them the same way if they are not exact returns. Keep all raw provenance. | None |

## User Decisions Required

**USER DECISION REQUIRED 1: evidence from the case-03 analyst's Phase 2 reads of Coder Git blobs and trees (F-05).**
- **What happened:** during the Phase 2 documentation case analysis, the case-03 analyst read two Coder Git blobs (`62e217cd`, `0a01c9a4`) and three Coder trees (`f60d2c39727ec1c65b2a5fd475c0c9ebd2a0c894`, `3c5fdfacef70399481ed851f92d217d7b10011b0`, `00d8f4ae0d9a617eac6bf882e9c9ecf1c602e0a8`) in `/config/workspace/Coder/.git` (`research/03-session-6f744b87.md:121-131,212-250`). No authorization for those reads is on record. The user's 2026-10-24 confirmation covers only the read-only IronClaude Git reads at Steps 6.3-6.20 (`report-gate-decision.md:115`). The source does not record which tool performed the reads.
- **Not optional:** the report currently denies these reads (Report:901). The disclosure correction in F-05 is a fidelity fix and must be applied whatever the user decides.
- **Option "keep, disclosed":** the evidence stays, labelled as unauthorized Phase 2 Git object access. Rank impact: none.
- **Option "remove":** the report would lose the independent confirmation that the Task 2 baseline was falsely attributed. Report:166 ("Retained earlier Git objects independently establish the genuine delta"), Option D Support (Report:602, "The earlier truthful tree `f60d2c3…` contains them") and Option D Evidence strength (Report:607, "recovered Git trees") would fall back to the executor's own comment at record 188 and the reviewer's admitted reliance at record 234. Option D (ranked cause V4) would keep its documentation-baseline context but with weaker support. **Rank impact:** the displayed order would not change mechanically, because V4 is already last. However, this removes evidence the V4 card carried into the debate, so it changes a ranked cause's support. Under Step 6.29, that invalidates the affected earlier gates (debate-dependent synthesis and report gates) until they are actually rerun, not assumed to PASS. It would also weaken the 3-of-5 dissent that places V4 above V5 (Report:698).
- **Unknown, either way:** the contents of these Git objects could not be re-read in this gate (no Git allowed). Partition 2 corroborated only outside Git: the loose object files exist with modification times of 21:13, 21:15 and 21:16 on 2026-10-22. Blob `0a01c9a4` has a modification time of 2026-10-24T06:05, cause unknown; the report does not cite it directly (`qa-source-fidelity-report-2.md:55-58`).
- **Recommendation:** keep the evidence with the full disclosure. Removing it changes ranked-cause support and forces the earlier gates to rerun, while keeping it preserves the source and makes the unauthorized reads visible.

**USER DECISION REQUIRED 2: ranking criterion mismatch (F-02).**
- **What happened:** the request asked to "rank the five by likelihood given this sample", ordinal and without probability percentages (`BUILD-REQUEST.md:12,34`; task file `:311,:379,:559`). The debate adopted rule A-001 (explanatory reach first, direct transition evidence second) because the cards could not be compared on likelihood without a shared rule (`diff-analysis.md:64,69`). The report ranks "explanatory support" and says it is "not a likelihood" (Report:358, :713). No user authorization for the substitution is on record.
- **Not optional:** the disclosure in F-02 (quote the requested criterion and state the substitution) is a fidelity fix and must be applied.
- **Option "disclosure only":** the user accepts explanatory support as the delivered answer. Rank impact: none.
- **Option "something more" (for example, re-rank by likelihood given this sample):** this changes the governing criterion of the headline deliverable. It needs a new comparative judgment, which means rerunning the debate or the Step 5.12 ranking. **Rank impact:** it could change any placement, and it would invalidate the earlier gates that depend on Sections 6-7: the Phase 5 ranking step and synthesis gate, the Step 6.21 report gate, and the Section 6-7 PASS identities in this fidelity cycle (P1-S7, P1-S9 and the related PASS checks below) until they are actually rerun.
- **Recommendation:** disclosure only, unless the user specifically needs a likelihood order. The debate record shows likelihood and reach were judged different questions, and re-ranking would reopen every gate after Phase 5.

## Unresolved Source Contradictions

| # | Statements in conflict | Sources | Status | Required handling |
|---|---|---|---|---|
| U-1 | Reviewer 1's intermediate "16 fixed, 2 partial" (CI log record 821; `research/04-session-43582de1.md:117-118`, "corrected in debate") **versus** the completed review's own final count "16 of the 18 ... in full and the other 2 in part" (`REPORT.md:21`; records 1052, 1084; `research/04-session-43582de1.md:361`) | `qa-cross-source-contradictions-report.md:25,48` | **Irreducible in part.** It is established that the 16/2 count survived debate. Which two of the 18 earlier findings the final count treats as partial cannot be recovered from any surviving source: the merged verdict (`:8`) and consensus summary (`:3`) have no item-by-item checklist. Case 04's own table (M-05 partial at `:130`, M-18 partly corrected at `:143`) is consistent with a 16/2 count but does not prove it is the same pair. | Keep both statements with the searchable `[CONTRADICTION: ...]` marker given in F-07. Do not pick a pair. |
| U-2 | Orca `source.md:381-382` (diagram: current candidate means no-op) **versus** `source.md:142` (an up-to-date state that still runs patch checks) | `qa-cross-source-contradictions-report.md:17` | Cannot be resolved from the sources; already marked | Already preserved with markers at Report:253, Q6 (Report:947), Report:898 and `gaps-and-questions.md:33`. No action. |
| U-3 | Orca `source.md:402` (self-check before any upstream call) **versus** `source.md:128,134` (fetch step first) | `qa-cross-source-contradictions-report.md:18` | Cannot be resolved from the sources; already marked | Already preserved at Report:254, :403, :947 and `gaps-and-questions.md:35`. No action. |

**Disagreements between reviewers or with the map, resolved from primary evidence (not source contradictions):**
- **Historical `ledger.md` bytes.** The map (`fidelity-source-map.md:299`) and the cross-source limitations (`:47`) say they are unavailable. Partition 4 says they are preserved. Resolved in favor of Partition 4 by the record 874 re-check (sha256 `bd66451d…`, line-3 difference only). This drives F-09.
- **"Rubric versions for any reviews other than the two captured loads: Not captured"** (`fidelity-source-map.md:303`). Partition 4 found five more `qa.md` loads, all hashing to `0b533765…`, in the nested logs `a59e…` record 17, `a6248…` 17, `a9c0…` 18, `abd76…` 16 and `a6d8…` 19 (`qa-source-fidelity-report-4.md:68`). The map line overstates the gap. The report's Q3 wording is not false, so this is not a report defect.

**Bounded unknowns (kept as unknown, not inferred):**
- Contents of the Coder Git objects (Git not allowed in this gate), and the cause of blob `0a01c9a4`'s 2026-10-24T06:05 modification time.
- Who or which process ran the 2026-10-22T20:29:54Z install, and whether installed `ledger.md` was among the files written then (cannot be tested without Git; P4 found no install command in session 17).
- The historical bytes behind the assembly-time hashes of synth-01, synth-04 and synth-05, and the historical inventory counts at 22:14:30Z, 01:26:42Z and 03:51:27Z (`qa-source-fidelity-report-2.md:60`).
- Historical log line counts the report gives as of 04:37Z. CI now has 1,156 lines (1,153 recorded); this is growth, not a contradiction (`qa-source-fidelity-report-3.md:66`).
- Unavailable originals listed at `fidelity-source-map.md:295-302`: the issue-358 worktree, `pull-sync-framework.yml:89-108`, the Task 3 temporary lint files and the pre-authorization oracle snapshot. The report does not substitute current files for them. The `ledger.md` row at `:299` is the exception and is corrected above.

## Cycle-0 PASS Set

These are the verified-PASS claim identities each reviewer recorded against primary sources. They are frozen at fidelity cycle 0. Any one of them that FAILs in a later cycle triggers the regression guard at Step 6.32.

**Partition 1 (`qa-source-fidelity-report-1.md`):**
- P1-S1 `:25` Orca planning chronology and records: timestamps and UUIDs of records 15-946; Writes 544 and 841; blocked Edit 150/151 and retry 163/164; 15 Edits at 906-934; structural gates at 849 and 944.
- P1-S2 `:26` Orca review counts and contents: 16 `partial` findings at 499; N-01 to N-20 with duplicate N-02 and non-defect N-16; `prior_fix_check` 14 fixed and 2 partial against the 13/16 narrative; targeted PARTIAL at 874 condensed at 877; the 946 "NOT CHECKED" disclosure; no implementation in records 947-954.
- P1-S3 `:27` Orca hashes: the same source hash `32211523…` in both snapshots; v2, v3 and v4 reproduce; live plan = v4 `94af0cda…`.
- P1-S4 `:28` Orca artifact citations: coverage-matrix 1749-1756; merged-verdict 39-47, 57-65, 75-83, 120-128; `source.md` 142/382 and 285/402; test-50 599-628.
- P1-S5 `:29` Session 19 control: nine compliant verdicts; `verdict=missing` hits are injected template text.
- P1-S6 `:30` Synthetic slots 21-24: 30-line MagicMock logs with zero tool calls.
- P1-S7 `:31` Debate citations: Round 1 attributions 128/129/167/168/208; Round 2 at 256-438; orders 477-484; base-selection writing order V4, V5, V2, V3, V1 with input-order tiebreak; probe, refactor-plan, plan-review, return-contract, merged-analysis, run-evidence and post-merge lines.
- P1-S8 `:32` Merge record 71 at 05:54:05.390Z; canonical-review FAIL at record 79; PASS at record 38.
- P1-S9 `:33` Gate records: Phase 3 cycle-2 and Phase 4 closures; synthesis-gate statuses; task-log entries behind header line 8.
- P1-C1 `:44` Historical loaded version (PASS). P1-C2 `:45` Partial-verdict validity (PASS). P1-C3 `:47` Chronology (PASS). P1-C4 `:48` Before/after causality (PASS). P1-C5 `:49` Unreviewed endpoint limits (PASS; the qualification is carried by F-04, which is in the FAIL set).

**Partition 2 (`qa-source-fidelity-report-2.md`, Claims Verified table):**
- P2-V1 `:25` truncated record 291 supplemented by `t12-review-1.md:20-34`.
- P2-V2 `:26` frozen corpus and authorization restrictions (records 383, 521; builder record 52).
- P2-V3 `:27` three fixed, one retained.
- P2-V4 `:28` one-field correction and re-freeze (line 600; hashes `d54be745…`/`2751e86c…`; 74/85 counts).
- P2-V5 `:29` original criteria (plan `:87`; `merged-requirements.md:607,610,652`).
- P2-V6 `:30` evidence-only renderer retry (records 413, 433-434, 443, 450; `/usr/bin/man` notice script).
- P2-V7 `:31` explicit acceptance, with no render falsely shown as compliant.
- P2-V8 `:32` unsupported baseline provenance (records 188, 234). PASS except the "second reviewer" wording, which is F-06.
- P2-V9 `:33` no phantom causal claim in the oracle or documentation transitions.
- P2-V10 `:34` current state not substituted for missing historical bytes. PASS except the Coder Git disclosure, which is F-05.
- P2-V11 `:35` timestamps and record identities (oracle, builder, documentation).
- P2-V12 `:36` Partition 2 QA and synthesis records (Git-read QA lines, Phase 5 and 6 consolidations, cycle-2 log, intake, seven-pair comparison, erratum, `web-01`, cards, synth hashes, 204-file brace expansion).

**Partition 3 (`qa-source-fidelity-report-3.md`, Claims Verified table, rows `:24` to `:48`):**
- P3-C1 `:24` 18 original CI concerns (10 medium, 8 low).
- P3-C2 `:25` refactor authorization 627; 651/653; 663/670.
- P3-C3 `:26` 791 every-note-applied, then the 801 calibrator.
- P3-C4 `:27` reviewer 1 16/2, `ready_with_notes`, 4 new medium; debate changed the verdict. PASS for the verdict change; that the count survived is F-07.
- P3-C5 `:28` completed second review not ready, 5/11/0, partial status.
- P3-C6 `:29` tooling exemption, search filters, phrase blacklist.
- P3-C7 `:30` dependency-repoint before/after defect; sequential order protection.
- P3-C8 `:31` boundary-file hardening and broad allowlist are optional.
- P3-C9 `:32` observation windows 1,000 and 1,086 rows.
- P3-C10 `:33` record 1087 user message.
- P3-C11 `:34` Q7 post-window ledger; plan hashes.
- P3-C12 `:35` monitor single invocation (14/40); 640-line Write at 585.
- P3-C13 `:36` structural plan acceptance; behavior tests deferred to Task 14.
- P3-C14 `:37` seven verdicts, five reviewer identities, five repairs, four `fix` replies.
- P3-C15 `:38` older-pin judged nonblocking at 697; equal-tag case at 804.
- P3-C16 `:39` protocol migration reopened the compliant result with no repair between 849 and 906.
- P3-C17 `:40` trap regression 759-762 reproduced at 1240; sibling guard only on the detect job.
- P3-C18 `:41` argument-size failure with 89 tags; the roughly 9,000 ceiling is theoretical; field-10 cap.
- P3-C19 `:42` edits at 1164-1170 were blocked.
- P3-C20 `:43` prefix endpoint 1247; acceptance 1250; completion 1261; no eighth review.
- P3-C21 `:44` out-of-window adviser activity (859 listing; 1620-2049; 1670, 1997).
- P3-C22 `:45` monitor Tasks 10 and 11 one-repair convergence.
- P3-C23 `:46` Session 19 nine compliant reviews.
- P3-C24 `:47` deck citations :280, :312, :501-518, :505, :547-548.
- P3-C25 `:48` Section 10 descriptions of Partition 3 inventory items.

**Partition 4 (`qa-source-fidelity-report-4.md`, Focus checks that held):**
- P4-H1 `:29` hidden nested second FINAL (nested `:116`; parent 1989/1991; ledger lines 37-44).
- P4-H2 `:30-36` stale or blank citations against delivered behavior (1425; blank line 10; 2012; 2015/2016 digest; Task 10 reviewer `:16`/`:33`).
- P4-H3 `:37-42` accepted-criterion and authority limits (`t6-owner-acceptance.md:10-13`; 2028; 1215/1230; `a6d8fbaf…:61`).
- P4-H4 `:43` separate package controls (390, 396, 411, 415, 435; ledger lines 8 and 11-13).
- P4-H5 `:44-48` full population exclusions (all 30 slots; slots 09-14, 17, 25, 26, 28-30; slot 17 record 1295).
- P4-H6 `:49-52` current rules against historical executions (`qa.md` `faff03b7…` at 20:29:54.0176Z between the loads; rubric hashes from record 18; installed line anchors).
- P4-H7 `:53` no fabricated history (capture retained; .651Z changed to .777Z traced to `phase3-evidence-c.md:71-75`).

**Cross-source (`qa-cross-source-contradictions-report.md`, rows with Severity None):**
- XS-R1 `:16` Orca 13/3 narrative versus 14/2 checklist.
- XS-R2 `:17` Orca no-op versus patch-check contradiction preserved.
- XS-R3 `:18` Orca prefetch versus self-check contradiction preserved.
- XS-R4 `:19` credential ledger omits the second FINAL.
- XS-R5 `:20` two rubric loads bracket the install.
- XS-R6 `:21` monitor ledger versus transcript verdict count.
- XS-R7 `:22` documentation ledger versus two reviews.
- XS-R8 `:23` oracle test counts per review stage.
- XS-R9 `:24` CI review counts are not confused.
- XS-R11 `:26` `unresolved_conflicts: 0` scope versus dissent.
- XS-R12 `:27` seven-pair equality aged.
- XS-R13 `:28` preserved plan and source version hashes.

## Cycle-0 FAIL Set

|F_0| = 10 (deduplicated).

| ID | Severity | Raw origin | Status |
|---|---|---|---|
| F-01 | IMPORTANT | P1 Finding 1 | Open |
| F-02 | IMPORTANT | P1 Finding 2 | Open; disclosure required; further action is USER DECISION 2 |
| F-03 | MINOR | P1 Finding 3 | Open |
| F-04 | MINOR | P1 Finding 4 | Open |
| F-05 | IMPORTANT | P2 Finding 1 | Open; disclosure required; keep or remove is USER DECISION 1 |
| F-06 | MINOR | P2 Finding 2 | Open |
| F-07 | IMPORTANT | P3 Finding 1 + cross-source row `:25` (XS-R10) | Open; includes the U-1 contradiction marker |
| F-08 | MINOR | P3 Finding 2 | Open; same paragraph as F-09 |
| F-09 | IMPORTANT | P4 Finding 1 | Open; same paragraph as F-08 |
| F-10 | MINOR | P4 Finding 2 | Open; includes the unverified scope-04/05 residual |

Not in the set: J1 (known, user-accepted, `report-gate-decision.md:116`). Also not in the set: the map errors at `fidelity-source-map.md:299,303` and the cross-source limitation line `:47`, because they are review-infrastructure records, not report defects.

## QA Complete

**Verdict: FAIL.** All five expected fidelity reviews are present and all returned FAIL. Ten deduplicated fidelity defects are open (5 IMPORTANT, 5 MINOR). Two need a user decision on how far the correction goes, but their disclosure corrections are required either way. None of the required corrections changes a rank or a ranked cause. Removing the Coder Git evidence (decision 1) or re-ranking by likelihood (decision 2) would, and either would invalidate the affected earlier gates until they are actually rerun.

| Status | Result |
|---|---|
| DONE | Merged 5 of 5 fidelity reviews against the report (sha256 `9ac64f13…e568`, 1,310 lines). 11 raw issues reduced to 10 (F-07 kept at IMPORTANT). |
| DONE | Spot-checked all 10 findings against primary lines and records, including a fresh hash of monitor record 874 (`bd66451d…`) that confirms F-09 and corrects the map and the cross-source limitation line. |
| DONE | Froze 84 cycle-0 PASS identities and the 10-item FAIL set. One irreducible contradiction (U-1) is bounded with a marker; two existing Orca markers are preserved. |
| NEXT | User decides item 1 (keep the Coder Git evidence disclosed, recommended, or remove it) and item 2 (disclosure only, recommended, or re-rank by likelihood) before or alongside Step 6.29. |
| NEXT | Step 6.29: one serialized fixer applies F-01 to F-10, with F-08 and F-09 in a single edit of Report:578, and checks the scope-04/05 provenance residual. Steps 6.30-6.31 then re-verify every FAIL item and every PASS identity above. |

## Erratum: Frozen PASS-Set Count (Phase 6 /task gate, 2026-10-24, finding G6-45)

**Attribution:** appended by the Phase 6 /task phase-gate fixer, applied by the parent. The consolidator's text above is unchanged.

The Summary line at `:60` and the DONE row near the end state 84 frozen cycle-0 PASS identities. The Cycle-0 PASS Set lists 70: Partition 1 14 (P1-S1 to P1-S9 and P1-C1 to P1-C5), Partition 2 12, Partition 3 25, Partition 4 7, cross-source 12. The 84 counts the "14 ranges inside P1" a second time. The structural verifier recorded this correction (`qa/qa-fidelity-verification-structural.md:109`), and `phase-outputs/plans/fidelity-gate-decision.md:16` uses 70. The frozen set is 70.
