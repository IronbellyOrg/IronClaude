This issue is the spec for ccsession tier failover. The owner confirmed the retry, single-model fallback and logging plan on 2026-11-09. Stream buffering and inspection before forwarding are excluded: successful HTTP replies stream through immediately, including pings and error events, with no new time limit once a reply starts.

## How a request reaches a model today

- The gateway always receives one specific model and serves exactly that model. It never switches models itself.
- ccsession's local proxy (the shim, `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py`) sits between Claude Code and the gateway. One shim process serves every session on the machine.
- A session started on a tier sends its requests with the tier's name (for example `claude --model claude-gw-tier1a`). The shim picks the tier's first model that is not cooling down (Tier 1a: Claude Opus 5.5) and sends that model to the gateway (`_forward_tier`). Helper agents with no model setting inherit the session's tier and go the same way.
- A request that names one model goes to the gateway unchanged (`_proxy`), with no failover. This happens when a session is started on one model (`ccsession notes --model gpt-6-astra`, README: "one model, no failover"), when a model is picked on its own in `/model`, and when a helper agent's file sets a model (`model: sonnet` resolves to Claude Sonnet 5.5 through `ANTHROPIC_DEFAULT_SONNET_MODEL`). Saved transcripts on 2026-11-05 show `evidence-validator` and `confidence-calibrator` helpers answered only by `claude-sonnet-5-5`, never through a tier. 13 agent files set a model. PR #391 points the nicknames at tiers for the tiers a person may use, but the single-model rule below must cover every remaining case.

## Problems

1. **Only a fixed list of errors switches models.** `SWITCH_RULES` covers out-of-usage, billing, overloaded, provider busy, retired or unrouted models and an outdated provider login. A plain 429 "Rate limited", a 500, 502, 503 or 504 is passed straight back, and the model is not marked as failing, so every Claude Code retry (up to 10 by default, `CLAUDE_CODE_MAX_RETRIES`) lands on the same model and then the error is shown.
2. **A request that names one model has no failover** (see above).
3. **The shim's log is thrown away.** `GW_PROXY_LOGFILE` is unset by default and the running shim's output goes to `/dev/null`, so nobody can see which model failed, with what error, or whether the shim switched.

## Required behaviour

### A. Errors and parking

Every failure is one of three kinds:

| Kind | Which errors | What the shim does |
|---|---|---|
| Out of usage | Everything already in `SWITCH_RULES` (unchanged list) | Switch at once. Park the model for the gateway's `Retry-After` time, else `CCSESSION_COOLDOWN_SECONDS` (default 1 hour). Unchanged from today. |
| Server error | Status 408, 429, 500, 502, 503 or 504 that does not match `SWITCH_RULES`; an error reply cut off part-way | Count it against that model (see below). |
| The request's own fault | Any other 4xx (for example a malformed request, 413), and a "too large" error from the main model | Pass back unchanged; never counted, never switched. The existing rule that a too-small backup is skipped stays. |

Server errors, counted per model across every request and session of the shim:

- A failure adds 1 to the model's count of failures in a row. A successful reply sets the count to 0.
- While the count is below 3, the error goes back to Claude Code unchanged, and Claude Code's own retry tries again.
- The 3rd failure in a row parks the model and sends the same request on to the next model of the list (as an out-of-usage switch does).
- The first park lasts 5 minutes. When it ends the model is back in line and, being first in its list, is tried again by the next request. Each later park of the same model doubles: 10, 20, 40 minutes, capped at 1 hour. A successful reply resets the park length to 5 minutes.
- No start of a reply within `CCSESSION_FIRST_BYTE_TIMEOUT` (default 5 minutes, streamed requests only): switch at once, as today, because the request has already waited 5 minutes; the park follows the growing park above (start 5 minutes) instead of a fixed hour.
- A gateway that cannot be reached is still passed back with no switch (every model would fail).
- New settings, with these defaults: `CCSESSION_FAILS_BEFORE_SWITCH=3`, `CCSESSION_PARK_SECONDS=300`, `CCSESSION_PARK_MAX_SECONDS=3600`.

