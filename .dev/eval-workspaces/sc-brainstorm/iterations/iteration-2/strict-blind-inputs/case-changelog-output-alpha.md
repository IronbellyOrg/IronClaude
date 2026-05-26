---
spec_type: requirements
source: seed-brief.md
domain: product
strategy: agile
depth: standard
adversarial_status: pass
convergence_score: 0.78
proposal_count: 3
personas: [architect, frontend, scribe]
created: 2026-05-25T00:00:00Z
---

# Merged Requirements: AI-Powered Changelog Summarizer (MVP)

## Problem Statement

Release managers and engineering leads at mid-market SaaS companies (50–500 engineers) spend 30–90 minutes per release converting raw git PRs, commits, and ticket references into a customer-readable changelog. The work is repetitive, format-inconsistent, error-prone, and delays release announcements by half a day or more. Existing tools either solve only the per-PR step (What The Diff), require heavy editorial workflow without an explicit trust contract (Release.com, GitButler), or aren't AI-powered at all (GitHub's native release notes — the inherently-trustworthy floor). There is a wedge for a tool that combines themed grouping, persona tuning, BYO-key privacy, inline cost transparency, and — **load-bearing** — an explicit, documented, enforceable **trust contract** (per-claim citations, breaking-change corroboration, pre-LLM redaction layer, and immutable audit log with version-controlled decision records) so release managers can publish AI-generated copy externally without painful line-by-line verification AND get the tool approved by their security review.

## User Personas

1. **Release Manager (primary)** — engineering lead or release coordinator at a 50–500-engineer SaaS company. JTBD: "When I cut a release, I want a draft changelog grouped by theme and tuned to my audience, so I can publish customer-facing release notes within 5 minutes of release cut instead of 30–90 minutes." Cares about: speed, predictable format, no per-seat pricing, ability to ship without legal/privacy lift, ability to trust LLM-generated copy without line-by-line verification.

2. **Engineering Manager / VP Engineering (buyer)** — approves tools that touch customer-facing copy. JTBD: "When my release manager wants to use an AI tool to draft customer-facing changelogs, I need a documented trust contract I can hand to security and a control surface I can audit." Cares about: documented trust posture, audit log, threat model, redaction policy, BYO-key for private repos. **Buyer veto power; cannot ship to this persona without the trust contract.**

3. **Product Manager / Customer Success (downstream editor & consumer)** — edits the customer-facing copy before publish; reads it after publish to field support tickets. JTBD: "When the release manager hands me a draft, I want to retone individual entries for the audience and trust that the breaking-change calls are real." Cares about: per-entry persona retone, clarity, no internal jargon, no false breaking-change claims.

## Trust Contract

**Feature-blocking; ships in v1.** No release of the product to GA without all four components below operational.

### 1. Citation Contract

Every aggregate-output bullet MUST cite ≥1 source PR ID. A post-generation **trust validator** runs over every draft and enforces:
- Every bullet has ≥1 citation.
- Every cited PR ID resolves to a PR in the input set (rejects hallucinated PR references).
- Every breaking-change claim has a corroborating signal: a `breaking` label on the source PR, a `BREAKING:` prefix in the commit message, OR a `BREAKING CHANGE:` footer (conventional-commits).
- Validator output (`{claim_id, claim_text, citations[], breaking_corroborated, validation_status}`) lands in the audit log on every generation, pass OR fail.

**Editor surface:** every citation rendered as a clickable pill (e.g., `(#1234)`); failed-validation entries render as red pills with hover-explanation.

**Enforcement mode:** controlled per-repo via `strict_trust: true | false` config (default `false`; auto-set `true` when redaction patterns with `severity: block` are configured). When `strict_trust: true`, publish is hard-blocked on any red-pill entry. When `false`, publish is nudge-only and the audit log records `published_with_overrides: [...]`.

### 2. Redaction Contract

A configurable regex + named-entity-recognition pass operates on `ChangeRecord` fields (PR titles, descriptions, commit messages) **BEFORE any LLM call**. Pluggable matchers: regex, deny-list, NER entity types, built-in secret matchers (AWS keys, GitHub tokens, generic high-entropy strings).

**Per-pattern severity:** `block` (refuses generation if matched), `redact` (replaces with placeholder), `flag` (logs but passes through).

