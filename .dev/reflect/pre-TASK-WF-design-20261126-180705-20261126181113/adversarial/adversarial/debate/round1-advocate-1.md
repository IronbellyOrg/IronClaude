# Round 1 advocate: Variant 1 (reviewer-1, analyzer, sonnet)

## Position summary

V1 is the best card on prior-item tracing and on plan-internal contradictions (C-007, C-009, C-010, C-012). It is wrong on the headline item: it graded the Task 28 no-key rule (C-001) Medium, and under this review's grading rule that is Blocking. V3 is the best card on cross-checks against the repo and the machine (C-002, C-003, C-004, C-017). V2 found the one item V1 saw and graded correctly, but covered little else. The right merged result has 2 Blocking rows (C-001, C-002), neither of which V1 graded Blocking.

## Steelman

- V2: it read the design line for line and found that M-10's repair introduced a contradiction with FR-122, and it refused to count "repair present" as "resolved". It is the only card that tied the finding to a changed acceptance check (Task 34's pin). Its 26-id table is a real coverage service, and a spot grep found no active definition for the ids it calls inactive.
- V3: it opened the live machine and CI. `/etc/gitconfig` does define `filter.lfs.clean`. `.github/workflows/test.yml` uses `actions/checkout@v4` with no `fetch-depth` and runs the whole `pytest` suite. The plugin twin `plugins/superclaude/commands/git.md` exists. These are facts V1 never checked, and V3 got the Blocking call on Task 19 right.

## Strengths claimed (with evidence)

- C-007: `source.md:560` records the first review's M-20 (test-first order not carried into the plan). The regenerated plan only adds a Constraint line (PLAN:28) while Tasks 20-23 and 26-33 still put their pins last (Tasks 24, 34). V1 alone saw this.
- C-009: FR-109 (`merged-requirements.md:580`) says "Cover: ..." for about 12 cases. Task 17's acceptance lists three. Task 17 cites FR-102 to FR-108, not FR-109. V1 alone raised it.
- C-012: `source.md:228` names a `why` token for every path rule except `.dev/implement/`, so Task 13's "the `why` the design names" has no referent. This is true but harmless, so the right grade is Note.

## Weaknesses in the other variants

- V2: one row and one reviewer; it missed C-002, C-004 and C-009.
- V3: it missed C-001 and called M-10 resolved on the strength of PLAN:326. C-003's proposed fix (keep config-isolation variables in the runner) would hurt production, because preflight must read the person's real config (`hooks_path`, `submodule_recurse`, `snapshot_lossless`). Isolation belongs in the tests, through a narrow keep-list. V3 also cites the plugin-twin Constraint at PLAN:34. In the file it is the bullet at line 25 (line 34 is the Phase 1 heading). C-005 is over-graded: Task 26 itself instructs the `_ALLOW` entry and the override record, and the new STOP rows do not match `_SITE`.

## Concessions

- C-001: Task 28 (PLAN:326) says a no-key reply is never a resolution. `source.md:387` and FR-122 (`merged-requirements.md:606`) say it counts when exactly one key was displayed. No recorded override exists, and Constraint line 19 says the design wins. Correcting it changes Task 28's required behaviour and the Task 34 pin, so the grade is Blocking. V1's Medium was wrong because it used "does it halt `/sc:implement`" and not the review's rule.
- C-002: Task 19 breaches the twin Constraint (PLAN:25). `refs/qa.md:52,61` makes a quotable Constraint breach a blocking finding. V3 is right.
- C-008: Note (V3). C-011: Note, and `git version` is a valid git subcommand. C-012: Note. C-014: NOT-A-DEFECT, because the 15-line cap is NFR-012 and V1's own count was about 12.
- C-010: the ambiguity is real, but V1 misdescribed the design table. Rows 290-291 carry no "Run with flag" header (only row 289 does). It stays Medium because Task 12's test table must pick an answer.

## Shared assumptions

- A-001: QUALIFY. The deciding test is the review's rule (a change to a decision, required behaviour, acceptance check or number). Halting `/sc:implement` is sufficient evidence, as in C-002, but not necessary: C-001 fails closed and still must be Blocking.
- A-002: QUALIFY. Existing tests and the CI workflow count, because the plan's own gate runs them (Task 38). Machine facts count where a plan step runs on that machine (this worktree). The GitHub runners' `/etc/gitconfig` is UNVERIFIED. Without a named acceptance that fails, these findings stay Medium.

## Per-point table

point | superior | right grade | verified | reason
---|---|---|---|---
S-001 | TIE | n/a | verified | layout only; V2's id table adds coverage but is not structure
S-002 | TIE | n/a | verified | V1 and V3 grade consistently
C-001 | V2 | Blocking | verified | PLAN:326 vs `source.md:387` and FR-122; no override; changes Task 28 and the Task 34 pin
C-002 | V3 | Blocking | verified | twin exists; Constraint at PLAN:25 (V3 cited 34); Task 19 has no copy or `cmp`; qa.md B4
C-003 | V3 | Medium | UNVERIFIED runtime | `/etc/gitconfig` and the conftest isolation are real; no named acceptance fails; V3's fix needs a test-side keep-list
C-004 | V3 | Medium | verified | CI depth 1 plus the full pytest run; Task 32 lists the base-commit diff among test cases; local acceptance passes
C-005 | V3 | Note | UNVERIFIED | Task 26 itself instructs the entry and the override record; whether Tasks 30/31 add halt/Ruling lines is unverified
C-006 | V3 | Medium | verified | Task 34's "reasons appear only in commit-step.md" clashes with the `index-locked` token Task 26 puts in SKILL.md; the lifecycle pin matches only `E-RESUME-NEEDED reason=`
C-007 | V1 | Medium | verified | `source.md:560` (M-20) still open; the Constraint is unfollowable in Tasks 20-23, 26-33
C-008 | V3 | Note | verified | signature gap, trivially resolved; no task depends on the exact signature
C-009 | V1 | Medium | verified | FR-109 lists far more cases than Task 17's acceptance; the T-19 pointer keeps it from Blocking
C-010 | V1 | Medium | verified | PLAN:158, 216 vs 316; a record-skipped versus stop precedence for an unflagged run is undefined
C-011 | V1 | Note | UNVERIFIED | wording; `git version` is a valid subcommand; runner interplay not run
C-012 | V1 | Note | verified | `source.md:228` names no token; nothing tests it
C-013 | TIE | Note | verified | `git diff` against the index vs the recorded base commit
C-014 | NONE | NOT-A-DEFECT | UNVERIFIED | the budget comes from NFR-012; about 7-12 lines needed against 15
C-015 | V3 | Note | verified | `archive_workspace.py:44-67` holds 11 compiled patterns; the nine named are exact
C-016 | V3 | Note | UNVERIFIED | Task 38 already says CI repeats the checks; the word-list test was not read
C-017 | V3 | Medium | verified (CI part UNVERIFIED) | Task 5 makes `snapshot_lossless` false for any filter config; with lfs here every boundary refuses; fails safe
C-018 | V2 | Note | verified | FR-022 (Task 20 body) covers the content; no acceptance; first review treated it as Note
C-019 | V2 | n/a | verified (spot check) | coverage table; not a finding
X-001 | V2 | n/a | verified | M-10's repair is present but pins a rule contradicting FR-122, so "regressed" is accurate in substance
X-002 | V2 | n/a | verified | Blocking, per the concessions above
X-003 | V3 | n/a | verified | Note
