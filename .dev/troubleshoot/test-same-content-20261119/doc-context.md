# Documentation Context Card

**Generated**: 2026-11-19T01:24:30Z
**Wave**: 1.5
**Scope**: src/superclaude/cli/install_keep.py

## Release context

- **Release**: None found
- **Artifacts**: none
- **Summary**: No PRD, TDD, spec or roadmap under `.dev/releases/` scopes `install_keep.py` or the keep-or-backup behaviour.
- **Confidence**: n/a

## Architectural docs consulted

- `docs/getting-started/upgrading.md` — verdict: `current` — says an upgrade overwrites every shipped file and keeps no backup of edited ones; no content-comparison rule.
- `docs/getting-started/installation.md` — verdict: `current` — `--force` overwrites existing files; settings.json is backed up before a merge.
- `docs/user-guide/freshness-hooks.md` — verdict: `current` — settings.json backup before hook installs (different code path).
- `docs/reference/troubleshooting.md` — verdict: `current` — settings.json restore recipe.
- `docs/designs/orchestrator-mode.md` — verdict: `current` — only a tangential use of `filecmp.cmp` in a test.

Currency used git commit dates because every file mtime is the worktree checkout time.

## Restrictions / decisions that constrain the fix

- `src/superclaude/cli/install_keep.py:19` (same_content) — "True only when both files are readable and byte-identical."
- `src/superclaude/cli/install_keep.py:39` (backup_if_differs) — "Returns ``None`` when the files already match. Raises ``OSError`` when the copy cannot be made; the caller must then leave ``target`` untouched."
- `src/superclaude/cli/install_keep.py:3` (module) — "a kept file that differs from this version's copy is stale or customized and should be named in the report."
- `src/superclaude/cli/install_user_setup.py:77` and `src/superclaude/cli/install_commands.py:65` — callers rely on a correct "differs" answer to report stale files and to save a backup before a forced overwrite.

## Re-frame signals

- The documented contract of `same_content` is exactly what the test asserts, so the test is right and the code is what can break it; the diagnosis is not a doc-versus-expectation case.
- A false "identical" answer would hide a stale file from the install report and skip the backup before a forced overwrite, so the cache behaviour is a real, if small, contract risk and not only test flakiness.
- `docs/getting-started/upgrading.md` ("keeps no backup") may be out of date against `install_keep.py` (#480, 2026-11-09), which saves a differing file as `<name>.bak.<stamp>` before a forced overwrite. That is a separate doc finding, not part of this fix.
