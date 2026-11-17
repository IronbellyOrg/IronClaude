# Refactoring Plan

## Overview
- Base: Variant 1 (`variant-1-original.md`). Incorporate: Variant 2 findings, Variant 3 finding, INV-001 and INV-002..004 as advisory.
- Planned changes: 6. Rejected: 3. Overall risk: Low (additive findings; severities and blocking flags set by the Round 2 rulings).
- Review: auto-approved.

## Planned Changes
1. Replace V1's per-finding blocking flags with the Round 2 rulings: every merged finding non-blocking (V2 withdrew blocking on its F1; V1 and V3 recorded F4 and F5 non-blocking; V2's F4 blocking vote lost 2 to 1).
2. Append V2's findings F1-F11 as merged findings M-004, M-009, M-010, M-011, M-012 (source: debate points C-007..C-012).
3. Append V3 F1 as M-013 (C-013, plan:49).
4. Add INV-001 as M-005 (HIGH unaddressed invariant; released PR with an unpublished earlier fix) and INV-002..INV-004 as advisory M-014.
5. Merge V1 F1 with V2 F4 into M-001 (cycle id binding and once-per-cycle share one root).
6. Re-state V1 F5 as M-006 with the Round 2 note that the spec never says where resume gets `target_sha`.

## Changes NOT Being Made
- V2 F1 blocking: dropped, fails closed (release row 9 holds, spec 157).
- V1 F5 blocking: dropped (needs two simultaneous conditions; V2 and V3 non-blocking).
- V2 F4/V1 F4 blocking vote: dropped (engage row 6 is not reached on the engage-failure trace, spec 274).

## Final merged findings (authoritative table for the merged output)

SPEC = `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md`; PLAN = `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md`.

| ID | Sev | Blocking | Category | Sources | Claim | Citations |
|---|---|---|---|---|---|---|
| M-001 | MAJOR | no | missing-requirement | V1 F1, V2 F4 | The guard record's cycle_id is never set or rebound by any fold row, yet held_cycle_published and resume row 4 key on it; engage row 7 returns NOOP for a later cycle, and no decision row enforces once-per-cycle (a RELEASED guard re-engages at row 11). | SPEC 190-206, 139, 143, 108, 166; PLAN 52-60, 168 |
| M-002 | MAJOR | no | contradiction | V1 F2 | Task 8 builds refs/merge-guard.md from spec sections 3, 4.1, 4.5, 4.6, 5 while the spec says it carries sections 3 and 4.1 to 4.4; event fields, key format and the --read JSON are not required by any criterion. | SPEC 240; PLAN 124 |
| M-003 | MAJOR | no | missing-requirement | V1 F4 | After a failed first engage the guard is RELEASE_PENDING with owned_draft false and engage row 6 holds without re-checking the live draft; reachable on resume or a later cycle, not covered by any task criterion. | SPEC 199, 138, 170; PLAN 60, 70 |
| M-004 | MAJOR | no | unpassable-check | V2 F1, F9 | No criterion checks that the protocol passes this cycle's applied_edits (not the run-wide count) to release_decision, and Task 1's O1 criterion passes whether or not a single cycle-id source exists. Fails closed. | SPEC 107, 366, 251; PLAN 75, 37, 127-130, 166 |
| M-005 | MAJOR | no | safety | INV-001 | Release row 7 (zero edits) precedes the head check, so a zero-edit cycle after a committed but unpublished earlier cycle releases the PR while that earlier fix was never pushed; the plan tests only a zero after a published cycle. Unresolved HIGH invariant. | SPEC 155-156, 69, 107; PLAN 75 |
| M-006 | MAJOR | no | contradiction | V1 F5 | Resume row 4 (published) is evaluated before rows 5 and 6, and the spec never says where resume gets target_sha; task 4 tests published=True only with no dangling branch. | SPEC 166-168, 156; PLAN 77 |
| M-007 | MINOR | no | contradiction | V1 F3 | The spec says a draft_guard_unavailable halt reports unavailable, but read-failed and unreadable-timeline engage halts write no event, so guard_status returns released; plan pins no record at ordinal 3 as released. | SPEC 112, 135, 140; PLAN 61 |
| M-008 | MINOR | no | contradiction | V1 F6, F7 | guard_status OFF wording can hide a held draft that resume row 2 must report, and resume row 6 has no phase condition unlike row 5. | SPEC 112, 164, 167-168; PLAN 61, 77 |
| M-009 | MINOR | no | missing-requirement | V2 F3 | One cycle id shared by guard events, push key and rereview_requested is required; the acceptance trace asserts event order only. | SPEC 251; PLAN 170 |
| M-010 | MINOR | no | missing-requirement | V2 F5 | The PR body release-gate statement and the --merge-guard off rule for the opening run have no producing task and no criterion. | SPEC 326; PLAN 33, 182 |
| M-011 | MINOR | no | missing-requirement | V2 F6, F7, F8, F10, F11 | Several stated requirements sit only in task bodies: Task 9 flag and wave-line tests, the no file:NNN rule outside Task 8, original_is_draft never re-read, the engage-failure message; Task 10 lacks a Depends on Task 8 line. | PLAN 137, 139-144, 124, 128, 148, 129; SPEC 363, 369, 274 |
| M-012 | MINOR | no | unpassable-check | V2 F2 | The byte-identical check compares live text with a start-text constant, so a changed tail would pass; weak because the spec mandates literal constants. | PLAN 154; SPEC 377 |
| M-013 | MINOR | no | unpassable-check | V3 F1 | Task 2's grep criterion for 43 is a judgment call because a legitimate 42nd-43rd comment remains. | PLAN 49 |
| M-014 | MINOR | no | other | INV-002..004 | Advisory: a conflict cycle arriving while the guard is HELD, the trace holding by construction, and the auto-merge disarm note have no criterion. | SPEC 149, 143, 333, 270; PLAN 166, 170, 153 |

## Risk Summary
All changes are additive text; rollback = discard `merged-output.md`.

## Review Status
auto-approved
