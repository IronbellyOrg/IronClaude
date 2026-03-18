# Final Ranking — Unified Audit Gating v1.2.1 Proposals

**Date**: 2026-03-17
**Phase**: D — Post-Debate Synthesis
**Input**: 5 proposals × 3-round adversarial debates scored against the standardized scoring framework
**Reference incident**: cli-portify executor no-op bug — shipped across v2.24, v2.24.1, v2.25

---

## Executive Summary

All five proposals address real and distinct failure modes identified in the forensic investigation.
None scored in Tier 1 (≥7.5) in isolation; the highest scored 7.30. This reflects a genuine
architectural finding: **no single proposal fully closes the gap**. The combination of Proposals
05 + 04 + 02 (D-03/D-04 only) achieves Tier 1 coverage at Tier 2 cost.

The composite picture:
- **Fastest to ship**: Proposal 05 (Silent Success Detection) — 6.5 days, no spec dependencies
- **Highest catch rate**: Proposal 04 (Smoke Test Gate) — 10/10, fires on timing + artifact + content
- **Best architectural investment**: Proposal 02 (D-03/D-04 subset) — prevents Link 1 rot at the source
- **Most complex**: Proposals 01 and 03 — subsystem-level builds; defer until core system stable

---

## Ranked Results

### Rank 1 — Proposal 05: Silent Success Detection

**Composite Score: 7.30** | Tier 2 (top of band, 0.20 below Tier 1 boundary)

| Axis | Score | Weight | Weighted |
|------|-------|--------|---------|
| Catch Rate | 9 | 25% | 2.25 |
| Generalizability | 7 | 25% | 1.75 |
| Implementation Complexity (inv.) | 6 | 20% | 1.20 |
| False Positive Risk (inv.) | 7 | 15% | 1.05 |
| Integration Fit | 7 | 15% | 1.05 |
| **Composite** | | | **7.30** |

**Why it ranks first**: The only proposal that detects the bug at runtime in any execution environment,
not just in CI or pre-release gates. The SilentSuccessDetector is purely observational — 8 additive
lines in `_execute_step()` — and requires no prerequisite infrastructure. The debate confirmed it
produces a deterministic 1.0 suspicion score against the exact no-op run. Generalizability to the
sprint executor covers two additional "defined but not wired" instances from the forensic report.

**Debate adjustment from proposal self-score**: Proposal scored itself 7.70; debate adjusted to 7.30.
Gap driven by: (a) pre-existing artifact false-negative (FN2) in environments without clean output
directory hygiene, (b) S2 timing threshold has no documented calibration methodology.

**Adoption condition**: Deploy Phase 1 immediately without waiting for Proposals 03 or 04. Three
conditions before full release: Phase 1 deployment, S2 calibration protocol, Phase 2 GateResult
integration.

**Top failure conditions**:
1. Pre-existing artifacts from a prior real run cause S1+S3 to pass while S2 is marginal — composite
   stays below soft-fail threshold, producing a false negative
2. S2 timing thresholds become stale over 12–24 months as infrastructure improves; no recalibration
   protocol specified

---

### Rank 2 — Proposal 04: Smoke Test Gate

**Composite Score: 7.05** | Tier 2

| Axis | Score | Weight | Weighted |
|------|-------|--------|---------|
| Catch Rate | 10 | 25% | 2.50 |
| Generalizability | 7 | 25% | 1.75 |
| Implementation Complexity (inv.) | 5 | 20% | 1.00 |
| False Positive Risk (inv.) | 6 | 15% | 0.90 |
| Integration Fit | 6 | 15% | 0.90 |
| **Composite** | | | **7.05** |

**Why it ranks second**: Perfect 10/10 catch rate — the only proposal scoring 10. The timing check
(sub-5-second execution of 12 steps), artifact absence check, and content evidence check each
independently fire against the known no-op. This is the most direct possible test: run the pipeline,
check the result.

**Critical debate finding**: The timing check should be demoted from BLOCKING to WARN. The
artifact-absence check is the gate's primary mechanism and is immune to fast-CI false positives.
Shipping without this demotion creates a systematic false positive class in constrained CI
environments.

