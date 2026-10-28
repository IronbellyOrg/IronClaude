# QA Report: Phase 5 Synthesis Corrections, Cycle 2

**Topic:** User-authorized second correction pass for the open synthesis findings after the cycle-1 halt
**Date:** 2026-10-24
**Status:** Complete as returned text. All patches are prepared and were validated in memory against the current files. None is applied. The parent must persist this log and apply the patches.
**Phase:** Phase 5 synthesis gate, cycle 2 of 2
**Authorization:** User message 2026-10-24T03:41Z: "I authorize the fixes but not the verifiers.. once fixes are in you are authorized to move on"
**Governing template:** Task Standard QA Report Output Format (`/config/.claude/skills/task/SKILL.md:466-506`) and Serialized Fix Protocol step 3 (`:359`). Report Structure and Content Rules: `/config/.claude/skills/tech-research/SKILL.md:1426-1487` and `:1579-1601`, including "Tables over prose whenever presenting multi-item data" at `:1598`.

**Delivery limitation:** My higher-priority instructions do not allow me to write report files. I edited no file, including this log, the synthesis files and the cards. The parent must:
1. Persist this text at `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/qa/qa-synthesis-fix-log-cycle2.md`, replacing the stub.
2. Apply the JSON array below in array order.

The only file I created was in my private directory `/tmp/ironclaude-fix2.*`, which held the validation script and patch JSON. That directory was removed (`CLEANUP_OK`).

All relative paths resolve under `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/`. `ADV/` means `reviews/adversarial/adversarial/`.

---

## Overall Verdict
**Application state: 19 literal patches PREPARED and validated in memory, not applied.** This log gives no gate verdict.

- **Scope:** exactly the open set in `phase-outputs/plans/synthesis-gate-decision.md:42-51`. That is nine finding groups across synth-01, synth-04, synth-05, synth-06 and the five cards' 10.5 areas.
- **Starting state:** the current SHA-256 of all 11 synthesis files equals the cycle-1 "After all patches" column (`qa/qa-synthesis-fix-log.md:112-122`). So the patches target the exact applied cycle-1 state.
- **Sequence check:** run in sequence, every needle matched exactly once (`ALL_NEEDLES_EXACT_ONCE 19`).
- **Nothing else changes:**
  - No rank, and not the displayed order V1 > V3 > V2 > V5 > V4.
  - No card's causal text and no historical classification.
  - No variant, debate artifact, research file, gap register, task file or other QA file.

