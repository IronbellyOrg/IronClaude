# QA Report - Synthesis Coherence, Partition 2

**Topic:** Phase 5 synthesis gate
**Date:** 2026-10-24
**Status:** Complete (report-only review; returned as text because report-file writes are prohibited for this reviewer)
**Phase:** synthesis-gate
**Lens:** synthesis-coherence
**Task item:** Step 5.22
**Partition:** 2 of 2
**Fix cycle:** N/A
**Fix authorization:** false
**Governing template:** Project rf-qa-qualitative Output Format (All Phases); tech-research qualitative review template (`/config/.claude/skills/tech-research/SKILL.md:995-1040`, 12-item checklist, used as the reference checklist) and synthesis-coherence lens (`SKILL.md:507`)

---

## Overall Verdict: FAIL

## Criteria and Partition Scope

**Assigned targets:**
- `synthesis/synth-04-options-recommendation.md` (342 lines)
- `synthesis/synth-05-implementation-plan.md` (140 lines)
- `synthesis/synth-06-questions-evidence.md` (232 lines)
- the five cards `synthesis/hypothesis-01.md` through `hypothesis-05.md`

**Supporting inputs read:**
- `reviews/adversarial/run-evidence.md`
- the debate artifacts it locates (`ADV/` = `reviews/adversarial/adversarial/`)
- `research/evidence-deck.md`
- `gaps-and-questions.md`
- `synthesis/synth-02-target-gaps.md` (Gap Analysis only, for the gap-to-check link)

**Criteria (Step 5.22, task file line 351):**
- Are the five causes distinct, and is their overlap explicit?
- Does the actual debate evidence support the likelihood order?
- Are opposing controls retained?
- Is the recommendation proportionate?
- Are the unexecuted next checks realistic?
- Is the uncertainty and evidence index complete?
- Do the gaps, options, recommendation and plan agree?
- Presentation polish must not be treated as causal proof.
- No fabricated probability, no falsely finished artifact, no implementation authorization.

These are mapped onto the 12-item qualitative checklist, plus four step-specific checks.

**Original hypothesis identities:** the immutable `ADV/variant-1..5-original.md`. Card Section 10.5 Parent Persistence Records were treated as delivery receipts, not approvals.

[PARTITION NOTE: Cross-file checks are limited to the assigned subset. synth-02 was read only to test gap-to-check links. Partition 1 targets (synth-01 to synth-03) were not reviewed. Full cross-file verification requires merging both partition reports.]

## Items Reviewed

