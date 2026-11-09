model: claude-opus-5-5 family: claude rung: top family-fallback: GPT T1 model gpt-6.1-sol (T1Model02) has no verified spawn path on this install (refs/retry.md "GPT spawn path: none verified"); spawned on the strongest reachable model, Agent model=opus
outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T5.AC1 | Only status `open` or `regressed` counts as open (attempt-2.diff:93). A resolution row whose status word is not recognised gets an empty status and is quietly treated as resolved, so the probe gave PASS with exit 0 (review-2.md:6). The source requires an unparseable table to fail closed (source.md:133; plan line 103). Separately, a row with no severity label is picked up only when it contains the word `blocking` (attempt-2.diff:46). A row with an id and no grade at all is dropped, which breaks "unknown counts as blocking" (review-2.md:7; source.md:131; plan line 103). | Replace `unlabelled_blocking` with a single pass over review 3 that finds records the way `parse_report` does but without requiring a label. That pass returns two lists: (a) resolution-table rows with no status word, which go into `unparseable`, so the run exits 2 with `verdict: FAIL`; (b) unlabelled records outside the resolution table whose grade is not `non-blocking`, which go into `new_blocking`. Add tests for `\| N2 \| no \| partially resolved \|` and `\| R3-1 \| - \| missing anchor \|`. |
| T5.AC2 | The held count skips any held id that review 3 lists at all (`if t not in new`, attempt-2.diff:106). A closed MAJOR that review 3 relabels MINOR therefore drops out, and the owner count goes down (review-2.md:5). Neither the plan nor the owner decision allows that (plan line 21, line 108). The four owner tests (attempt-2.diff:299-342) never put a held id into review 3's new findings. | Skip a held id only when review 3 already counts it as CRITICAL or MAJOR: `held_cm = sum(ids.get(t,{}).get("label") in CM for t in held if not (t in new and new[t]["label"] in CM))`. Add a test where a closed MAJOR N1 appears in review 3 as `\| N1 \| MINOR \| non-blocking \|`, expecting owner = new + 1. Add a second test where N1 appears as MAJOR, expecting owner = new (counted once). |
| T5.AC3 | Not missed. The last line is always PASS or FAIL (attempt-2.diff:128-133) and the test helper asserts it on every run (attempt-2.diff:192; review-2.md:4). | Keep both as they are. The new unparseable path goes through the same final-line code, so no other change is needed. |

differs-by: the verdict code walks review 3 again with `parse_report`'s own record detection (the table id cell plus `lead_ids` prose records), but drops the label requirement. Every record outside the resolution table therefore gets graded (no grade means blocking), and every resolution row must carry a status word or the table is unparseable. Attempt 2 only looked for the word `blocking`. The held count is also de-duplicated against review 3's CRITICAL/MAJOR set, not against review 3 merely listing the id.

steps:
1. Start from the Q0 snapshot and re-create attempt 2 from attempt-2.diff:1-372. Keep `cmd_verdict`, the `main` wiring (attempt-2.diff:146-152), the docstring (attempt-2.diff:9-15) and all its tests. Do not change `parse_report`.
2. Replace `unlabelled_blocking` (attempt-2.diff:29-48) with `review3_gaps(text) -> tuple[list[str], list[str]]`. It returns `(unknown_blocking_ids, statusless_ids)` and copies `parse_report`'s loop: `key = report_key(text)`; a `#` heading sets `in_prior` from `PRIOR_HEADING_RE`; non-table lines give `toks = lead_ids(line)`; skip separator rows and header rows (the row after it is a separator); a table row uses `id_tokens(cell)` only when `ID_CELL_RE.fullmatch(cell)`; `status` is the first cell in `STATUS_WORDS` or `""`; read the `bcell` column as `parse_report` does; drop `FR-` tokens. Then:
   - `label, blocking, fr = parse_grade(line, key)`, applying the `bcell` yes/no adjustment as `parse_report` does.
   - If `in_prior` and `status == ""`, the ids go to the statusless list.
   - Else, if not `in_prior`, `status == ""`, `label == "unknown"`, `not fr` and `blocking is not False`, the ids go to the unknown-blocking list. Labelled and FR records stay with `parse_report`'s `graded`.
3. In `cmd_verdict`, set `unknown_ids, statusless = review3_gaps(r3)`. Build `new_blocking` from `graded` blocking ids plus `unknown_ids`. If `statusless` is not empty, append `f"resolution row without a status word: {', '.join(statusless)}"` to `unparseable`. That gives exit 2 and FAIL through the existing code at attempt-2.diff:128-136.
4. Change `held_cm` (attempt-2.diff:106) to the line given in the AC2 row.
5. Add these tests to `tests/skills/test_fix_audit_script.py`:
   - (a) The `applied` fixture with `r3(RESOLVED.replace("| N2 | yes | resolved |", "| N2 | no | partially resolved |"))` and last line `verdict: PASS`: expect exit 2, last line `verdict: FAIL` and an `unparseable:` line.
   - (b) `r3(RESOLVED, "| R3-1 | - | missing anchor |\n")`: expect `open blocking: R3-1` and FAIL.
   - (c) A prose record `**R3-3.** missing anchor` after the new-findings table: expect `open blocking: R3-3`.
   - (d) The `_run_audit` MAJOR-revert setup (attempt-2.diff:299-308) with new rows `NEW_CM + "| N1 | MINOR | non-blocking |\n"`: expect `_owner(lines) == (1, 2)`.
   - (e) The same setup with `| N1 | MAJOR | blocking |`: expect `_owner(lines) == (2, 2)`. DISAGREE is expected here; check only the counts.
   - Keep the `| R3-2 | non-blocking | wording |` PASS case (attempt-2.diff:369-372).
6. Run `uv run ruff check` on the two files, then `uv run pytest tests/skills/test_fix_audit_script.py -q`. Save the output as the extras log.

Files: plan `/home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/.dev/tasks/to-do/TASK-WF-spec-20261108-181547/TASK-WF-spec-20261108-181547.md`; source `/home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/.dev/tasks/to-do/TASK-WF-spec-20261108-181547/source.md`; inputs in `/home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/.dev/tasks/to-do/TASK-WF-spec-20261108-181547/artifacts/retries/T5/`.

What I left out: I did not run any of the probes myself. One risk: with step 2, an unlabelled evidence table outside the resolution section in review 3 now counts as blocking. That means a FAIL, and a DISAGREE if the id is closed. This is fail-closed by design (source.md:131), but a real review 3 that uses such tables will FAIL.

| DONE | NEXT |
|---|---|
| Read the plan, source, review-2, attempt-2.diff and extras-2.log; wrote one approach covering F2.1, F2.2 and F2.3 | Parent saves this advice and starts attempt 3 from Q0 using steps 1-6 |
