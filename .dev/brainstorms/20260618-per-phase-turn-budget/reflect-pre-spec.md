---
title: "sc:reflect PRE/DEEP — Coverage + Best-Practice Audit of merged-requirements-v2.md"
command: /sc:reflect
mode: pre
depth: deep
tier_reached: 2
spec_under_validation: ".dev/brainstorms/20260618-per-phase-turn-budget/merged-requirements-v2.md (spec_version 2.0)"
driving_context:
  - ".dev/brainstorms/20260618-per-phase-turn-budget/seed-brief.md (C1-C6, S1-S6, Q1-Q7)"
  - ".dev/troubleshoot/phase56-budget-exhaustion-20260617/REPORT.md (root cause; OLD drifted anchors)"
  - ".dev/brainstorms/20260618-per-phase-turn-budget/spec-panel/PANEL-REVIEW.md"
ground_truth_worktree: ".claude/worktrees/perPhaseturnBudget (HEAD = origin/master)"
review_date: 2026-06-18
reviewers: [requirements-analyst/sonnet (analyzer), quality-engineer/haiku (qa), system-architect/opus (architect)]
merge_method: adversarial-convergence (cross-class agreement)
verdict: PARTIAL → remediated to PASS
score: 0.93
remediated_to: ".dev/brainstorms/20260618-per-phase-turn-budget/merged-requirements-FINAL.md (spec_version 3.0)"
---

# sc:reflect PRE/DEEP — Per-Phase Turn-Budget Spec v2 Coverage Audit

> DEEP depth forced Tier 2 (heterogeneous reviewer ensemble + adversarial merge). Three reviewers on
> three model classes (sonnet/haiku/opus) audited spec v2 against the seed brief independently. Every
> `file:line` code anchor cited below was re-Read against the live worktree files **this turn**.

## 1. Verdict

| Field | Value |
|-------|-------|
| **Pre-remediation verdict** | **PARTIAL** (0.78) — strong coverage, but 5 gaps all rooted in two unresolved open questions (OQ-1, OQ-2) plus one conditional/untestable test row (TM-13). |
| **Post-remediation verdict** | **PASS** (0.93) — both open questions were adjudicated by the orchestrator; applying the rulings closes all 5 gaps and pins TM-13. |
| **Remediated spec** | `merged-requirements-FINAL.md` (spec_version 3.0) |

The spec's *engineering substance* is sound and exhaustively anchored (spec-panel already verified the executor.py mechanism against live code; this reflect pass re-verified the load-bearing anchors and the KPI consumer chain). The PARTIAL was **not** a substance failure — it was a "design doc handed to task-builder while still carrying two open questions and a test with two contradictory expected values." That is a real pre-execution blocker (a task-builder cannot build a test that asserts `== 5 OR == 2`). The orchestrator's two adjudications resolve it.

## 2. Anchor re-verification (this turn, live files)

| Anchor (spec claim) | Live code | Verdict |
|---------------------|-----------|---------|
| Global construction `initial_budget=config.max_turns * len(config.active_phases)` @`executor.py:1777-1780` | exact | VERIFIED |
| `shadow_metrics = ShadowGateMetrics()` @`executor.py:1782` (R-10 accumulator site) | exact | VERIFIED |
| Phase loop `for phase in config.active_phases:` @`executor.py:1813` | exact | VERIFIED |
| python `continue` @1819-1820, skip `continue` @1823-1834 | exact | VERIFIED |
| `tasks = _parse_phase_tasks(phase, config)` @1838, `if tasks:` @1839 | exact | VERIFIED |
| Task-branch `ledger=ledger` @1860 | exact | VERIFIED |
| Task-path wiring hook `run_post_phase_wiring_hook(..., ledger=ledger)` @1911-1917 (`ledger=` @1915) | exact | VERIFIED |
| Legacy wiring hook @2281-2287 (`ledger=ledger` @2285) | exact | VERIFIED |
| Reconciliation `pre_allocated = ledger.minimum_allocation` @1125-1132 (var @1128) | exact | VERIFIED |
| Post-loop `build_kpi_report(..., turn_ledger=ledger)` @2414-2418 | exact | VERIFIED |
| KPI write `gate-kpi-report.md` @2419-2420 | exact | VERIFIED |
| `kpi.py` `build_kpi_report` signature @151-158; `if turn_ledger is not None` @192; reads @193/195/197 | exact | VERIFIED |
| `models.py` `TurnLedger` class @1011-1124; fields @1024-1034; `available()` @1044-1046; `debit` @1048-1053; `__post_init__` @1036-1042 | exact (v2 re-anchor correct) | VERIFIED |

