---
topic: "AI-powered changelog summarizer feature"
domain: product
strategy: agile
depth: standard
proposals_target: 3
handoff_target: none
created: 2026-05-25T00:00:00Z
---

# Seed Brief: ai-powered-changelog-summarizer

## Problem Statement

Release managers and engineering leads at mid-market SaaS companies (50–500 engineers) spend 30–90 minutes per release converting raw git commits, PR titles, labels, and linked Jira/Linear tickets into a customer-readable changelog. The translation is repetitive, format-inconsistent across teams, error-prone (internal jargon leaking out, breaking changes under-flagged), and routinely delays release announcements by half a day or more. An AI-powered summarizer would ingest a structured release range, emit themed and persona-tuned changelog drafts, and provide a trust contract (traceable citations, redaction of sensitive content, immutable audit log) so that release managers can confidently ship LLM-generated copy to external audiences.

## Known Context

**Standard-depth Socratic clarification (Q1–Q3) and validation (Q6–Q10) answered against the product domain:**

- **Q1 — Who is the primary user?** Release manager / engineering lead at mid-market SaaS companies; secondarily a product manager who edits the customer-facing copy before publish. Buyer is typically the engineering manager or VP Engineering.
- **Q2 — What is the job-to-be-done?** "When I cut a release, I want a draft changelog grouped by theme and tuned to my audience, so I can publish customer-facing release notes within 5 minutes of release cut instead of 30–90 minutes."
- **Q3 — What does success look like in 90 days?** ≥10 active weekly release managers, ≥70% of finalized changelogs ship with ≤30% line-diff from the AI-generated draft, p95 cost-per-release ≤$0.75, and zero confirmed incidents of hallucinated breaking-change claims or leaked redacted content.
- **Q6 — What are the must-have constraints?** Cost ceiling (~$1 per 50-PR release), BYO-key privacy posture for private repos, Markdown-only output (no proprietary format), GitHub PR as primary input source for MVP.
- **Q7 — What is the riskiest assumption?** That release managers will trust LLM-generated copy enough to publish externally without painful line-by-line verification. Mitigation: a trust contract — every claim cites its source PR, breaking-change claims require corroborating signal (label or commit-message marker), and a redaction layer scrubs configured patterns before any LLM call.
- **Q8 — What is in vs. out of scope for MVP?** In: GitHub App, two-pass LLM pipeline, theme grouping, BYO-key, cost telemetry, redaction layer, traceability citations, audit log, web editor. Out: hosted inference, Jira/Linear/GitLab adapters, CLI/GitHub Action, mobile, multi-repo aggregation.
- **Q9 — What downstream consumers does the output serve?** Customer-facing changelog readers (end users of the SaaS product), internal engineering staff (for internal release summaries), and support/CS teams who reference the changelog when fielding tickets.
- **Q10 — What does "done" mean for v1?** A release manager installs the GitHub App, completes BYO-key + redaction-pattern onboarding in ≤10 minutes, receives a draft on a real release in ≤60 seconds, edits in the web editor with full traceability + audit, and publishes to the GitHub release with one click.

- Primary user persona: Release manager / engineering lead at mid-market SaaS companies (50-500 eng).
- Job-to-be-done: turn raw change feed into a customer-facing changelog grouped by theme (features / fixes / breaking) with optional persona tuning (developer-facing vs. business-facing) AND a trust contract that lets the user publish externally without manual line-by-line verification.
- Strategy: agile — MVP-first, ship a thin end-to-end slice including the trust contract, learn from real release cycles. The trust contract is feature-blocking, not a "fast follow."
- Depth: standard — explicit trust contract and editorial flow modeled, persona tuning included from v1, multi-tenant and monetization deferred.

## Constraints

- LLM cost per release must stay under $1 for a typical 50-PR release (BYO-key passthrough).
- Must accept GitHub PRs as the primary input source for MVP; Jira/Linear are deferred.
- Output must be editable Markdown — no proprietary format lock-in.
- Privacy: must not leak private PR titles to third-party LLMs without explicit per-repo opt-in AND a redaction layer pass.
- Time-to-MVP: 3 sprints (~6 weeks) for an internal-dogfood release — one sprint longer than iter-1 because trust contract is in-scope.
- Trust contract is feature-blocking: no proposal-level shipping without traceability citations, redaction layer, and immutable audit log.

## Success Criteria

- A release manager can paste/connect a GitHub release range and receive a draft changelog with full citation in under 60 seconds.
- Draft groups entries into ≥3 themes (features, fixes, breaking/deprecations) using structured extraction, not free-form rewriting.
- Every claim in the draft links back to a source PR ID; breaking-change claims require a corroborating signal (label, commit-message marker, or explicit "BREAKING" prefix).
- Redaction layer scrubs configured regex patterns (e.g., secrets, customer names, embargoed feature names) BEFORE any LLM call. Redaction events are logged.
- Immutable audit log records: who generated the draft, which model + version, prompt hash, input PR-set hash, redaction events, and final-published delta from draft.
- Editorial diff (final vs. generated) ≤30% lines changed across a 10-release sample.
- Cost telemetry visible per generation so a release manager can see "this draft cost $X".

## Open Questions

- Build-vs-buy: do existing tools (Release.com, What The Diff, GitHub's native auto-notes) cover 80% of this need, or is there a real wedge?
- In-product placement: standalone tool, GitHub App, or embedded in the existing release tooling?
- Persona tuning: is "developer-facing vs. business-facing" a meaningful axis at v1, or premature segmentation?
- Privacy posture for private repos: BYO-key (user provides OpenAI/Anthropic key) vs. hosted (we pay for inference) — and when does the hosted-inference SOC2 lift become worth it?
- Trust-contract enforcement: is "every claim must cite a source PR" a hard block on publish (current proposal) or a warning-only nudge? Architect leans block; frontend leans nudge.

## Enrichment Context

**Source**: `enrichment/research-light.md` (quality_tier: primary, simulated)

**Key findings**:
- Existing tools: What The Diff (per-PR, per-seat $19+, GitHub-app), Release.com (editorial, per-release pricing), GitButler's Release Notes (newer entrant, editorial), GitHub native release notes (free, label-driven, not LLM-powered — the "good enough" baseline to beat), Linear's auto-changelog (Linear-issue-driven, not PR-driven).
- Design patterns: (1) two-pass LLM (cheap per-PR structured extraction → stronger aggregate model for themed narrative), cost ~$0.10–$0.50 per 50-PR release; (2) structured extraction (JSON schema per PR) consistently beats free-form rewriting on grouping quality; (3) citation + grounding pattern (every claim cites source PR, post-generation validator checks every citation resolves to an actual PR in the input set) is emerging as the trust-contract standard.
- Privacy posture: BYO-key + per-repo opt-in is the safe MVP path; hosted inference requires SOC2 + DPA for enterprise. A redaction layer (regex + named-entity recognition on configured patterns) sits in front of the LLM call regardless of BYO-vs-hosted.
- Pricing: per-release or BYO-key + flat platform fee aligns with release-manager usage cadence; per-seat is poor fit.
- Trust/hallucination mitigation patterns: (a) citation requirement on every claim with post-gen validator; (b) breaking-change corroboration (LLM claim must match a label or commit marker); (c) redaction layer pre-LLM; (d) immutable audit log of model + prompt-hash + input-hash + redactions + final-published delta; (e) human-in-loop diff view in the editor.
- Plausible MVP wedge: GitHub App + themed grouping + persona tuning + cost-transparent telemetry + **trust contract** as a first-class feature, not a settings-page checkbox. Full artifact in `enrichment/research-light.md`.
