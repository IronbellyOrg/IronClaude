model: claude-opus-5-5 family: claude rung: top (T1Model01; Agent model=opus)
outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T5.AC1 | **F2.2:** the code only checks that the resolution table has some rows (attempt-2.diff:86-87). Line 93 then keeps only `open`/`regressed` rows, so a row whose status matched no known word is silently treated as resolved (review-2.md:6, probe P3, present since A1). The brief requires an unparseable table to exit 2 with FAIL (TASK-WF-spec-20261108-181547.md:103, :116). **F2.3:** `unlabelled_blocking` counts a row only when it contains the word `blocking` (attempt-2.diff:46-47). A row with no grade at all is skipped, which breaks "unknown counts as blocking" (TASK-WF-spec-20261108-181547.md:103; review-2.md:7, probe P2). | Any resolution row with an empty status makes the report unparseable (exit 2, `verdict: FAIL`). Any unlabelled id row outside the resolution table counts as blocking unless `parse_grade` positively reads it as non-blocking. |
| T5.AC2 | `held_cm` drops a held id whenever review 3 lists it, whatever label review 3 gives it (attempt-2.diff:106; review-2.md:5, probe P1, present since A1). The owner count must include every held id that review 2 labelled CRITICAL or MAJOR, and nothing may lower it (TASK-WF-spec-20261108-181547.md:21, :108, :117). | Leave a held CRITICAL/MAJOR id out of the added count only when `new_cm` already counts it, meaning review 3 itself labels it CRITICAL or MAJOR. |
| T5.AC3 | Not missed. The last line is always written (attempt-2.diff:128-133; review-2.md:4). | No change. The new unparseable path goes through the same `fail`/last-line code. |

differs-by: every exclusion now needs positive evidence. A review-3 row leaves the open set only if it says non-blocking. A resolution row counts only if it has a recognised status word. A held id leaves the owner count only if review 3 already counts it CRITICAL or MAJOR. Attempts A1 and A2 both excluded by default whenever evidence was missing.

steps:
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

Files: plan `/home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/.dev/tasks/to-do/TASK-WF-spec-20261108-181547/TASK-WF-spec-20261108-181547.md`; script `/home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py`; tests `/home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/tests/skills/test_fix_audit_script.py`.

| DONE | NEXT |
|---|---|
| Found the cause of each of F2.1-F2.3 and wrote one approach that fixes all three | The parent saves this advice and runs attempt 3 from Q0 |

Not done: I did not read source.md, and nothing was run because this step is read-only.

Risks:
- An unlabelled id row in any other review-3 table outside the resolution section (an evidence table, for example) will now make the verdict FAIL. That is the fail-closed direction.
- A resolution section written as prose instead of a table now exits 2 as unparseable.
- Unlabelled prose records in review 3 are still ignored, which is outside the scope of F2.3.
