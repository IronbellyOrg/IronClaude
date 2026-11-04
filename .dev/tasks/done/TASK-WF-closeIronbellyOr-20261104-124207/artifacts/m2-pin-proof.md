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
