# Round 2 rebuttal, advocate for Variant 3

## Response to criticisms

- **F4 rated MAJOR is too high (V1 R1 and R2, my own R1).** Conceded, and the cause is in the spec. The existing pins are fragments: `test_static_grep.py:672` pins "Pre-push head guard, before `push_decision`", and lines 886-890 pin an S5a fragment that ends in "post". Spec 377 calls a comparison against those constants "byte-identical", and plan 154 copies the claim. The overclaim starts in spec 377 and conflicts with spec 342 (O4); plan 21 (add after, never inside) reduces the risk. New grade: MINOR, spec-origin.
- **F1 overstated.** Conceded in part. Spec 6, 57 and 60 support three of the six limits. Only commit statuses, rulesets and concurrent runs are invented by the plan.
- **"`not_applied` covered in both directions" (V2 R1).** Conceded in part. Plan 60 covers both directions, which is what spec 376 asks for. It misses the `RELEASE_PENDING` return in spec 201, so V1 F6 is right.
- **F8 (my own R1).** Conceded. Spec 373 names only `gh pr` and `gh api`, while spec 255 also names the git write verbs. Plan 22 states the broader rule for the whole plan.
- **Missed the state-tracking gaps (C-002, C-003, C-004, C-010).** Conceded. V3 is the weakest card for deciding whether the plan can go ahead.

## Updated assessment of V1 and V2

- **V2.** Its F1 and F2 are blocking and spec-origin; I accept both. Row 4 at spec 166 re-enters `release_decision`, whose row 8 (spec 156) needs `target_sha`. Spec 109 gives `resume_decision` no `target_sha`, so no test for row 4 can be written.
- **V1.** F2 and F3 are plan-origin MAJORs and matter more at run time than any V3 finding.

## New evidence

1. The fragment pins at `test_static_grep.py:672` and 886-890 show that F4 starts in the spec.
2. This session's `git status` lists `?? docs/memory/reflect/...`, an untracked file outside the roots plan 200 allows. A correct build can fail that criterion, so F2 stands.
3. Spec 363 says "the protocol tasks need the pre-build record". Tasks 9 and 12 (plan 134-135, 179-180) still omit Task 1, so F6 breaks an explicit example in the spec.

## Points still split

- **C-005.** V1 is superior on how the gap works: MAJOR, non-blocking, limited to the named tests with no assertion bullet. Engage failure (FR-15) and the release retry (FR-16) have no behaviour criterion anywhere; plan 129 only checks that phrases are present. Decisive line: plan 169 requires names only, and plan 170-172 assert only the trace, crash and forbidden-call tests.
- **C-020.** V1 and V3 are superior. Decisive line: plan 172 forbids any `pr ready` call at ordinal 2 or with `off`, and plan 73 returns `NOOP` there.
- **X-004.** Yes, empty test bodies pass for those named tests. V1 is superior. Decisive line: plan 173 requires only that `uv run pytest tests/pr_submit -q` passes.

Overall: for deciding whether the plan can go ahead, V2 is best, V1 second and V3 third. V3 is best for exact fixes to the plan's wording.

## Revised V3 findings

| Finding | Severity | Blocking | Origin |
|---|---|---|---|
| F1 limits labelled as spec non-goals | MINOR | no | plan-origin; only commit statuses, rulesets and concurrent runs (plan 25) |
| F2 `git status` criterion | MINOR | no | plan-origin; spec 301 says only "Never stage `.claude/`" |
| F3 Phase string values | MINOR | no | spec-origin (spec 80 gives names only); Task 3 should pin lowercase values |
| F4 "byte-identical" check | MINOR (was MAJOR) | no | spec-origin (spec 377 conflicts with spec 342) |
| F5 `file:NNN` ban unchecked | MINOR | no | plan-origin, best practice (not covered by the spec 366 bar) |
| F6 Depends-on lines incomplete | MINOR | no | plan-origin; breaks spec 363 |
| F7 Wave 8 test is weak | MINOR | no | plan-origin, best practice |
| F8 git write verbs | MINOR | no | spec-origin (spec 373 conflicts with spec 255) |

Not checked: whether the fragment pins existed before the feature was added to this tree.
