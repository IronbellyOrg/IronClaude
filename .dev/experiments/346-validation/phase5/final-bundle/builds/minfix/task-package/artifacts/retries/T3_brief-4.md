pick: advice-4-a.md; runner-up: advice-4-b.md; reason: tie, -a
## Task 3: Implement `check --enforce`
Acceptance criteria:
- `tests/skills/test_sc_fixcheck.py` passes with tests for: `--enforce` restores the over-budget and unattributed text and keeps in-budget fixes byte-for-byte; `depends:` partners are reverted whole; a second `--enforce` changes nothing (spec bytes identical); `--enforce` without a ledger exits 3 and the spec bytes are unchanged; the cycle cap reverts in the stated order; a finding reverted for exceeding its entries limit scores 0 entries afterwards; after `--enforce`, a plain `check` on the same four inputs exits 0 and scores the reverted entries `reverted`; `check --enforce` on a baseline whose hash does not match the report exits 4 and leaves the spec unchanged (the plain-`check` hash test is in Task 2).
- A property test with a fixed-seed `random.Random` generates at least 200 random edit sets and random ledgers and asserts that after `--enforce` a plain `check` exits 0 every time.
- `--enforce` writes no file other than the spec (directory listing before and after compared in a test).
- `uv run pytest tests/skills/test_sc_fixcheck.py -v` passes.
Steps:
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
differs-by: the unit diff and the moved-unit pool use (kind, normalised text) as the unit's identity, so a whitespace change that alters structure becomes a hunk that the existing revert covers. Every earlier attempt kept the text-only identity and only reworked separator rebuilding inside non-equal regions.
