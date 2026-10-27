# D-0091 — Consolidated GA-Readiness Governance Table (T07.10)

**Task:** T07.10 (Phase 7 — M7)
**Roadmap items:** R-151
**Date:** 2026-05-18
**Branch:** `feat/hook-sync-and-matcher-fix`
**Tier:** STANDARD
**Verification method:** Direct enumeration check (6 FF_* + 6 MET-* + 7 OPS-*)
**Audience:** GA-tagging committee (v3.9 release gate)
**Overall: PASS** (4/4 acceptance criteria met)

---

## 0. TL;DR

This single-page artifact aggregates every flag, metric, and runbook
relevant to the GA-tagging decision for **Task-Builder Convergence
v3.9**. It is the load-bearing input to the GA-tagging committee at
T07.20 (MIG-007b) and the durable governance reference cited by
release-spec §8.3 audit rows and the M7 §M7 governance section.

- **6 logical feature flags** — one per FR-CONV.X (FR-CONV.1..6), each
  with owner, cleanup window, and revert path.
- **6 observability metrics** — MET-001..006, each with target /
  threshold and the OPS runbook(s) it triggers.
- **7 operational runbooks** — OPS-001..007, each with response SLA
  and 5-section structure (symptoms / diagnosis / resolution /
  escalation / prevention).

The table reproduces the roadmap §M7 *Consolidated GA-Readiness
Governance Table* (roadmap.md:446-470) verbatim in column order so the
GA-tagging committee can read a single page without traversing the
roadmap.

---

## 1. Audience and scope

**Primary audience:** GA-tagging committee at T07.20 (MIG-007b).
**Secondary audience:** task-builder maintainers on-call rotation
(consumed via integration point at roadmap.md:477).

**Scope:** Only enumerated artifacts that gate the v3.9 GA tag. This
table does NOT replace per-FR feature-flag rows in the originating
milestone tables (M1..M6) — those remain authoritative for per-FR
rollback envelopes. This page is the *consolidated* dual-presentation
artifact called out at roadmap.md:596.

---

## 2. Consolidated Governance Table

|Flag / Metric / Runbook|Type|Default / Threshold|Owner|Cleanup / Action Window|Source FR|
|---|---|---|---|---|---|
|FF_TB_ADD_1_THROUGH_8|Logical flag|Enabled at merge|rf-qa maintainer|GA+30d; TB-Add-2 stays ADVISORY until Phase-2 (OPEN-INV-006)|FR-CONV.1|
|FF_EXECUTION_CONTEXT_HEADER|Logical flag|Enabled at merge|task-builder maintainer|GA+30d; fallback References-only natural rollback|FR-CONV.2|
|FF_INHERITED_STRUCTURAL_VERDICT|Logical flag|Enabled at merge|QA Lead|Post-K-003 audit pass (release-spec §8.3 row 4); rollback disables passthrough|FR-CONV.3|
|FF_FIVE_ADVERSARIAL_AXES|Logical flag|Enabled at merge|rf-qa-qualitative maintainer|GA+30d post-axis-distribution audit (K-004); rollback removes overlay|FR-CONV.4|
|FF_RETRY_MONOTONICITY_GUARDS|Logical flag|Enabled at merge|rf-task-builder maintainer|GA+30d post false-halt-rate audit (K-005); rollback disables guards individually|FR-CONV.5|
|FF_SYNTHETIC_DNSP_EMISSION|Logical flag|Enabled at merge|rf-analyst / rf-qa maintainers|GA+30d post-emission-count audit (K-006); rollback removes DNSP sites|FR-CONV.6|
|MET-001|Single-Pass PASS Rate|Target ≥80% on 5 BUILD_REQUESTs|Engineering|NFR-CONV-R1 first-cycle measurement; sub-threshold → review fix-cycle prompts|All FRs|
|MET-002|Detection Rate|100% unresolved-token + 100% DAG-cycle on synthetic fixtures|Engineering|Sub-100% → TB-Add-1 / TB-Add-4 calibration review|FR-CONV.1|
|MET-003|Self-Audit Coverage|100% on first 5 rf-qa-qualitative runs; ≥1 independent semantic check each|QA Lead|Sub-100% → block release; trigger OPS-001|FR-CONV.3|
|MET-004|Halt Rate (combined)|HALT-MONOTONICITY >50% → OPS-004; regression-halt >20% → OPS-005|rf-task-builder maintainer|Offline-grep aggregation per release; sampling cadence weekly|FR-CONV.5|
|MET-005|DNSP Emission|twice-exhaust fixture ≥1; healthy run = 0; production >0 → review|rf-qa maintainer|>0 emissions in production triggers OPS-002 triage within 24h|FR-CONV.6|
|MET-006|Token-Cost Ratio|≤1.10 (post-merge / pre-merge)|Engineering Lead|>1.10 → K-010 contingency (summarise FR-CONV.3 verdict table); measured on 5 BUILD_REQUESTs across Quick/Standard/Deep tiers|All FRs (NFR-CONV.4)|
|OPS-001|K-003 audit runbook (first 5 rf-qa-qualitative runs)|Operational|QA Lead|4 business hours response SLA; gauge target 100% Self-Audit coverage on first 5 runs|FR-CONV.3|
|OPS-002|DNSP triage runbook|Operational|rf-qa maintainer|24-hour response SLA; weekly inspection cadence; escalate ≥3 distinct dedup-keys/week|FR-CONV.6|
|OPS-003|All-partitions-exhaust HALT runbook|Operational|rf-team-lead maintainer|Activates on zero-success path; mutual-exclusivity check (line-417 escalation fires, NO synthetic-dnsp emitted)|FR-CONV.6|
|OPS-004|HALT-MONOTONICITY rate runbook|Operational|rf-task-builder maintainer|Threshold >50% of batches; resolution path = improve upstream BUILD_REQUESTs or TB-Add-2 calibration (OPEN-INV-006)|FR-CONV.5|
|OPS-005|Regression-halt rate runbook|Operational|Engineering Lead|Threshold >20% of batches; resolution path = tighten fix-cycle prompts (X-003 stays REJECTED)|FR-CONV.5|
|OPS-006|`make verify-sync` failure runbook|Operational|Per-commit author|Immediate response SLA; A-001 sync-discipline; K-009 contingency on persistent failure|All FRs|
|OPS-007|`.dev/tasks/` layout-change runbook|Operational|Engineering Lead|Portfolio-wide blast radius (K-008); SP-33 stability commitment; re-integration commit covering all 6 FRs per §19.4|All FRs|

