---
spec_type: requirements
source: seed-brief.md
domain: product
strategy: agile
depth: quick
adversarial_status: pass
convergence_score: 0.81
proposal_count: 2
created: 2026-05-25T00:00:00Z
---

# Merged Requirements: AI-Powered Changelog Summarizer (MVP)

## Problem Statement

Release managers and engineering leads at mid-market SaaS companies spend 30–60 minutes per release converting raw git PRs, commits, and ticket references into a customer-readable changelog. The work is repetitive, format-inconsistent across teams, and delays release announcements. Existing tools either solve only the per-PR summarization step (What The Diff), require heavy editorial workflow (Release.com), or aren't AI-powered at all (GitHub's native release notes). There is a wedge for a tool that combines themed grouping, fast editorial finalization, persona tuning, BYO-key privacy, and inline cost transparency, shipped via a low-friction GitHub App.

## User Personas

1. **Release Manager (primary)** — engineering lead or release coordinator at a 50–500-engineer SaaS company. Owns the weekly or biweekly release process. Currently spends 30–60 min hand-editing changelog drafts. Cares about: speed, predictable format, no per-seat pricing, ability to ship without legal/privacy lift.
2. **Engineering Manager (secondary, dogfood)** — uses the tool ad-hoc for internal release summaries to staff. Cares about: ability to switch tone to "internal-engineering" persona, low cost.
3. **Customer Success / PM consumer (downstream, non-user)** — reads the final changelog. Cares about: clarity, customer-relevant grouping, no internal jargon. Their needs shape the persona-tuning requirement even though they don't operate the tool.

## Functional Requirements

1. **GitHub App integration**: install per-repo via GitHub App OAuth; subscribe to release-creation events; auto-post a draft changelog as a comment on the new GitHub release within 60 seconds of release creation.
2. **Two-pass LLM pipeline**: (a) per-PR structured extraction using a cheap model (Haiku-class) emitting JSON `{type, scope, summary, customer_visible, breaking}`; (b) aggregate themed-narrative pass using a stronger model (Sonnet-class) over validated extractions. Failed per-PR extractions retry once then fall back to PR title verbatim.
3. **Themed grouping in output**: drafts MUST group entries into at least three themes — Features, Fixes, Breaking/Deprecations. Entries marked `customer_visible=false` excluded from the customer-facing draft.
4. **Minimal web editor**: three-column theme view, drag-to-regroup between themes, per-entry retone button (developer-facing / business-facing / executive), per-entry exclude toggle, live Markdown preview, "Publish to GitHub release" terminal action.
5. **BYO-key flow**: user pastes an Anthropic or OpenAI API key during onboarding; key stored encrypted per-repo; all inference proxied through user's key. No hosted inference in MVP.
6. **Cost telemetry**: every generated draft shows token counts + dollar cost (computed from the user's vendor pricing), surfaced inline in the GitHub comment AND as a status-bar element in the web editor.
7. **Markdown export**: every draft and finalized output available as raw Markdown via copy button and "Publish to GitHub release" action.

## Non-Functional Requirements

1. **Performance**: draft generation completes in ≤60 seconds for a release with up to 50 PRs; web editor first-paint in ≤2 seconds.
2. **Cost ceiling**: typical 50-PR release MUST cost ≤$1 in vendor inference fees (achieved via two-pass split + prompt caching on system prompt across per-PR calls).
3. **Privacy**: BYO-key required for private repos; per-repo opt-in toggle for any third-party inference; no PR content stored beyond 7 days post-generation.
4. **Accessibility**: web editor MUST support full keyboard navigation including drag-and-drop (arrow keys + space-to-pick-up); screen-reader labels on theme columns and per-entry actions; WCAG 2.1 AA compliance for color contrast and focus indicators.
5. **Reliability**: extraction-pass failures degrade gracefully (PR title fallback) rather than blocking the aggregate pass; the GitHub comment always lands even if some entries are stubs.

## Acceptance Criteria

1. A release manager can install the GitHub App, complete BYO-key onboarding, and receive a draft on a real release in under 10 minutes end-to-end.
2. Draft generation for a 50-PR release completes in ≤60 seconds and costs ≤$1 in inference fees (measured + asserted by integration tests against vendor-pricing fixtures).
3. Across a 10-release sample of dogfooded internal releases, ≥70% of finalized changelogs ship with ≤30% line-diff from the AI-generated draft.
4. Web editor passes WCAG 2.1 AA automated checks (axe-core) and keyboard-only user-journey test (install → edit → publish without mouse).
5. Private-repo enforcement: attempting to generate a draft on a private repo without a configured BYO-key returns a clear actionable error AND does not transmit any PR content to any LLM vendor (verified by a network-mock integration test).

## Success Metrics

1. **Weekly active release managers** (north-star): ≥10 distinct release managers actively generating drafts weekly within 8 weeks of GA.
2. **Draft-shipped-without-rewrite rate**: ≥70% of finalized changelogs ship with ≤30% line-diff from draft (per AC #3).
3. **Cost-per-release p95**: ≤$0.75 at p95 across all generated drafts (validates the two-pass + caching architecture).

## Open Questions

1. **Hosted-inference upgrade timing**: when (if ever) do we add hosted inference as a paid tier? Requires SOC2 + DPA — meaningful enterprise lift. Defer until ≥5 enterprise prospects explicitly ask.
2. **Multi-source ingestion** (Jira, Linear, GitLab): adapter pattern is designed-in but only GitHub PR adapter ships in MVP. Trigger for second adapter = ≥3 dogfood users explicitly request a specific source.

## MVP Scope

**In scope**:
- GitHub App with auto-post on release creation.
- BYO-key onboarding (Anthropic + OpenAI).
- Two-pass LLM pipeline with structured extraction + themed-narrative aggregate.
- Minimal web editor: three-column theme view, drag-to-regroup, per-entry retone (3 personas), per-entry exclude, Markdown preview, "Publish to GitHub release".
- Cost telemetry inline in GitHub comment + editor status bar.
- Markdown-only output.
- Persona tuning behind a feature flag (off by default for v1; turn on after dogfood).

**Out of scope (deferred)**:
- Web standalone UI (without GitHub App). Reason: GitHub App is the wedge.
- CLI / GitHub Action. Reason: data shows demand first.
- Jira / Linear / GitLab adapters. Reason: GitHub is 80% of target market.
- Hosted inference. Reason: SOC2 lift not justified pre-product-market-fit.
- Mobile editor. Reason: desktop release-manager workflow only.
- Custom-section editing in the web editor. Reason: structured-only is the differentiator.
- Multi-repo aggregated changelogs. Reason: per-repo is the unit users think in.
