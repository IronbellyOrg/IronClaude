# TDD §22-§26 — Open Questions, Timeline, Release Criteria, Operational Readiness, Cost

**Status:** Complete
**Date:** 2026-05-14
**Synthesis agent:** synth-08
**Scope:** TDD §22 Open Questions, §23 Timeline & Milestones, §24 Release Criteria, §25 Operational Readiness, §26 Cost & Resource Estimation
**Sources:** research/00-prd-extraction.md, research/06-rf-task-builder-encoding.md, research/07-rf-team-lead-escalation.md, research/12-fr5-retry-monotonicity.md, qa/research-gate-consolidated.md (SC-1..SC-8)

---

## §22 Open Questions

Combines the six PRD-sourced OPEN questions (PRD §13) with the new SC-1 critical contradiction
(elevated to §22 status by the Phase-3 research gate, see `qa/research-gate-consolidated.md` line 71)
and three design-management questions resolved within the TDD body.

| ID | Question | Owner | Target Date | Status | Resolution |
|----|----------|-------|-------------|--------|------------|
| **Q-DM-1** | **§25.4 Per-Item Checklist Schema PRD-vs-source contradiction:** PRD declares the per-item 5-field schema `{Description, Context, Acceptance, Confidence, Verification}` is "preserved unchanged" at `SKILL.md:1452-1457`, BUT grep confirms zero hits for `Acceptance` / `TB-Add-8` in SKILL.md and current content at SKILL.md:1450-1460 is `{Context, Action, Output, Verification, Completion gate}`. Three resolution options listed in §7.1 Entity 4. Engineering Lead decision required before FR-CONV.1 implementation. | Engineering Lead | Pre-FR-CONV.1 implementation | 🔴 OPEN | Pending |
| OPEN-PR05 | When does `.dev/tasks/done/` reach ≥10-tasks-of-≥3-task_types threshold to re-evaluate PR-05? | Engineering Lead | Re-check each major release | 🟡 Tracked | Documented in KNOWLEDGE.md |
| OPEN-INV-006 | Empirical calibration of TB-Add-2 item-count bounds (≥3 / ≤40 track / ≤50 single-track) | Engineering | Phase-2 with PR-05 | 🔴 OPEN | TB-Add-2 stays `[ADVISORY]` until calibrated |
| OPEN-INV-017 | Historical-file staleness check for PR-05 advisory citations | Engineering | Resolve when PR-05 re-evaluated | 🟡 Deferred | Academic given PR-05 Phase-2 deferral |
| OPEN-INV-018 | If `.dev/tasks/` directory layout changes, all 7 proposals require re-integration | Engineering Lead | Per release | 🔴 OPEN | Document layout-change contract; re-integrate on demand |
| OPEN-X-002 | PR-04 anti-inflation operational test — "reliance ≠ verification" distinction empirically observable, not structurally provable | QA Lead | First 5 rf-qa-qualitative runs after FR-CONV.3 | 🔴 OPEN — K-003 audit-target | Audit per release-spec.md §8.3 row 4 |
| OPEN-TOKEN | NFR-CONV.4 token-ceiling empirical measurement | Engineering Lead | Post-merge | 🔴 OPEN | Measure on 5 representative BUILD_REQUESTs |
| Q-DM-2 | Should §19 Migration & Rollout enumerate per-FR rollback dependency matrix inline (recommendation: yes) or reference externally? | Tech Lead | Pre-implementation | 🟢 RESOLVED (per TDD §19.4) | Enumerate inline — TDD §19.4 |
| Q-DM-3 | Five Adversarial Axes canonical definitions: where should they live? | TDD authors | Pre-FR-CONV.4 land | 🟢 RESOLVED (per TDD §6.4 + §8.2 Contract 2) | Define in §8.2 Contract 2 per SC-3 |
| Q-DM-4 | Per-gate fix-cycle limits authority location (rf-task-builder.md I16 vs rf-qa.md global max) | Engineering | Pre-implementation | 🟢 RESOLVED (per TDD §6.4 + §12) | rf-task-builder.md I16 is authoritative; rf-qa.md max=3 is per-cycle global ceiling layered on top |

**Notes on Q-DM-1 (critical path blocker):**
- Surfaced as SC-1 [CRITICAL] in the Phase-3 research gate consolidated verdict; it is the single
  synthesis-blocking issue and cannot be resolved by re-spawning research agents.
