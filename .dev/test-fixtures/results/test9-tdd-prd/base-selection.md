---
base_variant: "B (Haiku)"
variant_scores: "A:66 B:74"
---

## 1. Scoring Criteria

Ten criteria derived from debate divergence clusters and PRD requirements. Each scored 0–10, equal weight.

| # | Criterion | Source |
|---|---|---|
| 1 | Phase Structure Clarity | Debate Cluster A |
| 2 | Compliance Sequencing | Debate Cluster B |
| 3 | Task Actionability | Debate Cluster C |
| 4 | Timeline Realism | Debate Cluster D |
| 5 | Testing Strategy | Debate Cluster D |
| 6 | Business Value Delivery | PRD S19 Success Metrics |
| 7 | Persona Coverage | PRD S7 Personas |
| 8 | Compliance Alignment | PRD S17 Legal/Compliance |
| 9 | Risk Management | Debate Cluster C |
| 10 | Operational Readiness | Debate Cluster D |

## 2. Per-Criterion Scores

| Criterion | A (Opus) | B (Haiku) | Justification |
|---|---|---|---|
| Phase Structure | 7 | 6 | Opus's 7 phases give clear checkpoints but Phases 2+3 are an artificial split (debate concession: "one continuous implementation effort"). Haiku's 4 phases reflect actual workflow boundaries but compress distinct concerns (FE+testing+admin gaps in Phase 3). Neither is ideal; debate synthesis recommends 5–6. |
| Compliance Sequencing | 5 | 9 | Debate's strongest convergence point: regulations (GDPR, SOC2, NIST) are stable — they don't shift during implementation. Opus's own rebuttal ("the schema already includes compliance fields") proves Haiku's point: if compliance shapes the schema, constraints must be ratified before the schema freezes. Opus defers validation to Phase 5; Haiku ratifies NFR-COMP-001/003/004 as Phase 1 gate constraints on DM-001/DM-003. |
| Task Actionability | 6 | 7 | Opus's OQ table says OQ-004 blocks Phase 2 but creates no resolution task — depends on ad-hoc action. Haiku makes every OQ a gate task with AC and dependencies (e.g., OQ-004: "per-user-limit:decided; eviction-policy:defined"). However, Haiku's SC-001–010 as M-effort tasks inflates the tracker — metric checks like "validate login p95" take 15 minutes, not M-effort. Net: Haiku is more actionable but noisier. |
| Timeline Realism | 8 | 6 | Opus's 14 weeks includes realistic buffer for security-critical work. Haiku's 11 weeks assumes zero Phase 1 gate slip, zero frontend scope creep, and perfect compliance–implementation parallelism. Haiku's Phase 2 covers the same scope as Opus's Phases 2+3 in 3 weeks (vs 3.5), while adding API contracts, performance tuning, and SOC2 audit persistence. The debate did not resolve whether this is compression or underestimation. |
| Testing Strategy | 6 | 8 | Debate reached convergence: co-located unit/integration testing is modern practice; Opus conceded this point. Opus's dedicated Phase 6 QA catches defects introduced in Phase 2 that have propagated through Phases 3–5. Haiku co-locates TEST-001–006 with Phase 3 implementation. Opus retains an edge on E2E (dedicated time prevents QA squeeze when frontend runs long). |
| Business Value Delivery | 7 | 8 | PRD targets Q2 2026 release. Opus at 14 weeks from 2026-04-15 ends ~July 22 — past Q2. Haiku at 11 weeks ends June 30 — barely makes Q2 and the SOC2 Q3 deadline. PRD states delay past Q2 "risks SOC2 audit failure in Q3 and a full-quarter slip to the personalization roadmap." Faster delivery of SC-006 (registration conversion >60%) and SC-007 (>1000 DAU in 30d) maps directly to the $2.4M revenue dependency. |
| Persona Coverage | 7 | 8 | Both serve Alex (registration/login) and Sam (API contracts). Key differentiator: Jordan (admin). Opus defers OQ-007 (admin audit viewer) indefinitely ("pending TDD update"). Haiku designs COMP-011 (audit viewer) in Phase 1 and specifies OQ-007 scope in Phase 3. Haiku also explicitly designs logout (OQ-006/COMP-010) for Alex's shared-device scenario per PRD user story AUTH-E1. |
| Compliance Alignment | 5 | 9 | PRD S17 states: "Users must consent to data collection at registration" (GDPR), "All auth events logged...12-month retention" (SOC2), "One-way adaptive hashing" (NIST). Haiku ratifies all three as Phase 1 constraints (NFR-COMP-001, NFR-COMP-002 wired in Phase 2, NFR-COMP-003). Opus defers GDPR consent capture to Phase 5 — but the PRD requires consent *at* registration, meaning any pre-Phase-5 testing with real-like flows would lack consent capture. |
| Risk Management | 7 | 6 | Opus's risk table (7 rows with severity/likelihood/impact/mitigation/owner) is a clean governance artifact. Haiku places R-001–R-007 as Phase 4 tasks with AC and effort — thorough but adds 7 task rows to an already-dense 28-row phase. Debate synthesis recommended Opus's risk table format. Both identify the same 7 risks with similar mitigations. |
| Operational Readiness | 8 | 7 | Both allocate 4 weeks for rollout (Phase 7/Phase 4). Opus separates ops (Phase 5: runbooks, HPA, monitoring) from rollout — cleaner delineation of "make it ready" vs "ship it." Haiku combines ops+rollout+risks+SC-validation in one Phase 4, which compresses distinct operational concerns. Opus's integration-point tables per phase are more detailed for Phase 5/7 wiring. |

