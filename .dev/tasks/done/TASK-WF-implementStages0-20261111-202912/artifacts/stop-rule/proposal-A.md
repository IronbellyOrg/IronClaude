# Stop-rule review, reviewer A

Scope: only the section "Stop rule" of `pilot-design.md` (lines 178-189). Citations: `pd:<line>` = `.dev/tasks/to-do/TASK-WF-implementStages0-20261111-202912/artifacts/pilot-design.md`; `src:<line>` = `.dev/brainstorms/20261111T182026-reflect-tier2-panel-replacement/merged-requirements.md`; `cost-profile.yaml` and `SKILL.md` are under `src/superclaude/skills/sc-reflect-protocol/` (`refs/` for the profile). Arm letters follow the source and the pilot design (A = T1 only, B = legacy T2, C = panel-parity T2, D = panel-lite; `src:532`, `pd:46-51`), not the letters in the review brief, which swapped them.

Verdict on the section as written: FAIL (three blocking defects below).

## Improvements (3)

**I-1. Fix the run order so that any stop leaves usable, paired data and a measured d0.**
The pilot's only outputs are d_BC, d_AB and d0 (`pd:71`, `src:538`), and d is defined per defect, paired across two arms run on the same plans (`pd:75`, `src:536`). The confirmatory request must state all three (`pd:197`). Rule 2 stops "before any run" (`pd:188`), and nothing fixes the order of runs, so a spend stop can land between arm B and arm C of one plan (that plan's defects then have no pair) or before the 6 arm-B repeats (then d0, T-6 and the confirmatory request are all missing). Proposal: run in plan blocks (all arms of one plan, in random arm order, before the next plan), schedule the 6 repeats one per block in the first 6 blocks, and let the spend check act only between blocks. A stop then always leaves complete pairs and, after block 6, a d0 estimate. No new number: block size and repeat count come from `pd:28`, `pd:68-69`.

**I-2. State that the pilot harness enforces the per-run hard kill, and how a killed run is scored.**
The profile says callers MUST abort a run above 1.25 x the midpoint estimate (`cost-profile.yaml:68-70`; `SKILL.md:1717` "Targets, not caps. Hard kill at 1.25x estimate") and that reflect itself never reads the profile at run time (`cost-profile.yaml:4-5`). So the only per-run brake against runaway cost is the caller, here the pilot harness, and the stop rule does not mention it. The kill value for T2 is 52 x 1.25 = 65k (`cost-profile.yaml:55,70`, `src:479`), the same number as T-4 (`pd:20`). If kills are enforced but a killed run is recorded at its token count, no arm-C run can ever exceed 65k and T-4 (p95 at most 65k) passes by construction; the source rates a pre T2 run exceeding the 65k kill as Medium probability at the legacy high end (`src:518`), so this is not hypothetical. Proposal: the harness kills at the profile value; a killed run is not a stop condition and is not rerun; for H-C it counts as above T-4 (censored, own note); for recall its partial output is scored, and a run with no report scores its seeded defects as not found (own note). Per-run kill for T1 is 6 x 1.25 = 7.5k (`cost-profile.yaml:43,70`, own arithmetic).

**I-3. Make "no early stop" symmetric and give T-6 a stated place.**
Rule 3 forbids an early stop for success only (`pd:189`). It is silent on an early stop because arm C looks worse, or because H-A looks lost, although the same reason applies: at 60 defects power is about 79% at d = 0.10 and 54% at d = 0.20 (`src:536`), and 69% and 45% with the clustering factor (`pd:99`, row A-12), so an interim look on fewer plans decides even less. The section also lists T-6 under "what the source does fix" (`pd:183`) and then never says what T-6 does, which invites reading it as a stop trigger. T-6 needs d0 from the 6 repeats and d from all plans (`src:538`), so it can only be applied once, at the end. Proposal: no interim recall or precision is computed (grading runs after the last block, which also protects grader blinding, `src:532`, `src:534`); T-6 is applied once at the end and reported in the confirmatory request (`pd:197`), not used to stop runs. (own note) For H-B, d_BC close to d0 is what parity predicts, so T-6 holding between B and C is not a futility signal for H-B.