## Items Reviewed
| # | Finding | Location (current file) | Result | What the patch does (source re-read this cycle) |
|---|---|---|---|---|
| 1 | R1 / S25-N2 (regression, content-2 row 10) | synth-04:309, §7.7 "Excluded with rationale" | Patched | Turns the six-control prose into a table with columns Screened control / Deck anchor / Placement / Reason or stated limit (one row per deck line `:650-655`, re-read). Keeps the opening sentences and the sentence "They do not change the ranking, and they are not presented as positions the debate advocates weighed." All six rows have 4 cells. |
| 2 | P5-18 remainder / U-1 | synth-04:83 (Option B Opposition), :161 (Option E Opposition), synth-05:87 | Patched | Options B and E now give the Session 10 Task 4 and Session 17 Task 8 limits, worded as in Option A (synth-04:56). synth-05:87 now gives all three limits from `research/evidence-deck.md:650-652` (re-read). The Sessions 13/14 limit was already present. No re-ranking. |
| 3 | N-1 / S25-N4 | synth-06:64 | Patched | The historical-snapshot sentence now says three rows were corrected in place at Task Step 5.24: the web-01 row moved from 10.2 to Web Research, and the 10.5 plan-review-evidence and merge-log rows were corrected. It points to the original wording in the cycle-1 fix log. I confirmed these are the only unmarked in-place changes inside 10.1-10.8 by parsing the cycle-1 synth-06 patches: patch 85 removes the row, patches 91 and 92 rewrite the rows, and every other one is an append marked Superseding. |
| 4 | N-2 / S25-N5 | synth-04:324 (§7.8) | Patched | Adds a dated row "Task Step 5.24 corrections (synthesis-gate fix cycle 1, 2026-10-24)". It records the fixer's full read of all six components (including synth-05), its reads of `ADV/variant-2-original.md` lines 10 and 37 and `ADV/debate-transcript.md:269,272`, and its re-read of deck `:650-655`. These match the cycle-1 log's Items Reviewed (P5-17, P5-18, P5-31) and Actions Taken (`qa/qa-synthesis-fix-log.md:87`). The producer's rows are unchanged. |
| 5 | N-3 / S25-N3 | synth-05:11, :25, :64, :66, :77, :120 | Patched | (a) :11 and :120 now distinguish the five original Phase 2 comparisons, the order-4 scope-decision row and the two Phase 3 separation checks. (b) :25 and :77 now disclose that the order-4 row cites the debate transcript, which is outside the input table. `ADV/debate-transcript.md:270` was re-read: it is the C-001 transition-label row. (c) Phase 2's Goal (:64) and Dependencies (:66) now state that the last row is the exception: it has no existing input, does not depend on Phase 1, needs a user scope decision and is outside the current scope. The row stays UNEXECUTED and unchanged. |
| 6 | S25-N1 | synth-01:74, credential row Evidence cell | Patched | Adds the absolute `research/evidence-deck.md:350` citation. That line was re-read: "1932 issues". |
| 7 | S25-N6 | synth-04:335 | Patched | Adds the same kind of parenthetical used at synth-05:140. The moved Status line's remaining sentence ("The ranking below inherits the adversarial return status `partial`, because the causal order is not a consensus.") stays in the header at :4. This was verified against cycle-1 patch 41's needle, which split the original Status line at "inherits". |
| 8 | S25-N7 | hypothesis-01..05, 10.5 area | Patched | Appends a dated amendment receipt after each card's original 10.5 record. No original card line is edited. Each receipt states the P5-28 insertion (439 bytes), the new pre-record body size and SHA-256, and the re-run exact-once result. Boundary convention: I reproduced each recorded pre-fix hash by reversing the cycle-1 card patch and taking every byte before the `### 10.5` heading except its two preceding newline characters. All five recorded hashes matched under that rule. |
| 9 | S25-N8 | `qa/qa-synthesis-fix-log.md:71` (process record) | Recorded here; file not edited | I parsed the cycle-1 JSON array: 102 patches, split synth-01 15, synth-02 21, synth-03 5, synth-04 31, synth-05 11, synth-06 14 and 1 each for hypothesis-01..05, total 102. The counts at :71 (15, 22, 5, 32, 13, 15, plus 5 cards) add up to 107 and are wrong. Per instruction, the cycle-1 log stays unchanged, and this record is the correction. |

## Summary
- Findings in scope: 9 groups (R1/S25-N2, P5-18/U-1, N-1/S25-N4, N-2/S25-N5, N-3/S25-N3, S25-N1, S25-N6, S25-N7, S25-N8).
- Patched by literal patch: 8 groups. Corrected by record in this log: 1 group (S25-N8). Not applied: 0.
- Patches: 19 literal patches, each `expected_count: 1`, validated in sequence.
- Patches per file:

| File | Patches |
|---|---|
| synth-01 | 1 |
| synth-04 | 5 |
| synth-05 | 7 |
| synth-06 | 1 |
| hypothesis-01..05 | 1 each |

- Files not touched: synth-02 and synth-03.
- Issues fixed in place: 0. The patches take effect only when the parent applies them.
- Re-debate required: none.

## Issues Found
| # | Severity | Location | Issue | Required action |
|---|---|---|---|---|
| 1 | MINOR (process) | 9 target files | The patches are not applied because this fixer cannot write. | The parent checks each "Current" SHA-256 below, applies the array in order, then checks each "Expected after" SHA-256. |
| 2 | Note (pre-existing, not introduced) | hypothesis-01..05 | The generic table separator line `\|---\|---\|---\|` appears once in each `variant-N-original.md` but twice in each card, both before and after Task Step 5.24. So the literal rule "each non-heading line exactly once" holds for every substantive line but not for this markdown separator. Each S25-N7 receipt discloses this. | None in this cycle. It is markdown syntax, and editing card table structure is out of scope. |

## Actions Taken
- **Instructions and formats read:** the gate decision (Issues Found list), both verification reports in full, the stub, the Serialized Fix Protocol and Standard QA format (`task/SKILL.md:349-506`), and the Report Structure and Content Rules (`tech-research/SKILL.md:1426-1601`).
- **Target files read:**
  - synth-04 and synth-05 in full.
  - synth-06 in full.
  - synth-01:60-91.
  - The cycle-1 fix log :1-125.
- **Sources re-read:**
  - `research/evidence-deck.md:340-354` and `:640-664`.
  - `ADV/debate-transcript.md:268-272`.
