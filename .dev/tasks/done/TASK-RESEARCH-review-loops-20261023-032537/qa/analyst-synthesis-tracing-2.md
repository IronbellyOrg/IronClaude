# Synthesis Quality Review: Source Tracing, Partition 2

**Topic:** Phase 5 synthesis gate
**Date:** 2026-10-24
**Status:** Complete
**Files reviewed:** 3 targets: `synthesis/synth-04-options-recommendation.md`, `synthesis/synth-05-implementation-plan.md`, `synthesis/synth-06-questions-evidence.md`. They were traced against all five hypothesis cards, every debate artifact named by `reviews/adversarial/run-evidence.md`, the six case reports, the evidence deck, the rule map, the gap register, `web-01-gap-applicability.md`, the QA and phase-output inventories, and the three external rendering targets that synth-05 cites.
**Lens:** source-tracing (Synthesis Quality Review Checklist items 6-10, plus the Step 5.16 tracing obligations)
**Task item:** Step 5.16
**Partition:** 2 of 2
**Governing template:** Project rf-analyst Synthesis Quality Review Output Format; tech-research synthesis checklist (`/config/.claude/skills/tech-research/SKILL.md:1506-1529`)

## Overall Verdict: FAIL (8 issues)

## Per-File Review

### synth-04-options-recommendation.md
**Sections covered:** 6 and 7
**Verdict:** FAIL

| Check # | Check | Result | Evidence/Issue |
|---------|-------|--------|---------------|
| 6 | Implementation-plan specificity (here: proposed next checks have real targets) | FAIL | §7.6 (line 286) says "Step-level targets are in Section 8". Step 1 includes the monitor replay (line 290), but synth-05's matching row (synth-05:72) names no monitor input. Step 4 (line 293, extend to new independently selected sessions) has no Section 8 target at all. Issue 4. |
| 7 | Cross-section consistency | FAIL | Same break with Section 8 as above. All five rank entries match `ADV/debate-transcript.md:477-486`, `return-contract.md:24` and `merged-root-cause-analysis.md:37-43`. |
| 8 | No doc-only claims in Sections 6/7 | PASS | Every current-rule statement is labelled "source-read only" and cites the code-verified rule map (`research/scope-rules.md:32,41,43,45,56`). Current text is never used as proof of what historical runs loaded. The installed-versus-checkout drift is cited (`gaps-and-questions.md:56`). |
| 9 | Stale / contradicted sources surfaced | PASS | Line 64 and line 282 surface the installed/checkout drift. The two historical rubric loads are cited (`scope-rules.md:70-71`). |
| 10 | Key-finding coverage | FAIL | The §7.7 table covers all six cases, the deck, the rule map and the gap register. However, line 311 claims the screened controls "reach this component through the evidence deck's counterexample table (`:643-662`), which is cited here". No section 6/7 row uses the Session 09/10/13-14/17/19 controls (deck:650-655). Issue 5. |
| T1 | Each ranked cause traces to the actual debate | FAIL | The 7.1 and 7.2 orders and pair tallies are exact. All quotes were verified (`:128,167,208,256-257,264,265,302-304,333-335,343,380,384-385,414-416,421,425,426`). But the "against" position for Option B (line 90) and the rank-3 row (line 213) is attributed to the V3, V4 and V5 advocates while citing only `:129,343,425`. That is no V4 anchor. Issue 3. |
| T2 | Each cause traces to primary cases | FAIL | Line 64 cites planning log 943/944 as plans that "passed structural checks and still received substantive semantic findings". Record 943/944 is v4's structural pass, followed by 946 "NOT CHECKED: v4 has had no review" (`research/01-session-ac2cd1fd.md:86-87`). Issue 1. Line 67 also overstates hash matching (Issue 2). Every other anchor checked substantiates its claim (see Source Bindings). |
| T3 | No fabricated run, signature or current-to-past inference | PASS | All replays are marked "Proposed, unexecuted". No function or signature appears. Writing scores, convergence and the base selection are explicitly separated from likelihood (§6.0, §7.3; `base-selection.md:150,170-171`; `invariant-probe.md:18-20`). |

