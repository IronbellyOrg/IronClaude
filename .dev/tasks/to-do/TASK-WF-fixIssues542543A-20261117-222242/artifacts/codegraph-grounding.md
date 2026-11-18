# Codegraph grounding

## Run state

- index_state: stale (`codegraph_status` reported "Changes since index: unknown" and 199585 pending references from an interrupted index run)
- checked_at: 2026-11-17T22:23:30Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/v6-ic-launcher-fixes
- access: mcp (status only used); token `graph:stale`
- floor used: Glob, Grep, Read. The subject is a bash script, which codegraph does not index (only `src/superclaude/cli/ic.py`, a 6-line launcher, is indexed).

## Resolved symbols

- `src/superclaude/scripts/ic`: `resolve` (file line 37), `apply_preset` (48), the main parse loop (72 to 96), the `AIENV` source block (25 to 31), the help handler (80 to 82). Read in full.
- `src/superclaude/cli/ic.py`: `main` (execs `bash <script> "$@"`). Read in full.
- `src/superclaude/cli/sprint/aienv.py`: comment lines 39 and 40 cite `ic:61-63` and `ic:98`. Read.

## Dependents

- `resolve` callers (Grep, call sites read): `apply_preset` lines 61, 62, 63; main loop lines 75, 76, 77, 89. Resolution: call-site-verified by Read.
- `ic` script consumers: `src/superclaude/cli/ic.py:12-15`; packaging checks `tests/unit/test_cli_install.py:477,938-940`; comment citations in `src/superclaude/cli/sprint/aienv.py:39-40`.
- Mirrors: none (`.claude/`, `plugins/superclaude/` hold no copy).

## Pre-check

Done after the gate passed (Grep and Read, no codegraph): all files named by Tasks 1 to 4 exist (`src/superclaude/scripts/ic`, `src/superclaude/cli/sprint/aienv.py`, `tests/unit/test_cli_install.py`, `tests/sprint/test_aienv.py`; `tests/cli/test_ic_launcher.py` is created by Task 1). The symbols `resolve` and `apply_preset` resolve in the script, and the line numbers quoted in the tasks match the file as read. No dependent of the touched symbols is missing from the tasks. 4 tasks checked, 0 problems.
