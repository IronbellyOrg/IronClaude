# Decision Summary — Mastra + Backlog.md + Beads Port Feasibility

**Date:** 2026-06-03
**Audience:** Engineering leadership making a go/no-go on a company-wide, multi-tenant orchestration layer.
**Source:** `FEASIBILITY-STUDY.md` (full validated report; Sections 1, 6, 7, 8, 9). This memo is a faithful condensation — it adds no claims beyond the study and does not overstate certainty.

---

## Verdict

| Field | Value |
|---|---|
| **Feasibility verdict** | **Conditionally Recommended** |
| **Recommended approach** | **Option D → Option A** — fund a time-boxed validation spike first; proceed to **Hybrid adapter-first** only if the spike clears its exit gates. **Do NOT start with a native rewrite (Option B).** |
| **Confidence** | **Medium (~70%)** that hybrid adapter-first is feasible and the right first build posture; **Low-Medium (~55%)** that a *full company-wide multi-tenant* layer is deliverable on Mastra + Backlog.md + Beads **alone** without significant added Enterprise + control-plane investment. |

**One-line bottom line:** A port is feasible and worth a **gated start** — as hybrid adapter-first after a validation spike, not as a native rewrite, not as a Backlog/Beads-only half-measure, and not as a "multi-tenant on the three components alone" assumption. If the company need is not urgent or the spike gates cannot be funded, **deferral is a legitimate, honest choice — not a failure.**

---

## Why This Recommendation Wins

**Why "Conditionally" and not "Recommended":** the core orchestration port is technically feasible — the orchestration↔runtime coupling is a single, already-abstracted seam (`ClaudeProcess` + a shared `execute_pipeline()`/`StepRunner` protocol), the gate/model/diagnostic logic is runtime-agnostic pure Python, and the knowledge corpus (42 commands, 39 agents, 24 skills) is portable markdown. But the **strategic** goal (multi-tenant company orchestration) depends on conditions that are currently unverified or licensing/maturity-gated.

**Why "Recommended" and not "Not Recommended":** no structural blocker makes a port impossible. The blockers are cost, parity-proof, and governance scope — all manageable by a phased hybrid path.

**Why A over the alternatives:**

| | Why not chosen as the path |
|---|---|
| **B — Native Mastra rewrite** | XL effort + High risk. Sprint's process/monitor/tmux/checkpoint complexity plus unverified Mastra long-running-supervision parity makes a big-bang rewrite the worst risk/reward. The in-house `cli-portify` history (code-gen drift) is a direct warning. |
| **C — Backlog/Beads only** | Delivers neither strategic driver (multi-tenant, multi-model). It is a useful **sub-step inside A** (externalize task-of-record), not a competing endpoint. |
| **D — Defer (as a permanent endpoint)** | Leaves strategic drivers unmet. D is the right **first move** (retire unverified risk cheaply), but as a forever-endpoint it forfeits the company-wide goal. The recommendation is **D-then-A**, not D forever. |

---

## Spike Exit Gates (the conditions on "Conditionally")

Proceed from D to A only when ALL pass — each retires a named risk:

| Gate | Retires | Evidence target |
|---|---|---|
| **SG1** — Mastra durably supervises a long-running subprocess (suspend/resume, restart, partial rerun, timeout, kill-escalation) at parity with `ClaudeProcess`/watchdogs. | Unverified Mastra supervision; hook/permission/freshness safety parity. | Working spike (not docs); Workspace `executeCommand` safety validated. |
| **SG2** — One round-trip: import a real tasklist bundle into Backlog.md + Beads and export back so `discover_phases()`/`parse_tasklist_file()` succeed with matching counts + dependencies. | Backlog/Beads schema fit (unverified). | Round-trip parser test. |
| **SG3** — Beads server-mode multi-writer + Dolt sync survives a pinned version with backup/restore smoke tests; no v1.0.5-class corruption. | Beads churn / Dolt sync risk. | Version-pinned spike with `bd doctor` + push/pull. |
| **SG4** — A documented multi-tenant cost/identity decision: which Mastra license tier, and what the separate control-plane scope is. | Enterprise licensing + governance/control-plane. | Written decision, not code. |

---

## Mandatory Honesty Statements (do not skip)

