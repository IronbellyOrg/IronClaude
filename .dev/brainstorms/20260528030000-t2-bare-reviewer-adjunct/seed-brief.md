---
topic: "Incorporate 2-4 parallel 'bare reviewer' agents into SuperClaude review-style pipelines (troubleshoot, reflect, auggie-review, code-review, adversarial). Models settable via env vars T2Model01..T2Model04 with defaults deepseek-v4-pro / qwen3.6-plus / kimi-k2.6 / glm-5.1. Output to per-reviewer .md files in a compressed-markdown template; feed into /sc:adversarial --compare --merge with explicit hallucination-suspect framing requiring rigorous validation before any claim is taken seriously."
domain: architecture
strategy: systematic
depth: standard
proposals_target: 0  # spec-direct-write; adversarial wave skipped
handoff_target: none
created: 2026-05-28T03:00:30Z
deviation: "Wave 3 adversarial skipped. User explicitly asked to 'prepare a spec' with concrete directives. Generating variants of a spec written from concrete directives would re-create ambiguity, not resolve it. Confirmed user intent via AskUserQuestion on three load-bearing ambiguities; baked answers into the spec."
---

# Seed Brief — T2 Bare-Reviewer Adjunct

## Problem Statement

The /sc:reflect ↔ bare-review comparison run in the prior session (story 7.8, 2026-05-28 00:50) produced an empirical finding: a structured reviewer (Reflect, grounded in /sc:reflect protocol) and an unstructured "bare" reviewer (no protocol scaffolding, just `Review {target}.`) generate *complementary* signal classes.

- Structured reviewer wins on grounded correctness, AC coverage, completion-verdict, evidence-citation
- Bare reviewer wins on edge-case yield, latent-risk surfacing, dismissed-findings transparency
- The merged report incorporated 8 grafts from the bare review that the structured pass missed entirely

But the bare reviewer is also where hallucinations land: its load-bearing premise in the 7.8 run was wrong ("Diff Scope: Story file review, no implementation diff" — contradicted by on-disk reality). One of its patches (P4 — add `{motd}` to AC #5 table) was moot. Several others (P5, P6) were spec-polish noise.

Net: the bare-reviewer angle is *valuable* but *poisonous if trusted without validation*. The current workflow runs bare-review manually per call. The user wants this generalized into pipeline infrastructure with first-class "suspect" tagging that flows through to validation gates.

## Known Context

- The prior 7.8 experiment used two reviewers (one structured, one bare), both Anthropic-model agents
- The user wants to scale to 2-4 parallel bare reviewers, each on a *different non-Anthropic model* (DeepSeek, Qwen, Kimi, GLM)
- Model diversity is the diversification mechanism — different training distributions → different hallucination patterns → cross-model agreement is a stronger signal than within-model agreement
- /sc:adversarial is the merge engine; it already has an evidence-validator, scoring matrix, Round 2.5 invariant probe, and provenance annotation system — extending it for SUSPECT-source treatment is cheaper than building a parallel validator
- Existing brainstorm artifacts in `.dev/brainstorms/` follow a house style: seed-brief + merged-requirements + adversarial/ + return-contract.yaml

## Confirmed Decisions (via AskUserQuestion, 2026-05-28)

1. **Scope:** Standalone skill `sc-bare-review`, wired into multiple commands (troubleshoot, reflect, auggie-review, code-review, adversarial). NOT troubleshoot-only.
2. **Transport:** OpenAI-compatible proxy / LiteLLM-style router. Cross-vendor models invoked via a single HTTP endpoint with bearer auth.
3. **Validation gate location:** Inside /sc:adversarial as a tagged-input mode. Bare outputs carry `suspect: true`; adversarial's evidence-validator demotes unverified suspect claims.

## Constraints

- Must NOT break existing /sc:adversarial Mode A / Mode B / Pipeline Mode contracts (additive only)
- Must be controllable from caller side via a single flag (`--bare-reviewers N` where N ∈ {0, 2, 3, 4})
- Must fail-soft when env vars are unset (clear STOP message, no silent partial)
- Must fail-soft when fewer than N reviewers succeed (continue with whatever landed if ≥2; status=partial if 1, failed if 0)
- Compressed-markdown output template is mandatory — heterogeneous output from different vendor models must be normalized to a single consumable shape
- T2 models are explicitly external/non-Anthropic — no alias-routing to Anthropic models permitted

## Success Criteria

- Any /sc:troubleshoot, /sc:reflect, /sc:auggie-review, /sc:code-review, or /sc:adversarial invocation can request bare-reviewer adjunct via a single flag
- Per-reviewer output files land in a predictable location with the compressed template
- /sc:adversarial accepts suspect-tagged sources and applies validation-gated incorporation
- Merged output carries provenance annotations distinguishing T1 (structured/grounded) from T2 (bare/suspect) source claims, with validator verdict per T2 claim
- Adding/swapping a T2 model is a one-line env-var change — no skill/agent file edits

## Open Questions (deferred to implementation)

- Should the proxy adapter be implemented as a Bash+curl shell-out, an MCP server, or both? Spec lands on "transport-agnostic contract; reference implementation = Bash+curl"
- Should the T2 model count map 1:1 to env vars (T2Model01..T2Model04 only), or extend to T2Model01..T2ModelNN for arbitrary scaling? Spec lands on 1..4 cap (user asked for 2-4)
- Should there be a "T2 lite" mode that uses cheaper models for fast triage? Out of scope for v1
- Should the suspect-source-audit artifact be a separate file or a section in debate-transcript.md? Spec lands on separate file: `adversarial/suspect-source-audit.md`
- Should bare reviewers receive the target as inline content or as a file path? Inline only — proxy models don't have filesystem access

## Domain & Strategy Classification

- **Domain:** architecture (cross-cutting design change affecting one new skill, one extension to existing skill, and ≥5 caller commands)
- **Strategy:** systematic (clear sequential dependency: skill → adversarial extension → caller plumbing → validator hardening → docs)
- **Depth:** standard (the design space is well-bounded by user directives; deep adversarial debate not needed)