---

## 3. Enumeration check

| Category | Required | Present | Status |
|---|---|---|---|
| FF_* logical flags | 6 | 6 (FF_TB_ADD_1_THROUGH_8, FF_EXECUTION_CONTEXT_HEADER, FF_INHERITED_STRUCTURAL_VERDICT, FF_FIVE_ADVERSARIAL_AXES, FF_RETRY_MONOTONICITY_GUARDS, FF_SYNTHETIC_DNSP_EMISSION) | PASS |
| MET-* metrics | 6 | 6 (MET-001..006) | PASS |
| OPS-* runbooks | 7 | 7 (OPS-001..007) | PASS |
| **Total rows** | **19** | **19** | **PASS** |

Each row carries a cleanup window / SLA / threshold per roadmap §M7
Consolidated Governance Table (roadmap.md:450-470). The GA-tagging
committee is identified as the audience per §1.

---

## 4. Cross-references

- **Roadmap §M7 Consolidated Governance Table** —
  `roadmap.md:446-470` (verbatim source of column order and content).
- **Roadmap §M7 Integration Points** — `roadmap.md:472-479` (where
  this artifact is consumed at GA tag).
- **Release-spec §8.3 audit rows** — governance baseline for ongoing
  inspection of MET-* counters.
- **MIG-007b GA tag gate (T07.20)** — this artifact is a hard
  pre-requisite (acceptance criterion #4 of T07.10; dependency edge
  T07.10 → T07.20).
- **OPS runbook artifacts** —
  OPS-001 D-0092 (T07.11),
  OPS-002 D-0093 (T07.13),
  OPS-003 D-0094 (T07.14),
  OPS-004 D-0095 (T07.15),
  OPS-005 D-0096 (T07.16),
  OPS-006 + OPS-007 D-0097 (T07.17).
- **MET instrumentation** — D-0098 (T07.19) wires offline-grep
  aggregation for all 6 MET-* metrics.

---

## 5. GA-tagging decision use

The GA-tagging committee reads this single page at T07.20 (MIG-007b)
and confirms, in order:

1. All six FF_* logical flags have an explicit cleanup window —
   either GA+30d (post-audit) or post-K-003-audit-pass.
2. All six MET-* metrics have a numerical threshold and a binding to
   an OPS runbook (or release-block path).
3. All seven OPS-* runbooks have a response SLA and a documented
   owner.

If any row in §2 lacks one of these three properties at the time of
GA tag inspection, the committee withholds the v3.9 tag and routes
the gap back to the originating FR-CONV.X / MIG task for remediation
(per §M7 R-M7-3 mitigation at roadmap.md:501).

---

## 6. Acceptance criteria — T07.10

| # | Criterion | Status |
|---|---|---|
| 1 | File `TASKLIST_ROOT/artifacts/D-0091/spec.md` exists and lists exactly 6 FF_* flags, 6 MET-* metrics, 7 OPS-* runbooks. | PASS (§2 + §3) |
| 2 | Each row includes cleanup window / SLA / threshold per roadmap §M7 Consolidated Governance Table. | PASS (§2 column 5) |
| 3 | GA-tagging committee referenced as the audience. | PASS (§1, §5) |
| 4 | Evidence at `TASKLIST_ROOT/artifacts/D-0091/evidence.md`. | PASS (see sibling file) |

**Verdict: PASS** — single-page consolidated governance table is
decision-ready for the GA-tagging committee.
