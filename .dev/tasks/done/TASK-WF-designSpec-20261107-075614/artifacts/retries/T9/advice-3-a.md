model: opus (claude-gw-tier1a alias) family: claude rung: top
outcome: ready

| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T9.AC1 | Both attempts tried to list the gate words. Attempt 1 checked only four literal phrases (review-1.md:2). Attempt 2 switched to a regex scan, but it starts the scan after the bold heading (`bullet.split(":**", 1)[-1]`, attempt-2.diff:84) and stops it at "At L3 with". So a heading edited to "(L3 only)" or "(draft mode)" is never scanned, and "at level 3" matches none of the patterns at attempt-2.diff:88 (review-2.md:2). Review 2's suggested fix, scanning the heading with the same list, would fail on the real file: the real heading says "every ordinal" (attempt-2.diff:33) and `ordinal` is one of the gate patterns (attempt-2.diff:88). Every mutation case also edits the same spot ("or when the run log already holds", attempt-2.diff:118-121). Each one adds a hand-picked phrase, so wording outside the list or outside that spot is never tested. | Pin the whole bullet line to one exact constant, so any change of wording anywhere in it fails. Add a one-time check that the pinned constant itself names no gate. Generate the mutations mechanically at every word position, heading included. |
| T9.AC2 | Not missed. The reviewer marked it met (review-2.md:5). The output row at attempt-2.diff:17 and the test at attempt-2.diff:144-154 cover it. | Reapply attempt-2.diff:17 and the test at :144-154 unchanged. |
| T9.AC3 | Not missed. The command passed (extras-2.log:4-6; review-2.md:6). | Add new tests only. Re-run the AC3 command after the change. |
| T9.AC4 | Not missed (review-2.md:7). attempt-2.diff:166-180 asserts one python fence, no `src/superclaude` string and no banned tokens. | Keep that test unchanged. The new constant lives in the test file, not in SKILL.md. |
| T9.AC5 | Not missed (review-2.md:8). | Run `make sync-dev`, then `make verify-sync`, after the test edit. |

differs-by: The gate check stops being a scan for chosen words. The whole bullet must equal a pinned constant (`WAVE0_BULLET`), so an L3 or `draft` condition in any wording, heading included, fails the test. The gate-word scan runs only once, on the constant, to prove the pin itself is ungated.

steps:
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

I did not run anything. I also did not read `pre-build-gate.md` or the live SKILL.md: the plan relies on attempt-2.diff:33 being the bullet the reviewer accepted. The cost of the exact pin is that any future rewording of the bullet must update `WAVE0_BULLET` in the same change.

Files:
- /home/coder/workspaces/worktrees/IronClaude/issue-375-pr-submit-draft-guard/.dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/retries/T9/review-2.md
- /home/coder/workspaces/worktrees/IronClaude/issue-375-pr-submit-draft-guard/.dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/retries/T9/attempt-2.diff
- /home/coder/workspaces/worktrees/IronClaude/issue-375-pr-submit-draft-guard/tests/pr_submit/test_merge_guard_protocol.py

| DONE | NEXT |
|---|---|
| Found why AC1 failed twice: both attempts listed gate words, and attempt 2 never scanned the heading | Parent saves this advice and runs attempt 3 with the exact-pin check |
