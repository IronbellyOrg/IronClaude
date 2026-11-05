# Probe: Claude Code resolves aliases through ANTHROPIC_DEFAULT_*_MODEL, including tier ids (2026-11-05)

Run by the #384 worker in a throwaway HOME and CLAUDE_CONFIG_DIR under /tmp (removed afterwards), against the workspace gateway at the ANTHROPIC_BASE_URL of this session. Claude Code 2.x binary at the path in CLAUDE_CODE_EXECPATH. No credentials are recorded here.

## Probe 1: the main-session alias

Command shape: `ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a claude -p --model opus --output-format json --max-turns 1 "Reply with the single word ok"`

Observed: the request was served and the reply was "ok"; the JSON `modelUsage` had the single key `claude-gw-tier1a`; Claude Code printed `[claude-code:unrecognized_model] {"model":"claude-gw-tier1a","query_source":"sdk"}` and went on.

## Probe 2: subagent frontmatter aliases

Command shape: `ANTHROPIC_DEFAULT_OPUS_MODEL=claude-gw-tier1a ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-gw-tier2 claude -p --model claude-sonnet-5-5 --agents '{"probe-opus":{... "model":"opus"},"probe-haiku":{... "model":"haiku"}}' "Use the Agent tool once with subagent_type probe-opus and once with subagent_type probe-haiku (no model parameter), then reply done."`

Observed (jq of the result): `modelUsage` keys `claude-gw-tier1a`, `claude-gw-tier2`, `claude-sonnet-5-5`; `subagent_stats.by_type` `{"probe-opus":1,"probe-haiku":1}`; `is_error` false; notices `[claude-code:unrecognized_model] {"model":"claude-gw-tier1a","query_source":"agent:custom:probe-opus"}` and `{"model":"claude-gw-tier2","query_source":"agent:custom:probe-haiku"}`.

## Reading

- A tier id is accepted as the value of ANTHROPIC_DEFAULT_OPUS_MODEL and ANTHROPIC_DEFAULT_HAIKU_MODEL; the plain alias in a subagent's `model:` frontmatter resolved through it; the main session kept its own model.
- Claude Code logs an `unrecognized_model` notice for each tier id but serves the request.
- The Agent-call `model` parameter was not exercised here (the docs say it takes aliases and resolves them the same way); only frontmatter and `--model` were observed.
