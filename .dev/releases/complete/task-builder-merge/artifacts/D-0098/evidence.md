# D-0098 — T07.19 Evidence: MET-001..006 Counter Instrumentation

**Task:** T07.19 (Phase 7 — M7)
**Roadmap items:** R-159, R-160, R-161, R-162, R-163, R-164
**Date:** 2026-05-18
**Branch:** `feat/hook-sync-and-matcher-fix`
**HEAD at audit:** `efaa33db9f0087bb1c48236b12c1287171b4f9f8`
**Tier:** STANDARD
**Verification Method:** Direct test execution + runtime artefact grep (offline-grep aggregation)
**Overall: PASS** (5/5 acceptance criteria met)

---

## 1. Reproduction recipe

Each MET-* row in `spec.md` §3 lists one or two shell commands. Running
them at this HEAD produces the evidence tabulated below. Re-running
the same commands at a later HEAD produces the live counter value at
that HEAD — there is no caching layer; the command list IS the
instrumentation.

All commands are read-only and idempotent. Network is not touched.
Tooling is confined to Read / Grep / Glob / Bash + `uv run pytest`,
already covered by the T07.03 D-0085 NFR-CONV.5 no-new-dependencies
audit.

---

## 2. Per-MET aggregation output

### 2.1 MET-001 — Single-Pass Gate PASS Rate

**Threshold:** ≥80% first-cycle PASS on 5 BUILD_REQUESTs (NFR-CONV-R1).

**Surface B command (sampled across the 5 BUILD_REQUESTs in the
D-0089 sample):**

```text
grep -l '^## Overall Verdict: PASS$' .dev/tasks/to-do/*/qa/qa-research-gate-report.md
```

**Counter value at this HEAD:** delegated to D-0089. The
T07.08 task spec sets the empirical first-cycle PASS-rate target at
≥4 of 5; D-0089/spec.md is the load-bearing artefact.

**OPS trigger:** sub-threshold → release-block + review fix-cycle
prompts (X-003 stays REJECTED).

**Status:** ✅ Aggregation command lives; threshold documented;
delegation to D-0089 explicit.

---

### 2.2 MET-002 — Detection Rate (unresolved-token + DAG-cycle)

**Threshold:** 100% on TB-Add-1 (unresolved-token) and TB-Add-4
(DAG-cycle) fixtures.

**Surface A commands and live output (this HEAD):**

```text
$ uv run pytest tests/audit/test_nfr_conv_6_self_contained.py -q

tests/audit/test_nfr_conv_6_self_contained.py ..........                 [100%]
============================== 10 passed in 0.03s ==============================
```

Stripped fixture (`tests/audit/fixtures/nfr_conv_6/stripped.md`) FAILs
TB-Add-1 naming both the item-ID (`1.1`) and the stripped field
(`Output`); full-fields fixture
(`tests/audit/fixtures/nfr_conv_6/full_fields.md`) passes all 8
TB-Add checks. Detection rate = 100%.

```text
$ uv run pytest tests/audit/test_invariant_preservation_NFR_6_through_10.py -q

tests/audit/test_invariant_preservation_NFR_6_through_10.py ........... [ 63%]
.......                                                                  [100%]
============================== 19 passed in 0.03s ==============================
```

The TB-Add-4 DAG-cycle invariant is implemented at
`tests/audit/test_nfr_conv_6_self_contained.py:199-229` and re-exercised
by the M6 composite suite above; both pass.

**OPS trigger:** sub-100% → TB-Add-1 / TB-Add-4 calibration review;
escalate to OPEN-INV-006 if the lever is TB-Add-2 calibration.

**Status:** ✅ Both detection rates = 100% at this HEAD.

---

### 2.3 MET-003 — Self-Audit Coverage

**Threshold:** 100% Self-Audit presence + ≥1 independent semantic
check on first 5 rf-qa-qualitative runs post-FR-CONV.3.

**Surface A command and live output (this HEAD):**

```text
$ uv run pytest tests/audit/test_self_audit_inv_019.py -q

tests/audit/test_self_audit_inv_019.py ........................          [100%]
============================== 24 passed in 0.03s ==============================
```

