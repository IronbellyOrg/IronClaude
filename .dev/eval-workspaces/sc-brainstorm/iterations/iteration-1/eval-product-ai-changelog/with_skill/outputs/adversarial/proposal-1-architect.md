---
proposal_id: 1
persona: architect
model: opus
domain: product
strategy: agile
simulated: true
---

# Proposal 1: Architect — Platform Capability First, Ship Through GitHub App MVP Surface

## Framing

Treat the changelog summarizer not as a single in-product feature but as a **platform capability** — a "change-event → structured-summary" pipeline — with the GitHub App as the first consumer. This costs slightly more up front (one extra abstraction boundary) and pays back the moment we want a second surface (CLI, web UI, Jira import, in-product release-notes block in a customer's own product).

## Technical Architecture

**Two-pass LLM pipeline as a service**:
1. **Ingest layer**: accepts a normalized `ChangeEvent[]` (PR title, body, labels, author, files-changed-summary). Adapter pattern — first adapter is GitHub PRs via webhook + REST; future adapters drop in without changing downstream code.
2. **Per-PR extraction pass (cheap model — Haiku-class)**: prompts each PR through a JSON schema → `{type: feature|fix|breaking|chore, scope, customer_visible: bool, summary: str, persona_hints: [...]}`. Schema-validated; bad outputs retry once then fall back to PR title verbatim.
3. **Aggregate pass (stronger model — Sonnet-class)**: groups extracted entries by theme + persona, writes themed narrative Markdown. Deterministic templating wraps the LLM-generated prose so format is predictable.
4. **Output adapter**: renders Markdown (MVP); future adapters for HTML, JSON-LD, in-product blocks.

## Build vs. Buy

- **Buy**: GitHub native is free but template-driven, not LLM-powered. What The Diff is per-PR-focused; aggregation is afterthought. Release.com is editorial-heavy, opinionated format.
- **Build**: justified because the wedge is the *combination* of (themed grouping + persona tuning + cost-transparent telemetry + BYO-key privacy), none of which existing tools combine cleanly.
- **Don't reinvent**: use vendor SDKs (Anthropic / OpenAI), don't roll our own inference. Use existing schema-validation lib (Zod / Pydantic) for structured extraction guardrails.

## LLM Integration Decisions

- **BYO-key default, hosted as a paid upgrade.** Removes SOC2 lift for MVP; lets us learn what enterprises actually want before paying for compliance.
- **Two-model split** (Haiku per-PR, Sonnet aggregate) keeps cost in the $0.10–$0.50 range per 50-PR release. Telemetry surfaces this per-generation.
- **Schema-driven prompts**, not free-form. Easier to evaluate offline (golden dataset of PR → expected schema), easier to swap models, easier to add personas as schema variants.
- **Prompt caching** on the system prompt across per-PR calls in a single release — cuts cheap-pass cost by ~50% on large releases.

## Risks I'd Surface in Debate

- "Platform-first" can become "platform-only" — discipline required to ship the GitHub App MVP first, not yak-shave the abstraction.
- Model-vendor coupling: BYO-key means we have to support multiple providers (Anthropic, OpenAI, possibly Bedrock) which adds maintenance.
- Cost-transparency is a feature we have to build (token counting per call, summing per generation) — small but non-zero.

## MVP Scope I'd Ship First

1. GitHub App that posts a draft changelog as a comment on release creation.
2. BYO-key flow (user pastes Anthropic/OpenAI key, stored encrypted per-repo).
3. Markdown output with 3-theme grouping; persona tuning behind a feature flag.
4. Cost telemetry shown inline in the comment ("This draft cost $0.23").
5. NO web UI, NO Jira, NO CLI in MVP. Earn them with usage data.

## Why This Wins

A platform layer means the second feature (CLI / Jira / in-product block) ships in days, not weeks. The GitHub App MVP still lands in 2 sprints because most of the work (LLM pipeline) is shared. The cost is one extra abstraction boundary — small price for the optionality.
