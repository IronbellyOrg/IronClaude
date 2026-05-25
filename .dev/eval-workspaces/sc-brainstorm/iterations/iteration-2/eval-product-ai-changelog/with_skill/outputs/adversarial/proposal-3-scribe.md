---
proposal_id: 3
persona: scribe
model: haiku
custom_instruction: "focus on documentation clarity, decision rationale, and audit trail"
stance: trust-contract-feature-blocking
created: 2026-05-25T00:00:00Z
---

# Proposal 3 — Scribe: Trust Contract as Feature-Blocking

## Stance

**No proposal-level shipping without the trust contract.** Architect treats the trust contract as a layer in the pipeline; frontend treats it as a UX pattern. **Both miss the load-bearing point: the trust contract is a *publishable document* that release managers must be able to point their security team, their PM, and their VP Engineering at, on day one, to justify using an LLM on customer-facing copy.** Without that document — and without the deterministic enforcement that the document describes being TRUE — the product cannot ship to any company larger than its founder's previous employer. Trust is not a feature; it is the price of admission for B2B SaaS dealing with external publication of AI-generated text.

## What the Trust Contract Includes

**1. Citation contract** — every aggregate-output claim cites its source PR ID(s). A post-generation validator runs over every draft and enforces:
- Every bullet carries ≥1 citation.
- Every cited PR ID is in the input set (no hallucinated PR references).
- Every breaking-change claim has a corroborating signal: a `breaking` label on the source PR, a `BREAKING:` prefix in the commit message, or a `BREAKING CHANGE:` footer.

The validator output is structured (`{claim_id, claim_text, citations[], breaking_corroborated, validation_status: ok|missing_citation|breaking_uncorroborated|cited_pr_not_in_input}`) and lands in the audit log on every generation, pass OR fail.

**2. Redaction contract** — the redaction layer is the FIRST thing that touches a PR's content, before any LLM call. Configurable via a `.changelog/redaction.yaml` file in the user's repo (per architect — agreed) AND via a settings-page UI (per frontend — agreed); both surfaces write to the same canonical config. Redaction patterns supported in MVP:
- Regex patterns (with named capture groups for the audit log).
- Deny-list literals (e.g., embargoed feature names, customer-from-CRM names).
- Built-in matchers for common secrets (AWS keys, GitHub tokens, generic high-entropy strings).
- A `severity` per pattern: `block` (refuses generation if matched), `redact` (replaces with a placeholder), `flag` (logs but passes through — for things we want to know about but not block on).

Redaction events log `{pattern_id, severity, redacted_token_count, source_field}` — never the raw redacted content.

**3. Audit log contract** — append-only, immutable. Every generation, redaction, publish, override, and validator-rejection writes an event. The event store is queryable via a documented `audit_log_export` API (CSV + JSONL) so the release manager can hand the security team a file. Audit log retention: 13 months minimum (one year for typical compliance + a 30-day buffer).

**4. Decision-record artifact** — every changelog publish writes a Markdown decision-record into a `.changelog/decisions/` directory in the user's repo (PR-able). The decision record captures: who published, when, which model + prompt hash, input PR-set hash, redactions-applied count, final-vs-draft delta, and any overrides. **This is the document the security team reads.** It is plain Markdown, lives in version control, and survives the eventual deprecation of our hosted audit-log service.

## Disagreement With Other Personas

**Frontend's "nudge, don't block":** disagree for repos with embargoed-content patterns or for breaking-change claims on customer-facing repos. **Compromise:** the `block | redact | flag` severity is per-redaction-pattern AND per-repo `strict_trust: true | false`. Default for new installs: `strict_trust: false` + breaking-uncorroborated = `flag`. Repos with embargoed-content patterns: `strict_trust: true` auto-set + breaking-uncorroborated = `block`. This gives the frontend's editorial fluency on most repos and the scribe's hard-block on the repos that actually need it.

**Architect's "audit log as backend layer":** the audit log MUST be a *first-class product surface*, not a SQLite table the user can't see. The export API and the `.changelog/decisions/` Markdown writeback are the user-visible surfaces. Otherwise the audit log is a compliance theatre, not a real trust signal.

**Frontend's "audit log invisible in v1":** disagree. The audit log doesn't need to be on every draft, but the `.changelog/decisions/` writeback MUST exist v1, AND the editor MUST surface a "view audit trail for this draft" link in the publish-confirmation modal. The release manager sees it once per publish, the security team can see all of them; neither is in the day-to-day flow.

## Documentation Deliverables (MVP)

Doc deliverables are not "fast follow." They block GA:

1. **Trust-Contract Whitepaper** (≤8 pages) — describes the citation contract, redaction contract, audit log contract, decision-record artifact, and exact validator behavior. This is the document a customer's security review will ask for.
2. **Redaction Pattern Cookbook** — 12+ recipes (secrets, customer-names-from-CRM, embargoed-feature codenames, internal-team-names, customer-instance-ids, signed-NDAs, etc.) with copy-paste regex.
3. **Audit Log Schema Reference** — event types, fields, retention policy, export format. Versioned (`audit_log_schema_version: 1`).
4. **Decision-Record Template** — the canonical Markdown format for `.changelog/decisions/{release_id}.md`.
5. **Threat Model** — explicit "what we defend against, what we do not" doc. Defend: hallucinated PR references, hallucinated breaking-change claims, leaking secrets to LLM vendor logs, leaking embargoed feature names. Do NOT defend (out of scope, called out): malicious user with valid credentials, vendor-side data retention beyond their published policy.

## Why This Wins

The product cannot be sold to a 200-engineer SaaS company without a published trust contract; the trust contract cannot be retrofitted without re-architecting the pipeline. Make it feature-blocking in v1; the cost is one sprint of documentation + one validator pass + one decision-record writeback. The benefit is the difference between "demo-only" and "buyable."
