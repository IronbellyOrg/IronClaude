pick: advice-3-a.md; runner-up: advice-3-b.md; reason: tie, -a
## Task 9: Wire the Wave 0 resume and `off` hook, the flag row, the output row and the wave line into `SKILL.md`

Acceptance criteria:
- T9.AC1: The Wave 0 test fails when the bullet is placed after the Wave 1 bullet, when it names an L3 or `draft` condition, or when the literal `off` line is missing, and passes on the real file.
- T9.AC2: A test asserts the literal text "PR #N is still mergeable; this run's fixes are local only." is present in `SKILL.md` itself (not only in the ref), so a fresh L2 run needs no ref load.
- T9.AC3: `uv run pytest tests/pr_submit/test_static_grep.py tests/pr_submit/test_conflict_sync_protocol.py tests/pr_submit/test_cosmos_protocol.py tests/pr_submit/test_codex_reviews.py tests/pr_submit/test_merge_guard_protocol.py tests/skills/test_worker_contract.py -q` passes with no edit to any existing test expectation other than those listed in Tasks 2, 5, 7 and 8.
- T9.AC4: `SKILL.md` still has exactly one python code fence and no `src/superclaude` string, and the new lines contain neither `evidence-validator` nor `conflict-intent.md`.
- T9.AC5: `make verify-sync` exits 0.

Steps:
1. Reapply the four SKILL.md additions exactly as in attempt-2.diff:9, :17, :25 and :33. The reviewer accepted the bullet text, so do not reword it.
2. In `tests/pr_submit/test_merge_guard_protocol.py`, reapply the test-file block from attempt-2.diff:47-180. Then add the constant `WAVE0_BULLET`, equal byte for byte to the bullet at attempt-2.diff:33 without the leading `+`. Use a single-quoted Python string: the line has double quotes and backticks but no apostrophe. Line length does not matter here because ruff ignores E501 (pyproject.toml:186).
3. Rewrite `_wave0_problems`:
   - Keep the check that the bullet appears exactly once.
   - Keep the before-Wave-1 position check.
   - Keep the `need` presence loop, including `OFF_LINE`.
   - Delete the `loading` slice and its regex loop (attempt-2.diff:84-90).
   - Add: if `bullet != WAVE0_BULLET`, append the problem "the bullet differs from the pinned ungated wording (gate)", so the existing `"gate" in p` assertions still work.
4. Add `test_the_pinned_wave0_bullet_names_no_gate`. It should:
   - Take `WAVE0_BULLET`.
   - Remove the literal `(every ordinal, both modes)` exactly once, and assert that removal happened.
   - Remove the exact `off` sentence (from "At L3 with `--merge-guard off`" to the end of the line) exactly once, and assert that too.
   - Remove the two event names.
   - Assert that the rest matches none of `\bL[0-3]\b`, `\blevel\s*[0-3]\b`, `ordinal`, `monitor`, `draft` (case-insensitive).
   - Assert the heading literal is `(every ordinal, both modes)`.

   Because each removal matches exactly once, a gate added inside the heading or the `off` sentence still leaves text that this scan sees.
5. Rewrite the mutation test. Every case must first assert `mutated != text`, so a replace that matches nothing cannot pass silently. Cases:
   - (a) The bullet moved after Wave 1: expect "after the Wave 1".
   - (b) `OFF_LINE` removed: expect "lacks".
   - (c) The heading `(every ordinal, both modes)` replaced with `(L3 only)`, then with `(draft mode)`.
   - (d) "at level 3, ", "at L3, " and "when the PR is a draft, " inserted before "or when the run log already holds".
   - (e) A mechanical loop over every space position in the bullet, heading and `off` sentence included, inserting "in draft mode " and then "at L3 only ". Each mutated text must give a problem containing "gate".
6. Keep the flag-row, output-row, wave-structure and no-gh / no-python tests from attempt-2.diff:127-180 unchanged.
7. Run `uv run pytest tests/pr_submit/test_static_grep.py tests/pr_submit/test_conflict_sync_protocol.py tests/pr_submit/test_cosmos_protocol.py tests/pr_submit/test_codex_reviews.py tests/pr_submit/test_merge_guard_protocol.py tests/skills/test_worker_contract.py -q`, then `make lint`, `make sync-dev` and `make verify-sync`. Save their output as the task's check log.

differs-by: The gate check stops being a scan for chosen words. The whole bullet must equal a pinned constant (`WAVE0_BULLET`), so an L3 or `draft` condition in any wording, heading included, fails the test. The gate-word scan runs only once, on the constant, to prove the pin itself is ungated.
