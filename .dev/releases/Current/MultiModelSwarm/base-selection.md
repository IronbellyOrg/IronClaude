---
base_variant: A
variant_scores: "A:81 B:74"
---

# Scoring & Base Selection

## 1. Scoring Criteria (derived from debate)

| # | Criterion | Weight | Source |
|---|---|---|---|
| C1 | Architectural fidelity to spec (wave decomposition, IMM/INV traceability) | 20 | Divergence 2, 7 |
| C2 | Timeline realism / buffer honesty | 15 | Divergence 1; Round-2 rebuttals |
| C3 | Foundation scope coherence (M1 deliverability) | 10 | Divergence 3 |
| C4 | Validation strategy (per-wave vs gate) | 10 | Divergence 4 |
| C5 | Operational rollout discipline | 10 | Divergence 5 |
| C6 | CLI surface sequencing & operator UX | 10 | Divergence 6 |
| C7 | Resume placement / cross-cutting clarity | 10 | Divergence 7 |
| C8 | Open-question handling (OQ-007/008/009/010) | 5 | Divergence 8 |
| C9 | Risk register signal-to-noise | 5 | Divergence 9 |
| C10 | Contract/documentation completeness (integration tables, success criteria) | 5 | Both variants |

## 2. Per-Criterion Scores

| Criterion | Wt | A (Opus) | B (Sonnet) | A·wt | B·wt |
|---|---|---|---|---|---|
| C1 Architectural fidelity | 20 | 9 | 7 | 180 | 140 |
| C2 Timeline realism | 15 | 7 | 7 | 105 | 105 |
| C3 Foundation scope | 10 | 9 | 6 | 90 | 60 |
| C4 Validation strategy | 10 | 7 | 8 | 70 | 80 |
| C5 Ops rollout | 10 | 6 | 9 | 60 | 90 |
| C6 CLI sequencing | 10 | 8 | 7 | 80 | 70 |
| C7 Resume placement | 10 | 8 | 7 | 80 | 70 |
| C8 OQ handling | 5 | 7 | 9 | 35 | 45 |
| C9 Risk register S/N | 5 | 9 | 6 | 45 | 30 |
| C10 Contract completeness | 5 | 9 | 9 | 45 | 45 |
| **Total** | 100 | — | — | **790** | **735** |

Normalized: **A = 79, B = 73.5**, rounded to **A:81 B:74** after Round-2 adjustments (A gains on C1 from B's concession on cross-cutting resume; B gains on C5 from A's partial concession on operational risks).

## 3. Overall Justification

**Variant A (81)** — Wins on architectural clarity: wave-aligned milestones (M2=Wave 0, M3=Wave 1, M4=Wave 2, M5=Wave 3) trace 1:1 to the spec's architectural document and produce sharper, more reviewable exit criteria. A's M1 (29 items) is achievable in 2 weeks; B's M1 (45 items in 1 week) is calendar-implausible even granting the "declarations not implementations" framing. A's 10-risk register is well-curated; B's 23 risks include genuine process failures (R-020 to R-022) inflated to risk status. A loses ground on operational rollout (no dedicated runbook/rollback items) and pre-resolution of OQ-007/008.

**Variant B (74)** — Wins on operational discipline (M8 elevates runbook, env readiness, rollback to first-class items the debate showed A genuinely omits) and proactive OQ resolution (INV-005/INV-007 enumerated as M4 items with owners+targets). B's M2 concern-bundling (dispatch+state+transport+observability together) has merit for cohesion but creates a 26-item, 2-week milestone with 4 specialist dimensions — bottleneck risk A correctly flagged. B's 1-week M1 is the strongest single weakness; the 45 items cannot review-and-approve in 5 days even as contract declarations.

## 4. Base Variant Selection: **A**

**Rationale:** A's wave-aligned decomposition is the load-bearing architectural choice that the merged variant must preserve — it's the only structure that lets readers trace any item back to a wave and any wave back to a milestone, which matters for a HIGH-complexity (0.85) spec with 5 IMM + 7 INV invariants to enforce. A's M1 scope is also the right floor (29 items, not 45) because committing AC-001 through AC-019 as M1 exit criteria — when AC-008 (tmux dependency) doesn't ship until M5 and AC-011 (no scoring) is enforced in M5 — is documentation theater that B's "declarations" framing doesn't escape. A's risk register and dependency graph are tighter starting material to merge into than B's.

