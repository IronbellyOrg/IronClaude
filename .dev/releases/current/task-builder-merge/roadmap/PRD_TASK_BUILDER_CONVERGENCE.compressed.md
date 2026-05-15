---
id: "TASK-BUILDER-CONVERGENCE-PRD-CORE"
title: "Task-Builder Convergence (v3.9) - Product Requirements Document (PRD)"
description: "Inverse-direction merge of /sc:tasklist qualities into the task-builder skill, importing five generation-time rigor mechanisms (structural gate additions, execution-context header, gate-results passthrough, adversarial category naming, retry monotonicity guards) plus one paradigm-neutral execution-resilience finding (DNSP synthetic finding) — six additive landings governed by the G6 four-case conflict rule and the five task-builder invariants."
version: "1.0"
status: "🟡 Draft"
type: "📋 Product Requirements"
priority: "🔥 Highest"
created_date: "2026-05-14"
updated_date: "2026-05-14"
assigned_to: "task-builder-convergence-team"
autogen: false
autogen_method: "Phase 8 of /sc:adversarial Mode A orchestration; Source: direct-synthesis (prd skill returned protocol text)"
coordinator: "orchestrator-pipeline"
parent_task: "v3.8-RigorFlowMerger"
depends_on:
- ".dev/releases/current/task-builder-merge/release-spec.md"
- ".dev/releases/current/task-builder-merge/conflict-register.md"
- ".dev/releases/current/task-builder-merge/adversarial/merge-log.md"
- ".dev/releases/current/task-builder-merge/adversarial/refactor-plan.md"
- ".dev/releases/current/task-builder-merge/reflection/reflect-task.md"
- ".dev/releases/current/task-builder-merge/reflection/gate-report.md"
- ".dev/releases/backlog/v3.8-RigorFlowMerger-tasklist/FINAL-REPORT.md"
related_docs:
- "src/superclaude/skills/task-builder/SKILL.md"
- "src/superclaude/skills/sc-tasklist-protocol/SKILL.md"
- "src/superclaude/agents/rf-qa.md"
- "src/superclaude/agents/rf-qa-qualitative.md"
- "src/superclaude/agents/rf-analyst.md"
- "src/superclaude/agents/rf-task-builder.md"
tags:
- prd
- requirements
- task-builder
- sc-tasklist
- convergence
- v3.9
- adversarial-merge
- invariant-preservation
- four-case-conflict-rule
- additive-only
template_schema_doc: "src/superclaude/examples/prd_template.md"
estimation: "6 additive edit-batches across 5 files; per-FR rollback granularity"
sprint: "v3.9"
due_date: "2026-Q3"
start_date: "2026-05-14"
completion_date: ""
blocker_reason: ""
ai_model: "claude-opus-4-7"
model_settings: ""
review_info:
  last_reviewed_by: "phase-8-orchestrator"
  last_review_date: "2026-05-14"
  next_review_date: "2026-06-14"
task_type: "static"
---

# Task-Builder Convergence (v3.9) - Product Requirements Document (PRD)

> **Source:** direct-synthesis (prd skill returned protocol text)
> **WHAT:** Inverse-direction merge of `/sc:tasklist`'s generation-time rigor qualities into the `task-builder` skill, comprising six additive landings (PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03) plus one Phase-2 deferral (PR-05).
> **WHY:** Engineering planning decision document for the v3.9 merger work; the G6 four-case conflict rule is authoritative wherever `/sc:tasklist` and `task-builder` behaviors disagree.
> **HOW TO USE:** Engineering, QA, and orchestration teams reference this PRD throughout v3.9 implementation, gate validation, and post-merge audit cycles.

### Document Lifecycle Position

|Phase|Document|Ownership|Status|
|-------|----------|-----------|--------|
|**Requirements**|**This PRD**|**Engineering Planning**|**Draft**|
|Design|TDD (to be authored from this PRD)|Engineering|Not started|
|Implementation|Tech Reference (post-merge)|Engineering|Not started|

### Tiered Usage

|Tier|When to Use|Sections to Skip|
|------|-------------|------------------|
|**Lightweight**|Quick reviewer scan|§5, §8, §9, §17, §18, §22 (platform-level — N/A for this feature PRD)|
|**Standard**|Engineering planning, gate audits, FR-level reference|None — complete all sections|
|**Heavyweight**|Cross-team review including downstream PRD/TDD/Tech Reference handoff|None — complete all sections plus appendices|


## Document Information

|Field|Value|
|-------|-------|
|**Product Name**|Task-Builder Convergence (Inverse-Direction `/sc:tasklist` Merge)|
|**Product Type**|Feature/Component PRD (inside the SuperClaude framework)|
|**Product Owner**|SuperClaude Engineering Planning|
|**Engineering Lead**|task-builder maintainer|
|**Design Lead**|N/A — additive engineering merge, no UX surface|
|**Maintained By**|Orchestrator pipeline (Phase 8 owner) until Phase 9 PR merges close|
|**Stakeholders**|rf-task-builder, rf-qa, rf-qa-qualitative, rf-analyst agent maintainers; orchestrator pipeline; v3.9 release manager|
|**Status**|Draft — awaiting TDD authorship|
|**Target Release**|v3.9|
|**Last Verified**|2026-05-14 against release-spec.md v1.0.0 (`status: draft`, `complexity_score: 0.7`, all 5 Phase 5.2 gates PASS)|

### Document Approval

|Role|Name|Signature|Date|
|------|------|-----------|------|
|Engineering Lead|task-builder maintainer|__________|TBD|
|QA Lead|rf-qa / rf-qa-qualitative maintainer|__________|TBD|
|Orchestrator|Phase 8 pipeline owner|__________|TBD|


## Completeness Status

**Completeness Checklist:**
- [x] Section 1: Executive Summary — Populated from release-spec.md §1 + §2
- [x] Sections 2-5: Problem, Background, Vision, Business Context — Populated; §5 N/A per feature-PRD scope
- [x] Sections 6-9: JTBD, Personas, Value Proposition, Competitive Analysis — Personas + JTBD populated; §8/§9 N/A per feature-PRD scope
- [x] Sections 10-13: Assumptions, Dependencies, Scope, Open Questions — Populated from release-spec.md §1.2/§9/§11
- [x] Sections 14-15: Technical Requirements, Technology Stack — Populated from release-spec.md §3/§4/§6
- [x] Sections 16-18: UX, Legal/Compliance, Business Requirements — §16 minimal (no UX surface); §17/§18 N/A per feature-PRD scope
- [x] Sections 19-20: Success Metrics, Risk Analysis — Populated from release-spec.md §6/§7/§8
- [x] Section 21: Implementation Plan (Epics/Stories, Product Reqs, Phasing, DoD, Timeline) — Populated from release-spec.md §3/§4.6/§9
- [x] Sections 22-25: Customer Journey, Error Handling, Design, API Contracts — §22/§24/§25 N/A per feature-PRD scope; §23 populated
- [x] Sections 26-28: Contributors, Related Resources, Maintenance & Ownership — Populated
- [x] All links verified — release-spec.md citations resolve
- [ ] Reviewed by engineering — pending

**Contract Table:**

|Element|Details|
|---------|---------|
|**Dependencies**|release-spec.md v1.0.0, conflict-register.md, merge-log.md, refactor-plan.md, reflect-task.md, gate-report.md (all PASS)|
|**Upstream**|Phases 1-7 of the orchestration pipeline; FINAL-REPORT.md §6.3 asymmetric finding|
|**Downstream**|Feeds to: TDD authorship (Phase 9?), Tech Reference (post-merge), implementation tickets aligned to FR-CONV.1..6|
|**Change Impact**|Notify: rf-* agent maintainers, task-builder maintainers, v3.9 release manager|
|**Review Cadence**|Per fix-cycle audit (K-003 mitigation); quarterly otherwise|
|**Living Document**|This PRD is frozen at v1.0 until v3.9 ships; post-merge audit findings (K-003, OPEN-PR05, OPEN-TOKEN) update v1.1|


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


## 1. Executive Summary

Task-Builder Convergence (v3.9) imports five `/sc:tasklist` generation-time rigor mechanisms plus one paradigm-neutral execution-resilience mechanism into the `task-builder` skill — the inverse direction of the v3.8 RigorFlow Merger work. FINAL-REPORT §6.3 surfaced that four of five v3.8 RF→SC proposals were over-engineered because RF mechanisms designed for **execution context** (long-running, stateful, non-deterministic agents) imported their *implementations* rather than their *intent* into SC's **generation context** (single-pass, stateless, determinism-first). This release runs the reverse port: from `/sc:tasklist`'s generation context into `task-builder`'s execution context, adapting *intent* not *implementation*, governed by the G6 four-case conflict rule wherever the two skills' behaviors disagree.

The release consists of six per-proposal landings — PR-06 (Structural Gate Additions), PR-01 (Execution Context Header, revise-then-adopt), PR-04 (Gate Results Passthrough), PR-07 (Adversarial Category Naming), PR-02 (Retry Monotonicity Guards), and PR-03 (DNSP Synthetic Finding, the base proposal at combined 0.959) — plus one Phase-2 deferral (PR-05 Tier-History Advisory). Every landing is strictly additive (A-002 zero-trust governance); no existing rf-qa check, rf-qa-qualitative checklist item, gate stage, output field, or `.dev/tasks/` layout entry is removed or renamed. All five load-bearing task-builder invariants — **self-contained-item**, **evidence-bound-item**, **persistent-`.dev/tasks/`-artifact**, **zero-trust QA**, **parallel-research** — are preserved or strengthened, with MEDIUM invariant-probe findings (INV-002, INV-010, INV-012, INV-015, INV-019) routed through explicit per-FR acceptance criteria.

**Key Success Metrics:**
- All 6 FR Acceptance Criteria (Observable / Verification / Negative) PASS on synthetic fixtures: 100%
- All 5 task-builder invariants preserved (verified by NFR-CONV.6..10): 100%
- Token-cost increase over pre-merge baseline (NFR-CONV.4): ≤10%
- Hidden-input determinism guard (NFR-CONV.3): byte-identical structural output with empty vs fixture-populated `.dev/tasks/done/`
- `make verify-sync` PASS after all six landings (cross-cutting A-001 acceptance)


## 2. Problem Statement

<!-- SCOPE NOTE: Feature/component PRD — no Market Opportunity (TAM/SAM/SOM). Replaced with "Why This Feature is Required". -->

