<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 1 (OURS, variant-1-original.md) -->
<!-- Merge date: 2026-11-20T09:13:28Z -->

<!-- Source: Base (original) -->
# QG1 position paper: OURS (the owner's line)

Topic: planning and hand-back. Sub-questions OD-1 (default plan depth), OD-2 (how hand-back round 2 starts), OD-13 (a hand-back waiting for re-approval versus the in-flight count). Source of the answers: D15 VERDICT section 7 (`/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/VERDICT.md`, lines 150-166) and the merged D15 position, section (h).

<!-- Source: Base (original, modified) - Claim 1 extended per Change #2 (from Variant 2, Claim 1, goal G6); Claim 3 extended per Change #5 (from the debate transcript); Claim 2 is Base (original) -->
<!-- Source: Variant 2, Claim 1 and Mechanism bullet 1 (design lines 60, 722-724) - merged per Change #2 -->
## Claim

1. OD-1: the default `plan_depth` is `quick` (the `--plan` default; equal to leaving the key unset). A repo may opt in to `standard` or `deep` with a per-repo `plan_depth`, a plain key passed straight to `--depth`, with no tier-to-depth table.
2. OD-2: round 2 and later re-plan the issue body and the person re-applies the approval (option a). No separate chat go per round.
3. OD-13: an issue that waits for that re-approval is NOT counted in `max_in_flight`; show it as a visible waiting reason; add an expiry later only if waiting issues pile up. The waiting step is carried by a state file with status `escalated` and step `handback_awaiting_approval(body_sha)`, which the in-flight count already skips (this carrier is UNVERIFIED as to side effects; see the fourth Mechanism bullet).

<!-- Source: Base (original, modified) - bullet 3 path corrected per Change #4 and extended per Change #3 (from Variant 2, Cited fact 9, D01 MR-1); bullet 4 replaced and extended per Change #5 (from the debate transcript, checked against route.py:399 and design lines 605, 608, 616, 617); bullets 1 and 2 are Base (original) -->
## Mechanism

