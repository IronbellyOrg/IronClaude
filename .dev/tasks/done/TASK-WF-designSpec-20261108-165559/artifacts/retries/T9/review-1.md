# T9 review 1 (spec compliance)

Start snapshot: 423b71c73ce63d71db2e7b853b96978b0f71e62d (a tree object). Reviewed live HEAD 9c3b7a2aa (commit C, `feat(hooks): deny L2 hook tampering in the L1 guard (#441)`). All five scoped paths are committed; `git status --porcelain` on them is empty, so no `??` path needed a separate read. Every scoped path was read in full or by its full diff.

## Earlier blocking findings

None (first review).

## Evidence run by this reviewer

- `uv run pytest tests/hooks/test_launch_level_guard_l2_tokens.py -q`: 131 passed.
- `cmp src/superclaude/hooks/scripts/launch-level-guard.sh plugins/superclaude/hooks/scripts/launch-level-guard.sh`: identical.
- `git diff --stat HEAD~1 -- tests/hooks/test_launch_level_guard.py`: empty. `git diff --stat 423b71c7 -- tests/hooks/test_launch_level_guard.py`: empty.
- `uv run pytest tests/hooks/test_launch_level_guard.py tests/cli/test_install_hooks.py -q`: 3881 passed. `make verify-sync`: "All components in sync."
- Commit C body ends with `Co-Authored-By: Claude Code <noreply@anthropic.com>` and names SD-2; commit C stages no `.claude/` path (18 files under `.dev/tasks/`, `docs/`, `plugins/`, `src/`, `tests/`).
- Guard probes (levels W, WA, F, FS, through the #440 test helpers): `git --config-env=include.path=V push origin x` and `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=include.path GIT_CONFIG_VALUE_0=/tmp/c git push origin x` exit 2 at every level with the LL-UNKNOWN text ("a git or gh command the guard does not recognise"), not LL-TAMPER. `git push --No-Verify origin x` exits 2 with the new LL-TAMPER text.
- U-2 re-check against the local `origin/master` ref (085afc8d1, fetched 2026-11-08 23:06 UTC): `git log 5dc29d23..origin/master -- <guard> <mirror>` has no commits; `tests/hooks/test_launch_level_guard.py` was changed by 085afc8d1 (#440, #457). That commit keeps every helper the new test imports (`DESIGN`, `HOOK`, `LEVEL_FILES`, `LEVEL_ORDER`, `ROOT`, `_assert_decision`, `_bash`, `_bind`, `_edit`, `_run`).

## Acceptance criteria

- T9.AC1 met: T9.AC1@tests/hooks/test_launch_level_guard_l2_tokens.py:142 (mirror byte test; suite 131 passed) and src/superclaude/hooks/scripts/launch-level-guard.sh:712 (second lowercased tamper case); `cmp` of the two guard copies is clean.
- T9.AC2 met: T9.AC2@.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t9-u2-check.md:11 ("Result: no U-2 conflict"); `git diff --stat HEAD~1 -- tests/hooks/test_launch_level_guard.py` is empty, and HEAD~1..HEAD is commit C.

## Findings

F1.1 ac=scope at=.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/spec-deviations.md:22 anchor=src/superclaude/hooks/scripts/launch-level-guard.sh:712 chk=n,y,n,n family=doc-claim-overreach fix=Narrow the sentence, for example: "A transport that names core.hooksPath or hook.pre-push still adds TAMPER; one that reaches the hook only indirectly (for example include.path) is denied by its L1 class (UNKNOWN) instead." covers="where code and spec disagree ... list it in that commit's body for owner review": SD-2 says "A transport that disables the hook still names `core.hooksPath` or `hook.pre-push`, so it still adds `TAMPER`." That is false as written. `--config-env=include.path=V` or `GIT_CONFIG_KEY_0=include.path` can load a config file that sets core.hooksPath without naming it, and the token list at :712 (no `--config-env`, `git_config_*` or `include.path`) does not add TAMPER for it; the probe shows LL-UNKNOWN at all four levels. Denial still holds at every level, so there is no safety gap, only a claim wider than its evidence.

F1.2 ac=scope at=src/superclaude/hooks/scripts/launch-level-guard.sh:712 anchor="add the second tamper `case` (spec FR-050..FR-052) ... as in source §7.5" chk=n,n,n,n family=owner-approved-deviation fix=None needed; keep SD-2 and the commit-body note for owner review. covers="add the second tamper `case` (spec FR-050..FR-052) ... as in source §7.5": The case drops 4 of the 10 tokens in FR-050 and source §7.5:538,540 (`*--config-env*`, `*git_config_count*`, `*git_config_parameters*`, `*git_config_key_*`). This is recorded as SD-2 (spec-deviations.md:17-23), with owner decision msg_dcfefa6f29e4 noted at .dev/issues/441/handoff-implement.md:30, and the commit C body names it. The stated reason (adding them would change pinned message ids in the read-only #440 file, NFR-009) is plausible; I did not re-run that counterfactual. The owner decision itself could not be checked beyond those records. AC-7's `--config-env` and `GIT_CONFIG_*` forms carrying core.hooksPath are pinned as TAMPER (test file :58-59, :107-114). Not counted as a breach because the owner approved the change.

F1.3 ac=T9.AC2 at=.dev/tasks/to-do/TASK-WF-designSpec-20261108-165559/artifacts/t9-u2-check.md:6 anchor="origin/master: 2c8109b30aee2a5170b2c097b3c0b41c239dc464 (2 commits ahead: #453, #455)" chk=n,n,n,n family=stale-record fix=Optionally add a dated line: origin/master later moved to 085afc8d1 (#457, #440), which changes tests/hooks/test_launch_level_guard.py only, not the guard; U-2 still holds and the imported helpers are unchanged. covers="the U-2 result is recorded in `./artifacts/t9-u2-check.md`": The record was true when it was made, but the local origin/master ref now points at 085afc8d1 (fetched 23:06 UTC, before commit C at 23:14 UTC). Line 7's "no commits" for `tests/hooks/test_launch_level_guard.py` is now out of date. The U-2 question (did #440 change the guard) still answers no, so the AC outcome stands. A later rebase brings in the #457 test changes, but the helpers that test_launch_level_guard_l2_tokens.py imports are unchanged.
