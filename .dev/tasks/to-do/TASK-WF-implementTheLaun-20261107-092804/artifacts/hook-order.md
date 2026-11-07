# Task 14: the guard and the job identity hook on the same payload (finding F3)

Test: `tests/hooks/test_launch_level_guard_with_identity.py` (6 passed, log `t14-test.log`).
Each case runs `src/superclaude/hooks/scripts/launch-level-guard.sh` and
`src/superclaude/hooks/scripts/launch-job-identity.sh` one after the other on the
same PreToolUse Bash payload, with a temporary HOME, `CLAUDE_CONFIG_DIR` unset, a
PATH holding only a temporary bin directory (cat, sed, tr, mkdir, mv, ln, rm, jq,
uv), `UV_PYTHON` set to the test interpreter and `UV_PYTHON_DOWNLOADS=never`. The
real `~/.claude` is never read or written. Both hooks read the same store:
`$HOME/.claude/state/launch-level/sessions/<session_id>`.

## Observed results of the four cases

| Case | Session file | Command | Guard | Identity hook |
|---|---|---|---|---|
| 1 | `full-submit` | `git status` | exit 0, silent | exit 0; `updatedInput` equal to `tool_input` except `command`, which becomes `/bin/bash <script> execute <sid> <tool_use_id> 'git status'`; no `permissionDecision` |
| 2 | `worktree` | `git commit -m wip` | exit 2, header "level worktree", "Blocked: creating a commit", no LL-STATE note | exit 0 with the same kind of rewrite (recorded; not part of the decision, the guard's exit 2 blocks) |
| 3 | none for this id (another session bound) | `git commit -m wip` | exit 0, silent | exit 0, silent |
| 4 | `degraded` (with and without a trailing newline) | `git commit -m wip` | exit 2, header "level worktree", "Blocked: creating a commit", LL-STATE note | exit 2, stdout empty, stderr `launch job: governed Bash call cannot be wrapped safely` |
| 4 | `degraded` | `git status` | exit 0, silent | exit 2, same message |

Case 1 also checks that the guard decides on the original command. An extra test
copies the identity script to `$HOME/.claude/hooks/launch-job-identity.sh`, where
the installer puts it. Its rewrite then names that real path. Fed that rewrite,
the guard blocks `git status` at full-submit as LL-TAMPER ("touching the
launch-level state ...") because the text contains `.claude/hooks`. So the
composition works only if Claude Code gives the guard the original input, not
the identity hook's `updatedInput`.

## Not observed here

The order in which Claude Code runs two matching PreToolUse hooks is not
observed. Neither is whether one hook's `updatedInput` reaches a later hook, or
how Claude Code combines one hook's block (exit 2) with another hook's
`updatedInput`. These tests run the scripts directly, not inside Claude Code.
Finding the answer needs a live governed session. The pending live observations
in `tests/hooks/test_launch_level_observations.py` (OB-H1 items 1 to 9, OB-H2,
OB-H3, OB-CTX) are skipped tests that have not been run. None of them names hook
ordering explicitly, so this check should be added to OB-H3 (live sessions at
each level). The identity hook's own text also says "concurrent hook rewrite
ordering ... unverified".

Registration order for the record: since Task 13 the installer inserts a missing
guard registration before the launch-job-identity registration on an upgrade.
On a fresh install and on an upgrade the guard therefore comes before the
identity hook in PreToolUse, as in the shipped `hooks.json`. The test does not
assert any position in an installed `settings.json`, and a position in the file
does not prove the order of execution.

## The degraded word

- **Identity hook:** its supported set is `LEVELS = {worktree, full, full-submit}`,
  with one optional trailing newline. Any other word in an existing session file,
  `degraded` included, fails `governed()`. In hook mode that prints
  `launch job: governed Bash call cannot be wrapped safely` and exits 2 for
  every Bash call of that session. It never treats the session as ordinary.
- **Guard:** any word other than the three is level worktree with the LL-STATE
  note. Allowed calls stay silent, and blocked calls show the note. Asserted by
  `test_degraded_word_guard_worktree_with_state_note_identity_blocks_all`.
- **Mismatch found:** the guard writes `degraded` itself (binding rules B11 and
  B12: a used or missing nonce with a leading marker, and a bad taken record),
  and treats it as worktree. The identity hook blocks every Bash call of such a
  session, including read-only ones like `git status` that the guard allows. A
  degraded session therefore cannot run Bash at all, which is stricter than
  design section 9 describes. It fails closed, so it is not a safety gap.
- **Proposed resolution:** in a separate change to `launch-job-identity.sh` (not
  made here, per the plan's constraint), add `degraded` to its `LEVELS` so a
  degraded session is wrapped and identified as governed like a worktree session,
  and leave its strictness to the guard.
