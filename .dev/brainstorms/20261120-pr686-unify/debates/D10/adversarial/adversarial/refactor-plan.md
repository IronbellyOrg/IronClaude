# Refactoring Plan (D10 wake transport)

## Overview
- Base variant: Variant 2 (CLAY paper, `variant-2-original.md`)
- Incorporated variants: Variant 1 (OURS) plus debate findings (rounds 1, 2, 2.5)
- Planned changes: 10
- Overall risk: Medium (the merged document is a recommendation text; it changes the base's claims in several places)
- Output: `/home/coder/workspaces/IronClaude/.dev/brainstorms/20261120-pr686-unify/debates/D10/adversarial/merged-output.md`

The merged document is titled "Merged position: wake transport (HYBRID)". It states what the spec should say about how the poll wakes the coordinator.

## Planned Changes

### Change #1: Reframe the claim as a HYBRID
- Source: debate rounds 1 and 2 (both advocates accepted)
- Target: base "The claim"
- Approach: replace
- Rationale: both advocates accepted: durable wake file plus acknowledgment is the truth; mailbox and typed line are optional nudges; no listener. Confidence 80 percent on A-001, 62 percent on C-001.
- Risk: Medium

### Change #2: Add the no-listener decision with the owner's evidence
- Source: Variant 1 facts 1 and 2 (`issue-watcher.md:47`, `:55`, `:76`; owner decision Q3)
- Target: after "The claim"
- Approach: insert
- Rationale: C-003 tie at 95 percent; the base credits Clay for rejecting 477 but the rejection is the owner's D1 option A and NG-1, and Q3 narrowed Coder issue 477 to read-only with no prompt routing.
- Risk: Low

### Change #3: Make the coordinator loop read the wake directory
- Source: round 2 (both advocates); INV-005
- Target: base "The mechanism", new step
- Approach: insert
- Rationale: the pull is not written in the design (D:571 lists "the state files"); a `check --wait` returns on any message of its types, so reading on timeout only is not enough. Rule: read the wake directory at every return of the wait, rate limited, at most once per 5 minutes, only wakes whose `target` is this orchestrator.
- Risk: Medium

### Change #4: Fix the acknowledgment ordering (HIGH INV-001)
- Source: invariant probe INV-001, verified at `pr-a` `cycle.py:777-810` and `orchestrator.md:536-539`
- Target: base mechanism step 4
- Approach: replace
- Rationale: the order "record first, acknowledgment second" is pinned only for plan requests (D:539). It must be pinned for every assigned item: the acknowledgment says `accepted` only after the per-issue state file exists. Otherwise a crash between the two loses the issue.
- Risk: Medium

### Change #5: Make abandonment recoverable (HIGH INV-002)
- Source: invariant probe INV-002, verified at `pr-a` `route.py:407-413`, `:598-602`
- Target: base "What it risks"
- Approach: insert
- Rationale: an abandoned entry is never woken again and its wake file names an orchestrator that can be marked ended. The spec must say what happens to an abandoned wake: either the poll re-targets it to the next orchestrator of the repo with a new wake id, or it stays visible to a named reader. Spec text only; no code in this debate.
- Risk: Medium

### Change #6: Drop issue titles and defer the plan hold payload
- Source: both Round 2 rebuttals (d); INV-017
- Target: base facts and "What it risks"
- Approach: replace
- Rationale: the title has no consumer (D:116: the plan call takes a number) and is GitHub text read by a model. The wake carries `repo`, `number`, `url` only; `plan_requests[]` belongs to the plan-hold decision (D09), not to this transport.
- Risk: Low

### Change #7: Keep the rule on every channel; credit D3 as its origin
- Source: Variant 1 fact 3; X-002 resolution
- Target: base "What it gets right"
- Approach: replace
- Rationale: the rule is the owner's D3, generalized to typed line, mailbox subject and argv. Keep Clay's wider scope, and name D3 as the source.
- Risk: Low

### Change #8: Typed line is a nudge to an idle or freshly started session only; add the guard gap
- Source: round 2 (both); INV-007
- Target: base mechanism step 3
- Approach: replace
- Rationale: the typed line has a use for a person-opened idle session and for the first command of a started session (D:319, D:710). The idle check reads only the draft and output age, so a session waiting on a permission dialog passes it (INV-007). The spec must add "the screen tail shows the main input prompt" as a precondition, as FR-24 rule 1 already requires for approvals (D:573).
- Risk: Medium

### Change #9: Session start through one fixed-pattern verb if a live spike passes
- Source: Variant 1 fact 5; C-004; INV-008, INV-021
- Target: base mechanism step 5
- Approach: replace
- Rationale: prefer `orca agent launch` with a second fixed prompt pattern for the wake line, provided a live spike shows it carries the ccsession tag the lookup needs (U25). Otherwise keep the typed start. In both cases a blind lookup must not start a duplicate session (INV-008): an unreadable process table means "unknown", not "none".
- Risk: Medium

### Change #10: One shared terminal helper with a parity test; neutral acknowledgment name
- Source: Variant 1 fact 7; C-005; INV-019
- Target: base "What it costs"
- Approach: replace
- Rationale: no copy of `orca_term.py` ships to a second consumer; one helper in the package, with a test that runs it against the same fixtures as the report waker. The acknowledgment bucket is renamed only together with both readers and a pinned schema version (INV-019).
- Risk: Medium

## Changes NOT Being Made

| Diff point | Non-base approach | Why the base approach stays |
|------------|-------------------|-----------------------------|
| C-001 | Launch a claim session as the only channel | It cannot reach a coordinator that is already running (concession of the OURS advocate; Coder issue 516's gap) |
| C-007 | One model session per claim | The idle poll costs no tokens (D:120); the OURS advocate conceded |
| C-008 | "Nothing starts while the coordinator is down" | `issue-watcher.md:43` is a merge-ordering note and the poll can start a session (D:112) |
| A-002 (reject as a premise) | Do not build on screen state at all | The mailbox and file do not depend on it; the typed line stays a guarded optional nudge (Change #8) |
| Drop the typed line | OURS Round 2 suggestion for looping sessions | The CLAY advocate showed it is the first command of a started session; kept as a nudge |

## Risk Summary
| Change | Risk | Impact | Rollback |
|--------|------|--------|----------|
| #1 | Medium | Changes the thesis | Restore base text |
| #3 | Medium | New loop duty in the orchestrator skill (PR B) | Remove the step |
| #4, #5 | Medium | Two ack and abandonment rules that PR 686 does not have | Keep as open conditions |
| #8, #9 | Medium | Guard and start behavior need a live spike | Mark UNVERIFIED |
| Others | Low | Wording | n/a |

## Review Status
Auto-approved (unattended; `--interactive` is refused in unattended mode).