### synth-05-implementation-plan.md
**Sections covered:** 8
**Verdict:** FAIL

| Check # | Check | Result | Evidence/Issue |
|---------|-------|--------|---------------|
| 6 | Specific steps with real file paths | PASS | All 11 input paths exist. The three external rendering targets exist, and their cited lines match: task file 81-87 (Task 6 AC "when `man` is available"), `t6-fix-evidence.log:1-3` (no renderer, 275-byte notice), `progress.md:14-18` (cannot-verify, head-moved halt, acceptance ruling, FINAL pass). Case section references resolve to real headings. |
| 7 | Cross-section consistency | FAIL | Row 1 (line 72) leaves out the monitor context that synth-04 §7.6 step 1 assigns to it. No row matches synth-04 step 4. Issue 4 (shared). |
| 8 | No doc-only claims | PASS | Line 100 explicitly asserts no current architecture. Historical loads govern historical comparisons. |
| 9 | Stale sources surfaced | PASS | The installed/checkout freshness warning is kept (line 48). The rule that a missing ledger FINAL is not inserted is kept (line 75). |
| 10 | Key-finding coverage | PASS | The table at lines 111-122 covers every required input, including `web-01` (reasoned N/A). |
| T4 | Every next check traces to a real target or gap | PASS | Five rows map one-to-one onto V1-V5. Record anchors check out: 544/545, 841, 585, 759-762, 1240, 849, 874/884, 893/902, 906, 383/450, 521/573/668, 430/443/450, 506 (`research/03-session-6f744b87.md:177`). Deck ranges `:376-422,:430-459,:490-518,:528-569,:585-598,:814-847`, gaps `:33-59,:43-59`, rule map `:66-88` and web-01 `:97-148` all hold the described content. |
| T5 | No omitted control | FAIL | The "Preserve successful-repair controls" row (line 88) lists only Orca amendments, oracle repairs 1-3, monitor Tasks 10/11 and the initial credential package. It omits the deck's screened controls: Session 10 Task 4, Session 17 Task 8 and FINAL, Sessions 09/19 and 13/14 (deck:650-655). Session 17's FINAL is a real delivery bug corrected before PASS, which bears directly on the proof-only comparison. Issue 6. |
| T3 | No fabricated run or signature | PASS | The integration checklist is N/A and lines 128-133 say no checks were executed. |

### synth-06-questions-evidence.md
**Sections covered:** 9 and 10
**Verdict:** FAIL

| Check # | Check | Result | Evidence/Issue |
|---------|-------|--------|---------------|
| 7 | Cross-section consistency | FAIL | §10.1 (line 51), §10.4 (line 128) and §10.8 (line 223) say synth-04 is absent and synthesis/ holds 10 files. synth-04 now exists, with a 2026-10-24 Parent Persistence Record (synth-04:339-341). Issue 8. |
| 9 | Stale / contradicted sources surfaced in Section 9 | PASS | Q20 surfaces the rule map's "no source/installed divergence" (`scope-rules.md:92`), which the later 4-of-7 drift contradicts (`gaps-and-questions.md:56`). Q15 and Q17 surface pointer and live-byte staleness. |
| 10 | Key-finding coverage | PASS | Q1-Q20 trace to deck:827-847, gaps:29-59, scope-rules:64-96 and return-contract:23-31. Zero external findings are traced to web-01:97-123. |
| T6 | Source index matches real producer artifacts | FAIL | (a) Line 145 credits `plan-review-evidence.md` with "original canonical-review failure ... targeted passing re-review". That file holds only the transcript-input PASS, identity notes and the source guard; the FAIL and re-review are in `merge-log.md:161-163`. Issue 7. (b) The inventory is stale against the current package. Issue 8. |
| T7 | Counts derived from actual files | PASS at snapshot | research 23, reviews 17, phase-outputs 9 and root 4 match the files on disk. A brace-expanded `ls` of all 191 named QA files found no missing file. The 133 + 58 group sums are correct. |
| T3 | No fabricated run or current-to-past inference | PASS | The merge PASS is scoped (lines 148-150). The gate-decision citations hold: `task-phase3-gate-decision.md:71` (20:48:38 authorization) and `task-phase4-gate-decision.md:134-177`. The erratum citation holds (`qa/qa-phase-3-fix-log.md:95-116`). |