## 3. Overall Scores

| Variant | Score | Summary |
|---|---|---|
| **A (Opus)** | **66/100** | Stronger on timeline honesty (+8), operational readiness (+8), phase granularity (+7), and risk governance (+7). Weaker on compliance sequencing (5) and compliance alignment (5) — the two dimensions most critical for a SOC2-auditable service with GDPR obligations. |
| **B (Haiku)** | **74/100** | Stronger on compliance sequencing (+9), compliance alignment (+9), testing strategy (+8), persona coverage (+8), and business value delivery (+8). Weaker on timeline realism (6) and risk table format (6). |

**Score delta: 8 points.** The gap is driven primarily by compliance dimensions (combined 14 vs 10) where the PRD's legal requirements strongly favor Haiku's constraint-first approach, and by testing strategy where the debate reached convergence in Haiku's favor.

## 4. Base Variant Selection Rationale

**B (Haiku)** is the base variant for three reasons:

1. **Compliance is structurally correct.** For a SOC2-auditable service with GDPR obligations, compliance constraints must shape the schema — not validate it after the fact. Haiku's Phase 1 ratification of NFR-COMP-001/003/004 as constraints on DM-001/DM-003 prevents the exact late-stage rework pattern Opus's Phase 5 placement risks. The debate's strongest convergence point supported this.

2. **PRD alignment is tighter.** Haiku addresses all three personas (Alex, Jordan, Sam) with explicit design tasks for logout (COMP-010) and admin audit viewer (COMP-011). Opus defers both. The PRD includes logout as a user story (AUTH-E1) and admin log viewing (AUTH-E3) — these are in-scope, not deferrable.

3. **Absolute dates anchor stakeholder communication.** Haiku's 2026-04-15 through 2026-06-30 timeline maps directly to the SOC2 Q3 deadline. Opus's relative weeks require a supplementary schedule — the debate reached convergence on this point.

## 5. Improvements from A (Opus) to Incorporate in Merge

| # | Improvement | Source | How to Apply |
|---|---|---|---|
| 1 | **Increase to 5–6 phases** | Debate synthesis | Split Haiku's Phase 2 (3 weeks, overloaded) into two: "Core Backend" (auth flows + API contracts) and "API Hardening + Performance" (rate limits, load tests, NFR-PERF). Split Haiku's Phase 3 into "Frontend + Integration Testing" and keep Phase 4 rollout. Target: 5 phases. |
| 2 | **Convert SC-001–010 from task rows to phase exit checklists** | Opus's separation-of-concerns argument | Remove 10 M-effort SC-xxx tasks from Phase 4. Add a "Phase Exit: Success Criteria Validation" checklist to Phases 2, 3, and 4 exit gates. Each criterion lists metric, target, validation method — not effort/priority/ID. |
| 3 | **Use Opus's risk table format** | Debate synthesis | Replace Haiku's 7 R-xxx Phase 4 task rows with Opus's risk assessment table (severity/likelihood/impact/mitigation/owner). Retain Haiku's AC content as mitigation detail. Reduces Phase 4 from 28 to ~11 rows. |
| 4 | **Extend timeline to 12–13 weeks** | Opus's timeline realism | Add 1–2 weeks buffer: 1 week between implementation and rollout (dedicated E2E + security review), 0.5 week buffer on Phase 1 (26 tasks is front-loaded). Absolute dates shift GA from June 30 to ~July 7–14. This slightly exceeds Q2 but is more honest than 11 weeks and more aggressive than 14. |
| 5 | **Add dedicated E2E testing window** | Opus Phase 6 argument | Allocate 1 week between frontend completion and rollout for E2E Playwright tests (TEST-006), penetration testing (R-005), and security review. Co-located unit/integration testing stays with implementation per Haiku; E2E gets uncompressed time per Opus's concession point. |
| 6 | **Adopt Opus's per-phase integration-point tables** | Opus structural quality | Haiku's integration tables are adequate but Opus's are more granular (artifact/type/wired-phase/consumed-by). Adopt Opus's format across all phases for traceability. |
| 7 | **Retain Haiku's team ownership section** | Debate convergence | Keep Haiku's teaming/ownership section mapping auth-team, frontend, security/compliance, and platform/ops to specific domains. Opus's fragmented owner column is insufficient for a multi-team effort. |

**Net effect of merge:** ~5 phases, ~65 task rows (down from 83), 12–13 week timeline with absolute dates, compliance-first sequencing, co-located unit/integration testing + dedicated E2E window, risk governance table, SC validation as exit checklists, and explicit team ownership.