**KPI consumer-chain confirmation (OQ-1 Position A grounding):** `executor.py:2417` passes `turn_ledger=ledger`; `kpi.py:193` reads `turn_ledger.wiring_turns_used`, `:195` reads `wiring_turns_credited`, `:197` reads `wiring_analyses_count`; the result is written to the persisted `gate-kpi-report.md` at `executor.py:2419-2420`. The architect reviewer's package-wide grep confirmed this is the **only** post-loop consumer of ledger wiring fields. After per-phase fresh-construct, the post-loop `ledger` is the **last phase's** instance → silent collapse of sprint-cumulative wiring KPIs to last-phase-only. The accumulator (Position A) is read-only summation; it does NOT reintroduce a shared mutable budget pool. **This grounds mandatory remediation #1.**

## 3. Coverage Matrix (C / S / Q → covered? evidence)

Status legend: Y = covered; P = partial (pre-remediation); → = closed by remediation.

| ID | Pre | Spec evidence (v2) | Gap (pre) | Post-remediation |
|----|-----|--------------------|-----------|------------------|
| C1 (`--max-turns` per-phase semantics) | Y | C1 @188; R-2 @96-103; R-3 @105-109 | — | Y |
| C2 (legacy subprocess unchanged) | P | Q3 @50; R-6 @127-140; C2 @189-190 | legacy wiring-hook ledger input intentionally changed; "unchanged" needs scoping | → resolved: FINAL scopes C2 to subprocess log; wiring delta is the deliberate, OQ-2-noted refinement, pinned TM-13/TM-8 |
| C3 (thread-safety K>1) | Y | Q1 @48; R-9 @155-166; TM-12 @208 | — | Y |
| C4 (monotonicity across reset) | Y | Q1 @48; R-7 @142-147; TM-6 @202 | — | Y |
| C5 (wiring/reimbursement fate across reset) | P | Q5 @52; R-4 @111-118; R-10 @168-184; TM-13 @209 | KPI wiring fate left open (OQ-1) | → resolved: OQ-1 Position A pins sprint-cumulative wiring via accumulator |
| C6 (minimal blast radius) | P | R-1/R-2 @87-103; blast table @213-226 | final blast radius depends on OQ-1 | → resolved: Position A blast radius now fixed (1 del + 1 add + small accumulator + 2 add-sites + 1 arg swap) |
| S1 (3×5 sprint, zero spurious SKIPPED) | Y | TM-0 @198 | — | Y |
| S2 (starvation impossible by construction) | Y | R-3 @105-109; R-4 @111-118; TM-10 @206 | — | Y |
| S3 (budget = max_turns × phase task count) | Y | Q2 @49; R-2 @96-103; TM-0/TM-1 @198-199 | — | Y |
| S4 (legacy path unchanged) | P | R-6 @127-140; TM-7 @203; TM-8 @204 | same as C2 — subprocess log only | → resolved with C2 |
| S5 (wiring + reimbursement per documented decision) | P | Q5 @52; R-10 @168-184; TM-13 @209 | decision not finalized | → resolved: OQ-1 ruling = the documented decision |
| S6 (testable unit + integration + per-phase assertion) | Y | TM matrix @194-211 | — | Y |
| Q1 (reset mechanism = fresh construct) | Y | Q1 @48; R-7 @142-147 | — | Y |
| Q2 (lazy sizing at phase entry) | Y | Q2 @49; R-2 @96-103 | — | Y |
| Q3 (legacy budget = max_turns × 1, ledger IS consulted) | Y | Q3 @50; R-6 @127-140; TM-8 @204 | — | Y |
| Q4 (reimbursement/consumed reset to 0, no carryover) | Y | Q4 @51; R-4 @111-118 | — | Y |
| Q5 (wiring fields fate) | P | Q5 @52; R-10 @168-184; K-4 @239-240 | OQ-1 open | → resolved: Position A |
| Q6 (reset placement @1838, both branches) | Y | Q6 @53; R-8 @149-153 | — | Y |
| Q7 (gate = pure safety net) | P | Q7 @54; R-5 @120-125; TM-9 @205 | OQ-2 resume-exactness caveat dangling; handoff gates only on OQ-1 | → resolved: OQ-2 hybrid ruling softens the invariant wording + adds resume note |