- It is a PRD-vs-source contradiction, not a research gap — the research correctly identified it.
- Blocks FR-CONV.1 (PR-06) because TB-Add-8 (per-item Context `file:line` citation) and the
  Execution Context header negative criterion both reference the per-item schema. If the schema in
  SKILL.md is `{Context, Action, Output, Verification, Completion gate}` rather than the PRD-asserted
  `{Description, Context, Acceptance, Confidence, Verification}`, NFR-CONV.6 (self-contained-item
  preservation) acceptance criteria cannot be authored against a wrong baseline.
- Resolution options (TDD §7.1 Entity 4): (a) FR-CONV.1/TB-Add-8 LANDS the §25.4 schema — rejected,
  contradicts A-002 strictly-additive governance; (b) correct the PRD §25.4 pointer to the real
  operational source; (c) §25.4 describes a separate schema living in rf-task-builder.md B2 pattern
  (`:230-244`) or rf-qa.md guidance, not SKILL.md; (d) Engineering Lead decision required before
  implementation. Option (d) is the operative status until the Lead rules.

**Notes on Q-DM-4 (resolved within §12):**
- Per `research/06-rf-task-builder-encoding.md` §6 and SC-4: per-gate fix-cycle caps live in
  rf-task-builder.md I16 (`:352-358` — research-gate 3 / synthesis-gate 2 / report-validation 3 /
  task-integrity 2 / qualitative 3). rf-qa.md `:310-313` specifies only a global `max=3`.
- FR-CONV.5 monotonicity + regression halts layer ON TOP of these caps and trip earlier on
  pathological loops (`research/12-fr5-retry-monotonicity.md` §6 composition order).

---

## §23 Timeline & Milestones

### §23.1 High-Level Timeline

| Milestone | Target Date | Status | Dependencies |
|-----------|-------------|--------|--------------|
| Design Complete (this TDD approved) | 2026-05-21 | 🟡 In Review | Q-DM-1 Engineering Lead decision |
| Implementation Start | TBD post-Q-DM-1 | ⬜ | Design approval |
| FR-CONV.1 (PR-06) merge — M1.1 | TBD | ⬜ | Q-DM-1 decision; design approval |
| FR-CONV.2 (PR-01) merge — M1.2 | TBD | ⬜ | M1.1 PASS |
| FR-CONV.3 (PR-04) merge — M1.3 | TBD | ⬜ | M1.2 PASS |
| FR-CONV.4 (PR-07) merge — M1.4 | TBD | ⬜ | M1.3 PASS |
| FR-CONV.5 (PR-02) merge — M1.5 | TBD | ⬜ | M1.4 PASS |
| FR-CONV.6 (PR-03) merge — M1.6 | TBD | ⬜ | M1.5 PASS |
| K-003 audit (first 5 rf-qa-qualitative runs post-FR-CONV.3) | TBD post-M1.3 | ⬜ | M1.3 + 5 real runs |
| NFR-CONV.4 measurement (5 BUILD_REQUESTs) | TBD post-M1.6 | ⬜ | All 6 FRs landed |
| v3.9 GA | 2026-Q3 | ⬜ | All FRs + audit + measurement PASS |

**Sequencing note:** The merge order PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03 is the corrected
canonical order per SC-6 (`qa/research-gate-consolidated.md` line 47) and PRD §14.1 landing-order
fields. K-007 (PR-04 lands before PR-06) is explicitly mitigated by enforcing this serial chain in
the git log — verified in the §24.2 release checklist.

### §23.2 Implementation Phases

- **Phase 1 — Structural Gate Reinforcement:** FR-CONV.1 (PR-06) + FR-CONV.2 (PR-01).
  Establishes the TB-Add catalogue and Execution Context header. FR-CONV.2 depends on FR-CONV.1
  (TB-Add-7 cross-validation + TB-Add-8 scope-confinement test live first).
- **Phase 2 — Inter-Agent Verdict Channel:** FR-CONV.3 (PR-04) + FR-CONV.4 (PR-07).
  rf-qa → rf-qa-qualitative inherited verdict passthrough plus Five Adversarial Axes overlay.
- **Phase 3 — Retry & Exhaust Resilience:** FR-CONV.5 (PR-02) + FR-CONV.6 (PR-03 BASE).
  Retry monotonicity + regression halts and DNSP synthetic-finding emission. FR-CONV.5 ↔ FR-CONV.6
  share the INV-012 dedup-key composition contract (`research/12` §4).
