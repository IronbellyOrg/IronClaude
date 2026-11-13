# Refactoring Plan

## Overview
- Base variant: Variant 1 (variant-1-original.md, analyzer card, sonnet class). Selected by tiebreaker level 1 (debate points won): V3 scored 0.800 against V1 0.753 (margin 0.047, under 5%); see base-selection.md.
- Incorporated variants: 2 and 3
- Total planned changes: 9; changes not made: 4
- Overall risk: Low (the merged output is a review card; no repository file is touched)
- Output: `merged-output.md` in `DIR/` (DIR = the adversarial/adversarial folder of this run). It is the merged reflect verdict: a short verdict, a findings table, an "open invariants" list and one fenced `findings-v2` block that holds exactly the merged findings listed below, in this order, with these severities and `blocking` flags.

## Planned Changes

### Change #1: Remove variant 1's withdrawn F9
- Source: variant 1, F9 (Task 5 over-claims `_NEW_KEY_DEFAULTS`)
- Rationale: withdrawn by its own advocate in Round 1 and confirmed not real by variant 3 in Round 2 (plan line 88 does not make that claim; line 175 is a different task). Integration: delete. Risk: Low

### Change #2: Fix variant 1's wrong line numbers
- Rationale: calibrator and the scorer found about 10 wrong anchors in variant 1 (spec cites about 39 lines low in the 4.1 type block, plan cites about 87 low for Tasks 3 to 5). Use the correct lines: source.md:112 (not 73), :82-85 (not 43-47), :88-91 (not 49-51), :107-109, :165-166; plan lines 60-62 (Task 3), 70-77 (Task 4), 124 (Task 8), 137-140 (Task 9), 76 (Task 4 RECONCILE criterion). Integration: replace. Risk: Low

### Change #3: Make F2 and F1 blocking as variant 1 has them, and add invariant INV-001 and INV-002 detail
- Source: invariant-probe.md INV-001 and INV-002; variants 2 and 3 for the repo evidence
- Merged F1 claim must say: the fix is not only to reuse `_repo_scoped`; the plan line 113 runtime clause (fake-gh argument log must show `--repo` or `repos/` on every call) also meets the `gh repo view` fallback, and the scan needs `_command_lines` and `_GH_CMD`. Merged F2 claim must say the three extra arguments are necessary but not sufficient (see Change #4). Risk: Low

### Change #4: Add a new blocking finding for the stale guard cycle id (variant 3 F8, probe INV-002)
- Source: variant 3 F8; debate U-005; both other advocates and variant 3 itself agreed blocking
- Claim: no fold row sets `cycle_id` (source.md:190-206), engage row 7 returns NOOP on a held guard (source.md:139), `held_cycle_published` keys on `guard.cycle_id` (source.md:108), resume row 4 releases on `published` (source.md:166); after a held release in cycle 1 and a crash in cycle 2 before its push, resume can release with cycle 2's fixes unpushed. Plan lines 62 and 77 test only single-cycle cases. Risk: Low

### Change #5: Add the untested producer payload (variant 2 F5, debate U-003)
- MAJOR, not blocking. Evidence source.md:184-185; plan lines 62, 124, 168-172. Fix: add spec section 4.2 to Task 8's sources and assert key format, retry suffix and first-request fields in the Task 11 trace test. Risk: Low

### Change #6: Set the calibrated severities from the debate
- F3 (halt reports released): MAJOR, not blocking (variant 2 withdrew its blocking flag; variant 3 and variant 1 agree). Add variant 2's fix text: a status override for the `draft_guard_unavailable` halt, with a test.
- F7 (Wave 0 wording): MINOR (variant 3 withdrew MAJOR; variant 1 and 2 agree).
- F4: MINOR, adopt variant 2's test form (settle, fold, status).
Risk: Low

### Change #7: Keep the three variant-1 MINOR findings that two of three variants confirmed
- F5 baseline before sync-dev (variant 3's bound: the two separate sync tests narrow but do not close it; variant 2 conceded), F6 JSON-to-GuardRead mapping (variant 2 conceded the plan names no owner), F8 resume row 3 check order (variant 2's correction: the "foreign toggle" reading is too narrow because source.md:119-124 allows one unsettled transition; the real gap is weak evidence for "no toggle landed"). Risk: Low

### Change #8: Add variant 3's two verified MINOR findings
- F10 classification keys: steps name only `gh pr`/`gh api` while `WRITE_VERB_RE` also hits git write verbs and multi-verb lines key as `a+b` (narrowed per its own concession: plan line 22 already names git verbs, the stale-entry test catches a miss).
- F9 (variant 3's numbering) pinned sentences compared by start text only (plan lines 33 and 154). Risk: Low

### Change #9: Add an "Open invariants" section from the probe (not findings)
- INV-003 (guard cycle id reused as push and re-trigger id), INV-004 (zero-edit cycle release site not placed in the SKILL criteria), INV-005 (a `not_applied`-erased first record leaves the interrupted cycle unguarded on resume), INV-006 (`applied_edits` not stored in events or fold). MEDIUM, single fault-finder source, not debated; listed as warnings, as the gate rule says. Risk: Low

## Changes NOT Being Made
| Diff point | Non-base approach | Rationale |
|---|---|---|
| U-002 (V1 F9) | Keep the `_NEW_KEY_DEFAULTS` over-claim | Not real (plan line 88). Removed. |
| X-001/X-002 rejections | Variant 2's "premise unverified" dismissals of baseline and mapping findings | Variant 2 withdrew them in Round 1 and 2. |
| U-004 (V2 F6) | A finding that the 66-row matrix is not exhaustive | Real but not a plan defect; kept only as a coverage note in the report. |
| Variant 3's F7 as MAJOR | Widened severity | Withdrawn by variant 3. |

## Risk Summary
| Change | Risk | Impact | Rollback |
|---|---|---|---|
| 1 to 9 | Low | Wording and severity of review findings only | Re-run the merge from this plan |

## Review Status
- Approval: auto-approved (non-interactive)
- Timestamp: 2026-11-13
