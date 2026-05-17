# Synthesis 01 — TDD §1-§4 (Executive Summary, Problem Statement, Goals, Success Metrics)

**Status:** In Progress
**Date:** 2026-05-14
**Scope:** TDD §1 Executive Summary · §2 Problem Statement & Context · §3 Goals & Non-Goals · §4 Success Metrics
**Sources:** research/00-prd-extraction.md, research/14-invariant-preservation.md, research/15-data-models.md, qa/research-gate-consolidated.md
**Applied constraints:** SC-1..SC-8 (research-gate-consolidated.md)

---

## §1 Executive Summary

**WHAT.** This release imports six strictly-additive functional requirements (FR-CONV.1..6) into the `task-builder` skill via an *intent-port* from `sc-tasklist` — adopting the *intent* of proven sc-tasklist mechanisms while re-expressing them in task-builder's idiom rather than copying code. Per the G6 four-case conflict rule (PRD§5), four FRs are CASE-D adopt-adapted ports (PR-06→FR-CONV.1, PR-01→FR-CONV.2, PR-07→FR-CONV.4, PR-02→FR-CONV.5 — each with a conflict-register row naming the conflicting mechanism and protected invariant) and two are CASE-B silent-adopt ports (PR-04→FR-CONV.3, PR-03→FR-CONV.6 — no conflict, no register row). PR-05 (Tier-History Advisory) is explicitly DEFERRED to Phase-2 (PRD§1).

**WHY.** The six FRs close three structural-rigor gaps in the pre-merge task-builder gate topology: no task-level executor-readability summary, no structural gate checks for placeholder/DAG/granularity/format consistency, and an implicit inherited-verdict passthrough between rf-qa and rf-qa-qualitative that risks rubber-stamping. They also attack the oscillation cost surfaced empirically in FINAL-REPORT §6.2 F2 — a 21-retry / 18-batch oscillation loop with silent partition-agent exhaust — by adding monotonicity halt conditions and a synthetic Do-Not-Silently-Pass (DNSP) finding.

**HOW.** Delivery is governed by strictly-additive A-002 governance: no existing rf-qa check is renamed, renumbered, or removed (PRD§2 FR-CONV.1 negative criterion); each FR has per-FR rollback granularity (a single revertable append line per K-001/K-005); the G6 four-case rule classifies every proposal; and five load-bearing invariants — self-contained-item, evidence-bound-item, persistent-`.dev/tasks/`-artifact, zero-trust QA, parallel-research — are preserved and provable via NFR-CONV.6..10 fixtures (research/14 §3-§4). One synthesis-time contradiction is carried forward: PRD §25.4 asserts the per-item 5-field schema `{Description, Context, Acceptance, Confidence, Verification}` is "preserved unchanged" at `SKILL.md:1452-1457`, but that range currently holds a different `{Context, Action, Output, Verification, Completion gate}` phase-template (research/15 §7 D-1; SC-1). This is forwarded to TDD §22 Open Questions for Engineering Lead resolution and must not be silently resolved at synthesis time.

**Key Deliverables**
- **Six FRs landing in strict serial order:** PR-06 (FR-CONV.1) → PR-01 (FR-CONV.2) → PR-04 (FR-CONV.3) → PR-07 (FR-CONV.4) → PR-02 (FR-CONV.5) → PR-03 (FR-CONV.6) (SC-6 corrected ordering).
- **NFR-CONV.6..10 invariant preservation** provable on synthetic fixtures — every invariant maps to a falsifiable pass/fail fixture (research/14 §4).
- **`make verify-sync` PASS after each FR merge** — all FRs touch `src/superclaude/` paths exclusively; sync-discipline (A-001) enforced per merge (PRD§6 K-009).

---

## §2 Problem Statement & Context

### §2.1 Background

