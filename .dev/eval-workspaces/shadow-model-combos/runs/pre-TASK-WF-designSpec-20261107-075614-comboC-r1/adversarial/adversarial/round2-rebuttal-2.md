# Round 2 Rebuttal: Variant 2 (qa)

## Response to criticisms

1. **Seven blocking flags inflated (V1, V3).** Conceded. None of V2's findings blocks; my round 1 already withdrew them.
2. **F3 "no mechanism" (V3, X-002).** Conceded. Plan 124 says "one retry; `already in target state` counts as confirmed". What remains is a criterion gap: no criterion asserts that one-retry phrase.
3. **F1 and F6 overstated (V3).** Conceded. Spec 241 releases "before the CI re-poll", so "not held through ... CI" (plan 25) is consistent with it. Plan 170-172 assert content, so empty stubs would fail them.
4. **F2 should stay blocking (V1 rebuttal).** Partly conceded. The contradiction is literal (see the new evidence), but it comes from the spec: spec 241 carries both "no L3 or `draft` condition" and "at L3 with `--merge-guard off`". The task body narrows the test to "no `L3 only` or `draft` gate wording" (plan 137), so a builder can resolve it. MAJOR, not blocking.
5. **V2 missed the cross-cycle trace (V1).** Conceded as a miss. The finding is conditional, though (see below).

## Updated assessment of other variants

- **V1:** F1 is real and fails safe. F2 is narrower than claimed. Its "dependencies complete" claim is withdrawn.
- **V3:** Its findings are accurate and correctly graded MINOR. F1 is a literal breach of spec 363 only: Task 9 and Task 12 depend on Task 8, which declares `Depends on: Task 1` (plan 120), so the execution order still holds.

## New evidence

- **C-001:** Spec 59 and plan 137 require the bullet to say "no draft call is made". So the bullet must contain the word `draft`, and the literal reading of criterion 140 cannot pass. The defect is real but comes from the spec.
- **C-004:** Release row 9 has two causes. A `head_mismatch` comes after `push_completed`, so fix-1 is already published (spec 108). Only `push_not_completed` leaves a fix unpublished, and spec 69 treats that case as an exit. Neither the plan nor the spec shows a new cycle starting after a failed push. Plan 75 copies spec 107 and spec 322 faithfully. Blocking false.
- **C-007:** A push with a different id makes `held_cycle_published` false (spec 108), so resume holds. Safe; the criterion gap stays.
- **C-008:** Without `--undo`, verify fails (spec 234) and engage halts before any edit (spec 68). Safe, but the feature is inert.

## Final rulings

C-001: keep MAJOR false
C-002: keep MAJOR false
C-003: keep MAJOR false
C-004: keep MAJOR false
C-005: downgrade MINOR false
C-006: downgrade MINOR false
C-007: keep MAJOR false
C-008: keep MAJOR false
C-009: downgrade MINOR false
C-010: keep MINOR false
C-011: keep MINOR false
C-012: keep MINOR false
