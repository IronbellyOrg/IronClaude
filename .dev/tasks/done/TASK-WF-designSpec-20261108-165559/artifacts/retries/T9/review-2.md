# T9 review 2 (spec compliance, adversarial)

Reviewed tree: worktree at HEAD 82eb3123a (commit C, `feat(hooks): deny L2 hook tampering in the L1 guard (#441)`), against start tree 423b71c73ce6. All five listed paths are committed (no `??` entries); the diff is 183 insertions, 3 deletions over the five paths.

## Earlier blocking findings

None were given in the prompt slot (empty), so there is nothing to mark resolved, open or regressed.

## Saved-probe re-check (doc-claim-overreach family)

- `.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/spec-deviations.md:22`: true. Checked by running the guard (through the #440 test helpers `_bind`/`_run`/`_bash`) at W, WA, F and FS:
  - The second case matches only the six listed tokens (`src/superclaude/hooks/scripts/launch-level-guard.sh:711-712`).
  - `GIT_CONFIG_PARAMETERS="'core.hookspath'='/dev/null'" git push origin x` and `git -c HOOK.PRE-PUSH.enabled=false push origin x` give LL-TAMPER at all four levels. So a transport that names `core.hooksPath` or `hook.pre-push` adds TAMPER.
  - `git --config-env=include.path=V push origin x` and `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=include.path GIT_CONFIG_VALUE_0=/tmp/c git push origin x` give the LL-UNKNOWN text (`launch-level-guard.sh:79`) at all four levels.
  - "The 4 transport forms are still denied ... with their old message ids" refers to the four #440-pinned commands in the sentence before it (`spec-deviations.md:19`), and the #440 test file passes unchanged.
- `src/superclaude/hooks/scripts/launch-level-guard.sh:710` (and its byte-identical plugin copy): true. `--config-env` and the `GIT_CONFIG_*` names are absent from the case at `:711-712`, so they keep only the classes L1 already gives them.

## AC verdicts

- **T9.AC1 met.** Cited at `.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/TASK-WF-designSpec-20261108-165559.md:131`.
  - `uv run pytest tests/hooks/test_launch_level_guard_l2_tokens.py tests/hooks/test_launch_level_guard.py -q`: 3971 passed, exit 0. The new file is at `tests/hooks/test_launch_level_guard_l2_tokens.py:1-160`.
  - `cmp src/superclaude/hooks/scripts/launch-level-guard.sh plugins/superclaude/hooks/scripts/launch-level-guard.sh` exits 0, and `tests/hooks/test_launch_level_guard_l2_tokens.py:149-151` pins this.
  - `make verify-sync` prints "All components in sync."
- **T9.AC2 met.** Cited at `.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/TASK-WF-designSpec-20261108-165559.md:132`.
  - `git diff --stat HEAD~1 -- tests/hooks/test_launch_level_guard.py` is empty, with HEAD = commit C. The diff against the start tree is also empty.
  - The U-2 result is recorded at `.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t9-u2-check.md:11` ("no U-2 conflict"), and the file is tracked.
  - I checked it independently: `git log -3 origin/master -- src/superclaude/hooks/scripts/launch-level-guard.sh` shows only 3b344dd4e (#394/#432), so #440 has not changed the guard on origin/master.

## Brief items checked beyond the AC bullets

- The LL-TAMPER `b=` text names the git hook (FR-054) at `src/superclaude/hooks/scripts/launch-level-guard.sh:95`. The design table row at `docs/designs/sc-issue-launch-level-hook.md:249` matches it, and the `text=True` decisions in the new tests compare the emitted message.
- FR-104 coverage, all in `tests/hooks/test_launch_level_guard_l2_tokens.py`:
  - Edit and Write to both hook files: `:40-47`.
  - Every FR-104 Bash form, `--no-verify` outside a push, and the LIM-16 over-blocks: `:51-74`.
  - The send-pack form, kept denied as UNKNOWN: `:81`.
  - The combined L1/L2 table with named leaks, plus the check that every allowed hidden push is refused by L2: `:102-146`.
  - The mirror check: `:149-151`.
- FR-052 drops the `--config-env` and `GIT_CONFIG_*` TAMPER tokens. This is the owner-approved SD-2 (msg_dcfefa6f29e4, `spec-deviations.md:17-23`), and the commit C body names it, so it is not a finding.
- Commit C rules, all met:
  - The subject is `feat(hooks): ...`.
  - The body ends with `Co-Authored-By: Claude Code <noreply@anthropic.com>`.
  - No `.claude/` path is staged.
  - The staged paths are only `src/`, `plugins/`, `tests/`, `docs/` and `.dev/tasks/`.
  - It is local only.

## Findings

None.

## Self-Audit (zero findings)

- **Tests I ran myself:**
  - Both guard test files: 3971 passed.
  - `make verify-sync`: in sync.
  - `cmp` on the two guard copies: identical.
- **Adversarial probes I ran against the live guard at all four levels:**
  - With an unrelated key, `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=user.name ... git status`, `GIT_CONFIG_PARAMETERS="'user.name'='x'" git status` and `git --config-env=user.name=V status` are allowed.
  - Why this is not a finding: it is the same behaviour as before T9 (source §7.5 "Today: not covered"). SD-2 removed the tokens that would have caught these forms, with owner approval. None of these forms names or reaches the pre-push hook.
  - Read `spec-deviations.md:22` "The 4 transport forms are still denied" as the four pinned commands (`:19`), not as every use of those transports. A reader who takes it more broadly would overread it. The text is true under the reading its own context sets.
- **Not checked:**
  - `GIT_CONFIG_GLOBAL` and `GIT_CONFIG_SYSTEM` file redirection of `core.hooksPath`. These are not FR-050..FR-052 tokens and are outside T9's spec scope.
  - I did not re-run `git fetch`. The U-2 check uses the existing `origin/master` ref (085afc8d1).
- I read no file in a retries folder or `.dev/troubleshoot/`, and I cite none. The prompt itself was the only retries-folder input.
