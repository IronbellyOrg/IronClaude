---
complexity_class: HIGH
validation_philosophy: continuous-parallel
validation_milestones: 6
work_milestones: 6
interleave_ratio: "1:1"
major_issue_policy: stop-and-fix
spec_source: TDD_TASK_BUILDER_CONVERGENCE.md
generated: "2026-05-15T06:05:10.479629+00:00"
generator: superclaude-roadmap-executor
---

# Test Strategy — Task-Builder Convergence v3.9

## 1. Validation Milestones Mapped to Roadmap Milestones

**V1: Foundation Contracts Validation** | 1 week | Validates M1 contracts before any FR implementation
**V2: Structural Gate Validation (PR-06)** | 1 week | Validates M2 FR-CONV.1 TB-Add-1..8 catalogue
**V3: Execution Context Header Validation (PR-01)** | 0.5 week | Validates M3 FR-CONV.2 header emission + degradation
**V4: Inter-Agent Verdict Channel Validation (PR-04/PR-07)** | 1 week | Validates M4 FR-CONV.3 passthrough + FR-CONV.4 5-axis overlay
**V5: Retry Resilience & DNSP Validation (PR-02/PR-03)** | 1 week | Validates M5 FR-CONV.5 monotonicity + FR-CONV.6 DNSP composition
**V6: Hardening & GA Audit Validation** | 12 weeks (calendar-bound) | Validates M6 K-003 audit + NFR-CONV.4 + REL-001 GA gate

**Validation milestones interleave 1:1 with work milestones** (HIGH complexity requirement). Each Vn runs concurrently with Mn implementation and gates progression to M(n+1).

## 2. Test Categories

| Category | Tooling | Coverage Target | Notes |
|---|---|---|---|
| **Unit (Synthetic Fixtures)** | `uv run pytest` (per CLAUDE.md UV-only rule); 25 fixtures TEST-001..TEST-025 from TDD §15.2 | 100% AC coverage per FR | Each FR-CONV.X AC has ≥1 fixture; fixtures are markdown input + grep/byte-diff assertion |
| **Integration (Cross-FR Composition)** | Custom multi-FR fixtures | INV-010 + INV-012 + INV-013 + INV-019 composition paths | TEST-022 (FR-CONV.5↔6 dedup), TEST-024 (PR-06↔PR-04 sequencing), TEST-025 (composite NFR-CONV.6..10) |
| **E2E (Pipeline)** | Realistic BUILD_REQUEST through A.1–A.11 | 5 representative BUILD_REQUESTs (Quick/Standard/Deep tiers) | Drives NFR-CONV.4 token measurement |
| **Acceptance (Persona-driven)** | Per persona §7 PRD | rf-task-builder, rf-qa, rf-qa-qualitative workflow validation | Maps to JTBD coverage (Job 1→FR-CONV.1/2; Job 2→FR-CONV.3/4; Job 3→FR-CONV.5/6) |
| **Contract (API-001..API-005)** | Spawn-prompt + report artifact validation | Per-contract schema validation (DM-001..DM-005) | Verbatim string matching for halt messages, fixed-value fields (wire ABI) |
| **Data Model (Schema)** | YAML/markdown structure validation | DM-001..DM-005 field-type + constraint validation | Q-DM-1 schema target validation gated by Engineering Lead decision |
| **Operational Readiness** | OPS-001..OPS-007 runbooks | Counter/gauge metric emission to `docs/generated/metrics/` | grep-based offline metric extraction |
| **Manual Audit** | Human review by QA Lead | K-003 first-5-runs Self-Audit coverage | INV-019 operational compliance; 4-hour response SLA |
| **Determinism** | Two-run byte-diff of structural fields | NFR-CONV.1 byte-equal; NFR-CONV.2 prose excluded | Re-run task-builder on identical BUILD_REQUEST |
| **Hidden-Input Guard** | TEST-023 (`test_hidden_input_guard`) | NFR-CONV.3 byte-equality across empty/populated `.dev/tasks/done/` | Behavior-modifying hidden input forbidden |
| **Invariant Preservation** | TEST-025 composite + per-NFR fixtures | NFR-CONV.6..10 all PASS | Self-contained-item, evidence-bound-item, persistent-artifact, zero-trust QA, parallel-research |