- **Phase 4 — Post-merge Audit + Measurement:** K-003 audit (first 5 rf-qa-qualitative runs) and
  NFR-CONV.4 token-ceiling measurement. Neither is on the merge critical path; both gate v3.9 GA.

---

## §24 Release Criteria

### §24.1 Definition of Done (per-FR)

- [ ] All three Acceptance Criteria fields (Observable behavior / Verification method / Negative criterion) PASS on synthetic fixtures
- [ ] Unit tests per §15.2 catalogue written and passing
- [ ] Integration tests for cross-FR composition (INV-010 + INV-012 + INV-019) passing
- [ ] `make verify-sync` PASS (src/superclaude/ ↔ .claude/ in sync — A-001 discipline)
- [ ] Code reviewed by the relevant rf-* agent maintainer
- [ ] No invariant weakening — NFR-CONV.6..10 confirmed (self-contained-item, evidence-bound-item, persistent-`.dev/tasks/`-artifact, zero-trust QA, parallel-research)
- [ ] Per-FR rollback procedure documented in §19.4 dependency matrix
- [ ] No bundle-specific `/sc:tasklist` checks leaked in (FR-CONV.1 negative criterion)

### §24.2 Release Checklist

- [ ] All 6 FRs Done per §24.1
- [ ] No critical or high bugs open
- [ ] Q-DM-1 resolved (Engineering Lead decision on §25.4 schema contradiction landed before FR-CONV.1)
- [ ] K-003 audit PASS — first 5 rf-qa-qualitative runs after FR-CONV.3 show no inflation
- [ ] NFR-CONV.4 ≤1.10 token ratio on 5 representative BUILD_REQUESTs
- [ ] `make verify-sync` PASS after each FR merge (not just at the end)
- [ ] Strict serial sequencing PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03 visible in git log (K-007 mitigation)
- [ ] All 6 FRs co-revertable per the §19.4 rollback dependency matrix
- [ ] NFR-CONV.1 determinism spot-check: re-run task-builder on identical BUILD_REQUEST twice; structural fields byte-identical
- [ ] NFR-CONV.3 hidden-input guard: fixture-populated `.dev/tasks/done/` produces byte-identical structural output to empty

---

## §25 Operational Readiness

### §25.1 Runbook

| Scenario | Symptoms | Diagnosis Steps | Resolution | Escalation |
|----------|----------|-----------------|------------|------------|
| K-003 audit-target (first 5 rf-qa-qualitative runs post-FR-CONV.3) | rf-qa-qualitative output missing `## Self-Audit` section OR Self-Audit shows zero independent semantic checks | Read `.dev/tasks/to-do/TASK-*/reviews/qa-qualitative-review.md`; grep for `## Self-Audit`; verify ≥1 semantic check beyond inherited PASS | If missing: prompt FR-CONV.3 spawn-prompt; if zero independent checks: K-003 FAIL → disable passthrough flag (§19.2) | QA Lead immediate; Engineering Lead if pattern across all 5 runs |
| DNSP triage (synthetic-dnsp emission count >0 in production) | rf-qa report contains a `synthetic-dnsp` finding (HIGH severity) | Read affected partition's spawn-log (cited in `evidence` field); identify root cause of escalation-ladder exhaust; check `dedup_key` for prior similar events | Manual investigation per `recommendation` field; consider whether root cause should land as a new TB-Add | rf-qa maintainer; escalate to Engineering if ≥3 distinct dedup-keys in a week |
| All-partitions-exhaust HALT (no DNSP emitted) | rf-team-lead HALTs and asks user; zero partitions succeeded | Confirm zero partition successes in spawn-log; verify line-417 escalation path fired and NO synthetic-dnsp was emitted (correct per FR-CONV.6 mutual-exclusivity) | This is the preserved all-agents-fail guard, not a defect — user resolves unresolved findings before re-run | rf-team-lead maintainer if HALT misfires when ≥1 partition succeeded |
| `[HALT-MONOTONICITY]` rate >50% of fix-cycle batches | Many fix-loops halting before convergence with `[HALT-MONOTONICITY] \|F\|=<n>` | Sample 3 halt events; inspect BUILD_REQUESTs for upstream defects (vague requirements, missing context); inspect generated MDTM for structural issues | Improve upstream BUILD_REQUESTs; consider per-FR TB-Add-2 calibration (OPEN-INV-006) | rf-task-builder maintainer |
| Regression-halt rate >20% of fix-cycle batches | Many fix-cycles emitting the verbatim regression halt message (`Regression detected on Item X.Y...`) | Sample 3 regression events; inspect what changed between cycles (new FAIL items vs previously PASS); look for fix-cycle pattern introducing collateral damage | Tighten fix-cycle prompts; consider whether monotonicity should regress to slower threshold (note: X-003 slow-convergence threshold was REJECTED) | Engineering Lead |
| `make verify-sync` FAIL post-FR-merge | Sync verification fails between `src/superclaude/` and `.claude/` | Re-run `make sync-dev`; check git status for unsynced changes; verify CLAUDE.md sync-discipline rule (A-001) followed | Re-sync; commit only on PASS; if persistent, revert the direct `.claude/` edit and re-run from `src/superclaude/` (K-009 contingency) | Per-commit author |
| INV-018 layout change detected (K-008) | `.dev/tasks/` directory schema differs from pre-merge | Inspect all 7 FRs for path/naming references; re-integrate at the new layout | Re-integration commit covering all 6 FRs per the §19.4 dependency matrix | Engineering Lead + orchestrator |

