# Proposal B: review of the "Stop rule" section of pilot-design.md

Reviewed text: `pilot-design.md:178-189` (section "Stop rule"), plus SD-6 (`pilot-design.md:210`). `src` = `merged-requirements.md`. `pd` = `pilot-design.md`. Other paths: `SKILL.md` = `src/superclaude/skills/sc-reflect-protocol/SKILL.md`; `cost-profile.yaml` = `src/superclaude/skills/sc-reflect-protocol/refs/cost-profile.yaml`.

Method: read all of `pd`; read `src:474-545` (cost model, risks, first measurement); read `src:411`, `cost-profile.yaml:30-75` and `SKILL.md:265-272` for the kill line. Did not read any other reviewer's file.

## Improvements (3)

**I-1. Classify the safety events, attribute them to an arm, and name the detector for each, instead of one "stop at the first T-5 event".**
Rationale: the source states T-5 as a verdict criterion ("fails regardless of savings", `src:530`, `pd:23`), not as a halt order. Rule 1 (`pd:187`) turns it into "no further runs" for all five events and all four arms. The five events differ in harm and in whose behaviour they measure: a reviewer repository write (item 4) is real damage and must halt everything; a MALFORMED contract (item 2) is baseline behaviour of legacy on 2-of-3 runs today (`src:519` row 11; `SKILL.md:666`). A table with class (harm / verdict), arm scope and a run-boundary detector makes the rule executable and keeps the pilot's purpose (estimating d, `pd:3`, `pd:71`).

**I-2. Make the cost stop a number the owner sets before run 1, tested before every dispatch, with a per-run guard and a projection warning.**
Rationale: rule 2 (`pd:188`) names a ceiling as "row C-5 upper bound, or C-2" and does not say who fixes it, in which unit it is metered, or how "a run that would take spend above" is computed. The profile already has a per-run guard: `hard_kill_multiplier: 1.25`, "Callers MUST abort runs that exceed 1.25x the midpoint" (`cost-profile.yaml:69-70`; 52 x 1.25 = 65k, `src:479`), and T-4 is that same number (`pd:20`). The pilot must say what happens to a run aborted there. A projection from observed per-arm cost gives the operator a warning before the ceiling bites, which a ceiling set at the worst case cannot (see D-2).

**I-3. Add run-order, interim checkpoints, a precedence order and a stop record, so each run boundary has a defined decision and each stop leaves usable evidence.**
Rationale: rule 3 (`pd:189`) says "no early stop for success" and nothing else about information value. The pilot can burn all of C-5 (1.30M-2.62M, `pd:131`) and still return nothing usable if the seeding is too easy (T1 recall above 1 - T-1 = 0.85 leaves no room for H-A, own arithmetic), a grader sees arm identity (`src:532`), too many runs are null/killed, or the 6 arm-B repeats for d0 (`src:538`) run last so T-6 (`pd:22`) is learned after all spend. Checkpoints at a fixed fraction of the pilot, a fixed order of rules and a fixed log record turn "report to the owner" (`pd:187`, `pd:188`) into something the owner can act on.

## Defects (3)

**D-1. Rule 1 can end the pilot on baseline legacy behaviour and cannot be evaluated at the run boundary for at least one event.**
Evidence: (a) T-5 item 2, "a MALFORMED contract" (`pd:37`, `src:530`), is not scoped to the panel arms; `src:519` row 11 says the interactive skill calls a 2-of-3 run MALFORMED today (`SKILL.md:666`, probability "High (exists today)"). Arm B is legacy T2 (`pd:49`). Rule 1 would therefore halt the pilot at the first arm-B run that hits the legacy shortfall, with no estimate of d. (b) T-5 item 3, "an unsupported citation certified" (`pd:38`), is only known after the citation is re-read against the repository; the pilot grades with a blinded grader (`pd:63`) after runs, so "first safety event" has no defined detection time. (c) Rule 1 conflicts with the section's own rule 3 and with `pd:3`: a verdict criterion (T-5) becomes a halt, so a single arm-C contract problem on plan 1 throws away arms A, B and D, which are the H-A and d0 data. Result: the rule as written either halts spuriously or detects late.