- The plan call is `/sc:issue --plan <N> --depth <d>`. The depth picks the worker: quick `issue-worker-t3`, standard `issue-worker-t2`, deep `issue-worker-t1` (D12/D15 G-2, citing PR P `refs/plan.md:56-60`). With no key the call runs `quick`.
- The plan check (`plan_check`, `hold.py:122-143` in PR 686) proves that three headings are filled in. It proves presence, not quality. A person's approval is the quality gate (D01 verdict, Strongest points 1; D15 OD-1 row).
- A re-plan edits the issue body. Any body edit after the approval voids it (`src/superclaude/cli/issue_watch/predicates.py:249-259` in snapshot master, D01 item 5). So round 2 must pass the start gate again; "re-plan then re-approve" is the order D01 item 5 already requires ("the plan must exist before the approval"). The check at the moment of start must repeat the approval, not only `hold:backlog` and `plan_check` (D01 VERDICT item 3, MR-1; Clay's wave-1 re-check at design line 488 covers only those two). Test: remove the approval between the wake and the start; the start must be refused.
- A waiting issue has no worker running. `route.in_flight` (`pr-a/.../route.py:379-426`) counts a state file only while it is `in_progress`, a poll entry while `pending`/`woken`/`unknown`, and an open plan request; `done`, `skipped`, `failed`, `escalated` do not count. A waiting step written as status `escalated` with step `handback_awaiting_approval` follows the same principle: only live work holds a place. `route.in_flight` skips any readable file whose status is not `in_progress` (`route.py:399`), so that file is not counted, and it counts again when it is set back to `in_progress`. Design line 605 already sets the state file of a `closeout_failed` issue to `escalated` so that the issue leaves the places in flight, and design line 608 says that an `escalated` file that waits mid-work for a person keeps today's behaviour (its entry is `stalled` when its orchestrator is down, and `--take` refuses it). Open points, all UNVERIFIED:
  - Design line 616 says "Nothing is escalated for a hand-back", so using `escalated` for the waiting step is an extension of the design. Its row-9, `stalled` and `--take` side effects (design lines 608 and 617) have not been checked.
  - Setting the file back to `in_progress` can overshoot `max_in_flight` if new work took the freed place. Two ways out: allow a one-slot overshoot, or require a free place before the flip. Neither is decided.
  - Which component runs the wake path (C-INV-2) is not decided. The poll does not (`cycle.py:993-994`).
  - Whether the restored WC-17 flow can serve as the round-2 gate (Cited fact 6) is not known.

<!-- Source: Variant 2, Mechanism bullets 3-4 and Cited facts 6-8 (design lines 612-614, 620, 1078-1081) - merged per Change #1 (new section) -->
## Loop bounds under any start rule

These bounds come from Clay's design (`docs/designs/orchestrator.md`; the line references below are to that file) and hold whether or not a person re-approves each round.

- The verb `handback` decides in a fixed order: `no_remaining` (the result has no unmet line), then `cap` (`HANDBACK_MAX` = 3 hand-backs, so at most 4 rounds; "this design's value, not measured"), then `no_progress` (the unmet lines are the same as the previous round's remaining list) (design line 612).
- Round n+1 starts only when the old worker is final: its `worker_done` was received for the active Task and Dispatch, and "absence never authorizes a release or a second worker" (design line 614).
- The re-plan is idempotent. It writes the marker `<!-- sc:issue:replan round=<n> -->`, so a rerun after a kill writes nothing twice. `--remaining` replaces only `## Fix approach` and `## Test plan`, keeps done items as `- [x]`, and leaves every other byte unchanged (design lines 1078-1080). Whether the worker keeps the done items faithfully is UNVERIFIED (U60, design line 1081).
- Restart: every step is read-then-write, and a restart resumes at the recorded step (`handback_recorded` resumes at wave 2; design line 620).

<!-- Source: Base (original, modified) - Fact 2 re-labelled and Fact 4 path corrected per Change #4 (orchestrator spot-check in base-selection.md; reviewer note in diff-analysis.md); Facts 1, 3, 5, 6, 7, 8, 9 are Base (original) -->
## Cited facts

1. D15 VERDICT section 7, OD-1 row: `quick`; "the owner has no cost baseline for a higher floor (D12 deferral)".
2. Related cost-baseline deferral at create time, not a direct source for OD-1 (the direct source is fact 3): D12 VERDICT item 6 (`debates/D12/VERDICT.md:22`): a higher tier floor at create is deferred "with a recorded reason ... (no cost baseline)".
3. Merged D15 G-2 (`debates/D15/adversarial/merged-d15-position.md`, G-2 paragraph): `--plan` takes `--depth quick|standard|deep`, default `quick`; OURS is right that `plan_tier` as designed needs a tier-to-depth table that does not exist.
4. D01 VERDICT item 5 (`debates/D01/VERDICT.md:16`): the plan must exist before the approval; a body edit after approval voids it (`src/superclaude/cli/issue_watch/predicates.py:249-259` in snapshot master, `/home/coder/.cache/ic-snap-20261120/master/src/superclaude/cli/issue_watch/predicates.py`: function `unchanged_since` returns `edited_after_approval`; the `pr-a` snapshot copy of this file has 219 lines and does not hold this code).
5. D15 R-6 (`debates/D15/VERDICT.md:32`): round 2 passes the start gate again; "no separate chat go per round".
6. D14 VERDICT: both gates stay (the start approval and the plan approval), and PR 682's deletion is reverted only if the owner says so (D15 line 252 summary); the restored plan-approval flow (WC-17) may serve as the round-2 gate (UNVERIFIED fit).
7. D15 C-INV-1 (line 140): three waiting hand-backs must not make a repo answer `coordinator_full` to new work.
8. Design `docs/designs/orchestrator.md:616` itself says the place "is never freed between rounds"; without a person step that is harmless, with one it blocks the repo while nobody works (this is the defect C-INV-1 closes).
9. Design `docs/designs/orchestrator.md:612`: `HANDBACK_MAX` = 3 is "this design's value, not measured".

<!-- Source: Base (original, modified) - first bullet replaced and last bullet appended per Change #2 (from Variant 2, goal G6 and design lines 60, 618); the second, third and fourth bullets are Base (original) -->
## What it costs

- `quick` runs the cheapest planner, the opposite of Clay's goal G6 ("stronger models plan", design line 60). A repo can set a higher `plan_depth` to get that lever back, so G6 is kept as an option and not as the default.
- Option (a) costs one person step per round. Rounds are capped at 4 (`1 + HANDBACK_MAX`).
- Needs C-INV-2: something must wake the coordinator after re-approval, because the poll never wakes an acknowledged entry (`cycle.py:993-994`).
- A repo set to `deep` runs the most expensive planner up to 4 times per issue, because the wave-2 re-plan passes the same depth (design line 618). No cost baseline exists (D12).

<!-- Source: Base (original, modified) - four risk lines appended per Change #6 (from diff-analysis.md A-001 to A-004 and the debate transcript); the first three bullets are Base (original) -->
## What it risks

- A weak plan at `quick` is caught only if the person reads it; the check passes any filled-in text.
- Excluding the waiting step from the count means an unbounded pile of waiting issues, each cheap but visible; no expiry means stale waiting issues. Mitigated by a visible reason and a later expiry.
- Reuse of the restored WC-17 as the round-2 gate is UNVERIFIED.
- No measurement of plan quality or cost per depth exists (A-001). Impact: neither `quick` nor `deep` is evidenced as the better default, so OD-1 could be wrong in either direction. Mitigation: the per-repo `plan_depth` key lets the owner change the depth for one repo, and the person's approval stays the quality gate.
- Hand-backs are assumed to be rare (A-002), and `HANDBACK_MAX` = 3 is unmeasured. Impact: if hand-backs are common, waiting issues pile up and the expiry in OD-13 is needed sooner. Mitigation: the visible waiting reason now (a waiting pile is visible, a counted pile would block the repo) and an expiry later.
- A login-based approval is weak against an agent on the same login (A-003; accepted risk L-1 in D01; the orchestrator shares Clay's login, ruling 11, design lines 111 and 488). Impact: the approval is a recorded step, not proof that a person said yes, so option (a) in OD-2 is a weaker gate than it looks. Mitigation: it still forces a visible human step in each round, and the owner accepted L-1.
- The counting code (`route.in_flight`) is cited from PR 686 (snapshot `pr-a`), and D14 says PR 686 is adapted in place and its `repos.py` does not land (A-004). Whether `route.py` survives that adaptation is UNVERIFIED. Impact: how the exclusion in OD-13 is implemented depends on it. Mitigation: the exclusion is a status choice (`escalated`) and needs no new counting code, though the carrier is UNVERIFIED (see the fourth Mechanism bullet).

<!-- Source: Base (original) -->
## What it gets right

- Keeps a human between plan edit and implementation, which is the owner's recorded line (R19, R22, D01).
- Does not invent a second mechanism (no `handback_awaiting_go`, no `answer-check` per round); the start gate decides.
- Matches existing counting rules: only live work holds a place.
