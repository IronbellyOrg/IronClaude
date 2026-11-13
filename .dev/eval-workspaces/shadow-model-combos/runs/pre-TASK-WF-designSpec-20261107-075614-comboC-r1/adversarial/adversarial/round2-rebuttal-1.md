# Round 2 Rebuttal: Variant 1 (analyzer)

## Response to criticisms

1. **"F2 is a spec defect, not a plan deviation" (V2, V3). Partly conceded.** The origin is spec L107: "a zero-edit cycle after a fixing cycle still releases with `no_edits`." But spec L6 says "an exit with unpublished fixes keeps the PR draft", and L69 keeps the PR draft unless there is "zero-edit proof". Plan L75 turns the release into a passing criterion, so a faithful build ships it. It is spec-origin and plan-pinned, and it breaks an owner decision. It stays blocking.

2. **"A-001 is unstated" (V2).** Conceded as a qualifier. The trace needs a run that continues after a release-row-9 HOLD. The design expects that path: engage row 7 (L139) returns `NOOP(already_held)` for a second engage while HELD. If the run halts after HOLD, the finding narrows to a note.

3. **"Data loss filed as non-blocking; dependencies complete" (V2).** Conceded. The flag was wrong and I withdraw "complete". V3 F1 holds: Task 9 cites `pre-build-gate.md` (plan L137) with no Task 1 line.

4. **Missed V2's F3, F5 and F7 (my round 1).** F5 (`--undo`, spec L231) and F7 (`notes`, spec L143) are real. F3 is a criterion gap, not a missing mechanism: plan L124 says "one retry; `already in target state` counts as confirmed".

## Updated assessment of other variants

- **V2:** Its advocate withdraws most of its blocking flags, and I accept F1, F3 and F6 as MINOR. F2 stays blocking. Its "L3 only" reading comes from the test sentence at plan L137, but the acceptance criterion at L140 binds: it fails any bullet that "names an L3 or `draft` condition", and spec L59 requires the off line at L3. F4, F5 and F7 are real criterion gaps.
- **V3:** F1, F2 and F4 are real. F3 is arguable. Its lack of behavioural findings is a scope limit, not an error.

## New evidence

- Task 7's `transitions` feeds `classify_toggles` (spec L118, L120). A script that prints a fixed count gives `observed < run_toggles`, which is `unreadable`, so every release HOLDs (release row 5, L153). Task 7's criteria (L111) would still pass. The result is a held PR, not a wrong release, so V1 F1 is MAJOR and non-blocking.
- A missing `--undo` is caught by the verify step: "A verification mismatch after a mutation is `ok:false, error:"verify_failed"`" (spec L234). That also fails safe.

## Final rulings

C-004: keep MAJOR true
C-001: keep MAJOR true
C-002: keep MAJOR false
C-003: keep MAJOR false
C-007: keep MAJOR false
C-008: keep MAJOR false
C-005: downgrade MINOR false
C-006: downgrade MINOR false
C-009: downgrade MINOR false
C-010: keep MINOR false
C-011: keep MINOR false
