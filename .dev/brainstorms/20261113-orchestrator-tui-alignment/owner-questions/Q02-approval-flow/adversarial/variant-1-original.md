# Proposal A: every channel may start a stage, but only by winning one shared claim on a stage record

Shared terms, the stage table (S0 to S7) and the failure modes (F1 to F10) are in `00-state-machine-and-failure-modes.md` in this folder. Nothing in this proposal is built.

## Design

Each channel keeps the right to start the next stage itself: the coordinator (for an approval typed in Orca or, later, in the TUI), a new stage handler in the watcher (for an approval made on GitHub), and the governed agent (for a person who types the approval in the agent's own session). None of them may start anything until it has won one exclusive claim on a **stage record** keyed by (issue, stage, plan version):

1. **Local claim.** A new store file `stage.json` next to the watcher's `dispatch.json`, with the same discipline the watcher already uses for launches: take the file lock, look for the key, and if absent write the entry as `pending` and fsync it before doing anything else (the watcher's write-ahead rule, `issue-watcher.md` 7.4 transition T-4). A small CLI helper does this so all three actors share one implementation.
2. **Public claim.** Right after the local write, the winner posts one issue comment carrying a marker, `<!-- sc:stage:approved issue=<N> plan=<sha256> token=<id> -->`. This is evidence for other hosts and for people; GitHub comments have no conditional write, so it is not a lock.
3. **Start.** Only then does the winner tell the agent to proceed (the coordinator and the watcher by typing one line into the waiting agent session; the agent by continuing).
4. **Losers.** Any actor that finds the key in `stage.json`, or a marker with the same plan version on the issue, does nothing and logs `already_started`.
5. **Echo suppression.** A GitHub change (Status move, label) that matches a marker the actors wrote themselves is ignored as an echo.
6. **Reconciliation by level.** On every cycle each actor compares the levels (GitHub Status and labels, marker comments, `stage.json`, the agent's state) and acts only when they disagree and it holds the record for that key.

**Invariant.** For each (issue, stage, plan version), at most one `stage.json` entry leaves `pending`, and no actor starts a stage before that entry is fsynced. The guarantee has the same scope as the watcher's own: one intact store per host and login.

## How an approval flows

**GitHub channel.**
1. The plan is posted as an issue reply with its plan version; Status goes to a review value; the assignee is mentioned (who does this is the coordinator, per the owner).
2. The assignee approves by applying an approval label for that stage (the actor of a label event is readable; the actor of a Project Status move is not read by any code today) and moves the Status as the visible sign.
3. The watcher's new stage handler sees it on its next 5-minute cycle, checks the label actor against the approvers file and that the plan comment was not edited after the label, takes the local claim, posts the marker, and types the approval line into the agent session.
4. If the coordinator saw it first, the watcher finds the key and stops.

**Orca channel (coordinator session, later the TUI).**
1. Orca notifies the person; the person approves in the coordinator session (TUI approval needs a write path the observer does not have).
2. The coordinator takes the local claim, posts the marker, applies the label and Status move as a mirror, and types the approval line into the agent session.
3. The watcher's next cycle sees the label and the marker, finds the key, and does nothing.

**In-session channel.** The person types `approved` in the agent's session; the agent runs the helper, wins or loses the claim, and continues only if it won.

## What happens in each failure mode

| id | Outcome under A |
|---|---|
| F1 Double start | Prevented on one host: the second actor finds the `stage.json` key and stops. Across two stores (two hosts, or a restored backup) only the marker comment protects, and two actors can both post within one polling window |
| F2 Coordinator down | GitHub approvals still progress: the watcher handler starts the stage alone. The coordinator, when it returns, finds the key and adopts the state |
| F3 Same-account echo | Handled by the marker token, not by the account. A marker written by any session on the host's login is trusted, so a forged marker also suppresses |
| F4 Plan edited after approval | Key includes the plan version; a changed plan is a new key that needs a new approval. Every actor and the agent must recompute the hash before starting |
| F5 Moved backwards after start | Every actor sees the level disagree and may send a stop; stops must be idempotent. A later forward move with the same plan version finds the key and does not restart |
| F6 Lag or lost events | Level reconciliation tolerates lag; the claim prevents duplicates; lag only delays |
| F7 Two approvals at once | Serialised by the file lock on one host; the second sees the key |
| F8 Someone else, or the agent, moves it | GitHub path: label actor checked against the approvers file, but on a single shared login the agent can apply the label as an allow-listed account. In-session path: the permission-free agent is itself an actuator and can approve itself. Not solved |
| F9 Stale TUI | A TUI approval must carry the record version it showed; the claim fails if the key already exists |
| F10 ClickUp | Never read and never written for stages |

## Who is allowed to approve and how that is verified

- GitHub: an approval label event whose actor is a User account id in the approvers file, after the plan comment, with the plan comment unedited since (the watcher's existing checks reused).
- Orca: whoever types in the coordinator session.
- In-session: whoever types in the agent session, including text the agent itself produces.
- No channel can tell the person from a session acting as the same login.

## What the TUI and the issue show, and how they stay in step

The issue shows the plan comment, the marker comment and the Status. The TUI would show the `stage.json` entry for the key (needs a new read in the observer). They converge on each actor's next cycle; between cycles they can disagree for up to the watcher's 5 minutes.

## What it adds to the build

| Change | Watcher | Coordinator protocol | Observer | Claim command |
|---|---|---|---|---|
| `stage.json` store and a shared claim helper (new CLI verb) | code | uses it | reads it | agent uses it |
| Watcher stage handler for post-claim stages; reverses design decision D2 and non-goal NG-2 (the watcher would post comments and type into sessions) | code | none | none | none |
| Coordinator duties: post plan, mirror label and Status, take the claim, deliver approval | none | protocol | none | none |
| TUI approval: write-back release (OB-09 plus the #409 boundary change) | none | none | code | none |
| Launch prompt: run the claim helper before continuing; verify the plan hash | none | none | none | template |

Existing items that change: WA-01 to WA-05 stay; WA-07 (handoff) is replaced by this; a new owner decision is needed to lift NG-2.

## Cost and risk

Highest build cost: three actors implementing one protocol, the watcher gaining GitHub writes and session typing, and the permission-free agent becoming an actuator. Strength: progress does not depend on any single process being up.

## What stays unresolved

Cross-host or two-store duplicates (GitHub has no conditional comment write); self-approval by the permission-free agent on a shared login; the Project Status field names; whether Orca restricts which session may type into another session (UNVERIFIED).