- **Cycle-1 patch array:** parsed for per-file counts (S25-N8), for the synth-06 in-place row changes (N-1) and for the synth-04 Status split (S25-N6).
- **Cards:** for each card, reversed the cycle-1 note patch and reproduced the recorded pre-fix body hash, which fixed the boundary rule. Then computed the current pre-record body hash and size, and the variant hash.
- **Validation:** built all 19 patches and applied them in memory in sequence. Recomputed the hashes and ran the preservation checks below.
- **Not done:** no file was edited. No agents, tests, Git, staging, archive, move, delete or publication.

## Exact Patches If Direct Writes Are Prohibited

**SHA-256 values.** The applier must match "Current" before applying and "Expected after" once all patches are applied.

| File | Current SHA-256 | Expected after SHA-256 | Bytes after |
|---|---|---|---|
| `synthesis/synth-01-problem-current-state.md` | `52118a082e4723c9864a6c08c4f91806033af7297fa88aa544a84fc6d634fef9` | `912c408e339475d29198094edcaae223b13f77ab5ed4ce38361019fef67f03e5` | 42,834 |
| `synthesis/synth-04-options-recommendation.md` | `f8f26e0737f0fe3c6f601bc9132405b59c2e00bc1df2b2a25adad55d6f23b85b` | `ca9ec77be6ba42297bd92d6a2df8f3f3e32c2aa01cce412d7704485c193bcbd7` | 61,108 |
| `synthesis/synth-05-implementation-plan.md` | `dfa8bfc4d39adbc4107e5e33fdbf6173d8d082186e39f95fabea69fef1620c52` | `0d02b9b816764e94375e26721b748925366cf9b32f234d6e0013162ef8c9080b` | 29,404 |
| `synthesis/synth-06-questions-evidence.md` | `3218ebba48317c3eec2191f13734bcdd85424c371a3b3b32e76c84d465cd8c82` | `bcffe37af678f598f3e7c4cea5b3982d26462184b6a9e0226505ab52270c626b` | 61,098 |
| `synthesis/hypothesis-01.md` | `a86f6332c71f241b08181411ff6f30c507ca66649f34f5071781e35cb1f7e287` | `cc9462cd978e983e4be75b8918822f1ed835e9d0bba1a342666fc815092c1049` | 25,300 |
| `synthesis/hypothesis-02.md` | `e4aa891370a0c3af8948ceb7128428333b8e3e7e060d781b4d2e6dd0351ef965` | `305dde4e42ab201c824132c9827fb29281f47537d099f698d0c2c39ed9a5aa87` | 27,581 |
| `synthesis/hypothesis-03.md` | `cab427db8fc2203e3fd84166847f0e427607dbf4b1eef70f3af4c83d76310db3` | `7c894b43b76309191c57f59ea6546f9e5373c2f40951de2b6c8fe8c7e00f6be7` | 28,930 |
| `synthesis/hypothesis-04.md` | `ff476cd30ae05cb753ea77e69382fab06eaa44f0e16687406367e1676f4fc19b` | `4458ef26941f2816a57bd62a6d9692e02a964dac9c30327d18527dd050c21eba` | 26,051 |
| `synthesis/hypothesis-05.md` | `cc462e2b80207e9ad2f36233814d8e2475f462520fc7a777d58458d7ded26dac` | `8cef74221fa38325af873e2bdfef3d86aad9d361a4eca112479ddc0df3ebae6c` | 28,245 |

**How to apply:**
1. Take each object in array order.
2. Confirm its `needle` occurs exactly once in the current state of its file.
3. Replace it with `repl`.

The files are UTF-8. The card receipts contain a Unicode ellipsis (…) after each 8-character hash prefix.

