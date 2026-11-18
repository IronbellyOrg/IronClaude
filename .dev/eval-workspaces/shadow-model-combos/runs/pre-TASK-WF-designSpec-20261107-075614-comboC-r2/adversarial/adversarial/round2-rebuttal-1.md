# Round 2 rebuttal, advocate for Variant 1

## Response to criticisms

- **F1 overrated (V2, V3, my own R1 concession).** Conceded. I re-read plan 138 and 140. The task body (plan 138) bans only "`L3 only` or `draft` gate wording", which a correct bullet can satisfy. The acceptance criterion (plan 140) bans "an L3 or `draft` condition", which it cannot. So the defect is one criterion worded more broadly than its own task text, copied from spec 241. Downgrade to MINOR.
- **F5 stub-passing is overstated (V2, V3).** Partly conceded. Plan 170-172 do carry behavioural bullets: trace order, crash windows built from the real `detect_crash_window`, and forbidden-call checks. Those cover only three of the twelve tests. Plan 169 is the only criterion that touches the other nine (retry, external toggle, missing timeline, moved head and others), and it checks names only. My claim stands for those nine and is wrong as a blanket claim.
- **F4 "edits may proceed" (V2, V3).** Conceded as stated. Spec 274 halts a failed engage before any edit. Spec 138 row 6 and spec 199 (`settled(draft, failed)` leaves `owned_draft` unchanged) still make `HOLD(ownership_unproven)` reachable on a later `--resume`. Neither document says what the SKILL does on that HOLD. That narrower gap holds.
- **No blocking flags (S-001).** Conceded as a usefulness gap. My F2 and F3 are execution-relevant, but a missing criterion is not a stop-the-line defect, so I keep both non-blocking. I accept that V2's flag is more informative.
- **Missed findings (C-010, C-006, C-009, C-007).** Conceded.

## Updated assessment of V2 and V3

- **V2.** Strongest card on state mechanics. F1 (resume inputs) is real, but it is spec-origin: spec 109 and 166 define `resume_decision` without `target_sha`, and plan 70 and 77 copy them. F9 and F11 are weak. Plan 166 and 172 prove no `pr ready` call at ordinals 0 to 2 and with `off`. Plan 60 says "every row" and then lists extra cases, which adds to the coverage. F4 is real but not blocking.
- **V3.** Best on plan hygiene (C-007, C-013, C-014). F4 at MAJOR is too high. Spec 377 asks for constants "taken from the existing pins", so the real defect is the "byte-identical" label, which is MINOR. It missed every state-mechanics gap, so it is the least useful card for gating.

## New evidence

- Plan 138 and plan 140 disagree with each other on what the Wave 0 test bans. This is checkable and shows F1 is fixable inside the plan.
- Spec 274 makes the failed-engage halt a spec rule, so the F4 risk exists only on the resume path.
- Plan 169's first bullet requires only that test names be defined, and no later bullet maps to the retry test or the moved-head test.

## Points still split

- **C-005.** Position: V2 is better calibrated; V1's finding survives only for the nine unasserted tests. Decisive line: plan 169 requires names alone, while plan 170-172 assert only the trace, crash and forbidden-call tests. Superior: V2, narrowly.
- **C-020.** Position: V2 F9 is refuted. Decisive line: plan 172 requires "no `pr ready` call at ordinal 2 or with `off`", and plan 73 returns `NOOP` there. Flag-parse inertness is covered by Task 6. Superior: V1 and V3 (silence was correct).
- **X-004.** Position: stubs pass only for the nine tests with no assertion bullet. The blanket "Task 11 passes on empty stubs" is false. Decisive line: plan 170 names the exact event order that the trace test must assert. Superior: V2 on severity (MINOR), with V1's mechanism accepted.

Overall: V2 is the best card, V3 second on hygiene, V1 third. V1's unique findings F6 and F7 are valid but low value.

## Revised V1 findings

| Finding | Severity | Blocking | Origin |
|---|---|---|---|
| F1 Wave 0 contradiction | MINOR (was MAJOR) | no | spec-origin (spec 241); plan 140 widens it |
| F2 FR-16 retry has no criterion | MAJOR | no (V2 blocking is defensible) | plan-origin: spec 315 gives the test name and the plan never adds a case |
| F3 shared cycle_id | MAJOR | no | plan-origin: plan 37 accepts "no id minted today", spec 251 requires one source |
| F4 HOLD with no SKILL action on resume | MINOR (was MAJOR) | no | spec-origin (spec 138 and 199); plan copies it |
| F5 Task 11 weak criteria | MINOR (was MAJOR), narrowed to nine tests | no | plan-origin |
| F6 `not_applied` return to RELEASE_PENDING untested | MINOR | no | plan-origin: spec 201 vs plan 60 |
| F7 PR body and opening-run flag have no task | MINOR | no | plan-origin: spec 326 vs plan 33 |

Not checked: gh's runtime behaviour, and the code or test files the cards mention. Risk: all line cites come from the plan and spec text read this session.
