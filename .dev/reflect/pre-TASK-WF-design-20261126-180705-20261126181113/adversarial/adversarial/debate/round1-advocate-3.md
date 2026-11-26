# Round 1, advocate for Variant 3 (reviewer 3, refactorer, opus class)

- Depth: quick (only round). Focus: correctness, coverage, deviation classification. Custom instruction: none.
- Evidence: Read and Grep only, no command run. `PLAN` = the regenerated plan, `D` = its `source.md`, `REQ` = merged requirements, `ARCH` = the archived first plan.

## Position summary

Variant 3 is the only card that tested the repairs for second-order breakage: the M-05 fix's own Constraint is breached at Task 19 (C-002), the M-12 fix strips the fixtures' config isolation (C-003), and the M-18 base commit leaks into a permanent test that CI cannot run (C-004). But it missed C-001, which is real and Blocking, so its "M-10 resolved" is wrong. The right merge keeps V3's breakage rows, V2's C-001, and V1's C-007, C-009 and C-010.

## Steelman per opposing variant

- **V1:** It is the broadest tracker. It is the only card that re-checks M-12 to M-24, which the plan's goal (PLAN:15) promises to avoid. Its citations are accurate (PLAN:20, 28, 31). It found the test-first contradiction, the gap in Task 17 and the `record-skipped` ambiguity. It grades C-001 Medium because the stricter rule fails closed.
  Critique: failing closed matters only for the safety-boundary clause. The behaviour clause decides here, because FR-122 requires a single-key reply without a key to count. V1's claim that D:290-291 sit under a "Run with flag" table is inaccurate: only D:289 names the flag. V1 also ran out of turns.
- **V2:** It is the only card with the right grade and the right repair for C-001 (accept a reply without a key after one displayed key, reject it after several), and the only card that disposes of all 26 unnamed ids.
  Critique: "regressed" is the wrong category. ARCH:324 had no rule about replies without a key, and the first review said Task 28 "omits" it, so the repair added new Drift rather than breaking a working rule. Its single row for 38 tasks misses C-002, C-003, C-004, C-007 and C-009.

## Strengths claimed (Variant 3)

- C-002: `plugins/superclaude/commands/git.md` exists (Glob). PLAN:25 says to copy the twin and run `cmp` "in the same task". Task 19 (PLAN:234-238) does neither, and the copy waits until Task 25 (PLAN:294). A QA reviewer can quote the Constraint (`qa.md:52`, `:61`).
- C-003: the fixtures isolate config only through `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_NOSYSTEM` (`conftest.py:148-151`). `/etc/gitconfig:1-5` defines `filter.lfs`. Task 5's acceptance tests only the false case (PLAN:86).
- C-004: CI checks out at the default depth of 1 and runs the full suite (`test.yml:17`, `:47`), while PLAN:366 writes `git diff --quiet <base>` into a permanent test.
- Every prior-blocker status carries test-file evidence, not only plan lines.

## Weaknesses identified in the other variants

- V2: 1 row. It never checked whether the repairs for M-05, M-12 and M-18 created new defects.
- V1: grades a contradiction of a required behaviour (C-001) as Medium. C-014 is a risk under a budget the requirements fix (NFR-012), not a plan defect.

## Concessions

- **C-001 is real and Blocking.** PLAN:326 says "a reply that carries no key is not a resolution", but D:387 and REQ:606 say such a reply "counts only when exactly one key was displayed". No override is recorded (PLAN:19), and Task 34 pins the wrong rule (PLAN:386). My card's "M-10 resolved", citing PLAN:326 and 329, was wrong.
- C-008: V1 is right, the grade is Medium. PLAN:65 needs an input (index or mode) that `validate_argv(argv)` cannot carry, and Tasks 4 and 13 to 15 use that interface.
- My fix for C-003 is wrong for production. Letting the runner inherit `GIT_CONFIG_NOSYSTEM` would hide a real system filter. The right fix is a test-only environment injection plus a test where `snapshot_lossless` is true.
- My citations of the Constraints drifted: the Constraint on plugin twins is PLAN:25, not 34, and the T-16 override is PLAN:20, not 29.
- I did not raise C-007 or C-009, and I did not re-check M-12 to M-24.

