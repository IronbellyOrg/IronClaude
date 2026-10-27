---
base_variant: opus
variant_scores: "opus:82 haiku:74"
---

# Variant Evaluation — Roadmap Merge Selection

## 1. Scoring Criteria (derived from debate)

| # | Criterion | Weight | Rationale |
|---|---|---|---|
| C1 | Milestone granularity & gate clarity (D1) | 15 | Debate's central D1 dispute on 5-vs-6 milestones, SC1/SC5 gate separation |
| C2 | CLI/contract sequencing rigor (D2, D3) | 15 | Stub-flag drift vs contract-first; OQ-7 closure timing |
| C3 | Deliverable & test enumeration granularity (D4, D10) | 10 | Per-primitive tracking vs first-class TEST-XXX deliverables |
| C4 | Security & containment depth (FR-SCH2, FR-ISO2, NFR-SEC2/3) | 15 | Path-traversal, symlink, HOME containment correctness |
| C5 | OQ management & resolution sequencing (D5, D6) | 10 | Contract-shaping vs empirical OQs; M2 NOTICE entry |
| C6 | Risk register quality & consolidation (D9) | 8 | Debate noted Haiku double-counts RR-008/011, RR-002/015 |
| C7 | Effort/timeline honesty (D12, D7) | 10 | 7d vs 14d eval window; day-vs-week presentation |
| C8 | Architecture/integration fidelity to spec | 10 | IsolationLayers extension, ThreadPoolExecutor, N′-vs-K |
| C9 | Documentation & decision-ledger discipline | 7 | ADR sign-offs, PROVENANCE, NOTICE, decisions.md cross-refs |

## 2. Per-Criterion Scores

| Criterion | Opus (A) | Haiku (B) | Notes |
|---|---|---|---|
| C1 Granularity | 13/15 | 11/15 | Opus's separate M6 enables atomic SC1/SC5 gate; Haiku folds into M5 exit criteria (defensible but loses observability) |
| C2 CLI sequencing | 13/15 | 10/15 | Opus M4 placement avoids OQ-7 churn; Haiku M1 contract-first depends on synchronous OQ closure that debate showed is fragile |
| C3 Enumeration | 8/10 | 8/10 | Opus per-primitive (COMP-010.1–6, E2.1–3) gives PR-level DoD; Haiku TEST-XXX gives audit ledger — debate called this a tie, philosophical |
| C4 Security | 14/15 | 13/15 | Both strong; Opus adds explicit NFR-SEC1 negative test set + AC12 allowlist enforcement step; Haiku has equivalent TEST-002/003 but less explicit pre-FS-write ordering |
| C5 OQ mgmt | 8/10 | 7/10 | Opus distinguishes contract-shaping vs empirical (OQ-10 empirical in M5); Haiku front-loads 6 OQs to M1 entry — debate conceded this is too rigid for OQ-10 |
| C6 Risk register | 7/8 | 5/8 | Opus R1–R9 consolidated; Haiku RR-001..015 double-counts disk/RAM (RR-008+RR-011) and scope creep (RR-002+RR-015); debate explicitly favored consolidation |
| C7 Timeline | 7/10 | 8/10 | Haiku's 14d eval window matches realistic 0.93d/eval velocity; Opus's 7d is optimistic per debate. Haiku wins this criterion |
| C8 Architecture | 9/10 | 8/10 | Both cite same anchors (executor.py:107-182, cli/prd/executor.py:774-802). Opus has tighter N′-vs-K invariant phrasing and more explicit reuse adapters (COMP-013, COMP-014, COMP-015 probes) |
| C9 Documentation | 6/7 | 5/7 | Opus dedicates M6 with OPS gates; Haiku scatters OPS-001..005 across milestones — works but harder to audit as a "release-readiness" gate |

## 3. Overall Scores

| Variant | Score | Justification |
|---|---|---|
| Opus (A) | **82/100** | Implementation-sequencing rigor: clean dependency chain, separate hardening gate, consolidated risk register, contract-vs-empirical OQ split, explicit defense-in-depth ordering. Weaker on eval-window estimation. |
| Haiku (B) | **74/100** | Contract-first stakeholder framing, more realistic eval-authoring timeline, first-class TEST-XXX auditability. Loses points on inflated risk register, fragile front-loaded OQ gating, and bundled M5 release gate. |

