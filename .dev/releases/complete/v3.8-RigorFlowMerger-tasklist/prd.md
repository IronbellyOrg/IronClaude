---
id: "FR-RFMERGE-PRD-CORE"
title: "RFMerger Refresh — Product Requirements Document (PRD)"
description: "Refreshed product requirements for selectively borrowing RigorFlow execution-time mechanisms into the SuperClaude sc:tasklist generator, rebased onto current src/superclaude source-of-truth"
version: "1.0"
status: "🟡 Draft (reviewed-planning)"
type: "📋 Product Requirements"
priority: "🔥 Highest"
created_date: "2026-06-18"
updated_date: "2026-06-18"
assigned_to: "product-team"
autogen: false
autogen_method: ""
coordinator: "product-manager"
parent_task: "TASK-RF-rfmerger-refresh-20260618-172224"
depends_on:
- ".dev/releases/current/v3.8-RigorFlowMerger-tasklist/spec.md"
- ".dev/releases/current/v3.8-RigorFlowMerger-tasklist/artifacts/refresh-requirements-ledger.md"
- ".dev/releases/current/v3.8-RigorFlowMerger-tasklist/artifacts/refresh-validation-matrix.md"
related_docs:
- ".dev/releases/current/v3.8-RigorFlowMerger-tasklist/tdd.md"
- "src/superclaude/skills/sc-tasklist-protocol/SKILL.md"
tags:
- prd
- requirements
- product-core
- rfmerger
- sc-tasklist
template_schema_doc: "src/superclaude/templates/workflow/05_prd_template.md"
estimation: ""
sprint: ""
due_date: ""
start_date: ""
completion_date: ""
blocker_reason: "P2 and P5 human decisions are RECORDED (2026-06-19): P2 = retain-with-full-set-revalidation-and-guards, P5 = retain-advisory-only; downstream implementation-tasklist generation is unblocked"
ai_model: ""
model_settings: ""
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
task_type: "static"
---

# RFMerger Refresh — Product Requirements Document (PRD)

> **WHAT:** Refreshed product requirements for selectively borrowing RigorFlow (RF) execution-time mechanisms into the SuperClaude `sc:tasklist` generator, rebased onto the current `src/superclaude/...` source-of-truth.
> **WHY:** Records the inferred release intent of the April-2026 RFMerger investigation as a reviewed-planning draft, so a later, separate implementation step has an accurate WHAT/WHY anchored to today's surface — not the drifted historical one.
> **HOW TO USE:** Product, engineering, and QA reference this PRD during the document-review checkpoint. The two P2 and P5 human decisions are now RECORDED (2026-06-19), so downstream implementation-tasklist generation is authorized once review sign-off is complete.

> **CRITICAL:** This PRD is a **reviewed-planning draft**. The two human decisions P2 and P5 are now **RECORDED (2026-06-19): P2 = `retain-with-full-set-revalidation-and-guards`, P5 = `retain-advisory-only`** (explicit human choices, not defaults). With both decisions recorded, downstream implementation-tasklist generation is **UNBLOCKED** (subject to human review sign-off of `spec.md` / `prd.md` / `tdd.md`). The P2/P5 decisions never blocked this document's QA/review.

### Document Lifecycle Position

| Phase | Document | Ownership | Status |
|-------|----------|-----------|--------|
| **Requirements** | **This PRD** | **Product** | **🟡 Draft (reviewed-planning, not implementation-ready)** |
| Requirements (release intent) | `spec.md` (sibling) | Product/Eng | 🟡 Draft |
| Design | `tdd.md` (sibling) | Engineering | 🟡 Draft |
| Implementation | Tech Reference | Engineering | ⛔ Blocked — pending review sign-off (P2/P5 decisions recorded 2026-06-19) |

### Tiered Usage

| Tier | When to Use | Sections to Skip |
|------|-------------|------------------|
| **Lightweight** | Single-feature PRD, <10 sections | Value Proposition Canvas, Customer Journey Map, API Contract Examples, Appendices |
| **Standard** | Multi-feature product, most PRDs — **this PRD** | Market-sizing/revenue subsections (N/A for an internal developer-tooling refactor) |
| **Heavyweight** | Platform PRD, 28 sections, cross-team | None — complete all sections |

> **Note:** This is a **feature/component PRD** for an internal developer-tooling refactor (the `sc:tasklist` generator). Per the template's SCOPE NOTES, market sizing, TAM/SAM/SOM, revenue projections, pricing, GTM, and platform-level compliance are **N/A** and intentionally omitted; metrics live in Section 19.

---

## Document Information

| Field | Value |
|-------|-------|
| **Product Name** | RFMerger Refresh — Selective RigorFlow Borrows into `sc:tasklist` |
| **Product Type** | Feature/Component PRD (internal developer tooling — the `sc:tasklist` generator) |
| **Product Owner** | Product team (SuperClaude framework) |
| **Engineering Lead** | Engineering team (`sc:tasklist` / `task-builder` / `reflect` maintainers) |
| **Design Lead** | N/A (no end-user UI surface) |
| **Maintained By** | RFMerger refresh owners; carried in this release directory |
| **Stakeholders** | `sc:tasklist` maintainers, reflect-gate maintainers, task-builder maintainers, QA |
| **Status** | 🟡 Draft (reviewed-planning, not implementation-ready) |
| **Target Release** | v3.8-RigorFlowMerger-tasklist |
| **Last Verified** | 2026-06-18 against current `src/superclaude/...` source (`sc-tasklist-protocol/SKILL.md`, `commands/tasklist.md`, `cli/tasklist/*`) |

### Document Approval

> **Important:** The P2/P5 human decisions are recorded (2026-06-19). This PRD reaches "Approved" once the document-review checkpoint records sign-off. Until then it stays a reviewed-planning draft.

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Manager | _pending review_ | __________ | _pending_ |
| Engineering Lead | _pending review_ | __________ | _pending_ |
| QA Lead | _pending review_ | __________ | _pending_ |
| P2 decision recorded | `retain-with-full-set-revalidation-and-guards` (explicit human choice, not a default) | human operator | 2026-06-19 |
| P5 decision recorded | `retain-advisory-only` (explicit human choice, not a default) | human operator | 2026-06-19 |

---

## Completeness Status

**Completeness Checklist:**

- [x] Section 1: Executive Summary — Complete
- [x] Sections 2-4: Problem, Background, Vision — Complete
- [ ] Sections 5-9: Business Context, JTBD, Personas, Value Prop, Competitive — Partial (market/competitive subsections N/A for an internal refactor; JTBD + personas provided)
- [x] Sections 10-13: Assumptions, Dependencies, Scope, Open Questions — Complete
- [x] Section 14: Technical Requirements — Complete
- [x] Sections 19-20: Success Metrics, Risk Analysis — Complete
- [x] Section 21: Implementation Plan (release intent — P2/P5 decisions recorded 2026-06-19; gated behind review sign-off) — Complete
- [x] Section 25: API/Contracts Impacts — Complete
- [x] Living-document status — Complete
- [x] Zero `SC_PLACEHOLDER` double-brace sentinels remain — Verified
- [ ] Reviewed by product/eng/QA — Pending review checkpoint

**Contract Table:**

