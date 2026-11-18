<!-- Base: Variant 1 (variant-1-original.md) -->
<!-- Merged: 2026-11-13 by merge-executor; plan: refactor-plan.md; incorporated V2 findings, V3 finding, INV-001..INV-004 -->

# Merged reflection verdict (UC-1 pre, design spec v3 vs plan)

Citation key. SPEC = `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/source.md`. PLAN = `.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/TASK-WF-designSpec-20261107-075614.md`. Numbers are line numbers.

## Verdict
<!-- Source: refactor-plan.md Overview and Planned Changes 1; debate-transcript.md Convergence Assessment -->

0 blocking findings, 6 MAJOR and 8 MINOR non-blocking. The plan is executable with amendments. Convergence is 0.9524 (20 of 21 diff points) with status BLOCKED_BY_INVARIANTS, because INV-001 (merged as M-005) stays unaddressed at depth standard; no Round 3 runs at that depth.

## Merged findings

### M-001
<!-- Source: Variant 1 F1 + Variant 2 F4 (plan change 5) -->
- Severity: MAJOR
- Blocking: no
- Category: missing-requirement
- Sources: V1 F1, V2 F4
- Claim: The guard record's cycle_id is never set or rebound by any fold row, yet held_cycle_published and resume row 4 key on it; engage row 7 returns NOOP for a later cycle, and no decision row enforces once-per-cycle (a RELEASED guard re-engages at row 11).
- Citations: SPEC 190-206, 139, 143, 108, 166; PLAN 52-60

### M-002
<!-- Source: Variant 1 F2 -->
- Severity: MAJOR
- Blocking: no
- Category: contradiction
- Sources: V1 F2
- Claim: Task 8 builds refs/merge-guard.md from spec sections 3, 4.1, 4.5, 4.6, 5 while the spec says it carries sections 3 and 4.1 to 4.4; event fields, key format and the --read JSON are not required by any criterion.
- Citations: SPEC 240; PLAN 124

### M-003
<!-- Source: Variant 1 F4 -->
- Severity: MAJOR
- Blocking: no
- Category: missing-requirement
- Sources: V1 F4
- Claim: After a failed first engage the guard is RELEASE_PENDING with owned_draft false and engage row 6 holds without re-checking the live draft; reachable on resume or a later cycle, not covered by any task criterion.
- Citations: SPEC 199, 138, 170; PLAN 60, 70

### M-004
<!-- Source: Variant 2 F1, F9 (plan change 2; debate points C-007..C-012) -->
- Severity: MAJOR
- Blocking: no
- Category: unpassable-check
- Sources: V2 F1, F9
- Claim: No criterion checks that the protocol passes this cycle's applied_edits (not the run-wide count) to release_decision, and Task 1's O1 criterion passes whether or not a single cycle-id source exists. Fails closed.
- Citations: SPEC 107, 366, 251; PLAN 75, 37, 127-130, 166

### M-005
<!-- Source: INV-001 from invariant-probe.md (plan change 4) -->
- Severity: MAJOR
- Blocking: no
- Category: safety
- Sources: INV-001
- Claim: Release row 7 (zero edits) precedes the head check, so a zero-edit cycle after a committed but unpublished earlier cycle releases the PR while that earlier fix was never pushed; the plan tests only a zero after a published cycle. Unresolved HIGH invariant.
- Citations: SPEC 155-156, 69, 107; PLAN 75

### M-006
<!-- Source: Variant 1 F5, restated with Round 2 note (plan change 6) -->
- Severity: MAJOR
- Blocking: no
- Category: contradiction
- Sources: V1 F5
- Claim: Resume row 4 (published) is evaluated before rows 5 and 6, and the spec never says where resume gets target_sha; task 4 tests published=True only with no dangling branch.
- Citations: SPEC 166-168, 156; PLAN 77

### M-007
<!-- Source: Variant 1 F3 -->
- Severity: MINOR
- Blocking: no
- Category: contradiction
- Sources: V1 F3
- Claim: The spec says a draft_guard_unavailable halt reports unavailable, but read-failed and unreadable-timeline engage halts write no event, so guard_status returns released; plan pins no record at ordinal 3 as released.
- Citations: SPEC 112, 135, 140; PLAN 61