## 3. Test-Implementation Interleaving Strategy

**Ratio: 1:1 (HIGH complexity)** — one validation milestone per work milestone, justified by:
- 6 FRs with mutual dependencies (FR-CONV.5↔FR-CONV.6) require validation gate between landings to prevent cascading defects
- 5 load-bearing invariants must be provably preserved at every FR landing (NFR-CONV.6..10)
- One CRITICAL unresolved schema contradiction (SC-1/Q-DM-1) gates all downstream work
- Strict serial landing order (PR-06→PR-01→PR-04→PR-07→PR-02→PR-03) — early defect detection prevents portfolio-wide rework (K-008)
- Anti-inflation rule (rf-qa-qualitative.md:766-775) byte-stability requires CI-enforced verification at each commit
- Halt-message verbatim strings are wire-ABI (TDD §8.4) — drift detection must be immediate

**Interleaving pattern per milestone:**
1. Implementation begins at Mn entry
2. Vn fixtures authored in parallel during Mn (TDD-style)
3. Vn gate runs at Mn exit before M(n+1) can begin
4. CRITICAL/MAJOR failures halt progress; MINOR/COSMETIC tracked

## 4. Risk-Based Test Prioritization

**Priority 0 (CRITICAL — Block Progression):**
- Q-DM-1 schema resolution validation (V1) — blocks all FRs
- NFR-CONV.6..10 invariant preservation (V2-V5) — load-bearing
- K-003 inflation detection (V4, V6 audit) — first 5 runs MUST show Self-Audit
- K-008 INV-018 layout change detection (V1-V6 continuous) — portfolio-wide blast radius
- K-009 sync-discipline (`make verify-sync` PASS per commit) — A-001 contract
- Halt-message verbatim string drift (V5) — wire ABI

**Priority 1 (MAJOR — Block Next Milestone):**
- TB-Add false-positive rate (V2, V6)
- FR-CONV.6 all-agents-fail guard bypass (V5)
- INV-012 cross-cycle dedup false-regression (V5)
- TEST-016/TEST-015 ordering precedence (regression > monotonicity)
- Anti-inflation rule byte-stability (V4 byte-diff CI gate)

**Priority 2 (MINOR — Track, fix next sprint):**
- TB-Add-2 advisory calibration accuracy (V2, deferred to Phase-2)
- 5-axis annotation false-positive over-flagging (V4 — K-004)
- Hidden-input contamination (NFR-CONV.3 — guarded by TEST-023)

**Priority 3 (COSMETIC — Backlog):**
- Per-cycle log formatting consistency
- Metric histogram emission verbosity

## 5. Acceptance Criteria per Milestone

**M1 / V1:** Q-DM-1 RESOLVED with Engineering Lead decision; DM-001..DM-005 schema-validation fixtures PASS; API-001..API-005 contract fixtures PASS; INV-002/010/012/015/019/021 negative-criterion fixtures authored and runnable; `make verify-sync` PASS; conflict-register validated (5 CASE-D rows present); GOV-1 axes vocabulary locked; GOV-3 pre-commit guard operational.

**M2 / V2:** TEST-001 (TB-Add-1 placeholder), TEST-002 (TB-Add-4 DAG), TEST-003 (TB-Add-8 evidence-binding) PASS; 6 NFR-CONV.6/7 reinforcement fixtures PASS; rf-qa.md:268-287 + SKILL.md:~898-906 + SKILL.md:~1491-1507 grep ≥3 hits per TB-Add ID; NFR-CONV.1 determinism spot-check PASS; bundle-specific check leak audit PASS.

**M3 / V3:** TEST-004 (header full), TEST-005 (References-only degradation), TEST-006 (no file paths in header) PASS; NFR-CONV.3 hidden-input guard PASS; NFR-CONV.7 reinforcement (per-item Context retains file:line) PASS; TB-Add-7 cross-validation fires correctly on header source-areas drift.