Within one request the shim walks the list once: a parked model is skipped; out of usage parks and moves on; a server error that reaches the 3rd failure parks and moves on; a server error below 3 ends the walk and goes back to Claude Code; success streams the reply. When every model is parked, today's reply stays: the last error with the "all ... models are out of usage; next retry at ..." note.

### C. A request that names one model

In tier mode, when a request names one model (a real Claude id such as `claude-opus-5-5`, or a `claude-gw-<name>` alias of a non-Claude model, compared without a trailing `[1m]`):

- Its fallback list is the tier where that model is listed highest: the tier in which its position is first, and when it holds the same best position in two tiers, the higher tier (Tier 0 above 1a above 1b above 2 above 3 above 4).
- The requested model is tried first (skipped while parked), then that tier's other models in their listed order, with the error and parking rules above.
- Only tiers the person's role may use count (`curation()["tiers"]`, already filtered by `tier_access`). A model in none of them is forwarded unchanged with no failover, as today.
- A backup whose window is smaller than the requested model's window is skipped, like a too-small backup in a tier.

| Model requested on its own | Falls back within | Then tries |
|---|---|---|
| Claude Opus 5.5 | Tier 1a | Claude Sonnet 5.5 |
| Claude Sonnet 5.5 | Tier 1b | GPT-6.1 Sol, Muse Wonder Full |
| GPT-6.1 Sol | Tier 2 | GLM-5.3, Grok 4.7, Qwen3.8 Max, Muse Wonder, Muse Spark |
| GLM-5.3 | Tier 2 (second in Tier 2 and Tier 3) | GPT-6.1 Sol, Grok 4.7, Qwen3.8 Max, Muse Wonder, Muse Spark |
| Claude Fable 5.1 | Tier 0 | GPT-6 Astra |

### D. The shim's log

- The shim writes its log to `${XDG_CACHE_HOME:-$HOME/.cache}/ccsession/proxy.log` by default; `GW_PROXY_LOGFILE` still overrides the path. The file is kept at most 5 MB, with one older copy (`proxy.log.1`).
- Every failure, its kind, the model's count, each park with its end time, each switch and the model that answered are logged.
- The log never contains a key, a token, an authorization header, or any part of a request or reply body other than the gateway's error message.

## Tests (failing first, against the existing fake gateway in `tests/unit/test_ccsession_tiers.py`)

- Two 500s from a tier's first model go back to Claude Code; the 3rd parks it and the same request is answered by the next model.
- A success between failures resets the count.
- Park lengths: 5, then 10, 20, 40, then 60 minutes; a success resets to 5 (injected clock, as `test_cooldown_with_an_injected_clock`).
- An out-of-usage error still switches at once and parks for `Retry-After` or the cooldown.
- A malformed-request error and a main-model "too large" error are never switched or counted.
- Successful HTTP streams pass through immediately and unchanged, including a lone ping, a leading error event, or an error after content. Keep existing streaming timing and mid-reply failure tests unchanged.
- A single named model falls back within its highest-listed tier, ties go to the higher tier, a parked named model is skipped, and a tier the role may not use is never used.
- The log is written to the default path, rotates at 5 MB, and holds no key, token, authorization header or request body.
- Intended changes to existing tests: `test_named_model_has_no_failover` and `test_errors_outside_the_rules_pass_back_unchanged` change to the new rules; every other existing test passes unchanged.

## Done when

- The tests above pass, along with the full ccsession, installer, hook, doctor and skills suites, `ruff check .` and `ruff format --check src/ tests/`.
- End to end on a workspace: the real `claude` command, pointed at the new shim on a separate port, with a scripted fake gateway, shows a tier request and a single-model request answered by the backup after the scripted failures, and Claude Code's retries driving the count.
- A live smoke test of the new shim on a separate port against the real gateway: a tier request and a single-model request still answer normally. The shared shim the user's sessions run on is never stopped, restarted or replaced during testing.
- The README failover table and `CHANGELOG.md` describe the new rules.

## Related

- #384, PR #385, PR #391 (nicknames pointed at tiers); #393 (retry ladder).