**D-2. Rule 2 does not bind: its ceiling is the worst-case estimate, is not metered in a stated unit, and ignores cost the rows leave out.**
Evidence: (a) The ceiling is "row C-5 upper bound" = 2,616k (`pd:131`), the sum of the profile's high ends, which are estimates, not measurements (`pd:11`, `src:477`). A run only exceeds it if every run already ran at the profile high end or above, so the rule fires after the money is gone, not before. (b) "or C-2 if arm D and the repeats are dropped" (`pd:188`) makes dropping the repeats a spending outcome, but the repeats are the only source of d0 and T-6 (`pd:69`, `src:538`): the rule can silently remove the measurement it is protecting. (c) C-1 to C-6 price arms only (`pd:127-132`); grading by blinded graders, seeding, and pilot orchestration are not in them, and retrieval (R-1 to R-5) is excluded from any sum (`pd:123`, `pd:136`), so there is no meter on which "cumulative spend" is defined. (d) T-4 equals the kill line (`pd:20`, `src:479`), and the profile aborts runs above it (`cost-profile.yaml:69-70`), so measured tokens are censored at about 65k; the rule does not say whether a killed run is a data point, a retry, or a stop. (e) arm C may be the `shadow` run (`pd:50`), whose token cost for the pilot's meter is not stated.

**D-3. No stop or pause for an uninformative pilot, no ordering, and no precedence between the three rules.**
Evidence: (a) Rule 3 (`pd:189`) forbids early stops except 1 and 2, so a pilot whose arms are indistinguishable from noise (T-6, `pd:22`, `pd:183`) or whose seeded recall is at floor or ceiling runs to completion; `pd:183` records that T-6 exists but the rule does not say when it is checked. (b) The only run order implied is "arms A, B, C on 12 plans, plus 6 repeats" (`pd:48-49`); if repeats run last, d0 appears after all spend. (c) With 12 observations per arm, a p95 is essentially the maximum (own arithmetic: 0.95 x 12 = 11.4, so the 12th ranked value), so T-4 (`pd:20`) has no stable pilot value and a single kill decides it; the rule neither says this nor tells the operator to treat it as a descriptive number. (d) If rules 1 and 2 fire in the same boundary (a reviewer write that also crosses the ceiling), nothing says which is recorded. (e) The section lists no precondition: the Stage 0 conversion gate is FAIL and the plan stops at Task 4 for owner review (`pd:171`, `pd:199`, `pd:226`), so "before the pilot runs" has no stated state to start from. (f) "report to the owner" (`pd:187`, `pd:188`) lists no content, so a stop leaves no evidence that could be audited or used to re-plan.

## Proposed replacement text

Replace `pd:178-189` (the whole section "Stop rule") with the following.

---

## Stop rule

The source requires "a stop rule" as pilot hygiene but does not state one (`src:538`). What the source does fix:

- any safety event (T-5) fails the measurement regardless of savings (`src:530`);
- when d0 reaches T-6, the arms are indistinguishable from noise (`src:538`);
- runs above the profile's hard kill line (about 65k, the same number as T-4) are aborted by the caller (`cost-profile.yaml:69-70`, `src:479`).

**Everything below is PROPOSED (own note, not in the source; the owner confirms or replaces it before run 1).** Words used: **STOP** ends the pilot; **PAUSE** means no new run is dispatched until the owner answers; **LOG** means record and continue.

**Before run 1 (own note).** The owner has fixed in writing: (a) the spend ceiling, a single number in claude tokens (see rule S-3); (b) the reading of "6 repeats of arm B" (SD-3); (c) the run order (below); (d) this rule. The Stage 0 exit state (`pd:226`) is stated in the approval request; the pilot does not start while the owner has not accepted it.

**Run order (own note).** Plans are run one at a time; all arms of plan k finish before plan k+1 starts; the order of arms inside a plan is randomised and recorded; the 6 arm-B repeats are spread over the plan sequence (own choice: one after plans 2, 4, 6, 8, 10 and 12 when read as 6 runs in total) so that d0 is estimable at the half-way checkpoint. This does not change any threshold.

**Run-boundary check (own note).** After each run completes, and before the next is dispatched, the operator evaluates S-1 to S-5 in this order. The first rule that fires is the recorded cause; later rules that also fire at the same boundary are written into the same stop record.