**M4 / V4:** TEST-007..TEST-010 (FR-CONV.3 verdict block + freshness + Self-Audit + dynamic enumeration) PASS; TEST-011..TEST-014 (FR-CONV.4 axes overlay + column populated + drift-axis-inactive + severity floor unweakened) PASS; rf-qa-qualitative.md:766-775 byte-diff CI gate PASS; K-003 audit-target activated (first-5-runs window opens); INV-013 composition (axes apply to items NOT in inherited PASS) PASS.

**M5 / V5:** TEST-015 (monotonicity halt `|F|=5,5,5`), TEST-016 (regression halt PASS@1/FAIL@2 ordering), TEST-017 (slow-shrink continues) PASS; TEST-018..TEST-021 (DNSP twice-exhaust + dedup collapse + all-agents-fail bypass + no-cohort-serialization) PASS; TEST-022 (synthetic-dnsp dedup NOT regression) PASS; halt-message verbatim string validation PASS; rf-team-lead.md:417 NO DRIFT verified.

**M6 / V6:** TEST-023 (hidden-input guard), TEST-024 (PR-06↔PR-04 sequencing), TEST-025 (composite NFR-CONV.6..10) PASS; K-003 audit on first 5 real rf-qa-qualitative runs = 100% Self-Audit coverage; NFR-CONV.4 ≤1.10 token ratio measured on 5 representative BUILD_REQUESTs across Quick/Standard/Deep tiers; SC-001 ≥80% single-pass; SC-002 100% placeholder + DAG detection; SC-003 100% Self-Audit; SC-004 monotonicity <10% / regression <5% / DNSP=0 on healthy runs; OPS-001..OPS-007 runbooks operational; REL-001 GA readiness gate PASS.

## 6. Quality Gates Between Milestones

| Gate | Entry From | Exit To | Blocking Conditions | Action on Failure |
|---|---|---|---|---|
| **G1** | M1 complete | M2 start | Q-DM-1 unresolved; DM-001..005 not locked; `make verify-sync` FAIL; CASE-D rows missing | stop-and-fix CRITICAL; Engineering Lead decision required |
| **G2** | M2 complete | M3 start | TEST-001..003 FAIL; bundle-specific leak detected; rf-qa.md:141-142 byte-drift; `make verify-sync` FAIL | stop-and-fix MAJOR; revert specific TB-Add line if false-positive |
| **G3** | M3 complete | M4 start | TEST-004..006 FAIL; grep finds file paths in header; per-item Context regression; NFR-CONV.3 hidden-input fails | stop-and-fix MAJOR; degrade header to References-only |
| **G4** | M4 complete | M5 start | TEST-007..014 FAIL; rf-qa-qualitative.md:766-775 byte-drift; K-003 audit shows inflation; severity floor at :786-795 weakened | stop-and-fix MAJOR; co-revert FR-CONV.3+FR-CONV.1 per §19.4 |
| **G5** | M5 complete | M6 start | TEST-015..022 FAIL; halt-message string drift; rf-team-lead.md:417 modified; all-agents-fail bypass broken | stop-and-fix MAJOR; jointly revert FR-CONV.5+FR-CONV.6 |
| **G6** | M6 audit complete | v3.9 GA | NFR-CONV.4 >1.10; K-003 <100% on first 5 runs; SC-001..004 missing target; any HIGH/CRITICAL bug open; serial order not visible in git log | stop-and-fix CRITICAL; activate K-010 (verdict-table summarisation) or rollback per §19.4 |

**Gate enforcement:** All gates run via `uv run pytest` + `make verify-sync` in CI. CRITICAL/MAJOR failures halt the pipeline; the next milestone cannot begin until the failure class is resolved or the affected FR is reverted per the §19.4 co-revert matrix. MINOR/COSMETIC findings logged to `docs/mistakes/` and tracked into next sprint without gate impact.