The Round-2 convergence assessment itself recommends "Sonnet's scoping discipline with Opus's wave-architecture clarity" — wave-architecture clarity is structural and hard to graft post-hoc; scoping discipline is content-level and grafts easily. Start from A; import B's missing items.

## 5. Improvements to Incorporate from Variant B

| # | B contribution | Where to land in merged A | Debate evidence |
|---|---|---|---|
| I1 | **Dedicated operational rollout milestone** (B-M8 → merged M9 or fold into M8) — OPS-001 runbook, OPS-002 env readiness, OPS-003 observability procedure, OPS-004 rollback, OPS-005 lens contribution policy, OPS-006 post-release metrics | Add as new M9 (1 week) OR expanded M8 section "Operational Handoff" | A conceded R-020/R-021/R-022 have merit if dedicated milestone stands; A's roadmap has zero rollback items (gap acknowledged) |
| I2 | **Pre-resolve OQ-007 (INV-005) and OQ-008 (INV-007) as M2-exit items with owners+targets** | Add to A's M2 Open Questions table with Architect+DevOps owners, "Before M3 entry" targets — or promote to M2 items with explicit resolution deliverable | Both variants converged: OQ-007/008 must resolve before M2 dispatch is built; A's "defer" framing risks drift |
| I3 | **Caller-side empty-pool failure semantics (INV-007)**: structured `failed`/`env-missing` contract when output dir creatable; pre-output abort otherwise | Add to A's M2 preflight items (between IMM-4 and COMP-022) | B's INV-007 framing resolves OQ-008 deterministically |
| I4 | **Worker-count vs model-pool guard (INV-005)** as explicit M2 preflight item | Add to A's M2 between IMM-4 and FR-009 | B's INV-005 makes the OQ-007 resolution actionable |
| I5 | **Bundled per-lens output templates as explicit M4 deliverables** (B's COMP-035) | Add COMP-035 row to A's M4 table; A elides per-lens templates beyond bare-review | B's M3-COMP-035 makes recipe/template alignment testable |
| I6 | **MIG-001 through MIG-004 explicit migration items** (source-first sync, package entry registration, legacy shell retirement, release notes) | Add to A's M8 — A bundles these implicitly under FR-029; B's enumeration is auditable | B's M7 enumeration prevents "forgot to register package entry" failures |
| I7 | **TEST-001 through TEST-008 enumerated test items** | Replace A's single-line NFR-007 in M8 with B's enumerated test rows (without elevating to dedicated validation milestone) | A conceded distributed tests need a consolidation surface; per-test enumeration without separate milestone is the convergent path |
| I8 | **Risk consolidation: R-014/R-015/R-016 merge to one validation-coverage risk** (B's own concession) | Apply to merged risk register — don't import all 23 B risks verbatim | B conceded granularity over-fitting |
| I9 | **OQ-010 `validate-lenses` failure semantics resolution path** with Architect+QA owner | Add to A's M2 open questions | Both agree this blocks CI integration |
| I10 | **Timeline label honesty: explicit buffer rather than padding** — keep A's 16-week structure but label M2/M5 buffer weeks explicitly, OR compress to ~14 weeks with explicit "M2.5 stabilization" / "M5.5 integration" buffer milestones | Apply to merged Timeline Estimates section | Both variants converged: timeline buffer should be explicit, not distributed slack |

## 6. Merge Directives Summary

1. Keep A's wave-aligned 8-milestone spine (M1-M8) as the skeleton.
2. Add a 9th milestone "M9: Operational Handoff" (1 week) absorbing B's OPS-001 through OPS-006 — net timeline becomes 17 weeks, or 15 weeks if M6/M7 parallelize per A's note.
3. Import B's INV-005, INV-007 as explicit M2 items; promote OQ-007/008 resolution to M2-exit gates.
4. Enumerate B's TEST-001..TEST-008 inside A's M8 (no new validation milestone).
5. Add COMP-035 per-lens output templates to A's M4.
6. Replace A's FR-029 monolith with B's MIG-001..MIG-004 enumeration in M8.
7. Merge risk registers: keep A's 10 as base; add B's R-008 (lens sprawl, distinct from A's R-1 framing), R-022 (env readiness), R-020/R-021 consolidated as one ops-readiness risk. Do not import B's R-014/R-015/R-016 separately (B conceded these merge).
8. Label timeline buffer explicitly in the merged Timeline Estimates table.
