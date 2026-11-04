# Evidence for shared assumptions A-004 and A-005 (and A-002 context)

Collected by the orchestrator on 2026-11-04, before debate Round 1.

## A-005: skills are available whatever Ponytail's mode is

- `gh api .../skills/ponytail-review/SKILL.md` and `.../skills/ponytail-audit/SKILL.md`: a grep for `mode|off|.ponytail-active|PONYTAIL_DEFAULT` returns no lines. The skills do not read the mode.
- `skills/ponytail/SKILL.md:9,17`: the `ponytail` skill is the mode switch itself (`argument-hint: "[lite|full|ultra|off]"`; "Switch level: `/ponytail lite|full|ultra`").
- Skills are files under the plugin directory; the mode is read only by the hook scripts (`hooks/ponytail-config.js`). Conclusion: supported; skills ship in `off`.

## A-004: install-time `userConfig` prompts

- Claude Code plugins reference (Context7 `/pjbrito/claude-code-docs`, `plugins-reference.md`, "User configuration"): "The `userConfig` field declares values that Claude Code prompts the user for when the plugin is enabled." Each field may have a `default` ("Value used when the user provides nothing") and `required`.
- Ponytail `plugin.json` `userConfig`: `ledger` (boolean, default true), `webhookUrl` (string, default ""), `webhookToken` (string, sensitive, no default, not required), `sendNames` (boolean, default true). No field is `required`.
- Not documented: whether `claude plugin install ... -y` with stdin closed prompts, and whether an interactive session shows a configuration dialog on first start after a CLI install. UNVERIFIED. No field is required, so a missing value cannot fail validation.

## A-002 context: enabled but not yet installed

- Claude Code env-vars docs (`env-vars.md`, `CLAUDE_CODE_SYNC_PLUGIN_INSTALL`): "Without this, plugins install in the background and may not be available on the first turn." Claude Code itself installs plugins in the background in sessions, which suggests an enabled-but-not-installed plugin from a known marketplace is installed by Claude Code later rather than erroring. Exact trigger conditions UNVERIFIED.
- Settings docs (`settings.md`, `enabledPlugins`): project settings take precedence over user settings; a project `.claude/settings.json` enabling a plugin overrides a user `false`. Relevant to the opt-out wording.
