# Round 1 advocate 3 (variant 3)

**Variant 3 advocate, Round 1**

**Position summary.** Variant 3 is the most precise card on how the plan is written. It is the only card that checks the plan's own claims against the spec's plan-authoring rules (spec §10, lines 362-378), and it has the most complete dependency finding. Its real weakness is coverage: it missed the four high-impact gaps in how the guard tracks state (C-002, C-003, C-004, C-010). V1 and V2 caught those, and I concede them below.

**Steelman**

- **V1 (analyzer).** V1 found the gaps that matter most at run time. These are the release-retry rule (FR-16) with no table row or cap, the cycle id that is never checked to be shared, and the guard getting stuck on `HOLD(ownership_unproven)` after a failed engage (spec 138 and 199). V1 also says outright that the Wave 0 contradiction was "copied from spec lines 59 and 241". That is the right way to classify a defect that starts in the spec. Its PR-body finding (C-017) and its finding on the `not_applied` return to `RELEASE_PENDING` (C-018, spec 201 against plan 60) are both correct.
- **V2 (qa).** V2 has the strongest single finding, C-010. Spec 109 gives `resume_decision` no `target_sha` and no per-cycle `applied_edits`. Yet row 4 (spec 166) must "re-enter `release_decision`", which needs both, and plan 77 tests that re-entry. V2 is also the only card that uses the blocking flag to separate findings, and its Caveats section (the working tree already holds the feature) is honest about what grounding could not check.

**Strengths claimed**

1. **Most complete dependency audit (C-007).** Spec 363 requires one `Depends on:` line for every task whose output is consumed. The plan breaks this in several places:
   - Task 9 uses the pins recorded in `pre-build-gate.md` (plan 137) but declares only Tasks 6 and 8 (plan 134-135).
   - Task 12 does the same (plan 182) and declares only Tasks 6 and 8 (plan 179-180).
   - Task 10 declares only Task 9 (plan 148), but it extends Task 8's test file and compares against Task 1's record (plan 154).
   - Task 13 declares the indirect Task 2 but not Task 1, whose record it compares against (plan 190-199).

   V2's F10 names only Tasks 10 and 13.
2. **Phase string values are never defined (C-013).** Spec 80 gives `Phase` member names with no values. Task 3 tests use `HELD` (plan 60). Task 5 asserts `"held"` and `engage_pending` (plan 90). A `str` Enum with uppercase values or `auto()` would pass Task 3 and fail Task 5. Only V3 found this.
3. **The "byte-identical" check only compares the start of each sentence (C-006).** Plan 154 claims a byte-identical check but compares only "the literal start text" (plan 33). Spec 342 (O4) says "the S5a text must stay unchanged". V3 cites both, and the same gap appears in V2's F6.
4. **Spec §10 checks no other card did.**
   - The `file:NNN` ban (spec 369) is never checked. Plan 128's criteria leave it out.
   - The Wave 8 test is weaker than the Wave 6 test (plan 153 against spec 241).
   - The per-task classification steps cover only `gh pr` and `gh api` (plan 108, 124), while spec 255 also covers the git write verbs.
5. **Correct deviation classification.** I re-read plan 25 and spec 1-60:
   - "Commit statuses", "rulesets" and "concurrent" do not appear anywhere in the spec, so labelling them "non-goals of ./source.md" misattributes them.
   - V3 graded its confirmations of earlier findings as MINOR/other rather than inflating them.
   - V3 also refuted an earlier coverage row: INF-073 is covered by plan 200.

**Weaknesses identified in others**

1. **V2:F9 (C-020) is refuted by the plan itself.** Three places already cover a guard that does nothing below ordinal 3:
   - plan 73: engage at ordinal 2 and with `mode=OFF` returns `NOOP`;
   - plan 166: "ordinals 0 to 2 and `off` make no call";
   - plan 172: the fake `gh` log has no `pr ready` call at ordinal 2 or with `off`.
2. **V2:F4 (C-009) should not be blocking.** Any static text test can only check that phrases are present. Plan 153 already makes the test fail when either phrase is deleted. A sentence that contains both phrases but drops the condition is a review-quality risk, not something that stops the plan from running.
3. **V2:F11 (C-019) misreads plan 60.** The plan says the parametrized test "covers every row" and then lists extra cases that must each fail if the row is wrong. The list adds to full coverage; it does not replace it. Spec 376 asks for exactly those extra cases.
4. **V1:F5 (C-005) is overstated.** Plan 170-172 add real assertions on top of the twelve test names: the exact event order, crash windows built from a real `detect_crash_window`, and forbidden calls checked on `RunLog.read_events()`. Not every test passes as an empty stub. V2's narrower F7 (missing cases) is accurate.
5. **V2 marks spec defects as blocking plan findings.** C-010 comes straight from the signature in spec 109. The plan reproduces it faithfully (plan 70, 77). It should be reported as a spec defect that blocks readiness, not as the plan drifting from its spec. V1:F1 makes this distinction; V2 does not (see A-002).

**Concessions**

- V3 missed C-001, C-002, C-003, C-004 and C-010. It said it read spec §4.5-§10 but did not look closely at the release, retry and resume rows in §4.1-§4.2. That is a real hole in the state-mechanics review.
  - C-002: the retry cap appears only in plan 124 prose and a test name (plan 169).
  - C-003: there is no check that the guard, the push triad and `rereview_requested` share one id (spec 251 against plan 127 and 170).
  - C-010 is the most serious finding on the table.
