# Codegraph grounding

## Run state

- index_state: stale
- token: graph:stale
- checked_at: 2026-11-17T19:53:40Z
- worktree_root: /home/coder/workspaces/worktrees/IronClaude/v6-cleanup-audit-runner
- projectPath: /home/coder/workspaces/worktrees/IronClaude/v6-cleanup-audit-runner
- access: mcp (lookup tools listed)
- reason: `codegraph_status` answered "Changes since index: unknown (measurement timed out or failed)" with two files pending sync. Not `fresh`, so this run used Grep, Glob and Read for the plan. Earlier in the session (before this run), `codegraph_callers cleanup_audit_group` and `codegraph_impact execute_cleanup_audit` were called; they are leads and were confirmed by Grep below.

## Resolved symbols

- `cleanup_audit_group`: defined `src/superclaude/cli/cleanup_audit/commands.py:19`, re-exported `src/superclaude/cli/cleanup_audit/__init__.py:9-11`.
- `execute_cleanup_audit`: `src/superclaude/cli/cleanup_audit/executor.py`; called only from `cleanup_audit/commands.py:89`.
- `_KNOWN_CLI_MODULES`: `src/superclaude/cli/cli_portify/config.py:24`, read once at `config.py:282`.
- `_PACKAGE_RESOURCES["cli"]`: `tests/unit/test_cli_install.py:70-72`, read by `_assert_present` at `tests/unit/test_cli_install.py:894`.

## Dependents

- Importers of `superclaude.cli.cleanup_audit` outside the package: `src/superclaude/cli/main.py:527` (import) and `main.py:529` (registration), confirmed by `git grep -n cleanup_audit` (resolution: call-site-verified by Grep). Tests: `tests/test_cleanup_audit_structure.py` only.
- Names without an import: `tests/cli/test_cli_registration.py:33` (expected top-level command set), `tests/swarm/test_cli_registration.py:7,86`, `tests/unit/test_cli_install.py:72` (baseline package member that must exist, so it must be removed from the list), `src/superclaude/cli/cli_portify/config.py:29-30`.
- Docs: listed in `.dev/cleanup/cleanup-audit-runner/dependency-map.md`.

## Pre-check

Run after the gate, floor only (Grep, Read; index_state stale).

- 16 of 16 named files exist; the runner directory has 13 files plus `__pycache__` (14 entries).
- Dependents of the touched symbols that no task names: none found. Watch item: `visual-architecture-summary.md` lines 291 and 295 (`K1 --> K5`, `K1 --> P`) also use node `K1`; Task 15 covers them through "any further K1 lines".
- `docs/generated/sprint-cli/04-gates-validation.md:198` text matches Task 17.