## Defects (3)

**D-1 (blocking). Rule 1 halts on legacy baseline behaviour and assumes every safety event is visible at run time.**
Rule 1 stops "at the first safety event (T-5)" in any arm (`pd:187`). The safety list includes "a MALFORMED contract" (`pd:37`, `src:530`), and the legacy engine already produces those: Stage 0a found 4 recorded T2 runs with an illegal `merge_method` value (`pd:173`), and the skill defines any such value as MALFORMED (`SKILL.md:837`). The source also states that today a 2-of-3 run is called MALFORMED interactively (`src:519`, risk 11, probability High). Arm B (legacy T2) runs 12 + 6 = 18 times (`pd:49`). Illustration only (own arithmetic, assuming the recorded rate of 4 in 34 recorded merged verdicts, `pd:170`, `pd:173`, applies to the pilot): the chance of at least one MALFORMED in 18 arm-B runs is 1 - (30/34)^18 = 1 - 0.105, about 89%. The likely outcome of rule 1 as written is therefore a pilot halted by the control arm, with no estimate of d and no information about the panel. The source's safety criterion is a criterion on the panel ("fails regardless of savings", `src:529-530`, H-C context; Stage 3 entry, `src:411`), not on legacy. Separately, event 3, "an unsupported citation certified", can only be seen when the blinded grader checks citations (`src:534`), which happens after runs, so "stop at the first event" cannot apply to it and the rule does not say what happens when it is found after the last run.

**D-2 (blocking). Rule 2's ceiling has no value, no approval step, no meter and no forecast.**
(a) It cites "the approved pilot ceiling" (`pd:188`), but the only approval in the document and the source is for the confirmatory spend (`pd:197`, `src:538`); no step approves the pilot's. (b) Its value depends on the unresolved reading of the arm-B repeats (SD-3, `pd:134`, `pd:207`): C-5's upper bound is 2,616k for 6 repeats in total (`pd:131`), but 1,776k + 420k + 5,040k = 7,236k for 6 per plan (own arithmetic from `pd:128-129`, `pd:134`), 2.8 times more; the rule picks neither. (c) "Stop before any run that would take cumulative spend above" (`pd:188`) needs a forecast of the next run's cost, which the rule does not give, and the measured spend is not tied to a meter, although the source keeps three cost bases apart and the pilot uses the profile unit (`src:477`, `pd:123`). (d) Retrieval tokens are listed as a separate cost (`pd:136-144`) but the rule caps only claude tokens, so auggie spend has no ceiling at all, and no whole-pilot retrieval row exists to set one from.

**D-3 (blocking). Rule 3 has no handling for runs that end without a result, so it allows unbounded reruns or silent gaps.**
Rule 3 says all planned runs complete unless rule 1 or 2 fires (`pd:189`). A run can also end without a usable result and without a safety event: killed at the profile's hard-kill line (`cost-profile.yaml:68-70`), crashed, timed out, or ended with no contract at all. The rule does not say whether such a run is rerun, how many times, whether reruns count toward the ceiling, or how its defects are scored. If "complete" means rerun until a result exists, a run that is killed every time (a plan near the 65k line, `src:518`) loops until rule 2 fires, which is the runaway spend the stop rule exists to prevent. If failed runs are silently dropped, their plan's defects lose their pair (`pd:75`) and the arm with more failures looks no worse in recall, which biases H-B toward the panel when arm C fails more often. The same gap leaves open whether a run with no contract is a "MALFORMED contract" (a safety event under rule 1) or an ordinary failure.

## Proposed replacement text

Replaces `pd:178-189` in full.

