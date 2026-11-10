Implementer claims (A3 brief run + its repair, not verified):
- Followed T5_brief-3.md: unlabelled_blocking() reads every id-cell row outside the resolution section with no severity label and counts it blocking unless parse_grade reads it non-blocking; header rows skipped.
- Resolution rows with no status word make the report unparseable (exit 2, FAIL).
- held_cm skips a held id only when review 3 already labels it CRITICAL or MAJOR.
- Repair 3-1: a status-word row is skipped as a resolution row only when all its ids are review-2 ids (so new R3 ids with a status word count).
- Believed T5.AC1-AC3 met (100 tests pass). Known gap from the repair re-review: a status-word row of a closed review-2 id graded blocking is skipped, so DISAGREE is missed.
