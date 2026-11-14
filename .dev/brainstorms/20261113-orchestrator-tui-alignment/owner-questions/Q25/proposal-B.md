# Proposal B: the owner opens each PR session personally, when ready

## Answer

No program session starts a PR session. When a worker's change is admitted, the coordinator records "ready for PR" in the ledger and tells the owner; the owner personally opens an ordinary Claude session in that worktree, reviews the change, and runs `/sc:pr-submit --monitor 3` there (or asks that session to). Each PR session is person-opened, like the coordinator.

## What happens next if the owner picks it

1. Per item: worker runs, `worker_done` admitted, worker session ended; the coordinator writes a "ready for PR" ledger row with the worktree path, branch, changed paths, the suggested `/sc:pr-submit --monitor 3 --head <branch> --title ... --body ...` line and the grant row to approve.
2. The owner opens a Claude session in that worktree (a person-opened top-level session, the same kind as the coordinator), looks at the diff, approves the grant row, and runs the command.
3. The session commits named paths, opens the PR on `IronbellyOrg/IronClaude`, monitors reviews and stops at merge.
4. The coordinator tracks the PR with `gh pr view <N> --repo IronbellyOrg/IronClaude`.

## What it unlocks

- No dependence on whether Orca allows a second `agent launch` in a `worker-start` worktree (UNVERIFIED, merged-requirements.md line 964): a person opening a session is the ordinary case.
- The person sees every change before it is published by construction, which is what `WORKER-CONTRACT.md:244` requires ("shows them to the person and pushes only on the person's go").
- The strongest reading of "an ordinary top-level session" (`WORKER-CONTRACT.md:243`) and of the pr-submit skill's "MUST run in the main orchestrating session" (`SKILL.md:47`).
- The coordinator never starts sessions that publish code.

## What it costs or risks

- Owner time: one session to open and attend per PR, nine PR items in this program. "Owner latency is the real schedule" (merged-requirements.md line 523); PRs wait for the owner.
- The pr-submit poll loop is attended; the owner's session stays open until reviews land.
- Lanes stall whenever the owner is away, the same effect as the default for that period.

## What stays unresolved

- Whether the owner wants to delegate later (switching to proposal A or C) once a few PRs have gone through.
