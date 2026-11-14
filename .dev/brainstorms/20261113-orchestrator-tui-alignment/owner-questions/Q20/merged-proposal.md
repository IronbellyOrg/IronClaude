<!-- Provenance: This document was produced by /sc:adversarial -->
<!-- Base: Variant 2 (proposal-B) -->
<!-- Merge date: 2026-11-14 -->

<!-- Source: Base (original) -->
# Proposal B: a named person owns the agent; watcher sessions stay person-reviewed top-level sessions

<!-- Source: Base (original, modified); reason: day-cap wording replaced, merged per Change #2 -->
## Answer

A person you name creates the watcher worktree with an agent and owns that agent. Yes, that one worktree may hold up to the confirmed day cap of watcher sessions a day (default 6); they are ordinary top-level sessions reviewed by that person, never owned by a coordinator.

<!-- Source: Base (original) -->
## What happens next if the owner picks it

<!-- Source: Base (original, modified); reason: review cadence and absence fallback appended from advocate findings (round1-advocate-2.md, round1-advocate-3.md), merged per Change #3 -->
- The ledger records "Q20: <person> owns the issue-watch agent; watcher sessions are person-reviewed top-level sessions, never coordinator-owned" with the date. The ledger also records how often that person looks at the open sessions, and either a named substitute or the rule that the schedule is disabled while the owner is away.
<!-- Source: Base (original) -->
- WA-03 ships runbook step 1.3a: that person runs `orca worktree create --name issue-watch --agent claude --prompt "<task>"` and the runbook names them as the agent's owner; it also adds that `reset --forfeit-guarantee` on an `unknown` entry first requires checking Orca for a live session in that worktree (merged-requirements.md line 305).
- #450 edit 4 (step 1.3a) joins the single #450 edit set (WA-02, line 304).
- WA-04 (FU-1) can run in the `issue-watch` worktree once its other preconditions hold (Q2, its written permission acceptance, live Orca) (line 306).
- The runbook notes that every watcher session writes `.dev/issues/<N>/` in that worktree, so the sweep will show it as uncommitted, not removable (variant-2-original.md line 48).
<!-- Source: Variant 1 (proposal-A) "What happens next" bullet 4 (U-001) with advocate findings, merged per Change #1 -->
- Before the watcher's schedule is enabled (WA-05), a written rule says who closes watcher sessions and by when. FU-1 itself launches one session on one test issue (merged-requirements.md line 306), so it does not wait for that rule.
<!-- Source: Advocate findings A-001 (round1-advocate-1.md, round1-advocate-2.md), merged per Change #2 -->
- The day cap is a code constant (`DAY_CAP = 6`) that the design lists as a proposal for you to confirm after the shadow run; lowering it is a small code change, not a configuration edit.

<!-- Source: Base (original) -->
## What it unlocks

- The watcher's first live test and then its schedule (WA-05).
- Matches the watcher's own design: a plain process, never an Orca worker, starting ordinary sessions (round2-rebuttal-V2.md line 91), and Orca's rule that a worktree's creator owns its agent.
- Keeps watcher sessions out of the coordinator's contract: WC-13 does not apply to them and no coordinator has to adopt sessions it did not start.
<!-- Source: Variant 3 (proposal-C) "What happens next" bullet 3 (U-003), narrow form, merged per Change #5 -->
- Optionally, the coordinator's recurring check may report a read-only count of open sessions in `issue-watch`, without reading their transcripts and without owning them, so the named person gets a reminder.

<!-- Source: Base (original) -->
## What it costs or risks

<!-- Source: Base (original, modified); reason: consistency with Change #2 ("Up to 6" tied to the day cap) and consistency with Change #1 and Change #4 (the quoted "nothing closes" scoped to the watcher's design); extension from advocate 1 (round1-advocate-1.md "Strengths claimed" 3) merged per Change #4 -->
- Up to the day cap (default 6) of sessions a day accumulate in one worktree and, by the watcher's design, "nothing closes or reaps those sessions" (round2-rebuttal-V2.md line 91); the named person must close them by hand. Orca's creator rule covers the agent made when the worktree is created; the watcher starts later sessions itself, so the named person is their owner by this decision and their reviewer, not by Orca's record (whether Orca attributes them to the creator is UNVERIFIED). The runbook gives no command to end a running session; it is closed by hand in Orca.
<!-- Source: Base (original) -->
- These sessions have no Orca Run, so the observer cannot see them and the sweep shows them only as transcript rows marked "could not determine" (ADJ line 242), until Q21's label exists after FU-1.
- The person must actually review each session; if they do not, open sessions with permission checks off (the host's mode, a Q2 concern) sit unattended.

<!-- Source: Base (original) -->
## What stays unresolved

<!-- Source: Base (original, modified); reason: consistency with Change #1 (the closing rule is now required before WA-05) -->
- Who closes or reaps watcher sessions, and when; that rule must be written before the schedule is enabled (WA-05).
<!-- Source: Base (original) -->
- Whether a later coordinator should ever adopt them (left as "never" by this answer).
<!-- Source: Advocate findings A-002 (all three advocates), merged per Change #6 -->
- If Q2 keeps the default claim level, each claim also starts a second agent in its own `issue-<N>` worktree; you would also name who owns those agents. Under Q2's recommended `--pipeline none` there is no second agent.
