# Tier 2 — refactoring-expert hypothesis (H-RefExp)

**Author**: refactoring-expert (inline)
**Tier**: 2
**Type**: bug

## Claim

**Root cause: residual anchoring leak from card's self-reported confidence + narrative framing, despite the agent spec forbidding it.** `confidence-calibrator.md:25-27` explicitly says "Self-reported confidence on the card is a signal, not a number. Treat it as part of the card's narrative, not as input to your score." But the agent spec is a *prompt*, not a structural constraint. In pr86's RCA calibration the calibrator's narrative section reads: "card's self-report was pulled down by F2-independence uncertainty; calibrator rewards mechanical strength" — that's the calibrator *reasoning about* the self-report, which is the very anchor the spec told it to ignore. Delta of +0.02 (0.88 self-report → 0.90 calibrated) is suspicious-clean.

In H3: the refactoring-expert's confident REFUTE language ("source-only reads at v0.44.2 conclusively show…") likely anchored the calibrator on the prose certainty, not the evidential gap. The calibrator's prompt-level defense ("never inherit the card's self-reported confidence") is overridden by **the cognitive cost of producing a divergent calibrated score**: the prompt says "if it diverges sharply, surface it honestly" — a soft norm easily defeated by mid-context drift.

The flat-mean rubric is then complicit but not causal: it provides the *channel* through which the residual anchor expresses itself.

## Evidence

- `confidence-calibrator.md:25-27, 36-38`: explicit anti-anchoring instructions phrased as norms, not constraints.
- `confidence-calibrator.md:117-118`: "Placebo risk: if calibrated score consistently matches inline calibration to within ±0.05" — meta-spec acknowledgment that the agent has trouble distinguishing itself from inline.
- `tier2-root-cause-analyst-calibration.md:23`: "Delta: +0.02 — card's self-report was pulled down by F2-independence uncertainty" — calibrator is **reasoning about** the self-report (engaging with it as a number, not just a signal). Exactly what the spec told it not to do.
- `tier2-quality-engineer-calibration.md:23`: Delta of -0.28 — but the -0.28 came from a *second* dimension also dropping (fix-directness), which is mechanical. When only ONE dimension drops, the delta hugs the self-report. The calibrator's defense scales linearly with how many mechanical dimensions disagree, which is upside-down — it should scale with the depth of the single disagreement.

## Proposed Fix

**Structural anti-anchoring via ensemble + format constraint:**
1. Spawn 2 calibrator instances per card (different model/prompt seeds); take the *minimum* calibrated score, not the average. Adversarial selection on calibration itself.
2. Pre-fill the calibration report template with the card's self-report **masked** (replace with `<HIDDEN>` in the agent's input). The narrative will lack a numeric anchor.
3. Add a "what would have changed your score by 0.1" probe — forces the calibrator to articulate evidential dependencies, which surfaces hidden anchoring.

These are H-RefExp's interventions; they compose with H-RCA's rubric fix and H-QE's pin-tests.

## Confidence

**Self-reported: 0.72**. Anchoring leak is mechanistically plausible and the delta-pattern evidence is suggestive, but proving anchoring vs. arithmetic propagation in a single transcript is hard. The pr86 deltas are consistent with both stories.

## Risks

- Ensemble doubles calibrator cost.
- Masking the self-report may also mask context the calibrator legitimately needs (e.g., the "If I'm wrong..." section sometimes contains evidential nuance).

## If I'm wrong...

...the calibrator IS following the spec faithfully and the residual signal in the delta-pattern is just noise. Then H-RCA (rubric arithmetic) carries the load and ensemble is overkill.