### 2.1 The Core Problem

**`task-builder` lacks three classes of cross-cutting structural and task-level reinforcement that `/sc:tasklist` already documents.**

Three specific gaps motivate this release (release-spec.md §1):

- **Gap A — No task-level executor-readability summary.** `task-builder` has a per-item self-contained 5-field schema (SKILL.md:1452-1457) but no task-LEVEL header that gives a downstream executor agent the "what this whole task is about" view distinct from per-item Context fields.
- **Gap B — No structural gate checks for known failure modes.** Generated MDTM files can contain placeholder/title-only items, circular dependencies, granularity outliers, and confidence-format inconsistencies — none of which today's 9-item A.10 task-integrity checklist catches, and none of which `/sc:tasklist`'s 17-point gate misses.
- **Gap C — Implicit inherited-verdict passthrough.** Between rf-qa (machine-verifiable structural verdict) and rf-qa-qualitative (semantic adversarial review), the inherited verdict is implicit; rf-qa-qualitative re-runs structural checks mechanically and risks rubber-stamping rather than focusing on semantic quality.

Without addressing these gaps, the five load-bearing task-builder invariants (**self-contained-item**, **evidence-bound-item**, **persistent-`.dev/tasks/`-artifact**, **zero-trust QA**, **parallel-research**) are operationally enforced per-item but lack cross-cutting reinforcement. Empirical evidence: FINAL-REPORT §6.2 F2 observed 21 retry files across 18 batches — a clear oscillation pattern justifying retry monotonicity guards.

### 2.2 Why Existing Solutions Fall Short

**Existing task-builder mechanisms** (pre-merge):
- Per-item 5-field schema enforces self-containment item-by-item but provides no task-level summary.
- 9-item A.10 task-integrity checklist covers basics (schema completeness, evidence binding) but lacks placeholder scans, DAG checks, count bounds, granularity, format consistency.
- rf-qa-qualitative has generic adversarial stance but no named 5-axis taxonomy; structural overlap with rf-qa is left to the executing agent's judgment.

**A bulk import of `/sc:tasklist` mechanisms** (REJECTED — per CB-3):
- Bundle-specific checks (phase-file naming, index references) do not apply to a single-MDTM output target.
- A blanket "no specific file paths" rule (X-001) would break the **evidence-bound-item** invariant by stripping per-item `file:line` citations.
- Full-verdict-reliance (X-002) would break the anti-inflation rule at rf-qa-qualitative.md:766-775.
- Hidden-input determinism risk (FINAL-REPORT §6.2 F4): PR-05's "tier modification based on history" would re-introduce the over-engineering pattern in reverse.

**Continuing v3.8 RF→SC direction only** (REJECTED):
- FINAL-REPORT §6.3 documented the asymmetry one-way only. Portfolio-wide adversarial debate identified 5 ADOPT-grade qualities in the inverse direction not yet imported.

### 2.3 Why This Feature is Required

This feature is critical to the SuperClaude framework because `task-builder` is the entry point for every MDTM-driven workflow in the system. Strengthening its generation-time rigor compounds across every downstream sprint, roadmap, and tasklist execution. The cost of not solving it: continued silent acceptance of placeholder items, undetected DAG cycles, and rubber-stamped rf-qa-qualitative passes — all of which surface as expensive rework in later phases. Reference the Platform PRD (SuperClaude framework PRD) for platform-level market context; this feature PRD scopes to the merger work itself.


## 3. Background & Strategic Fit

<!-- SCOPE NOTE: Feature PRD — focus on why THIS FEATURE is needed now; reference Platform PRD for platform-level strategic context. -->

### 3.1 Why Now?

1. **v3.8 RigorFlow Merger has shipped** — establishes the bidirectional-merger pattern and the FINAL-REPORT §6.3 asymmetric finding that motivates this release.
2. **Portfolio convergence reached 0.88 in Round 2 + invariant probe** — above the 0.80 threshold; HIGH-UNADDRESSED = 0; all 5 MEDIUM invariant concerns routed through per-FR Acceptance Criteria.
3. **Phase 5.2 G1-G5 citation/invariant gate verdict = PASS on all five gates** — Phase 6 cleared to proceed; no degradation required.
4. **Empirical oscillation pattern documented (21 retry files / 18 batches)** — justifies the retry monotonicity guards in PR-02 with concrete data, not speculation.

### 3.2 How This Fits Framework Objectives

- **Mission Alignment**: SuperClaude's mission is rigor-first agent orchestration; this release closes structural-rigor gaps in the generation step.
- **Quality Goal**: Zero placeholder items, zero DAG cycles, zero rubber-stamped qualitative passes in v3.9 outputs.
- **Architectural Position**: Reinforces the 4-stage gate topology (research / task-integrity / qualitative / end-to-end) without adding stages.
- **Maintainability Moat**: G6 four-case conflict rule + invariant-protection ledger (conflict-register.md) prevents future mergers from silently weakening load-bearing behavior.

### 3.3 Strategic Bets

1. **Bet 1 — Intent-port over implementation-port**: Adapting *intent* not *implementation* (FINAL-REPORT §6.3) is the right pattern for cross-paradigm merges and will compound across future SC↔RF work.
2. **Bet 2 — Additive-only governance (A-002)**: Strictly additive landings keep blast radius low; per-FR rollback granularity preserves operability under failure.
3. **Bet 3 — Hidden-input vigilance scales**: Treating PR-05's tier-history advisory as a Phase-2 deferral validates that hidden-input determinism risk is taken seriously regardless of merger direction.
4. **Bet 4 — Per-check classification (CB-3) over bulk-port**: Importing 8 unique TB-Add checks (not all 17 `/sc:tasklist` checks) demonstrates that fine-grained selection beats bundle-import.


## 4. Product Vision

**"Every MDTM task generated by task-builder is structurally complete, evidence-bound, deterministic at the gate, and self-contained at the item — with cross-cutting reinforcement borrowed from `/sc:tasklist` but adapted to task-builder's execution-context paradigm."**

When this release succeeds, every generated MDTM task carries a task-level Execution Context header, every item's Context field has either a `file:line` citation or a justified-absence comment, every rf-qa gate run emits a structural verdict that rf-qa-qualitative inherits and audits semantically (not mechanically), every retry loop halts on regression-or-non-shrink, and every partition agent's exhaust point yields a HIGH-severity synthetic finding rather than a silent abort. The five task-builder invariants remain load-bearing, and the G6 four-case conflict rule remains the authoritative tiebreaker for all future merges.


## 5. Business Context

<!-- SCOPE NOTE: Feature PRD — TAM/SAM/SOM, revenue projections, KPI tables N/A. Replaced with feature-business rationale + forward reference to §19. -->

This feature is part of the SuperClaude framework's internal tooling and does not carry independent revenue or pricing. Its business value lies in **reduced rework cost** at downstream phases (sprint execution, roadmap validation) when generated MDTM tasks pass structural rigor at the source. See §19 for the success metrics that quantify this value; see the Platform PRD for SuperClaude framework-level business context.

**Cost Drivers Specific to This Feature**:
- LLM token consumption increase (target ≤10% per NFR-CONV.4) for the additional gate checks, Execution Context header generation, and Inherited Structural Verdict block.
- No new external dependencies, no new network calls (NFR-CONV.5), no storage cost increase.


## 6. Jobs To Be Done (JTBD)

> **Format:** "When [situation], I want to [motivation], so I can [expected outcome]."

### 6.1 Primary Jobs

**Job 1: Detect structural defects at generation time**
- **When**: I am the rf-qa agent gating a newly generated MDTM task file.
- **I want to**: Catch placeholder-title items, circular dependencies, granularity outliers, and confidence-format inconsistencies before downstream agents waste cycles on a defective task.
- **So I can**: Surface defects with item-ID-naming error messages at A.10 — not at sprint-execution time.
- **Current alternatives**: A 9-item task-integrity checklist that lacks placeholder scans, DAG checks, granularity, count bounds, and format consistency.
- **Pain with alternatives**: Defects pass through silently and surface as fix-cycle thrash or sprint-execution failures.

**Job 2: Pass machine-verifiable verdict between rf-qa and rf-qa-qualitative**
- **When**: I am the rf-qa-qualitative agent reviewing items that have already been structurally gated.
- **I want to**: Receive rf-qa's PASS/FAIL verdict as an inherited block in my spawn prompt and focus my attention on semantic quality, not mechanical re-checking.
- **So I can**: Apply 5 named adversarial axes (drift / contradictions / omissions / weakened-criteria / invented-content) to the items not covered by inherited PASS — without re-doing the structural work.
- **Current alternatives**: Implicit verdict — rf-qa-qualitative re-runs structural checks mechanically or rubber-stamps with no Self-Audit trail.
- **Pain with alternatives**: Inflation risk, anti-inflation rule violation, expensive re-verification.

**Job 3: Halt retry loops on regression or non-shrink**
- **When**: I am the rf-task-builder running a fix cycle.
- **I want to**: Halt immediately if any item that PASSed at cycle N FAILs at cycle N+1 (regression) OR if `|gate_failures|` does not strictly shrink between cycles (monotonicity).
- **So I can**: Prevent oscillating retries (21 retry files / 18 batches in FINAL-REPORT §6.2 F2) and surface partition-agent escalation exhaustion as a HIGH-severity synthetic finding instead of silent abort.
- **Current alternatives**: Retry loops without stop-conditions on regression or non-shrink.
- **Pain with alternatives**: Oscillation cost; silent aborts on partition-agent exhaust mask real failures.

### 6.2 Related Jobs

|Job|Frequency|Importance|Satisfaction with Current Solutions|
|-----|-----------|------------|-------------------------------------|
|Surface task-level executor-readability summary|Per MDTM generation|High|3/10 — per-item context but no task-level header|
|Cross-validate header source-areas against item Context fields|Per MDTM generation|High|2/10 — no cross-validation exists|
|Annotate adversarial findings by named axis|Per rf-qa-qualitative run|Medium|4/10 — generic adversarial stance, no taxonomy|


## 7. User Personas

### 7.1 Primary Persona: rf-task-builder Agent