| Rule | Fires when | Action |
|---|---|---|
| S-1 harm event | T-5 item 4 (a reviewer wrote to the repository) in any arm, or item 1 (a forbidden model or executor-class collision was dispatched) in any arm | STOP. Cancel in-flight runs. |
| S-2 verdict event | T-5 item 2 (MALFORMED), 3 (unsupported citation certified) or 5 (a T1 or `--depth quick` run called the panel) in an arm that is not legacy; or item 5 in arm A | PAUSE dispatch of arms C and D. Arms A and B continue only if the owner says so. The pilot's T-5 verdict is recorded as failed. |
| S-3 spend | before dispatching a run, cumulative claude tokens spent plus that run's profile high estimate (3k-8k for arm A: 8k; 35k-70k for B, C and D: 70k, `src:479`) would exceed the owner's ceiling | STOP. Do not drop arms or repeats to fit under the ceiling. |
| S-4 run validity | at the end of a plan: 2 or more of the first 4 runs of any one arm are invalid (null convergence score, MALFORMED, aborted at the kill line, or crashed), or a grader received arm identity | PAUSE |
| S-5 information | see "Checkpoints" below | PAUSE |

Notes on the rules (own note unless a source is given):

1. **S-1 and S-2: scope.** T-5 item 2 is not counted against arm B (legacy T2) because the source records that legacy already returns MALFORMED on a 2-of-3 run (`src:519` row 11, `SKILL.md:666`); a MALFORMED in arm B is LOGGED as baseline and counted in the H-B comparison. Item 4 (reviewer write) is a harm event in every arm, because reviewers never write (`src:392`).
2. **Detectors at the run boundary.** Item 1: the dispatch record of resolved models and executor class. Item 2: the contract status of the run. Item 3: a mechanical re-read of every certified `file:line` citation (the evidence-validator pattern), run by the operator, not by a blinded grader. Item 4: the repository status and a tree hash taken before and after each run, compared. Item 5: the dispatch log of arm A and of any `--depth quick` run. An event that no detector can see at the boundary is evaluated at the next checkpoint and logged as "detected late".
3. **S-3: the ceiling.** The ceiling is chosen by the owner in claude tokens and must be at least the pilot's priced high end, row C-5 (2.62M) when arm D and 6 arm-B repeats are included, and is expected to include the cost of grading and orchestration, which rows C-1 to C-6 do not price (SD-8 below). Retrieval tokens are watched on their own meter against rows R-1 to R-4 and never added to the claude-token total (`pd:123`); a retrieval total above 1.5 x row R-2 plus R-3 plus R-4 (own choice, no source) is a PAUSE.
4. **Per-run guard.** A run that reaches the profile hard kill line (T-4, 65k) is aborted by the pilot driver, as the profile requires for callers (`cost-profile.yaml:69-70`). It is recorded as KILLED with its tokens at abort, counts as an H-C exceedance (T-4), is not retried and is not dropped from the recall data (its partial findings are scored as found). If the owner prefers to let such runs finish to measure the true tail, that is a change to this rule and to T-4's meaning, and is the owner's call.
5. **Projection warning.** After each plan, the operator computes projected total = spent + (remaining runs of each arm x that arm's observed mean tokens). If it exceeds the ceiling, that is a PAUSE with the projection in the stop record. This fires before S-3 and costs nothing.

**Checkpoints (S-5, own note).** The pilot has 12 plans, so the checkpoints are fixed at plan 4 (one third, 20 seeded defects) and plan 6 (half, 30 defects). Numbers are the pilot's own sizes, not thresholds from the source.

| At | Check | PAUSE when |
|---|---|---|
| plan 4 | harness headroom: arm A recall on the seeded defects | above 0.85 (so T2 could not beat T1 by T-1: 1 - 0.15 = 0.85, own arithmetic) or at 0 (the seeded defects are not findable at all) |
| plan 4 | blinding and grading: graders' labels agree with the operator's plan numbers and no arm identity appears in grader input | any leak |
| plan 6 | noise: d0 from the repeats done so far (at least 3 are done under the run order above) against d_BC | d0 at least T-6 x d_BC, i.e. d0 >= 0.8 x d_BC (`src:538`); with 3 repeats this is a rough value and the stop record says so |
| plan 6 | spend: projection against the ceiling | projected total above the ceiling |

A PAUSE at S-4 or S-5 gives the owner three answers: continue unchanged, change the seeding or harness and restart the affected plans (earlier runs are kept in the record and not mixed into the estimate), or stop. The stop is the owner's, not the operator's.

**No early stop for success (`src:538` reading).** The pilot estimates d and does not decide H-B (`src:536`); success of H-B, H-C or H-A is never a reason to stop. T-3, T-4 and T-5 are reported at the end of every pilot that completes, T-4 as a descriptive value (with 12 runs per arm a p95 is essentially the maximum run, own arithmetic).

**Stop record (own note).** Every STOP and every PAUSE writes one record to `<pilot output dir>/stop-record.md` before anything else happens, with:

1. the rule id (S-1 to S-5), the threshold id (T-n) and the observed value against it;
2. the run id (plan, arm, repeat number), start and end time (UTC), and the position in the run order;
3. cumulative claude tokens and, separately, retrieval tokens; per-arm totals; the run's own tokens; the projection if rule S-3 or the projection warning was involved;
4. the detector output that triggered it (for S-1: the before/after repository status and the diff; for S-2: the contract status or the citation re-read result; for S-4: the invalid-run list);
5. in-flight runs and what was done with them (finished, cancelled, scored);
6. runs completed so far by arm, and whether their data is usable for d_AB, d_BC and d0 (own note: a pilot stopped by S-1 gives no estimate, one stopped by S-3 gives estimates with the stated n);
7. any other S-rule that also fired at the same boundary (precedence: S-1, then S-2, S-3, S-4, S-5);
8. the owner's answer and its time, when the record is for a PAUSE.

The operator, not a grader, writes the stop record. Graders keep seeing blinded input; arm identity is unblinded only in the operator's record (`src:532`).

---

## Consistency edits needed

Minimal list of other lines in `pilot-design.md` that must change if the replacement is adopted (this reviewer did not edit them):

1. `pd:70` ("Hygiene: ... a stop rule (see "Stop rule") ..."): keep as is; the reference still resolves.
2. `pd:195-199` ("Owner approval"): add a "Before the pilot" bullet listing the five things the owner confirms: the ceiling number, the SD-3 reading, the run order, the S-1 to S-5 rule, and acceptance of the Stage 0 exit state. The present bullet at `pd:199` names the stop rule and SD-3 only.
3. `pd:210` (SD-6): change "Proposed rule marked as own, for owner decision." to say that the rule is expanded to S-1 to S-5 with checkpoints and a stop record, still all own and still for owner decision.
4. After `pd:211`, add **SD-8** (own note): "Rows C-1 to C-6 omit the cost of blinded grading, seeding and orchestration; retrieval is outside the claude-token sum. The ceiling in rule S-3 must be set with these in mind." (Owner supplies the figure; see below.)
5. `pd:222` (Stage 0 exit checklist item 4): change "the stop rule and the reading of the arm-B repeats await the owner (SD-3, SD-6)" to add "and the spend ceiling".
6. `pd:134` (SD-3 note): add a sentence that the 6-run reading fixes where the repeats sit in the run order (rule above), and the 72-run reading would move the ceiling from 2.62M to about 5.0M (own arithmetic from row C-5: 876k + 210k + 2,520k = 3,606k low, 1,776k + 420k + 5,040k = 7,236k high, so the ceiling, not just C-4, changes).
7. `pd:146` (H-C data sentence): add "T-4 is reported as a descriptive value at pilot size (12 runs per arm); a run aborted at the kill line counts as an exceedance."
8. Thresholds table: no row changes. No new T-n is added, because every number in the replacement is either a source value, a source-derived arithmetic value (0.85, 0.8 x d, 65k, 70k, 8k) or a pilot-size choice marked own (4 of the first 4 runs invalid is 2 of 4; checkpoints at plan 4 and 6; retrieval 1.5x). If the owner wants them as thresholds, add T-11 to T-13 at that time.

## What I could not determine

- The cost of blinded grading, seed construction and pilot orchestration. No row prices them, and nothing in `src:474-500` does; the ceiling figure is therefore the owner's to give. I did not invent one.
- Whether the `shadow` form of arm C (`pd:50`) runs legacy and panel both in one run, in which case arm C's cost per plan is more than 35k-70k and C-1, C-2 and the meter in S-3 are too low. `src` does not say.
- Who enforces the 65k kill line in a pilot run. `cost-profile.yaml:69-70` says "callers", and `SKILL.md:269-270` says no constraint applies for a budget of 65 or more or when `--budget-remaining` is unset (`src:411` records the default `/sc:workflow` call as unset). Rule note 4 therefore makes the pilot driver the enforcer; whether the driver can do that is not verified.
- Whether a pre/post repository tree hash (detector for T-5 item 4) is cheap and race-free when several runs run in parallel; the replacement assumes plans run one at a time.
- The choice between "PAUSE the panel arms only" and "STOP everything" for S-2 is a policy call with no source; it is marked own. The threshold "2 of the first 4 runs invalid" and the 1.5x retrieval watch are my own placeholders, chosen as round numbers that the owner should replace.
- How many seeded-defect findings a killed run has already produced; "scored as found" in note 4 assumes partial cards exist at abort.
