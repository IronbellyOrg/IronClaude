# S-ID results: reviewer identity and read-only allowlist

Run 2026-11-12, probe window 00:10:28Z to 00:10:54Z (UTC). Runbook: `./s-id-runbook.md`. Three probes were dispatched in one message through `subagent_type: reflect-reviewer`, with the Agent tool `model` set to the pin. All three were dispatched and answered.

## Probe table

| Pin (Agent `model`) | Self-report (`reviewer_model_self_report`) | Write attempt | `probe_tools` (exact names) | Write, Edit or Bash in the list? | Model id exposed |
|---|---|---|---|---|---|
| haiku | "Underlying model name/id unknown; supplied context labels it `claude-gw-tier2[1m]`" | none attempted: "no write tool available" | `functions.Read`, `functions.Grep`, `functions.Glob`, `functions.mcp__codegraph__codegraph_search`, `functions.mcp__codegraph__codegraph_node`, `functions.mcp__codegraph__codegraph_callers`, `functions.mcp__codegraph__codegraph_impact`, `multi_tool_use.parallel` | No | Transcript: **`gpt-6.1-sol`** (both assistant turns; `retries/T14/probe-models.txt`). Self-reported alias: `claude-gw-tier2[1m]` |
| sonnet | "`claude-gw-tier1b[1m]` (the model id given in my system prompt; I can't confirm the underlying model beyond that)" | none attempted: "no write tool available" | `mcp__razor_culture__pool_Read`, `mcp__razor_culture__mean_Grep`, `mcp__razor_culture__anchor_Glob`, `mcp__codegraph__codegraph_search`, `mcp__codegraph__codegraph_node`, `mcp__codegraph__codegraph_callers`, `mcp__codegraph__codegraph_impact` | No | Transcript: **`claude-sonnet-5-5`** (both assistant turns). Self-reported alias: `claude-gw-tier1b[1m]` |
| opus | "`claude-gw-tier1a[1m]`. My environment block names this model. I cannot independently confirm which model class sits behind that gateway alias." | none attempted: "no write tool available" | `mcp__razor_culture__pool_Read`, `mcp__razor_culture__mean_Grep`, `mcp__razor_culture__anchor_Glob`, `mcp__codegraph__codegraph_search`, `mcp__codegraph__codegraph_node`, `mcp__codegraph__codegraph_callers`, `mcp__codegraph__codegraph_impact` | No | Transcript: **`claude-opus-5-5`** (both assistant turns). Self-reported alias: `claude-gw-tier1a[1m]` |

Because no probe had a write tool, the write was never attempted, so no refusal text exists. The evidence for the allowlist is the tool list, as the runbook says.

## Working tree check (AC3)

`git status --porcelain` was taken immediately before the first dispatch and immediately after the last answer, with this task's own `artifacts/retries/T14/` files filtered out. The full outputs are saved:

- before: `./retries/T14/status-before.txt` (173 lines, sha256 starts `f513094cab8cc9cd`)
- after: `./retries/T14/status-after.txt` (173 lines, sha256 starts `f513094cab8cc9cd`)
- `diff` of the two: empty (identical).

`.dev/s-id-probe-haiku.txt`, `.dev/s-id-probe-sonnet.txt` and `.dev/s-id-probe-opus.txt` do not exist. The runbook (`./s-id-runbook.md`) was written before the before-snapshot, so it appears in both; this results file was written after the after-snapshot.

## Findings against the four questions

1. Does the self-report match the pin in 3 of 3? By model name: 0 of 3. No probe said haiku, sonnet or opus; each gave a gateway alias, and each said it could not confirm the model behind it. The self-reports are therefore not usable as identity. The transcript model ids (question 2) settle what ran: the sonnet pin ran `claude-sonnet-5-5` and the opus pin ran `claude-opus-5-5` (pin honoured, 2 of 3), but the haiku pin ran **`gpt-6.1-sol`**, a non-Anthropic model (pin not honoured). The haiku request resolved to the gateway tier2 alias, and tier2 lists no Anthropic model (`review-tiers.default.json`: `gpt-6.1-sol` first); the anthropic-only stand-in (Haiku for tier2) did not apply on this gateway. So the earlier reading "3 of 3 consistent with the alias table" was wrong for haiku and is withdrawn.
2. Does the tool result or transcript expose a model id? **Yes, in the transcript.** Each probe's sidechain transcript (`~/.claude/projects/.../subagents/agent-<id>.jsonl`) records `message.model` on its assistant turns: `gpt-6.1-sol` (haiku probe), `claude-sonnet-5-5` (sonnet probe), `claude-opus-5-5` (opus probe). The values are saved in `./retries/T14/probe-models.txt` with the `jq` command that produced them. The Agent tool result text returned to the caller carries only the probe's own words, with no model id; the id is in the transcript, not in the result.
3. Does the read-only allowlist survive the `model` override? Yes for all three pins: no probe had Write, Edit or Bash, and none had a write tool. Caveat: the tool names are not the agent file's names (`Read`, `Grep`, `Glob`, `mcp__codegraph__...`); two probes saw `mcp__razor_culture__...` names and the haiku probe saw `functions.`-prefixed names, so the harness renames tools. The set is still read-only.
4. Decision for `identity_source`: see below.

## Decision and Stage 1 exit facts

**identity_source: `observed`.** A model id is exposed: the probe transcripts record the model that answered. The rule of the task is `observed` if a model id is exposed. Two limits to carry forward: (1) the id is read from the sidechain transcript on disk, not from the Agent tool result, so the adapter can only use it where it can read that transcript; (2) the observation shows the `haiku` pin did not give a Claude model on this gateway, so Stage 1 must not assume that a pin yields the class it names.

- Allowlist survives the `model` override: **yes** (3 of 3 probes, no Write, Edit or Bash).
- Self-report match count: **0 of 3 by model name**; by observed transcript model, **2 of 3 pins honoured** (sonnet, opus; haiku ran `gpt-6.1-sol`).
- Model-id exposure in a transcript: **yes** (not in the Agent tool result text).
