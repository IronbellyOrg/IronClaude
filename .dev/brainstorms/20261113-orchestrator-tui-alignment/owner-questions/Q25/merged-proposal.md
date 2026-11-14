<!-- Provenance: Base: Variant 1 (proposal-A) -->
<!-- Merge date: 2026-11-14 -->
<!-- Plan: adversarial/refactor-plan.md (4 planned changes applied; 2 rejected by the plan) -->
<!-- Executor: merge-executor -->

# Proposal A: a supervised worker builds the change; then the coordinator launches a separate PR session in the same worktree

## Answer

<!-- Source: Base (Variant 1); last sentence of the PR session description modified by Change 2 (Variant 2, C-004 / A-001) -->
For each PR item, a supervised worker (started with `worker-start`) makes and tests the change and stops at `worker_done`. After the coordinator admits that result and the worker's session has ended, the coordinator launches one ordinary top-level PR session in the same worktree with `orca agent launch`; that session commits named paths, waits for the person's go in its own conversation before its first push, runs `/sc:pr-submit --monitor 3` for that one PR under its grant row, and closes when the PR merges. The owner designates this arrangement once and confirms that Orca allows the second launch.

## What happens next if the owner picks it

<!-- Source: Base (Variant 1) step 1, fallback replaced by Change 1 (Variant 3; Variant 3 advocate Concession 2) -->
1. Before the first PR item, the owner (or a session the owner directs) checks once that Orca accepts a second, sequential `agent launch` in a worktree created by `worker-start` after the worker has ended (UNVERIFIED today, merged-requirements.md line 964). If it does not, the owner is asked again, and the fallback is: PR items switch to one top-level agent per item, created with `orca worktree create --base-branch origin/master --agent claude --prompt "<item brief>"` (the spec's own named alternative, merged-requirements.md line 552). On that route the coordinator applies a deadline per item: if no PR exists by then, it makes a read-only check of the worktree and asks the owner (Orca idle notices for such agents are UNVERIFIED).
<!-- Source: Base (Variant 1) step 2, grant row contents added by Change 3 (all three advocates, A-001; Variant 1 advocate Concession 3); coordinator's showing kept per Change 2 -->
2. Per item: worker runs, `worker_done` admitted; the coordinator shows the person the diff they have not seen (`WORKER-CONTRACT.md:244`); the ledger gets `GRANT(<item>,pr-submit)` listing every write the tool makes: the commit of the worker's changes (named paths), PR create, the "augment review" re-trigger comment, review-fix commits and pushes made without asking at `--monitor 3`, and replies and resolves.
<!-- Source: Base (Variant 1) step 3, unchanged -->
3. The coordinator runs `orca agent launch` in that worktree with a prompt naming the item, the grant row and `/sc:pr-submit --monitor 3 --head <branch> ...`.
<!-- Source: Base (Variant 1) step 4; handoff-file read added by Change 4 (Variant 1 advocate Concession 2); person's go added by Change 2 (Variant 2, C-004 / A-001) -->
4. The PR session reads the worker's contract and handoff files, then stages and commits named paths (6.4 rule 14). Before the first push it shows the person the diff and waits for the person's go in its own conversation, which meets `WORKER-CONTRACT.md:240`'s "instruction in its live conversation"; the coordinator's earlier showing (`:244`) stays. It then opens the PR on `IronbellyOrg/IronClaude`, checks the URL, monitors reviews, fixes confirmed findings, and stops at merge (it never merges).
<!-- Source: Base (Variant 1) step 5, unchanged -->
5. The coordinator tracks the PR with `gh pr view <N> --repo IronbellyOrg/IronClaude` at its wakes.

## What it unlocks

<!-- Source: Base (Variant 1); second bullet qualified for consistency with Change 1; third bullet qualified for consistency with Change 3 -->
- All nine PR items (SW-07, SW-08, SW-10, SW-14, OB-06, OB-07, WA-01, WA-03, XC-07) can open PRs in W1 and later waves.
- On the primary route (not the fallback in step 1), keeps the supervised-worker model for the code itself: a brief, a contract, heartbeats and an admitted `worker_done`, with the coordinator's review between building and publishing.
- Respects every rule once the D3 sentence under "What it costs or risks" is added: no worker runs pr-submit (`WORKER-CONTRACT.md:23,243`), the coordinator never runs it (line 962), and one worktree never has two live agents (line 951).

## What it costs or risks

<!-- Source: Base (Variant 1); first bullet updated for consistency with Change 1; third bullet extended by Change 4; last two bullets added by Change 3 and Change 2 -->
- Rests on an UNVERIFIED Orca behaviour (a second launch in a `worker-start` worktree); if Orca refuses, the whole route is replaced by the fallback in step 1, which drops the brief guard, heartbeats and admitted `worker_done` for the code.
- Two agents per PR item (worker, then PR session) and a handoff step for the coordinator.
- The PR session starts cold: it did not write the change, so fixing review findings means re-reading it. Reading the worker's contract and handoff files (WC-15, `WORKER-CONTRACT.md:64`) before opening the PR reduces this cost but does not remove it.
- `orca agent launch` by the coordinator is a session start the coordinator owns; it must track and close each one.
<!-- Source: Change 3 (all three advocates, A-001; Variant 1 advocate Concession 3) -->
- Needs one sentence in the D3 text (or a contract note) stating that the actions listed in the `GRANT(<item>,pr-submit)` row are outward actions delegated to the PR session. Without it, `WORKER-CONTRACT.md:240,245` and 6.4 rule 14 (merged-requirements.md line 987) disagree on who commits the worker's changes.
<!-- Source: Change 2 (Variant 2, C-004 / A-001); Variant 2 advocate Concession 3; Variant 3 advocate weakness 3 -->
- The person's go is needed once per PR, in the PR session, before its first push. Later review-fix pushes at `--monitor 3` are made without asking, as the grant row states.

## What stays unresolved

<!-- Source: Base (Variant 1); first bullet updated and second bullet added by Change 1 (Variant 3; Variant 3 advocate Concession 2) -->
- Whether Orca permits the second launch; if it does not, the fallback in step 1 applies.
- Whether Orca sends idle notices for agents created with `orca worktree create --agent` (UNVERIFIED); the fallback's per-item deadline does not depend on them.
- Q32 (whether workers may make a local commit) changes who commits but not who runs pr-submit.