**Critical prerequisite**: The proposal explicitly requires Defect 1 (step_runner wiring) and
Defect 2 (validation call) to be fixed before the gate can pass a legitimate run. This makes it a
regression guard, not a preventive gate. It would not have caught the bug proactively — only
after it was fixed, to prevent its reintroduction.

**Complementarity with Proposal 05**: These are the most complementary pairing. Proposal 05 catches
bugs in any production run; Proposal 04 catches them in CI before any production run. Correct
layering: both should be adopted.

**Top failure conditions**:
1. CI API dependency creates permanent `transient` failures in network-restricted environments —
   must ship `--mock-llm` mode before CI integration
2. Fixture drift causes real runs to fail content evidence checks — `test_fixture_content_matches_gate_patterns`
   unit test must ship on day one

---

### Rank 3 (tie) — Proposal 02: Spec Fidelity Gate Hardening

**Composite Score: 6.55** | Tier 2

| Axis | Score | Weight | Weighted |
|------|-------|--------|---------|
| Catch Rate | 7 | 25% | 1.75 |
| Generalizability | 6 | 25% | 1.50 |
| Implementation Complexity (inv.) | 6 | 20% | 1.20 |
| False Positive Risk (inv.) | 6 | 15% | 0.90 |
| Integration Fit | 8 | 15% | 1.20 |
| **Composite** | | | **6.55** |

**Why it ranks here**: The only proposal that operates at the source — preventing the roadmap from
silently dropping spec requirements. D-03 (named dispatch table preservation) and D-04 (pseudocode
dispatch function name preservation) would each independently have caught the cli-portify roadmap
dropping `PROGRAMMATIC_RUNNERS` and `_run_programmatic_step`. Integration fit is the highest of any
proposal (8/10) because it directly extends the existing `GateCriteria`/`SemanticCheck` pattern.

**Critical debate finding**: D-01 (FR-NNN identifier coverage) is not load-bearing — cli-portify
specs used prose and pseudocode, not formal FR-NNN identifiers. D-01 would have vacuously passed.
D-05 (stub sentinel detection) has systematic false positives in TDD workflows without section-scope
filtering. **Adopt D-03 + D-04 only in Phase 2a (~6 hours); defer D-05 to Phase 2b after
section-scope filtering is added.**

**Top failure conditions**:
1. D-05 ships without section-scope filtering, causing TDD-phase false positives that erode gate
   trust and lead to suppression
2. D-03/D-04 pattern matching is too narrow — only catches exact string matches, misses
   semantically equivalent implementations with different naming

---

### Rank 3 (tie) — Proposal 03: Code Integration Gate

**Composite Score: 6.55** | Tier 2

| Axis | Score | Weight | Weighted |
|------|-------|--------|---------|
| Catch Rate | 9 | 25% | 2.25 |
| Generalizability | 7 | 25% | 1.75 |
| Implementation Complexity (inv.) | 3 | 20% | 0.60 |
| False Positive Risk (inv.) | 6 | 15% | 0.90 |
| Integration Fit | 7 | 15% | 1.05 |
| **Composite** | | | **6.55** |

**Why it ranks here**: Highest potential catch rate (9/10) via three independent checks that fire
deterministically — but the implementation complexity (3/10 inverted = most complex) drags it to a
tie with Proposal 02. NOPF would have directly fingerprinted `executor.py:397-399`; CPC would have
caught `step_runner` never being passed. Both are non-LLM-dependent.

**Critical debate finding**: The 5-day MVP claim is partially undermined — Stage 1 (NOPF+CPC)
alone catches only the archetypal bug pattern. Coverage of the other two known instances
(DEVIATION_ANALYSIS_GATE, SprintGatePolicy) requires the full 15-day Stage 1-4 suite. NOPF
heuristic staleness is a high-probability failure mode over 24 months.

**Adoption path**: Ship NOPF+CPC in conjunction mode as standalone CI tooling (5 days) to capture
immediate value. Full 4-check suite deferred to after Proposals 05 and 04 are stable.