| # | Check | Result | Evidence |
|---|-------|--------|----------|
| 1 | Problem statement matches findings | PASS | synth-04:8 restates the research question. All five options and 7.1 answer "why a repair/pass was followed by another failed review or entry". The sample boundary (synth-04:39-42) matches evidence-deck:49-58: three strict incidents (oracle, monitor, credential follow-up), one render blocker, two planning loops. |
| 2 | The five causes are distinct, and overlap is explicit | FAIL | The 7.4 overlap table and the confounding rows are explicit and correct. However, the retained-sibling transition has contradictory owners (Issue 4). |
| 3 | The recommendation and likelihood order follow from the actual debate | FAIL | 7.1 and 7.2 match `ADV/debate-transcript.md:477-486` exactly. So do the advocate tallies, the refactor-plan rationale (`ADV/refactor-plan.md:28-34`) and the plan review (`ADV/plan-review-evidence.md:16`). However, the justification for rank 5 misstates V4's reach (Issue 3), and "only unanimous placement" conflicts with the derived 5-of-5 tier (Issue 6). |
| 4 | Next checks are actionable and realistic | FAIL | The Section 8 rows are specific and correctly labelled unexecuted. However, Section 8 does not carry the 7.6 order, the monitor context or step 4 (Issue 1). Option D's reuse row understates evidence that is currently present (Issue 7). |
| 5 | Gaps are honestly acknowledged | PASS | synth-06 has 20 open questions that track evidence-deck:827-845 and gaps-and-questions:29-59. synth-05:91 is "Stop at the evidence boundary". synth-04:328-331 states its limits. Reviewer-miss reasons, the rubric updater and runtime behavior stay unknown. |
| 6 | No circular reasoning | PASS | The rankings cite the transcript and plan artifacts, not the synthesis itself. One self-referential coverage claim (synth-04:311) is recorded under check 13 rather than counted twice. |
| 7 | The evidence trail is complete | FAIL | synth-06 Section 10 is a 2026-10-23T22:14:30 snapshot that now misstates synth-04 and the card state (Issue 5). The QA inventory spot checks passed: eight named files exist, 18 and 24 group counts match, and the Phase 3 verification set is 7 PASS / 1 FAIL as stated at synth-06:166. |
| 8 | Conclusions are proportionate to evidence strength | PASS | The order is labelled `partial` and non-consensus. The bottom pair is disclosed as following the 2-of-5 side (synth-04:240-242). 7.3 denies probability, generalization and execution. "Run no remediation" is stated. |
| 9 | External research is properly contextualized | PASS | synth-06:38 records zero external queries and a reasoned N/A. No external claim overrides case evidence in synth-04 or synth-05. |
| 10 | Gap, options, recommendation and plan agree | FAIL | synth-02 gaps 1-5 map to Options A-E and to the synth-05 checks. However, synth-05 contradicts synth-04 7.6 on sequencing and scope (Issue 1). |
| 11 | Technical accuracy against research files | PASS | Spot-checked anchors all match their sources (see Self-Audit). |
| 12 | Depth matches the tier (Deep) | PASS | There are five full assessment tables, a comparison table, exact advocate orders, pair tallies, a current-versus-historical split, overlap cautions and a 20-question register. |
| 13 | Opposing controls are retained | FAIL | Screening-level controls (evidence-deck:650-655) are missing from the options and the plan, and the coverage claim is self-referential (Issue 2). |
| 14 | Presentation polish is not treated as causal proof; no probability | PASS | synth-04:22-30 and 7.3 separate writing convergence, base selection (tiebreak, `ADV/base-selection.md:150`) and the 95% process confidence from causal support. A grep for `%`, "probab" and "likel" across synth-04/05/06 found no causal probability. |
| 15 | No falsely finished artifact or implementation authorization | PASS | synth-04:286 and synth-05:101 and 128-133 say approval is required and the checks are UNEXECUTED, with the integration checklist N/A. Persistence of synth-05 and synth-06 is attributed in `qa/synthesis-component-intake.md:41-42`. The synth-04 header's "pending" state is resolved by its own record at :341. |
| 16 | Card preservation claims are coherent | PASS | In card 5, "34 original lines" (hypothesis-05.md:258) against "27 body lines" (:262) reconciles as 27 body lines plus 7 header lines (:207). A recount of `variant-5-original.md` gives 34 non-blank, non-heading lines, and its sha256 `1cf685b5…41ac` matches 10.5. All five card headers now read "Post-debate format-only presentation". |

## Summary
- Checks passed: 10 / 16
- Checks failed: 6
- Critical issues: 0 (issues by severity: 5 IMPORTANT, 2 MINOR; 7 total)
- Issues fixed in-place: 0 (report-only)
- **Confidence:** Verified: 16/16 | Unverifiable: 0 | Unchecked: 0 | Confidence: 100.0%. The verdict is FAIL because issues exist.
- **Tool engagement:** Read: 14 | Grep: 0 dedicated (about 20 grep and sed inspections ran inside 11 Bash calls) | Glob: 0 | Bash: 11

## Issues Found