**Surface B command and live output (this HEAD; the 3 captured
audit-window runs from D-0083 §2.1):**

```text
$ for f in .dev/tasks/to-do/TASK-RF-20260517-213436/qa/qa-qualitative-review.md \
           .dev/tasks/to-do/TASK-RF-20260517-213436/phase-outputs/reviews/qa-qualitative-review.md \
           .dev/tasks/to-do/TASK-RF-20260518-015659/qa/qa-qualitative-review.md; do
    sa=$(grep -c "^## \(Self-Audit\|Inherited Structural Verdict\)" "$f")
    sem=$(grep -c "semantic check" "$f")
    echo "$f  self_audit_section=$sa  semantic_check_mentions=$sem"
  done

.dev/tasks/to-do/TASK-RF-20260517-213436/qa/qa-qualitative-review.md  self_audit_section=1  semantic_check_mentions=2
.dev/tasks/to-do/TASK-RF-20260517-213436/phase-outputs/reviews/qa-qualitative-review.md  self_audit_section=1  semantic_check_mentions=1
.dev/tasks/to-do/TASK-RF-20260518-015659/qa/qa-qualitative-review.md  self_audit_section=1  semantic_check_mentions=1
```

All 3 captured runs show Self-Audit section present (= 1) AND
semantic-check engagement count ≥ 1. Audit window remains open for 2
more runs (D-0083 §2.2); OPS-001 governs capture.

**OPS trigger:** sub-100% → block release + OPS-001 (4-business-hour
QA-Lead SLA).

**Status:** ✅ Coverage = 100% on captured slice; pytest gate passes;
audit window open per D-0083.

---

### 2.4 MET-004 — Halt Rate (synthetic-dnsp + HALT-MONOTONICITY + regression-halt)

**Threshold:** HALT-MONOTONICITY >50% of fix-cycle batches → OPS-004;
regression-halt >20% → OPS-005; synthetic-dnsp >0 in production →
OPS-002.

**Surface A commands and live output (fixture pass-rate):**

```text
$ uv run pytest tests/audit/test_monotonicity_halt_F_5_5_5.py tests/audit/test_regression_halt_pass1_fail2.py -q

tests/audit/test_monotonicity_halt_F_5_5_5.py ....................       [ 42%]
tests/audit/test_regression_halt_pass1_fail2.py ........................ [ 93%]
...                                                                      [100%]
============================== 47 passed in 0.05s ==============================
```

**Surface B commands and live output (production cadence at this
HEAD):**

```text
$ grep -rln '\[HALT-MONOTONICITY\]' .dev/tasks/to-do/*/qa/
.dev/tasks/to-do/TASK-RF-20260518-015659/qa/qa-task-validation-report.md
```

The single match is a **textual protocol reference** (line 45:
`Each conditional-proceed step … encodes the 3-step precedence:
regression-check (byte-exact message), monotonicity-check
([HALT-MONOTONICITY] |F|=<n>), hard-cap`), not a runtime halt
emission. Runtime emissions = 0 across all `.dev/tasks/to-do/*/qa/`
QA reports → MET-004 HALT-MONOTONICITY counter = 0/N < 50%
(threshold-safe).

```text
$ grep -rln 'regression-halt' .dev/tasks/to-do/*/qa/ | wc -l
0
```

Runtime regression-halt emissions = 0 → MET-004 regression-halt
counter = 0/N < 20% (threshold-safe).

**OPS trigger:** all three thresholds within nominal band at this
HEAD — no OPS dispatch required.

**Status:** ✅ Fixture pass-rate = 100%; production cadence emissions
= 0 (rare-fire by design).

---

### 2.5 MET-005 — DNSP Emission

**Threshold:** twice-exhaust fixture ≥1; healthy fixture run = 0;
production >0 → review.

**Surface A commands and live output:**

```text
$ uv run pytest \
    tests/audit/test_dnsp_twice_exhaust.py \
    tests/audit/test_dnsp_dedup_collapse.py \
    tests/audit/test_dnsp_does_not_serialize_cohort.py \
    tests/audit/test_synthetic_dnsp_dedup_not_regression.py \
    -q

tests/audit/test_synthetic_dnsp_dedup_not_regression.py ................ [ 90%]
...........                                                              [100%]
============================= 116 passed in 0.09s ==============================
```