## Claim, Card, Debate and Key-Takeaway Source Bindings

| Claim (target location) | Traced source | Result |
|---|---|---|
| V1 first, unanimous (synth-04 7.1 rank 1) | `ADV/debate-transcript.md:258,297,337,378,419,477-484` | Substantiated |
| V3 second, 3/5 (rank 2) | `:343,380,421`; `invariant-probe.md:43` | Substantiated |
| V2 third, disputed (rank 3) | `:264,302,343,425`; V4 support exists at `:168,385` but is not cited | Partly anchored (Issue 3) |
| V5 above V4 on the 2/5 side, as a reviewed qualified judgment | `:384-385,426,486`; `refactor-plan.md:32`; `plan-review-evidence.md:16` | Substantiated |
| Writing base V4 by tiebreak, not likelihood | `base-selection.md:5,150-155,170-171`; `merged-root-cause-analysis.md:21` | Substantiated |
| Status partial, Round 3 not run | `return-contract.md:14,16,24,26`; `debate-transcript.md:449-450` | Substantiated |
| Option A primary support (oracle 67/78 tests, monitor 640 lines, Orca coverage, CI stub) | `research/02-session-a9b88895.md:228`; `research/05-session-e002bed2.md:56,64,84`; `hypothesis-01.md:54-57`; `research/04-session-43582de1.md` §6.2 and supplement §5 | Substantiated |
| Option A, "passed structural checks and still received findings (499, 843/849, 943/944)" | `research/01-session-ac2cd1fd.md:69,78,86-87` | 943/944 does not substantiate (Issue 1) |
| Orca v1-v4 "with matching hashes" | `research/01-session-ac2cd1fd.md:323` (first two plus final only) | Overstated (Issue 2) |
| Option B introductions; CI "two of four downgraded"; same source hash | `research/01-session-ac2cd1fd.md` §3.1-3.5, `:208-215,341`; `research/04-session-43582de1.md:16`; deck:378-379,383 | Substantiated |
| Option C rubric loads, relaxation, migration, source contradictions | `scope-rules.md:70-71`; `research/06-session-0690ee9f.md:160,167,179`; deck:706; `research/01-session-ac2cd1fd.md:296-297`; `hypothesis-03.md:57-58,107` | Substantiated |
| Option D proof loss, trees, missing t10 log | `hypothesis-04.md:57-59,104,151`; `research/03-session-6f744b87.md:216,229,237`; `research/06-session-0690ee9f.md:116` | Substantiated |
| Option E exclusion at 383, render notice, three current hashes | `research/02-session-a9b88895.md:208,214`; `research/03-session-6f744b87.md:177,341-358`; the external `t6-fix-evidence.log:1-3` | Substantiated |
| Credential Task 10 overreach (7.5) | `research/06-session-0690ee9f.md:222` (record 2028) | Substantiated |
| Recommendation is research-only, needs approval | `merged-root-cause-analysis.md:170,205`; `web-01:131-133` | Substantiated |
| Next check order (7.6) linked to Section 8 | synth-05:72-76 | Incomplete (Issue 4) |
| Screened controls represented (7.7) | deck:650-655; no use anywhere in synth-04 or synth-05 | Not represented (Issues 5 and 6) |
| synth-06 adversarial artifact descriptions | `plan-review-evidence.md:1-74`; `merge-log.md:161-163` | One mismatch (Issue 7) |
| synth-06 current package state | live `ls`: synthesis 11 files, qa 202; card headers; `qa/synthesis-component-intake.md:5,63` | Stale (Issue 8) |

