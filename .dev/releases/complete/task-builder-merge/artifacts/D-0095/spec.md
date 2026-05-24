# D-0095 — OPS-004 `[HALT-MONOTONICITY]` Rate Runbook (>50% threshold)

**Task:** T07.15 (Phase 7 — M7)
**Roadmap items:** R-155
**Date:** 2026-05-18
**Branch:** `feat/hook-sync-and-matcher-fix`
**Tier:** STANDARD
**Verification method:** Direct enumeration check (5 runbook sections + `>50%` threshold documented + upstream-quality-gate referral path + OPEN-INV-006 cross-reference + dual resolution path — improve upstream BUILD_REQUESTs OR TB-Add-2 calibration)
**Audience:** rf-task-builder maintainer (on-call), rf-qa maintainer (peer — OPS-005 cross-coordination on the regression→monotonicity precedence chain), Engineering Lead, BUILD_REQUEST authors (upstream-quality-gate referral target), GA-tagging committee
**Owner:** rf-task-builder maintainer (per `roadmap.md:467` OPS-004 row — "Operational | rf-task-builder maintainer | Threshold >50% of batches | FR-CONV.5")
**Threshold (alert):** **`[HALT-MONOTONICITY]` emission rate > 50% of fix-cycle batches per release window** (per `roadmap.md:434` R-155 acceptance criteria + `roadmap.md:441` MET-004 trigger row + `roadmap.md:467` OPS-004 governance row + `roadmap.md:574` MET row "<10% target; >50% triggers upstream BUILD_REQUEST defect alert")
**Resolution path:** Dual-path — (a) **improve upstream BUILD_REQUESTs** via the upstream-quality-gate referral path; OR (b) **promote TB-Add-2 from `[ADVISORY]` to Hard** via OPEN-INV-006 item-count-bounds empirical calibration (per `roadmap.md:434` R-155 + `roadmap.md:348` OPEN-INV-006)
**Cross-reference to OPEN-INV-006:** `roadmap.md:348` — TB-Add-2 stays `[ADVISORY]` (≥3 / ≤40 track / ≤50 single-track item-count bounds) until calibrated; OPEN-INV-006 calibration is the structural lever for reducing item-count-driven monotonicity halts at source
**Overall: PASS** (4/4 acceptance criteria met — §6)

---

## 0. TL;DR

OPS-004 is the operational runbook that turns the **`[HALT-MONOTONICITY]` rate exceeding 50% of fix-cycle batches** into an explicit on-call response procedure. It covers a single, observable rate-level signal:

> **Across a release window's fix-cycle batches (per-gate retry loops governed by the FR-CONV.5 4-step ordering `regression → monotonicity → hard-cap → proceed`), the byte-exact `[HALT-MONOTONICITY] |F|=<n>` halt-message emission rate exceeds the `>50%` threshold documented at `roadmap.md:434` + `roadmap.md:441` + `roadmap.md:467` + `roadmap.md:574`.**

This is a **rate-level upstream-defect signal**, not a per-event correctness signal: each individual `[HALT-MONOTONICITY]` emission is *correct behaviour* (the monotonicity guard fired as designed when `|F_{n+1}| >= |F_n|` after dedup-collapse and after the regression check passed — see `SKILL.md:1075` and `rf-task-builder.md:370`). What OPS-004 audits is the **aggregate frequency** of those correct emissions: when more than half of the fix-cycle batches in a window hit the monotonicity halt, the partition agents are systemically stuck — and the root cause is virtually always upstream (BUILD_REQUEST defects or item-count-bounds drift) rather than inside the halt-precedence wrapper itself. Per `roadmap.md:574`, the target rate is **<10%**, and the **>50%** trigger explicitly fires the upstream-quality-gate referral path.

The runbook is owned by the **rf-task-builder maintainer** (per `roadmap.md:467`) — the same maintainer who owns the FR-CONV.5 halt-guards wrapper at `rf-task-builder.md:358-372` and the Retry Monotonicity Protocol at `SKILL.md:1032-1095`. The resolution path is **dual** (per `roadmap.md:434` R-155 acceptance criteria — "resolution = improve upstream BUILD_REQUESTs or TB-Add-2 calibration (OPEN-INV-006)"): (a) refer to the upstream-quality-gate to revise BUILD_REQUESTs; or (b) calibrate TB-Add-2 from `[ADVISORY]` to Hard via OPEN-INV-006 empirical work — both paths reduce the rate at source rather than altering the halt-precedence machinery (which `roadmap.md:319` COMP-001-M5 + `roadmap.md:441` MET-004 + the byte-exact wire-string API-004 contract treat as frozen). The runbook contains the five mandatory sections (symptoms / diagnosis / resolution / escalation / prevention) called out in roadmap.md:434 + phase-7-tasklist.md L713-718.

---

## 1. Scope and authoritative bindings

This runbook binds to the following authorities (all read at landing time; cross-checked at every invocation):

