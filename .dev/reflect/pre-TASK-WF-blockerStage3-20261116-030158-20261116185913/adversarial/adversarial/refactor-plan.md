# Refactoring Plan: merged review card for the stage 3 plan, third review

## Overview
- Base variant: Variant 2 (`variant-2-original.md`, reviewer-2, qa, opus)
- Incorporated: Variant 1 (`variant-1-original.md`, reviewer-1, analyzer, haiku) and the invariant probe (`invariant-probe.md`, INV-001 to INV-004)
- Output: `../merged-review-card.md` (path relative to this folder) plus `merge-log.md`
- Final numbering F1 to F15 (new, replaces both cards' numbering); earlier-review findings are written "earlier F1 to F16" in a separate section so the two numberings never collide
- Final grades: 3 blocking (F1, F2, F3), 12 non-blocking (F4 to F8 Medium, listed under `## Follow-up candidates`; F9 to F15 minor)
- Review status: auto-approved

## Planned Changes

| Change | Source | Target | Rationale |
|--------|--------|--------|-----------|
| 1 | V1 F1 + V2 F4 + INV-003 (a), (b) | merged F1 (blocking) | R1b has no outcome word below min n in the expected case; R3 and ADVISORY/NOT-MEASURABLE overlap are the same hole (C-002, X-001; both advocates 62 to 65 percent) |
| 2 | V2 F1 | merged F2 (blocking) | Unequal-panel threshold (C-003, X-002; both advocates 72 percent) |
| 3 | V2 F5 + INV-001 | merged F3 (blocking), regraded from non-blocking | Fix pass and ladder can switch a rule file after a failed gate; Tasks 7 to 10 read only the registry row (INV-001 HIGH) |
| 4 | INV-002 + V2 F5 context | merged F4 (Medium) | Task 4 cannot reach PASS in the expected undersized case; resume path unstated |
| 5 | V2 F2 | merged F5 (Medium), regraded from blocking | Vacuous positive grep lines (C-005; both advocates ended at non-blocking, consequence is lost prose) |
| 6 | V2 F3 + V2 F10 (first half) | merged F6 (Medium), regraded from blocking | Unedited label-floor and relay lines (C-006, C-012; both advocates ended at non-blocking) |
| 7 | INV-003 (c), (d) | merged F7 (Medium) | Validity of reviewers judged after grades are read; R1 gloss |
| 8 | INV-004 | merged F8 (Medium) | Old-arm precondition not checked |
| 9 | V1 F2 | merged F9 (minor), regraded from blocking | `verify` against `verify-citations` (C-004) |
| 10 | V2 F8 | merged F10 (minor) | "two" against three test files |
| 11 | V2 F6 | merged F11 (minor) | Stage 4 reads Rule 6 bold form |
| 12 | V2 F9 | merged F12 (minor) | Scan breadth against SPEC:920, no current miss |
| 13 | V2 F10 (second half) | merged F13 (minor) | L1 text omits `reasked` and "listed first" |
| 14 | T1 card F2 | merged F14 (minor) | Stale base text in SRC |
| 15 | T1 card F5 + INV-005 | merged F15 (minor) | Entry-check gaps |

## Changes NOT Being Made
- V2 F7 (coverage matrix has no rows for SRC:12, :13, :14 and several bullets) is dropped: it reviews the orchestrator's `coverage-matrix.yaml`, not the plan, and V2 itself found each row covered by hand (C-009; both advocates 80 percent "not a plan defect"). The one mechanically unmapped row (INF-002, the stage 0b and 0c evidence) is covered by hand in Task 1 (PLAN:42); the card lists it under Checked.
- The V2 F10 premise that rf-qa.md lines 389 and 476 are "named in Task 7's body" is dropped (no such line number appears in PLAN); the underlying gap is kept in F6.
- V2's claim that the unequal threshold "reverses" PLAN:80's bias statement is softened in F2: the directions are stated for the panel-size effect only, and the confound's own bias is left as the plan states it.
- INV-005 minor guard gaps are folded into F15; INV-006 to INV-008 are checked items, not findings.

## Risk Summary
Low: all changes are text assembly from verified card text; every finding's evidence was re-read in the debate and again at the Wave 5 gate.

## Review Status
Auto-approved (non-interactive).
