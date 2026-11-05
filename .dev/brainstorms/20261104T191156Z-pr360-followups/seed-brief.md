---
topic: "Fix the 3 open review findings from PR #360 (pinned Ponytail install) in src/superclaude/cli/install_user_setup.py: symlink-loop resolve() escape, scope-blind stale-pin check, and the CLAUDE_CONFIG_DIR profile mismatch between validation and claude subprocesses; fix the plugin-state paths once where they converge."
domain: code
strategy: systematic
depth: quick
proposals_target: 2
handoff_target: none
created: 2026-11-04T19:12:30Z
---

# Seed Brief: pr360-followups

## Problem Statement

`install_plugins` (src/superclaude/cli/install_user_setup.py, master 605da2ff) must never abort `superclaude install`, must keep the user-scope Ponytail copy at its pinned commit, and must only run pinned plugins through IronClaude's own `ironclaude` directory marketplace. Three review threads on PR #360 show it can fail each promise: `_is_our_catalog` calls `Path.resolve()` (line 292) which raises `RuntimeError`/`OSError` on a symlink loop and escapes the function; the stale check (lines 323-330) accepts any installed record's `gitCommitSha`, so a project-scope copy at the pin hides a stale user-scope copy; and the registry/installed reads use `home/.claude/plugins/...` (line 315) while every `claude plugin ...` subprocess inherits `CLAUDE_CONFIG_DIR`, so the check and the commands can look at different profiles.

## Clarify answers (auto-proceed, quick depth)

1. Entry point: `install_plugins`, `_is_our_catalog`, `_write_catalog` in install_user_setup.py; tests in tests/cli/test_install_user_setup.py.
2. Scope: single module plus its test file.
3. Failure modes to prevent: install aborted by an exception; wrong commit left installed at user scope; a foreign `ironclaude` marketplace used because validation read a different profile than the commands use.

## Known Context

- Real-CLI proof (claude 2.1.318, throwaway HOME=/tmp/ccd-proof.0RIeVX/home, CLAUDE_CONFIG_DIR=/tmp/ccd-proof.0RIeVX/cfg): `claude plugin marketplace add <dir>` and `claude plugin install demo@ironclaude --scope user -y` wrote `plugins/known_marketplaces.json`, `plugins/installed_plugins.json`, `plugins/cache/`, `settings.json` (enabledPlugins + extraKnownMarketplaces) and `.claude.json` directly under `$CLAUDE_CONFIG_DIR` (no `.claude/` segment); nothing was written under HOME.
- With `CLAUDE_CONFIG_DIR=""` the CLI behaves as unset: it wrote `$HOME/.claude.json` and listed no `ironclaude` marketplace (it read `$HOME/.claude/plugins`).
- `installed_plugins.json` records carry `"scope": "user"` or `"scope": "project"` plus `"projectPath"`; one plugin id maps to a list holding both.
- Every other `superclaude install` step (rules, output styles, settings defaults, commands, skills, agents) writes under `Path.home()/.claude`, ignoring `CLAUDE_CONFIG_DIR`. `apply_settings_defaults` writes `enabledPlugins` to `~/.claude/settings.json`, and `install_plugins` reads its wanted list from that same file.
- The only existing `CLAUDE_CONFIG_DIR` resolver is `read_user_mcp_servers` in src/superclaude/cli/install_mcp.py (empty string = unknown, else `expanduser`, else `Path.home()`).
- `install_plugins(home=...)` is the test seam; tests fake `subprocess.run` and assert the exact env passed (`test_plugins_move_ponytail_to_a_new_pin` asserts the marketplace-update env is `None`).
- Paths under the plugin state converge in one place: `home` → `plugins_dir = home / ".claude" / "plugins"` (line 315), plus `home / _CATALOG_DIR` in `_write_catalog` and `_is_our_catalog`, plus `home / ".claude" / "settings.json"` (line 311).

## Constraints

- The plugin step is never fatal: every exception path must return `(True, message)`.
- Minimal diff: one module plus its test file; at most 5 edits allows a direct change, otherwise /sc:workflow.
- Do not change where the other installer steps write (out of scope).
- No new dependency; reuse existing helpers and patterns.
- Never run real `claude plugin` commands against this workspace's ~/.claude.

## Success Criteria

- A symlink-loop catalog path makes `install_plugins` return `(True, "⚠️ ...")` refusing the `ironclaude` registration; other plugins still proceed.
- A project-scope record at the pin plus a user-scope record off the pin yields `claude plugin update ponytail@ironclaude --scope user`.
- With `CLAUDE_CONFIG_DIR` pointing at a profile whose `known_marketplaces.json` holds a foreign `ironclaude`, no `ironclaude` command runs against a profile that was not validated.
- One new test per finding fails before the fix and passes after; existing plugin tests stay green.

## Enrichment Context

- Codebase (fallback_1, native Read/Grep; auggie tool not available): see enrichment/codebase-context.md. Key points: `_is_our_catalog` is called once outside any try block; `known`, `installed` and `settings` are all read under `home/.claude`; subprocess env is inherited (`None`) except `plugin update`; `test_plugins_accept_ours_through_a_symlinked_home` requires symlink resolution to keep working; `test_plugins_move_ponytail_to_a_new_pin` asserts the marketplace-update env is `None`.
- Research: skipped (no external library or framework in scope; the CLI behaviour was proven directly with the real claude binary).

## Open Questions

- Finding 3: honour `CLAUDE_CONFIG_DIR` (read/write plugin state under it, let subprocesses inherit it), refuse pinned plugins on mismatch, or pin each `claude` subprocess to the `home` the installer validated (strip `CLAUDE_CONFIG_DIR`, set `HOME=home`)? Which keeps the install coherent with the settings file the wanted list is read from?
- Should the catalog directory move with the profile, or stay at `home/.claude/ironclaude-marketplace` (registered by absolute path, so location does not affect correctness)?
- Finding 1: catch only `OSError`/`RuntimeError`, or wrap the whole comparison?
- Finding 2: does a missing user-scope record (project-scope only) count as "installed" (skip install) or "not installed" (install at user scope)?
