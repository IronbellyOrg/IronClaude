# Round 1 advocate, Variant 2

## Position summary
V2 is the only card that checks whether each criterion would fail on a wrong implementation, which spec 366 requires. Three of its criterion gaps hold: F5 (`--undo`), F7 (the auto-merge value) and F4 (cycle-id reuse). V2 over-used `blocking:true`: none of its seven blocking flags survives a careful read, and F1 and F3 are partly wrong.

## Steelman
- **V1.** F2 is the deepest finding of the three cards. After fix-1 ends in `HOLD` (spec 157), fix-2 gets `NOOP(already_held)` (spec 139) and, with zero edits, reaches `RELEASE(no_edits)` (spec 155). Plan 75 requires that release, which breaks spec 69. Critique: the defect is in the spec and the plan copies it faithfully. It depends on A-001. V1 files a "data-loss" category as non-blocking. It also claims the dependencies are complete, but Task 13 uses "the base-commit record of Task 1" (plan 195) and declares only Tasks 2, 10, 11 and 12 (plan 190-193).
- **V3.** Its F1 breaches an explicit plan rule: "one `Depends on:` line per dependency … the protocol tasks need the pre-build record" (spec 363). Tasks 9, 10 and 12 (plan 134-135, 148, 179-180) do not declare Task 1. Critique: V3 grades that breach MINOR, and it never tests whether a criterion can fail, so it misses C-003, C-007 and C-008.

## Strengths claimed
1. **F5.** The draft call needs `--undo` (spec 231). The Task 7 checks cover only "`--repo` or a `repos/` path" (plan 113). Plan 172 requires `--undo` only "for an originally draft PR". A script that leaves out `--undo` passes every criterion unless the fake `gh` keeps PR state, which the plan does not require.
2. **F7.** Engage row 11 carries `auto_merge_armed` in `notes` (spec 143). Task 4 asserts only "`action`, `reason` and `cause`" (plan 73), and Task 7 checks only that the `autoMergeRequest` key is present (plan 111).
3. **F4.** Spec 251 requires the push triad and `rereview_requested` to reuse the guard's id. Plan 127 and 129 check only where the id is minted, and plan 170 checks event order only.
4. **F10.** Task 10 says "byte-identical" but compares only "the literal start text" (plan 154).
5. **F9 and F11.** Plan 98 and 150 state the rule in the task body with no criterion, and no check covers the PR-body gate (spec 326).

## Weaknesses identified in other variants
1. V1's claim that the dependencies are complete is contradicted by plan 190-195.
2. V1 F2 gives no plan-versus-spec classification. It should be filed as a spec defect, not as plan drift.
3. V3 rates a breach of spec 363 as MINOR.
4. Neither applies the failability test of spec 366.

## Concessions
- **F1 is overstated.** "Not held through … CI" (plan 25) agrees with releasing "before the CI re-poll" (spec 241). Only the wrong label "non-goals" remains: MINOR.
- **F2 is not blocking.** The task body narrows the check to "no `L3 only` or `draft` gate wording" (plan 137), and the criterion wording comes from spec 241. MINOR.
- **F3 is wrong as written.** Plan 124 states "one retry; `already in target state` counts as confirmed", and spec 137, 169 and 205 carry the mechanism. The only gap left is that no criterion limits the release to one retry: MINOR.
- **F6 is overstated.** Plan 170-172 assert content, so empty stubs would fail them. MINOR.
- **F4, F5 and F7 stay MAJOR but not blocking.** F4 and F5 fail safe: they end in held or `verify_failed`.
- V1 F1 (plan 111 checks only that the timeline-count key exists) is a real gap that V2 missed.

## Shared assumptions
- **A-001 — QUALIFY.** The spec never says whether a new cycle follows a release `HOLD`. A `push_not_completed` may end the run, and "held_through_redrive" (spec 167) suggests the same cycle is redriven. A `head_mismatch` makes a continuing run plausible, so V1 F2 is a conditional spec risk.
- **A-002 — QUALIFY.** The principle is sound, and spec 366 mandates it. A criterion must still be read together with its task body and the other criteria of that task. Read that way, V2 F6 and V3 F3 and F4 shrink, while F5 and F7 survive.
