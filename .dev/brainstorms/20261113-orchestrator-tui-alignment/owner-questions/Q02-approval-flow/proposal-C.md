# Proposal C: GitHub is the only authority; Orca and the TUI write through to GitHub and act only on what they read back

Shared terms, the stage table (S0 to S7) and the failure modes (F1 to F10) are in `00-state-machine-and-failure-modes.md` in this folder. Nothing in this proposal is built.

## Design

The only thing that authorises a stage is an approval recorded on GitHub, and the only thing that acts on it is the coordinator, which acts only on what it reads back from GitHub.

1. **The authorisation record is a GitHub label event.** The coordinator posts the plan as an issue reply carrying its plan version (`<!-- sc:stage:plan issue=<N> stage=<S> plan=<sha256> -->`). Approval is the stage approval label applied after that reply, by a User account in the approvers file, with the plan reply unedited since. GitHub gives the label event a unique id; that id plus the plan version is the idempotency key. The Project Status move is display only, because no code today reads who moved it.
2. **Orca and the TUI never authorise directly; they write through.** When the person approves in the coordinator session (or, later, the TUI), the coordinator applies the approval label on GitHub and then treats that exactly like a label applied on github.com: it reads the label events back and acts only on what it reads.
3. **One actuator.** Only the coordinator instructs the agent. Before instructing, it writes "acted on label event <id> for plan <sha256>" to its ledger; an event id already in the ledger is never acted on again.
4. **The watcher stays a claim trigger.** It gains no post-claim logic. The coordinator may reuse the watcher's read functions through a new read-only verb (for example a stage-status read), so the label and edit checks are the same code.
5. **The agent** continues only on a line naming the label event id and the plan hash, recomputes the hash and refuses a mismatch.

**Invariant.** A stage starts only after the coordinator has read back from GitHub an approval label event, by an allowed account, later than the unedited plan reply for that exact plan version, and has recorded that event id as consumed; each event id is consumed at most once.

## How an approval flows

**GitHub channel.**
1. The coordinator posts the plan reply, moves Status to review and mentions the assignee.
2. The assignee applies the approval label and moves Status.
3. At its next wake the coordinator reads the label events, verifies actor, order and no edits, records the event id, and types the approval line into the waiting agent session.

**Orca channel (coordinator session now; TUI later).**
1. Orca notifies the person, who approves in the coordinator session.
2. The coordinator applies the label on GitHub as the host's `gh` login, then reads the events back.
3. It sees the new label event, verifies it like any other, records the event id, and instructs the agent. If the read-back does not show the event yet (GitHub lag), it waits for the next wake; it never acts on the Orca input itself.

## What happens in each failure mode

| id | Outcome under C |
|---|---|
| F1 Double start | Prevented: one actor, one consumed event id; a later read of the same event finds it consumed |
| F2 Coordinator down | GitHub holds the approval durably; the coordinator acts once on restart. An Orca approval cannot be made while the coordinator is down unless the person goes to GitHub |
| F3 Same-account echo | No echo problem by construction (the write-through and the read-back are the same record). But the record's actor is the host's login, so a write-through approval cannot be told apart from a forged one |
| F4 Plan edited after approval | The label must post-date the plan reply and the reply must be unedited; the agent checks the hash |
| F5 Moved backwards after start | Removing the label (actor readable) is the revocation; the coordinator sends one stop and asks the person. A Status move back alone is shown but not acted on |
| F6 Lag or lost events | Orca approvals appear to "not take" until GitHub returns the event; how long GitHub's events list lags is UNVERIFIED. No duplicates |
| F7 Two approvals at once | Two write-throughs of an already-present label: whether GitHub records a second `labeled` event is UNVERIFIED; either way the coordinator consumes per (issue, stage, plan version) and ignores the second |
| F8 Someone else, or the agent, moves it | Label actor allow-list holds for other people. On a single shared login every session on the host, including the permission-free agent, can apply the label as an allowed account. C is only safe with a separate approver account whose token the host's sessions do not hold, which also means the coordinator could not write through for the person |
| F9 Stale TUI | Harmless: a second write-through of the same label is a no-op for the coordinator |
| F10 ClickUp | Never read and never written for stages |

## Who is allowed to approve and how that is verified

An account in the approvers file, checked on the label event's actor id, after the plan reply, with the reply unedited. Full verification needs an approver account distinct from the host's login; with one login, a write-through and a forgery look the same.

## What the TUI and the issue show, and how they stay in step

The issue is the truth; the TUI shows what the coordinator last read from GitHub plus "approval sent, waiting for GitHub" for a write-through not yet read back. They agree within one coordinator wake plus GitHub's own lag.

## What it adds to the build

| Change | Watcher | Coordinator protocol | Observer | Claim command |
|---|---|---|---|---|
| Read-only stage-status verb reusing `github.py` reads and `predicates.py` checks | code (read-only) | uses it | none | none |
| Issue-pipeline duties: post plan, mention, write-through label, read back, record consumed event, deliver, revoke | none | protocol | none | none |
| Launch prompt: event-id and hash form only; no bare `approved` | none | none | none | template |
| TUI approval via the coordinator (OB-09 plus write-back) | none | none | code, later | none |
| A second GitHub account for approvers (owner setup), or acceptance of the forgery risk | none | none | none | none |

Existing items that change: WA-07 as in B; `issue-write` grant rows for the plan reply, label and Status writes.

## Cost and risk

Moderate build cost. Every approval depends on GitHub being reachable and readable; Orca approvals are slower by up to one wake plus GitHub lag. The audit trail is public and in one place, which is its main strength.

## What stays unresolved

The single-login forgery problem is sharper here than in B because GitHub is the authority; the Project Status value names; GitHub's events lag and duplicate-label behaviour (both UNVERIFIED).
