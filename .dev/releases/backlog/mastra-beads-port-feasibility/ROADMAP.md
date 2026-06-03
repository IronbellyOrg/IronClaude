# Roadmap — Mastra + Backlog.md + Beads Port (Hybrid Adapter-First)

**Date:** 2026-06-03
**Source:** `FEASIBILITY-STUDY.md` Section 8 (and `synth-05-implementation-roadmap.md`). This is a condensed planning extract; the full study is authoritative.
**Recommended approach:** **Option D → Option A** — fund a time-boxed validation spike (Phases 0–2), then continue into Hybrid adapter-first (Phases 3–5) **only if the spike exit gates pass**. If they fail, stop at deferral (do not port now).

> This roadmap is **phase-gated and decision-gated, not code-ready.** Steps marked `[DECISION-GATED]` or `[UNVERIFIED]` require a prerequisite decision or hands-on validation before implementation.

---

## Phase Overview

| # | Phase | One-line goal | Primary go/no-go |
|---|---|---|---|
| 0 | Spike discovery & decisions | Pin contracts; choose work-of-record; scope licensing | Decisions D1–D5 recorded (G0) |
| 1 | Spike adapter MVP (read-only) | Import current artifacts into Backlog.md + Beads, round-trip-safe | Parser round-trip parity passes (G1) |
| 2 | Spike hybrid pilot | Wrap ONE real pipeline (`tasklist validate`) behind a Mastra workflow | Pilot parity vs native CLI + durability proven (G2) |
| 3 | Committed parity port | Wrap `roadmap run` + sprint; reproduce gates/checkpoints/hooks | Artifact + gate + recovery parity suite passes (G3) |
| 4 | Multi-tenant hardening | Add governance/control-plane, tenant identity/audit/cost | EE + governance decisions resolved (G4) |
| 5 | Rollout | Progressive production rollout behind the control plane | Operational + recovery gates pass (G5) |

**Spike boundary:** Phases 0–2 ARE the validation spike. The program is only "committed" once **G2 passes** (Mastra durably supervises a long-running subprocess and reproduces rerun/recovery). Phases 0–2 = Option D's time-boxed spike; Phases 3–5 = Option A proper.

---

## Phase 0 — Discovery & Foundational Decisions
**Goal:** Lock the contracts that must survive the port and make the five gating decisions. No execution code; output is an inventory + decision record.

Key steps: freeze the **stable-ID contract** (`TASK-*`, `R-###`, `T<PP>.<TT>`, `D-####`) as the cross-system key (adapters preserve IDs verbatim); inventory the **sprint parser compatibility contract** (`sprint/config.py`); adopt the **canonical numbered-checkpoint contract** (`09-gap-fill-checkpoint-contract.md:127-154`, not legacy `### Checkpoint:`).

**Five decisions (gate later phases):**

| ID | Decision | Default if unresolved |
|---|---|---|
| D1 | Primary work-of-record: Backlog.md vs Beads | **NO-GO to Phase 1** — all mappings depend on it |
| D2 | Mastra OSS vs Enterprise licensing track | OSS pilot allowed; multi-tenant NO-GO until resolved |
| D3 | Separate governance/control-plane ownership | Multi-tenant NO-GO without it |
| D4 | Runtime subprocess/exec seam (hybrid wrapper) | Hybrid = keep calling existing CLI |
| D5 | Beads deployment mode + version pin | Embedded = solo eval only |

**Gate G0 → Phase 1:** PROCEED only if D1 and D4 are recorded and parser/checkpoint contracts are inventoried. NO-GO if work-of-record is unresolved.

## Phase 1 — Adapter MVP (Read-Only, No Ownership Transfer)
**Goal:** Read-only importers ingest existing tasklist bundles into Backlog.md (prose) + Beads (dependency graph) **without mutating current files**, proven round-trip-safe against the sprint parser.

Key steps: tasklist-bundle → Backlog.md importer (via `backlog` CLI/MCP, mapping to supported fields since MCP rejects unknown properties); tasklist → Beads graph mirror (`bd create`/`bd dep add`/`--json`, typed deps, cycle rejection); encode validation/PR-merge barriers as **Beads gates** (`gh:pr`/`gh:run`/`human`/`timer`); idempotent additive imports keyed on stable IDs; **round-trip parity exporter + test** asserting `discover_phases()`/`parse_tasklist_file()`/`count_tasks_in_file()` match; seed a corpus mixing numbered + legacy checkpoint shapes.

**Gate G1 → Phase 2:** PROCEED only if round-trip parity passes on the mixed corpus and importers are idempotent. No execution behavior changes — Python remains the oracle.

## Phase 2 — Hybrid Pilot (Wrap ONE Real Pipeline) — load-bearing spike gate
**Pilot recommendation (smallest safe first slice):** Wrap **`superclaude tasklist validate`** — a single-step, strict-gate, **non-destructive** pipeline (`tasklist/executor.py:191-218,221-248`) with a clean parseable pass/fail contract that reuses the shared pipeline layer. (Defer `roadmap run` to Phase 3 — too much surface for a first slice.)

Key steps: Mastra workflow with one step that **shells out** to the existing CLI; mirror the CLI gate as a Mastra scorer; run the **subprocess-safety spike** (reuse `eval/isolation.py` HOME-isolation model as the parity target); validate **durability (suspend/resume + failed-step restart)**; capture traces with SuperClaude IDs as custom attributes (the cost-attribution join key); reconcile results back into Backlog.md + Beads.