```markdown
## Stop rule

The source requires "a stop rule" as pilot hygiene but does not state one (`src:538`). What the source and the profile do fix:

- any safety event (T-5) fails the measurement regardless of savings (`src:530`); Stage 3 entry needs safety passed (`src:411`);
- when d0 reaches T-6, the arms are indistinguishable from noise (`src:538`);
- a caller must abort a run that exceeds 1.25 x the profile midpoint (`cost-profile.yaml:68-70`, `SKILL.md:1717`), and reflect itself does not read the profile at run time (`cost-profile.yaml:4-5`), so the pilot harness, as the caller, enforces the kill: 65k claude tokens for a T2 run (the T-4 value, `src:479`) and 6 x 1.25 = 7.5k for a T1 run (own arithmetic, `cost-profile.yaml:43,70`).

**PROPOSED stop rule (own note, not in the source; the owner confirms or replaces it before the pilot runs).** S-1 takes precedence over S-2, and S-2 over S-3. S-4 lists what never stops the pilot.

**S-0. Run order.** (own note) The pilot runs in plan blocks: one plan with arms A, B and C (and D, if the plan is one of the 6 arm-D plans, chosen at random before the first block) run back to back in a random arm order. The 6 arm-B repeats run one per block in blocks 1-6 (the "6 in total" reading of SD-3; under the other reading every block carries 6 repeats). A block starts only after the previous block has finished, so any stop leaves only complete blocks: every defect keeps its pair, and from block 6 on d0 can be estimated.

**S-1. Safety (T-5).**

1. After every run the harness checks events 1, 2, 4 and 5 of the safety list (dispatch manifest, contract status, the snapshot's `git status`, and whether a T1 or `--depth quick` run called the panel). Event 3 (an unsupported citation certified) is checked by the blinded grader after the last block (`src:534`).
2. Halt, no further runs, and report to the owner: any event in arm C or D; event 5 in any arm; event 4 in any arm (a reviewer write changes the repository that later runs read, so later results are invalid).
3. Record and continue: events 1, 2 and 3 in arm A or B. These are legacy code paths the panel does not change; their counts are reported per arm beside arm C's as the baseline (own note; the source does not say whether its safety list covers the legacy arms).
4. Event 3 found in arm C or D at grading fails the measurement under T-5 the same way; no runs remain to stop.
5. A halted pilot does not restart by itself; the owner decides.

**S-2. Spend.**

1. Before the first block the owner approves two pilot ceilings, one per unit, and the reading of SD-3 (`src:477`: the bases are never summed):
   - claude tokens: the upper bound of row C-5 for the confirmed reading (2,616k for 6 repeats in total; 7,236k for 6 per plan, see the note under C-5), or of row C-2 (1,776k) if arm D and the repeats are dropped;
   - retrieval tokens: the upper bound of row R-6 for the same reading (960k or 2,610k), or of row R-2 (660k) if arm D and the repeats are dropped.
   Dropping the repeats removes d0, so T-6 cannot be applied and the confirmatory request cannot state d0.
2. Spend is the measured per-run token count in each unit, the same claude-token figure used for H-C (T-3, T-4); reruns under S-3 count.
3. Before each block: if spend so far plus the block's runs at the profile's band tops (claude: 8k per arm-A run, 70k per arm-B, C or D run; retrieval: 5k and 25k; `src:479`) would exceed either ceiling, the block does not start; report to the owner with the blocks completed. (Band tops are above the kill values, so the forecast is conservative.)

**S-3. Runs that end without a usable result (not a safety event).**

1. Killed at the kill value: not rerun. For H-C it counts as above T-4 (its true cost is unknown but at least the kill value). For recall and precision its partial output is scored; if it wrote no report, its seeded defects are scored as not found in that arm (own note).
2. Crashed, timed out or ended with no contract at all (treated as a failed run, not as a MALFORMED contract; own note, owner confirms): one rerun (own note: the smallest allowance that tolerates a transient fault, not derived from the source). If the rerun also fails, the run is recorded as failed and scored as in S-3.1; the block is kept.
3. The report lists killed and failed runs per arm.

**S-4. Never a stop.**

- Any apparent result for H-A, H-B or H-C before the last block, in either direction: interim recall and precision are not computed, grading runs after the last block (which keeps graders blind to arm, `src:532`), and the pilot cannot decide H-B in any case (`src:536`).
- T-6: applied once after the last block, from the 6 repeats and the full set of plans, and reported in the confirmatory request (see "Owner approval").
- A shortfall against T-7: the report states that it measured sparse-labelled plans only (`src:540`).
- Events recorded under S-1.3, and runs handled under S-3.

On any stop the report gives the blocks completed, spend in each unit, the safety events by arm, and which of d_BC, d_AB and d0 the completed blocks can estimate.
```

