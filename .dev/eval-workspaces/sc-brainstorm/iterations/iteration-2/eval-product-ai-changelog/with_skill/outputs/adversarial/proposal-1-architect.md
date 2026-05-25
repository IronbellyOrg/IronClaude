---
proposal_id: 1
persona: architect
model: opus
custom_instruction: "prioritize maintainability and extension scaffolding for product domain"
stance: platform-capability
created: 2026-05-25T00:00:00Z
---

# Proposal 1 — Architect: Platform-Capability Foundation

## Stance

**Build the changelog summarizer as a thin product surface over a reusable "structured-LLM-pipeline" platform capability.** The two-pass extract-then-aggregate pipeline is not changelog-specific — it is the same shape we will need for release-risk summaries, customer-incident postmortems, and PR-batch reviews. Optimizing v1 for a single use case will produce a sunk cost when the second use case appears in two quarters. Optimizing for a clean platform abstraction now adds ~1 sprint of scaffolding cost and pays back on the second use case.

## Architecture

**Layered, with hard boundaries:**

1. **Ingestion adapters** (`adapters/*`) — one per source. MVP ships `github-pr-adapter`; the interface (`SourceAdapter.fetch(range) -> List[ChangeRecord]`) is sealed in v1 so Jira/Linear/GitLab adapters drop in without refactor. ChangeRecord is the universal currency.
2. **Redaction layer** (`redaction/`) — a configurable regex + NER pass operating on `ChangeRecord` fields BEFORE any LLM call. Configured per-repo via a `.changelog/redaction.yaml` checked into the user's repo (so redaction patterns live with the code they describe — not in our hosted database). Pluggable matchers: regex, deny-list, NER entity types. Every redaction emits a `RedactionEvent` to the audit log.
3. **Two-pass LLM pipeline** (`pipeline/`) — `ExtractPass` (Haiku-class, structured JSON schema per record) → `AggregatePass` (Sonnet-class, themed narrative over validated extractions). Both passes are provider-agnostic: an `LLMProvider` interface accepts `{model, prompt, schema}` and returns `{content, tokens_in, tokens_out, cost_usd}`. MVP ships `AnthropicProvider` + `OpenAIProvider`; new providers are ~100-line additions.
4. **Trust validator** (`validation/`) — runs over the AggregatePass output BEFORE the draft is rendered. Checks: every citation resolves to an input ChangeRecord; every breaking-change claim has a corroborating signal in the source record; no uncited claims. Validation failure = REJECT with structured error; the editor surfaces the failure inline (not a silent best-effort).
5. **Audit log** (`audit/`) — append-only event store. Backed by SQLite for MVP (small ops surface), with a clean interface that admits Postgres or DynamoDB later. Records every generation, every redaction, every publish, every model + prompt hash.
6. **Renderers** (`render/`) — `MarkdownRenderer` MVP; HTML/JSON deferred but the renderer interface is sealed in v1.
7. **Product surface** (`web/`, `github-app/`) — the thin layer. Web editor consumes the rendered draft + validation result + audit log. GitHub App is a webhook receiver that triggers the pipeline.

## Build vs. Buy

**Build** the pipeline + trust validator + audit log. These ARE the differentiator and CANNOT be safely bought (vendoring a black-box LLM summarizer for externally-published copy is the trust regression the seed brief calls out).

**Buy/use** vendor LLM APIs (Anthropic + OpenAI passthrough via BYO-key); vendor GitHub App OAuth flow (Octokit); vendor Markdown rendering (remark + rehype); vendor regex + NER libraries (re2 + spaCy or huggingface NER).

## Provider Abstraction Detail

The `LLMProvider` interface MUST be the only place provider-specific code lives. Rationale: in 12 months, half the value of this product is "we can switch from OpenAI to Anthropic to a local llama based on cost and the user's preference." Hard-coding `anthropic.messages.create(...)` in the pipeline would force a 2-week refactor at exactly the moment we want to ship a cost-saving move. Spending two days on the interface in v1 prevents that refactor.

**Interface contract:**
```python
class LLMProvider(Protocol):
    def call(self, model: str, prompt: str, schema: dict | None,
             cache_key: str | None) -> LLMResponse: ...

@dataclass(frozen=True)
class LLMResponse:
    content: str
    structured: dict | None  # populated if schema was provided
    tokens_in: int
    tokens_out: int
    cost_usd: Decimal
    model_used: str
    cache_hit: bool
```

## Performance & Cost Targets

- 50-PR release: ≤60s end-to-end (10s ingestion, 40s ExtractPass parallel-across-PRs, 8s AggregatePass, 2s validation + render).
- Cost ceiling enforced at pipeline-entry: pre-flight estimate via `tokens_estimated × pricing`. If estimate exceeds the user's configured budget, the pipeline STOPS and the editor surfaces "estimate $X exceeds budget $Y — adjust budget or split the release."
- Prompt-cache the ExtractPass system prompt; expect 30–40% cost reduction on the per-PR pass.

## Why This Wins

A purpose-built single-use changelog tool ships in 2 sprints; this proposal ships in 3 sprints with sealed interfaces that make the second product (incident postmortems, on the same pipeline) ship in 1 sprint instead of 3. The trust validator and audit log are required regardless — building them once cleanly costs the same as building them messily and prevents a second rewrite when the compliance review hits.

## Tradeoffs Acknowledged

- One extra sprint to MVP vs. the most aggressive cut.
- Adds an "interface" cognitive surface the frontend persona will want to skip.
- Provider abstraction adds ~150 lines that a purist-MVP would call premature.
- The redaction-config-in-user-repo choice (vs. our database) is a deliberate trust move: the user controls their redaction patterns; we never see them. This costs us a small product-analytics surface (we can't tell which patterns are popular across customers) but is the right answer for an enterprise-trustable changelog tool.
