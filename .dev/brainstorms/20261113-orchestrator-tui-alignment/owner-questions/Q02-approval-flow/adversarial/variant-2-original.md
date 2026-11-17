# Proposal B: one actuator; only the coordinator may tell the agent to proceed

Shared terms, the stage table (S0 to S7) and the failure modes (F1 to F10) are in `00-state-machine-and-failure-modes.md` in this folder. Nothing in this proposal is built.

## Design

Exactly one process may send the instruction that moves the governed agent past the plan boundary or starts any later stage: the coordinator that owns that issue. Every approval, from any channel, is only an input the coordinator validates.

1. **The watcher stays a claim trigger and nothing more.** It keeps its built behaviour (claim-stage at-most-once, `claimed` is terminal) and gains no post-claim logic. It never messages the coordinator or the agent. The coordinator reads GitHub itself at each wake, so the watcher is out of the race entirely.
2. **One approval record, written ahead.** Before it instructs anything, the coordinator writes one row to its ledger: `approval-id | issue | stage | plan sha256 | channel | approver | evidence (label event id, Orca message id or typed line) | state (recorded, instructed, acked, revoked) | time`, through a small CLI helper that takes a per-issue lock and refuses a second row for the same (issue, stage, plan version).
3. **The agent obeys only that record.** The launch prompt changes: the agent continues only on a line `approved <approval-id> plan-sha256=<hex>`, recomputes its plan file's hash, refuses a mismatch and a bare `approved`, and answers `ack <approval-id> applied|refused`. A person who types in the agent session is told to approve through Orca or GitHub.
4. **GitHub is a mirror and an input.** The coordinator posts the plan reply, moves Status to review and mentions the assignee; after an Orca approval it posts an approval comment with marker `<!-- sc:stage:approved id=<approval-id> plan=<sha256> -->` and moves Status. A GitHub change that matches an existing row is a no-op.
5. **Reconciliation by level.** At each wake (WC-16 already caps the pass at once every 5 minutes) the coordinator compares GitHub, the ledger and the agent's state and acts only on a difference.

**Invariant.** Exactly one approval record per (issue, stage, plan version), created only by the coordinator, durably written before any instruction; the agent proceeds only on an instruction that names that record and matches its plan hash.

## How an approval flows

**GitHub channel.**
1. The coordinator posted the plan reply (with plan version), moved Status to review and mentioned the assignee.
2. The assignee applies the stage approval label (actor readable) and moves Status (display only; its actor is not read by any code today).
3. At its next wake the coordinator reads the label events, checks the actor against the approvers file and that the plan comment was not edited after the label (reusing the watcher's `approval_of` and `unchanged_since` rules), writes the row, then types the one approval line into the waiting agent session.
4. The agent checks the hash and acks. The coordinator marks the row `acked`.

**Orca channel (coordinator session now; TUI after the write-back release).**
1. Orca shows the person the plan path and version. The person approves in the coordinator session (or, later, the TUI sends a typed approval message to the coordinator's Run carrying the plan version and record version it displayed).
2. The coordinator writes the row, delivers the line to the agent, then mirrors to GitHub (approval comment with the row id, label, Status).
3. At its next wake it reads its own mirror on GitHub, finds the row, and does nothing.

## What happens in each failure mode

| id | Outcome under B |
|---|---|
| F1 Double start | Prevented by structure: only one actor exists, and its second look at the same approval finds the row |
| F2 Coordinator down | Nothing starts. GitHub approvals wait as GitHub state; Orca approvals wait in the Run mailbox (replayed until acknowledged). The coordinator applies them once on restart. Cost: delay |
| F3 Same-account echo | Irrelevant to duplicates: the coordinator's mirror writes carry its row id, and any GitHub state that matches a row is a no-op. A GitHub approval with no row is accepted as new |
| F4 Plan edited after approval | Row and instruction carry the plan hash; the agent refuses a mismatch; a changed plan needs a new review |
| F5 Moved backwards after start | The coordinator marks the row `revoked`, sends one `stop <approval-id>`, and asks the person. It never restarts by itself; a later forward move needs a new row |
| F6 Lag or lost events | Level reads at each wake; lag delays, never duplicates |
| F7 Two approvals at once | Serialised through one coordinator and the per-issue lock; the second gets "already approved" |
| F8 Someone else, or the agent, moves it | Project Status moves alone never authorise. The label actor must be in the approvers file, but on a single shared login a permission-free agent can apply that label too. Mitigation: accept GitHub approvals only from an account id that is not the host's own login (needs a second account), or switch the GitHub channel off until FU-6 (per-actor checks). The in-session path is removed |
| F9 Stale TUI | The TUI message carries the plan version and record version; the coordinator rejects a stale one |
| F10 ClickUp | Never read and never written for stages |

## Who is allowed to approve and how that is verified

- GitHub: the assignee (or an account in the approvers file) applying the stage approval label after the plan comment, plan comment unedited since; recommended: an account id other than the host's `gh` login.
- Orca: the person at the coordinator's terminal, or the TUI once its write-back release exists. Whether a session on the same host can type into the coordinator's terminal (`orca terminal send`) and impersonate the person is UNVERIFIED and stays a residual risk.

## What the TUI and the issue show, and how they stay in step

The ledger row is the truth; the issue and the TUI are views of it. The issue shows the plan reply, the approval comment with the row id and the Status. The TUI would show the row state (recorded, instructed, acked, revoked). They agree within one coordinator wake (at most about 5 minutes); while they disagree, an approval made against the stale view is rejected by version, never doubled.

## What it adds to the build

| Change | Watcher | Coordinator protocol | Observer | Claim command |
|---|---|---|---|---|
| None; the watcher stays as built (WA-01 to WA-05 unchanged) | none | none | none | none |
| Approval-record helper (small CLI verb with a per-issue lock) | none | uses it | reads it later | none |
| Issue-pipeline duties: adopt the `issue-<N>` agent, post plan, mention, read GitHub at wake, record, deliver, revoke | none | protocol | none | none |
| How the coordinator reaches the agent: type one line into its waiting prompt (WC A3 rules), or make the agent a supervised worker started by the coordinator (redesign; SW-13) | none | protocol | none | possibly |
| Launch prompt: approval-id and hash form only; no bare `approved` | none | none | none | template |
| TUI approval message to the coordinator (OB-09 Decision Desk plus the write-back boundary change) | none | none | code, later | none |

Existing items that change: WA-07 (handoff) becomes "coordinator adopts the claimed agent"; the coordinator needs `issue-write` grant rows (section 6.8) for the plan reply, mention, label and Status.

## Cost and risk

Moderate build cost, almost all in the coordinator protocol plus one small helper; the watcher and observer stay untouched until the TUI release. Progress stops while the coordinator is down. The coordinator is an LLM session, so the helper must enforce the one-row rule mechanically rather than by instruction.

## What stays unresolved

Forgery on a single shared account; whether same-host sessions can type into the coordinator terminal; the Project Status value names; how the coordinator discovers a newly claimed issue (it can read `.dev/issues/<N>/worktree.json` or Orca's worktree list; which one is UNVERIFIED as reliable).
