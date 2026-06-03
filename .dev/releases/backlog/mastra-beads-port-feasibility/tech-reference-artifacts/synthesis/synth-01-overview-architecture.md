# Mastra + Backlog.md + Beads Hybrid Orchestration Architecture — Technical Reference (§1-2)

> **Synthesis fragment:** Sections 1 (Overview) and 2 (Architecture) of the Technical Reference for the **PROPOSED** Mastra + Backlog.md + Beads hybrid, adapter-first orchestration architecture.

| Field | Value |
|-------|-------|
| **Status** | Complete |
| **Date** | 2026-06-03 |
| **Code baseline (BUILT side)** | HEAD `9e864860` |
| **Sections in this fragment** | §1 Overview, §2 Architecture |

---

## 1. Overview

> **CRITICAL — PROPOSED, NOT-YET-BUILT ARCHITECTURE.** This document is a *design reference* for a hybrid orchestration architecture that **does not exist in the codebase today**. No source file in the repository implements any Mastra, Backlog.md, or Beads integration as of HEAD `9e864860` `[CODE-VERIFIED]` (absence across full scope, `04-cli-portify-prd-cleanup-audit-eval` row 5.6-27). The feasibility verdict is **Conditionally Recommended**, with a **spike-first, Option D → Option A** approach: fund a time-boxed validation spike, then proceed to the **hybrid adapter-first** target only if the spike clears its exit gates `[DESIGN — UNBUILT]` (`DECISION-SUMMARY.md` Verdict, XC-11). Treat every target-architecture statement here as a design intent to be validated, never as shipped behavior.

**What it does (target):** Wraps the existing, runtime-agnostic SuperClaude pipeline kernel (the parts that are BUILT) behind an adapter/seam-replacement layer so that **Mastra** owns durable workflow run/trace state, **Backlog.md** owns the markdown task-of-record, and **Beads** owns the dependency graph + agent memory — turning a single-runtime, Claude-Code-coupled Python orchestrator into a multi-tenant, multi-model orchestration layer `[DESIGN — UNBUILT]` (`seed-brief.md` Problem Statement; `FEASIBILITY-STUDY.md` §6.1). In the proposed posture, **Python remains the execution oracle** (gates, models, sprint runtime, roadmap pipeline run as-is) while the external substrate is added around it, not in place of it `[DESIGN — UNBUILT]` (XC-02, F2).

**Who/what it is for:** Engineering teams porting SuperClaude orchestration to a company-wide, multi-tenant, multi-tool substrate, and AI agents that need to understand the seam between BUILT Python and the proposed external stack. The strategic driver is multi-tenancy / multi-user / multi-model orchestration that the current single-`claude`-CLI driver cannot deliver `[CODE-VERIFIED]` (`seed-brief.md` Constraints; F8/F10/F11).

**Where the BUILT side lives:** `src/superclaude/cli/` — specifically the shared kernel `cli/pipeline/` (framework-neutral `models.py`, `executor.py`, `gates.py`, `process.py`, `trailing_gate.py`), plus the `cli/roadmap/`, `cli/tasklist/`, and `cli/sprint/` consumers, and the portable knowledge corpus under `src/superclaude/{skills,agents,commands,core,templates,hooks,mcp}/` `[CODE-VERIFIED]` (`01-pipeline-core-contracts` 5.1-01..5.1-44; `core/CLAUDE.md:17-29`). `src/superclaude/` is the source of truth; `.claude/` is synced dev copies and must not be scraped as primary `[CODE-VERIFIED]` (5.4-01).

**Key numbers:** 8 subsystems (5.1 pipeline-core seam · 5.2 roadmap/tasklist · 5.3 sprint runtime · 5.4 harness corpus · 5.5 target data model · 5.6 adapter layer · 5.7 external substrate · 5.8 governance plane); 3 external tools (Mastra, Backlog.md, Beads); ~20 reused BUILT source files across `cli/pipeline/`, `cli/roadmap/`, `cli/tasklist/`, `cli/sprint/`; portable knowledge corpus of 42 commands / 39 agents / 24 skill packages `[CODE-VERIFIED]` (5.4-16, F6); code baseline HEAD `9e864860`.

