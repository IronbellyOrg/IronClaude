# Research Notes: Model and effort router, proxy scope slice

**Date:** 2026-11-09
**Scenario:** A, focused scope discovery
**Depth Tier:** Deep parent research, bounded slice 3
**Status:** Complete (assigned scope discovery only; parent independent review pending)
**Assigned scope:** local gateway alias proxy lines 1-906 and related caller/test discovery only.
**Execution:** Independent Tier1b researcher; parent context ctx_c249d546e5f2.

---

## EXISTING_FILES
### Core proxy and boundaries

- `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py`: 906 lines, one executable standard-library HTTP proxy subsystem, with alias discovery, tier selection, cooldown, and response streaming. All 906 assigned lines were read in chunks of at most 100 lines; no source changed.
- Request entry is `Handler.do_POST` -> `_post` -> `_forward_tier` for syntactically recognized tier names, otherwise `_proxy`. `_post` reads the declared Content-Length, parses JSON, recognizes a numeric tier suffix with optional letter, or resolves a named `claude-gw-` alias from the map (refreshing it when cold). It changes the model field for recognized aliases but otherwise retains the request body (`src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:572-607`).
- `Handler._open_upstream` is the shared transport: original method and path/query, HTTP or HTTPS from the configured upstream, copied non-hop headers, recomputed Content-Length, and identity encoding for tier error inspection. Connection errors, first-byte timeout, and an upstream reply are separate return cases (`src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:674-721`).
- `switch_reason`, `retry_after_seconds`, `cool_down`, and `cooling_until` implement failover matching and process-local cooldown state. Matching is case-insensitive and includes selected status/body combinations, status-only 402/529, and status-independent billing/overload markers. Retry-After accepts seconds or HTTP dates and caps it at seven days (`src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:362-429`). A plain 500 is not enough, but a 500 body containing `overloaded` is enough.

### Integration inventory (discovery, not a deep read of neighboring slices)

- `src/superclaude/skills/ccsession-tag/models.py`: sibling module imported by the proxy. Integration APIs observed at proxy call sites: `load`, `tier_env`, `tier_mode`, `tier_access`, `assign_aliases`, `gateway_alias`, `is_native_model`, `unavailable`, `code_digest`, `settings_digest`, and `DEFAULT_WINDOW`. Their internal contracts remain assigned to the neighboring contracts slice.
- `src/superclaude/skills/ccsession-tag/ccsession`: shell launcher starts the proxy and supplies upstream, port, and component directory. Only the startup call site was read, not launcher selection/init logic.
- `src/superclaude/skills/ccsession-tag/ccsession-models.json`: model/tier data, not an effort policy engine; installed copy maps Tier1b to three environment slot names. No launcher default is proposed here.
- `src/superclaude/skills/ccsession-tag/README.md`: tier and failover documentation, cross-checked below.
- `tests/unit/test_ccsession_tiers.py`: principal behavioral regression suite. Directly read tests verify cooldown expiry, Retry-After, first-byte fallback, unreachable gateway, no failover for named models, live defaults reread, and no switch after streaming begins (`tests/unit/test_ccsession_tiers.py:1057-1135`). These are source-inspected tests, not observed passing runs.
- Search also found proxy references in `tests/unit/test_ccsession_tag.py`, `tests/unit/test_cli_install.py`, and `tests/cli/test_update_command.py`; these are follow-on test/package surfaces, not fully investigated here. Total discovered surfaces: one proxy source, three sibling integration/data files, one README, and four test files (9 paths across proxy, launcher/model data, documentation, and test/packaging concerns).

## PATTERNS_AND_CONVENTIONS
### CODE-VERIFIED: routing and protocol boundaries

- `Handler._forward_tier` rereads curation for each request, rejects unavailable tiers with a JSON 400, skips slots with a window smaller than the tier window, and skips models cooling down. It rewrites only `obj["model"]` before serializing the same request object for each attempt (`src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:723-746`). There is no model-specific effort or thinking rewrite in this loop.
- A connection failure returns 502 immediately without changing models; a streamed first-byte timeout cools the selected model and tries the next slot; success streams immediately (`src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:747-777`). A truncated error body returns 502 rather than retrying; matching switch errors cool down and retry; a backup rejecting conversation size is skipped without cooldown (`src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:778-821`).
- `Handler._stream` forwards status and non-hop headers, then flushes each `read1(8192)` chunk. It searches early response bytes for a model label for audit only; it does not translate response model names, SSE event types, tool calls, or thinking blocks (`src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:841-867`). Once success streaming begins, no alternate model is attempted by this function.

### Execution identity, not a proposed default