- V3's F2 overreads plan 200. "Changes only under ... gitignored `.claude/` mirrors" is an allowlist, so the ignored-mirror wording is dead text, not a check that would fail. The real point is the second half: there is no exception for untracked files that already existed outside those roots.
- V3's F1 overstates its case. "No labels" comes from the spec ("draft not label", spec 6), and "conflict cycles never engaged" comes from spec 57. Only commit statuses, rulesets and concurrent runs are invented by the plan.
- V3's MAJOR on F4 (C-006) is arguably too high. Spec 377 asks for constants "taken from the existing pins", and if those pins are prefixes, the plan matches them. The defect is the false "byte-identical" label, so V2's MINOR is better calibrated.
- V3's F8 is softened by the spec itself. Spec 373 also names only `gh pr` and `gh api`, and the worker-contract test run in each task would catch an unclassified line.

**Shared assumptions**

- **A-001: QUALIFY.** Spec 366 requires criteria that "a wrong implementation would fail" only for the fold, `guard_status`, resume-reason and per-cycle `applied_edits` rules. Applying the same bar to the Wave 8 test, the `file:NNN` check or the byte-identical check is reasonable practice, but it is not something the spec requires. Those findings, including V3's F5 and F7, should be tagged as best practice and not as spec deviations.
- **A-002: QUALIFY.** If the plan faithfully copies a spec that contradicts itself (spec 241) or leaves something out (spec 109, 138/199, 315), that is not drift. Report these as defects that start in the spec. They still count against readiness when they make a task impossible to write as stated; C-010 and C-001 are examples. All three cards should have tagged where each defect started. V1:F1 is the only one that did.

**Per-point table**

| Point | Level | Better treatment | Reason |
|---|---|---|---|
| S-001 | L2 | V2 | Only card that separates findings with the blocking flag, though F4 is graded too high. |
| S-002 | L1 | V2 | Widest valid coverage, despite the F9 and F11 overreach. |
| S-003 | L1 | V2 | The Caveats section states grounding limits (A-004). |
| C-001 | L1 | V2 | Correct MINOR grade plus a concrete fix (target the ref-load gate). |
| C-002 | L3 | V2 | Adds that `already_in_state` is not a value the script prints. |
| C-003 | L3 | V2 | Adds that switching the guard `off` must leave the cycle id unchanged. |
| C-004 | L3 | V1 | The resume path makes the stuck `HOLD` live, not latent. |
| C-005 | L2 | V2 | Case omissions are accurate; V1's stub claim ignores plan 170-172. |
| C-006 | L2 | tie | V3 cites more evidence (O4, spec 377); V2 has the better severity. |
| C-007 | L2 | V3 | Also names Tasks 9 and 12 and the indirect Task 2 inconsistency. |
| C-008 | L2 | V2 | Unique and valid: spec 230 shows a boolean, but gh returns an object or null. |
| C-009 | L2 | V2 | Valid point, but should be non-blocking. |
| C-010 | L3 | V2 | Strongest finding; should be tagged as starting in the spec. |
| C-011 | L1 | V3 | Unique; partly overstated (labels come from spec 6). |
| C-012 | L2 | V3 | Unique; the base-commit exception half is the real point. |
| C-013 | L2 | V3 | Unique and real conflict between plan 60 and plan 90. |
| C-014 | L1 | V3 | Unique; spec 369 rule with no check. |
| C-015 | L2 | V3 | Unique; Wave 8 test weaker than Wave 6. |
| C-016 | L2 | V3 | Unique; softened by spec 373. |
| C-017 | L2 | V1 | Unique; PR body has no producing task. |
| C-018 | L3 | V1 | Unique; spec 201 branch is untested. |
| C-019 | L3 | V1/V3 (tie) | V2 misreads plan 60. |
| C-020 | L2 | V1/V3 (tie) | V2:F9 is refuted by plan 73, 166 and 172. |
| X-001 | L1 | V2 | Wording defect that can be fixed, so MINOR. |
| X-002 | L2 | V2 | Spec 377 is met literally; MINOR is the better grade. |
| X-003 | L3 | V1 | `HOLD` with no defined handling, reachable on resume. |
| X-004 | L2 | V2 | V1 ignores plan 170-172. |
| X-005 | L2 | V1/V3 (tie) | Staying silent was correct. |

**Bottom line:** V2 wins most points, V3 wins every point on how the plan is written (C-007, C-011 to C-016), and V1 wins C-004, C-017, C-018 and the X-003 severity question. Nothing needs to be done before Round 2.

Files read:
- `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/eval-workspaces/shadow-model-combos/runs/pre-TASK-WF-designSpec-20261107-075614-comboC-r2/adversarial/adversarial/variant-{1,2,3}-original.md`
- `.../diff-analysis.md` in the same directory
- `/home/coder/workspaces/worktrees/IronClaude/brainstorm-reflect-panel/.dev/eval-workspaces/shadow-model-combos/input/TASK-WF-designSpec-20261107-075614/{TASK-WF-designSpec-20261107-075614.md,source.md}`

I checked every claim against the plan and spec text only. I did not read the code or the test files the cards mention (for example `test_worker_contract.py`).
