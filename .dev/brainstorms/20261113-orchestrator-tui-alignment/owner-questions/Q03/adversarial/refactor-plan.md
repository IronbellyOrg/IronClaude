# Refactoring Plan: Q3

## Overview
- Base variant: Variant 1 (proposal-A, narrow)
- Incorporated from: Variant 3 (close condition, posting details), Variant 2 (guards kept on record), debate consensus
- Planned changes: 5
- Overall risk: Low (additive; the answer stays "narrow")
- Rule carried: do not claim an orchestrator that manages work, a watcher handoff, or a TUIBBS screen exists.

## Planned Changes

### Change 1: name the condition under which close is right instead
- Source: Variant 3 "Answer" and reopen conditions (won X-001, X-003, A-003)
- Target: base "Answer", appended sentence
- Approach: append
- Rationale: all three advocates agree close is correct if the owner states single-host is lasting and no TUIBBS or remote reader is planned (ADJ line 283; Q18 at `merged-requirements.md:545`).
- Risk: Low

### Change 2: say that narrowing replaces the problem statement
- Source: debate A-001; V1 advocate concession 6
- Target: base "What it costs or risks"
- Approach: append bullet
- Rationale: the issue's written body serves only the watcher; text A is effectively a new problem under the old number. The owner should know that.
- Risk: Low

### Change 3: grant rows name each write; fix text C's link placeholder for the fallback
- Source: Variant 3 advocate concession 3 and A-002 response
- Target: base "What happens next", step 3, and a fallback note
- Approach: insert
- Rationale: XC-02 (4) requires a grant per post; whether `issue-write` covers a state change is UNVERIFIED; text C holds "[link to the comment holding option A]" (ADJ line 661).
- Risk: Low

### Change 4: reconcile "writes nothing" with the per-read audit line
- Source: V3 advocate; spec CO-03 (5)
- Target: base "What happens next", step 2 (CO-02)
- Approach: append clause
- Rationale: text A says the read route "writes nothing" and also requires an audit line per read; CO-03 (5) already calls for reconciling them.
- Risk: Low

### Change 5: text B's guards stay on record
- Source: Variant 2 (U-002), preserved in ADJ Part 6.3
- Target: base "What stays unresolved"
- Approach: append
- Rationale: if a watcher-design revisit condition ever occurs, the guarded routing text is ready; nothing is lost by not keeping routing now.
- Risk: Low

## Changes NOT Being Made

| Diff point | Non-base approach | Why rejected |
|---|---|---|
| C-002, X-002 | Variant 2: keep prompt routing with guards | 3 of 3: contradicts owner design decision D1 with no recorded revisit condition; largest attack surface; blocked on the #339 grant format. |
| C-001 | Variant 3: close as the primary answer | 2 of 3 preferred narrow while the owner's comment asks for alignment; close is kept as the named conditional answer (Change 1). |

## Risk Summary

| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 1 to 5 | Low | wording and conditions | revert to `variant-1-original.md` |

## Review Status
- Approval: auto-approved (non-interactive), 2026-11-14
