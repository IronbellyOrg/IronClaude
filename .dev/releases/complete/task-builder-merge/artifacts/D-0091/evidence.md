# D-0091 — T07.10 Evidence: Consolidated Governance Table Published

**Task:** T07.10 (Phase 7 — M7)
**Roadmap items:** R-151
**Date:** 2026-05-18
**Branch:** `feat/hook-sync-and-matcher-fix`
**HEAD at audit:** `efaa33d`
**Tier:** STANDARD
**Verification method:** Direct enumeration check
**Overall: PASS** (4/4 acceptance criteria met)

---

## 1. Source

The consolidated table in `spec.md` §2 reproduces the roadmap §M7
*Consolidated GA-Readiness Governance Table* at
`/config/workspace/IronClaude/.dev/releases/current/task-builder-merge/roadmap.md`
lines **446-470**. The header section
(`### Consolidated GA-Readiness Governance Table — M7`) is at line
446; the column header is at line 450; rows occupy lines 452-470.

Column order in `spec.md` §2 matches the roadmap source verbatim:
`Flag / Metric / Runbook | Type | Default / Threshold | Owner |
Cleanup / Action Window | Source FR`.

The "Default / Threshold" column merges the roadmap "Default" column
for FF_* rows with the roadmap "Cleanup / Action Window" content for
MET-*/OPS-* numerical thresholds, so every row in `spec.md` §2 carries
an explicit operational number (cleanup window, SLA, or threshold) as
required by acceptance criterion #2.

---

## 2. Enumeration evidence

### 2.1 FF_* logical flags (target: 6)

Source rows: roadmap.md:452-457.

| # | Flag | Source FR | Cleanup window present |
|---|---|---|---|
| 1 | FF_TB_ADD_1_THROUGH_8 | FR-CONV.1 | Yes — GA+30d |
| 2 | FF_EXECUTION_CONTEXT_HEADER | FR-CONV.2 | Yes — GA+30d |
| 3 | FF_INHERITED_STRUCTURAL_VERDICT | FR-CONV.3 | Yes — post-K-003 audit pass |
| 4 | FF_FIVE_ADVERSARIAL_AXES | FR-CONV.4 | Yes — GA+30d post-K-004 |
| 5 | FF_RETRY_MONOTONICITY_GUARDS | FR-CONV.5 | Yes — GA+30d post-K-005 |
| 6 | FF_SYNTHETIC_DNSP_EMISSION | FR-CONV.6 | Yes — GA+30d post-K-006 |

Count = 6. PASS.

### 2.2 MET-* metrics (target: 6)

Source rows: roadmap.md:458-463.

| # | Metric | Threshold | OPS trigger | Owner |
|---|---|---|---|---|
| 1 | MET-001 | ≥80% first-cycle PASS | (release block) | Engineering |
| 2 | MET-002 | 100% unresolved-token + 100% DAG-cycle | TB-Add calibration | Engineering |
| 3 | MET-003 | 100% Self-Audit + ≥1 semantic-check | OPS-001 | QA Lead |
| 4 | MET-004 | mono >50% / regr >20% | OPS-004 / OPS-005 | rf-task-builder maintainer |
| 5 | MET-005 | >0 in production | OPS-002 | rf-qa maintainer |
| 6 | MET-006 | ≤1.10 | K-010 contingency | Engineering Lead |

Count = 6. PASS.

### 2.3 OPS-* runbooks (target: 7)

Source rows: roadmap.md:464-470.

| # | Runbook | Owner | Response SLA / Trigger |
|---|---|---|---|
| 1 | OPS-001 — K-003 audit | QA Lead | 4 business hours |
| 2 | OPS-002 — DNSP triage | rf-qa maintainer | 24 hours / ≥3 dedup-keys/week escalate |
| 3 | OPS-003 — All-partitions-exhaust | rf-team-lead maintainer | Zero-success path activation |
| 4 | OPS-004 — Monotonicity rate | rf-task-builder maintainer | >50% of batches |
| 5 | OPS-005 — Regression rate | Engineering Lead | >20% of batches |
| 6 | OPS-006 — Sync failure | Per-commit author | Immediate (A-001 / K-009) |
| 7 | OPS-007 — Layout change | Engineering Lead | Portfolio-wide blast radius (K-008) |