| # | Severity | Location | Issue | Required Fix |
|---|----------|----------|-------|--------------|
| 1 | IMPORTANT | synth-05:64-78 vs synth-04:61-70 and :284-293 | **The recommendation and the plan disagree.** (a) synth-04:286 says "Step-level targets are in Section 8" and 7.6 sets an order: Option A first, then C with B, then D and E, then new sessions. synth-05:68 instead says its rows are "not an execution sequence" and lists them in card order. (b) 7.6 step 1 and Option A replay four contexts: oracle, monitor, Orca and CI. synth-05's "Check what acceptance actually proves" row lists the oracle, Orca planning and CI cases but omits the Orca monitor case (record 585 workflow, deferred Task 14 tests). (c) 7.6 step 4 has no Section 8 step. Step 4 applies the C-001 labels to additional, independently selected sessions, and synth-04 calls it the only way to settle the disputed pairs. synth-05 predates synth-04: file mtimes are 22:17 on 2026-10-23 for synth-05 and 01:03 on 2026-10-24 for synth-04. | Either (i) add a priority column to synth-05 Phase 2 citing synth-04 7.6, add the Orca monitor case (records 585 and 804-1021, Task 14 deferral) to the acceptance-proof row, and add a step-4 row marked as needing a user scope decision; or (ii) remove synth-04:286's claim that Section 8 holds the step-level targets and state that 7.6 alone governs order. Keep all rows UNEXECUTED and approval-bounded. |
| 2 | IMPORTANT | synth-04 Opposition rows (:58, :85, :112, :139, :163), synth-04:311; synth-05:88 | **Opposing controls are missing.** The screening controls in evidence-deck:650-655 appear nowhere in the options, the ranking or the plan's controls row: Session 10 Task 4 one-repair compliance; Session 17 Task 8 corrected deviation; Session 17 FINAL, where a real restore-basename bug was corrected and then passed; Session 09; Session 19; and Sessions 13/14 (authorized plan corrections without semantic re-review). Session 17 FINAL directly opposes an evidence-only reading of FINAL repeats (V4). Sessions 13/14 bear on the V1 and V2 planning claims. synth-04:311 says these controls "reach this component through the evidence deck's counterexample table ... which is cited here", but that sentence is the only place the table is cited. synth-05:88 lists only Orca, oracle, monitor Tasks 10/11 and the initial credential repair. | Add each relevant screening control, with evidence-deck:650-655 anchors, to the Opposition row of the candidate it challenges (at minimum Session 17 FINAL under D, Sessions 10 and 17 one-repair convergence under A, B and E, and Sessions 13/14 under A and B). Add them to synth-05's "Preserve successful-repair controls" row. Replace synth-04:311 with an honest per-control treatment, or give an explicit exclusion rationale for each control. |
| 3 | IMPORTANT | synth-04:215 (7.1, rank 5) vs :141, :182 and `ADV/refactor-plan.md:32` | **Contradiction about the reach of the last-ranked cause.** The rank-5 justification says V4 has "Narrow reach in one work family". The same component's Option D Scope says "two selected sessions and three package/task contexts". The comparison table says "Credential (one work family), documentation baseline". The refactor plan says "concentrated in credential/documentation work". The cited transcript line `:381` says only "Credential packages remain one work family". This misstates the evidence in the cell that justifies the lowest placement. | Reword the rank-5 cell to: "Narrow reach: one credential work family plus one documentation-baseline task; some evidence explains attribution or a halt rather than the repeat (`ADV/debate-transcript.md:381,384`; `ADV/refactor-plan.md:32`)." |
| 4 | IMPORTANT | synth-04:74 vs :86-87, :181 and :211-215; hypothesis-01.md Section 6 "Scope, Overlap and Competing Explanations" | **The "repair missed a sibling failure" transition has contradictory owners.** Examples are the CI hash exemption, unasserted CI search arguments and the monitor pin-trap sibling guard (evidence-deck:591-593). Option B's Description says V2 can "leave a sibling failure in place". Option B's Scope covers only absent-before/present-after failures, and its Alternative explanations call incomplete fixes "a different explanation from introduction". Card 1 assigns "fails to cover sibling paths" to candidate two. Neither the comparison row "Transition it best explains" nor the 7.1 override column assigns this class to anyone. | In synth-04, state one owner for retained siblings, consistent with debate S-002 and C-003, which keep them separate from introduction (`ADV/debate-transcript.md:269,272`). Align the Option B Description, the comparison table and the 7.1 override column with that owner. Note card 1's wording as a preserved pre-debate card statement. Do not edit the card's original lines. |
| 5 | IMPORTANT | synth-06:51, :119, :123-128, :223 | **The evidence index contradicts the current partition-2 inputs.** synth-06 says synthesis/ has 10 files and that synth-04 is "absent" (at :51, :128 and :223). It also says the hypothesis-04 and -05 cards carry a "debate pending" header and that their ten-section format acceptance is unresolved. Observed now: synth-04 exists (53,087 bytes, Parent Persistence Record at :339-341). All five cards are post-debate ten-section presentations with Section 10.5 persistence records, and no card header says "debate pending". synthesis/ holds 11 files and qa/ holds 202 (synth-06 says 191). The snapshot is disclosed and an assembly refresh is required (:227). Even so, a synthesis-gate PASS would certify statements that are now false about two partition-2 inputs. | In the Step 5.24 correction pass, append dated superseding rows to 10.1, 10.4 and 10.8. Each row should record: synth-04 present and parent-persisted, with gate pending; cards reformatted with persistence records, with format acceptance pending this gate; the Phase 5 QA reports; and the current counts. Keep the 2026-10-23T22:14:30 snapshot rows labelled historical, and do not rewrite them. |
| 6 | MINOR | synth-04:69, :204, :290 vs :236 | **Labelling inconsistency.** synth-04 says "V1 first is the only unanimous placement". Its own pairwise table derives a second 5-of-5 placement that reaches the threshold: V1, V2 and V3 each sit above V4 and V5 in all five recorded orders. Both statements are true only if "placement" means exact rank at :204 and pairwise grouping at :236. The rationale also omits the unanimous top-three/bottom-two split, which supports doing the D and E checks last. | Say "the only unanimous exact rank position" at :69, :204 and :290. Add the derived unanimous tier, labelled as derived and not stated in the debate, to the 7 Rationale. |
| 7 | MINOR | synth-04:148 (Option D, "Reuse of existing code/evidence") | **Available evidence is understated, so check D's realism is understated.** The row implies `t10-markdownlint.log` is unavailable: "A fresh Read ... returned 'file does not exist'". A file exists now at `/config/workspace/Coder/.dev/tasks/done/TASK-WF-issue358FollowUp-20261022-193837/artifacts/t10-markdownlint.log`, and its lines 9, 10 (blank), 14 and 17 match case 06's description (`research/06-session-0690ee9f.md:202-206`). A `t3-markdownlint.log` also exists under `.../done/TASK-WF-issue358InTempla-20261022-151058/artifacts/`. Option E maps the documentation package's current root, but Option D does not consider the parallel done roots of the credential packages. This reviewer did not verify the file's identity by hash. | Add to Option D's Reuse row: "Candidate current location observed at `<path>`; identity with the historical log not hash-verified; availability to be confirmed before any approved replay." Keep card 4 Section 9 verbatim and do not certify the file. |

