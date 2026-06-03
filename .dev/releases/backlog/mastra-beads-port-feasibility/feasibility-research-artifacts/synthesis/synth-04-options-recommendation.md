# Synthesis 04: Options Analysis and Recommendation (Report Sections 6-7)

**Research question:** Can SuperClaude's CLI orchestration pipeline be ported/recreated in a Mastra + Backlog.md + Beads stack as a multi-tenant company orchestration layer? Deferral ("do not port now") is a genuine, live option — a port is NOT assumed worthwhile.

**Status:** Complete
**Date:** 2026-06-02

**Evidence convention:** Codebase claims cite `file:line` within `.dev/tasks/to-do/TASK-RESEARCH-20260602-211124/research/` (abbreviated as `RES/<file>:<line>`). External claims cite `web-0N` agent files (which themselves carry Tavily/Context7 source URLs) or the source URL directly. Claims that remain `[UNVERIFIED]` per `gaps-and-questions.md` are flagged inline and are NOT presented as fact.

**Effort/Risk legend.** Effort bands (complexity, not story points): XS = days; S = 1-2 weeks; M = ~1 month; L = 1-3 months; XL = 3+ months / multi-quarter. Risk = likelihood × impact of the option failing to reach parity or producing drift/security exposure.

---

## Section 6 — Options Analysis

### 6.0 Scoping facts that constrain every option

These verified facts shape all four options and are referenced repeatedly below:

