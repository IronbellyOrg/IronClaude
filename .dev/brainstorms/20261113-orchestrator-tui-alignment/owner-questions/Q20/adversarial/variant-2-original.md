# Proposal B: a named person owns the agent; watcher sessions stay person-reviewed top-level sessions

## Answer

A person you name creates the watcher worktree with an agent and owns that agent. Yes, that one worktree may hold up to 6 watcher sessions a day; they are ordinary top-level sessions reviewed by that person, never owned by a coordinator.

## What happens next if the owner picks it

- The ledger records "Q20: <person> owns the issue-watch agent; watcher sessions are person-reviewed top-level sessions, never coordinator-owned" with the date.
- WA-03 ships runbook step 1.3a: that person runs `orca worktree create --name issue-watch --agent claude --prompt "<task>"` and the runbook names them as the agent's owner; it also adds that `reset --forfeit-guarantee` on an `unknown` entry first requires checking Orca for a live session in that worktree (merged-requirements.md line 305).
- #450 edit 4 (step 1.3a) joins the single #450 edit set (WA-02, line 304).
- WA-04 (FU-1) can run in the `issue-watch` worktree once its other preconditions hold (Q2, its written permission acceptance, live Orca) (line 306).
- The runbook notes that every watcher session writes `.dev/issues/<N>/` in that worktree, so the sweep will show it as uncommitted, not removable (variant-2-original.md line 48).

## What it unlocks

- The watcher's first live test and then its schedule (WA-05).
- Matches the watcher's own design: a plain process, never an Orca worker, starting ordinary sessions (round2-rebuttal-V2.md line 91), and Orca's rule that a worktree's creator owns its agent.
- Keeps watcher sessions out of the coordinator's contract: WC-13 does not apply to them and no coordinator has to adopt sessions it did not start.

## What it costs or risks

- Up to 6 sessions a day accumulate in one worktree and "nothing closes or reaps those sessions" (round2-rebuttal-V2.md line 91); the named person must close them by hand.
- These sessions have no Orca Run, so the observer cannot see them and the sweep shows them only as transcript rows marked "could not determine" (ADJ line 242), until Q21's label exists after FU-1.
- The person must actually review each session; if they do not, open sessions with permission checks off (the host's mode, a Q2 concern) sit unattended.

## What stays unresolved

- Who closes or reaps watcher sessions, and when.
- Whether a later coordinator should ever adopt them (left as "never" by this answer).
