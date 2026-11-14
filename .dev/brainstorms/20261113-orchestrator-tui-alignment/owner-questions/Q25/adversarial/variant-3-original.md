# Proposal C: no worker for PR items; one top-level agent per PR item builds the change and opens its own PR

## Answer

For each item that ends in a PR, the coordinator creates one Orca worktree with its own top-level agent (`orca worktree create --base-branch origin/master --agent claude --prompt "<item brief>"`). That agent implements and tests the change, commits named paths, and opens and monitors its PR with `/sc:pr-submit --monitor 3`. Supervised workers (`worker-start`) are used only for items that end in a report and need no push.

## What happens next if the owner picks it

1. The ledger marks each of the nine PR items as "top-level agent", not "worker": SW-07, SW-08, SW-10, SW-14, OB-06, OB-07, WA-01, WA-03, XC-07.
2. Per item: the owner approves `GRANT(<item>,pr-submit)`; the coordinator creates the worktree with `--agent` and a prompt containing the item's acceptance criteria and the grant row. One agent per worktree, created once, so the "never both" rule holds by construction (merged-requirements.md line 951).
3. The agent builds and tests, then, before pushing, stops and shows the person its diff (`WORKER-CONTRACT.md:244`), then runs `/sc:pr-submit --monitor 3` on `IronbellyOrg/IronClaude`, checks the URL, and stops at merge.
4. The coordinator tracks each agent by `gh pr view <N> --repo IronbellyOrg/IronClaude` and Orca idle notices at its wakes, not by `worker_done` (round3-invariants-V2.md:53 item (4)).

## What it unlocks

- No dependence on the UNVERIFIED second `agent launch` in a `worker-start` worktree: Orca's documented route (`worktree create --agent`) is used once per item.
- The agent that wrote the change also answers its reviews, so fixes come from the author, not a cold reader.
- One agent per PR item instead of two; simpler for the coordinator.
- It is the route the Round 3 advocate called "the only route the worker contract and the pr-submit skill both allow while D3 keeps pr-submit off workers" (round3-invariants-V2.md:53, confidence 85).

## What it costs or risks

- Loses the supervised-worker controls for the code: no worker brief guard, no heartbeats, no `worker_done` contract for the coordinator to admit before publishing. The check moves to "show the person the diff before pushing", which the agent itself must honour.
- A top-level agent is not bound by the worker contract's limits; its permissions on this host are those of any session (permission checks off, INV-011), so its prompt and grant row are the only bounds.
- The spec's work-item rows say "a supervised worker makes and tests the change to `worker_done`; the PR session opens the PR"; each of the nine rows must be reworded.

## What stays unresolved

- How the coordinator detects that an unsupervised agent has stalled or gone off-brief without `worker_done` and heartbeats.
