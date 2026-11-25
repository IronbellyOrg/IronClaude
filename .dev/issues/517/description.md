# Description given to /sc:issue --create

ccsession proxy: a tier whose first model always thinks fails every request that carries the default `effort: medium`, and the proxy never falls through to the tier's second model

## What happens

Any request routed to `claude-gw-tier3` with `output_config.effort: "medium"` returns `HTTP 400 invalid_request_error: This model always engages in thinking and cannot be disabled; please use low, high, or max`. Claude Code sends `medium` by default for subagents (a main session gets the effort from `settings.json`, here `high`). The first model of tier 3 is GLM-5.3 (`T3Model01=glm-5.3` in `/etc/aidev02/aienv.d/defaults.sh`); its gateway rejects `medium` and accepts `low`, `high`, `max` and no effort at all.

The local ccsession proxy (`src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py`, installed as `~/.claude/skills/ccsession-tag/local-gateway-alias-proxy.py`) classifies this 400 as `kind=request` (`_forward_tier`, the `TIER ... kind=request` audit line) and returns it to the client. `SWITCH_RULES` has no entry for it, so the proxy never tries `T3Model02` (Qwen3.8 Max), which would have answered. One bad first model therefore takes down the whole tier for every default-effort caller.

## Evidence (2026-11-12, all through the real proxy on 127.0.0.1:4114)

Request capture with a logging reverse proxy in front of the shim, `claude -p` spawning a subagent with `model: claude-gw-tier3`:

| Subagent definition | Request sent to `claude-gw-tier3` | Result |
|---|---|---|
| no `effort` field | `thinking: adaptive`, `output_config.effort: medium` | HTTP 400 |
| `effort: low` | `thinking: adaptive`, `output_config.effort: low` | HTTP 200 |
| `effort: high` | `thinking: adaptive`, `output_config.effort: high` | HTTP 200 |
| a real agent file with `effort: low`, then `effort: medium` (control) | low / medium | 200 / 400 |

Direct requests (non-streaming and streaming, with and without tools and the `interleaved-thinking` / `effort` beta headers) to `claude-gw-tier3`: effort `medium` is always 400; `low`, `high` and no `output_config` are always 200. Proxy log lines: `TIER tier3: glm-5.3 status=400 kind=request count=0; error=This model always engages in thinking and cannot be disabled; please use low, high, or max` (seven in `~/.cache/ccsession/proxy.log` on 2026-11-11 and 2026-11-12).

Settings in play: `~/.claude/settings.json` has `alwaysThinkingEnabled: true`, `effortLevel: high`, and per-model `modelSettings`; the subagent default of `medium` is Claude Code's, not the user's.

## Already done (not part of this issue)

PR #516 gives `issue-worker-t3` an `effort: low` line, which removes the failure for that one agent. Every other subagent, and any session or alias that reaches tier 3 (or any other tier whose first model behaves the same way) with the default `medium` effort, is still exposed. Members start on tier 2 and may choose tiers 2-4, so this reaches them too.

## What the issue asks for

Make a tier survive a first model that rejects `medium` effort. Candidate fixes, to be decided in the design step:

1. In the proxy, on a `400` whose body contains `always engages in thinking`, retry the same model once with `output_config.effort` rewritten to `low` (or the nearest accepted value from the message), and remember per model that it needs the rewrite so later requests do it up front. Keep the one-extra-round-trip cost in mind.
2. Or add a `SWITCH_RULES` entry so this 400 moves the request to the tier's next model (with no long cooldown, since the model works for other efforts).
3. Or fix it at the gateway (`192.168.133.101:4000`): map `medium` for GLM-5.3. The Coder repo holds no LiteLLM config, so that is outside this repository.

Acceptance: a request with `thinking: adaptive` and `effort: medium` to `claude-gw-tier3` returns 200 (via the rewrite or via the next model); a test in `tests/unit/test_ccsession_tiers.py` (or a new test next to it) fails without the fix; other 400s (a real malformed request, a too-large prompt) still pass through unchanged; no change to the cooldown rules for usage and server errors.

## Out of scope

The tier 3 model list itself, `issue-worker-t3` (done in #516), Claude Code's subagent effort default.
