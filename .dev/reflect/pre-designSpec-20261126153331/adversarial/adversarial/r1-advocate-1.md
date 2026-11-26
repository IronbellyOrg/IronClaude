# Round 1, advocate 1 (card 1, analyzer lens, sonnet). Links reduced to file:line.

Read: plan, source.md, client.py:80-200, budget.py, validate.py:20-45; a Grep for `jevlib` under `.dev/research`.

## Positions and grades defended

- C-001 / X-004: concede. Card 1 marked the stop classes clean but never checked the post count. client.py:114-117 returns `refused/budget_exhausted` before any transport call; client.py:133-135 raises `KeyMissing` before `_attempts` (client.py:137); budget.py:72-78 shows a draw cannot run short after the whole-run reservation. So plan:165 ("exactly one post" for those two stops) cannot pass: Blocking (Decision). V2 and V3 are right.
- C-003 / X-001: defend Medium. Gate 2's `spend_bound` (plan:106) has no stated prompt source; plan:108 and source.md:155 say gates never call the corpus loader. Reading corpus.jsonl as raw JSON lines satisfies both and passes the load_corpus-raises test at plan:115, so the check at plan:114 is runnable and one sentence fixes it. The ledger-read gap is real (Budget.__init__ writes the ledger, budget.py:25-28) but is a fixable sentence.
- C-004: Medium. One citation conceded: source.md:149 supports only the `prior_run` point; the missing-key point is source.md:26. Burning the go is partly the spec's own design (M-12); nothing is lost or exposed and the cap is untouched.
- C-005: defend Blocking (Missing). source.md:142 says "A person also reads the six definitions once before the freeze." A grep of the plan matches only plan:20 (the labeller); the README order of work (plan:201) goes straight to `freeze-corpus` and Task 7 has no such step. A step the spec names is absent in substance. Calibrator 2 downgraded the same finding on card 2 because the source labels M-5 Medium and the fix is one README line; the label is information and fix cost is not a grade input for Missing.
- C-008: concede Medium (plan:27 and plan:127 already decide error is not right; what remains is a weak T-06 check at plan:138).
- C-009: Medium, narrowly. plan:79 says the factor is read from the rule but the two-argument calls at plan:85 give no rule input; a hardcoded 20 passes every listed check. Not Blocking. V3's reference-loop point is only redundancy; the smallest-b table is the real check.
- C-010: Medium. plan:26 says "final answered attempt", plan:81 says "the population `median_population` says", plan:56 sets `answered_only`; none defines "answered".
- C-011: concede Note (plan:94 says "small synthetic frozen files"; the gap shows at the first test run).
- C-012: Note, now checkable. The Grep found 26 `.py` files mentioning `jevlib` under `.dev/research`, 25 outside `jevlib` itself, so "31 importers" (plan:173) does not match. validate.py:32-33 rejects a model mismatch, so the `ok`-rows model check cannot fail.

## Steelmen of the other cards

- V3 on C-002: plan:125 and plan:129 make Task 5 read jev-rows.jsonl and run-record.md; plan:155-156 defines them only in Task 6 and Task 5 does not depend on it; every Task 5 test uses hand-built rows. But plan:155 lists the row fields in prose, so the format is not absent in substance; a dependency edge and an end-to-end test are a fixable check: Medium (held loosely).
- V2 on C-007: plan:41 records only the metadata of `runs/` itself; an in-place edit of a nested file leaves a directory mtime unchanged. M-13's primary guard is `Paths(root)` on temporary roots (source.md:150) and the fixture is a backstop; side with calibrator 2 on Medium.
- V2 on C-006: concede; card 1 missed it. source.md:144 says each freeze command writes "its own keys and never an existing key"; plan:101 gives the refusal only to `freeze-corpus`; plan:103 and plan:104 have none; plan:115 tests only a second `freeze-corpus`. A re-run of `freeze-table` could replace the frozen table hash and hide `table_answers_changed`. A behaviour the spec names is absent for two of three commands with no check: Blocking (Missing).
- V3 on C-003: V3's best case is that the rebuilt plan repeats M-1's defect for the prompt input; the raw-read fix stays inside plan:108, while V3's manifest-estimate fix changes the plan:101 keys, so it is a design choice, not a forced correction.

## Remaining disagreements

C-003 and C-005 are held. Would move on C-003 if V3 shows no reading of plan:106-115 can be built without changing a named decision; would move on C-005 if the rule is read to exclude human procedure steps.