Pre-merge, task-builder runs a **four-stage gate topology** (research-gate / synthesis-gate / report-validation / task-integrity / qualitative, with per-gate fix-cycle caps in `rf-task-builder.md` I16 lines 352-358, NOT in rf-qa.md — SC-4). The task-integrity gate (rf-qa A.10) carries a **9-item checklist** (`SKILL.md:898-906`, mirrored as a 15-item validation block at `SKILL.md:1491-1507`). The downstream rf-qa-qualitative adversarial pass uses a **generic adversarial stance** with no named-axis annotation. Retry loops have **no monotonicity halt** — a fix cycle that fails to shrink the failure set simply re-runs. Partition agents (rf-analyst / rf-qa cohorts) **silently exhaust** their escalation ladder, aborting the gate without surfacing a finding.

### §2.2 Problem Statement

**Core problem:** task-builder's gate enforces evidence and zero-trust QA at the *item* level but lacks task-level structural rigor, an explicit inter-agent verdict channel, and retry-loop convergence guards — letting structural defects, rubber-stamp passthrough, and oscillating retry loops escape or burn fix-cycles.

- **Gap A — no task-level executor-readability summary.** Generated MDTM files have per-item context but no task-level `## Execution Context` header (References / Source areas / Key constraints), so an executor cannot orient without reading every item.
- **Gap B — no structural gate checks.** rf-qa A.10 has no checks for placeholder/title-only items, circular dependencies (DAG), granularity (XL items lacking subtasks), or Confidence/Verification format consistency.
- **Gap C — implicit inherited-verdict passthrough.** rf-qa's task-integrity verdict reaches rf-qa-qualitative only implicitly; without an explicit `## Inherited Structural Verdict` block plus a Self-Audit obligation, rf-qa-qualitative risks rubber-stamping rf-qa PASS items as semantically VERIFIED (K-003 inflation risk).
- **Gap D — silent partition exhaust + retry oscillation.** Partition-agent escalation-ladder exhaust aborts silently; retry loops have no halt-on-regression / halt-on-non-shrink condition. Empirical evidence: a 21-retry / 18-batch oscillation loop (FINAL-REPORT §6.2 F2).

### §2.3 Business Context

The release is scoped against the Reference Platform PRD. The dominant cost driver is the **token-cost ceiling: ≤10% increase** over the pre-merge task-builder baseline per equivalent BUILD_REQUEST (NFR-CONV.4, PRD§3). All gate additions are local checks using only existing tooling (Read, Grep, Glob, Bash) with no new external dependencies or synchronous network calls (NFR-CONV.5), keeping wall-clock impact bounded.

---

## §3 Goals & Non-Goals

### Goals

| ID | Goal | Success Criteria |
|----|------|------------------|
| **G1** (FR-CONV.1) | Append 8 structural checks (TB-Add-1..8) to rf-qa A.10 + 15-item validation block | Each TB-Add-1..8 fires a distinct, item-ID-naming error on violation; TB-Add-1..7 (excl. 2) block the gate; TB-Add-2 emits `[ADVISORY]` and does not block (PRD§2) |
| **G2** (FR-CONV.2) | Insert task-level `## Execution Context` header in generated MDTM files | Header renders exactly 3 labeled lines (References / Source areas / Key constraints); minimal BUILD_REQUEST degrades to References-only with WHY/source-area lines explicitly omitted (PRD§2 FR-CONV.2) |
| **G3** (FR-CONV.3) | Inject `## Inherited Structural Verdict` block + Self-Audit obligation into rf-qa-qualitative spawn | Spawn prompt carries rf-qa verdict table verbatim; rf-qa-qualitative emits a `## Self-Audit` entry on first 5 runs listing relied-on PASS items AND ≥1 semantic check where PASS is insufficient (INV-019, K-003) |
| **G4** (FR-CONV.4) | Insert "Five Adversarial Axes" overlay before the 15-item task-qualitative checklist | Items Reviewed table `axis` column populated from {drift, contradictions, omissions, weakened-criteria, invented-content, none}; `drift-axis-inactive` annotation emitted when no item captures BUILD_REQUEST.GOAL baseline (PRD§2 FR-CONV.4) |
| **G5** (FR-CONV.5) | Add monotonicity + regression halt guards to existing retry loops | `[HALT-MONOTONICITY]` fires when `F_{n+1} >= F_n`; regression halt fires (precedence over monotonicity) when an item PASS@N is FAIL@N+1; dedup-key synthetic findings do not trigger regression halt (INV-012); all halt fixtures pass |
| **G6** (FR-CONV.6) | Emit synthetic-dnsp HIGH finding on partition escalation-ladder exhaust | 5-field finding emitted with dedup-key `(assigned_files_range, escalation_ladder_exhaust_point)`; identical dedup-keys collapse with `found N times`; all-agents-fail guard preserved — zero synthetic emits, existing `rf-team-lead.md:417` escalation runs (SC-2) |
| **G7** (overall) | Preserve all 5 load-bearing invariants | NFR-CONV.6..10 synthetic fixtures PASS — every invariant has a falsifiable fail-closed fixture (research/14 §4) |

