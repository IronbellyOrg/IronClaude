# Adversarial Debate Transcript

## Metadata
- Depth: quick
- Rounds completed: 1 (Round 2 skipped: depth=quick; Round 2.5 (invariant probe) skipped: --depth quick; Round 3 skipped: depth=quick)
- Convergence achieved: 93.75% (15 of 16 diff points)
- Convergence threshold: 80%
- Focus areas: All
- Advocate count: 2 (Variant 1 = OURS advocate, Variant 2 = CLAY advocate; both dispatched as parallel Task agents, persona analyzer, default model)
- Debate rule given to both advocates: the owner's weighting rule (owner wins unless Clay shows a clear evidenced benefit; tie goes to owner; separable Clay benefit is adopted as hybrid)
- Taxonomy coverage after Round 1: L1 = S-001, S-002; L2 = C-001, C-002, C-005, X-001, A-001; L3 = C-003, C-004, C-006, C-007, X-002, X-003, A-002, A-003, A-004. All three levels covered; no forced round needed.
- Shared-assumption responses: both advocates answered every A-001 to A-004 (no [OMISSION] flags).

## Round 1: Advocate Statements

### Variant 1 Advocate (OURS, default model, persona analyzer)
**Position**: Variant 1 should hold on OD-2 and OD-13: Clay's own text admits that a re-plan voids the approval and that nothing replaces it, and a held place with no worker running is a defect the in-flight code can already avoid. Variant 1 is weakest on OD-1, where its evidence is thin; the tie rule still favors `quick` because Clay's benefit is unmeasured. Clay's loop mechanics (C-006) are a separable benefit to adopt as a hybrid.

**Steelman of Variant 2**:
Clay's design is one coherent machine. Ruling 36 sends a `left_open` issue back "to the orchestrator and not to the owner" (D:610). The `handback` verb is bounded by `cap`, `no_progress` and `no_remaining` (D:612). The old worker must be final first (D:614), and every step is read-then-write so a restart is safe (D:620). The state file stays `in_progress`, so "in flight means someone owns it" (D:616). G6 is a real cost argument: one good plan lets cheaper models build, and a weak plan is paid for in every later wave (D:60, D:722). V2 also found the gap in its own design (the wave-1 re-check covers only `hold:backlog` and `plan_check`, V2 fact 9).

**Key strengths claimed**:
1. Round 2 must pass a gate. D01 item 5: any body edit after the approval voids it (`predicates.py:249-259`); D01 item 3 (MR-1): the check at start must repeat the approval; V2's own costs section concedes nothing replaces the voided approval; D15 R-6 (line 32) already ruled that round 2 passes the start gate again.
2. Only live work holds a place. Verified at `route.py:393`: "`done`, `skipped`, `failed` and `escalated` files do not count, and an `escalated` file that returns to `in_progress` counts again." A waiting hand-back modeled as `escalated` follows the code's own principle; it is not a new counting rule.
3. The never-freed place becomes a defect once a person is in the loop (D:616; C-INV-1, D15 line 140): three waiting hand-backs make the repo answer `coordinator_full` while nobody works.
4. C-INV-2 is real and verified: `cycle.py:993-994` returns `None` for any entry whose state is not `failed` ("already woken, acknowledged or abandoned: never woken again"); without a new wake path a re-approval is never noticed.
5. `quick` is the default of record (D15 G-2). Clay's benefit depends on a `plan_tier`-to-depth table that is not on master (UNVERIFIED). Neither side has a cost or quality baseline. A plain `plan_depth` key still lets the owner choose `deep` per repo, so Clay's lever is kept.