- Live health of this worker's configured shim showed tier mode enabled and Tier1b slots ordered as `claude-sonnet-5-5`, `gpt-6.1-sol`, `muse-wonder-full-1.0`. The workspace defaults file independently names the same ordered slots (`/etc/aidev02/aienv.d/defaults.sh:28-33`, read through a selected-key search).
- This worker's own session transcript reports actual backend `gpt-6.1-sol` on its latest three assistant records at 2026-11-09T02:42:59Z. This is the second live Tier1b slot, not merely the displayed tier alias. Evidence file: `/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-issue-463/455d2ebc-ed23-4503-8749-a03c858b3678.jsonl`; only timestamp and model fields were extracted, not message content or credentials.
- Transcript metadata verifies the reported backend label, not provider-side execution internals or the reason the first slot was skipped. No deliberate fallback or model switch was triggered. Tier1b is this investigation's execution choice only; this research does not alter or reinterpret issue 462's `default=user` Coder-role default.

## SOLUTION_RESEARCH
N/A: focused scope discovery, not implementation or web research. The current proxy is reusable transport/alias/failover machinery; it is not itself an effort-policy engine.

### Documentation cross-validation

- CODE-VERIFIED: README's selected out-of-usage fallback, cooldown, and context-window filtering descriptions agree with the proxy and existing regression assertions. The regression explicitly checks that a conversation containing signed thinking, tool-use, and tool-result blocks reaches the backup unchanged apart from model (`src/superclaude/skills/ccsession-tag/README.md:447-449`; `tests/unit/test_ccsession_tiers.py:898-938`). This proves intended payload preservation in the mock gateway fixture, not cross-provider acceptance in production.
- CODE-VERIFIED: the documented model picker lists tiers plus individual models when enabled. `curation` filters tiers by access, and `transform_models` emits tier IDs, assigns aliases before sorting/filtering displayed models, and updates the shared alias map (`src/superclaude/skills/ccsession-tag/README.md:446`; `src/superclaude/skills/ccsession-tag/local-gateway-alias-proxy.py:190-221`, `:299-359`).
- CODE-CONTRADICTED if interpreted literally as every HTTP 500: README's phrase that “a 500” is passed unchanged is too broad. A 500 containing `overloaded` is explicitly in the switch-rule regression (`src/superclaude/skills/ccsession-tag/README.md:447`; `tests/unit/test_ccsession_tiers.py:945-970`). An ordinary unrelated 500 remains passthrough. This is a documentation precision follow-up, not authorization to edit it.
- UNVERIFIED: README's launcher defaults, profile refusal, and named-model window derivation are owned by other scope slices and were not validated by this proxy investigation. Proxy comments claiming the client filters model IDs or strips `[1m]` are external client behavior, not proven by this Python implementation.

### Negative evidence and unresolved boundaries

- Search of the full assigned proxy for `effort|reasoning_effort|output_config|budget_tokens|thinking` found only a display-label token, the phrase “best-effort,” and a streaming comment. Combined with directly read request rewrites, this supports a bounded conclusion: this file has no explicit effort translation, validation, or per-backend effort selection. It does not establish absence across the launcher, gateway, or client.
- The existing payload-preservation regression exercises thinking and tools, not an explicit effort/output_config mapping. Search of `tests/unit/test_ccsession_tiers.py` found an `effortLevel` setting fixture in picker/launcher tests, but this slice did not inspect that neighboring launcher test in depth. No proxy-specific effort-compatibility test was located in the bounded discovery; do not generalize this to the whole repository.
- CodeGraph reported a fresh index with no indexed file dependents for the proxy. This is not “no callers”: shell launch and dynamically loaded test references were found by text search. The model/launcher source internals were deliberately not deep-read.
- Initial selected-key searches in the user ccsession env found no Tier1b slots; the authoritative workspace defaults file and live shim health did. Inherited shell slot windows differed from the workspace defaults, so live settings must not be inferred from inherited environment alone. Slot model names agreed.
- A broad `/tmp` filename discovery timed out and was not used as evidence. The worker backend was instead verified from its own session transcript plus live shim health.
- Inspection side effect: the exact command below, intended only to extract transcript fields, automatically created the checkout's `.venv`, built the local project, and installed 27 dependencies. Tool output reported CPython 3.11.15, local `superclaude` build, and 27 packages installed. This was unintended and disclosed to the coordinator; the coordinator instructed preservation and static inspection only, and no deletion, tests, or further package commands followed. No source/test/config changes or test runs were made by this worker. The assigned artifact remains for parent staging along with the other parent-owned research outputs; this worker did not stage shared work after the static-only direction.

```bash
uv run python -I -c 'import json,collections; p="/home/coder/.claude/projects/-home-coder-workspaces-worktrees-IronClaude-issue-463/455d2ebc-ed23-4503-8749-a03c858b3678.jsonl"; rows=collections.deque(maxlen=3); f=open(p); [(rows.append({"timestamp":o.get("timestamp"),"model":o.get("message",{}).get("model")}) if o.get("type")=="assistant" else None) for line in f for o in [json.loads(line)]]; print(json.dumps(list(rows)))'
```