## Actions Taken
- None. fix_authorization is false. No target, card, debate artifact, task file or other file was modified. No agents, tests, Git, staging, archive, move, delete or publication were used. All Bash commands were read-only (`ls`, `grep`, `sed -n`, `cat`, `sha256sum`, `wc`).

## Inherited Structural Verdict - Reliance Audit
The spawn prompt contained no `## Inherited Structural Verdict` block, so this review used standalone behavior and no rf-qa PASS item was relied on. The parallel structure reviews (Steps 5.17 and 5.18) were stubs at review time and were not consulted.

## Self-Audit
**(a) Reliance list - rf-qa PASS items skipped for structural re-check:**
- None. No inherited verdict was supplied.

**(b) Independent semantic checks:**
- **Advocate orders and tallies:** synth-04 7.1, 7.2 and the comparison row were compared line by line with `ADV/debate-transcript.md:477-486`. They match, including the 3/5 and 2/5 splits.
- **Bottom-pair rationale:** traced to `ADV/refactor-plan.md:32` and to `ADV/plan-review-evidence.md:16`, where Change 2 retains V1 > V3 > V2 > V5 > V4.
- **Writing order:** "V4, V5, V2, V3, V1" and the tiebreak gap of 0.0034, below 0.05, were confirmed in `ADV/base-selection.md:150`.
- **Rank-5 "one work family" claim:** compared against transcript :381 and :384, Option D :141 and the refactor plan :32, producing Issue 3.
- **Recommendation against plan:** synth-04 7.6 was compared with synth-05 Phase 2, producing Issue 1, and with the synth-02 gap rows 1-5 (:50-54), which do map to the checks.
- **Controls:** the evidence-deck:643-662 rows were checked against every Opposition row and synth-05:88. A grep for session numbers and "643" in synth-04 and synth-05 found only synth-04:311, producing Issue 2.
- **Index currency:** synth-06 10.1, 10.4 and 10.8 were compared with the current `ls` counts (synthesis 11, qa 202), the card headers and synth-04's persistence record, producing Issue 5.