## 4. Base Variant Selection: **Opus**

Rationale anchored in debate:

1. **Convergence assessment §"Recommended Merge Posture" explicitly endorses Opus's structure** for D4 (per-primitive enumeration), D9 (risk consolidation), and D1 (6-milestone) when maintainer wants a distinct release-readiness gate — which is the SC1/SC5 design intent of the spec.
2. **Opus's rebuttals on D2 (OQ-7) and D5 (OQ-10) were not refuted** — Haiku conceded OQ-10 empirical resolution and partially conceded D6 (NOTICE M2 not M1).
3. **Opus's defense-in-depth ordering** (FR-SCH2 pre-FS-write → FR-ISO2 post-creation symlink resolve → NFR-SEC2/3 attack tests) maps 1:1 to the spec's security guards; Haiku's TEST-002/003 cover the same surface but the sequencing in deliverables is implicit, not explicit.
4. **Risk register consolidation** — debate's §Areas of Agreement #3 explicitly recommends Opus's R1–R9 over Haiku's RR-001..015 regardless of base.
5. Opus's 99-deliverable enumeration with per-primitive IDs (COMP-010.1–6, E2.1–3) gives merger a more granular substrate to graft Haiku's contributions onto.

## 5. Improvements to Incorporate from Haiku (B)

These map to debate concessions and unrebutted Haiku strengths:

| # | Source | Improvement | Insertion Point in Opus |
|---|---|---|---|
| I1 | D6 convergence | Move NOTICE/LICENSE (OQ-4-res) from M6 to **M2 entry blocker** | Promote `OQ-4-res` from M6 deliverable #91 to M2 entry criterion; keep NFR-MAINT1 in M1 |
| I2 | D12 unrebutted | Extend eval-body window from 7d → **14d** in M5 | Update M5 Duration "7 days" → "14 days"; update Timeline table Day 20 → Day 33; total 28 → 35 working days |
| I3 | D10 Haiku strength | Add **first-class TEST-XXX ledger** alongside embedded AC | Add TEST-001 (schema/ID rejection), TEST-006 (PTY lifecycle), TEST-007 (reporter contract), TEST-008 (exit-code semantics), TEST-009 (artifact reproducibility), TEST-013 (coverage gate) as new deliverables cross-linking to existing AC fields |
| I4 | D3 compromise | Land **ExpectDSL interface (COMP-010) in M1**, primitives (COMP-010.1–6) remain in M4 | Move COMP-010 from M4 to M1 (after DM-002); keep COMP-010.1–6 in M4 with explicit dep on M1 interface |
| I5 | Haiku OPS deliverables | Add **OPS-001..OPS-005** (decision closure, scratch root policy, artifact retention, validation command set, release checklist) | Distribute: OPS-001→M1, OPS-002→M2, OPS-003→M4, OPS-004→M4, OPS-005→M6 |
| I6 | Haiku C7 strength | Add **RAM headroom note** for `--parallel 15` (~2.25GB) to M3 NFR-PERF2 and Infrastructure Requirements section | Augment NFR-PERF2 AC with "free RAM warning ≥2.25GB before clamp accept" |
| I7 | Haiku Decision Summary clarity | Adopt Haiku's **Decision Summary "Validation order"** row (schema+ID before FS ops) | Add row to Opus Decision Summary |
| I8 | Haiku MIG entries | Add **MIG-002 (eval-batch rollout)** and **MIG-003 (platform follow-up plan)** as planning deliverables in M5/M6 | Add to M5 deliverables list (batches of 3–5 evals per PR per R9 mitigation); MIG-003 to M6 alongside OQ-9-res |

## 6. Items Explicitly NOT Adopted from Haiku

- Haiku's 5-milestone collapse (M5 = evals + release). Debate left D1 unresolved but convergence recommendation defers to maintainer preference for distinct release gate — spec SC1/SC5 favors separation.
- Haiku's M1 CLI placement (D2). OQ-7 closure cannot be guaranteed at M1 entry; Opus M4 placement is safer per Opus's unrebutted rebuttal.
- Haiku's expanded RR-001..015 risk register. Debate §Agreement #3 explicitly favored Opus's R1–R9 consolidation.
- Haiku's week-level effort sizing (D7). Day-level is more actionable for sprint planning; low-stakes per debate.
