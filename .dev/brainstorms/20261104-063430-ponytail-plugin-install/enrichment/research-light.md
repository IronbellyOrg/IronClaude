# Research (light): the Ponytail plugin

quality_tier: fallback_1 (sc-research-protocol not invoked; read the upstream source directly with `gh api repos/DietrichGebert/ponytail/...`, 2026-11-04)

| Fact | Source |
|---|---|
| Marketplace name `ponytail`, one plugin `ponytail`, source `./`, category productivity. Install id `ponytail@ponytail`, marketplace repo `DietrichGebert/ponytail`. | `.claude-plugin/marketplace.json` |
| Version 5.3.3, MIT, default branch `main`, last push 2026-10-29, releases v5.3.1-v5.3.3 in Oct 2026. | `.claude-plugin/plugin.json`; repo metadata |
| Hooks: SessionStart (`startup\|resume\|clear\|compact`), SubagentStart, UserPromptSubmit; each runs `node -e` on a script under `CLAUDE_PLUGIN_ROOT`, timeout 15 s. Requires `node` on PATH. | `hooks/claude-codex-hooks.json` |
| Band module `./band/register.tsx` (Claude Code band above the prompt). | `hooks/claude-band.json` |
| `userConfig.ledger` default true: per-turn row in `~/.config/ponytail/band/<project>.csv`. Webhook empty by default. | `plugin.json` |
| Default mode order: `PONYTAIL_DEFAULT_MODE` env, `~/.config/ponytail/config.json` `defaultMode`, else `full`. Valid runtime modes `off, lite, full, ultra`. | `hooks/ponytail-config.js` |
| Mode `off`: SessionStart clears the flag and exits; no rules, no map, no statusline nudge. Other modes emit the ruleset, a codebase map (3 s cap, `PONYTAIL_MAP=0` disables) and a one-time statusline nudge when `settings.statusLine` is unset. | `hooks/ponytail-activate.js` |
| Skills: ponytail, ponytail-review, ponytail-audit, ponytail-debt, ponytail-help, ponytail-gain. `/ponytail [lite\|full\|ultra\|off]` switches level in-session. | `skills/` listing; README "Commands" |
| README: "An optional `~/.config/ponytail/config.json` or `PONYTAIL_DEFAULT_MODE` env var can set the default level, but nothing is required." | `README.md:194` |