### 1.1 Tag Legend (built-vs-design demarcation)

Every architectural claim in this reference carries **exactly one** tag. Never read a `[DESIGN]` claim as built.

| Tag | Meaning | Evidence basis |
|-----|---------|----------------|
| `[CODE-VERIFIED]` | Existing SuperClaude Python that the port **reuses**; real at HEAD `9e864860`. | Real `source path:line` **and** a research/spot-check file. Verify spot-check `path:line` over prior research where they differ (R4). |
| `[DESIGN — UNBUILT]` | The **target** hybrid — Mastra workflows, Backlog/Beads adoption, the adapter layer, the multi-tenant control plane. | FEASIBILITY-STUDY / research synthesis. **Not** integrated code; nothing in the repo implements it yet. |
| `[EXTERNAL-VERIFIED]` | Mastra / Backlog.md / Beads / MCP capability facts. | `web-01`..`web-04` (Tavily/Context7) with source URLs. Capability of the external tool, not a current-repo fact. |

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

The eight subsystems span the BUILT kernel, the proposed adapter layer, the external substrate, and the governance plane. Tags reflect the **dominant** evidence basis of each subsystem (mixed subsystems note both).

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

### 2.3 Key Design Decisions

These are the load-bearing architectural decisions for the proposed hybrid. Each is a design choice (`[DESIGN — UNBUILT]`) justified by a verified property of the BUILT system or external substrate.

| Decision | What is proposed | Rationale | Tag |
|----------|------------------|-----------|-----|
| **Strangler-fig replatforming** (not big-bang rewrite) | Wrap the BUILT Python kernel behind adapters and migrate incrementally; start D→A (spike, then hybrid adapter-first), never Option B native TS rewrite. | The orchestration↔runtime coupling is a single already-abstracted seam, and sprint's process/monitor/tmux/checkpoint complexity plus unverified Mastra long-running-supervision parity makes a big-bang rewrite the worst risk/reward. The in-repo cli-portify code-gen-drift history is a direct in-house warning. | `[DESIGN — UNBUILT]` (XC-11, F7; `FEASIBILITY-STUDY.md` §6.2/§7.2) |
| **Python-as-oracle parity gating** | Keep the BUILT Python executing as the behavioral source of truth; the adapter/Mastra layer orchestrates and traces but does not re-derive gate/convergence/diagnostic results. Each adapter contract is round-trip parser-validated before ownership transfer. | Gate logic, models, deliverable decomposition, and the diagnostic chain are pure Python with no Claude imports — runtime-agnostic and highly portable; preserving them by construction keeps behavior parity. Native (B) converts this reuse into rewrite-and-re-test, where parity risk concentrates. | `[DESIGN — UNBUILT]` decision over `[CODE-VERIFIED]` basis (F3, 5.1-21, 5.5-14; honesty statement 2) |
| **Single-runtime-seam replacement** | Replace only `StepRunner`/`ClaudeProcess` first (wrap in Phase 1), preserving `execute_pipeline` + gate semantics; translate `Step`/`GateCriteria`/`StepResult`/`PipelineConfig` to Mastra schemas / Beads metadata. | `ClaudeProcess` is the narrow runtime seam reused by sprint/roadmap/tasklist/cli-portify; replacing it is the central replatforming act and is decoupled from the runtime-agnostic core. Spike exit gate SG1 must prove Mastra durable subprocess-supervision parity before this seam is actually replaced. | `[DESIGN — UNBUILT]` (5.7-29, F1; spike gate SG1, XC-12) |

> **Important:** A fourth cross-cutting decision is forced before Phase 1: a **primary work-of-record** choice (Backlog.md vs Beads, decision D1). Backlog.md and Beads overlap as task stores and their mutual integration is immature (Backlog.md FR #588); the recommended split assigns Backlog.md = human-readable prose work-of-record and Beads = dependency graph + memory + ready-queue + gates, with status canonicality on exactly one owner `[EXTERNAL-VERIFIED]` (5.7-17, F9; `DECISION-SUMMARY.md` honesty statement 4).

---
