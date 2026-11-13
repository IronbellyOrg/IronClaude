# Round 1 advocate 1 (variant 1)

## Position summary

V1 is the most conservative card and has the cleanest calibration on coverage gaps traceable to spec text (FR-16 retry, shared cycle_id, PR body and flag, ready-request `not_applied`). It misses several real plan defects that V2 and V3 caught, and it overrates two findings (F1, F5). I argue V1 is a sound but incomplete base, not the best card overall.

## Steelman

**V2.** V2 is the most thorough and the only card to find a design-level hole. F1 is real: `resume_decision` takes `mode, ordinal, guard, read, pending, dangling_branch, published` (spec 109), but row 4 re-enters `release_decision`, which needs `applied_edits` and `target_sha` (spec 107, 166). V2 also grounded F4 in the plan text: the Wave 3 test (plan 153) checks only that two phrases are present. Its `blocking` flags separate decision-critical items from polish. It pairs severity with an explicit fix, for example "reword the test to target the ref-load gate" in F5. It also states its grounding limit openly: the working tree already holds the feature.

**V3.** V3 is precise and cheap to act on. F4 is correct: plan 154 compares only "the literal start text" of the pinned sentences, so a later edit to either sentence passes a "byte-identical" claim. F6 is the most complete Depends-on audit (spec 363 says a task depends on every earlier task whose output it consumes). F2 (plan 200: plain `git status --short` never lists ignored files) and F3 (Phase string values undefined in Task 3 but lowercase in Task 5, plan 90) are checkable facts. V3 also carries a good "covered, no gap" list, including the INF-073 refutation.

## Strengths claimed

1. **FR-16 retry gap (F2).** The one-retry rule appears only as ref prose (plan 124) and a test name (plan 169). V1 reached it independently, and V2 agrees at MAJOR.
2. **cycle_id gap (F3).** Plan 127 and 170 assert event order only. Spec 251 requires one source shared by the guard, `push_idempotency_key` and `rereview_requested`. V1 and V2 agree.
3. **Spec-gap handling (F4).** V1 notes that spec 138 and 199 produce an engage that returns `HOLD(ownership_unproven)` with no stated consequence for edits. Spec 274 halts a failed engage. But `resume_decision` row 8 (spec 170) also yields that HOLD on a later resume, where nothing says edits stop.
4. **Calibration.** V1 states each finding's nature in its prose, "a wording problem more than a logic one" for F1. It marks nothing blocking.
5. **Unique, valid gaps.** F7 is a real gap: spec 326 says the PR-opening run must pass `--merge-guard off`, and the plan only records it in Task 1 (plan 33). F6 is also valid: the `not_applied` return to `RELEASE_PENDING` (spec 201) is untested. Task 3 line 60 covers only the `HELD` return.
6. **Verified-not-a-gap.** V1 correctly checked that no SKILL front-matter grant is needed for Task 7.

## Weaknesses identified in others

1. **V2 F1 may be a SKILL-level step, not a plan flaw.** The SKILL can supply `target_sha` from the dangling push event, and the plan does not forbid that. Blocking at MAJOR is generous, though the row 4 test, as written, is unspecified.
2. **V2 F3 and F4 are over-flagged.** Four blocking findings out of twelve, while V2's own F12 is latent by its own admission.
3. **V2 F9 and F11 are weak.** "Inert below monitor 3" is already covered by plan 73 and 172, as V1 notes (see X-005). F11 lists fold rows that plan 60's "every row" wording arguably already covers.
4. **V3 F4 is overrated at MAJOR.** Plan 154 says the constants are "as the existing pins write them", and existing pins already protect those sentences. The risk is prefix-only coverage, which is MINOR.
5. **V3 is thin on behaviour.** It raises no FR-level coverage gaps and no state-machine issue. Seven of its eight findings are MINOR hygiene.
6. **V3 F1 is a labeling quibble.** Plan 25 says "non-goals of ./source.md", and V3 itself notes the spec has no non-goals section.

## Concessions

1. V1 F1 is overrated. A MAJOR rating against its own "wording problem" description is inconsistent. V2's MINOR is better calibrated.
2. V1 F5 is partly refuted. Plan 170-172 do contain behavioural criteria: trace order, forbidden-call assertions and crash tests with real recovery. Only plan 169, the test-name criterion, is names-only. V2's "case omissions" framing is more accurate.
3. V1 missed C-010 (resume inputs), C-006 (prefix-only byte-identical check), C-009, and the Depends-on gaps.
4. V1 marks nothing blocking even though F2 and F3 are execution-critical. That makes it less useful for gating.
5. V1 F4's "edits may proceed" overstates it. Spec 274 halts a failed engage first, so the path needs a later resume.

## Shared assumptions

- **A-001: ACCEPT.** Spec 366 sets failability as the yardstick, and all three cards use it. It is the right test, though it should be explicit in the card.
- **A-002: QUALIFY.** Measuring the plan against the spec is correct, but a plan fault that the spec itself carries (V1 F1 against spec 241; V1 F4 and V2 F12 against spec 138 and 199) should be labeled spec-origin, not scored as a plan defect. Only the plan-introduced faults are plan faults.

## Per-point table

| Point | Level | Superior |
|---|---|---|
| S-001 | L1 | V2 (blocking flag separates critical items; V1 uses none) |
| S-002 | L1 | tie |
| S-003 | L1 | tie |
| C-001 | L1 | V2 (MINOR is better calibrated) |
| C-002 | L3 | V2 (adds that `already_in_state` is not a script output) |
| C-003 | L3 | V2 (adds off-mode invariance; V1 comparable) |
| C-004 | L3 | V1 (states the resume consequence; V2 only calls it latent) |
| C-005 | L2 | tie (V1 sees the stub risk; V2 sees the missing cases) |
| C-006 | L2 | V3 (MAJOR is over-rated, but it has the fuller reading) |
| C-007 | L1 | V3 (the complete list) |
| C-008 | L2 | V2 |
| C-009 | L2 | V2 |
| C-010 | L3 | V2 |
| C-011 | L1 | V3 |
| C-012 | L1 | V3 |
| C-013 | L2 | V3 |
| C-014 | L1 | V3 |
| C-015 | L2 | V3 |
| C-016 | L1 | V3 |
| C-017 | L2 | V1 |
| C-018 | L3 | V1 |
| C-019 | L3 | V2 |
| C-020 | L2 | V2 |
| X-001 | L1 | V2 |
| X-002 | L2 | V2 (MINOR; the existing pins mitigate it) |
| X-003 | L3 | tie (V1 sees the resume path, V2 the halt ordering) |
| X-004 | L2 | tie (V1 right that line 169 is names-only, V2 right on 170-172) |
| X-005 | L2 | V1 (notes plan 73 and 172 already cover it) |
