# Refactoring Plan: Merge into Base (Variant 1, proposal-A)

## Overview
- Base: Variant 1 (proposal-A, summary and named steps first, in the sweep), selected by tiebreaker level 1
- Incorporating strengths from: Variant 3 (proposal-C), Variant 2 (proposal-B), advocate findings
- Planned changes: 6
- Risk level: Medium overall (Change 1 restructures the Answer; the rest are additive)

## Planned Changes

### Change 1: Two-part answer: the screen direction first in the observer, the summary as the second ask (from Variant 3)
- **Source**: Variant 3 "Answer" and "What happens next"; diff points C-001, C-002, C-005, X-001 (won by V3, 2 of 3 or 3 of 3); review 01 line 167 (item 9: "choose the direction first among Fleet Quilt, Decision Desk, Signal Bridge, then add only the fields those need"), cited by advocate 2
- **Target**: Base, "Answer" (replace) and title (replace)
- **Rationale**: the debate's majority placed the first ask on the observer screen; the base's data finding is kept as the second ask.
- **Integration point**: new title "Proposal A (merged): Fleet Quilt first in the observer; the summary and named steps second, with their data prepared by the sweep". New Answer: "The first ask is a screen in the observer: Fleet Quilt (suggested) or Decision Desk, named now and started only after the contract note is final (XC-07) and the shared read-only capture is recorded (XC-03). The second ask is the plain-English summary with named steps; its data has a known deterministic source (the task title and `Command:` lines from the Orca Task brief, and step states from workers' handoff files), so that data can be prepared as a sweep Phase 2 follow-up after PR #539 merges. Issue and PR links come later."
- **Risk**: Medium; restructures the base answer.

### Change 2: Why Fleet Quilt is the suggested pick (from Variant 3 advocate)
- **Source**: round1-advocate-3.md "Concessions" 1 and "Overall"
- **Target**: Base, "What happens next" (insert first bullet after the ledger bullet)
- **Rationale**: Decision Desk cannot move until QUESTION-LINK is established (review 05 line 66) plus OB-06 and OB-02; Fleet Quilt is in no release row and carries none of those gates, but its data source is unknown, so its first step is writing its data gate.
- **Integration point**: bullet: "One row is added to the observer's `release-gates.md` for the chosen screen ask with its data gate (review 05 D7). If Fleet Quilt: its first step is recording what data it reads, since no source records that. If Decision Desk: it stays behind QUESTION-LINK, OB-06 and OB-02."
- **Risk**: Low.

### Change 3: Ledger wording follows the new answer
- **Source**: consistency with Change 1
- **Target**: Base, first "What happens next" bullet (replace)
- **Integration point**: "The ledger records 'Q19: <Fleet Quilt or Decision Desk> first, in the observer, after XC-07 and XC-03; summary and named steps second' with the date. OB-09 condition (2) ('Q19 names the first ask and its program') is met."
- **Risk**: Low.

### Change 4: Absent step state shows as unknown (from Variant 1 advocate concession)
- **Source**: round1-advocate-1.md "Concessions" 4
- **Target**: Base, the bullet describing `steps: [{name, state}]` (append)
- **Integration point**: append: "A worker that crashed leaves no handoff file for its current step, so a missing state is shown as unknown, never as a colour; reading handoff files is a new read for the sweep and needs its own review and allow-list check."
- **Risk**: Low.

### Change 5: Re-read the reviewer's comment before recording the order (all advocates, A-001)
- **Source**: round1-advocate-1.md, -2.md, -3.md "Shared assumptions" A-001
- **Target**: Base, "What it costs or risks" (append)
- **Integration point**: bullet: "The order 'Fleet Quilt and Decision Desk first' is review 05's reading of the reviewer's 2026-11-11 comment; no source read shows the reviewer ranking the asks. Re-read that comment on #409 before recording Q19."
- **Risk**: Low.

### Change 6: Update costs and unresolved items to the two-part answer
- **Source**: consistency with Change 1; Variant 3 "What it costs or risks"
- **Target**: Base, "What it costs or risks" bullets 1 and 2, and "What stays unresolved" (replace)
- **Integration point**: replace the base's "goes against the spec" and "appears in the sweep's report" bullets with: "Both screen candidates are slow: Fleet Quilt needs its data discovered, Decision Desk waits for QUESTION-LINK." and "The summary data, if prepared in the sweep, appears on the dashboard only if Q17 later says yes; until then it is in the coordinator's local report." Replace "What stays unresolved" with: "The final pick between Fleet Quilt and Decision Desk; where issue and PR links live; whether Orchestrator v2 (#423, not started) ever displays summaries."
- **Risk**: Low.

## Changes NOT Being Made

| Diff Point | Non-Base Approach | Rationale |
|---|---|---|
| X-002 | Defer the choice entirely (V2) | V2's advocate conceded it equals the default and adds nothing; review 05's first step is "the owner picks the first ask" |
| U-002 | Tie the choice to release 3's gates (V2) | Those gates apply only to Decision Desk (advocate 2 concession) |

## Risk Summary

| Change # | Risk | Impact if Failed | Rollback |
|---|---|---|---|
| 1 | Medium | Answer becomes inconsistent with remaining base text | Changes 3 and 6 align the rest; restore base on failure |
| 2 to 6 | Low | None beyond the base | Restore base text |

## Review Status
- Approved by: auto (non-interactive)
- Approval timestamp: 2026-11-14
