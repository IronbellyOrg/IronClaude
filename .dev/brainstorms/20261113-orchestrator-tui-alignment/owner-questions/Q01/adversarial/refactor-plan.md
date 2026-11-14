# Refactoring Plan: Q1

## Overview
- Base variant: Variant 2 (proposal-B)
- Incorporated from: Variant 3 (premise), Variant 1 (focused review, fan-out framing), debate consensus on A-001 and A-003, CONTRADICTION-1
- Planned changes: 5
- Overall risk: Low (all additive wording; the answer itself does not change)
- Hard constraint carried: no change may specify the code fix (worker brief, Q1 rule).

## Planned Changes

### Change 1: state the premise the ruling relies on
- Source: Variant 3, step 1 (C-004; Variant 2 advocate concession 1)
- Target: base "What happens next", step 1
- Approach: insert
- Rationale: SW-01 (2) requires every ruling to state its premise (`merged-requirements.md:190`). For a fix, the premise is the worst-case lens of `SECURITY.md:168-170` (configuration assessed at worst case; agent coordination checked for escalation), with the counterweight (every session already permission-free, ADJ E-11) named and not relied on.
- Risk: Low

### Change 2: phrase the scope by outcome, list as a minimum
- Source: debate A-001 (V2 advocate REJECT; V1, V3 QUALIFY); `merged-requirements.md:36`
- Target: base "Answer" part (b)
- Approach: append one sentence
- Rationale: no source claims the measured list is complete; the spec states the requirement by outcome.
- Risk: Low

### Change 3: say what the fix does and does not remove
- Source: debate A-003 and X-003 (Variant 1 won both points)
- Target: base "What stays unresolved"
- Approach: append
- Rationale: the sweep adds fan-out across every listed worktree on every coordinator wake (`HOW-WE-WORK.md:406`); other sessions may run `git status` too (UNVERIFIED whether with the same config).
- Risk: Low

### Change 4: keep the fix reviewable on its own
- Source: Variant 1, U-002
- Target: base "What it costs or risks", first bullet
- Approach: append a clause
- Rationale: #539 is a 1003-file PR; a security change is easier to review as its own push with its own description. Process only, no code design.
- Risk: Low

### Change 5: record the XC-04 reading conflict
- Source: CONTRADICTION-1 (debate transcript)
- Target: base "What it unlocks", second bullet
- Approach: append a qualifier
- Rationale: `merged-requirements.md:630` lets a recorded acceptance satisfy the git trust boundary, while `:452` and `:889` forbid the unfixed sweep for XC-04; the base's advantage is certain only under the strict reading.
- Risk: Low

## Changes NOT Being Made

| Diff point | Non-base approach | Why rejected |
|---|---|---|
| C-001, C-005 | Variant 1: accept now, fix after merge under a trigger | Lost 3 of 3: leaves the hole on master and makes the acceptance irreversible at merge; the trigger is not mechanical and may already be met by the every-wake coordinator sweep (V3 advocate, `HOW-WE-WORK.md:406`). |
| C-002, X-002 | Variant 3: permanent acceptance with caveats | Lost 3 of 3: permanently weakens a shipped claim; XC-04 blocked under the strict reading; its premise contradicts its own risk section (X-003). |
| X-001 | Any claim about which option is fastest overall | Unresolved (split); not stated in the merged answer. |

## Risk Summary

| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 1 to 5 | Low | wording only | revert the merged file to the base copy `variant-2-original.md` |

## Review Status
- Approval: auto-approved (non-interactive), 2026-11-14