### M-008
<!-- Source: Variant 1 F6, F7 -->
- Severity: MINOR
- Blocking: no
- Category: contradiction
- Sources: V1 F6, F7
- Claim: guard_status OFF wording can hide a held draft that resume row 2 must report, and resume row 6 has no phase condition unlike row 5.
- Citations: SPEC 112, 164, 167-168; PLAN 61, 77

### M-009
<!-- Source: Variant 2 F3 -->
- Severity: MINOR
- Blocking: no
- Category: missing-requirement
- Sources: V2 F3
- Claim: One cycle id shared by guard events, push key and rereview_requested is required; the acceptance trace asserts event order only.
- Citations: SPEC 251; PLAN 170

### M-010
<!-- Source: Variant 2 F5 -->
- Severity: MINOR
- Blocking: no
- Category: missing-requirement
- Sources: V2 F5
- Claim: The PR body release-gate statement and the --merge-guard off rule for the opening run have no producing task and no criterion.
- Citations: SPEC 326; PLAN 33, 182

### M-011
<!-- Source: Variant 2 F6, F7, F8, F10, F11 -->
- Severity: MINOR
- Blocking: no
- Category: missing-requirement
- Sources: V2 F6, F7, F8, F10, F11
- Claim: Several stated requirements sit only in task bodies: Task 9 flag and wave-line tests, the no file:NNN rule outside Task 8, original_is_draft never re-read, the engage-failure message; Task 10 lacks a Depends on Task 8 line.
- Citations: PLAN 137, 139-144, 124, 128, 148, 129; SPEC 363, 369, 274

### M-012
<!-- Source: Variant 2 F2 -->
- Severity: MINOR
- Blocking: no
- Category: unpassable-check
- Sources: V2 F2
- Claim: The byte-identical check compares live text with a start-text constant, so a changed tail would pass; weak because the spec mandates literal constants.
- Citations: PLAN 154; SPEC 377

### M-013
<!-- Source: Variant 3 F1 (plan change 3; debate point C-013) -->
- Severity: MINOR
- Blocking: no
- Category: unpassable-check
- Sources: V3 F1
- Claim: Task 2's grep criterion for 43 is a judgment call because a legitimate 42nd-43rd comment remains.
- Citations: PLAN 49

### M-014
<!-- Source: INV-002..INV-004 from invariant-probe.md (plan change 4) -->
- Severity: MINOR
- Blocking: no
- Category: other
- Sources: INV-002..004
- Claim: Advisory: a conflict cycle arriving while the guard is HELD, the trace holding by construction, and the auto-merge disarm note have no criterion.
- Citations: SPEC 149, 143, 333, 270; PLAN 166, 170, 153

## Unresolved
<!-- Source: debate-transcript.md Convergence Assessment and Round 2 notes; invariant-probe.md; base-selection.md -->

- INV-001 / M-005: HIGH invariant, UNADDRESSED. Blocks convergence under the invariant gate; no Round 3 at depth standard. Note from the probe: its row-7 citation was off by one and the correct line is SPEC 155 (reflected in M-005's 155-156).
- S-001: V3 layout versus V1 layout. Reviewers agreed it is layout only and of low impact; no agreement on a superior layout (50%), left unresolved.
- Quote-not-found flags: 8 of V2's 47 citations lost markdown backticks in their quotes. The debate checked 3 (PLAN 75, SPEC 107, SPEC 366: stripped backticks). The other 5 of 8 were not checked by anyone.

## Changes not made
<!-- Source: refactor-plan.md "Changes NOT Being Made" -->

- V2 F1 blocking vote: dropped; the gap fails closed (release row 9 holds, SPEC 157).
- V1 F5 blocking: dropped; the bypass needs two simultaneous conditions, and V2 and V3 recorded it non-blocking.
- V2 F4 / V1 F4 blocking vote: dropped; engage row 6 is not reached on the engage-failure trace (SPEC 274). The vote lost 2 to 1.
