# Proposal C: the program's coordinator session creates and owns the watcher worktree's agent and reviews watcher sessions

## Answer

The person-opened coordinator session of this program creates the watcher worktree with an agent, so it owns that agent, and it reviews watcher sessions in its recurring checks. Watcher sessions stay outside Orca Runs (they are not adopted as workers), but they are no longer "never owned by a coordinator": the coordinator is their named owner.

## What happens next if the owner picks it

- The ledger records "Q20: the coordinator session owns the issue-watch agent and reviews watcher sessions" with the date.
- WA-03's runbook step 1.3a names the coordinator session (not a person) as the creator: the coordinator runs `orca worktree create --name issue-watch --agent claude --prompt "<task>"`. The project rule allows this: "The eligible session that creates a worktree owns its agent(s)" (ROOT/CLAUDE.md, Git Workflow section).
- The coordinator's recurring check (the owner's 2026-11-05 order, Q31) adds a look at the `issue-watch` worktree and its open sessions; closing them stays a person's action unless you grant otherwise.
- WA-04 (FU-1) runs in that worktree when its other preconditions hold.

## What it unlocks

- One accountable session that is already watching the program, instead of a person who must remember to look.
- Fits the plan's longer direction, in which a watcher eventually hands approved issues to an orchestrator (WA-07, deferred and unbuilt, merged-requirements.md line 309).
- A single place to report open watcher sessions to you.

## What it costs or risks

- The coordinator cannot see these sessions well: they have no Orca Run, so its sweep shows them only as transcript rows marked "could not determine" (ADJ line 242); its "review" is mostly listing.
- Mixes two designs the source debate kept apart: the recommended action was to state that watcher sessions are never coordinator-owned (round2-rebuttal-V2.md line 93). Whether a coordinator may adopt them is UNVERIFIED.
- A coordinator session ends and is resumed; ownership tied to a session is less stable than ownership tied to a person.
- The watcher-to-orchestrator handoff does not exist; this answer only changes who owns and looks, not how sessions start.

## What stays unresolved

- What the coordinator may do about a watcher session beyond reporting it.
- Who closes or reaps watcher sessions.