## Consistency edits needed

| Where | Change | Why |
|---|---|---|
| `pd:53` (own note on the repeats) | Add: "They run one per block in blocks 1-6 (Stop rule S-0)." | S-0 fixes where the repeats run. |
| `pd:134` (note under the cost table) | Add the whole-pilot total for the per-plan reading: "C-5 then becomes 876k + 210k + 2,520k = 3,606k to 1,776k + 420k + 5,040k = 7,236k (own arithmetic)." | S-2.1 cites this upper bound; today only C-4's per-plan value is stated. |
| `pd:144` (retrieval table) | Add row R-6: "whole pilot (R-2 + R-3 + R-4), 6 repeats in total: 264k + 60k + 60k = 384k to 660k + 150k + 150k = 960k; 6 per plan (R-4 = 72 x 10k-25k = 720k-1,800k): 1,044k to 2,610k" (own arithmetic). | S-2.1 needs a retrieval ceiling; no whole-pilot retrieval row exists (D-2 d). |
| `pd:146` (H-C data line) | Add: "A run killed at the kill value counts as above T-4 (Stop rule S-3.1)." | Without it T-4 cannot fail when kills are enforced (I-2). |
| `pd:197-199` (Owner approval) | Add a first bullet: "Before the pilot: the owner approves the stop rule, the reading of SD-3 and the two pilot ceilings of Stop rule S-2.1." Shorten the own note at `pd:199` accordingly. | Rule 2 cites an approved ceiling that no step approves (D-2 a). |
| `pd:210` (SD-6) | Change the handling column to: "Proposed rule S-0 to S-4 marked as own, for owner decision; it also settles the safety scope for the legacy arms and the handling of killed and failed runs, which the source does not state." | Records the two further gaps the rule fills. |
| `pd:222` (Stage 0 exit item 4) | No change needed; it already says the stop rule awaits the owner. | |

## What I could not determine

1. **Whether the source's safety list covers the legacy arms.** `src:530` lists the events without naming arms; S-1.3 reads it as a criterion on the panel. If the owner reads it as covering all arms, S-1.2 must halt on arm-B events too, and D-1's likely outcome (a halt caused by the control arm) applies.
2. **Whether `src:519`'s citation still holds.** It cites `SKILL.md:666` for "a 2-of-3 run is MALFORMED"; line 666 of the current `SKILL.md` is about agents not introduced, and a search for "2-of-3", "reviewer-shortfall" and "fewer than 3" found no such rule. D-1 does not depend on it: it rests on `pd:173` and `SKILL.md:837`.
3. **Whether a run with no contract is a "MALFORMED contract".** The source does not say; S-3.2 treats it as a failed run, for the owner to confirm.
4. **Which meter the pilot harness will use, and whether it enforces the kill today.** No pilot harness exists in the files I read. The profile unit is "1 turn ≈ 1k claude tokens" (`cost-profile.yaml:27-29`); whether the harness's measured claude tokens equal that unit is unverified, and S-2 assumes they do.
5. **Which "d between arms" T-6 compares with d0.** `src:538` says "d between arms" without naming the pair; S-4 applies it after the last block for whichever pair the owner names (d_BC, d_AB, or both).
6. **Which 6 plans arm D runs on.** The source does not say (`src:538`); S-0 picks them at random before block 1.
7. **The arm letters in the review brief.** The brief called A legacy T2, B panel T2 and C T1 only; the source and the pilot design use A = T1, B = legacy, C = panel (`src:532`, `pd:46-51`). This review follows the source.
8. **The one-rerun allowance in S-3.2** is my choice, not derived from any source figure; the owner may set it to zero.