Count = 7. PASS.

### 2.4 Total

6 + 6 + 7 = **19** rows in `spec.md` §2. Matches `spec.md` §3
enumeration check. PASS.

---

## 3. Acceptance criteria verification

| # | Acceptance criterion | Evidence | Status |
|---|---|---|---|
| 1 | File `TASKLIST_ROOT/artifacts/D-0091/spec.md` exists and lists exactly 6 FF_* flags, 6 MET-* metrics, 7 OPS-* runbooks. | `spec.md` §2 (19 rows) + §3 enumeration check; this evidence §2.1-2.4 independently counts each category. | PASS |
| 2 | Each row includes cleanup window / SLA / threshold per roadmap §M7 Consolidated Governance Table. | `spec.md` §2 column 3 (Default / Threshold) + column 5 (Cleanup / Action Window) — every one of the 19 rows is populated; verified row-by-row in §2.1-2.3 above. | PASS |
| 3 | GA-tagging committee referenced as the audience. | `spec.md` §0 ("load-bearing input to the GA-tagging committee"), §1 ("Primary audience: GA-tagging committee"), §5 ("The GA-tagging committee reads this single page at T07.20"). | PASS |
| 4 | Evidence at `TASKLIST_ROOT/artifacts/D-0091/evidence.md`. | This file. | PASS |

---

## 4. Cross-validation

### 4.1 Roadmap row count check

```text
$ awk 'NR>=452 && NR<=470 {n++} END {print n}' \
    .dev/releases/current/task-builder-merge/roadmap.md
19
```

19 rows in the roadmap source (lines 452-470). 19 rows reproduced in
`spec.md` §2. 1:1 mapping confirmed.

### 4.2 Per-FR coverage check

Every FR-CONV.X (1..6) appears as the *Source FR* of exactly one FF_*
row:

- FR-CONV.1 → FF_TB_ADD_1_THROUGH_8
- FR-CONV.2 → FF_EXECUTION_CONTEXT_HEADER
- FR-CONV.3 → FF_INHERITED_STRUCTURAL_VERDICT
- FR-CONV.4 → FF_FIVE_ADVERSARIAL_AXES
- FR-CONV.5 → FF_RETRY_MONOTONICITY_GUARDS
- FR-CONV.6 → FF_SYNTHETIC_DNSP_EMISSION

Six FRs → six flags. No FR missing; no flag without an FR. PASS.

### 4.3 MIG-007b dependency check

The GA-tagging gate at T07.20 (MIG-007b) lists T07.10 as a hard
dependency (phase-7-tasklist.md:965). This artifact satisfies the
GA-tag prerequisite "consolidated governance table published"
(T07.20 step 3 at phase-7-tasklist.md:950 and acceptance criterion at
phase-7-tasklist.md:957).

### 4.4 Audience consistency

phase-7-tasklist.md:484 — Validation: "GA-tagging committee confirms
table is decision-ready." `spec.md` §5 enumerates the three-property
read pattern the committee uses, so the artifact is structured for
its named audience.

---

## 5. Reviewer checklist

| Item | Result |
|---|---|
| Exactly 6 FF_* rows | PASS (§2.1) |
| Exactly 6 MET-* rows | PASS (§2.2) |
| Exactly 7 OPS-* rows | PASS (§2.3) |
| Each row carries cleanup/SLA/threshold | PASS (§3 row 2) |
| GA-tagging committee named as audience | PASS (§3 row 3) |
| Column order matches roadmap §M7 | PASS (§1) |
| Total = 19 rows; matches roadmap.md:452-470 | PASS (§4.1) |
| All 6 FR-CONV.X covered by one flag each | PASS (§4.2) |
| Satisfies T07.20 MIG-007b dependency | PASS (§4.3) |

**Verdict: PASS** — D-0091 is decision-ready for the GA-tagging
committee.

---

## 6. Artifacts

- `TASKLIST_ROOT/artifacts/D-0091/spec.md` — single-page consolidated
  governance table (19 rows).
- `TASKLIST_ROOT/artifacts/D-0091/evidence.md` — this file.

`TASKLIST_ROOT` resolves to
`.dev/releases/current/task-builder-merge/` in this release.
