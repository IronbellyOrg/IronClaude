## Bug Summary

The ccsession proxy does not recover when a tier's first model rejects the default `output_config.effort: "medium"`: the request fails with HTTP 400 instead of retrying compatibly or reaching the next model. In the reported deployment, tier 3 starts with GLM-5.3, so every default-effort caller of that tier is exposed.

## Environment (OS, version)

- OS: Linux; OS version not known yet.
- Version: Claude Code 2.1.322; reported affected branch: `master`. SuperClaude package version not known yet.
- Proxy: `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py`, installed as `~/.claude/skills/ccsession-tag/local-gateway-alias-proxy.py`; reported listener: `http://127.0.0.1:4114`.
- Reported live tier configuration: `T3Model01=glm-5.3` in `/etc/aidev02/aienv.d/defaults.sh`; `T3Model02` is Qwen3.8 Max. `origin/master` documents the same order (`MODEL-TIERS.md:43`: GLM-5.3 first, then Qwen3.8 Max).
- Reported settings: `alwaysThinkingEnabled: true`, `effortLevel: high`, and per-model `modelSettings` in `~/.claude/settings.json`. The observed subagent default of `medium` is Claude Code's, not the user's main-session setting.

## Current Behavior

The supplied live evidence from 2026-11-12 captures `claude -p` spawning a subagent with `model: claude-gw-tier3` and no effort field. Claude Code sends `thinking: adaptive` and `output_config.effort: medium`, which receives HTTP 400. Explicit subagent `effort: low` and `effort: high` receive HTTP 200; a real agent-file control using low and then medium produces 200 and 400 respectively.

Direct requests through the real proxy, streaming and non-streaming, with and without tools and the `interleaved-thinking` / `effort` beta headers, also fail for medium. Low, high, and no `output_config` return 200. The description reports GLM-5.3 accepts low, high, max, or omitted effort.

No `SWITCH_RULES` entry matches this error. The proxy returns it unchanged without trying Qwen3.8 Max, and audits it as `kind=request` (`local-gateway-alias-proxy.py:941` on `origin/master`; the log line is quoted below).

## Expected Behavior

A tier should survive a first model that rejects medium effort. A request to `claude-gw-tier3` with `thinking: adaptive` and `output_config.effort: medium` should return 200, either through a compatible effort rewrite or the next model, while unrelated request errors and existing usage/server-error cooldown behavior remain unchanged.

## Steps to Reproduce

1. Use the reported environment with the real proxy listening on `127.0.0.1:4114`, tier 3 beginning with GLM-5.3, and Qwen3.8 Max available next. Supply the gateway credentials normally used for this proxy.
2. POST this body to `http://127.0.0.1:4114/v1/messages` with `Content-Type: application/json` and the configured authentication header:

   ```json
   {
     "model": "claude-gw-tier3",
     "max_tokens": 1024,
     "stream": false,
     "messages": [{"role": "user", "content": "Reply with OK."}],
     "thinking": {"type": "adaptive"},
     "output_config": {"effort": "medium"}
   }
   ```

3. Observe HTTP 400 with the exact error below, rather than a successful reply from the tier's next model. Repeat with effort `low` and `high`: the supplied evidence reports HTTP 200. Omitting `output_config` also succeeds.
4. Alternatively, run `claude -p` with a prompt that spawns a subagent whose definition has `model: claude-gw-tier3` and no effort field. Capture its request: the supplied evidence shows adaptive thinking plus medium effort and HTTP 400. Explicit low/high effort provides the contrast.

## Impact Assessment (Severity, Blast Radius)

- Severity: medium — one effort-incompatible first model makes the tier fail consistently for default-effort requests despite an available fallback.
- Blast Radius: every default-effort caller of tier 3 in the reported deployment, including other subagents and sessions or aliases reaching it. Other tiers with a similarly incompatible first model are also exposed. Members start on tier 2 and may choose tiers 2–4, so they are included. PR #516 only works around the problem for `issue-worker-t3`.

## Error Messages

Exact response text supplied in the description:

```text
HTTP 400 invalid_request_error: This model always engages in thinking and cannot be disabled; please use low, high, or max
```

Exact supplied proxy log line (reported seven occurrences in `~/.cache/ccsession/proxy.log` on 2026-11-11 and 2026-11-12):

```text
TIER tier3: glm-5.3 status=400 kind=request count=0; error=This model always engages in thinking and cannot be disabled; please use low, high, or max
```

## Codebase Context (from `/sc:analyze`)

