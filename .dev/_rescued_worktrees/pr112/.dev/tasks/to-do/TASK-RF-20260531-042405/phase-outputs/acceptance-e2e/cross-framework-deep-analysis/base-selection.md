---
base_variant: "sonnet-architect"
variant_scores: "A(opus-architect):86 B(sonnet-architect):87"
---

# Roadmap Variant Evaluation — Cross-Framework Deep Analysis Sprint

Variant A = `roadmap-opus-architect` (8 milestones / 13 weeks, M0 foundation + 1:1 phase mapping).
Variant B = `roadmap-sonnet-architect` (5 composite milestones / 12 weeks).
Debate convergence: 0.74 (2 rounds, strong content agreement, 2 honest residual disputes).

## 1. Scoring Criteria (derived from the debate)

The 14 divergence points collapse onto six evaluable axes. Weights reflect which axes the debate treated as substantive vs cosmetic.

| # | Criterion | Weight | Debate origin |
|---|---|---|---|
| C1 | Spec fidelity & end-to-end traceability | 20% | Div 10 (parent-FR closure), all-19-component coverage |
| C2 | Risk-management completeness | 15% | Div 9 (R1–R10 vs R-001–R-017) |
| C3 | Resilience / restartability design | 15% | Div 1 & 5 (NFR-5 timing) |
| C4 | Verification & gate rigor | 20% | Div 4 & 14 (validation/assembly separation) |
| C5 | Schedule realism & leanness | 15% | Div 2 & 3 (8 vs 5 milestones, the extra week) |
| C6 | Structural accountability & clarity | 15% | Div 2 (per-phase ownership), Div 8 (priorities) |

## 2. Per-Criterion Scores

| Criterion | A (opus) | B (sonnet) | Evidence |
|---|---|---|---|
| C1 Fidelity/traceability | 86 | 90 | B adds an explicit `FR-XFDA-001` closure row (M5) asserting "8 child FRs + 6 NFRs + 19 components + 3 contracts traced" in one auditable line; A distributes the same claim across the M7 artifact-index. A conceded this is "pure gain" with no contradiction. |
| C2 Risk completeness | 80 | 92 | B's 17-row register (R-001–R-017) surfaces strategy-bias, citation-variance, shell-overfit, and field-completeness as discrete mitigated modes; A's R1–R10 folds related modes. A conceded the superset adds surface "with no contradiction." |
| C3 Resilience design | 95 | 80 | A proves `--start` resume on a no-op gate in M0 — "cheapest-possible discovery of a structurally broken executor," uncontested in rebuttal. B verifies only at M5 (NFR-XFDA.5), so the first real resume could be week-12 crash recovery with no prior signal. A's strongest, least-contested win. |
| C4 Gate rigor | 86 | 84 | A makes adversarial validation a discrete P0 **Quality** boundary (M6) closing before assembly (M7); B co-locates it as FR-XFDA-001.7 inside M5. A conceded the verification **content is equivalent** — the dispute is structural prominence, not correctness — so A's edge here is narrow. |
| C5 Schedule leanness | 78 | 90 | B is 12 weeks / 5 milestones. A's 13th week is entirely M0; A conceded the resume smoke test "can overlap M1," collapsing most of M0's standalone justification, and called the week "the weakest part of A's case." B's DM-003 already delivers per-phase attribution, neutralizing A's accountability premium for the week. |
| C6 Accountability | 88 | 84 | A's per-phase milestones give per-phase ownership; B bundles Phases 2+3 (M2) and 4-phase closing work (M4/M5). But B conceded nothing here and A conceded the "blur is illusory" point partially — DM-003's per-phase deterministic minima make a Phase-2 vs Phase-3 defect attributable at gate-row level regardless of wrapper count. A retains a modest, real edge. |

## 3. Overall Scores

Weighted totals:
- **Variant A (opus-architect): 86** — `(86×.20)+(80×.15)+(95×.15)+(86×.20)+(78×.15)+(88×.15) = 85.6`
- **Variant B (sonnet-architect): 87** — `(90×.20)+(92×.15)+(80×.15)+(84×.20)+(90×.15)+(84×.15) = 86.7`

The variants are within ~1 point — consistent with a 0.74 convergence and "strong content agreement." A leads decisively on a single high-value axis (resilience, C3); B leads on three axes (fidelity, risk, schedule) by smaller-but-real margins. A's C4 lead was self-conceded as visibility-only, so it does not offset B's spread.

## 4. Base Variant Selection — `sonnet-architect` (B)

B is selected as the merge spine for three evidence-backed reasons:

1. **B's structural contributions are large, objective supersets.** The 17-row risk register, the consolidated `FR-XFDA-001` closure assertion, and flat OI-1..6 IDs are all things A *explicitly conceded* to adopt ("strict supersets… pure gain," "adopt flat IDs with semantic aliases"). Importing these wholesale defines the spine; rebuilding them onto A's frame would re-derive what A already agreed B does better.

2. **The debate converged on B's 12-week envelope.** A conceded the extra week is its weakest point and that the resume smoke test can overlap M1 — so the standalone M0 milestone, A's one structural differentiator, was the most-eroded element in rebuttal. Starting from B's 5-milestone / 12-week structure avoids carrying a milestone scaffold the author himself discounted.

3. **A's two surviving wins are discrete, bounded grafts.** A's advantages — the early `--start` resume proof and the independent P0 validation boundary — are point-features, not pervasive structure. Grafting two bounded features onto B's spine is lower-risk than importing B's entire registry+envelope onto A and then deleting A's per-phase scaffolding. Crucially, **A's marginal rigor edge is fully preserved via graft, so no rigor is lost by choosing the leaner base.**

## 5. Improvements to Incorporate from Variant A (the non-base)

Graft the following A-sourced elements into the B spine during merge:

1. **Early restartability proof (A's strongest win, C3).** Add an **M1 foundation sub-phase** that authors DM-002/DM-003 *before* the gates they govern and runs a `--start` resume **smoke test on a no-op gate** at sprint start — while **retaining B's M5 NFR-XFDA.5 full validation**. The debate's explicit resolution: "keep *both* an M0 smoke test and M5 validation." This closes B's sole material weakness (week-12 first-resume risk) at the cost of one no-op test.

2. **Independent P0 validation boundary (C4).** Even co-located in B's closing M5, model adversarial validation (FR-XFDA-001.7) as an explicit **P0 Quality pass/fail gate that must close before assembly (FR-XFDA-001.8) begins** within the milestone — preserving A's "the transition is the check's teeth" prominence without re-adding a milestone wrapper.

3. **Decision Summary table (A §"Decision Summary").** A carries an auditable decisions ledger (orchestration model, milestone decomposition, evidence sourcing, pipeline-analysis granularity, backlog validation) that B omits. Adopt it — pure documentation gain.

4. **Foundation-contract authoring discipline.** A's point that contract authoring "must precede the gates it defines" is correct and survives the week-collapse; fold DM-002/DM-003 authoring into B's M1 as a hard precondition sub-step, not interleaved with inventory.

Conversely, **drop** the following A elements per debate resolution: the standalone M0 milestone wrapper (fold into M1), per-phase milestone proliferation (B's DM-003 delivers attribution), and uniform-P0 framing where B's tiers are retained as inert centrality documentation (no behavioral force under an all-19-required gate, per B's concession to A).

Net merge: B's 12-week / 5-milestone envelope + B's superset risk/closure/ID registries, hardened with A's early resume smoke test, independent validation gate, and decision ledger.
