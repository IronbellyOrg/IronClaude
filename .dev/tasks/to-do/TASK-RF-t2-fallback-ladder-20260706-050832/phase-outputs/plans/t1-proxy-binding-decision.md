# T1 Proxy Binding Decision (Phase 5 Step 5.1 — needs_human_decision gate)

**Date:** 2026-07-07
**Verdict:** CONFIRMED — real T1-proxy fallback dispatch AUTHORIZED and enabled.

## Gate conditions (both met)

1. **Env-var NAMES confirmed present** (read-only, NAMES only — no values read/printed, no `:4000/v1` or proxy-API probe):
   `grep -oE '^(export )?(T1ProxyUrl|T1ProxyKey|T1Model01|T1Model02)' ~/.aienv | sed 's/^export //' | sort -u`
   → `T1Model01`, `T1Model02`, `T1ProxyKey`, `T1ProxyUrl` all present. `~/.aienv` exists.
2. **Operator sign-off (mechanism, for auditability):** the executor did NOT rely on the build-time pre-authorized Open Questions entry alone. At the actual gate this session, the executor PAUSED and presented the decision to the operator via the harness structured decision prompt (the `AskUserQuestion` tool: "Do you authorize enabling REAL T1-proxy fallback dispatch now, or defer it?", with a recommended "Defer" default). The operator explicitly selected **"Enable real dispatch now"** on 2026-07-07. This is a fresh, interactive human decision that honors the `needs_human_decision` HALT (`feedback_human_decision_items_must_halt`) — the executor did NOT auto-apply a default. A reviewer can verify this against the session transcript (the `AskUserQuestion` tool call + the recorded selection). The build-time entry dated 2026-07-06 is a task-authoring pre-authorization; the load-bearing authorization is this session's interactive selection (2026-07-07), and the read-only NAME-presence check was an independent defense-in-depth confirmation, never a substitute for the human decision.

## Resolved binding (supersedes the design §7.3 T2-reuse default)

Per `research/06-config-threading-gap-fill.md` (T1-proxy reconciliation) — the dedicated T1 proxy contract, NOT the T2-reuse default:

```python
_T1_PROXY_BINDING = {
    "model_prefix": "T1Model0",
    "proxy_url_env": "T1ProxyUrl",
    "proxy_key_env": "T1ProxyKey",
    "max_slots": T1_MODEL_MAX_SLOTS,  # imported from superclaude.cli.swarm.config
}
```

Only env-var NAME strings are written into source — never a proxy key/url VALUE.

## Effect

`resolve_t1_fallback_factory("openai_compat", ...)` now resolves the REAL T1 fallback transport via `read_env_for_pool` with the confirmed `T1ProxyUrl`/`T1ProxyKey`/`T1Model0N` names, binding each ladder slot NAME to a distinct pool model by ladder position (F1) via `make_fallback_slot_factory`. On a live `openai_compat --depth deep` reflect run, a single transient primary Tier-2 reviewer failure is now topped up by a real T1 reviewer instead of collapsing to Tier-1/exit-11.

The env read is deferred lazily into the returned factory, so an incomplete/absent T1 env at dispatch time still degrades to `terminal_reason: fallback_config_missing` (caught in the controller) rather than crashing the run.