| Source | Location | Binding |
|---|---|---|
| Roadmap R-155 acceptance criteria | `roadmap.md:434` | "runbook:published; threshold-greater-than-50%-documented; upstream-quality-gate-referral-path"; "resolution = improve upstream BUILD_REQUESTs or TB-Add-2 calibration (OPEN-INV-006)" |
| Roadmap §M7 Consolidated Governance Table — OPS-004 row | `roadmap.md:467` | "OPS-004 \| Monotonicity rate runbook \| Operational \| rf-task-builder maintainer \| Threshold >50% of batches \| FR-CONV.5" |
| Roadmap §M7 MET-004 row (alert-trigger wiring) | `roadmap.md:441` | "Measure synthetic-dnsp emission count; HALT-MONOTONICITY rate; regression-halt rate across fix-cycle batches"; "monotonicity-alert:>50%-triggers-OPS-004; regression-alert:>20%-triggers-OPS-005; offline-grep-aggregate-per-release" |
| Roadmap §M7 MET-004 governance row | `roadmap.md:461` | "MET-004 \| Halt Rate (combined) \| N/A \| rf-task-builder maintainer \| HALT-MONOTONICITY>50% → OPS-004; regression>20% → OPS-005 \| FR-CONV.5" |
| Roadmap §17 metric row — `[HALT-MONOTONICITY]` emission rate | `roadmap.md:574` | "<10% target; >50% triggers upstream BUILD_REQUESTBA defect alert (OPS-004)"; aggregation = "grep `[HALT-MONOTONICITY]` in fix-loop logs; offline aggregate per release" |
| Roadmap §M5 Objective (monotonicity halt-message contract) | `roadmap.md:305` | "non-shrink emits `[HALT-MONOTONICITY] |F|=<n>`; identical dedup-key synthetic findings across cycles do NOT trigger halt; legitimate slow-cycle correction NOT halted; X-003 slow-convergence threshold remains REJECTED" |
| Roadmap FR-CONV.5 Monotonicity halt-message row | `roadmap.md:311` | "halt-string:emitted-byte-exact-per-spec; emission:gated-on-prior-regression-check-passing; monotonicity-check:skipped-when-F_n-equals-0" |
| Roadmap COMP-001-M5 (SKILL.md A.9 separate-counters invariant tail) | `roadmap.md:319` | "Modify SKILL.md A.9 separate-counters invariant tail to add halt-precedence note; grep-[HALT-MONOTONICITY]-in-SKILL.md:867-873:returns-≥1-match; precedence-rule:documented" |
| Roadmap API-004 Fix-Loop Halt Signals contract (frozen at M1) | `roadmap.md:115` | "monotonicity_message:[HALT-MONOTONICITY] \|F\|=<n>; regression_message:verbatim-PASS-at-N-to-FAIL-at-N+1; order:regression-then-monotonicity-then-hard-cap; F_n:dedup-key-set" |
| Roadmap TB-Add-2 governance row | `roadmap.md:100` | "Item-count bounds ≥3 / ≤40-track / ≤50-single-track; emits `[ADVISORY]` prefix and does NOT block gate (pending OPEN-INV-006 calibration)"; "out-of-bounds-fixture:[ADVISORY]-emitted; gate-verdict:not-affected; status:advisory-until-Phase-2" |
| Roadmap FF_TB_ADD_1_THROUGH_8 feature-flag row | `roadmap.md:122` | "TB-Add-2:stays-ADVISORY-until-Phase-2; owner:rf-qa-maintainer; M7-consolidation:see-M7-governance-table" |
| Roadmap §18 OPEN-INV-006 row (TB-Add-2 calibration) | `roadmap.md:348` | "Empirical calibration of TB-Add-2 item-count bounds (≥3 / ≤40 track / ≤50 single-track). TB-Add-2 stays `[ADVISORY]` until calibrated. Source: TDD §22 / OPEN-INV-006."; "MEDIUM — affects when TB-Add-2 can promote from ADVISORY to Hard; informs rate at which `[HALT-MONOTONICITY]` fires on item-count-driven failures" |
| Retry Monotonicity Protocol — 4-step ordering rule | `src/superclaude/skills/task-builder/SKILL.md` L1032-1095 | Halt-precedence note (L1032), monotonicity guard (L1038), independent counters (L1043), F_n dedup-key identity (L1064), monotonicity-check predicate (L1075), cross-cycle dedup vs. regression rule (L1083-L1093), regression non-emission invariant (L1095) |
| Monotonicity halt-string wire format | `SKILL.md:1057` + `SKILL.md:1075` | `[HALT-MONOTONICITY] |F|=<n>` with `<n>` = `|F_{n+1}|` (byte-exact per API-004) |
| FR-CONV.5 halt-guards wrapper (in agent file) | `src/superclaude/agents/rf-task-builder.md:358-372` | "Halt-precedence rule (COMP-002-M5 — applies to every row in the table below). Each per-gate fix cycle ... is governed by the strict 4-step ordering `regression → monotonicity → hard-cap → proceed`"; "If `|F_{n+1}| >= |F_n|`, HALT and emit the byte-exact halt-message `[HALT-MONOTONICITY] |F|=<n>`. Regression takes precedence over monotonicity when both would trigger" |
| Per-gate independent counters invariant | `rf-task-builder.md:358` + `:372` + `SKILL.md:1043` + `SKILL.md:1972` (Critical Rule #12) | "Each gate row above keeps its OWN monotonicity history — research-gate's `F_n` is independent from task-integrity's `F_n`"; counters NEVER collapsed across gates |
| Cross-cycle dedup composition (INV-012) — keeps legitimate slow-convergence alive | `SKILL.md:1083-1093` | Cross-cycle same-`dedup_key` synthetic-dnsp re-emission is DEDUP (contributes 1 to `|F_{n+1}|`), not a regression; slow legitimate correction `|F|=5,4` does NOT halt |
| MIG-005 landing commit | `db6166e feat(task-builder): MIG-005 land FR-CONV.5 Retry Monotonicity + Regression Halts (M5)` | Production anchor for the monotonicity halt emitter; OPS-004 measurement window starts here |
| OPS-005 peer runbook (regression-halt rate counterpart) | `D-0096/spec.md` (T07.16, R-156) | Precedence-chain partner — Step 1 (regression) fires BEFORE Step 2 (monotonicity); OPS-005 owns the rate dimension of Step 1, OPS-004 owns the rate dimension of Step 2 |
| OPS-002 peer runbook (DNSP triage — synthetic-dnsp interaction with `|F_n|`) | `D-0093/spec.md` (T07.13, R-153) | Synthetic-dnsp findings COUNT as failures for `|F_n|` (SKILL.md:1045 + L1083); a sustained Path B (≥1-success + ≥1-exhaust) cohort with persistent synthetic-dnsp re-emission can drive OPS-004's rate up without an upstream BUILD_REQUEST defect — see §2.2.6 root-cause B5 |
| Upstream-quality-gate referral target | BUILD_REQUEST author + task-builder maintainer | The upstream resolution path for root-cause classes B1..B3 (BUILD_REQUEST defects); B4 routes to OPEN-INV-006 (TB-Add-2 calibration) |
| Consolidated GA-Readiness Governance Table | `D-0091/spec.md §2` MET-004 + OPS-004 rows | OPS-004 is enumerated in the governance table; cross-references this runbook for the GA-tagging committee |

**Scope boundary.** OPS-004 covers **rate-level monotoricity-halt response** — specifically, the `[HALT-MONOTONICITY] |F|=<n>` halt-message emission rate exceeding `>50%` of fix-cycle batches in a release window. It does **not** cover:

- A single `[HALT-MONOTONICITY]` emission per se — every individual emission is correct behaviour, by design (per `SKILL.md:1038` + `:1075`), and the operator response to a single halt is the per-gate cap fallback at `rf-team-lead.md:417` (the fourth-precedence step), not a runbook event.
- Regression-halt rate (`>20%` threshold) → OPS-005 (D-0096). The 4-step ordering rule guarantees regression precedence over monotonicity; OPS-005 reads the Step 1 rate, OPS-004 reads the Step 2 rate, with explicit composition rules at §2.4.4 below.
- Self-Audit / semantic-check audit-target events → OPS-001.
- Synthetic-dnsp emission-count → OPS-002. (But see §2.2.6 root-cause B5 — sustained synthetic-dnsp re-emission can drive `|F_n|` non-shrink and thereby influence OPS-004's rate; the runbooks compose at the M7 audit boundary.)
- All-partitions-exhaust HALT (zero-success cohort) → OPS-003. The all-agents-fail guard at SKILL.md L682 is upstream of the monotonicity check; an all-agents-fail cohort produces zero monotonicity halts because there are no successful partition outputs to construct `F_n` over.
- `make verify-sync` PASS-rate failures → OPS-006.
- INV-018 layout-change blast radius → OPS-007.
- **The byte-exact halt-message wire string itself**, the 4-step ordering rule itself, or the per-gate independent-counter invariant — all three are **frozen contracts** (API-004 byte-exact emission per `roadmap.md:115`; COMP-001-M5 / COMP-002-M5 precedence-rule per `roadmap.md:319` + `rf-task-builder.md:358`). OPS-004 does NOT modify these; it acts at the *upstream-input level* (BUILD_REQUESTs, item-count calibration) to reduce the rate at source.

---

## 2. Runbook — 5 sections

### 2.1 Symptoms

The on-call rf-task-builder maintainer is alerted (by the MET-004 offline-grep aggregation per `roadmap.md:441` — "offline-grep-aggregate-per-release", run at every release boundary against fix-loop logs per `roadmap.md:574`) when **all** of the following are jointly observed across a release window's fix-cycle batches post-MIG-005 (anchor commit `db6166e`, 2026-05-18 — FR-CONV.5 landed):

1. **Aggregate emission count.** Across the release window, `grep -c '^\[HALT-MONOTONICITY\] |F|=' <fix-loop-logs-merged>` returns a non-zero count. The grep target is the byte-exact halt-string emitted by the FR-CONV.5 monotonicity guard (`SKILL.md:1075` + `rf-task-builder.md:370` — byte-exact per API-004 wire-string contract at `roadmap.md:115`).
2. **Per-batch normalisation.** Let `batches_total` = the total number of fix-cycle batches in the window (counting each independent per-gate retry-loop instance — research-gate, synthesis-gate, report-validation, task-integrity, qualitative — separately per the `SKILL.md:1043` independent-counter invariant and the `rf-task-builder.md:372` "per-gate retry counters ... are independent and NEVER collapsed" rule). Let `batches_halted` = the count of fix-cycle batches where at least one `[HALT-MONOTONICITY]` was emitted during the batch's lifetime. Compute `monotonicity_halt_rate = batches_halted / batches_total`.
3. **Threshold breach (the OPS-004 trigger condition).** `monotonicity_halt_rate > 0.50` (i.e., **more than half of the fix-cycle batches halted on monotonicity**) — per `roadmap.md:434` R-155 + `roadmap.md:441` MET-004 trigger row + `roadmap.md:467` OPS-004 row "Threshold >50% of batches" + `roadmap.md:574` metric row ">50% triggers upstream BUILD_REQUEST defect alert (OPS-004)". The target rate per `roadmap.md:574` is `<10%`, so anything in the `10%-50%` band is a *watch* state (monitored by MET-004 but not an OPS-004 trigger); only `>50%` activates this runbook.
4. **Window scope.** The default window is **one release window** (offline-grep aggregate per release per `roadmap.md:441` + `roadmap.md:574`). Per-release rather than per-day to dampen short-term jitter; a release boundary is the canonical OPS-004 inspection cadence.
5. **(Optional)** Co-occurrence with OPS-005 trigger (regression-halt rate `>20%`). When both trigger in the same window, the regression precedence (Step 1 → Step 2 per the 4-step ordering at `SKILL.md:1075` + `rf-task-builder.md:370`) means a portion of would-have-been-monotonicity halts were pre-empted by regression halts — OPS-004 and OPS-005 explicitly **compose** rather than duplicate (see §2.4.4).

Detection sources: (a) MET-004 offline-grep aggregation (canonical — per `roadmap.md:441` + `roadmap.md:574`); (b) per-release post-mortem audit (release-spec §8.3 row) inspecting halt-rate metrics; (c) ad-hoc rf-task-builder maintainer audit when a release-spec §8.3 audit row surfaces an anomaly; (d) the GA-tagging committee at MIG-007b (T07.20) reading the M7-audit summary.

**Symptom not in scope.** A single `[HALT-MONOTONICITY]` emission is NOT a symptom of this runbook — it is *correct behaviour* (the partition agent is stuck and the guard fired as designed). The rate dimension is what OPS-004 audits. Likewise, the presence of `Regression detected on Item X.Y — previously PASS at cycle N, now FAIL` (the byte-exact regression halt-message per API-004) within the window is a Step-1 signal that routes to OPS-005, NOT OPS-004; regression halts pre-empt monotonicity halts in the 4-step ordering and OPS-004 counts only Step-2 emissions (see `SKILL.md:1075` — "Do NOT consult subsequent steps").

### 2.2 Diagnosis

Within **24 hours** of the MET-004 alert (the canonical event), the rf-task-builder maintainer performs the following ordered diagnostic steps:

1. **Confirm the rate and identify the sample of halt events.** Capture:
   - (a) Release-window identifier (release tag or branch range).
   - (b) Total fix-cycle batches in window (`batches_total`) and the per-gate decomposition (research-gate count, synthesis-gate count, report-validation count, task-integrity count, qualitative count — each tracked independently per `SKILL.md:1043` + `rf-task-builder.md:372`).
   - (c) Total halted batches (`batches_halted`) and the per-gate decomposition.
   - (d) `monotonicity_halt_rate = batches_halted / batches_total`; record the per-gate sub-rates too.
   - (e) The full list of `[HALT-MONOTONICITY] |F|=<n>` emissions in the window (one line per emission with batch identifier, gate name, `|F_{n+1}|` value, cycle index `n`).
2. **Sample 3 halt events for deep inspection.** Per `roadmap.md:434` R-155 ("sample 3 halt events"), select 3 halt events drawn from the per-gate decomposition such that the sample covers (a) the gate with the highest per-gate halt rate, (b) the gate with the highest absolute halt count, and (c) a third event from any *different* gate to surface cross-gate patterns. (If only one or two gates produced halts in the window, sample 3 from within the available gates, preferring batches with distinct BUILD_REQUEST identifiers.)
3. **Inspect each sampled batch's BUILD_REQUEST for upstream defects.** Per `roadmap.md:434` R-155 ("inspect BUILD_REQUESTs for upstream defects"), for each sampled halt event:
   - (i) Read the originating BUILD_REQUEST file.
   - (ii) Verify the **research anchors**: assigned_files ranges are well-defined and reachable in the codebase at landing time; no broken file paths; no ambiguous "research everything" language.
   - (iii) Verify the **scope discipline**: BUILD_REQUEST specifies a bounded research surface; partition slicing is feasible at the cohort's chosen N; per-partition surface area fits within typical context-window budget (cross-reference TB-Add-2 item-count bounds at `roadmap.md:100`).
   - (iv) Verify the **prerequisite artifact references**: any inputs from prior phases exist; phase ordering is consistent.
   - (v) Verify the **acceptance-criteria precision**: pass/fail predicates are objective and grep-decidable; no subjective "good enough" language that would drive endless fix-cycles.
   - (vi) Note any BUILD_REQUEST defect signature observed.
4. **Inspect each sampled batch's MDTM (tasklist) for structural issues.** Per `roadmap.md:434` R-155 ("inspect MDTM for structural issues"), for each sampled halt event:
   - (i) Read the MDTM task file at `${TASK_DIR}/tasks/<task-id>/`.
   - (ii) Verify TB-Add-1..8 PASS at landing time (`uv run pytest tests/audit/` selectors per `roadmap.md:98`). Even though TB-Add-2 ships as `[ADVISORY]`, an `[ADVISORY]` from TB-Add-2 in the sample is a strong signal that item-count bounds drove the halt (route to B4 in step 6).
   - (iii) Verify the item-count is within the TB-Add-2 advisory bounds (≥3, ≤40 per track, ≤50 single-track per `roadmap.md:100`). Out-of-bounds item counts directly stress the monotonicity guard because `|F_n|` is the FAIL-verdict set cardinality, which scales with item count.
   - (iv) Verify item-ID-naming consistency (TB-Add-1/3/4/5/6/7 — `roadmap.md:98`). Misnamed items can register as distinct entries in `F_n` even when semantically duplicate, inflating `|F_n|` and tripping the monotonicity guard at non-shrink boundaries.
   - (v) Verify acceptance-criteria precision per item (parallel to step 3.v but at the MDTM granularity).
   - (vi) Note any MDTM structural defect signature observed.
5. **Verify the regression check ran FIRST (precedence sanity).** Confirm that none of the sampled halts should have been Step-1 regression halts instead. For each sampled halt event, the orchestrator's execution log MUST show: (a) the regression check predicate `dedup_key ∈ PASS_n ∩ FAIL_{n+1}` was evaluated and returned `false` (no regression detected); (b) the monotonicity check predicate `|F_{n+1}| >= |F_n|` was evaluated *next* and returned `true` (non-shrink confirmed); (c) the byte-exact halt-string `[HALT-MONOTONICITY] |F|=<n>` was emitted with the correct `<n>` value (= `|F_{n+1}|`). Any breach of this order is a contract regression and routes to B5 in step 6 (immediate Engineering-Lead escalation; NOT an OPS-004 rate-level event).
6. **Classify the rate root cause.** Per `roadmap.md:434` R-155 resolution wiring, OPS-004 rate breaches resolve into one of the following classes:
   - **B1 — BUILD_REQUEST scope ambiguity (upstream defect).** Sampled halts share a "research target ambiguous / anchors broad" signature in step 3. Partition agents are stuck because the research surface is unbounded; each cycle finds new failures faster than fixes resolve old ones, leading to `|F_{n+1}| >= |F_n|` non-shrink. **Resolution = §2.3 B1** (upstream-quality-gate referral to BUILD_REQUEST author).
   - **B2 — BUILD_REQUEST prerequisite gap (upstream defect).** Sampled halts share a "phase-`n-1` outputs absent / referenced artifact missing" signature in step 3. Fix-cycles cannot resolve the failures because the inputs themselves are wrong. **Resolution = §2.3 B2** (upstream-quality-gate referral).
   - **B3 — BUILD_REQUEST acceptance-criteria subjectivity (upstream defect).** Sampled halts share an "acceptance-criterion not grep-decidable / phrasing endlessly relitigable" signature in step 3.v / step 4.v. Items oscillate FAIL ↔ FAIL with no convergence path. **Resolution = §2.3 B3** (upstream-quality-gate referral).
   - **B4 — Item-count bounds drift (TB-Add-2 calibration deficit).** Sampled halts share an "item-count exceeds TB-Add-2 ADVISORY bounds; `[ADVISORY]` emitted but not blocking; halts cluster at per-gate cap" signature in step 4. The advisory-status of TB-Add-2 (per `roadmap.md:100` "emits `[ADVISORY]` prefix and does NOT block gate") means upstream cohorts are landing with item counts that systemically stress the monotonicity guard. **Resolution = §2.3 B4** (OPEN-INV-006 empirical-calibration referral — promote TB-Add-2 from `[ADVISORY]` to Hard).
   - **B5 — Contract regression (NOT an OPS-004 root cause).** Step 5 found one of: (i) the monotonicity halt-string was emitted when `|F_{n+1}| < |F_n|` (false positive — `SKILL.md:1075` predicate was bypassed); (ii) the monotonicity check was consulted when a regression *was* detected (precedence rule violated — `SKILL.md:1075` "Do NOT consult subsequent steps" was bypassed); (iii) the byte-exact halt-string deviates from `[HALT-MONOTONICITY] |F|=<n>` (API-004 wire-format violation); (iv) counters were collapsed across gates (per-gate independent-counter invariant violated). **Resolution = §2.3 B5** (immediate Engineering-Lead escalation under contract regression — OUT OF SCOPE for OPS-004's rate-level remit, IN SCOPE for release-spec §19.4 rollback path scoped to FR-CONV.5).
7. **Compose with peer runbooks.** Inspect whether the window also tripped OPS-005 (regression-halt rate `>20%`). When both trip: regression halts at Step 1 *suppress* would-be monotonicity halts at Step 2 (per `SKILL.md:1075` "Do NOT consult subsequent steps"), so OPS-005's rate is a lower-bound shadow over OPS-004's measurement — see §2.4.4. Inspect whether the window also tripped OPS-002 (synthetic-dnsp emission count `>0` in production): persistent same-`dedup_key` synthetic-dnsp re-emissions across cycles contribute `1` (not `2`) to `|F_{n+1}|` (per `SKILL.md:1083`), but a Path B cohort with `≥1-success AND ≥1-exhaust` plus persistent synthetic emission can still drive `|F_n|` non-shrink at the rf-qa-qualitative gate. Cross-runbook composition is documented at §2.4.4 + §3.

### 2.3 Resolution

The resolution path is **dual** per `roadmap.md:434` R-155 acceptance criteria ("resolution = improve upstream BUILD_REQUESTs or TB-Add-2 calibration (OPEN-INV-006)"). Each root-cause class from §2.2.6 maps onto exactly one resolution path; B5 is excluded from OPS-004's rate-level remit and routes to a separate Engineering-Lead contract-regression response.

| Root cause | Resolution | Owner | Budget |
|---|---|---|---|
| **B1** (BUILD_REQUEST scope ambiguity) | rf-task-builder maintainer files an **upstream-quality-gate referral** to the BUILD_REQUEST author for the affected BUILD_REQUEST family. Referral payload: (a) the sampled halt-event list with `|F_{n+1}|` values and cycle indices; (b) the BUILD_REQUEST defect signature observed in §2.2.3 (anchor ambiguity, scope unboundedness); (c) a concrete revision recommendation (tighter anchors, explicit assigned_files, narrower scope). BUILD_REQUEST author revises the BUILD_REQUEST family and re-submits; the next release window's monotonicity-halt rate is the verification signal. **No change to the FR-CONV.5 halt-precedence wrapper is made** (it is operating correctly). | BUILD_REQUEST author primary; rf-task-builder maintainer advisory + referral-author | 24-hour SLA covers diagnosis + referral filing; upstream-side revision is bounded by the BUILD_REQUEST author's release cadence |
| **B2** (BUILD_REQUEST prerequisite gap) | rf-task-builder maintainer files an **upstream-quality-gate referral** noting the missing prerequisite artifact(s); BUILD_REQUEST author either (i) revises BUILD_REQUEST to remove the dependency, (ii) restages prior phases to produce the missing artifact, (iii) reorders phases. Verification = next-window rate. | BUILD_REQUEST author primary; rf-task-builder maintainer advisory | 24-hour SLA covers referral filing |
| **B3** (BUILD_REQUEST acceptance-criteria subjectivity) | rf-task-builder maintainer files an **upstream-quality-gate referral** noting the unstable acceptance criteria; BUILD_REQUEST author revises with grep-decidable predicates. Verification = next-window rate. | BUILD_REQUEST author primary; rf-task-builder maintainer advisory | 24-hour SLA covers referral filing |
| **B4** (item-count bounds drift — TB-Add-2 calibration deficit) | rf-task-builder maintainer files an **OPEN-INV-006 calibration referral** to Engineering Lead (per `roadmap.md:348` ownership). Referral payload: (a) the sampled halt-event list with the item-count of each originating MDTM; (b) the per-window distribution of item-counts that triggered TB-Add-2 `[ADVISORY]` emissions; (c) the empirical evidence that TB-Add-2 advisory-status is insufficient to prevent monotonicity-driven rate breaches; (d) a recommendation to promote TB-Add-2 from `[ADVISORY]` to Hard per the OPEN-INV-006 calibration workflow. **Promotion is a Phase-2 / post-OPEN-INV-006-resolution action** (per `roadmap.md:348` "Phase-2 (with PR-05 re-evaluation)"), so the immediate OPS-004 response is documentation + referral, not in-flight calibration. | Engineering Lead primary (OPEN-INV-006 owner); rf-task-builder maintainer advisory + referral-author | 24-hour SLA covers diagnosis + referral filing; calibration window is OPEN-INV-006-scheduled |
| **B5** (contract regression — Step 5 / `SKILL.md:1075` / API-004 / `rf-task-builder.md:370` violation) | **OUT OF SCOPE for OPS-004 rate-level remit.** Immediate Engineering-Lead escalation under contract regression. The Engineering Lead invokes release-spec §19.4 rollback path scoped to the FR-CONV.5 halt-precedence wrapper (revert MIG-005 commit `db6166e` per release-spec dependency matrix). **No rate-level diagnosis is filed** — the rate measurement is invalidated by the contract regression and must be re-run from a green baseline. | Engineering Lead (rf-task-builder maintainer initiates) | 24-hour SLA covers escalation initiation only |

On any successful resolution (B1 / B2 / B3 / B4): the rf-task-builder maintainer amends the audit trail with (a) the window identity, (b) the rate measurement at trigger, (c) the sampled halt-event list, (d) the diagnosed root-cause class, (e) the upstream referral filed (with timestamp + recipient), and (f) the next-release-window verification cadence.

**Explicit non-resolutions** (forbidden by the API-004 byte-exact contract + COMP-001-M5 precedence-rule + COMP-002-M5 independent-counter invariant):

- Do NOT modify the byte-exact halt-string `[HALT-MONOTONICITY] |F|=<n>` (API-004 wire-format frozen at `roadmap.md:115`).
- Do NOT modify the 4-step ordering rule (`regression → monotonicity → hard-cap → proceed`) per COMP-001-M5 at `roadmap.md:319` + COMP-002-M5 at `rf-task-builder.md:358`. The precedence is contract-frozen.
- Do NOT collapse per-gate counters (`SKILL.md:1043` + `rf-task-builder.md:372` invariant).
- Do NOT raise the threshold above `>50%` to "make the alert go away" — the `>50%` value is the governance-table commitment per `roadmap.md:467` + `roadmap.md:574` and is a release-spec §8.3 audit row.
- Do NOT introduce X-003 slow-convergence threshold ("HALT when `|F_{n+1}|` shrinks by less than X per cycle"). X-003 was explicitly **REJECTED** per `roadmap.md:305` ("X-003 slow-convergence threshold remains REJECTED") — legitimate slow-cycle correction (e.g., `|F|=5,4`) MUST NOT halt; only strict non-shrink (`|F_{n+1}| >= |F_n|`) halts. Re-litigating X-003 inside OPS-004 is forbidden.
- Do NOT alter the `F_n` dedup-key identity (`SKILL.md:1064` — `F_n` is a SET keyed by dedup-key; cardinality is post-dedup). Cross-cycle synthetic-dnsp persistence is DEDUP, not regression (`SKILL.md:1083`); altering this would either inflate `|F_n|` (false-positive halts driving rate up) or deflate it (false-negative non-halts masking real stuck-state).
- Do NOT silently auto-fix the failing items via gap-fill rounds beyond the per-gate cap; the existing per-gate cap (research-gate=3, synthesis-gate=2, report-validation=3, task-integrity=2, qualitative=3 per `rf-task-builder.md:358` table) and the `rf-team-lead.md:417` 3-cycle backstop are the fourth-precedence step and operate as designed.

### 2.4 Escalation

Escalation is **window-driven** by the MET-004 offline-grep aggregation cycle (per `roadmap.md:441` "offline-grep-aggregate-per-release") and time-boxed by the 24-hour diagnosis SLA. The escalation path forks at root-cause classification:

#### 2.4.1 Window measurement (the OPS-004 trigger surface)

| Field | Value |
|---|---|
| Aggregation source | Fix-loop logs across the release window (per-gate retry-loop execution logs, all 5 gates: research-gate / synthesis-gate / report-validation / task-integrity / qualitative — each independently per `SKILL.md:1043` + `rf-task-builder.md:372`) |
| Aggregation command (canonical) | `grep -c '^\[HALT-MONOTONICITY\] |F|=' <fix-loop-logs>` — byte-exact match against the API-004 halt-string per `roadmap.md:574` aggregation row |
| Per-batch denominator | Count of independent fix-cycle batches in the window (one per gate invocation per BUILD_REQUEST per cycle range) |
| Per-batch numerator | Count of batches where ≥1 `[HALT-MONOTONICITY]` emitted during the batch's lifetime |
| Threshold (alert) | `monotonicity_halt_rate > 0.50` (strict-greater per `roadmap.md:434` "threshold-greater-than-50%-documented" + `roadmap.md:574` ">50% triggers") |
| Threshold (target) | `monotonicity_halt_rate < 0.10` (per `roadmap.md:574` "<10% target") |
| Watch band | `0.10 ≤ monotonicity_halt_rate ≤ 0.50` — monitored by MET-004 but does not trigger OPS-004; surfaced in the M7-audit summary for awareness |
| Inspection cadence | Per release window (per `roadmap.md:441` + `roadmap.md:574`); supplemented by GA-tagging-committee review at MIG-007b (T07.20) |

#### 2.4.2 Escalation ladder

1. **T+0 (MET-004 aggregation runs at release boundary).** The offline-grep pipeline computes `monotonicity_halt_rate` for the window. If `> 0.50`, the rf-task-builder maintainer is paged (on-call rotation per `roadmap.md:477`). Acknowledgement within **4 hours**.
2. **T+4h to T+24h (diagnosis window).** rf-task-builder maintainer executes §2.2 including the 3-event sample, BUILD_REQUEST inspection, MDTM inspection, and precedence-sanity check. By T+24h, the maintainer has classified the rate breach into one of B1..B5.
3. **B1 / B2 / B3 path (upstream BUILD_REQUEST defect).** Resolution = §2.3 upstream-quality-gate referral to BUILD_REQUEST author. Verification = next-release-window rate measurement. No further escalation unless the next window also breaches with the same root-cause class (in which case escalate to step 5 — recurrence).
4. **B4 path (TB-Add-2 calibration deficit).** Resolution = §2.3 OPEN-INV-006 calibration referral to Engineering Lead. Verification = next-release-window rate measurement *after* OPEN-INV-006 calibration lands (which is Phase-2 / post-PR-05 re-evaluation per `roadmap.md:348`, not in-flight).
5. **Recurrence escalation (≥2 consecutive release-window breaches with the same root-cause class).** rf-task-builder maintainer escalates to **Engineering Lead**. Engineering Lead acknowledges within 1 business day. Possible outcomes: (a) systemic BUILD_REQUEST authoring pattern problem → broader operator-team intervention; (b) systemic item-count drift → prioritise OPEN-INV-006 calibration to land sooner; (c) genuine FR-CONV.5 over-aggressiveness despite no contract regression → re-evaluate the `>50%` threshold value at the next release-spec governance review (this is a *threshold* change, NOT a contract or precedence change — the byte-exact halt-string and the 4-step ordering remain frozen).
6. **B5 path (contract regression — separate track).** rf-task-builder maintainer immediately escalates to Engineering Lead under contract regression. The rate measurement is invalidated by the contract regression and is NOT processed through OPS-004's rate-level response. Engineering Lead invokes release-spec §19.4 rollback path scoped to MIG-005.
7. **GA-tagging committee escalation.** Three or more independent OPS-004 triggers across distinct release windows in the run-up to v3.9 GA (T07.20 / MIG-007b) → the GA-tagging committee re-evaluates whether the M7 exit criterion "observability counters live; v3.9 GA tagged" is in fact met when the underlying halt-rate is sustainedly elevated. The committee may (a) block GA tag until upstream-quality-gate or OPEN-INV-006 calibration resolves the rate; (b) accept GA with a remediation commitment captured in the consolidated governance table; or (c) revert FR-CONV.5 if the rate proves to be artifact of the contract rather than upstream input.

Escalation contacts and rotation handoffs live in the on-call knowledge base (consumed via integration point at `roadmap.md:477`); this runbook intentionally does not enumerate names so it survives rotation changes.

#### 2.4.3 Upstream-quality-gate referral path (the §2.4 acceptance-criterion artefact)

Per `roadmap.md:434` R-155 acceptance criteria ("upstream-quality-gate-referral-path"), B1 / B2 / B3 resolutions all converge on a single concrete referral channel:

| Field | Value |
|---|---|
| Referral name | **OPS-004 Upstream-Quality-Gate Referral** |
| Recipient | BUILD_REQUEST author for the affected BUILD_REQUEST family (typically the operator running the pipeline, or the BUILD_REQUEST authoring team for a system-driven pipeline) |
| Filed by | rf-task-builder maintainer (on-call) at T+24h diagnosis close |
| Payload format | (a) Release-window identifier; (b) `monotonicity_halt_rate` measurement with numerator/denominator; (c) per-gate decomposition; (d) sampled halt-event list (3 events per §2.2.2) with `|F_{n+1}|` values, cycle indices, gate names; (e) BUILD_REQUEST defect signature per sampled event (anchor ambiguity / prerequisite gap / acceptance-criterion subjectivity); (f) concrete revision recommendation per BUILD_REQUEST family |
| Acceptance signal | BUILD_REQUEST author acknowledges receipt within an agreed window; revises BUILD_REQUEST(s) before next pipeline re-launch in the affected family |
| Verification | Next release window's `monotonicity_halt_rate` for the affected family is back below the `>50%` threshold (target is `<10%`); the next-window rate is the canonical close signal |
| Non-acceptance | If BUILD_REQUEST author does not engage and the next window again breaches `>50%` with the same root-cause class, the referral is escalated to step 5 (Engineering-Lead recurrence handling) |
| Integration point | On-call knowledge base (per `roadmap.md:477`) — the referral template lives there; this runbook is the trigger and the upstream-quality-gate channel is the destination |

The upstream-quality-gate referral path is the structural lever for B1 / B2 / B3 root-cause resolution — it is **explicitly documented** here to satisfy phase-7-tasklist.md L716 ("upstream-quality-gate referral path") + roadmap.md:434 R-155 acceptance criterion.

#### 2.4.4 Cross-runbook composition (with OPS-002, OPS-003, OPS-005)

| Peer | Composition rule | Action |
|---|---|---|
| **OPS-005 (regression-halt rate `>20%`)** | Step 1 (regression) fires BEFORE Step 2 (monotonicity) per the 4-step ordering rule at `SKILL.md:1075` ("Do NOT consult subsequent steps") and `rf-task-builder.md:370` ("Regression takes precedence over monotonicity when both would trigger"). When OPS-005 trips in the same window, a portion of would-be monotonicity halts were pre-empted by regression halts — OPS-004's denominator (`batches_total`) is unchanged, but its numerator (`batches_halted` on monotonicity specifically) may be *suppressed* by regression activity. OPS-004 and OPS-005 are read **jointly** at the M7 audit boundary; resolving the regression-halt rate (OPS-005) may by itself lower the monotonicity-halt rate (OPS-004) without any OPS-004-specific action. | When both trip: diagnose OPS-005 root cause first (Engineering-Lead-owned per `roadmap.md:468`); revisit OPS-004 rate at the next release window post-OPS-005 resolution; only file an OPS-004-specific referral if OPS-004 still breaches `>50%` after OPS-005 is resolved. |
| **OPS-002 (DNSP triage — synthetic-dnsp emission count `>0` in production)** | Synthetic-dnsp findings COUNT as failures for `|F_n|` (per `SKILL.md:1045` + `SKILL.md:1083`). A persistent same-`dedup_key` synthetic-dnsp re-emission across cycles contributes `1` (not `2`) to `|F_{n+1}|` (DEDUP case per `SKILL.md:1083` cross-cycle composition rule — `R-124`/`INV-012`). A sustained Path B cohort (≥1-success + ≥1-exhaust per OPS-002 territory at D-0093) with persistent synthetic-dnsp re-emission can drive `|F_n|` non-shrink at the rf-qa / rf-qa-qualitative gate even when no item-count or BUILD_REQUEST defect is present — the partition agent is genuinely stuck and the dedup-collapse correctly counts the same exhaust once per cycle. | When OPS-002 emission count is elevated in the same window, jointly inspect the affected dedup_keys in the OPS-004 sample. If the elevated OPS-004 rate is dominated by cross-cycle synthetic-dnsp persistence (and the diagnosed BUILD_REQUEST + MDTM are clean), the root cause is upstream-DNSP-driven and route through OPS-002 (D-0093) for the partition-exhaust remediation rather than filing an OPS-004 upstream-quality-gate referral. The two runbooks share the M7 audit table. |
| **OPS-003 (all-partitions-exhaust HALT — Path A zero-success cohort)** | OPS-003 covers Path A cohorts where every partition agent exhausted its escalation ladder. In a Path A cohort, **no monotonicity halt fires for that cohort** because there are no successful partition outputs over which to construct `F_n` — the all-agents-fail guard at `SKILL.md:682` (R-122) upstream-of-the-monotonicity-check routes control to `rf-team-lead.md:417` instead. OPS-003 events therefore do NOT contribute to OPS-004's numerator. | No joint action; OPS-003 events are out-of-band for OPS-004's rate measurement. They both feed MET-004 combined halt-rate but enter through different aggregation paths. |
| **OPS-001 (K-003 audit-target)** | Independent — Self-Audit coverage is orthogonal to monotonicity-halt rate. | No joint action. |

The cross-runbook composition is **explicitly documented** in §2.4.4 + §3 to ensure the M7 audit table reads OPS-004 rate measurements in the correct context.

### 2.5 Prevention

Prevention is enforced by four layered controls, all of which exist at landing time and persist through GA:

1. **API-004 byte-exact halt-string contract.** The wire string `[HALT-MONOTONICITY] |F|=<n>` is frozen at M1 per `roadmap.md:115` ("contract-freeze"); any drift (typo, capitalisation, spacing, `<n>` value) is detectable by exact-match grep and rejected at the COMP-001-M5 `roadmap.md:319` gate. The byte-exact contract makes the rate measurement deterministic at the offline-grep aggregation layer (the same regex catches the same string at every release boundary).
2. **COMP-001-M5 / COMP-002-M5 precedence-rule freeze.** The 4-step ordering rule (`regression → monotonicity → hard-cap → proceed`) is documented in three byte-stable places: the A.9 invariant tail at `SKILL.md:1032`, the protocol body at `SKILL.md:1038-1095`, and the rf-task-builder halt-precedence-rule paragraph at `rf-task-builder.md:358-372`. Triple-anchoring makes accidental modification surface in at least one place under `make verify-sync`.
3. **Per-gate independent-counter invariant.** Each retry counter keeps its own `F_n` history (per `SKILL.md:1043` + `rf-task-builder.md:372` + `SKILL.md:1972` Critical Rule #12 — "Counters are NEVER collapsed"). This prevents one over-aggressive gate from contaminating another's halt-rate measurement and makes per-gate root-cause attribution (§2.2.1.b) possible without restructuring the offline-grep aggregation.
4. **OPEN-INV-006 empirical-calibration roadmap.** The TB-Add-2 advisory→hard promotion path is explicitly tracked at `roadmap.md:348` (OPEN-INV-006 row, Engineering-Lead owner, Phase-2 + PR-05 re-evaluation). Promotion lowers the rate of item-count-driven monotonicity halts at source by blocking out-of-bounds MDTMs at the task-integrity gate rather than letting them propagate into fix-cycle loops. The Phase-2 timing is a deliberate choice: it gives M5+M6+M7 enough operational data to ground the calibration empirically (cross-reference `roadmap.md:348` "informs rate at which `[HALT-MONOTONICITY]` fires on item-count-driven failures").

Secondary preventive measures:

- **Pre-merge gate.** Every PR that touches the FR-CONV.5 surface — `SKILL.md` L1032-1095 (Retry Monotonicity Protocol), `SKILL.md:1972` Critical Rule #12, `rf-task-builder.md:358-372` (halt-precedence rule + monotonicity-guard wrapper) — MUST run `make verify-sync` (A-001), the FR-CONV.5 fixtures (TEST-014..017 per `roadmap.md:323` ff), and a byte-diff confirmation that the API-004 wire-string contract at `roadmap.md:115` is unchanged.
- **TEST-015 fixture** (`test_monotonicity_halt_F_5_5_5` at `roadmap.md:323`) — 3-cycle fixture: `|F|=5, 5, 5` halts at cycle 2 with `[HALT-MONOTONICITY] |F|=5`; cycle 3 not attempted. Locks the halt-message byte-exact and the cycle-boundary semantics.
- **MET-004 dashboard** (per `roadmap.md:441` + `roadmap.md:574`) — combined halt-rate metric tracks all 3 halt-message families (synthetic-dnsp, HALT-MONOTONICITY, regression-halt) with explicit per-trigger routing into OPS-002 / OPS-004 / OPS-005.
- **Release-spec §8.3 audit row** — every release's post-mortem inspects the monotonicity-halt rate; the rf-task-builder maintainer maintains a rolling window log so trend lines (not just per-release point readings) feed the GA-tagging committee.
- **Cross-cycle dedup composition invariant** (`SKILL.md:1083-1093`) — synthetic-dnsp same-`dedup_key` re-emissions contribute `1` (not `2`) to `|F_{n+1}|`, so legitimate slow-convergence cohorts are NOT spuriously halted. Without this invariant, OPS-004 would chase ghost rate breaches driven by counter-double-counting; with it, the halts that fire are real and the rate-level signal is information-bearing.
- **X-003 rejection** (per `roadmap.md:305` "X-003 slow-convergence threshold remains REJECTED") — by explicitly rejecting the "halt if shrinks less than X" variant, the contract guarantees legitimate slow convergence (`|F|=5,4`) does NOT halt; this caps the false-positive rate at the contract boundary rather than letting it drift into operational tuning.
- **Audit-trail explicitness.** Every monotonicity-halt emission carries (i) the `<n>` value (= `|F_{n+1}|`), (ii) the cycle index, (iii) the gate name, (iv) the originating BUILD_REQUEST identifier — making per-window aggregation per-gate-decomposable from logs without re-running pipelines.

---

## 3. `>50%` threshold (signature measurement)

| Field | Value |
|---|---|
| Threshold value | **`monotonicity_halt_rate > 0.50`** (strict-greater; the `>50%` value is the alert trigger per `roadmap.md:434` R-155 + `roadmap.md:441` MET-004 + `roadmap.md:467` OPS-004 + `roadmap.md:574` MET row) |
| Target value | `monotonicity_halt_rate < 0.10` (per `roadmap.md:574` "<10% target") |
| Watch band | `0.10 ≤ monotonicity_halt_rate ≤ 0.50` — surfaced in MET-004 but does NOT trigger OPS-004 |
| Numerator | Count of fix-cycle batches in the window where ≥1 `[HALT-MONOTONICITY]` was emitted |
| Denominator | Count of independent fix-cycle batches in the window (per-gate decomposed: research-gate / synthesis-gate / report-validation / task-integrity / qualitative — never collapsed per `SKILL.md:1043` + `rf-task-builder.md:372`) |
| Aggregation mechanism | Offline grep against fix-loop logs (per `roadmap.md:574` "grep `[HALT-MONOTONICITY]` in fix-loop logs; offline aggregate per release") |
| Inspection cadence | Per release window (per `roadmap.md:441` "offline-grep-aggregate-per-release"); GA-tagging committee at MIG-007b reads rolling trend |
| Why `>50%` (not lower) | Below 50%, the underlying behaviour is well within the "some partition agents are getting stuck on some BUILD_REQUESTs" baseline that the FR-CONV.5 guard exists to catch — i.e., the halts are useful information, not a defect signal. Above 50%, more batches halt than succeed, which crosses from "guard is doing its job" into "upstream input is systemically defective" territory. The choice of 50% reflects the design intent of the guard (stop wasted fix-cycles when the partition agent is stuck) calibrated against the cost of upstream-quality-gate referrals (which are non-trivial; each referral consumes BUILD_REQUEST-author attention). The `<10%` target is the steady-state goal; the 10%-50% band is a watch state, not an alert state. |
| Why strict-greater (not ≥) | Per `roadmap.md:434` "threshold-greater-than-50%-documented" — the threshold is strictly above 50%, so exactly-50% is below the alert and exactly-50%+1-event is at the alert. This matches the OPS-005 strict-greater `>20%` convention for symmetry. |

The `>50%` threshold is **explicitly documented** in §0 TL;DR, §1 frontmatter (Threshold row), §2.1 symptom 3, §2.4.1 (window measurement table), and §3 (this section) to satisfy phase-7-tasklist.md L715 (">50% threshold documented") + roadmap.md:434 R-155 acceptance criterion.

---

## 4. Cross-reference to OPEN-INV-006

| Field | Value |
|---|---|
| Anchor | `roadmap.md:348` — §18 Open Items row 1 |
| Verbatim text | "Empirical calibration of TB-Add-2 item-count bounds (≥3 / ≤40 track / ≤50 single-track). TB-Add-2 stays `[ADVISORY]` until calibrated. Source: TDD §22 / OPEN-INV-006." |
| Severity | MEDIUM — "affects when TB-Add-2 can promote from ADVISORY to Hard; informs rate at which `[HALT-MONOTONICITY]` fires on item-count-driven failures" |
| Owner | Engineering (per the §18 owner column) |
| Scheduled resolution | Phase-2 (with PR-05 re-evaluation) — per `roadmap.md:348` |
| Linkage to OPS-004 | OPS-004 root-cause class **B4** (item-count bounds drift) is the operational signal that materialises the OPEN-INV-006 cost: an elevated monotonicity-halt rate driven by item-count-driven failures is the empirical evidence that TB-Add-2 advisory-status is insufficient. The OPS-004 sampled-3-events + MDTM inspection (§2.2.4) directly produces the calibration evidence that OPEN-INV-006 needs. |
| TB-Add-2 advisory governance | `roadmap.md:100` — "Item-count bounds ≥3 / ≤40-track / ≤50-single-track; emits `[ADVISORY]` prefix and does NOT block gate (pending OPEN-INV-006 calibration)" |
| FF_TB_ADD_1_THROUGH_8 row | `roadmap.md:122` — "TB-Add-2:stays-ADVISORY-until-Phase-2; owner:rf-qa-maintainer; M7-consolidation:see-M7-governance-table" |
| Resolution path linkage | OPS-004 B4 resolution = file OPEN-INV-006 calibration referral to Engineering Lead (per §2.3 B4 row). The referral is the bridge between the OPS-004 rate-level signal and the OPEN-INV-006 calibration workflow. |
| Why TB-Add-2 calibration matters for monotonicity rate | `|F_n|` is the FAIL-verdict set cardinality (`SKILL.md:1064`); set membership is keyed by dedup-key. An MDTM with item-count above the TB-Add-2 advisory bounds (say, 60 items on a single track when ≤50 is recommended) typically produces an enlarged FAIL set per cycle, which makes the monotonicity guard fire faster on non-shrink (a 60-item track that resolves only 3 items per cycle hits `|F_{n+1}| >= |F_n|` on the same cycle a 30-item track would have converged) — i.e., the rate of monotonicity halts is partially a function of item-count distribution, and TB-Add-2 calibration is the structural lever for shifting that distribution. |
| Promotion path | When OPEN-INV-006 calibration lands (Phase-2 / post-PR-05 re-evaluation): TB-Add-2 promotes from `[ADVISORY]` (per `roadmap.md:100`) to Hard (gate-blocking on out-of-bounds item-counts). Out-of-bounds MDTMs are then rejected at task-builder boundary rather than propagating into fix-cycle loops, lowering the OPS-004 rate at source. |
| Linkage to M7 cleanup window | The FF_TB_ADD_1_THROUGH_8 flag has GA+30d cleanup window per `roadmap.md:452` — the M7 consolidated governance table tracks the path from "TB-Add-2 advisory" through "OPEN-INV-006 calibration lands" through "TB-Add-2 hard" through "GA+30d feature-flag cleanup". OPS-004 is a downstream observability channel that surfaces evidence for the calibration step. |

The cross-reference is **explicitly documented** in §0 TL;DR, §1 frontmatter (Cross-reference row), §1 authority bindings (OPEN-INV-006 row + TB-Add-2 governance row + FF_TB_ADD_1_THROUGH_8 row), §2.2.4 MDTM inspection (TB-Add-2 advisory check), §2.2.6 B4 root-cause classification, §2.3 B4 resolution (OPEN-INV-006 calibration referral), §2.5 prevention control 4, and §4 (this section) to satisfy phase-7-tasklist.md L718 ("Cross-reference to OPEN-INV-006") + roadmap.md:434 R-155 wiring.

---

## 5. Resolution path — improve upstream BUILD_REQUESTs OR TB-Add-2 calibration

| Field | Value |
|---|---|
| Resolution model | **Dual** — every OPS-004 rate breach resolves into one of two paths: (a) **improve upstream BUILD_REQUESTs** via the upstream-quality-gate referral path; OR (b) **calibrate TB-Add-2** from `[ADVISORY]` to Hard via OPEN-INV-006 empirical calibration. The dual path is by design — single rate-level signal at the output, but two distinct upstream levers, so the maintainer's job is to identify which lever applies to the sampled events. |
| Authority | `roadmap.md:434` R-155 row ("resolution = improve upstream BUILD_REQUESTs or TB-Add-2 calibration (OPEN-INV-006)") |
| Path (a) — upstream BUILD_REQUEST improvement | Triggered by root-cause classes B1 / B2 / B3 (BUILD_REQUEST scope ambiguity, prerequisite gap, acceptance-criterion subjectivity). Mechanism = OPS-004 upstream-quality-gate referral (§2.4.3). Owner = BUILD_REQUEST author. Verification = next-release-window rate. |
| Path (b) — TB-Add-2 calibration | Triggered by root-cause class B4 (item-count bounds drift). Mechanism = OPEN-INV-006 calibration referral (§2.3 B4). Owner = Engineering Lead (per `roadmap.md:348`). Verification = post-calibration release-window rate. Calibration timing = Phase-2 / post-PR-05 re-evaluation (per `roadmap.md:348` schedule). |
| What "improve upstream BUILD_REQUESTs" means | Revise BUILD_REQUEST(s) in the affected family with: (i) tighter research anchors (concrete assigned_files ranges, no "research everything" language), (ii) bounded scope (per-partition surface fits within typical context-window budget), (iii) explicit prerequisite artifact references with verifiable file paths, (iv) grep-decidable acceptance-criterion predicates. Each revised BUILD_REQUEST is re-submitted to a fresh pipeline run. |
| What "TB-Add-2 calibration" means | Empirical determination of the operational ≥3 / ≤40 track / ≤50 single-track item-count bounds via OPEN-INV-006 methodology — drawing on M5+M6+M7 operational data to set bounds at values where TB-Add-2's `[ADVISORY]` emissions correlate strongly with downstream monotonicity-halt events; once calibrated, TB-Add-2 promotes from `[ADVISORY]` to Hard so out-of-bounds MDTMs are rejected at the task-integrity gate. |
| Forbidden resolutions | Modifying the FR-CONV.5 halt-precedence wrapper itself, changing the byte-exact halt-string, collapsing per-gate counters, raising the `>50%` threshold, introducing X-003 — all explicitly disallowed (see §2.3 "Explicit non-resolutions"). The dual resolution path operates exclusively on the upstream-input side of the system. |
| Why dual (not single) | A monotonicity-halt rate breach can be caused by (a) BUILD_REQUEST-level defects that propagate into stuck fix-cycles regardless of item-count, OR (b) item-count distribution that overwhelms the cycle budget regardless of BUILD_REQUEST quality. The two causes are distinct and need distinct levers; the §2.2 diagnosis classifies into B1/B2/B3 (path a) vs. B4 (path b). A single-path resolution would either over-burden BUILD_REQUEST authors with referrals when calibration was the right lever, or accumulate unfiled calibration evidence when BUILD_REQUEST revision was the right lever. |
| Acceptance signal | The next-release-window `monotonicity_halt_rate` for the affected family is back below the `>50%` threshold (target `<10%`). For path (b), the verification window is post-calibration-landing, not the next window after referral filing. |
| Window-by-window tracking | Each OPS-004 trigger is logged in the M7 audit table with: trigger window, rate measurement, sampled events, root cause, resolution path filed, verification window, verification result. Patterns across windows surface to the GA-tagging committee at MIG-007b. |

The dual resolution path is **explicitly documented** in §0 TL;DR, §1 frontmatter (Resolution path row), §2.3 (resolution table per B1..B5), and §5 (this section) to satisfy phase-7-tasklist.md L717 ("Resolution path: improve upstream BUILD_REQUESTs or TB-Add-2 calibration") + roadmap.md:434 R-155 acceptance criterion.

---

## 6. Acceptance criteria — T07.15

| # | Criterion (phase-7-tasklist.md L713-718) | Status | Evidence |
|---|---|---|---|
| 1 | File `TASKLIST_ROOT/artifacts/D-0095/spec.md` exists with 5 runbook sections. | **PASS** | This file at `.dev/releases/current/task-builder-merge/artifacts/D-0095/spec.md`; §2.1 Symptoms, §2.2 Diagnosis, §2.3 Resolution, §2.4 Escalation, §2.5 Prevention. |
| 2 | `>50%` threshold documented. | **PASS** | §3 (dedicated threshold section — value, target, watch band, numerator/denominator definitions, aggregation, cadence, strict-greater rationale); also §0 TL;DR, §1 frontmatter "Threshold (alert)" row, §1 authority bindings (R-155, MET-004, OPS-004, MET-row at `roadmap.md:574`), §2.1 symptom 3 (`monotonicity_halt_rate > 0.50`), §2.4.1 (window measurement table). Authority: `roadmap.md:434` "threshold-greater-than-50%-documented" + `roadmap.md:441` "monotonicity-alert:>50%-triggers-OPS-004" + `roadmap.md:467` "Threshold >50% of batches" + `roadmap.md:574` ">50% triggers upstream BUILD_REQUEST defect alert (OPS-004)". |
| 3 | Resolution path: improve upstream BUILD_REQUESTs or TB-Add-2 calibration. | **PASS** | §5 (dedicated dual-path resolution section — model, authority, path (a) upstream BUILD_REQUEST improvement via §2.4.3 referral, path (b) TB-Add-2 calibration via OPEN-INV-006, forbidden alternatives, why dual, acceptance signal, window-by-window tracking); §2.3 (B1..B4 resolution table maps each root-cause class to one of the two paths); §2.4.3 upstream-quality-gate referral channel; §0 TL;DR + §1 frontmatter "Resolution path" row. Authority: `roadmap.md:434` "resolution = improve upstream BUILD_REQUESTs or TB-Add-2 calibration (OPEN-INV-006)". |
| 4 | Cross-reference to OPEN-INV-006. | **PASS** | §4 (dedicated cross-reference section — anchor, verbatim text, severity, owner, scheduled resolution, linkage to OPS-004 B4, TB-Add-2 advisory governance, FF_TB_ADD_1_THROUGH_8 row, resolution path linkage, why calibration matters for the rate, promotion path, M7 cleanup-window linkage); cross-referenced at §0 TL;DR, §1 frontmatter "Cross-reference to OPEN-INV-006" row, §1 authority bindings (OPEN-INV-006 + TB-Add-2 + FF_TB_ADD_1_THROUGH_8 rows), §2.2.4 MDTM inspection, §2.2.6 B4 root-cause class, §2.3 B4 resolution row, §2.5 prevention control 4. Authority: `roadmap.md:348` OPEN-INV-006 row + `roadmap.md:100` TB-Add-2 row + `roadmap.md:122` FF_TB_ADD_1_THROUGH_8 row + `roadmap.md:434` R-155 wiring. |

**Verdict: PASS** — OPS-004 `[HALT-MONOTONICITY]` Rate runbook is published, 5-section structured, `>50%` threshold documented end-to-end with numerator/denominator definitions and aggregation specification, dual resolution path (improve upstream BUILD_REQUESTs OR TB-Add-2 calibration) anchored to roadmap.md:434 R-155, and OPEN-INV-006 cross-referenced at ten call sites with promotion-path linkage. Ready for rf-task-builder maintainer review and for consumption by the GA-tagging committee at T07.20 (MIG-007b).

---

## 7. Cross-references

| Linkage | Target | Role |
|---|---|---|
| **FR-CONV.5 halt-precedence wrapper (rf-task-builder)** | `src/superclaude/agents/rf-task-builder.md:358-372` | Production halt-emission site; OPS-004 measures its output rate |
| **FR-CONV.5 Retry Monotonicity Protocol (SKILL.md)** | `src/superclaude/skills/task-builder/SKILL.md` L1032-1095 | Authoritative protocol — 4-step ordering rule, F_n dedup-key identity, cross-cycle composition rule, regression non-emission invariant |
| **API-004 halt-signal byte-exact contract** | `roadmap.md:115` | Wire-string contract `[HALT-MONOTONICITY] \|F\|=<n>`; offline-grep target for MET-004 aggregation |
| **COMP-001-M5 (SKILL.md A.9 separate-counters invariant tail)** | `roadmap.md:319` + `SKILL.md:1032` | Halt-precedence note location; verified by `grep-[HALT-MONOTONICITY]-in-SKILL.md:867-873:returns-≥1-match` |
| **COMP-002-M5 (rf-task-builder.md halt-precedence rule)** | `rf-task-builder.md:358` | "Halt-precedence rule (COMP-002-M5 — applies to every row in the table below)" |
| **Per-gate independent-counter invariant** | `SKILL.md:1043` + `SKILL.md:1972` Critical Rule #12 + `rf-task-builder.md:372` | Never-collapse rule; per-gate root-cause attribution depends on this |
| **F_n dedup-key set identity** | `SKILL.md:1064` + `SKILL.md:1068` | `F_n` is a SET keyed by dedup-key; `\|F_n\|` is post-dedup cardinality |
| **Cross-cycle dedup composition (synthetic-dnsp DEDUP vs. regression)** | `SKILL.md:1083-1093` (R-124 / INV-012) | Cross-cycle same-`dedup_key` re-emission contributes 1 to `\|F_{n+1}\|`; legitimate slow-convergence kept alive |
| **X-003 slow-convergence threshold (REJECTED)** | `roadmap.md:305` | Explicit rejection — `\|F\|=5,4` does NOT halt; only strict non-shrink halts |
| **TB-Add-2 ADVISORY governance** | `roadmap.md:100` | Item-count bounds emitting `[ADVISORY]`; gate-verdict unaffected |
| **OPEN-INV-006 calibration roadmap** | `roadmap.md:348` | Phase-2 / post-PR-05 re-evaluation; structural lever for B4 root cause |
| **FF_TB_ADD_1_THROUGH_8 feature-flag governance** | `roadmap.md:122` + `roadmap.md:452` | Logical flag; TB-Add-2 stays ADVISORY until Phase-2; GA+30d cleanup |
| **MET-004 Halt Rate (combined) measurement** | `roadmap.md:441` + `roadmap.md:461` | Aggregation source; trigger row for OPS-002 / OPS-004 / OPS-005 |
| **MET-004 metric row in M7 audit table** | `D-0091/spec.md §2` MET-004 + OPS-004 rows | Consolidated GA-Readiness Governance Table entry |
| **§17 metric row — `[HALT-MONOTONICITY]` emission rate** | `roadmap.md:574` | "<10% target; >50% triggers" with offline-grep aggregation recipe |
| **OPS-005 peer runbook (regression-halt rate)** | `D-0096/spec.md` (T07.16, R-156) | Precedence-chain partner — regression halts pre-empt monotonicity halts per Step 1 → Step 2 ordering |
| **OPS-002 peer runbook (DNSP triage)** | `D-0093/spec.md` (T07.13, R-153) | Synthetic-dnsp finds count as failures for `\|F_n\|`; sustained Path B re-emission can drive rate up without an upstream BUILD_REQUEST defect (§2.4.4) |
| **OPS-003 peer runbook (all-partitions-exhaust HALT)** | `D-0094/spec.md` (T07.14, R-154) | Path A cohorts produce zero monotonicity halts (all-agents-fail guard upstream); out-of-band for OPS-004 measurement |
| **OPS-001 peer runbook (K-003 audit-target)** | `D-0092/spec.md` (T07.11, R-152) | Orthogonal — Self-Audit coverage independent of monotonicity-halt rate |
| **TEST-015 fixture (monotonicity halt at F=5,5,5)** | `roadmap.md:323` | Locks halt-message byte-exact + cycle-boundary semantics |
| **TEST-014..017 FR-CONV.5 fixtures** | `roadmap.md:323` ff (Phase-5 task block) | Pre-merge gate fixtures for the halt-precedence wrapper |
| **Release-spec §19.4 rollback dependency matrix** | `release-spec.md` §19.4 | Path invoked under §2.4 step 6 (B5 contract-violation rollback scoped to MIG-005) |
| **Consolidated GA-Readiness Governance Table** | `D-0091/spec.md §2` (OPS-004 row) | This runbook is OPS-004 in that table |
| **GA-tagging gate (MIG-007b)** | `D-0099/spec.md` (T07.20, R-165) | Hard pre-requisite — all 7 OPS runbooks must be live for GA tag |
| **Integration point — on-call knowledge base** | `roadmap.md:477` (M7 Integration Points row 2) | Where this runbook is consumed by rf-task-builder maintainers on-call rotation; upstream-quality-gate referral template lives here |
| **MIG-005 landing anchor commit** | `db6166e feat(task-builder): MIG-005 land FR-CONV.5 Retry Monotonicity + Regression Halts (M5)` | Production monotonicity-halt enforcement anchor; OPS-004 measurement window starts here |
| **Phase-7 dependency (T07.14 → T07.15)** | `phase-7-tasklist.md` L723 ("Dependencies: Phase 5 (M5 PASS); T07.14") | OPS-003 (D-0094) must land before OPS-004 (mutual-exclusivity peer ordering on the Path-A composition; OPS-005 lands next at T07.16) |

---

## 8. Provenance

- **Dependency:** Phase 5 (M5 PASS — MIG-005 landed at `db6166e`); T07.14 OPS-003 runbook (D-0094) — Path-A peer must land first to establish the cohort-level guard composition (all-agents-fail upstream of monotonicity).
- **Downstream consumers:** T07.16 OPS-005 regression-halt rate runbook (D-0096) — Step 1 partner in the precedence chain, lands next; T07.18 mid-phase checkpoint (`CP-P07-T13-T17.md`); T07.19 MET-001..006 instrumentation (MET-004 reads HALT-MONOTONICITY rate this runbook responds to); T07.20 GA-tag (MIG-007b) — hard pre-requisite (all 7 OPS runbooks live).
- **Anchor commit (monotonicity-halt enforcement start in production):** `db6166e feat(task-builder): MIG-005 land FR-CONV.5 Retry Monotonicity + Regression Halts (M5)`.
- **API-004 byte-exact wire-string invariant:** `[HALT-MONOTONICITY] |F|=<n>` (pinned at `roadmap.md:115` contract-freeze; `SKILL.md:1057` + `SKILL.md:1075` + `rf-task-builder.md:370`).
- **COMP-001-M5 precedence-rule invariant:** 4-step ordering `regression → monotonicity → hard-cap → proceed` pinned at `SKILL.md:1032` + `SKILL.md:1075` (NO DRIFT verified per `roadmap.md:319` grep target "SKILL.md:867-873:returns-≥1-match").
- **COMP-002-M5 halt-precedence rule invariant:** Per `rf-task-builder.md:358` + `:370` + `:372` (NO DRIFT verified per FR-CONV.5 fixtures TEST-014..017 at `roadmap.md:323` ff).
- **TB-Add-2 advisory-status binding:** `roadmap.md:100` ("emits `[ADVISORY]` prefix and does NOT block gate (pending OPEN-INV-006 calibration)") + `roadmap.md:122` ("TB-Add-2:stays-ADVISORY-until-Phase-2").
- **OPEN-INV-006 calibration schedule:** Phase-2 with PR-05 re-evaluation (per `roadmap.md:348`).
- **Reporting cut-off:** 2026-05-18 14:44 UTC (current session timestamp from session-context envelope).
- **Release branch:** `feat/hook-sync-and-matcher-fix`.
- **Session HEAD:** `efaa33db9f0087bb1c48236b12c1287171b4f9f8` (`chore(hooks): resolve OQ-2 (archive+delete bash-gate orphan) and OQ-3 (register reject-workspace-writes.sh)`).
- **MCP usage:** Sequential (preferred) — applied for runbook authoring (multi-step reasoning across §2.1-§2.5 + rate-measurement window definition + dual-resolution path partitioning into root-cause classes B1..B4 + cross-runbook composition rules vs. OPS-002/OPS-003/OPS-005 + OPEN-INV-006 linkage closure against TB-Add-2 advisory governance + API-004 byte-exact wire-string preservation).
