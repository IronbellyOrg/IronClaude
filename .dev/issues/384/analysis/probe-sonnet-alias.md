# Probe: ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b remaps `sonnet` (2026-11-05)

Follow-up to `probe-alias-remap.md`, which covered only the opus and haiku variables. Run by the launcher-follow-up worker of #384 in a throwaway HOME and CLAUDE_CONFIG_DIR under `/tmp` (directory removed afterwards, never this workspace's `~/.claude`), against the workspace gateway at this session's ANTHROPIC_BASE_URL, with the same Claude Code binary. Each run started with `env -u` for ANTHROPIC_MODEL and the other two ANTHROPIC_DEFAULT_*_MODEL variables, so only the SONNET variable was in play. No credentials are recorded here.

## Result: PASS

| # | Setup | `modelUsage` keys | Reading |
|---|---|---|---|
| 1 | `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b claude -p --model sonnet ...` | `claude-gw-tier1b` | `--model sonnet` runs on the tier id; Claude Code printed `[claude-code:unrecognized_model] {"model":"claude-gw-tier1b","query_source":"sdk"}` and served the request (reply "ok"). |
| 2 | Control: same command with `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-5-5` | `claude-sonnet-5-5` | The variable decides the model; the tier id in run 1 came from it. |
| 3 | `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-gw-tier1b claude -p --model claude-opus-5-5 --agents '{"probe-sonnet":{"model":"sonnet",...}}'`, one Agent call to `probe-sonnet` with no `model` parameter | `claude-gw-tier1b`, `claude-opus-5-5` | The subagent with `model: sonnet` frontmatter ran on `claude-gw-tier1b`; the opus parent kept its own model. `subagent_stats.by_type` `{"probe-sonnet":1}`, `is_error` false, notice `{"model":"claude-gw-tier1b","query_source":"agent:custom:probe-sonnet"}`. |
| 4 | Control: same as 3 with `ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-5-5` | `claude-opus-5-5`, `claude-sonnet-5-5` | Without the tier id the subagent runs on the plain sonnet model. |

## A trap found on the way

A first subagent run used `--model claude-sonnet-5-5` as the parent. Its `modelUsage` showed only `claude-sonnet-5-5`, so the `model: sonnet` subagent did NOT pick up the tier id. Claude Code keeps the parent's model for a subagent whose alias is in the parent's own model family (this is what the single key shows; the Claude Code source was not read, so the rule itself is UNVERIFIED). Consequence for the launcher: a session whose main model is a Sonnet runs its `model: sonnet` subagents on the main model, not on `claude-gw-tier1b`. The same applies to the opus and haiku variables when the main model is an Opus or a Haiku. Probes 3 and 4 used an Opus parent to avoid it.

## Not exercised

The Agent-call `model` parameter with `sonnet` (the docs say it resolves aliases the same way). The `opus` and `haiku` variables were probed in `probe-alias-remap.md`.
