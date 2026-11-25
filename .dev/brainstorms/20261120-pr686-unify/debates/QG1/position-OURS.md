# QG1 position paper: OURS (the owner's line)

Topic: planning and hand-back. Sub-questions OD-1 (default plan depth), OD-2 (how hand-back round 2 starts), OD-13 (a hand-back waiting for re-approval versus the in-flight count). Source of the answers: D15 VERDICT section 7 (`/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D15/VERDICT.md`, lines 150-166) and the merged D15 position, section (h).

## Claim

1. OD-1: the default `plan_depth` is `quick` (the `--plan` default; equal to leaving the key unset).
2. OD-2: round 2 and later re-plan the issue body and the person re-applies the approval (option a). No separate chat go per round.
3. OD-13: an issue that waits for that re-approval is NOT counted in `max_in_flight`; show it as a visible waiting reason; add an expiry later only if waiting issues pile up.

## Mechanism

- The plan call is `/sc:issue --plan <N> --depth <d>`. The depth picks the worker: quick `issue-worker-t3`, standard `issue-worker-t2`, deep `issue-worker-t1` (D12/D15 G-2, citing PR P `refs/plan.md:56-60`). With no key the call runs `quick`.
- The plan check (`plan_check`, `hold.py:122-143` in PR 686) proves that three headings are filled in. It proves presence, not quality. A person's approval is the quality gate (D01 verdict, Strongest points 1; D15 OD-1 row).
- A re-plan edits the issue body. Any body edit after the approval voids it (`pr-a/src/superclaude/cli/issue_watch/predicates.py:249-259`, D01 item 5). So round 2 must pass the start gate again; "re-plan then re-approve" is the order D01 item 5 already requires ("the plan must exist before the approval").
- A waiting issue has no worker running. `route.in_flight` (`pr-a/.../route.py:379-426`) counts a state file only while it is `in_progress`, a poll entry while `pending`/`woken`/`unknown`, and an open plan request; `done`, `skipped`, `failed`, `escalated` do not count. A waiting step modeled as not-in-progress follows the same principle: only live work holds a place.

## Cited facts

1. D15 VERDICT section 7, OD-1 row: `quick`; "the owner has no cost baseline for a higher floor (D12 deferral)".
2. D12 VERDICT item 6 (`debates/D12/VERDICT.md:22`): a higher tier floor at create is deferred "with a recorded reason ... (no cost baseline)".
3. Merged D15 G-2 (`debates/D15/adversarial/merged-d15-position.md`, G-2 paragraph): `--plan` takes `--depth quick|standard|deep`, default `quick`; OURS is right that `plan_tier` as designed needs a tier-to-depth table that does not exist.
4. D01 VERDICT item 5 (`debates/D01/VERDICT.md:16`): the plan must exist before the approval; a body edit after approval voids it (`predicates.py:249-259`).
5. D15 R-6 (`debates/D15/VERDICT.md:32`): round 2 passes the start gate again; "no separate chat go per round".
6. D14 VERDICT: both gates stay (the start approval and the plan approval), and PR 682's deletion is reverted only if the owner says so (D15 line 252 summary); the restored plan-approval flow (WC-17) may serve as the round-2 gate (UNVERIFIED fit).
7. D15 C-INV-1 (line 140): three waiting hand-backs must not make a repo answer `coordinator_full` to new work.
8. Design `docs/designs/orchestrator.md:616` itself says the place "is never freed between rounds"; without a person step that is harmless, with one it blocks the repo while nobody works (this is the defect C-INV-1 closes).
9. Design `docs/designs/orchestrator.md:612`: `HANDBACK_MAX` = 3 is "this design's value, not measured".

## What it costs

- `quick` runs the cheapest planner, the opposite of Clay's goal G6 ("stronger models plan", design line 60).
- Option (a) costs one person step per round. Rounds are capped at 4 (`1 + HANDBACK_MAX`).
- Needs C-INV-2: something must wake the coordinator after re-approval, because the poll never wakes an acknowledged entry (`cycle.py:993-994`).

## What it risks

- A weak plan at `quick` is caught only if the person reads it; the check passes any filled-in text.
- Excluding the waiting step from the count means an unbounded pile of waiting issues, each cheap but visible; no expiry means stale waiting issues. Mitigated by a visible reason and a later expiry.
- Reuse of the restored WC-17 as the round-2 gate is UNVERIFIED.

## What it gets right

- Keeps a human between plan edit and implementation, which is the owner's recorded line (R19, R22, D01).
- Does not invent a second mechanism (no `handback_awaiting_go`, no `answer-check` per round); the start gate decides.
- Matches existing counting rules: only live work holds a place.
