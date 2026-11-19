## What was tried
Found while reviewing the fix for the stale-cache bug in `install_core.py` (issue 606 branch). `src/superclaude/cli/install_keep.py:3-7` says `install --force` and `update` save a differing file next to itself (`<name>.bak.<UTC stamp>`) before overwriting it. The core-file installer does not do that: with `force=True`, `install_core_files` copies with `shutil.copy2` and no backup (`src/superclaude/cli/install_core.py:71-77`), and `update` always passes `force=True` (`src/superclaude/cli/main.py:365`). A user-edited `~/.claude/RULES.md` or `~/.claude/CLAUDE.md` is therefore overwritten with no copy kept. Checked by reading the code only; nothing was run to reproduce it.

For comparison (read, not run):
- Backs up: `src/superclaude/cli/install_commands.py:68` and `src/superclaude/cli/install_user_setup.py:95` call `backup_if_differs`.
- Does not back up: `src/superclaude/cli/install_core.py:76`, `src/superclaude/cli/install_agents.py:56`, `src/superclaude/cli/install_templates.py:76` copy with `shutil.copy2` only.

## Relevant files and links
- `src/superclaude/cli/install_keep.py` (`backup_if_differs`, `same_content`)
- `src/superclaude/cli/install_core.py` (`install_core_files`)
- `src/superclaude/cli/main.py` (`install` at line 178, `update` at line 365)
- `src/superclaude/cli/install_agents.py`, `src/superclaude/cli/install_templates.py`
- Branch `ironbelly/issue-606` (the stale-cache fix that surfaced this); review report `.dev/reflect/pre-makeInstallCoreS-20261119-tier2/REPORT.md` (finding INV-008, recommendation R-003)

## Done when
A decision is recorded for each installer that overwrites with `force=True`: either it calls `backup_if_differs` like the commands and user-setup installers, or the docstring in `install_keep.py` and the user guide say plainly which installers keep a backup and which do not. If backups are added, a test overwrites a user-edited file with `force=True` and finds the `.bak.<stamp>` copy next to it.

## Pick-up note
This is a lead, not a confirmed defect report: it may be deliberate that core files, agents and templates are treated as shipped files rather than user-owned ones. Check with the owner before changing behaviour. `backup_if_differs` raises `OSError` when the copy cannot be made and the caller must then leave the target untouched (`install_keep.py:39-44`), so adding it also changes failure behaviour for those installers.
