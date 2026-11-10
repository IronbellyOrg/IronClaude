ladder entry: escalation 2, adviser B on the top rung T1Model01 (claude-opus-5-5); Agent model parameter: opus
outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T3.AC1 | All three attempts fixed only the rewrite side of the revert. Attempts 1 and 2 rebuilt the text from units and separators; attempt 3 recomposes only the diff regions that hold a reverted part, and its docstring says "Other regions are left byte for byte" (attempt-3.diff:201, :224-226). The unit diff in `diff_hunks` compares normalised text only (probe-3-1.md:6). A whitespace-only change that alters a unit's kind therefore lands in an "equal" region that no revert ever reaches. Example: a code-fence line joined onto a sentence, or a table row cut to one word. The re-check then exits 1 (review-3.md:10, both repros). Both brief-3 advisers saw this gap and left it open: advice-3-b.md:46 (fences) and advice-3-a.md:29 (table/plain changes only partly covered). | Make unit kind part of each unit's identity in the diff. `diff_hunks` matches units on `(u.kind, u.norm)`, and the moved-unit pool uses the same key (the coupled site named at probe-3-1.md:7). The unit whose kind changed is then in a non-equal region, and reverting that region restores its separators too. Port attempt 3's revert code unchanged. |
| T3.AC2 | Met (review-3.md:7). But `PROP_BASE` has no code fence (attempt-3.diff:516-517), and `random_edit` has no line-join or row-cut edit (attempt-3.diff:533-548). That is why the property test never caught F3.1 (review-3.md:10, last sentence). | Keep `Random(346)` and at least 200 cases. Add a fence block to `PROP_BASE`, plus two undeclared edit kinds: `join` (a line joined onto the line before it) and `rowcut` (a row replaced by its first cell's text). |
| T3.AC3 | Met (review-3.md:8). The only write is `atomic_write`, and only when the bytes changed (attempt-3.diff:328-329). The test is at attempt-3.diff:466-475. | Port unchanged. The new key is in-memory only. |
| T3.AC4 | Met: 71 passed, lint clean (review-3.md:9, extras-3.log:1-2). | Keep the whole file passing, with the Task 2 tests unedited, after the new tests are added. |

differs-by: the unit diff and the moved-unit pool in `diff_hunks` match on `(kind, norm)` instead of `norm` alone, so every structural change sits in a non-equal region that `--enforce` can revert. No earlier attempt changed the diff; all three only changed how reverted regions are rewritten.

steps:
1. Start from the Task 2 snapshot and port all of attempt-3.diff unchanged. Review-3.md:2-5 marks all four earlier findings resolved. In `fixcheck.py` that means: `split_region` (5-90), `btail` in `analyze` (94-110), `new_key` and the grouped `attribute` (142-185), `region_edits` (192-246), `apply_edits` (249-257), `depends_closure` (260-271), `moved_closure` (274-290), `enforce` (293-337) and the `cmd_check` hook (348). Port the tests at 362-726.
2. In `diff_hunks`, build `bk = [(u.kind, u.norm) for u in bu]` and `rk = [(u.kind, u.norm) for u in ru]`. Pass them to `difflib.SequenceMatcher(None, bk, rk, autojunk=False)`. Key the `deleted` pool on `bk[i]` and look it up with `rk[j]`, so "identical moved unit" means same kind and same text. Update the docstring to match. Change nothing else in `diff_hunks`, `split_region` or `region_edits`.
3. Accept one deliberate plain-`check` change: a kind-only change, such as the single-cell row `| c |` cut to `c`, used to be invisible and now shows as an unattributed hunk (+0/-0) with exit 1. Run the Task 2 tests unedited. If one fails, stop and report it; do not adjust the key.
4. Add the two repros from review-3.md:10 word for word as tests.
   - Fence join: baseline `"# Doc\n\nAlpha text here.\n\n```\nuv run thing\n```\n\nBeta text here. Gamma more text.\n\nOld entries leave the cache after one hour.\n"`, revision joining `"Alpha text here. ```"`, F1 replacing the last sentence in budget.
   - Row-prefix cut: `"| c | three |"` cut to `"c"` with no ledger entry, plus one in-budget fix elsewhere.
   - For each, assert: `--enforce` exits 0; the output holds `restored-baseline=no` and `hunks=` lists the reverted hunk; the spec equals the baseline with only F1's new text; a later plain `check` exits 0.
   - Add one plain-`check` test showing that `| c |` cut to `c`, with no ledger entry, reports `UNATTRIBUTED` and exits 1.
5. Property test, still `Random(346)` and at least 200 cases:
   - Insert ```` "```\nuv run thing\n```\n\n" ```` between the first paragraph and the table in `PROP_BASE`.
   - Add the undeclared edit kind `join`: pick a non-empty line other than the first and replace the line breaks before it with one space. This covers a fence, row or heading line joined onto the line above.
   - Add the undeclared edit kind `rowcut`: replace a row with its first cell's text.
   - Keep the kept-slice assertion and both exit-0 assertions.
   - Outside the suite, run at least 2,400 cases over several seeds and shuffled baselines that contain fences, matching the reviewer's fuzz. Record the counts in `.dev/tasks/to-do/TASK-WF-spec-20261108-181543/artifacts/t3-extra-seeds.txt`.
6. Run `uv run pytest tests/skills/test_sc_fixcheck.py -v` and `uv run ruff check src/superclaude/skills/sc-fixcheck/scripts/fixcheck.py tests/skills/test_sc_fixcheck.py`.

| DONE | NEXT |
|---|---|
| Found why attempt 3 failed: kind changes are hidden from the diff, so they never get reverted. Wrote one brief that differs from all earlier ones: match units on (kind, norm). | Save this brief and have the implementer apply it on top of a full port of attempt 3. |

I traced both repros through the ported code by hand and both come out clean, but I did not run anything. Step 5's fuzz run is the real proof. One risk remains: when a fence-state change produces a very large region (more than 40,000 unit pairs), the code leaves it unpaired, so a nearby in-budget fix becomes unattributed and gets reverted. The exit code is still 0, but that fix is lost.

Files:
- /home/coder/workspaces/worktrees/IronClaude/bs346-minfix/.dev/tasks/to-do/TASK-WF-spec-20261108-181543/artifacts/retries/T3/review-3.md
- /home/coder/workspaces/worktrees/IronClaude/bs346-minfix/.dev/tasks/to-do/TASK-WF-spec-20261108-181543/artifacts/retries/T3/attempt-3.diff
- /home/coder/workspaces/worktrees/IronClaude/bs346-minfix/.dev/tasks/to-do/TASK-WF-spec-20261108-181543/artifacts/retries/T3/probe-3-1.md