### §25.2 On-Call Expectations

| Aspect | Detail |
|--------|--------|
| On-call team | task-builder maintainers (rotating) |
| Expected page volume | <2 pages / week at steady state (most operations are batch / async) |
| Required response time | K-003 audit failure: 4 business hours; DNSP triage: 24 hours; `make verify-sync` FAIL: immediate |
| Knowledge prerequisites | task-builder skill v3.9 architecture (this TDD); rf-qa.md / rf-qa-qualitative.md gate semantics; rf-team-lead.md:417 escalation ladder; sync workflow per CLAUDE.md (A-001) |

### §25.3 Capacity Planning

N/A — internal skill with no infrastructure scaling. All gate additions are local checks (Read,
Grep, Glob, Bash); NFR-CONV.5 forbids new external dependencies or synchronous network calls.

---

## §26 Cost & Resource Estimation

### §26.1 Infrastructure Costs

N/A — no infrastructure deployed. task-builder v3.9 is a skill + agent definition change only.

### §26.2 LLM Token Costs

Per NFR-CONV.4, target is ≤10% token-cost increase over the pre-merge task-builder baseline per
equivalent BUILD_REQUEST (ratio ≤1.10). Measured post-merge on 5 representative BUILD_REQUESTs
(OPEN-TOKEN). Per-FR estimates below are pre-measurement projections.

| Cost driver | Pre-merge baseline | Post-merge target | Notes |
|-------------|--------------------|--------------------|-------|
| Per-FR token cost increase (aggregate) | Baseline | ≤10% total | Distributed across all 6 FRs |
| FR-CONV.3 verdict block (largest single addition) | 0 | ~1-3% per run | `## Inherited Structural Verdict` table verbatim; can be summarised if token ceiling exceeded (rollback per §19.4) |
| FR-CONV.4 axis annotations | 0 | <1% per run | Small text addition — Five Adversarial Axes header + `axis` column |
| FR-CONV.1 TB-Add catalogue | 0 | <2% per run | 8 structural checks appended to rf-qa checklist |
| FR-CONV.2 Execution Context header | 0 | <1% per run | Three-line block per generated MDTM file |
| FR-CONV.5 / FR-CONV.6 (retry + DNSP) | 0 | <2% per run | Halt messages + synthetic-dnsp 5-field findings — only emitted on pathological paths |

### §26.3 Cost Optimization Opportunities

| Opportunity | Estimated Savings | Effort | Priority |
|-------------|-------------------|--------|----------|
| FR-CONV.3 verdict-table summarisation (if NFR-CONV.4 exceeded) | 1-3% per run | Low | Medium (only if token ceiling hit; K-010 contingency) |
| Per-FR rollback of high-cost FRs | Up to 10% per FR | Low | High (granular co-revertable rollback per §19.4 dependency matrix) |

---

## Synthesis Complete

§22-§26 authored. Q-DM-1 (SC-1 critical PRD-vs-source schema contradiction) is recorded as a
🔴 OPEN §22 item with Engineering-Lead owner and a pre-FR-CONV.1 target date — it is the single
critical-path blocker for the release. §19.4 rollback dependency matrix is referenced in §24.2
(co-revertability checklist), §25.1 (INV-018 re-integration runbook row), and §26.3 (per-FR
rollback optimization). All timeline dependencies chain off the corrected SC-6 merge order
PR-06 → PR-01 → PR-04 → PR-07 → PR-02 → PR-03.
