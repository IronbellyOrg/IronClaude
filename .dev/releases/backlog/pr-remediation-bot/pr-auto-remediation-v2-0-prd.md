---
id: "PR-AUTO-REMEDIATION-V2-PRD-CORE"
title: "PR Auto-Remediation V2.0 (Mention-Triggered Headless Bot) - Product Requirements Document (PRD)"
description: "Foundational product requirements, user stories, security architecture, and acceptance criteria for the superclaude remediate mention-triggered, headless, on-prem PR auto-remediation bot"
version: "1.0"
status: "🟡 Draft"
type: "📋 Product Requirements"
priority: "🔥 Highest"
created_date: "2026-06-11"
updated_date: "2026-06-11"
assigned_to: "product-team"
autogen: false
autogen_method: "synthesis-assembly"
coordinator: "product-manager"
parent_task: ""
depends_on:
- "V2.0 Merged-Requirements Spec (.dev/brainstorms/20260611-005638-pr-remediation-v2-mention-bot/merged-requirements.md)"
- "V1.0 pr_submit/ decision core (src/superclaude/pr_submit/)"
related_docs:
- "V1.0 Predecessor Spec (.dev/brainstorms/20260610-234750-pr-review-auto-remediation/merged-requirements.md)"
- "sc-auggie-review-protocol severity rubric"
tags:
- prd
- requirements
- product-core
- user-stories
- acceptance-criteria
- pr-auto-remediation
- prompt-injection
- on-prem
template_schema_doc: ".claude/templates/workflow/05_prd_template.md"
estimation: ""
sprint: ""
due_date: ""
start_date: ""
completion_date: ""
blocker_reason: ""
ai_model: ""
model_settings: ""
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
task_type: "static"
---

# PR Auto-Remediation V2.0 (Mention-Triggered Headless Bot) - Product Requirements Document (PRD)

> **WHAT:** Foundational product requirements, security architecture, user stories, and acceptance criteria for the `superclaude remediate` mention-triggered, headless, on-prem PR auto-remediation bot.
> **WHY:** Serves as the single source of truth for product scope, the split Dispatcher/Runner safety architecture, autonomy/loop-safety invariants, and success criteria for a feature that lets an authorized `@bot` mention safely remediate a review comment without leaking secrets or pushing unauthorized code.
> **HOW TO USE:** Product, engineering, and security teams reference this PRD throughout the development lifecycle; it feeds the downstream TDD and the §21.3 probe-first build sequence.

### Document Lifecycle Position

| Phase | Document | Ownership | Status |
|-------|----------|-----------|--------|
| **Requirements** | **This PRD** | **Product** | **🟡 Draft** |
| Design | TDD | Engineering | Not started |
| Implementation | Tech Reference | Engineering | Not started |

### Tiered Usage

| Tier | When to Use | Sections to Skip |
|------|-------------|------------------|
| **Lightweight** | Single-feature PRD, <10 sections | Value Proposition Canvas, Customer Journey Map, API Contract Examples, Appendices, Document History (first version) |
| **Standard** | Multi-feature product, most PRDs | None — complete all sections |
| **Heavyweight** | Platform PRD, 28 sections, cross-team | None — complete all sections, add additional appendices as needed |

> **Note:** This is a **feature/component PRD** documented at Standard/Heavyweight depth because the security architecture (split-host secret separation, prompt-injection containment, autonomy lattice) warrants the full section set even though the feature is a component of the SuperClaude / IronClaude framework rather than a standalone product.

---

## Document Information

| Field | Value |
|-------|-------|
| **Product Name** | PR Auto-Remediation V2.0 (Mention-Triggered Headless Bot) — `superclaude remediate` |
| **Product Type** | Feature/Component PRD (capability of the SuperClaude / IronClaude framework) |
| **Product Owner** | [TBD — product-team] |
| **Engineering Lead** | [TBD] |
| **Design Lead** | N/A (no GUI/web surface; control surface is a `@bot` comment grammar) |
| **Maintained By** | product-team (coordinator: product-manager) |
| **Stakeholders** | Repo maintainers / on-call reviewers, Platform/DevOps operators, Security/Governance engineers |
| **Status** | 🟡 Draft |
| **Target Release** | TBD (external anchor: EU AI Act high-risk deadline, August 2026) |
| **Last Verified** | 2026-06-11 against current source (`cli/remediate/` confirmed greenfield; reuse anchors code-verified) |

### Document Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Manager | [TBD] | __________ | [Date] |
| Engineering Lead | [TBD] | __________ | [Date] |
| Security Lead | [TBD] | __________ | [Date] |
| Executive Sponsor | [TBD] | __________ | [Date] |

---

## Completeness Status

**Completeness Checklist:**

- [x] Section 1: Executive Summary — **Complete**
- [x] Sections 2-5: Problem, Background, Vision, Business Context — **Complete**
- [x] Sections 6-9: JTBD, Personas, Value Proposition, Competitive Analysis — **Complete**
- [x] Sections 10-13: Assumptions, Dependencies, Scope, Open Questions — **Complete**
- [x] Sections 14-15: Technical Requirements, Technology Stack — **Complete**
- [x] Sections 16-18: UX, Legal/Compliance, Business Requirements — **Complete**
- [x] Sections 19-20: Success Metrics, Risk Analysis — **Complete**
- [x] Section 21: Implementation Plan (Epics/Stories, Product Reqs, Phasing, DoD, Timeline) — **Complete**
- [x] Sections 22-25: Customer Journey, Error Handling, Design, API Contracts — **Complete**
- [x] Sections 26-28: Contributors, Related Resources, Maintenance & Ownership — **Complete**
- [ ] All links verified — **Pending (probe-locked GitHub shapes TBD)**
- [ ] Reviewed by leads — **Pending sign-off**

**Contract Table:**

