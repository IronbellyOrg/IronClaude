# Spec-Panel Review — Troubleshoot Pipeline Hardening

## Metadata

- **Reviewed**: `troubleshoot-pipeline-hardening-spec.md` (draft) → produced `troubleshoot-pipeline-hardening-RELEASE-SPEC.md`
- **Panel**: 11 experts (Wiegers, Adzic, Cockburn, Fowler, Nygard, Whittaker, Newman, Hohpe, Crispin, Gregory, Hightower)
- **Mode**: critique · **Focus**: correctness (auto-activated) · **Iterations**: 2 · **Format**: detailed
- **Date**: 2026-06-10
- **Output spec type**: infrastructure (release-spec-template format)

## Quality Assessment (0–10)

| Dimension | Source draft | Improved release-spec | Delta |
|-----------|-------------:|----------------------:|------:|
| Clarity | 7.0 | 8.5 | +1.5 |
| Completeness | 6.0 | 8.0 | +2.0 |
| Testability | 4.5 | 8.5 | +4.0 |
| Consistency | 6.5 | 8.0 | +1.5 |
| **Overall** | **6.0** | **8.2** | **+2.2** |

Largest gain is **testability**: the draft's prose waves became 13 atomic, verifiable FRs with acceptance criteria and mapped unit tests.

## Critical Issues (consolidated)

| # | Severity | Expert | Issue | Resolution in release-spec |
|---|----------|--------|-------|----------------------------|
| 1 | CRITICAL | Whittaker (F-S1) | No-re-greening was prose, bound to no variable, no guard | FR-12 + SV `waiver_status` one-way latch + NFR-4 test |
| 2 | CRITICAL | Nygard (F-N3) | H2 empty ledger passes vacuously | FR-5: empty/zero-row ledger = FAIL |
| 3 | CRITICAL | Whittaker (F-D1) | H4 missed non-empty-wrong-surface (real E5) | FR-10: fail closed unless surface-correctness proven |
| 4 | CRITICAL | Whittaker (F-SC1) | E2 word-boundary rule only in appendix | FR-8: word-boundary rule promoted to blocking + near-miss fixtures |
| 5 | CRITICAL | Whittaker (F-A1) | `known_escapes_caught` accepted un-earned membership | FR-12 anti-inflation: each ID needs a cited passing card |
| 6 | CRITICAL | Wiegers | Waves were prose, not SMART FRs | §3: FR-1..FR-13 with acceptance criteria |
| 7 | CRITICAL | Newman | Output contract unversioned | FR-13: `contract_version` + NFR-6 backward-compat |
| 8 | CRITICAL | Hohpe | Verdict→REPORT→downstream one-directional; no-re-green only prose | FR-12/FR-13 integration FRs |
| 9 | CRITICAL | Hightower | Waived probe not observably distinct from passed | FR-12 pipeline-health FAIL on absent probe |

Plus 10 MAJOR + 16 GAP rows from the Guard Boundary Table (each → a specified behavior in the release-spec; see `guard-boundary-table.md`).

## Quantity Flow — CRITICAL dimensional mismatches

Unifying defect: **gates measured the *enumerated/present* count and assumed it equalled the *true* count.**

- DIV-2 (H2): `N_enum=0 ⇒ unclassified=0 ⇒ PASS`, but `N_true=2` (E4: `gate_passed` + `_evaluate_gate`). → FR-5 empty-ledger FAIL.
- DIV-3 (H3): E2-fix unmasks 4 sibling `Findings` headings; sweep covers 1 → 3 escape (E3). → FR-9 full-family sweep.
- DIV-4 (H4): selector resolves to 5 commits, `|E ∩ true_surface|=0` (E5). → FR-10 surface-correctness.

## Expert Consensus

- The draft's mechanism-based direction is **sound and externally corroborated** (Appendix A of the merged report), but it shipped as prose and was therefore unverifiable and gameable.
- The single most important hardening is the **anti-theatre waiver/no-re-greening invariant** — and it was the weakest part of the draft. It is now FR-12 + a state-latched variable, but its *mechanical cross-stage enforcement* remains an open question (OI-1).
- "Predicted coverage" must stay `advisory` until an E1–E5 backtest runs post-build (NFR-1, §7 risk).

## Iteration Log

- **Iteration 1 (structural/critical)**: atomized waves → FR-1..13; added the versioned output contract (FR-13); added the State Variable Registry as the data model (§4.5); fixed the 9 CRITICALs above; established the canonical wave-numbering crosswalk (kills the 4th-scheme collision).
- **Iteration 2 (detail/edge)**: embedded the Guard Boundary Table into §5.2 and the Quantity Flow Diagram into §2.2; added near-miss negative fixtures (FR-8) and the H4 wrong-surface case (FR-10); added boundary-condition unit tests (§8.1) one-per-CRITICAL; populated risk/NFR/open-items; ran the sentinel self-check (0 placeholders).

## Downstream Integration Wiring

| Source | Target | Integration Point | Data Flow |
|--------|--------|-------------------|-----------|
| Guard Condition Boundary Table (GAP rows) | `sc:adversarial` AD-1 | Invariant probe input | The 16 GAP entries are priority invariant candidates |
| Whittaker attack findings | `sc:adversarial` AD-2 | Assumption challenge input | 6 CRITICAL + 10 MAJOR feed assumption identification |
| Correctness findings | `sc:adversarial` AD-5 | Edge case input | State/guard/boundary findings inform edge-case generation |
| Quantity Flow Diagram (DIV-2/3/4) | `sc:roadmap` RM-3 | Risk input | Dimensional mismatches inform risk-weighted prioritization |
| FR-1..13 + §10 themes | `sc:roadmap` / `sc:tasklist` | Spec input | Milestones M1–M5; one task per FR with FR-acceptance DoD |

## Artifacts

- `../troubleshoot-pipeline-hardening-RELEASE-SPEC.md` — the improved spec (primary deliverable)
- `state-variable-registry.md`, `guard-boundary-table.md`, `quantity-flow-diagram.md`, `adversarial-findings.md`, `panel-findings-req-arch.md` — full panel outputs