**Gate G2 → Phase 3 (load-bearing):** PROCEED only if Mastra-wrapped verdict == native CLI verdict, suspend/resume + restart behave correctly, and the safety spike produced an explicit parity/gap report. **NO-GO if Mastra rerun/recovery cannot be demonstrated** — that is the assumption the stateful `roadmap`/`sprint` ports depend on (`web-01:86`). This is the spike's decisive exit.

## Phase 3 — Parity Port (Roadmap Run, Sprint, Gates, Checkpoints, Hooks)
**Goal:** Extend the hybrid pattern to the full orchestration surface, keeping Python as the oracle until each step passes a parity gate.

- **Roadmap run:** map the wired 12-step graph to a Mastra workflow (one node per registry step; parallel generate steps); reproduce gates preserving blocking vs `TRAILING` modes; **preserve, do not normalize** the defined-but-unwired `CERTIFY_GATE`; port the convergence/remediation state machine.
- **Sprint (hardest surface):** reproduce Path A (per-task) vs Path B (freeform) routing; **wire checkpoint verification into the per-task path** (closes the known `_verify_checkpoints()` gap); map phases/tasks to the Beads `bd ready` scheduler with atomic `--claim`; preserve status/result/telemetry/budget models (telemetry → Mastra traces, not Backlog/Beads bodies).
- **Hooks → Mastra middleware/guards:** recreate UV-only, `.claude/` SoT/staging, fork-PR target, freshness pre-edit, safe command execution as explicit guards (`[UNVERIFIED]` portability — verify each hook). Begin selective native reimplementation of **deterministic steps only** after they pass parity.

**Parity suite (acceptance):** artifact parity, gate verdict+mode parity, graph/order parity, safe-execution parity (eval harness), recovery/resume parity.

**Gate G3 → Phase 4:** PROCEED only if the parity suite passes for `roadmap run` AND a representative sprint, and every hook is a verified guard.

## Phase 4 — Multi-Tenant Hardening (not a thin add-on)
**Goal:** Convert the single-tenant parity port into a multi-tenant layer. Gated on four things Mastra+Backlog+Beads do NOT provide on their own:

1. **Mastra Enterprise licensing decision (D2)** — production RBAC/SSO/FGA/audit/on-prem are EE-licensed; OSS leaves Studio/API public.
2. **A separate governance/control-plane service** — tenant registry, identity mapping, RBAC/ABAC, tool catalog, audit log, cost/budget metering. MCP is not a governance layer.
3. **Tenant-aware identity/audit/cost** — net-new; current models carry no tenant/actor fields; separate trigger/execution/authorization/tenant/attribution identities.
4. **Final primary work-of-record decision (D1)** between Backlog.md and Beads.

Key steps: stand up Mastra auth + RBAC/FGA (EE) or document OSS limits; build the control-plane service; add an MCP/AI gateway (OAuth 2.1, no token passthrough, single-issuer pinning, tool allowlists); map command/skill privileges to **granular scopes** (no `superclaude:*`); per-invocation audit records; cost attribution + budget/rate enforcement (promote `TurnLedger` to a tenant cost model); promote Beads to server/shared-server mode with per-tenant prefixes; freeze one canonical work-of-record + curated tool catalog.

**Gate G4 → Phase 5:** PROCEED only if D1+D2 are final and the governance plane + MCP gateway enforce tenant isolation + per-invocation audit + cost attribution on a two-tenant test. **NO-GO if any tenant can read another's tasks/traces/costs**, token passthrough is possible, or EE features are assumed without a licensing decision. Do not deploy company-wide on the three components alone.

## Phase 5 — Rollout
**Goal:** Progressive production rollout behind the control plane, lowest-risk pipeline + tenant first.

Key steps: roll out the pilot (`tasklist validate`) to one internal tenant; expand to `roadmap run` then sprint **one pipeline at a time** (re-run parity per expansion); add tenants progressively with **isolation re-validation per onboarding**; operationalize recovery + backup hygiene (`bd backup`/`dolt push`, tested restore, sprint crash-recovery drills); keep a **native-vs-hybrid fallback** per step; run **drift detection** between Backlog.md, Beads, and Mastra continuously.

**Gate G5 (recurring):** each increment PROCEEDS only if parity + isolation + recovery pass in production config; rollback if drift detection flags divergence.

---

## Validation / Eval Strategy (cross-phase)
Reuse the existing `cli/eval` harness patterns at every phase: round-trip parser parity (Phase 1), capability preflight (Phases 2–3), safe parallel execution via HOME-isolation/scratch-root allowlist (Phases 2–3), ordered outcome accounting (Phase 3), forensic JSONL logs + preserve-failed-HOME (Phases 2–5), retry-once for flaky MCP steps, return-contract/artifact diffing (Phase 3), gate-verdict+mode parity (Phase 3), checkpoint enforcement parity (Phase 3), recovery/resume parity (Phases 3, 5), and a net-new tenant isolation + audit + cost two-tenant test (Phases 4–5).

## Pilot Recommendation (one line)
Start by wrapping **`superclaude tasklist validate`** (single-step, strict-gate, non-destructive) behind a Mastra workflow; the decisive early gate is **G2 — proving Mastra rerun/recovery/durability**, without which the stateful `roadmap`/`sprint` ports are infeasible.
