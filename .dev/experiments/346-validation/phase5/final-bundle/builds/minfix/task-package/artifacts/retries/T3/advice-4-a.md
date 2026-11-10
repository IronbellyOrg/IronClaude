ladder entry: escalation 2, adviser A on the top rung T1Model01 (claude-opus-5-5); Agent model parameter: opus
outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T3.AC1 | The only open finding is F3.1 (review-3.md:10); F1.1 to F2.2 are resolved (review-3.md:2-5). The unit diff and the moved-unit pool compare normalised text only (probe-3-1.md:6-7). So a whitespace-only change that changes a unit's kind lands in an "equal" region: a fence line joined onto a sentence, or a table row cut down to its first cell. `region_edits` skips equal regions (attempt-3.diff:225-226) and leaves them "byte for byte" (attempt-3.diff:201). The fence join is never restored, and the row cut gets rebuilt as the broken `"c \| three \|"` (review-3.md:10). The source says `--enforce` is 0 "by construction", because every exit-1 reason is a hunk it reverts (source.md:62). That breaks when the cause sits outside every hunk. All three attempts only changed how separators are rebuilt inside non-equal regions; none changed what counts as "equal". | Compare `(u.kind, u.norm)` instead of `u.norm` in `diff_hunks`, both in the `SequenceMatcher` input and in the moved-unit pool. A unit whose kind changed then forms a non-equal region. `region_edits` already rebuilds such a region from the end of the previous equal unit, using the baseline's own separators for reverted parts, so the changed separator comes back with the baseline units. Nothing else in the revert code changes. |
| T3.AC2 | Met as written (review-3.md:7). But `PROP_BASE` has no fence (attempt-3.diff:516-517), and `random_edit` has no line-join or row-cut edit: its only whitespace edit appends spaces (attempt-3.diff:533, :548). So it never produces a kind change in an equal region, which is the case behind the reviewer's 5 failures in 2,400 fuzz runs (review-3.md:10). | Keep `Random(346)`, at least 200 cases and the existing assertions (attempt-3.diff:562-602). Add a fenced block to `PROP_BASE`, plus two undeclared edit kinds: join a target line (a row or the fence line) onto the previous line, and cut a row to its first cell. |
| T3.AC3 | Met (review-3.md:8). The only write is the atomic spec write when the bytes differ (attempt-3.diff:328-329); the test is at attempt-3.diff:466-475. | Port it unchanged. The diff-key change writes nothing. |
| T3.AC4 | Met: 71 passed, lint clean (review-3.md:9, extras-3.log:1-2). The failure is in behaviour the tests did not cover (review-3.md:6). | Keep the whole file passing after the new tests. Changing the key also changes plain `check` hunks; the Task 2 tests in the same file must still pass. |

differs-by: the unit diff and the moved-unit pool use (kind, normalised text) as the unit's identity, so a whitespace change that alters structure becomes a hunk that the existing revert covers. Every earlier attempt kept the text-only identity and only reworked separator rebuilding inside non-equal regions.

steps:
1. Start from the Task 2 snapshot and re-apply all of attempt-3.diff (code at :1-351, tests at :352-726). Review-3 resolves every earlier finding and faults only the diff key (review-3.md:2-5, :10).
2. In `diff_hunks`, change the `SequenceMatcher` sequences from `[u.norm for u in bu]` and `[u.norm for u in ru]` to `[(u.kind, u.norm) for u in ...]`. Key `deleted` and the `pool` lookup on `(bu[i].kind, bu[i].norm)` and `(ru[j].kind, ru[j].norm)`. The pool must change too. If it stays text-only, a kind-changed unit matches its own deleted counterpart as "moved", `analyze` drops it from `part.b` and `part.r`, and the region produces no hunk to revert (probe-3-1.md:7, "coupled sites"). Leave `pair_units`, `locate`, `split_region`, `attribute`, `region_edits` and `enforce` unchanged.
3. Add tests, both repros word for word from review-3.md:10:
   - Fence join: baseline `"# Doc\n\nAlpha text here.\n\n```\nuv run thing\n```\n\nBeta text here. Gamma more text.\n\nOld entries leave the cache after one hour.\n"`. The revision joins `"Alpha text here. ```"`, and F1 replaces the last sentence in budget.
   - Row cut: baseline row `"| c | three |"` cut to `"c"` with no ledger entry, plus one in-budget F1 fix elsewhere.
   - For each, assert that `--enforce` exits 0 with `restored-baseline=no`, that the spec equals the baseline with only F1's new sentence in place, and that a plain `check` afterwards exits 0.
   - Add a third parametrised case: a heading joined onto the sentence before it (`"Text.\n\n## Note"` becomes `"Text. ## Note"`).
4. Property test: insert `"```\nuv run thing\n```\n\n"` into `PROP_BASE` between the first paragraph and the table, and add the fence line to the target pool. Add two undeclared kinds to `random_edit`:
   - `join`: replace the line break(s) before the target's line with one space.
   - `cut`: replace a row with its first cell's text.
   Keep `Random(346)`, 200 cases and the kept-slice and exit-0 assertions.
5. Run 2,000 cases on a few other seeds locally (not committed), on this base and on a shuffled-blocks base with fences.
6. Run `uv run pytest tests/skills/test_sc_fixcheck.py -v` (all Task 2 tests must still pass under the new key) and `uv run ruff check` on both files.

Not checked: I did not run the new key against the repros; step 3 is the proof. One gap is likely and outside F3.1: an in-budget kept fix that adds a single unmatched fence line turns everything after it into code. Reverting the later parts cannot undo that, so the re-check can still exit 1, and neither the reviewer nor the property test has hit it. A smaller unchecked risk: a kept sentence with no final period, placed on the same line as restored text, can merge into one unit.

Files:
- /home/coder/workspaces/worktrees/IronClaude/bs346-minfix/.dev/tasks/to-do/TASK-WF-spec-20261108-181543/artifacts/retries/T3/review-3.md
- /home/coder/workspaces/worktrees/IronClaude/bs346-minfix/.dev/tasks/to-do/TASK-WF-spec-20261108-181543/artifacts/retries/T3/attempt-3.diff
- /home/coder/workspaces/worktrees/IronClaude/bs346-minfix/.dev/tasks/to-do/TASK-WF-spec-20261108-181543/artifacts/retries/T3/probe-3-1.md
- /home/coder/workspaces/worktrees/IronClaude/bs346-minfix/.dev/tasks/to-do/TASK-WF-spec-20261108-181543/source.md

| DONE | NEXT |
|---|---|
| Found the cause: units are matched by text only, so kind changes sit in equal regions that `--enforce` never rewrites | Save this as brief 4 and have the implementer apply it to the Task 2 snapshot |
| One new approach: match units by (kind, text) in the diff and the moved-unit pool, keeping the attempt-3 revert code | Run the wider property test (fences, joins, row cuts) with extra seeds before the review |