```json
[
 {
  "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/synthesis/synth-01-problem-current-state.md",
  "mode": "literal",
  "needle": "research/06-session-0690ee9f.md:11-32,64-129,131-266,268-319,336-387`. Primary transitions:",
  "repl": "research/06-session-0690ee9f.md:11-32,64-129,131-266,268-319,336-387`; `/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/research/evidence-deck.md:350`. Primary transitions:",
  "expected_count": 1,
  "finding_ids": [
   "S25-N1"
  ]
 },
 {
  "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/synthesis/synth-04-options-recommendation.md",
  "mode": "literal",
  "needle": "Screened controls Session 10 Task 4 and Session 17 Task 8 converged after one repair (missing comment; real deviation), and Sessions 13/14 made",
  "repl": "Screened controls Session 10 Task 4 and Session 17 Task 8 converged after one repair (missing comment; real deviation); limits: Session 10's original implementation package was absent from searched locations, and Session 17's later PR reviews are separate work. Sessions 13/14 made",
  "expected_count": 1,
  "finding_ids": [
   "P5-18",
   "U-1"
  ]
 },
 {
  "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/synthesis/synth-04-options-recommendation.md",
  "mode": "literal",
  "needle": "which cautions against treating any failed review as predicting a repeat (`research/evidence-deck.md:650-651`).",
  "repl": "which cautions against treating any failed review as predicting a repeat; limits: Session 10's original implementation package was absent from searched locations, and Session 17's later PR reviews are separate work (`research/evidence-deck.md:650-651`).",
  "expected_count": 1,
  "finding_ids": [
   "P5-18",
   "U-1"
  ]
 },
 {
  "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/synthesis/synth-04-options-recommendation.md",
  "mode": "literal",
  "needle": "Excluded with rationale: screening slices `scope-01.md` through `scope-05.md` were not reread for this component. Their control dispositions are taken from the evidence deck's counterexample table (`research/evidence-deck.md:643-662`) and placed per control: Session 10 Task 4 and Session 17 Task 8 (one-repair convergence, `:650-651`) in the Opposition rows of Options A, B and E; Session 17 FINAL (a real delivery bug found by FINAL, `:652`) in Option D; Sessions 13/14 (authorized plan corrections without semantic re-review, `:655`) in Option B. Session 09 (seven compliant tasks, FINAL never ran, `:653`) and Session 19 (nine compliant task reviews, `:654`) are not placed in an Opposition row, because they bound what counts as an observed failure or a shared-ledger block rather than any single candidate's mechanism. These placements were added at Task Step 5.24 as synthesis-fidelity corrections. They do not change the ranking, and they are not presented as positions the debate advocates weighed.",
  "repl": "Excluded with rationale: screening slices `scope-01.md` through `scope-05.md` were not reread for this component. Their control dispositions are taken from the evidence deck's counterexample table (`research/evidence-deck.md:643-662`) and placed per control as shown below. These placements were added at Task Step 5.24 as synthesis-fidelity corrections. They do not change the ranking, and they are not presented as positions the debate advocates weighed.\n\n| Screened control | Deck anchor | Placement | Reason or stated limit |\n|---|---|---|---|\n| Session 10 Task 4: missing comment corrected, compliant re-review | `research/evidence-deck.md:650` | Opposition rows of Options A, B and E | One-repair convergence. Limit: original implementation package absent from searched locations; logs and Edit survive |\n| Session 17 Task 8: real deviation corrected, passing re-review | `research/evidence-deck.md:651` | Opposition rows of Options A, B and E | One-repair convergence. Limit: later PR reviews are separate development work |\n| Session 17 FINAL: real restore-basename bug plus evidence defects corrected, then pass | `research/evidence-deck.md:652` | Option D Opposition | A real delivery bug found by FINAL. Limit: not strict fail-fix-fail |\n| Sessions 13/14: authorized plan corrections without semantic re-review | `research/evidence-deck.md:655` | Option B Opposition | Not every corrected plan has a second failed review. Limit: an unreviewed correction is not clean approval either |\n| Session 09: seven compliant tasks; FINAL never ran | `research/evidence-deck.md:653` | Not placed in an Opposition row | Bounds what counts as an observed failure, not any single candidate's mechanism. Deck limit: overlapping writers are a real operational blocker |\n| Session 19: nine compliant task reviews | `research/evidence-deck.md:654` | Not placed in an Opposition row | Bounds a shared-ledger block, not any single candidate's mechanism. Deck limit: later Task 12 belongs to another session |",
  "expected_count": 1,
  "finding_ids": [
   "R1",
   "S25-N2"
  ]
 },
 {
  "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/synthesis/synth-04-options-recommendation.md",
  "mode": "literal",
  "needle": "| `synthesis/synth-05-implementation-plan.md` | Lines 1-40 only; referenced by path, not by step identifiers |",
  "repl": "| `synthesis/synth-05-implementation-plan.md` | Lines 1-40 only; referenced by path, not by step identifiers |\n| Task Step 5.24 corrections (synthesis-gate fix cycle 1, 2026-10-24) | The rows above record the producer's Step 5.12 reads and are unchanged. The fixer read all six components in full, including `synthesis/synth-05-implementation-plan.md` (basis for the 7.6 grouping and order-4 note); read `ADV/variant-2-original.md` lines 10 and 37 and `ADV/debate-transcript.md:269,272` (basis for Option B's two outcomes); and re-read every other source range its corrections cite, including `research/evidence-deck.md:650-655` for the 7.7 control placements (`qa/qa-synthesis-fix-log.md`, Items Reviewed and Actions Taken) |",
  "expected_count": 1,
  "finding_ids": [
   "N-2",
   "S25-N5"
  ]
 },
 {
  "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/synthesis/synth-04-options-recommendation.md",
  "mode": "literal",
  "needle": "The producer's original header lines, moved here unchanged at Task Step 5.24:",
  "repl": "The producer's original header lines, moved here unchanged at Task Step 5.24 (the Status line's remaining sentence, \"The ranking below inherits the adversarial return status `partial`, because the causal order is not a consensus.\", stays in the header):",
  "expected_count": 1,
  "finding_ids": [
   "S25-N6"
  ]
 },
 {
  "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/synthesis/synth-05-implementation-plan.md",
  "mode": "literal",
  "needle": "This section retains and sharpens the existing five discriminating checks.",
  "repl": "This section retains and sharpens the existing five discriminating comparisons in Phase 2. Phase 2 also lists one comparison that needs a user scope decision (Section 7.6 order 4), and Phase 3 adds two separation checks (consent, scope and ruling records; checkpoint guard versus repository movement).",
  "expected_count": 1,
  "finding_ids": [
   "N-3",
   "S25-N3"
  ]
 },
 {
  "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/synthesis/synth-05-implementation-plan.md",
  "mode": "literal",
  "needle": "Every file below was directly read for this component. Names in the comparison tables resolve to these exact absolute paths.",
  "repl": "Every file below was directly read for this component. Names in the comparison tables resolve to these exact absolute paths. One later row cites a file outside this table: the Phase 2 order-4 row names the debate transcript by its own absolute path, because that row has no existing research input (added at Task Step 5.24).",
  "expected_count": 1,
  "finding_ids": [
   "N-3",
   "S25-N3"
  ]
 },
 {
  "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/synthesis/synth-05-implementation-plan.md",
  "mode": "literal",
  "needle": "**Goal:** Test the competing explanations using existing counterexamples and retained history.",
  "repl": "**Goal:** Test the competing explanations using existing counterexamples and retained history. The last row is the one exception: it would need newly selected sessions.",
  "expected_count": 1,
  "finding_ids": [
   "N-3"
  ]
 },
 {
  "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/synthesis/synth-05-implementation-plan.md",
  "mode": "literal",
  "needle": "These rows are possible research comparisons, not an execution sequence or permission to perform experiments.",
  "repl": "These rows are possible research comparisons, not an execution sequence or permission to perform experiments. The last row (Section 7.6 order 4) does not depend on Phase 1, because it has no existing input; it needs a user scope decision and lies outside the current research scope.",
  "expected_count": 1,
  "finding_ids": [
   "N-3"
  ]
 },
 {
  "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/synthesis/synth-05-implementation-plan.md",
  "mode": "literal",
  "needle": "These are the exact existing inputs listed above.",
  "repl": "These are the exact existing inputs listed above. The order-4 row's reference to the C-001 labels in the debate transcript is outside this input table and is not an evidence binding for a comparison.",
  "expected_count": 1,
  "finding_ids": [
   "N-3",
   "S25-N3"
  ]
 },
 {
  "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/synthesis/synth-05-implementation-plan.md",
  "mode": "literal",
  "needle": "| Evidence deck | All five comparisons use its six causal classes, corrected transitions, successful controls, accepted gaps and unit distinctions.",
  "repl": "| Evidence deck | The five original Phase 2 comparisons use its six causal classes, corrected transitions, successful controls, accepted gaps and unit distinctions. The order-4 row has no evidence-deck input, and the two Phase 3 separation checks bind the deck rows cited in them.",
  "expected_count": 1,
  "finding_ids": [
   "N-3",
   "S25-N3"
  ]
 },
 {
  "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/synthesis/synth-05-implementation-plan.md",
  "mode": "literal",
  "needle": "Session 10 Task 4 (missing comment corrected, compliant re-review), Session 17 Task 8 (real deviation corrected, passing re-review), Session 17 FINAL (real restore-basename bug and evidence defects corrected, then pass)",
  "repl": "Session 10 Task 4 (missing comment corrected, compliant re-review; limit: original implementation package absent from searched locations, logs and Edit survive), Session 17 Task 8 (real deviation corrected, passing re-review; limit: later PR reviews are separate development work), Session 17 FINAL (real restore-basename bug and evidence defects corrected, then pass; limit: not strict fail-fix-fail)",
  "expected_count": 1,
  "finding_ids": [
   "P5-18",
   "U-1"
  ]
 },
 {
  "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/synthesis/synth-06-questions-evidence.md",
  "mode": "literal",
  "needle": "records the 22:14:30Z observation above and is kept unchanged as historical.",
  "repl": "records the 22:14:30Z observation above and is kept as historical, except for three rows corrected in place at Task Step 5.24: the `research/web-01-gap-applicability.md` row moved from 10.2 to the Web Research table above, and the 10.5 `plan-review-evidence.md` and `merge-log.md` rows were corrected so that the canonical-review FAIL and the targeted re-review PASS sit in the merge-log row. Their original wording is preserved in `qa/qa-synthesis-fix-log.md` (P5-26 and P5-27 patches).",
  "expected_count": 1,
  "finding_ids": [
   "N-1",
   "S25-N4"
  ]
 },
 {
  "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/synthesis/hypothesis-01.md",
  "mode": "literal",
  "needle": "Added text is presentation, N/A rationale and provenance only; this record is not an independent synthesis-gate verdict.\n",
  "repl": "Added text is presentation, N/A rationale and provenance only; this record is not an independent synthesis-gate verdict.\n\n**Amendment receipt (2026-10-24, synthesis-gate fix cycle 2):** This receipt is appended below the original record above, which is not edited. At Task Step 5.24 (synthesis-gate fix cycle 1, finding P5-28) one presentation note, marked as added after the debate and not part of the debated text, was inserted in chapter 1 between `## 1. Problem Statement` and `### Original Hypothesis` (`qa/qa-synthesis-fix-log.md`, P5-28). That insertion added 439 UTF-8 bytes, so the saved-body figures in the record above (22,587 bytes, SHA-256 `cd72eab0…`) describe the body before Task Step 5.24. Measured the same way (every byte before the `### 10.5` heading except the two newline characters that precede it), the body now measures 23,026 UTF-8 bytes, SHA-256 `0e24ce0e180c888f16a3b55c3d240936f755c871ca8dcecb072dc66906e2f340`. A re-run exact-once check against the immutable `reviews/adversarial/adversarial/variant-1-original.md` (SHA-256 `3f39f065ffb13efad680694e9e699fb04456a03a93cabab75be90bee3d2dbac9`, unchanged) found each of its 34 distinct non-blank, non-heading lines other than the table separator exactly once in this card. The generic table separator line appears 1 time in the variant and 2 times in this card, both before and after Task Step 5.24; it is markdown syntax, not identity text. This receipt states or implies no synthesis-gate verdict.\n",
  "expected_count": 1,
  "finding_ids": [
   "S25-N7"
  ]
 },
 {
  "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/synthesis/hypothesis-02.md",
  "mode": "literal",
  "needle": "This record is not an independent synthesis-gate verdict.\n",
  "repl": "This record is not an independent synthesis-gate verdict.\n\n**Amendment receipt (2026-10-24, synthesis-gate fix cycle 2):** This receipt is appended below the original record above, which is not edited. At Task Step 5.24 (synthesis-gate fix cycle 1, finding P5-28) one presentation note, marked as added after the debate and not part of the debated text, was inserted in chapter 1 between `## 1. Problem Statement` and `### Original Hypothesis` (`qa/qa-synthesis-fix-log.md`, P5-28). That insertion added 439 UTF-8 bytes, so the saved-body figures in the record above (24,904 bytes, SHA-256 `4bd72796…`) describe the body before Task Step 5.24. Measured the same way (every byte before the `### 10.5` heading except the two newline characters that precede it), the body now measures 25,343 UTF-8 bytes, SHA-256 `523d02eae82e71c35924ca50ed9cdeb23588f5a141793b1102af5cd6dfb875d2`. A re-run exact-once check against the immutable `reviews/adversarial/adversarial/variant-2-original.md` (SHA-256 `e62a753c7b5c9df11d0a57469de1717e115f3166e2596342adf26ad3fa882ebc`, unchanged) found each of its 36 distinct non-blank, non-heading lines other than the table separator exactly once in this card. The generic table separator line appears 1 time in the variant and 2 times in this card, both before and after Task Step 5.24; it is markdown syntax, not identity text. This receipt states or implies no synthesis-gate verdict.\n",
  "expected_count": 1,
  "finding_ids": [
   "S25-N7"
  ]
 },
 {
  "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/synthesis/hypothesis-03.md",
  "mode": "literal",
  "needle": "This record is not an independent synthesis-gate verdict.\n",
  "repl": "This record is not an independent synthesis-gate verdict.\n\n**Amendment receipt (2026-10-24, synthesis-gate fix cycle 2):** This receipt is appended below the original record above, which is not edited. At Task Step 5.24 (synthesis-gate fix cycle 1, finding P5-28) one presentation note, marked as added after the debate and not part of the debated text, was inserted in chapter 1 between `## 1. Problem Statement` and `### Original Hypothesis` (`qa/qa-synthesis-fix-log.md`, P5-28). That insertion added 439 UTF-8 bytes, so the saved-body figures in the record above (26,363 bytes, SHA-256 `db587957…`) describe the body before Task Step 5.24. Measured the same way (every byte before the `### 10.5` heading except the two newline characters that precede it), the body now measures 26,802 UTF-8 bytes, SHA-256 `01026f904e52622266e870b23e126128799b0f9168179f2e0fc19abd801155c7`. A re-run exact-once check against the immutable `reviews/adversarial/adversarial/variant-3-original.md` (SHA-256 `f20f7fd37114f1c3d529bd7eca97b2af748fe9c5b3c73559b78837a7dfb5a8e3`, unchanged) found each of its 35 distinct non-blank, non-heading lines other than the table separator exactly once in this card. The generic table separator line appears 1 time in the variant and 2 times in this card, both before and after Task Step 5.24; it is markdown syntax, not identity text. This receipt states or implies no synthesis-gate verdict.\n",
  "expected_count": 1,
  "finding_ids": [
   "S25-N7"
  ]
 },
 {
  "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/synthesis/hypothesis-04.md",
  "mode": "literal",
  "needle": "This record is not an independent synthesis-gate verdict.\n",
  "repl": "This record is not an independent synthesis-gate verdict.\n\n**Amendment receipt (2026-10-24, synthesis-gate fix cycle 2):** This receipt is appended below the original record above, which is not edited. At Task Step 5.24 (synthesis-gate fix cycle 1, finding P5-28) one presentation note, marked as added after the debate and not part of the debated text, was inserted in chapter 1 between `## 1. Problem Statement` and `### Original Hypothesis` (`qa/qa-synthesis-fix-log.md`, P5-28). That insertion added 439 UTF-8 bytes, so the saved-body figures in the record above (23,307 bytes, SHA-256 `3069f94f…`) describe the body before Task Step 5.24. Measured the same way (every byte before the `### 10.5` heading except the two newline characters that precede it), the body now measures 23,746 UTF-8 bytes, SHA-256 `39509e9b38f8bc42935509b7aac8fc5bff4cdbfe200cfe86f742b8dc29f3c179`. A re-run exact-once check against the immutable `reviews/adversarial/adversarial/variant-4-original.md` (SHA-256 `fe15dc657c4e6ee11e9d60ce655d2b61d364e5c6055e090abd58e87395f36117`, unchanged) found each of its 35 distinct non-blank, non-heading lines other than the table separator exactly once in this card. The generic table separator line appears 1 time in the variant and 2 times in this card, both before and after Task Step 5.24; it is markdown syntax, not identity text. This receipt states or implies no synthesis-gate verdict.\n",
  "expected_count": 1,
  "finding_ids": [
   "S25-N7"
  ]
 },
 {
  "file_path": "/config/workspace/IronClaude/.dev/tasks/to-do/TASK-RESEARCH-review-loops-20261023-032537/synthesis/hypothesis-05.md",
  "mode": "literal",
  "needle": "This record is not an independent synthesis-gate verdict.\n",
  "repl": "This record is not an independent synthesis-gate verdict.\n\n**Amendment receipt (2026-10-24, synthesis-gate fix cycle 2):** This receipt is appended below the original record above, which is not edited. At Task Step 5.24 (synthesis-gate fix cycle 1, finding P5-28) one presentation note, marked as added after the debate and not part of the debated text, was inserted in chapter 1 between `## 1. Problem Statement` and `### Original Hypothesis` (`qa/qa-synthesis-fix-log.md`, P5-28). That insertion added 439 UTF-8 bytes, so the saved-body figures in the record above (25,171 bytes, SHA-256 `43d9fbed…`) describe the body before Task Step 5.24. Measured the same way (every byte before the `### 10.5` heading except the two newline characters that precede it), the body now measures 25,610 UTF-8 bytes, SHA-256 `29a4863a69fd14c5ad37df42fa2fad14c4728ce4caa8e08a81d6f03fbd63ccc9`. A re-run exact-once check against the immutable `reviews/adversarial/adversarial/variant-5-original.md` (SHA-256 `1cf685b5356db01e1409ffb335dd25543622c3701dcf8072264ef1a9467941ac`, unchanged) found each of its 33 distinct non-blank, non-heading lines other than the table separator exactly once in this card. The generic table separator line appears 1 time in the variant and 2 times in this card, both before and after Task Step 5.24; it is markdown syntax, not identity text. This receipt states or implies no synthesis-gate verdict.\n",
  "expected_count": 1,
  "finding_ids": [
   "S25-N7"
  ]
 }
]
```

## Preservation Checks
All checks below were run on the in-memory post-patch state.

| Check | Result |
|---|---|
| Ranks and displayed order | `V1 > V3 > V2 > V5 > V4` occurs 3 times in synth-04, the same as before. No patch touches 7.1, 7.2, the comparison table or any rank cell. |
| No probability | synth-04 contains 0 `%`. No replacement text adds a percentage, probability or likelihood. |
| Debate-weighting sentence kept | "they are not presented as positions the debate advocates weighed" occurs exactly once in synth-04, directly above the new §7.7 table. |
| §7.7 table shape | All 6 rows have 4 cells, matching the 4-column header. |
| Section 8 rows UNEXECUTED | synth-05 `UNEXECUTED` count is 6 before and 6 after. No row status changes. The order-4 row's text is unchanged; only Phase 2's Goal, its Dependencies and the counts and disclosures around the row change. |
| Card identity | For each card, every distinct non-blank, non-heading line of `variant-N-original.md` appears exactly once after the patches (34/36/35/35/33 lines). The only exception is the separator `\|---\|---\|---\|` (variant 1, card 2), which is pre-existing and unchanged. The receipts add no variant line. |
| Card pre-record body | The receipts are appended after each 10.5 record, so each body hash before the record is unchanged by this cycle (checked for all five). |
| Card causal text | Only the 10.5 area changes: one appended paragraph per card. No original card line is edited. |
| Historical classifications | None changes. The patches add limits, disclosures, reading records and a table layout only. |
| Off-limits files | No patch targets `reviews/adversarial/**`, `research/**`, `gaps-and-questions.md`, the task file, `qa/qa-synthesis-fix-log.md` or any other QA file. |

## QA Complete
- **Confidence:** Verified 9/9 findings | Unverifiable 0 | Unchecked 0 | Confidence 100.0%. Limit: these are prepared patches, validated in memory. Their effect on disk depends on the parent applying them byte-exactly.
- **Tool engagement:** Read 9 | Grep 0 (greps ran inside Bash) | Glob 0 | Bash 7 (hashes, patch-array parsing, card boundary reconstruction, one private-directory validation script with cleanup). No web research: tavily_search 0 | tavily_extract 0 | web_search_fallback 0 | web_fetch_fallback 0.
- **Self-Audit:** each correction was written from source lines re-read this session: deck `:350` and `:650-655`, transcript `:270`, the cycle-1 patch needles for the synth-04 Status split and the synth-06 rows, and the reversed card patches that reproduce all five recorded body hashes. One residual is disclosed rather than hidden: the separator duplication (Issues Found #2).

| Status | Result |
|---|---|
| DONE | Prepared 19 hash-guarded literal patches covering all 9 open findings. Every needle matched exactly once in sequence, and the expected-after SHA-256 values are computed. |
| DONE | Recorded the corrected cycle-1 per-file patch counts (15/21/5/31/11/14 plus 1 per card = 102) without editing the cycle-1 log. |
| NEXT | Parent persists this log at `qa/qa-synthesis-fix-log-cycle2.md`, then applies the JSON array in order. Check the 9 "Current" hashes first and the 9 "Expected after" hashes once all patches are applied. |

## Parent Application Record (2026-10-24)

The parent persisted this exact fixer return (subagents/agent-asg-fixer-2-*.jsonl; 335 lines, 36,072 bytes before this record) and applied the 19 literal patches with one all-or-nothing script: all 9 starting SHA-256 values matched the "Current" column, every needle matched once in sequence, and all 9 results equalled the "Expected after" column before writing and after re-reading. Every non-heading line of each `reviews/adversarial/adversarial/variant-N-original.md` still appears exactly once in its card. The parent read the new synth-04 section 7.7 control table (six rows, four cells each, deck anchors 650-655) and confirmed the sentence that the debate advocates did not weigh these controls remains. Per the user's authorization, no cycle-2 verifiers were run; this record establishes application identity only, not finding resolution.