**Configuration surfaces** (both write to the same canonical config):
- `.changelog/redaction.yaml` in the user's repo (version-controlled, code-adjacent).
- Web editor settings page (for users who don't want config-in-repo).

**Logging:** redaction events log `{pattern_id, severity, redacted_token_count, source_field}` only — never the raw redacted content.

### 3. Audit Log Contract

Append-only, immutable event store. Records every generation, redaction, validator-rejection, publish, and override.

**Event fields per generation:** `{generation_id, user_id, repo_id, release_range, model_name, model_version, prompt_hash, input_pr_set_hash, redactions_applied_count, draft_content_hash, cost_usd, validator_pass, validator_failures[]}`.

**Event fields per publish:** `{generation_id, published_content_hash, final_vs_draft_line_diff_pct, published_with_overrides[]}`.

**Retention:** 13 months minimum.

**Export API:** documented `audit_log_export` endpoint emits CSV + JSONL for compliance handoff.

### 4. Decision-Record Artifact

Every changelog **publish** writes a Markdown decision record to `.changelog/decisions/{release_id}.md` in the user's repo (PR-able, version-controlled). The decision record captures: who published, when, model + prompt hash, input PR-set hash, redactions count, final-vs-draft delta, any overrides. **This is the document the security team reads.** Plain Markdown; survives deprecation of the hosted audit-log service.

## Functional Requirements

1. **GitHub App integration** — install per-repo via GitHub App OAuth; subscribe to release-creation events; auto-post a draft changelog as a comment on the new GitHub release within 60 seconds of release creation. (Provenance: all 3 proposals — convergence.)

2. **Two-pass LLM pipeline** — (a) per-PR structured extraction using a cheap model (Haiku-class) emitting JSON `{type, scope, summary, customer_visible, breaking, source_pr_id, supporting_signals[]}`; (b) aggregate themed-narrative pass using a stronger model (Sonnet-class) over validated extractions. Failed per-PR extractions retry once then fall back to PR title verbatim with `validation_status: extraction_fallback`. (Provenance: architect proposal-1 pipeline section.)

3. **Themed grouping in output** — drafts MUST group entries into at least three themes — Features, Fixes, Breaking/Deprecations. Entries marked `customer_visible: false` excluded from the customer-facing draft. (Provenance: convergence.)

4. **Web editor with three-column theme view** — drag-to-regroup between themes (keyboard-accessible: arrow + space-bar), per-entry retone button (developer / business / executive — per-entry, not global), per-entry exclude toggle, inline citation pills, live Markdown preview with diff-vs-draft toggle, "Publish to GitHub release" terminal action. (Provenance: frontend proposal-2 editor section.)

5. **BYO-key flow only in v1** — user pastes Anthropic or OpenAI API key during onboarding; key stored encrypted per-repo; all inference proxied. Hosted inference deferred until ≥5 enterprise prospects ask OR BYO-key onboarding drop-off >30%. (Provenance: architect+scribe; debate Tension 2.)

6. **Provider abstraction** — `LLMProvider` interface admits Anthropic + OpenAI in MVP; sealed in v1 so additional providers (including future hosted-inference) drop in without re-architecting. (Provenance: architect proposal-1.)

7. **Trust validator + audit log + decision-record writeback** — see Trust Contract section above. Validator runs on every generation; audit log writes on every event; decision-record writes on every publish. (Provenance: scribe proposal-3, with architect+frontend compromises.)

8. **Redaction layer pre-LLM** — see Trust Contract section above. Configurable via `.changelog/redaction.yaml` AND web editor settings; same canonical config. (Provenance: scribe + architect.)

9. **Cost telemetry** — every generated draft shows token counts + dollar cost (computed from user's vendor pricing), surfaced inline in the GitHub comment AND as a status-bar element in the web editor. Pre-flight cost-ceiling check rejects generation if estimate exceeds user-configured budget. (Provenance: architect proposal-1 + convergence.)

10. **Persona tuning (per-entry retone), behind feature flag** — developer / business / executive tones, applied per-entry. Feature flag `personas_enabled: false` default for new installs, on for dogfood. Trust validator + audit log apply to retoned output. (Provenance: frontend proposal-2 + scribe compromise on Tension 4.)

## Non-Functional Requirements

1. **Performance** — draft generation completes in ≤60 seconds for a release with up to 50 PRs; web editor first-paint ≤2 seconds; per-entry retone LLM call returns in ≤3 seconds. (Architect.)

2. **Cost ceiling** — typical 50-PR release MUST cost ≤$1 in vendor inference fees (achieved via two-pass split + prompt caching on system prompt across per-PR calls). p95 cost-per-release ≤$0.75. (Architect.)

3. **Privacy** — BYO-key required for private repos; per-repo opt-in toggle for any third-party inference; redaction layer required on all repos; no PR content stored beyond 7 days post-generation (audit log retains only hashes). (Scribe + architect.)

4. **Accessibility** — web editor MUST support full keyboard navigation including drag-and-drop (arrow + space-bar pick/drop), screen-reader labels on theme columns and per-entry actions, WCAG 2.1 AA on color contrast and focus indicators, axe-core CI gate. (Frontend proposal-2.)

5. **Reliability** — extraction-pass failures degrade gracefully (PR-title fallback) rather than blocking the aggregate pass; the GitHub comment always lands even if some entries are stubs; validator-failed entries are surfaced with red pills, not dropped. (All three personas.)

6. **Audit integrity** — append-only audit log, 13-month minimum retention, exportable to CSV + JSONL. Decision-record Markdown writeback per publish. (Scribe proposal-3.)

## Acceptance Criteria

1. A release manager installs the GitHub App, completes BYO-key + redaction-pattern onboarding, and receives a draft on a real release in under 10 minutes end-to-end. (Provenance: frontend onboarding.)

2. Draft generation for a 50-PR release completes in ≤60 seconds and costs ≤$1 in inference fees, measured + asserted by integration tests against vendor-pricing fixtures. (Architect performance + cost.)

3. Across a 10-release sample of dogfooded internal releases, ≥70% of finalized changelogs ship with ≤30% line-diff from the AI-generated draft. (Convergence success metric.)

4. **Trust validator AC** — across the dogfood 10-release sample, every published changelog has: 100% of bullets carry ≥1 citation; 100% of cited PR IDs resolve to the input set; 0 false-positive breaking claims (independently verified). Validator-failure rate ≤10% pre-edit. (Scribe trust contract.)

5. **Redaction layer AC** — a test corpus of 100 synthetic PR bodies (containing secrets, embargoed feature names, customer-CRM tokens) is processed; redaction layer catches 100% of `block`-severity matches and ≥95% of `redact`-severity matches. No raw redacted content appears in any LLM-vendor call (verified by network-mock integration test). (Scribe redaction.)

6. **Audit log + decision-record AC** — every dogfood publish produces both an audit-log event (with all required fields populated) AND a Markdown decision record committed to `.changelog/decisions/`. Audit log export API emits CSV + JSONL with no field loss. (Scribe.)

7. Web editor passes WCAG 2.1 AA automated checks (axe-core) and keyboard-only user-journey test (install → edit → publish without mouse). (Frontend.)

8. Private-repo enforcement: attempting to generate a draft on a private repo without a configured BYO-key returns a clear actionable error AND does not transmit any PR content to any LLM vendor (verified by network-mock integration test). (Architect + scribe.)

## Success Metrics

1. **Weekly active release managers (north-star)** — ≥10 distinct release managers actively generating drafts weekly within 8 weeks of GA.

2. **Draft-shipped-without-rewrite rate** — ≥70% of finalized changelogs ship with ≤30% line-diff from draft (per AC #3).

3. **Cost-per-release p95** — ≤$0.75 at p95 across all generated drafts.

4. **Trust contract integrity** — zero confirmed incidents of hallucinated breaking-change claims AND zero confirmed incidents of redaction-layer bypass in the first 90 days post-GA. (Scribe trust contract.)

5. **Buyer-approval rate** — ≥60% of release-manager installs result in a buyer (eng manager / VP Eng) approving the tool for ongoing use within 30 days, measured by `decision-record commits > 1`. (Scribe — buyer-veto consideration.)

## MVP Scope

**In scope:**
- GitHub App with auto-post on release creation.
- BYO-key onboarding (Anthropic + OpenAI).
- Two-pass LLM pipeline with structured extraction + themed-narrative aggregate.
- Provider abstraction (`LLMProvider` interface).
- Trust validator (citation + breaking-corroboration enforcement).
- Redaction layer (regex + deny-list + built-in secret matchers; `block | redact | flag` severities).
- Audit log (append-only, 13-month retention, export API).
- Decision-record Markdown writeback to `.changelog/decisions/`.
- Web editor: three-column theme view, drag-to-regroup, per-entry retone (3 personas behind feature flag), per-entry exclude, inline citation pills, live Markdown preview, "Publish to GitHub release."
- Cost telemetry inline + pre-flight cost-ceiling check.
- Markdown-only output.
- Per-repo `strict_trust` config (default `false`, auto-set `true` on `block`-severity patterns).
- Trust-Contract Whitepaper, Redaction Pattern Cookbook, Audit Log Schema Reference, Decision-Record Template, Threat Model — all ship in week 5 (one week post code-freeze, before GA announce).

**Out of scope (deferred):**
- Hosted inference (deferred until trigger conditions; see FR #5).
- Web standalone UI without GitHub App.
- CLI / GitHub Action (pipeline interface ready; ship when an enterprise dogfood user asks).
- Jira / Linear / GitLab adapters (`SourceAdapter` interface sealed; ship by demand).
- Mobile editor (read-only mobile view IS in scope).
- Custom-section editing (structured-only is the differentiator).
- Multi-repo aggregated changelogs.
- Persona tuning default-on (flag stays off until post-dogfood feedback).

## Risks

1. **Trust contract slows MVP by one sprint** — severity: medium. Mitigation: validator + audit log + decision-record are one sprint; documentation can run in parallel during sprints 2–3 and ship week 5 (code-freeze + 1). Per debate Tension 1 resolution.

2. **BYO-key onboarding drop-off** — severity: medium-high. Mitigation: a $0.001 test ping in onboarding to validate the key; clear copy-paste instructions per vendor; track drop-off as a leading indicator for the hosted-inference timing decision (FR #5).

3. **LLM cost overrun on large releases** (>200 PRs) — severity: medium. Mitigation: pre-flight cost estimate with user-configured budget; refuse generation if estimate exceeds budget; document "split a large release into multiple range calls."

4. **Validator false-positive rate erodes trust** — severity: medium. Mitigation: tune corroboration signals against a curated dogfood test set BEFORE GA; ship in `strict_trust: false` default so false-positives are nudges, not blocks, on most repos.

5. **Vendor LLM API changes break extraction schema** — severity: low-medium. Mitigation: provider abstraction isolates the change; schema validation retry-once-then-fallback on extraction failures (FR #2).

## Open Questions

1. **Hosted-inference upgrade timing** — when do we add hosted inference as a paid tier? Trigger: ≥5 enterprise prospects ask OR BYO-key onboarding drop-off >30%. SOC2 + DPA required.

2. **CLI / GitHub Action timing** — pipeline interface admits both. Trigger: a single enterprise dogfood user asks for CI integration.

3. **Multi-source ingestion** (Jira, Linear, GitLab) — `SourceAdapter` interface ready. Trigger: ≥3 dogfood users explicitly request a specific source.

4. **Persona tuning default-on timing** — feature flag flips when dogfood feedback shows the retone surface is well-loved AND the validator handles retoned output cleanly.

## Provenance

| Requirement | Source proposals |
|-------------|-----------------|
| FR #1 GitHub App | All 3 — convergence on Tension 3 |
| FR #2 Two-pass pipeline | Architect proposal-1 §Architecture |
| FR #3 Themed grouping | All 3 — convergence |
| FR #4 Web editor | Frontend proposal-2 §The Editor |
| FR #5 BYO-key v1 | Architect + Scribe; Tension 2 resolution |
| FR #6 Provider abstraction | Architect proposal-1 §Provider Abstraction |
| FR #7 Trust validator + audit + decisions | Scribe proposal-3 §Trust Contract |
| FR #8 Redaction layer | Scribe proposal-3 + Architect §Redaction layer |
| FR #9 Cost telemetry | Architect + convergence |
| FR #10 Persona tuning behind flag | Frontend + Scribe; Tension 4 resolution |
| Trust Contract section | Scribe proposal-3 (primary); compromises from all 3 |
| `strict_trust` per-repo toggle | Architect compromise on Tension 5 |
| Documentation deliverables week 5 | Scribe proposal-3 §Documentation; debate Tension 1 |
| AC #4 (validator), #5 (redaction), #6 (audit) | Scribe proposal-3 |
| Success Metric #4 (trust integrity), #5 (buyer approval) | Scribe — buyer-veto framing |
| Risks #1 (trust contract sprint cost) | Tension 1 |
| Risks #2 (BYO drop-off) | Tension 2 |
| MVP out-of-scope items | All 3 — convergence on what to defer |
