# Ponytail pin proof (PR #358, Codex P1 finding on the unpinned marketplace)

Run: 2026-11-04, Claude Code 2.1.318, worktree venv. Every step ran with `HOME=<throwaway under /tmp>` and without `CLAUDE_CONFIG_DIR`, `XDG_CONFIG_HOME`, `PONYTAIL_DEFAULT_MODE` or the parent session's messaging variables. Throwaway directories were removed afterwards; the real `~/.claude` files hashed the same before and after (`settings.json` 5711b646dfb93d13, `installed_plugins.json` 55a39037ff3fcc56, `known_marketplaces.json` f32c1debd3188553) and `~/.claude/ironclaude-marketplace` does not exist there.

## Upstream at the pin

- `git ls-remote --tags https://github.com/DietrichGebert/ponytail.git`: `7801d061243d7b753bad0e0b3c057cd250b11755 refs/tags/v5.3.3`, `16352ac229eb08a9598dcae48fe9f2b342567d86 refs/tags/v5.3.2`.
- At 7801d061 the repository root is the plugin: `.claude-plugin/plugin.json` has `"name": "ponytail"`, `"version": "5.3.3"`, hooks `./hooks/claude-codex-hooks.json` and `./hooks/claude-band.json`; upstream's own `marketplace.json` lists it with `"source": "./"`. `claude plugin validate <checkout>` prints `✔ Validation passed`, so the plugin works fetched straight from the repo with no `./` marketplace indirection.

## Settings-source marketplace (first proposal): cannot be installed by the installer

- Fresh HOME whose `settings.json` declares `extraKnownMarketplaces.ironclaude` with `"source": "settings"` and the sha-pinned plugin entry:
  - `claude plugin install ponytail@ironclaude --scope user -y` exit 1: `Plugin "ponytail" not found in marketplace "ironclaude". Your local copy may be out of date — try \`claude plugin marketplace update ironclaude\`.`
  - `claude plugin marketplace update ironclaude` exit 1: `Marketplace 'ironclaude' not found. Available marketplaces: anthropic-plugin-directory`.
  - `plugin list`, `plugin list --available --json`, `plugin details`, `plugin marketplace update` (all), `doctor`, `mcp list`, `auth status`: none registers it.
- Only a session start (`claude -p ...`) registers it; the session does not install the plugin. Once registered, the install pins correctly (`gitCommitSha` 7801d061).
- Coordinator decision: option A, an IronClaude-owned directory marketplace with the same pin.

## Shipped design: directory marketplace written from the defaults

| Check | Result |
|---|---|
| Fresh HOME, `apply_settings_defaults` then `install_plugins` (30 s budget) | PASS: `✅ Plugins: installed ... ponytail@ironclaude` in 16.8 s; `installed_plugins.json` `ponytail@ironclaude` = version 5.3.3, gitCommitSha 7801d061243d7b753bad0e0b3c057cd250b11755 |
| Claude Code declares the marketplace itself | PASS: `extraKnownMarketplaces.ironclaude = {"source": {"source": "directory", "path": "<home>/.claude/ironclaude-marketplace"}}`; `ironclaudeMarketplace` key not copied into `settings.json` |
| Second run | PASS: `✅ Plugins: already installed`, 0.0 s |
| Written catalog validates | PASS: `claude plugin validate ~/.claude/ironclaude-marketplace` prints `✔ Validation passed` |
| Pin change: first run with the catalog patched to v5.3.2 (16352ac2) | installed 5.3.2 / 16352ac229eb08a9598dcae48fe9f2b342567d86 |
| Pin change: rerun with the shipped catalog | PASS: catalog rewritten to 7801d061, `marketplace update ironclaude` then `plugin update ponytail@ironclaude --scope user`; installed 5.3.3 / 7801d061243d7b753bad0e0b3c057cd250b11755 in 2.1 s |
| Pin change: third run | PASS: `✅ Plugins: already installed` |

Note on `claude plugin update`: without the HTTPS rewrite it failed in the throwaway HOME with `git@github.com: Permission denied (publickey)` (it clones over SSH, while `plugin install` printed `SSH not configured, cloning via HTTPS`). `install_plugins` therefore runs only the update command with `GIT_CONFIG_COUNT=1`, `GIT_CONFIG_KEY_0=url.https://github.com/.insteadOf`, `GIT_CONFIG_VALUE_0=git@github.com:`; with that, the update succeeded and kept the plugin's `pluginConfigs` options (checked with `ledger=false`).

## Migration from master's unpinned `ponytail@ponytail` (PR #358 merged as 9b9497e6 before the pin landed)

Same throwaway-HOME conditions, removed afterwards.

| Step | Ponytail entries afterwards |
|---|---|
| 1. Master's way: `claude plugin marketplace add DietrichGebert/ponytail`, `claude plugin install ponytail@ponytail --scope user -y` | enabled `ponytail@ponytail`; marketplace `ponytail` = `{"source":"github","repo":"DietrichGebert/ponytail"}` (the same shape master's defaults write); installed at gitCommitSha 96608e07, upstream HEAD, not v5.3.3 |
| 2. New installer (`apply_settings_defaults` + `install_plugins`) | both enabled: `ponytail@ponytail` (96608e07) and `ponytail@ironclaude` (7801d061); `ponytail@ponytail` left untouched |
| 3. `claude plugin marketplace remove ponytail` | only `ponytail@ironclaude` (7801d061) remains; the `ponytail@ponytail` enabledPlugins key and the `ponytail` marketplace are gone; Claude Code says it also deletes the removed plugins' saved options and data |
| 4. New installer again | `✅ Settings defaults: already present`, `✅ Plugins: already installed`; `ponytail@ponytail` not added back |

Why the installer does not remove `ponytail@ponytail` itself: step 1 shows that `claude plugin marketplace add` writes the same `extraKnownMarketplaces.ponytail` value master's defaults wrote, and master kept no record of what it added, so the installer cannot prove it added the entry. The docs and CHANGELOG give the step 3 command instead.

## Foreign `ironclaude` registrations and failed marketplace commands (Codex security finding on PR #360)

Same throwaway-HOME conditions, real Claude Code 2.1.318, removed afterwards.

- `claude plugin marketplace add <home>/.claude/ironclaude-marketplace` when the name `ironclaude` is already registered from another directory: exit 0, prints "Marketplace 'ironclaude' was already added from dir:<foreign> and now points at dir:<home>/.claude/ironclaude-marketplace. Plugins already installed from it now update from the new source." The registry entry is rebound to our directory.
- `install_plugins` after the fix, fresh HOME with only `ponytail@ironclaude` enabled: `✅ Plugins: installed ponytail@ironclaude`; installed 5.3.3 at gitCommitSha 7801d061243d7b753bad0e0b3c057cd250b11755; registry entry `{"source": "directory", "path": "<home>/.claude/ironclaude-marketplace"}`.
- `install_plugins` after the fix, HOME where a foreign directory marketplace already holds the name `ironclaude`: `⚠️  Plugins: not installed: ironclaude (registered from another source, so its plugins were not installed or updated; run claude plugin marketplace add <home>/.claude/ironclaude-marketplace to use IronClaude's pinned catalog)`; nothing installed; the foreign registration is unchanged.
