# D-0098 Spec — T07.19 MET-001..006 Observability Counter Instrumentation

**Task:** T07.19 — Instrument MET-001..006 observability counters
**Phase:** Phase 7 — M7 Production Readiness + GA
**Roadmap Item IDs:** R-159 (MET-001), R-160 (MET-002), R-161 (MET-003), R-162 (MET-004), R-163 (MET-005), R-164 (MET-006)
**Date published:** 2026-05-18
**Branch:** `feat/hook-sync-and-matcher-fix`
**HEAD at publication:** `efaa33db9f0087bb1c48236b12c1287171b4f9f8`
**Tier:** STANDARD
**Verification Method:** Direct test execution (offline-grep aggregation against the deterministic test surfaces that gate each metric, plus runtime QA-report scans)
**MCP Requirements:** Sequential (Preferred) — applied for cross-reference reasoning
**Instrumentation owner (per roadmap §M7 governance table):** see §3 column "Owner" per metric
**Overall: PASS** (5/5 acceptance criteria met — see §6)

---

## 0. TL;DR

This artifact wires the six post-merge observability counters required
by the M7 governance table (roadmap.md:458-463) onto deterministic,
already-present test and runtime-grep surfaces. No new MCP servers,
libraries, or services are introduced (NFR-CONV.5 preserved); every
counter is computed by re-running an existing pytest target or by
grepping artefacts already produced by the standard task-builder
pipeline (`.dev/tasks/<task-id>/qa/`).

Each counter is bound to the OPS-* runbook(s) it triggers, so a single
release inspection round can mechanically classify any threshold
breach to the runbook that owns the response — closing the loop from
the consolidated governance table (D-0091) through the runbooks
(D-0092..D-0097) to the metric instrumentation here.

---

## 1. Specification (verbatim from authority)

The six MET-* counters are defined at three loci that all agree on
target / threshold and OPS binding:

| Source | Location | Verbatim binding |
|---|---|---|
| Roadmap §"Items" rows (M7 observability block) | `roadmap.md:438-443` | "MET-001 Single-Pass Gate PASS Rate measurement … target:≥80%; MET-002 unresolved-token-detection:100%; DAG-cycle-detection:100%; MET-003 window:first-5-runs; target:100%; semantic-checks:≥1-each; failure:block-release; MET-004 synthetic-dnsp:>0-triggers-OPS-002; monotonicity-alert:>50%-triggers-OPS-004; regression-alert:>20%-triggers-OPS-005; offline-grep-aggregate-per-release; MET-005 twice-exhaust:≥1; healthy-run:0; production-threshold:>0-triggers-review; MET-006 sample:5-BUILD_REQUESTs; tiers:Quick/Standard/Deep; target:≤1.10; contingency:summarise-inherited-verdict-table-if-exceeded." |
| Roadmap §"Consolidated GA-Readiness Governance Table — M7" | `roadmap.md:458-463` | "MET-001 Engineering Target ≥80% on 5 BUILD_REQUESTs (NFR-CONV-R1); MET-002 Engineering 100% TB-Add-1/4 on synthetic fixtures; MET-003 QA Lead 100% on first 5 runs; block release on failure; MET-004 rf-task-builder maintainer HALT-MONOTONICITY>50% → OPS-004; regression>20% → OPS-005; MET-005 rf-qa maintainer >0 in production → OPS-002 review; MET-006 Engineering Lead ≤1.10 target; contingency K-010 summarise inherited verdict." |
| Phase-7 tasklist T07.19 | `phase-7-tasklist.md:870-917` | "MET-001 Single-Pass Gate PASS Rate; MET-002 Detection Rate (unresolved-token + DAG-cycle 100%); MET-003 Self-Audit Coverage; MET-004 Halt Rate (synthetic-dnsp + HALT-MONOTONICITY + regression-halt); MET-005 DNSP Emission; MET-006 Token-Cost (NFR-CONV.4)." |

**PASS criterion (composite for D-0098):**
1. The aggregation method for each MET-* is captured here as a runnable
   command, executable against the current HEAD with `uv run pytest …`
   or `grep …`.
2. Each MET-* is cross-referenced to the OPS-* runbook(s) that responds
   when its threshold trips.
3. MET-002 unresolved-token + DAG-cycle detection both measure 100% on
   their authoritative fixtures.
4. MET-006 target ≤1.10 is documented and bound to D-0084.

**FAIL trigger:** any of the four PASS clauses above missing.
**FAIL consequence:** the GA-tagging committee at T07.20 (MIG-007b)
withholds the v3.9 tag, because the governance table (D-0091) is no
longer mechanically observable.

