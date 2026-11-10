pick: advice-4-a.md; runner-up: advice-4-b.md; reason: tie, -a
## Task 5: Implement `fix_audit.py verdict` with the still-open count
Acceptance criteria:
- `uv run pytest tests/skills/test_fix_audit_script.py -q` passes, with tests for: a report whose own line is FAIL never yields a final PASS; open and regressed prior findings that R2 graded blocking stay in `open blocking`; a listed-open row for an R2-minor id does not count, and a closed one prints `closed-minor, listed open: <id>`; a closed id graded blocking by review 3 gives `consistency: DISAGREE`, exit code 2 and `verdict: FAIL`; an unparseable table exits 2 with last line `verdict: FAIL`; in `427` mode a disagreeing report line gives `consistency: DISAGREE`, exit code 2 and the stricter line; in `any-severity` mode the report line appears as `t09-verdict:`.
- Owner-count tests: a reverted finding labelled MAJOR in R2 raises `review-3 critical+major (owner count, held findings included)` by 1 over `review-3 new critical+major`; a `DOWNGRADE` id labelled CRITICAL raises it by 1; a reverted id labelled MINOR does not raise it; with the audit skipped both numbers are equal.
- The last line of `D/final-verdict.md` is always exactly `verdict: PASS` or `verdict: FAIL`.
AC ids: T5.AC1, T5.AC2, T5.AC3 (in the order of the bullets above)
Steps:
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
differs-by: the row's own blocking grade is checked before its status word and before who owns its ids. A row that grades its ids blocking, by the word or by a `yes` in a `blocking` column, is never treated as a resolution note. Attempts 1 and 2 only looked for the word `blocking`. Attempt 3 decided by id ownership alone (review-2 ids versus new ids).