| Element | Details |
|---------|---------|
| **Dependencies** | V2.0 Merged-Requirements Spec; V1.0 `pr_submit/` decision core; `ClaudeProcess` headless-spawn primitive |
| **Upstream** | Feeds from: parallel research fan-out (8 codebase-investigator passes + 3 web/market passes), V1.0 predecessor spec |
| **Downstream** | Feeds to: TDD, §21.3 probe-first build sequence, implementation tickets under `cli/remediate/` |
| **Change Impact** | Notify: Engineering, Security, QA, product-team; the in-flight V1.0 `pr_submit` build owner |
| **Review Cadence** | Quarterly + ad-hoc on any Open Decision (OD-1…OD-4) resolution |
| **Living Document** | This PRD evolves as the product learns and iterates — see Document History for change log |

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Problem Statement](#2-problem-statement)
3. [Background & Strategic Fit](#3-background--strategic-fit)
4. [Product Vision](#4-product-vision)
5. [Business Context](#5-business-context)
6. [Jobs To Be Done (JTBD)](#6-jobs-to-be-done-jtbd)
7. [User Personas](#7-user-personas)
8. [Value Proposition Canvas](#8-value-proposition-canvas)
9. [Competitive Analysis](#9-competitive-analysis)
10. [Assumptions & Constraints](#10-assumptions--constraints)
11. [Dependencies](#11-dependencies)
12. [Scope Definition](#12-scope-definition)
13. [Open Questions](#13-open-questions)
14. [Technical Requirements](#14-technical-requirements)
15. [Technology Stack](#15-technology-stack)
16. [User Experience Requirements](#16-user-experience-requirements)
17. [Legal & Compliance Requirements](#17-legal--compliance-requirements)
18. [Business Requirements](#18-business-requirements)
19. [Success Metrics & Measurement](#19-success-metrics--measurement)
20. [Risk Analysis](#20-risk-analysis)
21. [Implementation Plan](#21-implementation-plan)
22. [Customer Journey Map](#22-customer-journey-map)
23. [Error Handling & Edge Cases](#23-error-handling--edge-cases)
24. [User Interaction & Design](#24-user-interaction--design)
25. [API Contract Examples](#25-api-contract-examples)
26. [Contributors & Collaboration](#26-contributors--collaboration)
27. [Related Resources](#27-related-resources)
28. [Maintenance & Ownership](#28-maintenance--ownership)
- [Appendices](#appendices)
- [Document History](#document-history)
- [Document Provenance](#document-provenance)

---

## 1. Executive Summary

PR Auto-Remediation V2.0 is a **mention-triggered, headless, on-prem pull-request remediation bot**, shipped as a new `superclaude remediate` CLI group. An authorized collaborator replies to a PR review comment with an `@bot`-style mention (e.g. `@bot fix --depth deep`); a long-lived **Dispatcher** (systemd daemon) detects the mention, runs a live authorization gate on the *replier*, claims the trigger in an on-disk ledger, and dispatches an ephemeral, sandboxed **Runner** that runs `claude -p` against an isolated PR-head checkout. The Runner treats the parent review comment (`opComment`) as **untrusted data inside a trusted prompt envelope**, never as instructions, and by default only *proposes* a fix.

The product exists because executing an LLM agent with file-write and git-push authority in response to untrusted GitHub comment text is the dominant agentic-AI attack class of 2026 — demonstrated in the wild against the market leaders ("Comment and Control," Johns Hopkins, Apr 2026; "Clinejection," Feb 2026) and assigned multiple CVEs. The Cloud Security Alliance's prescribed "fundamental mitigation" is an **architectural separation of the agent's reasoning layer from the credential-holding execution layer** — which is a one-to-one description of V2.0's split Dispatcher/Runner host. V2.0 is the headless successor to V1.0's in-session Monitor-tool host: it reuses V1.0's tested deterministic decision core (`src/superclaude/pr_submit/` — severity routing, autonomy gating, round/budget counter, `needs_human_decision` HALT) [CODE-VERIFIED] and rebuilds only the host, the secret-scoped execution boundary, and the GitHub I/O surface.

Strategically, V2.0 occupies a documented market whitespace: the intersection of **mention-triggered PR auto-remediation** (where GitHub Copilot Coding Agent leads but is cloud-only) and **on-prem / air-gapped self-hosted deployment** (where Tabnine/Windsurf/Qodo lead but ship inline/IDE assist, not autonomous remediation bots). No incumbent occupies both axes. Its conservative propose-only default directly answers the market leader's most-complained-about failure mode (Copilot's unconditional trigger that "ignores intent").

**Key Success Metrics:**

- **Runner secret isolation (AC-7):** 0 occurrences of `GH_TOKEN` / push credential / `ANTHROPIC_*` token values in the Runner's `/proc/<pid>/environ`
- **Authorization correctness (AC-1):** 100% of triggers from non-write-collaborators rejected with a polite ack, zero remediation action taken
- **Loop safety (SC-5/SC-6):** per-PR push budget enforced — default 2, hard cap 5 — surviving daemon restarts via the disk-authoritative ledger
- **Conservative default:** `propose` is the effective autonomy level whenever no level flag is supplied; reaching `push` requires explicit flag **AND** write-permission **AND** passing validation (lattice-minimum)
- **Injection containment:** adversarial prompt-injection corpus passes as a release-blocking acceptance gate (opComment never interpolated as instructions)

---

## 2. Problem Statement

<!-- Feature/component PRD: Section 2.3 reframes "Market Opportunity" as the feature-level market unlock; full TAM/SAM/SOM lives in Section 5. -->

### 2.1 The Core Problem

**There is no safe way to let an autonomous agent act on a PR review comment when that comment is untrusted text and the agent holds file-write and git-push authority.**

- **What is the current state?** When a reviewer (human or the Augment review bot) flags an issue on a PR, a maintainer must manually context-switch back into the PR, re-derive the fix, apply it, push, reply, and resolve the thread. The V1.0 predecessor automated this only *inside a live Claude session* hosted by the in-session Monitor tool — which dies the moment the session closes (V1.0 red-team risk R3), making 24/7 unattended remediation impossible.
- **Who is affected?** Repo maintainers and on-call reviewers on the `IronbellyOrg/IronClaude` fork, and more broadly any team that wants review findings remediated without a human babysitting a terminal session — especially regulated teams that cannot send code to cloud-hosted runners.
- **What is the impact/cost of not solving this?** The naive "just run the agent on the comment" approach is actively dangerous. In 2026 a single crafted PR title / issue body / review comment caused GitHub Copilot Agent, Claude Code, **and** Gemini CLI to leak their own API keys and `GITHUB_TOKEN` into publicly visible PR comments ("Comment and Control," Johns Hopkins, Apr 2026), with zero maintainer interaction beyond the automated trigger. "Clinejection" (Feb 2026) chained an issue-title injection into a live npm supply-chain compromise. The root cause is vendor-agnostic: *"any agent given both a bash execution tool and access to secrets while ingesting untrusted comment text"* is exploitable — and *"LLMs cannot tell the difference between instructions and data"* (OpenAI CISO: prompt injection is an acknowledged unsolved problem).
- **What barriers exist today?** (1) Host longevity — an in-session host cannot run unattended. (2) Secret blast radius — the existing `ClaudeProcess.build_env()` is additive-only (`os.environ.copy()` + merge), so it **cannot strip** an inherited `GH_TOKEN` from a spawned child [CODE-VERIFIED, `cli/pipeline/process.py:145-160`]. (3) No authorization concept — V1.0 had no notion of *who* is allowed to trigger an action. (4) Trust — only ~3–33% of developers trust AI output (SonarSource 2026: 66% refuse to merge without manual review), so any bot that over-acts erodes trust and gets muted within months.

### 2.2 Why Existing Solutions Fall Short

**Cloud-hosted mention-triggered agents (GitHub Copilot Coding Agent, public `@claude` Action, Devin):**

- Run in GitHub-Actions-hosted / SaaS cloud environments — structurally unavailable to air-gapped or regulated teams that cannot send code to cloud runners (Copilot Enterprise is "cloud-dependent, not natively self-hostable"; Cursor scores 3/10 on self-hosted deployment).
- Most rely on `pull_request_target`, which **injects secrets into the runner** — the exact exposure underlying most 2026 GitHub-Actions agent CVEs.
- Copilot Coding Agent **unconditionally opens a child PR even when the comment says "don't do anything"** — "intent is ignored, no conversational mode, no middle ground" (GitHub Community Discussion #190027), the market leader's #1 documented complaint.

**Third-party review/remediation bots (CodeRabbit, Ellipsis, Qodo Merge, Greptile, Sweep):**

- Most stop at *review/suggest* and deliberately avoid taking file-write + push authority; the ones that do implement fixes foreground little-to-no untrusted-input / secret-separation story.
- Configuration lives in-repo (`.github/workflows/`, `.toml`) and runs on the cloud platform — same data-residency and supply-chain surface (tj-actions, GhostAction, trivy-action tag-poisoning).

**V1.0 in-session Monitor-tool host (`sc:pr-submit`):**

- Hosted by the in-session Monitor tool; the live session must remain open (V1.0 FR-2.4) — dies on session close (V1.0 R3), so no unattended/24-7 operation.
- Triggered by an Augment review *landing* (poll-and-detect), with no authorization gate and no notion of a third-party `@`-mention triggering action on someone else's behalf.
- Its deterministic core (`pr_submit/`) is sound and reusable, but its **host** is the precise fragility V2.0 exists to eliminate.

### 2.3 The Market Opportunity

Solving this unlocks a documented, under-served segment. "Autonomous pull request resolution" and "security vulnerability discovery and remediation" are **analyst-named emerging high-value use cases** (not yet commoditized) inside a fast-growing agentic-development market (estimates vary by scope: ~$2.99B agentic-AI-frameworks 2025 → ~$19.32B by 2031 at 36.3% CAGR; ~$10.4B agentic-dev 2025 at ~39.5% CAGR — treat *trend direction*, not the absolute figure, as the reliable signal). Within it, the **on-prem × mention-triggered-remediation intersection is empty whitespace**: cloud incumbents lead the trigger UX but cannot self-host; on-prem leaders ship inline/IDE assist, not autonomous remediation bots. A governance-first posture (live authorization gate, immutable trigger ledger, secret separation, propose-only default) is exactly what 2026 enterprise buyers name as the *gating constraint* on agent adoption — "governance-by-design as critical as innovation-by-design" — and aligns with the EU AI Act high-risk compliance deadline of **August 2026**.

---

## 3. Background & Strategic Fit

### 3.1 Why Now?

1. **The threat is real, named, and exploited (not hypothetical).** Prompt injection against tool-bearing coding agents went from theory to in-the-wild supply-chain compromise in early 2026 (Comment-and-Control, Clinejection, CVE-2025-66032, CVE-2026-22708, CVE-2026-21852). A 78-study meta-analysis found **every tested coding agent vulnerable, with adaptive attack success >85%**, and OWASP named prompt injection the #1 risk in both LLM01:2025 and the new **OWASP Top 10 for Agentic Applications (Dec 2025)**. Building remediation *without* the split-host containment is no longer defensible.
2. **The industry has converged on the exact mitigation V2.0 implements.** The CSA Labs research note prescribes separating the reasoning layer (no credentials, processes untrusted text) from the credential-holding execution layer (evaluates a structured recommendation against policy, never touches untrusted input) — independently mirrored by Simon Willison's Dual-LLM pattern, the Anthropic/ETH/DeepMind "Design Patterns for Securing LLM Agents" paper, AWS AgentCore's "never put the token in the VM," and OSS sandboxes (microsandbox, brood-box, cplt). V2.0's Dispatcher/Runner split *is* this pattern.
3. **The reusable foundation already exists in-repo.** The headless spawn primitive `ClaudeProcess` (`cli/pipeline/process.py:72`) is verified — stdin prompt delivery bypassing the 128 KB argv limit, a 16 MiB pre-spawn guard, process-group kill, lifecycle hooks [CODE-VERIFIED]. V1.0's deterministic decision core (`pr_submit/` — `fsm.evaluate_push_decision`, `should_halt_rounds` with `DEFAULT_MAX_ROUNDS=2`/`HARD_CAP_MAX_ROUNDS=5`, `severity_router`, `DetectionContractLocked`) is built and tested [CODE-VERIFIED]. The severity rubric (`sc-auggie-review-protocol/refs/severity-rubric.md`) and the `gh` posting precedent are in place. The host is the only large greenfield surface — meaning the riskiest *logic* is already paid down.
4. **The market gap and the compliance clock are open simultaneously.** No incumbent occupies the on-prem × mention-triggered-remediation intersection; the most-adopted tools (Cursor 67% Fortune 500) score *lowest* on self-hosted deployment and enterprise governance. The EU AI Act high-risk deadline (Aug 2026) and NIST AI RMF / ISO 42001 referencing prompt-injection controls make a governed, auditable, self-hosted posture a near-term procurement requirement, not a future nicety.

### 3.2 How This Fits Company / Framework Objectives

- **Mission Alignment:** Extends the SuperClaude framework's existing operator-automation surface (`sprint`, `swarm`, `roadmap`, `pipeline` all wrap `ClaudeProcess`) with a 24/7 unattended remediation capability, while honoring the framework's hard invariants — fork-only `--repo IronbellyOrg/IronClaude` targeting, SoT/sync-dev discipline, and human-owned merge state.
- **Reuse / Cost Posture:** The build is "a mostly-new subsystem with a few sturdy anchors": reuse the V1.0 pure decision core and `ClaudeProcess`, build new only the I/O + host layer V1.0 deliberately externalized. This avoids duplicating ~3 tested modules of decision logic and prevents divergent severity grading between the `sc:pr-submit` skill and the daemon.
- **Market Position:** Targets the explicitly under-served governed/on-prem segment (~29% of the agentic-frameworks market by share, the security-driven minority) where cloud incumbents structurally cannot follow.
- **Competitive Moat:** The split-host secret-separation architecture is a credibility moat backed by named 2026 CVEs — "same `@mention` UX as `@claude`/Copilot, but architected so a malicious comment can't exfiltrate secrets or push unauthorized code."

### 3.3 Strategic Bets

1. **Architecture-as-mitigation beats guardrails.** Bet: because detection/prompting demonstrably *reduce but never eliminate* injection (>85% adaptive success), the durable defense is structural — secret separation + ephemeral sandbox + propose-only + external authorization — not a better filter. The whole split-host design rests on this.
2. **Conservative-by-default wins the trust deficit.** Bet: in a market with 84% adoption but ~3–33% trust, a bot that proposes and lets a human/authorization gate decide will be adopted and retained where auto-acting bots get muted. Reaching `push` must require explicit flag + write-permission + passing validation (lattice-minimum), and `propose` is the no-flag default.
3. **On-prem headless is a defensible niche, not a feature checkbox.** Bet: the unserved intersection of mention-triggered remediation and self-hostable deployment is large enough (regulated defense/finance/healthcare/gov/telecom) to justify the operational cost of a systemd daemon + sandbox over a cloud Action.
4. **The trigger model is the real novelty; the decision core is shared.** Bet: V2.0's genuine new surface is the mention grammar + parent resolution, live per-trigger authorization, the split host + sandbox, host-side short-lived-token push, and reply/resolve — while autonomy/round/severity/HALT logic is inherited from `pr_submit`. Mis-scoping this (rebuilding the core) would be the project's biggest avoidable cost and an SoT-duplication risk.

---

## 4. Product Vision

**"Any review comment can be safely remediated by an authorized mention — fixed, pushed, replied to, and resolved by a headless bot that treats every comment as untrusted and can never be talked into leaking a secret or pushing unauthorized code."**

When V2.0 succeeds, a maintainer on the `IronbellyOrg/IronClaude` fork no longer babysits a Claude session to act on review findings. They (or any write-collaborator) simply reply to a flagged comment with `@bot fix --depth deep`, and a 24/7 systemd-hosted Dispatcher takes it from there: it verifies the *replier* is authorized, claims the trigger exactly once in a durable ledger, hands the untrusted parent comment to an ephemeral sandboxed Runner as data-in-an-envelope, validates the result, and — only when the autonomy lattice, write-permission, and validation all permit — pushes host-side with a short-lived token, replies with the summary and SHA, and resolves the thread. By default it proposes; it never modifies merge state; humans still merge.

The end state is a governed, auditable remediation control plane that an independent security research body would recognize as the prescribed "fundamental mitigation" for the dominant agentic-AI threat of the era — delivered on-prem, where the cloud incumbents cannot go, and built into the SuperClaude CLI rather than bolted on. Every trigger, every authorization decision, and every exact opComment input is recorded in an immutable ledger, turning provenance and audit from internal plumbing into a first-class, queryable feature that answers the market's loudest demand: *show me what the agent did, why, and on whose authority.*

---

## 5. Business Context

> **Scope note:** PR Auto-Remediation V2.0 is a **feature/component** of the SuperClaude /
> IronClaude framework, delivered as a self-hosted `superclaude remediate` CLI group + systemd
> service — not a commercially-sold SaaS product. There is no standalone pricing or ARR model.
> The market sizing below is **category context** (it sizes the AI-code-remediation space the
> feature competes in), not a revenue forecast for this feature. All KPIs are owned by
> **Section 19 (Success Metrics & Measurement)** — this section forward-references them and does
> not duplicate targets.

### 5.1 Why This Feature Matters to the Business

**The strategic bet:** the SuperClaude framework already automates the *review* side of the PR
loop (the `sc:auggie-review` protocol posts severity-graded findings via `gh`). PR
Auto-Remediation V2.0 closes the loop — turning a flagged review comment into a proposed (or,
at higher authority, applied) fix — **without requiring a live Claude Code session to stay open**.
This is the explicit reason V2.0 exists: V1.0 hosted the monitor inside an in-session Monitor
tool that "dies on session close" (V1 Red-Team R3); V2.0 re-hosts it as a headless systemd
daemon so remediation survives session and machine restarts [CODE-VERIFIED: agents 1, 3, 5].

**Three business-level justifications, each grounded in the 2026 market record:**

| Justification | Evidence | Source |
|---------------|----------|--------|
| **Neutralizes the dominant agentic-AI attack class of 2026.** Running an LLM agent with file-write + git-push authority on untrusted PR comment text is *exactly* the precondition that produced real CVEs and in-the-wild exploits. The split Dispatcher/Runner design is the architecture an independent research body prescribes as "the fundamental mitigation." | "Comment and Control" (JHU, Apr 2026) hijacked Claude Code, Gemini CLI **and** GitHub Copilot Agent via PR/issue comments into leaking `ANTHROPIC_API_KEY`/`GITHUB_TOKEN`; "Clinejection" (Feb 2026) chained an issue-title injection into a live npm supply-chain compromise. CSA Labs: *"separate the reasoning layer … from the credential-holding execution layer."* | web-01 §3.1–3.2, web-02 §2, web-03 §2.2 |
| **Answers the market leader's #1 documented complaint.** GitHub Copilot Coding Agent (GA Sep 2025) unconditionally opens a child PR even when the comment says "don't" — "intent ignored, no middle ground." A conservative propose-only default + live authorization gate is the confirmation step users explicitly ask for. | GitHub Community Discussion #190027 | web-01 §1.2 |
| **Occupies open whitespace: on-prem × mention-triggered remediation.** Cloud incumbents (Copilot, Amazon Q, Cursor) cannot be self-hosted; on-prem leaders (Tabnine, Windsurf, Qodo) ship inline/IDE assist, not autonomous PR-remediation bots. No incumbent occupies both axes. | Copilot Enterprise "cloud-dependent"; Cursor 3/10 self-host; Mordor: self-hosted ≈29% of market, explicitly under-served | web-01 §2.2, §4.4; web-03 §4.2 |

**Cost drivers (feature-specific, for platform-level usage accounting):**

- **LLM token consumption** — each trigger spawns a `claude -p` Runner (`ClaudeProcess`, default
  `max_turns=100`; build sets `propose≈30 / fix≈60`) [CODE-VERIFIED: agents 7, 8].
- **Sandbox compute** — one ephemeral, disposable PR-head checkout + isolated runtime per trigger
  (greenfield; OD-1 container-vs-microVM decision is unresolved) [CODE-VERIFIED greenfield: agents 4, 5, 8].
- **Bounded by design** — a per-PR push budget (default 2, hard cap 5) and a poll floor (≥30s)
  cap runaway spend [CODE-VERIFIED: `pr_submit/fsm.py` `DEFAULT_MAX_ROUNDS=2`, `HARD_CAP_MAX_ROUNDS=5`, `MIN_POLL_INTERVAL=30`, agents 4, 6].

### 5.2 Market Opportunity (Category Context)

> ⚠️ **Reliability caveat (carried from web-01 §4.1):** AI-coding market figures diverge **100×+**
> by analyst scope. Treat **trend direction and the named use case** as the reliable signal, never
> a single headline dollar figure.

| Market | Size | Notes |
|--------|------|-------|
| **Total Addressable Market (TAM)** — agentic / AI-code tooling | Agentic AI frameworks: **$2.99B (2025) → $19.32B (2031), 36.3% CAGR** (Mordor); AI code tools: **$4.3B (2023) → $12.6B (2028), 24% CAGR** (MarketsandMarkets); broader agentic-dev: **$10.4B (2025), ~39.5% CAGR** (marketintelo) | Fast-growing; estimates vary by scope. 84% developer adoption; PR-stage AI is operational infrastructure, not experiment (web-01 §4, web-03 §4.1) |
| **Serviceable Addressable Market (SAM)** — self-hosted / governed agentic coding | **≈29% of the market is self-hosted/on-prem** (Mordor: cloud-hosted held 71.3% in 2025) — the explicitly under-served, security-driven segment | Regulated sectors named: defense, government, finance, healthcare, telecom — structurally locked out of cloud-only incumbents (web-01 §2.2, web-03 §4.2) |
| **Serviceable Obtainable Market (SOM)** — mention-triggered PR auto-remediation, on-prem | **No dollar figure — internal/framework-scoped.** Initial target = the `IronbellyOrg/IronClaude` fork + SuperClaude self-hosted users needing autonomous remediation | "Autonomous pull request resolution + security vulnerability remediation" is an **analyst-named emerging high-value use case**, not yet commoditized (web-01 §4.2) |

### 5.3 Business Objectives

> This feature has **no commercial revenue model** (internal/self-hosted capability). The
> template's ARR-style objectives are reframed as strategic/capability objectives.

1. **Close the review→remediation loop** safely: deliver a headless bot that converts an
   authorized `@bot` reply into a proposed fix, surviving session/machine restarts (the core V2.0
   bet over V1.0's session-bound host) [CODE-VERIFIED lineage: agents 1, 3].
2. **Establish governance-by-construction** as the differentiator: secret separation, live
   per-trigger authorization, immutable trigger ledger, and propose-only default — the controls
   NIST AI RMF / ISO 42001 / OWASP now reference as table-stakes (web-02 §2.4, web-03 §4.3).
3. **Own the on-prem × mention-triggered intersection** — the documented market whitespace
   (web-01 §2.2).
4. **Harden a previously prose-only safety rule into code**: the fork-only
   `--repo IronbellyOrg/IronClaude` invariant (H5) becomes the *first* machine-enforced GitHub
   target guard — today it lives only in CLAUDE.md prose and has previously failed (PR mis-routed
   to upstream) [CODE-VERIFIED: agents 3, 4, 5, 6].

**Capability Milestones (replacing revenue milestones):**

- **Phase 1:** propose-only Runner behind the probe-gated GitHub-I/O surface and the live authz gate.
- **Phase 2:** host-side push (`fix`/`push` autonomy) with short-lived tokens + per-PR push budget.
- **Phase 3:** thread reply + GraphQL resolve (`resolve` autonomy) — the highest-novelty surface.

### 5.4 Key Performance Indicators (KPIs)

> **KPIs are owned by Section 19 (Success Metrics & Measurement).** To avoid drift, this section
> does not restate targets. The category-level success signals the design is measured against:

| Category | Signal | Source / Rationale |
|----------|--------|--------------------|
| **Security** | Adversarial prompt-injection suite passes as a release gate (Runner cannot exfiltrate secrets or push unauthorized code) | CSA recommends injection red-teaming as a standard deployment gate (web-02 §2.4, web-03 §2.2) → see §19 |
| **Trust / adoption** | Propose-only default upheld; authorized-replier-only action; zero unauthorized pushes | 84% adoption vs ~3–33% trust; auto-posting bots get muted within months (web-01 §4.3, web-02 §4) → see §19 |
| **Latency / cost** | Bounded round/budget (default 2, cap 5); poll floor ≥30s; benchmarked against "single LLM call ~30s" (PR-Agent) and Copilot's criticized 90s+ cold start | web-01 §1.3, §5; [CODE-VERIFIED budgets: agents 4, 6] → see §19 |

---

## 6. Jobs To Be Done (JTBD)

> **Framework:** Jobs To Be Done focuses on the underlying motivation and desired outcome, not the
> solution. Format: "When [situation], I want to [motivation], so I can [expected outcome]."

### 6.1 Primary Jobs

**Job 1: Turn a flagged review comment into a fix without opening a coding session**

- **When**: an AI reviewer (Augment/`sc:auggie-review`) or a human leaves a review comment flagging
  an issue on a PR, and I (an authorized collaborator) want it remediated.
- **I want to**: reply to that specific comment with a short directive — e.g. `@bot fix --depth deep`
  — and have a headless agent check out PR-head, run `/sc:troubleshoot` against the comment, and
  propose a diff.
- **So I can**: clear review findings without context-switching into a live IDE/Claude session or
  babysitting a long-running tool.
- **Current alternatives**: manually open an editor and fix it; or run the V1.0 in-session monitor
  (which dies when the session/laptop closes — V1 R3).
- **Pain with alternatives**: the in-session host is fragile (no 24/7 survival); manual fixing is
  the toil the whole framework exists to remove [CODE-VERIFIED lineage: agents 1, 3, 5].

**Job 2: Delegate the fix but stay in control of what lands**

- **When**: I trust an agent to *draft* a fix but not to silently push or merge it.
- **I want to**: keep the bot at **propose-only by default**, and have it reach `push`/`resolve`
  only when I explicitly raise the autonomy flag, I hold write permission, validation passes, and
  the push budget is unspent — a lattice-minimum cap, with `needs_human_decision` items hard-halting.
- **So I can**: get leverage from automation without inheriting its mistakes (the "middle ground"
  the market is asking for).
- **Current alternatives**: GitHub Copilot Coding Agent, which unconditionally opens a child PR
  even when told not to.
- **Pain with alternatives**: over-action erodes trust; auto-posting/auto-acting bots get muted
  within months (84% adoption vs ~3–33% trust) [web-01 §1.2, §4.3; web-02 §4; CODE-VERIFIED gate
  logic: `pr_submit/fsm.py` 5-predicate `evaluate_push_decision`, agents 5, 6].

**Job 3: Run autonomous remediation on untrusted comment text without getting owned**

- **When**: the bot must process attacker-influenceable GitHub text (the parent `opComment`) while
  the system holds push credentials.
- **I want to**: ensure the credential-holding layer (Dispatcher) never ingests the untrusted text
  as instructions, the reasoning layer (Runner) holds no exfiltratable secrets, and the comment is
  delivered as JSON **DATA inside a trusted envelope** — never interpolated as
  `/sc:troubleshoot "${opComment}"`.
- **So I can**: avoid the "Comment and Control" credential-theft class that hit Claude Code, Gemini
  CLI, and Copilot Agent in 2026.
- **Current alternatives**: cloud GitHub-Actions agents using `pull_request_target` (which injects
  secrets into the runner that sees untrusted text).
- **Pain with alternatives**: that exact pattern produced the 2026 CVEs and supply-chain exploits;
  detection/prompting alone is not a defense (>85% adaptive attack success across 78 studies)
  [web-01 §3, web-02 §2, web-03 §2; CODE-VERIFIED envelope requirement: agent 8].

**Job 4: Operate PR auto-remediation where the cloud can't go**

- **When**: I run a regulated, firewalled, or air-gapped shop and cannot send code to GitHub-hosted
  runners.
- **I want to**: deploy the whole bot on-prem as a systemd service against my fork, with a
  deny-by-default egress allowlist and host-side-only credentials.
- **So I can**: get mention-triggered remediation that cloud-only incumbents (Copilot, Amazon Q,
  Cursor) structurally cannot provide.
- **Current alternatives**: on-prem inline/IDE assistants (Tabnine, Windsurf, Qodo).
- **Pain with alternatives**: they assist in the editor; none offer autonomous mention-triggered PR
  remediation — the whitespace V2.0 targets [web-01 §2.2, web-03 §4.2].

### 6.2 Related Jobs

| Job | Frequency | Importance | Satisfaction with Current Solutions |
|-----|-----------|------------|-------------------------------------|
| Operate a 24/7 headless service that survives restarts (operator) | Continuous | Critical | 2/10 — V1.0 in-session host dies on session close (agents 1, 3) |
| Prove who triggered what, with an immutable audit trail | Per trigger | High | 3/10 — governance/audit is the "missing link" for 25% of leaders (web-03 §4.3) |
| Prevent the bot from ever pushing to the wrong (upstream) repo | Per push | Critical | 2/10 — fork-only `--repo` is prose-only today, has already failed once (agents 3–6) |
| Keep remediation cost/latency bounded on large diffs | Per trigger | Medium | 4/10 — PR-Agent sets the ~30s/low-cost bar; Copilot criticized for 90s+ cold start (web-01 §1.3) |

---

## 7. User Personas

### 7.1 Primary Persona: Maya — Authorized Reviewer / Repo Maintainer

| Attribute | Details |
|-----------|---------|
| **Demographics** | Senior engineer / maintainer with **write (or admin) permission** on the `IronbellyOrg/IronClaude` fork; lives in PRs and the terminal; high familiarity with the `superclaude` CLI surface (agent 8 §3) |
| **Goals** | Clear review findings fast; delegate routine fixes to an agent while controlling what lands; never trust the bot blindly |
| **Pain Points** | Context-switching into a coding session to apply a one-line fix; the V1.0 monitor dying on session close; incumbent agents over-acting on intent |
| **Technical Proficiency** | High |
| **Budget Authority** | Influences (sets autonomy level per trigger via the mention grammar) |
| **Success Metrics** | Findings remediated per PR with zero unauthorized pushes; time-to-proposed-fix; trust that propose-only holds |

**Quote:** "I want to reply `@bot fix` on a review comment and get a clean diff to look at — not a child PR I never asked for, and definitely not a push I didn't approve."

**A Day in Their Life:**
Maya is the **sole authority** on a trigger — she replies to an AI/human review comment with a tiny
whitelisted directive (`propose|patch|fix|push|resolve` + `--depth`/`--scope`/`--rounds`); the
parent comment is data, not a command (agent 8 §3). Default with no flag = `propose` (safest). She
reviews the bot's proposed diff and decides what merges — humans always merge (web-01 §5.1).

### 7.2 Secondary Persona: Devraj — Platform / DevOps Operator

| Attribute | Details |
|-----------|---------|
| **Demographics** | DevOps/SRE responsible for standing up and running the headless service on-prem; manages systemd, secrets, and the sandbox runtime |
| **Goals** | A 24/7 service that survives restarts; secrets held host-side only; deny-by-default egress; an immutable audit trail |
| **Pain Points** | No existing daemon/long-lived-service pattern in the CLI to copy; `deploy/` + systemd units are fully greenfield (OD-1 sandbox tech unresolved) [CODE-VERIFIED greenfield: agents 2, 4, 6] |
| **Technical Proficiency** | High |
| **Budget Authority** | Yes (owns deployment, token issuance, sandbox/compute footprint) |
| **Success Metrics** | Uptime / restart survival; zero secret leakage into the Runner env (AC-7); zero pushes to the wrong repo |

**Quote:** "It has to run as a service I can `systemctl restart` and walk away from — and I need proof that `GH_TOKEN` never makes it into the box that reads the untrusted comment."

### 7.3 Tertiary Persona: Sofia — Security / Governance Engineer

| Attribute | Details |
|-----------|---------|
| **Demographics** | AppSec/governance owner accountable for safe adoption of autonomous coding agents; tracks OWASP LLM01, CSA guidance, NIST AI RMF / ISO 42001 |
| **Goals** | Verify the bot cannot be weaponized by a crafted comment; confirm reasoning/execution separation, least-privilege, and tamper-evident audit |
| **Pain Points** | The "Comment and Control" / "Clinejection" attack class; cloud `pull_request_target` secret injection; detection/prompting alone proven insufficient (web-01 §3, web-02 §2) |
| **Technical Proficiency** | High |
| **Budget Authority** | Influences (sign-off / release gate) |
| **Success Metrics** | Adversarial injection suite passes as a release gate; quantified injection-resistance; immutable trigger ledger covers every trigger + exact input + decision |

**Quote:** "Show me the architecture separates the layer that reads the comment from the layer that holds the token — and show me the red-team suite that proves it."

### 7.4 Anti-Personas (Who This Is NOT For)

| Anti-Persona | Why Not Target |
|--------------|----------------|
| Read-only / external (fork) contributors who @-mention the bot | The live authorization gate rejects them by default; the *replier* is the sole authority, a `read`-permission user gets a polite ack-reject, zero action (AC-1, agent 8 §3) |
| Teams wanting fully-autonomous auto-merge / "delegate and forget" | Propose-only is the deliberate default; humans merge — the design explicitly refuses to modify merge state (web-01 §5.1, web-03 §1; severity rubric forbids `--approve`/`--request-changes`, agent 8 §4) |
| Cloud-only teams happy on GitHub-hosted runners | The product's reason to exist is on-prem/air-gapped self-hosting; teams with no self-host requirement are better served by Copilot Coding Agent / `@claude` Action (web-01 §1.1, web-03 §1.1) |

---

## 8. Value Proposition Canvas

> **Framework:** Maps customer pains and gains to product pain relievers and gain creators.
> **Note:** the `superclaude remediate` host is greenfield (not yet built); the value map below
> describes **designed** capabilities. Items grounded in already-built code are marked
> [CODE-VERIFIED].

### 8.1 Customer Profile: Maya (Primary Persona — Authorized Reviewer / Maintainer)

**Customer Jobs:**

1. (Functional) Convert a flagged review comment into a proposed fix without opening a coding session.
2. (Functional) Control the autonomy level per trigger — propose vs. push — and keep humans on the merge.
3. (Social) Adopt agent automation that the team trusts rather than mutes.
4. (Emotional) Delegate routine remediation without fear of an unauthorized push or a leaked secret.

**Pains:**
| Pain | Severity (1-10) | Frequency |
|------|-----------------|-----------|
| Context-switching into an IDE/session to apply small review fixes | 7 | Every review cycle |
| Remediation host dies on session/laptop close (V1.0) | 9 | Every long-running monitor attempt |
| Incumbent agents over-act / ignore intent (unwanted child PRs) | 8 | Per Copilot trigger (web-01 §1.2) |
| Untrusted comment → secret theft / unauthorized push ("Comment and Control") | 10 | Latent on every trigger (web-01 §3, web-02 §2) |
| Bot pushing to the wrong (upstream) repo | 9 | Per push — has happened once (agents 3–6) |

**Gains:**
| Gain | Importance (1-10) | Current Satisfaction |
|------|-------------------|---------------------|
| Mention → headless proposed fix, no session needed | 9 | 2/10 (V1.0 session-bound) |
| Stay in control: propose-only default, lattice-min autonomy, human merges | 10 | 3/10 (incumbents over-act) |
| Provable safety on untrusted input (secret separation, sandbox) | 10 | 2/10 (cloud agents leak) |
| Runs on-prem / air-gapped | 8 | 3/10 (incumbents cloud-only) |

### 8.2 Value Map

**Pain Relievers:**
| Pain | How We Relieve It | Measurement |
|------|-------------------|-------------|
| Session-bound, fragile host | Split **Dispatcher (systemd daemon) + ephemeral Runner**; survives session/machine restart; ledger is SoT, counter derived on startup | Restart-survival test; uptime (see §19) |
| Over-action / ignored intent | **Propose-only default**; effective autonomy = lattice-min over {flag, authz, validation, budget}; `needs_human_decision` hard-halt [CODE-VERIFIED 5-predicate gate: `pr_submit/fsm.py`, agents 5, 6] | Zero unauthorized pushes; authorized-replier-only action (AC-1) |
| Untrusted-comment secret theft | Reasoning/execution **split**: Runner holds no push/Anthropic secrets, opComment delivered as JSON **DATA via stdin envelope**, never interpolated; Dispatcher (credential layer) never ingests untrusted text | Adversarial injection suite as release gate; AC-7 `/proc/<pid>/environ` scrape = 0 secrets |
| Wrong-repo push | **H5 `gh` wrapper** unconditionally injects `--repo IronbellyOrg/IronClaude` — first *code* enforcement of a today-prose-only rule [CODE-VERIFIED no Python `gh` caller exists: agents 3–6] | Unit test: no argv can omit `--repo`; verified target owner |
| Cloud lock-out | **On-prem** systemd deployment, deny-by-default egress allowlist, host-side-only short-lived tokens | Runs air-gapped; sidesteps `pull_request_target` exposure |

**Gain Creators:**
| Gain | How We Create It | Measurement |
|------|------------------|-------------|
| Frictionless mention→fix | `@bot <level> --depth/--scope/--rounds` grammar → sandboxed Runner runs `/sc:troubleshoot` on PR-head, emits diff (propose) or sandbox-branch commit (fix) [CODE-VERIFIED executor reuse: `ClaudeProcess`, `roadmap/remediate_executor.py`, agents 1, 5, 8] | Time-to-proposed-fix; findings remediated per PR |
| Control + trust | Conservative default + severity→action routing (reuse rubric/`severity_router`) [CODE-VERIFIED: agents 2, 3] + immutable trigger ledger for provenance | Propose-only adherence; audit completeness |
| Governance-by-construction | Live per-trigger collaborator-permission authz gate (reject-by-default); two-phase intent/outcome ledger; bounded push budget (default 2, cap 5) | Authz coverage; ledger replay correctness |
| On-prem assurance | Whole bot self-hosted; no third-party GitHub Action in the trust path | Compliance posture (OWASP/CSA/NIST-aligned) |

### 8.3 Fit Assessment

| Fit Type | Score (1-10) | Evidence |
|----------|--------------|----------|
| **Problem-Solution Fit** | 9 | The exact threat (untrusted-comment + tool-bearing agent) produced named 2026 CVEs; CSA Labs prescribes reasoning/execution separation as "the fundamental mitigation" — a 1:1 description of the Runner/Dispatcher split (web-01 §3.2, web-02 §2, web-03 §2.2). The decision core is ~40–80% already built and tested in `pr_submit/` [CODE-VERIFIED: agents 3–6] |
| **Product-Market Fit** | 7 | Mention-trigger UX is idiomatic and validated by the platform owner (Copilot, `@claude`); propose-only is the universal safe default; on-prem × mention-triggered remediation is documented open whitespace. Tempered by: greenfield host (sandbox/systemd/GraphQL net-new, agents 4–8) and narrow initial audience (fork-scoped) |

---

## 9. Competitive Analysis

> **Scope note:** PR Auto-Remediation V2.0 competes directly with the standalone "mention →
> autonomous PR fix" product category, so a full competitive landscape is warranted. All
> capabilities attributed to **Our Product (V2.0)** are *target design requirements* — the
> `cli/remediate/` group is greenfield (CODE-VERIFIED absent today); only the underlying reuse
> primitives (`ClaudeProcess`, `pr_submit/` decision core, severity rubric) exist in code.

### 9.1 Competitive Landscape

| Competitor | Type | Target Market | Key Strengths | Key Weaknesses |
|------------|------|---------------|---------------|----------------|
| **GitHub Copilot Coding Agent** | Direct | GitHub-hosted teams | Category leader (GA Sep 2025); `@copilot` mention → autonomous draft PR in an ephemeral GitHub-Actions env; runs tests/linters; never auto-merges; trigger-er's approval doesn't count toward required review | **GitHub-hosted only — not self-hostable** (Copilot Enterprise "cloud-dependent"); **unconditionally opens a child PR even when the comment says "don't"** — #1 documented complaint (GitHub Community #190027: "intent ignored, no conversational mode, no middle ground"); inherits `pull_request_target` secret-injection exposure |
| **Claude Code GitHub Action (`@claude`)** | Direct | GitHub-hosted teams using Claude | Same `claude -p` lineage as our Runner; `@claude` mention → analyze/fix in isolated env; multi-agent code review with severity markers + `file:line` citations; <1% findings marked incorrect (vendor internal) | Runs as a **GitHub-Actions cloud job** with repo read/write; `@claude` is a workflow-`if` convention, not a hardened untrusted-comment envelope; secrets live in the runner |
| **Devin (Cognition)** | Direct | Enterprise (Goldman Sachs, Santander, Nubank) | Autonomous PR review/fix; clones repo, runs code to verify; ~5–10 min/PR; explicit pre-push git-hook guard against agent pushes; positioned "extra set of eyes, not a replacement" | Cloud SaaS — **not on-prem**; full-autonomy end of the spectrum; ~$10.2B valuation pricing tier |
| **CodeRabbit / PR-Agent (Qodo) / Ellipsis** | Indirect (review tier) | Broad GitHub/GitLab | CodeRabbit: 40+ analyzers + interactive PR-comment chat; PR-Agent: open-source, model-agnostic, self-hostable, `/review` `/improve` commands; Ellipsis: "automated fix implementation" ($20/user/mo) | Mostly **review/suggest-only** (CodeRabbit, PR-Agent stop at proposing); thin or absent untrusted-input/secret-separation story; the fix-implementing ones run cloud-Action-hosted |
| **Tabnine / Windsurf / Qodo (air-gapped tier)** | Substitute | Regulated (defense, finance, healthcare, gov) | Lead the on-prem/air-gapped segment with compliance certs (SOC2 Type II, FedRAMP High, DoD IL5, ITAR, zero-retention) | Ship **inline / IDE assistants**, NOT mention-triggered autonomous PR-remediation bots — different product shape; do not occupy the remediation-bot category |

### 9.2 Feature Comparison Matrix

| Feature | Our Product (V2.0, target) | Copilot Coding Agent | Claude `@claude` Action | Devin | CodeRabbit / PR-Agent |
|---------|---------------------------|----------------------|-------------------------|-------|-----------------------|
| Mention-triggered (`@bot` in PR comment) | ✅ | ✅ | ✅ | ⚠️ (PR-event, not mention) | ⚠️ (slash-command) |
| On-prem / self-hosted (no cloud runner) | ✅ | ❌ | ❌ | ❌ | ⚠️ (PR-Agent only) |
| Headless (no IDE, no GitHub-Actions host) | ✅ | ❌ | ❌ | ❌ | ⚠️ |
| File-write + git-push remediation | ✅ | ✅ | ✅ | ⚠️ (review-centric) | ⚠️ (Ellipsis only) |
| Propose-only **default** + intent evaluation | ✅ | ❌ (over-triggers) | ❌ | ✅ | ✅ |
| Live per-trigger authorization gate (collaborator-permission) | ✅ | ⚠️ (org policy) | ❌ (workflow `if`) | ❌ | ❌ |
| Untrusted-comment injection containment (data-in-envelope) | ✅ | ❌ | ❌ | ❌ | ❌ |
| Secret separation (Runner holds no push token) | ✅ | ❌ (`pull_request_target` exposure) | ❌ | ⚠️ | ❌ |
| Never auto-merge (humans merge) | ✅ | ✅ | ✅ | ✅ | ✅ |
| Reply-to-thread + thread resolve | ✅ | ⚠️ | ⚠️ | ⚠️ | ✅ (review chat) |

**Legend:** ✅ Full support | ⚠️ Partial/Limited | ❌ Not supported

### 9.3 Competitive Positioning

**Our Unique Differentiation:**

1. **On-prem × mention-triggered remediation — an empty market intersection.** Copilot / Amazon Q / Cursor lead mention-triggered or autonomous coding but are cloud-only / not self-hostable; Tabnine / Windsurf / Qodo lead air-gapped/on-prem but ship inline/IDE assist, not autonomous PR-remediation bots. **No incumbent occupies both axes** — the regulated segments (defense, finance, healthcare, telecom, government) that are structurally locked out of cloud-hosted agents are addressable only by an on-prem bot.
2. **The split-host architecture is the industry-prescribed injection mitigation.** CSA Labs names "architectural separation of the agent's reasoning layer from the credential-holding execution layer" as *the fundamental mitigation* for prompt injection — a 1:1 description of our tokenless Runner (reasoning) + credential-holding Dispatcher (policy/execution). Independently mirrored by Simon Willison's Dual-LLM pattern, the Anthropic/ETH/DeepMind design-patterns paper, and AWS AgentCore's "never put the token in the VM."
3. **Propose-only default + authorization gate answers the market leader's #1 complaint.** Copilot Coding Agent unconditionally opens a child PR even when the comment says "don't"; our live authorization gate + conservative propose-only default is the "middle ground / confirmation step" users explicitly ask for — and aligns with the universal safe default (draft-PR, human-approves, agent-cannot-self-merge) across Copilot, Continue ("Level 2 Continuous AI"), Devin, and Anthropic's 2026 trends report.

**Positioning Statement:**
"For repo maintainers and on-call reviewers on regulated, self-hosted code who cannot send their source to cloud-hosted runners, **PR Auto-Remediation V2.0** is an on-prem, mention-triggered remediation bot that turns an authorized `@bot` reply into a sandboxed, propose-by-default fix. Unlike GitHub Copilot Coding Agent and the `@claude` GitHub Action, our product runs headless on-prem with a split Dispatcher/Runner host that treats the triggering comment as untrusted data and keeps push credentials out of the agent's reach."

### 9.4 Competitive Response Plan

| If Competitor Does... | Our Response |
|-----------------------|--------------|
| Copilot/GitHub ship a self-hosted-runner variant of the Coding Agent | Lead with the secret-separation + untrusted-comment-envelope story (sidesteps the `pull_request_target` exposure underlying 2026 GitHub-Actions agent CVEs) and the live per-trigger authorization gate, which a GitHub-Actions host does not provide natively |
| Copilot adds an "evaluate intent before acting" confirmation step | Emphasize the deeper differentiation — on-prem deployment, propose-only-by-default lattice, and architectural injection containment — not just the intent check |
| An air-gapped IDE vendor (Tabnine/Windsurf/Qodo) adds a mention-triggered PR-remediation bot | Compete on the governance posture: two-phase audit ledger, deterministic loop-guard (push budget 2/cap 5), fork-only `--repo` code enforcement, and OWASP-LLM-Top-10-aligned-by-construction design as procurement evidence for the EU AI Act (Aug 2026) high-risk deadline |

---

## 10. Assumptions & Constraints

### 10.1 Technical Assumptions

| ID | Assumption | Risk if Wrong | Validation Method |
|----|------------|---------------|-------------------|
| TA-1 | `ClaudeProcess` (`cli/pipeline/process.py:72`) is reusable as the Runner's headless `claude -p` executor — `build_command()` flags, chunked-stdin prompt delivery (bypasses 128KB argv limit), 16 MiB `PROMPT_MAX_BYTES` guard, process-group kill, and `timeout_seconds=6300` all behave as the spec relies on | Runner cannot spawn `claude -p` reliably; large `opComment` envelopes fail or deadlock | CODE-VERIFIED across research 01-08 (exact line, byte-accurate flag string, stdin delivery, size guard) |
| TA-2 | `ClaudeProcess.build_env()` can be given an allowlist/replace mode (or the Runner spawned from a pre-scrubbed parent) so the Runner env excludes `GH_TOKEN`/push token/`ANTHROPIC_*` | INV-001/SC-7/AC-7 secret-isolation fails silently — push credential leaks into the untrusted-comment-processing Runner | CODE-CONTRADICTED as-is: `build_env()` is additive-merge over `os.environ.copy()` and **cannot subtract** inherited keys; requires a `base_env`/`env_mode="allowlist"` code change + an `assert "GH_TOKEN" not in runner_env` regression test (AC-7 `/proc/<pid>/environ` scrape) |
| TA-3 | `ClaudeProcess` can run the child in the sandbox PR-head checkout via a new `cwd` parameter or a Runner-side `os.chdir()` | Runner edits the wrong working tree | CODE-CONTRADICTED: `Popen` at `process.py:192` passes no `cwd=`; needs a small code change or `os.chdir()` in the one-shot Runner |
| TA-4 | The V1.0 `pr_submit/` pure decision core (`fsm.evaluate_push_decision`, `should_halt_rounds`, `severity_router`, `classifier`, `detection.DetectionContractLocked`, `models`) is import-and-extend reusable for the autonomy gate, round counter, severity routing, and probe-lock | V2.0 rebuilds tested logic from scratch — drift risk, divergent severity grading vs the `sc:pr-submit` skill, double-maintenance | CODE-VERIFIED present + tested (`tests/pr_submit/*`); **landing in parallel today** (still git-untracked) — `loop_guard.py`/`run_log.py`/`recovery.py` have since landed built + tested (`test_loop_guard.py`/`test_run_log.py`/`test_crash_recovery.py`); coordinate so V2 work doesn't race the in-flight V1 build |
| TA-5 | The real GitHub-API shapes for the trigger surface — `in_reply_to_id`, comment `databaseId`, `reviewThreads` pagination, the Augment bot login — can be locked from a throwaway-PR probe before parser code is written | Parser built against guessed bytes; "resolved the wrong thread" (INV-010) class bug | Probe-first gate (§21.3); no committed/tracked precedent, but a reference reply→resolve bash flow has since landed in the untracked parallel V1 `sc-pr-submit-protocol` skill (`scripts/reply-resolve-thread.sh` covers `in_reply_to`/`reviewThreads`/`resolveReviewThread`) — crib its shape, but the live probe still must lock the real `in_reply_to_id`/`databaseId` bytes |
| TA-6 | ETag/304 conditional polling + rate-limit (`If-None-Match`/`Retry-After`/`X-RateLimit-Remaining`) discipline can be built net-new for the Dispatcher ingest | Polling either rate-limit-bans the bot or misses triggers | CODE-VERIFIED no in-repo precedent (grep = 0); D3 is greenfield |
| TA-7 | A container or microVM sandbox can run `claude --dangerously-skip-permissions` safely with deny-all egress + an endpoint allowlist that still reaches the Anthropic proxy (`~/.aienv` `:4000/cli`) and `api.github.com` | Untrusted-comment-driven code execution escapes isolation; or the proxy is unreachable and the Runner cannot call the model | OD-1 open decision; shared-kernel containers flagged insufficient by external consensus (Firecracker/gVisor/Kata/libkrun or Landlock+seccomp recommended); proxy reachability must be confirmed against the chosen topology |

### 10.2 Business Assumptions

| ID | Assumption | Risk if Wrong | Validation Method |
|----|------------|---------------|-------------------|
| BA-1 | "Autonomous pull request resolution / security vulnerability remediation" is an emerging high-value, not-yet-commoditized use case worth occupying | Effort spent on a saturating category | Analyst-named emerging high-value use case (marketintelo); fast-growing agentic-dev market (varied estimates ~$10.4B 2025 / CAGR ~39.5%; ~$12.6B by 2028 / CAGR 24%) |
| BA-2 | The on-prem/governed segment (~29% of market, security-driven) is real and under-served by cloud-first incumbents | Differentiation axis is illusory | Mordor: cloud-hosted held 71.3% (2025), self-hosted the explicitly under-served minority; VDF/TrueFoundry/Greptile name governed on-prem as the hard, under-served problem |
| BA-3 | A conservative propose-only, safety-first posture wins more trust than raw autonomy in a trust-constrained market | Product perceived as a capability-limited laggard | 84% adoption vs ~3–33% trust AI output; "auto-post → muted bots within months"; Anthropic 2026: "collaborative, not delegated" |

### 10.3 User Assumptions

| ID | Assumption | Risk if Wrong | Validation Method |
|----|------------|---------------|-------------------|
| UA-1 | The `@bot` mention-in-a-review-reply trigger is idiomatic and low-adoption-risk for maintainers | Users don't discover or trust the trigger | Established UX standard: `@claude`, `@copilot`, `@review-bot`, `/gs review` — mention-as-command is the de-facto convention |
| UA-2 | A 4-token mention grammar (autonomy level + `--depth` + `--scope` + `--rounds`), default `propose`, is the entire control surface users need | Users want richer control or are confused by defaults | Mirrors incumbents' minimal command surfaces; default-propose is the market-validated safe posture |
| UA-3 | The *replier* (authorized write-collaborator) is the sole authority; the *parent comment author* supplies only data | An unauthorized or read-only user triggers consequential action | Live per-trigger collaborator-permission gate (D5/C4); read-permission mention → polite ack-reject, zero action (AC-1) |

### 10.4 Constraints

| Type | Constraint | Impact on Product | Mitigation |
|------|------------|-------------------|------------|
| **Technology** | No Python `gh` subprocess wrapper exists anywhere in the repo; all `gh` I/O today is skill-markdown/bash | H5 (`gh_call()` with unconditional `--repo` injection) is foundational net-new, the first *code* enforcement of fork-only `--repo` — must be built and tested before any `gh`-calling code | Build H5 first (§21.3 sequencing); unit test asserting no argv can omit `--repo IronbellyOrg/IronClaude`; optional CI grep-guard against raw `gh` outside `gh.py` |
| **Technology** | No execution sandbox, no systemd/`deploy/` precedent in-repo (OD-1 unresolved: container vs microVM) | The 24/7 daemon, sandbox image, and `deploy/remediate-bot/` units are the largest greenfield surface and gate R4/S2 | Resolve OD-1 early; `eval/isolation.py` scratch-root model is partial prior art for filesystem confinement only |
| **Security/Regulatory** | Prompt injection is OWASP's #1 LLM/agentic risk and is effectively unsolved (no fool-proof prevention); EU AI Act high-risk compliance deadline Aug 2026 | Forces defense-in-depth (envelope + secret separation + propose-only + bounded scope), not a single filter; injection red-teaming becomes a release gate | opComment as untrusted DATA in a CONTROL/DATA envelope delivered via stdin (never `/sc:troubleshoot "${opComment}"` interpolation); align to OWASP LLM01:2025, OWASP Top 10 for Agentic Apps (Dec 2025), NIST AI RMF, ISO 42001 |
| **Process / SoT** | Fork-only PR target: `origin = IronbellyOrg/IronClaude`, never upstream `SuperClaude-Org`; `.claude/` is gitignored sync-dev output | Autonomous pushes to the wrong repo = exposure of private fork work (historically burned the operator); careless staging breaks `verify-sync` | C5 fork-only `--repo` invariant enforced in H5 code; secret-source `~/.aienv` proxy contract (`:4000/cli` + `T2Model*` only) is the sole credential allowed into the sandbox |
| **Operational** | Poll interval floor ≥30s; per-PR push budget default 2, hard cap 5 | Bounds GitHub API load and remediation-loop blast radius | Reuse `pr_submit` `MIN_POLL_INTERVAL=30`, `DEFAULT_MAX_ROUNDS=2`, `HARD_CAP_MAX_ROUNDS=5` (V1.0 already chose these); disk-authoritative ledger is SoT, counter derived on startup |
| **Resource** | V1.0 `pr_submit/` decision core is landing in parallel; `~/.aienv` secret file is 644 (not the 600 the spec cites as exemplar) | Risk of two teams building overlapping ledger/round-counter logic; false secret-hygiene provenance | Sequence/own V1-core completion vs V2-host build; require `chmod 600` + systemd `EnvironmentFile=` on its own merits, don't cite `.aienv` as the permissions exemplar |

---

## 11. Dependencies

### 11.1 External Dependencies

| Dependency | Type | Owner | Risk Level | Contingency |
|------------|------|-------|------------|-------------|
| GitHub REST + GraphQL API (comment polling, `pulls/<N>/comments`, `pulls/<N>/comments/<parent>/replies`, `reviewThreads`, `resolveReviewThread`) | API | GitHub | High | Reply/resolve GraphQL has no committed Python precedent (a reference bash flow now exists in the untracked `sc-pr-submit-protocol` skill); lock real shapes via §21.3 probe before parser code; reply-only fallback if `resolveReviewThread` proves unreliable |
| `gh` CLI (host-side GitHub I/O, invoked via the H5 wrapper) | Tool | GitHub | Medium | All calls routed through `H5.gh_call()` with unconditional `--repo IronbellyOrg/IronClaude`; no raw `subprocess(["gh", …])` permitted |
| Anthropic model access via the `~/.aienv` proxy (`:4000/cli` base + `T2Model*` model ids) | API | Internal proxy / Anthropic | High | The **only** credential class allowed into the sandbox; sandbox egress allowlist must reach the proxy host; `PromptTooLargeForArgv` (16 MiB guard) bounds envelope size |
| `claude` CLI (`claude --print …`, spawned by the Runner via `ClaudeProcess`) | Tool | Anthropic | Medium | Pinned flags via `build_command()`; `--dangerously-skip-permissions` safe **only** inside the sandbox boundary |
| Sandbox runtime (container or microVM — Firecracker/gVisor/Kata/libkrun, or Landlock+seccomp) | Infrastructure | Operator (OD-1) | High | OD-1 open decision; shared-kernel containers flagged insufficient for untrusted-code execution; build-vs-buy refs: microsandbox, brood-box, cplt |
| `systemd` (Dispatcher daemon supervision: `Restart=always`, `WatchdogSec`, `EnvironmentFile=`) | Infrastructure | Operator | Medium | No existing daemon precedent in the CLI; spike `sd_notify`/`WatchdogSec` integration; `deploy/remediate-bot/` is greenfield |
| Augment review bot (the upstream producer of the review comments the bot remediates) | Service | Augment | Medium | Bot login locked as a config constant via the §21.3 probe; unknown login → not-detected (safe default) |

### 11.2 Internal Dependencies

| Dependency | Type | Owner | Status | Target Date |
|------------|------|-------|--------|-------------|
| `ClaudeProcess` (`cli/pipeline/process.py:72`) — shared headless-spawn primitive | Component | Pipeline/CLI | Built (needs back-compat `base_env`/`cwd` additions) | Before R2/R4 |
| `pr_submit/` decision core (`fsm`, `severity_router`, `classifier`, `detection`, `models`) | Package | pr_submit (V1.0) | ~60% built + tested; landing in parallel | Coordinate before H1/H2/S1 |
| `pr_submit/` `loop_guard.py` / `run_log.py` / `recovery.py` (write-ahead JSONL, crash recovery) | Module | pr_submit (V1.0) | Built + tested (untracked, landing in parallel) | Build the durable two-phase ledger here, not a forked `remediate/ledger.py` |
| `sc-auggie-review-protocol/refs/severity-rubric.md` (5-tier rubric) | Reference | auggie-review skill | Built; already encoded in `pr_submit.severity_router` | Import the router, don't re-parse the markdown |
| `swarm/state.py` `write_state` (atomic tmp + `os.replace`) + `models.py:1141` `SwarmState` | Pattern | swarm | Built | Borrow the atomicity idiom for the ledger; append-only `O_APPEND`+`flock` model is net-new |
| `cli/main.py` deferred-import group registration (`# noqa: E402,I001`) | Wiring | CLI | Built | Add `remediate_group` + `add_command(name="remediate")`, else the command is dead |
| `roadmap/remediate_executor.py` (existing `ClaudeProcess`-driven remediation: allowlist, snapshot/rollback, diff-size guard, patch-apply) | Component | roadmap | Built | Mirror-shape analog for R2/R4 executor + patch-emit/rollback path |

### 11.3 Cross-Team Dependencies

| Team | Dependency | What We Need | When Needed | Status |
|------|------------|--------------|-------------|--------|
| V1.0 `pr_submit` build | Decision-core completion + module layout | Settled `fsm`/`severity_router`/`models` APIs and the (now-landed but untracked) `loop_guard`/`run_log`/`recovery` ownership, so V2 imports rather than forks | Before H1/H2/S1 build | In flight (landing today) — race risk |
| Pipeline/CLI (shared primitive owners) | `ClaudeProcess` env-allowlist + `cwd` changes | Back-compatible `base_env`/`env_mode` and `cwd` additions, re-tested against sprint/roadmap/swarm callers | Before R2 at propose-only | Open design decision |
| Security / operator | OD-1 sandbox tech + OD-2 push-token mechanism | Chosen isolation tier (container vs microVM) and token type (GitHub App vs fine-grained PAT) — both gate R4/H3 | Early (gates largest greenfield surface) | Open (OD-1, OD-2) |

---

## 12. Scope Definition

### 12.1 In Scope (Phase 1 / MVP)

| Category | Included | Notes |
|----------|----------|-------|
| **CLI host (D1)** | New `superclaude remediate` CLI group under `src/superclaude/cli/remediate/`, registered in `cli/main.py` via the deferred-import `# noqa: E402,I001` idiom | Mirrors `sprint`/`swarm`/`pipeline`; runs headless outside any Claude session. Feature home is `cli/remediate/`; the empty top-level `remediation/` placeholder is to be deleted/ignored |
| **Dispatcher (D2–D6, S2)** | systemd daemon: poll (≥30s floor) → ETag/304 ingest → `@bot` mention grammar parse → live collaborator-permission authz gate → parent-comment (`opComment`) resolution → trigger claim in the ledger | The replier is the sole authority; read-permission mention → polite ack-reject (AC-1). D5/D6/D3 are greenfield (no in-repo prior art) |
| **Mention grammar (D4)** | Whitelisted tokens: autonomy level (`propose\|patch\|fix\|push\|resolve`), `--depth`, `--scope`, `--rounds`; **default = `propose`** | The entire end-user control surface — a 4-token comment; no GUI/web/new slash command |
| **Runner (R1–R4)** | Ephemeral, sandboxed, disposable per-trigger `claude -p` against an isolated PR-head checkout; `opComment` delivered as JSON DATA in a CONTROL/DATA envelope via stdin (never `"${opComment}"` interpolation); emits diff (propose) or sandbox-branch commit (fix) | Runner holds NO long-lived push/GitHub secret (INV-001/SC-7); only the `~/.aienv` proxy credential is allowed in |
| **Severity routing (S1/§17)** | Re-grade each Augment finding through the reused rubric (`pr_submit.severity_router`): Critical/High → `--depth deep --fix`; Medium → `--fix`; Low/Nit → report-only; unknown → Medium fail-safe | Augment severity is a hint, not authoritative |
| **Autonomy gate (H2)** | Effective level = lattice-min over {mention flag, authz projection, validation} then off-lattice HALT short-circuits (`needs_human_decision`, push-budget==0); structurally impossible to reach `push` without explicit flag AND write-permission AND passing validation | Extends `pr_submit.evaluate_push_decision` (4 of 5 predicates carry over); `needs_human_decision` HALT inherited verbatim from V1.0 FR-4.4 |
| **Loop-guard + two-phase ledger (H1, §9/§10)** | Disk-authoritative, atomic-write (tmp + `os.replace`), append-only JSONL with per-PR `flock` (fail-closed); per-PR push budget default 2, hard cap 5; SHA-correlated round counting; intent-without-outcome ⇒ RESUME, never silent re-execute | Genuinely net-new durable state core; borrows swarm's atomicity idiom |
| **Host-side push + reply (H3, H4-reply)** | Dispatcher pushes with a short-lived host-side token; replies to the review thread with summary + pushed SHA | Reply-to-thread templates off auggie-review posting precedent |
| **gh wrapper (H5)** | A single `gh_call()` chokepoint that unconditionally injects `--repo IronbellyOrg/IronClaude`; no code path can call `gh` without it | First *code* enforcement of the fork-only C5 invariant; build + test first |
| **Audit log (§14)** | JSONL event stream (poll, trigger_seen, authz_check, parse_mention, intent, `claude_process_spawn`, validation, push, reply_posted, round_outcome) distinct from the state ledger, surviving Runner teardown | Start from `pr_submit.models.EventType` and extend; surface as a first-class queryable audit artifact |

### 12.2 Out of Scope (Phase 1 / MVP)

| Item | Reason | Target Phase |
|------|--------|--------------|
| ❌ Thread **resolve** (`resolveReviewThread` GraphQL, `resolve` autonomy level) | Highest-risk net-new GitHub surface; no committed Python precedent (a reference bash flow exists in the untracked `sc-pr-submit-protocol` skill); `databaseId` pagination shape unverified until the §21.3 probe | Phase 2 (after probe locks the GraphQL shape) |
| ❌ Dual-LLM hardening of `opComment` (quarantined LLM pre-normalizes the parent comment into structured intent before the acting Runner) | Defense-in-depth enhancement atop the envelope; not required for the propose-only MVP | Phase 2 |
| ❌ Auto-apply / auto-push as a non-default | Trust data says auto-apply is a retention liability; ships only as opt-in, per-repo, gated behind the same authorization layer | Phase 2+ (opt-in only) |
| ❌ Multi-repo / multi-PR / multi-branch per trigger | Matches incumbent guardrail (single-repo, single-branch, one PR); bounds blast radius for MVP | Phase 3 |
| ❌ `offer-pr-review.sh` hook integration as a distributed touchpoint | Depends on reconciling the `src/superclaude/hooks/hooks.json` SoT drift first | Deferred / optional |

### 12.3 Permanently Out of Scope

| Item | Reason |
|------|--------|
| ❌ Modifying merge state (`gh pr review --approve` / `--request-changes`, auto-merge) | Humans merge — inherited non-goal, reinforced by the severity rubric's code-enforced "the verdict does NOT translate into approve/request-changes" invariant |
| ❌ V1.0's in-session Monitor-tool host | Fully replaced by the split Dispatcher(systemd)+Runner(sandbox) headless host (the entire reason V2.0 exists); the V1.0 *decision core* is reused, the *host* is not |
| ❌ Long-lived push/GitHub credentials inside the Runner | Architectural invariant — the Runner processes untrusted comment text and must never hold an exfiltratable consequential credential (the precondition that produced the 2026 "Comment and Control" CVEs) |

---

## 13. Open Questions

> Sourced from the merged-requirements Open Decisions (OD-1…OD-4) plus code-grounded gaps surfaced by the parallel codebase investigation (research 01–08). Status legend: 🔴 Urgent (build-blocking) / 🟡 Researching / 🟢 Resolved.

| # | Question | Owner | Target Date | Status | Resolution |
|---|----------|-------|-------------|--------|------------|
| 1 | **Runner secret-isolation mechanism (INV-001/SC-7/AC-7).** `ClaudeProcess.build_env()` (`cli/pipeline/process.py:145-160`) is **additive-only** — `env = os.environ.copy()` then `env.update(env_vars)`; passing `env_vars` can add/override but **cannot strip** an inherited `GH_TOKEN`/push token/`ANTHROPIC_*`. How is "no push credential in the Runner env" achieved: (a) new `base_env`/`env_mode="allowlist"` param on the shared primitive, (b) a Runner-owned env built from `{}`, or (c) a secret-free sandbox parent whose `os.environ` is already minimal? | Engineering (TDD) | Pre-build | 🔴 Urgent | Leaning (c) sandbox-level minimal environ as the primary guarantee (cleanest, aligns with §6 "no host home mount"); if (a) chosen, the edit touches a primitive shared by sprint/roadmap/swarm and must stay back-compatible (default keep current behaviour) with its own regression test. [CODE-VERIFIED additive-only across research 01/02/03/05/06/07/08] |
| 2 | **Reconcile V2.0 against the in-flight `src/superclaude/pr_submit/` V1.0 decision core.** The package (`fsm.py`, `severity_router.py`, `classifier.py`, `detection.py`, `models.py`; tested under `tests/pr_submit/`) is being landed today and overlaps V2's H1/H2/S1/D3/D6 **near 1:1** (e.g. `DEFAULT_MAX_ROUNDS=2`, `HARD_CAP_MAX_ROUNDS=5`, `MIN_POLL_INTERVAL=30`, `evaluate_push_decision` 5-predicate conjunction, `should_halt_rounds`, `remap_severity`/`route`, `DetectionContractLocked`). Does `cli/remediate/` **import-and-extend** `pr_submit` (reuse the brain) or fork it? | Eng Lead + Product | Pre-build | 🔴 Urgent | Strong recommendation across research 01/03/04/05/06: **import the pure decision core, build only the I/O+host layer** (Dispatcher/Runner/gh). Coordinate so V2 work does not race the untracked in-flight V1 build. [CODE-VERIFIED] |
| 3 | **OD-1 — Runner sandbox technology.** Container vs microVM (Firecracker/gVisor/Kata/libkrun) vs kernel-LSM (Landlock + seccomp-BPF). Zero in-repo execution-sandbox precedent (`eval/isolation.py` gives scratch-root *filesystem* confinement only, not network/process isolation). | DevOps + Security | Pre-build (gates R4/S2/§15) | 🔴 Urgent | External consensus (Northflank, CSA, awesome-agent-runtime-security): shared-kernel containers are **insufficient** for untrusted-comment-driven code; production pattern is microVM or kernel-LSM. `microsandbox`/`brood-box`/`cplt` are build-vs-buy references. Genuinely open; gates the largest greenfield surface. |
| 4 | **OD-2 — Host-side push-token mechanism.** GitHub App installation token vs fine-grained PAT vs OIDC/STS-minted short-lived token, scoped to the single fork repo. | DevOps + Security | Pre-build | 🟡 Researching | Industry direction of travel (GitHub docs, StepSecurity, AWS, Sysdig): short-lived OIDC/per-run tokens over static PATs; "keep tokens off the runner." Token lives host-side with the Dispatcher only. |
| 5 | **OD-3 — Per-PR push-budget default & cap.** Provisional `default 2, cap 5` pending the §21.3 probe's measurement of real Augment re-review cadence. | Product | Post-probe | 🟡 Researching | Partly **pre-decided** in code: V1 `pr_submit/fsm.py` already sets `DEFAULT_MAX_ROUNDS=2`/`HARD_CAP_MAX_ROUNDS=5`. Confirm against observed re-review timing in the probe before freezing. |
| 6 | **OD-4 — `patch` autonomy-level semantics.** What `patch` (between `propose` and `fix` on the lattice) is allowed to do vs `fix`. | Product | Pre-build | 🟡 Researching | Lattice is `propose < patch < fix < push < resolve`, default `propose`. The distinct capability ceiling of `patch` is unresolved. |
| 7 | **GitHub reply/resolve API shapes (INV-010).** `databaseId` vs node `id`, `reviewThreads` pagination, `in_reply_to_id` reliability, Augment bot login — **no committed/tracked precedent**; a reference reply→resolve bash flow has since landed in the untracked parallel V1 `sc-pr-submit-protocol` skill (`scripts/reply-resolve-thread.sh`, `refs/augment-poll.md`), but the real byte shapes must still be locked before parser/H4 code. | Engineering | §21.3 probe (hard gate) | 🔴 Urgent | The §21.3 throwaway-fixture-PR probe is a **non-optional hard gate**; captured shapes become committed config constants/fixtures (mirrors V1's `DetectionContractLocked`). The untracked bash flow is a shape reference, not a locked contract. |
| 8 | **`needs_human_decision` populator.** The §8 HALT guarantee rests on a flag that **no Python code sets today** — `Finding.needs_human_decision` is *consumed* in 5+ places in `pr_submit/fsm.py` but `grep 'needs_human_decision = True'` across `src/` returns nothing; the populating taxonomy (ambiguous intent / security trade-offs / API-contract changes / multiple valid fixes) is skill/agent-driven prose. Does V2's autonomous Dispatcher build a **deterministic populator**, or trust the in-sandbox agent to self-report? | Eng Lead + Security | Pre-build | 🔴 Urgent | For an autonomous daemon this is a concrete safety gap: a HALT that nothing triggers does not gate. Recommend a deterministic classifier or an explicit, documented agent-self-report dependency. [CODE-VERIFIED no Python setter] |
| 9 | **Source-home & stale placeholder.** Feature SoT is `src/superclaude/cli/remediate/` (absent today). A top-level `remediation/` dir exists but is **empty** (stale placeholder). | Eng Lead | Pre-build | 🟡 Researching | Confirm feature lives under `cli/remediate/`; delete/ignore the empty `remediation/` to avoid confusion. [CODE-VERIFIED] |
| 10 | **`main.py` group registration step.** D1 needs a deferred-import + `main.add_command(remediate_group, name="remediate")` pair in `cli/main.py:400-438` carrying the mandatory `# noqa: E402,I001` annotation — omitted from the build sequencing. Without it the group is dead; wrong annotation trips `make lint` (E402). | Engineering | Build (D1) | 🟢 Resolved | Add the registration pair with `name="remediate"` explicitly (majority pattern; `cli_portify` omits `name=` — do not copy that). [CODE-VERIFIED convention at `main.py:400-438`] |
| 11 | **Reuse-Map citation correction (`cli/swarm/commands.py:2269`).** Cited as a "monotonic, disk-authoritative, survives-restarts" round counter; the line is actually an **in-memory `swarm status --watch` iteration cap** (resets every run, never persisted). | Tech writer / Eng | Pre-TDD doc fix | 🟢 Resolved | Re-point: durable persistence idiom → `swarm/state.py` `write_state` (tmp + `os.replace`); bounded-counter idiom → `pr_submit/fsm.py::should_halt_rounds`. Spec §10 says `os.rename`; code uses `os.replace` — align wording. [CODE-CONTRADICTED at `:2269`] |
| 12 | **Two-phase append-only ledger concurrency model.** §10 needs `O_APPEND` + per-PR `flock` for intent/outcome records; only **whole-file** atomic-replace precedent exists (`install_hooks.py:443`, `swarm/state.py`, `recommend/cache.py`). No `fcntl.flock` in any Python module — only bash freshness hooks, which **fail-open**. | Engineering | Build (H1) | 🟡 Researching | H1's push serializer must **fail-closed** (invert the bash hooks' fail-open). Budget the append-only ledger as greenfield borrowing only the atomicity idiom. [CODE-VERIFIED] |
| 13 | **Optional `offer-pr-review.sh` hook touchpoint.** Could surface the mention-trigger path, but the distributable `src/superclaude/hooks/hooks.json` lacks the registration (SoT drift); it is registered only project-local in `.claude/settings.json`. | Eng (optional) | Backlog | 🟡 Researching | Low priority; do not depend on it being distributed until the hooks.json drift is reconciled. |

---

## 14. Technical Requirements

> **WHAT:** Cross-cutting technical requirements for the `superclaude remediate` mention-triggered headless PR auto-remediation bot — a split Dispatcher (systemd daemon) + ephemeral sandboxed Runner (`claude -p`) architecture.
> **Scope note:** This is a feature/component PRD. The `cli/remediate/` package is greenfield [CODE-VERIFIED absent]; requirements below state what to build. Reuse anchors (`ClaudeProcess`, `pr_submit`, severity rubric) are [CODE-VERIFIED] as existing primitives, not new product capability.

### 14.1 Architecture Requirements

| Requirement | Description | Rationale |
|-------------|-------------|-----------|
| **Split-host: reasoning/execution separation** | Long-lived **Dispatcher** (systemd daemon, holds credentials, runs authz + push) + ephemeral per-trigger **Runner** (`claude -p`, sandboxed, no secrets, processes the untrusted comment). | CSA Labs prescribes this verbatim as "the fundamental mitigation" for prompt injection: a reasoning layer that cannot execute + a credential-holding execution layer that never processes untrusted input. Directly neutralizes the 2026 "Comment and Control" CVE class. |
| **CLI group, not a skill** | New `superclaude remediate` Click group under `src/superclaude/cli/remediate/`, registered in `cli/main.py` via deferred import + `main.add_command(remediate_group, name="remediate")` carrying `# noqa: E402,I001`. | Host runs headless outside any Claude session; mirrors existing `sprint`/`swarm`/`pipeline` groups. Registration idiom is [CODE-VERIFIED] at `cli/main.py:400-438`; omitting the `# noqa` trips `make lint` (E402), omitting the edit ships a dead group. |
| **Reuse the pure decision core; build only the I/O layer** | Import V1.0's tested decision core from `src/superclaude/pr_submit/` (`fsm`, `severity_router`, `classifier`, `detection`, `models`); build new only the Dispatcher/Runner host + GitHub I/O. | `pr_submit/` is [CODE-VERIFIED] built+tested and already embodies the pure-core / dirty-I-O split (NFR-6: zero `gh`/`git` tokens in the core). V2.0's autonomy gate, round counter, severity routing, push-decision, and detection-contract lock have a near-1:1 ancestor there. Rebuilding under `remediate/` would duplicate tested logic and risk divergent severity grading. |
| **opComment as DATA inside a trusted envelope** | The parent review comment is JSON-encoded into a CONTROL/DATA envelope delivered via Runner stdin — **never** interpolated as `/sc:troubleshoot "${opComment}"`. | The hardened design supersedes the seed-brief's literal interpolation; OWASP LLM01:2025 + CSA both mandate structurally delimiting untrusted content from instructions. Re-introducing interpolation re-opens the exact injection vuln (SC-2/AC-3). |
| **Ephemeral, disposable Runner** | One sandboxed Runner per trigger against an isolated PR-head checkout; torn down after the run; no state carried between triggers. | GitHub's own self-hosted-runner guidance: ephemerality "limits exposure of sensitive resources from previous jobs." Blast-radius minimization (Willison "limit the blast radius"). Logs/ledger must survive teardown. |
| **Conservative propose-only default** | Autonomy lattice `propose < patch < fix < push < resolve`; default `propose` with no flag. Effective level = min over {flag, authz-projection, validation}, then off-lattice HALT (`needs_human_decision`, exhausted push budget). | Market consensus (Copilot draft-PR, Continue "Level 2 Continuous AI", Anthropic 2026 report) + the #1 incumbent complaint (Copilot over-triggers, ignores intent). Reaching `push` must require explicit flag AND write-permission AND passing validation. |
| **Two-phase intent/outcome state ledger** | On-disk ledger records `intent` before any side-effect and `outcome` after; intent-without-outcome on restart = RESUME (re-verify), never silent re-execute. | Survives Dispatcher restart (the core reason V2.0 leaves V1.0's in-session host). Borrows swarm's atomic-write discipline; the append-only two-phase model is [NET-NEW]. |
| **Single `gh` chokepoint** | Every GitHub-mutating call routes through one `gh_call()` wrapper that unconditionally injects `--repo IronbellyOrg/IronClaude`; no raw `subprocess(["gh", ...])` outside that module. | Fork-only `--repo` is [CODE-VERIFIED] enforced today by prose only (CLAUDE.md); no Python in the repo calls `gh`. A headless daemon cannot rely on prose — a single un-wrapped call re-introduces the upstream-PR-misroute hazard. First code-level enforcement of C5. |

### 14.2 Performance Requirements

| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| Mention-detection latency (poll → trigger seen) | ≤ 30–60s | Dispatcher poll interval; `MIN_POLL_INTERVAL = 30` floor [CODE-VERIFIED in `pr_submit/fsm.py`]. Conditional `If-None-Match`/304 polling keeps cost low between changes. |
| Runner spawn → first action | < 5s after dispatch (sandbox cold-start dependent) | Sandbox cold-start ~90–150ms for microVM (Firecracker/libkrun) per external best practice; measured via audit-log `claude_process_spawn` event timestamp. |
| Runner max wall-clock per trigger | `propose` ≈ 30 turns / `fix` ≈ 60 turns; hard ceiling `timeout_seconds` (default 6300 ≈ 105 min) | `ClaudeProcess.timeout_seconds` [CODE-VERIFIED `process.py`]; `wait()` returns `124` on timeout (bash-compatible). `StuckRun` alert keys on this attribute. Caller MUST pass low `max_turns` (default 100 ≫ propose-30). |
| Large opComment handling | Up to `PROMPT_MAX_BYTES` (16 MiB default, env-overridable) delivered via stdin | Prompt via stdin in 64 KiB chunks, bypassing the 128 KB argv (`MAX_ARG_STRLEN`) ceiling [CODE-VERIFIED `process.py:221-258`]; `PromptTooLargeForArgv` raised pre-spawn for over-cap envelopes. |
| Poll API efficiency under rate limits | Zero secondary-rate-limit trips at steady state | `If-None-Match`/`ETag`/304 conditional requests + `Retry-After`/`X-RateLimit-Remaining` backoff [NET-NEW — 0 in-repo precedent]. |
| Round/push budget convergence | ≤ default 2 rounds per PR (hard cap 5) | `DEFAULT_MAX_ROUNDS = 2`, `HARD_CAP_MAX_ROUNDS = 5` [CODE-VERIFIED `pr_submit/fsm.py`]; round counts as next round only if PR head SHA == bot's recorded push SHA (exact-SHA correlation). |

### 14.3 Security Requirements

| Requirement | Implementation | Compliance |
|-------------|----------------|------------|
| **Prompt-injection containment** | opComment delivered as JSON CONTROL/DATA envelope on stdin, never instruction-interpolated; reasoning Runner holds no secrets and cannot push. | OWASP LLM01:2025; OWASP Top 10 for Agentic Apps (Dec 2025); CSA "delimit untrusted content + minimize tools" — a reviewer/proposer "does not need push." Defends the "Comment and Control" (JHU, Apr 2026) CVE class. |
| **Runner secret isolation (INV-001 / SC-7 / AC-7)** | Runner env built from an empty/allowlist base — **not** `os.environ.copy()`. No `GH_TOKEN`, no push token, no `ANTHROPIC_*` host token in the Runner. Only minimal Claude proxy auth (`~/.aienv` `:4000/cli` base + `T2Model*` ids) enters the sandbox. | ⚠️ **Required code change:** `ClaudeProcess.build_env()` is [CODE-CONTRADICTED] — additive-only `os.environ.copy()` + `env.update(env_vars)` cannot *strip* inherited secrets. Must add an allowlist/`base_env` mode OR build the Runner env from a pre-scrubbed sandbox parent. Gate: `/proc/<pid>/environ` secret-scrape test = 0 hits. |
| **Live per-trigger authorization gate (D5 / C4)** | The **replier** (not the parent-comment author) must hold write/maintain permission, checked live at trigger time via `gh api repos/{owner}/{repo}/collaborators/{login}/permission`. Reject-by-default; unknown/insufficient → polite ack-reject, zero action (AC-1). | [NET-NEW] — 0 in-repo GitHub-authz precedent. Replier is the sole authority; parent author supplies only data. External authz evaluated *outside* the LLM (Teleport: injection "steers systems with legitimate access," so authz must not be model-self-policed). |
| **Fork-only push target (C5 / H5)** | `gh_call()` unconditionally injects `--repo IronbellyOrg/IronClaude`; unit test asserts no argv path can omit it; optional CI grep-guard against raw `gh` outside `gh.py`. Never `--approve`/`--request-changes`; humans merge. | First code-level enforcement of the CLAUDE.md fork-only rule (today prose-only). Severity rubric already forbids merge-state changes — reinforces §20 non-goal. |
| **Short-lived host-side push tokens** | Long-lived read+comment credential lives only in the Dispatcher; push uses a short-lived, narrowly-scoped token minted host-side at push time (OD-2: GitHub App vs fine-grained PAT — open). Secret files `chmod 600`, owner-scoped, sourced via systemd `EnvironmentFile=`. | AWS AgentCore "never put the token in the VM; short-lived scoped token, rotatable/revocable"; GitHub/StepSecurity/Sysdig hardening: short-lived OIDC-style over static PATs; keep secrets off the runner. (Note: `~/.aienv` is content-sourcing model; on-disk it is 644, so cite the chmod-600 discipline on its own merit.) |
| **Sandbox network egress** | Deny-by-default egress; allowlist only the Anthropic proxy (`:4000/cli`), `api.github.com`, and single-repo git. No host home mount; `--dangerously-skip-permissions` is safe **only** because of this boundary. | Coder "Agent Firewall / default-deny egress" (DoD-used); microsandbox/brood-box/cplt deny-all + domain allowlist; GitHub runner guidance "restrict runner network access." |
| **Per-PR mutation lock (fail-closed)** | Per-PR `fcntl.flock(LOCK_EX)` serializes tree mutations and push; a failed lock acquisition for a push **fails closed** (the only in-repo flock precedent — freshness bash hooks — fails *open* and must NOT be copied). | [NET-NEW] in Python. Prevents the "parallel sessions share git index" hazard the repo has hit before. |
| **Immutable audit trail** | Append-only JSONL audit log (closed `EventType` enum) distinct from the state ledger, written atomically, forwarded/persisted before Runner teardown. | NIST AI RMF / ISO 42001 reference audit + injection controls; tamper-evidence (exploits "revert the title and delete the PR to erase evidence"). |

### 14.4 Scalability Requirements

| Dimension | Current Target | Future Target | Approach |
|-----------|----------------|---------------|----------|
| Concurrent PRs / triggers | 1 Runner per trigger, serialized per-PR via `flock` | Bounded concurrent Runner pool across distinct PRs | Disposable per-trigger Runner; per-PR lock prevents tree-mutation races; Dispatcher schedules dispatch. |
| Repositories | Single fork (`IronbellyOrg/IronClaude`) | N/A (fork-scoped by design) | `gh_call()` hard-pins `--repo`; single-repo egress allowlist. Cross-repo is explicitly out of scope. |
| Poll volume vs GitHub rate limits | Steady-state polling within primary rate limit | Backoff-aware adaptive polling | ETag/304 conditional requests + `Retry-After`/`X-RateLimit-Remaining` honoring; ≥30s poll floor. |
| State/ledger growth | Append-only JSONL with truncated-last-line replay tolerance | Periodic compaction/rotation | Atomic `os.replace` snapshot + `O_APPEND` event stream; ledger is SoT, in-memory counters derived from it on startup. |

### 14.5 Data & Analytics Requirements

| Data Type | What to Collect | Why | Storage/Retention |
|-----------|-----------------|-----|-------------------|
| Trigger ledger | `(trigger_comment_id, parsed_flag_hash)` claim key, intent record, outcome record, recorded push SHA | At-most-once trigger claiming; two-phase RESUME after restart; idempotency/dedup across rounds (also keep content `fix_key = sha256(path+line+body)`) | On-disk JSONL, atomic-write; durable across restarts (SoT) |
| Audit event log | Closed `EventType` taxonomy: `poll`, `trigger_seen`, `authz_check`, `parse_mention`, `intent`, `claude_process_spawn`, `validation`, `push`, `reply_posted`, `thread_resolved`, `round_outcome`, terminal states | Tamper-evident provenance; debugging; NIST AI RMF / ISO 42001 evidence; "every trigger + exact opComment input + decision" | Append-only JSONL (distinct from ledger); dual `jsonl`+`md` writer; forwarded before Runner teardown |
| Probe-locked detection constants | Augment bot login, `in_reply_to_id` shape, `databaseId` shape (captured from a throwaway fixture PR before parser code) | §21.3 probe-first gate; locks unknown GitHub-API shapes against real bytes via `DetectionContractLocked` | Committed config constants/fixtures |
| Runner run logs | `claude -p` stream-json output, exit code, applied-edits count, validation status | StuckRun detection (timeout→124); push-decision predicate inputs; round correlation | Per-trigger log file; persisted before sandbox teardown |
| Adversarial injection test corpus | Public PoC payloads (hidden `-- Additional instruction --` blocks, `gh issue edit $TOKEN` exfil, white-on-white text, fake "authorized/urgent" framing) | Release-blocking injection-containment acceptance gate (OWASP #7 / CSA red-team gate) | Test fixtures under `tests/cli/remediate/` |

**Analytics Tools:** Native JSONL ledger + audit log queried via `gh`/`jq`-style tooling and the `superclaude remediate` status surface; no external analytics dependency. Provenance/audit is surfaced as a first-class queryable artifact (governance-by-design positioning).

---

## 15. Technology Stack

### 15.1 Backend

| Layer | Technology | Version | Notes |
|-------|------------|---------|-------|
| Language | Python | ≥ 3.10 | Project standard; all ops via UV ([CODE-VERIFIED] `pyproject.toml`, `>=3.10`). |
| CLI framework | Click | ≥ 8.0.0 | `remediate_group` registered in `cli/main.py` via deferred-import idiom [CODE-VERIFIED at `:400-438`]; pin `name="remediate"`. |
| Agent executor | `ClaudeProcess` wrapping `claude --print` (`claude -p`) | reuse (`cli/pipeline/process.py:72`) | Headless spawn: stdin prompt delivery (chunked 64 KiB, EINTR-retry, BrokenPipe-safe), 16 MiB pre-spawn guard, process-group kill (`os.setpgrp`→`os.killpg`), `timeout_seconds`, `stream-json` output, lifecycle hooks. **Required mods:** allowlist `build_env()` + `cwd`/`os.chdir` for sandbox checkout. |
| Decision core | `superclaude.pr_submit` (`fsm`, `severity_router`, `classifier`, `detection`, `models`) | reuse (built+tested) | Import the pure brain; supply real I/O hands. Provides autonomy gate, 5-predicate push conjunction, `should_halt_rounds` (`>=` fence-post), severity remap, `DetectionContractLocked`, `EventType` enum, dual-shape login parser. |
| LLM models | Claude via `~/.aienv` proxy | `:4000/cli` base, `T2Model*` ids | Only credential class allowed into the sandbox; all GitHub creds stay host-side. Default to most-capable Claude for the reasoning Runner. |
| Severity routing | `sc-auggie-review-protocol/refs/severity-rubric.md` + `pr_submit.severity_router` | reuse | 5 tiers (Critical/High/Medium/Low/Nit); Augment severity is a hint, re-graded. Routes Critical/High→`--depth deep --fix`, Medium→`--fix`, Low/Nit→report-only, unknown→Medium fail-safe. |
| State store | JSONL ledger + audit log | — | Atomic write via `os.replace` (not `os.rename`) + randomized same-dir tmp + `finally` cleanup (precedent: `cli/recommend/cache.py`, `swarm/state.py`); `O_APPEND` event stream; `fcntl.flock` (fail-closed) [NET-NEW in Python]. |
| GitHub I/O | `gh` CLI (REST + GraphQL via `gh api graphql`) | — | Polling/ingest (ETag/304), `in_reply_to_id` parent resolution, reply-to-thread (`pulls/<N>/comments/<id>/replies`), `resolveReviewThread` + `reviewThreads`/`databaseId` pagination [NET-NEW in Python; a reference bash flow exists in the untracked parallel V1 `sc-pr-submit-protocol/scripts/reply-resolve-thread.sh`, no committed Python caller]. All routed through `gh_call()` `--repo` injector. |

### 15.2 Frontend / Control Surface

| Layer | Technology | Version | Notes |
|-------|------------|---------|-------|
| User interface | GitHub PR review-comment `@bot` mention grammar | N/A | **No GUI / web / new slash command.** The entire user-facing control surface is a ~4-token comment grammar: autonomy level (`propose\|patch\|fix\|push\|resolve`), `--depth`, `--scope`, `--rounds`. Default (no flag) = `propose`. |
| Operator surface | `superclaude remediate` CLI + systemd | N/A | Operator-facing only; status/ledger inspection. End users never touch the CLI. |

### 15.3 Infrastructure

| Component | Technology | Notes |
|-----------|------------|-------|
| Long-lived host | systemd service (Dispatcher) | `Restart=always`, `WatchdogSec`/`sd_notify` supervision; `EnvironmentFile=` for chmod-600 secrets. `deploy/remediate-bot/` [NET-NEW — no `deploy/` dir, no `.service` units in repo today]. |
| Execution sandbox (Runner) | Container or microVM — **OD-1 open** | External consensus: shared-kernel containers insufficient for untrusted-comment-driven code; production pattern is Firecracker/gVisor/Kata/libkrun microVM or Landlock+seccomp (cplt-style). Refs: microsandbox, brood-box, cplt. Deny-by-default egress; no host home mount; ephemeral PR-head checkout. |
| Containerization (MCP only, not Runner) | Docker (existing, MCP-gateway only) | [CODE-VERIFIED] the only in-repo Docker usage is `install_mcp.py` for the MCP gateway — NOT a code-execution sandbox. Runner sandbox is greenfield. |
| Secret management | systemd `EnvironmentFile=` + short-lived push tokens | Long-lived read+comment creds in Dispatcher; push token minted host-side, narrowly scoped, rotatable (OD-2: App vs fine-grained PAT). |
| CI/CD | GitHub Actions (existing project CI) + UV | `make lint` (ruff check) + `ruff format --check` + `make verify-sync` + `uv run pytest`. Doc⇆CLI parity test for the `remediate` group. |
| Monitoring / alerting | Audit-log events + `StuckRun` alert | Keys on `ClaudeProcess.timeout_seconds` (timeout→124); `claude_process_spawn`/`exit` lifecycle hooks emit audit events. |
| Logging | Dual-format JSONL + Markdown writer | Precedent: `cli_portify/logging_.py` (`execution-log.{jsonl,md}`). Audit log distinct from state ledger; forwarded before Runner teardown. |
| Testing | pytest (via UV) | `tests/cli/remediate/` [NET-NEW]; mirror `tests/cli/test_cli_registration.py`; release-blocking adversarial injection suite. |
| Build system | hatchling (PEP 517) | Project standard; package `superclaude`. |

> **Open technical decisions carried into TDD (from research):**
>
> 1. **OD-1 — Sandbox tech** (container vs microVM): gates R4/S2/§15; largest greenfield surface; resolve early.
> 2. **`build_env()` allowlist mechanism**: add `env_mode="allowlist"`/`base_env` to the shared `ClaudeProcess` primitive (touches sprint/swarm/pipeline — needs regression gate) vs. scrub env in the sandbox parent. Gated by AC-7 secret-scrape test.
> 3. **`ClaudeProcess` `cwd`**: add a `cwd` kwarg vs. `os.chdir` in the one-shot Runner entrypoint.
> 4. **OD-2 — Push-token mechanism**: GitHub App vs fine-grained PAT.
> 5. **§21.3 probe-first gate** (hard prerequisite): lock `in_reply_to_id`/`databaseId`/Augment-bot-login + `resolveReviewThread` GraphQL shape against a throwaway fixture PR before any parser/threading code — the #1 build-blocking unknown no existing code can resolve.
> 6. **Citation corrections** (pre-TDD doc fixes): swarm `commands.py:2269` is a `--watch` iteration cap, not a durable counter — re-point round counter to `pr_submit/fsm.py:should_halt_rounds` and persistence to `swarm/state.py:write_state`; `os.rename`→`os.replace`.

---

## 16. User Experience Requirements

> **Scope note:** This is a feature PRD. The product's entire "interface" is a four-token
> `@`-mention comment grammar plus an operator-facing systemd service — there is **no GUI, no web
> surface, and no new end-user slash command** [research 08 §3]. Accessibility (16.3) and
> localization (16.4) are therefore N/A for this feature and defer to the Platform PRD. The
> substance of this feature's UX lives in the core user flows (16.2).

### 16.1 Onboarding & Interaction Experience

The "user" splits into two roles, each with a distinct first-touch experience [research 08 §3]:

| Role | First-touch experience | Target | Source basis |
|------|------------------------|--------|--------------|
| **Repo maintainer / reviewer** (trigger-er) | Reply to a PR review comment with `@bot <level> [flags]` | Single comment; ≤4 whitelisted tokens to learn | research 08 §3 (control surface = mention grammar) |
| **Operator** (deploys the daemon) | Install the systemd Dispatcher unit + sandbox image (`deploy/remediate-bot/`) | Greenfield deploy; no `deploy/` precedent in-repo today [CODE-VERIFIED absent, research 04/08] | research 04 §6, 08 §2 |

**Time-to-first-value (proposed targets, latency-bound by design):**

| Metric | Proposed target | Rationale / source |
|--------|-----------------|--------------------|
| Mention → Dispatcher detection | ≤ 30–60 s (poll-bound) | `MIN_POLL_INTERVAL = 30` is [CODE-VERIFIED] in `pr_submit/fsm.py`; spec floors polling at ≥30 s [research 04/06/08] |
| Mention → first thread reply (propose) | Set an explicit target; benchmark bar is PR-Agent "single LLM call, ~30 s"; avoid Copilot's criticized 90 s+ cold-start stop-go UX | research web-01 Rec 5 |
| Tokens-to-learn the control surface | 4 (autonomy level + `--depth` + `--scope` + `--rounds`) | research 08 §3 |

> **Important:** The conservative **propose-only default** (no flag ⇒ `propose`) is the dominant
> UX decision [research 08 §3]. It directly answers the market leader's #1 documented complaint:
> GitHub Copilot Coding Agent unconditionally opens a child PR "even when the comment says don't…
> intent is ignored, no middle ground" (GitHub Community #190027) [research web-01 §1.2]. Every
> credible source converges on propose-by-default / human-approves / agent-cannot-self-merge
> [research web-01 §5.1, web-02 §4, web-03 §1].

### 16.2 Core User Flows

| Flow | Steps | Success Criteria | Source |
|------|-------|------------------|--------|
| **F1 — Happy path: authorized `fix`** | (1) Augment/human leaves a PR review comment flagging an issue → (2) authorized collaborator replies `@bot fix --depth deep` → (3) Dispatcher polls (≤30–60 s), runs live authz gate on the **replier**, claims the trigger in the ledger, resolves the **parent** comment as `opComment`, parses whitelisted flags → (4) sandboxed Runner checks out PR-head, runs `/sc:troubleshoot` against `OP_COMMENT_JSON.body` **as DATA**, validates, emits a diff (propose) or sandbox-branch commit (fix) → (5) Dispatcher pushes host-side with a short-lived token, replies to the thread with summary + pushed SHA | Authorized fix lands on the PR branch; thread reply carries the summary + SHA; no secret ever entered the Runner env (AC-7) | research 08 §3; web-01 §3.2; web-03 §1.1 |
| **F2 — Unauthorized trigger (read-only user)** | A `read`-permission user `@`-mentions the bot → Dispatcher's live per-trigger collaborator-permission gate rejects the **replier** | Polite ack-reject, **zero action** (AC-1); the parent author supplies only data, never authority | research 08 §3 (critical UX safety property) |
| **F3 — Escalation to `push`/`resolve`** | Trigger-er specifies an explicit higher autonomy flag | `push` is reachable **only** with: explicit flag **AND** write-permission **AND** passing validation (lattice-min); `resolve` additionally resolves the review thread | research 08 §3; lattice `propose<patch<fix<push<resolve` (research 01/05) |
| **F4 — `needs_human_decision` HALT** | Runner classifies the finding as needing a human decision (ambiguous intent / security trade-off / API-contract change / multiple valid fixes) | Item **HALTs**; never auto-pushed, even at higher autonomy levels (inherits V1.0 FR-4.4). ⚠️ The HALT machinery is [CODE-VERIFIED] consumed in `pr_submit/fsm.py`, but **no Python code sets the flag today** — the populator is agent/skill-driven [CODE-VERIFIED gap, research 06] | research 01/05/06 §8 |

**UX safety invariants (the experience is defined by what the bot will NOT do):**

- The **replier is the sole authority**; the parent comment author supplies only data [research 08 §3].
- The bot uses **`--comment` only — never `--approve`/`--request-changes`**; humans merge. This is an existing, [CODE-VERIFIED] cultural invariant in the severity rubric ("the verdict does NOT translate into a `gh pr review --approve`") [research 07/08].
- Clear **AI provenance** on generated commits/PRs is a market expectation; the `Co-Authored-By` debate is about provenance/accountability, not authorship [research web-03 §1.4].

### 16.3 Accessibility Requirements

| Requirement | Standard | Implementation |
|-------------|----------|----------------|
| GUI accessibility (WCAG, keyboard nav, screen reader, color contrast) | **N/A for this feature** | No GUI/web surface exists; the interface is a GitHub PR comment + a headless systemd service [research 08 §3]. Defer to the Platform PRD for any platform-level surface. |

### 16.4 Localization Requirements

| Requirement | Priority | Status |
|-------------|----------|--------|
| Multi-language UI | **N/A for this feature** | The control surface is a fixed-token English `@`-mention grammar; no localized UI strings [research 08 §3]. Defer to the Platform PRD. |

---

## 17. Legal & Compliance Requirements

> **Scope note:** This feature's primary compliance surface is **data handling of untrusted GitHub
> comment text** and the **audit trail** of autonomous actions. The broader regulatory frameworks
> below are included because the external research establishes them as table-stakes vocabulary for
> the on-prem / regulated segment this product targets — and because the feature's split-host
> architecture is what makes those postures attainable. Platform-level certification ownership
> (SOC 2 audit, formal DPA) defers to the Platform PRD.

### 17.1 Regulatory & Standards Compliance

| Regulation / Standard | Requirement | How this feature's design addresses it | Status / Source |
|-----------------------|-------------|-----------------------------------------|-----------------|
| **EU AI Act (high-risk)** | High-risk compliance obligations; deadline **August 2026** | On-prem split-host model sidesteps the `pull_request_target` secret-injection exposure entirely (secrets live with the Dispatcher, never in the Runner that sees untrusted text); procurement-grade differentiator | ⬜ Proposed positioning [research web-01 §3.4] |
| **OWASP LLM01:2025 Prompt Injection** + **OWASP Top 10 for Agentic Apps** (Dec 2025) | Prompt injection named the #1 LLM/agentic risk; "no fool-proof prevention exists" → mandates defense-in-depth | `opComment` treated as untrusted data inside a trusted prompt envelope; tool minimization (Runner cannot push); propose-only default; secret separation; bounded scope — each maps 1:1 to an OWASP control | ⬜ Standards-aligned by construction [research web-02 §2.4, web-03 §2.1] |
| **CSA GitHub-Actions research note** (May 2026) | "Architectural separation of the reasoning layer from the credential-holding execution layer" prescribed as **the fundamental mitigation** | Runner = reasoning layer (no host secrets, processes untrusted text); Dispatcher = credential-holding execution layer (holds tokens, evaluates structured output against policy, never processes untrusted input) — a 1:1 description of the design | ⬜ Architecture prescribed by industry body [research web-01 §3.2, web-03 §2.2] |
| **NIST AI RMF / ISO 42001** | Now reference specific prompt-injection prevention/detection + sandboxing controls | On-prem + sandbox + audit-ledger + least-privilege design satisfies referenced controls; trigger ledger provides evidence | ⬜ Compliance accelerant [research web-02 §4, web-03 §4.2] |
| **SOC 2 / GDPR / ISO 27001 / data residency** (FedRAMP, HIPAA) | Code/data cannot leave the VPC; certifications are table-stakes for regulated buyers | On-prem, no-third-party-Action posture keeps code behind the corporate firewall; sidesteps GitHub-Actions supply-chain surface (tj-actions, GhostAction, trivy-action) | ⬜ Roadmap signposting; segment competitors (Tabnine SOC2 Type II, Windsurf FedRAMP High/DoD IL5/ITAR) lead with these [research web-01 §2.2, web-02 §2/§3] |
| **Fork-only PR targeting (C5)** — internal governance | Every GitHub-mutating call must pin `--repo IronbellyOrg/IronClaude`; no push to upstream | H5 `gh_call()` chokepoint **unconditionally injects** `--repo`; first *code-level* enforcement of a rule that is **prose-only today** (CLAUDE.md + skill markdown), and which previously failed (PR mis-targeted to upstream) | ⬜ Net-new hardening [CODE-VERIFIED prose-only today, research 03/04/05/06] |

### 17.2 Data Privacy & Handling

| Data Type | Collection Purpose | Retention | Handling / User Rights |
|-----------|--------------------|-----------|------------------------|
| **`opComment` (parent review-comment body)** | Input to remediation; the issue to be fixed | Captured in the trigger ledger as the exact triggering input | Treated as **untrusted DATA**, JSON-encoded in a CONTROL/DATA envelope delivered via stdin — **never** shell-interpolated as `/sc:troubleshoot "${opComment}"` [research 08 §5, web-02 §2]. Length-capped (SC-2) under the 16 MiB `PROMPT_MAX_BYTES` guard [CODE-VERIFIED `process.py`, research 01/08] |
| **Trigger ledger record** (trigger id, exact `opComment`, replier identity, authz result, decision, outcome, pushed SHA) | At-most-once claim mutex + tamper-evident audit provenance | Append-only on-disk (atomic temp + `os.replace`; per-PR `flock`) | Immutable audit log; surfaces "every trigger + exact input + decision" for NIST AI RMF / ISO 42001 evidence and source-traceability [research web-02 R4, web-03 §4.2] |
| **GitHub credentials** (`GH_TOKEN`, short-lived push token, `ANTHROPIC_*`) | Host-side push + Claude auth | Held by Dispatcher only; never written into the Runner env | **Secret separation (INV-001/SC-7):** Runner `/proc/<pid>/environ` must contain no `GH_TOKEN`/push token/`ANTHROPIC_*` (AC-7). ⚠️ NOT achievable by `ClaudeProcess.env_vars` alone — `build_env()` is additive over `os.environ.copy()`; requires an allowlist/empty-base env path or a secret-free sandbox parent [CODE-VERIFIED gap, research 01/02/03/06/07/08] |
| **Runner network egress** | Reach Claude proxy + GitHub for the single repo only | Per-run; sandbox is disposable | Deny-by-default egress, allowlist `:4000/cli` proxy + `api.github.com` + single-repo git (INV-015); external log/ledger forwarding before Runner teardown [research web-03 §3, 04 Q-1/Q-6] |

### 17.3 Terms, Policies & Release Gates Required

- [ ] **Adversarial prompt-injection test suite as a release-blocking acceptance gate** — systematic red-teaming against the `opComment`/trigger channel (per CSA, "a standard gate in the deployment review process"); reuse public PoC payloads (hidden `-- Additional instruction --` blocks, `gh issue edit $TOKEN` exfil attempts, white-on-white text, fake "authorized/urgent" framing) [research web-02 R2/§2.3, web-03 R3].
- [ ] **Secret-scrape regression test** — assert `GH_TOKEN`/push-token ∉ Runner env (AC-7) [research 07/08].
- [ ] **`gh` `--repo` injection test** — assert no code path can construct a `gh` argv lacking `--repo IronbellyOrg/IronClaude` (AC-4); optional CI grep-guard against raw `gh` outside `gh.py` [research 03/04/06].
- [ ] **AI-provenance policy** on generated commits/PRs (provenance/accountability, not authorship) [research web-03 §1.4/R7].
- [ ] **Deployment-guidance constraint:** never run the self-hosted Runner against public repos (fork-PR code-execution risk) [research web-03 §3.2].
- [ ] Data Processing Agreement (DPA), Privacy Policy, Acceptable Use Policy — **defer to Platform PRD** (platform-level obligations).

---

## 18. Business Requirements

> **Scope note:** This is a feature of the SuperClaude framework running on the
> **IronbellyOrg/IronClaude** fork; the end user is a repo maintainer / on-call reviewer on that
> fork [research 08 §3]. It has **no independent pricing, monetization, or GTM** of its own —
> 18.1's pricing table is therefore **N/A**, replaced by feature-specific cost drivers. The market
> and competitive data below is included as **strategic justification and positioning context**
> (per the feature-PRD scope guidance), not as a revenue plan. ⚠️ Market-size figures vary 100×+ by
> analyst scope — treat **trend direction and the named use case**, not absolute dollars, as the
> reliable signal [research web-01 §4.1 caveat].

### 18.1 Monetization Strategy

**Pricing Model: N/A** — internal/on-prem capability of the platform; no per-feature pricing or GTM.

**Feature-specific cost drivers (the only "business" cost surface for this feature):**

| Cost driver | Notes | Source |
|-------------|-------|--------|
| **LLM token consumption** | Each trigger spawns a `claude -p` Runner; `max_turns` is the throttle — propose ≈ 30, fix ≈ 60 (default 100 is too high and must be overridden per autonomy level) [CODE-VERIFIED default, research 07/08] | research 07/08 |
| **Sandbox compute** | One ephemeral, disposable sandbox (container/microVM) per trigger; per-PR push budget (default 2, hard cap 5) bounds re-runs [CODE-VERIFIED `DEFAULT_MAX_ROUNDS=2`/`HARD_CAP=5` in `pr_submit/fsm.py`, research 03/04/06] | research 03/04/06 |
| **Daemon residency** | Long-lived Dispatcher (systemd) polling at ≥30 s floor; minimal steady-state cost between triggers | research 04/08 |
| **Industry pricing trend (context)** | Market moving seat-based → usage-based; outcome-based pricing (pay-per-resolved-issue) projected 2028–2030 — relevant if this is ever externalized | research web-01 §4.2, web-03 §4.1 |

### 18.2 Market & Strategic Justification (positioning context)

**Why this feature matters to the business — the competitive whitespace:**

1. **The named, emerging high-value use case.** Analysts explicitly name "**autonomous pull request resolution**" and "**security vulnerability discovery and remediation**" as *emerging high-value* (not yet commoditized) use cases inside a fast-growing agentic-dev market [research web-01 §4.2].
2. **The on-prem × mention-triggered intersection is empty whitespace.** Cloud incumbents (Copilot Coding Agent, Amazon Q, Cursor) lead mention-triggered/autonomous coding but are **cloud-only / not self-hostable** (Copilot Enterprise "cloud-dependent"; Cursor 3/10 self-host). Air-gap leaders (Tabnine, Windsurf, Qodo) ship **inline/IDE assist, not autonomous PR-remediation bots**. **No incumbent occupies both axes** [research web-01 §2.2/§4.4, web-03 §4.2].
3. **The product's value proposition IS the governance posture.** "Governance-by-design" is the dominant 2026 enterprise narrative; autonomy without audit/injection-resistance is "a compliance liability" [research web-03 §4.2/§4.3].

**Competitive landscape (feature-comparison context):**

| Product | Trigger model | Apply model | Self-hostable? | Source |
|---------|---------------|-------------|----------------|--------|
| **This feature (V2.0)** | `@bot` reply on review comment | **Propose-only default**; lattice up to push/resolve, gated | **Yes — on-prem split-host** | research 08, web-01/02/03 |
| GitHub Copilot Coding Agent | `@copilot` / issue assign | Draft PR, never auto-merge | No (GitHub-Actions cloud) | web-01 §1.1, web-03 §1.1 |
| Claude Code `@claude` action | `@claude` mention (Actions `if` convention) | Fix in isolated env / review | No (GitHub-Actions cloud) | web-02, web-03 §1.2 |
| Devin (Cognition) | PR open/update (Actions) | Review + optional fix; pre-push hook blocks agent pushes | No (SaaS) | web-03 §1.3 |
| CodeRabbit / Ellipsis / Qodo Merge / Greptile | Auto-on-PR or command | Review-centric; Ellipsis/Qodo implement fixes | Mostly cloud; Greptile self-host segment | web-01 §1.3, web-02 §1 |
| PR-Agent (Qodo OSS) | `/review` `/improve` tags + CLI | Suggestions, single LLM call ~30 s | Yes (CLI/Docker/Action) | web-01 §1.3, web-03 §1.4 |

**Positioning Statement** (derived from research, not aspirational):
"For **regulated/on-prem engineering teams** who are **structurally locked out of cloud-only PR-fix agents**, the `superclaude remediate` bot is a **mention-triggered, headless, on-prem remediation capability** that **proposes fixes by default and proves it cannot exfiltrate secrets or push unauthorized code**. Unlike GitHub Copilot Coding Agent and the public `@claude` action, it runs the reasoning layer with no host credentials and gates every consequential action on a credential-holding Dispatcher outside the LLM's reach" [research web-01 §1.1, web-02 §2, web-03 §1.1].

### 18.3 Adoption & Strategic Risks (the trust dynamics)

| Factor | Evidence | Implication for this feature |
|--------|----------|------------------------------|
| **Adoption-vs-trust gap** | 84% dev adoption but only ~29–33% trust AI output; SonarSource: 66% refuse to merge without manual review, only 3% trust AI output | Sells *safety & control*, not raw autonomy; propose-only default is the market-validated posture [research web-01 §4.3, web-02 §4] |
| **Over-action erodes trust** | "Every time an AI bot auto-posts a comment a team doesn't agree with, trust erodes… within months half the team mutes the bot"; Copilot's #1 complaint is unconditional triggering | Conservative default + authz gate + intent evaluation is the retention argument, not just safety [research web-01 §1.2/§4.3, web-02 §4] |
| **~95% of GenAI tools "not production-ready"** | Failure mode is poor *workflow integration*, not model capability | Differentiator is integration (systemd daemon + ledger + existing `superclaude` CLI surface), not model power [research web-01 §4.3] |
| **Detection/prompting is not a defense** | 78-study meta-analysis: every tested coding agent vulnerable, >85% adaptive attack success; guardrails reduce but never eliminate | Architecture (isolation + least-privilege + propose-only), not "better guardrails," is the only credible posture [research web-02 §2/§4] |

### 18.4 Go-to-Market & Support

**N/A for this feature** — it is an internal/on-prem platform capability with no independent GTM or
support tier. Any future externalization, support SLAs, and pricing tiers **defer to the Platform
PRD**. The research-supported GTM *direction* (lead with the proven "Comment and Control" threat
class; target regulated segments — defense, finance, healthcare, government, telecom — that are
structurally locked out of cloud-only agents) is recorded here as positioning input only [research
web-01 Rec 1–3, web-02 R1/R6, web-03 R1].

---

## 19. Success Metrics & Measurement

> **Note:** PR Auto-Remediation V2.0 is a greenfield `superclaude remediate` CLI group (the
> `cli/remediate/` package does not exist today — [CODE-VERIFIED]). The metrics below are
> **targets for the built system**, not current measurements. Security-resistance and
> safety-gate metrics are release-blocking; latency/cost metrics are benchmarked against the
> external bar set by comparable products (PR-Agent "~30s, single LLM call"; Copilot cloud
> agent criticized for 90s+ cold-start stop-go UX).

### 19.1 Product Metrics

| Metric | Definition | Target | Measurement Frequency |
|--------|------------|--------|----------------------|
| Authorization-gate correctness | % of triggers where the **replier's** live collaborator permission is evaluated and a read-only/non-collaborator replier is ack-rejected with zero action (AC-1) | 100% | Per-trigger (audit log) |
| Propose-only default adherence | % of mention triggers with no autonomy flag that resolve to `propose` (safest level) | 100% | Per-trigger |
| Intent-respected rate | % of triggers where the bot does **not** act when the comment intent is non-actionable (directly answers Copilot's #1 documented complaint: unconditional child-PR creation even when the comment says "don't") | ≥ baseline (no false action) | Weekly |
| Time-to-first-response | Dispatcher poll-to-acknowledgement latency for a new mention (poll floor is ≥30s — `MIN_POLL_INTERVAL=30` [CODE-VERIFIED in `pr_submit/fsm.py`]) | ack within 1 poll cycle (≤30–60s) | Per-trigger |
| End-to-end remediation latency | Mention → proposed diff / sandbox-branch commit posted (benchmark bar: PR-Agent ~30s; Copilot cloud agent criticized at 90s+) | Set explicit target; large-diff path treated as first-class (compression/chunking) | Per-run |
| Round/loop convergence | % of PRs that terminate within the per-PR push budget (default 2, hard cap 5 — `DEFAULT_MAX_ROUNDS=2`/`HARD_CAP_MAX_ROUNDS=5` [CODE-VERIFIED]) without a runaway loop | 100% (budget never exceeded) | Per-PR |
| Provenance completeness | % of bot-authored replies/commits carrying clear AI provenance + triggering-SHA correlation | 100% | Per-action |

### 19.2 Business Metrics

| Metric | Definition | Target | Measurement Frequency |
|--------|------------|--------|----------------------|
| On-prem differentiation coverage | The bot operates fully headless/on-prem (systemd Dispatcher + `claude -p` Runner), sidestepping the `pull_request_target` secret-injection exposure that underlies most 2026 GitHub-Actions agent CVEs — a capability cloud-only incumbents (Copilot Enterprise "cloud-dependent"; Cursor 3/10 self-host) cannot match | On-prem operation with no third-party Action in the trigger path | Per-release |
| Trust-aligned posture | Default behavior is propose-only + human-approves + agent-cannot-self-merge — the market-validated safe default (Copilot draft-PR; Continue "Level 2 Continuous AI"; Anthropic 2026 "collaborative, not delegated"). Auto-publish bots get muted within months (trust data: ~3–33% trust AI output) | propose-only default; auto-apply opt-in only | Per-release |
| Audit/provenance availability | Trigger ledger + authorization-gate decisions + run logs are queryable, immutable audit artifacts (NIST AI RMF / ISO 42001 reference these controls; "governance-by-design" is the dominant 2026 enterprise narrative) | Immutable per-trigger audit record retained | Continuous |

### 19.3 Technical Metrics

| Metric | Definition | Target | Alerting Threshold |
|--------|------------|--------|--------------------|
| Runner secret-isolation (AC-7) | `/proc/<pid>/environ` of the Runner contains **no** `GH_TOKEN`, no push credential, no `ANTHROPIC_*` token value (INV-001/SC-7). Note: `ClaudeProcess.build_env()` is additive-only `os.environ.copy()` [CODE-VERIFIED] — this target requires an allowlist/replace env path, not the existing `env_vars` param | 0 secrets present | Any secret present → release-block |
| Prompt-injection resistance (AC-3) | Adversarial opComment corpus (hidden `-- Additional instruction --` blocks, `gh ... $TOKEN` exfil attempts, fake "authorized/urgent" framing) cannot cause secret exfiltration or unauthorized push; opComment is delivered as JSON envelope DATA via stdin, **never** interpolated as `/sc:troubleshoot "${opComment}"` (SC-2) | 100% containment on the suite | Any escape → release-block |
| Correct-thread resolution (INV-010) | Reply + GraphQL `resolveReviewThread` always targets the correct thread (matched on `databaseId`); never resolves the wrong thread. No committed Python precedent (a reference bash flow landed in the untracked parallel V1 `sc-pr-submit-protocol` skill); real shape locked by the §21.3 probe gate | 100% correct | Any mismatch → halt H4 |
| At-most-once trigger claiming | Idempotency: each `(trigger_comment_id, parsed_flag_hash)` is claimed exactly once via the two-phase ledger; intent-without-outcome ⇒ RESUME (re-verify), never silent re-execute | 100% exactly-once | Duplicate execution → alert |
| Counter durability (SC-5/SC-6/INV-002) | Round/push counter is disk-authoritative and survives daemon restarts (ledger is SoT; counter derived on startup). Atomic writes via temp + `os.replace` (idiom from `swarm/state.py` / `cache.py` [CODE-VERIFIED] — not the mis-cited `swarm/commands.py:2269` in-memory watch cap) | Survives restart with no loss/double-count | Counter reset on restart → alert |
| Fork-only `--repo` injection (SC-4) | Every `gh` invocation routes through the H5 wrapper that unconditionally injects `--repo IronbellyOrg/IronClaude`; no code path can construct a `gh` argv lacking it (first **code-level** enforcement of C5 — today prose-only in CLAUDE.md) | 0 un-pinned `gh` calls | Any raw `gh` outside `gh.py` → CI fail |
| Egress containment (INV-015) | Runner sandbox enforces deny-by-default network; allowlist limited to the Anthropic proxy (`:4000/cli`), `api.github.com`, and single-repo git | Only allowlisted endpoints reachable | Any other egress → alert |
| `needs_human_decision` HALT integrity | A finding flagged `needs_human_decision` is structurally prevented from shipping as a push (push-gate predicate 3). Risk: no Python code sets this flag today [CODE-VERIFIED] — the populator is agent/skill-driven, so HALT is only as strong as the populator | No `needs_human_decision` item ever auto-pushed | Auto-push of flagged item → release-block |

---

## 20. Risk Analysis

> Probability/Impact scored H/M/L. Risks are grounded in the codebase reuse verification
> (research 01–08) and the external security/market record (web 01–03). The single highest
> cross-cutting risk is prompt injection on untrusted comment text — the dominant agentic-AI
> attack class of 2026, with named CVEs and in-the-wild supply-chain exploits.

### 20.1 Technical Risks

| Risk | Probability | Impact | Mitigation | Contingency |
|------|-------------|--------|------------|-------------|
| **Prompt injection via opComment** — untrusted PR comment steers the agent into exfiltrating secrets or pushing unauthorized code ("Comment and Control", JHU 2026, hijacked Claude Code + Gemini CLI + Copilot from a single crafted comment; "Clinejection" Feb 2026 → live npm supply-chain compromise; 78-study meta-analysis: every coding agent vulnerable, >85% adaptive success) | H | H | Architectural separation = CSA Labs' prescribed "fundamental mitigation": Runner is the credential-less reasoning layer; Dispatcher is the credential-holding execution/policy layer. opComment delivered as JSON envelope DATA via stdin (SC-2), never interpolated. Secret separation removes the "bash tool + secrets" precondition. Adversarial injection test suite as a release-blocking gate (AC-3) | Tighten envelope/tooling; add Dual-LLM quarantine pre-normalization of opComment; revoke push tokens; propose-only blast-radius cap holds |
| **Runner secret leak via additive `build_env()`** — `ClaudeProcess.build_env()` is `os.environ.copy()` + additive `env.update(env_vars)` [CODE-VERIFIED]; passing `env_vars` cannot *subtract* inherited `GH_TOKEN`/push/`ANTHROPIC_*`, so INV-001/SC-7/AC-7 are unsatisfiable as-cited | H | H | Treat R2 as **reuse-with-modification**: add an allowlist/replace env mode to `build_env()` (back-compat, re-tested against sprint/roadmap/swarm callers) OR build the Runner env from a secret-free sandbox parent (§6) — preferred. Gate with the AC-7 `/proc/<pid>/environ` secret-scrape test | If primitive edit regresses shared callers, fall back to sandbox-level minimal environ; never rely on `env_vars` for removal |
| **Wrong-thread resolution (INV-010)** — GraphQL `resolveReviewThread` + `databaseId` pagination has **no committed Python precedent** (a reference bash flow has since landed in the untracked parallel V1 `sc-pr-submit-protocol` skill); threading semantics unproven in Python | M | H | Hard probe-first gate (§21.3): lock `in_reply_to_id`/`databaseId`/Augment-bot-login against a throwaway fixture PR and commit them as config constants **before** any parser/resolve code | If shapes drift, fall back to reply-only (skip resolve); resolve stays behind the lattice `resolve` level |
| **`ClaudeProcess` has no `cwd` parameter** — `Popen` omits `cwd=` [CODE-VERIFIED]; §7's "cwd = sandbox checkout" cannot be met as-is | M | M | Add a `cwd` kwarg to the primitive, OR `os.chdir()` into the PR-head checkout in the one-shot Runner before spawn | Runner-side chdir is safe (disposable process) |
| **`needs_human_decision` has no code populator** — flag is consumed in 5+ FSM sites but **no Python sets it to True** [CODE-VERIFIED]; §8 HALT guarantee rests on an agent/skill self-report | M | H | Build a deterministic populator for the FR-4.4 taxonomy (ambiguous intent / security trade-off / API-contract change / multiple valid fixes), or explicitly document + test the agent-self-report dependency | If self-report unreliable, default ambiguous findings to HALT (fail-safe) |
| **Append-ledger concurrency (flock) net-new in Python** — only bash `flock` precedent exists and it **fails open** (`flock … \|\| true`) [CODE-VERIFIED] | M | M | H1 per-PR push serializer must `fcntl.flock(LOCK_EX)` and **fail-closed** (a failed lock for a push must abort, not fall through) | Serialize all pushes through a single ledger writer; reject on lock contention |
| **Duplication/divergence with in-flight `pr_submit/` core** — V1.0's tested decision core (`fsm`, `severity_router`, `models`, `DetectionContractLocked`) is landing in parallel and is **omitted from the Reuse Map**; rebuilding it under `remediate/` risks two divergent autonomy/severity machines (SoT violation) | M | M | Reconcile in design/TDD: `import superclaude.pr_submit` for the pure decision core, build only the I/O+host layer ("reuse the brain, replace the hands"). Coordinate so V2 host work doesn't race the V1 core landing | If forced to fork, pin a shared rubric/test contract to prevent severity drift |
| **Mis-cited reuse anchors mislead the build** — `swarm/commands.py:2269` is an in-memory `--watch` cap, not a disk-authoritative counter [CODE-CONTRADICTED]; `~/.aienv` is 644 not chmod-600 [CODE-CONTRADICTED] | M | M | Pre-build doc fix: repoint counter→`swarm/state.py`/`pr_submit.should_halt_rounds`, atomic-write→`os.replace`; drop `.aienv` as the chmod-600 exemplar | Treat citations as advisory until re-verified at build time |
| **ETag/304 rate-limit polling net-new** — no `If-None-Match`/`ETag`/`X-RateLimit` precedent in repo [CODE-VERIFIED 0 hits] | M | M | Build conditional-request ingest (D3) with `Retry-After`/`X-RateLimit-Remaining` backoff; poll floor ≥30s | Exponential backoff + jitter; degrade to longer poll interval under rate-limit pressure |

### 20.2 Business Risks

| Risk | Probability | Impact | Mitigation | Contingency |
|------|-------------|--------|------------|-------------|
| **Incumbent dominance (GitHub Copilot Coding Agent)** — GA since Sep 2025; closed-loop review→fix→PR since Mar 2026; the dominant mention→PR-fix workflow | H | M | Differentiate on the open intersection no incumbent occupies: **on-prem × mention-triggered remediation** (Copilot/Amazon Q/Cursor are cloud-only / not self-hostable). Target regulated segments (defense, finance, healthcare, telecom, gov) structurally locked out of cloud runners | Lean into compliance signposting (SOC2/air-gap/zero-retention) as roadmap items |
| **Trust gap suppresses adoption** — 84% adoption vs ~3–33% trust; auto-publishing bots get muted within months; ~95% of GenAI tools "not production-ready" | M | M | Conservative propose-only default + authorization gate + provenance/audit ledger sells *safety and control*; workflow integration (systemd + ledger + existing `superclaude` CLI) is the differentiator, not raw model capability | Keep auto-apply opt-in, per-repo, behind the same authorization layer — never default |
| **Over-action erodes trust** — the market leader's #1 complaint is unconditional triggering / ignored intent | M | M | Live authorization gate + intent evaluation + propose-only is the "middle ground / confirmation step" users explicitly ask for | Add explicit ack-without-action mode for non-actionable comments |

### 20.3 Operational Risks

| Risk | Probability | Impact | Mitigation | Contingency |
|------|-------------|--------|------------|-------------|
| **Sandbox runtime greenfield (OD-1)** — no container/microVM/Firecracker execution harness in repo [CODE-VERIFIED]; external consensus says shared-kernel containers are insufficient for untrusted-code execution (Firecracker/gVisor/Kata/libkrun or Landlock+seccomp recommended) | H | H | Resolve OD-1 early — it gates R4/S2/§15. Evaluate microVM (microsandbox/brood-box) or kernel-LSM (cplt-style `gh`/`git` command guards) as build-vs-buy references; `eval/isolation.py` scratch-root is partial prior art for filesystem confinement only | Start with strongest available isolation tier; propose-only caps blast radius while isolation hardens |
| **systemd/deploy fully greenfield (S2)** — no `deploy/` dir, no `.service`/`WatchdogSec`/`EnvironmentFile` in repo [CODE-VERIFIED]; CLI surfaces are all invoke-and-exit, no long-lived daemon precedent | M | M | Spike the systemd `WatchdogSec`/`sd_notify` integration in Python; chmod-600 `EnvironmentFile` secret-sourcing; external log/ledger forwarding before Runner teardown (ephemerality is "not a complete control" per GitHub's own guidance) | Run Dispatcher under a supervised `Restart=always` unit; forward logs off-host |
| **Probe-first unknowns block the build** — `in_reply_to_id`/`databaseId`/Augment-bot-login shapes are the #1 build-blocking unknown; no code can substitute for a live probe | H | M | Make the throwaway-fixture-PR probe a **hard prerequisite** gate (§21.3) before parser/resolve/authz code; commit captured shapes as fixtures/constants | If probe reveals unstable shapes, narrow scope to reply-only until stabilized |
| **Wrong-repo push (C5) in a headless daemon** — fork-only `--repo` is prose-only today (CLAUDE.md); the daemon is the first autonomous Python `gh` caller; a single un-pinned call re-introduces the upstream-PR hazard | M | H | H5 single-chokepoint `gh_call()` injecting `--repo IronbellyOrg/IronClaude`; unit test asserting no argv omits it; CI grep-guard forbidding raw `subprocess([...,"gh",...])` outside `gh.py`. Build+test H5 first (§21.3) | Disable push autonomy until H5 enforcement test passes |
| **Parallel sessions share git index/HEAD** — concurrent host-side git mutations can corrupt staged state | M | M | Per-PR `flock` (fail-closed) serializes tree mutations; host-side push from an isolated checkout; SHA-correlated round counting | Reject concurrent triggers on the same PR; queue them |
| **`remediation/` stale empty placeholder confused for the home** — top-level `remediation/` exists but is empty [CODE-VERIFIED]; the feature home is `cli/remediate/` | L | L | State explicitly that the feature lives under `src/superclaude/cli/remediate/`; recommend deleting/ignoring the stale `remediation/` dir | Document the canonical path in the TDD |

---

## 21. Implementation Plan

> This section consolidates the full delivery plan: what to build (epics, stories, requirements), how to phase it, what "done" means per phase, and when it lands. Read top to bottom for the complete implementation picture. The decision core is **reused, not rebuilt** (`import superclaude.pr_submit`); the new build is the Dispatcher/Runner host + GitHub I/O.

### 21.1 Epics, Features & Stories

> **Format:** Each epic contains user stories in the format "As a [persona], I want [goal] so that [benefit]". Personas: **Maintainer/On-call Reviewer** (the human who replies `@bot fix`), **Authorized Collaborator** (write-permission replier = the sole action authority), **Operator** (deploys/runs the systemd service), **Security Owner** (accountable for the secret/injection boundary). Components map to the merged-requirements inventory: D = Dispatcher, R = Runner, H = Host-side, S = Shared, T = Test.

#### 21.1.1 Epic Summary

| Epic # | Epic Name | Features | Stories | Priority | Phase |
|--------|-----------|----------|---------|----------|-------|
| 1 | Probe-First De-Risking & Test Harness (T1, §21.3) | 2 | 3 | P0 | Phase 1 |
| 2 | Mention Detection, Grammar & Authorization (D3, D4, D5, D6) | 4 | 6 | P0 | Phase 1–2 |
| 3 | Secure Headless Execution — Sandbox, Envelope, Executor (R2, R3, R4) | 3 | 5 | P0 | Phase 2 |
| 4 | Autonomy & Loop-Safety Governance (H1, H2) | 2 | 5 | P0 | Phase 2 |
| 5 | GitHub Write-Back — Push, Reply, Resolve, `--repo` Injector (H3, H4, H5) | 3 | 5 | P0/P1 | Phase 2–3 |
| 6 | Severity-Based Depth Routing (S1) | 1 | 2 | P1 | Phase 2 |
| 7 | Host Platform & Deployment (D1, D2, S2) | 3 | 4 | P0/P1 | Phase 1 & 3 |

---

#### Epic 1: Probe-First De-Risking & Test Harness

**Description:** Lock the unknown GitHub-API and detection constants from a real throwaway-fixture PR **before** any parser/threading code is written, and stand up an adversarial injection corpus as a release gate. This is the §21.3 hard prerequisite — research 02/04/05/06/08 all confirmed (at research time) that reply/resolve threading, `in_reply_to_id`, `databaseId`, and the Augment bot login had **no in-repo precedent**; a reference bash flow has since landed in the untracked parallel V1 `sc-pr-submit-protocol` skill, but the real byte shapes still cannot be safely inferred without the live probe.

**US-1.1: Lock detection constants from a live probe PR**

- **As a** Maintainer
- **I want** the bot's detection constants (`in_reply_to_id` shape, `databaseId` pagination, `resolveReviewThread` GraphQL shape, Augment bot login) captured from a real throwaway PR and committed as config/fixtures
- **So that** the parser and thread-resolver are built against real bytes, not guesses, and cannot resolve the wrong thread (INV-010)

**Acceptance Criteria:**

- ✅ A throwaway-fixture PR run captures every reply/resolve API shape into committed constants/fixtures (mirrors V1's `DetectionContractLocked` "locked-contract" vessel)
- ✅ No H4 (reply/resolve) or D6 (parent resolution) parser code merges before the probe constants are locked — enforced as a build-sequencing gate
- ✅ Captured Augment bot login is a config constant; a different login is treated as "not detected" (T-211 discipline)

**Success Metrics:**

- Probe completes and locks 100% of the four unknown shapes before parser work begins

---

**US-1.2: Adversarial prompt-injection corpus as a release gate**

- **As a** Security Owner
- **I want** an explicit adversarial injection test suite (hidden `-- Additional instruction --` blocks, `gh issue edit $TOKEN` exfil attempts, white-on-white text, fake "authorized/urgent" framing) run against the Runner envelope
- **So that** "Runner contains injection X" is a release-blocking test, matching the OWASP/CSA recommendation that injection red-teaming be a standard deployment gate

**Acceptance Criteria:**

- ✅ Public PoC payloads (from the "Comment and Control" / Aikido "PromptPwned" corpus) are encoded as test cases
- ✅ A passing injection test asserts the opComment never escapes the DATA envelope and no secret leaves the sandbox
- ✅ The suite is wired as an acceptance gate, not an optional unit test

**Success Metrics:**

- 0 injection payloads escape the envelope; suite blocks release on any escape

---

**US-1.3: Secret-scrape regression test (AC-7)**

- **As a** Security Owner
- **I want** a regression test asserting `GH_TOKEN`, push token, and `ANTHROPIC_*` token values are absent from the Runner's `/proc/<pid>/environ`
- **So that** the Runner secret-isolation invariant (INV-001/SC-7) is mechanically verified, not assumed

**Acceptance Criteria:**

- ✅ Test reads the spawned Runner's environ and asserts `"GH_TOKEN" not in runner_env` and no push/Anthropic-auth token values present
- ✅ Test fails today against the unmodified `build_env()` additive-merge path (proving it is load-bearing)

**Success Metrics:**

- Secret-scrape test green only after the allowlist/sandbox-environ mechanism is in place

---

#### Epic 2: Mention Detection, Grammar & Authorization

**Description:** The trigger pipeline — poll GitHub for `@bot` mention replies (rate-limit-aware), parse the whitelisted flag grammar, run a **live per-trigger authorization gate on the replier**, and resolve the parent comment as the `opComment`. The replier is the sole authority; the parent author supplies only data.

**US-2.1: Rate-limit-aware mention polling (D3)**

- **As an** Operator
- **I want** the Dispatcher to poll GitHub for new `@bot` mention replies using ETag/`If-None-Match` 304 conditional requests, `since=` cursors, and `X-RateLimit`/`Retry-After` backoff, at a ≥30s floor
- **So that** the bot detects triggers promptly without exhausting the API rate limit

**Acceptance Criteria:**

- ✅ Conditional requests return 304 when nothing changed (no quota burn on idle polls)
- ✅ Poll interval is enforced at a ≥30s minimum (mirrors V1 `MIN_POLL_INTERVAL=30`)
- ✅ `Retry-After`/`X-RateLimit-Remaining` headers drive backoff
- ✅ Dual-shape login parsing handled (`{"author":{"login"}}` vs `{"user":{"login"}}` — reuse `pr_submit/classifier._login_of`, already tested)

**Success Metrics:**

- Idle polling consumes 0 rate-limit quota via 304s; trigger detected within one poll interval

---

**US-2.2: Whitelisted mention grammar (D4)**

- **As an** Authorized Collaborator
- **I want** to control the bot with a tiny whitelisted comment grammar — autonomy level (`propose|patch|fix|push|resolve`), `--depth`, `--scope`, `--rounds` — defaulting to `propose` when no level is given
- **So that** I have a simple, predictable control surface with the safest possible default

**Acceptance Criteria:**

- ✅ Only whitelisted tokens are parsed; unknown tokens are ignored or rejected, never executed
- ✅ A mention with no autonomy flag resolves to `propose` (safest)
- ✅ Grammar parsing is independent of the untrusted parent-comment body

**Success Metrics:**

- 100% of no-flag mentions default to `propose`; 0 non-whitelisted tokens reach execution

---

**US-2.3: Live authorization gate on the replier (D5)**

- **As a** Maintainer
- **I want** the bot to check the *replier's* live collaborator permission (`collaborators/{login}/permission`) at trigger time and reject-by-default anyone without write access
- **So that** only authorized humans can cause action, and a `read`-permission user gets a polite ack-reject with zero action (AC-1)

**Acceptance Criteria:**

- ✅ The replier (not the parent author) is the sole action authority
- ✅ A `read`-permission mention produces an ack-reject comment and performs no file write, push, or resolve
- ✅ Authorization is evaluated **outside** the LLM, on the Dispatcher (external-policy enforcement, per OWASP/CSA)
- ✅ Unknown/unfetchable permission → safe default (reject)

**Success Metrics:**

- 0 actions taken on behalf of non-write-permission users across the test corpus

---

**US-2.4: Parent comment resolution as opComment (D6)**

- **As a** Maintainer
- **I want** the bot to resolve the parent review comment (via `in_reply_to_id`) and treat its body as the `opComment` data input
- **So that** the issue flagged in the original review comment is what gets remediated

**Acceptance Criteria:**

- ✅ Parent resolution uses the probe-locked `in_reply_to_id` shape (US-1.1)
- ✅ The resolved `opComment` is carried as DATA only, never as instructions
- ✅ Resolution failure halts the trigger with an explanatory reply rather than guessing

**Success Metrics:**

- Correct parent resolved for 100% of probe-fixture trigger shapes

---

**US-2.5: At-most-once trigger claiming**

- **As an** Operator
- **I want** each detected trigger claimed in the on-disk ledger before dispatch, keyed on `(trigger_comment_id, parsed_flag_hash)`
- **So that** a restart or overlapping poll never double-executes the same mention

**Acceptance Criteria:**

- ✅ A trigger already claimed in the ledger is skipped (idempotency)
- ✅ Claim is written atomically before any Runner is dispatched
- ✅ Claim key is distinct from the cross-round content-dedup `fix_key=sha256(path+line+body)`

**Success Metrics:**

- 0 double-executions across simulated restart/overlap tests

---

**US-2.6: Conservative intent handling (competitive wedge)**

- **As a** Maintainer
- **I want** the bot to never take a consequential action on an ambiguous or "don't do anything" mention
- **So that** it avoids the market leader's #1 documented complaint (GitHub Copilot Coding Agent unconditionally opens a child PR even when told not to — Community Discussion #190027)

**Acceptance Criteria:**

- ✅ Default `propose` + authorization gate together constitute the "middle ground / confirmation step" users request
- ✅ No path reaches `push`/`resolve` without an explicit flag AND write permission AND passing validation

**Success Metrics:**

- 0 unsolicited child-PR / push actions on no-op or question-only mentions

---

#### Epic 3: Secure Headless Execution — Sandbox, Envelope, Executor

**Description:** The reasoning layer. An ephemeral, sandboxed, disposable per-trigger Runner checks out PR-head, runs `claude -p` against a CONTROL/DATA envelope (opComment as JSON DATA via stdin), and emits a diff (propose) or sandbox-branch commit (fix). This is the CSA-prescribed "reasoning layer that holds no credentials" half of the split.

**US-3.1: opComment-as-DATA envelope (R3, SC-2/AC-3)**

- **As a** Security Owner
- **I want** the parent comment delivered to `claude -p` inside a JSON CONTROL/DATA envelope on stdin — **never** shell-interpolated as `/sc:troubleshoot "${opComment}"`
- **So that** attacker-controlled comment text cannot be executed as instructions (the seed-brief's literal interpolation is explicitly superseded by §6)

**Acceptance Criteria:**

- ✅ opComment is JSON-encoded as DATA and delivered via stdin (leveraging `ClaudeProcess` stdin delivery — chunked 64 KiB, EINTR-retry, 16 MiB `PROMPT_MAX_BYTES` guard — [CODE-VERIFIED at `process.py:221-258`])
- ✅ No code path interpolates opComment into an argv or shell string
- ✅ Over-large opComment raises the typed `PromptTooLargeForArgv` before spawn (used for SC-2 length-capping)

**Success Metrics:**

- 0 injection escapes from the DATA boundary (gated by US-1.2)

---

**US-3.2: Credential-free sandboxed Runner (R4, INV-001/INV-015)**

- **As a** Security Owner
- **I want** the Runner to execute in an ephemeral sandbox with a minimal environment (no host home mount, no `~/.aienv` secrets, no `GH_TOKEN`/push token), `cwd` = the disposable PR-head checkout, and deny-by-default egress allowlisting only `:4000/cli` (Anthropic proxy) + `api.github.com` + the single-repo git endpoint
- **So that** even a successful injection cannot exfiltrate secrets or reach the network broadly (blast-radius minimization)

**Acceptance Criteria:**

- ✅ Runner env contains no push/Anthropic-auth token values (AC-7, verified by US-1.3)
- ✅ Runner `cwd` is the PR-head checkout — note `ClaudeProcess` has **no `cwd` parameter** today ([CODE-CONTRADICTED at `process.py:192`]); resolved by a new `cwd` kwarg or a Runner-side `os.chdir()` (TDD)
- ✅ Egress is deny-by-default with the §6 allowlist; the Anthropic proxy host must be reachable from the chosen sandbox topology (OD-1)
- ✅ Runner only edits files inside the sandbox workspace (write-scope confinement; mechanism ports from `roadmap/remediate_executor.py::enforce_allowlist`, policy widens from named files to "inside the sandbox")
- ✅ `--dangerously-skip-permissions` (the `ClaudeProcess` default, [CODE-VERIFIED at `process.py:93`]) is safe **only because** of the sandbox boundary — the safety is in the sandbox, not the flag

**Success Metrics:**

- Secret-scrape (US-1.3) green; 0 writes outside the workspace; egress blocked to all non-allowlisted hosts

---

**US-3.3: Headless remediation executor (R2)**

- **As a** Maintainer
- **I want** the Runner to spawn `claude -p` via the `ClaudeProcess` primitive with caller-set `max_turns` per autonomy level (≈30 propose / ≈60 fix), `output_format="stream-json"`, and process-group kill on teardown
- **So that** the remediation runs headlessly, streams progress, and is cleanly killable / timeout-bounded

**Acceptance Criteria:**

- ✅ Executor wraps `ClaudeProcess` ([CODE-VERIFIED at `process.py:72`; `build_command()` flag string verified at `:121-143`]); `roadmap/remediate_executor.py` (which already runs `ClaudeProcess` for remediation with snapshot/rollback/retry/diff-size guards) is the primary executor reuse reference
- ✅ `max_turns` is passed explicitly per level (default 100 is too high for propose — caller must override)
- ✅ Process-group kill (`os.setpgrp` → `os.killpg`) and `timeout_seconds`→124 are honoured for sandbox teardown / `StuckRun` alerting
- ✅ Lifecycle hooks (`on_spawn`/`on_signal`/`on_exit`) feed the §14 audit events

**Success Metrics:**

- Runner spawns, streams, and tears down cleanly; stuck runs alert at `timeout_seconds`

---

**US-3.4: Validation before any commit/diff**

- **As a** Maintainer
- **I want** the Runner to validate its own change (tests/coherence) and emit a diff (propose/patch) or sandbox-branch commit (fix) only when validation passes
- **So that** a failed remediation never advances toward push

**Acceptance Criteria:**

- ✅ Validation-fail short-circuits before push (push-decision predicate 2, reused from `fsm.evaluate_push_decision`)
- ✅ Propose/patch emit a patch bundle; fix emits a sandbox-branch commit (no host-side push from the Runner)

**Success Metrics:**

- 0 pushes proceed on validation failure

---

**US-3.5: Snapshot / rollback discipline**

- **As a** Maintainer
- **I want** per-file snapshot + rollback around Runner edits
- **So that** a partial or incoherent remediation can be reverted within the sandbox

**Acceptance Criteria:**

- ✅ Snapshot/restore reuse the atomic read→tmp→`os.replace` discipline (`roadmap/remediate_executor.py` `create_snapshots`/`restore_from_snapshots`)
- ✅ Cross-file coherence checked before emitting the change

**Success Metrics:**

- Incoherent multi-file fixes rolled back, not emitted

---

#### Epic 4: Autonomy & Loop-Safety Governance

**Description:** The execution-layer policy. A two-phase intent/outcome ledger and an autonomy gate that caps effective autonomy at the lattice-min and HALTs on off-lattice conditions (`needs_human_decision`, exhausted push budget).

**US-4.1: Effective-autonomy lattice cap (H2, §8)**

- **As a** Security Owner
- **I want** effective autonomy computed as the minimum over the lattice of {requested flag, authorization projection, validation status}, then short-circuited to HALT on off-lattice conditions
- **So that** the bot can never act above the most restrictive applicable ceiling

**Acceptance Criteria:**

- ✅ Effective level = `min` over the lattice; e.g. a `push`-flag from a write-collaborator whose validation failed cannot reach push
- ✅ Reuses/extends V1 `fsm.evaluate_push_decision` (5-predicate G-push conjunction, tested) — predicates 2–5 (validated / no-human-decision / under-budget / real-work) carry over verbatim; predicate 1 (`monitor_ordinal>=3`) drops out under the mention-triggered model; a new authorization-projection predicate is added
- ✅ Structurally impossible to construct a push for a `needs_human_decision` item (subject to Open Question #8 — the populator)

**Success Metrics:**

- 0 actions above the computed effective ceiling

---

**US-4.2: `needs_human_decision` HALT (inherited V1.0 FR-4.4)**

- **As a** Maintainer
- **I want** any item classified `needs_human_decision` to HALT and post a PENDING reply — even at the top autonomy level — never auto-applying a default
- **So that** ambiguous-intent / security-trade-off / API-contract / multiple-valid-fix items are escalated to a human, not shipped

**Acceptance Criteria:**

- ✅ HALT short-circuits before push regardless of requested level (the flag is consumed in `pr_submit/fsm.py` pre-gate at `:204`/`:353` and push predicate 3 at `:158`)
- ✅ A deterministic populator sets the flag, OR the agent-self-report dependency is explicitly documented (Open Question #8)

**Success Metrics:**

- 100% of `needs_human_decision` items HALT to PENDING; 0 auto-applied

---

**US-4.3: Per-PR push budget with SHA-correlation (H1, §9)**

- **As a** Maintainer
- **I want** a per-PR push budget (default 2, cap 5) where a re-review counts as the next round **only if** the PR head SHA equals the bot's recorded push SHA
- **So that** the bot cannot enter an infinite remediation loop

**Acceptance Criteria:**

- ✅ Monotonic budget counter with `>=` fence-post (reuse `fsm.should_halt_rounds` semantics, not swarm `:2269`)
- ✅ Round increments only on exact SHA-match between re-review and recorded push
- ✅ Budget exhaustion posts a cap-summary and stops

**Success Metrics:**

- 0 unbounded loops; budget enforced across SHA-correlation tests

---

**US-4.4: Two-phase intent/outcome ledger (H1, §10)**

- **As an** Operator
- **I want** a durable, disk-authoritative, restart-surviving ledger that writes an intent record before each consequential action and an outcome record after
- **So that** a crash mid-action is recovered as RESUME (re-verify), never as silent re-execute

**Acceptance Criteria:**

- ✅ Atomic writes via tmp + `os.replace` (idiom from `swarm/state.py` / `recommend/cache.py` / `install_hooks.py:443`); append-only JSONL via `O_APPEND`
- ✅ Per-PR `flock` serializes tree mutations and **fails-closed** (inverting the fail-open bash freshness hooks)
- ✅ Intent-without-matching-outcome on startup ⇒ RESUME/re-verify path; the ledger is SoT and the counter is derived from it on startup (not the reverse)
- ✅ Tolerates a truncated last line on replay

**Success Metrics:**

- 100% of simulated crash windows recover as RESUME; 0 silent re-executions

---

**US-4.5: Tamper-evident audit log (§14)**

- **As a** Security Owner
- **I want** an immutable audit log (distinct from the state ledger) recording every poll, authz check, mention parse, intent, process spawn, validation, push, reply, and round outcome with the exact triggering input
- **So that** every action is traceable for governance/compliance (NIST AI RMF / ISO 42001 evidence)

**Acceptance Criteria:**

- ✅ Closed-enum event taxonomy, started from `pr_submit/models.py::EventType` (~70–80% overlap) and extended with authz/mention/intent/`claude_process_spawn` events; in-session-only events dropped
- ✅ Dual-format jsonl+md writer (idiom from `cli_portify/logging_.py`); logs forwarded/persisted before Runner teardown

**Success Metrics:**

- 100% of consequential actions have a matching audit event with the triggering input

---

#### Epic 5: GitHub Write-Back — Push, Reply, Resolve, `--repo` Injector

**Description:** The credential-holding side-effects, performed host-side by the Dispatcher (never the Runner). Push with a short-lived token, reply to the review thread with a summary + SHA, resolve the thread at the `resolve` level — all through a single `gh` chokepoint that unconditionally pins the fork repo.

**US-5.1: Fork-only `--repo` injector chokepoint (H5, C5/SC-4)**

- **As a** Security Owner
- **I want** every GitHub-mutating call to route through a single `gh_call()` that unconditionally injects `--repo IronbellyOrg/IronClaude`, with no code path able to omit it
- **So that** autonomous pushes/replies can never land on the public upstream (the prose-only discipline that previously misfired)

**Acceptance Criteria:**

- ✅ This is the **first code-level enforcement** of C5 — today `--repo` is enforced only by CLAUDE.md prose ([CODE-VERIFIED: 0 Python `gh` callers in the repo]); the injector is net-new [NEW]
- ✅ A unit test asserts no constructed `gh` argv can lack `--repo IronbellyOrg/IronClaude`
- ✅ Optional CI grep-guard forbids raw `subprocess([... "gh" ...])` outside `gh.py`

**Success Metrics:**

- 0 `gh` invocations without `--repo`; 0 actions on the upstream repo

---

**US-5.2: Host-side push with short-lived token (H3)**

- **As an** Operator
- **I want** the validated change pushed host-side by the Dispatcher using a short-lived, narrowly-scoped token — never from inside the Runner
- **So that** the push capability lives entirely outside the untrusted-text-processing layer (CSA "fundamental mitigation")

**Acceptance Criteria:**

- ✅ Push occurs only after the autonomy gate authorizes it (Epic 4) and validation passed (Epic 3)
- ✅ Token is short-lived/revocable (OD-2); never written into the sandbox
- ✅ Never modifies merge state — strictly no `--approve`/`--request-changes`/merge (inherited from the auggie-review `--comment`-only discipline; §20 "humans merge")

**Success Metrics:**

- 100% of pushes are host-side with a scoped token; 0 merge-state mutations

---

**US-5.3: Reply-to-thread + resolve (H4, §12, INV-010)**

- **As a** Maintainer
- **I want** the bot to reply to the originating review thread with a summary + pushed SHA, and at the `resolve` level resolve the thread via GraphQL `resolveReviewThread` matched on `databaseId`
- **So that** the conversation is closed on the exact thread that triggered it, with no mis-resolution

**Acceptance Criteria:**

- ✅ Reply uses the `pulls/<N>/comments/<parent_id>/replies` endpoint (templated from auggie-review's posting precedent; reply/resolve are net-new in Python — a reference bash flow exists in the untracked parallel V1 `sc-pr-submit-protocol/scripts/reply-resolve-thread.sh`, but no committed/tracked Python caller exists) [NEW]
- ✅ Resolve matches the correct thread by `databaseId` (probe-locked shapes from US-1.1); never resolves a sibling thread (INV-010)
- ✅ Resolve only at the `resolve` autonomy level

**Success Metrics:**

- 100% correct-thread resolves on probe fixtures; 0 mis-resolutions

---

**US-5.4: Summary reply with provenance**

- **As a** Maintainer
- **I want** each bot reply to carry clear AI provenance and the pushed SHA
- **So that** reviewers can trace what the bot did and why (market demand for source traceability)

**Acceptance Criteria:**

- ✅ Reply includes pushed SHA, autonomy level used, and AI provenance marker
- ✅ Provenance is explicit (not a silent commit)

**Success Metrics:**

- 100% of bot replies carry SHA + provenance

---

**US-5.5: Ack-reject reply for unauthorized triggers**

- **As an** Authorized Collaborator
- **I want** a polite ack-reject reply when a non-write-permission user mentions the bot
- **So that** unauthorized users get clear feedback while zero action is taken (AC-1)

**Acceptance Criteria:**

- ✅ Ack-reject posts a comment and performs no file write / push / resolve
- ✅ The event is audit-logged

**Success Metrics:**

- 100% of unauthorized mentions get an ack-reject with 0 side-effects

---

#### Epic 6: Severity-Based Depth Routing

**Description:** Re-grade each finding through the auggie-review severity rubric and route remediation depth accordingly — Augment severity is a hint, not authoritative.

**US-6.1: Severity-to-depth routing (S1, §17)**

- **As a** Maintainer
- **I want** each finding re-graded via the severity rubric and routed by tier — Critical/High → `--depth deep --fix`, Medium → `--fix`, Low/Nit → report-only, unknown → Medium fail-safe
- **So that** remediation effort matches the real severity, not the raw Augment hint

**Acceptance Criteria:**

- ✅ Routing reuses `pr_submit/severity_router.remap_severity()` + `route()` **by import** ([CODE-VERIFIED]: pure, encodes the rubric's category floor/ceiling table, never emits the `--depth quick --fix` conflict) rather than re-parsing `severity-rubric.md`
- ✅ Augment `severity_hint` is treated as a starting point and remapped (the rubric's own stated contract)
- ✅ Unknown severity defaults to Medium (fail-safe)

**Success Metrics:**

- 100% of findings routed by remapped (not raw) severity; 0 depth/flag conflicts

---

**US-6.2: No merge-state changes from severity verdicts**

- **As a** Security Owner
- **I want** severity verdicts to never translate into `gh pr review --approve`/`--request-changes`
- **So that** merge decisions remain with humans (a code-enforced cultural invariant the rubric already states)

**Acceptance Criteria:**

- ✅ No severity tier maps to a merge-state mutation

**Success Metrics:**

- 0 approve/request-changes actions

---

#### Epic 7: Host Platform & Deployment

**Description:** The operational shell — a `superclaude remediate` CLI group, a long-lived supervised Dispatcher daemon, and the systemd + sandbox-image deploy story. Entirely greenfield (no `deploy/` dir, no service/long-lived-daemon precedent in the repo).

**US-7.1: `superclaude remediate` CLI group (D1)**

- **As an** Operator
- **I want** the bot delivered as a `superclaude remediate` CLI group (not a skill), mirroring sprint/swarm/pipeline
- **So that** it runs headless outside any Claude session and composes with existing tooling

**Acceptance Criteria:**

- ✅ `remediate_group` registered in `cli/main.py` via the deferred-import + `main.add_command(remediate_group, name="remediate")` idiom with the mandatory `# noqa: E402,I001` annotation ([CODE-VERIFIED convention at `main.py:400-438`]) — omitting it ships a dead command (Open Question #10)
- ✅ Package decomposed under `cli/remediate/` (structural template: `swarm/`, `prd/`); test home `tests/cli/remediate/`
- ✅ The empty stale `remediation/` dir is removed/ignored (Open Question #9)

**Success Metrics:**

- `superclaude remediate` is discoverable and runnable; registration test green

---

**US-7.2: Supervised Dispatcher daemon (D2)**

- **As an** Operator
- **I want** a long-lived Dispatcher that runs the poll → detect → authz → claim → dispatch loop under supervision (watchdog, rate-limit awareness, restart)
- **So that** the bot survives crashes and runs 24/7 (the core reason V2 exists vs V1's in-session host)

**Acceptance Criteria:**

- ✅ Dispatcher composes D3/D4/D5/D6 + H1/H2 into a supervised loop (new operational shape — no `Restart=always`/`sd_notify` precedent in the repo; warrants a spike)
- ✅ Counter/state derived from the ledger (SoT) on startup, surviving restart

**Success Metrics:**

- Daemon recovers from kill/restart with no lost or double-processed triggers

---

**US-7.3: systemd deploy + sandbox image (S2)**

- **As an** Operator
- **I want** systemd unit(s) + a non-root sandbox image under `deploy/remediate-bot/`, with secrets sourced via `EnvironmentFile=` (chmod-600, owner-scoped) and hardening (`NoNewPrivileges`, `WatchdogSec`)
- **So that** the bot deploys as a hardened on-prem service

**Acceptance Criteria:**

- ✅ `deploy/` tree is net-new [NEW] (0 `.service`/`WatchdogSec`/`EnvironmentFile=`/`NoNewPrivileges` in the repo today)
- ✅ Secret files are chmod-600 (note: the `~/.aienv` cited exemplar is **644 on disk** — [CODE-CONTRADICTED]; cite the chmod-600 `EnvironmentFile=` requirement on its own merits / as a content-sourcing model only)
- ✅ Sandbox image is non-root with deny-by-default egress (depends on OD-1)

**Success Metrics:**

- Service starts under systemd, survives reboot, secrets not world-readable

---

**US-7.4: Latency & cost targets**

- **As an** Operator
- **I want** explicit latency/cost targets — trigger-to-action within the poll interval, large-diff handling via compression/chunking
- **So that** the bot is competitive with the established bar (PR-Agent "~30s single call"; Copilot criticized for 90s+ cold-start)

**Acceptance Criteria:**

- ✅ Trigger detected within one ≥30s poll interval; Dispatcher is daemon-resident (warm) while Runners are ephemeral
- ✅ Large diffs handled as a first-class concern (compression/chunking), within the 16 MiB stdin budget

**Success Metrics:**

- p95 trigger-to-Runner-spawn within one poll interval; large-diff triggers complete without prompt-size failure

---

### 21.2 Product Requirements

#### 21.2.1 Core Features

> Each feature maps to merged-requirements components. **Reuse anchors** carry [CODE-VERIFIED] provenance; everything else is greenfield [NEW]. Priority uses MoSCoW: P0 = Must Have, P1 = Should Have, P2 = Could Have.

##### Feature 1: Split-Host Architecture (Dispatcher + ephemeral Runner)

| Attribute | Value |
|-----------|-------|
| **Priority** | P0 (Must Have) |
| **Component(s)** | D2 (Dispatcher daemon), R1–R4 (Runner) |
| **Description** | A long-lived credential-holding Dispatcher (systemd daemon) splits from an ephemeral, sandboxed, tokenless per-trigger Runner (`claude -p`). The Dispatcher reasons over policy and holds secrets; the Runner reasons over untrusted text and holds none. |
| **User Value** | Even a successful prompt injection in the Runner cannot exfiltrate secrets or push code — the exact "fundamental mitigation" CSA Labs prescribes (reasoning layer / credential-holding execution layer separation). |
| **Dependencies** | `ClaudeProcess` [CODE-VERIFIED `process.py:72`]; OD-1 (sandbox tech); secret-isolation mechanism (Open Question #1). |

**Acceptance Criteria:**

- Runner holds no `GH_TOKEN`/push token/`ANTHROPIC_*` (AC-7, verified by secret-scrape test US-1.3)
- Dispatcher performs all GitHub I/O and policy; Runner performs only reasoning + sandboxed edits
- Runner is disposable per trigger (no state carried between triggers)

**Success Metrics:** 0 secrets in Runner environ; 0 pushes originating inside the Runner.

---

##### Feature 2: Mention-Triggered Authorization Pipeline

| Attribute | Value |
|-----------|-------|
| **Priority** | P0 (Must Have) |
| **Component(s)** | D3 (ingest), D4 (grammar), D5 (authz), D6 (parent resolution) |
| **Description** | Rate-limit-aware polling detects `@bot` mention replies; a whitelisted flag grammar is parsed; a live collaborator-permission gate on the *replier* (reject-by-default) authorizes; the parent comment is resolved as the `opComment`. |
| **User Value** | Only authorized humans cause action; the replier is the sole authority and the parent author supplies only data — directly answering Copilot's #1 complaint (unconditional trigger / ignored intent). |
| **Dependencies** | ETag/304 polling [NEW]; `collaborators/{login}/permission` authz [NEW]; `in_reply_to_id` parent resolution [NEW, probe-locked]; `classifier._login_of` dual-shape parser (reuse). |

**Acceptance Criteria:**

- `read`-permission mention → ack-reject, zero action (AC-1)
- No-flag mention defaults to `propose`
- Idle polling consumes 0 rate-limit quota via 304s; poll floor ≥30s
- Unknown permission → safe default (reject)

**Success Metrics:** 0 actions for non-write users; 100% no-flag defaults to propose.

---

##### Feature 3: Prompt-Injection-Contained Execution Envelope

| Attribute | Value |
|-----------|-------|
| **Priority** | P0 (Must Have) |
| **Component(s)** | R3 (envelope), R2 (executor) |
| **Description** | The opComment is delivered to `claude -p` as JSON DATA inside a CONTROL/DATA envelope via stdin — never shell-interpolated. Backed by `ClaudeProcess` stdin delivery + 16 MiB guard. |
| **User Value** | Attacker-controlled comment text cannot be executed as instructions — neutralizes the "Comment and Control" CVE class (Claude Code/Gemini/Copilot all leaked secrets via comment injection in 2026). |
| **Dependencies** | `ClaudeProcess` stdin delivery [CODE-VERIFIED `process.py:221-258`]; supersedes seed-brief's `"${opComment}"` interpolation (§6). |

**Acceptance Criteria:**

- opComment JSON-encoded as DATA, delivered via stdin; never in argv/shell
- Over-large opComment raises `PromptTooLargeForArgv` before spawn (SC-2 capping)
- Adversarial injection corpus (US-1.2) passes as a release gate

**Success Metrics:** 0 injection escapes from the DATA boundary.

---

##### Feature 4: Autonomy Lattice & needs_human_decision HALT

| Attribute | Value |
|-----------|-------|
| **Priority** | P0 (Must Have) |
| **Component(s)** | H2 (autonomy gate) |
| **Description** | Effective autonomy = min over the lattice {flag, authorization-projection, validation}, with off-lattice HALT short-circuits (`needs_human_decision`, exhausted budget). Lattice: `propose < patch < fix < push < resolve`, default `propose`. |
| **User Value** | The bot can never act above the most restrictive applicable ceiling, and escalates genuinely ambiguous/high-stakes items to a human instead of shipping a default. |
| **Dependencies** | Extends V1 `fsm.evaluate_push_decision` (5-predicate conjunction, tested) — predicates 2–5 carry over, predicate 1 drops, authz-projection predicate added; `needs_human_decision` populator (Open Question #8). |

**Acceptance Criteria:**

- Effective level = lattice-min; structurally impossible to exceed it
- `needs_human_decision` item HALTs to PENDING even at top level; never auto-applied
- A deterministic populator sets the flag, or the agent-self-report dependency is documented

**Success Metrics:** 0 actions above effective ceiling; 100% of HALT items escalated.

---

##### Feature 5: Loop-Safe Two-Phase Ledger & Push Budget

| Attribute | Value |
|-----------|-------|
| **Priority** | P0 (Must Have) |
| **Component(s)** | H1 (ledger) |
| **Description** | Durable, disk-authoritative, restart-surviving ledger: intent record before each consequential action, outcome record after; per-PR push budget (default 2, cap 5) with exact-SHA round correlation; per-PR fail-closed `flock`. |
| **User Value** | No infinite remediation loops; a crash mid-action recovers as RESUME (re-verify), never silent re-execute; at-most-once trigger claiming across restarts. |
| **Dependencies** | Atomic-write idiom (reuse `swarm/state.py`/`recommend/cache.py`/`install_hooks.py:443`); counter semantics `fsm.should_halt_rounds` (NOT swarm `:2269`); append-only `O_APPEND`+`flock` [NEW]. |

**Acceptance Criteria:**

- tmp+`os.replace` atomic writes; `O_APPEND` JSONL; per-PR `flock` fails-closed
- Round increments only on exact head-SHA == recorded-push-SHA match
- Intent-without-outcome on startup ⇒ RESUME; ledger is SoT for the counter
- Budget exhaustion posts a cap-summary and stops

**Success Metrics:** 0 unbounded loops; 0 double-executions; 100% crash-window RESUME.

---

##### Feature 6: GitHub Write-Back with Fork-Only `--repo` Chokepoint

| Attribute | Value |
|-----------|-------|
| **Priority** | P0 (Must Have) |
| **Component(s)** | H3 (push), H4 (reply/resolve), H5 (gh wrapper) |
| **Description** | Host-side push with a short-lived scoped token; reply-to-thread with summary + SHA; GraphQL `resolveReviewThread` (databaseId-matched) at `resolve` level; every `gh` call routed through a single `gh_call()` that unconditionally injects `--repo IronbellyOrg/IronClaude`. Never modifies merge state. |
| **User Value** | Autonomous writes can never land on the public upstream; threads close on the exact triggering thread; merge decisions stay with humans. |
| **Dependencies** | First Python `gh` caller in the repo [CODE-VERIFIED 0 existing Python callers]; reply/resolve net-new in Python (reference bash flow now in untracked `sc-pr-submit-protocol/scripts/reply-resolve-thread.sh`); posting template from auggie-review SKILL; OD-2 (token). |

**Acceptance Criteria:**

- No constructed `gh` argv can omit `--repo IronbellyOrg/IronClaude` (unit-tested)
- Push host-side only, after authz + validation; token never in the sandbox
- Resolve matches correct thread by `databaseId` (probe-locked); never a sibling (INV-010)
- Strictly `--comment`; no `--approve`/`--request-changes`/merge (§20)

**Success Metrics:** 0 `gh` calls without `--repo`; 0 mis-resolutions; 0 merge-state mutations.

---

##### Feature 7: Severity-Based Depth Routing

| Attribute | Value |
|-----------|-------|
| **Priority** | P1 (Should Have) |
| **Component(s)** | S1 |
| **Description** | Each finding is re-graded through the auggie-review severity rubric and routed: Critical/High → `--depth deep --fix`, Medium → `--fix`, Low/Nit → report-only, unknown → Medium fail-safe. |
| **User Value** | Remediation effort matches real severity; Augment's `severity_hint` is treated as a hint, not gospel. |
| **Dependencies** | Reuse-by-import `pr_submit/severity_router.remap_severity()`+`route()` [CODE-VERIFIED, pure, rubric-faithful]. |

**Acceptance Criteria:**

- Routing uses the imported router, not a re-parse of `severity-rubric.md`
- Unknown severity defaults to Medium
- Never emits the `--depth quick --fix` conflict

**Success Metrics:** 100% routed by remapped severity; 0 depth/flag conflicts.

---

##### Feature 8: Hardened systemd Deployment

| Attribute | Value |
|-----------|-------|
| **Priority** | P1 (Should Have) |
| **Component(s)** | D1 (CLI group), S2 (deploy) |
| **Description** | `superclaude remediate` CLI group + systemd unit(s) + non-root sandbox image under `deploy/remediate-bot/`, secrets via `EnvironmentFile=` (chmod-600), hardened with `NoNewPrivileges`/`WatchdogSec`. |
| **User Value** | A hardened, restart-surviving on-prem service — the textbook hardened-self-hosted-runner pattern (GitHub docs / StepSecurity / AWS / Sysdig). |
| **Dependencies** | `main.py` registration with `# noqa: E402,I001` [CODE-VERIFIED convention `main.py:400-438`]; `deploy/` tree net-new [NEW]; OD-1. |

**Acceptance Criteria:**

- `remediate_group` registered with `name="remediate"`; `superclaude remediate` discoverable
- Secret files chmod-600 (do not rely on the 644 `~/.aienv` as the exemplar)
- Service survives reboot

**Success Metrics:** registration test green; service restarts cleanly; secrets not world-readable.

---

#### 21.2.2 Feature Prioritization Matrix

> **Framework:** RICE — (Reach × Impact × Confidence) / Effort. Reach = relative share of triggers/operators touched (1–10). Impact = 3 (massive) / 2 (high) / 1 (medium). Confidence = % (driven by code-verified reuse vs greenfield/probe-dependent surfaces). Effort = person-weeks (greenfield surfaces with no prior art cost more; reuse-by-import costs less).

| Feature | Reach | Impact | Confidence | Effort (pw) | RICE Score | Priority |
|---------|-------|--------|------------|-------------|------------|----------|
| F3 Injection-contained envelope | 10 | 3 | 90% (ClaudeProcess stdin [CODE-VERIFIED]) | 2 | 13.5 | P0 |
| F4 Autonomy lattice & HALT | 10 | 3 | 80% (extends tested `fsm`; populator open) | 3 | 8.0 | P0 |
| F7 Severity depth routing | 8 | 2 | 95% (reuse-by-import [CODE-VERIFIED]) | 1 | 15.2 | P1 |
| F2 Mention authz pipeline | 10 | 3 | 60% (ETag/authz/parent all [NEW], probe-dependent) | 5 | 3.6 | P0 |
| F1 Split-host architecture | 10 | 3 | 70% (env-isolation mechanism open #1; OD-1) | 4 | 5.25 | P0 |
| F5 Loop-safe ledger & budget | 9 | 3 | 70% (atomicity idiom reuse; append/flock [NEW]) | 4 | 4.7 | P0 |
| F6 Write-back + `--repo` chokepoint | 9 | 3 | 50% (first Python `gh`; reply/resolve [NEW], probe-gated) | 5 | 2.7 | P0 |
| F8 Hardened systemd deploy | 6 | 2 | 55% (registration verified; sandbox/deploy [NEW], OD-1) | 5 | 1.3 | P1 |

**RICE Formula:** (Reach × Impact × Confidence) / Effort. Lower-confidence/higher-effort scores (F6, F8, F2) concentrate on the greenfield GitHub-I/O + sandbox/deploy surfaces with no in-repo prior art — consistent with the build-accounting finding that the Dispatcher half is the cost/risk center while the decision core is largely reusable.

---

#### 21.2.3 Competitive Feature Comparison Matrix

> Evidence-based (web research 01–03). **Our Product** = PR Auto-Remediation V2.0 (target capability, [NEW]). Legend: ✅ Full · ⚠️ Partial/Limited · ❌ Not supported.

| Feature | Our Product (V2.0) | GitHub Copilot Coding Agent | Claude Code GitHub Action (`@claude`) | Devin | CodeRabbit / PR-Agent |
|---------|--------------------|-----------------------------|---------------------------------------|-------|------------------------|
| Mention-triggered (`@bot`) | ✅ | ✅ | ✅ | ⚠️ (PR-event) | ✅ |
| Implements fixes (writes commits) | ✅ | ✅ | ✅ | ✅ | ⚠️ (mostly review/suggest) |
| On-prem / self-hosted | ✅ | ❌ (GitHub-Actions cloud) | ❌ (GitHub-Actions cloud) | ❌ (SaaS) | ⚠️ (some self-host) |
| Propose-only default | ✅ | ⚠️ (draft PR, but over-triggers) | ⚠️ | ✅ (human-in-loop) | ✅ |
| Live per-trigger authorization gate | ✅ | ⚠️ (org policy enable) | ❌ (workflow `if` convention) | ⚠️ | ❌ |
| opComment as untrusted DATA envelope | ✅ | ❌ (leaked secrets via comment injection, 2026) | ❌ (same CVE class) | ⚠️ | ❌ |
| Runner holds no push/secret token | ✅ | ❌ (`pull_request_target` injects secrets) | ❌ | ⚠️ | ❌ |
| Tamper-evident audit/trigger ledger | ✅ | ⚠️ | ⚠️ | ⚠️ | ❌ |
| Sidesteps GitHub-Actions supply-chain surface | ✅ | ❌ | ❌ | n/a | ⚠️ |

**Positioning Statement:** For maintainers on regulated/air-gapped forks who need autonomous PR remediation but cannot send code to cloud runners, PR Auto-Remediation V2.0 is an on-prem, mention-triggered remediation bot that treats the triggering comment as untrusted data inside a credential-free sandbox. Unlike GitHub Copilot Coding Agent (cloud-only, over-triggers, secrets in the runner) and the public `@claude` action (cloud Actions, no live authz), our split Dispatcher/Runner design holds the only differentiated position at the **on-prem × mention-triggered-remediation** intersection — a gap no incumbent occupies.

---

### 21.3 Implementation Phasing

> Phasing follows the spec's §19 build sequencing: front-load the highest-risk net-new
> surfaces behind a hard probe-first gate, build the credential/enforcement chokepoints in
> isolation before any autonomous `gh` I/O, then layer the Dispatcher ingest/authz, the
> sandboxed Runner, and finally the write actions (push/reply/resolve) gated by the autonomy
> lattice. The decision core is **reused, not rebuilt** (`import superclaude.pr_submit`).

| Phase | Components / Features | Rationale |
|-------|----------------------|-----------|
| **Phase 0 — Probe & Reconcile (hard gate)** | Throwaway-fixture-PR probe to lock `in_reply_to_id` / `databaseId` / Augment-bot-login as committed config constants; reconcile against in-flight `pr_submit/` decision core (decide import-and-extend vs fork); fix mis-cited reuse anchors (swarm `:2269`, `.aienv` 644, `os.replace`); resolve OD-1 (sandbox tech) and OD-2 (push-token mechanism) | The GitHub threading/resolve/authz shapes are the #1 build-blocking unknown — no code can substitute for a live probe. OD-1 gates the largest greenfield surface (R4/S2). Reconciliation prevents a duplicate autonomy/severity machine (SoT) |
| **Phase 1 — Credential & Enforcement Chokepoints** | D1 CLI-group registration in `main.py` (deferred-import + `# noqa: E402,I001`); H5 `gh_call()` fork-only `--repo` injector + injection test + CI grep-guard; H1 two-phase ledger (atomic `os.replace` + fail-closed `flock`, intent/outcome RESUME); the `build_env()` allowlist/secret-free-environ seam + AC-7 secret-scrape test | H5 is the first code-level enforcement of C5 (today prose-only) and must exist before any autonomous `gh` call. The env-allowlist seam is the load-bearing secret-isolation fix. Build and unit-test these in isolation |
| **Phase 2 — Dispatcher Ingest, Grammar & Authz** | D3 ETag/304 conditional polling (≥30s floor, rate-limit backoff); D4 mention grammar (whitelist: `propose\|patch\|fix\|push\|resolve`, `--depth`, `--scope`, `--rounds`); D6 parent-comment (`opComment`) resolution; D5 live collaborator-permission authz gate on the **replier** (reject-by-default; read-only replier → ack-reject, zero action) | These are the trust-boundary surfaces. Authz keys on the replier; the parent author supplies only data. All net-new GitHub I/O, dependent on Phase 0's locked shapes |
| **Phase 3 — Sandboxed Runner & Decision Core** | R4 ephemeral sandbox (PR-head checkout, deny-by-default egress allowlist, no host mounts); R2 Runner executor wrapping `ClaudeProcess` (propose-level `max_turns`, stdin envelope, `cwd`); R3 CONTROL/DATA envelope (opComment as JSON DATA, never interpolated); H2 autonomy gate + S1 severity routing reused from `pr_submit` (5-predicate push conjunction, `needs_human_decision` HALT, severity→depth) | The Runner is the credential-less reasoning layer (CSA "fundamental mitigation"). Severity routing and autonomy gating are reuse-by-import. Propose-only is the default and the first end-to-end happy path |
| **Phase 4 — Write Actions (lattice-gated)** | H3 host-side push with short-lived token (per-PR push budget default 2 / cap 5, SHA-correlated rounds); H4 reply-to-thread (`/replies`) + GraphQL `resolveReviewThread`; S2 systemd deploy (unit, `WatchdogSec`, chmod-600 `EnvironmentFile`, log forwarding) | Write authority is layered last and only reachable by explicit flag AND write-permission AND passing validation (lattice-min). Resolve sits behind the highest `resolve` level. Push budget and loop-safety enforced by the Phase-1 ledger |

> **Phase gating rule:** No phase may begin until the prior phase's release-blocking gates pass.
> Phase 0's probe is an absolute prerequisite for Phases 2–4; H5 (Phase 1) must pass its
> injection test before any Phase 2–4 code constructs a `gh` argv.

---

### 21.4 Release Criteria & Definition of Done

#### 21.4.1 Phase/Release Criteria

**MVP (propose-only) Release Criteria:**

| Category | Criterion | Validation Method | Status |
|----------|-----------|-------------------|--------|
| **Functionality** | Authorized replier `@bot` mention → opComment resolved → sandboxed Runner produces a proposed diff and posts a thread reply; read-only/non-collaborator replier is ack-rejected with zero action (AC-1) | Live fixture-PR e2e + authz unit tests | ⬜ |
| **Functionality** | Default with no flag resolves to `propose`; reaching `push`/`resolve` requires explicit flag AND write-permission AND passing validation (lattice-min) | Autonomy-gate unit tests (reuse `pr_submit` `evaluate_push_decision`) | ⬜ |
| **Security** | Runner `/proc/<pid>/environ` contains no `GH_TOKEN`/push token/`ANTHROPIC_*` value (INV-001/SC-7/AC-7) | Secret-scrape regression test | ⬜ |
| **Security** | Adversarial injection corpus (hidden instruction blocks, `$TOKEN` exfil, fake-authorized framing) achieves 0 escapes; opComment delivered as stdin JSON DATA, never interpolated (SC-2/AC-3) | Release-blocking red-team suite | ⬜ |
| **Security** | No `gh` argv can be constructed without `--repo IronbellyOrg/IronClaude` (SC-4); no raw `gh` subprocess outside `gh.py` | H5 injection unit test + CI grep-guard | ⬜ |
| **Safety** | Per-PR push budget (default 2, cap 5) never exceeded; counter is disk-authoritative and survives daemon restart (SC-5/SC-6/INV-002); `needs_human_decision` item never auto-pushed | Loop-guard + ledger restart tests | ⬜ |
| **Correctness** | Reply/resolve always targets the correct thread by `databaseId` (INV-010); each `(trigger_comment_id, flag_hash)` claimed at-most-once; intent-without-outcome ⇒ RESUME | Threading + idempotency tests against fixture PR | ⬜ |
| **Quality** | All reused `pr_submit` tests still pass; new `tests/cli/remediate/` registration + unit suite green; `make lint`, `ruff format --check`, `make verify-sync` clean | CI | ⬜ |
| **Operations** | Dispatcher runs as a supervised systemd unit; deny-by-default egress allowlist enforced (proxy `:4000/cli` + `api.github.com` + single-repo git, INV-015); run logs/ledger forwarded off-host before Runner teardown | Deploy smoke test + egress probe | ⬜ |
| **Documentation** | `cli/remediate/` documented as the SoT home; `--repo`/secret-separation/propose-only invariants and the mention grammar documented | Doc⇆CLI parity review | ⬜ |

#### 21.4.2 Definition of Done (Feature/Component Level)

A `remediate` component is considered "Done" when:

- [ ] All acceptance criteria met (AC-1, AC-3, AC-4, AC-7 as applicable)
- [ ] Unit tests written and passing; reused `pr_submit` contract tests unbroken
- [ ] Integration/e2e validated against a throwaway fixture PR (not just happy-path units)
- [ ] Security review: injection containment + secret isolation gates pass
- [ ] `gh` calls route only through H5 (`--repo` injection verified by test + grep-guard)
- [ ] Loop-safety: push budget + counter durability + `needs_human_decision` HALT verified
- [ ] `make lint` + `ruff format --check src/ tests/` + `make verify-sync` clean
- [ ] Code reviewed and approved; documentation updated (SoT path, invariants)
- [ ] No raw `gh`/secret leakage path introduced; product-owner acceptance

#### 21.4.3 Rollback & Contingency Plans

| Scenario | Detection Method | Rollback Procedure | Decision Maker |
|----------|------------------|-------------------|----------------|
| Injection escape or secret leak detected | Red-team suite / AC-7 scrape / audit log | Disable Runner dispatch (Dispatcher stops claiming triggers); revoke/rotate push tokens; revert to comment-only | Security owner |
| Wrong-thread resolution / wrong-repo push | INV-010 mismatch alert / `--repo` audit | Disable `resolve` + `push` levels (lattice cap to `propose`/`patch`); fall back to reply-only | Eng lead |
| Runaway remediation loop | Push budget exceeded / counter anomaly | Halt PR via ledger; cap rounds; require human re-arm | Eng lead |
| Rate-limit / API-shape drift | `X-RateLimit`/`Retry-After` / parse failures | Back off polling; freeze parser; re-run Phase-0 probe to relock shapes | On-call operator |
| Sandbox isolation failure | Egress-allowlist violation alert | Stop Runner; quarantine workspace; harden isolation tier before resume | Security owner |

---

### 21.5 Timeline & Milestones

> **Note:** The research inputs do not specify calendar dates, durations, or person-week
> estimates; this PRD is dated 2026-06-11. Milestones below are therefore **relative and
> dependency-ordered** (from the §19 build sequencing) with calendar dates marked TBD —
> set at kickoff. The one external anchor is the **EU AI Act high-risk compliance deadline
> (August 2026)**, a buyer-facing consideration for the on-prem/governed positioning.

#### 21.5.1 High-Level Timeline

```
[Phase 0: Probe & Reconcile] ─────────── [TBD] - [TBD]   (HARD GATE)
    ├── M0.1: GitHub shapes locked (in_reply_to_id / databaseId / bot-login)   [TBD]
    ├── M0.2: pr_submit reuse decision (import-and-extend) + citation fixes     [TBD]
    └── M0.3: OD-1 sandbox tech + OD-2 push-token mechanism resolved            [TBD]

[Phase 1: Credential & Enforcement Chokepoints] ── [TBD] - [TBD]
    ├── M1.1: D1 CLI group registered (superclaude remediate live)             [TBD]
    ├── M1.2: H5 --repo injector + injection test + CI grep-guard green        [TBD]
    └── M1.3: H1 ledger + build_env allowlist seam + AC-7 scrape test green    [TBD]

[Phase 2: Dispatcher Ingest, Grammar & Authz] ──── [TBD] - [TBD]
    ├── M2.1: D3 ETag/304 polling (≥30s floor) + backoff                       [TBD]
    ├── M2.2: D4 mention grammar + D6 parent (opComment) resolution            [TBD]
    └── M2.3: D5 live replier authz gate (AC-1: read-only → ack-reject)        [TBD]

[Phase 3: Sandboxed Runner & Decision Core] ────── [TBD] - [TBD]
    ├── M3.1: R4 sandbox (egress allowlist) + R2 executor + R3 envelope        [TBD]
    ├── M3.2: H2 autonomy gate + S1 severity routing (reused from pr_submit)   [TBD]
    └── M3.3: MVP propose-only e2e green (injection suite + secret scrape pass) [TBD]

[Phase 4: Write Actions (lattice-gated)] ───────── [TBD] - [TBD]
    ├── M4.1: H3 host-side push (budget 2/cap 5, SHA-correlated)               [TBD]
    ├── M4.2: H4 reply + GraphQL resolveReviewThread (INV-010 correct)         [TBD]
    └── M4.3: S2 systemd deploy (WatchdogSec, chmod-600 EnvironmentFile)       [TBD]
```

#### 21.5.2 Detailed Phase Breakdown

##### Phase 0: Probe & Reconcile (HARD GATE)

**Focus:** De-risk the #1 build-blocking unknowns before any parser/resolve/authz code.

**Deliverables:**

- [ ] Throwaway fixture-PR probe → `in_reply_to_id`/`databaseId`/Augment-bot-login committed as fixtures/constants
- [ ] Reuse decision: `import superclaude.pr_submit` (brain) vs fork; coordination with the in-flight V1 core landing
- [ ] Citation fixes (swarm `:2269`→`state.py`/`pr_submit.should_halt_rounds`; `os.replace`; drop `.aienv` chmod exemplar)
- [ ] OD-1 (sandbox tech) and OD-2 (push-token mechanism) resolved

**Success Criteria:** GitHub I/O shapes locked from real bytes; no parallel autonomy/severity machine; sandbox tech chosen.

**Target Completion:** TBD

---

##### Phase 1: Credential & Enforcement Chokepoints

**Focus:** Build the secret-isolation and `--repo` enforcement primitives that everything downstream depends on.

**Deliverables:**

- [ ] D1 group registered in `main.py` (`# noqa: E402,I001`)
- [ ] H5 `gh_call()` unconditional `--repo` injector; test asserting no argv omits it; CI grep-guard
- [ ] H1 two-phase ledger (atomic `os.replace`, fail-closed `flock`, intent/outcome RESUME)
- [ ] `build_env()` allowlist/secret-free-environ seam + AC-7 secret-scrape test

**Success Criteria:** `superclaude remediate` resolves; AC-7 passes; no un-pinned `gh` path exists.

**Target Completion:** TBD

---

##### Phase 2: Dispatcher Ingest, Grammar & Authz

**Focus:** The trust-boundary surfaces — detect mentions, resolve the parent, gate the replier.

**Deliverables:**

- [ ] D3 ETag/304 conditional polling (≥30s floor, rate-limit backoff)
- [ ] D4 mention grammar whitelist + D6 `opComment` parent resolution
- [ ] D5 live collaborator-permission authz gate on the replier (AC-1)

**Success Criteria:** Authorized replier triggers a claim; read-only replier ack-rejected with zero action.

**Target Completion:** TBD

---

##### Phase 3: Sandboxed Runner & Decision Core (MVP)

**Focus:** The credential-less reasoning layer and the reused decision core — first end-to-end propose-only path.

**Deliverables:**

- [ ] R4 ephemeral sandbox + R2 `ClaudeProcess` executor + R3 CONTROL/DATA envelope
- [ ] H2 autonomy gate + S1 severity routing (reuse-by-import from `pr_submit`)
- [ ] MVP propose-only e2e: mention → proposed diff → thread reply

**Success Criteria:** Injection suite 0 escapes; secret-scrape clean; propose-only happy path green.

**Target Completion:** TBD

---

##### Phase 4: Write Actions (lattice-gated)

**Focus:** Layer push/reply/resolve last, each reachable only by explicit flag + write-permission + validation.

**Deliverables:**

- [ ] H3 host-side push (budget 2/cap 5, SHA-correlated rounds)
- [ ] H4 reply-to-thread + GraphQL `resolveReviewThread` (INV-010)
- [ ] S2 systemd deploy (unit, `WatchdogSec`, chmod-600 `EnvironmentFile`, log forwarding)

**Success Criteria:** Lattice-min holds (no path to push without all gates); resolve targets correct thread; daemon supervised and auditable.

**Target Completion:** TBD

---

## 22. Customer Journey Map

> **Scope note (feature PRD):** The product has **no GUI and no web surface**. The end user is a **repo
> maintainer / on-call reviewer** on the `IronbellyOrg/IronClaude` fork; the entire control surface is a
> short `@bot` comment grammar plus an operator-run systemd service [Agent 8 §3]. The journey below maps
> the *authorized collaborator* (primary actor) and *operator* (deployer) experience for a
> mention-triggered remediation request.

### 22.1 Journey Stages

| Stage | User Goal | Actions | Touchpoints | Emotions | Pain Points | Opportunities |
|-------|-----------|---------|-------------|----------|-------------|---------------|
| **Awareness** | Learn that a headless `@bot` can fix flagged PR findings on-prem | Reads team docs / sees the bot reply on a prior PR; learns `@bot` grammar | `superclaude remediate` CLI docs; existing PR threads | Curious, cautiously hopeful | Distrust of AI auto-changes (only ~3–33% of devs trust AI output) [EXTERNAL web-02/03] | Position as the "middle ground / confirmation step" the market leader lacks [EXTERNAL web-01 §1.2] |
| **Consideration** | Decide whether to delegate a finding vs fix by hand | Compares effort; checks that propose-only is the default and a human still merges | Severity-rubric tiers (🔴/🟠/🟡/🟢/💬) [CODE-VERIFIED]; §20 "humans merge" non-goal | Skeptical but reassured by conservative default | Fear of over-action / unauthorized push (Copilot's #1 complaint) [EXTERNAL web-01 §1.2] | Propose-only default + live authz gate directly answers the incumbent gap |
| **Acquisition (Deploy)** | Stand up the bot for the repo | Operator installs systemd unit + sandbox image; sources secrets via `EnvironmentFile=` chmod-600 | `deploy/remediate-bot/` units [SPEC]; `~/.aienv` proxy contract (`:4000/cli`, `T2Model*` only) [memory] | Focused, security-conscious | `deploy/` + sandbox tech (OD-1) are fully greenfield, zero in-repo precedent [CODE-VERIFIED 04/08] | Ship hardened defaults (deny-all egress, no host mounts) as turn-key NFRs [EXTERNAL web-03 §3.2] |
| **Onboarding (First mention)** | Trigger the bot correctly the first time | Replies to an Augment/human review comment: `@bot fix --depth deep` | PR review-comment reply thread; `@bot` grammar (D4) [SPEC] | Tentative, watching for an ack | Unsure which flags are whitelisted; mention is app-level convention, not a GitHub primitive [EXTERNAL web-03 §1.2] | Bot acks the claim quickly (poll floor ≥30s) so the user knows it was seen |
| **First Value** | Get a usable proposed fix | Bot resolves the **parent** comment as `opComment`, runs `/sc:troubleshoot` in sandbox, replies with a diff/summary + SHA | Threaded reply with proposed patch; round-outcome summary | Relief / "it understood the issue" | Latency (cold-start; benchmark vs PR-Agent ~30s, Copilot 90s+) [EXTERNAL web-01 §5] | Stream progress; cap opComment length under the 16 MiB stdin guard [CODE-VERIFIED process.py] |
| **Engagement** | Iterate within a bounded budget | Re-reviews, replies again to refine; bot increments round only when PR head SHA == bot's recorded push SHA | Per-PR push budget (default 2, cap 5) [CODE-VERIFIED `pr_submit/fsm.py` DEFAULT_MAX_ROUNDS=2/HARD_CAP=5]; round-outcome replies | Confident, in control | Loop anxiety ("will it run forever?") | Bounded monotonic counter + HALT summary makes the ceiling visible and trustworthy |
| **Retention** | Rely on the bot across many PRs without surprises | Uses it routinely; trusts that a `read`-only user mentioning it does nothing | Live per-trigger authz gate (D5); trigger ledger (H1) [SPEC] | Trusting, low-friction | Trust erodes the moment an unwanted change lands | Immutable trigger ledger as a visible provenance/audit artifact [EXTERNAL web-02 R4] |
| **Advocacy** | Recommend the bot to other regulated/air-gapped teams | Shares the on-prem, injection-contained story internally | Audit log / ledger exports; security narrative | Proud of the safety posture | — | Lead with the "Comment and Control" threat the split-host design neutralizes [EXTERNAL web-01/02] |

### 22.2 Moments of Truth

| Moment | Description | Success Criteria | Failure Recovery |
|--------|-------------|------------------|------------------|
| **The authorization decision** | A user replies `@bot fix`; the Dispatcher runs a live collaborator-permission check on the *replier* (not the parent author) | Write-permission replier → trigger claimed; `read`-only replier → polite ack-reject, **zero action** (AC-1) [SPEC] | Reject is itself the safe outcome; post a one-line "not authorized" reply, log the attempt, take no remediation |
| **Parent-comment resolution (opComment capture)** | Dispatcher resolves the mentioned comment's *parent* via `in_reply_to_id` and treats its body as untrusted DATA | Correct parent body captured and JSON-encoded into the CONTROL/DATA envelope, delivered via stdin — **never** `/sc:troubleshoot "${opComment}"` interpolation (SC-2/AC-3) [CODE-VERIFIED seam; SPEC envelope] | If parent cannot be resolved, HALT and reply asking the user to mention directly on the finding; never guess |
| **The push gate** | After validation, the Dispatcher decides whether to push host-side with a short-lived token | Push only if effective autonomy ≥ `push` AND validation passed AND `needs_human_decision==false` AND under budget AND real edits exist (5-predicate conjunction) [CODE-VERIFIED `evaluate_push_decision`] | Any predicate false → fall back to propose (post diff, don't push); `needs_human_decision` → HALT with explanation |
| **Thread reply + resolve** | Bot replies to the review thread with the outcome and (at `resolve` level) resolves it | Reply lands on the correct thread (matched by `databaseId`); resolve targets the right `threadId` (INV-010) [SPEC] | Wrong-thread risk is the highest net-new GitHub surface — gated behind the §21.3 probe-first lock; on ambiguity, reply-only, do not resolve |

---

## 23. Error Handling & Edge Cases

> **Design principle:** The product exists to neutralize a *named, proven* attack class — "Comment and
> Control" (Johns Hopkins, Apr 2026) hijacked Claude Code, Gemini CLI, and Copilot Agent via PR/issue
> comments into leaking secrets, zero maintainer interaction [EXTERNAL web-01/02]. Error handling is
> therefore **fail-safe / fail-closed by construction**, not best-effort. Where a failure mode protects
> a security invariant, the safe outcome (reject, HALT, propose-not-push) **is** the recovery.

### 23.1 Error Categories

| Category | Examples | User Experience | Recovery |
|----------|----------|-----------------|----------|
| **Authorization Errors** | `read`-permission replier mentions `@bot`; non-collaborator sender; bot login spoofing attempt | Polite one-line "not authorized to trigger remediation" reply; no remediation runs (AC-1) | Reject-by-default; log the attempt to the trigger ledger; classifier keys only on the configured collaborator-permission + Augment-bot-login, unknown → safe default [CODE-VERIFIED `pr_submit/classifier.py` 3-state, T-211] |
| **Validation / Intent Errors** | Unparseable/unknown flag in the `@bot` grammar; ambiguous intent; `needs_human_decision` finding (security trade-off, API-contract change, multiple valid fixes) | Bot replies stating the item needs a human decision and HALTs; no push | `needs_human_decision` HALT short-circuit is honored before the push gate [CODE-VERIFIED consumed at `fsm.py:204/:353/:158`]; ⚠️ no Python code *sets* the flag today — V2.0 must build a deterministic populator or document the in-sandbox self-report dependency [CODE-VERIFIED gap, Agent 6] |
| **Prompt-Injection Attempts** | opComment contains hidden `-- Additional instruction --` blocks, `gh issue edit $TOKEN` exfil payloads, white-on-white "authorized/urgent" framing [EXTERNAL web-02 §2.3] | Transparent to user; injection cannot reach a consequential action | Architectural: opComment is JSON DATA in a CONTROL/DATA envelope via stdin, never interpolated (SC-2); Runner holds **no** push token / long-lived secret; propose-only blast-radius cap [CODE-VERIFIED stdin delivery; SPEC envelope + secret split] |
| **System / Process Errors** | Runner `claude -p` hangs; exceeds `timeout_seconds` (default 6300s ≈ 105 min); process tree must be killed | `StuckRun` alert raised; trigger marked failed; no partial push | `ClaudeProcess` returns rc `124` on timeout and kills the whole child tree via `os.setpgrp`→`os.killpg` [CODE-VERIFIED process.py]; ledger intent-without-outcome ⇒ RESUME/re-verify, never silent re-execute (§9) [SPEC] |
| **Secret-Leak (config) Errors** | Runner env inadvertently inherits `GH_TOKEN` / push token / `ANTHROPIC_AUTH_TOKEN` | Invisible to user but a release-blocking defect | `build_env()` is additive-only `os.environ.copy()` and **cannot** strip inherited secrets via `env_vars` [CODE-VERIFIED process.py:145-160]; AC-7 (`/proc/<pid>/environ` grep = 0) requires a new empty-base/allowlist seam OR a secret-free sandbox parent — gated by a named regression test [CODE-VERIFIED gap, all 8 agents] |
| **Integration / GitHub-API Errors** | Reply posts to wrong thread; `resolveReviewThread` targets wrong `threadId`; `in_reply_to_id` missing/unreliable | Risk of resolving an unrelated reviewer's thread (INV-010) | Reply/resolve are net-new GraphQL in Python — no committed Python caller; a reference bash flow has since landed in the untracked parallel V1 `sc-pr-submit-protocol/scripts/reply-resolve-thread.sh`, but it is locked behind the §21.3 throwaway-PR probe that captures real `databaseId`/`in_reply_to_id` shapes as committed config before parser code; on mismatch, reply-only |
| **Rate-Limit / Timeout Errors** | GitHub primary/secondary rate limits; `429`/`Retry-After`; poll storms | Slower acks; no dropped triggers | ETag/`If-None-Match` conditional polling + `Retry-After`/`X-RateLimit-Remaining` backoff (§13); poll floor ≥30s [CODE-VERIFIED `MIN_POLL_INTERVAL=30`]; net-new (0 in-repo precedent) [CODE-VERIFIED] |
| **Concurrency Errors** | Two Dispatcher passes claim the same trigger; parallel git tree mutations on one PR | At-most-once execution per trigger | Two-phase ledger claim keyed on `(trigger_comment_id, parsed_flag_hash)` + per-PR `flock`; lock acquisition must **fail-closed** (the only in-repo flock precedent is bash + fail-open — wrong model to copy) [CODE-VERIFIED gap, Agent 4 F9] |
| **Push / Repo-Target Errors** | `gh` call omits `--repo`; PR lands on upstream parent instead of fork | Catastrophic if unguarded (historically burned the operator) | H5 `gh_call()` unconditionally injects `--repo IronbellyOrg/IronClaude`; today this is **prose-only** discipline (CLAUDE.md), never code-enforced — H5 is the first mechanical gate, with a test asserting no argv can omit `--repo` [CODE-VERIFIED 0 Python `gh` callers, C5] |

### 23.2 Edge Cases

| Scenario | Expected Behavior | Test Case |
|----------|-------------------|-----------|
| Replier has `read` permission only | Ack-reject reply, zero remediation (AC-1) | Mock collaborator-permission = `read`; assert no Runner spawn, ledger logs reject |
| opComment exceeds envelope length cap | Typed pre-spawn failure, no process started | `PromptTooLargeForArgv` raised before any handle opens when encoded prompt > `PROMPT_MAX_BYTES` (16 MiB default, env-overridable) [CODE-VERIFIED process.py:56-69,169-173] |
| Re-review arrives but PR head SHA ≠ bot's recorded push SHA | Does **not** count as a new round (prevents infinite loop) | Assert round increments only at the single FSM edge when `head_sha == recorded_push_sha` [CODE-VERIFIED `should_halt_rounds` `>=` fence-post, `fsm.py:129`] |
| Push budget exhausted (reached cap 5) | HALT with cap-summary reply; no further pushes | Drive 5 rounds; assert 6th transitions to `HALT_MAX_ROUNDS` [CODE-VERIFIED `HARD_CAP_MAX_ROUNDS=5`] |
| Parent comment unresolvable (`in_reply_to_id` null) | HALT; reply asking user to mention directly on the finding | Probe-locked `DetectionContract`; assert no opComment fabricated |
| Dual GitHub payload shapes (`author.login` vs `user.login`) | Both shapes parsed identically | `classifier._login_of` already handles both, tested [CODE-VERIFIED Agent 6 §D] |
| Dispatcher restart mid-trigger (crash window) | Resume from ledger; re-verify, never re-execute a recorded intent | Two-phase intent/outcome replay; intent-without-outcome ⇒ RESUME (§9) [SPEC; pattern from `sprint/recovery.py` JSONL replay, Agent 4/5] |
| `--dangerously-skip-permissions` default flag | Safe **only** because of the sandbox boundary (no host mounts, deny egress), not the flag itself | Assert flag present AND sandbox network deny-all + no host home mount [CODE-VERIFIED default `process.py:93`; SPEC sandbox] |
| Sandbox needs Anthropic proxy but deny-all egress | Proxy host (`:4000/cli`) must be on the egress allowlist alongside `api.github.com` + single-repo git | Assert egress allowlist includes proxy base from `~/.aienv`; GitHub creds stay host-side [INV-015, Agent 4 Q-1; memory] |
| Stale `remediation/` top-level dir (empty placeholder) | Feature lives under `cli/remediate/`; ignore/delete `remediation/` | Confirm source home is `cli/remediate/` [CODE-VERIFIED empty `remediation/`, Agent 8 §2] |

### 23.3 Graceful Degradation

| Component Failure | Degraded Experience | User Communication |
|-------------------|--------------------|--------------------|
| Runner sandbox unavailable / spawn fails | No remediation runs; trigger marked failed, not silently dropped | Threaded reply: "remediation could not start — retry later"; ledger records the failure |
| Validation step fails inside Runner | Falls back from `push`/`fix` to **propose**: posts the diff, does not push | Reply includes the proposed patch + "validation did not pass — proposing only, not pushing" |
| GitHub reply/resolve API errors after a successful push | Push (intent+outcome) is durable; reply retried; resolve skipped on ambiguity | Two-phase ledger ensures the push is recorded; reply-only fallback, never resolve the wrong thread |
| Rate-limit exhaustion | Polling backs off; acks delayed but no triggers lost | Longer ack latency; conditional-request polling resumes when budget returns |
| Short-lived push token mint fails | Degrades to propose-only (no host-side push) | Reply posts the diff; "could not obtain push credential — proposing only" |
| Dispatcher down (systemd) | Bot is unavailable; mentions queue in GitHub until restart | `Restart=always` watchdog; on restart, ledger replay resumes in-flight triggers (no double-execute) |

---

## 24. User Interaction & Design

> **No GUI, no web surface, no new slash command for end users.** The product's entire "interface" is a
> **4-token `@bot` comment grammar** (D4) plus an operator-run systemd service [CODE-VERIFIED product
> surface, Agent 8 §3]. There are no wireframes in the visual sense — the interaction is text in GitHub
> review threads and the bot's threaded replies. The sections below adapt the template to this CLI /
> conversational surface.

### 24.1 Interaction Surfaces (in lieu of Wireframes)

| Surface | Description | Status | Notes |
|---------|-------------|--------|-------|
| **`@bot` mention grammar** | A whitelisted comment grammar the authorized collaborator types as a reply to a review comment | Proposed (D4) [SPEC] | Tiny whitelist; everything else is config/operator-set |
| **Bot threaded reply** | The bot's response on the same thread: claim ack, proposed diff/summary + SHA, round-outcome, or HALT reason | Proposed (H4) [SPEC] | Reply endpoint is net-new; templated from auggie-review `gh` posting precedent [CODE-VERIFIED SKILL.md:304-314] |
| **Thread resolution** | At `resolve` autonomy, the bot resolves the review thread after a successful outcome | Proposed (H4) [SPEC] | GraphQL `resolveReviewThread` — net-new, §21.3-probe-gated |
| **`superclaude remediate` CLI group** | Operator entrypoint (start/status of the Dispatcher), mirroring `sprint`/`swarm`/`pipeline` | Proposed (D1) [SPEC] | Registers in `cli/main.py` via the deferred-import `# noqa: E402,I001` idiom [CODE-VERIFIED main.py:400-438] |
| **systemd service** | The deployment "screen" the operator manages | Proposed (S2) [SPEC] | `deploy/remediate-bot/` greenfield; `Restart=always`, `EnvironmentFile=` chmod-600 secrets |

### 24.2 The `@bot` Comment Grammar (Control Surface)

The control surface is a small, whitelisted token set. **Default with no flag = `propose`** (the safest
level) [Agent 8 §3]. Reaching `push` requires an explicit flag **AND** write-permission **AND** passing
validation (lattice-minimum) — it must be *structurally impossible* to reach `push` otherwise.

| Token | Values | Default | Meaning |
|-------|--------|---------|---------|
| **Autonomy level** | `propose` < `patch` < `fix` < `push` < `resolve` (lattice) | `propose` | Capability ceiling; effective level = min over (flag, authz projection, validation) [SPEC; generalizes V1 `--monitor {0,1,2,3}` ordinal, CODE-VERIFIED `pr_submit`] |
| **`--depth`** | `quick` \| `deep` | severity-routed | Troubleshoot depth; Critical/High → `deep --fix`, Medium → `--fix`, Low/Nit → report-only [CODE-VERIFIED severity rubric S1] |
| **`--scope`** | path/area hint | full PR-head | Narrows the remediation target |
| **`--rounds`** | integer ≤ cap | 2 (cap 5) | Per-PR push budget [CODE-VERIFIED `DEFAULT_MAX_ROUNDS=2`/`HARD_CAP_MAX_ROUNDS=5`] |

**Example invocation (happy path):** an authorized collaborator replies to an Augment review comment with
`@bot fix --depth deep` → Dispatcher authorizes the *replier*, claims the trigger, resolves the *parent*
comment as `opComment`, runs the sandboxed Runner, and replies with a diff (propose/patch) or a
sandbox-branch commit + SHA (fix/push) [Agent 8 §3].

### 24.3 Design Conventions & Invariants (in lieu of Design System)

- [ ] **Conservative default** — no flag ⇒ `propose` only; cannot reach `push` without explicit flag + write-perm + validation pass [SPEC]
- [ ] **Replier-is-authority** — the *replier* is the sole authorization subject; the *parent author* supplies only DATA (a `read` user mentioning the bot gets ack-reject, AC-1) [SPEC]
- [ ] **Untrusted-data envelope** — opComment is JSON DATA in a CONTROL/DATA envelope, never interpolated into the prompt (SC-2) [CODE-VERIFIED stdin seam]
- [ ] **Severity markers reused** — bot reply tiers follow the existing rubric (🔴 Critical / 🟠 High / 🟡 Medium / 🟢 Low / 💬 Nit) [CODE-VERIFIED severity-rubric.md]
- [ ] **Never modify merge state** — strictly `--comment`; never `--approve`/`--request-changes`; humans merge (§20) [CODE-VERIFIED auggie SKILL.md:349 + rubric decision-mode]
- [ ] **AI provenance** — generated commits/replies carry clear bot provenance (provenance, not authorship) [EXTERNAL web-03 §1.4]
- [ ] **Fork-only target** — every `gh` mutation pins `--repo IronbellyOrg/IronClaude` [CODE-VERIFIED C5]

### 24.4 Prototype / Reference Implementations

| Reference | Purpose | Link / Path |
|-----------|---------|-------------|
| `pr_submit/` (V1.0 decision core) | Tested FSM + severity router + autonomy gate the V2.0 interaction logic extends | `src/superclaude/pr_submit/` [CODE-VERIFIED] |
| auggie-review `gh` posting | Template for the bot's summary/inline reply | `sc-auggie-review-protocol/SKILL.md:304-314` [CODE-VERIFIED] |
| OSS "Architect" guardrail framing | External analog of Dispatcher-enforced guardrails the LLM cannot bypass | [EXTERNAL web-01 §2.1] |

---

## 25. API Contract Examples

> **Status:** All GitHub-facing contracts below are **net-new** — there is **no Python `gh` caller
> anywhere in the repo today** [CODE-VERIFIED 0 Python `gh` callers]; ETag/authz surfaces have
> zero in-repo precedent, and reply/resolve have only an untracked bash reference flow
> (`sc-pr-submit-protocol/scripts/reply-resolve-thread.sh`), no committed Python caller. Concrete request/response *shapes* (especially `databaseId` and
> `in_reply_to_id`) MUST be locked by the §21.3 throwaway-PR probe before parser code is written. All
> `gh` calls route through `H5.gh_call()`, which unconditionally injects `--repo IronbellyOrg/IronClaude`.
> The minimal GitHub permission baseline is `contents`, `pull-requests`, `issues`, `id-token` [EXTERNAL
> web-03 §1.2].

### 25.1 Poll for `@bot` Mentions (D3 ingest — conditional request)

**Request (ETag/304 conditional polling, poll floor ≥30s):**

```http
GET /repos/IronbellyOrg/IronClaude/pulls/comments?since={cursor}
If-None-Match: "{etag_from_last_poll}"
Authorization: Bearer {read_comment_token}   # host-side Dispatcher credential, never in Runner
```

**Response (no change):**

```http
HTTP/1.1 304 Not Modified
X-RateLimit-Remaining: 4987
```

**Response (new mention found):** `200 OK` with new `ETag`; the comment whose `body` contains the `@bot`
mention becomes the *trigger comment*; its `in_reply_to_id` points at the *parent* (the `opComment`).
On `429`/secondary limit, honor `Retry-After`/`X-RateLimit-Reset` backoff (§13). *[SPEC; net-new]*

### 25.2 Resolve Parent Comment → opComment (D6)

**Request:**

```http
GET /repos/IronbellyOrg/IronClaude/pulls/comments/{in_reply_to_id}
Authorization: Bearer {read_comment_token}
```

**Response (Success):** the parent review comment; its `.body` is the **untrusted `opComment`**. Login is
read from either `author.login` or `user.login` (both shapes handled) [CODE-VERIFIED `classifier._login_of`].
If `in_reply_to_id` is null/unresolvable → HALT (do not fabricate an opComment). *[SPEC; net-new]*

### 25.3 Live Authorization Gate (D5)

**Request — check the *replier's* permission (not the parent author's):**

```http
GET /repos/IronbellyOrg/IronClaude/collaborators/{replier_login}/permission
Authorization: Bearer {read_comment_token}
```

**Response (Success):**

```json
{ "permission": "write", "user": { "login": "{replier_login}" } }
```

**Decision:** `permission ∈ {write, admin, maintain}` → claim the trigger. `read`/unknown → **ack-reject,
zero action** (AC-1). Reject-by-default; classifier keys only on configured constants, unknown → safe
default [CODE-VERIFIED `pr_submit/classifier` discipline]. *[SPEC; net-new — 0 in-repo precedent.]*

### 25.4 Internal opComment Envelope → Runner (R2/R3 — stdin, not argv)

The Dispatcher delivers a **CONTROL/DATA envelope** to the Runner over **stdin** — never as
`/sc:troubleshoot "${opComment}"` interpolation (SC-2/AC-3). This is the central injection containment.

```json
{
  "control": {
    "intent": "fix",
    "depth": "deep",
    "scope": null,
    "max_rounds": 2,
    "pr_head_sha": "{sha}",
    "trigger_comment_id": "{id}"
  },
  "data": {
    "op_comment_body": "<untrusted parent-comment text, JSON-encoded, treated as DATA only>"
  }
}
```

The Runner spawns via `ClaudeProcess` [CODE-VERIFIED process.py:72], whose command is:

```text
claude --print --verbose --dangerously-skip-permissions --no-session-persistence \
  --tools default --max-turns {30|60} --output-format stream-json [--model {T2Model*}]
```

Prompt (the envelope) is written to **child stdin in 64 KiB chunks** (bypasses the 128 KB argv limit),
with a pre-spawn `PROMPT_MAX_BYTES` guard (16 MiB default) raising `PromptTooLargeForArgv`
[CODE-VERIFIED process.py:121-258]. Runner env MUST exclude `GH_TOKEN`/push/`ANTHROPIC_AUTH_TOKEN`
(AC-7) — requires a new allowlist seam, since `build_env()` is additive-only [CODE-VERIFIED gap].

### 25.5 Post Threaded Reply (H4 — outcome)

**Request:**

```http
POST /repos/IronbellyOrg/IronClaude/pulls/{pr}/comments/{parent_comment_id}/replies
Content-Type: application/json
Authorization: Bearer {short_lived_token}

{ "body": "Proposed fix for this finding:\n\n```diff\n...\n```\nValidation: passed. Round 1/2." }
```

**Response (Success):** `201 Created`. Reply must land on the correct thread (matched by `databaseId`);
on ambiguity, reply-only and skip resolve. Strictly `--comment` semantics; never `--approve`/
`--request-changes` [CODE-VERIFIED auggie SKILL.md:349]. *[SPEC; reply endpoint net-new.]*

### 25.6 Resolve Review Thread (H4 — GraphQL, `resolve` autonomy only)

**Request:**

```http
POST /graphql
Authorization: Bearer {short_lived_token}

{ "query": "mutation { resolveReviewThread(input: {threadId: \"{thread_node_id}\"}) { thread { isResolved } } }" }
```

**Response (Success):**

```json
{ "data": { "resolveReviewThread": { "thread": { "isResolved": true } } } }
```

`{thread_node_id}` is obtained by paginating `reviewThreads` and matching on `databaseId` (INV-010). This
is the **highest-risk net-new surface — no committed Python GraphQL caller** (a reference bash flow exists in the untracked parallel V1 `sc-pr-submit-protocol` skill) [CODE-VERIFIED] — and is a hard
§21.3 probe dependency. On any thread-match ambiguity, do **not** resolve. *[SPEC; net-new.]*

### 25.7 Standard Error Envelope

```json
{
  "status": "error",
  "error": {
    "code": "NOT_AUTHORIZED | PARENT_UNRESOLVABLE | VALIDATION_FAILED | BUDGET_EXHAUSTED | NEEDS_HUMAN_DECISION | PROMPT_TOO_LARGE | RATE_LIMITED",
    "message": "Human-readable reason posted to the thread; full detail recorded in the trigger ledger."
  }
}
```

Every error code maps to a fail-closed outcome in §23.1 (reject / HALT / propose-not-push). All triggers,
exact opComment input, and decisions are written to the immutable **trigger ledger** as a queryable
provenance/audit artifact [EXTERNAL web-02 R4 / web-03 R8].

---

## 26. Contributors & Collaboration

### 26.1 Document Contributors

> **Note:** This PRD was synthesized from a parallel research fan-out (8 codebase-investigator passes + 3 web/market-research passes) against the V2.0 merged-requirements spec. Human owner assignments are **unassigned** as of this Draft (frontmatter `status: 🟡 Draft`, `assigned_to: product-team`); the table records the evidenced contribution streams and reserves the named human roles for sign-off.

| Role | Name | Contribution |
|------|------|--------------|
| Product Owner | [TBD — product-team] | Product vision, scope, autonomy-lattice and propose-only-default decisions |
| Engineering Lead | [TBD] | Split-host (Dispatcher/Runner) architecture, reuse-vs-build accounting, TDD hand-off |
| Security Lead | [TBD] | Prompt-injection threat model, secret-separation (INV-001/SC-7), authorization gate (D5) |
| QA Lead | [TBD] | Acceptance criteria (AC-7 secret-scrape, AC-4 `--repo` injection), §21.3 probe-first gate, injection red-team corpus |
| Codebase Reuse Investigation (research/01–08) | 8 parallel investigator passes | Verified every reuse anchor against live source — `ClaudeProcess` (`process.py:72`), `pr_submit/` decision core, swarm state/atomic-write, severity rubric, `gh`-posting precedent; surfaced the `pr_submit` Reuse-Map omission, the `build_env()` allowlist gap, and the `swarm:2269` mis-citation |
| Web / Market Research (research/web-01–03) | 3 parallel ecosystem passes | Competitive landscape, prompt-injection incident record (2026 CVEs), security-standards alignment (OWASP/CSA), on-prem market sizing and positioning |

### 26.2 How to Contribute

- **Comment inline** for questions, suggestions, or clarifications on specific requirements (especially the open decisions OD-1…OD-4).
- **Tag relevant leads** using @ mentions; route security-invariant changes (INV-001/SC-7, C5 `--repo` pin) to the Security Lead.
- **Update the Open Questions table** when an open decision (sandbox tech OD-1, push-token mechanism OD-2, push-budget default OD-3, `patch` semantics OD-4) is resolved.
- **Re-verify code citations before editing** — multiple reuse citations in the source spec were found stale (`swarm/commands.py:2269`, the `~/.aienv` chmod-600 exemplar, `build_env()` allowlist mechanism). Treat any `file:line` claim as needing a fresh Read before it is relied upon.
- **Coordinate with the in-flight V1.0 `pr_submit` build** — that package is landing in parallel; link decisions that touch the shared decision core rather than forking it.
- **Review quarterly** and flag outdated sections (see Section 28.2).

---

## 27. Related Resources

### 27.1 Customer / Market Research

> Competitive and ecosystem research gathered to position the on-prem, mention-triggered remediation bot. Codebase remains source of truth for capabilities; these sources add market context only.

| Resource | Link | Description |
|----------|------|-------------|
| Web Research — Topic 1 (Market & Ecosystem) | `prd-pr-auto-remediation-v2-0/research/web-01-web-research-topic-1.md` | Competitive landscape, 2026 prompt-injection incident record, market sizing, propose-only positioning |
| Web Research — Topic 2 (Comparable Products & Secure-Agent Best Practices) | `prd-pr-auto-remediation-v2-0/research/web-02-web-research-topic-2.md` | Comparable products, "Comment and Control" threat class, sandbox tooling, OWASP alignment |
| Web Research — Topic 3 (Ecosystem & Standards) | `prd-pr-auto-remediation-v2-0/research/web-03-web-research-topic-3.md` | Mention-trigger UX precedent, ephemeral-runner/token hygiene, governance-by-design trends |
| GitHub Copilot Coding Agent (primary incumbent) | https://github.blog/changelog/2025-09-25-copilot-coding-agent-is-now-generally-available | GA Sep 2025; mention→draft-PR in ephemeral Actions env; #1 documented complaint = unconditional trigger / ignored intent (GitHub Community #190027) |
| Claude Code GitHub Action (`@claude`) | https://code.claude.com/docs/en/code-review | Closest `claude -p` lineage analog; `@mention` is an app-level `if`-condition convention, not a platform primitive |
| Devin (Cognition) — autonomous PR review/fix | https://cognition.ai/blog/devin-101-automatic-pr-reviews-with-the-devin-api | Cloud SaaS; pre-push git hook blocks agent pushes; "extra set of eyes, not a replacement" |
| Comparable bots (CodeRabbit, Ellipsis, Qodo Merge, Greptile, Sweep) | `prd-pr-auto-remediation-v2-0/research/web-02-web-research-topic-2.md` (§Area 1) | Review-vs-fix market split; Greptile 82% bug-catch benchmark; Ellipsis closest commercial fix-implementing peer |
| Market sizing (treat trend, not absolute $) | `prd-pr-auto-remediation-v2-0/research/web-01-web-research-topic-1.md` (§4) | Agentic-dev market estimates diverge 100×; "autonomous pull request resolution" named an emerging high-value use case |

### 27.2 Technical Documentation

> Source specs and **verified** in-repo reuse anchors. The `superclaude remediate` feature is greenfield (`src/superclaude/cli/remediate/` does not exist [CODE-VERIFIED]); anchors below are the existing primitives it builds on.

| Document / Anchor | Link / Path | Description |
|----------|------|-------------|
| V2.0 Merged-Requirements Spec | `merged-requirements.md` (this brainstorm) | The driving specification this PRD documents |
| V1.0 Predecessor Spec | `.dev/brainstorms/20260610-234750-pr-review-auto-remediation/merged-requirements.md` | "PR Review Auto-Remediation Monitor (V1.0)"; V2.0 is a **host swap** (in-session → headless), not a logic rewrite [CODE-VERIFIED lineage] |
| `ClaudeProcess` headless executor | `src/superclaude/cli/pipeline/process.py:72` | Runner's load-bearing reuse anchor; `build_command()` + stdin prompt delivery (64 KiB chunked, 16 MiB guard) [CODE-VERIFIED]. **Gaps:** no `cwd` param; `build_env()` is additive-only (`os.environ.copy()`) — cannot satisfy INV-001/SC-7 allowlist without a code change |
| `pr_submit/` V1.0 decision core | `src/superclaude/pr_submit/` (`fsm.py`, `severity_router.py`, `classifier.py`, `detection.py`, `models.py`) | Tested decision core (autonomy gate, round counter `DEFAULT_MAX_ROUNDS=2`/`HARD_CAP=5`, severity routing, `DetectionContractLocked`) — **omitted from the spec's Reuse Map**; landing in parallel (git-untracked). `loop_guard.py`/`run_log.py`/`recovery.py` have since landed **built + tested** (`test_loop_guard.py`/`test_run_log.py`/`test_crash_recovery.py`) [CODE-VERIFIED] |
| `remediate_executor.py` (closest R2/R4 analog) | `src/superclaude/cli/roadmap/remediate_executor.py` | Existing `ClaudeProcess`-driven remediation orchestrator: file allowlist, atomic snapshot/rollback, retry, diff-size guard, patch-apply [CODE-VERIFIED] |
| Severity rubric (S1 / §17) | `src/superclaude/skills/sc-auggie-review-protocol/refs/severity-rubric.md` | 5-tier rubric; "severity_hint is a hint, not authoritative" — already compiled into `pr_submit.severity_router` [CODE-VERIFIED] |
| `gh`-posting precedent (H4 template) | `src/superclaude/skills/sc-auggie-review-protocol/SKILL.md:304–315,349` | Summary/inline comment posting + strict `--comment` (never `--approve`/`--request-changes`). Reply-to-thread + GraphQL `resolveReviewThread` are **net-new in Python** (no committed Python caller; a reference bash flow has since landed in the untracked parallel V1 `sc-pr-submit-protocol/scripts/reply-resolve-thread.sh`) [CODE-VERIFIED] |
| Atomic-write / state persistence reuse | `src/superclaude/cli/swarm/state.py` (`write_state`), `cli/install_hooks.py:443`, `cli/recommend/cache.py` | tmp + `os.replace` atomic-write idiom for the §10 ledger (spec says `os.rename`; code uses `os.replace`) [CODE-VERIFIED]. Per-PR Python `flock` is net-new (only fail-open bash precedent exists) |
| CLI-group registration seam | `src/superclaude/cli/main.py:400–438` | Deferred-import + `main.add_command(..., name="remediate")` with `# noqa: E402,I001` — required wiring step (omitting it ships a dead group) [CODE-VERIFIED] |
| Fork-only `--repo` rule (C5 / H5) | project `CLAUDE.md` + memory `feedback_pr_target_fork_only.md` | `--repo IronbellyOrg/IronClaude` enforced today by **prose only**; no Python `gh` caller exists in the repo — H5 is the first code-level enforcement [CODE-VERIFIED] |

### 27.3 Design Assets

> **N/A for this feature.** The product surface is a `superclaude remediate` CLI group + a systemd service + a ~4-token `@bot` mention grammar (autonomy level, `--depth`, `--scope`, `--rounds`). There is no GUI, web surface, or new slash command for end users (`research/08-agent-8.md` §3). No wireframes/mockups/component-library apply.

### 27.4 Standards, Security & Business References

> External standards and incident evidence that anchor the threat model and the on-prem/governance positioning.

| Document | Link | Description |
|----------|------|-------------|
| OWASP LLM01:2025 — Prompt Injection | https://genai.owasp.org/llmrisk/llm01-prompt-injection | #1 LLM risk; no fool-proof prevention → mandates defense-in-depth (our layered design) |
| OWASP Top 10 for Agentic Applications (Dec 2025) | `prd-pr-auto-remediation-v2-0/research/web-03-web-research-topic-3.md` (§2.1) | Names prompt injection the leading agentic risk |
| OWASP AI Agent Security Cheat Sheet | https://cheatsheetseries.owasp.org/cheatsheets/AI_Agent_Security_Cheat_Sheet.html | Least-privilege tools, untrusted-data segregation, human approval for high-risk actions, immutable audit logs — design is aligned by construction |
| CSA Labs — Prompt Injection in AI-Powered GitHub Actions (May 2026) | https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-github-actions-security-20260503-csa-st | Prescribes "architectural separation of reasoning layer from credential-holding execution layer" — a 1:1 description of the Runner/Dispatcher split |
| "Comment and Control" (Aonan Guan, JHU, Apr 2026) | https://oddguan.com/blog/comment-and-control-prompt-injection-credential-theft-claude-code-gemini-cli-github-copilot | PR/issue comments leaked secrets from Claude Code, Gemini CLI, and Copilot Agent — the exact threat class the product neutralizes |
| Design Patterns for Securing LLM Agents (Anthropic/ETH/DeepMind) | https://arxiv.org/html/2506.08837v2 | Dual-LLM, blast-radius minimization — theoretical foundation for the split host |
| AWS AgentCore — hosting coding agents | https://aws.amazon.com/blogs/machine-learning/its-safe-to-close-your-laptop-now-hosting-coding-agents-on-amazon-bedrock-agentcore | "Never put the token in the VM"; short-lived scoped tokens — independent convergence on the split-host model |
| GitHub self-hosted runner reference | https://docs.github.com/en/actions/reference/runners/self-hosted-runners | Ephemeral-runner guidance + caveat that ephemerality is not a complete control (pair with sandbox) |
| Anthropic 2026 Agentic Coding Trends Report | https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf | "Collaborative, not fully delegated" — supports propose-only default |
| EU AI Act high-risk compliance deadline | `prd-pr-auto-remediation-v2-0/research/web-01-web-research-topic-1.md` (§3.4) | August 2026 — a buyer-facing positioning anchor for the on-prem posture |

---

## 28. Maintenance & Ownership

### 28.1 Document Ownership

> **Note:** Human owners are unassigned in this Draft (frontmatter `assigned_to: product-team`, `coordinator: product-manager`). Roles below reserve the responsibilities; assign before approval.

| Role | Name | Responsibility |
|------|------|----------------|
| **Primary Owner** | [TBD — product-team] | Overall PRD accuracy, scope, autonomy-lattice/propose-only decisions, Open-Questions resolution |
| **Technical Owner** | [TBD — Engineering Lead] | Split-host architecture, reuse anchors (`ClaudeProcess`, `pr_submit/`, severity rubric), accuracy of all `file:line` citations |
| **Security Owner** | [TBD — Security Lead] | Secret-separation (INV-001/SC-7), `--repo` chokepoint (C5/H5), injection-containment requirements |
| **Backup Owner** | [TBD] | Coverage when primary unavailable |

> **CRITICAL — cross-build coordination:** The V1.0 `pr_submit/` decision core is **landing in parallel** with this PRD (untracked, ~60% built, on branch `fix/prd-advisory-gate`). Ownership MUST coordinate so V2.0's `cli/remediate/` host layer **extends** `pr_submit`'s pure core (FSM, severity router, models) rather than forking a divergent autonomy/round/severity machine — shipping two decision cores would be a Source-of-Truth/duplication violation (`research/04-agent-4.md` G-1, `research/06-agent-6.md` §C).

### 28.2 Review Schedule

> **Note:** High-level review cadence is defined in the Contract Table (Completeness Status section). This section captures detailed scheduling for each review type.

| Review Type | Next Date | Participants |
|-------------|-----------|--------------|
| **Full Review** | [TBD — before TDD hand-off] | Product, Engineering, Security, QA leads |
| **Technical Review** | [TBD] | Engineering + Security; re-verify reuse citations against live source |
| **Security Review** | [TBD — gate before any `gh`-calling code] | Security Lead; validate INV-001/SC-7, C5/H5 `--repo` chokepoint |
| **§21.3 Probe Gate** | [TBD — hard prerequisite before parser/H4 code] | Engineering; lock `in_reply_to_id` / `databaseId` / Augment bot login from a throwaway fixture PR |
| **Ad-Hoc Review** | - | Triggered by major changes (e.g., an Open Decision OD-1…OD-4 resolving) |

### 28.3 Update Process

1. **Propose Changes**: Comment on the specific section or open an issue.
2. **Re-verify code citations**: Before relying on any `file:line` anchor, perform a fresh Read — the source spec carried stale citations (`swarm/commands.py:2269`, `~/.aienv` chmod-600, `build_env()` allowlist mechanism). Mark capability claims `[CODE-VERIFIED]` only when confirmed against live source.
3. **Review with Stakeholders**: Route to the relevant lead; security-invariant changes require the Security Owner.
4. **Coordinate with the `pr_submit` build**: For any change touching the shared decision core, confirm with the V1.0 owner before editing.
5. **Update Document**: Incorporate approved changes; keep Source-of-Truth discipline (`src/superclaude/` → `make sync-dev`).
6. **Increment Version**: Update version number and Document History.
7. **Notify Team**: Announce changes with a summary; flag any change to the autonomy lattice, push budget, or secret boundary.
8. **Archive Old Version**: Retain previous versions for reference.

---

## Appendices

### Appendix A: Glossary

| Term | Definition |
|------|------------|
| **Dispatcher** | The long-lived, credential-holding systemd daemon that polls GitHub, runs the authorization gate, claims triggers, and performs all host-side GitHub I/O (push, reply, resolve). The "execution/policy layer" of the split host. |
| **Runner** | The ephemeral, sandboxed, per-trigger `claude -p` process that reads the untrusted `opComment` and produces a fix. Holds no consequential secrets. The "reasoning layer" of the split host. |
| **opComment** | The parent review comment (resolved via `in_reply_to_id`) whose body describes the issue to remediate. Always treated as untrusted DATA inside a CONTROL/DATA envelope — never as instructions. |
| **Replier** | The author of the `@bot` mention reply. The **sole action authority** — their live collaborator permission is the authorization subject (not the parent-comment author). |
| **CONTROL/DATA envelope** | The JSON structure delivered to the Runner via stdin: `control` carries parsed flags/metadata; `data` carries the untrusted opComment body. Structurally separates instructions from untrusted text. |
| **Autonomy lattice** | The ordered capability ceiling `propose < patch < fix < push < resolve`; effective level = minimum over {requested flag, authorization projection, validation}. Default (no flag) = `propose`. |
| **`needs_human_decision` HALT** | A short-circuit that escalates a finding (ambiguous intent / security trade-off / API-contract change / multiple valid fixes) to a human PENDING reply instead of acting, even at the top autonomy level. |
| **Two-phase ledger** | The disk-authoritative, append-only intent→outcome record. An intent without a matching outcome on restart triggers RESUME (re-verify), never silent re-execution. |
| **Push budget** | Per-PR cap on remediation rounds (default 2, hard cap 5). A re-review increments the round only when PR head SHA == the bot's recorded push SHA (exact-SHA correlation). |
| **Split-host architecture** | The separation of the reasoning layer (Runner, no credentials, processes untrusted text) from the credential-holding execution layer (Dispatcher) — CSA Labs' prescribed "fundamental mitigation" for prompt injection. |
| **Probe-first gate (§21.3)** | The hard prerequisite of locking unknown GitHub-API shapes (`in_reply_to_id`, `databaseId`, Augment bot login, `resolveReviewThread`) from a throwaway fixture PR before any parser/threading code. |
| **`gh_call()` chokepoint (H5)** | The single wrapper through which every `gh` invocation routes, unconditionally injecting `--repo IronbellyOrg/IronClaude`. First code-level enforcement of the fork-only rule. |

### Appendix B: Acronyms

| Acronym | Meaning |
|---------|---------|
| AC-n | Acceptance Criterion (e.g., AC-1 authorization correctness, AC-3 injection containment, AC-4 `--repo` injection, AC-7 secret-scrape) |
| C5 | Constraint 5 — fork-only PR targeting (`--repo IronbellyOrg/IronClaude`) |
| CSA | Cloud Security Alliance |
| CVE | Common Vulnerabilities and Exposures |
| Dn | Dispatcher component (D1 CLI group, D2 daemon, D3 ingest, D4 grammar, D5 authz, D6 parent resolution) |
| Hn | Host-side component (H1 ledger, H2 autonomy gate, H3 push, H4 reply/resolve, H5 `gh` wrapper) |
| INV-n | Invariant (e.g., INV-001 secret isolation, INV-010 correct-thread resolution, INV-015 egress containment) |
| JTBD | Jobs To Be Done |
| OD-n | Open Decision (OD-1 sandbox tech, OD-2 push token, OD-3 push budget, OD-4 `patch` semantics) |
| OWASP | Open Worldwide Application Security Project |
| PAT | Personal Access Token |
| Rn | Runner component (R1–R4) |
| RICE | Reach × Impact × Confidence / Effort (prioritization framework) |
| Sn | Shared component (S1 severity routing, S2 deploy) |
| SC-n | Success Criterion / safety control (e.g., SC-2 envelope, SC-4 `--repo`, SC-5/SC-6 counter durability, SC-7 secret isolation) |
| SoT | Source of Truth |
| TA/BA/UA | Technical / Business / User Assumption |

### Appendix C: Technical Architecture Diagrams

Detailed architecture diagrams (split-host topology, sandbox egress allowlist, two-phase ledger state machine) are deferred to the downstream **TDD**. The split-host model is summarized in §14.1; the trigger/authz/envelope flow in §22.1 (F1 happy path) and the API contracts in §25.

### Appendix D: User Research Data

This PRD is grounded in (1) a parallel **codebase reuse verification** (research passes 01–08, verifying reuse anchors against live source) and (2) **web/market research** (web-01–03: competitive landscape, the 2026 prompt-injection incident record, security-standards alignment). See §27.1 / §27.4 for the source ledger. No primary customer-interview data was collected for this internal/on-prem feature; the primary persona (Maya) and operator/security personas are derived from the framework's existing maintainer workflow and the named market evidence.

### Appendix E: Financial Projections

**N/A.** This is an internal/on-prem platform capability with no independent revenue model. Cost drivers (LLM token consumption, sandbox compute, daemon residency) are captured in §18.1; market-category context is in §5.2. Any future externalization defers to the Platform PRD.

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-11 | product-team (synthesis assembly) | Initial draft — assembled from 9 synthesis fragments (synth-01…09) over the V2.0 merged-requirements spec; full 28-section coverage with split-host security architecture, autonomy lattice, and probe-first build sequence |

---

## Document Provenance

> **How this document was produced.** This PRD was assembled by consolidating nine synthesis
> fragments — each itself derived from a parallel research fan-out — into the project's standard
> PRD template (`.claude/templates/workflow/05_prd_template.md`). No new findings were introduced
> during assembly; content fidelity to the synthesis files was preserved with only minimal
> transitional text.

| Aspect | Detail |
|--------|--------|
| **Output** | `pr-auto-remediation-v2-0-prd.md` (this file) |
| **Template** | `.claude/templates/workflow/05_prd_template.md` (v1.0) |
| **Driving spec** | `merged-requirements.md` (V2.0, this brainstorm) |
| **Synthesis sources** | `prd-pr-auto-remediation-v2-0/synthesis/synth-01…09` (9 fragments) |
| **Research corpus** | `prd-pr-auto-remediation-v2-0/research/` — 8 codebase-investigator passes (01–08) + 3 web/market passes (web-01–03) |
| **Evidence convention** | `[CODE-VERIFIED]` = confirmed against current source; `[CODE-CONTRADICTED]` = spec citation does not hold as written; `[NEW]`/`[NET-NEW]` = greenfield, no in-repo precedent; `[SPEC]` = required behavior, not yet built; `[EXTERNAL]` = market/standards corroboration |
| **Greenfield caveat** | `src/superclaude/cli/remediate/` does **not** exist today; every V2.0 capability is a forward-looking requirement except the explicitly `[CODE-VERIFIED]` reuse anchors (`ClaudeProcess`, `pr_submit/` decision core, severity rubric, swarm atomic-write, `gh`-posting precedent) |
| **Assembly date** | 2026-06-11 |
| **Status** | 🟡 Draft — pending lead sign-off and §21.3 probe-locked GitHub shapes |

<!-- END PRD — PR Auto-Remediation V2.0 (Mention-Triggered Headless Bot) -->
