model: claude-opus-5-5 family: claude rung: top (escalation 2, T1Model01; Agent model=opus)
outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T5.AC1 | Attempt 3 skips any row with a status word when all its ids are review-2 ids, and it does this before it reads the row's grade (attempt-3.diff:52-53). The grade check only comes after that (attempt-3.diff:54-55). So `\| N1 \| blocking \| open \|` under `## New findings` is dropped. The id never reaches `new_blocking` (attempt-3.diff:108-113), and the closed-id DISAGREE check at attempt-3.diff:115 misses it. The probe in review-3.md:5 gets `verdict: PASS`, exit 0. That breaks plan:103 and plan:116 ("a closed id graded blocking by review 3 gives `consistency: DISAGREE`, exit code 2 and `verdict: FAIL`"), and source.md:132 ("so a relabelling dispute can never produce a PASS"). The only closed-id test (attempt-3.diff:251-256) uses a labelled row with no status word. The test that skips the status-word row (attempt-3.diff:450-452) never gives that row a blocking grade. | In `unlabelled_blocking`, read the row's grade first, the same way `parse_report` reads it: `parse_grade(line, key)[1]`, then the yes/no cell under a header column whose name contains `blocking`. The status-word skip for review-2 ids applies only when that grade is not `True`. A row that grades its ids blocking always reaches `new_blocking`, so a closed id gets DISAGREE in both report modes. |
| T5.AC2 | Not missed. review-3.md:3 marks it met. The `held_cm` rule at attempt-3.diff:120-124 stays as it is. | No change. |
| T5.AC3 | Not missed. review-3.md:4 marks it met. The last line is written at attempt-3.diff:151-152, and the test helper checks it on every run (attempt-3.diff:210). | No change. The new path goes through the same `disagree` code, FAIL and exit 2 (attempt-3.diff:144-154). |

differs-by: the row's own blocking grade is checked before its status word and before who owns its ids. A row that grades its ids blocking, by the word or by a `yes` in a `blocking` column, is never treated as a resolution note. Attempts 1 and 2 only looked for the word `blocking`. Attempt 3 decided by id ownership alone (review-2 ids versus new ids).

steps:
1. Start from the Q0 snapshot and re-create attempt 3 from attempt-3.diff:1-452 (script hunks at 1-173, tests at 174-452). Leave `parse_report` (Task 2) unchanged.
2. In `unlabelled_blocking` (attempt-3.diff:29-56), track `header` the way `parse_report` does:
   - Set `header = None` on a heading line and on any line that is not a table row. That means splitting the `not cs` check at attempt-3.diff:43 into its own `header = None; continue`.
   - On a header row (attempt-3.diff:45-47), set `header = [c.lower() for c in cs]` before the `continue`.
3. In the same function, replace attempt-3.diff:52-55 with:
   ```python
   blocking = parse_grade(line, key)[1]
   col = next((i for i, h in enumerate(header or []) if "blocking" in h), None)
   if col is not None and col < len(cs):
       if cs[col].lower() in YES_CELLS:
           blocking = True
       elif cs[col].lower() in NO_CELLS and blocking is None:
           blocking = False
   # a row that grades its ids blocking is a finding, never a resolution note
   if blocking is not True and any(c.lower() in STATUS_WORDS for c in cs[1:]) and set(toks) <= r2_ids:
       continue
   if blocking is not False:
       out += toks
   ```
   Then update the docstring to say: "A status-word row of review-2 ids is a resolution note only when it does not grade them blocking."
4. Add these tests to `tests/skills/test_fix_audit_script.py`:
   - (a) A test parametrized over `rule` in `("427", "any-severity")`: `verdict(applied, r3(RESOLVED, "| N1 | blocking | open |\n", "verdict: PASS"), rule)`. Assert return code 2, `lines[-1] == "verdict: FAIL"`, and a line that starts with `consistency: DISAGREE`. This is the probe from review-3.md:5.
   - (b) A blocking-column variant: take `r3(RESOLVED, "| N1 | yes | open |\n", "verdict: PASS")`, swap `"| id | severity | grade |"` for `"| id | blocking | status |"`, and expect DISAGREE, exit 2 and FAIL. Then make the same swap with row `| N1 | no | open |` and expect `open blocking: none`, exit 0 and `verdict: PASS`.
   - Keep every attempt-3 test unchanged, in particular attempt-3.diff:251-256, :382-390, :435-452.
5. Run `uv run ruff check src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py tests/skills/test_fix_audit_script.py` and `uv run pytest tests/skills/test_fix_audit_script.py -q`. Save both outputs as the extras log.
6. Re-run the review-3.md:5 probe by hand. It should now exit 2 with a `consistency: DISAGREE` line and `verdict: FAIL`. The same row without the status word should still give DISAGREE and FAIL.

| DONE | NEXT |
|---|---|
| Found why F4.1 happens: the status-word skip runs before the grade is read (attempt-3.diff:52-55). Wrote one attempt-4 approach that keeps F1.1-F3.1 resolved | The parent saves this advice and runs attempt 4 from Q0 using steps 1-6 |

Files: plan `/home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/.dev/tasks/to-do/TASK-WF-spec-20261108-181547/TASK-WF-spec-20261108-181547.md`, source `/home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/.dev/tasks/to-do/TASK-WF-spec-20261108-181547/source.md`, script `/home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py`, tests `/home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/tests/skills/test_fix_audit_script.py`.

Skipped: F4.2 is minor and advisory, and its fix would make a report whose resolution section has an unusual heading exit 2. Skipped: a review-3 row inside the resolution section that grades a closed id blocking still gives no DISAGREE. source.md:131 treats those rows as notes. Not checked: I ran nothing, because this step is read-only. Risk: the blocking-column yes/no reading in step 3 is slightly wider than review-3.md:5 asks for. An unlabelled row with `no` under a `blocking` column now counts as non-blocking, which matches how `parse_report` reads that cell.