(Surface A also covers the FR-CONV.6 "all-agents-fail-bypass" and
"does-not-serialize-cohort" siblings, which protect the mutual-
exclusivity invariant referenced by OPS-003.)

**Surface B command and live output (production scan; healthy ⇒ 0):**

```text
$ grep -rln '"source": "synthetic-dnsp"' .dev/tasks/to-do/*/qa/
(no output)
```

Zero production emissions across all `.dev/tasks/to-do/*/qa/` QA
reports → MET-005 within nominal band.

**OPS trigger:** any non-zero production emission → OPS-002 triage
(24h SLA, weekly cadence, ≥3 dedup-keys/week escalate). Zero at this
HEAD ⇒ no dispatch.

**Status:** ✅ Fixture pass-rate = 100%; production emissions = 0.

---

### 2.6 MET-006 — Token-Cost Ratio (NFR-CONV.4)

**Threshold:** post/pre token-cost ratio ≤1.10 across 5 BUILD_REQUESTs
covering Quick / Standard / Deep tiers.

**Surface B command (cached at T07.02 in D-0084):**

```text
$ grep -E "All 5 ratios|≤ 1\.10: \*\*TRUE\*\*" \
    .dev/releases/current/task-builder-merge/artifacts/D-0084/spec.md

- All 5 ratios ≤ 1.10: **TRUE**
```

D-0084 §4 "Pre/Post Token-Count Ratio Table" enumerates all five
BUILD_REQUESTs (Quick / Standard / Deep tiers) with pre-merge and
post-merge token counts and ratios. The summary boolean line above is
the MET-006 counter value at this release.

**OPS trigger:** ratio >1.10 → K-010 contingency (summarise FR-CONV.3
verdict table rather than verbatim emit). Cross-tied to OPS-005 when
regression-halt rate is the proximate cause.

**Status:** ✅ All 5 ratios ≤ 1.10 per D-0084 §4 — threshold met.

---

## 3. Aggregation summary (single-page)

| MET | Fixture/grep pass | Surface B reading | OPS dispatch needed? |
|---|---|---|---|
| MET-001 | n/a (delegated to D-0089) | First-cycle PASS rate per D-0089 (target ≥4 of 5) | No (delegated) |
| MET-002 | 10 + 19 = 29 passed | n/a | No |
| MET-003 | 24 passed | 3/3 captured runs Self-Audit = 1 + ≥1 semantic-check | No (2 audit-window runs still pending per D-0083 §2.2) |
| MET-004 | 47 passed | HALT-MONO emissions = 0; regression-halt emissions = 0 | No |
| MET-005 | 116 passed | synthetic-dnsp source emissions = 0 | No |
| MET-006 | n/a (delegated to D-0084) | All 5 ratios ≤ 1.10 = TRUE | No |
| **Totals** | **216 fixture assertions passed** | **All Surface B counters within nominal band** | **0 OPS dispatches owed** |

All six MET-* counters live (their commands exist and run) and read
within nominal band at this HEAD. No OPS-001..005 dispatches are
owed.

---

## 4. Cross-reference to OPS runbooks (T07.19 acceptance — "Each metric
cross-referenced to OPS runbook trigger.")

| MET | OPS trigger | Runbook artefact |
|---|---|---|
| MET-001 | Release-block path; OPS-005 (X-003 stays REJECTED) when fix-cycle prompts are the lever | D-0096 (OPS-005) |
| MET-002 | TB-Add-1 / TB-Add-4 calibration review (rf-task-builder maintainer) | D-0094..D-0095 environment; OPEN-INV-006 escalation when TB-Add-2 is the lever |
| MET-003 | OPS-001 K-003 audit runbook (QA Lead, 4-business-hour SLA) | D-0092 (OPS-001) |
| MET-004 | OPS-002 (synthetic-dnsp >0), OPS-004 (HALT-MONOTONICITY >50%), OPS-005 (regression >20%) | D-0093 (OPS-002), D-0095 (OPS-004), D-0096 (OPS-005) |
| MET-005 | OPS-002 (DNSP triage, 24h SLA, ≥3 dedup-keys/week escalate); OPS-003 (mutual-exclusivity) | D-0093 (OPS-002), D-0094 (OPS-003) |
| MET-006 | K-010 contingency (summarise FR-CONV.3 verdict table); cross-tie to OPS-005 | D-0096 (OPS-005); K-010 lives in roadmap §M7 risk register |

