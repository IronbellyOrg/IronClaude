---
id: "MASTRA-BEADS-HYBRID-TECHREF"
title: "Mastra + Backlog.md + Beads Hybrid Adapter-First Orchestration Architecture (PROPOSED) - Technical Reference"
description: "Design reference documenting the architecture, subsystems, data flow, and operational details of the PROPOSED Mastra + Backlog.md + Beads hybrid adapter-first orchestration architecture. The hybrid is NOT yet built; this reference describes the built SuperClaude Python kernel being adapted and the proposed target stack around it."
version: "1.0"
status: "🟡 Draft"
type: "📖 Technical Reference"
priority: "🔼 High"
created_date: "2026-06-03"
updated_date: "2026-06-03"
assigned_to: "orchestration-platform-team"
autogen: false
autogen_method: ""
coordinator: "tech-lead"
parent_doc: ".dev/releases/backlog/mastra-beads-port-feasibility/FEASIBILITY-STUDY.md"
related_prd: ""
related_tdd: ""
depends_on:
- ".dev/releases/backlog/mastra-beads-port-feasibility/FEASIBILITY-STUDY.md"
related_docs:
- ".dev/releases/backlog/mastra-beads-port-feasibility/ROADMAP.md"
- ".dev/releases/backlog/mastra-beads-port-feasibility/RISK-REGISTER.md"
- ".dev/releases/backlog/mastra-beads-port-feasibility/DECISION-SUMMARY.md"
tags:
- technical-reference
- mastra-beads-hybrid
- post-implementation
- architecture
- design-reference
template_schema_doc: ""
estimation: ""
sprint: ""
due_date: ""
start_date: ""
completion_date: ""
blocker_reason: ""
review_info:
  last_reviewed_by: ""
  last_review_date: ""
  next_review_date: ""
verified_against_code:
  last_verified_date: "2026-06-03"
  verified_by: "tech-reference skill"
  code_version: "9e864860"
---

# Mastra + Backlog.md + Beads Hybrid Adapter-First Orchestration Architecture (PROPOSED) - Technical Reference

> **WHAT:** Design reference documenting the architecture, subsystems, data flow, and operational details of the **PROPOSED** Mastra + Backlog.md + Beads hybrid adapter-first orchestration architecture. The BUILT side is the runtime-agnostic SuperClaude Python pipeline kernel; the hybrid stack wrapped around it is design intent, not shipped behavior.
> **WHY:** Serves as the canonical built-vs-design source of truth for AI coding agents and human developers who need to understand the seam between the BUILT Python orchestrator and the proposed external Mastra/Backlog.md/Beads substrate, without reading every source file.
> **HOW TO USE:** Treat every `[DESIGN — UNBUILT]` claim as proposed and every `[CODE-VERIFIED]` claim as real at HEAD `9e864860`. Consult the Built-vs-Design Status Ledger (§15.3) before treating any subsystem as implemented.

> **CRITICAL — PROPOSED, NOT-YET-BUILT ARCHITECTURE.** The hybrid Mastra + Backlog.md + Beads system **does not exist in the repository today**. No source file implements any Mastra, Backlog.md, or Beads integration at HEAD `9e864860`. The feasibility verdict is **Conditionally Recommended**, approach **Option D → Option A** (a time-boxed validation spike, then hybrid adapter-first only if spike exit gates clear).

### Document Lifecycle Position

| Phase | Document | Ownership | Status |
|-------|----------|-----------|--------|
| Requirements | Product PRD | Product | n/a (feasibility-driven, no frozen PRD) |
| Design | FEASIBILITY-STUDY | Engineering | Reference parent for this document |
| **Implementation** | **This Technical Reference** | **Engineering** | **Design reference — describes BUILT kernel + PROPOSED hybrid; updated as the port is built** |

### Tiered Usage

| Tier | When to Use | Sections Required |
|------|-------------|-------------------|
| **Lightweight** | Small features, single subsystem, <5 components | 1, 2, 3, 4, 5, 12, 13 |
| **Standard** | Most features (5-20 components, multiple subsystems) | All numbered sections; skip conditional sections marked *(if applicable)* |
| **Heavyweight** | Major features, cross-cutting systems, platform-level | All sections fully completed, including all conditional sections |

> **This document is Tier: Heavyweight** — cross-cutting orchestration replatforming spanning a built Python kernel, a proposed adapter layer, three external substrates, and a net-new governance plane.

---

## Document Information

| Field | Value |
|-------|-------|
| **Feature Name** | Mastra + Backlog.md + Beads Hybrid Adapter-First Orchestration Architecture (PROPOSED) |
| **Feature Type** | Backend / Service / Infrastructure (orchestration replatforming) |
| **Tech Lead** | orchestration-platform-team |
| **Engineering Team** | orchestration-platform-team |
| **Maintained By** | orchestration-platform-team |
| **Source Location** | `src/superclaude/cli/` (the BUILT side being adapted) |
| **Last Verified Against Code** | 2026-06-03 (HEAD `9e864860`) |
| **Implementation Status** | Design reference — BUILT kernel stable; hybrid PROPOSED / unbuilt |

### Living Document Contract

This document MUST be updated when:

- A component is added, removed, or significantly refactored
- A subsystem's behavior, data flow, or interface changes
- New conventions or patterns are introduced to the feature
- State shape or ownership approach changes
- The BUILT/DESIGN boundary moves (any Mastra/Backlog.md/Beads integration lands — update the §15.3 ledger)

---

## Completeness Status

**Completeness Checklist:**

- [x] Section 1: Overview — **Complete**
- [x] Section 2: Architecture — **Complete**
- [x] Section 3: Directory Structure — **Complete**
- [x] Section 4: Data Flow — **Complete**
- [x] Section 5: Subsystem Reference — **Complete**
- [x] Section 6: State & Data Model *(repurposed)* — **Complete**
- [x] Section 7: Contract & Workflow Inventory *(repurposed)* — **Complete**
- [x] Section 8: API & Integration Points — **Complete**
- [x] Section 9: Configuration & Environment — **Complete**
- [x] Section 10: Error Handling & Recovery — **Complete**
- [x] Section 11: Performance Characteristics — **Complete**
- [x] Section 12: Conventions & Patterns — **Complete**
- [x] Section 13: Extension Guide — **Complete**
- [x] Section 14: Known Limitations & Technical Debt — **Complete**
- [x] Section 15: Verification & Accuracy — **Complete**
- [x] Section 16: Glossary — **Complete**
- [ ] All links verified — **Pending QA**
- [ ] Reviewed by orchestration-platform-team — **Pending**

**Contract Table:**

