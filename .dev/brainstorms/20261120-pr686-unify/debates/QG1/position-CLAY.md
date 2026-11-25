# QG1 position paper: CLAY (Clay's line)

Topic: planning and hand-back. Sub-questions OD-1, OD-2, OD-13. Source: Clay's design `docs/designs/orchestrator.md` (snapshot `/home/coder/.cache/ic-snap-20261120/master/docs/designs/orchestrator.md`; line references D:nnn).

## Claim

1. OD-1: the plan call runs at a stronger depth than `quick`: the default follows `plan_tier` = `tier1b` (D:60, D:724), which implies `deep` (the merged D15 file says "the value Clay's default tier implies" is `deep`; the tier-to-depth table is in `refs/intake.md` of PR P, not on master: UNVERIFIED).
2. OD-2: a hand-back round starts without a new approval. Wave 8 hands the issue back "to the orchestrator and not to the owner"; wave 2 re-plans through `/sc:issue --plan <N> --remaining <file> --depth <d>` and the issue "re-enters the waves at wave 2 ... the same workflow" (D:610, D:615, D:618). The strongest alternative, if a gate is wanted, is option (b): leave the body alone and carry the remaining list in the handoff round block (D:619).
3. OD-13: a hand-back issue stays `in_progress` and stays counted in flight; "the place in flight is never freed between rounds" (D:616). The question of an excluded waiting step does not arise in this design because there is no waiting step.

## Mechanism

- The plan is written once by the better model, so cheaper models can build (ruling of 2026-11-19 03:09 UTC, D:722; goal G6, D:60). A weak plan multiplies cost downstream.
- Ruling 36 (D:610): "If closeout runs and finds the PR didn't finish the issue, it should escalate back to the orchestrator to initiate the work that was not done, following the same workflow." The orchestrator is the actor; the person is reached only under the escalation table of 5.6.
- The state file stays `in_progress`, so the poll counts the issue and the orchestrator does not end itself while it is in flight (D:616, 5.7 point 5). This gives a simple, restart-safe rule (`handback_recorded` resumes at wave 2, D:620).
- The loop is bounded by the verb `handback`: `cap` (HANDBACK_MAX = 3), `no_progress` (same remaining list as last round), `no_remaining` (D:612). A stop is escalated once as row 9 of 5.6 (D:617).

## Cited facts

1. D:60 (goal G6) and D:722-724: `plan_tier` default `tier1b`; "stronger models plan, cheaper models build".
2. D:1083: the plan call and the hand-back re-plan both pass `--depth <d>` from `plan_tier`; D:618 repeats it for wave 2.
3. D12 VERDICT / merged D15 G-2: `--plan` default depth is `quick`, run by `issue-worker-t3`, and "nothing picks the depth from complexity", so without a key the plan falls to the cheapest worker (a real gap that the key fills).
4. D:610 (ruling 36) and D:615: hand-back goes to the orchestrator, "not to the owner", through the same waves.
5. D:616: "The state file stays `in_progress` ... the place is never freed between rounds".
6. D:614: the old worker must be final (`worker_done` for the active Task and Dispatch) before `handback` is called; this makes the round start safe without a person.
7. D:1076-1080: `--remaining` replaces only `## Fix approach` and `## Test plan`, keeps done items, and writes one body edit; the marker `<!-- sc:issue:replan round=<n> -->` makes a rerun write nothing twice.
8. D:612: hard bounds on the loop (`cap`, `no_progress`, `no_remaining`) mean a runaway needs no human.
9. D01 VERDICT item 3 (MR-1): the owner's line itself demands that the check at the moment of start repeats the approval; Clay's wave-1 re-check covers only `hold:backlog` and `plan_check` (`orchestrator.md:488`), showing the design as written has no round-2 approval (a gap in Clay's text, not an argument for it).

## What it costs

- Under Clay's text there is no human between a re-plan and a new worker: the re-plan voids any earlier approval (`predicates.py:249-259`) and nothing replaces it. That is the cost the owner's line names.
- The counted place never frees: three hand-backs in flight block the repo (`max_in_flight` default 3) even if each loops through slow rounds.
- A `deep` default plan is the most expensive planner on every issue; no cost baseline exists (D12).

## What it risks

- Autonomous loops of up to 4 rounds with no person step (if the start gate is not repeated); a bad re-plan goes straight to a new worker.
- `--remaining` fidelity is UNVERIFIED (U60: the worker keeps done items faithfully).
- `plan_tier`-to-depth table is not on master (UNVERIFIED), so the `deep` claim rests on D15's reading.

## What it gets right

- A named, bounded, restart-safe loop (verb `handback`, reasons `cap`, `no_progress`, `no_remaining`).
- Spends the strong model where the work is planned (G6), which is a real quality lever the owner's line gives up at `quick`.
- Keeping the place counted gives one simple invariant: "in flight means someone owns it".
