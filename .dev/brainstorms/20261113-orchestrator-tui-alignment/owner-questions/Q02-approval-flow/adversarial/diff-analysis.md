# Diff Analysis: approval-flow design proposal comparison

## Metadata

- Generated: 2026-11-14 (Step 1, written inline by the orchestrating worker)
- Variants compared: 3 (variant 1 = proposal A, symmetric channels with a shared claim; variant 2 = proposal B, single actuator; variant 3 = proposal C, GitHub as sole authority)
- Shared input: `../00-state-machine-and-failure-modes.md` (stages S0 to S7, failure modes F1 to F10)
- Total differences found: 20 debate points plus 8 unique contributions
- Categories: structural (1), content (10), contradictions (3), unique (8), shared assumptions (6 promoted)

## Structural Differences

| # | Area | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity |
|---|---|---|---|---|---|
| S-001 | Section set and order | The 8 required sections in the required order | Same | Same | Low (identical skeleton by brief) |

## Content Differences

| # | Topic | Variant 1 (A) | Variant 2 (B) | Variant 3 (C) | Severity |
|---|---|---|---|---|---|
| C-001 | Who may start a stage (actuators) | Three: coordinator, a new watcher stage handler, the governed agent itself | One: the coordinator | One: the coordinator, but only on GitHub read-back | High |
| C-002 | Where the authorisation record lives | Local `stage.json` (file lock, write-ahead `pending`) plus a GitHub marker comment | Coordinator ledger row written by a locked helper; GitHub is a mirror | GitHub label event (server-assigned id); ledger only records "consumed" | High |
| C-003 | Watcher role after the claim | New stage handler that posts comments and types into sessions (reverses D2 and NG-2) | Unchanged; coordinator reads GitHub itself | Unchanged trigger plus a new read-only stage-status verb | High |
| C-004 | Approval typed in the agent's own session | Kept; agent runs the claim helper and may act | Removed; only `approved <id> plan-sha256=<hex>` from the coordinator | Removed; only the event-id and hash line | High |
| C-005 | Coordinator down | GitHub approvals still progress via the watcher | Nothing starts; approvals wait (GitHub state, Orca mailbox) | GitHub approvals wait; Orca approvals impossible while down | Medium |
| C-006 | Orca approval path | Coordinator wins claim, posts marker, mirrors, instructs | Coordinator writes row, instructs, then mirrors | Coordinator writes label to GitHub, reads it back, then instructs | High |
| C-007 | Echo handling | Token in marker comments | Row id in mirror comment; matching state is a no-op | No echo by construction (write-through and read-back are one record) | Medium |
| C-008 | Backward move and revocation | Any actor may send an idempotent stop | Coordinator marks revoked, one stop, asks the person, never auto-restarts | Label removal is revocation; Status-only move shown, not acted on | Medium |
| C-009 | How the agent is reached | Watcher and coordinator type one line into the session | Type one line (WC A3 rules) or redesign the agent as a supervised worker (SW-13) | Type one line | Medium |
| C-010 | Build footprint | Watcher (writes), coordinator, observer, claim template, store and helper | Coordinator protocol, helper, claim template; observer later | Watcher read-only verb, coordinator, claim template, a second GitHub account | Medium |

## Contradictions

| # | Point of conflict | Position | Opposing position | Impact |
|---|---|---|---|---|
| X-001 | Variant 1's watcher writes against the owner's recorded design | A: "Watcher stage handler ... reverses design decision D2 and non-goal NG-2 (the watcher would post comments and type into sessions)" | Owner's D2 "The poller never assigns, comments or moves Project items" (`issue-watcher.md` 2.1); B and C keep the watcher write-free | High (requirement-constraint conflict; needs an owner decision) |
| X-002 | Variant 3 internal: write-through versus verifiable actor | C: "the coordinator applies the label on GitHub as the host's `gh` login" | C: "C is only safe with a separate approver account whose token the host's sessions do not hold, which also means the coordinator could not write through for the person" | High (the two halves of C cannot both hold) |
| X-003 | All three versus the owner's literal wording | Owner: "moving the issue into the next state ... that move is taken as approval" | A, B, C: Status move is display only; the approval is a label event, because no code reads who moved the Status | Medium (the owner must accept the substitution, or the actor of a Status move must be proven readable) |