Key Takeaways traced: case 01 (correction-induced plus coverage over-credit), case 02 (labels are not meaning, frozen fixture), case 03 (head-moved is not proof, acceptance is not rendering), case 04 (several "new" findings were not fix-caused), case 05 (seven verdicts, one trap regression, migration reopening), case 06 (lost proof, relaxation, missing ledger FINAL). The deck's "no single uniform loop / no fleet rate", the rule map's "current is not historical", and web-01's "N/A, zero findings" are each represented in at least one target. The exception is the screened-control takeaway (deck:666 "Successful repairs are real counterevidence"), which is only partly represented.

## Issues Requiring Fixes
| # | File | Check | Issue | Required Fix |
|---|------|-------|-------|-------------|
| 1 | synth-04 | T2 | Line 64 lists planning log 943/944 among plans that "passed structural checks and still received substantive semantic findings". 943/944 is v4's structural pass, and v4 received no semantic review (record 946; `research/01-session-ac2cd1fd.md:86-87`). This contradicts the unreviewed-v4 endpoint used in synth-06 Q5. IMPORTANT. | Remove 943/944 from that support list, or state that v4 passed the structural gate and was never semantically reviewed. |
| 2 | synth-04 | T2 | Line 67: "Orca v1-v4 reconstructable ... with matching hashes". `research/01-session-ac2cd1fd.md:323` reports matches only for v1, v2 (review snapshots) and v4 (live plan). The v3 hash `cbfb606…` has no comparison target. MINOR. | Say that v1, v2 and v4 match their snapshot or live comparisons and that v3 is reconstructed without an independent match. |
| 3 | synth-04 | T1 | Lines 90 and 213 attribute the anti-V2 position to the V4 advocate without a V4 anchor (only `:129,343,425` are cited). MINOR. | Add `ADV/debate-transcript.md:168` (V4, Round 1) and `:385` (V4, Round 2). |
| 4 | synth-04, synth-05 | 6, 7, T4 | synth-04 line 286 says the step-level targets are in Section 8. synth-05's row 1 (line 72) has no monitor input, although step 1 (line 290) and Option A include the monitor's record-585 replay. synth-04 step 4 (line 293) has no Section 8 row at all. IMPORTANT. | Add the monitor case (record 585, §§2 and 4) to synth-05 row 1. Either add a scoped step-4 entry to Section 8 or reword synth-04 line 286 to say that step 4 traces only to the generalization gap (`gaps-and-questions.md:11`; synth-06 Q1). |
| 5 | synth-04 | 10, T5 | Line 311 claims the screened controls are represented through deck:643-662, "which is cited here". No section 6/7 row uses Session 09/10/13-14/17/19 (deck:650-655). In particular, Session 17's FINAL (a real delivery bug corrected before PASS, deck:652) is unused, although it bears on V4's proof-only scope. IMPORTANT. | Add these controls to the relevant Opposition rows or the §7.4 caution table, or replace the claim with an explicit, justified exclusion. |
| 6 | synth-05 | T5 | The "Preserve successful-repair controls" row (line 88) cites "All six case files; evidence deck" but lists only in-case controls and drops the deck's screened controls (deck:650-655). IMPORTANT. | Add the Session 10 Task 4, Session 17 Task 8 and FINAL, Session 09/19 and Session 13/14 controls with their deck limits, or state why they are out of scope. |
| 7 | synth-06 | T6 | Line 145 credits `plan-review-evidence.md` with the "original canonical-review failure ... and targeted passing re-review". Those records are in `merge-log.md:161-163` (`agent-aba0ed57846538ad4.jsonl:79` FAIL; `agent-a815d047710b89c22.jsonl:38` PASS), and line 146 (merge-log) omits them. The inherited wording at `run-evidence.md:18` is outside this partition. MINOR. | Move the canonical-review FAIL and targeted re-review to the merge-log row and describe plan-review-evidence as the transcript-input PASS, identity notes and source-directory guard. |
| 8 | synth-06 | 7, T6 | The inventory snapshot (2026-10-23T22:14:30Z) no longer matches the package: (a) lines 51, 128 and 223 say synth-04 is absent and synthesis/ has 10 files, but it exists (11 files); (b) lines 123-126 and 220 describe card ten-section format closure as unresolved and point to "debate pending" headers, but all five cards are now ten-section format-only presentations with §10.5 persistence records, and the pending wording appears only as quoted history (e.g. `hypothesis-04.md:177-185`); (c) lines 52, 154 and 190 give 191 QA files and an "unfinished skeleton" intake, but qa/ now has 202 files and `synthesis-component-intake.md` is Complete with 5/5 persisted. The snapshot framing and the refresh requirement (line 227) are honest, but the component as delivered to this gate contradicts synth-04 and the cards. IMPORTANT. | Refresh §§10.1, 10.4, 10.6 and 10.8 in the Step 5.24 correction pass (or at assembly, recorded explicitly) from a new observed inventory. Keep the original snapshot as history. |

