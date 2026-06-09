# Swarm Transport Limits — Phase 1 (AC-010 / T07.20)

> 📚 Part of the [swarm documentation](./README.md). See also the
> [User Guide → real proxy](./user-guide.md#6-running-against-a-real-model-proxy).

This page documents the **deliberate transport-feature exclusions** that
apply to the Phase-1 swarm deployment. The same limits are inherited
verbatim from the parent `sc-bare-review` spec §7.3 ("Transport
options") and §11.4 ("Schema drift across vendors"), and are enforced
in code by the OpenAI-compatible httpx transport
(`src/superclaude/cli/swarm/transports/openai_compat.py`).

> **AC reference note.** The phase-7 tasklist refers to this work as
> "AC-016 Phase-1 transport limits" (T07.20). The substantive
> roadmap row is **AC-010 / R-134** ("No streaming, function-calling,
> or vision input — operational, Phase 1; inherited from parent spec
> §7.3"). The two IDs cover the same constraint; AC-010 is the binding
> source for enforcement and audit.

## Excluded modes (Phase 1)

| Excluded mode | What it means | Phase-1 status |
|---|---|---|
| **Streaming** | Server-Sent-Events / chunked Chat-Completions responses (`stream: true`). | NOT supported. Transport omits the `stream` field; responses are read whole. |
| **Function calling / tool use** | OpenAI-style `tools` / `tool_choice` / `function_call` parameters. | NOT supported. Transport omits all tool-call fields; responses are treated as plain assistant text. |
| **Vision input** | Multi-modal `content` arrays containing `image_url` / `image` parts. | NOT supported. Transport accepts only a single user message with a `string` `content` field. |

The Phase-1 transport payload is intentionally minimal — `model`,
`messages` (one user turn, string content), and `temperature`. Any
other parameter is omitted, not silently passed through; see
`OpenAICompatTransport.send` in `openai_compat.py`.

## Rationale

The Phase-1 transport targets the **lowest-common-denominator** of
OpenAI-compatible Chat-Completions endpoints exposed by the T2 proxy
(DeepSeek, Qwen, Kimi, GLM, …). Each upstream vendor diverges in its
support for streaming, function-call shape, and vision content. Per
parent spec §11.4:

> *Reference implementation targets the lowest-common-denominator
> (OpenAI v1 chat/completions, no streaming, no function calling) ...
> per-vendor quirks documented in `docs/t2-proxy-setup.md`.*

The exclusions exist for three concrete reasons:

1. **Cross-vendor portability.** Streaming and tool-call schemas differ
   per upstream; omitting them lets the same transport address every
   T2-proxy-fronted model without per-vendor adapter logic.
2. **Determinism for reviewer dispatch.** The bare-review use case
   (the M8 caller) expects each worker to return a single completed
   markdown blob. Streaming buys nothing here and would complicate the
   atomic-write / `raw_path` contract (FR-017 / NFR-010).
3. **Auditability surface.** Excluding tool-use means the swarm
   contract surface stays free of any caller-side execution primitive
   — reinforcing AC-013 (contract non-precluding) and NFR-016
   (no Claude-isms in the contract surface).

## Enforcement (transport rejects / omits)

The exclusions are mechanical, not aspirational:

- **Payload shape.** `OpenAICompatTransport.send` builds the request
  body with exactly three keys (`model`, `messages`, `temperature`)
  and posts to `<T2ProxyUrl>/chat/completions`. There is no code path
  that adds `stream`, `tools`, `tool_choice`, `function_call`, or an
  image-bearing content array.
- **Response handling.** The transport reads the full response body
  via `response.text` / `response.json()` (no streaming consumer).
  Parsing requires a non-empty `choices[0].message.content` string;
  anything else maps to `parse_error` (§7.4 salvage stays a downstream
  concern).
- **Input validation.** `WorkerSpec.prompt` is typed as `str`; the
  CLI surface, recipes, and lenses never construct multi-part image
  content. The contract-surface grep audit (T07.15 / NFR-016) catches
  any future regression that would introduce vendor-specific tool
  fields into the swarm surface.

A future addition of any of these modes is a **Phase-4+** concern (see
below) and must arrive paired with a corresponding contract update,
not as a silent transport-layer expansion.

## Future work

- **Phase 4+ MCP transport.** Parent §7.3 names
  `mcp__t2-proxy__chat` as an optional later transport whose pros
  include "native streaming, structured errors". When that
  transport lands, streaming becomes an opt-in *transport feature*,
  not a default; the bare-review reducer would still expect whole
  blobs per worker.
- **Tool-call / function-calling support.** Out of scope until a
  reviewer recipe genuinely needs structured outputs (e.g., a
  machine-checked finding schema). At that point the recipe — not the
  transport — should declare the schema and the transport gains a
  guarded code path behind a recipe-level capability flag.
- **Vision / multi-modal input.** Out of scope until a swarm caller
  needs image-based review (e.g., UI-screenshot diff review). Any
  future enablement must come with: (a) a recipe-level opt-in, (b) a
  per-vendor capability matrix in `docs/t2-proxy-setup.md`, and (c)
  cost / token accounting updates in the reducer.

## See also

- Parent spec: `sc-bare-review` merged-requirements §7.3, §11.4.
- Roadmap row R-134 / AC-010: "No streaming, function-calling, or
  vision input (operational, Phase 1)".
- Transport implementation: `src/superclaude/cli/swarm/transports/openai_compat.py`
  (Phase-1 reference, OpenAI-compatible httpx).
- Contract-surface audit: `tests/swarm/test_contract_surface.py`
  (T07.15 / NFR-016) — guards against Claude-isms and tool primitives
  leaking into the swarm contract.
- Vendor quirks: `docs/t2-proxy-setup.md` (per-vendor schema notes).
