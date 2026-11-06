# Analysis report: src/superclaude/cli/install_core.py

- Command: `/sc:analyze src/superclaude/cli/install_core.py --focus quality --depth quick --unattended --report-dir .dev/p1-live/analyze/`
- Focus: quality. Depth: quick (static read of the file plus a check of its callers and the core folder it installs from).
- Source modified: none.

## Metrics

| Item | Value |
|---|---|
| Lines | 156 |
| Functions | 4 (`install_core_files`, `_get_core_source`, `list_core_files`, `list_installed_core_files`) |
| Module constants | 1 (`KNOWN_CORE_FILES`, 12 names) |
| `KNOWN_CORE_FILES` vs `src/superclaude/core/*.md` | identical (12 of 12 match, checked by listing the folder) |
| Callers outside the file | `cli/main.py` (lines 71-90, 178, 354-365); tests in `tests/cli/` |

## Findings

No high or critical findings. Four low-severity items.

| # | Severity | Location | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Low | `install_core.py:98-99` | The `if not installed and not skipped and not failed` branch cannot run. `core_files` is non-empty (line 59 returns early otherwise), and every loop pass appends to `skipped`, `installed` or `failed`. | Delete the branch. |
| 2 | Low | `install_core.py:107-126` | `_get_core_source` has one real check (`package_root / "core"`) and returns the same path whether it exists or not, so the `if` at line 122 does nothing. The docstring lists two locations and a "Priority 1" with no priority 2. | Collapse to `return Path(__file__).resolve().parent.parent / "core"` and fix the docstring. |
| 3 | Low | `install_core.py:32` | `target_path: Path = None` is typed as `Path` but defaults to `None`. | Type it `Optional[Path]`. |
| 4 | Low | `install_core.py:12-28, 156` | `list_installed_core_files` only reports names in the hand-kept `KNOWN_CORE_FILES`, while `install_core_files` copies every `*.md` in the core folder. A new core file added to the folder is installed but not listed until someone also edits the set. The set matches the folder today, and a test cited in `tests/cli/test_issue_body_templates.py` pins this. | No change needed now; keep the pinning test. |

## Checked and fine

- Failures per file are collected and returned (`success = len(failed) == 0`), not swallowed.
- `Path.home()` is read at call time, so tests can patch it.
- Callers in `cli/main.py` use the `(success, message)` return as designed.

## Not checked (quick depth)

Test coverage depth, Windows path behaviour, partial-copy atomicity, and behaviour with symlinked core files.
