# Tier 1 Hypothesis — Arithmetic-mean rubric permits load-bearing-dimension drag to be diluted by orthogonal strengths

**Author**: inline orchestrator (root-cause-analyst not spawned in this transcript; treat as inline fallback per Wave 1.7 failure-handling clause)
**Tier**: 1
**Type**: bug (calibration aggregation)
**Scope**: `/config/.claude/agents/confidence-calibrator.md` + `refs/escalation-rubric.md`
**consistency_with_docs**: not_applicable (--no-doc-discovery)

## Claim

The calibrator returns a **flat arithmetic mean** of 5 dimensions with no floor, no veto, and no domain-aware weighting. When a hypothesis is grounded only in static-source reads but predicts runtime behavior, Evidence-grounding correctly drops to 0.5 — but the other four dimensions (symptom coverage, reproducibility-fit, fix-directness, domain-coherence) remain high because they're scored *against the card's internal coherence*, not against the unverified runtime predicate. The mean is then 0.90 = pass. The calibrated number says "ship" precisely when the only dimension that could have caught the runtime miss has been flagged.

## Evidence (substrate + mechanism)

### E1 — Rubric is flat arithmetic mean, no dimension is load-bearing

`/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md:19`:
```
Confidence = arithmetic mean of the five dimension scores.
Round to two decimals.
```
No "if grounding < 1.0 then cap overall ≤ 0.85" floor. No veto. No weight. Single failure mode: 0.5 grounding with four 1.0s = 0.90 — passes the 0.85 threshold at line 41 of the same file.

### E2 — Three pr86 Tier 2 calibrations confirm the shape

`tier2-root-cause-analyst-calibration.md:13`: `Evidence grounding | 0.5 | ... calibrator lacked Bash to git show and verify`. Mean = 0.90.
`tier2-quality-engineer-calibration.md:13`: same 0.5 with same Bash-absent reason. Only landed at 0.60 because *fix-directness ALSO dropped to 0.5* (broad change surface). Two-dimension drop required; one isn't enough.

### E3 — Calibrator structurally lacks runtime verification

`/config/.claude/agents/confidence-calibrator.md:7`: `tools: Read`. Plus `permissionMode: plan` at line 8. No Bash. The agent's own role text at line 51 says "Read the file at that range and verify the snippet matches" — capped at static citation matching. Predicates like "this Rust code path produces this terminal output" are off-domain.

### E4 — REPORT.md acknowledges the gap but ships anyway

`REPORT.md:116`: "Tier 1 confidence-calibrator scored evidence-grounding 0.5 because it lacked Bash to verify PR-sha citations via `git show`. The orchestrator (this skill) DID verify those citations directly in Wave 0." The orchestrator silently substitutes its own verification for the calibrator's — but the calibrator's 0.5 still averages into the published number. The rubric never sees the orchestrator's veto.

### E5 — Placebo-risk self-warning already in the calibrator spec

`/config/.claude/agents/confidence-calibrator.md:118`: "if the calibrated score consistently matches inline calibration to within ±0.05, the agent is not earning its overhead." The spec acknowledges anchor leakage as a known risk but offers no structural counter — only "periodically run head-to-head meta-evals."

## Proposed Fix (high-level)

Replace the flat mean with a **load-bearing-dimension floor** for the dimension domain-relevant to the hypothesis:
- If the hypothesis predicts runtime behavior AND `Evidence grounding < 1.0` (i.e., calibrator could not execute), cap calibrated confidence at `min(mean, 0.84)` — forcing escalation into Tier 2 where parallel hypotheses + adversarial debate can compensate for the unverifiable predicate.
- Generalize: add a `grounding_predicate_type` field to the hypothesis-card template — `static_source | runtime_behavior | external_doc | mixed`. The rubric then knows which dimension is load-bearing and applies the floor when the load-bearing dimension < 1.0.

## Confidence

**Self-reported: 0.78**. The arithmetic case (E1+E2) is rock-solid; the mechanism explanation (E3) is structurally verified; the policy fix is concrete. The 0.22 reserved for: (a) possibility that other failure modes contribute (e.g., calibrator anchors on card's self-report despite the spec saying it shouldn't), (b) Tier 2 expected to surface co-mechanisms.

Calibration deferred to inline-fallback (we ARE the calibrator inline; arithmetic case is unambiguous).

## Risks

- Floor risk: forces a Tier 2 escalation on every runtime-predicate hypothesis, even when the prediction is sound. Token cost rises systematically. Need a counterbalance — maybe a `--runtime-verified-externally` flag the orchestrator can pass when it has substituted its own verification, raising the floor only when no such substitution exists.
- A floor on grounding may simply shift the gaming surface: agents could mark `static_source` to dodge the floor when behavior is actually runtime-dependent. Needs a Wave 5 audit pass.

## "If I'm wrong, it's probably because..."

...the calibration miss is dominated by **anchoring leak from the card's self-report** (calibrator agent saw "0.92 self-reported" and walked toward it despite the spec forbidding this), not by the arithmetic-mean rubric. In that case the fix is calibrator-prompt + ensemble-of-calibrators, not rubric-arithmetic.

## Files to change

- `/config/.claude/skills/sc-troubleshoot-protocol/refs/escalation-rubric.md` (add load-bearing-dimension floor rule)
- `/config/.claude/skills/sc-troubleshoot-protocol/refs/hypothesis-card-template.md` (add `grounding_predicate_type` field)
- `/config/.claude/agents/confidence-calibrator.md` (apply floor when load-bearing dimension < 1.0)
