model: claude-opus-5-5 family: claude rung: top (escalation 2, T1Model01; Agent model=opus)
outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T5.AC1 | The DISAGREE check only looks at closed ids that land in `new_blocking` (attempt-3.diff:115). `new_blocking` comes from `parse_report`'s `graded` plus `unlabelled_blocking` (attempt-3.diff:108-113). A row with a status word and no label goes into `prior` (attempt-3.diff:92-93), and `unlabelled_blocking` skips it when all its ids are review-2 ids (attempt-3.diff:52-53). So `\| N1 \| blocking \| open \|` never reaches the check, and the run ends with PASS and exit 0 (review-3.md:5). The plan requires DISAGREE, exit 2 and FAIL for a closed id that review 3 grades blocking, in both modes (TASK-WF-spec-20261108-181547.md:103, :116; source.md:132). Advisory F4.2: the "no resolution table" check tests `prior`, which also holds status-word rows from outside the resolution section (attempt-3.diff:94-95; review-3.md:6; source.md:133). | Stop deriving DISAGREE from the open set. Add one verdict-side scan of review 3 that, in every section, finds each record naming a closed id, using `parse_report`'s record detection: an id cell, or `lead_ids` for prose. The record counts when its line is positively graded blocking (`parse_grade(line, key)[1] is True`) or when its `blocking`-header column cell is in `YES_CELLS`. Those ids are added to `disagree`. The same scan records whether any id row sits under a resolution heading, and that replaces `if r3 and not prior`. `unlabelled_blocking`, `parse_report` and the open-set rules stay unchanged. |
| T5.AC2 | Not missed (review-3.md:3). The owner count does not read the new scan (attempt-3.diff:119-124). | No change. |
| T5.AC3 | Not missed (review-3.md:4). The new DISAGREE ids go through the existing `fail` path and final line (attempt-3.diff:144-154). | No change. |

differs-by: The closed-id consistency check gets its own scan of every review-3 record in every section, and it fires only on a positive blocking grade. Earlier attempts tested membership in `new_blocking` and kept changing how records are sorted into the open set. Under this approach a review-2 id with a status word is still not a new finding. That keeps F3.1 resolved and keeps the source's "R2-minor rows are notes and never count" / "upgrades ignored" rule (source.md:131, :167). It also catches a blocking grade inside the resolution table, which the reviewer's suggested fix (changing the skip in `unlabelled_blocking`) would still miss.

steps:
1. Start from the Q0 snapshot and re-create attempt 3 from attempt-3.diff:1-452: the script hunks at :1-172 and the tests at :174-452. Do not change `parse_report` or `unlabelled_blocking`.
2. Add `scan_review3(text: str, closed: set[str]) -> tuple[list[str], bool]` next to `unlabelled_blocking`. It copies `parse_report`'s loop shape and grades nothing new:
   - Set `key = report_key(text)`, `in_prior = False`, `header = None`.
   - Non-table line: set `header = None`. A `#` line sets `in_prior` from `PRIOR_HEADING_RE`. Then `toks = lead_ids(line)`.
   - Table line: skip separators. A row followed by a separator sets `header = [c.lower() for c in cs]` and continues. Otherwise `cell = cs[0].strip("*` ")`, and `toks = id_tokens(cell)` when `ID_CELL_RE.fullmatch(cell)`, else `[]`. Set `bcell` from the first header column containing `blocking`.
   - Drop `FR_RE` tokens.
   - If `in_prior` and `toks` on a table row, set `has_resolution = True`.
   - If `parse_grade(line, key)[1] is True or bcell in YES_CELLS`, add `[t for t in toks if t in closed]` to the hits.
   - Return `(list(dict.fromkeys(hits)), has_resolution)`. Add a one-line comment: only a positive blocking grade counts, because a closed id listed open is expected (source.md:132).
3. In `cmd_verdict`, after `parsed = parse_report(r3)` (attempt-3.diff:92), call `closed_hits, has_res = scan_review3(r3, set(closed))`. Replace `if r3 and not prior:` (attempt-3.diff:94) with `if r3 and not has_res:`. This is F4.2; the message stays the same.
4. Replace attempt-3.diff:115 with `disagree = list(dict.fromkeys([t for t in closed if t in new_blocking] + closed_hits))`. Keep the `new_blocking` term, so an unknown or conflicting grade on a labelled closed record still disagrees. Leave the rest of the code as it is (attempt-3.diff:116-154).
5. Add tests to `tests/skills/test_fix_audit_script.py`, using the `applied` fixture (N1 closed):
   - (a) `r3(RESOLVED, "| N1 | blocking | open |\n", "verdict: PASS")`: exit code 2, a `consistency: DISAGREE` line containing `N1`, last line `verdict: FAIL`.
   - (b) The same row in the resolution table, `r3(RESOLVED + "| N1 | blocking | open |\n", last="verdict: PASS")`: same three assertions.
   - (c) Parametrize (a) over `"427"` and `"any-severity"` to cover "both modes".
   - (d) F4.2: `r3("", "| R3-1 | - | open |\n", "verdict: FAIL")`: exit code 2, an `unparseable:` line, last line `verdict: FAIL`.
   - Keep the existing `| N1 | no | open |` PASS cases (attempt-3.diff:245-248, :450-452) and the R3-1 status-word cases (attempt-3.diff:442-447) unchanged. They guard F3.1 and the listed-open rule.
6. Run `uv run ruff check src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py tests/skills/test_fix_audit_script.py` and `uv run pytest tests/skills/test_fix_audit_script.py -q`. Then re-run the review-3.md:5 probe by hand. Expected result: a `consistency: DISAGREE` line, exit code 2, `verdict: FAIL`.

Files: plan `/home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/.dev/tasks/to-do/TASK-WF-spec-20261108-181547/TASK-WF-spec-20261108-181547.md`, source `/home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/.dev/tasks/to-do/TASK-WF-spec-20261108-181547/source.md`, script `/home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/src/superclaude/skills/sc-fix-audit/scripts/fix_audit.py`, tests `/home/coder/workspaces/worktrees/IronClaude/bs346-ponytail/tests/skills/test_fix_audit_script.py`.

I did not run anything; this step is read-only. One known risk is deliberate: after this change a closed id is not added to `open blocking`, even when review 3 grades it blocking. The run still ends in FAIL through DISAGREE, and the DISAGREE line names the id. The F4.2 fix is included because it is cheap but optional. Drop it (step 3, test d) if the executor wants the smallest diff.
