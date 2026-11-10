pick: advice-3-a.md; runner-up: advice-3-b.md; reason: tie, -a
## Task 5: Implement `fix_audit.py verdict` with the still-open count
Acceptance criteria:
- `uv run pytest tests/skills/test_fix_audit_script.py -q` passes, with tests for: a report whose own line is FAIL never yields a final PASS; open and regressed prior findings that R2 graded blocking stay in `open blocking`; a listed-open row for an R2-minor id does not count, and a closed one prints `closed-minor, listed open: <id>`; a closed id graded blocking by review 3 gives `consistency: DISAGREE`, exit code 2 and `verdict: FAIL`; an unparseable table exits 2 with last line `verdict: FAIL`; in `427` mode a disagreeing report line gives `consistency: DISAGREE`, exit code 2 and the stricter line; in `any-severity` mode the report line appears as `t09-verdict:`.
- Owner-count tests: a reverted finding labelled MAJOR in R2 raises `review-3 critical+major (owner count, held findings included)` by 1 over `review-3 new critical+major`; a `DOWNGRADE` id labelled CRITICAL raises it by 1; a reverted id labelled MINOR does not raise it; with the audit skipped both numbers are equal.
- The last line of `D/final-verdict.md` is always exactly `verdict: PASS` or `verdict: FAIL`.
AC ids: T5.AC1, T5.AC2, T5.AC3 (in the order of the bullets above)
Steps:
1. Start from Q0. Re-create attempt 2 from attempt-2.diff: script hunks at lines 1-155, tests at lines 156-372.
2. In `unlabelled_blocking` (attempt-2.diff:29-48), set `key = report_key(text)` once. Skip a header row the way `parse_report` does: a row whose next line is a separator row. Keep the existing filters: the prior-heading toggle, the separator skip, the id-cell match, the label skip, the status-word skip and the `FR-` filter. Replace the `BLOCKING_RE` test at line 46 with `if parse_grade(line, key)[1] is not False:`. An unknown grade (`None`) then counts as blocking, as the brief says. Update the docstring to match. Leave `parse_report` (Task 2) unchanged.
3. In `cmd_verdict`, after attempt-2.diff:87, add `blank = [t for t, st in prior if not st]` and, when it is non-empty, `unparseable.append(f"resolution rows without a status ({', '.join(sorted(STATUS_WORDS))}): {', '.join(blank)}")`. The exit code 2 (line 136) and the FAIL (line 128) then follow.
4. Replace attempt-2.diff:106 with `held_cm = sum(ids.get(t, {}).get("label") in CM and not (t in new and new[t]["label"] in CM) for t in held)`. Add a one-line comment: the id is skipped only when `new_cm` already counts it, so the count never drops below the held total.
5. Add these tests to `tests/skills/test_fix_audit_script.py`:
   - (a) Use the `test_owner_count_reverted_major_adds_one` setup (diff:299-308) with review-3 new row `| N1 | MINOR | non-blocking |` and prior row `| N2 | yes | resolved |`. Assert `_owner(lines) == (0, 1)`. Repeat with `| N1 | MAJOR | non-blocking |` and assert `(1, 1)`.
   - (b) `applied` fixture with `r3("| N2 | no | partially resolved |\n| N3 | yes | resolved |\n", last="verdict: PASS")`. Assert return code 2, an `unparseable:` line naming N2, and last line `verdict: FAIL`.
   - (c) `applied` fixture with `r3(RESOLVED, "| R3-1 | - | missing anchor |\n", "verdict: PASS")`. Assert `open blocking: R3-1` and last line `verdict: FAIL`.
   - Keep the R3-2 `non-blocking` PASS case (diff:369-372).
6. Run `uv run ruff check src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py tests/skills/test_fix_audit_script.py` and `uv run pytest tests/skills/test_fix_audit_script.py -q`. Then re-run probes P1-P3 by hand:
   - P1 should print owner count 1.
   - P2 should print `open blocking: R3-1` and `verdict: FAIL`.
   - P3 should exit 2 with `verdict: FAIL`.
differs-by: every exclusion now needs positive evidence. A review-3 row leaves the open set only if it says non-blocking. A resolution row counts only if it has a recognised status word. A held id leaves the owner count only if review 3 already counts it CRITICAL or MAJOR. Attempts A1 and A2 both excluded by default whenever evidence was missing.
