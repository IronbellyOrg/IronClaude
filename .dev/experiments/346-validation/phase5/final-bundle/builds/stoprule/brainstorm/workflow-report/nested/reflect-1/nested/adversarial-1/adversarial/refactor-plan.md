# Refactoring Plan

## Overview
- Base variant: Variant 1 (variant-1-original.md, reviewer-1 analyzer card)
- Incorporated: Variant 2 (QA-002), Variant 3 (R3-1 analysis, R3-3, R3-4, R3-5, R3-6 part, R3-10, R3-12, R3-A1), invariant probe (INV-001 to INV-009)
- Output: ../merged-verdict-card.md (a single merged finding card, YAML in a markdown file)
- Planned changes: 8; rejected: 4; overall risk: Low (additive and severity corrections)

## Planned Changes

- Change 1 (severity correction, base modify): F1 -> minor, F2 -> minor, F7 -> not-a-defect, F12 stays minor. Rationale: scoring matrix C-001, C-002, C-007 (unanimous after Round 2). Risk Low.
- Change 2 (base modify): F3 (C-003) stays the ONLY blocking finding; rewrite its claim with the Round 2 mechanism (V2/V3: without --re-review the ratchet is off and the per-claim late-found assertion fails; with it, begin exits 5 for lack of a sentinel prior) and its recommendation to also cover INV-001 (seal a second time or add checked lines for the 28 real changed hunks), INV-002 (fix the quote-line rule as the line the report cites, record it per claim, and do not derive the expected split from the code under test) and INV-003 (blocking reason: Task 7's fixture list names no prior report and the assertion can never pass, not merely an unstated design). Risk Low.
- Change 3 (base modify, from V3 R3-1 and INV-004): F4 (C-004) keeps minor; add that Task 10's equality test locks the Usage line in, and that the E-SKILL-MISSING rule as its own line is not in Task 10's replaced-block list. Risk Low.
- Change 4 (insert, from V2 QA-002): new finding C-009 minor: Task 3's first-pass form line must also keep `prior` so Task 6's count can exclude withdrawn carried priors; add a fixture with a withdrawn new MAJOR and a withdrawn carried MAJOR. Risk Low.
- Change 5 (insert, from V3): new minor findings C-014 (R3-3 positive wording checks), C-015 (R3-4 stage before running the git-tracked sweep), C-016 (R3-5 add tests/agents, tests/docs, tests/cli), C-018 (R3-10 section-5 templates need an owner citation or removal), C-020 (R3-12 allow one comment line), C-021 (R3-A1 Integration Patterns advisory). Extend F11 with R3-6 (stoprule.py and canaries.json in the src/superclaude scan; script-relative default rubric path). Risk Low.
- Change 6 (insert, from invariant probe): new MEDIUM-risk minor findings INV-005 (check/begin cannot recompute statuses from the report alone unless the ledger stores what they need), INV-006 (review number has two unchecked sources), INV-007 (one claim on an open prior double-counts M1), INV-008 (omitting --re-review resets the count, so the cap never fires), INV-009 (after a grader outage the NONE brief makes every real defect late-found next round). Risk Low.
- Change 7 (base keep): confirmed classification of the plan's declared deviations: Unattended-section removal = authorized (owner ruling), test_routing_refresh.py edit = necessary; deviation_counts {authorized: 1, necessary: 1, drift: 1 (C-018), regression: 0}. Risk Low.
- Change 8 (header): verdict line `blocking_findings: [C-003]`, merged convergence 0.97, provenance comments per finding. Risk Low.

## Changes NOT Being Made
- C-017 (R3-7 rubric hash read from artifact): consensus not-a-defect.
- C-019 (R3-11 category frontmatter): consensus not-a-defect; source.md 3.3 lists exact keys.
- C-007 (F7 INSTALL ordering): consensus not-a-defect.
- V2 QA-001 as blocking drift: conceded by its own advocate; merged as F12 minor.

## Risk Summary
All changes are additive or severity corrections to a findings card; rollback is the unmodified variant-1-original.md.

## Review Status
Auto-approved (non-interactive, --unattended), 2026-11-08T19:02:00Z.
