# Round 1 advocate, variant 3 (refactorer)

## 1 Position
Variant 3 found the three defects the harness rests on: a stop rule the client cannot trigger, no whole-run spend check, and no defined freeze step for the manifest. It over-graded two fixable items, which I concede.

## 2 Steelman of variants 1 and 2
- V1 grades most carefully. It alone found that Gate 1 refuses `UNSET`, which the design's Gate 1 does not (plan:103; source.md:72), and that T-05 has no band mapping (plan:71,76). Its Medium on C-001 and C-002 holds if the tests at plan:124-125 would expose the gaps anyway.
- V2 is the tightest card, all on Task 6, the part that spends money. Its C-003 point is true: `live=False` returns only `dry_run` (client.py:127-131), so the CLI dry run checks nothing past budgeting.

## 3 Strengths of variant 3
- F-1 covers every path: `BudgetExhausted` is caught and returned (client.py:114-117), `model_mismatch` arrives as `invalid` (validate.py:32-33; client.py:170-174), dry runs are refusals (client.py:127-131), so "rerun on any non-ok" (plan:119) reruns them all.
- F-2 names the fix already in the library, `reserve_phase` (budget.py:63-70).
- F-3 shows `tests_passed` carries one hash (plan:101) while Gate 2 compares "hashes" (plan:103).
- It is the only card with a `blocking_reason` on every finding, and the only one to find C-009, C-010, C-012 and C-013.

## 4 Weaknesses of variants 1 and 2
- V1 grades C-001 Medium, but the design requires the estimate (source.md:82) and no task has it. It grades the grep check Blocking-Decision (plan:47), though the grade rule calls a fixable check not Decision.
- V2 grades an import phrase Blocking-Decision (plan:117). It fails loudly, and `jevlib.client` already holds every name (client.py:10-15,21-26). Its C-003 Blocking ignores the reason at plan:30: a mock dry run in the CLI needs `live=True` and a key (client.py:133), which conflicts with checking the gates before reading the environment (plan:119). It misses C-006 and C-007.

## 5 Concessions
- F-5 (git status) is a fixable check, so Medium, not Decision.
- F-4 (README rescore) should be Medium: the rescore code and its test exist (plan:84,90), and plan:156 names the scorer's subcommands.
- F-7: `Journal` sets `schema: jev-journal/1` and does not sort keys (journal.py:18,29), but events need sorted keys (plan:101). Reusing it is not a clean fit.
- F-2's fix also needs `release_phase` at run end. Otherwise undrawn reservations stay committed in the shared ledger (budget.py:54,98-100).
- V3 missed C-008 and C-014.

## 6 SCORING
C-001 | valid yes | grade Blocking-Missing | confidence 75 | source.md:82; plan:119,124; budget.py:63-70
C-002 | valid yes | grade Blocking-Decision | confidence 78 | plan:119,125; client.py:114-117,127-131,170-174; validate.py:32-33
C-003 | valid yes | grade Medium | confidence 70 | plan:30,119; source.md:82; client.py:127-131
C-004 | valid yes | grade Note | confidence 60 | plan:117; jevlib/__init__.py:5; client.py:10-15
C-005 | valid yes | grade Medium | confidence 85 | plan:39,47; SKILL.md:154,156
C-006 | valid yes | grade Medium | confidence 75 | plan:159; session git status snapshot
C-007 | valid yes | grade Blocking-Missing | confidence 68 | plan:101,103,137,156
C-008 | valid yes | grade Medium | confidence 70 | plan:55,103; source.md:70,72
C-009 | valid yes | grade Medium | confidence 75 | source.md:42,44; plan:84,151
C-010 | valid yes | grade Medium | confidence 65 | source.md:34; plan:153,156
C-011 | valid yes | grade Medium | confidence 65 | source.md:104
C-012 | valid yes | grade Medium | confidence 75 | plan:82,84,97,103
C-013 | valid yes | grade Medium | confidence 60 | source.md:68; plan:101,103; journal.py:16-33
C-014 | valid yes | grade Medium | confidence 70 | plan:39,71,76; source.md:77
C-015 | valid yes | grade Note | confidence 85 | SKILL.md:152-159; plan:137,141
C-016 | valid no | grade Not-a-defect | confidence 90 | plan:19,21

X-001 | Blocking-Missing | 75 | the design requires the step and no task has it; `draw` still holds the cap (budget.py:72-78), so not Safety
X-002 | Blocking-Decision | 78 | the stop and rerun rules must test `Result.error`, and which refusals get a rerun is undecided
X-003 | Medium | 70 | the departure is reasoned at plan:30; only the contradiction in line 119 needs a fix
X-004 | Note | 60 | wording; one module name fixes it and it fails loudly
X-005 | Medium | 85 | a fixable check
X-006 | Blocking-Missing | 68 | nothing defines who writes the manifest at freeze, and the table hash cannot exist at Gate 1 (plan:137)

S-001 | winner 3 | 65 | widest evidenced base; add V1's C-008 and C-014
S-002 | winner 3 | 80 | `blocking_reason` makes each grade checkable against the rule

U-001 | incorporate yes | the design's Gate 1 has no `UNSET` check (source.md:72)
U-002 | incorporate yes | T-05 needs expected values (plan:76)
U-003 | incorporate yes | as Medium
U-004 | incorporate yes | the verdict's reasons need Task 5's formats (plan:84)
U-005 | incorporate yes | qualify the `Journal` part of C-013
U-006 | incorporate yes | C-015 as a Note; C-006 evidence matches V3 F-5

## 7 SHARED ASSUMPTIONS
A-001 QUALIFY: the design governs unless the plan gives a reason the library supports (plan:30 matches client.py:127-131); then only the unresolved contradiction is a defect.
A-002 QUALIFY: a literal reading matters where it silently does the wrong thing (C-002) but not where it fails loudly (C-004).
A-003 REJECT: the cards applied the test unevenly; V1 and V3 graded fixable checks (C-005, C-006) as Decision.
A-004 ACCEPT: plan:21 keeps `jevlib` read-only, and every behaviour claim was checked against the current files.
