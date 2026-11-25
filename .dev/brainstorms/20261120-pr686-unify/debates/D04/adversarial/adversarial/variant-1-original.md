# Position OURS (D04: claim level and grants)

Question: should the watcher always claim at level none with a standing `grants` list, or should the issue's Pipeline field choose the launch level, with one grant row per issue?

## Claim

The person who owns the issue decides, per issue, how far automation goes. The Project field `Pipeline` (None, Worktree, Full, Full Submit) is that decision. The watcher reads it and the coordinator launches the claim at that level (`/sc:issue --claim <N> --pipeline <none|worktree|full>`, with `--submit` for Full Submit). Every outward write the coordinator makes for an issue needs that issue's own grant row. The Pipeline field is the owner's only per-issue throttle between "claim and stop" and "go all the way to a pull request".

## Mechanism

1. Status picks the command (Research, Spec, Plan, Debug) and Pipeline picks how far it goes (R23, requirements.md line 47). Board value to flag: None = `--pipeline none`, Worktree = `--pipeline worktree`, Full = `--pipeline full`, Full Submit = `--pipeline full --submit`; an empty Pipeline means None (R25, line 51).
2. The claim records the level outside the worktree in `~/.claude/state/launch-level/pending/<nonce>`; the launch-level guard (hook, #394 closed) reads it and enforces the stop. The agent cannot edit it. If the guard is missing the claim refuses with `W-ENFORCEMENT-ABSENT` and starts no agent (`docs/designs/sc-issue-claim-pipeline-flag.md` section 6, lines 117-135).
3. Full Submit commits, pushes a feature branch and runs `/sc:pr-submit --monitor 3`; no level ever merges (same doc, lines 19-26). The owner's Pipeline value plus the `Approved` field is the person's go for that one issue's push (R25; `docs/designs/issue-watcher-status-pipelines.md:83` in the worktree `claim-handoff-planb`).
4. The coordinator, not the agent, makes the GitHub writes, and only under that issue's grant row (Decision 8, owner-answers.md line 130; pre-PR-682 `WORKER-CONTRACT.md:300` "Never ... post an issue write without that issue's grant row").
5. A closed ship gate keeps this safe today: `GOVERNED_LEVELS_ALLOWED = False` (`src/superclaude/cli/issue_watch/launch.py:48`, branch `ironbelly/issue-watcher-zero-setup-plan`; R33, requirements.md line 59). Only Pipeline None launches until a reviewed commit flips it.

## Cited facts

1. Owner decisions R23 and R25 dated 2026-11-18 and 2026-11-19 ("launch levels widened"), requirements.md lines 47 and 51 (worktree `claim-handoff-planb`). The board field exists: "read 2026-11-18" (same line 47).
2. The levels are built and merged, not just planned: `--pipeline` and `--submit` (PR 425, the flag design above), the launch-level guard (issue 394, closed 2026-11-17), the L2 pre-push layer (PR 441).
3. The guard does not see a `worker-start` worker. Clay's own design says so: DQ7 (`docs/designs/orchestrator.md:117`) "these workers run with no L1 guard and no L2 pre-push hook", `master` is "not protected" (`protected: false`, D:285) and K12 records the risk. A level chosen per issue, with the guard behind it, is the control that exists today.
4. Clay's design has no per-issue stop point between nothing and everything. Assignment is the only trigger (R1, D:73); the orchestrator then claims, plans, starts the worker, merges and closes (D:519, Will Do). The only per-issue brake I found is the label `hold:backlog` (D:445). UNVERIFIED that no other exists: I searched `orchestrator.md` for "Pipeline field" and found none.
5. Decision 8 (2026-11-14, owner-answers.md line 130): "one grant row per pipeline issue, created when the issue is claimed, listing the plan reply, marker comment, mention, label and Status writes". It is a per-issue, listed, bounded authorisation.
6. A standing grant list includes `pr.merge` and `issue.close` (D:116, D:291) for every issue of every listed repo. `WORKER-CONTRACT.md:239-246` says the coordinator acts outward only when the person's instruction names the action and pushes worker commits only on the person's go.
7. The list that guards the standing grants sits in a file the orchestrator itself edits. Design D:688: "ours are inside it and are guarded by the verb and by a test". That is a rule, not a permission boundary. A per-issue row written from the owner's chat has no such gap.
8. The ship gate is evidence of care, not recklessness. The observations that must pass before a governed level runs (`tests/hooks/test_launch_level_observations.py`, 12 items `OB-H1` 1-9, `OB-H2`, `OB-H3`, `OB-CTX`) are listed and skipped (master, `_PENDING`); the claim doc (lines 4 and 92 of `SKILL.md`) forbids a governed claim on a real issue before they pass.

## What it costs

- No governed level can run today: 12 observations are skipped and issue 442 (live observations) is open. Until then OURS behaves exactly like CLAY at the claim step.
- A grant row per issue needs a person at each issue and two sessions per approval. The owner accepted that "for now" only (Q36, owner-answers.md line 185).
- A launched agent at Worktree, Full or Full Submit is outside the Orca Run mailbox; it reports through `.dev/issues/<N>/result.md` and the coordinator notices it through the sweep (R24, line 50). Supervision is weaker than for a `worker-start` worker.
- The Status x Pipeline matrix is large (R23, R32 P-8, R33, R34): each pair needs a rule on whether the command runs, is limited or is refused.
- The grant row as written ("the grant row is written by the owner, not by an agent", owner-answers.md line 130) sits badly with the owner's later order that approvals are given in chat and never written into files (memory `approvals-through-chat-never-files`, 2026-11-17; the D2 narrowing in PR 585 covered Rulings only, owner-answers.md line 285).

## What it risks

- Dead weight: a Pipeline field and a Project read that nothing can use until the gate opens.
- Delay: every issue waits for a person.
- Divergence: if the claim is none-only in the live path and level-based in the docs, the two drift.

## What it gets right

- The decision about how far automation goes stays with the person who knows the issue, per issue, in the place the owner already works (the board).
- Level and guard are enforced by something the agent cannot edit.
- Grants are narrow, listed and per issue. Merge and close are never granted in bulk.
- The gate is closed by default: the safe state is also the current state.
