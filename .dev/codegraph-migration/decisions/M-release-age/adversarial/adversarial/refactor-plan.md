# Refactoring Plan: merge into Option B

## Overview

- Base variant: Variant 2 (Option B), file `variant-2-original.md`
- Incorporated variants: Variant 3 (Option C), Variant 1 (Option A), plus the shared-assumption resolutions from the debate
- Planned changes: 8
- Rejected changes: 4
- Overall risk: Medium. Change 1 reverses B's fallback, and the rest add to the text.
- Output: `../merged-output.md` (the `--output` directory root), written as a decision option in the same style as the inputs (title, rule bullets, rationale, cost), plus a short "Edge cases and tests" list and provenance comments.

## Planned Changes

### Change 1: Replace B's fallback with C's no-fallback rule
- Source: Variant 3, rule bullet ("if it is younger, do nothing this run (no fallback to an older eligible release)")
- Target: Base bullet 2 ("If the newest release is younger, the monitor may still bump to an older release that is eligible ...")
- Approach: replace. The candidate is the highest-semver release in the candidate set. If it is younger than the minimum age, the run does nothing and never falls back to an older release.
- Rationale: debate point C-002, won by C on a 2-of-3 majority at 70% confidence, and point X-002, unanimous for C at 95%. B's advocate conceded that "the eligible release is the settled one" is false as written. In the replay, B's fallback bumped to 1.3.0 on 07-21 and to 1.6.1 on 10-13, after their patches existed.
- Risk: Medium. It modifies the core rule. The starvation side effect is handled by Change 4.

### Change 2: Define the candidate set precisely (semver, published_at, filters)
- Source: shared assumptions A-001 (all QUALIFY), A-002 (all ACCEPT), A-003 (all REJECT), and base bullet 1
- Target: base bullet 1
- Approach: restructure bullet 1.
  - The set is the full release list, minus drafts, minus prereleases, minus tags that do not parse as semver, minus releases without `published_at`.
  - Keep only releases strictly newer than the pin by semver.
  - Order by semver, never by date. Do not use the `releases/latest` endpoint or flag.
- Rationale: debate points A-001, A-002 and A-003 at 85 to 95% confidence. This removes the backport and maintainer-flag hazards.
- Risk: Low

### Change 3: Define the age boundary exactly
- Source: shared assumption A-004 (all QUALIFY)
- Target: base bullet 1
- Approach: insert. Eligible means `now_utc - published_at >= MIN_AGE_DAYS * 86400` seconds, which is inclusive. `MIN_AGE_DAYS = 14` stays one constant in the bump script.
- Rationale: A-004, unanimous, 90%.
- Risk: Low

### Change 4: Add a stall warning to the run summary
- Source: proposals from the Variant 1 and Variant 3 advocates; base reporting bullet (C-005)
- Target: the base reporting text, split into its own bullet. This also fixes the Clar-3 finding that bullet 2 mixed the rule with reporting.
- Approach: append.
  - The run summary always names the newest release that is waiting, and the UTC date and time it becomes eligible.
  - It adds a stall warning when the oldest release newer than the pin is at least `2 * MIN_AGE_DAYS` (28) days old and the run still bumps nothing.
  - Reporting only; it never changes the pick.
- Rationale: C-005 was unanimous. Both the C and A advocates named starvation as the cost of no fallback.
- Risk: Low

### Change 5: Split the candidate set by major line according to M-a
- Source: shared assumption A-005 (majority B and C, 65%)
- Target: new rule bullet after bullet 1
- Approach: insert.
  - If the M-a decision keeps majors off the automated PR path, the age rule runs separately on two sets: releases within the pinned major, and releases with a higher major.
  - A pending major never blocks minor or patch bumps.
  - The higher-major set goes to the M-a handling once its own candidate passes the same 14-day rule.
  - If M-a treats majors like minors, there is one set.
- Rationale: A-005. Under a no-fallback rule, a single set would let a held 2.0.0 freeze all 1.x bumps.
- Risk: Medium. It depends on a decision that has not been made yet, so it is flagged for the user.

### Change 6: Tighten the manual override
- Source: base bullet 3 (C-003, unanimous)
- Target: base bullet 3
- Approach: modify.
  - `workflow_dispatch` input `min_age_days`: a whole number, 0 or more. Any other value fails the run before any download.
  - Scheduled runs always use `MIN_AGE_DAYS`.
  - The override changes only the age. Every other step stays the same: the same candidate pick (no fallback), hash checks, attestation, proof and human merge.
  - The run summary and the PR body record that an override was used, and its value.
- Rationale: debate point C-003 at 95% confidence. Guard gap found on review: B's text did not say how input is validated, or that the override is visible.
- Risk: Low

### Change 7: State the pulled and re-tagged release behavior
- Source: Variant 1 cost bullet ("a pulled or re-tagged release can already be in an open PR"), Risk-4 (only A covered it)
- Target: new "Edge cases and tests" list
- Approach: append.
  - A deleted and re-created release gets a new `published_at`, so its 14-day clock restarts.
  - A deleted release drops out of the candidate set on the next run.
  - What to do with an already-open bump PR whose release was deleted is not decided here. It is flagged for the user.
- Risk: Low

### Change 8: Add offline test cases
- Source: shared assumption A-006 (all ACCEPT), base cost bullet ("one more date comparison to test")
- Target: new "Edge cases and tests" list, and the cost bullet
- Approach: append.
  - The selection logic is a pure function of (release list JSON, now, pin, min age, major policy) that returns the candidate or none, plus a reason.
  - Tests use saved fixture JSON and a fixed clock, with no network.
  - Required cases:
    - The boundary at 14 days minus 1 second, exactly 14 days, and 14 days plus 1 second.
    - An empty list, and a list with nothing newer than the pin.
    - A list where everything is a draft or prerelease.
    - A backport published after a higher version.
    - A re-created release.
    - Override 0.
    - A pending major alongside an eligible minor.
    - The 2026 replay, with expected bumps 08-04 1.5.0, 09-09 1.6.0 and 10-17 1.6.2 when the pin starts below 1.3.0 and runs are daily.
- Rationale: A-006 at 95% confidence. The Comp-1 gap is that no variant said "offline".
- Risk: Low

## Changes NOT Being Made

| Diff point | Non-base approach | Rationale for rejection |
|---|---|---|
| C-001 | A: 0 days; C: 7 days | The 14-day threshold was unanimous. A and C both conceded that their threshold diverges from the user's rule. |
| C-004, A-003 | A and C: `releases/latest` | Unanimous REJECT. The latest flag is maintainer-set and can disagree with the newest semver. |
| C-002 (minority) | B advocate: keep the fallback but skip any release that already has a newer patch on the same major.minor line | Lost 1 to 2. It adds a second rule that has to be tested, and in this history its only gain is two extra July PRs (1.3.1 on 07-23, 1.4.1 on 07-24) that 1.5.0 superseded within two weeks. Recorded as the fallback design if the stall warning fires often in practice. |
| X-001 | A: no age gate, with the proof and the human merge as the safety net | Unanimous against A. The proof checks the tool list and the registration shape, not semantics, and a merged pin reaches every workspace. |

## Risk Summary

| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 1 | Medium | Longer gaps between bumps when releases come less than 14 days apart | Switch to the recorded minority rule (same-line skip) |
| 5 | Medium | Wrong if M-a is decided differently | Collapse to one set when M-a treats majors like minors |
| 2, 3, 4, 6, 7, 8 | Low | Additive precision | Remove the bullet |

## Review Status

- Approval: auto-approved (non-interactive run)
- Timestamp: 2026-10-30T15:45:00Z