### Non-Goals

| ID | Non-Goal | Disposition |
|----|----------|-------------|
| **NG1** | Bulk-port all 17 sc-tasklist gate checks | REJECTED per CB-3 — per-check classification only, not bulk import |
| **NG2** | Modify tier selection based on historical pattern (X-004) | REJECTED — hidden-input determinism guard (NFR-CONV.3) forbids it |
| **NG3** | Replace rf-qa-qualitative's existing 15-item checklist (X-002) | REJECTED — axes annotate, they do not substitute |
| **NG4** | PR-05 Tier-History Advisory | DEFERRED to Phase-2 per release-spec §2.1 |
| **NG5** | Roadmap regeneration / downstream tasklist generation | Out of scope — this release touches task-builder gate behavior only |
| **NG6** | Any structural change to `.dev/tasks/` directory layout | Out of scope — INV-018 / persistent-`.dev/tasks/`-artifact invariant held inviolate |

### Future Considerations (Phase-2 deferrals, PRD §12.3)

- **PR-05 re-evaluation** when `.dev/tasks/done/TASK-RF-*` reaches ≥10 tasks spanning ≥3 distinct task_types (OPEN-PR05).
- **TB-Add-2 calibration** — item-count bounds (≥3 / ≤40 track / ≤50 single-track) stay `[ADVISORY]` until an empirical calibration sweep on `.dev/tasks/done/` produces thresholds (OPEN-INV-006).
- **`.dev/tasks/` layout versioning** — a layout-change contract; if the directory layout changes, all 7 proposals require re-integration (OPEN-INV-018).

---

## §4 Success Metrics

### §4.1 Technical Metrics

| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| Single-pass gate PASS rate | ≥80% | ↑ post-merge | Fraction of BUILD_REQUESTs passing task-integrity gate on first cycle |
| Placeholder-defect detection rate | n/a (no check pre-merge) | 100% on synthetic fixtures | TB-Add-1 fires on every placeholder/title-only fixture item |
| DAG-cycle detection rate | n/a (no check pre-merge) | 100% on synthetic fixtures | TB-Add-4 fires on every circular-dependency fixture |
| Self-Audit coverage post-FR-CONV.3 | n/a | 100% on first 5 runs | Every rf-qa-qualitative run carries a `## Self-Audit` entry (K-003 audit target, OPEN-X-002) |
| `[HALT-MONOTONICITY]` emission rate | n/a | <10% | >50% emission rate alerts upstream BUILD_REQUEST defect, not a guard defect |
| Synthetic-dnsp emission count | n/a | ≥1 on twice-exhaust fixture; 0 on healthy run | Inject twice-timeout partition fixture → ≥1 finding; healthy run → 0 |

### §4.2 Business Metrics

- **Token-cost ratio** post-merge / pre-merge **≤1.10** on 5 representative BUILD_REQUESTs (NFR-CONV.4; OPEN-TOKEN — empirical post-merge measurement; contingency K-010 = FR-CONV.3 verdict-table summarisation if exceeded).
- **Fix-cycle convergence rate** ≥75% baseline, expected ↑ post-merge — fraction of fix-cycle sequences that converge to gate PASS rather than hitting the per-gate cap or a monotonicity halt.

---

**Status:** Complete