|Attribute|Details|
|-----------|---------|
|**Demographics**|Subagent invoked by the task-builder skill; reads BUILD_REQUEST.md; writes a generated MDTM task file under `.dev/tasks/`.|
|**Goals**|Emit a structurally valid, evidence-bound MDTM file that passes A.8/A.10/A.10.5 gates without fix-cycle thrash.|
|**Pain Points**|Pre-merge: no task-level header to emit; no per-item file:line enforcement structurally tested; no monotonicity stop-conditions.|
|**Technical Proficiency**|High — operates within a deterministic prompt-driven gate pipeline.|
|**Budget Authority**|None — invariants and gates govern; can request retries up to fix-cycle limit.|
|**Success Metrics**|Single-pass gate PASS rate; fix-cycle convergence rate; zero placeholder/DAG/granularity defects.|

**Quote:** "If the gate verdict is deterministic and the retry halts are explicit, I can converge without oscillation."

**A Day in Their Life:**
Receives BUILD_REQUEST.md → spawns research agents (parallel) → generates the MDTM task file with Execution Context header + per-item 5-field schema → submits to rf-qa A.10 task-integrity gate → on PASS, hands off to rf-qa-qualitative with Inherited Structural Verdict.

### 7.2 Secondary Persona: rf-qa Agent (task-integrity gate)

|Attribute|Details|
|-----------|---------|
|**Demographics**|Partitioned QA agent running A.10 task-integrity checks; emits PASS/FAIL verdict table.|
|**Goals**|Apply 17-item checklist (9 existing + 8 TB-Add) deterministically; emit synthetic-dnsp finding on escalation exhaust; surface regressions before downstream agents consume defective items.|
|**Pain Points**|Pre-merge: 9-item checklist misses placeholder scans, DAG, granularity, format consistency; partition exhaust = silent abort.|
|**Technical Proficiency**|High — Read/Grep/Glob/Bash only (no new tool dependency per NFR-CONV.5).|
|**Budget Authority**|Zero-trust stance: any gap regardless of severity = FAIL (rf-qa.md:140-142).|
|**Success Metrics**|TB-Add-1..7 deterministic PASS/FAIL emission; TB-Add-2 ADVISORY emission; synthetic-dnsp 5-field finding on exhaust.|

**Quote:** "Any gap regardless of severity is FAIL. Monotonicity guards plus regression detection mean I never waste a cycle."

### 7.3 Tertiary Persona: rf-qa-qualitative Agent (semantic gate)

|Attribute|Details|
|-----------|---------|
|**Demographics**|Adversarial QA agent running A.10.5 semantic review; receives Inherited Structural Verdict; applies 5-axis overlay.|
|**Goals**|Skip mechanical re-checking on inherited PASS items; flag inherited FAIL items HIGH; apply 5 axes (drift / contradictions / omissions / weakened-criteria / invented-content) to remaining items; emit Self-Audit listing relied-on PASS items AND ≥1 semantic check where rf-qa PASS is insufficient (INV-019).|
|**Pain Points**|Pre-merge: implicit verdict, no axis taxonomy, no Self-Audit requirement.|
|**Technical Proficiency**|High — semantic review through prompt-only checks.|
|**Budget Authority**|Anti-inflation rule (rf-qa-qualitative.md:766-775): mechanical re-checking skipped, semantic verification STILL required.|
|**Success Metrics**|Self-Audit entry per first 5 real runs post-FR-CONV.3; zero items VERIFIED solely from inherited verdict.|

### 7.4 Anti-Personas (Who This Is NOT For)

|Anti-Persona|Why Not Target|
|--------------|----------------|
|`/sc:tasklist` end users|This release does NOT modify `/sc:tasklist`; the port direction is sc → task-builder only.|
|Downstream sprint executors|This release does NOT modify sprint execution; gate-stage outputs are stable.|
|`.dev/tasks/` directory consumers expecting layout changes|Out of scope — `.dev/tasks/` layout is a stable contract for this release (§9 SP-33).|


## 8. Value Proposition Canvas



N/A for this feature PRD — see §2.3 (Why This Feature Is Required) and §4 (Product Vision) for the value contribution, and the SuperClaude framework Platform PRD for platform-level value proposition.


## 9. Competitive Analysis



N/A — `task-builder` and `/sc:tasklist` are internal SuperClaude framework components, not competing products. The closest analog is the inter-skill comparison documented in `.dev/releases/current/task-builder-merge/context-digests/` (digests A/B/C contrast the two skills). This release does not change task-builder's external positioning; it strengthens internal rigor.


## 10. Assumptions & Constraints

### 10.1 Technical Assumptions

|ID|Assumption|Risk if Wrong|Validation Method|
|----|------------|---------------|-------------------|
|TA-1|`.dev/tasks/` directory layout is stable for the scope of this release (§9 SP-33)|All 6 FRs invalidated (K-008 portfolio-wide blast radius)|Cross-check at each release; document layout-change contract in CLAUDE.md|
|TA-2|rf-qa, rf-qa-qualitative, rf-analyst partition protocols continue to spawn N parallel agents|NFR-CONV.10 (parallel-research invariant) violated|Inspect spawn-log; verify N partitions run concurrently on `test_dnsp_does_not_serialize_cohort` fixture|
|TA-3|rf-team-lead.md:417 retains 3-fix-cycle escalation|FR-CONV.6 all-agents-fail guard short-circuits|`grep -n` of rf-team-lead.md before merge; do not modify|
|TA-4|`make sync-dev` / `make verify-sync` pipeline operative|A-001 sync-discipline cross-cutting AC fails|Run `make verify-sync` after each FR lands; commit only on PASS|

### 10.2 Business Assumptions

|ID|Assumption|Risk if Wrong|Validation Method|
|----|------------|---------------|-------------------|
|BA-1|Engineering team can absorb a ≤10% token-cost increase per equivalent BUILD_REQUEST|NFR-CONV.4 token ceiling exceeded; ops cost overrun|Sample 5 representative BUILD_REQUESTs; measure post-merge token counts; ratio must be ≤1.10|
|BA-2|Phase-2 deferral of PR-05 is acceptable to stakeholders|Stakeholder pressure to ship PR-05 in Phase-1 with advisory framing|Re-evaluate at `.dev/tasks/done/` ≥10 completed tasks of ≥3 distinct task_types threshold|


## 11. Dependencies

