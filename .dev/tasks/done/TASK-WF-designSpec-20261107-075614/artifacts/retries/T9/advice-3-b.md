model: opus (claude-gw-tier1a alias) family: claude rung: top family-fallback: no GPT spawn path is verified on this install (refs/retry.md, Model ladder)
outcome: ready
| AC | why earlier attempts missed it (path:line) | change |
|---|---|---|
| T9.AC1 | Attempt 1 only checked for four fixed phrases (review-1.md:2). Attempt 2 swapped that for a list of banned words (attempt-2.diff:88), but the scan starts after the bold heading (attempt-2.diff:84) and stops at "At L3 with", so an edited heading or a gate inside the `off` sentence is never scanned (review-2.md:2). Every mutation case inserts text at one spot in the loading sentence (attempt-2.diff:110-123), so heading edits were never tested. Any banned-word list also misses wordings nobody thought of (for example "once the PR is ready for review"). Note that F2.1's own suggested fix ("the real heading ... holds none of the gate words", review-2.md:2) is wrong: the real heading says "every ordinal" (attempt-2.diff:33) and `ordinal` is on the list (attempt-2.diff:88). Scanning the heading with that list would fail the real file. | Pin the whole Wave 0 bullet as one exact string in the test. The check fails on any change to the bullet, whatever words are used. A separate small test proves the pinned string has no gate in it. The mutation cases edit the heading, the loading sentence and the `off` sentence. |
| T9.AC2 | Not missed: met twice (review-2.md:5, review-1.md:4). The text is the output row at attempt-2.diff:17, and the test is at attempt-2.diff:144-154. | Re-apply attempt-2.diff:17 and :144-154 unchanged. |
| T9.AC3 | Not missed: met (review-2.md:6). Lint and both test directories passed (extras-2.log:1-6). | Re-run the exact AC3 command after the change. |
| T9.AC4 | Not missed: met (review-2.md:7). The fence and string checks are at attempt-2.diff:166-180. | Re-apply attempt-2.diff:166-180 unchanged. |
| T9.AC5 | Not missed: met (review-2.md:8). | `make sync-dev`, then `make verify-sync`. |

differs-by: The check compares the whole bullet, heading included, to one pinned exact string, instead of scanning part of it for banned words. A small separate test checks the pinned string itself, with the heading, the `off` sentence and the two event names removed first.

steps:
1. Re-apply the four SKILL.md changes byte for byte from attempt-2.diff: lines 9, 17, 25 and 33. Do not reword the bullet at line 33.
2. In tests/pr_submit/test_merge_guard_protocol.py, re-add attempt-2.diff:47-180 with these changes:
   - Add a constant `WAVE0_HEADING = "- **Wave 0 merge-guard hook (every ordinal, both modes):**"`.
   - Add a constant `WAVE0_OFF`, built from `OFF_LINE`, holding the exact `off` sentence: "At L3 with `--merge-guard off`, print \"…\" once and make no draft-state call."
   - Add a constant `WAVE0_BULLET` = `WAVE0_HEADING` + " " + the loading sentence copied exactly from attempt-2.diff:33 + " " + `WAVE0_OFF`. Split it with implicit string joining so ruff line length passes.
3. In `_wave0_problems`, keep the "missing or repeated", "after the Wave 1 bullet" and "lacks" checks (attempt-2.diff:62-80). Delete the banned-word scan (attempt-2.diff:81-90). In its place, if the bullet is not exactly `WAVE0_BULLET`, add a problem whose message contains the word "gate", for example "the bullet differs from the pinned ungated text (a gate or other edit)".
4. Add `test_the_pinned_wave0_text_names_no_gate`. It asserts that `WAVE0_HEADING` contains "every ordinal, both modes". It then removes `WAVE0_HEADING`, `WAVE0_OFF`, `draft_guard_requested` and `draft_guard_settled` from `WAVE0_BULLET` and asserts nothing in the rest matches `\bL\d\b|level|ordinal|monitor|draft|mode|only|tier`. This keeps the pin from fixing a gated bullet in place. The real loading sentence holds none of these words outside the event names (attempt-2.diff:33).
5. Rewrite the mutation test. Keep the moved-bullet case and the off-line-removed case (attempt-2.diff:103-109 and :124). Replace the single-spot loop (attempt-2.diff:110-123) with (old, new) edits, applied once each to the real text:
   - heading: "(every ordinal, both modes)" → "(L3 only)", and → "(draft mode)"
   - loading sentence: insert "at level 3, ", "at L3, ", "when the PR is a draft, " and "with --monitor 3, " before "or when the run log already holds"
   - one wording no banned-word list would catch: "once the PR is marked ready for review, "
   - `off` sentence: "At L3 with" → "At L3 in draft mode with"

   For each edit, first assert the edited text differs from the original so the case cannot pass without changing anything, then assert some problem contains "gate".
6. Run `make sync-dev`, then the exact AC3 pytest command, `make verify-sync` and `make lint`. Confirm SKILL.md still has one python fence and no `src/superclaude` string; the test at attempt-2.diff:166-180 checks this.

Relevant files:
- /home/coder/workspaces/worktrees/IronClaude/issue-375-pr-submit-draft-guard/.dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/retries/T9/attempt-2.diff
- /home/coder/workspaces/worktrees/IronClaude/issue-375-pr-submit-draft-guard/.dev/tasks/to-do/TASK-WF-designSpec-20261107-075614/artifacts/retries/T9/review-2.md
- /home/coder/workspaces/worktrees/IronClaude/issue-375-pr-submit-draft-guard/tests/pr_submit/test_merge_guard_protocol.py
- /home/coder/workspaces/worktrees/IronClaude/issue-375-pr-submit-draft-guard/src/superclaude/skills/sc-pr-submit-protocol/SKILL.md

Not checked: I did not run any test. Risk: the exact-string pin fails on any later edit to the bullet, including harmless ones, and that is on purpose.
