# Spec deviations: TASK-WF-designSpec-20261108-165559 (#441)

Each entry names the spec rule, what the code does instead, who approved it, and the tests that pin it.

## SD-1: FR-001 allows `/usr/bin/stat` for the data-file mode check

- **Spec rule.** FR-001 (`.dev/brainstorms/20261108-094705-l2-pre-push-guard/merged-requirements.md:113`): the hook uses only bash builtins plus `/usr/bin/env` and `/usr/bin/timeout`.
- **Conflict.** FR-020 requires the data file `pre-push.launch-level` to be neither group- nor other-writable (`mode & 0o022 == 0`). Bash has no builtin that reads mode bits, so FR-020 cannot be met under FR-001 as written.
- **Owner decision.** msg_38e4a99261a7 (2026-11-08): allow `/usr/bin/stat` by absolute path with fixed arguments only (no PATH lookup, no user-controlled argv), and fail closed.
- **What the hook does.** `src/superclaude/hooks/scripts/launch-level-pre-push.sh` (`l2_data`, plugin mirror byte-identical) runs `/usr/bin/timeout 5 /usr/bin/stat -c '%a %s' -- "$L2_DATA"` with stdin from `/dev/null` and stderr discarded. The only variable argument is the data-file path, which the hook derives from its own location (`${0%/*}/pre-push.launch-level`).
- **Fail closed.** If stat is missing, exits non-zero, times out after 5 s, prints anything other than `<octal mode> <size>`, or reports a mode with a group- or other-write bit, `l2_data` fails. The actor is then unknown, with the reason `no valid data file`, so a push to refs/heads/main or refs/heads/master is refused (OD-2) and pushes to other refs are allowed.
- **Tests** (`tests/hooks/test_launch_level_pre_push.py`):
  - `test_t18_stat_missing_failing_or_hanging_fails_closed[stat-missing|stat-fails|stat-hangs]`: swaps the stat path in the installed hook copy for a missing, an `exit 1`, or a 30 s sleep stand-in. Main is refused with `no valid data file`; a feature branch is allowed.
  - `test_t18_invalid_data_file_or_selector[data-group-writable|data-other-writable]`: mode 0o664 or 0o646 on the data file. Main is refused with `no valid data file`.
- **Version line.** It stays at `# launch-level-pre-push-version: 1` because the hook has not been released. The sha256 pin `L2_HOOK_SHA256` in `tests/cli/test_install_hooks.py` was updated to the new bytes.

## SD-2: FR-052 drops the config-transport tokens from the TAMPER case

- **Spec rule.** FR-052 (`.dev/brainstorms/20261108-094705-l2-pre-push-guard/merged-requirements.md:225`): `hookspath`, `--config-env`, `hook.pre-push` and the `GIT_CONFIG_*` names add `TAMPER` through the FR-050 case.
- **Conflict.** Adding `TAMPER` for `--config-env`, `git_config_count`, `git_config_parameters` and `git_config_key_` changes the denial message of 4 commands from `LL-UNKNOWN` / `LL-PUSHFORM` to `LL-TAMPER`, because TAMPER has message precedence. The #440-owned, read-only `tests/hooks/test_launch_level_guard.py` pins those messages (`test_git_grid_oracle[UNKNOWN-2]`, `test_git_named_cases[g18]`, `test_push_form_reject_cases[PR9]` and `[PR19]`): 16 failures across 4 levels. NFR-009 forbids editing that file. Analysis: `.dev/issues/441/ponytail-t9.md`.
- **Owner decision.** msg_dcfefa6f29e4 (2026-11-08): option (c), drop the 4 transport tokens from the guard and its mirror; no edit to the #440 test file.
- **What the guard does.** The second lowercased tamper `case` in `src/superclaude/hooks/scripts/launch-level-guard.sh` (plugin mirror byte-identical) matches `*.git/hooks*`, `*hooks/pre-push*`, `*pre-push.launch-level*`, `*--no-verify*`, `*hookspath*` and `*hook.pre-push*` only. The 4 transport forms are still denied at every level by their existing L1 classes (UNKNOWN or PUSH/PUSHFORM), with their old message ids. A transport that names `core.hooksPath` or `hook.pre-push` still adds `TAMPER`. One that reaches the hook only indirectly, for example `git --config-env=include.path=V push` or `GIT_CONFIG_KEY_0=include.path`, does not; it is still denied at every level, by its L1 class (`UNKNOWN`, message `LL-UNKNOWN`).
- **Tests** (`tests/hooks/test_launch_level_guard_l2_tokens.py`): `test_transport_only_forms_keep_their_ids` pins `--config-env=alias.ci` to UNKNOWN and `GIT_CONFIG_COUNT=1 git push` to the push ids, and the two `include.path` forms to UNKNOWN; the TAMPER table pins the hooksPath and `hook.pre-push` forms carried by `--config-env` and `GIT_CONFIG_*`.