**Root-cause coverage (REPORT.md):** the spec's Problem section (@32-42) is a verbatim match to REPORT.md's diagnosis (global pool `max_turns × phase_count`, 309 > 300 → SKIPPED → ERROR). REPORT.md's OLD anchors (1651-1653, 1119-1130) are drifted as warned; the spec re-anchored them correctly to live code (1777-1780, 1125-1132). Root cause fully covered.

## 4. Gap Registry (pre-remediation) + disposition

| # | Gap | Source reviewers | Severity | Disposition |
|---|-----|------------------|----------|-------------|
| G-1 | OQ-1 (KPI accumulator vs accept-last-phase) left unresolved → C5/S5/Q5 partial, blast radius (C6) unstable | analyzer, qa, architect | HIGH (blocks task-build) | **CLOSED** by mandatory remediation #1 (Position A — accumulator + wire to build_kpi_report). |
| G-2 | TM-13 carries two contradictory expected values (`==5` Position A OR `==2` Position B) — not a runnable test | qa, analyzer | HIGH (untestable) | **CLOSED** — TM-13 pinned to Position A (`wiring_analyses_run == 5`, sprint-cumulative). |
| G-3 | OQ-2 (resume-run sizing exactness) dangling; Q7 invariant over-claims "exactly covers N" on `--resume`; handoff gates only on OQ-1 | analyzer, qa | MEDIUM (doc precision) | **CLOSED** by mandatory remediation #2 (hybrid: keep `max_turns × len(tasks)` sizing, soften invariant wording, add resume/dependency-wave note). |
| G-4 | C2/S4 "legacy unchanged" over-claims given intended wiring-hook delta | analyzer, architect | LOW (wording) | **CLOSED** — FINAL scopes "byte-equivalent" to subprocess log; wiring delta is the deliberate refinement, explicitly documented. |
| G-5 | F-T4: no TM row for `--resume`/`--start` per-phase sizing parity | qa, analyzer | LOW (belt-and-suspenders) | **CLOSED** — FINAL adds TM-14 (resume-window parity), making the OQ-2 note testable. |

No best-practice violations beyond the above. No fabricated anchors (every cited line re-Read this turn). No untestable requirement survives remediation (TM-13 pinned; TM-14 added).

## 5. Deviation classification (UC-1)

This is a PRE-execution review, so the 4-category UC-2 deviation taxonomy (Authorized/Necessary/Drift/Regression) does not apply to executed work. The only "deviations" are spec-internal: two **Authorized expansions** (the orchestrator-adjudicated OQ-1 and OQ-2 rulings) and three **doc-precision corrections** (TM-13 pin, C2/S4 scoping, TM-14 add). All are authorized by the orchestrator mandate.

## 6. Score derivation

| Dimension | Pre | Post | Notes |
|-----------|-----|------|-------|
| Citation grounding | 1.00 | 1.00 | every anchor re-Read live, exact |
| Coverage completeness | 0.72 | 0.95 | 5 partial C/S/Q rows pre; all closed post |
| Decision-classification clarity | 0.60 | 0.95 | OQ-1/OQ-2 open pre; adjudicated post |
| Risk-surface coverage | 0.85 | 0.92 | F-T4 resume gap closed by TM-14 |
| Recommendation actionability | 0.70 | 0.92 | TM-13 untestable pre; pinned post |
| **Mean** | **0.77** | **0.93** | PARTIAL → PASS |

## 7. Hallucination contract

Every claim above is **Grounded** (real `file:line` re-Read this turn, or a real spec/brief/panel section). No `[INFERRED]` claims were load-bearing. Zero fabricated anchors. The KPI consumer chain (the spine of mandatory remediation #1) was independently confirmed by the opus architect reviewer's package-wide grep AND this orchestrator's direct Read of `kpi.py:192-197` + `executor.py:2414-2420`.