1. **Enterprise licensing.** Production multi-tenant RBAC, SSO, audit logs, FGA, and on-prem/VPC are **Mastra Enterprise-licensed**, not in the Apache-2.0 core. Without auth, Mastra Studio and API routes are public. Company-wide multi-tenant deployment most likely **requires Enterprise conversations and cost/lock-in acceptance** — a budget/procurement gate, not just engineering. Treat any "multi-tenant on Mastra OSS" assumption as false for production RBAC.
2. **Python/TS boundary.** The runtime-agnostic value (gates, models, deliverable decomposition, diagnostics) is **pure Python**. Hybrid (A) keeps it executing; native (B) converts reuse into rewrite-and-re-test — where parity risk concentrates.
3. **Beads Dolt / version churn.** Beads is **Dolt-first** (correcting the seed-brief's "SQLite or Dolt" framing); `.beads/issues.jsonl` is export-only. Embedded mode is single-writer; multi-agent **requires server mode**. v1.0.5 was gated "do not upgrade" over a sync-corruption migration. **Mandate version pinning, server mode for multi-writer, and tested backup/restore before adoption.**
4. **Backlog/Beads overlap — pick a primary work-of-record.** Both can represent tasks; their mutual integration is **immature** (maintainer asks for "a narrower integration decision before tasking"). Recommended split: **Backlog.md = primary human-readable work-of-record**; **Beads = dependency graph + agent memory + ready-queue + gates**, not a second prose owner. Assign status canonicality to exactly one.
5. **Governance/control-plane layer beyond the three components.** Mastra + Backlog.md + Beads is an orchestration/task **substrate, not a complete enterprise platform**; MCP is explicitly not a governance layer. Company-wide multi-tenant use requires an **additional control-plane service**: tenant registry, separated trigger/execution/authorization/tenant/attribution identities, RBAC/ABAC policy, tool/skill catalog + change control, per-invocation audit, and cost attribution/budget metering. Current models carry no tenant/actor identity. **This layer is not optional for the strategic goal and is not provided by any of the three components.**

---

## Pilot Recommendation

Wrap **`superclaude tasklist validate`** as the first Mastra-wrapped pipeline — it is the smallest pipeline (one LLM fidelity step, one strict gate), has a clean parseable pass/fail contract, is read-only/non-destructive, and reuses the shared pipeline layer so lessons transfer to `roadmap run`. The decisive early gate is **G2 — proving Mastra rerun/recovery/durability**, without which the stateful `roadmap`/`sprint` ports are infeasible.

---

## Major Risks (top of register — see RISK-REGISTER.md)

- **R1 License** (High) — production RBAC/SSO/FGA/audit/on-prem are Mastra EE.
- **R2 Runtime migration** (High) — ~65K-LOC Python → Mastra TS; subprocess seam replacement.
- **R6 Subprocess/hook safety parity** (High) — Mastra Workspace does not replicate Claude Code hooks/permissions/freshness.
- **R8 Governance/tenancy/cost gaps** (High) — none of the three components supplies a tenant-aware control plane.
- Plus R3 (Backlog/Beads overlap), R4 (Beads/Dolt churn), R5 (concurrency/multi-writer) — High; R7 (checkpoint/wiring drift), R9 (fast-moving tools) — Medium-High.

---

## Immediate Next Decisions

| ID | Decision needed now | If unresolved |
|---|---|---|
| D1 | Primary work-of-record: Backlog.md vs Beads | NO-GO to Phase 1 — all mappings depend on it |
| D4 | Runtime subprocess/exec seam for the hybrid wrapper | Hybrid = keep calling existing CLI |
| Fund? | Approve the time-boxed Phases 0–2 validation spike (SG1–SG4) | Default to deferral (D) — a legitimate outcome |
| D2 | Mastra OSS vs Enterprise track (gates Phase 4) | OSS pilot allowed; multi-tenant NO-GO until resolved |
| D3 | Governance/control-plane ownership (built Phase 4) | Multi-tenant NO-GO without it |
| D5 | Beads deployment mode + version pin | Embedded = solo eval only |

**Recommended immediate action:** approve a time-boxed spike (Phases 0–2) to retire SG1–SG4 before any committed build, and record D1 + D4. Treat company-wide multi-tenant rollout as a separate, EE-and-governance-gated program — not an extension of the spike.