| # | Fact | Evidence |
|---|---|---|
| F1 | The orchestration↔runtime coupling is a single seam: `ClaudeProcess` builds `claude --print --verbose <perm> --no-session-persistence --tools default --max-turns N --output-format <fmt>`. | `RES/01-pipeline-core-contracts.md:80-91`; `RES/08-gap-fill-feasibility-enrichment.md:39,114` [CODE-VERIFIED] |
| F2 | Roadmap, tasklist-validate, and cli-portify/prd/cleanup-audit already share a generic `execute_pipeline()` + injected `StepRunner` protocol; the runner is the swap point. | `RES/01:36-53`; `RES/02-roadmap-tasklist-pipelines.md:38-39,54-60`; `RES/04-cli-portify-prd-cleanup-audit-eval.md:67,74` [CODE-VERIFIED] |
| F3 | Gate logic (`gate_passed`, tiers EXEMPT/LIGHT/STANDARD/STRICT), `Step`/`GateCriteria`/`StepResult` models, deliverable decomposition, and diagnostic chain are pure Python with no Claude imports — runtime-agnostic. | `RES/01:55-72,119-152,196-209` [CODE-VERIFIED] |
| F4 | Sprint does NOT use the generic executor for its main loop; it runs a custom phase/task loop with two divergent paths (A: per-task subprocess; B: freeform + `OutputMonitor`/tmux/watchdogs), file-based result sentinels, checkpoints, `TurnLedger`, summarizer/retrospective. ~8,568 LOC across 19 files; `executor.py` alone is 2,148 lines. | `RES/03-sprint-execution-runtime.md:10,67-71,90-95,139-153` [CODE-VERIFIED] |
| F5 | Roadmap is the largest single subsystem: `executor.py` 3,702 lines + `gates.py` 1,441 lines; 12-step wired pipeline (extract→generate×2→diff→debate→score→merge→anti-instinct→test-strategy→spec-fidelity→wiring→deviation→remediate). | `RES/02:12,14,88-90` [CODE-VERIFIED] |
| F6 | Reusable knowledge corpus: 42 commands, 39 agents, 24 skill packages (~31,820 lines incl. refs), 12 core files, MDTM templates, hooks, MCP configs. Markdown/YAML, runtime-agnostic content but Claude-Code-coupled tool vocabulary (`Skill`, `Task`, `TeamCreate`). | `RES/05-skills-agents-harness-reuse.md:159-172` [CODE-VERIFIED] |
| F7 | An in-repo portification pattern already exists (`/sc:cli-portify` + `sc-cli-portify-protocol`): inventory→step graph→gates→executor spec. Its own history is a cautionary precedent — early code-gen/spec drift caused failures; contract-first planning became the safer pattern. | `RES/05:136-141`; `RES/06-docs-and-existing-feasibility-artifacts.md:217` [CODE-VERIFIED] |
| F8 | Multi-tenant auth/RBAC/FGA/audit/SSO/on-prem are Enterprise-licensed in Mastra (`@mastra/core/auth/ee`, Studio Auth, Agent Builder); without auth, Studio and API routes are public. | `web-01:51-56,78-82` [tavily/context7] |
| F9 | Backlog.md and Beads overlap as task stores AND their mutual integration is immature (Backlog.md issue #588: maintainer says "narrower integration decision before tasking"). Beads is Dolt-first (not SQLite/JSONL as seed-brief assumed); embedded mode is single-writer; server mode needed for multi-agent. Beads v1.0.5 carried a "do not upgrade" sync-corruption warning. | `web-02:93-98`; `web-03:54-70,107-128` [tavily] |
| F10 | None of Mastra+Backlog.md+Beads provides a tenant-aware governance/control plane (identity, policy, tool catalog, audit, cost attribution); MCP itself is explicitly NOT a governance layer. A separate control-plane service is required for company-wide multi-tenant use. | `web-04:93-128,144-153` [tavily] |
| F11 | Current scoped models (`PipelineConfig`, `SprintConfig`, `TaskResult`, `MonitorState`, `TurnLedger`) carry model/permission/budget fields but NO tenant/actor/audit identity fields. | `RES/07-target-data-model-and-ownership.md:102,197`; `RES/11-gap-fill-unverified-inputs-classification.md:115` [CODE-VERIFIED scoped; repo-wide UNVERIFIED] |

---

### 6.1 Option A — Hybrid adapter-first

**Description.** Mastra orchestrates workflows + traces and owns the durable run state; existing Python CLIs continue to execute via adapters (MCP/subprocess wrappers behind the `StepRunner` seam, F2); Backlog.md owns markdown tasks/specs/decisions; Beads owns the dependency graph + agent memory. The `ClaudeProcess` seam (F1) is wrapped, not replaced, in phase 1.

| Dimension | Assessment |
|---|---|
| **Effort** | **M-L.** Adapter layer + Mastra workflow shells + Backlog/Beads importers; reuses Python execution wholesale. Roadmap/tasklist/cli-portify wrap cleanly via F2; sprint needs a supervisory wrapper only (F4), not a rewrite. |
| **Risk** | **Low-Med.** Python remains the execution oracle (`RES/07:182`), so behavior parity is preserved by construction. Main risks: ownership drift between Backlog.md/Beads (F9), and adapter-state persistence outside transient Python objects (`RES/04:67`). |
| **Reuse of existing code** | **Highest.** All gate logic, models, executor semantics, sprint runtime, roadmap pipeline reused as-is (F2, F3, F4, F5). Knowledge corpus (F6) consumed as instruction packs. |
| **Files/systems affected** | New: Mastra workflow defs, `StepRunner`→Mastra adapter, Backlog.md importer, Beads graph sync, control-plane stub. Unchanged: `cli/pipeline/*`, `cli/sprint/*`, `cli/roadmap/*` (wrapped, not edited). |
| **Pros** | Preserves verified contracts; lowest parity risk; incremental/strangler-fig; lets the Backlog-vs-Beads and native-rewrite decisions be deferred until adapters prove the mapping (`RES/06:220`); can drive non-Claude models later via Mastra agents without touching the Python core. |
| **Cons** | Two runtimes to operate (Python + TypeScript/Mastra); does NOT by itself deliver multi-tenancy (still needs F8 EE + F10 control plane); Backlog/Beads overlap unresolved if both adopted at once; the `claude` CLI single-model limit persists for wrapped paths until the seam is actually replaced. |

---

### 6.2 Option B — Native Mastra reimplementation

**Description.** Translate pipeline core / roadmap / tasklist / sprint / PRD / audit into TypeScript Mastra workflows + agents. Replace `ClaudeProcess` (F1) with Mastra agent/Workspace execution; reimplement gates, models, monitors, checkpoints natively.

| Dimension | Assessment |
|---|---|
| **Effort** | **XL.** Must re-home: roadmap (5.1K LOC, 12-step pipeline, F5), sprint (8.5K LOC, dual paths, monitors, tmux, watchdogs, checkpoints, F4), pipeline core, plus port ~31.8K lines of knowledge corpus tool vocabulary (F6). cli-portify history (F7) shows code-gen ports drift and fail without contract-first discipline. |
| **Risk** | **High.** Sprint is the hardest stress test — "Any Mastra port that only models phases and tasks will miss the real complexity: process lifecycle, output files, result sentinels, monitors, watchdogs, and tmux IPC" (`RES/03:133`). Mastra long-running subprocess-supervision parity is `[UNVERIFIED]` (`RES/03:240`; `web-01:86-88`). `@mastra/temporal` durable runner is experimental (`web-01:18,87`). Many subtle behaviors (compressed-sidecar gate target, warning-only trailing gates, permissive frontmatter regex) must be re-tested (`RES/01:213-220`). |
| **Reuse of existing code** | **Low for runtime** (rewritten in TS), **Medium for knowledge** (markdown corpus translatable as instructions, F6). Pure-Python gate logic (F3) becomes a TS re-implementation, not a reuse. |
| **Files/systems affected** | Effectively the entire `src/superclaude/cli/` tree re-authored in TypeScript + every skill/agent re-homed to Mastra agent format. |
| **Pros** | Single runtime; native Mastra durability/observability/Studio; clean multi-model support; removes the `claude`-CLI single-model limit (seed-brief line 33); best long-term maintainability IF parity is achieved. |
| **Cons** | Largest effort and highest parity risk; Python→TS boundary means losing pure-Python reuse (F3); loses Claude-Code-native hooks/`/sc:*` dispatch/permission modes/freshness enforcement, all of which must be rebuilt as Mastra middleware (`RES/05:88-91`, `web-01:88`); cli-portify drift precedent (F7) warns against big-bang code-gen; still needs F8 EE + F10 control plane on top. |

---

### 6.3 Option C — Preserve Python CLI, add Backlog/Beads only (no Mastra runtime initially)

**Description.** Keep the Python CLI as the orchestration runtime. Add Backlog.md as the markdown work-of-record and Beads as the dependency graph + memory, via importers/sync adapters. No Mastra workflow runtime in phase 1.

| Dimension | Assessment |
|---|---|
| **Effort** | **S-M.** Two importer/sync adapters + round-trip parser-compatibility tests (`RES/07:125,138`). No runtime rewrite. Smallest of the build options. |
| **Risk** | **Med.** Backlog/Beads overlap and immature mutual integration (F9) is the central risk; Beads Dolt churn / v1.0.5 sync warning (F9) requires version pinning + backup gates (`web-03:135`). Ownership drift if both own status (`RES/07:107,193`). |
| **Reuse of existing code** | **Highest** (Python untouched, like Option A) but with **no new orchestration capability** — only task/graph state externalized. |
| **Files/systems affected** | New: Backlog.md importer, Beads graph sync, stable-ID preservation layer (`RES/07:100,109`). Unchanged: all of `cli/`. |
| **Pros** | Lowest-cost way to test the Backlog/Beads mapping and the task-of-record decision before committing to Mastra; preserves all current behavior; directly answerable by round-trip tests against `discover_phases()`/`parse_tasklist_file()` (`RES/07:125`). |
| **Cons** | Delivers neither multi-tenancy (F8/F10) nor multi-model orchestration (the strategic drivers, seed-brief lines 40-41); Mastra still required later for workflow/trace/governance-telemetry; risks investing in a Backlog/Beads schema that a later Mastra layer reshapes; does not address the `claude`-CLI single-runtime limit at all. |

---

### 6.4 Option D — Defer / not recommended now

**Description.** Do not port now. Keep the Python+Claude-Code stack. Optionally fund a narrow, time-boxed validation spike (Mastra durable-workflow + Workspace-subprocess safety; Backlog↔Beads single-workflow sync) to retire the `[UNVERIFIED]` external assumptions before any build decision.

| Dimension | Assessment |
|---|---|
| **Effort** | **XS-S.** Zero for pure defer; S for a time-boxed spike (`web-01:100-104,110`). |
| **Risk** | **Low (execution) / strategic.** No parity/migration risk. Risk is opportunity cost: multi-tenant/multi-model goals remain unmet, and target-stack churn (Beads v1.x sharp edges, F9; Mastra EE licensing, F8) keeps shifting. |
| **Reuse of existing code** | **Full** — nothing changes. |
| **Files/systems affected** | None (defer) or a throwaway spike workspace. |
| **Pros** | Honest response to the large `[UNVERIFIED]` external surface (`gaps-and-questions.md` RG-I1/RG-I2; F-facts above); avoids committing to immature Backlog↔Beads integration (F9) and EE licensing (F8) prematurely; a spike retires the highest-uncertainty assumptions cheaply (Mastra subprocess-supervision parity `RES/03:240`; Beads multi-writer/Dolt behavior `web-03:135`). |
| **Cons** | Strategic drivers (company-wide multi-tenant, multi-tool orchestration) stay unaddressed; `claude`-CLI single-model limit persists; defers rather than answers the go/no-go; if the company need is urgent, deferral is a cost. |

---

### 6.5 Options Comparison

| Criterion | A — Hybrid adapter-first | B — Native Mastra rewrite | C — Backlog/Beads only | D — Defer |
|---|---|---|---|---|
| **Effort** | M-L | XL | S-M | XS-S |
| **Risk** | Low-Med | High | Med | Low (strategic only) |
| **Maintainability** | Med (two runtimes) | High long-term *if* parity reached; High-risk to reach | Med (Python + 2 stores) | High (status quo, known) |
| **Integration complexity** | High (Mastra + Backlog + Beads + adapters) | Very High (full re-home + control plane) | Med (2 stores, no Mastra) | None / Low (spike only) |
| **Reuse potential** | Highest (F2-F6 as-is) | Low runtime / Med knowledge | Highest (Python untouched) | Full |
| **Multi-tenant readiness** | Partial — needs F8 EE + F10 control plane added | Partial — same F8/F10 still required | None in phase 1 | None |

**Cross-cutting note for all build options (A/B/C):** multi-tenancy is NOT delivered by the three named components. It requires (a) Mastra Enterprise licensing for production RBAC/SSO/audit/FGA/on-prem (F8, `web-01:51-56`) and (b) a separate governance/control-plane layer for tenant isolation, identity separation, tool catalog, audit, and cost attribution (F10, `web-04:125-128`). Current models also lack tenant/actor identity fields (F11). This is an additive requirement on top of whichever build option is chosen.

---

## Section 7 — Recommendation

### 7.1 Feasibility verdict

| Field | Value |
|---|---|
| **Verdict** | **Conditionally Recommended** |
| **Recommended approach** | **Option D → Option A** — fund a time-boxed validation spike first (D), then proceed with **Hybrid adapter-first (A)** if and only if the spike clears its exit gates. Do NOT start with Option B. |
| **Confidence band** | **Medium (≈70%)** that Hybrid adapter-first is technically feasible and the right first build posture; **Low-Medium (≈55%)** that a *full company-wide multi-tenant* layer is deliverable on Mastra+Backlog+Beads alone without significant added Enterprise + control-plane investment. |

**Why "Conditionally" and not "Recommended":** the core orchestration port is technically feasible (the seam is clean — F1, F2, F3; the existing `sc-cli-portify-protocol` proves the method — F7). But the *strategic* goal (multi-tenant company orchestration) depends on conditions that are currently `[UNVERIFIED]` or licensing/maturity-gated: Mastra long-running subprocess-supervision parity (`RES/03:240`, `web-01:86-88`), Mastra EE licensing for production RBAC/SSO/audit (F8), immature Backlog↔Beads integration (F9), and the absence of any control-plane/tenant-identity layer in the three components (F10, F11). The verdict is therefore gated on a spike, not an unconditional go.

**Why "Recommended" rather than "Not Recommended":** the no-go case is not supported — the runtime coupling is a single, already-abstracted seam (F1/F2), the gate/model/diagnostic logic is runtime-agnostic Python (F3), and the knowledge corpus is portable markdown (F6). Nothing in the research shows a structural blocker that makes a port impossible; the blockers are cost, parity-proof, and governance scope, which a phased hybrid path manages.

### 7.2 Rationale against the comparison

| Why A over B | Why A over C | Why A over D-as-endpoint |
|---|---|---|
| B is XL effort + High risk; sprint subprocess/monitor/tmux/checkpoint complexity (F4) plus `[UNVERIFIED]` Mastra supervision parity (`RES/03:240`) makes a big-bang rewrite the worst risk/reward. The cli-portify drift precedent (F7) is a direct in-house warning. | C delivers neither strategic driver (multi-tenant, multi-model). It is a useful *sub-step inside* A (externalize task-of-record), not a competing endpoint. A subsumes C's work and adds the workflow/trace layer the governance plane needs. | D alone leaves the strategic drivers unmet. D is the right *first* move (retire `[UNVERIFIED]` risk cheaply), but as a permanent endpoint it forfeits the company-wide goal. The recommendation is D-then-A, not D forever. |

A also aligns with the independently-reached framing in prior research: keep Python as execution oracle, replace the seam in a narrow runner first, decide task-of-record after a dependency-graph behavior test (`RES/03:216`, `RES/06:220`, `RES/07:182`).

### 7.3 Spike exit gates (the conditions on "Conditionally")

Proceed from D to A only when ALL of these pass (each retires a named risk):

| Gate | Retires | Evidence target |
|---|---|---|
| G1 — Mastra durably supervises a long-running subprocess (suspend/resume, restart, partial rerun, timeout, kill-escalation) at parity with `ClaudeProcess`/watchdogs. | `[UNVERIFIED]` Mastra supervision (`RES/03:240`, `web-01:86-88`) | Working spike, not docs. Workspace `executeCommand` safety validated (`web-01:101`). |
| G2 — One round-trip: import a real `tasklist-index.md`+`phase-N` bundle into Backlog.md+Beads and export back so `discover_phases()`/`parse_tasklist_file()` succeed with matching task counts and dependencies. | Backlog/Beads schema fit `[UNVERIFIED]` (`RES/07:191-192`) | Round-trip test (`RES/07:125,138`). |
| G3 — Beads server-mode multi-writer + Dolt sync survives a pinned version with backup/restore smoke tests; no v1.0.5-class corruption. | Beads churn/Dolt risk (F9, `web-03:135`) | Version-pinned spike with `bd doctor` + push/pull tests. |
| G4 — A documented multi-tenant cost/identity decision: which Mastra license tier, and what the separate control-plane scope is. | F8 licensing + F10 control plane | Written decision, not code. |

### 7.4 Mandatory honesty statements

**Enterprise licensing.** Production multi-tenant RBAC, SSO, audit logs, FGA, and on-prem/VPC are Mastra **Enterprise-licensed**, not in the Apache-2.0 core (`web-01:51-56,89` [tavily/context7]). Without auth, Mastra Studio and API routes are public (`web-01:80`). A local/single-team port may avoid EE; a company-wide multi-tenant deployment most likely **requires Enterprise conversations and cost/lock-in acceptance**. This is a budget and procurement gate, not just an engineering one. Treat any "multi-tenant on Mastra OSS" assumption as false for production RBAC.

**Python/TS boundary.** The runtime-agnostic value (gates, models, deliverable decomposition, diagnostics — F3) is **pure Python**. Option A keeps it; Option B forces a TypeScript re-implementation, converting reuse into rewrite-and-re-test (`RES/01:213-220`). The boundary is the single biggest reason to prefer adapter-first: it lets the Python IP keep executing while only the *orchestration shell* moves to Mastra. Crossing the boundary wholesale (B) is where parity risk concentrates.

**Beads Dolt / version churn.** Current Beads is **Dolt-first**, contradicting the seed-brief's "SQLite or Dolt" framing (`web-03:54-59` [tavily]); `.beads/issues.jsonl` is export-only, not canonical sync. Embedded mode is single-writer; multi-agent **requires server mode** (`web-03:61-70`). v1.0.5 was gated "do not upgrade" over a sync-corruption migration (`web-03:20-25`). Beads is "fast-moving with sharp edges… safe for dev/internal with backup/sync hygiene" but risky as a sole record for mission-critical use (`web-03:105-107`). **Mandate version pinning, server mode for any multi-writer use, and tested backup/restore before adoption.**

**Backlog/Beads overlap — pick a primary work-of-record.** Both can represent tasks; their mutual integration is **immature** (Backlog.md maintainer asks for a "narrower integration decision before tasking," issue #588, `web-02:93-98` [tavily]). Dual status owners create silent drift (`RES/07:107,193`). **Recommended split:** **Backlog.md = primary human-readable work-of-record** (task/spec/decision prose, stable IDs); **Beads = dependency graph + agent memory + ready-queue + gates**, NOT a second prose owner. Status canonicality must be assigned to exactly one (recommend Backlog.md for human status, Beads mirrors normalized status for graph queries only) — `RES/07:95-110,106-109`.

**Governance/control-plane layer beyond the three components.** Mastra+Backlog.md+Beads is an orchestration/task substrate, **not** a complete enterprise platform. MCP is explicitly not a governance layer (`web-04:12-13,119` [tavily]). Company-wide multi-tenant use requires an **additional control-plane service**: tenant registry, separated trigger/execution/authorization/tenant/attribution identities (`web-04:66-71`), RBAC/ABAC policy, tool/skill catalog + change control, per-invocation audit log, and cost attribution/budget metering (`web-04:125-128,144-153`). Current SuperClaude models carry no tenant/actor identity (F11). **This layer is not optional for the strategic goal and is not provided by any of the three components.**

### 7.5 One-line bottom line

A port is **feasible and worth a gated start**, but only as **hybrid adapter-first after a validation spike** — not as a native rewrite, not as a Backlog/Beads-only half-measure, and not as a "multi-tenant on the three components alone" assumption. If the company need is not yet urgent or the spike gates cannot be funded, **deferral (D) is a legitimate and honest choice**, not a failure.

---

## Status: Complete

### Synthesis summary

- **Section 6** presents four options (A Hybrid adapter-first, B Native Mastra rewrite, C Backlog/Beads only, D Defer) each with an Effort/Risk/Reuse/Files/Pros/Cons table, anchored to 11 verified scoping facts (F1–F11), plus an Options Comparison across Effort, Risk, Maintainability, Integration complexity, Reuse potential, and Multi-tenant readiness.
- **Section 7** gives the verdict — **Conditionally Recommended**, recommended approach **D→A** (spike then hybrid), confidence **Medium (~70%)** for hybrid feasibility / **Low-Med (~55%)** for full multi-tenant on the three components — with spike exit gates (G1–G4) and mandatory honesty statements on Enterprise licensing, the Python/TS boundary, Beads Dolt/version churn, Backlog/Beads overlap (Backlog primary work-of-record; Beads graph/memory), and the required governance/control-plane layer.
- Every load-bearing claim cites `RES/<file>:<line>` (codebase) or `web-0N` (external, Tavily/Context7). `[UNVERIFIED]` external assumptions are kept in options/risks, not promoted to current-state facts, per `gaps-and-questions.md` and `RES/11` synthesis guardrails.
