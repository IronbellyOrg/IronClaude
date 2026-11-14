# Proposal A: name no owner yet; hold the watcher's first live test

## Answer

Do not name an owner or accept the 6-a-day pattern now. The watcher worktree is not created, the runbook step that names its owner is not written, and the first live test waits until you decide how watcher sessions are owned and cleaned up.

## What happens next if the owner picks it

- The ledger records "Q20: held" with the date; the spec's default applies (merged-requirements.md line 547).
- WA-03 (runbook step 1.3a) is not shipped; WA-04 (FU-1, the first live test) does not run; #450 edit 4 is omitted from the single #450 edit set and the omission is recorded (WA-02 item 7, line 304).
- WA-05 (enable the watcher's schedule) cannot start, since it waits on FU-1 (line 307).
- The question is asked again together with a decision on closing or reaping watcher sessions, which nothing does today (round2-rebuttal-V2.md line 91).

## What it unlocks

- No session is started that no coordinator owns and nothing closes; the risk of a worktree filling with open sessions does not arise.
- Time to decide the cleanup rule first, so the owner answer and the cleanup answer are made together.
- The other #450 edits still post (the set posts once without edit 4).

## What it costs or risks

- The watcher rollout stops at its first live test; #450 cannot progress, and the questions FU-1 is meant to settle (does a launch create a Run, what the session rows hold: D-A and D-B in the source debate) stay open.
- Q21 (labelling machine-started sessions) also waits, since it needs FU-1's results (line 548).
- A deferred answer with no trigger may stall the watcher indefinitely.

## What stays unresolved

- Who owns the watcher worktree's agent.
- Whether up to 6 open, coordinator-less sessions a day are acceptable.