**Top failure conditions**:
1. CPC false positives on dependency injection patterns erode gate signal, leading to suppression
2. NOPF heuristic becomes stale after code refactoring (variable renaming, enum adoption) — the
   exact bug pattern changes form but the gate doesn't follow

---

### Rank 5 — Proposal 01: Link 3 Code Fidelity Gate

**Composite Score: 6.30** | Tier 2

| Axis | Score | Weight | Weighted |
|------|-------|--------|---------|
| Catch Rate | 8 | 25% | 2.00 |
| Generalizability | 7 | 25% | 1.75 |
| Implementation Complexity (inv.) | 3 | 20% | 0.60 |
| False Positive Risk (inv.) | 6 | 15% | 0.90 |
| Integration Fit | 7 | 15% | 1.05 |
| **Composite** | | | **6.30** |

**Why it ranks last**: The most architecturally complete proposal — it closes the structural gap
that allowed the bug to exist (no Link 3 gate). But the debate exposed a critical circular problem:
the gate only fires if tasklist acceptance criteria contain WIRING assertions, and the v2.25 tasklist
didn't require dispatch wiring. Shipping Link 3 without also fixing tasklist generation practices
produces a gate that always passes — the same failure mode it was built to detect.

**Critical debate finding**: The gate is conditional on Phase 3 (tasklist generator changes) having
shipped. Without WIRING assertions in the phase file, Phase A has nothing to scan. This creates
a 9-file, 1,055-line subsystem with a hard dependency chain before it provides any value.

**Key redeeming value**: The `noop_detector.py` component (Phase 1, standalone) can be extracted
and shipped as CI tooling immediately — independent of the full Link 3 system. This is the
fastest-value extraction path.

**Top failure conditions**:
1. Phase 3 (tasklist generator changes) is deprioritized — the gate ships as infrastructure that
   fires on nothing, providing false confidence
2. Acceptance criteria use behavioral-only assertions that pass no-op implementations (same failure
   mode as the original v2.25 tasklist)

---

## Composite Scores Summary

| Rank | Proposal | Score | Tier | Catch Rate | Complexity (inv.) |
|------|----------|-------|------|------------|-------------------|
| 1 | 05 — Silent Success Detection | **7.30** | Tier 2 | 9 | 6 |
| 2 | 04 — Smoke Test Gate | **7.05** | Tier 2 | 10 | 5 |
| 3= | 02 — Spec Fidelity Hardening | **6.55** | Tier 2 | 7 | 6 |
| 3= | 03 — Code Integration Gate | **6.55** | Tier 2 | 9 | 3 |
| 5 | 01 — Link3 Code Fidelity | **6.30** | Tier 2 | 8 | 3 |

---

## Top Recommendation

**Implement Proposal 05 (Silent Success Detection) first, then Proposal 04 (Smoke Test Gate).**

These two proposals are complementary, not redundant:
- Proposal 05 catches the bug at **execution time** in any environment — production, developer
  laptop, CI — as soon as a run is attempted
- Proposal 04 catches the bug at **release time** in CI — requires the pipeline to be invoked
  against a real fixture with real LLM calls

Combined, they provide defense-in-depth: if a developer runs `superclaude cli-portify run` with the
no-op still present, Proposal 05 raises the alarm immediately. If somehow that run was skipped,
Proposal 04 blocks the release gate.

**Why not Proposal 03 or 01 first?** Both require 15+ days of implementation, have higher false
positive risk under normal workflows, and provide no value until their full suite is complete. The
5-day MVP of Proposal 03 (NOPF+CPC) is worth extracting as a parallel workstream, but should not
block the faster-value proposals.

**Why not Proposal 02 first?** D-03/D-04 are valuable and should ship in Phase 2, but they only
prevent future incidents at the spec→roadmap link. They do nothing for already-coded no-ops.

---

## Implementation Sequence Recommendation

### Wave 1 — Immediate (weeks 1–2)
**Proposal 05**: Deploy `SilentSuccessDetector` as a post-execution hook in `executor.run()`.
No spec infrastructure dependency. Provides runtime protection for all future cli-portify runs.