|ID|Dependency|Type|Status|Risk|
|----|------------|------|--------|------|
|D-1|release-spec.md v1.0.0 (this release's authoritative scope)|Internal|Draft|None — spec is the source|
|D-2|conflict-register.md (5 CASE-D rows)|Internal|Complete|None — append-only ledger|
|D-3|merge-log.md (per-change merge events)|Internal|Complete|None|
|D-4|reflect-task.md + gate-report.md (Phase 5.2 PASS on G1-G5)|Internal|Complete|None|
|D-5|FINAL-REPORT.md §6.3 asymmetric finding|Upstream (v3.8)|Complete|None|
|D-6|rf-team-lead.md:417 escalation behavior|Internal|Stable|TA-3 violation|
|D-7|`.dev/tasks/` directory layout (INV-018)|Internal|Stable per SP-33 commitment|K-008|
|D-8|`make sync-dev` / `make verify-sync` pipeline (A-001)|Tooling|Operational|K-009|


## 12. Scope Definition

### 12.1 In Scope

**Six additive landings** into `src/superclaude/skills/task-builder/SKILL.md` and `src/superclaude/agents/rf-{qa,qa-qualitative,analyst,task-builder}.md`. All landings adapt `/sc:tasklist` *intent* per FINAL-REPORT §6.3 — implementations stay native to task-builder's existing 4-stage gate topology and rf-* agent partitioning model. Acceptance criteria for INV-002, INV-010, INV-012, INV-015, INV-019 are spec-resident. All edits flow through `make sync-dev` / `make verify-sync` (A-001).

Per release-spec.md §1.2.

### 12.2 Out of Scope

- Bulk-port of all 17 `/sc:tasklist` quality-gate checks (REJECTED per CB-3 — see Appendix E in release-spec.md).
- Modifying tier selection on historical pattern (REJECTED per FR §6.2 F4 hidden-input risk — X-004).
- Replacing rf-qa-qualitative's 15-item task-qualitative checklist (REJECTED — overlay-only per X-002 anti-inflation rule).
- PR-05 tier-history advisory (DEFERRED to Phase-2 — see §13 Open Items).
- Any roadmap regeneration or downstream tasklist generation (Phase 8+ work — see §10 Downstream Inputs in release-spec.md).
- Any structural change to `.dev/tasks/` directory layout (INV-018 portfolio-wide note).

### 12.3 Future Scope (Phase-2)

- PR-05 Tier-History Advisory re-evaluation when `.dev/tasks/done/TASK-RF-*` count ≥10 with ≥3 distinct task_types.
- TB-Add-2 item-count-bounds calibration (currently `[ADVISORY]` per OPEN-INV-006).
- `.dev/tasks/` layout versioning mechanism (OPEN-INV-018).


## 13. Open Questions

|Item|Question|Impact|Resolution Target|
|------|----------|--------|-------------------|
|OPEN-PR05|When does `.dev/tasks/done/` reach the ≥10-tasks-of-≥3-task_types threshold to re-evaluate PR-05?|Determines Phase-2 release timing|Re-check at each major release; document in `KNOWLEDGE.md`|
|OPEN-INV-006|Empirical calibration of TB-Add-2 item-count bounds (≥3 / ≤40 track / ≤50 single-track)|TB-Add-2 stays `[ADVISORY]` until calibrated|Phase-2 with PR-05|
|OPEN-INV-017|Historical-file staleness check for PR-05 advisory citations|Academic given PR-05 Phase-2 deferral|Resolve when PR-05 re-evaluated|
|OPEN-INV-018|If `.dev/tasks/` directory layout changes, all 7 proposals require re-integration|Portfolio-wide blast radius|Document layout-change contract; re-integrate on demand|
|OPEN-X-002|PR-04 anti-inflation operational test — "reliance ≠ verification" distinction empirically observable, not structurally provable|First 5 rf-qa-qualitative runs after FR-CONV.3 lands MUST be audited (K-003)|Post-merge audit per release-spec.md §8.3 row 4|
|OPEN-TOKEN|NFR-CONV.4 token-ceiling empirical measurement|Confirms ≤10% increase target|Post-merge measurement on 5 representative BUILD_REQUESTs|


## 14. Technical Requirements

### 14.1 Functional Requirements

Six functional requirements correspond to the six accepted proposals. Each carries the three-field Acceptance Criteria (Observable / Verification / Negative) from release-spec.md §3, mapped to the PRD's `✅` style. CASE classification per the G6 four-case rule is annotated.

#### FR-CONV.1: Structural Gate Additions (PR-06, lands first)

**Description**: Append 8 structural checks (TB-Add-1..8) to rf-qa's task-integrity checklist (currently 9 items at SKILL.md:898-906; rf-qa.md:264-287 has the 20-item form) and mirror in the 15-item validation block (SKILL.md:1491-1507). Per CB-3 (per-check, not bulk) from `/sc:tasklist`'s 17-point gate (checks 11/13/14/15/16/17). TB-Add-7 (Execution-Context source-areas reappear in items) absorbs PR-01 failure-mode #4 cross-validation. TB-Add-8 (per-item Context field file:line citation OR justified absence) resolves INV-015.

**TB-Add catalogue**:
- TB-Add-1: Placeholder scan ("TBD"/"TODO"/title-only) — Hard check
- TB-Add-2: Item count bounds (≥3 / ≤40 track / ≤50 single-track) — `[ADVISORY]`-fail-until-calibrated (INV-006 LOW)
- TB-Add-3: Clarification adjacency to blocked items — Hard check
- TB-Add-4: Circular dependency detection (DAG check) — Hard check
- TB-Add-5: Granularity check (XL items have subtasks) — Hard check
- TB-Add-6: Confidence/Verification format consistency — Hard check
- TB-Add-7: Execution Context source-areas reappear in items (cross-validates PR-01) — Hard check
- TB-Add-8: Every per-item Context field referencing a code surface includes ≥1 file:line citation OR justified-absence comment — Hard check

**CASE**: D — see conflict-register.md row PR-06. Conflicting `/sc:tasklist` mechanism: 17-point gate bulk import. **Protected invariant: zero-trust QA.**

**Acceptance Criteria:**
- ✅ **Observable behavior**: Each of TB-Add-1..8 fires a distinct, item-ID-naming error message when its condition is violated; TB-Add-2 emits an `[ADVISORY]` prefix and does NOT block the gate; TB-Add-1..7 (excluding 2) block the gate on failure.
- ✅ **Verification method**: `grep -nE "TB-Add-[1-8]" src/superclaude/agents/rf-qa.md src/superclaude/skills/task-builder/SKILL.md` must return ≥3 hits per ID (rf-qa.md:264-287 + SKILL.md:898-906 + SKILL.md:1491-1507); synthetic fixture with one placeholder-titled item runs rf-qa and TB-Add-1 emits in the gate log.
- ✅ **Negative criterion (Out of scope / Must not break)**: No existing rf-qa check is renamed, renumbered, or removed; the 9-item A.10 and 15-item validation existing-items are preserved verbatim; bundle-specific `/sc:tasklist` checks (phase-file naming, index references) MUST NOT appear in any TB-Add.

**Dependencies**: None (lands first).

#### FR-CONV.2: Execution Context Header (PR-01, revise-then-adopt, lands second)

**Description**: Insert a task-level `## Execution Context` block in generated MDTM task files (after frontmatter, before checklist). Block contains: References (BUILD_REQUEST GOAL, WHY, related-doc IDs), Source areas (named modules/packages — **strictly NO specific file paths**), Key constraints (top 1-3 invariants from BUILD_REQUEST). Edits at SKILL.md:228-238, SKILL.md:1409-1485, SKILL.md:719. The "no specific paths" rule is **scope-confined to the header**: per-item Context fields and research/*.md retain file:line citations to preserve the **evidence-bound-item** invariant. INV-015 is resolved by TB-Add-8.

**CASE**: D — see conflict-register.md row PR-01. Conflicting `/sc:tasklist` mechanism: `## Execution Context` block per FINAL-REPORT §7-R2. **Protected invariant: evidence-bound-item.**

**Acceptance Criteria:**
- ✅ **Observable behavior**: Generated MDTM task files contain a `## Execution Context` block with exactly three labeled lines (References / Source areas / Key constraints); when BUILD_REQUEST is minimal, the block degrades to References-only with WHY/source-area lines explicitly omitted (PR-01 failure-mode #2).
- ✅ **Verification method**: `grep -n "## Execution Context" <generated-task-file>` returns line N; the next 10 lines contain ≥1 of `References:` / `Source areas:` / `Key constraints:`; `grep -E "src/|/.*:[0-9]+" <header-block-range>` returns zero hits (no file paths or file:line citations within the header).
- ✅ **Negative criterion (Out of scope / Must not break)**: Per-item Context fields elsewhere in the file MUST retain file:line citations OR justified-absence comments (validated by TB-Add-8); the per-item self-contained 5-field schema MUST NOT be altered or supplemented by header content.

**Dependencies**: FR-CONV.1 (TB-Add-7 cross-validation + TB-Add-8 scope-confinement test must already be live).

#### FR-CONV.3: Gate Results Passthrough (PR-04, lands third)

**Description**: Inject rf-qa's task-integrity verdict table verbatim into rf-qa-qualitative's spawn prompt under the heading `## Inherited Structural Verdict`, with prompt language: "PASS items machine-verified — skip structural re-checking; FAIL items machine-verified defects — flag HIGH. Focus on semantic quality." Edits at SKILL.md:923-1000 and rf-qa-qualitative.md:794. Operationalises an already-stated rule.

**CASE**: B — no conflict (correctly absent from conflict-register.md). **Invariant alignment: zero-trust QA** (semantic verification still required).

**Acceptance Criteria:**
- ✅ **Observable behavior**: rf-qa-qualitative's spawn prompt contains `## Inherited Structural Verdict` with the rf-qa table verbatim; on a fix-cycle re-run, the orchestrator re-injects the NEW verdict (INV-002); the spawn prompt's checklist enumeration is dynamic (auto-picks up TB-Add catalogue from FR-CONV.1, INV-010); rf-qa-qualitative's first run after FR-CONV.3 lands produces a `## Self-Audit` entry listing relied-on rf-qa PASS items AND ≥1 semantic check where rf-qa PASS is insufficient (INV-019).
- ✅ **Verification method**: Capture rf-qa-qualitative spawn-prompt log; `grep -n "## Inherited Structural Verdict" <spawn-log>` returns line N; the block immediately below matches rf-qa's emitted verdict table byte-for-byte; on a synthetic 2-cycle fixture, the second cycle's spawn log shows the NEW (cycle-2) verdict, not the stale (cycle-1) verdict; the same fixture's rf-qa-qualitative output contains a Self-Audit section with ≥1 entry per category above.
- ✅ **Negative criterion (Out of scope / Must not break)**: rf-qa-qualitative MUST NOT mark any item VERIFIED solely from the inherited verdict — every VERIFIED item must show an independent semantic-check engagement in the Self-Audit listing; anti-inflation rule rf-qa-qualitative.md:766-775 MUST NOT be weakened, removed, or rephrased; no stale verdict from a prior fix cycle is permitted to govern current-cycle decisions.

**Dependencies**: FR-CONV.1 (TB-Add catalogue is the verdict content); FR-CONV.2 (TB-Add-7 cross-validation runs at A.10 before A.10.5 spawn).

#### FR-CONV.4: Adversarial Category Naming (PR-07, lands fourth)

**Description**: Insert a "Five Adversarial Axes" header subsection BEFORE rf-qa-qualitative's existing 15-item task-qualitative checklist, with axis-annotation requirement on the Items Reviewed table. Five axes: drift / contradictions / omissions / weakened criteria / invented content. Edits at rf-qa-qualitative.md:527-583, rf-qa-qualitative.md:675-714, SKILL.md:961. Overlay annotation, not replacement.

**CASE**: D — see conflict-register.md row PR-07. Conflicting `/sc:tasklist` mechanism: 5-category adversarial agent prompt. **Protected invariant: zero-trust QA.**

**Acceptance Criteria:**
- ✅ **Observable behavior**: rf-qa-qualitative's output renders a "Five Adversarial Axes" subsection BEFORE the 15-item checklist; the Items Reviewed table contains an `axis` column populated with one of {drift, contradictions, omissions, weakened-criteria, invented-content, none} per row; when no item captures BUILD_REQUEST.GOAL verbatim, output includes a single-line `drift-axis-inactive` annotation.
- ✅ **Verification method**: `grep -n "Five Adversarial Axes" <rf-qa-qualitative-output>` returns line N; the Items Reviewed table parses to N rows each with a non-empty `axis` value from the canonical set; synthetic fixture with no GOAL-baseline item produces `drift-axis-inactive` in the output.
- ✅ **Negative criterion (Out of scope / Must not break)**: The existing 15-item task-qualitative checklist MUST NOT be removed, reordered, or replaced — axes annotate, they do not substitute; the severity floor at rf-qa-qualitative.md:789 MUST NOT be weakened; no axis may rely on a code-path change (overlay-only, per CB-3).

**Dependencies**: FR-CONV.3 (5 axes apply to items NOT covered by inherited PASS — composition is clean per INV-013).

#### FR-CONV.5: Retry Monotonicity Guards (PR-02, lands fifth)

**Description**: Add two stop-conditions to EXISTING retry loops (no new loop or stage): (1) Monotonicity guard — HALT if `|gate_failures|` does not strictly shrink between cycles (`F_{n+1} >= F_n` halts); (2) Regression detection — HALT if any item that PASSed at cycle N FAILs at cycle N+1. Precedence: **Regression > monotonicity**. Halt message format: `"Regression detected on Item X.Y — previously PASS at cycle N, now FAIL. Halt overrides monotonicity check."` Edits at SKILL.md:870, SKILL.md:1550, rf-task-builder.md:336-359, rf-qa.md:310-313.

**INV-012 composition criterion**: Synthetic findings emitted by FR-CONV.6 (DNSP) COUNT as failures for `|F_n|` monotonicity. BUT a synthetic finding with identical dedup-key `(assigned_files_range, escalation_ladder_exhaust_point)` across consecutive cycles is a dedup case, NOT a regression.

**CASE**: D — see conflict-register.md row PR-02. Conflicting `/sc:tasklist` mechanism: Stages 9-10 monotonicity guard + regression detection + full-set re-validation. **Protected invariant: zero-trust QA.**

**Acceptance Criteria:**
- ✅ **Observable behavior**: On a fix-cycle where `F_{n+1} >= F_n`, the loop emits `[HALT-MONOTONICITY] |F|=<n>` and exits; on a cycle where Item X.Y was PASS at cycle N and is FAIL at cycle N+1, the loop emits the verbatim regression halt message and exits BEFORE the monotonicity check; on a cycle where a synthetic-dnsp finding with identical dedup-key appears in both N and N+1, no halt fires (dedup recognized).
- ✅ **Verification method**: Synthetic 3-cycle fixture with `F_1=5, F_2=5, F_3=5` halts at cycle 2 with `[HALT-MONOTONICITY]`; synthetic 2-cycle fixture with Item 3.2 PASS@1/FAIL@2 halts at cycle 2 with the regression message; synthetic 2-cycle fixture with one synthetic-dnsp finding (same `assigned_files_range`+`escalation_ladder_exhaust_point` in both cycles) proceeds to cycle 3 without halting; `grep -n "Retry Monotonicity Protocol" src/superclaude/skills/task-builder/SKILL.md` returns ≥2 lines (SKILL.md:870 + SKILL.md:1550).
- ✅ **Negative criterion (Out of scope / Must not break)**: Legitimate slow-cycle correction MUST NOT be halted — any cycle where `|F|` strictly shrinks (even by 1) continues; the four independent retry counters MUST NOT be collapsed into a shared monotonicity state; no halt-on-slow-convergence threshold (e.g., `F_{n+1} = F_n - 1`) is permitted (X-003 REJECTED).

**Dependencies**: FR-CONV.1 (gate produces `F_n` count); FR-CONV.6 (synthetic-dnsp findings consumed by monotonicity per INV-012).

#### FR-CONV.6: DNSP Synthetic Finding (PR-03, BASE, lands sixth)

**Description**: After the entire escalation ladder exhausts on a partition agent (rf-analyst or rf-qa partition), emit a synthetic HIGH-severity finding rather than silently aborting the gate. **Emission contract**: `severity: HIGH; source: "synthetic-dnsp"; affected_range: <agent's assigned_files slice>; evidence: <spawn-log path, OR stub citing log absence>; recommendation: "Manual review required — partition agent failed twice"`. **Dedup key**: `(assigned_files_range, escalation_ladder_exhaust_point)`. **All-agents-fail guard preserved**: if zero partition agents succeeded, escalate normally (rf-team-lead.md:417 — 3 fix cycles per phase) and DO NOT emit synthetic. Edits at SKILL.md:574-654, SKILL.md:872-916, rf-analyst.md:60-69, rf-qa.md:70-77, rf-qa-qualitative.md:72-78.

**CASE**: B — no conflict (correctly absent from conflict-register.md). **Invariant alignment: zero-trust QA + evidence-bound-item + parallel-research.**

**Acceptance Criteria:**
- ✅ **Observable behavior**: When a partition agent's escalation ladder exhausts, the agent's output stream emits a JSON-or-block finding with all 5 fixed fields; two synthetic findings with identical dedup-key collapse with a `found 2 times` note; when zero partitions succeeded, no synthetic emits (existing all-agents-fail escalation runs).
- ✅ **Verification method**: Inject a partition-agent fixture that times out twice; verify synthetic-dnsp finding appears in the gate output with all 5 required fields; inject two identical exhaust events; verify only one finding emits with `found N times`; inject all-agents-fail fixture; verify zero synthetic emits and existing escalation path activates; `grep -n "synthetic-dnsp" src/superclaude/agents/rf-analyst.md src/superclaude/agents/rf-qa.md` returns ≥1 hit per file at the partition-protocol section.
- ✅ **Negative criterion (Out of scope / Must not break)**: Synthetic-dnsp MUST NOT emit before the escalation ladder exhausts — proposal line 35 all-agents-fail guard runs first; the existing escalation behavior at rf-team-lead.md:417 (3 fix cycles per phase) MUST NOT be replaced or short-circuited; synthetic findings MUST NOT mask real findings — HIGH severity ensures gate-level visibility; the dedup-key collapse MUST NOT cross-cycle (PR-02 monotonicity treats dedup as not-regression per INV-012).

**Dependencies**: FR-CONV.5 (PR-02 monotonicity consumes synthetic-dnsp per INV-012 dedup-key rule).

### 14.2 Non-Functional Requirements

Source: release-spec.md §6.

|ID|Requirement|Target|Measurement|
|----|-------------|--------|-------------|
|NFR-CONV.1|Determinism scope — gate outputs deterministic|Gate-results structure (TB-Add-* PASS/FAIL, synthetic-dnsp 5 fields, dedup-key) MUST be deterministic for fixed BUILD_REQUEST + fixed source tree|Re-run task-builder on identical BUILD_REQUEST twice; diff the rf-qa A.10 verdict table; structural fields must be byte-identical|
|NFR-CONV.2|Determinism scope — research-driven prose excluded|Per-item Context prose and rf-qa-qualitative semantic-check prose remain LLM-research-driven; NOT required to be byte-deterministic|Diff prose between two runs; non-byte-equality acceptable; structural fields (axis annotations, finding-counts) must remain byte-equal|
|NFR-CONV.3|Hidden-input guard (per FR §6.2 F4)|Task-builder MUST NOT read any input outside BUILD_REQUEST + source-tree that could modify behavior; PR-05 advisory mechanism REJECTED for Phase-1|Fixture-populated `.dev/tasks/done/` MUST produce byte-identical structural output to empty `.dev/tasks/done/`|
|NFR-CONV.4|Token ceiling|≤10% token-cost increase over pre-merge task-builder baseline per equivalent BUILD_REQUEST|Sample 5 representative BUILD_REQUESTs; record pre-merge and post-merge token counts; ratio ≤1.10|
|NFR-CONV.5|Wall-clock|No new external dependencies; gate additions are local checks; no synchronous network calls added|Inspect rf-qa.md and SKILL.md diffs: only existing tools (Read, Grep, Glob, Bash) permitted|
|NFR-CONV.6|**Invariant preservation — self-contained-item**|5-field per-item schema MUST remain operational across all 8 TB-Add checks and the Execution Context header|Synthetic fixture with all 5 fields passes all TB-Add checks; same with one field stripped fails TB-Add-1 — fails closed|
|NFR-CONV.7|**Invariant preservation — evidence-bound-item**|Every per-item Context referencing code surface MUST retain file:line citation OR justified-absence (TB-Add-8 enforces)|Synthetic fixture with bare `Context: src/foo` (no `:N`) fails TB-Add-8; same with `Context: src/foo:42` passes; same with `Context: <none — pure refactor> [justified-absence]` passes|
|NFR-CONV.8|**Invariant preservation — persistent-`.dev/tasks/`-artifact**|Research/qa persistence in `.dev/tasks/<task-id>/` MUST remain unchanged|Diff `.dev/tasks/` directory layout pre- and post-merge; no path, no naming pattern altered|
|NFR-CONV.9|**Invariant preservation — zero-trust QA**|"Any gap regardless of severity = FAIL" stance (rf-qa.md:140-142) MUST remain operative; no TB-Add or PR-04 mechanism weakens it|Synthetic fixture with 1 LOW finding fails the gate; FR-CONV.3 inherited verdict does NOT mark items VERIFIED in absence of independent semantic check|
|NFR-CONV.10|**Invariant preservation — parallel-research**|rf-analyst / rf-qa partition cohort MUST remain parallel; DNSP fires within-agent-instance (INV-021)|Spawn-log inspection: N partition agents run concurrently; on one agent's escalation exhaust, N-1 continue to completion before DNSP synthesises a finding|

### 14.3 Decisions & Constraints

**G6 Four-Case Conflict Rule (Authoritative)**

Wherever `/sc:tasklist` and `task-builder` behaviors disagree, the G6 four-case rule governs. Per release-spec.md Appendix D:

- **CASE-A**: `/sc:tasklist` has a mechanism; task-builder has a conflicting mechanism. Disposition: explicit decision; one of {ADOPT-ADAPTED, REJECT}. Required: conflict-register row naming the conflicting mechanism and the protected invariant.
- **CASE-B**: `/sc:tasklist` has a mechanism; task-builder is silent (no conflict). Disposition: ADOPT (or ADOPT-ADAPTED). No conflict-register row required.
- **CASE-C**: `/sc:tasklist` is silent; task-builder has a mechanism. Disposition: keep task-builder behavior; nothing to import.
- **CASE-D**: `/sc:tasklist` has a mechanism; task-builder has a *related but non-conflicting* mechanism. Disposition: ADOPT-ADAPTED with scope-confinement or per-check classification (CB-3). Required: conflict-register row.

**Portfolio distribution**: PR-01 D, PR-02 D, PR-03 B, PR-04 B, PR-05 D, PR-06 D, PR-07 D. Conflict-register has exactly 5 rows (one per CASE-D proposal); CASE-B proposals correctly omitted.

**The Five Task-Builder Invariants (Load-Bearing)**

Per release-spec.md §1.0:

1. **self-contained-item**: Every checklist item carries the five fields {Description, Context, Acceptance, Confidence, Verification} sufficient to execute it without reading other items. Operational source: SKILL.md:1452-1457.
2. **evidence-bound-item**: Every per-item Context field referencing a code surface includes a `file:line` citation OR a justified-absence comment. Operational source: SKILL.md:1530 rule #2.
3. **persistent-`.dev/tasks/`-artifact**: Research and QA outputs persist to `.dev/tasks/<task-id>/` with stable naming. Operational source: §11 OPEN-INV-018.
4. **zero-trust QA**: "Any gap regardless of severity = FAIL" stance at the task-integrity gate. Operational source: rf-qa.md:140-142.
5. **parallel-research**: rf-analyst and rf-qa partition cohorts run concurrently; per-partition failures do not serialize the cohort. Operational source: NFR-CONV.10; INV-021.

These invariants are referenced throughout this PRD body and govern every FR's Negative Criterion.


## 15. Technology Stack

|Layer|Component|Purpose|
|-------|-----------|---------|
|Skill host|`task-builder/SKILL.md`|Generation orchestration, 4-stage gate topology|
|Agent hosts|`rf-task-builder.md`, `rf-qa.md`, `rf-qa-qualitative.md`, `rf-analyst.md`|Per-agent prompts and partition protocols|
|Tooling|Read, Grep, Glob, Bash (existing)|No new tools (NFR-CONV.5)|
|Sync pipeline|`make sync-dev`, `make verify-sync`|A-001 cross-cutting AC|
|Output target|`.dev/tasks/<task-id>/` (stable layout per SP-33)|Persistence (NFR-CONV.8)|

No CLI surface changes (release-spec.md §5.1). Task-builder is invoked via the Skill tool; BUILD_REQUEST.md remains the sole input contract.


## 16. User Experience Requirements



### 16.1 Agent-Operator Experience

The only "user" is a downstream agent operator inspecting the generated MDTM file and the gate spawn-logs. Observable improvements:
- Generated MDTM file gains a `## Execution Context` header (FR-CONV.2) providing task-level readability.
- rf-qa A.10 spawn log emits item-ID-naming error messages per TB-Add (FR-CONV.1) instead of generic failures.
- rf-qa-qualitative spawn prompt contains `## Inherited Structural Verdict` block (FR-CONV.3).
- rf-qa-qualitative output renders `## Five Adversarial Axes` subsection (FR-CONV.4).
- Retry loops emit `[HALT-MONOTONICITY]` or verbatim regression halt messages (FR-CONV.5).
- Partition exhaust emits `synthetic-dnsp` finding instead of silent abort (FR-CONV.6).

### 16.2 Accessibility / Localization

N/A — internal framework, plain text logs.


## 17. Legal & Compliance Requirements



N/A — internal framework code change. No new data is collected, stored, or transmitted (NFR-CONV.5).


## 18. Business Requirements



N/A independent pricing. See §5 for the cost-driver note (≤10% token-cost increase per NFR-CONV.4).


## 19. Success Metrics & Measurement

### 19.1 Product Metrics

|Metric|Definition|Target|Measurement Frequency|
|--------|------------|--------|----------------------|
|Single-pass gate PASS rate|% of generated MDTM tasks that pass A.10 task-integrity on first run|≥80% baseline; trend ↑ post-merge|Per fix-cycle|
|Placeholder-defect detection rate|TB-Add-1 firings per 100 generated tasks on synthetic fixtures|100% on placeholder-injected fixtures|Per release|
|DAG-cycle detection rate|TB-Add-4 firings per 100 generated tasks on synthetic fixtures with circular deps|100% on circular-dep fixtures|Per release|
|Self-Audit coverage (post-FR-CONV.3)|% of rf-qa-qualitative runs containing a `## Self-Audit` entry with ≥1 semantic check beyond inherited PASS|100% (INV-019 mandate)|Per run, first 5 real runs audited (K-003)|

### 19.2 Business Metrics

|Metric|Definition|Target|Measurement Frequency|
|--------|------------|--------|----------------------|
|Token-cost ratio (post-merge / pre-merge)|NFR-CONV.4 token-ceiling empirical|≤1.10|Once post-merge on 5 representative BUILD_REQUESTs|
|Fix-cycle convergence rate|% of fix-cycles that converge within 3 cycles|≥75% baseline; trend ↑ post-merge (PR-02 effect)|Per fix-cycle|
|Phase-2 PR-05 re-evaluation trigger|`.dev/tasks/done/TASK-RF-*` count ≥10 with ≥3 distinct task_types|Threshold reached|At each major release|

### 19.3 Technical Metrics

|Metric|Definition|Target|Alerting Threshold|
|--------|------------|--------|-------------------|
|Synthetic-dnsp emission count|Per gate run, count of synthetic-dnsp findings emitted (FR-CONV.6)|≥1 on twice-exhaust fixture; 0 on healthy run|>0 in production triggers human review|
|`[HALT-MONOTONICITY]` emission count|Per fix-cycle batch, count of monotonicity halts (FR-CONV.5)|<10% of fix-cycle batches (most converge by shrinking)|>50% indicates upstream BUILD_REQUEST defect|
|Regression-halt emission count|Per fix-cycle batch, count of regression halts (FR-CONV.5)|<5% of fix-cycle batches|>20% indicates fix-cycle introducing new defects|
|`make verify-sync` PASS rate|Per FR-merge, sync-verification status|100% (A-001)|Any FAIL blocks commit|


## 20. Risk Analysis

### 20.1 Technical Risks

Source: release-spec.md §7.

|Risk|Probability|Impact|Mitigation|Contingency|
|------|-------------|--------|------------|-------------|
|K-001 — TB-Add false positives waste fix-cycles|low|low|Each TB-Add cites source-check-ID for traceability; TB-Add-2 `[ADVISORY]`; FR-CONV.1 negative criterion forbids removing items, but each TB-Add can be individually disabled by reverting its append line|Disable specific TB-Add line; document false-positive class|
|K-002 — Execution Context header drift (header says X, items say Y)|low|low|TB-Add-7 cross-validates header source-areas reappear in items; on drift, gate fails and rf-task-builder retries; header is optional (degrades to References-only)|Header optional fallback|
|K-003 — PR-04 passthrough causes inflation despite anti-inflation rule|low|med|INV-019 acceptance criterion mandates Self-Audit listing on first run; X-002 flagged as audit target — first 5 rf-qa-qualitative runs after FR-CONV.3 lands MUST be audited|If any audit shows inflation, disable passthrough and fall back to current behavior|
|K-004 — 5-axis annotation ambiguity over-flags items|low|low|Axes are annotation-only; existing 15-item checklist still runs; severity floor preserved; `drift-axis-inactive` annotation when GOAL-baseline missing|Audit axis distribution; tune annotation rules|
|K-005 — Retry monotonicity halts legitimate slow-cycle correction|low|low|Strict-shrink threshold (`F_{n+1} >= F_n`); any forward motion permits continuation; X-003 "halt on slow convergence" REJECTED|Rollback by disabling guards individually|
|K-006 — Synthetic-dnsp findings mask real issues|low|low|HIGH severity ensures gate-level visibility; all-agents-fail guard preserves existing escalation path; dedup-key prevents over-emission while preserving the failure signal|Inspect synthetic-dnsp emission count metric weekly|

### 20.2 Operational Risks

|Risk|Probability|Impact|Mitigation|Contingency|
|------|-------------|--------|------------|-------------|
|K-007 — PR-04 + PR-06 sequencing inversion (PR-04 lands before PR-06)|low|med|Sequencing rule PR-06 → PR-04 enforced in §4.6; PR-04 prompt uses dynamic checklist enumeration so it richens automatically when TB-Add items go live (INV-010 mitigation)|Re-merge in correct order; verify INV-010|
|K-008 — INV-018 `.dev/tasks/` directory structure changes invalidate all 7 proposals|low|high|Portfolio-wide note; SP-33 stability commitment; if directory structure changes, re-integrate all 7 proposals at the new layout|Re-integration commit covering all six FRs|
|K-009 — sync-discipline (A-001) violated: `.claude/` edited directly without `make verify-sync`|low|med|All FRs name `src/superclaude/` paths exclusively; CLAUDE.md mandates the sync workflow; `make verify-sync` MUST pass before commit|Revert `.claude/` direct edit; re-run from `src/superclaude/`|
|K-010 — Token ceiling NFR-CONV.4 exceeded by >10%|low|low|Empirical measurement post-merge; if exceeded, profile per-FR contribution and revise FR-CONV.3 Inherited Structural Verdict block (verdict table can be summarised rather than verbatim)|FR-CONV.3 verdict-table summarisation|

### 20.3 Business Risks

N/A independent — internal framework change. See K-010 for cost-related risk.


## 21. Implementation Plan

> Source: release-spec.md §3, §4, §4.6, §8, §9.

### 21.1 Epics, Features & Stories

#### 21.1.1 Epic Summary

|Epic #|Epic Name|Features|Stories|Priority|Phase|
|--------|-----------|----------|---------|----------|-------|
|1|Structural Gate Reinforcement|FR-CONV.1, FR-CONV.2|2|P0|Phase-1|
|2|Inter-Agent Verdict Channel|FR-CONV.3, FR-CONV.4|2|P0|Phase-1|
|3|Retry & Exhaust Resilience|FR-CONV.5, FR-CONV.6|2|P0|Phase-1|
|4|Tier-History Advisory (deferred)|PR-05|1|P2|Phase-2|

#### Epic 1: Structural Gate Reinforcement

**Description**: Strengthen rf-qa's task-integrity gate and the generated MDTM file's task-level readability.

**US-1.1: TB-Add catalogue lands in rf-qa A.10**
- **As a** rf-qa agent operator
- **I want** 8 new structural checks (TB-Add-1..8) appended to the 9-item A.10 task-integrity checklist
- **So that** placeholder items, DAG cycles, granularity outliers, and format inconsistencies are caught at gate-time

**Acceptance Criteria:**
- ✅ Each of TB-Add-1..8 fires a distinct item-ID-naming error message when violated (FR-CONV.1 Observable)
- ✅ `grep -nE "TB-Add-[1-8]" src/superclaude/agents/rf-qa.md src/superclaude/skills/task-builder/SKILL.md` returns ≥3 hits per ID (FR-CONV.1 Verification)
- ✅ No existing rf-qa check is renamed/renumbered/removed; bundle-specific `/sc:tasklist` checks (phase-file naming, index references) MUST NOT appear in any TB-Add (FR-CONV.1 Negative / Out of scope)

**Success Metrics:**
- TB-Add-1 detection rate on placeholder fixture: 100%
- TB-Add-4 detection rate on circular-dep fixture: 100%

**US-1.2: Execution Context header lands in generated MDTM files**
- **As a** downstream executor agent
- **I want** a task-level `## Execution Context` header with References / Source areas / Key constraints
- **So that** I have a "what this whole task is about" view without re-reading every item Context field

**Acceptance Criteria:**
- ✅ Generated MDTM files contain `## Execution Context` with exactly three labeled lines; minimal BUILD_REQUEST degrades to References-only (FR-CONV.2 Observable)
- ✅ `grep -E "src/|/.*:[0-9]+" <header-block-range>` returns zero hits (FR-CONV.2 Verification)
- ✅ Per-item Context fields elsewhere MUST retain file:line citations or justified-absence comments (validated by TB-Add-8); per-item 5-field schema MUST NOT be altered (FR-CONV.2 Negative / Out of scope)

**Success Metrics:**
- Self-contained-item invariant preservation: 100% (NFR-CONV.6)
- Evidence-bound-item invariant preservation: 100% (NFR-CONV.7)

#### Epic 2: Inter-Agent Verdict Channel

**Description**: Make the rf-qa → rf-qa-qualitative verdict explicit and annotate adversarial findings by named axis.

**US-2.1: Inherited Structural Verdict block lands in rf-qa-qualitative spawn**
- **As a** rf-qa-qualitative agent operator
- **I want** rf-qa's verdict table verbatim in my spawn prompt with directive language
- **So that** I skip mechanical re-checking and focus on semantic quality

**Acceptance Criteria:**
- ✅ Spawn prompt contains `## Inherited Structural Verdict` with the rf-qa table verbatim; cycle 2 spawn shows cycle-2 verdict not cycle-1; first run produces a `## Self-Audit` entry with ≥1 semantic check beyond inherited PASS (FR-CONV.3 Observable)
- ✅ Verbatim byte-match against rf-qa output; synthetic 2-cycle fixture shows fresh verdict on cycle 2 (FR-CONV.3 Verification)
- ✅ No item VERIFIED solely from inherited verdict; anti-inflation rule rf-qa-qualitative.md:766-775 MUST NOT be weakened; no stale verdict (FR-CONV.3 Negative / Out of scope)

**Success Metrics:**
- Self-Audit coverage post-FR-CONV.3 land: 100% on first 5 real runs (K-003 audit gate)

**US-2.2: Five Adversarial Axes overlay lands in rf-qa-qualitative output**
- **As a** rf-qa-qualitative agent operator
- **I want** a "Five Adversarial Axes" header subsection BEFORE the 15-item checklist with axis-annotation on the Items Reviewed table
- **So that** I can sharpen the adversarial stance with named taxonomy {drift, contradictions, omissions, weakened-criteria, invented-content}

**Acceptance Criteria:**
- ✅ Output renders "Five Adversarial Axes" subsection BEFORE the 15-item checklist; Items Reviewed table has `axis` column populated; no-GOAL-baseline produces `drift-axis-inactive` (FR-CONV.4 Observable)
- ✅ `grep -n "Five Adversarial Axes"` returns N; table parses with non-empty `axis` per row (FR-CONV.4 Verification)
- ✅ 15-item checklist MUST NOT be removed/reordered/replaced; severity floor MUST NOT be weakened; overlay-only per CB-3 (FR-CONV.4 Negative / Out of scope)

**Success Metrics:**
- Axis annotation coverage: 100% of rows
- `drift-axis-inactive` annotation rate matches GOAL-baseline absence rate

#### Epic 3: Retry & Exhaust Resilience

**Description**: Halt oscillating retry loops on regression-or-non-shrink; surface partition-agent exhaust as a HIGH-severity synthetic finding.

**US-3.1: Retry monotonicity + regression halt-conditions land in existing retry loops**
- **As a** rf-task-builder agent operator
- **I want** retry loops to halt on regression or non-shrink with verbatim messages
- **So that** I never waste a cycle on oscillating retries

**Acceptance Criteria:**
- ✅ `F_{n+1} >= F_n` halts with `[HALT-MONOTONICITY]`; PASS@N/FAIL@N+1 halts with regression message before monotonicity; dedup-key synthetic across cycles does not halt (FR-CONV.5 Observable)
- ✅ 3-cycle fixture `F=5,5,5` halts at cycle 2; PASS@1/FAIL@2 fixture halts with regression; dedup fixture proceeds to cycle 3 (FR-CONV.5 Verification)
- ✅ Slow-cycle shrink (even by 1) MUST NOT be halted; 4 retry counters MUST NOT be collapsed; no halt-on-slow-convergence threshold (X-003 REJECTED) (FR-CONV.5 Negative / Out of scope)

**Success Metrics:**
- Fix-cycle convergence rate post-merge: trend ↑
- `[HALT-MONOTONICITY]` emission count: <10% of fix-cycle batches

**US-3.2: DNSP synthetic-finding emission contract lands in partition agents**
- **As a** rf-team-lead orchestrator
- **I want** partition-agent escalation exhaust to emit a HIGH-severity synthetic finding with 5 fixed fields and a dedup-key
- **So that** silent aborts are eliminated and parallel-research invariant holds

**Acceptance Criteria:**
- ✅ Exhaust emits 5-field finding; two identical findings collapse with `found 2 times`; all-agents-fail bypass emits zero synthetic (FR-CONV.6 Observable)
- ✅ Twice-exhaust fixture emits finding with all 5 fields; identical-exhaust fixture collapses; all-agents-fail fixture activates existing escalation (FR-CONV.6 Verification)
- ✅ Synthetic-dnsp MUST NOT emit before exhaust; rf-team-lead.md:417 escalation MUST NOT be replaced/short-circuited; synthetic findings MUST NOT mask real findings (HIGH severity ensures visibility); dedup-key MUST NOT cross-cycle (FR-CONV.6 Negative / Out of scope)

**Success Metrics:**
- Parallel-research invariant preservation: 100% (NFR-CONV.10) — N-1 partitions complete on N-th exhaust

#### Epic 4: Tier-History Advisory (DEFERRED Phase-2)

**US-4.1: PR-05 advisory re-evaluation when historical-data threshold reached**
- Deferred per release-spec.md §2.1; trigger: `.dev/tasks/done/TASK-RF-*` ≥10 with ≥3 distinct task_types.

#### 21.1.2 Feature Prioritization Matrix

|Feature|Reach|Impact|Confidence|Effort|RICE Score|Priority|
|---------|-------|--------|------------|--------|------------|----------|
|FR-CONV.1 (PR-06)|All MDTM tasks|3|95%|2 pw|1.43|P0|
|FR-CONV.2 (PR-01)|All MDTM tasks|2|90%|1 pw|1.80|P0|
|FR-CONV.3 (PR-04)|All A.10.5 runs|3|90%|1 pw|2.70|P0|
|FR-CONV.4 (PR-07)|All A.10.5 runs|2|88%|1 pw|1.76|P0|
|FR-CONV.5 (PR-02)|All retry loops|3|92%|2 pw|1.38|P0|
|FR-CONV.6 (PR-03, BASE)|All partition exhausts|3|95%|2 pw|1.43|P0|
|PR-05 (DEFERRED)|tier selection only|1|50%|2 pw|0.25|P2|

### 21.2 Implementation Phasing

|Phase|Features|Rationale|
|-------|----------|-----------|
|Phase-1 (v3.9)|FR-CONV.1 → FR-CONV.2 → FR-CONV.3 → FR-CONV.4 → FR-CONV.5 → FR-CONV.6|Strict serial sequencing per release-spec.md §4.6 — resolves INV-010 (PR-06 first so PR-04 picks up TB-Add catalogue) and INV-012 (PR-02 dedup against PR-03)|
|Phase-2 (post-v3.9)|PR-05 (re-evaluation)|Triggered by `.dev/tasks/done/` ≥10 / ≥3 task_types threshold|

**Landing sequence binding** (release-spec.md §9 SP-26): §4.6 is the binding serial order. The "could parallel-land with 5" narrative in §4.5 is **non-binding advisory text**.

### 21.3 Release Criteria & Definition of Done

#### Phase-1 Release Criteria

|Category|Criterion|Validation Method|Status|
|----------|-----------|-------------------|--------|
|**Functionality**|All 6 FR Observable behaviors emit on synthetic fixtures|Test suite §8.1|⬜|
|**Determinism**|NFR-CONV.1 byte-identical structural output across two runs|Diff rf-qa A.10 verdict tables|⬜|
|**Hidden-input**|NFR-CONV.3 fixture-populated `.dev/tasks/done/` produces byte-identical output|Test `test_hidden_input_guard`|⬜|
|**Invariant preservation**|NFR-CONV.6..10 all PASS|Synthetic fixtures per NFR|⬜|
|**Token ceiling**|NFR-CONV.4 ≤10% increase on 5 BUILD_REQUEST samples|Token count comparison|⬜|
|**Sync discipline**|`make verify-sync` PASS after all 6 landings|`make sync-dev && make verify-sync`|⬜|
|**Sequencing**|PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03 strictly serial|git log inspection|⬜|
|**Documentation**|This PRD + TDD + Tech Reference linkbacks valid|Link check|⬜|
|**Post-merge audit**|First 5 rf-qa-qualitative runs audited (K-003)|Manual review|⬜|

#### Definition of Done (Per-FR)

A feature (FR-CONV.X) is "Done" when:
- [ ] All three Acceptance Criteria fields (Observable / Verification / Negative) PASS on synthetic fixtures
- [ ] Unit tests per release-spec.md §8.1 written and passing
- [ ] Integration tests per release-spec.md §8.2 passing
- [ ] `make verify-sync` PASS
- [ ] Code reviewed by rf-* agent maintainer
- [ ] No invariant weakening (NFR-CONV.6..10 confirmed)
- [ ] Per-FR rollback procedure documented in release-spec.md §9

#### Rollback & Contingency Plans

Source: release-spec.md §9 Rollback dependency matrix (SP-10).

|Scenario|Detection Method|Rollback Procedure|Decision Maker|
|----------|------------------|-------------------|----------------|
|FR-CONV.3 inflation detected (K-003)|Audit of first 5 rf-qa-qualitative runs|Disable passthrough; fall back to current behavior|QA lead|
|FR-CONV.5 false halt on legitimate slow-cycle|Halt rate >50% of fix-cycles|Disable guards individually|rf-task-builder maintainer|
|FR-CONV.1 TB-Add false-positive volume unacceptable|False-positive rate per check|Revert specific TB-Add append line|rf-qa maintainer|
|Token ceiling (K-010) exceeded|NFR-CONV.4 measurement|Summarise FR-CONV.3 verdict table|Engineering lead|
|`.dev/tasks/` layout changes (K-008)|INV-018 trigger|Re-integrate all 6 FRs at new layout|Engineering lead + orchestrator|
|Reverted FR-CONV.5 (monotonicity)|Per §9 SP-10|Co-revert FR-CONV.6 dedup-key emission|Engineering lead|
|Reverted FR-CONV.1 (TB-Add catalogue)|Per §9 SP-10|Co-revert FR-CONV.3 dynamic-enumeration consumer|Engineering lead|

### 21.4 Timeline & Milestones

```
Phase-1: Task-Builder Convergence ──────── 2026-05-14 - 2026-Q3
    ├── M1.1: FR-CONV.1 (PR-06) merges     TBD
    ├── M1.2: FR-CONV.2 (PR-01) merges     TBD
    ├── M1.3: FR-CONV.3 (PR-04) merges     TBD
    ├── M1.4: FR-CONV.4 (PR-07) merges     TBD
    ├── M1.5: FR-CONV.5 (PR-02) merges     TBD
    ├── M1.6: FR-CONV.6 (PR-03, BASE) merges TBD
    └── M1.7: Post-merge audit + NFR-CONV.4 measurement TBD

Phase-2 (PR-05 re-evaluation): trigger-dependent — no fixed date
```


## 22. Customer Journey Map

<!-- SCOPE NOTE: Feature PRD with no end-user journey. Replaced with agent-operator journey. -->

N/A end-user. The agent-operator journey is captured in §16.1 and release-spec.md §2.2 (Workflow / Data Flow).


## 23. Error Handling & Edge Cases

### 23.1 Error Categories

|Category|Examples|Agent Experience|Recovery|
|----------|----------|-----------------|----------|
|**Structural defects (TB-Add-1..7)**|Placeholder item, DAG cycle, granularity outlier, format mismatch, header drift|Gate FAILs with item-ID-naming error|rf-task-builder fix-cycle|
|**Advisory (TB-Add-2)**|Item count outside bounds|`[ADVISORY]` annotation; gate does NOT fail|None — informational only|
|**Evidence-binding miss (TB-Add-8)**|Bare `Context: src/foo` without `:N`|Gate FAILs with TB-Add-8 error|rf-task-builder adds `:line` or justified-absence|
|**Retry oscillation (FR-CONV.5)**|`F_{n+1} >= F_n` or PASS@N/FAIL@N+1|Loop halts with `[HALT-MONOTONICITY]` or verbatim regression message|Manual review|
|**Partition exhaust (FR-CONV.6)**|One agent escalation ladder exhausts twice|Synthetic-dnsp HIGH finding emits; N-1 partitions complete|Manual review (recommendation: "Manual review required — partition agent failed twice")|
|**All-agents-fail**|Zero partitions succeeded|No synthetic emits; existing rf-team-lead.md:417 escalation runs|3 fix cycles per phase|

### 23.2 Edge Cases

|Scenario|Expected Behavior|Test Case|
|----------|-------------------|-----------|
|Minimal BUILD_REQUEST|Execution Context degrades to References-only (PR-01 failure-mode #2)|`test_execution_context_minimal_buildrequest`|
|No GOAL-baseline item in checklist|`drift-axis-inactive` annotation surfaces (PR-07 failure-mode #3)|`test_drift_axis_inactive_when_no_goal_baseline`|
|Synthetic-dnsp dedup across cycles|Dedup recognized; not regression (INV-012)|`test_synthetic_dnsp_dedup_not_regression`|
|Fixture-populated `.dev/tasks/done/`|Byte-identical structural output to empty `.dev/tasks/done/` (NFR-CONV.3)|`test_hidden_input_guard`|
|Sequencing inversion (PR-04 before PR-06)|INV-010 mitigation: dynamic enumeration richens automatically when TB-Add items go live|`test_sequencing_PR06_before_PR04`|

### 23.3 Graceful Degradation

|Component Failure|Degraded Experience|Communication|
|-------------------|--------------------|--------------------|
|Execution Context header generation fails|Header degrades to References-only or omitted; TB-Add-7 still cross-validates if present|rf-task-builder log|
|FR-CONV.3 passthrough block missing|rf-qa-qualitative spawns without inherited verdict; falls back to current behavior (mechanical re-check or rubber-stamp risk)|K-003 audit fires|
|Synthetic-dnsp emission fails|Existing all-agents-fail escalation activates (rf-team-lead.md:417)|rf-team-lead log|


## 24. User Interaction & Design

<!-- SCOPE NOTE: Feature PRD with no UI surface. -->

N/A — no UI. Spawn-log diff is the observable surface (see §16.1).


## 25. API Contract Examples

Source: release-spec.md §4.5 (Data Models) + §5.3 (Phase Contracts).

### 25.1 Execution Context Header (FR-CONV.2)

```yaml
"## Execution Context":
  References:        # list of BUILD_REQUEST refs (GOAL, WHY, related-doc IDs)
    - "R-###: <ref-line>"
  Source areas:      # list of named modules/packages — NEVER specific file paths
    - "<package-or-module-name>"
  Key constraints:   # top 1-3 invariants from BUILD_REQUEST
    - "<invariant statement>"
```

### 25.2 Inherited Structural Verdict Block (FR-CONV.3)

```yaml
"## Inherited Structural Verdict":
  rf_qa_table_verbatim: <copy of rf-qa task-integrity table at spawn time>
  prompt_directive: "PASS items machine-verified — skip structural re-checking; FAIL items machine-verified defects — flag HIGH. Focus on semantic quality."
  reinjection_rule: "On fix-cycle re-run, orchestrator MUST re-inject the NEW verdict; stale verdicts forbidden."
```

### 25.3 Synthetic DNSP Finding (FR-CONV.6)

```yaml
synthetic_dnsp_finding:
  severity: HIGH                                # fixed
  source: "synthetic-dnsp"                      # fixed
  affected_range: "<agent's assigned_files slice>"
  evidence: "<spawn-log path, OR stub citing log absence>"
  recommendation: "Manual review required — partition agent failed twice"
  dedup_key: "(assigned_files_range, escalation_ladder_exhaust_point)"
  found_n_times: <int, default 1>               # increments on dedup collapse
```

### 25.4 Per-Item Checklist Schema (referenced by NFR-CONV.6)

```yaml
per_item_schema:
  Description: "<one-line task-item action statement>"
  Context: "<file:line citation OR justified-absence comment>"     # TB-Add-8 enforced
  Acceptance: "<observable success condition>"
  Confidence: "<HIGH|MEDIUM|LOW> — with one-line rationale"
  Verification: "<command, file inspection, or test to confirm Acceptance>"
```

### 25.5 Phase Contract: rf-qa → rf-qa-qualitative

```yaml
phase_contract:
  producer: rf-qa
  consumer: rf-qa-qualitative
  artifact: "## Inherited Structural Verdict block in spawn prompt"
  schema_version: "1.0.0"
  delivery_semantics: "at-most-once-per-cycle"
  freshness_rule: "On fix-cycle re-run, orchestrator re-injects NEW verdict; stale verdicts forbidden (INV-002)"
  enumeration_rule: "Checklist enumeration is dynamic — auto-picks up TB-Add catalogue from FR-CONV.1 (INV-010)"
  consumer_obligation: "Self-Audit listing relied-on PASS items AND ≥1 semantic check (INV-019)"
  anti_inflation: "Mechanical re-checking SKIPPED for PASS items; semantic verification STILL REQUIRED (rf-qa-qualitative.md:766-775)"
  failure_mode: "If rf-qa fails to emit a verdict, rf-qa-qualitative MUST NOT spawn — gate halts at A.10 before A.10.5"
```


## 26. Contributors & Collaboration

|Role|Owner|Responsibility|
|------|-------|----------------|
|Orchestrator pipeline|Phase 8 owner|PRD authorship; verdict gates G1-G5|
|task-builder skill maintainer|task-builder owner|SKILL.md edits for FR-CONV.1/2/3/4/5/6|
|rf-qa agent maintainer|rf-qa owner|rf-qa.md edits for TB-Add-1..8, DNSP emission, retry monotonicity|
|rf-qa-qualitative agent maintainer|rf-qa-qualitative owner|rf-qa-qualitative.md edits for Inherited Verdict, 5 Adversarial Axes, DNSP emission|
|rf-analyst agent maintainer|rf-analyst owner|rf-analyst.md edits for DNSP emission|
|rf-task-builder agent maintainer|rf-task-builder owner|rf-task-builder.md edits for retry monotonicity integration|
|QA lead|QA owner|K-003 post-merge audit; Self-Audit verification on first 5 real runs|
|Engineering lead|engineering owner|NFR-CONV.4 token-ceiling measurement; sync-discipline (A-001)|


## 27. Related Resources

- **Source release spec**: `.dev/releases/current/task-builder-merge/release-spec.md`
- **Conflict register**: `.dev/releases/current/task-builder-merge/conflict-register.md`
- **Merge log**: `.dev/releases/current/task-builder-merge/adversarial/merge-log.md`
- **Per-proposal verdicts**: `.dev/releases/current/task-builder-merge/adversarial/per-proposal-verdicts.md`
- **Invariant probe**: `.dev/releases/current/task-builder-merge/adversarial/invariant-probe.md`
- **Refactor plan**: `.dev/releases/current/task-builder-merge/adversarial/refactor-plan.md`
- **Reflection task**: `.dev/releases/current/task-builder-merge/reflection/reflect-task.md`
- **Gate report (Phase 5.2 PASS)**: `.dev/releases/current/task-builder-merge/reflection/gate-report.md`
- **Upstream FINAL-REPORT**: `.dev/releases/backlog/v3.8-RigorFlowMerger-tasklist/FINAL-REPORT.md`
- **Source code targets**:
  - `src/superclaude/skills/task-builder/SKILL.md`
  - `src/superclaude/skills/sc-tasklist-protocol/SKILL.md`
  - `src/superclaude/agents/rf-qa.md`
  - `src/superclaude/agents/rf-qa-qualitative.md`
  - `src/superclaude/agents/rf-analyst.md`
  - `src/superclaude/agents/rf-task-builder.md`
- **PRD template**: `src/superclaude/examples/prd_template.md`


## 28. Maintenance & Ownership

|Aspect|Owner|Cadence|
|--------|-------|---------|
|PRD content currency|Orchestrator pipeline (Phase 8)|Until Phase 9 closes; then engineering lead|
|FR-CONV.1..6 implementation|Per-FR owner per §26|Per FR landing|
|Post-merge audit (K-003)|QA lead|First 5 rf-qa-qualitative runs after FR-CONV.3|
|Token-ceiling measurement (NFR-CONV.4)|Engineering lead|Once post-merge on 5 representative BUILD_REQUESTs|
|Phase-2 PR-05 re-evaluation trigger|Engineering lead|At each major release; threshold check|
|Invariant integrity audit|QA lead|Per release; NFR-CONV.6..10 confirmation|
|`.dev/tasks/` layout stability (K-008)|Engineering lead|Per release; SP-33 commitment review|
|`make verify-sync` discipline (A-001, K-009)|Per-commit author|Per commit|

**Document history**: v1.0 created 2026-05-14 by Phase 8 of /sc:adversarial Mode A orchestration; direct-synthesis fallback (prd skill returned protocol text).
