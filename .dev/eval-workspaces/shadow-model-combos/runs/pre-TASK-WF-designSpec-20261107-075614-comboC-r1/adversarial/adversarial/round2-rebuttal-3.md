# Round 2 Rebuttal: Variant 3 (refactorer)

## Response to criticisms

1. **"No behavioural findings" (V1, V2).** Conceded. V3 audits order and structure, and missed the `--undo` and `notes` gaps. Its "no drift" verdict also missed the loose attribution at plan line 25. That is a scope limit, not an error in what it did report.
2. **F1 "transitively covered" (V2).** Conceded as a weight point. Task 9 and Task 12 reach Task 1 through Task 8 (plan 120), so execution order holds. It still breaches spec 363 ("one `Depends on:` line per dependency"), and V1 withdrew its "dependencies complete" claim. Stays MINOR.
3. **F3 arguable (V3 round 1).** Conceded. Adding a classification entry is an addition, not an edit of an "existing test expectation", so the contradiction is weak. It stays MINOR, low confidence.
4. **F2 and F4.** Not contested. F4 is a plain conditional against an unconditional criterion (plan 108 vs 113).
5. **"V3 confirmed T1 F2 with no recorded severity."** Accepted. I record it now (C-001 below).

## Updated assessment of the other variants

- **V1:** Its F1 is real and fails safe, since an unreadable count HOLDs the PR. F2 is its strongest finding but its blocking flag does not survive (see C-004).
- **V2:** The advocate withdrew the blocking flags and the "no mechanism" claim. Plan 124 states the retry. Its criterion gaps (F4, F5, F7) are real.

## New evidence

**C-004: can a later cycle follow a release HOLD?** The spec supports the path in part.
- Engage row 7 (spec 139) returns `NOOP(already_held)` when `guard.phase == HELD`. A run can therefore see HELD at a later engage.
- Release row 9 (spec 157) holds and leaves the phase HELD. Spec 275 also leaves it HELD after a validation failure.
- A zero-edit later cycle then meets release row 7 (spec 155, `applied_edits == 0`), which comes before row 9. It would release with `no_edits`.
- Against that: the `head_mismatch` cause has already pushed, so nothing is lost. Only `push_not_completed` leaves a fix unpublished. Nothing in spec 139, 147-157, 164-171 or 274-281 shows a new cycle starting after that case; resume row 5 (spec 167) keeps HELD through a redrive instead.
- Verdict: the scenario is reachable in principle but not shown. The rule is spec text copied faithfully into the plan, so it is a spec gap. MAJOR, not blocking.

**C-001:** Spec 241 says the Wave 0 bullet "contains no L3 or `draft` condition" and also that "at L3 with `--merge-guard off`" it prints the unprotected line. The first clause is about whether the bullet applies, the second is its content. The plan's task body (137) narrows the test to gate wording, so a builder can resolve it. A literal reading of criterion 140 fails. MINOR, not blocking.

## Final rulings

C-001: downgrade MINOR false
C-002: keep MAJOR false
C-003: downgrade MINOR false
C-004: keep MAJOR false
C-005: downgrade MINOR false
C-006: downgrade MINOR false
C-007: downgrade MINOR false
C-008: keep MAJOR false
C-009: downgrade MINOR false
C-010: keep MINOR false
C-011: keep MINOR false
C-012: keep MINOR false
