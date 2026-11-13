# Refactoring Plan

## Overview
- Base: Variant 2 (reviewer-2 card). Output: a merged verdict `merged-output.yaml` (list of merged findings M-1..M-15 with origin and severity), derived from the V2 findings block plus incorporated findings.
- Incorporated variants: V1 (4 findings), V3 (7 findings), invariant probe (INV-011 plus 3 MEDIUM notes).
- Changes planned: 15 merged findings (see below). Overall risk: Low (additive and re-grading only).

## Planned Changes
Severity and blocking come from the Round 2 concessions. "Origin" is where the defect starts (A-002).

| M | Source | Claim (one line) | Severity | Blocking | Origin | Rationale |
|---|---|---|---|---|---|---|
| M-1 | V2:F1 | `resume_decision` row 4 re-enters `release_decision` but gets no `target_sha` or per-cycle `applied_edits`; the folded state holds neither | MAJOR | true | spec | C-010, 3 of 3, 95% |
| M-2 | V2:F2 + V1:F2 | FR-16 retry-once, `already_in_state` and `release_pending` have no table row, fold rule or criterion; the script never prints `already_in_state` | MAJOR | true | spec + plan | C-002, 85% |
| M-3 | V2:F3 + V1:F3 | no criterion ties guard, push triad and `rereview_requested` to one `cycle_id`, nor `off` invariance | MAJOR | false | plan | C-003, 90%; V2 conceded non-blocking |
| M-4 | V2:F4 | Task 10 Wave 3 test passes any sentence holding both phrases | MAJOR | false | plan | C-009, 80%; V2 conceded non-blocking |
| M-5 | V1:F5 + V2:F7 | Task 11 criterion requires test names only for tests with no assertion bullet; case list omits moved head, unreadable timeline, FR-17 exits | MAJOR | false | plan | C-005, X-004, 70 to 80% |
| M-6 | V1:F4 + V2:F12 | after a failed draft settle the fold is `RELEASE_PENDING` with `owned_draft` false, so a later engage returns `HOLD(ownership_unproven)` and no document says what the SKILL does on that HOLD (resume path) | MINOR | false | spec | C-004, X-003 |
| M-7 | V2:F5 + V1:F1 | Task 9 criterion rejects "an L3 or `draft` condition" while the same bullet must say "at L3 with off" | MINOR | false | spec | C-001, X-001; reword the test to target the ref-load gate |
| M-8 | V2:F8 | `autoMergeRequest` is an object or null in `gh`; no text converts it to the boolean of spec 230, no criterion tests values or the `transitions` count | MINOR | false | spec + plan | C-008 |
| M-9 | V1:F7 | PR body and the opening run's `--merge-guard off` have no producing task | MINOR | false | plan | C-017 |
| M-10 | V1:F6 | `not_applied` of a ready request returning to `RELEASE_PENDING` after a failed release is untested | MINOR | false | plan | C-018 |
| M-11 | V3:F4 + V2:F6 | "byte-identical" check compares only fragments; the existing pins are fragments | MINOR | false | spec | C-006, X-002 |
| M-12 | INV-011 | the fsync-request-before-call order exists only as ref prose; add an ordering assertion on the ref text and a spy or log-order check in Task 11 | MAJOR | false | plan | invariant probe, adopted |
| M-13 | V3:F6 + V2:F10 | `Depends on:` lines incomplete (Tasks 9, 10, 12, 13) | MINOR | false | plan | C-007, 90% |
| M-14 | V3:F1, F2, F3, F5, F7, F8 + V2:F11 | hygiene: non-goals label, git-status wording, Phase string values, `file:NNN` check, Wave 8 test, git write verbs, fold list incompleteness | MINOR | false | plan or spec | C-011 to C-016, C-019 |
| M-15 | INV-001, 003, 004, 009 | spec-origin warnings: `guard.cycle_id` never advances, zero-edit release over an unpublished earlier fix, landed branch not matched to the guard's cycle, drafting disarms auto-merge | MINOR | false | spec | invariant probe MEDIUM items (warnings, not debated) |

## Changes NOT Being Made
- V2:F9 (inertness below monitor 3): withdrawn by its own advocate; plan 73 and 172 cover it (C-020).
- V1:F1 MAJOR and V3:F4 MAJOR: kept at the lower severity agreed in Round 2.
- V1:F4 "edits may proceed unguarded" on the direct path: refuted by spec 274 (engage failure halts); only the resume path remains (M-6).
- V2:F3 and F4 blocking flags: dropped to non-blocking.

## Risk Summary
All changes are re-gradings or additions of findings; no content is deleted. Risk: over-incorporation of minor hygiene items (M-14) dilutes the verdict; they are grouped into one row.

## Review Status
Auto-approved (non-interactive).