| Element | Details |
|---------|---------|
| **Dependencies** | `spec.md`, `refresh-requirements-ledger.md`, `refresh-validation-matrix.md`; current `src/superclaude/skills/sc-tasklist-protocol/*`, `commands/tasklist.md`, `cli/tasklist/*` |
| **Upstream** | Feeds from: April-2026 RFMerger investigation (HISTORICAL-ONLY), Phase 1 discovery, refresh requirements ledger |
| **Downstream** | Feeds to: sibling `tdd.md`; after the review checkpoint records P2+P5, a separate `/task-builder` handoff |
| **Change Impact** | Notify: `sc:tasklist` / reflect / task-builder maintainers, QA |
| **Review Cadence** | As-needed (release-scoped); next review = the document-review checkpoint |
| **Living Document** | This PRD evolves as P2/P5 decisions are recorded and review feedback lands — see Document History |

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
19. [Success Metrics & Measurement](#19-success-metrics--measurement)
20. [Risk Analysis](#20-risk-analysis)
21. [Implementation Plan (Placeholder)](#21-implementation-plan-placeholder)
25. [API & Contracts Impacts](#25-api--contracts-impacts)
28. [Maintenance & Living-Document Status](#28-maintenance--living-document-status)

> **Note:** Sections 15-18 and 22-27 of the full template (Technology Stack, UX, Legal, Business/GTM, Customer Journey, Error UX, Design, Contributors, Related Resources) are **N/A or folded** for this internal-tooling refactor and are intentionally omitted; the kept sections match this task's required set.

---

## 1. Executive Summary

The April-2026 RigorFlow-Merger (RFMerger) investigation produced a five-proposal package (P1 Context-Armed Steps, P2 Bounded Patch Loop, P3 DNSP, P4 Evidence-Anchored Validation, P5 Feedback-Driven Tier Calibration) proposing that the SuperClaude `sc:tasklist` generator borrow selected RigorFlow (RF) execution-time mechanisms. That package was authored against a `sc:tasklist` surface that has since drifted — it assumed a 10-stage model, an RF agent-team flow (`/rf:*`, TeamCreate/SendMessage), a `.gfdoc` shell harness, an external `llm-workflows` / `/config/.claude` source-of-truth, and a `sc:task-unified` patch delegate, **none of which are operative today**. This PRD records the **refreshed release intent**: per proposal, what to retain in its adversarially-revised form, what to defer to an explicit human decision, and what to keep advisory — all rebased onto the current **11-stage** generator (Stages 1-10 plus the **Stage 10.5 Pre-Reflect Sign-off** audit gate) with `sc:task` as the patch delegate, `/task` for MDTM execution, and `src/superclaude/...` as the single source-of-truth.

This is a **reviewed-planning draft**. Three proposals are retained in conservative, adversarially-revised forms (P1, P3, P4); the two human decisions P2 and P5 are now **RECORDED (2026-06-19): P2 = `retain-with-full-set-revalidation-and-guards`, P5 = `retain-advisory-only`** (explicit human choices, not defaults). The product value is a more robust, self-contained, evidence-anchored tasklist generator that preserves the existing determinism guarantee ("same roadmap → same scored tiers"; and, with P5 advisory retained, "same roadmap + same `feedback-log.md` → same advisory output") and never lets hidden feedback mutate deterministic tier scores. With both decisions recorded, downstream implementation — source edits, tests, and any `/task-builder` tasklist generation — is **UNBLOCKED**, subject to human review sign-off.

**Key Success Metrics:**

- **Determinism preserved**: Same roadmap (+ same `--spec`) → same scored tiers (always; scored tiers remain a pure function of the roadmap). When P5 advisory is retained, a byte-identical bundle additionally requires the same `feedback-log.md` (the advisory varies with `feedback-log.md`); byte-identical bundle ⇔ same `(roadmap, --spec, feedback-log.md)` tuple (target: 100% — no hidden-feedback mutation of scored tiers).
- **Auditability**: 100% of P3-synthesized validation findings carry the `source: "synthetic-dnsp"` provenance marker.
- **Zero stale-token regression**: 0 stale tokens (`/rf:*`, `.gfdoc`, `llm-workflows`, `/config/.claude`, `sc:task-unified`) promoted to current operative instructions across the refreshed documents.
- **Coverage hardening**: The currently-untested `--no-reflect` / Stage 10.5 generation contracts gain direct test assertions in the refreshed test plan.

---

## 2. Problem Statement

### 2.1 The Core Problem

**The RFMerger design package is anchored to a `sc:tasklist` surface that no longer exists, so acting on it verbatim would reintroduce stale tokens as operative instructions and re-derive proposals against a vanished architecture.**

- **Current state**: The historical package assumes a 10-stage tasklist model, `/rf:*` agent-team commands, a `.gfdoc` shell-script execution harness, an external `llm-workflows` / `/config/.claude` source-of-truth, and a `sc:task-unified` Stage-9 patch delegate. The current generator instead runs an **11-stage** model with a **Stage 10.5** reflect gate, delegates patch execution to `sc:task`, executes MDTM work through the `/task` skill loop, and treats `src/superclaude/...` as the single source-of-truth with `.claude/` as a generated mirror (evidence: `sc-tasklist-protocol/SKILL.md:1525-1558`, `:130-132`, `:1409-1427`; `research/02`).
- **Who is affected**: Maintainers of `sc:tasklist`, the reflect gate, and `task-builder`; and any downstream automation that would consume the historical package to generate implementation work.
- **Impact of not solving**: A builder reading the historical package would (a) reintroduce stale tokens as operative edit targets, (b) re-derive proposals against a non-existent surface, and (c) ship structural-correctness defects the original adversarial validation already flagged — notably P2's subset-only re-validation oscillation risk and P5's hidden-feedback determinism violation.
- **Barriers today**: The historical artifacts are written with confident, operative phrasing; without an explicit refresh + stale-token quarantine, a downstream reader cannot tell which tokens are HISTORICAL-ONLY from which are current.

### 2.2 Why Existing Solutions Fall Short

**The historical RFMerger package (as written)**:

- Targets a 10-stage model and `/rf:*` / `.gfdoc` / `sc:task-unified` surfaces that are not operative in the current repository.
- Proposes P2 as a subset-only re-validation loop (oscillation/regression risk) and P5 as a tier-score mutation from hidden `feedback-log.md` input (determinism violation).
- Treats `/config/.claude` and `llm-workflows` as the source-of-truth, which would mis-target every edit.

**Doing nothing (drop the package)**:

- Discards three genuinely valuable, adversarially-validated mechanisms (P3 DNSP — the adversarial winner; P4 evidence passthrough; P1 conservative step context) that map cleanly onto the current generator.
- Loses the two carried open questions (OQ-1 reflect-test path, OQ-2 deliverable count) that a future builder would otherwise re-discover.

**Implementing verbatim now (no refresh, no human gate)**:

- Auto-defaults P2 and P5, shipping a determinism violation and an oscillation risk the adversarial pass explicitly flagged.

### 2.3 Why This Feature Is Required

A refresh is the only path that keeps the validated value (P1/P3/P4) while neutralizing the two structural-correctness defects (P2/P5) — by rebasing onto current source, quarantining stale tokens, and recording P2/P5 as explicit human decisions rather than engineering defaults. It unlocks a later, safe implementation step without committing to a wrong-surface design now.

---

## 3. Background & Strategic Fit

> **SCOPE NOTE applied:** This is a feature/component PRD. Per the template, this section focuses on *why this refresh is needed now* and what bets it makes — not platform-level market trends or revenue.

### 3.1 Why Now?

1. **Surface drift is confirmed, not assumed**: Phase 1 discovery and `research/02`–`research/03` verified the current 11-stage / Stage-10.5 / `sc:task` / `src/superclaude/...` surface against source, so the rebase targets are known.
2. **The adversarial dispositions already exist**: The historical adversarial validation produced revised scores and conservative forms for all five proposals; the refresh consumes those rather than re-litigating them.
3. **A clean human-decision boundary was applied**: P2 and P5 are the only two proposals whose disposition is a product/risk judgment rather than an engineering default — so each was routed to an explicit human decision (both now recorded 2026-06-19 as `retain-*`) rather than auto-defaulted.
4. **Carried gaps are cheap to record now**: The untested `--no-reflect` / Stage 10.5 contracts and the OQ-1/OQ-2 open items are best captured in a refresh before they are silently lost.

### 3.2 How This Fits Framework Objectives

- **Mission alignment**: Keeps `sc:tasklist` deterministic, evidence-anchored, and self-contained — core SuperClaude generation principles.
- **Source-of-truth discipline**: Reinforces that all edits resolve under `src/superclaude/...` with `.claude/` as a generated mirror.
- **Reliability**: P3's all-agents-fail guard and P4's evidence passthrough harden validation without overlapping the existing Stage 10.5 reflect gate.

### 3.3 Strategic Bets

1. **Conservative-over-clever**: The conservative, adversarially-revised forms (task-level context block, quality-gate passthrough) deliver most of the value at a fraction of the risk of the original heavyweight mechanisms.
2. **Human-gate the risky two**: Routing P2/P5 to explicit human decisions prevents a synthesis pass from silently shipping a determinism violation or an oscillation loop.
3. **Determinism is non-negotiable**: Preserving "same roadmap → same scored tiers" (scored tiers stay roadmap-pure; the P5 advisory, retained advisory-only, is a function of `(roadmap, feedback-log.md)` and never feeds back into scored tiers) is treated as a hard invariant, not a tunable.

---

## 4. Product Vision

**"A `sc:tasklist` generator that is more robust and evidence-anchored, with self-contained tasks — without sacrificing determinism, and without ever letting hidden feedback mutate deterministic tier scores."**

When this refresh succeeds, the retained proposals attach cleanly to the current 11-stage pipeline: P1 adds an optional, additive task-level `## Execution Context` block; P4 passes existing quality-gate evidence into validation prompts; P3 keeps validation moving past a single failed agent while, on total failure, following the all-agents-fail escalation path (surfacing it as a typed `StageError` is release intent / an implementation-time decision, not current behavior) and stamping every synthesized finding with provenance. P2 and P5 remain explicit, recorded human decisions — implemented only if and when a human chooses to retain them, and even then only in their determinism-preserving, guarded forms. The generator stays a pure function of the roadmap, ships its bundle on every Stage 10.5 verdict, and respects the `--no-reflect` escape hatch exactly as it does today.

---

## 5. Business Context

> **SCOPE NOTE applied:** Market sizing (TAM/SAM/SOM), revenue projections, and a KPI table are **N/A** for an internal developer-tooling refactor. Per the template, this section gives only the business justification and a forward reference to Section 19 (the single source of truth for metrics).

**Why this matters to the framework:** `sc:tasklist` is a core generation surface; defects in it propagate into every downstream Sprint/MDTM execution. The cost driver here is *correctness risk*, not money — a determinism violation (P5 as originally proposed) or a patch-loop oscillation (P2 as originally proposed) would erode trust in generated bundles and cost engineer debugging time. The refresh's value is risk reduction plus three robustness wins, achieved with no CLI surface change and full backward compatibility.

All measurable outcomes are defined in **Section 19 (Success Metrics & Measurement)** — this section does not duplicate them.

---

## 6. Jobs To Be Done (JTBD)

> **Framework:** "When [situation], I want to [motivation], so I can [expected outcome]."

### 6.1 Primary Jobs

**Job 1: Trust the generated tasklist**

- **When**: A maintainer generates a tasklist bundle from a roadmap.
- **I want to**: Get the same bundle for the same input and see evidence behind validation findings.
- **So I can**: Rely on the output without re-checking it by hand.
- **Current alternatives**: Manual spot-checks; re-running generation and diffing.
- **Pain with alternatives**: Non-determinism (if tiers were mutated from hidden feedback) makes diffs meaningless and erodes trust.

**Job 2: Keep validation moving past a single flaky agent**

- **When**: One Stage-7 validation agent fails its retry while others succeed.
- **I want to**: Proceed with a conservative, clearly-marked synthetic finding instead of blocking the whole pipeline.
- **So I can**: Finish generation while still flagging the affected range for review.
- **Current alternatives**: Hard-fail Stage 7 on any single agent failure.
- **Pain with alternatives**: One transient agent failure blocks an otherwise-complete bundle.

**Job 3: Safely consider the risky borrows (patch loop, tier feedback)**

- **When**: Deciding whether to adopt P2 (bounded patch loop) or P5 (tier calibration).
- **I want to**: Make an explicit, recorded decision rather than inherit a silent default.
- **So I can**: Avoid shipping an oscillation risk or a determinism violation by accident.
- **Current alternatives**: Accept the historical proposal as-written.
- **Pain with alternatives**: The as-written forms carry the exact defects the adversarial pass flagged.

### 6.2 Related Jobs

| Job | Frequency | Importance | Satisfaction with Current Solutions |
|-----|-----------|------------|-------------------------------------|
| Generate a deterministic bundle | Daily | Critical | Medium (no hidden-feedback path today; refresh keeps it that way) |
| Audit synthetic validation findings | As-needed | High | Low (no provenance marker exists yet) |
| Avoid stale-token mis-targeting | Per refactor | High | Low (historical package is full of stale tokens) |

---

## 7. User Personas

> **Note:** "Users" here are internal developers and maintainers of the SuperClaude framework — there is no external end-user persona.

### 7.1 Primary Persona: `sc:tasklist` Maintainer

| Attribute | Details |
|-----------|---------|
| **Demographics** | Senior engineer maintaining the tasklist generator and its 11-stage pipeline |
| **Goals** | Deterministic, evidence-anchored generation; clean attachment points for new mechanisms |
| **Pain Points** | Stale historical designs; non-deterministic inputs; untested reflect-gate contracts |
| **Technical Proficiency** | High |
| **Budget Authority** | Influences (engineering decisions) |
| **Success Metrics** | Determinism preserved; tests green; no stale tokens promoted |

**Quote:** "Give me the validated wins rebased onto the current pipeline — and don't let anything mutate scored tiers behind my back."

**A Day in Their Life:** Reviews a generated bundle, checks the Stage 10.5 sign-off, and needs to trust that the same roadmap will always produce the same scored tiers (and, if P5 advisory is retained, the same advisory for the same `feedback-log.md`) — with scored tiers never mutated by hidden feedback.

### 7.2 Secondary Persona: Reflect-Gate Maintainer

| Attribute | Details |
|-----------|---------|
| **Demographics** | Engineer owning the Stage 10.5 reflect gate and `tests/cli/reflect/` |
| **Goals** | No new mechanism overlaps or double-remediates with the reflect gate |
| **Pain Points** | Proposals (P2) that could remediate the same finding the reflect gate already handles |
| **Technical Proficiency** | High |
| **Budget Authority** | Influences |
| **Success Metrics** | Zero double-remediation; Stage 10.5 advisory semantics unchanged |

**Quote:** "If P2 ships, it must be provably disjoint from Stage 10.5 remediation."

### 7.3 Tertiary Persona: QA / Reviewer

| Attribute | Details |
|-----------|---------|
| **Demographics** | QA engineer running the document gates and the test suites |
| **Goals** | Verifiable acceptance criteria; the carried `--no-reflect`/Stage 10.5 coverage gap closed |
| **Pain Points** | Untested generation contracts; reflect-test path drift (`tests/reflect/` vs `tests/cli/reflect/`) |
| **Technical Proficiency** | High |
| **Budget Authority** | No |
| **Success Metrics** | Required suites green; coverage gap closed |

**Quote:** "The reflect-guard suite lives at `tests/cli/reflect/` — pin the real path."

### 7.4 Anti-Personas (Who This Is NOT For)

| Anti-Persona | Why Not Target |
|--------------|----------------|
| End users of generated apps | This is internal tooling; no end-user surface |
| RF agent-team operators (`/rf:*`) | That flow is HISTORICAL-ONLY and not operative in this repo |

---

## 8. Value Proposition Canvas

> **SCOPE NOTE applied:** For this feature/component PRD the value-proposition canvas is **N/A** — the value contribution is captured in the Problem Statement (S2) and Product Vision (S4).

---

## 9. Competitive Analysis

> **SCOPE NOTE applied:** **N/A** — this is an internal generator refactor with no competing product category. Strategic context lives in S3.

---

## 10. Assumptions & Constraints

### 10.1 Technical Assumptions

| ID | Assumption | Risk if Wrong | Validation Method |
|----|------------|---------------|-------------------|
| TA-1 | The current generator is 11-stage with a Stage 10.5 advisory reflect gate. | Proposals re-derived against the 10-stage model are mis-anchored. | Verified against `sc-tasklist-protocol/SKILL.md:1525-1558`; `research/02`. |
| TA-2 | Stage 9 delegates patch execution to `sc:task` (not `sc:task-unified`); tier uses the `/sc:task` algorithm. | P2's delegate name would be wrong. | Verified against `SKILL.md:130-132,544-548,1409-1427`; `rules/tier-classification.md`. |
| TA-3 | The generator works on roadmap *text*, not a live codebase. | P1's per-step file paths would be hallucinated. | Architecture of the generator; adversarial revision of P1 (22→34/50). |
| TA-4 | `--no-reflect` lives on the slash command, not on `superclaude tasklist validate`; `--dry-run` also sets it. | Misrepresenting the escape hatch. | Verified against `commands/tasklist.md:20-39`; `research/03:30-31`. |

### 10.2 Business / Product Assumptions

| ID | Assumption | Risk if Wrong | Validation Method |
|----|------------|---------------|-------------------|
| BA-1 | P2 and P5 dispositions are product/risk judgments, not engineering defaults. | Auto-defaulting ships a known defect. | Adversarial validation flagged both; each recorded 2026-06-19 as an explicit human `retain-*` choice (not a default). |
| BA-2 | Document QA proceeded independently of the P2/P5 decisions (now recorded); those decisions gate only downstream implementation. | Over-blocking stalls review; under-blocking ships unreviewed work. | Refresh validation matrix human-decision gate semantics. |

### 10.3 User Assumptions

| ID | Assumption | Risk if Wrong | Validation Method |
|----|------------|---------------|-------------------|
| UA-1 | Maintainers value determinism over feedback-driven auto-tuning. | P5 advisory-only would be the wrong call. | Decided by the human: P5 recorded `retain-advisory-only` (2026-06-19). |

### 10.4 Constraints

| Type | Constraint | Impact on Product | Mitigation |
|------|------------|-------------------|------------|
| **Authorization** | Documents-only task: no source edits, no `.claude/` mirror edits, no implementation tasklist. | No code changes ship from this task. | Enforced by the review checkpoint and git status; `/task-builder` is a later step. |
| **Determinism** | Hidden feedback must never mutate deterministic tier scores (the **P5 constraint**). | P5 (retained) is advisory-only. | Scored tiers stay a pure function of the roadmap; determinism test gate. |
| **Source-of-truth** | All future edits target `src/superclaude/...`, then `make sync-dev` + `make verify-sync`; never `.claude/` mirrors. | Edit targets are fixed. | NFR + sync gate; `.claude/{skills,commands,agents,hooks,templates}` never staged. |
| **Human gate** | P2/P5 are explicit human decisions, not defaults; auto-defaulting either would be a halt condition. Both recorded 2026-06-19 (`retain-*`). | Downstream implementation is unblocked. | Review checkpoint recorded both before any tasklist generation. |
| **No-overlap** | Any retained P2 loop must not overlap Stage 10.5 reflect remediation. | Avoids double-remediation. | Qualitative gate; NFR-RFMERGE.2. |

---

## 11. Dependencies

### 11.1 External Dependencies

| Dependency | Type | Owner | Risk Level | Contingency |
|------------|------|-------|------------|-------------|
| `pytest` (UV-run) | Tooling | dev env | Low | Standard test harness |
| Claude subprocess (validation steps) | Tooling | framework | Low | Existing in current pipeline |

### 11.2 Internal Dependencies

| Dependency | Type | Owner | Status | Target Date |
|------------|------|-------|--------|-------------|
| `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (11-stage inline runtime) | Component | tasklist maintainers | Operative | N/A (existing) |
| `src/superclaude/skills/sc-tasklist-protocol/templates/phase-template.md` (read-only mirror) | Template | tasklist maintainers | Operative | N/A (existing) |
| Stage 10.5 reflect gate + `tests/cli/reflect/` | Component | reflect maintainers | Operative | N/A (existing) |
| `sc:task` patch delegate + tier classification | Component | task maintainers | Operative | N/A (existing) |

### 11.3 Cross-Document Dependencies

| Document | Dependency | What We Need | When Needed | Status |
|----------|------------|--------------|-------------|--------|
| `spec.md` (sibling) | Release intent + FR set | P1-P5 dispositions, FR-RFMERGE.1-7, gate criteria | Authored (Step 2.3) | Present |
| `refresh-requirements-ledger.md` | Canonical P1-P5 ledger | Historical→current rebase per proposal | Authored (Step 2.1) | Present |
| `refresh-validation-matrix.md` | Per-output gate contract | Gate obligations + halt conditions | Authored (Step 2.2) | Present |
| `tdd.md` (sibling) | Technical design | Attachment points, test plan detail | Sibling step | Sibling |

---

## 12. Scope Definition

### 12.1 In Scope (this refresh — documents-only)

| Category | Included | Notes |
|----------|----------|-------|
| Release intent | Refreshed PRD (this doc) rebasing P1-P5 onto current source | Reviewed-planning draft only |
| Retained proposals (release intent) | P1 conservative `## Execution Context`; P3 DNSP + guards; P4 quality-gate passthrough | Conservative, adversarially-revised forms |
| Human decisions | P2 = `retain-with-full-set-revalidation-and-guards`, P5 = `retain-advisory-only` (recorded 2026-06-19; explicit choices, not defaults) | Now decided; downstream implementation unblocked |
| Current-behavior fidelity | 11-stage model, Stage 10.5 advisory, `--no-reflect`, `sc:task` delegate | Accurately represented |
| Stale-token quarantine | `/rf:*`, `.gfdoc`, `llm-workflows`, `/config/.claude`, `sc:task-unified` cited HISTORICAL-ONLY only | Each paired with a current rebase target |

### 12.2 Out of Scope (this task)

| Item | Reason | Target Phase |
|------|--------|--------------|
| ❌ Authoring any implementation tasklist | Documents-only task; explicitly forbidden | Later, separate `/task-builder` handoff (after review + P2/P5) |
| ❌ Editing source code or `.claude/` mirrors | Documents-only; SoT discipline | Later implementation step |
| ❌ Invoking `/task-builder` for implementation | Non-blocking later handoff, not work here | After the review checkpoint records P2+P5 |
| ❌ Selecting a default for P2 or P5 | Auto-defaulting either is a halt condition | Human decision at the review checkpoint |
| ❌ Claiming implementation readiness | This is a reviewed-planning draft | After review sign-off + P2/P5 decisions |

### 12.3 Permanently Out of Scope (Non-Goals)

| Item | Reason |
|------|--------|
| ❌ RF mechanism R5 (session management) | Execution-time concept judged N/A to SuperClaude generation |
| ❌ RF mechanism R6 (batch-immutability / UID tracking) | Execution-time concept judged N/A to SuperClaude generation |
| ❌ Re-implementing reflect's own UC-2 P1-P5 fields | A separate, quarantined taxonomy — no semantic correspondence to RFMerger P1-P5 (see Glossary) |
| ❌ Any hidden-feedback mutation of deterministic tier scores | Violates "same roadmap → same scored tiers"; the **P5 constraint** — advisory-only; scored tiers remain roadmap-only; the advisory may read `feedback-log.md` and must never feed back into scored tiers |

---

## 13. Open Questions

> Carried forward from Phase 1 discovery. Both are **out of this PRD's edit scope to resolve** (they require edits to `BUILD-REQUEST.md` / research files); recorded so a downstream builder does not lose them.

| # | Question | Owner | Target Date | Status | Resolution |
|---|----------|-------|-------------|--------|------------|
| OQ-1 | `BUILD-REQUEST.md:15` and `research/07:137` now use `uv run pytest tests/cli/reflect/ -v` (the disk-correct path is `tests/cli/reflect/`, not `tests/reflect/`). | refresh owners | done | ✅ Resolved (fixed at source 2026-06-19) | Fixed at source: `BUILD-REQUEST.md:15` + `research/07:137` now use `tests/cli/reflect/` (with a dated correction note). No further action. |
| OQ-2 | 5-vs-7 output-count taxonomy — **RESOLVED** (see spec §11 OQ-2 and `refresh-validation-matrix.md` "Deliverable taxonomy"): 5 GATED deliverables (spec/prd/tdd/ledger/matrix) + 2 DERIVED control artifacts (`review-checkpoint.md`, `downstream-task-builder-handoff.md`) + 1 process report (`final-validation-evidence-report.md`). | refresh owners | resolved in this package | ✅ Resolved (in-package; research-file residual WAIVED) | Taxonomy fixed in-package; the raw research-file residual (`research/07:46-50` / research-notes) is WAIVED — the refreshed spec/PRD/TDD are the authoritative inputs for any downstream `/task-builder` run and supersede the raw research notes. |
| Q-P2 | P2 disposition: `defer` vs `retain-with-full-set-revalidation-and-guards`. | human reviewer | review checkpoint | 🟢 RECORDED 2026-06-19: `retain-with-full-set-revalidation-and-guards` (explicit choice, not a default) | Recorded at the review checkpoint per `.dev/tasks/to-do/TASK-RF-rfmerger-refresh-20260618-172224/phase-outputs/reviews/p2-human-decision-record.md`; downstream implementation unblocked. |
| Q-P5 | P5 disposition: `defer` vs `retain-advisory-only`. | human reviewer | review checkpoint | 🟢 RECORDED 2026-06-19: `retain-advisory-only` (explicit choice, not a default) | Recorded at the review checkpoint per `.dev/tasks/to-do/TASK-RF-rfmerger-refresh-20260618-172224/phase-outputs/reviews/p5-human-decision-record.md`; downstream implementation unblocked. |

---

## 14. Technical Requirements

> These product requirements describe the **release intent** for the retained RFMerger proposals as rebased onto the current `sc:tasklist` surface. They are traceable to the spec's FR-RFMERGE.1-7 and the canonical P1-P5 ledger. **PR-2 and PR-5 were gated behind the P2/P5 human decisions, which are now RECORDED (2026-06-19: P2 = `retain-with-full-set-revalidation-and-guards`, P5 = `retain-advisory-only`); both are now active implementation requirements.** All edit targets are `src/superclaude/...`; `.claude/` is a generated mirror, never an edit target.

### 14.1 Product Requirements (retained proposals as release intent)

#### PR-1 — P1 Context-Armed Steps (conservative `## Execution Context` block) → **Retain**

| Attribute | Value |
|-----------|-------|
| **Priority** | P1 (Should Have) |
| **Maps to** | spec FR-RFMERGE.1; ledger P1 (Retain, conservative) |
| **Description** | Generated phase tasks may carry an optional task-level `## Execution Context` block including relevant roadmap ref(s) and named "source areas" (not file paths). **Emission rule**: emitted at Stage 4 iff ≥1 roadmap ref resolves for the phase; References-only degraded form when no source areas; omitted when no ref resolves (deterministic — same roadmap → same block). See spec FR-RFMERGE.1 for the exact markdown shape. |
| **User Value** | More self-contained tasks without hallucinated per-step paths. |
| **Edit target (later)** | `src/superclaude/skills/sc-tasklist-protocol/SKILL.md` (inline runtime — the **single authoritative edit target**); the source-side `templates/phase-template.md` reflects the shape (NOT a `.claude/` mirror; do not hand-edit). |
| **Schema-collision boundary** | `task-builder` already mandates a `## Execution Context` section (`task-builder/SKILL.md:1066,1231`). P1 **reuses** the same `References`/`Source areas` sub-field names + no-file-path discipline; the only difference is P1's block is optional, task-builder's is required. No second, incompatible "Execution Context" meaning is introduced. |

**Acceptance Criteria:**

- The block, when emitted, contains roadmap refs and "source areas" only — no file paths, no `Ensuring:` clause.
- No per-step file path is generated (the generator works on roadmap text, not a live codebase).
- Acceptance Criteria remain unduplicated and authoritative; the block is additive/optional.
- The block reuses task-builder's `## Execution Context` sub-field names + no-file-path discipline; a no-semantic-collision check asserts no incompatible second meaning (`task-builder/SKILL.md:1066,1231`).

#### PR-2 — P2 Bounded Patch Loop → **RETAINED (recorded 2026-06-19): `retain-with-full-set-revalidation-and-guards`**

| Attribute | Value |
|-----------|-------|
| **Priority** | Active — the decision is recorded (2026-06-19) |
| **Maps to** | spec FR-RFMERGE.2; ledger P2 (`retain-with-full-set-revalidation-and-guards`) |
| **Decision space** | `defer` \| `retain-with-full-set-revalidation-and-guards` → **recorded: `retain-with-full-set-revalidation-and-guards`** |
| **Description** | After Stage 10, loop back to Stage 9 (delegate: `sc:task`, remapped from historical `sc:task-unified`) to re-patch unresolved work. |
| **User Value (retained)** | Convergence on unresolved patches without manual re-runs. |

**Acceptance Criteria:**

- The disposition is recorded as `retain-with-full-set-revalidation-and-guards` (chosen from `{defer, retain-with-full-set-revalidation-and-guards}`; recorded 2026-06-19, explicit human choice, **not a default**).
- Auto-defaulting P2 would have been a halt condition; the recorded value is an explicit human choice.
- Retained — implement with: **full-set** (not subset-only) re-validation, a monotonicity guard, regression detection, the **2-total-pass cap** (original pass + at most 1 re-patch pass) — the adversarially-adopted cap (`artifacts/adversarial-validation.md:141`; corroborated `FINAL-REPORT.md:236,334`); the pre-adversarial "3 total passes" is the rejected Variant-B value and is **historical-only**, not current — and **no overlap** with Stage 10.5 reflect remediation.
- **Propagation on decision**: the recorded P2 decision is propagated to **all four** carriers — `spec.md`, **`prd.md` (this doc — PR-2 AC, Q-P2, Approval row, MoSCoW)**, `tdd.md`, and `refresh-requirements-ledger.md` — so no document is left with a stale P2 field. (The P5 carrier set already includes `prd.md`; P2 is kept symmetric.)
- Downstream implementation-tasklist generation is **UNBLOCKED** (the P2 decision is recorded and the review checkpoint passed).

#### PR-3 — P3 DNSP (Detect-Nudge-Synthesize-Proceed) with guards → **Retain (adopted + refined)**

| Attribute | Value |
|-----------|-------|
| **Priority** | P0 (Must Have — the adversarial winner) |
| **Maps to** | spec FR-RFMERGE.3; ledger P3 (Retain, adopted + refined) |
| **Description** | On Stage-7 validation-agent retry failure, synthesize a conservative HIGH finding for the affected range and proceed rather than blocking Stage 8 on one agent. |
| **User Value** | Validation keeps moving past a single flaky agent while flagging the range for review. |
| **Edit target (later)** | Stage-7 validation-agent failure handling / orchestrator merge in `SKILL.md`. |
| **Ownership / reuse** | A `synthetic-dnsp` contract **already exists**, owned by `task-builder` (`task-builder/SKILL.md:873-911`: fixed `HIGH`+`source`, 2-element dedup key, found-count, all-agents-fail path, additive merge, N-1 concurrency). P3 in `sc:tasklist` **reuses** that contract (same fields/severity/dedup-key shape) — it is the narrower Stage-7 case, NOT a new divergent contract. Compatibility tests vs the existing contract are required. |

**Acceptance Criteria:**

- DNSP activates **only when ≥1 validation agent succeeded**; zero-success follows the all-agents-fail escalation path — surfacing it as a typed `StageError` is release intent / an implementation-time decision, NOT current behavior (no masking of total failure either way).
- Every synthesized finding carries `source: "synthetic-dnsp"` provenance metadata, conformant to the existing task-builder field contract (`HIGH` severity non-overridable; 2-element dedup key).
- Stage 8 is never blocked by a single failed-then-synthesized validation agent (given ≥1 success).
- P3 reuses the existing `task-builder` `synthetic-dnsp` contract (no divergent parallel contract); compatibility/regression tests vs `tests/skills/test_task_builder_merge.py` (and `tests/audit/test_dnsp_*` where present) are included.

#### PR-4 — P4 Evidence-Anchored Validation (quality-gate passthrough) → **Retain (lighter form)**

| Attribute | Value |
|-----------|-------|
| **Priority** | P1 (Should Have) |
| **Maps to** | spec FR-RFMERGE.4; ledger P4 (Retain as passthrough) |
| **Description** | Stage 6 emits `TASKLIST_ROOT/validation/gate-results.txt` from the existing quality gate; Stage 7 prompts inject it. |
| **User Value** | Validation agents see concrete gate evidence; no new artifact system or regex surface. |
| **Edit target (later)** | Stage 6 emission + Stage 7 prompt injection in `SKILL.md`. |

**Acceptance Criteria:**

- Stage 6 emits `gate-results.txt` from the existing quality gate (no new Stage 6.5).
- Stage 7 prompts include the gate-results passthrough content.
- **No** new `generation-evidence.json` artifact and **no** regex-extraction PABLOV pipeline are introduced.

#### PR-5 — P5 Feedback-Driven Tier Calibration → **RETAINED advisory-only (recorded 2026-06-19): `retain-advisory-only`**

| Attribute | Value |
|-----------|-------|
| **Priority** | Active — the decision is recorded (2026-06-19) |
| **Maps to** | spec FR-RFMERGE.5; ledger P5 (`retain-advisory-only`) |
| **Decision space** | `defer` \| `retain-advisory-only` → **recorded: `retain-advisory-only`** |
| **Description** | Retained advisory-only: render a `## Tier Calibration Advisory` section (min 2 matching overrides) with STRICT-downgrade warnings. |
| **User Value (retained)** | Visibility into feedback-suggested tier overrides — **as advice only**. |

**Acceptance Criteria:**

- The disposition is recorded as `retain-advisory-only` (chosen from `{defer, retain-advisory-only}`; recorded 2026-06-19, explicit human choice, **not a default**).
- Auto-defaulting P5 would have been a halt condition; the recorded value is an explicit human choice.
- Retained advisory-only — implement with: the advisory section **never alters scored tiers** — scored tiers stay a pure function of the roadmap, preserving "same roadmap → same **scored tiers**" determinism (the advisory output itself varies with `feedback-log.md` and is not roadmap-only; only the scored tiers are). **Hidden feedback must never mutate deterministic tier scores (the P5 constraint).**
- Downstream implementation-tasklist generation is **UNBLOCKED** (the P5 decision is recorded and the review checkpoint passed).

> **Deliberate departure from the historical recommendation (cited).** The controlling historical adversarial
> outcome recommended P5 as **REVISE → advisory-only** (`artifacts/adversarial-validation.md:227-249`;
> `FINAL-REPORT.md:240-246`) — i.e. retain the advisory directly. This refresh **intentionally supersedes**
> that direct-retain recommendation by routing P5 through an **explicit human decision**
> (`defer | retain-advisory-only`), **now recorded 2026-06-19 as `retain-advisory-only`**. This is a deliberate,
> recorded decision, not drift: the refresh treated the retain-vs-defer call as a product/risk judgment made by a
> human at the review checkpoint rather than inherited as an engineering default. The approach is **conservative** —
> it only added a `defer` option and a human gate; it does **not** weaken the historical guidance, and the human
> chose advisory-only (consistent with the historical recommendation). **Advisory-only remains the only permitted
> retain shape**: the recorded retain form is the determinism-preserving
> advisory-only contract above. Auto-mutation of scored tiers (the rejected Variant-B) stays a non-goal.

#### PR-6 — Accurate current Stage 10.5 / `--no-reflect` representation → **Retain (fidelity)**

| Attribute | Value |
|-----------|-------|
| **Priority** | P0 (Must Have — correctness invariant) |
| **Maps to** | spec FR-RFMERGE.6 |
| **Description** | All documents describe the 11-stage model; Stage 10.5 is audit-first/advisory (PASS/PARTIAL/FAIL all ship the bundle); `--remediate` offers remediation without auto-mutating phase files; `--no-reflect` skips Stage 10.5 entirely (also auto-set by `--dry-run`) and lives on the slash command only. |

**Acceptance Criteria:**

- Documents describe the **11-stage** model with Stage 10.5, never the stale 10-stage-only model.
- Stage 10.5 is described as advisory-for-shipping; the bundle ships on PASS/PARTIAL/FAIL.
- `--no-reflect` skips Stage 10.5 **and** the templated post-reflect task, is auto-set by `--dry-run`, and lives on the slash command only (NOT on `superclaude tasklist validate`).
- No retained proposal auto-mutates phase files.

#### PR-7 — Stale-token quarantine + source-of-truth discipline → **Retain (discipline)**

| Attribute | Value |
|-----------|-------|
| **Priority** | P0 (Must Have — correctness invariant) |
| **Maps to** | spec FR-RFMERGE.7 |
| **Description** | `/rf:*`, `.gfdoc`, `llm-workflows`, `/config/.claude`, `sc:task-unified`, and "10-stage-only" wording appear **only** as HISTORICAL-ONLY evidence, each paired with a current rebase target. MDTM execution is `/task <absolute-path>`, never `/sc:task`. Edits resolve under `src/superclaude/...`; `.claude/` is a generated mirror. |

**Acceptance Criteria:**

- No stale token appears as a current edit target or operative instruction; each historical mention names a current rebase target.
- `sc:task-unified` is replaced by `sc:task`; MDTM execution is `/task <path>`, not `/sc:task`. Reflect tests live at `tests/cli/reflect/`.
- Source edits target `src/superclaude/...`; `.claude/` mirrors are never staged (except `settings.json`).

### 14.2 Feature Prioritization (MoSCoW)

| Requirement | Priority | Gated? |
|-------------|----------|--------|
| PR-3 (P3 DNSP + guards) | Must | No |
| PR-6 (Stage 10.5 / `--no-reflect` fidelity) | Must | No |
| PR-7 (stale-token quarantine + SoT) | Must | No |
| PR-1 (P1 conservative context block) | Should | No |
| PR-4 (P4 quality-gate passthrough) | Should | No |
| PR-2 (P2 bounded patch loop) | **Must (recorded 2026-06-19: retain)** | No (decision recorded) |
| PR-5 (P5 advisory tier calibration) | **Must (recorded 2026-06-19: retain advisory-only)** | No (decision recorded) |

### 14.3 Architecture & Performance Requirements

| Requirement | Description | Rationale |
|-------------|-------------|-----------|
| Attach to existing pipeline | Retained proposals attach to existing 11-stage stages, not new pipeline phases (P1→Stage 4, P4→Stages 6/7, P3→Stage 7, P2→Stage 9 (retained), P5→Stage 4 advisory (retained)). | Minimal surface change; backward compatible. |
| Determinism | Same roadmap (+ same `--spec`) → same scored tiers (always). Byte-identical bundle ⇔ same `(roadmap, --spec, feedback-log.md)` tuple when P5 advisory is retained (the advisory varies with `feedback-log.md`). | Hard invariant; scored tiers stay roadmap-pure; the P5 advisory must never feed back into scored tiers. |
| No CLI surface change | No `tasklist generate` subcommand is added; generation stays the `/sc:tasklist` skill path. | Backward compatibility. |

### 14.4 Security / Integrity Requirements

| Requirement | Implementation | Standard |
|-------------|----------------|----------|
| Provenance of synthetic findings | `source: "synthetic-dnsp"` on every P3-synthesized finding | Auditability (NFR-RFMERGE.5) |
| No hidden-input mutation | Scored tiers a pure function of the roadmap; feedback advisory-only | Determinism (NFR-RFMERGE.1) |
| SoT integrity | Edits under `src/superclaude/...`; `make verify-sync` green; no `.claude/` mirror staged | SoT discipline (NFR-RFMERGE.3) |

---

## 19. Success Metrics & Measurement

> Single source of truth for this PRD's metrics (Section 5 forward-references here). Targets are framed for the **release intent**; runtime/test measurement applies once a later implementation step runs — not in this documents-only task.

### 19.1 Product / Quality Metrics

| Metric | Definition | Target | Measurement |
|--------|------------|--------|-------------|
| Determinism preserved | Same roadmap (+ same `--spec`) → same scored tiers (always; scored tiers a pure function of the roadmap). Byte-identical bundle ⇔ same `(roadmap, --spec, feedback-log.md)` tuple with P5 advisory retained. | 100% | Determinism test asserts identical scored tiers across runs (roadmap-only) and identical advisory across runs with the same `feedback-log.md`; P5 advisory (retained) renders without mutating scored tiers (NFR-RFMERGE.1). |
| Synthetic-finding auditability | % of P3-synthesized findings carrying `source: "synthetic-dnsp"` | 100% | P3 provenance test; grep of validation output (NFR-RFMERGE.5). |
| No reflect-gate overlap | Double-remediation of the same finding by P2 (retained) and Stage 10.5 | 0 | P2 loop provably disjoint from Stage 10.5 remediation; qualitative gate (NFR-RFMERGE.2). |

### 19.2 Process / Documents Metrics

| Metric | Definition | Target | Measurement |
|--------|------------|--------|-------------|
| Stale-token leakage | Stale tokens promoted to current operative instructions | 0 | Source-fidelity + stale-token gates; each historical mention paired with a current rebase target (PR-7). |
| Placeholder leakage | Remaining `SC_PLACEHOLDER` double-brace sentinels in this PRD | 0 | Structural gate sentinel self-check (NFR-RFMERGE.7). |
| Human-decision integrity | P2/P5 recorded as explicit human `retain-*` choices (2026-06-19), not defaults | 100% | Human-decision gate; auto-defaulting either would have been a halt condition. |
| Documents-only safety | Source-code edits and implementation tasklists produced by this task | 0 | Review checkpoint + git status; no `task-builder` implementation invocation (NFR-RFMERGE.6). |

### 19.3 Technical / Coverage Metrics

| Metric | Definition | Target | Alerting |
|--------|------------|--------|----------|
| `--no-reflect` / Stage 10.5 coverage | Direct test assertions for the currently-untested generation contracts | Added in refreshed test plan | Required suites must include them when implemented. |
| Sprint-parser compatibility | Any downstream tasklist uses literal `phase-N-tasklist.md` + `### T<PP>.<TT>` headings + Execution Mode ∈ {claude, python, skip} | 100% | CODE-VERIFIED vs `src/superclaude/cli/sprint/config.py:15-32,34-55,73-124,134-146` (NFR-RFMERGE.4). |

---

## 20. Risk Analysis

### 20.1 Product / Correctness Risks

| Risk | Probability | Impact | Mitigation | Contingency |
|------|-------------|--------|------------|-------------|
| P5 hidden-feedback determinism violation (historical K2) | Med | High | P5 recorded `retain-advisory-only` (2026-06-19); advisory-only — scored tiers never mutated. | Determinism test gate; revert P5 to `defer`. |
| P2 patch-loop oscillation/regression (historical K4) | Med | High | P2 recorded `retain-with-full-set-revalidation-and-guards` (2026-06-19); full-set re-validation + monotonicity guard + regression detection + 1-extra-pass cap (2 total; `artifacts/adversarial-validation.md:141`) + non-overlap with Stage 10.5. | 1-extra-pass cap (2 total); revert P2 to `defer`. |
| P2/P5 auto-defaulted by a downstream synthesis pass | Low | High | Auto-defaulting either is an explicit halt condition; review checkpoint records both first. | Halt + record blocker in Open Questions. |
| P3 DNSP masks a total validation failure | Low | High | All-agents-fail guard: DNSP activates only when ≥1 agent succeeded; zero-success follows the all-agents-fail escalation path (release intent: `StageError`; no typed `StageError` in current source). | Fall back to the all-agents-fail escalation path (release intent: `StageError`). |

### 20.2 Process / Integrity Risks

| Risk | Probability | Impact | Mitigation | Contingency |
|------|-------------|--------|------------|-------------|
| Stale token re-promoted as operative instruction | Med | High | Source-fidelity + stale-token gates; each historical mention paired with a current rebase target; `sc:task-unified` → `sc:task`. | Halt; correct the citation. |
| Implementation tasklist generated inside this documents-only task | Low | High | Authorization boundary: no `task-builder` implementation invocation; downstream handoff is a separate, later, non-blocking step. | Review checkpoint + git status catch it. |
| Edits target `.claude/` mirrors instead of `src/superclaude/...` | Low | High | SoT discipline; `make verify-sync`; never stage `.claude/{skills,commands,agents,hooks,templates}`. | Move change to `src/`, re-sync. |

### 20.3 Operational / Coverage Risks

| Risk | Probability | Impact | Mitigation | Contingency |
|------|-------------|--------|------------|-------------|
| Reflect-guard test command pins a non-existent path (`tests/reflect/`) | Med | Med | Standardize on disk-verified `tests/cli/reflect/`; OQ-1 ✅ Resolved (fixed at source 2026-06-19). | Resolved: `BUILD-REQUEST.md:15` / `research/07:137` now use `tests/cli/reflect/`. |
| `--no-reflect` / Stage 10.5 generation contracts remain untested | High | Med | Refreshed test plan adds direct assertions (carried gap). | Block coverage sign-off until added. |
| Mirror-lag in `rules/file-emission-rules.md` propagated as runtime truth | Low | Med | Respect mirror-lag; the inline `SKILL.md` copy is authoritative; never hand-edit the mirror. | Regenerate mirrors via `make sync-dev`. |

---

## 21. Implementation Plan (Release Intent)

> **CRITICAL:** **No implementation work is performed in this task**, and **no implementation tasklist is generated here.** The plan below is the **release intent only**. The P2 and P5 human decisions are now RECORDED (2026-06-19: P2 = `retain-with-full-set-revalidation-and-guards`, P5 = `retain-advisory-only`), so the corresponding implementation steps are unblocked; the plan now depends only on the document-review checkpoint sign-off. Downstream `/task-builder` invocation is a **later, separate handoff**, not work done now.

### 21.1 Sequencing (release intent — gated by review sign-off; P2/P5 decisions recorded)

| Step | Work (later, separate step) | Depends on | Gated by |
|------|------------------------------|------------|----------|
| 1 | Refresh docs (this PRD + spec + TDD) + record P2/P5 decisions at the review checkpoint | — | This release |
| 2 | PR-4 quality-gate passthrough (`gate-results.txt` → Stage 7) — lowest risk, reuses existing gate | Step 1 (review sign-off) | Review checkpoint |
| 2 (parallel) | PR-1 conservative `## Execution Context` block — template-only, additive | Step 1 | Review checkpoint |
| 3 | PR-3 DNSP + all-agents-fail guard + `synthetic-dnsp` provenance (Stage 7 / orchestrator merge) | Step 1 | Review checkpoint |
| 4 | **P2 == retain (recorded 2026-06-19)** — bounded patch loop (full-set re-validation + guards; no Stage 10.5 overlap) | Steps 1, 3; P2 decision recorded | Review checkpoint |
| 4 | **P5 == retain-advisory-only (recorded 2026-06-19)** — `## Tier Calibration Advisory` (determinism-preserving) | Step 1; P5 decision recorded | Review checkpoint |
| 5 | Tests for all retained features + carried gaps (close `--no-reflect`/Stage 10.5 gap) | Steps 2, 3, (4) | Review checkpoint |

### 21.2 Downstream Handoff (later, non-blocking)

The P2 and P5 decisions are recorded (2026-06-19); after the review checkpoint sign-off:

1. A separate step invokes `/task-builder` from the refreshed `spec.md` + `prd.md` + `tdd.md` to author an MDTM tasklist. **This is not performed in the current task.**
2. The resulting MDTM tasklist is executed with `/task <absolute-path>` (**not** `/sc:task`).
3. Any stale `sc:tasklist`-generated RFMerger tasklists from the historical package are ignored.
4. P2/P5 implementation tasks are included: both human decisions recorded a `retain-*` choice (2026-06-19: P2 retain-with-full-set-revalidation-and-guards, P5 retain-advisory-only).

### 21.3 Definition of Done (release intent — not asserted now)

A retained proposal is "Done" (in a **later** implementation step) when its acceptance criteria are met, the relevant tests pass under UV, source edits live under `src/superclaude/...`, `make verify-sync` is green, and no `.claude/` mirror was staged. **None of these are asserted complete by this PRD.**

---

## 25. API & Contracts Impacts

> No CLI surface is added or changed by this refresh. The current surface is documented so no retained proposal silently alters it. The slash command is a wrapper that mandatorily invokes `Skill sc:tasklist-protocol`; the generator does not run from the command file alone.

### 25.1 Current CLI / Command Surface (unchanged)

```
/sc:tasklist <roadmap-path> [--spec <spec-path>] [--output <output-dir>] [--no-reflect]
superclaude tasklist validate <output_dir> [--roadmap-file ...] [--tasklist-dir ...] [--model ...]
                                           [--max-turns ...] [--debug] [--tdd-file ...] [--prd-file ...]
```

| Option | Surface | Default | Description |
|--------|---------|---------|-------------|
| `--spec` | slash | none | Optional supplementary spec/context; must resolve to a readable file when provided; threaded into the Stage 10.5 PRE reflect. Slash command only. |
| `--output` | slash | derived `TASKLIST_ROOT` | Output directory for the bundle. |
| `--no-reflect` | slash | off | Skips Stage 10.5 (pre-reflect sign-off) and the templated post-reflect task; auto-set by `--dry-run`. **Slash command only — NOT on `superclaude tasklist validate`.** |
| `--tdd-file` | validate | autowired from `.roadmap-state.json` | Supplementary TDD validation input (missing → MEDIUM). |
| `--prd-file` | validate | autowired from `.roadmap-state.json` | Supplementary PRD validation input (missing → MEDIUM; priority contradiction → LOW). |
| `--model` | validate | `""` (empty) | Overrides the validation step model; subprocess uses `step.model or config.model`. |

> `superclaude tasklist validate` is **validation-only**: ROADMAP → TASKLIST fidelity (not spec→tasklist or roadmap→spec), exits 1 on HIGH-severity deviations, and does **not** own `--no-reflect`. There is **no** `tasklist generate` CLI subcommand; inference-based generation is the `/sc:tasklist` skill path.
>
> **Surface split (do not conflate) + open risk.** `--spec` is a **slash-generator** supplementary input (resolution order: explicit `--spec` → autowired TDD/PRD from `.roadmap-state.json` → roadmap; `SKILL.md:1466-1471`); `--tdd-file`/`--prd-file` are **validate-CLI** inputs autowired from `.roadmap-state.json`. They are distinct surfaces and must not be merged into one "autowire" claim. The `sc:tasklist` skill body is itself inconsistent — "exactly one input: the roadmap text" (`SKILL.md:49-57`) vs `--spec` enrichment/autowire (`SKILL.md:169-182,1466-1471`); this refresh carries that contradiction as an **open risk** for upstream-source reconciliation rather than treating autowire as settled (see spec §5.1 / §11).

### 25.2 Runtime-Artifact / Data-Shape Impacts (release intent)

| Contract | Impact | Notes |
|----------|--------|-------|
| `TASKLIST_ROOT/validation/gate-results.txt` (P4) | New plain-text runtime artifact emitted by Stage 6, injected into Stage 7 prompts. | Explicitly **not** `generation-evidence.json`, **not** a new Stage 6.5. |
| P3 synthesized finding | REUSES the existing `task-builder`-owned `synthetic-dnsp` / DM-003 contract (`task-builder/SKILL.md:873-911`): fixed `HIGH`+`source`, canonical `affected_range`, `evidence`, fixed `recommendation`, 2-element `dedup_key`, `found_n_times`. | Not a new model; the canonical contract is owned by `task-builder`, not redefined in current Stage-7 code. Synthesize only when ≥1 agent succeeded, else the all-agents-fail escalation path (release intent: `StageError`). |
| Stage 10.5 invariant | Unchanged — advisory-for-shipping (PASS/PARTIAL/FAIL all ship); `--remediate` never auto-mutates phase files; `--no-reflect` skips it. | No retained proposal may auto-mutate phase files. |
| P5 advisory (retained) | `## Tier Calibration Advisory` section rendered; **scored tiers never mutated**. | Determinism preserved — advisory-only; scored tiers remain roadmap-only; the advisory may read `feedback-log.md` and must never feed back into scored tiers. |

### 25.3 Backward Compatibility

Full. Bundles remain N+1 files with Sprint-compatible filenames/headings; determinism is preserved; Stage 10.5 still ships on PASS/PARTIAL/FAIL. P1 adds an optional additive block; P3/P4 are internal to validation; P2/P5 are now recorded (retain) and are active implementation requirements.

---

## 28. Maintenance & Living-Document Status

### 28.1 Living-Document Status

> **This PRD is a living document and a reviewed-planning draft — it does NOT claim implementation readiness.**

- **Current status**: 🟡 Draft (reviewed-planning). Not implementation-ready.
- **Blocking gates before implementation**: (1) human review sign-off of `spec.md` / `prd.md` / `tdd.md`. The P2 and P5 human decisions are RECORDED (2026-06-19: P2 = `retain-with-full-set-revalidation-and-guards`, P5 = `retain-advisory-only`) and no longer gate implementation.
- **What unblocks downstream work**: The P2 and P5 decisions are recorded; once the review checkpoint records sign-off, a separate `/task-builder` handoff may author an implementation tasklist; that tasklist executes via `/task <absolute-path>`.
- **Determinism guarantee held open**: Hidden feedback must never mutate deterministic tier scores (the P5 constraint); any P5 retention is advisory-only.
- **Edit discipline**: Future code edits target `src/superclaude/...` then `make sync-dev` + `make verify-sync`; `.claude/` mirrors are never edit/stage targets (except `.claude/settings.json`).

### 28.2 Ownership

| Role | Responsibility |
|------|----------------|
| **Primary Owner** | RFMerger refresh owners — document accuracy and P2/P5 decision capture |
| **Technical Owner** | `sc:tasklist` maintainers — attachment-point accuracy |
| **Reflect Owner** | Reflect-gate maintainers — Stage 10.5 non-overlap (P2) |

### 28.3 Update Process

1. Propose changes by commenting on specific sections.
2. Review with `sc:tasklist` / reflect / QA leads at the document-review checkpoint.
3. Record the P2 and P5 decisions in this PRD's Approval and Open Questions tables.
4. Increment version and update Document History.
5. Only then hand off to a separate `/task-builder` step.

---

## Appendix A: Glossary

| Term | Definition |
|------|------------|
| RFMerger | RigorFlow-Merger — the April-2026 investigation proposing selected RF execution-time mechanisms be borrowed into `sc:tasklist`. |
| Canonical RFMerger P1-P5 | P1 Context-Armed Steps, P2 Bounded Patch Loop, P3 DNSP, P4 Evidence-Anchored Validation, P5 Feedback-Driven Tier Calibration (per `design-rfmerger-proposals.md`). **This is the taxonomy used throughout this PRD.** |
| DNSP | Detect-Nudge-Synthesize-Proceed (P3). Canonical name; the gloss "Dynamic / synthetic no-source provenance" refers to the same entry. |
| **Reflect UC-2 "P1-P5" (QUARANTINED — DO NOT CONFUSE)** | The `sc:reflect` UC-2 protocol independently uses P1-P5 for a *different* taxonomy (per-task verdicts, cross-task scan, report rendering, budget routing). They share only the `P<n>` label with RFMerger P1-P5 — **no semantic correspondence**. Keep strictly separate; never reuse reflect's `P<n>` labels for RFMerger proposals. |
| Stage 10.5 (Pre-Reflect Sign-off) | 11th tracked stage of `sc:tasklist`; fans out `/sc:reflect --mode pre --remediate` per phase; **advisory for shipping** (PASS/PARTIAL/FAIL all ship); `--remediate` offers remediation without auto-mutating phase files; skipped under `--no-reflect`. |
| `--no-reflect` | Slash-command flag that skips Stage 10.5 (and the templated post-reflect task); auto-set by `--dry-run`; not present on `superclaude tasklist validate`. |
| `sc:task` | Current Stage-9 patch-execution delegate and tier-classification algorithm (`STRICT > EXEMPT > LIGHT > STANDARD`). Replaces the historical `sc:task-unified`. |
| `/task` | The MDTM execution skill loop. MDTM tasklists are executed via `/task <absolute-path>` — **not** `/sc:task`. |
| HISTORICAL-ONLY | A token/claim existing only in the historical RFMerger package; never promoted to current operative guidance; cited as evidence with a current rebase target. |
| Source-of-truth (SoT) | `src/superclaude/...` is canonical; `.claude/{skills,commands,agents,hooks,templates}` is a generated mirror (`make sync-dev` + `make verify-sync`), never an edit/stage target (except `.claude/settings.json`). |
| `gate-results.txt` | P4 runtime artifact: plain-text quality-gate evidence emitted by Stage 6, injected into Stage 7 prompts. Explicitly **not** `generation-evidence.json` and **not** a new Stage 6.5. |
| `source: "synthetic-dnsp"` | Mandatory provenance marker on every P3-synthesized validation finding. |

## Appendix B: Stale-Token Quarantine (HISTORICAL-ONLY → current)

| Stale token / wording (HISTORICAL-ONLY) | Current operative equivalent (do not edit the stale form) |
|---|---|
| `/rf:*` (`/rf:taskbuilder`, `/rf:pipeline`, `/rf:run`) + TeamCreate/SendMessage agent-team flow | `/task-builder` (Agent tool; no agent teams) for authoring, then `/task <absolute-path>` for MDTM execution. |
| `.gfdoc` (e.g. `.gfdoc/scripts/automated_qa_workflow.sh`, `.gfdoc/templates/...`) | Source of truth is `src/superclaude/templates/workflow/...`; execution is the `/task` skill loop, not a shell script. (`.claude/templates/workflow/...` is a generated mirror, not an edit target.) |
| `llm-workflows` (`/config/workspace/llm-workflows/`) | In-repo `src/superclaude/...`. |
| `/config/.claude` (global-config SC source) | In-repo `src/superclaude/...`; never edit `/config/.claude`. |
| `sc:task-unified` (historical Stage-9 patch delegate) | `sc:task` (current Stage-9 patch-execution delegate). |
| "10-stage-only" tasklist wording | **11-stage** model with Stage 10.5 advisory reflect gate + `--no-reflect` + PRD/TDD autowire. |

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-18 | claude (TASK-RF-rfmerger-refresh-20260618-172224, Step 2.4) | Initial refreshed PRD — reviewed-planning draft; P1/P3/P4 retained (conservative/guarded forms), P2/P5 recorded PENDING with no default; rebased onto current 11-stage / Stage-10.5 / `sc:task` / `src/superclaude/...` surface; stale tokens quarantined HISTORICAL-ONLY. Not implementation-ready. |
| 1.1 | 2026-06-19 | claude (decision propagation) | Propagated the two now-RECORDED human decisions: P2 = `retain-with-full-set-revalidation-and-guards`, P5 = `retain-advisory-only` (explicit human choices, not defaults). Decision-status wording updated from PENDING to RECORDED; downstream implementation-tasklist generation now UNBLOCKED. Guard design, P2 2-total-pass cap, P5 determinism semantics, and historical/adversarial evidence unchanged. |

---

> **Template:** `src/superclaude/templates/workflow/05_prd_template.md` (Product PRD v1.0), adapted to feature/component tier for an internal developer-tooling refactor.