## Summary
- Files passed: 0
- Files failed: 3
- Total issues: 8 (IMPORTANT 5: Issues 1, 4, 5, 6, 8; MINOR 3: Issues 2, 3, 7)
- Critical issues (block assembly): 0. Issue 8 must still be resolved before final assembly, because the component carries an explicit refresh requirement.

## Self-Audit
- Read in full: the Step 5.16 text, the checklist at `SKILL.md:1506-1529`, the stub, all three targets, the debate transcript (lines 1-489), the return contract, the invariant probe, the refactor plan, the plan-review evidence, the merged analysis, the diff analysis, run-evidence and the gap register.
- Read in part: the rule map (all), the deck (lines 1-140, 370-430, 555-744, 800-900), base-selection lines 1-180, cards 01 and 04 (§§1-10.1), card 02 §6, the case 01/02/03/04/05/06 passages cited above, both intake files, `qa-phase-3-fix-log.md:90-119` and the phase-gate cited lines.
- Verified with tools: every brace-expanded QA filename in synth-06 §10.6 exists (191/191). The modification times identified the 12 newer QA files. Card headings confirm the ten-section format. The three external rendering targets were read at their cited lines.
- Checked for these defect classes: fabricated runs, signatures, probabilities or percentages (none found); doc-only current architecture (none); current-to-past inference (none). Anchor-to-claim substantiation was checked semantically, not by ID matching, which is how Issue 1 was found.
- Side effect, disclosed: one `ls` command also wrote a scratch listing to `/tmp/qa_actual_list_review.txt`. It is not a package file and was not used. No target or package file was edited. No agent, test, Git, staging, archive, move or delete action was taken.

## Partition Limits and Evidence Boundaries
[PARTITION NOTE: Cross-file checks limited to assigned subset. Full cross-file analysis requires merging all partition reports.]
- synth-01/02/03 (partition 1) were not traced. Consistency with Sections 2-5 is not assessed here.
- Not read directly: `variant-*-original.md`; `score-source-manifest.json`; `base-selection.md` past line 180; cards 03 and 05 beyond their grepped sections; the case reports outside the cited passages. Card-to-original preservation was taken from each card's §10.5 record and was not re-hashed.
- Historical JSONL physical records were not replayed. Record anchors were checked against the case reports and cards, not against the original session logs.
- Graph coverage was unavailable for package files, so every conclusion comes from direct reads.

| Status | Result |
|---|---|
| DONE | Traced synth-04/05/06 claims, ranks, next checks, controls and the source index to the debate, cases and artifacts on disk. Result: FAIL with 8 issues. |
| NEXT | Parent persists this exact text at `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/analyst-synthesis-tracing-2.md`. Step 5.23 consolidates the findings. |