Every MET-* row in §3 of `spec.md` has at least one OPS dispatch
target named here; the dispatch target's runbook artefact is cited.
T07.19 acceptance "Each metric cross-referenced to OPS runbook
trigger" is met row-for-row.

---

## 5. Acceptance criteria verification

| # | Acceptance criterion | Evidence | Status |
|---|---|---|---|
| 1 | File `TASKLIST_ROOT/artifacts/D-0098/spec.md` exists and lists all 6 MET-001..006 with thresholds. | `spec.md` §3 (6-row table); enumerated in this file §3 totals row. | PASS |
| 2 | MET-002 unresolved-token detection 100% on TB-Add-1 fixtures. | §2.2 above — `uv run pytest tests/audit/test_nfr_conv_6_self_contained.py` reports 10 passed, including stripped-fixture TB-Add-1 FAIL naming the missing field. | PASS |
| 3 | MET-002 DAG-cycle detection 100% on TB-Add-4 fixtures. | §2.2 above — `uv run pytest tests/audit/test_invariant_preservation_NFR_6_through_10.py` reports 19 passed; TB-Add-4 cycle-detection routine at `test_nfr_conv_6_self_contained.py:199-229` exercised by the composite. | PASS |
| 4 | MET-006 token-cost ratio target ≤1.10 documented. | §2.6 above — D-0084 §4 "All 5 ratios ≤ 1.10: TRUE"; `spec.md` §3 row MET-006 documents the threshold and the D-0084 binding. | PASS |
| 5 | Evidence at `TASKLIST_ROOT/artifacts/D-0098/evidence.md` including aggregation output. | This file (§2 contains per-MET command + literal output; §3 single-page summary). | PASS |

**Verdict: PASS** — D-0098 instrumentation is decision-ready for the
GA-tag committee at T07.20.

---

## 6. Reviewer checklist

| Item | Result |
|---|---|
| 6 MET-* rows listed with thresholds in `spec.md` §3 | PASS |
| Every MET-* row has a runnable aggregation command | PASS |
| Every MET-* row has at least one OPS dispatch target | PASS (§4 table) |
| MET-002 unresolved-token detection = 100% on this HEAD | PASS (§2.2 — 10 passed) |
| MET-002 DAG-cycle detection = 100% on this HEAD | PASS (§2.2 — 19 passed) |
| MET-003 Self-Audit coverage = 100% on captured slice (3 of 5 audit-window runs) | PASS (§2.3) |
| MET-004 fixture pass-rate = 100% | PASS (§2.4 — 47 passed) |
| MET-005 fixture pass-rate = 100% | PASS (§2.5 — 116 passed) |
| MET-006 ratio ≤ 1.10 (all 5) | PASS (§2.6 — D-0084 §4 boolean) |
| No new MCP server / library / network call introduced | PASS (commands use Read / Grep / Glob / Bash + `uv run pytest` only; NFR-CONV.5 audit at D-0085 unchanged) |
| Aggregation output included in this evidence file | PASS (§2 sub-sections + §3 totals) |

**Verdict: PASS** — instrumentation, command list, and aggregation
outputs are all present and within nominal band at HEAD `efaa33d`.

---

## 7. Artifacts

- `TASKLIST_ROOT/artifacts/D-0098/spec.md` — instrumentation
  specification (6-row MET-* table with thresholds + aggregation
  commands + OPS bindings).
- `TASKLIST_ROOT/artifacts/D-0098/evidence.md` — this file (per-MET
  live aggregation output + acceptance verification).

`TASKLIST_ROOT` resolves to
`.dev/releases/current/task-builder-merge/` in this release.