---

## 2. Measurement model — offline-grep aggregation

All six MET-* counters are evaluated by **re-reading artefacts the
pipeline already produces**, with no new runtime instrumentation
(NFR-CONV.5 §"no new MCP servers / libraries / synchronous network
calls" preserved; T07.03 D-0085 audit). The instrumentation is the
documented command list in §3 below; the "counter" for any metric on a
given release is the literal output of running the listed commands at
that release HEAD.

Two evaluation surfaces are used:

- **Surface A — pytest gates.** For metrics whose threshold is
  enforced by an existing pytest assertion (MET-002 detection rate,
  MET-003 Self-Audit coverage, MET-004 halt-fixture pass-rate,
  MET-005 DNSP-fixture pass-rate), the offline-grep is `uv run pytest
  <fixture> -q` and the counter is the literal exit status (0 = at
  target, non-zero = breach → OPS trigger).
- **Surface B — runtime artefact grep.** For metrics whose threshold
  is measured *across pipeline runs* (MET-001 single-pass PASS rate,
  MET-004 runtime halt-event frequency, MET-005 production DNSP
  emissions, MET-006 token-cost ratio), the offline-grep walks
  `.dev/tasks/<task-id>/qa/*.md` for the established emission strings
  (`Overall Verdict: PASS|FAIL`, `Fix cycle:`, `[HALT-MONOTONICITY]`,
  `"source": "synthetic-dnsp"`) and tallies the result.

Surface A produces a deterministic same-release reading (re-running
the same pytest commands at the same HEAD produces the same exit
codes). Surface B produces a release-window reading whose denominator
is the count of pipeline outputs in `.dev/tasks/` published in that
window — the OPS-001 and OPS-002 runbooks describe the cadence
(`per-release for halt + emission counters`, `4-business-hour SLA on
Self-Audit anomalies`).

---

## 3. MET-001..006 instrumentation table

| MET | Title (verbatim from roadmap) | Threshold | Surface | Offline-grep aggregation command(s) | OPS trigger(s) | Owner | Source FR |
|---|---|---|---|---|---|---|---|
| **MET-001** | Single-Pass Gate PASS Rate measurement | ≥80% first-cycle PASS on 5 BUILD_REQUESTs (NFR-CONV-R1) | Surface B | `grep -l '^## Overall Verdict: PASS$' .dev/tasks/to-do/*/qa/qa-research-gate-report.md` over the 5 sampled BUILD_REQUESTs, divided by 5. Sample anchor: D-0089 spec (T07.08 first-cycle PASS rate measurement). | Sub-threshold → release-block path (review fix-cycle prompts; X-003 stays REJECTED per OPS-005) | Engineering | All FRs (NFR-CONV-R1) |
| **MET-002** | Detection Rate measurement | 100% unresolved-token detection on TB-Add-1 fixtures; 100% DAG-cycle detection on TB-Add-4 fixtures | Surface A | `uv run pytest tests/audit/test_nfr_conv_6_self_contained.py -q` (TB-Add-1 / unresolved-token, stripped fixture FAIL); `uv run pytest tests/audit/test_invariant_preservation_NFR_6_through_10.py -q` (TB-Add-4 / DAG-cycle invariant) | Sub-100% → TB-Add-1 / TB-Add-4 calibration review (rf-task-builder maintainer; OPEN-INV-006 escalation when TB-Add-2 calibration is the lever) | Engineering | FR-CONV.1 (TB-Add-1..8) |
| **MET-003** | Self-Audit Coverage measurement | 100% Self-Audit presence + ≥1 independent semantic check on first 5 rf-qa-qualitative runs post-FR-CONV.3 | Surface A + Surface B | Surface A: `uv run pytest tests/audit/test_self_audit_inv_019.py -q`. Surface B: `grep -c "^## \(Self-Audit\|Inherited Structural Verdict\)" .dev/tasks/to-do/*/qa/qa-qualitative-review.md` across the 5 audit-window runs (must equal 5) — anchor: D-0083 §2.1 (audit population). | Sub-100% → **block release** + trigger **OPS-001** (K-003 audit runbook; QA-Lead 4-business-hour SLA) | QA Lead | FR-CONV.3 (INV-019, K-003 audit-target) |
| **MET-004** | Halt Rate measurement (synthetic-dnsp + HALT-MONOTONICITY + regression-halt) | HALT-MONOTONICITY >50% of fix-cycle batches → OPS-004; regression-halt >20% of batches → OPS-005; synthetic-dnsp >0 in production → OPS-002 | Surface A + Surface B | Surface A (fixture pass-rate): `uv run pytest tests/audit/test_monotonicity_halt_F_5_5_5.py tests/audit/test_regression_halt_pass1_fail2.py -q`. Surface B (production cadence, weekly per OPS-002): `grep -rln '\[HALT-MONOTONICITY\]' .dev/tasks/to-do/*/qa/` and `grep -rln 'regression-halt' .dev/tasks/to-do/*/qa/` divided by total fix-cycle batches in window. | **OPS-002** (synthetic-dnsp >0), **OPS-004** (HALT-MONOTONICITY >50%), **OPS-005** (regression-halt >20%) | rf-task-builder maintainer (HALT-MONOTONICITY, regression-halt); rf-qa maintainer (synthetic-dnsp) | FR-CONV.5 (retry-monotonicity + regression-halt), FR-CONV.6 (synthetic-dnsp) |
| **MET-005** | DNSP Emission measurement | twice-exhaust fixture ≥1 DNSP emission; healthy fixture run = 0 emissions; production >0 → review | Surface A + Surface B | Surface A: `uv run pytest tests/audit/test_dnsp_twice_exhaust.py tests/audit/test_dnsp_dedup_collapse.py tests/audit/test_dnsp_does_not_serialize_cohort.py tests/audit/test_synthetic_dnsp_dedup_not_regression.py -q`. Surface B (production scan): `grep -rln '"source": "synthetic-dnsp"' .dev/tasks/to-do/*/qa/` — healthy production cadence MUST return 0 file matches. | **OPS-002** (DNSP triage runbook; 24-hour SLA, weekly cadence, ≥3 dedup-keys/week escalate); **OPS-003** (all-partitions-exhaust HALT runbook, mutual-exclusivity check) | rf-qa maintainer / rf-analyst | FR-CONV.6 (synthetic-DNSP on partition exhaust) |
| **MET-006** | Token-Cost measurement (NFR-CONV.4) | post/pre token-cost ratio ≤1.10 across 5 BUILD_REQUESTs covering Quick / Standard / Deep tiers | Surface B (derived) | Already computed at T07.02; re-derive by reading `.dev/releases/current/task-builder-merge/artifacts/D-0084/spec.md` §4 ("Pre/Post Token-Count Ratio Table") and asserting the "All 5 ratios ≤ 1.10: TRUE" boolean. | **K-010 contingency** (summarise FR-CONV.3 verdict table rather than verbatim emit) on ratio >1.10. Cross-tied to **OPS-005** when regression-halt rate is the proximate cause of token inflation. | Engineering Lead | All FRs (NFR-CONV.4) |

Six rows, one per MET-001..006. Every row has: threshold, runnable
aggregation command, OPS trigger, owner, and source FR. Mapping
matches the consolidated governance table at D-0091 §2 row-for-row.

---

## 4. Cross-references

- **Roadmap §M7 Items** — `roadmap.md:438-443` (verbatim MET-* row
  definitions; threshold and OPS trigger source-of-truth).
- **Roadmap §M7 Consolidated Governance Table** — `roadmap.md:458-463`
  (audience-of-record column mapping; reproduced verbatim in D-0091
  §2 rows 7-12).
- **D-0091 consolidated governance table** — single-page audience
  artefact at GA-tag. D-0098 here is the *mechanically observable*
  counterpart: every MET-* row in D-0091 §2 has a runnable command in
  §3 above.
- **D-0084 NFR-CONV.4 token-cost ratio** — supplies the MET-006
  measurement directly; §4 of D-0084/spec.md contains the 5-row
  Pre/Post Token-Count Ratio Table whose "All 5 ratios ≤ 1.10" Boolean
  is the MET-006 counter value at this release.
- **D-0083 K-003 first-5-runs audit** — supplies the MET-003 audit
  window (first 5 rf-qa-qualitative runs after MIG-003 anchor
  `ad083b6a`); §2.1 inventory is the denominator for MET-003 Surface
  B aggregation.
- **D-0089 NFR-CONV-R1 first-cycle PASS rate** — supplies MET-001
  empirically (T07.08 acceptance criterion: ≥4 of 5 first-cycle PASS).
- **OPS runbook bindings** — OPS-001 (D-0092) ↔ MET-003; OPS-002
  (D-0093) ↔ MET-004 synthetic-dnsp + MET-005; OPS-003 (D-0094) ↔
  MET-005 mutual-exclusivity; OPS-004 (D-0095) ↔ MET-004
  HALT-MONOTONICITY rate; OPS-005 (D-0096) ↔ MET-004 regression-halt
  rate; OPS-006 + OPS-007 (D-0097) are sync / layout runbooks not
  bound to MET-* counters (they govern environment integrity rather
  than pipeline-output metrics).
- **NFR-CONV.5 no-new-dependencies audit** — `D-0085/evidence.md`
  confirms only Read/Grep/Glob/Bash tooling; every command in §3 above
  is exactly one of those four primitives plus `uv run pytest` (the
  standard runner already covered by the no-new-dep audit).

---

## 5. GA-tag instrumentation use

At T07.20 (MIG-007b) the quality-engineer sub-agent runs the §3
command list in one batch and confirms:

1. **MET-002 row** — both pytest commands exit 0 (100% detection).
2. **MET-003 row** — pytest exits 0 AND the Surface B grep returns
   coverage = 100% across the D-0083 §2.1 audit-window runs.
3. **MET-006 row** — D-0084 §4 reports "All 5 ratios ≤ 1.10: TRUE".
4. **MET-001 row** — D-0089 spec reports first-cycle PASS rate ≥80%
   (≥4 of 5).
5. **MET-004 + MET-005 fixture rows** — pytest exits 0 across the
   listed fixtures.
6. **MET-004 + MET-005 production-cadence rows** — runtime grep
   returns zero `synthetic-dnsp` source emissions and zero
   `[HALT-MONOTONICITY]` emissions in healthy `.dev/tasks/to-do/*/qa/`
   outputs, OR any non-zero values are recorded against the
   appropriate OPS runbook (OPS-002 / OPS-004 / OPS-005) with the
   SLA-bound owner notified.

If any of these six readings is missing or breaching threshold without
a corresponding OPS dispatch record, the GA-tag is withheld per the
T07.10 "withhold the v3.9 tag" routing (D-0091 §5).

---

## 6. Acceptance criteria — T07.19

| # | Criterion | Status | Evidence |
|---|---|---|---|
| 1 | File `TASKLIST_ROOT/artifacts/D-0098/spec.md` exists and lists all 6 MET-001..006 with thresholds. | PASS | This file, §3 (6 rows; threshold column populated for each). |
| 2 | MET-002 unresolved-token detection 100% on TB-Add-1 fixtures. | PASS | `uv run pytest tests/audit/test_nfr_conv_6_self_contained.py -q` → 10 passed (stripped fixture FAILs TB-Add-1 naming the missing field as required). See `evidence.md` §2.2. |
| 3 | MET-002 DAG-cycle detection 100% on TB-Add-4 fixtures. | PASS | `uv run pytest tests/audit/test_invariant_preservation_NFR_6_through_10.py -q` → 19 passed (composite invariant suite exercising TB-Add-4 / DAG-cycle via the cycle-detection routine at `test_nfr_conv_6_self_contained.py:199-229`). See `evidence.md` §2.2. |
| 4 | MET-006 token-cost ratio target ≤1.10 documented. | PASS | §3 row MET-006 binds the metric to D-0084 §4 ("All 5 ratios ≤ 1.10: TRUE"); §4 cross-reference list calls out the D-0084 binding by name. |
| 5 | Evidence at `TASKLIST_ROOT/artifacts/D-0098/evidence.md` including aggregation output. | PASS | Sibling `evidence.md` re-runs the §3 command list and tabulates the result row-by-row. |

**Verdict: PASS** — all 6 MET-* counters live via offline-grep / pytest
aggregation; each metric is cross-referenced to its OPS runbook
trigger; GA-tag committee can mechanically verify the governance
table at T07.20.

---

## 7. Notes on instrumentation discipline

- **No new dependencies.** Every command in §3 uses Read / Grep /
  Glob / Bash + `uv run pytest`, already accounted for in the
  T07.03 D-0085 NFR-CONV.5 audit.
- **No telemetry buses.** The "counter" semantics are achieved by
  re-running the listed commands on demand at release-window
  inspection time; there is no persistent metric store. This is
  intentional and matches `roadmap.md:441` "offline-grep-aggregate-
  per-release" language for MET-004.
- **Re-running is the refresh.** Treat the §3 commands as the single
  source of truth: if a recorded counter in a release report
  disagrees with the live re-run, trust the live re-run and update
  the recorded value (no caching layer to invalidate).
- **OPS dispatch is the only side-effect.** A threshold breach has
  exactly one consequence: opening the indicated OPS runbook with the
  SLA owner notified. No automated rollback fires from a metric
  reading alone; rollback decisions stay with the OPS runbook owner
  per the per-FR rollback envelope at `roadmap.md:472-479` /
  release-spec §19.4.