**Weaknesses identified in Variant 2**:
1. Its design as written contradicts the owner's gate: V2 fact 9 and its costs say no round-2 approval exists; D:488 re-checks only `hold:backlog` and `plan_check`; the re-plan edits the body (D:1076-1080), voiding the approval; a new worker then starts on a body nobody approved.
2. The "no waiting step" claim holds only because there is no person step; that is the gap, not a feature. V2 offers option (b) as a patch but does not choose it.
3. The tier-to-depth mapping is undefined: D:726 says the plan call "passes `plan_tier` as the `--depth` of `/sc:issue --plan`", but `plan_tier` holds tier names (`tier1b`) and `--depth` takes `quick|standard|deep`; the bridging table is in PR P `refs/intake.md`, not on master (UNVERIFIED). V2's `deep` claim rests on D15's reading, not on Clay's text.
4. Cost is multiplied and unmeasured: the wave-2 re-plan also passes `--depth <d>` (D:618), so a `deep` default runs the most expensive planner up to 4 times per issue (`1 + HANDBACK_MAX`); D12 records no cost baseline.
5. A cap of 3 held places blocks the repo (V2's own cost line); that is the "simple invariant" failing under load.

**Concessions**:
- Reviewer note agreed: V1 fact 2 cites D12 item 6 (`D12/VERDICT.md:22`), which defers a higher tier floor at create for medium and complex issues ("no cost baseline"); it says nothing about the `--plan` default depth. It is a related argument, not a source for OD-1. The direct source is D15 G-2 (fact 3).
- G6 is a genuine quality lever and `quick` gives it up; a `quick` plan that passes `plan_check` is only caught if the person reads it.
- V1 has no loop mechanics; C-006 is a clear V2 win.
- Option (a) adds a person step per round and needs C-INV-2 built. Option (b) removes both C-INV-1 and C-INV-2; the advocate keeps (a) as the owner-line default but calls (b) acceptable if a cheaper path is wanted.
- Most of V1's evidence is second-hand verdict citations (S-002).

**Concrete proposal for C-003/C-004 (V1 advocate)**: use status `escalated` with a new step `handback_awaiting_approval(body_sha)`. (1) `handback` writes `in_progress`, wave 2, `handback_recorded` (D:613); a live plan worker counts. (2) After `plan_recorded(body_sha)` the orchestrator writes `escalated`, step `handback_awaiting_approval`; by `route.py:393` this stops counting. D:608 already has the category "an issue waiting mid-work for a person keeps today's behaviour" (entry `stalled` if the orchestrator is down; `--take` refuses it). (3) On re-approval a wake path (C-INV-2) repeats the full start check (approval, `unchanged_since`, Status allow-list, `plan_check`) then flips the file back to `in_progress` at wave 4. UNVERIFIED: whether the flip can overshoot `max_in_flight` if new work took the freed place; whether `--take` and the row-9 rules for `escalated` also catch this file (D:617 says a hand-back is "not an escalation", so a visible waiting reason may be needed); which component runs the wake path (the poll does not); whether the restored WC-17 flow can be the gate.

**Shared-assumption responses (V1 advocate)**: A-001 QUALIFY (favors V1); A-002 QUALIFY (favors V1); A-003 QUALIFY (favors V1; L-1 is real but the owner accepted it; approval still forces a visible human step per round); A-004 QUALIFY (favors V1; excluding `escalated` is a status choice, not counting code that must survive).

### Variant 2 Advocate (CLAY, default model, persona analyzer)
**Position**: Clay's line should lose the contested rule. A round that starts with no new approval has no stated gate in the design text, and the owner's start gate is the safer reading. Clay's line holds real, separable value that does not depend on that rule: the loop bounds, the old-worker-final rule, the idempotent re-plan marker, and the `--remaining` re-plan that keeps done items; it asks for those as a hybrid. It does not defend a `deep` default.

**Steelman of Variant 1**:
`plan_check` proves three headings are filled in (presence, not quality; `hold.py:122-143` in PR 686, cited by V1, not re-read by this advocate), so a person has to be the quality gate. A re-plan edits the issue body and a body edit after approval voids the approval (`predicates.py:249-259`, cited by D01 and V1, not re-read), so the plan must come before the approval and round 2 must pass the start gate again. Clay's own text gives wave 2 no approval check: wave 8 sends the issue back "to the orchestrator and not to the owner" (D:610) and "Wave 1 ... and wave 3 ... are not run again" (D:615). Counting only live work is how the code already behaves: in `route.in_flight` (route.py:379-426, read) `done`, `skipped`, `failed` and `escalated` files do not count (lines 393-395). V1 also names a real requirement: under any person step something must wake the coordinator, because `cycle.py:993-994` returns `None` for any entry that is not `failed` (read; matches).

**Key strengths claimed**:
1. The loop is fully specified and restart-safe: `handback` decides in a fixed order `no_remaining`, `cap` (`HANDBACK_MAX` = 3, four rounds at most), `no_progress` (D:612); writes state under lock by temp file and `rename`, keyed by round and merge commit so a repeat changes nothing (D:613). V1 has no equivalent.
2. The old worker must be final first: `handback` is not called until the old Dispatch has its `worker_done`, "absence never authorizes a release or a second worker" (D:614).
3. The re-plan is idempotent: marker `<!-- sc:issue:replan round=<n> -->` makes a rerun write nothing twice; `--remaining` replaces only `## Fix approach` and `## Test plan`, keeps done items as `- [x]`, leaves every other byte unchanged (D:1078-1080).
4. G6 is a real quality argument (D:60, D:722; verified in the text).
5. The design states its own limits: fidelity of done items marked UNVERIFIED (U60, D:1081); `HANDBACK_MAX` "this design's value, not measured" (D:612).

**Weaknesses identified in Variant 1**:
1. The round-2 gate has no owner: C-INV-2 admits the poll never wakes an acknowledged entry; nobody has specified who re-checks approval at round 2; the WC-17 restored flow as the gate is UNVERIFIED in V1 itself.
2. V1 has no loop mechanics (`no_progress`, marker, old-worker-final); a per-round approval still needs them, otherwise a person approves the same remaining list twice or a second worker starts while the first is live.
3. One source is mis-cited (V1 fact 2 / D12 item 6 is a creation-time tier floor); the OD-1 case rests on "tie goes to the owner", not on a cost baseline.
4. Much of V1's evidence is second-hand (verdicts D01, D12, D14); only `route.py` and `cycle.py` are first-hand, both confirmed.

**Concessions**:
- No round-2 approval in the design text (wave-1 re-check covers `hold:backlog` and `plan_check` only, `orchestrator.md:488`; wave 1 is not rerun, D:615); the re-plan voids any earlier approval and nothing replaces it; V2's own costs admit this. Under the weighting rule that settles OD-2 for the owner.
- `deep` is not evidenced: the tier-to-depth table sits in PR P `refs/intake.md`, not on master (UNVERIFIED); the D15 OD-1 row says only "a cheaper planner than Clay's goal G6 wants". No cost baseline (D12), so a tie goes to `quick`.
- Keeping a place counted can block the repo: three hand-backs in flight hold `max_in_flight` = 3.
- `--remaining` fidelity is unproven (U60).

**Parts of Variant 2 adoptable as hybrid (independent of the no-approval rule)**: (1) handback bounds (D:612); (2) old-worker-final (D:614); (3) idempotent re-plan and `--remaining` (D:1078-1080); (4) round-n handoff block (D:619); (5) the waiting step as `escalated`, step `handback_awaiting_approval` (the advocate's proposal, relying on route.py:393-395 and D:608); (6) G6 as an option: keep `quick` as default and let a repo set a higher `plan_depth`. Not adoptable under the weighting rule: the `deep` default (C-001) and "no approval between re-plan and worker" (C-003).

**Shared-assumption responses (V2 advocate)**: A-001 QUALIFY (favors V1; a deeper planner is plausibly better but unmeasured); A-002 QUALIFY (favors V1; rarity assumed, not shown); A-003 QUALIFY (favors V1; the approval is a recorded step, not proof of identity; does not flip OD-2, an owner policy); A-004 QUALIFY (favors V1; `in_flight` lives in `route.py`, not the `repos.py` that D14 says does not land; survival of `route.py` UNVERIFIED).

### Orchestrator verification of advocate-cited facts (read from disk after the round)
- `route.py:393-395` (snapshot pr-a): the docstring says `done`, `skipped`, `failed` and `escalated` files do not count and an `escalated` file that returns to `in_progress` counts again; line 399 skips a readable file whose status is not `in_progress`. Confirmed.
- `cycle.py:993-994`: `if entry.state != "failed": return None  # already woken, acknowledged or abandoned: never woken again (4.3)`. Confirmed.
- Design D:605 states that on `closeout_failed` "sets the issue's state file to `escalated` (so the issue leaves the places in flight, 5.7)". D:608 says "every other `escalated` file (an issue waiting mid-work for a person) keeps today's behaviour: its entry is `stalled` when its orchestrator is down and `--take` refuses it". Confirmed. D:617 says a hand-back stop is raised as row 9 and D:616 says nothing is escalated for a hand-back; so the waiting-for-approval use of `escalated` is an extension, UNVERIFIED as to the row-9 and `--take` side effects.
- D15 merged position, OD-1 option list says `deep` "the value Clay's default tier implies"; the D15 VERDICT OD-1 row says only "a cheaper planner than Clay's goal G6 wants". The V2 advocate's remark that D15 "never says deep" is true for the VERDICT table and false for the merged position file. Neither fixes the table, which is not on master (UNVERIFIED).
- D12 VERDICT item 6 (`debates/D12/VERDICT.md:22`): about a higher tier floor at create for medium and complex issues. Both advocates and the diff analysis agree it is not a direct source for the `--plan` default.

## Round 2: Rebuttals
Skipped: depth=quick.

## Round 3: Final Arguments
Skipped: depth=quick.

## Scoring Matrix

| Diff Point | Winner | Confidence | Evidence Summary |
|------------|--------|------------|-----------------|
| S-001 | Tie (no difference) | 90% | Identical six headings; both advocates call it Hybrid. |
| S-002 | Tie (Hybrid) | 60% | V2 cites design lines first-hand; V1's three code citations were verified by both advocates and by the orchestrator. |
| C-001 | Variant 1 | 66% | `quick` is the documented `--plan` default (D15 G-2); `deep` rests on an UNVERIFIED table and no cost baseline; both advocates side with V1. |
| C-002 | Variant 1 | 72% | A plain `plan_depth` key needs no table absent from master; D:726 passes a tier name where `--depth` takes quick/standard/deep. |
| C-003 | Variant 1 | 78% | A re-plan voids the approval (`predicates.py:249-259`); V2's text has no round-2 gate and V2's advocate concedes it. |
| C-004 | Variant 1 | 76% | `route.py:393-395` and D:605/D:608 already free a place when work waits on a person; the mechanism (status `escalated` plus step) is UNVERIFIED as to side effects. |
| C-005 | Hybrid | 60% | Person approval catches quality; a stronger planner lowers the cost of weak plans; a per-repo `plan_depth` keeps both open. |
| C-006 | Variant 2 | 86% | `handback` bounds, old-worker-final and the idempotent marker hold under any start rule (D:612-614, D:1078); V1 has none. |
| C-007 | Variant 1 | 80% | Any person step needs a wake path; `cycle.py:993-994` shows none exists today. |
| X-001 | Variant 1 | 66% | Same reasoning as C-001. |
| X-002 | Variant 1 | 55% | V1 advocate: defect; V2 advocate: Hybrid ("in flight means someone owns it" right for live workers; Clay's `escalated` handles the person wait). Not unanimous. |
| X-003 | Variant 1 | 79% | D01 item 5, D15 R-6; V2 admits the text lacks a gate. |
| A-001 | QUALIFY, favors V1 | 69% | No measurement of plan quality or cost per depth; the burden is on the side asking for the costlier default. |
| A-002 | QUALIFY, favors V1 | 67% | `HANDBACK_MAX` unmeasured; rarity assumed; a counted pile blocks the repo, a waiting pile is visible. |
| A-003 | QUALIFY, favors V1 | 65% | Approval is a recorded step, weak against an agent on the same login (L-1); it still forces a visible human step; it does not flip an owner policy. |
| A-004 | QUALIFY, favors V1 | 61% | Excluding `escalated` is a status choice that needs no new counting code; survival of `route.py` after PR 686 adaptation is UNVERIFIED. |

## Convergence Assessment
- Points resolved: 15 of 16 (agreed = both advocates name the same superior approach; X-002 is the one split: Variant 1 against Hybrid)
- Alignment: 93.75%
- Threshold: 80%
- Taxonomy coverage gate: passed (L1, L2, L3 all covered)
- Invariant probe gate: not applied (Round 2.5 skipped at depth quick)
- Status: CONVERGED
- Unresolved points: X-002 (is a held place with no worker a defect: both advocates reach the same practical result, exclude the waiting step, but differ on whether Clay's counting rule is "wrong")
- Limitation recorded: both advocates were given the owner's weighting rule and one advocate conceded C-001 and C-003 early, so the high convergence partly reflects the rule. The points where Clay's line wins or draws (C-005, C-006) are the ones that survived that pressure.