Standard-depth static pass, re-checked against `origin/master` (the first draft read an out-of-date local checkout; every line number below is from `origin/master`, 1,040 lines). Codegraph and Auggie were unavailable to the worker; Grep, Glob and Read were used. No source change, live reproduction or test run.

- `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:819` `_forward_tier` walks the tier's models in order; line 839 sets `obj["model"]` to the current model and the request is forwarded as is: effort and thinking are never rewritten.
- `local-gateway-alias-proxy.py:396` `SWITCH_RULES` (and `switch_reason`, line 421) has no entry for this error, so `reason` stays empty (line 899).
- `local-gateway-alias-proxy.py:928` the server-error branch only covers 408, 429, 500, 502, 503, 504. A 400 skips it.
- `local-gateway-alias-proxy.py:940-942` audits the error as `kind=request`, then line 951 returns it to the client unchanged (`# not a switch error`). This is the exact line behind the reported log entry.
- `local-gateway-alias-proxy.py:945-950` the one 400-class exception: a backup (position above 0) that rejects the request as too large moves to the next backup. The acceptance text must keep that behaviour.
- Cooldown helpers: `cool_down` (467), `model_failed` (474), `cooling_until` (503), `FAILS_BEFORE_SWITCH` (124). A new switch rule that reuses `reason` would enter the cooldown path (lines 909-927), so the "no long cooldown" wish in candidate fix 2 needs explicit handling.
- `src/superclaude/skills/ccsession-tag/ccsession-models.json` defines tier 3 as `models_env: [T3Model01, T3Model02]`; `models.py:666` resolves the slots in order. `MODEL-TIERS.md:43` documents GLM-5.3 first, then Qwen3.8 Max.
- Tests (`tests/unit/test_ccsession_tiers.py` on `origin/master`): the `shim` fixture (843) runs the real proxy against a scripted stand-in gateway; `test_every_switch_rule_moves_to_the_next_model` (1026) covers the switch rules; `test_errors_outside_the_rules_pass_back_unchanged` (1044) pins that an unmatched 400 passes back unchanged (it uses `context_management is not supported`, not this thinking/effort error); `test_backup_rejecting_size_tries_the_next_one` (1071) covers the size exception; `test_out_of_usage_switches_and_cools_down` (960) covers cooldown. None covers the thinking/medium rejection. Note `test_errors_outside_the_rules_pass_back_unchanged` is the test a fix must be careful not to break.

## Related Issues

- None found in the scout's duplicate search.
- Related workaround: [PR #516](https://github.com/IronbellyOrg/IronClaude/pull/516) adds `effort: low` for `issue-worker-t3`, according to the supplied description. That one-agent workaround is not the shared proxy fix requested here.

## Testing Notes

Acceptance from the description:

- A request with `thinking: adaptive` and `effort: medium` to `claude-gw-tier3` returns 200 (via the rewrite or via the next model).
- A test in `tests/unit/test_ccsession_tiers.py` (or a new test next to it) fails without the fix.
- Other 400s (a real malformed request, a too-large prompt) still pass through unchanged.
- No change to the cooldown rules for usage and server errors.
- **This 400 must never park a model.** The model works at `low`, `high` and no effort, so no entry may be added to the cooldown map (`_cooldowns`) for it. A test must show that after one such 400 the same model still serves a following `effort: high` request. See the comment on this issue for the measured reason (a default 1-hour park, keyed by model across all tiers).

Candidate fixes, to be decided in the design step:

1. In the proxy, on a `400` whose body contains `always engages in thinking`, retry the same model once with `output_config.effort` rewritten to `low` (or the nearest accepted value from the message), and remember per model that it needs the rewrite so later requests do it up front. Keep the one-extra-round-trip cost in mind.
2. Or move this one request to the tier's next model without parking the failing model. A plain `SWITCH_RULES` entry is not enough: a matching rule goes through `cool_down` and parks the model for `COOLDOWN_SECONDS` (default 3,600 s) when the reply has no `Retry-After` header, so the rule needs a no-cooldown path.
3. Or fix it at the gateway (`192.168.133.101:4000`): map `medium` for GLM-5.3. The description states the Coder repo holds no LiteLLM config, so that is outside this repository.

Preserve the existing backup-too-large behavior while checking unchanged pass-through for unrelated first-model request errors. The existing backup-size test (`test_backup_rejecting_size_tries_the_next_one`, `tests/unit/test_ccsession_tiers.py:1071`) intentionally advances to another backup; the acceptance text should not be read as removing that behavior.

Out of scope: the tier 3 model list itself, `issue-worker-t3` (handled in #516), and Claude Code's subagent effort default.

<!-- sc:issue:create template=issue-bug-simple -->