### External questions for later research, no web performed

1. What exact effort/thinking fields does the installed client send for each model family, and when does it suppress or retain them after a model switch?
2. Does the upstream `/cli` gateway normalize Anthropic-style effort/thinking into each selected backend's supported schema, reject unsupported values, or silently discard them?
3. Can the gateway safely reuse signed thinking/tool histories across backend families, and what error shape identifies incompatibility without duplicating a partially executed tool request?
4. What client guarantees exist for `[1m]` stripping, provider capability discovery, retry/idempotency, and streamed error handling? Verify against the installed client/gateway versions and controlled traces before recommending a policy boundary.

## RECOMMENDED_OUTPUTS
Only this assigned scope artifact is produced by this worker. The following are proposed parent-owned follow-on outputs under `.dev/tasks/to-do/TASK-RESEARCH-model-effort-router-20261109-023552/`, not existing or independently authored reports:

- `research/proxy-request-fidelity.md`: request/body/header and response fidelity, explicit effort fields, named alias versus tier behavior.
- `research/proxy-fallback-boundaries.md`: retry eligibility, cooldown ownership, context filtering, stream boundaries, and incomplete/error reply behavior.
- `research/gateway-effort-capabilities.md`: verified client/gateway/provider capability boundary with version-pinned external evidence and controlled traces if authorized later.
- `synthesis/request-effort-boundary.md`: map desired effort policy to the component that actually selects the final backend; distinguish routing intent from backend capability.
- `synthesis/fallback-and-observability.md`: map replay safety, fallback semantics, and reliable actual-backend evidence.
- Parent final report and parent independent quality review: use the parent skill's selected final paths, not a new path invented by this slice.

## SUGGESTED_PHASES
1. **Code Tracer: request and effort fidelity.** Inspect proxy `_post`, `_proxy`, `_open_upstream`, `_forward_tier`, `_stream`, and the mock gateway/_ask fixture in `tests/unit/test_ccsession_tiers.py`; inspect alias passthrough tests in `tests/unit/test_ccsession_tag.py`. Record named-model, tier, malformed/non-object JSON, missing/bad Content-Length, query paths, tier aliases with literal `[1m]`, and all effort/thinking fields without changing code. Output: `research/proxy-request-fidelity.md`; synthesis: `synthesis/request-effort-boundary.md`. External topic: actual client request schema and suffix behavior, only after internal gaps are mapped.
2. **Integration Mapper: final-backend capability boundary.** Consume the neighboring launcher and model-contract slice artifacts rather than redoing them. Trace only the upstream gateway interface and actual request/response model evidence; determine whether effort selection belongs before alias resolution, after final slot selection, or in the upstream translator. Output: `research/gateway-effort-capabilities.md`; synthesis: `synthesis/request-effort-boundary.md`. External topic: version-matched client/gateway/provider effort support and cross-provider history compatibility. Preserve issue 462's `default=user` rule independently of investigator execution tier.
3. **Architecture/Pattern Investigator: fallback and evidence.** Inspect `switch_reason`, cooldown helpers, `_FirstByteResponse`, `_forward_tier`, `_stream`, related error/timeout/TLS/compression tests, health reporting, and opt-in audit behavior. Investigate model-keyed process-local cooldown sharing, changed defaults while requests are active, error-body matching before size classification, no retry after stream starts, and audit model detection limits. Output: `research/proxy-fallback-boundaries.md`; synthesis: `synthesis/fallback-and-observability.md`. External topic: upstream first-byte/stream semantics and retry/idempotency guarantees.
4. **Parent independent review, not a child of this worker.** Check exact source citations and bounded absence claims against disk; verify docs labels, backend evidence, scope boundaries, and the environment-side-effect disclosure. No tests were run by this discovery worker; any later regression run requires the parent assignment/authorization. This worker does not claim its own notes passed an independent gate.

## TEMPLATE_NOTES
Structure derives directly from installed `tech-research/SKILL.md` A.4: all seven displayed headings are retained (the prose calls them six categories). The artifact was stubbed before source discovery and populated incrementally. Parent tech-research Stage A may use Template 02 as its skill prescribes; this worker neither selects a new implementation executor nor builds a task file. Deep parent research remains partitioned; this artifact covers only the assigned proxy slice. No web, children/native agents, implementation edits, or policy/default changes were performed.

## AMBIGUITIES_FOR_USER
None: assigned scope and execution-tier constraints are clear. External capability questions belong to later investigation, not a user-intent decision. The parent must retain the unintended environment creation disclosure and arrange independent review; no claim of a passed research-quality gate is made here.