| Element | Details |
|---------|---------|
| **Dependencies** | FEASIBILITY-STUDY.md, ROADMAP.md, RISK-REGISTER.md, DECISION-SUMMARY.md; research + synthesis files under `TASK-TECHREF-20260603-021348/` |
| **Upstream** | Feeds from: FEASIBILITY-STUDY, research files 01-11, spot-checks 01-04, evidence-index (243 rows), web-01..04 |
| **Downstream** | Feeds to: ROADMAP execution, tasklist generation, port implementation tasks |
| **Change Impact** | Notify: orchestration-platform-team, anyone porting SuperClaude orchestration |
| **Review Cadence** | As-needed (on code-version bump or feasibility-artifact change) |

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [Directory Structure](#3-directory-structure)
4. [Data Flow](#4-data-flow)
5. [Subsystem Reference](#5-subsystem-reference)
   - 5.1 [Existing Pipeline-Core Seam](#51-existing-pipeline-core-seam-code-verified)
   - 5.2 [Roadmap & Tasklist Workflows](#52-roadmap--tasklist-workflows-code-verified)
   - 5.3 [Sprint Execution Runtime](#53-sprint-execution-runtime-code-verified)
   - 5.4 [Reusable Harness Corpus](#54-reusable-harness-corpus-skills--agents--commands--core--templates--hooks--mcp-code-verified)
   - 5.5 [Target Data Model & Ownership](#55-target-data-model--ownership)
   - 5.6 [Adapter / Seam-Replacement Layer](#56-adapter--seam-replacement-layer)
   - 5.7 [External Component Substrate](#57-external-component-substrate-mastra--backlogmd--beads--mcp)
   - 5.8 [Governance / Multi-Tenant Control Plane](#58-governance--multi-tenant-control-plane)
6. [State & Data Model](#6-state--data-model-repurposed-from-state-management)
7. [Contract & Workflow Inventory](#7-contract--workflow-inventory-repurposed-from-component-inventory)
8. [API & Integration Points](#8-api--integration-points)
9. [Configuration & Environment](#9-configuration--environment)
10. [Error Handling & Recovery](#10-error-handling--recovery)
11. [Performance Characteristics](#11-performance-characteristics)
12. [Conventions & Patterns](#12-conventions--patterns)
13. [Extension Guide](#13-extension-guide)
14. [Known Limitations & Technical Debt](#14-known-limitations--technical-debt)
15. [Verification & Accuracy](#15-verification--accuracy-mandatory)
16. [Glossary](#16-glossary)
    - [Appendices](#appendices)
    - [Document History](#document-history)

---

## 1. Overview

> **CRITICAL — PROPOSED, NOT-YET-BUILT ARCHITECTURE.** This document is a *design reference* for a hybrid orchestration architecture that **does not exist in the codebase today**. No source file in the repository implements any Mastra, Backlog.md, or Beads integration as of HEAD `9e864860` `[CODE-VERIFIED]` (absence across full scope, evidence row 5.6-27). The feasibility verdict is **Conditionally Recommended**, with a **spike-first, Option D → Option A** approach: fund a time-boxed validation spike, then proceed to the **hybrid adapter-first** target only if the spike clears its exit gates `[DESIGN — UNBUILT]` (DECISION-SUMMARY.md Verdict, XC-11). Treat every target-architecture statement here as a design intent to be validated, never as shipped behavior.

**What it does (target):** Wraps the existing, runtime-agnostic SuperClaude pipeline kernel (the parts that are BUILT) behind an adapter/seam-replacement layer so that **Mastra** owns durable workflow run/trace state, **Backlog.md** owns the markdown task-of-record, and **Beads** owns the dependency graph + agent memory — turning a single-runtime, Claude-Code-coupled Python orchestrator into a multi-tenant, multi-model orchestration layer `[DESIGN — UNBUILT]` (seed-brief Problem Statement; FEASIBILITY-STUDY §6.1). In the proposed posture, **Python remains the execution oracle** (gates, models, sprint runtime, roadmap pipeline run as-is) while the external substrate is added around it, not in place of it `[DESIGN — UNBUILT]` (XC-02, F2).

**Who uses it:** Engineering teams porting SuperClaude orchestration to a company-wide, multi-tenant, multi-tool substrate, and AI agents that need to understand the seam between BUILT Python and the proposed external stack. The strategic driver is multi-tenancy / multi-user / multi-model orchestration that the current single-`claude`-CLI driver cannot deliver `[CODE-VERIFIED]` (seed-brief Constraints; F8/F10/F11).

**Where it lives (BUILT side):** `src/superclaude/cli/` — specifically the shared kernel `cli/pipeline/` (framework-neutral `models.py`, `executor.py`, `gates.py`, `process.py`, `trailing_gate.py`), plus the `cli/roadmap/`, `cli/tasklist/`, and `cli/sprint/` consumers, and the portable knowledge corpus under `src/superclaude/{skills,agents,commands,core,templates,hooks,mcp}/` `[CODE-VERIFIED]` (`01-pipeline-core-contracts` 5.1-01..5.1-44; `core/CLAUDE.md:17-29`). `src/superclaude/` is the source of truth; `.claude/` is synced dev copies and must not be scraped as primary `[CODE-VERIFIED]` (5.4-01).

**Key numbers:** 8 subsystems (5.1 pipeline-core seam · 5.2 roadmap/tasklist · 5.3 sprint runtime · 5.4 harness corpus · 5.5 target data model · 5.6 adapter layer · 5.7 external substrate · 5.8 governance plane); 3 external tools (Mastra, Backlog.md, Beads); ~20 reused BUILT source files across `cli/pipeline/`, `cli/roadmap/`, `cli/tasklist/`, `cli/sprint/`; portable knowledge corpus of 42 commands / 39 agents / 24 skill packages `[CODE-VERIFIED]` (5.4-16, F6); code baseline HEAD `9e864860`.

### 1.1 Tag Legend (built-vs-design demarcation)

Every architectural claim in this reference carries **exactly one** tag. Never read a `[DESIGN]` claim as built.

| Tag | Meaning | Evidence basis |
|-----|---------|----------------|
| `[CODE-VERIFIED]` | Existing SuperClaude Python that the port **reuses**; real at HEAD `9e864860`. | Real `source path:line` **and** a research/spot-check file. Spot-check `path:line` takes precedence over prior research where they differ (R4). |
| `[DESIGN — UNBUILT]` | The **target** hybrid — Mastra workflows, Backlog/Beads adoption, the adapter layer, the multi-tenant control plane. | FEASIBILITY-STUDY / research synthesis. **Not** integrated code; nothing in the repo implements it yet. |
| `[EXTERNAL-VERIFIED]` | Mastra / Backlog.md / Beads / MCP capability facts. | `web-01`..`web-04` (Tavily/Context7) with source URLs. Capability of the external tool, not a current-repo fact. |

> **Note on a §11 sub-variant:** Section 11 (Performance) additionally uses a `[DESIGN — UNVERIFIED]` sub-variant of `[DESIGN — UNBUILT]`, meaning "measurable in principle but not yet measured because no integrated system exists." It is **not a fourth canonical tag** — it is a performance-section refinement signalling that a metric *could* be benchmarked once the hybrid is built but has no measured value today.

---

## 2. Architecture

### 2.1 High-Level Architecture

The hybrid is a four-band stack. The **BUILT** band (the runtime-agnostic Python kernel + its consumers) is preserved and wrapped; the **adapter/seam-replacement** band, the **external substrate**, and the **governance plane** are all `[DESIGN — UNBUILT]`. The strangler-fig boundary is the single, already-abstracted runtime seam: `StepRunner` / `ClaudeProcess` `[CODE-VERIFIED]` (`pipeline/executor.py:41-60`, `pipeline/process.py:73-95`, spot-01 rows 13-14; F1/F2).

```
  ┌──────────────────────────────────────────────────────────────────────────────────┐
  │  GOVERNANCE / CONTROL PLANE   [DESIGN — UNBUILT]  (NOT in any of the 3 components)  │
  │  tenant registry · 5 identities (trigger/exec/authz/tenant/attribution) · RBAC/ABAC │
  │  tool+skill catalog & change-control · per-invocation audit · cost/budget metering  │
  │  (web-04: MCP is NOT a governance layer; F10/F11; XC-24/5.8-11)                      │
  └───────────────────────────────────────┬──────────────────────────────────────────┘
                                           │ identity / policy / cost context
  ┌────────────────────────────────────────▼─────────────────────────────────────────┐
  │  EXTERNAL SUBSTRATE   [EXTERNAL-VERIFIED capabilities / DESIGN adoption]             │
  │   ┌──────────────┐    ┌──────────────────┐    ┌──────────────────────────────┐      │
  │   │  Mastra      │    │  Backlog.md      │    │  Beads (Dolt-first)          │      │
  │   │  workflows + │    │  markdown task-  │    │  dependency graph + memory + │      │
  │   │  durable run/│    │  of-record (MIT) │    │  ready-queue + gates         │      │
  │   │  trace state │    │  (web-02)        │    │  (web-03; server mode for    │      │
  │   │  (web-01)    │    │                  │    │   multi-writer)              │      │
  │   └──────▲───────┘    └────────▲─────────┘    └──────────────▲───────────────┘      │
  └──────────┼──────────────────────┼─────────────────────────────┼────────────────────┘
             │ run/trace            │ task import/export           │ graph sync / bd ready
  ┌──────────┼──────────────────────┼─────────────────────────────┼────────────────────┐
  │  ADAPTER / SEAM-REPLACEMENT LAYER   [DESIGN — UNBUILT]                                │
  │   StepRunner→Mastra adapter   │  tasklist→Backlog importer  │  Backlog/tasklist→Beads │
  │   (wraps, not replaces, in    │  (round-trip parser-valid)  │  graph sync; results→   │
  │    Phase 1)                   │                             │  Backlog/Beads reconcile│
  │   (XC-13/5.6-04 return-contract.yaml bridges; 5.5-14 adapter contracts)               │
  └──────────────────────────────────────┬───────────────────────────────────────────┘
                                          │  THE SEAM: StepRunner / ClaudeProcess
                                          │  [CODE-VERIFIED] pipeline/executor.py:41-60
  ┌────────────────────────────────────────▼─────────────────────────────────────────┐
  │  BUILT — runtime-agnostic pipeline kernel + consumers   [CODE-VERIFIED] HEAD 9e864860│
  │                                                                                      │
  │   cli/pipeline/  (the shared kernel — stdlib-only, zero sprint/roadmap imports)      │
  │     models.py · executor.py (execute_pipeline) · gates.py (EXEMPT/LIGHT/STD/STRICT)  │
  │     process.py (ClaudeProcess) · trailing_gate.py · deliverables.py                  │
  │     (5.1-01..5.1-44; spot-01)                                                         │
  │             ▲                    ▲                         ▲                          │
  │   cli/roadmap/ (12-step    cli/tasklist/ (validate-   cli/sprint/ (custom phase loop, │
  │   hybrid DAG; 5.2)          only; 5.2-21)              NOT execute_pipeline; 5.3)      │
  │                                                                                      │
  │   Knowledge corpus: skills · agents · commands · core · templates · hooks · mcp      │
  │   (42 cmds / 39 agents / 24 skills — portable markdown; 5.4-16)                       │
  └──────────────────────────────────────────────────────────────────────────────────┘
```

> **Note:** Roadmap and tasklist already consume the shared `execute_pipeline()` + injected `StepRunner`, so they wrap cleanly at the seam `[CODE-VERIFIED]` (5.2-01, 5.2-02, F2). Sprint runs its **own** phase loop and only shares pipeline models/remediation contracts — it needs a supervisory wrapper, not a clean runner swap `[CODE-VERIFIED]` (5.3-11, 5.3-12, F4).

### 2.2 Subsystem Map

The eight subsystems span the BUILT kernel, the proposed adapter layer, the external substrate, and the governance plane. Tags reflect the **dominant** evidence basis of each subsystem (mixed subsystems note both). This table is the table of contents for Section 5.

| # | Subsystem | Purpose | Primary area | Tag |
|---|-----------|---------|--------------|-----|
| 5.1 | Pipeline-core seam | Runtime-agnostic kernel: `Step`/`GateCriteria`/`StepResult` models, `execute_pipeline` sequencer, pure-Python gates, `ClaudeProcess` subprocess seam, trailing gates/remediation. The single strangler-fig boundary. | `cli/pipeline/` (BUILT) | `[CODE-VERIFIED]` (5.1-01..5.1-44) |
| 5.2 | Roadmap / tasklist pipelines | Roadmap 12-step hybrid LLM/deterministic DAG (extract→generate→diff→debate→score→merge→…→remediate) + validation-only tasklist; both reuse `execute_pipeline`. | `cli/roadmap/`, `cli/tasklist/` (BUILT) | `[CODE-VERIFIED]` (5.2-01..5.2-28) |
| 5.3 | Sprint execution runtime | Heaviest surface: custom phase loop, two execution paths, monitors/tmux/TUI, TurnLedger, checkpoints, diagnostics, summaries. Hardest port stress test. | `cli/sprint/` (BUILT) | `[CODE-VERIFIED]` (5.3-01..5.3-34) |
| 5.4 | Harness corpus | Portable knowledge IP: skills, agents, commands, core instruction files, MDTM/document templates, hooks, MCP configs — consumed as instruction packs. | `src/superclaude/{skills,agents,commands,core,templates,hooks,mcp}/` (BUILT) | `[CODE-VERIFIED]` (5.4-01..5.4-20) |
| 5.5 | Target data model & ownership | Current MDTM/Step/status contracts (BUILT) **and** the proposed ownership split (Backlog=prose, Beads=graph, Mastra=run state) + adapter contracts. | BUILT contracts + DESIGN ownership | `[CODE-VERIFIED]` contracts / `[DESIGN — UNBUILT]` ownership (5.5-01..5.5-17) |
| 5.6 | Adapter layer | The proposed seam-replacement: `StepRunner`→Mastra adapter, Backlog importer, Beads graph sync, results reconciliation — modeled on BUILT in-repo portification patterns (cli_portify/prd/cleanup_audit/eval/audit). | DESIGN, grounded in BUILT patterns | `[CODE-VERIFIED]` patterns / `[DESIGN — UNBUILT]` integration (5.6-01..5.6-27) |
| 5.7 | External substrate | Mastra (workflows/trace), Backlog.md (markdown task store), Beads (Dolt-first graph) current capabilities + the narrow `ClaudeProcess` seam they replace. | Mastra / Backlog.md / Beads | `[EXTERNAL-VERIFIED]` capabilities / `[CODE-VERIFIED]` seam (5.7-01..5.7-34) |
| 5.8 | Governance plane | The additional control-plane layer (tenant registry, 5-identity separation, RBAC/ABAC, tool catalog, audit, cost attribution) required for multi-tenant deployment and supplied by none of the 3 components. | DESIGN control plane | `[EXTERNAL-VERIFIED]` requirements / `[CODE-VERIFIED]` current-model gaps (5.8-01..5.8-13) |

### 2.3 Key Design Decisions (As Built / As Proposed)

These are the load-bearing architectural decisions for the proposed hybrid. Each is a design choice (`[DESIGN — UNBUILT]`) justified by a verified property of the BUILT system or external substrate. The "TDD Divergence" column is recast as the verified basis each decision rests on, since this is a feasibility-driven design with no frozen TDD.

| Decision | What is proposed | Rationale | Verified basis / Tag |
|----------|------------------|-----------|----------------------|
| **Strangler-fig replatforming** (not big-bang rewrite) | Wrap the BUILT Python kernel behind adapters and migrate incrementally; start D→A (spike, then hybrid adapter-first), never Option B native TS rewrite. | The orchestration↔runtime coupling is a single already-abstracted seam, and sprint's process/monitor/tmux/checkpoint complexity plus unverified Mastra long-running-supervision parity makes a big-bang rewrite the worst risk/reward. The in-repo cli-portify code-gen-drift history is a direct in-house warning. | `[DESIGN — UNBUILT]` (XC-11, F7; FEASIBILITY-STUDY §6.2/§7.2) |
| **Python-as-oracle parity gating** | Keep the BUILT Python executing as the behavioral source of truth; the adapter/Mastra layer orchestrates and traces but does not re-derive gate/convergence/diagnostic results. Each adapter contract is round-trip parser-validated before ownership transfer. | Gate logic, models, deliverable decomposition, and the diagnostic chain are pure Python with no Claude imports — runtime-agnostic and highly portable; preserving them by construction keeps behavior parity. Native (B) converts this reuse into rewrite-and-re-test, where parity risk concentrates. | `[DESIGN — UNBUILT]` decision over `[CODE-VERIFIED]` basis (F3, 5.1-21, 5.5-14; honesty statement 2) |
| **Single-runtime-seam replacement** | Replace only `StepRunner`/`ClaudeProcess` first (wrap in Phase 1), preserving `execute_pipeline` + gate semantics; translate `Step`/`GateCriteria`/`StepResult`/`PipelineConfig` to Mastra schemas / Beads metadata. | `ClaudeProcess` is the narrow runtime seam reused by sprint/roadmap/tasklist/cli-portify; replacing it is the central replatforming act and is decoupled from the runtime-agnostic core. Spike exit gate SG1 must prove Mastra durable subprocess-supervision parity before this seam is actually replaced. | `[DESIGN — UNBUILT]` (5.7-29, F1; spike gate SG1, XC-12) |

> **Important:** A fourth cross-cutting decision is forced before Phase 1: a **primary work-of-record** choice (Backlog.md vs Beads, decision D1). Backlog.md and Beads overlap as task stores and their mutual integration is immature (Backlog.md FR #588); the recommended split assigns Backlog.md = human-readable prose work-of-record and Beads = dependency graph + memory + ready-queue + gates, with status canonicality on exactly one owner `[EXTERNAL-VERIFIED]` (5.7-17, F9; DECISION-SUMMARY.md honesty statement 4).

### 2.4 Technology Stack (Feature-Specific)

Only the external substrate technologies beyond the existing Python/Click platform are listed. Pin and runtime-verify all three — they move fast (§9.3).

| Technology | Version | Purpose in This Feature | Tag |
|------------|---------|------------------------|-----|
| Mastra (`@mastra/core`) | `1.1.0+` (1.x, fast-moving) | Durable typed workflows + `WorkspaceSandbox` subprocess substrate + observability/traces; proposed run/trace/gate-execution owner | `[EXTERNAL-VERIFIED]` (web-01) |
| Backlog.md | `v1.45.2` (MIT, TS/Bun) | Markdown task store + CLI/TUI/MCP MVP; proposed prose/task/doc/decision owner | `[EXTERNAL-VERIFIED]` (web-02) |
| Beads (`bd`) / Dolt | `v1.x` (`v1.0.5` do-not-upgrade caution) | Dolt-first dependency graph + ready-queue + gates + memory; proposed graph owner; server mode required for multi-agent | `[EXTERNAL-VERIFIED]` (web-03) |

---

## 3. Directory Structure

This section pairs the **existing** orchestration source tree (`[CODE-VERIFIED]`, HEAD `9e864860`) with a **proposed** adapter-layer layout (`[DESIGN — UNBUILT]`). The existing tree is the surface a hybrid port wraps; the proposed layer is additive and does not exist in the repository today.

### 3.1 Existing `src/superclaude/cli/` Orchestration Layout — `[CODE-VERIFIED]`

> **Source:** on-disk listing at HEAD `9e864860` (`ls src/superclaude/cli/{pipeline,roadmap,tasklist,sprint}`); roles per evidence-index 5.1-5.3, spot-01 (pipeline, 80/80 confirmed), RF 01. File counts: pipeline 25, roadmap 26, tasklist 6, sprint 19 `.py` files (`__pycache__` omitted).

```
src/superclaude/cli/                  # Click CLI root; main.py registers sprint/roadmap/
│                                     #   tasklist/cli-portify/prd/eval/cleanup-audit (cli/main.py:400-426)
│                                     #   NOTE: pipeline/ is a shared library package, NOT a root command (5.7-32)
│
├── pipeline/                         # [CODE-VERIFIED] Framework-neutral execution core — THE port seam
│   ├── models.py                     #   Shared dataclasses/enums: Step, StepResult, GateCriteria,
│   │                                 #     PipelineConfig, StepStatus, GateMode (models.py:1-235; 5.1-01..10)
│   ├── executor.py                   #   Generic step sequencer: retry/gates/parallel; StepRunner protocol
│   │                                 #     is the process-boundary seam (executor.py:41-60,63-188; 5.1-11..20)
│   ├── process.py                    #   ClaudeProcess — sole `claude --print` subprocess boundary;
│   │                                 #     SINGLE runtime substitution point (process.py:24-244; spot-01 §seam)
│   ├── gates.py                      #   Pure-Python tiered gate validation, no subprocess (gates.py:1-142; 5.1-21..23)
│   ├── trailing_gate.py              #   Async trailing-gate eval + deferred remediation log (trailing_gate.py:1-648; 5.1-29..36)
│   ├── deliverables.py               #   Behavioral detection + implement/verify decomposition (deliverables.py:1-194; 5.1-37..39)
│   ├── diagnostic_chain.py           #   4-stage deterministic diagnostic assembly (diagnostic_chain.py:1-247; 5.1-40..41)
│   ├── __init__.py                   #   65-symbol public API surface (compatibility anchors) (__init__.py:1-157; 5.1-42)
│   └── guard_*/fmea_*/dataflow_*/    #   Static-analysis passes (guard, FMEA, dataflow, conflict,
│       conflict_*/invariant*/...     #     invariants, mutation, state) — exported via __init__ (5.1-42)
│
├── roadmap/                          # [CODE-VERIFIED] Spec→roadmap pipeline; delegates to execute_pipeline
│   ├── commands.py                   #   `roadmap run` CLI surface + flags (commands.py:32-298; 5.2-03)
│   ├── executor.py                   #   Input routing, step DAG, hybrid Claude/Python steps,
│   │                                 #     resume/convergence (executor.py:74-3187; 5.2-01,04..08)
│   ├── gates.py                      #   All roadmap gate definitions (gates.py:1020-1441; 5.2-13)
│   ├── convergence.py                #   Deviation registry + fidelity convergence cycles (convergence.py:90-668; 5.2-15..16)
│   ├── remediate*.py                 #   Remediation tasklist gen + parallel per-file executor (5.2-17..18)
│   ├── validate_executor.py          #   Auto-invoked roadmap→spec fidelity validation (validate_executor.py:239-519; 5.2-09)
│   └── models.py / prompts.py / ...  #   RoadmapConfig, prompt builders, spec parsers, checkers
│
├── tasklist/                         # [CODE-VERIFIED] Roadmap→tasklist VALIDATION only (no `generate` CLI)
│   ├── commands.py                   #   Exposes ONLY `validate` subcommand (commands.py:31-82; 5.2-21)
│   ├── executor.py                   #   Single tasklist-fidelity step via shared execute_pipeline
│   │                                 #     (executor.py:23-25,191-276; 5.2-02,22)
│   ├── gates.py                      #   TASKLIST_FIDELITY_GATE (gates.py:23-46; 5.2-21)
│   ├── prompts.py                    #   Fidelity prompt + skill-only generator prompt (prompts.py:17-234; 5.2-23..24)
│   └── models.py / __init__.py       #   Tasklist validation config
│                                     #   NOTE: tasklist GENERATION is skill/protocol behavior, not CLI (5.2-24)
│
└── sprint/                           # [CODE-VERIFIED] Phase/task execution runtime (~8,568 lines, 19 files; 5.3-01)
    ├── commands.py                   #   `sprint run/attach/status/logs/kill/verify-checkpoints` (commands.py:15-207; 5.3-02..03)
    ├── config.py                     #   Phase discovery + tasklist parser (THE compat contract) (config.py:15-492; 5.3-04..06)
    ├── models.py                     #   SprintConfig(extends PipelineConfig), TaskEntry, TaskResult,
    │                                 #     PhaseStatus(13), TurnLedger, MonitorState (models.py:24-777; 5.3-07..10,17)
    ├── executor.py                   #   Core loop; TWO paths: Path A per-task / Path B freeform phase
    │                                 #     (executor.py:1135-2148; 5.3-11..16,23)
    ├── process.py                    #   Sprint ClaudeProcess subclass → /sc:task prompt (process.py:88-216; 5.3-13,18)
    ├── monitor.py / tui.py / tmux.py #   NDJSON stream reader, Rich TUI, tmux session (5.3-19..22)
    ├── checkpoints.py                #   Checkpoint extraction/verification/recovery (checkpoints.py:36-408; 5.3-26..27)
    ├── diagnostics.py / summarizer.py#   Failure diagnostics, phase summaries, retrospective (5.3-29..31)
    └── logging_.py / classifiers.py /#   JSONL+MD logs (status/logs read = STUBS, 5.3-28), KPIs, notify
        kpi.py / notify.py / ...      #
```

**Existing-tree key facts (all `[CODE-VERIFIED]`):**

| Fact | Evidence | Tag |
|---|---|---|
| `pipeline/` has zero imports from sprint/roadmap (framework-neutral) | `pipeline/models.py:1-5`, `executor.py:7` (NFR-007); 5.1-01,11 | `[CODE-VERIFIED]` |
| `ClaudeProcess` is the **single** `claude --print` subprocess boundary | `pipeline/process.py:24-244`; spot-01 §seam | `[CODE-VERIFIED]` |
| roadmap/tasklist consume the **shared** `execute_pipeline` + injected `run_step` | `roadmap/executor.py:26`, `tasklist/executor.py:23-25`; 5.2-01..02 | `[CODE-VERIFIED]` |
| sprint reuses shared models/remediation but runs its **own** phase loop | `sprint/executor.py:12-16`; 5.1-43, 5.3-11 | `[CODE-VERIFIED]` |
| `superclaude pipeline` is NOT a root Click command (library only) | `cli/main.py:400-426` vs `pipeline/__init__.py:1-21`; 5.7-32 | `[CODE-VERIFIED]` |

### 3.2 Proposed Adapter-Layer Directory Layout — `[DESIGN — UNBUILT]`

> **CRITICAL:** The tree below **does not exist** in the repository at HEAD `9e864860`. It is a design sketch derived from RF 07 adapter contracts (5.5-14), the verified migration method (5.6-25), and the hybrid/strangler posture (XC-02, XC-11..16). Directory names, module boundaries, and language (TS for Mastra workflows vs Python adapters) are proposals, not commitments.

```
adapters/                             # [DESIGN — UNBUILT] New top-level adapter layer (additive; wraps cli/)
│                                     #   Posture: read-only first → hybrid pilot → parity port (XC-14)
│
├── backlog/                          # [DESIGN] Prose / task / doc / decision owner (Backlog.md)
│   ├── import_tasklist.*             #   Contract 1: tasklist bundle → Backlog markdown import (RF07 Contract 1; 5.5-14)
│   │                                 #     MUST round-trip so discover_phases()/parse_tasklist_file() still pass
│   ├── export_tasklist.*             #   Reconcile Backlog state → tasklist-index.md + phase-N-tasklist.md
│   │                                 #     (preserve T<PP>.<TT> IDs verbatim; 5.5-04, RF07 rule 4)
│   └── schema_map.*                  #   MDTM frontmatter ↔ Backlog Task fields; MCP rejects unknown props (5.7-13)
│
├── beads/                            # [DESIGN] Dependency-graph mirror owner (Beads / Dolt)
│   ├── graph_sync.*                  #   Contract 2: tasklist/Backlog deps → Beads edges (RF07 Contract 2)
│   │                                 #     upsert by stable external ID; propose patch on divergence (5.5-14)
│   ├── gate_bridge.*                 #   Map gate FAIL/HALT → Beads blocker issues; bd gate check (5.7-22)
│   └── ready_claim.*                 #   bd ready + atomic --claim for multi-agent scheduling (5.7-20; XC-16)
│
├── mastra/                           # [DESIGN] Workflow run / trace / gate-execution owner (Mastra, TS)
│   ├── plan_builder.*                #   Contract 3: Backlog+Beads → deterministic Mastra workflow plan (RF07 Contract 3)
│   │                                 #     one workflow/bundle, one stage/phase, T<PP>.<TT> as step ID
│   ├── runner_seam.*                 #   StepRunner adapter: Mastra step → existing ClaudeProcess (hybrid)
│   │                                 #     OR native provider (parity). Substitutes behind executor.py:41-60 seam
│   ├── reconcile.*                   #   Contract 4: Mastra results → Backlog log + Beads status (idempotent) (RF07 Contract 4)
│   └── trace_map.*                   #   Attach R-*/T*/D-*/phase/tier/model as span metadata (5.5-08)
│
├── governance/                       # [DESIGN] Control-plane layer NOT supplied by any of the 3 components (5.8-11)
│   ├── tenant_registry.*             #   tenant / actor / authorization identities — ABSENT from current models (5.5-15)
│   ├── cost_attribution.*            #   Per-tenant token+tool metering (supersedes sprint-local TurnLedger; 5.5-09)
│   └── tool_catalog.*                #   Curated approved-tool/MCP inventory + versioned contracts (5.8-12)
│
└── contracts/                        # [DESIGN] Shared adapter contract + round-trip validation tests
    ├── ids.*                         #   Stable-ID invariants (TASK-*, T<PP>.<TT>, D-####, R-###) (5.5-04)
    ├── roundtrip_tests.*             #   Acceptance gate: import→export must satisfy sprint parser (RF07 §High-Level)
    └── return_contract.yaml          #   Reuse cli_portify return-contract pattern as adapter bridge record (5.6-04)
```

**Proposed-layer design constraints (all `[DESIGN — UNBUILT]` unless noted):**

| Constraint | Source | Tag |
|---|---|---|
| One prose owner (Backlog), one graph owner (Beads), one run owner (Mastra) | RF07 ownership rules 1-3; 5.5-12..13 | `[DESIGN — UNBUILT]` |
| Stable IDs preserved verbatim, never regenerated on import/export | RF07 rule 4; 5.5-04 | `[DESIGN — UNBUILT]` |
| Governance plane is **additional** — none of the 3 components supply tenancy/audit/cost | 5.8-09..11 | `[EXTERNAL-VERIFIED]` |
| Adapters MUST satisfy sprint parser round-trip as acceptance gate | RF07 Contract 1 validation; 5.5-11 | `[DESIGN — UNBUILT]` |
| Runner seam substitutes behind existing `StepRunner` (no second seam class) | `pipeline/executor.py:41-60`; spot-01 §seam | `[CODE-VERIFIED]` (seam) + `[DESIGN]` (adapter) |

### 3.3 File Naming Conventions

| Pattern | Convention | Example | Tag |
|---|---|---|---|
| Existing CLI subpackage | `<surface>/<role>.py` (commands/executor/gates/models/process) | `sprint/executor.py` | `[CODE-VERIFIED]` |
| Existing sprint phase file | `phase-N-tasklist.md` (canonical) + aliases `pN-`, `phase_N_`, `tasklist-pN-` | `phase-1-tasklist.md` | `[CODE-VERIFIED]` (5.3-04) |
| Existing task heading | `### T<PP>.<TT> -- Title` (dash/em-dash) | `### T01.03 -- Build importer` | `[CODE-VERIFIED]` (5.5-11) |
| Proposed adapter module | `<component>/<contract-verb>.<ext>` | `backlog/import_tasklist.py` | `[DESIGN — UNBUILT]` |

---

## 4. Data Flow

### 4.1 Primary Data Flow (Proposed Hybrid) — `[DESIGN — UNBUILT]`

> **CRITICAL:** The end-to-end flow below is a **proposed** hybrid routing. Only the marked **existing seams** (parser, `execute_pipeline`, `ClaudeProcess`, gates, file artifacts) are `[CODE-VERIFIED]`. Every routing hop into Backlog.md / Beads / Mastra is `[DESIGN — UNBUILT]`; all Backlog/Beads/Mastra capabilities consumed are `[EXTERNAL-VERIFIED]` (web-01..04). No integration code exists at HEAD `9e864860` (5.6-27).

```
                          ┌──────────────────────────────────────────────────┐
                          │  SOURCE OF RECORD (EXISTING, file-owned)          │
                          │  MDTM tasklist bundle:                            │  [CODE-VERIFIED]
                          │  tasklist-index.md + phase-N-tasklist.md          │  5.2-25, 5.5-01..04
                          │  ### T<PP>.<TT> -- Title  +  **Dependencies:**    │
                          └───────────────┬──────────────────────────────────┘
                                          │ (A) parse  [CODE-VERIFIED seam]
                                          │ sprint/config.py:374-492 discover_phases/parse_tasklist
                                          v
            ┌─────────────────────────────────────────────────────────────────┐
            │  ADAPTER INGEST (PROPOSED)  [DESIGN — UNBUILT]                    │
            │  Contract 1: tasklist bundle → import (RF07 Contract 1; 5.5-14)   │
            └───────┬─────────────────────────────────────────────┬───────────┘
        (B) prose   │                                  (C) graph   │
        [DESIGN]    v                                  [DESIGN]    v
   ┌────────────────────────────┐               ┌─────────────────────────────────┐
   │ BACKLOG.md                 │   (D) deps    │ BEADS (Dolt graph)              │
   │ PROSE / TASK / DOC OWNER   │──[DESIGN]────>│ DEPENDENCY-GRAPH + GATES OWNER  │
   │ task body, AC, decisions   │   sync deps   │ bd ready / --claim / blockers   │
   │ [EXTERNAL-VERIFIED 5.7-11] │<──patch only──│ [EXTERNAL-VERIFIED 5.7-19..22]  │
   └─────────────┬──────────────┘  (no silent   └────────────────┬────────────────┘
                 │                   md rewrite)                  │
                 │  (E) Backlog + Beads → workflow plan  [DESIGN] │
                 │      Contract 3 (RF07; deterministic dry-run)  │
                 v                                                v
   ┌──────────────────────────────────────────────────────────────────────────┐
   │ MASTRA DURABLE WORKFLOW   RUN / TRACE / GATE-EXECUTION OWNER  [DESIGN]      │
   │ one workflow/bundle, one stage/phase, T<PP>.<TT> = step ID                 │
   │ suspend()/resume() durable snapshots [EXTERNAL-VERIFIED 5.7-01..02]        │
   └───────────────┬───────────────────────────────────────────────────────────┘
                   │ (F) StepRunner adapter  [DESIGN wrapper] over [CODE-VERIFIED seam]
                   │     pipeline/executor.py:41-60 StepRunner protocol
                   v
   ┌──────────────────────────────────────────────────────────────────────────┐
   │ EXECUTION SEAM (EXISTING)  [CODE-VERIFIED]                                 │
   │ HYBRID: Mastra step → existing ClaudeProcess (`claude --print`)           │
   │ pipeline/process.py:24-244 (sole subprocess boundary; spot-01 §seam)      │
   │ → gate_passed() tiered validation  pipeline/gates.py:20-76 (5.1-22)       │
   └───────────────┬───────────────────────────────────────────────────────────┘
                   │ (G) results + gate outcomes
                   v
   ┌──────────────────────────────────────────────────────────────────────────┐
   │ RECONCILE BACK (PROPOSED)  [DESIGN — UNBUILT]                              │
   │ Contract 4 (RF07; idempotent): Mastra results → Backlog log + Beads status│
   │ telemetry/cost → Mastra traces (NOT md/issue bodies)  5.5-08, RF07 C4     │
   └───────────────┬───────────────────────────────────────────────────────────┘
                   │ (H) export round-trip  [DESIGN] — MUST satisfy sprint parser
                   v
   ┌──────────────────────────────────────────────────────────────────────────┐
   │ FILE ARTIFACTS (EXISTING, file-owned)  [CODE-VERIFIED ownership]           │
   │ tasklist-index.md/phase-N-tasklist.md (regenerated), checkpoint reports,  │
   │ execution-log.jsonl/.md, phase-*-result.md  (sprint/models.py:473-510)    │
   └──────────────────────────────────────────────────────────────────────────┘
```

**Flow narrative (hop tags):**

- **(A) Parse** — `[CODE-VERIFIED]`. The sprint parser (`sprint/config.py:374-492`) is the existing, strict ingest contract any adapter must satisfy; markdown tasklists are **ordered execution records**, not active graphs (5.7-31).
- **(B/C) Ingest split** — `[DESIGN — UNBUILT]`. Prose routes to Backlog.md; dependency edges route to Beads (Contract 1, 5.5-14).
- **(D) Backlog↔Beads sync** — `[DESIGN]`. Beads owns the queryable graph but must **propose patches, not silently rewrite** markdown (RF07 rule 2); Backlog/Beads integration is immature (5.7-17, FR #588).
- **(E) Plan build** — `[DESIGN]`. Deterministic Mastra plan from Backlog+Beads (Contract 3); dry-run before side effects (5.6-25 preflight).
- **(F) Runner seam** — `[DESIGN]` wrapper over `[CODE-VERIFIED]` seam. Mastra steps invoke the existing `StepRunner` (`pipeline/executor.py:41-60`); hybrid mode keeps `ClaudeProcess` as execution oracle (RF07 §High-Level rule 4).
- **(G) Execute + gate** — `[CODE-VERIFIED]`. `ClaudeProcess` (`process.py:24-244`) + pure-Python `gate_passed()` (`gates.py:20-76`) remain runner-authored truth (5.7-30).
- **(H) Reconcile + round-trip** — `[DESIGN]`. Idempotent write-back (Contract 4); export MUST round-trip through the parser as the acceptance gate (5.5-11, RF07 Contract 1 validation).

### 4.2 Data Sources

| Source | Type | Location | Description | Tag |
|---|---|---|---|---|
| MDTM tasklist bundle | File (markdown) | `tasklist-index.md` + `phase-N-tasklist.md` | Ordered phases/tasks with `T<PP>.<TT>` IDs + `**Dependencies:**`; current source of record | `[CODE-VERIFIED]` (5.2-25, 5.5-01..04) |
| MDTM task file frontmatter | File (YAML) | `.dev/tasks/.../TASK-*.md` | id/title/status/type/priority/dates/deps/tags | `[CODE-VERIFIED]` (5.5-01) |
| Shared pipeline `Step` | In-memory dataclass | `pipeline/models.py:108-123` | Portable workflow-step contract (id/prompt/output_file/gate/...) | `[CODE-VERIFIED]` (5.5-05) |
| Sprint `TaskEntry` | Parsed dataclass | `sprint/config.py:374-492`, `models.py:24-37` | Task id/title/deps/command/classifier (stores deps, executes in file order) | `[CODE-VERIFIED]` (5.3-06..07) |
| Execution outputs/logs | File | release dir: `execution-log.jsonl/.md`, `phase-*-result.md`, per-task output/error | Runner-authored results, file-owned | `[CODE-VERIFIED]` (5.5-07) |
| Backlog.md task store | External CLI/MCP | `backlog/` dir; MCP stdio | Proposed prose/task/doc owner; MCP rejects unknown props | `[EXTERNAL-VERIFIED]` (5.7-11..13) |
| Beads graph | External CLI (Dolt) | `.beads/` (Dolt-first; JSONL = export only) | Proposed dependency-graph + gate owner; `bd ready`/`--claim` | `[EXTERNAL-VERIFIED]` (5.7-19..23) |
| Mastra workflow store | External runtime (TS) | libSQL/Postgres/etc. storage | Proposed run/trace/gate-execution owner; durable suspend/resume | `[EXTERNAL-VERIFIED]` (5.7-01..05) |
| Tenant/actor/cost identity | (absent) | — | NOT present in current models; must be added by governance plane | `[CODE-VERIFIED]` (absence, 5.5-15) + `[DESIGN]` (5.8-11) |

### 4.3 Data Transformations

Each row marks whether the transformation is an **existing seam** (`[CODE-VERIFIED]`) or **proposed hybrid routing** (`[DESIGN — UNBUILT]`).

| Transformation | Input | Output | Location | Tag |
|---|---|---|---|---|
| Tasklist parse | `phase-N-tasklist.md` text | `Phase` + `TaskEntry` objects (deps, command, classifier) | `sprint/config.py:374-492` (`discover_phases`/`parse_tasklist`) | `[CODE-VERIFIED]` (5.3-04..06) |
| Behavioral decompose | `Deliverable` description | `.a` implement + `.b` verify steps | `pipeline/deliverables.py:146-194` | `[CODE-VERIFIED]` (5.1-39) |
| Step execute | `Step` + `PipelineConfig` | `StepResult` (status/timestamps/remediation) | `pipeline/executor.py:191-399` via `StepRunner` | `[CODE-VERIFIED]` (5.1-15) |
| Subprocess run | prompt (stdin) | stdout→output_file or `.log` sidecar; exit code | `pipeline/process.py:114-157` (`ClaudeProcess`) | `[CODE-VERIFIED]` (5.1-25..27) |
| Gate validation | output file + `GateCriteria` | `(passed, reason)`; `.compressed.md` sidecar preferred | `pipeline/gates.py:20-76`, `executor.py:23-35` | `[CODE-VERIFIED]` (5.1-12,22) |
| Tasklist → Backlog import | tasklist bundle | Backlog task/doc hierarchy (IDs preserved) | `adapters/backlog/import_tasklist.*` (Contract 1) | `[DESIGN — UNBUILT]` (5.5-14, RF07 C1) |
| Deps → Beads graph sync | `TaskEntry.dependencies` | Beads directed edges (upsert by external ID) | `adapters/beads/graph_sync.*` (Contract 2) | `[DESIGN — UNBUILT]` (5.5-14, RF07 C2) |
| Backlog+Beads → Mastra plan | task bodies + graph | deterministic Mastra workflow plan (dry-run) | `adapters/mastra/plan_builder.*` (Contract 3) | `[DESIGN — UNBUILT]` (RF07 C3) |
| Mastra runner seam | Mastra step | invocation of existing `StepRunner`/`ClaudeProcess` | `adapters/mastra/runner_seam.*` over `executor.py:41-60` | `[DESIGN]` wrapper + `[CODE-VERIFIED]` seam |
| Results → reconcile | `StepResult`/gate outcomes | Backlog log rows + Beads status (idempotent) | `adapters/mastra/reconcile.*` (Contract 4) | `[DESIGN — UNBUILT]` (RF07 C4) |
| Export round-trip | reconciled state | regenerated `tasklist-index.md`+`phase-N-tasklist.md` | `adapters/backlog/export_tasklist.*` | `[DESIGN — UNBUILT]` (must pass parser, 5.5-11) |
| Gate FAIL/HALT → blocker | `GateOutcome` FAIL/DEFERRED/HALT | Beads blocker issue + remediation edge | `adapters/beads/gate_bridge.*` (`bd gate check`) | `[DESIGN — UNBUILT]` (5.7-22, RF07 C4) |
| Cost/telemetry attribution | `TurnLedger`/`MonitorState` | per-tenant cost in Mastra traces (not md/issue) | `adapters/governance/cost_attribution.*` | `[DESIGN — UNBUILT]` (5.5-08..09, 5.8-07) |

> **Note:** The transformation chain deliberately keeps **runner-authored truth and gate semantics on the existing seams** (parse → execute → gate → file artifact). The hybrid design adds Backlog/Beads/Mastra as additional owners and routing hops but must not relocate the authoritative gate/result computation, which is pure-Python and runtime-agnostic (5.7-30). A behavioral change — making Beads/Backlog graphs **active** rather than the current ordered execution records — is itself `[DESIGN — UNBUILT]` (5.7-31), not a runtime swap.

---

## 5. Subsystem Reference

> **This is the core of the Technical Reference.** Subsystems 5.1–5.4 document the **existing built subsystems being adapted** (`[CODE-VERIFIED]`, real `path:line` at HEAD `9e864860`). Subsystems 5.5, 5.6, 5.8 are **design** (target architecture, not built). Subsystem 5.7 is **external** (third-party capability). Per the §1.1 demarcation contract, target-stack mappings are called out inline as `[DESIGN — UNBUILT]` and are NEVER presented as built.

### 5.1 Existing Pipeline-Core Seam `[CODE-VERIFIED]`

**Purpose:** The framework-neutral orchestration core (`src/superclaude/cli/pipeline/`) that all higher pipelines reuse: shared dataclass/enum contracts, a generic step sequencer with retry/gates/parallel dispatch, pure-Python gate validation, and the single replaceable subprocess boundary to the Claude CLI. This is the strongest port seam — orchestration, gating, and process execution are already separated behind injectable protocols `[CODE-VERIFIED]`.

**Key Files:**

| File | Purpose |
|------|---------|
| `pipeline/models.py:1-234` | Shared contracts; stdlib-only imports, zero sprint/roadmap imports (`models.py:1-6`, `:8-14`) `[CODE-VERIFIED]` |
| `pipeline/executor.py:1-469` | Generic `execute_pipeline()` sequencer; NFR-007 no sprint/roadmap imports (`executor.py:7`) `[CODE-VERIFIED]` |
| `pipeline/gates.py:1-142` | Pure-Python `gate_passed()` tier validation; no subprocess/LLM (`gates.py:1-10`) `[CODE-VERIFIED]` |
| `pipeline/process.py:1-244` | `ClaudeProcess` — THE runtime seam; sole `subprocess.Popen` (`process.py:134`) `[CODE-VERIFIED]` |
| `pipeline/trailing_gate.py:1-648` | Async gate eval, deferred-remediation log, scope-based mode resolution `[CODE-VERIFIED]` |
| `pipeline/deliverables.py:1-194` | Heuristic implement/verify decomposition `[CODE-VERIFIED]` |
| `pipeline/__init__.py:1-157` | 65-symbol public API surface (`__all__`, compatibility anchors) `[CODE-VERIFIED]` |

**How It Works:**

`execute_pipeline(steps, config, run_step, ...)` accepts `list[Step | list[Step]]`; a nested list is a parallel group (`executor.py:63-188`, sig `:63-72`). The executor owns ordering, retry, gates, cancellation, and state callbacks; it never spawns a subprocess directly — all execution is delegated to the injected `StepRunner` callable (`executor.py:41-60`). This injection point is the migration seam.

Per step, `_execute_single_step()` (`executor.py:191-399`) runs a retry loop and branches on gate mode `[CODE-VERIFIED]`:

```
run_step()  ──►  StepResult re-wrapped w/ attempt (executor.py:230-238)
   │
   ├─ no gate ............. trust runner status (:240-243)
   ├─ TIMEOUT/CANCELLED ... return without gate check (:245-248)
   ├─ TRAILING ........... submit to runner, return PASS immediately (:250-262)
   └─ BLOCKING ........... gate_passed(_gate_target(out), step.gate) (:264-278)
                              │ fail → cosmetic remediation (:280-364)
                              │      → retry if attempt<max (:375-376)
                              └      → terminal FAIL (:378-388)
```

`_gate_target()` (`executor.py:23-35`) prefers a sibling `.compressed.md` sidecar over the original output — gates validate what the downstream LLM actually consumes. Trailing-gate machinery (`trailing_gate.py`) is **advisory** in current code: at pipeline end, pending trailing results are collected with timeout `max(30.0, grace_period)` and failures are logged as warnings only, never converted to failed `StepResult`s (`executor.py:175-186`) `[CODE-VERIFIED]`.

`gate_passed()` (`gates.py:20-76`) enforces four tiers: EXEMPT always passes (`:28-30`); LIGHT requires existence + non-empty (`:41-43`); STANDARD adds min_lines + required frontmatter (`:45-60`); STRICT adds semantic checks short-circuiting on first non-`True` (`:65-74`). The frontmatter parser scans delimiter pairs anywhere (tolerates preamble) and matches top-level keys via regex rather than deep YAML (`gates.py:79-142`) `[CODE-VERIFIED]`.

**`ClaudeProcess` — THE replaceable runtime seam.** `ClaudeProcess` (`process.py:24-244`) is the sole concrete boundary to the `claude` CLI in the pipeline package: it is the only class that builds a `claude --print` argv (`build_command()`, `process.py:73-95`) and the only one that calls `subprocess.Popen` — at **`process.py:134`** (spot-01 confirmed). The prompt is delivered via stdin to dodge Linux `MAX_ARG_STRLEN` (`process.py:76-78`, `:136-139`); `wait()` returns exit code `124` on timeout to match bash semantics (`process.py:165`); `terminate()` escalates SIGTERM→10s→SIGKILL→5s on the process group (`process.py:173-214`) `[CODE-VERIFIED]`. Gates and trailing-gate code are pure-Python (no subprocess), so they are **not** a runtime seam. Replacing `ClaudeProcess` behind the `StepRunner` protocol is therefore the single substitution point to swap the Claude-CLI runtime.

**Public Interface (key signatures):**

```python
# models.py — portable contracts
class StepStatus(Enum): PENDING|PASS|FAIL|TIMEOUT|CANCELLED|SKIPPED   # is_failure ⇔ FAIL|TIMEOUT only (:64-66)
class GateMode(Enum): BLOCKING | TRAILING                              # (:69-78)
@dataclass GateCriteria(required_frontmatter_fields, min_lines, enforcement_tier, semantic_checks)  # (:90-105)
@dataclass Step(id, prompt, output_file, gate, timeout_seconds, inputs, retry_limit, model, gate_mode, tool_write_mode, template_path)  # (:108-122)
@dataclass StepResult(step, status, attempt, gate_failure_reason, started_at, finished_at, remediated, remediations)  # (:125-148)
@dataclass PipelineConfig(work_dir, dry_run, max_turns, model, permission_flag='--dangerously-skip-permissions', debug, grace_period=0, ...)  # (:212-234)

# executor.py — orchestration seam
class StepRunner(Protocol): def __call__(step, config, cancel_check) -> StepResult   # (:41-60)
def execute_pipeline(steps: list[Step|list[Step]], config, run_step, on_step_start=None, on_step_complete=None, ...) -> list[StepResult]  # (:63-188)

# gates.py — deterministic validation
def gate_passed(output_file: Path, criteria: GateCriteria) -> tuple[bool, str|None]   # (:20-76)

# process.py — THE runtime seam
class ClaudeProcess:  # (:24-244)  sole subprocess.Popen at :134
    def build_command(self) -> list[str]            # (:73-95)  claude --print --verbose <perm> --no-session-persistence --tools default --max-turns N --output-format <fmt>
    def start(self) -> subprocess.Popen             # (:114-157)
    def wait(self) -> int                           # (:159-171)  124 on timeout
```

**Dependencies:**

| Depends On | Type | Description |
|------------|------|-------------|
| `claude` CLI binary | subprocess | Spawned by `ClaudeProcess` only (`process.py:134`) `[CODE-VERIFIED]` |
| Python stdlib | import | `models`/`gates`/`trailing_gate` import only stdlib + pipeline-local (`models.py:8-14`, `gates.py:12-17`) `[CODE-VERIFIED]` |
| Filesystem | I/O | Output artifacts, `.compressed.md` sidecars, `.log` sidecars (tool_write_mode) `[CODE-VERIFIED]` |

**Consumers:**

| Used By | How |
|---------|-----|
| Roadmap (§5.2) | Generic `execute_pipeline` + injected `roadmap_run_step` (`roadmap/executor.py:25-35`) `[CODE-VERIFIED]` |
| Tasklist validate (§5.2) | `execute_pipeline` + `tasklist_run_step` (`tasklist/executor.py:23-25`, `:259-263`) `[CODE-VERIFIED]` |
| Roadmap validate | `execute_pipeline` + `ClaudeProcess` runner (`validate_executor.py:105-180`) `[CODE-VERIFIED]` |
| Sprint (§5.3) | Reuses `Step`/`StepResult`/`DeferredRemediationLog`/`TrailingGateResult` but runs its **own** phase loop, not `execute_pipeline` (`sprint/executor.py:12-16`) `[CODE-VERIFIED]` |

**Conventions & Patterns:**

- Gate validation targets the `.compressed.md` sidecar when present, NOT the raw output (`executor.py:23-35`, `trailing_gate.py:146-155`) `[CODE-VERIFIED]`. A roadmap comment claiming "gates run on the ORIGINAL output file" (`roadmap/executor.py:1217-1219`) is STALE/CODE-CONTRADICTED — feeds §14 (D6).
- Trailing-gate failures are advisory (warning-only) and do not alter returned status (`executor.py:175-186`) `[CODE-VERIFIED]`.
- `grace_period == 0` coerces a declared TRAILING step to BLOCKING (`executor.py:212-214`) `[CODE-VERIFIED]` — see §5.2 wiring-gate note and §14 L2.
- **`[DESIGN — UNBUILT]`** Port mapping: `Step`/`GateCriteria`/`StepResult`/`PipelineConfig` → Mastra workflow schema + Backlog.md/Beads task metadata; replace only `StepRunner`/`ClaudeProcess` first, preserving executor + gate semantics. `DeferredRemediationLog` → Beads durable ledger. Claude-specific `permission_flag`/`--tools default` must stay in a runner-side adapter config, not the portable orchestration model. Feasibility per research file 01 §4/§8; not implemented.

---

### 5.2 Roadmap & Tasklist Workflows `[CODE-VERIFIED]`

**Purpose:** The two highest-level generative/validation pipelines that consume the §5.1 core. Roadmap turns a spec/TDD/PRD into roadmap artifacts via a 12-element step DAG whose gates are registered in the 14-entry `ALL_GATES` table (`roadmap/gates.py:1426-1441`); tasklist exposes validation-only fidelity checking. Both prove the `StepRunner` seam by injecting their own runner into the generic `execute_pipeline` `[CODE-VERIFIED]`.

**Key Files:**

| File | Purpose |
|------|---------|
| `roadmap/executor.py:1947-2208` | `_build_steps()` — the wired 12-element roadmap DAG `[CODE-VERIFIED]` |
| `roadmap/executor.py:2985-3187` | `execute_roadmap()` — routing, resume, compression, shared-pipeline dispatch `[CODE-VERIFIED]` |
| `roadmap/gates.py:1020-1441` | All roadmap gate definitions (`ALL_GATES` reference list at `:1440`) `[CODE-VERIFIED]` |
| `roadmap/commands.py:32-298` | CLI `run` surface + flags `[CODE-VERIFIED]` |
| `tasklist/executor.py:92-218` | `tasklist_run_step()` pilot runner + single-step `_build_steps()` `[CODE-VERIFIED]` |
| `tasklist/gates.py:23-46` | `TASKLIST_FIDELITY_GATE` (sole gate of validation pipeline) `[CODE-VERIFIED]` |

**How It Works:**

`execute_roadmap()` routes 1–3 inputs (`detect_input_type()` scores PRD→TDD→spec; `roadmap/executor.py:74-335`), restores resume state from `.roadmap-state.json`, compresses, then calls `execute_pipeline(steps, config, roadmap_run_step, ...)` (dispatch `:3124-3131`). The wired DAG from `_build_steps()` (`roadmap/executor.py:1947-2208`) is, in order (spot-02 CONFIRMED):

```
extract → [generate-A, generate-B] (parallel) → diff → debate → score →
merge → anti-instinct → test-strategy → spec-fidelity → wiring-verification →
deviation-analysis → remediate
```

Step execution is **hybrid**: most steps launch `ClaudeProcess`, but anti-instinct / convergence-spec-fidelity / deviation-analysis / remediate / wiring-verification run deterministic Python (`roadmap/executor.py:955-1250`). The adversarial workflow (diff→debate→score→merge) is wired inline in the executor — it does NOT call the `sc-adversarial-protocol` skill (`roadmap/executor.py:2068-2128`). After a run, validation auto-invokes single-agent `reflect` (REFLECT_GATE) or multi-agent `reflect-{agent}` + `adversarial-merge` (`validate_executor.py:239-519`) `[CODE-VERIFIED]`.

**Spot-check-confirmed gate facts (feed §14):**

- **CERTIFY_GATE UNWIRED.** `CERTIFY_GATE` is defined (STRICT tier, 5 frontmatter fields) at `roadmap/gates.py:1324-1351` and listed in `ALL_GATES` at `gates.py:1440`, but no `certify` Step is appended in `_build_steps()` (terminates at `remediate`, `:2196-2204`). The comment "Step 12 (certify) constructed dynamically by `roadmap_run_step` after remediate" (`executor.py:2205`) is **unbacked**: `build_certify_step`/`check_certify_resume` have zero production callsites (spot-02 CONFIRMED). Defined-only gap (§14 L1).
- **WIRING_GATE TRAILING coerced to BLOCKING.** The `wiring-verification` Step declares `gate_mode=GateMode.TRAILING` (`roadmap/executor.py:2183`) but `PipelineConfig.grace_period` defaults to `0` (`pipeline/models.py:232`) and `_execute_single_step` coerces `grace_period == 0` → BLOCKING (`pipeline/executor.py:213-214`). So wiring-verification runs **synchronously/blocking** in production despite the trailing intent (spot-02 CONFIRMED; §14 L2).
- **Docstring staleness.** `_build_steps` docstring still says "9-step pipeline" (`executor.py:1948`) vs the 12 wired elements; two steps share a "Step 8" comment label (`:2140`, `:2157`). Cosmetic only; ordering unaffected (§14 D4).
- **Deviation classifier UNWIRED.** All deviation records render as UNCLASSIFIED; `DEVIATION_ANALYSIS_GATE` pins the `unclassified_count == total_analyzed` invariant (`executor.py:1603-1609`, `gates.py:1390-1422`) `[CODE-VERIFIED]` (§14 L4).

**Tasklist pilot.** The tasklist CLI exposes **only** a `validate` subcommand (no `generate`) (`tasklist/commands.py:31-82`). `_build_steps()` builds exactly one `tasklist-fidelity` Step gated by `TASKLIST_FIDELITY_GATE` (STRICT, 6 frontmatter fields, min_lines 20, 2 semantic checks) over `[roadmap.md] + tasklist_files (+ optional TDD/PRD)` (`tasklist/executor.py:191-218`, gate `tasklist/gates.py:23-46`). The pilot-port runner `tasklist_run_step()` (`tasklist/executor.py:92-188`) is a compact `ClaudeProcess` runner (inline input embedding, cancellation polling, timeout `124`→TIMEOUT, non-zero→FAIL, output sanitize) — the cleanest single-step seam to port first. CLI pass/fail is computed **independently** of the gate: `execute_tasklist_validate` runs the pipeline then parses `high_severity_count` from report frontmatter, returning failure on any HIGH severity or missing report (`tasklist/executor.py:221-276`). Tasklist GENERATION is skill/protocol behavior (`build_tasklist_generate_prompt`, used by `/sc:tasklist`), NOT a CLI subcommand (`tasklist/prompts.py:151-234`) `[CODE-VERIFIED]`.

**Public Interface (key signatures):**

```python
# roadmap/executor.py
def _build_steps(config, ...) -> list[Step | list[Step]]                 # (:1947-2208) 12-element DAG
def execute_roadmap(config, ...) -> RoadmapResult                         # (:2985-3187)
def roadmap_run_step(step, config, cancel_check) -> StepResult            # ClaudeProcess + deterministic-Python hybrid

# tasklist/executor.py
def tasklist_run_step(step, config, cancel_check) -> StepResult           # (:92-188) pilot-port runner
def execute_tasklist_validate(config) -> bool                            # (:251-276) pass ⇔ no HIGH-severity
```

**Dependencies:**

| Depends On | Type | Description |
|------------|------|-------------|
| §5.1 pipeline-core | import | `execute_pipeline`, `Step`, `StepResult`, `StepStatus`, `ClaudeProcess` (`roadmap/executor.py:25-35`) `[CODE-VERIFIED]` |
| `.roadmap-state.json` | file | Resume state: spec hash, input type, step statuses, validation/fidelity/certify status (`roadmap/executor.py:2627-2682`) `[CODE-VERIFIED]` |
| `roadmap/convergence.py` | import | `DeviationRegistry`, fidelity-with-convergence cycles (`:90-207`, `:434-668`) `[CODE-VERIFIED]` |

**Consumers:**

| Used By | How |
|---------|-----|
| `/sc:roadmap`, `superclaude roadmap run` | CLI front door (`roadmap/commands.py:32-298`) `[CODE-VERIFIED]` |
| `/sc:tasklist` validate, `superclaude` tasklist validate | Validation-only pipeline `[CODE-VERIFIED]` |
| Sprint (§5.3) | Consumes tasklist-format output (index + phase files) `[CODE-VERIFIED]` |

**Conventions & Patterns:**

- `SPEC_FIDELITY_GATE` is wired only in `--no-convergence` mode; convergence mode replaces it with deterministic pass/fail from `_run_convergence_spec_fidelity` (`executor.py:2158-2173`, `:994-1001`) `[CODE-VERIFIED]`.
- Sprint-compatible tasklist output (N+1 files, literal phase filenames, `T<PP>.<TT>` IDs, checkpoints) is **protocol-specified, not CLI-enforced** (`sc-tasklist-protocol/SKILL.md:91-123`) `[DESIGN — UNBUILT]` (skill spec, no CLI generator).
- **`[DESIGN — UNBUILT]`** Mastra-workflow mapping: the linear+parallel DAG maps to Mastra fan-out/fan-in nodes; per-step gates → Mastra validation steps; `roadmap_run_step` hybrid (LLM vs deterministic) → mix of Mastra agent steps and pure workflow steps. The single-step `tasklist-fidelity` runner is the recommended **first** port candidate. Beads can own the deviation registry / remediation state. Feasibility per research file 02; not implemented.

---

### 5.3 Sprint Execution Runtime `[CODE-VERIFIED]`

**Purpose:** The supervised multi-phase execution engine (`src/superclaude/cli/sprint/`, 19 files / ~8,568 lines) that runs a tasklist bundle phase-by-phase, supervising Claude subprocesses with monitors, watchdogs, checkpoints, diagnostics, and tmux/TUI. It is the **hardest port surface** — a deliberate acceptance stress test, not the first rewrite candidate `[CODE-VERIFIED]`.

**Key Files:**

| File | Purpose |
|------|---------|
| `sprint/executor.py:1135-1757` | `execute_sprint()` core loop (file is 2,148 lines) `[CODE-VERIFIED]` |
| `sprint/commands.py:15-32`, `:189` | `sprint` Click group; `run()` orchestration entry `[CODE-VERIFIED]` |
| `sprint/config.py:275-492` | Phase discovery + `parse_tasklist()` `[CODE-VERIFIED]` |
| `sprint/models.py:347-510` | `SprintConfig(PipelineConfig)`, `PhaseStatus` (13 values: 2 transient PENDING/RUNNING + 11 result states), `TurnLedger` `[CODE-VERIFIED]` |
| `sprint/process.py:88-216` | Sprint `ClaudeProcess` subclass + Path B prompt builder `[CODE-VERIFIED]` |
| `sprint/checkpoints.py:22-408` | Checkpoint path/heading parsing, manifest, recovery `[CODE-VERIFIED]` |
| `sprint/monitor.py:253-571` | `OutputMonitor` stream-json reader + stall/exhaustion detectors `[CODE-VERIFIED]` |

**How It Works:**

`execute_sprint(config)` (`sprint/executor.py:1135-1757`) preflights the `claude` binary, installs signal handlers, builds TUI/monitor/`SprintResult`, starts a summary worker, constructs `TurnLedger` / `ShadowGateMetrics` / `DeferredRemediationLog` / `SprintGatePolicy` (`:1228-1234`), runs python-mode preflight phases, then iterates active phases. `SprintConfig` **extends** `PipelineConfig` (`models.py:347-510`), so it inherits the §5.1 contracts but runs its own phase loop rather than `execute_pipeline` `[CODE-VERIFIED]`.

**Two execution paths** (`sprint/executor.py:1259-1457`) `[CODE-VERIFIED]`:

```
phase ──► _parse_phase_tasks()
            │
            ├─ tasks present → PATH A (per-task)            (:1259-1301)
            │     execute_phase_tasks() → one subprocess per TaskEntry
            │     aggregate task statuses → continue  ◄── ends at :1301
            │
            └─ freeform (no headings) → PATH B               (:1303-1457)
                  isolation dir + OutputMonitor + ClaudeProcess
                  poll + stall watchdogs → _determine_phase_status() (:1502)
                  if PASS → _verify_checkpoints()  ◄── sole call site :1519
```

**Subprocess supervision.** Sprint's `ClaudeProcess` (`sprint/process.py:88-121`) subclasses the generic pipeline process and delegates lifecycle to `pipeline.process.ClaudeProcess` — it reuses the §5.1 seam, adding a sprint prompt. Path B builds a rich prompt invoking `/sc:task Execute all tasks in @<phase_file> --compliance strict --strategy systematic` plus sprint context, checkpoint-before-result ordering, and an `EXIT_RECOMMENDATION: CONTINUE|HALT` sentinel (`sprint/process.py:123-216`). Path A builds only a minimal task prompt and writes **task-specific** output/error files (`config.task_output_file/task_error_file`, `executor.py:1098-1108`). `OutputMonitor` reads stream-json NDJSON in a daemon thread; runtime watchdogs use CLI-configured `--stall-timeout`/`--startup-stall-timeout` thresholds, with `stall_action=kill` mapping the phase to exit `124` (`monitor.py:253-396`). `_determine_phase_status()` (`executor.py:2067-2148`) is the authoritative classifier combining exit code + result-file freshness + prompt-too-long detection + checkpoint inference `[CODE-VERIFIED]`.

**Spot-check-confirmed facts (feed §14):**

- **Path A skips checkpoint verification.** The Path A branch (`executor.py:1262-1301`) aggregates task results and `continue`s at `:1301` with no checkpoint call. The **sole** `_verify_checkpoints()` invocation is `executor.py:1519`, inside Path B after the `status == PASS` guard at `:1517` (definition at `:1811`). Checkpoint enforcement therefore does NOT run for parsed-task phases (spot-03 CONFIRMED; §14 L3).
- **Numbered-checkpoint contract.** `CHECKPOINT_HEADING_PATTERN` (`checkpoints.py:30-33`) accepts BOTH numbered `### T<PP>.<TT> -- Checkpoint:` and legacy `### Checkpoint:` via an optional regex group; `Checkpoint Report Path:` is matched by `CHECKPOINT_PATH_PATTERN` (`checkpoints.py:22-25`). The runtime parser is dual-shape compatible. Stale legacy-only `### Checkpoint:` text remains in the Path B prompt (`process.py:188-195`) and the `verify-checkpoints` empty message (`commands.py:426`) — stale-but-harmless (§14 D1/D2).
- **`sprint rerun-tasks` is ABSENT at HEAD.** A tree-wide grep for `rerun-tasks`/`rerun_tasks` returns zero matches; the `sprint` Click group registers exactly six subcommands — `run`, `attach`, `status`, `logs`, `kill`, `verify-checkpoints` (`commands.py:71/293/305/317/342/360`). The operator-memory note of a v4.3.0 `sprint rerun-tasks` does NOT correspond to anything at commit `9e864860` (package is v4.2.0). **Do not describe `rerun-tasks` as existing** (spot-03 RESOLVED; §14 L8). Closest extant recovery surface is `verify-checkpoints` (recovers checkpoint reports only, does not re-run tasks).
- **Partial/unused isolation.** Four-layer `IsolationLayers`/`setup_isolation` exists (`executor.py:106-182`) but is NOT called in the main loop; Path B sets only `CLAUDE_WORK_DIR`, Path A passes no isolation env (`executor.py:1303-1324`, `:1076-1115`) `[CODE-VERIFIED]` (§14 L5).
- **Path A turn-accounting gap.** `_run_task_subprocess` returns `turns_consumed=0` (turn counting wired separately), limiting `TurnLedger` accuracy for Path A (`executor.py:1111-1115`) `[CODE-VERIFIED]` (§14 L7).
- **Stubbed status/logs.** `SprintLogger` JSONL+Markdown writes are real, but `read_status_from_log`/`tail_log` are stubs ("not yet connected"), so the `status`/`logs` commands do not report live (`logging_.py:224-235`) `[CODE-VERIFIED]` (§14 L6).

**Public Interface (key signatures):**

```python
# sprint/executor.py
def execute_sprint(config: SprintConfig) -> SprintResult                  # (:1135-1757)
def execute_phase_tasks(phase, tasks, config, ledger, ...) -> list[TaskResult]  # (:927-1073) Path A
def _determine_phase_status(...) -> PhaseStatus                            # (:2067-2148)
def _verify_checkpoints(...) -> PhaseStatus                                # (:1811) Path-B only call at :1519

# sprint/models.py
class PhaseStatus(Enum): PENDING|RUNNING|PASS|PASS_NO_SIGNAL|PASS_NO_REPORT|PASS_RECOVERED|PREFLIGHT_PASS|
                          PASS_MISSING_CHECKPOINT|INCOMPLETE|HALT|TIMEOUT|ERROR|SKIPPED  # 13 values (:211-270)
@dataclass SprintConfig(PipelineConfig): release_dir, state_dir, checkpoint_gate_mode, ...  # (:347-510)
```

**Dependencies:**

| Depends On | Type | Description |
|------------|------|-------------|
| §5.1 pipeline-core | import/inherit | `SprintConfig(PipelineConfig)`; reuses `Step`/`StepResult`/`DeferredRemediationLog`/`TrailingGateResult` (`sprint/executor.py:12-16`) `[CODE-VERIFIED]` |
| Tasklist bundle | file | Index + `phase-N-tasklist.md` files; `PHASE_FILE_PATTERN` (`config.py:15-26`) `[CODE-VERIFIED]` |
| `tmux`, Rich | external | Optional `sc-sprint-<sha1>` session + `SprintTUI` Live render (`tmux.py:81-210`, `tui.py:98-152`) `[CODE-VERIFIED]` |
| `claude` CLI | subprocess | Via sprint `ClaudeProcess` → base `subprocess.Popen` (`pipeline/process.py:134`) `[CODE-VERIFIED]` |

**Consumers:**

| Used By | How |
|---------|-----|
| `superclaude sprint run` | CLI orchestration entry (`commands.py:189`) `[CODE-VERIFIED]` |
| `manifest.json` / `execution-log.jsonl` | End-of-sprint artifacts (`executor.py:1702-1725`) `[CODE-VERIFIED]` |

**Conventions & Patterns:**

- Result-file sentinels (`EXIT_RECOMMENDATION: CONTINUE|HALT`, `status: PASS|FAIL|PARTIAL`) are authoritative control-plane evidence, not backlog metadata (`executor.py:1774-1808`) `[CODE-VERIFIED]`.
- Checkpoints are a filesystem protocol embedded in markdown tasklists (path declarations + manifest), not a database (`checkpoints.py:36-408`) `[CODE-VERIFIED]`.
- **`[DESIGN — UNBUILT]`** Port posture is **hybrid-first** (hardest port surface): keep the Python sprint runner as execution authority; evaluate Mastra as a supervisory/workflow layer and Backlog.md/Beads as task-state/dependency mirrors. Mastra agent-approval does not replace process-group lifecycle, file-tail watchdogs, tmux IPC, or stream-json telemetry; a faithful port must preserve deterministic phase/task discovery, result-file freshness, checkpoint manifest, process-group termination, and exit-code propagation. Per-task vs freeform Path A/B divergence should be normalized or consciously preserved before adding a framework. Feasibility per research file 03 §8; not implemented.

---

### 5.4 Reusable Harness Corpus (Skills / Agents / Commands / Core / Templates / Hooks / MCP) `[CODE-VERIFIED]`

**Purpose:** The harness corpus is the body of **instruction IP** — slash commands, agents, skill packages, core framework files, MDTM/document templates, hooks, and MCP configs — that encodes SuperClaude's orchestration discipline as natural-language protocol rather than as runtime code. In a Mastra+Backlog.md+Beads port this corpus is the *most portable and most reusable* asset: it is runtime-agnostic prose that any host capable of invoking Claude (or another model) can drive. `[CODE-VERIFIED]`

**Key Files / Components** (counts confirmed at HEAD `9e864860` per `spot-04-harness.md`; raw `*.md` directory counts include each directory README):

| Asset class | Count (HEAD `9e864860`) | Canonical location | Role in a port |
|---|---|---|---|
| Slash commands | **42** `*.md` (41 command defs + 1 README) | `src/superclaude/commands/` | Thin front-door manifests: parse flags, validate inputs, invoke skills; no embedded execution loops. `[CODE-VERIFIED]` (`commands/task.md:156-162`, `roadmap.md:82-92`) |
| Agents | **39** `*.md` (38 agent defs + 1 README) | `src/superclaude/agents/` | Role-prompt corpus (rf-team-lead, rf-task-researcher, rf-qa, rf-qa-qualitative, etc.). `[CODE-VERIFIED]` (`agents/rf-team-lead.md:36-48`) |
| Skill packages | **24** (each a dir with exactly one `SKILL.md` + refs/rules/templates/scripts) | `src/superclaude/skills/` | Main reusable instruction body (sc-task, task, task-builder, sc-tasklist, sc-cli-portify, …). `[CODE-VERIFIED]` (`skills/task/SKILL.md:83-105`) |
| Core instruction files | **12** `*.md` (+ `__init__.py`) | `src/superclaude/core/` | CLAUDE.md, COMMANDS.md, ORCHESTRATOR.md, MCP.md, RULES.md, FLAGS.md, MODES.md, PERSONAS.md, PRINCIPLES.md, RESEARCH_CONFIG.md, BUSINESS_*. `[CODE-VERIFIED]` (`core/MCP.md:269-304`, `RULES.md:5-82`) |
| Workflow templates | 8 | `src/superclaude/templates/workflow/` | MDTM generic (996 lines) + complex (1,204 lines) task templates with granular/self-contained constraints. `[CODE-VERIFIED]` (`01_mdtm_template_generic_task.md:1-159`) |
| Document templates | 7 | `src/superclaude/templates/documents/` | PRD, TDD, technical_reference, etc. — this document's own template lives here. `[CODE-VERIFIED]` |
| Hooks | `hooks.json` (2,110 B) + 9 scripts | `src/superclaude/hooks/` | Registers SessionStart/UserPromptSubmit/PreToolUse/PostToolUse/SubagentStart/SubagentStop; freshness-pre-edit, reject-workspace-writes, session-context injection. `[CODE-VERIFIED]` (`hooks/hooks.json:1-95`) |
| MCP assets | 11 MCP docs + 11 JSON configs | `src/superclaude/mcp/` | tavily/auggie/serena/sequential launch configs + circuit-breaker/fallback table. `[CODE-VERIFIED]` (`mcp/configs/*.json`, `core/MCP.md:269-304`) |

**How It Works:**

The corpus is layered. Slash commands are **thin manifests** that parse flags and delegate to skills — they do not embed the execution loop (`commands/task.md:156-162`, `tasklist.md:70-84`, `roadmap.md:82-92`, `adversarial.md:143-149`). Skill packages carry the actual behavioral protocol: e.g. the generic MDTM `task` skill runs an F1 loop (read first unchecked item → execute exactly → mark complete → repeat), explicitly prohibits delegating the loop, and supports parallel agent spawning for independent items (`skills/task/SKILL.md:83-105`, `110-123`, `371-373`). `task-builder` (2,190 lines) orchestrates scope discovery → parallel researchers → QA gates → builder → structural+qualitative validation, writing to `.dev/tasks/to-do/` (`skills/task-builder/SKILL.md:108-162`). Agents are role prompts addressed by an orchestration vocabulary (rf-team-lead dispatches rf-task-researcher/builder/executor via message vocabulary + task prefixes; `agents/rf-team-lead.md:79-103`). Core files (ORCHESTRATOR.md detection/complexity/domain matrices, MCP.md server selection + circuit breakers, RULES.md verification-before-recommendation) are the global instruction substrate the skills reference. `[CODE-VERIFIED]`

A crucial portability property: this corpus assumes **Claude Code tool semantics** (Skill / Task / Glob / Grep / TodoWrite / TeamCreate / SendMessage). Any non-Claude-Code host must supply an adapter vocabulary that maps these tool invocations onto the new runtime (`agents/rf-team-lead.md:79-103`). `[CODE-VERIFIED]` An in-repo precedent for converting inference workflows into deterministic CLI pipelines already exists — `/sc:cli-portify` + `sc-cli-portify-protocol` (component inventory → step graph → gates → executor/workflow spec) — and is the natural reuse seam for porting (`commands/cli-portify.md:20-91`, `sc-cli-portify-protocol/SKILL.md:12-28`). `[CODE-VERIFIED]`

**Dependencies:**

| Depends On | Type | Description |
|---|---|---|
| Claude Code tool runtime | Tool vocabulary | Skill/Task/Glob/Grep/TodoWrite/TeamCreate/SendMessage are assumed; a port must adapt them. `[CODE-VERIFIED]` (`agents/rf-team-lead.md:79-103`) |
| `src/superclaude/` canonical tree | Source-of-truth | Per `core/CLAUDE.md:17-29,45-48`, edit `src/` first then `make sync-dev`; `.claude/` are synced dev copies. `[CODE-VERIFIED]` |
| MCP servers (tavily/auggie/serena/sequential) | External tools | Skills reference MCP per `core/MCP.md` circuit-breaker table; strict-tier blocking on unavailability. `[CODE-VERIFIED]` (`core/MCP.md:269-304`) |

**Consumers:**

| Used By | How |
|---|---|
| Pipeline runtimes (sprint / roadmap / tasklist) | Sprint Path B prompt invokes `/sc:task ... --compliance strict --strategy systematic`; roadmap/tasklist steps deliver skill-defined prompts. `[CODE-VERIFIED]` (`sprint/process.py:123-216`) |
| A future Mastra step runner | Would deliver the same skill/agent prompts through a Mastra step instead of `ClaudeProcess`. `[DESIGN — UNBUILT]` (see 5.6) |

**Conventions & Patterns:**

- **`src/superclaude/` is canonical; `plugins/superclaude/` is a divergent mirror — do NOT scrape the mirror as primary.** At HEAD `9e864860`, `plugins/superclaude/` is git-tracked but materially out of sync: 30 commands / 20 agents / **1** skill / 6 core files vs `src/`'s 42 / 39 / 24 / 12. `diff -qr` reports many `Only in src` commands (adversarial, auggie-review, cleanup-audit, cli-portify, release-split, review-translation, roadmap) and many differing shared files. The plugin-tree READMEs ("edit `plugins/superclaude/` first") are a stale v5-transition artifact, not operative policy. `[CODE-VERIFIED]` (`spot-04-harness.md` (c); `core/CLAUDE.md:45-48` vs `commands/README.md:13-23`) (§14 D3)
- **READMEs are stale and must not be used for counts.** `commands/README.md` lists 5 command files (dir has 42); `agents/README.md` lists 3 (dir has 39). `[CODE-VERIFIED]` (`commands/README.md:5-11`, `agents/README.md:5-10`)
- **Slash commands stay thin; behavior lives in skills.** Never push an execution loop into a command manifest. `[CODE-VERIFIED]`
- **Dependency gap to flag, not invent:** `/sc:forensic` is invoked by the TFEP escalation in `sc-task-protocol/SKILL.md:181-261` but no such command/skill exists in the inventory — a real unverified dependency a port must resolve. `[CODE-VERIFIED]`

---

### 5.5 Target Data Model & Ownership

> **CRITICAL:** This subsystem is **`[DESIGN — UNBUILT]`**. No source file in the repository implements any Backlog.md / Beads / Mastra integration today. The current-code contracts cited below as `[CODE-VERIFIED]` are the *existing* models the design must preserve; the ownership split, join semantics, and adapter targets are *proposed architecture*, not built behavior.

**Purpose:** Define a single, drift-resistant ownership model for the hybrid stack so that prose, dependency graph, and run/trace state each have exactly one source of truth, joined by stable IDs. The design exists to prevent the central failure mode of a three-store stack: two systems both believing they own task status or dependencies, silently diverging until execution order changes. `[DESIGN — UNBUILT]`

**Key Components — three model groups** (current representation is `[CODE-VERIFIED]`; the target owner is `[DESIGN — UNBUILT]`):

| Model Group | Current representation (HEAD `9e864860`) | Proposed target owner | Tag |
|---|---|---|---|
| **A. Prose / task / doc / decision concepts** | MDTM markdown w/ YAML frontmatter (id/title/status/type/priority/dates/deps/tags) + ordered checklist phases; handoff artifacts in task subdirs | **Backlog.md** (prose owner) | current `[CODE-VERIFIED]` (`02_mdtm_template_complex_task.md:1-44`, `394-430`, `718-731`); target `[DESIGN — UNBUILT]` |
| **B. State / status / telemetry / quality signals** | StepStatus / TaskStatus / GateOutcome / SprintOutcome enums; `MonitorState` high-volume telemetry; `TurnLedger` budget; execution-log.jsonl / phase-*-result.md / per-task output files | **Mastra** (run/trace/gate-execution owner) | current `[CODE-VERIFIED]` (`pipeline/models.py:40-67`, `sprint/models.py:39-124`, `622-690`, `692-777`); target `[DESIGN — UNBUILT]` |
| **C. Tasklist-generation & sprint-parser contract** | phase-file name aliases, Execution Mode (claude/python/skip), `### T<PP>.<TT> -- Title` headings, `**Dependencies:**`/`**Command:**` extraction, release-dir resolution | **Beads** (dependency graph) + Backlog.md (visible dep text) | current `[CODE-VERIFIED]` (`sprint/config.py:15-26`, `67-119`, `374-492`, `236-272`); target `[DESIGN — UNBUILT]` |

**How It Works (proposed):**

The design splits **work-of-record** along two axes: **Backlog.md owns prose** (human-readable task body, acceptance criteria, checklist instructions, decisions) while **Beads owns the graph + gates** (normalized dependencies, ready-queue, external gates). **Mastra owns run/trace state** (retries, step status, model/provider calls, traces) — but only after a validation phase proves its durability/replay/observability; until then, current Python result files remain the source of truth. `[DESIGN — UNBUILT]`

The **join key** across all three stores is the set of **stable IDs** that already exist verbatim in current file formats and parsers: `TASK-*`, `T<PP>.<TT>`, `D-####` (deliverable), `D-CP…` (checkpoint deliverable), `R-###` (roadmap item). These are `[CODE-VERIFIED]` as current IDs (`sc-tasklist-protocol/SKILL.md:161-164`, `441-487`; `sprint/config.py:374-377`); their use as a cross-system reconciliation key is `[DESIGN — UNBUILT]`. The ownership matrix below is the proposed boundary:

| Data / artifact class | Current owner | Proposed target owner | Mirror owners | Sync direction |
|---|---|---|---|---|
| Human task body / AC / decisions | `.dev/tasks` markdown | Backlog.md | Mastra trace links, Beads metadata | Backlog.md → adapters |
| Machine dependency graph (`depends_on`, `Txx.yy` edges) | frontmatter + `**Dependencies:**` text | Beads | Backlog.md retains visible text; Mastra reads for scheduling | Backlog.md/tasklist → Beads |
| Workflow run state / retries / step status / traces | Python dataclasses / process outputs | Mastra | Backlog.md summaries; Beads status updates | Mastra → Backlog/Beads summaries |
| Logs / checkpoint reports / validation reports | files under release/task workspace | Backlog.md docs or artifact files w/ Mastra trace refs | Beads links only | files → Backlog docs; Beads stores pointers |
| Gate definitions / enforcement tiers | Python models + skill protocols | Mastra (execution) + Backlog.md (policy docs) | Beads fail/remediation issues | Backlog policy → Mastra config |
| Stable IDs / traceability | markdown / tasklist generator | shared cross-system IDs; Backlog.md assigns/preserves canonical | Mastra + Beads store as metadata | Backlog/tasklist → all |
| Multi-tenant auth / RBAC / cost | **absent** beyond `TurnLedger` budget | unresolved — governance service (see 5.8) | — | undetermined (gated on governance-plane decision, §5.8) |

*(All target-owner cells `[DESIGN — UNBUILT]`; "current owner" and "absent" cells `[CODE-VERIFIED]` per `pipeline/models.py`, `sprint/models.py` read ranges.)*

**Dependencies:**

| Depends On | Type | Description |
|---|---|---|
| Stable-ID contract | Current code fact | IDs must already exist and be parseable — they do (`sprint/config.py:374-377`). `[CODE-VERIFIED]` |
| Sprint parser compatibility | Current code constraint | Any adapter writing tasklists must satisfy `discover_phases()` / `parse_tasklist_file()` (see 5.6 Contract 1). `[CODE-VERIFIED]` (`sprint/config.py:399-492`) |
| Backlog.md schema | External | Target prose fields constrained by Backlog.md `Task` schema (see 5.7). `[EXTERNAL-VERIFIED]` |

**Consumers:**

| Used By | How |
|---|---|
| Adapter / seam-replacement layer (5.6) | Adapters read/write each store per the ownership matrix. `[DESIGN — UNBUILT]` |
| Governance plane (5.8) | Adds tenant/actor/audit identity that the matrix's bottom row leaves unresolved — **NOT PROVIDED by any of Mastra / Backlog.md / Beads; must be built net-new.** `[DESIGN — UNBUILT]` |

**Conventions & Patterns (ownership rules to preserve):**

- **One prose owner, one graph owner, one run owner.** Backlog.md (prose) / Beads (graph) / Mastra (run). Mirrors link or summarize; they never fork the canonical copy. `[DESIGN — UNBUILT]`
- **Stable IDs are non-negotiable.** Every adapter preserves current IDs verbatim and never regenerates them on import/export. `[DESIGN — UNBUILT]`
- **Checkpoint reports remain artifacts.** A checkpoint is both a task node and a report body; never conflate the two. `[DESIGN — UNBUILT]`
- **Tenant/actor/audit identity is ABSENT today.** `PipelineConfig`/`SprintConfig`/`TaskResult`/`PhaseResult`/`MonitorState`/`TurnLedger` carry model/permission/budget but **no** tenant or actor field — governance dimensions must be added, not assumed. `[CODE-VERIFIED]` (absence; `sprint/models.py:692-777`)
- **Known current-code conflict to carry forward, not silently fix:** `sc-tasklist-protocol/SKILL.md:343-391` specifies numbered `### T<PP>.<NN> -- Checkpoint:` tasks, but the extracted `phase-template.md:101-125` still documents sibling `### Checkpoint:` sections, and sprint `build_prompt()` (`sprint/process.py:187-195`) still instructs scanning for the sibling form. Adapters must emit the **numbered** form for sprint compatibility. `[CODE-VERIFIED]` (doc-contradicted; §14 D1)

---

### 5.6 Adapter / Seam-Replacement Layer

> **CRITICAL:** This subsystem is **`[DESIGN — UNBUILT]`**. No source file implements Mastra/Backlog.md/Beads integration. The reusable orchestration *patterns* cited as `[CODE-VERIFIED]` are existing in-repo precedents (cli_portify, prd, cleanup_audit, eval, audit) that the adapter design draws on; the four adapter contracts and the Mastra-step/CLI-shell-out hybrid are *proposed*.

**Purpose:** Define the thin translation layer that lets the existing Python orchestration and instruction corpus drive — and be driven by — the external substrate without a big-bang rewrite. The adapter layer is where the "hybrid, adapter-first" strategy lives: it wraps the one narrow runtime seam (`ClaudeProcess` / `StepRunner`) and adds four data adapters that move task/graph/run state between stores. `[DESIGN — UNBUILT]`

**Key Components — the four adapter contracts:** `[DESIGN — UNBUILT]`

| # | Adapter contract | Direction | Validation contract |
|---|---|---|---|
| **1** | Tasklist bundle → Backlog.md import | tasklist files → Backlog prose | Import must export back such that `discover_phases()` + `parse_tasklist_file()` succeed and counts match `count_tasks_in_file()`. |
| **2** | Backlog.md / tasklist → Beads graph sync | prose/IDs → Beads issues+edges | Graph export must reproduce a dependency list identical to parser-extracted `TaskEntry.dependencies` unless a human-approved patch exists. |
| **3** | Backlog.md / Beads → Mastra workflow plan | task+graph → Mastra plan | Plan generation must be deterministic and produce a dry-run plan (task order, gates, expected artifacts, provider commands) before execution. |
| **4** | Mastra run results → Backlog.md + Beads reconciliation | run state → prose+graph updates | Reconciliation must be idempotent (re-applying the same result is a no-op). |

*(All four `[DESIGN — UNBUILT]`, sketched in `07-target-data-model-and-ownership.md` Contracts 1-4; each maps onto current models — Contract 4 maps `StepStatus.PASS`/`TaskStatus.FAIL`/`GateOutcome.DEFERRED` which are `[CODE-VERIFIED]` at `pipeline/models.py:40-67`, `sprint/models.py:39-124`.)*

**How It Works (proposed):**

The **central replatforming act** is replacing the runtime seam. Today `ClaudeProcess` constructs `claude --print --verbose <perm> --no-session-persistence --tools default --max-turns N --output-format <fmt>`, delivers the prompt over **stdin** (not argv, to avoid Linux `MAX_ARG_STRLEN`), maps timeout→exit 124, and tears down the process group SIGTERM→SIGKILL (`pipeline/process.py:73-95`, `97-112`, `159-214`). `[CODE-VERIFIED]` The executor owns retry/gates/ordering while the runner owns subprocess+timeout, joined by the `StepRunner` protocol `__call__(step, config, cancel_check) -> StepResult` (`pipeline/executor.py:41-60`). `[CODE-VERIFIED]` In the target design **a Mastra step becomes the `StepRunner`**: `execute_pipeline()` (which already accepts an injected `run_step`, proven by roadmap/validate/tasklist consumers at `roadmap/executor.py:26`, `tasklist/executor.py:259-263`) would receive a Mastra-backed runner instead of `ClaudeProcess`. `[CODE-VERIFIED]` (seam exists) / `[DESIGN — UNBUILT]` (Mastra runner).

The **CLI shell-out hybrid** is the lower-risk first move: rather than reimplement gate/convergence/diagnostic logic (which is pure runtime-agnostic Python — `gates.py` imports only `re`/`Path`/`GateCriteria` at `pipeline/gates.py:1-17`), the adapter calls the existing `superclaude` CLI as a subprocess from a Mastra step, preserving runner-authored truth and gate semantics while gaining Mastra's durable orchestration shell. `[CODE-VERIFIED]` (Python portability) / `[DESIGN — UNBUILT]` (shell-out wrapper).

In-repo precedents the adapter design reuses (all `[CODE-VERIFIED]`): **cli_portify** emits a `return-contract.yaml` on every path (outcome/completed_steps/remaining_steps/suggested_resume_budget/resume_command) — a ready-made bridge record for Backlog/Beads (`cli_portify/executor.py:283-372`); its deterministic output classification (timeout→TIMEOUT, exit0+marker+artifact→PASS, artifact-no-marker→PASS_NO_SIGNAL) is the model for Contract 4 (`cli_portify/executor.py:224-257`). **prd** demonstrates tier-sized parallel fan-out + QA→fix→re-QA loops (`prd/executor.py:862-958`, `963-1047`). **eval** demonstrates HOME-dir isolation with a three-check containment guard and a retry-once policy (`eval/isolation.py:224-260`, `eval/retry.py:41-165`) — directly relevant to safe subprocess parity. **audit** demonstrates content-hash caching, atomic checkpoint writes, and calibrated validation that explicitly states self-agreement is *not* ground-truth correctness (`audit/validation.py:42-151`). The verified migration method: single typed graph as SoT → attach artifact/gate contracts → preflight before side effects → run with isolation+supervision → persist → QA/convergence loops → calibrated validation → retire duplicated resume/review matrices. `[CODE-VERIFIED]` (synthesis)

**Dependencies:**

| Depends On | Type | Description |
|---|---|---|
| `StepRunner` / `execute_pipeline` seam | Current code | The injection point a Mastra runner plugs into. `[CODE-VERIFIED]` (`pipeline/executor.py:41-60`, `63-188`) |
| Target data model (5.5) | Design | Adapters move state per the ownership matrix. `[DESIGN — UNBUILT]` |
| Mastra `createStep` / Workspace | External | Step + subprocess substrate the runner targets (see 5.7). `[EXTERNAL-VERIFIED]` |
| Backlog.md CLI/MCP, Beads `bd --json` | External | Mutation interfaces for Contracts 1-4. `[EXTERNAL-VERIFIED]` |

**Consumers:**

| Used By | How |
|---|---|
| Harness corpus (5.4) | Skills/agents are delivered through the new step runner unchanged. `[DESIGN — UNBUILT]` |
| Sprint/roadmap/tasklist runtimes | Their injected `run_step` is swapped for the adapter runner. `[DESIGN — UNBUILT]` |

**Conventions & Patterns:**

- **Contract-first, gated, resumable, source-verified.** The cli_portify evolution is the cautionary precedent: early code-gen/spec-drift failed; the contract-first/gated pattern became the safe one — favoring strangler/hybrid over big-bang. `[CODE-VERIFIED]` (synthesis)
- **Preserve runner-authored truth.** Current orchestration is artifact/gate-centric: Python owns sequencing/retry/halt/state/gates, Claude fills structured content. A Mastra port must re-host that division, not just re-host prompts. `[CODE-VERIFIED]` (`pipeline/gates.py`, `executor.py`)
- **Start read-only.** First adapters import existing `.dev/tasks` and tasklist bundles into target metadata *without changing current files*; add round-trip parser tests before any ownership transfer. `[DESIGN — UNBUILT]`
- **Reconciliation must be idempotent** (Contract 4) so retries/replays do not double-apply status or duplicate remediation issues. `[DESIGN — UNBUILT]`
- **DRIFT hazards to carry forward, not silently fix:** cli_portify `resume.py` legacy matrix uses conceptual step names that contradict the live `STEP_REGISTRY` (`resume.py:45-95` vs `executor.py:105-183`); cleanup_audit docstring claims ThreadPoolExecutor parallelism but executes sequentially (`cleanup_audit/executor.py:11-13`). A port must retire these duplicated matrices, not replicate them. `[CODE-VERIFIED]` (contradicted; §14 D7/D8)

---

### 5.7 External Component Substrate (Mastra / Backlog.md / Beads / MCP)

> **Note:** Every fact in this subsystem is **`[EXTERNAL-VERIFIED]`** — a third-party capability sourced via Tavily/Context7 web research (web-01..web-04), **not** a SuperClaude code fact. Inline URLs are the provenance. These describe what the substrate *can* do today; whether SuperClaude *uses* them is `[DESIGN — UNBUILT]` (5.5/5.6).

**Purpose:** Document the current, externally-verified capabilities and risks of the three substrate components plus MCP, so the design (5.5/5.6/5.8) rests on what these tools actually provide rather than on the seed brief's assumptions (several of which are corrected below). `[EXTERNAL-VERIFIED]`

**Mastra** (runtime / workflow / observability) `[EXTERNAL-VERIFIED]`

| Capability | Detail | Source URL |
|---|---|---|
| Durable workflows | `suspend()`/`resume()`/`resumeStream()`; snapshots persist across deploys/restarts; resume from a specific step ID; runners = built-in, Inngest, Temporal (Temporal **experimental/not prod-ready**) | https://mastra.ai/docs/workflows/suspend-and-resume ; https://mastra.ai/docs/deployment/workflow-runners |
| Typed step pipelines | `createWorkflow()`/`createStep()` w/ input/outputSchema; steps call functions/APIs/agents/tools/workflows; workflows deterministic vs agents probabilistic | https://mastra.ai/docs/workflows/overview |
| Workspace subprocess | `WorkspaceSandbox` (`executeCommand`/start/stop/destroy, timeouts, stdout/stderr/wait, `maxRetainedBytes`), added `@mastra/core@1.1.0` — **NOT proven parity** with Claude Code hook/permission model | https://mastra.ai/reference/workspace/sandbox |
| Storage | libSQL/Turso, PostgreSQL, MongoDB, Redis/Upstash, DynamoDB, MSSQL, ClickHouse, Cloudflare; `MastraCompositeStore` routes domains; in-memory resets | https://mastra.ai/docs/memory/storage ; https://mastra.ai/reference/storage/composite |
| Observability / Studio | auto-instruments agent runs/LLM gens/tool calls/workflow steps (tokens, model params); Studio visualizes graphs/traces/MCP servers; 1.0 schema entityId/entityType/entityName | https://mastra.ai/docs/observability/tracing/overview ; https://mastra.ai/docs/studio/overview |
| Auth / RBAC / EE (**key risk**) | Auth optional (Studio/API public without it); providers Simple/JWT/Auth0/Better/Clerk/Firebase/Okta/Supabase/WorkOS; **RBAC/FGA tied to Enterprise Edition** (`@mastra/core/auth/ee`, StaticRBACProvider, WorkOS FGA); dual license Apache-2.0 core + Mastra EE for `ee/` dirs | https://mastra.ai/docs/server/auth ; https://mastra.ai/pricing |
| MCP | `MCPClient` (stdio/HTTP/SSE) + `MCPServer` (expose agents/tools/workflows over HTTP); `requireToolApproval` HITL; FGA enforcement for MCP tool execution | https://mastra.ai/docs/mcp/overview |
| Deployment | `mastra dev/build/start`, `server deploy`; Hono-based server, Express/Hono/Fastify/Koa adapters; agents/workflows → REST + OpenAPI; Platform Organizations = multi-tenant containers | https://mastra.ai/docs/server/mastra-server ; https://mastra.ai/docs/mastra-platform/overview |

> **Important:** Mastra's risk is **parity/governance, not capability**: Claude Code hook parity is NOT established; workflow rerun/replay/idempotency needs hands-on validation; Temporal is experimental; Backlog/Beads are not native concepts. `[EXTERNAL-VERIFIED]` (https://mastra.ai/docs, synthesis)

**Backlog.md** (markdown-native work-of-record) `[EXTERNAL-VERIFIED]`

| Capability | Detail | Source URL |
|---|---|---|
| Core | markdown task store (`backlog/` dir), CLI + TUI board + browser UI + fuzzy search + docs + decisions + MCP; MIT; **v1.45.2**; TypeScript/Bun | https://github.com/MrLesk/Backlog.md ; .../package.json |
| Task schema | rich first-class fields (id/title/status/assignee/reporter/dates/labels/milestone/dependencies/references/documentation/modifiedFiles/description/implementationPlan/Notes/finalSummary/AC/DoD/parent-subtasks/priority/branch/ordinal) | https://raw.githubusercontent.com/MrLesk/Backlog.md/main/src/types/index.ts |
| MCP constraint (**key**) | MCP task schemas use `additionalProperties:false` — **arbitrary SuperClaude metadata cannot be added as MCP fields**; must use supported fields / body sections / docs or extend | https://raw.githubusercontent.com/MrLesk/Backlog.md/main/src/mcp/tools/tasks/schemas.ts |
| MCP MVP | current MCP is a minimal stdio surface (`task_*`/`milestone_*`/`definition_of_done_*`/`document_*`); decision tools are CLI-only, not MCP; contradicts older "75+ tools" claims | https://raw.githubusercontent.com/MrLesk/Backlog.md/main/src/mcp/README.md |
| Git optional | `backlog init --no-git` = filesystem-only; `autoCommit` default false; remoteOperations/bypassGitHooks/filesystemOnly config | https://raw.githubusercontent.com/MrLesk/Backlog.md/main/ADVANCED-CONFIG.md |
| Maturity limits | local-file/git-centric, **not** a centralized multi-user transactional PM backend (`proper-lockfile`; one-task-per-agent discipline); no built-in sprint/roadmap pipeline; Beads integration immature (FR #588); browser state-loss bug #578 | https://github.com/MrLesk/Backlog.md/issues/588 ; .../issues/578 |

**Beads** (Dolt-backed dependency graph) `[EXTERNAL-VERIFIED]`

| Capability | Detail | Source URL |
|---|---|---|
| Core | `gastownhall/beads` "distributed graph issue tracker for AI agents, powered by Dolt"; npm `@beads/bd`, PyPI `beads-mcp`; high churn (~24.3k stars, 227 open issues) | https://github.com/gastownhall/beads |
| CLI | `bd ready` (unblocked), `bd create`, `bd update --claim` (atomic assignee+in_progress), `bd dep add`, `bd show`, `bd prime` (context+memories), `bd remember`; always `--json` | https://github.com/gastownhall/beads ; SETUP.md |
| Dependency / gate semantics | blocking (blocks/parent-child/conditional-blocks/waits-for) + non-blocking annotations; cycles rejected at write; **gates** bridge to external state (`gh:pr`/`gh:run`/`timer`/`bead`/`human`) | https://github.com/gastownhall/beads/blob/main/docs/DEPENDENCIES.md |
| Storage (**corrects seed brief**) | **Dolt-first** (version-controlled SQL, cell-level merge, branching); `.beads/issues.jsonl` is **export/interchange only**, NOT canonical sync — corrects the "SQLite + JSONL" framing | https://github.com/gastownhall/beads/blob/main/docs/SYNC_CONCEPTS.md ; .../DOLT.md |
| Deployment modes | embedded (default, in-process Dolt, single-writer, solo) vs server (`dolt sql-server`, concurrent writers, `bd init --server`) — **server REQUIRED for multi-agent** | https://github.com/gastownhall/beads/blob/main/docs/DOLT.md |
| JSON contract | `--json` stable (schema v1); `BD_JSON_ENVELOPE=1` opts into uniform envelope (planned v2.0 default); legacy lists=raw arrays | https://github.com/gastownhall/beads/blob/main/docs/JSON_SCHEMA.md |
| Version caution (**pin**) | v1.0.5 pre-release/gated ("do not upgrade"; migration 0043 can break multi-machine sync, #4259); v1.0.4 server data-clobber regression — pin + gate versions | https://github.com/gastownhall/beads/releases ; .../issues/3870 |

**How It Works (relationship to the design):** The substrate provides three complementary stores that map onto the 5.5 ownership split — Mastra for run/trace (durable workflows + observability), Backlog.md for prose (markdown task/doc/decision records), Beads for graph (typed dependencies + ready-queue + gates). That substrate-capability mapping is `[EXTERNAL-VERIFIED]` (web-01..web-03). The narrow current seam they would replace is `ClaudeProcess` at `pipeline/process.py:73-147` `[CODE-VERIFIED]`. Markdown tasklists are currently **ordered execution records, not active dependency graphs** — sprint parses deps but executes in document order at `sprint/config.py:379-384` `[CODE-VERIFIED]` — so adopting Beads graph semantics is a *behavioral change*, not a runtime swap.

**Dependencies:** Each component is independently deployable; Backlog.md↔Beads integration is **not mature** (FR #588, maintainer suggests narrow import/export sync first — https://github.com/MrLesk/Backlog.md/issues/588). `[EXTERNAL-VERIFIED]`

**Consumers:** The adapter layer (5.6) is the sole intended consumer; nothing in the current repo consumes any of these today. `[DESIGN — UNBUILT]`

**Conventions & Patterns:**

- **Pin and gate versions** for all three (Mastra `@core` 1.1.0+, Backlog.md 1.45.2 MVP, Beads 1.x churn); runtime-verify schemas because docs drift. `[EXTERNAL-VERIFIED]`
- **Mutate via CLI/MCP, not hand-edited files** for Backlog.md (keeps field types consistent) and Beads (`--json`, never read legacy JSONL directly). `[EXTERNAL-VERIFIED]`
- **Server mode is mandatory for any multi-agent writer** scenario in Beads; embedded is solo-only. `[EXTERNAL-VERIFIED]`
- **Production RBAC/SSO/FGA/audit/on-prem are Mastra Enterprise-licensed**, not Apache-2.0 core — a gating commercial decision for multi-tenant deployment. `[EXTERNAL-VERIFIED]`

---

### 5.8 Governance / Multi-Tenant Control Plane

> **CRITICAL:** This subsystem is **`[DESIGN — UNBUILT]`** and is specifically **NOT PROVIDED by any of Mastra / Backlog.md / Beads — it must be built net-new.** It is the net-new layer that **none of the three components supplies** and that the current SuperClaude code does not contain. It is not "unbuilt SuperClaude work" in the sense of a planned SuperClaude feature; it is a category of capability that must be sourced or built separately before any company-wide multi-tenant deployment. External governance facts carry `[EXTERNAL-VERIFIED]` with URLs; current-code absence carries `[CODE-VERIFIED]`.

**Purpose:** Establish that a Mastra+Backlog.md+Beads stack — even fully integrated — is **not** a complete multi-tenant platform, and enumerate the governance/control-plane layer (identity, tenant isolation, policy, tool catalog, audit, cost/budget attribution, approvals) that must sit above the substrate. The subsystem exists to prevent the dangerous assumption that MCP or any single component is a governance layer. This layer is **NOT PROVIDED by any of Mastra / Backlog.md / Beads — it must be built net-new.** `[DESIGN — UNBUILT]`

**Key Components — the missing layer** (**NOT PROVIDED by any of Mastra / Backlog.md / Beads — must be built net-new**): `[DESIGN — UNBUILT]`

| Control-plane capability | Why none of the 3 components supplies it | Source URL |
|---|---|---|
| Tenant registry + isolation | Mastra Organizations are containers, not full tenant governance; Backlog.md is repo-local; Beads is project-scoped | https://github.com/MrLesk/Backlog.md ; https://github.com/gastownhall/beads |
| Identity mapping (5 identities) | Multi-tenant agents need **separate** trigger / execution / authorization / tenant / attribution identities; access-control bugs surface silently when execution+tenant are conflated; config-driven RBAC, not inferred from user messages | https://www.scalekit.com/blog/access-control-multi-tenant-ai-agents |
| RBAC/ABAC policy store | Mastra production RBAC/FGA is Enterprise-licensed, not core | https://mastra.ai/pricing |
| Tool/skill catalog + change control | Enterprise MCP needs a curated approved catalog with versioned contracts, staging, consumer tracking, review-like-code, rollback | https://tray.ai/blog/mcp-security-governance-enterprise |
| Audit log (per-invocation) | record caller identity/session, tool name+version+schema, inputs, target, outcome, policy decision, approval, cost, correlation ID | https://labs.cloudsecurityalliance.org/agentic/agentic-mcp-security-best-practices-v1 |
| Cost / rate / budget attribution | FinOps: cost attribution is a governance-layer concern outside MCP; meter model tokens + tool calls by tenant/team/user/agent/workflow/task | https://www.finops.org/wg/model-context-protocol-mcp-ai-for-finops-use-case |
| Approval engine + env separation | progressive elevation via `WWW-Authenticate`, approval gates for higher-risk actions, environment separation/rollout controls | https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices |

**How It Works (why MCP is NOT the governance layer):**

The decisive point: **MCP is a narrow integration protocol — host/client/server tool-resource exchange — and explicitly does NOT define enterprise governance.** Authorization is *optional* in MCP; it focuses on context exchange and does not dictate who acts, when, or under what conditions (https://modelcontextprotocol.io/docs/concepts/architecture). `[EXTERNAL-VERIFIED]` (web-04 #1) Where MCP authorization *is* used for enterprise, it is OAuth 2.1-based (PRM, resource indicators, audience binding, token validation), and **token passthrough is explicitly forbidden** because it breaks accountability/audit and enables exfiltration — downstream services need separate tokens + attribution, not forwarded credentials (https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices). `[EXTERNAL-VERIFIED]` (web-04 #2, #3) Official MCP guidance itself warns of multi-tenant/realm mix-ups, generic audiences, session-ID-as-auth, and broad scopes — confirming MCP needs an API-management/control-plane layer above it, analogous to early REST. `[EXTERNAL-VERIFIED]` (web-04 #4, #7, #10)

Consequently the three components are an **orchestration/task substrate, not the complete platform**: Mastra is runtime/workflow/MCP/observability (NOT a full tenant-governance/policy/budget/approval/catalog/cost plane); Backlog.md and Beads are task/memory substrates with no cross-tenant IAM, enterprise audit, rate limiting, or cost attribution. `[EXTERNAL-VERIFIED]` (web-04 #13, #14, #15) A Mastra+Backlog.md+Beads port therefore needs an **additional** governance/control-plane layer before company-wide multi-tenant deployment. `[EXTERNAL-VERIFIED]` (web-04 #11, synthesis)

**Dependencies:**

| Depends On | Type | Description |
|---|---|---|
| Target data model (5.5) | Design | Governance adds the tenant/actor/audit identity the ownership matrix leaves unresolved — **NOT PROVIDED by any of Mastra / Backlog.md / Beads; must be built net-new.** `[DESIGN — UNBUILT]` |
| Mastra observability | External (telemetry source) | Mastra traces can *feed* the governance plane (join traces with Backlog.md/Beads IDs) but do not *constitute* it. `[EXTERNAL-VERIFIED]` (web-04 #8) |

**Consumers:** All orchestration actions in a multi-tenant deployment would route policy/identity/audit/cost decisions through this layer — a layer **NOT PROVIDED by any of Mastra / Backlog.md / Beads; it must be built net-new.** `[DESIGN — UNBUILT]`

**Conventions & Patterns:**

- **MCP is not a governance platform.** Never delegate identity/policy/audit/cost to MCP alone. `[EXTERNAL-VERIFIED]` (web-04 #1)
- **Five separate identities.** Keep trigger / execution / authorization / tenant / attribution distinct; never conflate execution and tenant. `[EXTERNAL-VERIFIED]`
- **No token passthrough; granular scopes only.** Map command/skill privileges to least-privilege tool-level scopes (no `superclaude:*` wildcards); use progressive elevation + approval for higher-risk actions. `[EXTERNAL-VERIFIED]`
- **Current-code GAP (the starting point):** `TurnLedger` is sprint-local budget only; tenant/actor/audit identity is **ABSENT** from the scoped models (`PipelineConfig`/`SprintConfig` have model/permission/budget but no tenant/actor). Governance dimensions must be added, not assumed present. `[CODE-VERIFIED]` (absence; `sprint/models.py:692-777`)

---

## 6. State & Data Model *(repurposed from State Management)*

> **REPURPOSE NOTE (Section 6):** The template's Section 6 is "State Management (frontend / client-side state)." This is a backend orchestration architecture with no client-side state, so Section 6 is **repurposed to "State & Data Model."** It documents (a) the `[CODE-VERIFIED]` state and data contracts that exist today in the Python pipeline/sprint runtime, and (b) the `[DESIGN — UNBUILT]` ownership split across Mastra / Backlog.md / Beads that the proposed hybrid would impose on that same state.

### 6.1 State Architecture & Ownership

Today, all orchestration state lives in two physical tiers: **runtime Python dataclasses** (constructed by the runner, not self-reported by the agent) and **durable filesystem artifacts** (markdown task files, JSONL logs, result/checkpoint reports). The proposed hybrid does not collapse these into one store; it assigns each existing concept a single primary owner across three external substrates.

| State / data class | Current owner (today) | Tier | Proposed primary owner | Tag |
|--------------------|-----------------------|------|------------------------|-----|
| Human task body / AC / checklist / decisions | `.dev/tasks` + tasklist markdown (`templates/workflow/02_mdtm_template_complex_task.md:1-44`) | Durable file | Backlog.md | `[CODE-VERIFIED]` current; `[DESIGN — UNBUILT]` owner (`5.5-12`) |
| Machine dependency graph (`depends_on`, `T<PP>.<TT>` edges) | Markdown frontmatter + `**Dependencies:**` text (`sprint/config.py:379-384`) | Durable file | Beads (graph mirror) | `[CODE-VERIFIED]` current; `[DESIGN — UNBUILT]` owner (`5.5-12`) |
| Workflow run state, retries, step status, traces | Python dataclasses + process outputs (`pipeline/models.py`, `sprint/models.py`) | Runtime | Mastra (run/trace) | `[CODE-VERIFIED]` current; `[DESIGN — UNBUILT]` owner (`5.5-12`) |
| Execution logs, checkpoint reports, validation reports | Files under release/task dir (`sprint/models.py:473-510`) | Durable file | Backlog.md docs + Mastra trace refs | `[CODE-VERIFIED]` current; `[DESIGN — UNBUILT]` owner (`5.5-07`) |
| High-volume telemetry (`MonitorState`) | Sprint monitor runtime (`sprint/models.py:623-690`) | Runtime | Mastra observability (summaries only to Backlog/Beads) | `[CODE-VERIFIED]` (`5.5-08`) |
| Budget / cost ledger (`TurnLedger`) | Sprint runtime, sprint-local (`sprint/models.py:693-777`) | Runtime | Governance/control-plane service (insufficient in current model) | `[CODE-VERIFIED]` (`5.5-09`) |
| Stable IDs (`TASK-*`, `T<PP>.<TT>`, `D-####`, `D-CP...`, `R-###`) | Markdown / tasklist generator (`sc-tasklist-protocol/SKILL.md:161-164`) | Durable file | Cross-system sync key; Backlog.md assigns canonical | `[CODE-VERIFIED]` IDs (`5.5-04`); `[DESIGN — UNBUILT]` owner |
| Tenant / actor / audit identity | **Absent** from scoped models (`PipelineConfig`/`SprintConfig`/`TaskResult`/`MonitorState`/`TurnLedger` carry model/permission/budget but no tenant/actor) | — | Must be **added** (governance plane) | `[CODE-VERIFIED]` (absence) (`5.5-15`, `5.8-13`) |

> **Important:** Tenant/actor/audit identity is a verified *absence* in current scoped models, not a field to repoint. The proposed governance plane (§5.8) adds it; it is not assumed to already exist.

**Ownership rules the proposed design preserves** `[DESIGN — UNBUILT]` (`5.5-13`): one prose owner (Backlog.md), one graph owner (Beads), one run owner (Mastra), stable IDs preserved verbatim and never regenerated on import/export, and checkpoint reports remain linkable artifacts (the checkpoint *task node* and the checkpoint *report body* must not be conflated).

### 6.2 State Shape (Current Models — `[CODE-VERIFIED]`)

> State shape is summarized as a table of key fields + notable behavior, not reproduced as full dataclass source. All rows `[CODE-VERIFIED]` at HEAD `9e864860`.

| Model | Key fields | Notable behavior | `path:line` |
|-------|-----------|------------------|-------------|
| `Step` | id, prompt, output_file, gate, timeout_seconds, inputs, retry_limit, model, gate_mode, tool_write_mode, template_path | Core portable workflow-step unit; framework-neutral | `pipeline/models.py:108-123` (`5.1-07`, `5.5-05`) |
| `StepResult` | step pointer (optional), status, attempt, gate_failure_reason, timestamps, remediation metadata, computed duration | Runner-constructed; `step` is optional (state-build risk) | `pipeline/models.py:125-148` (`5.1-08`) |
| `TaskEntry` | task_id, title, description, dependencies, command, classifier | Stores deps but does **not** schedule by dependency order — preserves file order | `sprint/models.py:24-37` (`5.3-07`) |
| `TaskResult` | status, turns, exit_code, timing, output_bytes, gate outcome, reimbursement, output_path | Runner-constructed, **not** agent self-reported | `sprint/models.py:158-209` (`5.3-08`) |
| `CheckpointEntry` | phase, name, expected_path, exists, recovered, recovery_source | Backed by checkpoint report-path conventions on disk | `sprint/models.py:311-341` (`5.5-10`) |
| `MonitorState` | bytes, last event/growth times, activity log, turns, errors, assistant text, task progress, token counts | High-volume telemetry → belongs in tracing layer, not task-of-record | `sprint/models.py:622-690` (`5.5-08`) |
| `TurnLedger` | initial_budget, consumed, reimbursed, reimbursement_rate, minimum_allocation, remediation + wiring budgets | Sprint-local; insufficient for multi-tenant governance | `sprint/models.py:692-777` (`5.3-17`, `5.5-09`) |

### 6.3 Key State Transitions & Status Enums (Current — `[CODE-VERIFIED]`)

The status enums below are the authoritative lifecycle vocabulary the proposed Mastra run-status / Backlog status / Beads status mappings must round-trip without lossy normalization.

| Enum | Values | `path:line` |
|------|--------|-------------|
| `StepStatus` | PENDING, PASS, FAIL, TIMEOUT, CANCELLED, SKIPPED (`is_failure` true only for FAIL + TIMEOUT) | `pipeline/models.py:40-67` (`5.1-03`) |
| `TaskStatus` | PASS, FAIL, INCOMPLETE, SKIPPED | `sprint/models.py:39-54` (`5.5-06`) |
| `GateOutcome` | PASS, FAIL, DEFERRED, PENDING (+ display: CHECKING, FAIL_DEFERRED, REMEDIATING, REMEDIATED, HALT) | `sprint/models.py:56-124` (`5.5-06`) |
| `PhaseStatus` | 13 values: PENDING, RUNNING (transient) + 11 result states PASS, PASS_NO_SIGNAL, PASS_NO_REPORT, PASS_RECOVERED, PREFLIGHT_PASS, PASS_MISSING_CHECKPOINT, INCOMPLETE, HALT, TIMEOUT, ERROR, SKIPPED | `sprint/models.py:211-270` (`5.3-09`) |
| `SprintOutcome` | SUCCESS, HALTED, INTERRUPTED, ERROR | `sprint/models.py:272-279` (`5.5-06`) |

**Proposed mapping of these transitions onto the hybrid** `[DESIGN — UNBUILT]` (`5.5-12`, Contract 4): a Mastra run emits step/run terminal states; an idempotent reconciliation adapter projects them to Backlog.md (human status + execution-log summary) and Beads (normalized graph status / blocker edges). The reconciliation must be idempotent — re-running the same Mastra result event must not duplicate Backlog log rows or Beads edges (`5.5-14`).

### 6.4 Cross-Store Dependencies (Proposed Ownership Boundaries — `[DESIGN — UNBUILT]`)

| Source store | Consumer store | Relationship | Boundary rule | Tag |
|--------------|----------------|--------------|---------------|-----|
| Backlog.md (prose + IDs) | Beads (graph) | Backlog/tasklist → Beads upsert by stable ID | Backlog wins for existence/title/body; Beads owns status only if explicitly configured | `[DESIGN — UNBUILT]` (`5.5-14`) |
| Backlog.md + Beads | Mastra (run plan) | Read for deterministic dry-run workflow plan | Plan must be deterministic from Backlog + Beads before any side effect | `[DESIGN — UNBUILT]` (Contract 3) |
| Mastra (run results) | Backlog.md + Beads | Mastra → summaries/status updates | Idempotent; telemetry stays in Mastra traces, not Backlog/Beads bodies | `[DESIGN — UNBUILT]` (`5.5-14`, Contract 4) |
| Beads graph | Sprint execution order | Graph would drive scheduling | **Behavioral change:** today markdown tasklists are *ordered records*, sprint parses deps but executes in document order (`5.7-31`); making Beads `bd ready` authoritative changes execution semantics, not just storage | `[CODE-VERIFIED]` current behavior + `[DESIGN — UNBUILT]` change (`5.7-31`) |

> **CRITICAL:** Adopting Beads `bd ready` as the scheduler is a behavioral change, not a runtime swap. Current sprint execution is document-order (`sprint/config.py:379-384`, `executor.py:971-1010`, `5.7-31`); a dependency-graph scheduler can reorder execution. Round-trip parser-compatibility tests (`discover_phases()`, `parse_tasklist_file()`, task-count and dependency equality) are the proposed acceptance gate before any ownership transfer (`5.5-14`).

---

## 7. Contract & Workflow Inventory *(repurposed from Component Inventory)*

> **REPURPOSE NOTE (Section 7):** The template's Section 7 is "Component Inventory (frontend component tree + component catalog)." This architecture has no React/UI component tree, so Section 7 is **repurposed to "Contract & Workflow Inventory."** It inventories (a) the `[CODE-VERIFIED]` pipeline/runtime contracts that exist today and that any port must preserve, and (b) the four `[DESIGN — UNBUILT]` adapter contracts the proposed hybrid introduces.

### 7.1 Contract Dependency Map (replaces Component Tree)

```
[Existing — CODE-VERIFIED]                         [Proposed — DESIGN/UNBUILT]

 pipeline/models.py  (framework-neutral contracts)
   ├── Step / StepResult / StepStatus / GateMode
   ├── GateCriteria / SemanticCheck
   ├── Deliverable / DeliverableKind
   └── PipelineConfig + CosmeticRemediator proto
            │
            ▼
 pipeline/executor.py  execute_pipeline()
   └── StepRunner protocol  ◄─── process boundary ───►  ClaudeProcess (pipeline/process.py)
            │                                                   │
   ┌────────┼──────────┬───────────┐                           │  Contract 3
   ▼        ▼          ▼            ▼                           ▼  Backlog+Beads → Mastra plan
 roadmap  tasklist   sprint     trailing_gate            ┌─────────────────────┐
 executor executor   executor   (deferred remediation)   │  Adapter Layer      │
   (shared execute_pipeline + injected run_step)          │  C1 tasklist→Backlog│
            │                                              │  C2 Backlog/TL→Beads│
            ▼                                              │  C3 →Mastra plan    │
 sprint/config.py  parse_tasklist  (strict parser)  ◄──── │  C4 Mastra→reconcile│
   T<PP>.<TT> headings · Dependencies · Command · CP       └─────────────────────┘
                                                            round-trip parser tests = acceptance gate
```

> **Note:** The single migration seam is `ClaudeProcess` + `StepRunner` / `execute_pipeline`; gate, model, deliverable and diagnostic logic is runtime-agnostic pure Python and therefore highly portable (`5.1-13`, `5.7-29`, `5.7-30`).

### 7.2 Existing Contract Inventory (`[CODE-VERIFIED]`)

These are the contracts a hybrid port must preserve. All rows `[CODE-VERIFIED]` at HEAD `9e864860`.

| Contract | Role | Key signature / shape | `path:line` |
|----------|------|-----------------------|-------------|
| `Step` dataclass | Portable workflow-step unit | id, prompt, output_file, gate, timeout_seconds, inputs, retry_limit, model, gate_mode, tool_write_mode, template_path | `pipeline/models.py:108-123` (`5.1-07`) |
| `StepResult` dataclass | Runner-authored outcome | status, attempt, gate_failure_reason, timestamps, remediation metadata, duration | `pipeline/models.py:125-148` (`5.1-08`) |
| `StepRunner` protocol | Process-boundary seam | `__call__(step, config, cancel_check) -> StepResult` | `pipeline/executor.py:41-60` (`5.1-13`) |
| `execute_pipeline()` | Generic sequencer | accepts `list[Step \| list[Step]]`; nested list = parallel group; start/complete/state callbacks, cancellation, optional trailing runner | `pipeline/executor.py:63-188` (`5.1-14`) |
| `GateCriteria` + `gate_passed()` | Pure-Python validation | tiers EXEMPT/LIGHT/STANDARD/STRICT; frontmatter + min_lines + semantic checks | `pipeline/models.py:90-105`, `pipeline/gates.py:20-76` (`5.1-06`, `5.1-22`) |
| `GateMode` + `resolve_gate_mode()` | Blocking vs trailing | BLOCKING/TRAILING; release always blocking, task trailing only if grace_period>0; `grace_period==0` forces BLOCKING | `pipeline/models.py:69-79`, `pipeline/executor.py:211-215`, `trailing_gate.py:604-647` (`5.1-04`, `5.1-17`, `5.1-36`) |
| `ClaudeProcess` | Runtime subprocess seam | builds `claude --print --verbose <perm> --no-session-persistence --tools default --max-turns N --output-format <fmt>`; prompt via stdin; exit 124 = timeout | `pipeline/process.py:73-95`, `159-214` (`5.1-25`, `5.1-28`, `5.7-29`) |
| `Deliverable` + `decompose_deliverables()` | Behavioral split | `.a` implement + `.b` verify; idempotent | `pipeline/models.py:151-209`, `pipeline/deliverables.py:146-194` (`5.1-09`, `5.1-39`) |
| `DeferredRemediationLog` | Trailing-gate persistence | lock-guarded, disk-persistent JSON; PENDING/REMEDIATED/WAIVED | `pipeline/trailing_gate.py:471-596` (`5.1-35`) |
| Sprint parser contract | Tasklist compatibility | `### T<PP>.<TT> -- Title`, `**Dependencies:**`, `**Command:**`, classifier row, Execution Mode (claude/python/skip), phase filename aliases | `sprint/config.py:15-26`, `374-492` (`5.3-04`, `5.3-06`, `5.5-11`) |
| `TurnLedger` | Budget ledger | `can_launch()` / pre-debit / reconcile; sprint-local | `sprint/models.py:692-777` (`5.3-17`) |
| `pipeline/__init__.py` API surface | Compatibility anchor | 65 exported symbols in `__all__` (models, executor, gates, process, deliverables, guard/FMEA/dataflow/conflict/invariant/diagnostic) | `pipeline/__init__.py:1-157` (`5.1-42`) |

**Defined-but-unwired / drift contracts to preserve (not silently fix)** `[CODE-VERIFIED]`:

| Contract | State | `path:line` | Evidence |
|----------|-------|-------------|----------|
| `CERTIFY_GATE` / `build_certify_step` | Defined, **not wired** in production `_build_steps` | `roadmap/gates.py:1324-1351`, `roadmap/executor.py:2205` | `5.2-10` (§14 L1) |
| Deviation classifier | **Unwired**; all records render UNCLASSIFIED | `roadmap/executor.py:1603-1609`, `gates.py:1390-1422` | `5.2-19` (§14 L4) |
| `WIRING_GATE` trailing mode | Configured TRAILING but grace_period defaults 0 → effectively BLOCKING | `roadmap/executor.py:2175-2184` | `5.2-12` (§14 L2) |
| Path-A `_verify_checkpoints()` | Per-task path does **not** call it (only Path B does) | `sprint/executor.py:1259-1301` vs `1512-1531` | `XC-06` (§14 L3) |
| 4-layer `IsolationLayers` | Exists but **not called** in main loop; partial/unused | `sprint/executor.py:106-182`, `1303-1324` | `5.3-14` (§14 L5) |
| `read_status_from_log` / `tail_log` | **Stubs** ("not yet connected"); status/logs commands don't report live | `sprint/logging_.py:224-235` | `5.3-28` (§14 L6) |

> **CRITICAL:** A faithful port must preserve these states as-is and flag them, not normalize them. Silently wiring `CERTIFY_GATE` or the deviation classifier during migration would change gate semantics and mask known gaps (evidence index "key load-bearing facts" #2; `XC-16`).

### 7.3 Proposed Adapter-Contract Inventory (`[DESIGN — UNBUILT]`)

The hybrid introduces exactly four adapter contracts. **None is implemented in the repo today** (`5.6-27`). Each carries a round-trip / idempotency validation contract.

| # | Adapter contract | Direction | Mapping summary | Validation contract |
|---|------------------|-----------|-----------------|---------------------|
| C1 | Tasklist bundle → Backlog.md import | tasklist → Backlog | `TASKLIST_ROOT`→container, phase H1→milestone/doc, `T<PP>.<TT>`→task external ID, body→markdown, `**Dependencies:**`→dep metadata+text, numbered checkpoint tasks→verification task+linked doc | Export back to files such that `discover_phases()` + `parse_tasklist_file()` succeed and counts match `count_tasks_in_file()` (`5.5-14`, RF07 C1) |
| C2 | Backlog.md / tasklist → Beads graph sync | Backlog/tasklist → Beads | root issue, phase parent (epic), task issue (status/tier/risk/classifier/deliverable IDs), dependency edges `dep→dependent`, checkpoint node, artifact pointer (path only) | Graph export must produce dependency list identical to parser-extracted `TaskEntry.dependencies` unless a human-approved patch exists (`5.5-14`, RF07 C2) |
| C3 | Backlog.md / Beads → Mastra workflow plan | Backlog/Beads → Mastra | one workflow per bundle; one stage per phase; `T<PP>.<TT>` as step external ID; gate→blocking/trailing branch or scorer; trace metadata = R-*/T-*/D-*/phase/tier/model/permission/max_turns; provider = ClaudeProcess (hybrid) or new adapter | Plan generation must be **deterministic** from Backlog + Beads and produce a dry-run plan (task order, gates, expected artifacts, provider commands) before execution (`5.5-14`, RF07 C3) |
| C4 | Mastra run results → Backlog.md + Beads reconciliation | Mastra → Backlog/Beads | PASS→log entry + optional task done / issue close; FAIL/INCOMPLETE→failure note + remediation edge; DEFERRED→deferred gate report; HALT→halt report + resume command + blocked root; checkpoint→link doc + close node; telemetry→summarized budget line only | Reconciliation must be **idempotent**: replaying the same result event must not duplicate Backlog rows or Beads edges (`5.5-14`, RF07 C4) |

> **Tip:** The proposed pilot wraps `superclaude tasklist validate` first — the smallest surface (single strict gate, non-destructive, reuses the shared pipeline) — and the decisive early gate is proving Mastra rerun/recovery/durability before committing to broader port (`XC-13`).

---

## 8. API & Integration Points

This section documents the external integration surfaces of the three target substrates (`[EXTERNAL-VERIFIED]`, with source URLs) and the `[DESIGN — UNBUILT]` integration boundaries the hybrid would establish. The current system's only "API" is the `ClaudeProcess` subprocess seam (`[CODE-VERIFIED]`, §6.2 / §7.2); everything Mastra/Backlog/Beads is external capability, not current implementation.

### 8.1 External Integration Surfaces Used (`[EXTERNAL-VERIFIED]`)

| Surface | Substrate | Transport / contract | Key constraint | Source |
|---------|-----------|----------------------|----------------|--------|
| `MCPClient` | Mastra | Connects agents to external MCP servers over **stdio / HTTP / SSE** | — | mastra.ai/docs/mcp/overview (`5.7-07`) |
| `MCPServer` | Mastra | Exposes agents/tools/workflows over **HTTP(S)**; `requireToolApproval` = human-in-the-loop; FGA enforcement for MCP tool exec | FGA tied to Enterprise Edition | mastra.ai/docs/mcp/overview (`5.7-07`) |
| Mastra server (REST) | Mastra | Hono-based; Express/Hono/Fastify/Koa adapters; registered agents/workflows become REST endpoints with **OpenAPI/Swagger** | Studio/API public unless auth configured | mastra.ai/docs/server/mastra-server (`5.7-08`, `5.7-06`) |
| `WorkspaceSandbox` | Mastra | `executeCommand`/start/stop/destroy, timeouts, stdout/stderr/wait, maxRetainedBytes (@mastra/core@1.1.0) | Candidate subprocess substrate but **NOT proven** parity with Claude Code hook/permission model | mastra.ai/reference/workspace/sandbox (`5.7-03`, `XC-22`) |
| Backlog.md MCP (MVP) | Backlog.md | **stdio** MCP surface routing through Core APIs; tools `task_*`, `milestone_*`, `definition_of_done_defaults_*`, `document_*` | Decision tools are **CLI-only**, not MCP; contradicts older "75+ tools" claims | github.com/MrLesk/Backlog.md/src/mcp/README.md (`5.7-14`) |
| Backlog.md MCP task schemas | Backlog.md | list/search/view/archive/complete use **`additionalProperties: false`** | SuperClaude custom metadata **cannot** be arbitrary MCP fields — must use supported fields / body sections / docs, or extend the schema | github.com/MrLesk/Backlog.md/src/mcp/tools/tasks/schemas.ts (`5.7-13`) |
| Backlog.md CLI / filesystem | Backlog.md | `backlog/` dir; `backlog init --no-git` = filesystem-only; `autoCommit` default false; `proper-lockfile` | Local-file / git-centric, **not** a centralized multi-user transactional PM backend; one-task-per-agent discipline needed | github.com/MrLesk/Backlog.md; ADVANCED-CONFIG.md (`5.7-15`, `5.7-16`) |
| Beads `bd` CLI (`--json`) | Beads | `--json` stable contract (schema v1); `BD_JSON_ENVELOPE=1` opts into uniform envelope (planned v2.0 default); legacy lists = raw arrays; `bd export --json` = JSONL | Integration must parse `--json` with **dual** legacy + envelope compatibility; **not** JSONL reads | github.com/gastownhall/beads/docs/JSON_SCHEMA.md (`5.7-25`) |
| Beads core verbs | Beads | `bd ready` (unblocked), `bd create`, `bd update --claim` (atomic assignee + in_progress), `bd dep add`, `bd show`, `bd prime`, `bd remember` | `bd ready` = no open blocking deps; cycles rejected at write | github.com/gastownhall/beads; SETUP.md (`5.7-20`, `5.7-21`) |
| Beads server mode | Beads | `dolt sql-server`, concurrent writers, `bd init --server` (`--server-host/port/socket/user` + `BEADS_DOLT_PASSWORD`) | **Server mode REQUIRED** for multi-agent; embedded (default) is single-writer ("database is locked" under contention) | github.com/gastownhall/beads/docs/DOLT.md (`5.7-24`) |
| Beads gates | Beads | `gh:pr`, `gh:run`, `timer`, `bead` (cross-rig), `human` (approval); `bd gate check/discover` | Maps SuperClaude "done vs merged/validated" semantics | github.com/gastownhall/beads/docs/DEPENDENCIES.md (`5.7-22`) |

> **CRITICAL:** Storage is **Dolt-first** for Beads (version-controlled SQL, cell-level merge, branching). `.beads/issues.jsonl` is export/interchange **only**, not the canonical sync layer — this corrects the seed-brief "SQLite + JSONL" framing (`5.7-23`). Version caution: Beads v1.0.5 is pre-release/gated ("do not upgrade", migration 0043 can break multi-machine sync, #4259); v1.0.4 had a server data-clobber regression — **pin and gate versions** (`5.7-27`).

### 8.2 Internal Integration Points (Current `[CODE-VERIFIED]` + Proposed `[DESIGN — UNBUILT]`)

| Integration | Direction | Mechanism | Description | Tag |
|-------------|-----------|-----------|-------------|-----|
| Executor ↔ runner | Bidirectional | `StepRunner` protocol | Process-boundary seam; runner owns subprocess + timeout, executor owns retry/gates/ordering | `[CODE-VERIFIED]` (`5.1-13`) |
| Runner → Claude CLI | Outbound | `ClaudeProcess` subprocess | `claude --print` over stdin; stdout = output file (or `.log` sidecar in tool-write mode) | `[CODE-VERIFIED]` (`5.1-24`..`5.1-28`) |
| roadmap / tasklist / sprint → shared pipeline | Inbound | `execute_pipeline` + injected `run_step` | All consumers reuse generic sequencer (sprint runs its own phase loop on shared models) | `[CODE-VERIFIED]` (`5.1-43`) |
| Tasklist → Backlog.md (C1) | Outbound | adapter import | Markdown task/doc import preserving stable IDs | `[DESIGN — UNBUILT]` (`5.5-14`) |
| Backlog/tasklist → Beads (C2) | Outbound | `bd` CLI `--json` | Dependency-graph mirror by stable external ID | `[DESIGN — UNBUILT]` (`5.5-14`) |
| Backlog/Beads → Mastra (C3) | Outbound | workflow plan generation | Deterministic dry-run plan before execution | `[DESIGN — UNBUILT]` (`5.5-14`) |
| Mastra → Backlog/Beads (C4) | Inbound | idempotent reconciliation | Run results projected to status/log/graph | `[DESIGN — UNBUILT]` (`5.5-14`) |
| Governance plane → all | Bidirectional | control-plane (proposed) | Tenant registry, identity mapping, RBAC/ABAC, tool catalog, MCP inventory, approval, audit, cost/budget attribution | `[DESIGN — UNBUILT]` (`5.8-11`) |

> **Important:** MCP is a narrow integration protocol (host/client/server tool-resource exchange), **explicitly not a governance platform** (`5.8-01`). Token passthrough is forbidden (`5.8-03`). A company-wide multi-tenant deployment needs an **additional** governance/control-plane layer beyond all three components (`5.8-11`); none of Mastra OSS, Backlog.md, or Beads supplies cross-tenant IAM, enterprise audit, rate limiting, or cost attribution (`5.8-09`, `5.8-10`).

### 8.3 External Service Dependencies & Failure Modes

| Service | Purpose in hybrid | Failure mode | Proposed fallback / mitigation | Tag |
|---------|-------------------|--------------|--------------------------------|-----|
| Mastra runtime | Run/trace/gate-execution owner (C3/C4) | Hook/permission parity NOT established vs Claude Code; Temporal runner experimental; rerun/replay/idempotency unvalidated | Hybrid: keep current Python+ClaudeProcess as execution oracle until spike gate SG1 proves durable subprocess supervision parity | `[EXTERNAL-VERIFIED]` risk (`5.7-10`, `XC-12`, `XC-22`) |
| Mastra EE (auth/RBAC/FGA/audit) | Production governance | RBAC/SSO/FGA/audit/on-prem are **Enterprise-licensed**, not Apache-2.0 core; `ee/` dirs under Mastra EE license | License decision is a go/no-go gate (D2); cost/identity decision at SG4 | `[EXTERNAL-VERIFIED]` key risk (`5.7-06`, `XC-17`) |
| Backlog.md | Prose / task / doc owner (C1) | `additionalProperties:false` rejects custom metadata; browser-UI state-loss bug #578; Backlog↔Beads integration immature (open FR #588) | Use supported fields/body/docs or extend schema; assign canonical owner per D1/D3; narrow import/export sync first | `[EXTERNAL-VERIFIED]` risk (`5.7-13`, `5.7-17`, `5.7-18`) |
| Beads (Dolt) | Dependency-graph owner (C2) | Embedded mode single-writer; multi-agent needs server mode; session attribution churning (#3400/#3583); version sync corruption (#4259) | Server mode + atomic `--claim` + one-task-per-agent; pin + gate versions; tested backup/restore (SG3) | `[EXTERNAL-VERIFIED]` risk (`5.7-24`, `5.7-27`, `5.7-28`, `XC-20`, `XC-21`) |
| Claude CLI (current) | Execution provider today | Subprocess timeout (exit 124), prompt-too-long, max-turns; `ClaudeProcess` handles SIGTERM→SIGKILL escalation | Current behavior preserved in hybrid; Mastra WorkspaceSandbox is candidate replacement only after parity proof | `[CODE-VERIFIED]` (`5.1-28`, `5.7-29`) |

---

## 9. Configuration & Environment

> **Conditional Section status:** INCLUDED. The proposed hybrid is configuration-heavy: it composes three independently versioned external substrates (Mastra, Backlog.md, Beads), each with its own licensing, deployment-mode, and version-pinning constraints, on top of the existing Python pipeline's configuration surface.

### 9.1 Configuration Files

This table separates configuration that exists today (the Python pipeline the hybrid wraps) from configuration the hybrid would need to introduce.

| File / Surface | Purpose | Key Settings | Tag |
|----------------|---------|--------------|-----|
| `pipeline/models.py` `PipelineConfig` | Base run config for the generic executor | `work_dir`, `dry_run`, `max_turns`, `model`, `permission_flag` (default `--dangerously-skip-permissions`), `debug`, `grace_period`, cosmetic-remediation settings | `[CODE-VERIFIED]` `pipeline/models.py:212-235` |
| `sprint/models.py` `SprintConfig` | Sprint run config; extends `PipelineConfig` | `__post_init__` sets `work_dir=release_dir`, maps wiring fields, derives `wiring_gate_mode`, defaults `state_dir` to `.dev/sprint-state/<id>` | `[CODE-VERIFIED]` `sprint/models.py:347-510`, `415-471` |
| `.roadmap-state.json` | Roadmap resume/state file | spec path/hash, input type, TDD/PRD paths, agents, depth, per-step statuses, validation/fidelity/remediate/certify status | `[CODE-VERIFIED]` `roadmap/executor.py:2627-2682` |
| `cli_portify` `config YAML` + `STEP_REGISTRY` | Deterministic step config (precedent for hybrid step config) | 12 ordered step IDs, phase types, per-step timeouts, retry limits, named artifacts | `[CODE-VERIFIED]` `cli_portify/executor.py:105-183`, `767-840` |
| `backlog.config.yml` (Backlog.md) | Project-local task-store config | `statuses`, `labels`, `defaultStatus`, git settings, `filesystemOnly`, zero-padded IDs, `backlogDirectory`, prefixes, MCP HTTP config; `autoCommit` default `false`, `remoteOperations`, `bypassGitHooks` | `[EXTERNAL-VERIFIED]` ADVANCED-CONFIG.md ; src/types/index.ts |
| Beads Dolt mode config | Embedded vs server mode selection | embedded (default): `.beads/embeddeddolt/`, single-writer file lock; server: `bd init --server`, `--server-host/port/socket/user` + `BEADS_DOLT_PASSWORD`, `.beads/dolt/`; shared-server: `bd dolt set shared-server true`, port 3308 | `[EXTERNAL-VERIFIED]` github.com/gastownhall/beads/docs/DOLT.md |
| Mastra `Mastra` instance + `MastraCompositeStore` | Runtime/workflow/storage config | storage provider selection (libSQL/Turso, PostgreSQL, MongoDB, Redis/Upstash, DynamoDB, MSSQL, ClickHouse, Cloudflare); composite routing of memory/workflows/scores/observability domains; runner choice (built-in / Inngest / Temporal-experimental) | `[EXTERNAL-VERIFIED]` mastra.ai/docs/memory/storage ; reference/storage/composite ; docs/deployment/workflow-runners |
| Hybrid adapter config (e.g. `hybrid.config.yml`) | **DESIGN** — single typed graph as source-of-truth + adapter routing | ownership map (Backlog.md=prose/task/doc/decisions, Beads=dependency graph, Mastra=run/trace/gate state); stable-ID strategy; round-trip parser validation; per-adapter version pins | `[DESIGN — UNBUILT]` (5.5-12, 5.5-14, 5.6-25) |

### 9.2 Licensing as Configuration (External Substrates)

> **Important:** For this hybrid, licensing is not a footnote — it is a hard configuration gate that determines which features are even available. This is the single biggest strategic constraint (RISK R1, XC-17).

| Component | License | What is free | What is gated | Tag |
|-----------|---------|-------------|--------------|-----|
| Mastra core | Apache-2.0 | Agents, workflows, storage adapters, Server, observability core; `SimpleAuth` (API-key → `{id,name,role}`) | Everything under any `ee/` directory: `StaticRBACProvider`, `DEFAULT_ROLES` (owner/admin/member/viewer), WorkOS/Okta SSO, permission-based Studio UI, Agent Builder multi-tenant workflows — all import from `@mastra/core/auth/ee` and require a paid EE license in production | `[EXTERNAL-VERIFIED]` mastra.ai/docs/server/auth ; pricing ; Context7 `/mastra-ai/mastra` |
| Mastra EE | Mastra Enterprise License (bespoke commercial — NOT Elastic 2.0 / BSL) | dev + testing on your own systems | Any "production" use beyond dev/testing requires a written commercial agreement; redistribution/sublicense/sell forbidden; RBAC, audit logs, SLAs, VPC/on-prem data locality | `[EXTERNAL-VERIFIED]` web-01 finding 6; FEASIBILITY-STUDY M10/M11 |
| Backlog.md | MIT | Entire product (CLI, TUI board, browser UI, search, docs, decisions, MCP MVP) | (none) — but no native multi-tenancy/RBAC/auth/remote-HTTP transport exists; stdio + single-repo + single-trust-domain by design | `[EXTERNAL-VERIFIED]` github.com/MrLesk/Backlog.md ; package.json |
| Beads | open-source (`gastownhall/beads`) | Full CLI / Dolt store / dependency graph / gates / memory | (none) — but NO multi-tenancy/RBAC at the Beads layer; "multi-writer" (server mode) is concurrency, not tenancy | `[EXTERNAL-VERIFIED]` github.com/gastownhall/beads ; DOLT.md |

> **CRITICAL:** The OSS Apache path on Mastra yields only `SimpleAuth` (flat API-key→role) plus application-level storage scoping; the RBAC/tenant layer must be built DIY. A multi-tenant RBAC platform on Mastra is feasible but commercially gated. `[EXTERNAL-VERIFIED]` (FEASIBILITY-STUDY §5.1.2)

### 9.3 Version Pins and Deployment-Mode Settings

> **Important:** All three external components are fast-moving with sharp edges (RISK R9, XC-25). Every adapter MUST pin versions and runtime-verify schemas rather than assume a stable contract.

| Component | Version (verified) | Pin / mode guidance | Tag |
|-----------|--------------------|--------------------|----|
| Beads | `v1.0.5` | **`v1.0.5` is pre-release / gated with a "do not upgrade" warning** — migration `0043` can silently and unrecoverably break multi-machine `bd dolt` sync (issue #4259). `v1.0.4` had a server-mode data-clobber regression (#3870). Pin + gate versions; include `bd doctor` + backup/restore + push/pull smoke tests in adoption gates. Confirm exact current release against the live releases page before pinning. | `[EXTERNAL-VERIFIED]` github.com/gastownhall/beads/releases ; #3870, #4259 |
| Beads deployment mode | embedded (default) vs server | Embedded = in-process Dolt, single-writer with file lock ("database is locked" under contention), solo only. **Server mode (`bd init --server`) is REQUIRED for any multi-agent / parallel writer scenario.** Sync via Dolt remotes under `refs/dolt/data`. `.beads/issues.jsonl` is export/interchange ONLY — drive `bd ... --json`, never read JSONL as canonical. | `[EXTERNAL-VERIFIED]` DOLT.md ; SYNC_CONCEPTS.md |
| Beads JSON contract | schema version `1` | `--json` (not `--format json`) is the stable contract. `BD_JSON_ENVELOPE=1` opts into a uniform envelope (planned default v2.0). Legacy list commands emit raw arrays; `bd export --json` emits JSONL. Integrations need a dual parser (legacy + envelope). | `[EXTERNAL-VERIFIED]` JSON_SCHEMA.md |
| Backlog.md | `v1.45.2` | TypeScript/Bun; MVP stdio MCP surface with active churn and doc drift. Git is optional: `backlog init --no-git` creates a filesystem-only project (`autoCommit` default `false`). MCP task schemas use `additionalProperties: false` — custom orchestration metadata CANNOT be added as arbitrary MCP fields; must map to supported fields, body sections, docs, or extend the schema. | `[EXTERNAL-VERIFIED]` package.json ; src/mcp/tools/tasks/schemas.ts ; ADVANCED-CONFIG.md |
| Mastra core | `@mastra/core 1.1.0+` (1.x, fast-moving); precise current-latest is `[DESIGN — UNVERIFIED]` and MUST be verified/pinned at adoption time | `WorkspaceSandbox` was ADDED in `@mastra/core@1.1.0`, so `>= 1.1.0` is the hard floor `[EXTERNAL-VERIFIED]` (web-01; mastra.ai/reference/workspace/sandbox). Pin `@mastra/core` at a known-good `1.x` version at adoption time — verify exact current-latest before pinning rather than assuming a stable contract `[DESIGN — UNBUILT]`. Use composite storage in any serious deployment (PostgreSQL/libSQL for snapshots, ClickHouse for observability; avoid in-memory except tests). `@mastra/temporal` is experimental/not-production-ready; prefer built-in or Inngest runner. | `[EXTERNAL-VERIFIED]` web-01 ; reference/workspace/sandbox ; docs/deployment/workflow-runners |

### 9.3.1 Hybrid configuration the design would need to add `[DESIGN — UNBUILT]`

| Config need | Why | Tag |
|-------------|-----|-----|
| Ownership map (one prose owner, one graph owner, one run owner) | Dual task/status owners (Backlog.md + Beads) cause drift; integration is immature (Backlog.md FR #588). Canonical owners must be assigned in config. | `[DESIGN — UNBUILT]` (5.5-13; RISK R3 / XC-19) |
| Stable-ID mapping config (`TASK-*`, `T<PP>.<TT>`, `D-####`, `R-###` ↔ Backlog.md IDs ↔ Beads hash IDs) | Stable IDs are the cross-system sync keys and are non-negotiable. | `[DESIGN — UNBUILT]` (5.5-04, 5.5-13) |
| Beads ↔ Backlog.md sync scope (start narrow: import/export only) | Maintainer guidance on FR #588: choose one workflow (e.g. import/export sync) before a broad integration surface. | `[DESIGN — UNBUILT]` (5.7-17) |
| Governance/control-plane config (tenant registry, identity mapping, RBAC/ABAC, tool catalog, MCP inventory, approval engine, audit log, cost/rate/budget) | None of the three components supplies tenant isolation, per-invocation audit, or cost attribution; MCP is not a governance platform. Required before company-wide multi-tenant deployment. | `[DESIGN — UNBUILT]` (5.8-11; RISK R8 / XC-24) |

### 9.4 Environment Variables

| Variable | Purpose | Default | Required | Tag |
|----------|---------|---------|----------|-----|
| `CLAUDE_WORK_DIR` | Sprint Path B sets this on the spawned subprocess (the only isolation env reliably passed today) | (unset) | No | `[CODE-VERIFIED]` `sprint/executor.py:1303-1324` |
| `CLAUDECODE`, `CLAUDE_CODE_ENTRYPOINT` | Stripped by `build_env()` before launching the child `claude --print` process | (stripped) | n/a | `[CODE-VERIFIED]` `pipeline/process.py:97-112`, `136-139` |
| `BEADS_DOLT_PASSWORD` | Beads server-mode auth | (unset) | Yes (server mode) | `[EXTERNAL-VERIFIED]` DOLT.md |
| `BEADS_DOLT_SHARED_SERVER` / `BEADS_DIR` | Enable shared-server mode / relocate `.beads/` | (unset) | No | `[EXTERNAL-VERIFIED]` DOLT.md |
| `BD_JSON_ENVELOPE` | Opt into uniform Beads JSON envelope (planned v2.0 default) | `0` | No | `[EXTERNAL-VERIFIED]` JSON_SCHEMA.md |
| `CLAUDE_SESSION_ID` / `BEADS_SESSION_ID` | Beads multi-agent session attribution (actively changing — #3400/#3583) | (unset) | No (in flux) | `[EXTERNAL-VERIFIED]` #3400/#3583 |
| Mastra storage / auth provider env (PostgreSQL/ClickHouse DSNs, WorkOS/Auth0/Clerk keys) | Configure composite storage + auth provider | varies | varies | `[EXTERNAL-VERIFIED]` mastra.ai/docs/memory/storage ; docs/server/auth |

> **Note:** The four-layer `IsolationLayers` (`CLAUDE_WORK_DIR`, `GIT_CEILING_DIRECTORIES`, `CLAUDE_PLUGIN_DIR`, `CLAUDE_SETTINGS_DIR`) is DEFINED but NOT called in the sprint main loop today; only Path B sets `CLAUDE_WORK_DIR` and Path A passes no isolation env. A faithful Mastra port must either implement these for real or explicitly scope to the weaker active model — they are not a current runtime guarantee. `[CODE-VERIFIED]` `sprint/executor.py:106-182`, `1303-1324`, `1076-1115` (§14 L5)

### 9.5 Feature Flags

These exist in the current pipeline and would carry forward conceptually as hybrid run modes; the hybrid-specific flags are DESIGN.

| Flag / Surface | Description | Default | Impact When Toggled | Tag |
|----------------|-------------|---------|---------------------|-----|
| `--dry-run` | Roadmap/pipeline preview without side effects; skips sub-skill invocations | off | Structured preview only; no LLM calls | `[CODE-VERIFIED]` `roadmap/commands.py:32-298` |
| `--no-validate` / `--no-convergence` / `--no-compress` | Roadmap stage toggles | on (enabled) | Disables auto-validation / convergence loop / compression | `[CODE-VERIFIED]` `roadmap/commands.py:32-298` |
| `--allow-cosmetic-remediation` / `--strict-no-remediation` | Cosmetic-remediation lane | off | Injects roadmap remediator into `PipelineConfig` | `[CODE-VERIFIED]` `roadmap/commands.py:153-172` |
| sprint `--shadow-gates`, `--stall-timeout`, `--stall-action`, `checkpoint_gate_mode` (off/shadow/soft/full) | Sprint watchdog + checkpoint enforcement | shadow (checkpoints) | Controls stall handling and checkpoint blocking severity | `[CODE-VERIFIED]` `sprint/commands.py:71-188`, `executor.py:1811-1891` |
| Mastra `requireToolApproval` | Human-in-the-loop approval for MCP tool execution | off | Gates tool calls behind manual approval | `[EXTERNAL-VERIFIED]` mastra.ai/docs/mcp/overview |
| Hybrid `ownership.mode` (DESIGN) | Which substrate owns a given record class | n/a | Routes writes to canonical owner; prevents dual-owner drift | `[DESIGN — UNBUILT]` (5.5-12/13) |

---

## 10. Error Handling & Recovery

> **Note:** Section title aligns to the template's §10 "Error Handling & Edge Cases" and extends it to recovery, since durability/recovery is the decisive engineering concern for this hybrid (early-spike gate G2 is "prove Mastra rerun/recovery/durability" — XC-13). The hybrid would inherit two recovery models that must be reconciled: the existing Python pipeline's filesystem-artifact recovery (`[CODE-VERIFIED]`) and Mastra's snapshot-based durable workflow recovery (`[EXTERNAL-VERIFIED]`).

### 10.1 Error Handling Patterns

| Error Category | Handling Pattern | Recovery | Tag |
|----------------|------------------|----------|-----|
| Step failure (generic pipeline) | `StepStatus` FAIL/TIMEOUT are failures; CANCELLED/SKIPPED are not. Retry loop in `_execute_single_step()`; blocking vs trailing branching; cosmetic remediation; final fail | Retry up to `retry_limit`; trailing-mode failures logged as advisory warnings only | `[CODE-VERIFIED]` `pipeline/models.py:40-67`, `executor.py:191-399` |
| Subprocess timeout | `wait()` returns `124` (matches bash `timeout`); `terminate()` does SIGTERM → 10s → SIGKILL → 5s on the process group | Timeout maps to `124`/INCOMPLETE/TIMEOUT downstream | `[CODE-VERIFIED]` `pipeline/process.py:159-214` |
| Parallel-group failure | `_run_parallel_steps()` sets a shared cancellation event when any step fails; no group-level retry | Group cancelled; daemon threads observe cancellation | `[CODE-VERIFIED]` `pipeline/executor.py:402-452` |
| Sprint phase classification | `_determine_phase_status()` authoritative classifier: exit `124`→TIMEOUT; prompt-too-long→INCOMPLETE; end-checkpoint PASS + no contamination→PASS_RECOVERED; result-file HALT/CONTINUE markers; no result+output→PASS_NO_REPORT; no output→ERROR (13 `PhaseStatus` values total: 2 transient + 11 result states) | Runner-authored classification, not agent-self-reported | `[CODE-VERIFIED]` `sprint/executor.py:2067-2148`, `models.py:211-270` |
| Sprint diagnostic capture on failure | `DiagnosticCollector` snapshots monitor + tails logs; `FailureClassifier` prioritizes stall/timeout/context-exhaustion/crash/error/unknown; `ReportGenerator` writes diagnostic markdown; outcome HALTED | Diagnostic artifact + halt | `[CODE-VERIFIED]` `sprint/executor.py:1609-1639`, `diagnostics.py:72-127`, `157-232` |
| eval per-eval error | Per-eval JSONL forensic event buffer logs setup/teardown/spawn/inject/observe/errors; classify ERRORED/PASS/FAIL; timeout emits timeout events, best-effort cancel, preserves HOME, returns TIMEOUT, flushes JSONL | Failed/errored HOMEs preserved for forensics; optional retry-once | `[CODE-VERIFIED]` `eval/runner.py:537-588`, `591-673`, `1026-1101` |
| Beads cycle rejection | `bd dep add` rejects dependency cycles at write time; `bd ready` = no open blocking deps | Write rejected before graph corruption | `[EXTERNAL-VERIFIED]` github.com/gastownhall/beads/docs/DEPENDENCIES.md |
| Mastra durable suspend/resume | Workflows `suspend()` / `resume()` / `resumeStream()`; on suspend Mastra stores a snapshot in the configured storage provider; snapshots persist across deployments and restarts; resume from a specific step ID | Resume from snapshot at a specific step ID | `[EXTERNAL-VERIFIED]` mastra.ai/docs/workflows/suspend-and-resume |
| Mastra runner retries | Inngest runner provides step memoization + automatic retries + suspend/resume; Temporal provides durable execution + retries (experimental) | Runner-dependent; production retry/durability depends on runner + storage choice | `[EXTERNAL-VERIFIED]` mastra.ai/docs/deployment/workflow-runners |

### 10.2 Existing Code-Verified Recovery Surfaces (Reusable by the Hybrid)

These are the recovery primitives the hybrid would wrap or port — they already work today.

| Surface | Behavior | Tag |
|---------|----------|-----|
| Roadmap resume state | `.roadmap-state.json` carries spec path/hash, per-step statuses, validation/fidelity/remediate/certify status; `execute_roadmap()` restores resume state, supports spec-patch resume | `[CODE-VERIFIED]` `roadmap/executor.py:2627-2682`, `2985-3187` |
| Sprint checkpoint verification | `_verify_checkpoints()` runs only after PASS-like status; respects `checkpoint_gate_mode` (off / shadow=default / soft / full); full mode downgrades to `PASS_MISSING_CHECKPOINT` when files are missing. `verify_checkpoint_files()` returns existence status per declared checkpoint | `[CODE-VERIFIED]` `sprint/executor.py:1811-1891`, `checkpoints.py:97-112` |
| Sprint `verify-checkpoints` CLI | Builds a manifest, optionally recovers missing reports, writes `manifest.json`, prints table or JSON | `[CODE-VERIFIED]` `sprint/commands.py:360-415` |
| Sprint manifest + checkpoint recovery | End-of-sprint `build_manifest()` + `write_manifest()` write `<release_dir>/manifest.json` + a `checkpoint_manifest` JSONL event; `recover_missing_checkpoints()` synthesizes reports marked status UNKNOWN | `[CODE-VERIFIED]` `sprint/executor.py:1702-1725`, `checkpoints.py:209-408` |
| eval HOME isolation + forensic JSONL | Three-check `containment_guard` (eval-ID regex, scratch-root allowlist, post-mkdtemp containment); per-eval HOME under `home_root`; failed/errored HOMEs preserved; thread-safe JSONL forensic event buffer | `[CODE-VERIFIED]` `eval/isolation.py:224-260`, `456-642`; `eval/runner.py:537-588` |
| eval RetryOncePolicy | Immutable, policy-tag driven (`MCP-flaky` tag, flaky statuses FAIL/ERRORED/TIMEOUT); one retry on a fresh HOME; idempotent annotation | `[CODE-VERIFIED]` `eval/retry.py:41-165` |
| audit checkpoint/retry/budget | Atomic checkpoint writes (temp + rename); `batch_retry` (max 2, cascading-failure detection); budget degradation (warn/degrade/halt with ordered protected-capability overrides) | `[CODE-VERIFIED]` `audit/checkpoint.py:58-110`, `batch_retry.py:60-187`, `budget.py:26-320` |
| DeferredRemediationLog | Lock-guarded, disk-persistent, JSON serde; PENDING/REMEDIATED/WAIVED; pending entries survive across runs | `[CODE-VERIFIED]` `pipeline/trailing_gate.py:471-596` |

### 10.3 Checkpoint-Recovery Strategy (Hybrid) `[DESIGN — UNBUILT]`

The hybrid must reconcile two recovery substrates without losing the runner-authored-truth property of the current system.

| Design element | Strategy | Tag |
|----------------|----------|-----|
| Run/trace/gate state ownership | Mastra owns run/trace/gate-execution state via durable workflow snapshots; checkpoint stages map to workflow steps. Mastra workflow state could REPRESENT checkpoint stages, but the current implementation relies on filesystem manifests + JSONL events — a faithful port needs explicit filesystem-artifact handling or a migration plan for those artifacts | `[DESIGN — UNBUILT]` (5.5-12; research 03) |
| Checkpoint contract preservation | Preserve the canonical numbered `### T<PP>.<NN> -- Checkpoint:` task contract with `Checkpoint Report Path: TASKLIST_ROOT/checkpoints/...`; the runtime parser accepts BOTH legacy `### Checkpoint:` and numbered forms, but **Path A (per-task executor) does NOT call `_verify_checkpoints()`** today — a known runtime gap the port must wire in, not inherit | `[CODE-VERIFIED]` gap → `[DESIGN — UNBUILT]` fix (XC-05, XC-06; RISK R7 / XC-23; §14 L3) |
| Resume reconciliation | Map sprint phases/tasks to Beads `bd ready` + atomic `bd update <id> --claim`; reconcile Mastra run results back to Backlog.md + Beads idempotently (results→Backlog/Beads reconciliation adapter). Each adapter contract needs round-trip parser validation | `[DESIGN — UNBUILT]` (5.5-14; XC-16) |
| External gates as recovery boundaries | Encode SuperClaude "work done" vs "merged/validated" as Beads gates: `gh:pr` (PR merged), `gh:run` (CI), `timer`, `human` (approval); `bd gate check`/`discover`. These become durable recovery checkpoints external to the workflow runner | `[EXTERNAL-VERIFIED]` DEPENDENCIES.md → `[DESIGN — UNBUILT]` wiring |

### 10.4 Drift-Detection Strategy (Hybrid) `[DESIGN — UNBUILT]`

Dual ownership across three stores is the central new failure mode the hybrid introduces (RISK R3 / XC-19). Drift detection is therefore first-class, not optional.

| Drift surface | Detection strategy | Tag |
|---------------|--------------------|-----|
| Backlog.md ↔ Beads task/status drift | One canonical owner per record class (one prose owner, one graph owner, one run owner); periodic reconciliation diff keyed on stable IDs; start with narrow import/export sync (FR #588 maturity caveat) | `[DESIGN — UNBUILT]` (5.5-13, 5.7-17; RISK R3) |
| Stable-ID drift | Stable IDs (`TASK-*`, `T<PP>.<TT>`, `D-####`, `R-###`) are non-negotiable sync keys; round-trip parser validation on every adapter boundary detects ID divergence | `[DESIGN — UNBUILT]` (5.5-04, 5.5-14) |
| Beads sync corruption | Migration `0043` (v1.0.5) can silently break multi-machine `bd dolt` sync; detection = version-pin gate + `bd doctor` + backup/restore + push/pull smoke tests in adoption gates | `[EXTERNAL-VERIFIED]` (RISK R4 / XC-20; #4259) |
| Convergence/deviation drift (existing) | `DeviationRegistry.load_or_create` resets on spec-hash mismatch; merges structural + semantic findings with stable IDs, ACTIVE status, first/last_seen_run — an existing drift-tracking pattern the hybrid can reuse | `[CODE-VERIFIED]` `roadmap/convergence.py:90-207` |
| Schema/version drift (external tools) | Runtime-verify schemas rather than assume stable contracts: probe live Backlog.md MCP catalog (`additionalProperties:false` rejects unknown fields), use Beads dual JSON parser (legacy + envelope), pin `@mastra/core` at a known-good `1.x` version (`WorkspaceSandbox` requires `>= 1.1.0`; verify exact current-latest at adoption time) | `[EXTERNAL-VERIFIED]` (RISK R9 / XC-25) |

### 10.5 Graceful Degradation

| Failure | Impact | Degraded Experience | Tag |
|---------|--------|---------------------|-----|
| Beads server unavailable (multi-agent) | No concurrent claim/ready queue | Embedded single-writer fallback for solo work only ("database is locked" under contention) — multi-agent halts | `[EXTERNAL-VERIFIED]` DOLT.md |
| Backlog.md browser UI concurrent-edit | Unsaved draft text lost when files change underneath (open bug #578) | Avoid long unsaved browser drafts during agent mutation; CLI/MCP mutation unaffected | `[EXTERNAL-VERIFIED]` #578 |
| Mastra storage = in-memory | Snapshots reset on process change | Durability lost; use composite storage (PostgreSQL/libSQL + ClickHouse) in any non-test deployment | `[EXTERNAL-VERIFIED]` mastra.ai/docs/memory/storage |
| Mastra EE license absent | No production RBAC/SSO/FGA/audit | OSS path: `SimpleAuth` (flat API-key→role) + DIY application-level storage scoping only | `[EXTERNAL-VERIFIED]` (FEASIBILITY-STUDY M11) |
| Sprint summary/retrospective failure | No phase summary or retrospective | End-of-sprint waits up to 90s for summaries; failures logged but do NOT abort wrap-up | `[CODE-VERIFIED]` `sprint/executor.py:1661-1688` |
| sprint `status`/`logs` commands | Live status/log views unavailable | `read_status_from_log`/`tail_log` are STUBS ("not yet connected"); JSONL/Markdown logs still written | `[CODE-VERIFIED]` `sprint/logging_.py:13-213`, `224-235` (§14 L6) |

---

## 11. Performance Characteristics

> **CRITICAL — PERFORMANCE IS LARGELY `[DESIGN — UNVERIFIED]`.** There is **no integrated Mastra + Backlog.md + Beads system to measure**. No source file in the repo implements any of the three integrations (5.6-27). This section documents **characteristics-by-design only** — architectural properties whose *direction* is known from external substrate docs (`[EXTERNAL-VERIFIED]`) or current-code structure (`[CODE-VERIFIED]`), and explicitly marks every concrete throughput/latency expectation as `[DESIGN — UNVERIFIED]` (see §1.1 sub-variant note). **No metrics are fabricated. No "measured value" is asserted for the hybrid, because none has been measured.**

### 11.1 Performance Profile

> **Note:** The template's "Measured Value" column is intentionally filled with **"NOT MEASURED — no integrated system exists"** for all hybrid rows. The only genuinely measurable rows describe the *current* Python pipeline's structural performance levers, not the proposed hybrid.

| Metric | Measured Value | Measurement Method | Tag |
|--------|----------------|--------------------|-----|
| Hybrid end-to-end pipeline latency | NOT MEASURED — no integrated system exists | n/a (would require a built spike per XC-13) | `[DESIGN — UNVERIFIED]` |
| Mastra durable suspend/resume overhead | NOT MEASURED for SuperClaude workloads; snapshot cost depends on storage provider + runner choice | Vendor docs describe capability, not benchmarked latency | `[DESIGN — UNVERIFIED]` (capability `[EXTERNAL-VERIFIED]` mastra.ai/docs/workflows/suspend-and-resume) |
| Beads `bd ready` scheduling latency | NOT MEASURED for SuperClaude graph sizes | n/a | `[DESIGN — UNVERIFIED]` |
| Backlog.md mutation throughput under concurrent agents | NOT MEASURED; `proper-lockfile` + single-repo git model can contend under true concurrent write load | n/a | `[DESIGN — UNVERIFIED]` (contention risk `[EXTERNAL-VERIFIED]` package.json) |
| Current pipeline parallel step speedup | Documented design property (Wave→Checkpoint→Wave); not re-benchmarked here | Existing executor parallel dispatch | `[CODE-VERIFIED]` `pipeline/executor.py:63-188`, `402-452` |

### 11.2 Characteristics-by-Design (Concurrency, Durability, Single-Writer)

This is the substance of what *can* be said about hybrid performance: directional architectural properties, each tagged by provenance. No numbers are invented.

| Characteristic | By-design behavior | Tag |
|----------------|--------------------|-----|
| Mastra durability vs latency trade | Durable workflows persist a snapshot to storage on suspend; this adds storage I/O per suspend/resume boundary. Production durability/retry semantics depend on runner (built-in / Inngest / Temporal-experimental) and storage backend (ClickHouse recommended for prod observability; libSQL for dev; in-memory resets) | `[EXTERNAL-VERIFIED]` mastra.ai/docs/workflows/suspend-and-resume ; docs/memory/storage ; docs/deployment/workflow-runners |
| Mastra concurrency / noisy-neighbor | Real per-tenant concurrency isolation / noisy-neighbor protection is NOT in the Apache core — it comes from the Inngest engine integration. OSS-only deployments therefore have weaker concurrency-isolation guarantees | `[EXTERNAL-VERIFIED]` (FEASIBILITY-STUDY M12) |
| Mastra observability auto-instrumentation | Tracing auto-instruments agent runs, LLM generations, tool calls, workflow steps (token usage, model params) — this is an observability cost AND the primary source for any future hybrid performance measurement | `[EXTERNAL-VERIFIED]` mastra.ai/docs/observability/tracing/overview |
| Beads embedded = single-writer | Embedded mode (default) is in-process Dolt, single-writer with file locking; throughput-bound to one writer and yields "database is locked" under contention — solo only | `[EXTERNAL-VERIFIED]` github.com/gastownhall/beads/docs/DOLT.md |
| Beads server = multi-writer | Server mode (`dolt sql-server`) supports multiple concurrent writers; REQUIRED for any parallel/multi-agent throughput. Atomic claim via `bd update <id> --claim` serializes acquisition | `[EXTERNAL-VERIFIED]` DOLT.md ; FAQ.md |
| Beads operational stability cost | Dolt-only line has documented instability (orphaned `dolt sql-server` daemons, nil-pointer panics in `bd ready`/`bd list`, migration PK forks blocking `bd dolt pull`) — a reliability-affecting performance consideration, not a throughput number | `[EXTERNAL-VERIFIED]` (FEASIBILITY-STUDY BD10; #2938) |
| Backlog.md single-trust-domain | Local-file/git-centric; single-writer-per-repo git model contends under true concurrent multi-user write load; one-task-per-agent/session discipline needed | `[EXTERNAL-VERIFIED]` github.com/MrLesk/Backlog.md ; package.json |
| Current pipeline gate evaluation | `gates.py` is pure-Python validation (no subprocess/LLM) — cheap, deterministic, runtime-agnostic; the most portable and lowest-overhead layer | `[CODE-VERIFIED]` `pipeline/gates.py:1-17`, `20-76` |
| Current parallel dispatch | `_run_parallel_steps()` runs a group in daemon threads with shared cancellation; `prd`/`eval` use `ThreadPoolExecutor` (eval default 8 workers, 1-15; prd `max_workers=min(steps,10)`) — the existing concurrency model the hybrid must preserve or improve | `[CODE-VERIFIED]` `pipeline/executor.py:402-452`; `eval/orchestrator.py:113-360`; `prd/executor.py:862-958` |

### 11.3 Performance-Critical Code (Current System — Levers to Preserve)

The hybrid's performance ceiling is set by how faithfully it preserves these existing levers. These are `[CODE-VERIFIED]`; their post-port performance is `[DESIGN — UNVERIFIED]`.

| Area | Optimization | Why It Matters | Location |
|------|-------------|----------------|----------|
| Subprocess prompt delivery | Prompt delivered via stdin (not argv) to avoid Linux `MAX_ARG_STRLEN` | Large prompts would fail on argv; stdin is the safe path the Mastra Workspace substitute must replicate | `pipeline/process.py:73-78`, `97-112` |
| Gate target selection | `_gate_target()` prefers sibling `.compressed.md` over original output | Gates validate what the downstream LLM actually consumes; cheaper + correct | `pipeline/executor.py:23-35` |
| Turn budgeting | `TurnLedger` pre-debits min allocation, reconciles after; budget-gated launches | Bounds cost/turn consumption per phase; the cost-control lever | `sprint/executor.py:927-1073`, `models.py:693-776` |
| Trailing (non-blocking) gates | Trailing-mode steps return PASS immediately; pending results collected at pipeline end | Avoids blocking the critical path on advisory checks — but `grace_period` defaults to 0, forcing BLOCKING in practice (must be preserved/flagged, not silently fixed) | `pipeline/executor.py:250-262`, `211-215` (§14 L2) |
| Result caching (audit) | Content-hash `ResultCache` (SHA-256) avoids re-running identical classifications | Skips redundant work; a reuse pattern the hybrid could extend | `audit/tool_orchestrator.py:61-224` |

### 11.4 Measurement Plan (Required Before Any Performance Claim) `[DESIGN — UNVERIFIED]`

Because nothing is measurable today, the only honest "performance" content is *how* the hybrid would be measured. The decisive early gate is G2 / SG1: prove Mastra durable subprocess supervision parity and rerun/recovery/durability (XC-12, XC-13).

| To be measured | Via | Gate | Tag |
|----------------|-----|------|-----|
| Mastra suspend/resume + partial-rerun overhead on a real SuperClaude tasklist | Time-boxed validation spike wrapping `superclaude tasklist validate` (smallest single strict-gate, non-destructive) | SG1 / Pilot G2 | `[DESIGN — UNVERIFIED]` (XC-12/XC-13) |
| Tasklist round-trip latency into Backlog.md + Beads | Round-trip parser validation spike | SG2 | `[DESIGN — UNVERIFIED]` (XC-12) |
| Beads server-mode + Dolt sync throughput on pinned version | `bd doctor` + backup/restore + push/pull smoke under load | SG3 | `[DESIGN — UNVERIFIED]` (XC-12) |
| Multi-tenant cost/identity overhead | Governance-plane prototype with per-invocation metering (model tokens + tool calls by tenant/team/task) | SG4 | `[DESIGN — UNVERIFIED]` (XC-12; cost attribution is non-native — RISK R8) |

> **Bottom line for Section 11:** Any reader seeking throughput, latency, or speedup numbers for the hybrid will find none here, by design — they do not exist and will not until the Phase 0-2 validation spike runs. The substrate-level concurrency and durability *directions* above are the most that current evidence supports.

---

## 12. Conventions & Patterns

The proposed hybrid inherits its conventions from the **existing Python orchestration core**, which is already contract-first, artifact-centric, and runtime-agnostic. The port preserves these patterns rather than inventing new ones; the few genuinely new conventions (work-of-record split, file-first carried into Backlog/Beads) are `[DESIGN]` and clearly marked. A developer or AI agent extending this architecture MUST follow these rules of the road.

### 12.1 Code Conventions

| Convention | Description | Anchor | Tag |
|------------|-------------|--------|-----|
| Runtime-agnostic core (NFR-007) | `pipeline/models.py`, `executor.py`, `gates.py` import only stdlib + pipeline-local symbols — **zero** imports from `sprint`/`roadmap`. Any new shared contract goes in `pipeline/`, never reaches up into a consumer. | `models.py:1-14`, `executor.py:7`, `gates.py:1-17` | `[CODE-VERIFIED]` |
| Pure-Python gates (NFR-003) | Gate validation never spawns a subprocess or calls an LLM. `gates.py` imports only `re`/`Path`/`GateCriteria`. New gates are pure data + pure functions returning `tuple[bool, str\|None]`. | `gates.py:1-17`, `gates.py:20-76` | `[CODE-VERIFIED]` |
| Prompt via stdin, not argv | `ClaudeProcess` delivers the prompt on stdin to dodge Linux `MAX_ARG_STRLEN`; never pass a large prompt as a CLI arg. | `process.py:76-78`, `136-139` | `[CODE-VERIFIED]` |
| Env hygiene at the seam | `build_env()` strips `CLAUDECODE`/`CLAUDE_CODE_ENTRYPOINT` before spawning the child so nested Claude detection does not misfire. | `process.py:97-112` | `[CODE-VERIFIED]` |
| Timeout sentinel `124` | A timed-out step returns exit `124` (matches bash `timeout`); callers branch on `124 → TIMEOUT`, nonzero → `FAIL`. | `process.py:163-165` | `[CODE-VERIFIED]` |
| Runner-authored truth | `TaskResult`/`StepResult` are constructed by the runner from observed exit codes/artifacts — **never** self-reported by the agent. Preserve this when porting. | `sprint/models.py:158-209`, `pipeline/executor.py:230-238` | `[CODE-VERIFIED]` |
| Always `--json` to Beads | Every `bd` invocation in the adapter uses `--json` (stable schema v1; opt into `BD_JSON_ENVELOPE=1` for the uniform envelope). Parse the envelope, never scrape human text. | web-03 `docs/JSON_SCHEMA.md` | `[EXTERNAL-VERIFIED]` |
| Backlog.md supported-fields only | Backlog.md MCP task schemas set `additionalProperties:false`; SuperClaude custom metadata MUST map to supported fields/body sections/docs, never arbitrary MCP props. | web-02 `src/mcp/tools/tasks/schemas.ts` | `[EXTERNAL-VERIFIED]` |
| Edit `src/superclaude/` first | Source-of-truth is `src/superclaude/`; `.claude/` and `plugins/superclaude/` are synced/mirror copies. Never ingest mirrors as canonical (see §14 D3, `plugins/` is a stale subset). | `core/CLAUDE.md:17-48` | `[CODE-VERIFIED]` |

### 12.2 Architectural Patterns

| Pattern | Where Used (BUILT) | Description | Tag |
|---------|--------------------|-------------|-----|
| **Single runtime seam** | `ClaudeProcess` behind the injected `StepRunner` protocol | The *only* `subprocess.Popen` / `claude --print` boundary in the pipeline package. The executor never touches a subprocess directly — it delegates through `run_step`. Swapping the Claude-CLI runtime for a Mastra-supervised one is a single substitution at this seam. | `process.py:24-244`, `executor.py:41-60` — `[CODE-VERIFIED]`; Mastra substitution — `[DESIGN — UNBUILT]` |
| **Generic step/gate pipeline core** | `execute_pipeline()` consumed by roadmap, tasklist, validate | One portable unit (`Step`) + one sequencer (`execute_pipeline`) with retry/gates/parallel dispatch; consumers inject a `run_step`. Nested `list[Step]` = parallel group. | `executor.py:63-188`, `models.py:108-123`; consumer proof `roadmap/executor.py:26`, `tasklist/executor.py:259-263` | `[CODE-VERIFIED]` |
| **Strangler-fig replatforming** | Roadmap (Phases 0-5, gates G0-G5) | Wrap one existing pipeline at a time behind a Mastra workflow that shells out to the current CLI; keep Python as the oracle; reimplement natively only after a step passes a parity gate. NOT a big-bang rewrite (Option B rejected). | ROADMAP Phase 1-3; cli-portify cautionary precedent | `[DESIGN — UNBUILT]` (target); precedent `[CODE-VERIFIED]` |
| **Python-as-oracle parity gating** | Phases 1-3 acceptance suites | At every phase the Mastra-wrapped verdict must equal the native CLI verdict (artifact/gate-mode/order/recovery parity) before native reimplementation is allowed. Gate G2 is the load-bearing exit: Mastra rerun/recovery must be demonstrated. | ROADMAP Gate G2/G3; FEASIBILITY §8 | `[DESIGN — UNBUILT]` |
| **Stable-ID contract** | sprint parser, tasklist protocol, deviation registry | `TASK-*`, `T<PP>.<TT>`, `D-####`, `D-CP...`, `R-###` are the cross-system sync keys. Adapters preserve IDs verbatim; idempotent imports are keyed on them. | `sprint/config.py:374-377`, `sc-tasklist-protocol/SKILL.md:161-164` — `[CODE-VERIFIED]`; cross-system reuse — `[DESIGN — UNBUILT]` |
| **Work-of-record split** | Proposed ownership matrix | Backlog.md owns prose/task/doc/decisions (primary human-readable work-of-record); Beads owns the dependency-graph mirror + agent memory + ready-queue + gates; Mastra owns run/trace/gate-execution state. Exactly one prose owner, one graph owner, one run owner. | ownership matrix (synthesis); web-02/web-03 | `[DESIGN — UNBUILT]` |
| **Fan-out → consolidate → verify** | prd, eval, audit | Tier-sized parallel fan-out (ThreadPoolExecutor), per-future exception → ERROR step (never dropped), then deterministic consolidation and a calibrated validation stage that asserts self-agreement (NOT ground-truth accuracy). | `prd/executor.py:862-958`, `eval/orchestrator.py:113-360`, `audit/validation.py:42-151` | `[CODE-VERIFIED]` |
| **File-first artifacts** | sprint, roadmap, MDTM tasks | Handoff state lives in the filesystem (release dir, task subdirs, `manifest.json`, `execution-log.jsonl`, checkpoint reports, `.compressed.md` sidecars). Gates validate the file the downstream LLM actually consumes (`.compressed.md` preferred over original). | `executor.py:23-35`, `02_mdtm_template_complex_task.md:718-731` — `[CODE-VERIFIED]`; carried into Backlog/Beads bodies — `[DESIGN — UNBUILT]` |
| **Numbered-checkpoint contract** | tasklist protocol + sprint checkpoint parser | Canonical form is numbered `### T<PP>.<NN> -- Checkpoint:` tasks with `Checkpoint Report Path: TASKLIST_ROOT/checkpoints/...`. The runtime parser accepts both numbered and legacy `### Checkpoint:`; new generators MUST emit the numbered form. | `sc-tasklist-protocol/SKILL.md:343-391`, `checkpoints.py:22-33` | `[CODE-VERIFIED]` |
| **Return-contract bridge** | cli-portify | Every path emits a `return-contract.yaml` (outcome / completed_steps / remaining_steps / suggested_resume_budget / resume_command) — the natural bridge to a Backlog/Beads reconciliation record. | `cli_portify/executor.py:283-372` — `[CODE-VERIFIED]`; Backlog/Beads bridge — `[DESIGN — UNBUILT]` |

### 12.3 Anti-Patterns (Things to Avoid)

| Anti-Pattern | Why It's Wrong | Do This Instead | Tag |
|--------------|----------------|-----------------|-----|
| Big-bang native rewrite (Option B) | XL effort + High risk; converts pure-Python reuse into rewrite-and-re-test; the in-house cli-portify code-gen-drift history is a direct warning. | Strangler-fig: wrap one pipeline, prove parity, then port. | `[DESIGN — UNBUILT]` / `[CODE-VERIFIED]` (precedent) |
| Second prose owner | Backlog.md + Beads both representing task status causes drift; their mutual integration is immature (Backlog FR #588). | Assign canonical owner per data class (one prose, one graph). | `[EXTERNAL-VERIFIED]` |
| Beads embedded mode for multi-agent | Embedded Dolt is single-writer ("database is locked"); concurrent agents corrupt/serialize. | Beads **server mode** + atomic `bd update --claim` + one-task-per-agent. | `[EXTERNAL-VERIFIED]` |
| Unpinned Beads/Dolt upgrades | v1.0.5 "do not upgrade" (migration 0043 breaks multi-machine sync, #4259); v1.0.4 server data-clobber. | Pin + gate versions; `bd doctor` + tested backup/restore in adoption gates. | `[EXTERNAL-VERIFIED]` |
| Treating MCP as governance | MCP is a tool-exchange protocol, explicitly NOT a governance platform; token passthrough is forbidden. | Add a dedicated control-plane (tenant registry, RBAC/ABAC, audit, cost) + MCP gateway with scoped tools. | `[EXTERNAL-VERIFIED]` |
| Telemetry into task bodies | High-volume `MonitorState` telemetry (bytes/tokens/turns/events) does not belong in the task-of-record. | Route telemetry → Mastra traces (with SuperClaude IDs as custom attributes); keep Backlog/Beads bodies lean. | `sprint/models.py:622-690` `[CODE-VERIFIED]` / `[DESIGN — UNBUILT]` |
| Scraping `plugins/` or `.claude/` as source | `plugins/superclaude/` is a stale, divergent subset (30 cmd / 20 agent / 1 skill vs 42/39/24); `.claude/` is sync output. | Ingest `src/superclaude/` only. | `core/CLAUDE.md:17-48` `[CODE-VERIFIED]` |
| Arbitrary MCP fields on Backlog tasks | Backlog.md MCP rejects unknown properties (`additionalProperties:false`). | Map metadata to supported fields/body sections/docs. | `[EXTERNAL-VERIFIED]` |

---

## 13. Extension Guide

> **CRITICAL:** These recipes are `[DESIGN — UNBUILT]` against the proposed hybrid. **No Mastra/Backlog.md/Beads integration exists at HEAD `9e864860`.** Each recipe is written as a strangler-fig increment: the *existing-side* files you hook into are real (`[CODE-VERIFIED]` paths); the Mastra/Backlog/Beads steps are the target design. Sequence them against the roadmap — read-only adapters (Phase 1) before wrapping a pipeline (Phase 2) before the parity port (Phase 3). Do not skip the parity gate.

### 13.1 Common Extension Tasks

#### Recipe A — Add a wrapped pipeline (strangler-fig increment)

**Goal:** Put an existing SuperClaude CLI pipeline behind a Mastra workflow without changing its behavior, proven at parity. **Start with the smallest:** `superclaude tasklist validate` — single LLM step, one strict gate, non-destructive (the Phase 2 pilot).

| # | Step | Existing-side file / registration point | Tag |
|---|------|------------------------------------------|-----|
| 1 | Pick the pipeline. Pilot = tasklist validate: one `tasklist-fidelity` Step gated by `TASKLIST_FIDELITY_GATE`, CLI pass/fail = `not _has_high_severity()`. | `tasklist/executor.py:191-218` (build_steps), `221-248` (`_has_high_severity`), `tasklist/gates.py:23-46` (gate) | `[CODE-VERIFIED]` |
| 2 | Identify the adapter contract = the `StepRunner` seam. The pipeline already routes execution through `execute_pipeline(..., run_step=...)`; the Mastra wrapper substitutes a workflow node that shells out to the existing CLI. | `pipeline/executor.py:41-60` (`StepRunner`), `63-188` (`execute_pipeline`); consumer `tasklist/executor.py:259-263` | seam `[CODE-VERIFIED]`; Mastra node `[DESIGN — UNBUILT]` |
| 3 | Build the Mastra workflow: `createWorkflow()` + one `createStep()` whose handler invokes `superclaude tasklist validate ...` via Workspace `executeCommand`. | Mastra `createWorkflow`/`createStep` (web-01); Workspace sandbox (web-01) | `[DESIGN — UNBUILT]` / `[EXTERNAL-VERIFIED]` |
| 4 | **Mirror the gate as the parity-gate step.** Re-express the CLI gate verdict as a Mastra scorer, then assert `Mastra verdict == native CLI verdict`. The native verdict comes from parsing `high_severity_count` from the report frontmatter. | `tasklist/executor.py:221-248`; gate semantics `pipeline/gates.py:20-76` | parity assertion `[DESIGN — UNBUILT]`; native verdict `[CODE-VERIFIED]` |
| 5 | Validate durability: suspend/resume + failed-step restart through Mastra `suspend()`/`resume()`/`resumeStream()`. **This is Gate G2 — the load-bearing exit.** | Mastra suspend/resume (web-01) | `[DESIGN — UNBUILT]` / `[EXTERNAL-VERIFIED]` |
| 6 | Run the subprocess-safety spike using the existing `eval/isolation.py` HOME-isolation model as the parity target (three-check containment guard). | `eval/isolation.py:224-260`, `456-747` | target `[CODE-VERIFIED]`; Mastra parity `[DESIGN — UNBUILT]` |
| 7 | Reconcile results back into Backlog.md + Beads via the return-contract bridge pattern. | `cli_portify/executor.py:283-372` (return-contract precedent) | bridge `[CODE-VERIFIED]`; Backlog/Beads write `[DESIGN — UNBUILT]` |

**Pitfalls:** Do NOT reimplement the gate logic in TypeScript on first pass — shell out and compare. Gate validates the `.compressed.md` sidecar if present (`executor.py:23-35`), so the Mastra scorer must target the same file. `grace_period=0` coerces declared `TRAILING` gates to BLOCKING (`executor.py:212-214`) — preserve that effective behavior, do not "fix" it silently.

#### Recipe B — Add a Beads gate (external-state barrier)

**Goal:** Encode a "done vs merged/validated/approved" barrier as a Beads gate so the graph blocks until an external condition clears. Maps the SuperClaude notion that a task can be code-complete but not merged/CI-green/approved.

| # | Step | Reference | Tag |
|---|------|-----------|-----|
| 1 | Choose the gate type. Beads supports: `gh:pr` (PR merged), `gh:run` (CI run), `timer` (elapsed time), `bead` (cross-rig dependency on another bead), `human` (manual approval). | web-03 `docs/DEPENDENCIES.md` | `[EXTERNAL-VERIFIED]` |
| 2 | Decide the SuperClaude barrier to map: roadmap validation pass → `bead`/`human`; PR-merge before phase-complete → `gh:pr`; CI green → `gh:run`; checkpoint soak → `timer`. | `roadmap/validate_executor.py:239-519`; sprint checkpoint model `sprint/checkpoints.py:36-112` | mapping `[DESIGN — UNBUILT]`; existing barriers `[CODE-VERIFIED]` |
| 3 | Create the gate via `bd gate` against the bead representing the task/phase; the bead stays out of `bd ready` until the gate clears. Discover/check with `bd gate check`/`bd gate discover`. | web-03 `docs/DEPENDENCIES.md` (`bd ready` = no open blocking deps) | `[EXTERNAL-VERIFIED]` |
| 4 | The Mastra workflow (or adapter poller) polls `bd ready --json`; only ready beads are dispatched. Claim atomically with `bd update --claim` (sets assignee + in_progress in one op). | web-03 CLI surface (`bd ready`, `bd update --claim`) | `[EXTERNAL-VERIFIED]` |
| 5 | Keep Beads gates orthogonal to the pure-Python `GateCriteria`/`gate_passed` artifact gates — Beads gates govern *graph readiness* (external state); Python gates govern *artifact correctness*. Do not conflate. | `pipeline/gates.py:20-76` | Python side `[CODE-VERIFIED]`; orthogonality `[DESIGN — UNBUILT]` |

**Pitfalls:** Cycles are rejected at write time — design dependency direction carefully. Multi-agent writers REQUIRE Beads server mode (embedded is single-writer). `gh:pr`/`gh:run` gates depend on GitHub state; rate-limit polling and handle transient failures. Pin the Beads version (avoid v1.0.5-class sync corruption).

#### Recipe C — Add a tenant (governance plane)

**Goal:** Onboard a new tenant to the multi-tenant control plane. **This is the heaviest recipe and depends on a layer that does NOT exist in any of the three components** — it is Phase 4 work, gated on decisions D1/D2/D3.

| # | Step | What the governance plane needs | Tag |
|---|------|----------------------------------|-----|
| 1 | Register the tenant in a **tenant registry** (the control-plane service — net-new; not Mastra/Backlog/Beads). | Separate control-plane service: tenant registry. None of the three components supplies this. | `[DESIGN — UNBUILT]` / `[EXTERNAL-VERIFIED]` (gap) |
| 2 | Map the five distinct identities: **trigger / execution / authorization / tenant / attribution.** Access-control bugs surface silently when execution + tenant are conflated; RBAC must be config-driven, not inferred from user messages. | web-04 scalekit access-control guidance | `[EXTERNAL-VERIFIED]` |
| 3 | Add tenant/actor fields to the run models — **they are absent today** (`PipelineConfig`/`SprintConfig`/`TaskResult`/`MonitorState`/`TurnLedger` carry model/permission/budget but no tenant/actor/audit identity). | `pipeline/models.py:212-234`, `sprint/models.py:347-510`, `692-777` | absence `[CODE-VERIFIED]`; new fields `[DESIGN — UNBUILT]` |
| 4 | Wire RBAC/ABAC + scoped MCP tools through an MCP/AI gateway: OAuth 2.1, audience binding, single-issuer pinning, **no token passthrough** (forbidden), granular scopes (no `superclaude:*` wildcard). | web-04 MCP security best practices; CSA minimum maturity | `[EXTERNAL-VERIFIED]` |
| 5 | Promote `TurnLedger` to a **tenant cost model**: per-invocation cost attribution + budget/rate enforcement (model tokens + tool calls by tenant/team/user/agent/workflow/task). Cost attribution is NOT native to MCP. | `sprint/models.py:692-777` (sprint-local ledger); web-04 FinOps | ledger `[CODE-VERIFIED]`; tenant cost model `[DESIGN — UNBUILT]` |
| 6 | Promote Beads to **server/shared mode with per-tenant prefixes**; enforce tenant isolation so no tenant can read another's tasks/traces/costs (Gate G4 NO-GO condition). | web-03 server mode; ROADMAP Phase 4 G4 | `[DESIGN — UNBUILT]` / `[EXTERNAL-VERIFIED]` |
| 7 | Re-validate isolation + audit + cost on a two-tenant test per onboarding (Gate G5 recurring). | ROADMAP Phase 5 G5 | `[DESIGN — UNBUILT]` |

**Pitfalls:** Production RBAC/SSO/FGA/audit/on-prem are **Mastra Enterprise-licensed**, not Apache-2.0 core (R1) — "multi-tenant on Mastra OSS" is false for production RBAC. Without auth, Mastra Studio/API routes are public. Do NOT deploy company-wide on the three components alone — the control-plane service is mandatory and net-new.

### 13.2 Testing Requirements for Changes

| Change Type | Required Tests | Reference (existing harness to reuse) | Tag |
|-------------|----------------|----------------------------------------|-----|
| Wrap a pipeline (Recipe A) | Round-trip parser parity; Mastra verdict == native CLI verdict; suspend/resume + failed-step restart; subprocess-safety parity report. | `cli/eval` harness (`eval/orchestrator.py`, `eval/isolation.py`, `eval/runner.py`); round-trip vs `discover_phases()`/`parse_tasklist_file()` (`sprint/config.py`) | harness `[CODE-VERIFIED]`; parity suite `[DESIGN — UNBUILT]` |
| Add a Beads gate (Recipe B) | Cycle-rejection test; `bd ready` excludes gated beads until cleared; atomic `--claim` under concurrent writers (server mode); version-pinned `bd doctor` + backup/restore smoke. | web-03 CLI contracts; reuse eval forensic JSONL + retry-once for flaky steps (`eval/retry.py`) | `[EXTERNAL-VERIFIED]` / `[DESIGN — UNBUILT]` |
| Add a tenant (Recipe C) | Two-tenant isolation test (no cross-tenant read of tasks/traces/costs); per-invocation audit record assertion; cost-attribution join via trace IDs; token-passthrough negative test. | net-new; no existing test covers tenancy (absence is the finding) | `[DESIGN — UNBUILT]` / `[EXTERNAL-VERIFIED]` |
| Port a deterministic step natively | Artifact + gate-verdict + gate-mode + order + recovery/resume parity vs the Python oracle BEFORE replacing the shell-out. | `cli/eval` return-contract/artifact diffing; gate semantics `pipeline/gates.py` | parity `[DESIGN — UNBUILT]`; oracle `[CODE-VERIFIED]` |

---

## 14. Known Limitations & Technical Debt

> **CRITICAL — overall status:** The Mastra + Backlog.md + Beads hybrid architecture is **UNBUILT**. No source file at HEAD `9e864860` implements any Mastra/Backlog.md/Beads integration. The feasibility verdict is **Conditionally Recommended**, approach **Option D → Option A** (a time-boxed validation spike — Phases 0-2 / Gates G0-G2 — *then* hybrid adapter-first, only if the spike exit gates SG1-SG4 pass; NOT a native rewrite, NOT Backlog/Beads-only). Confidence ≈70% that hybrid is feasible; ≈55% that full company-wide multi-tenant is deliverable on the three components alone. Deferral is a legitimate outcome. `[DESIGN — UNBUILT]`

### 14.1 Current Limitations (BUILT-side gaps the port must carry, not silently fix)

These are real `[CODE-VERIFIED]` behaviors in the existing orchestrator at HEAD `9e864860`. The roadmap mandates **preserving and flagging** them (state effective-vs-intended separately), not normalizing them during the port.

| # | Limitation | Impact | Anchor | Tag |
|---|-----------|--------|--------|-----|
| L1 | **`CERTIFY_GATE` defined but NOT wired.** `CERTIFY_GATE`/`build_certify_step`/`check_certify_resume` exist; `_build_steps()` terminates at `remediate`; the "Step 12 (certify) constructed dynamically by roadmap_run_step" comment has **zero production callsites**. | Certification gate does not run in production roadmap; downstream "certified" frontmatter is never enforced. Port must preserve the gap (do not auto-wire). | def `roadmap/gates.py:1324-1351`; absent `executor.py:1947-2208`; comment `executor.py:2205`; `ALL_GATES` ref `gates.py:1440` | `[CODE-VERIFIED]` |
| L2 | **Wiring-verification grace=0 → effectively BLOCKING.** `wiring-verification` Step declares `gate_mode=TRAILING` ("shadow mode trailing") but `PipelineConfig.grace_period` defaults to 0 with no CLI override, and `_execute_single_step` coerces `grace_period==0 → BLOCKING`. | The gate runs synchronously/blocking in production despite shadow-trailing intent. Effective behavior ≠ declared behavior. | TRAILING `executor.py:2183`; default `pipeline/models.py:232`; coercion `pipeline/executor.py:211-214` | `[CODE-VERIFIED]` |
| L3 | **Path A skips `_verify_checkpoints()`.** The per-task (parsed) branch aggregates results and `continue`s at `executor.py:1301` with no checkpoint call. The sole `_verify_checkpoints()` call site is `executor.py:1519`, inside the Path B (freeform) branch only. | Checkpoint enforcement does not run for parsed-task phases — silent loss of checkpoint gating on the most common sprint path. Phase 3 must wire it into the per-task path. | Path A `executor.py:1262-1301`; sole call `executor.py:1519`; def `executor.py:1811` | `[CODE-VERIFIED]` |
| L4 | **Deviation classifier UNWIRED.** All deviation records render as `UNCLASSIFIED`; `DEVIATION_ANALYSIS_GATE` actually pins the invariant `unclassified_count == total_analyzed`. | The classifier is not producing classified output in production; the gate encodes the unwired state as the expected state. | `roadmap/executor.py:1603-1609`; gate `gates.py:1390-1422` | `[CODE-VERIFIED]` |
| L5 | **Partial / unused isolation in sprint.** Four-layer `IsolationLayers`/`setup_isolation` EXISTS but is not called in the main loop; Path B only sets `CLAUDE_WORK_DIR`, Path A passes no isolation env. Base process `Popen` has no `cwd` arg, so worker cwd is not guaranteed on Path A. | Sprint isolation guarantees are weaker than the code implies; the Mastra safety-parity target (eval HOME-isolation) is the stronger model to port toward. | `executor.py:106-182`, `1303-1324`, `1076-1115`; `process.py:125-134` | `[CODE-VERIFIED]` |
| L6 | **Stubbed sprint `status`/`logs`.** `SprintLogger` writes JSONL+Markdown (real), but `read_status_from_log`/`tail_log` are STUBS ("not yet connected") — the `status`/`logs` commands do not report live state. | Operator visibility into a running sprint is limited to the TUI/tmux; CLI status/logs are non-functional. | `sprint/logging_.py:13-213`, `224-235` | `[CODE-VERIFIED]` |
| L7 | **Path A turn-counting accuracy gap.** `_run_task_subprocess` returns `turns_consumed=0`; turn counting is wired separately, so per-task turn attribution is approximate. | Budget reconciliation on Path A is imprecise — relevant when promoting `TurnLedger` to a tenant cost model. | `executor.py:1086-1115`; `sprint/models.py:502-506` | `[CODE-VERIFIED]` |
| L8 | **`sprint rerun-tasks` is ABSENT at HEAD.** Tree-wide grep for `rerun-tasks`/`rerun_tasks` returns zero matches; the sprint Click group registers exactly `run/attach/status/logs/kill/verify-checkpoints`. The operator-memory note (v4.3.0) does not correspond to this commit (package is v4.2.0). | Any tech reference or recipe written against HEAD `9e864860` must state `rerun-tasks` ABSENT; the closest recovery surface is `verify-checkpoints` (checkpoint recovery only, not task re-run). | `sprint/commands.py` (6 subcommands, no `rerun`); resolved in spot-03 | `[CODE-VERIFIED]` (absence) |

### 14.2 Technical Debt — Stale / Contradiction Findings (confirmed at HEAD)

Documentation/comment/template drift confirmed against current source. Severity reflects risk that a port silently carries the *stale* statement instead of the *effective* behavior.

| # | Debt item | Severity | Description | Anchor | Tag |
|---|-----------|----------|-------------|--------|-----|
| D1 | Stale `### Checkpoint:` in sprint prompt | Medium | Path B freeform prompt tells the agent to scan for legacy `### Checkpoint:` sections and skip if none exist; does not mention the numbered task-form contract. Stale-but-harmless (Path A never uses this prompt) but misleads a port author. | `sprint/process.py:188-195` | `[CODE-VERIFIED]` |
| D2 | Stale `### Checkpoint:` in verify-checkpoints message | Low | `verify-checkpoints` empty-manifest message names only `` `### Checkpoint:` `` sections; omits `Checkpoint Report Path:` declarations the parser actually supports. | `sprint/commands.py:426` | `[CODE-VERIFIED]` |
| D3 | `src/` vs `plugins/` source-of-truth conflict | High | `core/CLAUDE.md` designates `src/superclaude/` canonical (42 cmd / 39 agent / 24 skill), but `commands/agents/hooks` READMEs say edit `plugins/superclaude/` first. `plugins/` is a materially out-of-sync subset (30/20/1). Ingesting the mirror as canonical would port a stale corpus. | `core/CLAUDE.md:17-48` vs `commands/README.md`, `agents/README.md`, `hooks/README.md`; counts in spot-04 | `[CODE-VERIFIED]` (contradicted) |
| D4 | `_build_steps` "9-step" docstring + duplicate "Step 8" labels | Low | `_build_steps` docstring still says "9-step pipeline" vs 12 wired list elements; inline comments label both spec-fidelity and test-strategy as "Step 8". Cosmetic — ordering is correct and matches research. | `roadmap/executor.py:1948`, `2140`, `2157` | `[CODE-VERIFIED]` |
| D5 | `TrailingGateResult` SPEC-DEVIATION shape | Low | Current shape `(step_id, passed, evaluation_ms, failure_reason)` (roadmap v3.0 authoritative); the older spec `(passed, evaluation_ms, gate_name)` is STALE. Docstring records the deviation. | `pipeline/trailing_gate.py:34-46` | `[CODE-VERIFIED]` (doc-contradicted) |
| D6 | Roadmap "ORIGINAL output file" comment | Low | Roadmap comment says "Gate checks run on the ORIGINAL output file" but `_gate_target()` prefers the `.compressed.md` sidecar. | `roadmap/executor.py:1217-1219` vs `pipeline/executor.py:23-35` | `[CODE-VERIFIED]` (contradicted) |
| D7 | cli-portify resume matrix drift | Medium | `cli_portify/resume.py` legacy matrix uses conceptual step names (analyze-workflow/design-pipeline/synthesize-spec) NOT the current `STEP_REGISTRY` IDs; resume validation contradicts the live registry. Retire duplicated resume matrices on port. | `cli_portify/resume.py:45-95`, `168-198` vs `executor.py:105-183` | `[CODE-VERIFIED]` (contradicted) |
| D8 | cleanup-audit parallel-batch docstring | Low | Docstring claims ThreadPoolExecutor parallel batch dispatch but code runs sequentially (no import); `--pass`/`--batch-size` flags accepted but not applied. | `cleanup_audit/executor.py:11-13`, `72-159`; `commands.py:24-40` | `[CODE-VERIFIED]` (contradicted) |
| D9 | Seed-brief substrate corrections | Medium | Seed-brief framing corrected by web research: Beads is **Dolt-first** (not SQLite+JSONL; `.beads/issues.jsonl` is export-only); `superclaude pipeline` is a shared package, NOT a root Click command; sprint prompt invokes `/sc:task` (not `/sc:task-unified`); ClaudeProcess uses stdin (not argv `-p`). | web-03 `SYNC_CONCEPTS.md`/`DOLT.md`; `cli/main.py:400-426`; `sprint/process.py:170`; `pipeline/process.py:114-147` | `[EXTERNAL-VERIFIED]` / `[CODE-VERIFIED]` |

### 14.3 Technical Debt — Risk Register (R1-R9) and the Four Critical Gaps

The port's debt is dominated by the validated risk register. **Severity** = Impact × Likelihood per RISK-REGISTER.md.

| # | Risk | Severity | Description | Critical-gap link | Tag |
|---|------|----------|-------------|-------------------|-----|
| R1 | License | **High** | Production multi-user RBAC/SSO/FGA/audit/on-prem are Mastra **Enterprise**-licensed (`ee/` dirs), not Apache-2.0 core. Strategic multi-tenant driver hits a budget/procurement gate. | G7 (auth/RBAC/governance/cost) | `[EXTERNAL-VERIFIED]` |
| R2 | Runtime migration | **High** | ~65K-LOC Python orchestration must replatform onto Mastra TS; the `ClaudeProcess` subprocess seam must be replaced; gate/convergence logic is pure Python (rewrite-and-re-test risk). | **G3** (subprocess/Claude-Code parity) | `[CODE-VERIFIED]` (risk) |
| R3 | Backlog/Beads overlap | **High** | Dual task/status owners cause drift; mutual integration immature (Backlog FR #588). Assign canonical owners (D1). | — | `[EXTERNAL-VERIFIED]` |
| R4 | Beads/Dolt version churn | **High** | v1.0.5 "do not upgrade" sync corruption (migration 0043, #4259); v1.0.4 server data-clobber. Pin + gate versions; tested backup/restore. | — | `[EXTERNAL-VERIFIED]` |
| R5 | Concurrency / multi-writer | **High** | Beads embedded mode is single-writer; multi-agent needs server mode; session attribution churning (#3400/#3583). Atomic `--claim` + one-task-per-agent. | — | `[EXTERNAL-VERIFIED]` |
| R6 | Subprocess / hook safety parity | **High** | Mastra Workspace `executeCommand` does NOT replicate Claude Code hooks/freshness/staging/permissions; UV-only, git-safety, `.claude/` SoT, fork-PR target must be rebuilt as middleware. | **G3** + **G4** (hook/safety parity) | `[EXTERNAL-VERIFIED]` |
| R7 | Checkpoint / wiring drift | **Medium-High** | Stale legacy `### Checkpoint:` refs (D1/D2 above), per-task skips `_verify_checkpoints()` (L3), certify maybe unwired (L1), trailing grace=0 forces blocking (L2). Adopt numbered contract; state effective-vs-intended. | — | `[CODE-VERIFIED]` (risk) |
| R8 | Governance / tenancy / cost gaps | **High** | None of the three components supplies tenant isolation, per-invocation audit, cost attribution, policy/approval/catalog. MCP is a protocol, not governance. Net-new control-plane required. | **G6** (tenant state) + **G7** (auth/RBAC/governance/cost) | `[EXTERNAL-VERIFIED]` |
| R9 | Fast-moving external tools | **Medium-High** | Mastra `@core` 1.1.0+ / Temporal experimental; Backlog v1.45.2 MVP + doc drift + bug #578; Beads 1.x frequent CLI/API changes. Pin versions; runtime-verify schemas. | — | `[EXTERNAL-VERIFIED]` |

**The four Critical gaps** cluster into two areas:

| Gap | Description | Maps to | Tag |
|-----|-------------|---------|-----|
| **G3** | Subprocess / Claude-Code execution parity cannot be assumed portable — the `ClaudeProcess` seam + Claude-Code-native runtime behavior. | R2 / R6 | `[CODE-VERIFIED]` (linkage) / `[EXTERNAL-VERIFIED]` |
| **G4** | Hook / safety parity (UV-only, freshness, staging, fork-PR, permissions) is not provided by Mastra defaults. | R6 | `[CODE-VERIFIED]` / `[EXTERNAL-VERIFIED]` |
| **G6** | Tenant state — current models carry no tenant/actor/audit identity (`PipelineConfig`/`SprintConfig`/`TaskResult`/`MonitorState`/`TurnLedger`). | R8 | `[CODE-VERIFIED]` (absence) |
| **G7** | Auth / RBAC / governance / cost control plane does not exist in any of the three components. | R1 / R8 | `[EXTERNAL-VERIFIED]` |

### 14.4 Future Considerations (deferred by design)

| Item | Deferred Because | Revisit When | Tag |
|------|------------------|--------------|-----|
| Native (non-shell-out) reimplementation of deterministic steps | Hybrid keeps Python as the oracle; native conversion concentrates parity risk. | Only per-step, after that step passes the Phase 3 parity suite. | `[DESIGN — UNBUILT]` |
| Full multi-tenant control plane | EE-licensing (D2) + governance-ownership (D3) decisions unresolved; ≈55% confidence on three components alone. | Phase 4, gated on D1+D2+D3 and a passing two-tenant isolation/audit/cost test (G4). | `[DESIGN — UNBUILT]` / `[EXTERNAL-VERIFIED]` |
| `roadmap run` + sprint wrap | Too much surface for a first slice; pilot is `tasklist validate`. | Phase 3, after Gate G2 (Mastra durability/rerun/recovery) passes. | `[DESIGN — UNBUILT]` |
| Backlog.md ↔ Beads native sync | Integration immature (FR #588); maintainer suggests a narrow import/export decision first. | After D1 (primary work-of-record) is recorded; start with one narrow sync workflow. | `[EXTERNAL-VERIFIED]` |
| Five gating decisions D1-D5 | Phase 0 outputs; all later mappings depend on them. | Phase 0 / Gate G0 (D1 + D4 mandatory before Phase 1). | `[DESIGN — UNBUILT]` |

---

## 15. Verification & Accuracy *(Mandatory)*

> **This section ensures the Technical Reference stays accurate.** Every fact in this document is verifiable against (a) the actual SuperClaude codebase at HEAD `9e864860` for `[CODE-VERIFIED]` claims, (b) the feasibility evidence base for `[DESIGN — UNBUILT]` claims, and (c) upstream documentation for `[EXTERNAL-VERIFIED]` claims.
>
> **CRITICAL — read before trusting any architectural claim:** This document describes a **PROPOSED, not-yet-built** architecture. The hybrid Mastra + Backlog.md + Beads system **does not exist in this repository**. No source file implements any Mastra, Backlog.md, or Beads integration today. The single most important integrity control in this document is the **Built-vs-Design Status Ledger** in §15.3 — consult it before treating any subsystem as implemented.

### 15.1 Verification Log

Record of each verification of this document against ground truth. The `[CODE-VERIFIED]` (BUILT) side was verified against the live codebase at the commit below; the `[DESIGN — UNBUILT]` and `[EXTERNAL-VERIFIED]` sides were verified against the cited feasibility artifacts and upstream documentation.

| Date | Verified By | Code Version / Commit | Sections Verified | Issues Found |
|------|------------|----------------------|-------------------|-------------|
| 2026-06-03 | `tech-reference` skill (Phase 2 adapted: ingest + 4 targeted spot-check code-tracers) | `9e864860` (`9e8648603636d6b9f8fab9e261e583d0de849f34`; package v4.2.0) | §5.1-5.8 subsystems, §15 Built-vs-Design Ledger, all `[CODE-VERIFIED]` `path:line` anchors | **0 code drift.** Spot-check totals: pipeline-core seam 80/80 CONFIRMED, 0 DRIFTED, 0 NOT-FOUND (spot-01); roadmap/tasklist 4/4 targets CONFIRMED (spot-02); sprint/checkpoint 3/3 CONFIRMED (spot-03); harness counts 42/39/24 CONFIRMED exact (spot-04). Line anchors accurate within ±0-2 lines. Pre-existing in-repo staleness preserved (not fixed) per design-reference scope. |

**Phase-2 spot-check protocol used (this verification):** The standard skill's fresh parallel codebase investigation was *adapted* — the 11 pre-completed code-traced research files (`TASK-RESEARCH-20260602-211124/research/01..11`) were ingested as the verified evidence base, then **4 targeted spot-check agents** re-read the load-bearing seam files at HEAD `9e864860` to confirm the research claims still hold (confirm-or-flag, not re-investigation):

| Spot-check | Files re-read at HEAD | Result |
|------------|-----------------------|--------|
| spot-01 (pipeline-core seam) | `cli/pipeline/{models,executor,gates,process,trailing_gate,deliverables}.py` | 80/80 symbol/line claims CONFIRMED; `ClaudeProcess` confirmed as the single runtime seam |
| spot-02 (roadmap/tasklist) | `cli/roadmap/{executor,gates}.py`, `cli/tasklist/{executor,gates}.py` | `_build_steps()` order, `CERTIFY_GATE` unwired, wiring-verification grace=0→BLOCKING, `TASKLIST_FIDELITY_GATE` all CONFIRMED |
| spot-03 (sprint runtime) | `cli/sprint/{executor,config,checkpoints,process,commands}.py` | Path A skips `_verify_checkpoints()` CONFIRMED; dual-shape checkpoint contract CONFIRMED; **`sprint rerun-tasks` resolved ABSENT at HEAD** (research file 11 correct; v4.3.0 operator-memory note does not reflect this commit) |
| spot-04 (harness corpus) | `src/superclaude/{commands,agents,skills,core,hooks}/` | 42 commands / 39 agents / 24 skills CONFIRMED exact; `src/superclaude/` confirmed canonical, `plugins/superclaude/` a divergent stale mirror (30/20/1) |

> **Note — pre-existing staleness was deliberately preserved, not corrected.** This is a design reference against an *unbuilt* target, not a code-cleanup pass. Known in-repo drift surfaced during verification (e.g. roadmap `_build_steps` docstring still says "9-step pipeline" while 12 steps are wired; stale `### Checkpoint:`-only prompt text in `sprint/process.py`; `src/` vs `plugins/` source-of-truth README conflict; deviation classifier renders all records UNCLASSIFIED) is documented as-found in §14 and the ledger, **not** silenced. A future maintainer must not treat its presence here as an endorsement to "fix and re-baseline" without a separate decision.

### 15.2 Spot-Check Protocol

How a future maintainer re-verifies this document. Because the architecture spans a BUILT side (real code) and a DESIGN/EXTERNAL side (proposed integration + upstream tools), the protocol has three lanes — one per tag. Run the BUILT lane on every code-version bump; run the DESIGN/EXTERNAL lanes whenever the feasibility study, roadmap, or upstream tool versions change.

**Lane A — `[CODE-VERIFIED]` claims (BUILT side, against current `src/superclaude/`):**

1. **Capture HEAD.** Record the current commit (`git rev-parse HEAD`). If it differs from §15.1's `9e864860`, every `path:line` anchor below may have drifted and must be re-checked.
2. **File existence check.** Confirm the seam files still exist: `cli/pipeline/{models,executor,gates,process,trailing_gate,deliverables}.py`, `cli/roadmap/{executor,gates}.py`, `cli/tasklist/{executor,gates}.py`, `cli/sprint/{executor,config,checkpoints,process,commands}.py`.
3. **Single-seam check.** Confirm `ClaudeProcess` is still the only `subprocess.Popen` / `claude --print` boundary in `cli/pipeline/` (`grep -rn "subprocess.Popen\|claude --print" src/superclaude/cli/pipeline/`). If a second runtime boundary appears, §5.1/§5.6 are stale — the strangler-fig premise (one seam to replace) no longer holds.
4. **Wiring invariants check.** Re-confirm the four load-bearing structural facts that the design depends on, since "preserve, do not normalize" guidance assumes they are still true: (a) `CERTIFY_GATE` defined in `roadmap/gates.py` but absent from `roadmap/executor.py::_build_steps()`; (b) wiring-verification declares `GateMode.TRAILING` but `PipelineConfig.grace_period` defaults to `0` (coerced to BLOCKING); (c) sprint Path A (per-task) does not call `_verify_checkpoints()`; (d) `CHECKPOINT_HEADING_PATTERN` accepts both numbered and legacy headings.
5. **Corpus-count check.** Re-count `src/superclaude/{commands/*.md, agents/*.md, skills/*/SKILL.md}`; the design's "instruction-IP reuse" claim (§5.4) assumes 42/39/24. Confirm `src/superclaude/` is still canonical vs the `plugins/superclaude/` mirror.
6. **Absence check.** Re-confirm the *negative* facts the design relies on: no Mastra/Backlog.md/Beads import anywhere in `src/` (`grep -rn "mastra\|backlog\|beads" src/superclaude/`); no tenant/actor/audit identity field in `PipelineConfig`/`SprintConfig`/`TaskResult`; no `sprint rerun-tasks` subcommand. If any of these now exist, the BUILT/DESIGN boundary in §15.3 has moved and the ledger must be updated.

**Lane B — `[DESIGN — UNBUILT]` claims (against the feasibility evidence base):**

7. **Provenance check.** Every `[DESIGN]` claim must trace to a feasibility artifact (`FEASIBILITY-STUDY.md`, `DECISION-SUMMARY.md`, `ROADMAP.md`, `RISK-REGISTER.md`) or a research file — never to integrated code. Spot-check 3-5 design claims (e.g. the 4 adapter contracts, the work-of-record split, the spike exit gates SG1-SG4) and confirm the cited source still says what the document attributes to it.
8. **"Never presented as built" check.** Scan §5.5, §5.6, §5.8 and §11 for any sentence that reads as though the hybrid system exists. Design claims must use conditional/proposed phrasing and carry the `[DESIGN — UNBUILT]` tag.

**Lane C — `[EXTERNAL-VERIFIED]` claims (against upstream documentation):**

9. **Version-pin check.** Re-verify the pinned upstream facts against current upstream docs, since these tools move fast: Mastra RBAC/SSO/FGA/audit are Enterprise-licensed (`@mastra/core/auth/ee`, Apache-2.0 core); Backlog.md MCP uses `additionalProperties:false`; Beads is Dolt-first with a `v1.0.5` "do-not-upgrade" caution. A changed upstream capability can invalidate a design decision (D1-D5) or risk (R1-R9).
10. **Integration-does-not-exist check.** Confirm `[EXTERNAL-VERIFIED]` is never silently upgraded to `[CODE-VERIFIED]`: the upstream *component* existing does not mean the *integration* exists. Cross-check against Lane A step 6.

### 15.3 Built-vs-Design Status Ledger

> **CRITICAL — this is the single most important integrity control in the document.** One row per subsystem (§5.1-§5.8). The **Status** column states unmistakably what exists in *this repository today* versus what is *proposed*. Read this ledger before treating any subsystem as implemented. The hybrid Mastra + Backlog.md + Beads system is **not built**; only the existing SuperClaude Python orchestration layer that the port would *reuse/adapt* is real code.

**Status vocabulary:**

- **BUILT** — fully implemented and shipping in this repo at HEAD `9e864860`; verified by code-traced spot-check.
- **partially-built-seam** — a real, shipping code seam exists and is the substitution point, but its *replacement* by the target stack is unbuilt; the BUILT portion is the integration boundary, not the integration.
- **DESIGN-only** — proposed architecture; **no implementing code exists in this repo**. Evidence is the feasibility study / research, not source.
- **EXTERNAL-component-exists-integration-design-only** — the upstream tool genuinely exists and its capabilities are documented, but **no integration into this repo exists**; only the integration *design* is described here.

| Subsystem | Name | Status | Evidence anchor | Tag |
|-----------|------|--------|-----------------|-----|
| **5.1** | Pipeline-core seam (step/gate/process kernel) | **BUILT** | `cli/pipeline/models.py:1-234`, `executor.py:1-469` (`execute_pipeline`, `StepRunner` protocol `41-60`), `gates.py:1-142`, `process.py:24-244` (`ClaudeProcess`), `trailing_gate.py:1-648`, `deliverables.py:1-194`. Spot-01: 80/80 CONFIRMED, 0 drift. `ClaudeProcess` is the sole `subprocess.Popen`/`claude --print` boundary. | `[CODE-VERIFIED]` |
| **5.2** | Roadmap & tasklist workflows | **BUILT** (workflows) — target migration mapping is **DESIGN-only** | `cli/roadmap/executor.py::_build_steps()` 12-step DAG `1947-2208`, `roadmap/gates.py:1020-1441` (14-entry `ALL_GATES` registry), `tasklist/executor.py:191-218` + `tasklist/gates.py:23-46` (`TASKLIST_FIDELITY_GATE`). Spot-02: `_build_steps` order, `CERTIFY_GATE` unwired (`gates.py:1324-1351`, absent from wired steps), wiring grace=0→BLOCKING (`executor.py:2183` + `pipeline/models.py:232` + `executor.py:213-214`) all CONFIRMED. Mastra-mapping = feasibility inference only. | `[CODE-VERIFIED]` (built) + `[DESIGN — UNBUILT]` (mapping) |
| **5.3** | Sprint execution runtime (hardest port) | **BUILT** (runtime) — target migration mapping is **DESIGN-only** | `cli/sprint/executor.py::execute_sprint()` `1135-1757`, dual-path A/B `1259-1457`, `config.py` parser `52-492`, `checkpoints.py:1-408`, `process.py` subclass. Spot-03: Path A skips `_verify_checkpoints()` (sole call `executor.py:1519`, Path B only) CONFIRMED; `CHECKPOINT_HEADING_PATTERN` dual-shape `checkpoints.py:30-33` CONFIRMED; **`sprint rerun-tasks` ABSENT at HEAD** (group registers only run/attach/status/logs/kill/verify-checkpoints). | `[CODE-VERIFIED]` (built) + `[DESIGN — UNBUILT]` (mapping) |
| **5.4** | Reusable harness corpus (skills/agents/templates/hooks/MCP) | **BUILT** (instruction IP) — target reuse-via-adapter is **DESIGN-only** | `src/superclaude/`: 42 commands, 39 agents, 24 skills (spot-04 CONFIRMED exact), `core/` 12 `.md`, `hooks/hooks.json` (2110B), `mcp/configs/*`. `src/superclaude/` canonical; `plugins/superclaude/` is a divergent stale mirror (30/20/1) and NOT canonical. Tool-invocation vocabulary assumes Claude Code tools → adapter required. | `[CODE-VERIFIED]` (corpus) + `[DESIGN — UNBUILT]` (target reuse) |
| **5.5** | Target data model & ownership (work-of-record split, stable-ID join) | **DESIGN-only** (current contracts/stable-ID *formats* are BUILT; the cross-system ownership split + join is proposed) | DESIGN: ownership matrix + 4 adapter contracts (`07-target-data-model-and-ownership.md`, synthesis). BUILT substrate it builds on: `Step` model `pipeline/models.py:108-123`, stable-ID formats `TASK-*`/`T<PP>.<TT>`/`D-####`/`R-###` (`sc-tasklist-protocol/SKILL.md:161-164`, `sprint/config.py:374-377`). Absence: no tenant/actor/audit identity in current models. | `[DESIGN — UNBUILT]` (ownership/join) + `[CODE-VERIFIED]` (ID formats, absence) |
| **5.6** | Adapter / seam-replacement layer (Mastra step = `StepRunner`; CLI shell-out hybrid) | **DESIGN-only** | DESIGN: 4 adapter contracts (`07-...`), Mastra-step-as-`StepRunner` substitution, hybrid CLI shell-out (`FEASIBILITY-STUDY.md` §8, `ROADMAP.md` Phases 1-3). **No source file implements any Mastra/Backlog.md/Beads integration** (`04-cli-portify-prd-cleanup-audit-eval.md` row 5.6-27, absence across scope). Reuses BUILT orchestration patterns (cli_portify `STEP_REGISTRY`, `return-contract.yaml` `cli_portify/executor.py:283-372`) as the migration method. | `[DESIGN — UNBUILT]` |
| **5.7** | External component substrate (Mastra / Backlog.md / Beads / MCP) | **EXTERNAL-component-exists-integration-design-only** | EXTERNAL (component exists upstream, integration does NOT): Mastra durable `suspend()/resume()` + `WorkspaceSandbox` (mastra.ai/docs/workflows/suspend-and-resume; reference/workspace/sandbox); Backlog.md CLI/MCP `additionalProperties:false` (github.com/MrLesk/Backlog.md; src/mcp/tools/tasks/schemas.ts); Beads `bd ready/create/--claim`, Dolt-first (github.com/gastownhall/beads; docs/DOLT.md). BUILT seam being replaced: `ClaudeProcess` `pipeline/process.py:73-147`. | `[EXTERNAL-VERIFIED]` (capabilities) + `[CODE-VERIFIED]` (seam) |
| **5.8** | Governance / multi-tenant control plane | **DESIGN-only — NOT PROVIDED by any of the three components** | DESIGN/gap: none of Mastra/Backlog.md/Beads supplies tenant isolation, per-invocation audit, cost attribution, policy/approval/catalog; MCP is explicitly not a governance layer (`web-04-mcp-multitenancy-governance.md`; modelcontextprotocol.io/docs/concepts/architecture). An additional control-plane layer is required (5 agent identities; scalekit.com access-control-multi-tenant-ai-agents). BUILT gap evidence: `TurnLedger` is sprint-local budget only (`sprint/models.py:692-777`); no tenant/actor identity in scoped models. | `[EXTERNAL-VERIFIED]` (gap facts) + `[DESIGN — UNBUILT]` (proposed plane) + `[CODE-VERIFIED]` (absence) |

**Ledger reading rule:** Subsystems **5.1, 5.2, 5.3, 5.4 are BUILT** (the existing SuperClaude Python orchestration layer — pipeline seam, roadmap/sprint workflows, harness corpus — that the port reuses/adapts). Subsystems **5.5, 5.6, 5.8 are DESIGN-only** (data model, adapter layer, governance plane — proposed, no implementing code in this repo). Subsystem **5.7 exists upstream** (Mastra/Backlog.md/Beads are real tools) **but its integration is design-only**. Nowhere in this repository does the hybrid system run.

### 15.4 Evidence Trail

This Technical Reference was assembled from the research + synthesis artifacts below (all under `.dev/tasks/to-do/`). `[CODE-VERIFIED]` claims trace to the spot-checks; `[DESIGN — UNBUILT]` to the research/feasibility files; `[EXTERNAL-VERIFIED]` to the web-research files.

| Artifact | Role |
|----------|------|
| `TASK-RESEARCH-20260602-211124/research/01-pipeline-core-contracts.md` .. `11-*.md` | 11 code-traced research files (the BUILT-side evidence base) |
| `TASK-TECHREF-20260603-021348/research/00-evidence-index.md` | 243-row evidence index (5.1-5.8 + XC cross-cutting facts) |
| `TASK-TECHREF-20260603-021348/research/spot-01..04` | 4 targeted spot-checks re-confirming load-bearing seam facts at HEAD `9e864860` |
| `TASK-RESEARCH-20260602-211124/research/web-01..04` | Tavily/Context7 external capability files (Mastra, Backlog.md, Beads, MCP/governance) |
| `TASK-RESEARCH-20260602-211124/research/07-target-data-model-and-ownership.md` | RF07 — the 4 adapter contracts + ownership matrix (`[DESIGN]` basis) |
| `TASK-TECHREF-20260603-021348/synthesis/synth-01..08-*.md` | 8 synthesis fragments (§1-2, §3-4, §5.1-5.3, §5.4-5.8, §6-8, §9-11, §12-14, §15-16) consolidated into this document |
| `FEASIBILITY-STUDY.md`, `DECISION-SUMMARY.md`, `ROADMAP.md`, `RISK-REGISTER.md` | Parent feasibility artifacts (verdict, decisions D1-D5, phases/gates, risks R1-R9) |

---

## 16. Glossary

Domain terms used throughout this Technical Reference. The **Tag** column marks whether the *referent* is built in this repo (`[CODE-VERIFIED]`), proposed (`[DESIGN — UNBUILT]`), an upstream component (`[EXTERNAL-VERIFIED]`), or a documentation convention (`—`).

| Term | Definition | Tag |
|------|------------|-----|
| **ClaudeProcess** | The runtime seam: the single class managing one `claude --print` child subprocess (prompt-via-stdin, permission flags, timeout→124, SIGTERM→SIGKILL termination, tool-write vs stdout output modes). The *only* `subprocess.Popen`/`claude --print` boundary in the pipeline package, sitting behind the injected `StepRunner` protocol — therefore the single substitution point a Mastra port must replace. `cli/pipeline/process.py:24-244`; sprint subclass `cli/sprint/process.py:88-121`. | `[CODE-VERIFIED]` |
| **StepRunner** | The process-boundary protocol — `__call__(step, config, cancel_check) -> StepResult`. The runner owns the subprocess + timeout; the executor owns retry, gates, and ordering. Dependency injection through this protocol is what makes the orchestration runtime-agnostic: swapping the runner swaps the runtime without touching pipeline logic. `cli/pipeline/executor.py:41-60`. | `[CODE-VERIFIED]` |
| **strangler-fig** | Replatforming pattern in which the new system grows around the old one, wrapping and replacing one pipeline at a time while the legacy system keeps running, rather than a big-bang rewrite. The proposed migration posture: wrap `superclaude tasklist validate` first, port further pipelines incrementally behind the `StepRunner` seam. `FEASIBILITY-STUDY.md` §8, `ROADMAP.md` Phases 0-5. | `[DESIGN — UNBUILT]` |
| **Python-as-oracle** | Parity-gating discipline for the migration: each step ported to the target stack must reproduce the existing native Python CLI's verdict (pass/fail) before the native implementation is retired. Python remains the authoritative reference ("oracle") during transition. `ROADMAP.md` parity gates G1-G3. | `[DESIGN — UNBUILT]` |
| **work-of-record split** | Proposed ownership division across the target stack: Backlog.md owns prose/tasks/docs/decisions (the human-readable work-of-record); Beads owns the dependency graph, agent memory, and external gates; Mastra owns run/trace/gate-execution state. One prose owner, one graph owner, one run owner — to prevent dual-owner drift. `DECISION-SUMMARY.md` honesty statement 4; `07-target-data-model-and-ownership.md`. | `[DESIGN — UNBUILT]` |
| **stable-ID join** | The proposed cross-system synchronization key. Existing stable ID *formats* (`TASK-*`, `T<PP>.<TT>`, `D-####`, `R-###`) already appear in current file formats and parsers; the *design* reuses them as the join key that keeps Backlog.md tasks, Beads issues, and Mastra runs in correspondence. ID formats: `sc-tasklist-protocol/SKILL.md:161-164`, `sprint/config.py:374-377` (BUILT); cross-system join (DESIGN). | `[CODE-VERIFIED]` (formats) + `[DESIGN — UNBUILT]` (join) |
| **Mastra workflow / Workspace** | Mastra is a TypeScript agent framework. A **workflow** is a deterministic, typed step pipeline (`createWorkflow()`/`createStep()` with input/output schemas) supporting durable `suspend()/resume()`. The **Workspace** `WorkspaceSandbox` (`executeCommand`/start/stop/destroy, timeouts, stdout/stderr) is the candidate subprocess substrate — but parity with the Claude Code hook/permission model is NOT established. The component exists upstream; the integration does not. mastra.ai/docs/workflows/overview; reference/workspace/sandbox. | `[EXTERNAL-VERIFIED]` |
| **Backlog.md** | Markdown-native task store (`backlog/` directory) with CLI + TUI board + browser UI + MCP MVP; MIT-licensed, TypeScript/Bun, v1.45.2. Local-file/git-centric (not a centralized multi-user transactional backend). MCP task schemas use `additionalProperties:false`, so arbitrary SuperClaude metadata cannot be injected as MCP fields. Proposed prose/work-of-record owner. github.com/MrLesk/Backlog.md. | `[EXTERNAL-VERIFIED]` |
| **Beads / bd / Dolt** | **Beads** (`gastownhall/beads`) is a distributed graph issue tracker for AI agents; **`bd`** is its CLI (`bd ready`, `bd create`, `bd update --claim`, `bd dep add`, always `--json`). Storage is **Dolt**-first (version-controlled SQL with cell-level merge and branching) — `.beads/issues.jsonl` is export/interchange only, NOT canonical sync (corrects the seed-brief's SQLite+JSONL framing). Embedded mode is single-writer; **server mode (`dolt sql-server`) is required for multi-agent** concurrency. Version `v1.0.5` carries a "do-not-upgrade" caution. Proposed graph/memory/gate owner. github.com/gastownhall/beads; docs/DOLT.md. | `[EXTERNAL-VERIFIED]` |
| **MCP (Model Context Protocol)** | Narrow integration protocol for host/client/server tool-and-resource exchange. Explicitly **NOT a governance platform**; authorization is optional (OAuth 2.1 for remote servers, token passthrough forbidden). Relevant because the target stack exposes/consumes MCP (Mastra MCPClient/MCPServer; Backlog.md MCP MVP; Beads `beads-mcp`), but MCP alone supplies no tenancy, audit, or cost attribution. modelcontextprotocol.io/docs/concepts/architecture. | `[EXTERNAL-VERIFIED]` |
| **CERTIFY_GATE** | A STRICT-tier roadmap gate (5 required frontmatter fields incl. `certified`/`certification_date`, 3 semantic checks) that is **defined in `roadmap/gates.py:1324-1351` and listed in `ALL_GATES`, but NOT wired into the production `_build_steps()` pipeline** — no production callsite of `build_certify_step`. A defined-only gap. The roadmap instruction is to **preserve, not normalize**, this finding during any port. Spot-02 CONFIRMED. | `[CODE-VERIFIED]` (defined-only) |
| **numbered-checkpoint contract** | The canonical checkpoint-task form: `### T<PP>.<TT> -- Checkpoint:` headings paired with a `Checkpoint Report Path: TASKLIST_ROOT/checkpoints/...` line. The runtime parser `CHECKPOINT_HEADING_PATTERN` (`checkpoints.py:30-33`) accepts BOTH the numbered form and the legacy sibling `### Checkpoint:` form via an optional group. Known gap: sprint **Path A (per-task) never calls `_verify_checkpoints()`** (only Path B does), so checkpoint enforcement does not run for parsed-task phases. Spot-03 CONFIRMED. | `[CODE-VERIFIED]` |
| **`[CODE-VERIFIED]`** | Built-vs-design tag: the claim refers to existing SuperClaude Python orchestration code that the port reuses/adapts. Cites an actual source `path:line` at HEAD `9e864860` and the research file that traced it. This is real, shipped code. | — |
| **`[DESIGN — UNBUILT]`** | Built-vs-design tag: the claim refers to the proposed target architecture (Mastra workflows, Backlog.md/Beads adoption, the adapter/seam-replacement layer, the multi-tenant control plane). Evidence traces to `FEASIBILITY-STUDY.md` / research files / web research — **NOT to integrated code, because none exists.** Never present a `[DESIGN]` claim as built. | — |
| **`[DESIGN — UNVERIFIED]`** | A §11-only sub-variant of `[DESIGN — UNBUILT]`: a target behavior whose performance/semantics are measurable in principle but have not been measured because no integrated system exists. Not a fourth canonical tag (see §1.1). | — |
| **`[EXTERNAL-VERIFIED]`** | Built-vs-design tag: a capability fact about Mastra/Backlog.md/Beads/MCP sourced from web/upstream research with URLs. The component exists upstream; the *integration into this repo* does not. Must never be silently upgraded to `[CODE-VERIFIED]`. | — |

---

## Appendices

### Appendix A: The Four Adapter Contracts (quick reference)

The proposed hybrid introduces exactly four adapter contracts (§5.6, §7.3). All `[DESIGN — UNBUILT]`; each carries a round-trip / idempotency validation gate. **C1** tasklist→Backlog import (export must satisfy `discover_phases()`/`parse_tasklist_file()`); **C2** Backlog/tasklist→Beads graph sync (dependency list identical to `TaskEntry.dependencies` unless human-approved patch); **C3** Backlog/Beads→Mastra plan (deterministic dry-run before side effects); **C4** Mastra results→Backlog/Beads reconciliation (idempotent re-apply = no-op).

### Appendix B: Spike Exit Gates (SG1-SG4)

The Option D validation spike (Phases 0-2) is gated by four exit gates (§11.4, §8.3): **SG1** Mastra durable subprocess-supervision parity (the load-bearing gate, == G2); **SG2** tasklist round-trip into Backlog.md + Beads; **SG3** Beads server-mode + Dolt sync throughput on a pinned version (backup/restore smoke); **SG4** multi-tenant cost/identity overhead via a governance-plane prototype.

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-06-03 | tech-reference skill | Initial design reference assembled from 8 synthesis fragments; BUILT side verified against HEAD `9e864860` (0 code drift). Status: 🟡 Draft, pending QA. |

---

> **See also:**
>
> - [FEASIBILITY-STUDY.md](FEASIBILITY-STUDY.md) — parent feasibility study (verdict, options A-D)
> - [ROADMAP.md](ROADMAP.md) — phased port roadmap (Phases 0-5, gates G0-G7)
> - [RISK-REGISTER.md](RISK-REGISTER.md) — validated risks R1-R9
> - [DECISION-SUMMARY.md](DECISION-SUMMARY.md) — gating decisions D1-D5 + honesty statements
