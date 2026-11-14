# Proposal A: a dedicated program worktree that the owner creates through Orca, whose agent is the coordinator

## Answer

The owner creates one new Orca worktree for the program from `origin/master` (for example `orca worktree create --name orchestrator-alignment --base-branch origin/master --agent claude --prompt "<coordinator brief>"`), and the agent Orca starts in it is the coordinator; the ledger package is staged on that worktree's own new branch.

## What happens next if the owner picks it

1. The owner (a person, not a session) runs the create command, so the person owns that agent under the project rule "the eligible session that creates a worktree owns its agent(s)"; no session creates a worktree for its own use.
2. The coordinator brief points the agent at the spec, ADJ, the worker contract and section 6; the agent writes the ledger package `.dev/tasks/<program-package>/` there, on the program branch, staged and not committed.
3. XC-10 part (3) records the worktree path from `orca worktree list` and the branch; XC-09 can start once ORCA-AVAILABLE also holds.
4. The main checkout stays on `docs/409-orca-dashboard-designs` with its 21 untracked entries untouched.

## What it unlocks

- XC-09 and everything it dispatches (edge 119), without touching the main checkout's branch or its untracked work.
- A clean branch where only program files are staged, so a later "commit the ledger" request has no unrelated files around it.

## What it costs or risks

- The program's rules say a coordinator is person-opened. Whether an agent started by `--agent` counts as person-opened is UNVERIFIED (`refactor-plan.md:90`, `:618`). If it does not, the coordinator is formally a top-level agent, not a coordinator, and any rule that relies on "person-opened" (for example who may run `worker-start`) is on uncertain ground.
- Orca must be reachable to create the worktree at all; it was unreachable on 2026-11-13 (`merged-requirements.md:604`).
- One more worktree on a host that already has 19.
- The person must read the coordinator's first screen to confirm the brief loaded; a launch receipt alone is not proof (owner memory `orca-worker-resume-verify-screen.md`).

## What stays unresolved

- Whether Orca's `--agent` launch is "person-opened" for the worker contract.
- Whether the project's "Session A: Open the main checkout" guidance is a rule or an example.