- New module: `src/superclaude/cli/cli_portify/silent_success.py` (~300 lines)
- Additive changes: `executor.py` (+20 lines), `models.py` (+10 lines)
- Prerequisite: Bug Fixes 1 and 2 (wire step_runner, add validate_portify_config call) must land first
- Also extract `noop_detector.py` from Proposal 01 as standalone CI tooling (value in parallel)

### Wave 2 — Phase 2 (weeks 3–5)
**Proposal 04**: Build smoke test gate G-012 at release tier.

- New files: `gates.py` extension, `tests/fixtures/cli_portify/smoke/`, `smoke_gate.py` (~400 lines)
- Must ship `--mock-llm` mode before CI integration
- Gate timing check demoted to WARN; artifact-absence check is primary BLOCKING mechanism
- Prerequisite: Bug Fixes 1 and 2 must be in production (gate is a regression guard)

**Proposal 02 (D-03 + D-04 only)**: Add two semantic check functions to `SPEC_FIDELITY_GATE`.

- New helper: `roadmap/fidelity_inventory.py` (~150 lines)
- Gate modifications: `roadmap/gates.py` (~80 lines)
- Estimated effort: ~6 hours, independently deployable
- D-05 deferred: add section-scope filtering before shipping

### Wave 3 — Phase 3 (weeks 6–10, after Wave 1+2 stable)
**Proposal 03 (NOPF + CPC conjunction mode)**: Static analysis gate for no-op fallbacks and
unwired optional callables.

- New module: `audit/code_integration.py` (~500 lines)
- Integration with existing `audit/dead_code.py` infrastructure
- Ship in conjunction mode (both checks must fire for ERROR) to minimize false positives

### Wave 4 — Phase 4 (deferred, after Wave 3 validated)
**Proposal 01 (full Link 3)**: Tasklist→Code fidelity gate.

- Depends on: Phase 3 tasklist generator changes (`sc-tasklist-protocol/SKILL.md` audit metadata)
- 9 files, ~1,055 lines
- Value unlocks only after tasklist generator ships WIRING assertion type

---

## Systemic Finding

The forensic investigation and these five proposals converge on a single architectural insight:

> **The existing gate system validates documents. The bug class requires validating behavior.**

Document gates (SPEC_FIDELITY_GATE, TASKLIST_FIDELITY_GATE, G-000 through G-011) are correct and
valuable for their domain. They cannot detect:
- Code that compiles and runs but does nothing
- Registries that have entries but no implementations
- Constructors with optional injectable dependencies that are never injected in production

The proposals address this gap at four different detection points:
1. **At spec time** (Proposal 02): prevent the roadmap from dropping dispatch requirements
2. **At code time** (Proposal 03): detect unwired components via static analysis
3. **At execution time** (Proposal 05): detect no-op runs by observing behavior
4. **At release time** (Proposal 04): detect no-op pipelines by running real fixtures

A mature gating system needs all four layers. The recommended sequence builds them in order of
implementation cost, starting with the fastest value.

---

## Artifacts Index

| File | Type | Status |
|------|------|--------|
| `proposals/scoring-framework.md` | Framework | Complete |
| `proposals/proposal-01-link3-code-fidelity.md` | Proposal | Complete |
| `proposals/proposal-02-spec-fidelity-hardening.md` | Proposal | Complete |
| `proposals/proposal-03-code-integration-gate.md` | Proposal | Complete |
| `proposals/proposal-04-smoke-test-gate.md` | Proposal | Complete |
| `proposals/proposal-05-silent-success-detection.md` | Proposal | Complete |
| `proposals/debate-01-link3-code-fidelity.md` | Debate | Complete |
| `proposals/debate-02-spec-fidelity-hardening.md` | Debate | Complete |
| `proposals/debate-03-code-integration-gate.md` | Debate | Complete |
| `proposals/debate-04-smoke-test-gate.md` | Debate | Complete |
| `proposals/debate-05-silent-success-detection.md` | Debate | Complete |
| `proposals/final-ranking.md` | This document | Complete |