**Independent factual claims and source files:**
- 22 claims were checked against primary files:
  - monitor 640-line workflow at record 585 (`research/05-session-e002bed2.md:56,84`)
  - trap introduction 759 and reproduction 1240 (`research/05-session-e002bed2.md:103,168,205`)
  - 67/78 tests passing before the first review (`research/02-session-a9b88895.md:228`)
  - Task 10 overreach at record 2028 (`research/06-session-0690ee9f.md:222`)
  - the "proven amplifier in two runs" quote (`hypothesis-03.md:107`)
  - `qa.md:82` moved-line rule (current source)
  - `managed-workspace.md:42` pin boundary (current source)
  - `scope-rules.md` qa.md:82 and :45 mappings
  - Round 1 A-001 vector (transcript :243) and Round 2 adoptions (:277, :316, :356, :397, :438)
  - V4 advocate's reversal (:384-385) and "materially strengthens V3" (:303)
  - invariant-probe PASS scope (:18-20, :38-44)
  - return-contract fields (status partial, convergence 1.0, base variant-4)
  - post-merge validation scope (:118-121)
  - merged-analysis :43 "not the majority's complete order"
  - card 5 line count and hash
  - t10 log existence and content
  - eight QA inventory filenames and two group counts
  - Phase 3 verification verdicts (7 PASS, 1 FAIL)
  - research/ composition: 16 + 1 + 6 = 23
- Files read: the task file (Steps 5.10-6.3), the stub report, SKILL.md :500-515 and :995-1040, run-evidence.md, synth-04, synth-05, synth-06, debate-transcript :236-490, gaps-and-questions.md (full), evidence-deck :40-64 and :580-849, synth-02 :30-93, hypothesis-04 :97-160, hypothesis-05 :95-157 and :205-262, the headers and section maps of all five cards, the overlap sections of cards 1-3, base-selection :148-172, refactor-plan :28-34, plan-review-evidence :14-17, invariant-probe excerpts, return-contract :10-31, merged-root-cause-analysis excerpts, adversarial-post-merge-validation :118-121, and synthesis-component-intake (grep).

**Clean-result justification and external-tool provenance:**
- Not a clean result: there are 7 issues.
- No web research was performed. Tavily and WebSearch were not needed or used, because every check was local-file-bound.
- Graph coverage was unavailable for package files, so all conclusions come from direct reads.

## Partition Limits and Evidence Uncertainty
- Partition 1 components (synth-01 to synth-03) were not reviewed, apart from the synth-02 Gap Analysis rows used for links. Cross-partition contradictions are left to the Step 5.23 merge.
- Historical JSONL records were not replayed. Record anchors were checked against the case reports only.
- `ADV/base-selection.md` was read only at :148-172. The variant originals were not reread, except variant-5's line count and hash.
- Issue 7's file identity is unverified: the content structure matches, but no historical hash was compared.
- The five cards were checked for coherence and preservation claims. Their full verbatim preservation against the variants was not recomputed, except card 5's counts.
- synth-06's QA inventory was spot-checked, not fully enumerated.

## Recommendations
- Consolidate Issues 1-7 into `qa/qa-consolidated-findings-phase5.md` (Step 5.23).
- Apply the fixes in the single serialized correction pass (Step 5.24).
- Fixes are confined to synth-04, synth-05 and synth-06. They need no card edits and no re-debate, because none of them changes a hypothesis identity, mechanism or rank position.
- Issue 3 changes only the wording of a justification. Issue 4 clarifies an owner without altering any card.

## QA Complete

| Status | Result |
|---|---|
| DONE | Reviewed partition 2 synthesis coherence against the actual debate artifacts, the evidence deck and the gaps. Verdict FAIL: 5 IMPORTANT and 2 MINOR issues, with no target edits. |
| NEXT | The parent persists this exact text at `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-synthesis-qualitative-report-2.md`, then consolidates it in Step 5.23. |