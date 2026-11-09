# T6 install choices (U-1, U-8, U-13, U-14(c))

File: `src/superclaude/skills/sc-issue-protocol/scripts/orca_worktree.py` (uncommitted; commit B at T8).

## U-1: git floor for `--path-format`

- Finding: `git rev-parse --path-format=absolute` was added in git 2.31.0 (RelNotes 2.31.0, https://github.com/git/git/blob/master/Documentation/RelNotes/2.31.0.adoc). Local git is 2.47.3.
- Choice: `_l2_preconditions` (line 1257) compares `--git-path hooks/pre-push` with `--git-common-dir`/hooks/pre-push; any git failure or mismatch returns `unsupported` with "git's pre-push hook path is not <hooks>/pre-push (needs git 2.31 or later)" (line 1280). No separate version probe: an older git fails the flag and lands in the same reason.

## U-8: which HOME the agent sees

- Finding: `cmd_launch` (line 1591) passes no HOME and no environment to `orca agent launch`; `--environment` there selects a saved Orca server, not process env.
- Choice: HOME comes from `home_dir()` (OC-8) in `l2_data_expected` (line 1126). That this equals the launched agent's HOME is UNVERIFIED (no Orca source read proves it).

## U-13: reason wording

Constants (lines 1057-1063): `L2_WHY_HOOKSPATH` "core.hooksPath is set, so git does not run hooks from the common hooks directory"; `L2_WHY_CONFIG` "git config unreadable"; `L2_WHY_HOOKS_DIR` "hooks-dir-unsafe"; `L2_WHY_NO_UV` "uv was not found on PATH"; `L2_WHY_NO_HOOK` "no pre-push hook".
f-strings: "the packaged hook <src> is missing or not version 1" (1316); "HOME or the uv directory is not a single-line absolute path" (1323); "the hook self-test failed at step <step>" (1348); "write failed: <strerror>" (1356).
Conflict suffix (`_l2_conflict`, line 1169): "<why>: remove both files with `rm <hooks>/pre-push <hooks>/pre-push.launch-level` and claim again; the claim never deletes them". Conflict whys: symlink, foreign, stale, not executable, data-file-differs.

## U-14(c): self-test timeout

- Choice: `L2_SELFTEST_TIMEOUT = 30.0` (line 1047): above the hook's own 10 s selector bound, under `DEFAULT_TIMEOUT = 120.0` (line 82).

## Other choices (beyond the plan text)

1. `run()` (line 126) gained `env` and `input` parameters; `input` is needed to feed push lines to the staged hook in `_l2_selftest` (line 1200).
2. `git config --worktree --get core.hooksPath` was dropped: it exits 128 in a linked worktree without `extensions.worktreeConfig`. Only plain `config --get` is used (line 1262); rc 0 = unsupported hookspath, rc other than 0/1 = "git config unreadable".
3. The selector regex `_L2_SELECTOR_RE` (line 1065) accepts all five shapes s1-s5, matching the hook.
4. An existing data file that differs makes the entry verdict `conflict data-file-differs` (line 1196, OC-12), and the same at publish time (line 1336).
5. Any OSError while publishing maps to `unavailable` "write failed: ..." (line 1356); the private `.<uuid>` directory is always removed in `finally`.
6. The packaged hook must be a regular non-symlink file containing the version-1 line, else `unavailable` (line 1316).
7. Publishing never replaces a file: `publish_no_replace` (line 1087) links a fsynced temp file with `os.link`; FileExistsError returns False.

## Smoke evidence (`./t6-smoke.py`, run on a temp HOME and temp repo)

```
first: ('installed', '')
others unchanged: True new: ['pre-push', 'pre-push.launch-level']
second: ('owned', '')
entries: ['pre-push', 'pre-push.launch-level']
data-differs: conflict
foreign: conflict
hookspath: ('unsupported', 'core.hooksPath is set, ...')
linked: ('installed', '') True
```
