# Refactoring Plan: Q1 (a2) and (b)

## Overview
- Base variant: Variant 1 (proposal-A)
- Incorporated from: Variant 2 (left-out channels, PR reasoning), Variant 3 (two-sided test, runner-up), all advocates (environment rule, scope separation)
- Planned changes: 6
- Overall risk: Low (the shape, F2 with the "could run for this worktree" rule, is unchanged)
- Rule carried: never specify the code fix; outcome level only.

## Planned Changes

### Change 1: replace the unlisted-channel claim with an auditable promise
- Source: Variant 2 (C-003, X-001); V1 advocate concession 1
- Target: base "Answer" part (b) and "What it unlocks" bullet 1
- Approach: replace
- New substance: the ruling names the six channels as a minimum and names any channel it deliberately leaves out; anything the check cannot classify is refused and reported `unscanned` with its reason. No claim that refusal covers channels nobody listed.
- Risk: Low

### Change 2: two-sided regression test
- Source: Variant 3 (U-003, C-005)
- Target: base "What happens next", step 2
- Approach: replace
- New substance: the test reproduces the 2026-11-13 probe and fails if any in-scope program runs in a scanned worktree, and fails if a worktree that should be refused is scanned.
- Risk: Low

### Change 3: environment counting rule
- Source: all advocates; `../../question.md` host facts
- Target: base "What happens next", step 3
- Approach: append
- New substance: an inherited-environment setting counts only when it names a program `git status` could run (the session's `credential.*` keys name none); an environment setting that does count affects the whole run, which is then reported, not partly scanned.
- Risk: Low

### Change 4: keep the git-status scope separate
- Source: A-002 (all advocates ACCEPT); SW-02 (2); INV-039
- Target: base "What happens next", new step 4
- Approach: insert
- Risk: Low

### Change 5: reasoning recorded in the PR, owner review before merge
- Source: Variant 2 (U-002)
- Target: base "What happens next", new step 5
- Approach: insert
- Risk: Low

### Change 6: name the runner-up and when it would win
- Source: Variant 3 advocate overall; V1 advocate concession 2
- Target: base "What stays unresolved"
- Approach: append
- New substance: the combination (disable programs by default, refuse only where disabling could change the answer) is the runner-up if a count shows many worktrees that use only fsmonitor, whose git facts F2 would withhold for no security gain.
- Risk: Low

## Changes NOT Being Made

| Diff point | Non-base approach | Why rejected |
|---|---|---|
| C-001, X-002 | Variant 2: leave the shape to the #539 author | 3 of 3, its own advocate conceded: SW-01 (1) requires the owner's ruling to name the shape; the author is unnamed (Q33). |
| C-002, A-001 | Variant 3: combination as the primary shape | 2 to 3 of 3: on filters it gives the same result as F2; its extra judgement ("could change the answer") is harder and unmeasured; two behaviours cost more. Kept as runner-up (Change 6). |

## Risk Summary

| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 1 to 6 | Low | wording, test requirement, added steps | revert to `variant-1-original.md` |

## Review Status
- Approval: auto-approved (non-interactive), 2026-11-14
