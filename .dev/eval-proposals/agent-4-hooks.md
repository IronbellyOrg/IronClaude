# Agent 4 — Hooks Eval Proposals

## Proposal 1 (one-off): `freshness_blocks_existing_unread_edit`

- **Target:** `freshness-pre-edit.sh`
- **Hypothesis:** Existing-file Write/Edit with no prior Read exits 2 and blocks; new-file create allows.
- **Cadence:** one-off.
- **Inputs:** ask Claude to Edit an existing seeded file without reading it; then ask Claude to create a new file.
- **Assertions:** denied edit stderr contains `FRESHNESS BLOCK`; telemetry has `decision:"block","reason":"no_prior_read"`; create allowed.
- **Requires:** `jq`, Claude PTY.
- **Complexity:** simple.
- **Value:** Catches stale-edit safety regressions.
- **Evidence:** `src/superclaude/hooks/scripts/freshness-pre-edit.sh:76-87`, `:122-140`.

## Proposal 2 (one-off): `auggie_first_sticky_until_matching_tool`

- **Target:** `freshness-session-start.sh`, `freshness-user-prompt.sh`, `auggie-flag-clear.sh`
- **Hypothesis:** Resume creates sticky when Auggie registered; UserPromptSubmit repeats `auggie_first_required=1`; matching Auggie PostToolUse clears it.
- **Cadence:** one-off.
- **Inputs:** seed `.claude.json`; spawn session; submit prompt; invoke Auggie MCP tool.
- **Assertions:** sticky file exists post-SessionStart; auggie_first_required=1 emitted on UserPromptSubmit; sticky cleared after matching tool call.
- **Requires:** seeded `.claude.json`, `jq`, fake/available Auggie MCP.
- **Complexity:** medium.
- **Value:** Catches sticky-state and matcher regressions.
- **Evidence:** `src/superclaude/hooks/scripts/freshness-session-start.sh:100-109`, `src/superclaude/hooks/scripts/freshness-user-prompt.sh:143-178`, `src/superclaude/hooks/scripts/auggie-flag-clear.sh:22-30`.

## Proposal 3 (recurring): `hook_latency_and_telemetry_schema_drift`

- **Target:** all wired hooks in `src/superclaude/hooks/hooks.json:35-68` + project hooks `.claude/settings.json:3-28`.
- **Hypothesis:** Timeout budgets respected, JSON schemas valid, fail-open behavior preserved.
- **Cadence:** recurring — continuous/nightly. Detect drift in hook latency p95 or telemetry schema (silent contract changes).
- **Inputs:** scripted hook payload matrix.
- **Assertions:** p95 latency below configured timeout; JSONL rows parse; no exit 1.
- **Requires:** `bash`, `jq`, `flock`.
- **Complexity:** medium.
- **Value:** Catches performance and telemetry-contract drift.
