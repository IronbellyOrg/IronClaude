# Proposal A: a supervised worker builds the change; then the coordinator launches a separate PR session in the same worktree

## Answer

For each PR item, a supervised worker (started with `worker-start`) makes and tests the change and stops at `worker_done`. After the coordinator admits that result and the worker's session has ended, the coordinator launches one ordinary top-level PR session in the same worktree with `orca agent launch`; that session commits named paths, runs `/sc:pr-submit --monitor 3` for that one PR under its grant row, and closes when the PR merges. The owner designates this arrangement once and confirms that Orca allows the second launch.

## What happens next if the owner picks it

1. Before the first PR item, the owner (or a session the owner directs) checks once that Orca accepts a second, sequential `agent launch` in a worktree created by `worker-start` after the worker has ended (UNVERIFIED today, merged-requirements.md line 964). If it does not, the owner is asked again; proposal C's route is the natural fallback.
2. Per item: worker runs, `worker_done` admitted; the coordinator shows the person the diff they have not seen (`WORKER-CONTRACT.md:244`); the ledger gets `GRANT(<item>,pr-submit)` listing every write the tool makes.
3. The coordinator runs `orca agent launch` in that worktree with a prompt naming the item, the grant row and `/sc:pr-submit --monitor 3 --head <branch> ...`.
4. The PR session stages and commits named paths (6.4 rule 14), opens the PR on `IronbellyOrg/IronClaude`, checks the URL, monitors reviews, fixes confirmed findings, and stops at merge (it never merges).
5. The coordinator tracks the PR with `gh pr view <N> --repo IronbellyOrg/IronClaude` at its wakes.

## What it unlocks

- All nine PR items (SW-07, SW-08, SW-10, SW-14, OB-06, OB-07, WA-01, WA-03, XC-07) can open PRs in W1 and later waves.
- Keeps the supervised-worker model for the code itself: a brief, a contract, heartbeats and an admitted `worker_done`, with the coordinator's review between building and publishing.
- Respects every rule: no worker runs pr-submit (`WORKER-CONTRACT.md:23,243`), the coordinator never runs it (line 962), and one worktree never has two live agents (line 951).

## What it costs or risks

- Rests on an UNVERIFIED Orca behaviour (a second launch in a `worker-start` worktree); if Orca refuses, the whole route needs replacing.
- Two agents per PR item (worker, then PR session) and a handoff step for the coordinator.
- The PR session starts cold: it did not write the change, so fixing review findings means re-reading it.
- `orca agent launch` by the coordinator is a session start the coordinator owns; it must track and close each one.

## What stays unresolved

- Whether Orca permits the second launch.
- Q32 (whether workers may make a local commit) changes who commits but not who runs pr-submit.
