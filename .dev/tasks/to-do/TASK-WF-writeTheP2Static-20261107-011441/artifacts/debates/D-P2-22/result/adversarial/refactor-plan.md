# Refactoring Plan

## Overview
- Base variant: Variant 1 (option A)
- Incorporated variants: Variant 2 (two items, both wording only)
- Planned changes: 2 (to the decision text, not to any repo file)
- Rejected changes: 3
- Overall risk: Low (additive wording in a decision record)

## Planned Changes

### Change 1: bound the exemption in the decision text
- Source: Variant 2 advocate, weakness 1 ("the exemption is a precedent")
- Target: Variant 1, claimed-weakness paragraph
- Approach: append
- Rationale: debate Round 1, C-004 and X-002 (confidence 62-67%). The exemption is bounded: exactly two deleted lines in workflow.md, both false under `--unattended`; the section applies only to a standalone `--unattended` token (workflow.md:70), so a person's run is unchanged (SA-1).
- Risk: Low

### Change 2: keep the count enforced
- Source: Variant 2 advocate, weakness 3 ("enforced only by the AC row's own annotation")
- Target: Variant 1, Evidence paragraph
- Approach: append
- Rationale: the `ac-c5.txt:18` text already reads "named exemption: exactly 2 deleted lines"; keep that wording so a third deleted line fails the review.
- Risk: Low

## Changes NOT Being Made
| Diff point | Non-base approach | Why rejected |
|------------|-------------------|--------------|
| S-002 / C-001 | B: leave `.dev/reflect/` in the Contract bullet and add a correcting line | The old path is false under `--output` (reflect.md:101 default vs the nested call at workflow.md:75); a coordinator would be pointed outside the report dir (WC-4) |
| X-001 | B2: keep "runs as today, without `--unattended`" and add an override | Contradicts spec line 62 and the sentence beside it; no precedence rule exists in WORKER-CONTRACT.md |
| C-003 | B/B2 test rewrite | `_check_workflow_reflect_wording` (test lines 1679-1686) would have to assert stale text is present; more change, not less |

## Risk Summary
| Change | Risk | Impact | Rollback |
|--------|------|--------|----------|
| 1 | Low | Wording only | Delete the added sentence |
| 2 | Low | Wording only | Delete the added sentence |

## Review Status
Auto-approved (no `--interactive`).