## Shared assumption responses

- **A-001: QUALIFY.** Implement's halt model (`qa.md:52`) is the evidence for Decision-kind Blocking only. C-001 halts nothing: implement would build the stricter rule and pass its checks. It is Blocking under the review's rule because it misleads implement and changes a required behaviour.
- **A-002: QUALIFY.** Existing tests and CI are in scope because the plan names them (PLAN:20, the Task 38 gate, and "CI run repeats them" at PLAN:428). A fact about one machine (`/etc/gitconfig`) only shows a defect in a mechanism. It caps the grade at Medium unless one of the plan's own checks fails here. Following the M-18 precedent, a failure that appears only after the run is Medium.

## Per-point table

| point | superior treatment | right grade | verified | reason |
|---|---|---|---|---|
| S-001 | V1 | n/a | verified | Only V1 also re-checks M-12 to M-24 |
| S-002 | TIE | n/a | verified | V1 and V3 are both consistent; V2 has one row |
| C-001 | V2 | Blocking | verified | PLAN:326 against D:387 and REQ:606; changes the required behaviour and the pins of Tasks 28 and 34 |
| C-002 | V3 | Blocking | verified | Quotable breach of PLAN:25 at Task 19; same class as M-01 and M-05 |
| C-003 | V3 | Medium | verified | PLAN:72 drops all `GIT_*` variables; `filter.lfs` makes the result always false here; Task 5's check is one-sided |
| C-004 | V3 | Medium | verified (CI run UNVERIFIED) | Depth-1 checkout; the test breaks only after the run (M-18 precedent) |
| C-005 | V3 | Medium | verified | The override at PLAN:20 covers Task 32 only, but PLAN:306 allows Task 26 entries; conditional (`test_implement_severity_static.py:296`, `:420-434`) |
| C-006 | V3 | Medium | verified | The bare form at PLAN:359 clashes with the `E-COMMIT-PRECONDITION` form at PLAN:356 only if Task 26 writes that literal |
| C-007 | V1 | Blocking | verified | PLAN:28 requires test-first per task including text; Tasks 20-23, 26-31 and 33 write no test; quotable like M-01; D:458 |
| C-008 | V1 | Medium | verified | PLAN:62 against PLAN:65; conceded |
| C-009 | V1 | Medium | verified | REQ:580 cases are missing from PLAN:215-216; the task body includes them by reference ("cases of T-19") |
| C-010 | V1 | Medium | verified | PLAN:158 stops any unflagged run, but `record-skipped` carries no flag condition; D:289-291 |
| C-011 | V1 | Note | UNVERIFIED | `git version` is a builtin, so either form works |
| C-012 | V1 | Note | verified | D:228 gives no token; a false pointer that any token satisfies (PLAN:173) |
| C-013 | TIE | Note | verified | PLAN:349 against PLAN:31; same result |
| C-014 | V1 | Note | UNVERIFIED | The budget is fixed by NFR-012; about 10 lines seem needed |
| C-015 | V3 | Note | verified | `archive_workspace.py:44-67` holds 11 patterns; the named nine match 187-197 |
| C-016 | V3 | Note | verified | PLAN:428 defers the check to CI |
| C-017 | V3 | Medium | verified (CI runner config UNVERIFIED) | D:374 gives filters as an example; PLAN:83 makes any filter refuse; fails closed; a question for the owner |
| C-018 | V2 | Note | verified | No NFR-013 in the plan; `head_before` and `head_after` partly cover it; M-27 precedent |
| C-019 | V2 | n/a | UNVERIFIED (per id) | A disposition, not a finding; 17+8+1=26 holds |
| X-001 | V2 (qualified) | n/a | verified | M-10 is open, but its category is Drift, not Regression (ARCH:324) |
| X-002 | V2 | n/a | verified | Blocking; failing closed only bears on the safety clause |
| X-003 | V1 | n/a | verified | Medium |
