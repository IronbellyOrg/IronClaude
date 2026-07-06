# 429 Signature Ground Truth (CLIProxyAPI → LiteLLM → claude CLI)

Captured from the real failed run: `.dev/releases/current/v0.1/results/phase-{3,4,5}-task-*-output.txt`.
Source format: Claude CLI `--output-format stream-json` (one JSON object per line) written to `*-output.txt`.

## Headline facts

1. **Nothing lands on stderr.** All `*-errors.txt` sidecars for 429 tasks are **0 bytes**. The detector MUST parse stdout stream-json, not stderr.
2. The 429 appears in **three distinct event types** in a single transcript:
   - N× `{"type":"system","subtype":"api_retry",...,"error_status":429,"error":"rate_limit"}` (in-CLI retry loop, `max_retries:10`)
   - 1× terminal `{"type":"assistant","message":{...,"model":"<synthetic>",...},"error":"rate_limit"}` (harness-injected error message; note the literal `"model":"<synthetic>"`)
   - 1× terminal `{"type":"result","subtype":"success","is_error":true,"api_error_status":429,...}` (the load-bearing terminal envelope)
3. **Two distinct upstream message bodies** — and they mean different things:
   - **Single-account limit (raw Anthropic body):** `This request would exceed your account's rate limit. Please try again later.` — 14 occurrences. One routed account hit its 5h/7d cap.
   - **All-account exhaustion (CLIProxyAPI's own body):** `All credentials for model claude-opus-4-8 are cooling down via provider claude` — 27 occurrences. CLIProxyAPI has already rotated through every account for that model and they are all cooling down. **This is the "switch model/alias" signal**, distinct from attempt-counting.
4. A genuine operation timeout is a different signature: `"result":"API Error: The operation timed out."`, `api_error_status: null`, `is_error: true` (seen once, T03.05). Do NOT fold this into the 429 class.

## Verbatim terminal `result` envelope — Case A (immediate, single-account, num_turns=1)

`phase-3-task-T03.14-output.txt` line 17 (full file is only 17 lines: hooks, init, 10× api_retry, synthetic assistant, result):

```json
{"type":"result","subtype":"success","is_error":true,"api_error_status":429,"duration_ms":200168,"duration_api_ms":0,"num_turns":1,"result":"API Error: Request rejected (429) · b'{\"type\":\"error\",\"error\":{\"type\":\"rate_limit_error\",\"message\":\"This request would exceed your account\\'s rate limit. Please try again later.\"}}'","stop_reason":"stop_sequence","session_id":"29314b57-...","total_cost_usd":0,"usage":{"input_tokens":0,...,"output_tokens":0},"modelUsage":{},"terminal_reason":"completed","fast_mode_state":"off"}
```

## Verbatim terminal `result` envelope — Case B (all-account cooldown; can occur after real work, num_turns=25)

`phase-3-task-T03.13-output.txt` line 88:

```json
{"type":"result","subtype":"success","is_error":true,"api_error_status":429,"duration_ms":489495,"duration_api_ms":297921,"num_turns":25,"result":"API Error: Request rejected (429) · b'{\"type\":\"error\",\"error\":{\"type\":\"rate_limit_error\",\"message\":\"All credentials for model claude-opus-4-8 are cooling down via provider claude\"}}'","stop_reason":"stop_sequence","session_id":"7787126c-...","total_cost_usd":1.9294045,"usage":{"input_tokens":10945,...,"output_tokens":22999},"modelUsage":{"claude-opus-4-8[1m]":{...}},"terminal_reason":"completed","fast_mode_state":"off"}
```

## Verbatim `api_retry` event (repeats up to max_retries:10)

`phase-3-task-T03.14-output.txt` line 6:

```json
{"type":"system","subtype":"api_retry","attempt":1,"max_retries":10,"retry_delay_ms":513.9429238737755,"error_status":429,"error":"rate_limit","session_id":"29314b57-...","uuid":"95fdaf2e-..."}
```

## Verbatim synthetic terminal assistant message

`phase-3-task-T03.14-output.txt` line 16:

```json
{"type":"assistant","message":{"id":"4b5833a5-...","model":"<synthetic>","role":"assistant","stop_reason":"stop_sequence","content":[{"type":"text","text":"API Error: Request rejected (429) · b'{\"type\":\"error\",\"error\":{\"type\":\"rate_limit_error\",\"message\":\"This request would exceed your account\\'s rate limit. Please try again later.\"}}'"}]},"error":"rate_limit"}
```

## Pinned detector predicates (recommended)

Classify the per-task terminal `result` line (last non-blank JSON line with `"type":"result"`):

- **is a provider-rate-limit terminal failure** when:
  `obj.type == "result" AND obj.is_error == true AND obj.api_error_status == 429`
  (equivalently the `result` string matches `/Request rejected \(429\)/` and contains `rate_limit_error`).
- **all-account exhaustion (→ recommend model/alias switch, halt after policy):** the `result` (or terminal assistant text) contains the literal substring
  `are cooling down via provider` (CLIProxyAPI-emitted). Regex: `/All credentials for model .+ are cooling down via provider/`.
- **single-account limit (→ new-session retry is worth trying, may route to a fresh account):** `result` contains
  `This request would exceed your account's rate limit`.
- **in-session retries already exhausted:** presence of `{"subtype":"api_retry",...,"error_status":429}` lines, max `attempt` == `max_retries` (10). The CLI already burned its own retry budget before emitting the terminal 429 — so a sprint-level in-session retry is pointless; only a NEW session (new CLIProxyAPI route) or a model switch can help.
- **operation timeout (distinct class, NOT 429):** `obj.is_error == true AND obj.api_error_status == null AND result == "API Error: The operation timed out."`

## Counts across phases 3-5 (41 total provider-429 terminal envelopes)

- 27× `All credentials for model claude-opus-4-8 are cooling down via provider claude` (all-account)
- 14× `This request would exceed your account's rate limit. Please try again later.` (single-account)
- 1× `API Error: The operation timed out.` (timeout, separate class)