## Unique Contributions

| # | Variant | Contribution | Value |
|---|---|---|---|
| U-001 | A | Progress continues without the coordinator (watcher starts GitHub-approved stages alone) | Medium |
| U-002 | B | The watcher is removed from the race entirely: it is not changed, and the coordinator reads GitHub at its own wake | High |
| U-003 | B | A helper with a per-issue lock enforces the one-record rule mechanically, not by an LLM instruction | High |
| U-004 | C | The GitHub label event id (server-assigned, unique) as the idempotency key | Medium |
| U-005 | C | TUI state "approval sent, waiting for GitHub" for a write-through not yet read back | Low |
| U-006 | A | States plainly that a forged marker also suppresses (echo suppression is forgeable on one login) | Low |
| U-007 | B | Names the open question of how the coordinator discovers a newly claimed issue (`worktree.json` or Orca's worktree list) | Medium |
| U-008 | C | A read-only verb so the coordinator reuses the watcher's `approval_of` and `unchanged_since` code rather than re-describing it in prose | Medium |

## Shared Assumptions

Agreement points found: all three bind approval to a plan hash; all three treat a Project Status move as display only; all three put the coordinator in charge of the plan reply and the mention; all three ignore ClickUp; all three accept a residual forgery risk on one shared login.

Documented, not promoted (STATED in at least one variant): single host and one local store (A states it); a permission-free agent holding `gh` credentials can forge GitHub actions (all three state it).

| A-NNN | Assumption | Source agreement | Impact | Status |
|---|---|---|---|---|
| A-001 | A coordinator exists that owns each claimed issue's governed agent; none is built, watcher sessions are Run-less, and who opens it and how many issues one coordinator holds is unstated | All three make the coordinator the poster and (in B, C) the only actuator | High: without it no design runs | UNSTATED, promoted |
| A-002 | Something other than the person may type into the governed agent's waiting session (`orca terminal send`), and Orca allows a session to type into one it did not start | All three deliver the approval line into the session | High: the delivery path of every design | UNSTATED, promoted |
| A-003 | "The plan" is one stable file whose hash the agent and the coordinator compute the same way; the plan path depends on the next-step chain (for example a `/sc:workflow` package) | All three bind approval to a plan SHA-256 | High: F4 protection rests on it | UNSTATED, promoted |
| A-004 | The owner will accept that the approval signal is a label event, with the Status move as display, rather than the move itself | All three substitute a label | Medium | UNSTATED, promoted |
| A-005 | The coordinator may hold a standing issue-write grant for every pipeline issue (plan reply, mention, label, Status); the grant table (6.8) is written per item and per action | All three have the coordinator post | Medium: grant shape is new | UNSTATED, promoted |
| A-006 | The governed agent stays alive, waiting at its prompt, for as long as review takes (hours or days, across host restarts) | All three deliver to a waiting session | High: if the session dies, a later approval has nowhere to go and a restart risks a second run | UNSTATED, promoted |

## Summary

- Total structural differences: 1
- Total content differences: 10
- Total contradictions: 3
- Total unique contributions: 8
- Total shared assumptions surfaced: 8 (UNSTATED: 6 promoted, STATED: 2, CONTRADICTED: 0)
- Highest-severity items: C-001, C-002, C-003, C-004, C-006, X-001, X-002, A-001, A-002, A-003, A-006
- Taxonomy levels: L1 S-001; L2 C-003, C-009, C-010, X-001, A-001, A-005; L3 C-001, C-002, C-004, C-005, C-006, C-007, C-008, X-002, X-003, A-002, A-003, A-004, A-006
- Similarity check: differences well above 10 percent; debate proceeds
