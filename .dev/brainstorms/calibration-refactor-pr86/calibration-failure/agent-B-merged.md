# Merged Theories — Why the Confidence-Calibrator Confidently Scores Source-Only Evidence on Runtime-Behavior Claims

**Merge agent**: B (sc:adversarial --compare --merge --depth quick, three theory variants A/B/C)
**Base variant**: B (combined hybrid score 0.983; won 3 of 5 contested diff points)
**Substrate**: `pr86-integration-contracts-20260526100600` (structurally analogous to H3 0.95-REFUTE; H3 artefacts absent on disk)
**Provenance**: M1/M2/M3 from B-base; M4 from C-U001; §3 cross-theory implications from A-U003; §4 caveat from A; §5 methodology note from B §1

---

## 1. Top-line findings

The H3 0.95-REFUTE / pr86-0.90-calibrated pathology is the **multiplicative compounding** of two structural design choices in the rubric (M1, M2), modulated by a decision-theoretic blind spot (M3), and propagated by a **silent-green test suite** that institutionalizes the blindness (M4).

**Convergent across all three channels**: M1 (arithmetic-mean dilution) and M2 (source-vs-runtime evidence conflation) are the load-bearing primary mechanisms — three independent investigative channels (unmediated direct-read, /sc:reflect-degraded, and /sc:troubleshoot --depth deep) all surfaced them.

---

## 2. Four Theories

### M1 — Arithmetic-mean dilution of the only honest dimension (PRIMARY)

**Mechanism**. The escalation rubric (`escalation-rubric.md:19`) defines calibrated confidence as the **arithmetic mean of five 0.0/0.5/1.0 dimension scores** with no minimum-floor rule, no weighting, and no veto clause. Evidence-grounding is the only dimension that asks "did you verify the claim against the artefact"; the other four (symptom coverage, reproducibility fit, fix directness, domain coherence) score the *card's internal coherence and shape*. A well-written but reality-untested card scores (0.5 + 1.0 + 1.0 + 1.0 + 1.0) / 5 = **0.90**, clearing the ≥0.85 STOP gate. Same shape produces H3's 0.95 REFUTE: four "card is internally tight" dimensions at 1.0 plus one "I can't actually run zellij" at ≥0.75 averages to ≈0.95.

**Evidence**:
- `escalation-rubric.md:19` — "Confidence = arithmetic mean of the five dimension scores." No floor, no weight, no veto.
- `tier2-root-cause-analyst-calibration.md:11-17` — actual dimension table: Evidence=0.5, Coverage=1.0, Repro=1.0, FixDir=1.0, Domain=1.0 → 0.90.
- `tier2-quality-engineer-calibration.md:11-17` — Evidence=0.5, FixDir=0.5, other three 1.0 → 0.80 only because a *second* dimension dropped.
- `audit.log:60-63` — "All 3 calibrators flagged evidence-grounding ≤ 0.5 due to lacking Bash to verify PR-sha citations." The signal was loud; the math swallowed it.

**Per-theory confidence**: **0.90** (averaged across channels: A 0.85, B 0.92, C 0.85)

**Systemic fix**: Replace arithmetic-mean with a gated minimum — `calibrated = min(evidence_grounding, mean(other_four))`, OR cap calibrated ≤ 0.84 when `evidence_grounding < 1.0` AND the hypothesis predicts runtime behavior (new card field `grounding_predicate_type=runtime_behavior`).

---

### M2 — "Evidence grounding" conflates source-citation with runtime-verification (PRIMARY)

**Mechanism**. The rubric's "Evidence grounding" 1.0 anchor: *"Cited `file:line` matches a real code path that exhibits the symptom; OR diagnostic command output reproduces the symptom"* (`escalation-rubric.md:13`). The OR is the trap. Source citation alone earns 1.0, even when the hypothesis is a **runtime-behavior claim** that source-reading cannot adjudicate. H3's "zellij subcommand dispatch order" claim is a CLI dispatch claim that source-reading clap definitions can *suggest* but only execution can *prove*. The calibrator's own tool surface (`confidence-calibrator.md:6` — `tools: Read`) means it cannot challenge a runtime claim; its "verify" is character-match against cited file (`confidence-calibrator.md:51` — "Read the file at that range and verify the snippet matches"), not behavioural check.

**Evidence**:
- `escalation-rubric.md:13` — OR clause; source citation alone admittable.
- `escalation-rubric.md:15` — Reproducibility fit anchors include "deterministic exception with a clear trigger" — scores 1.0 without anyone pulling the trigger.
- `confidence-calibrator.md:6` — `tools: Read`; the calibrator structurally cannot execute anything.
- `confidence-calibrator.md:51` — "verify the snippet matches" — snippet match, not behavioural check.
- `REPORT.md:114-116` — "Tier 1 confidence-calibrator scored evidence-grounding 0.5 because it lacked Bash to verify PR-sha citations." Confession the calibrator's evidence-grounding score is structurally truncated with no mechanism to translate that into a confidence ceiling.

**Per-theory confidence**: **0.84** (averaged: A 0.80, B 0.88, C folds into M1 = effective 0.85)

**Systemic fix**: Add a sixth rubric dimension "**Runtime check**" with anchors `1.0 = executed reproducer with captured stdout/stderr / 0.5 = runnable command but no captured output / 0.0 = source-only`, and tier-gate it: REFUTE/REJECT verdicts on runtime-behavior claims require Runtime check ≥ 0.5.

---

### M3 — Verdict-direction asymmetry: the calibrator scores diagnostic confidence, not refutation cost-of-being-wrong (NOVEL)

**Mechanism**. The rubric and calibrator treat all hypothesis verdicts (AFFIRM / REFUTE / REJECT) as **symmetric assertions** about a cause. But the cost asymmetry is sharp: a wrong AFFIRM ships a fix that doesn't help and is rolled back by CI; a wrong REFUTE **closes the investigation door** and lets the real bug ship. H3's 0.95 REFUTE is the canonical case — the agent said "H3 is not the cause" at 0.95, the troubleshoot pipeline accepted the REFUTE, the alternative cause was pursued, and CI then reproduced exactly H3's symptom. Nowhere in `confidence-calibrator.md` or `escalation-rubric.md` is verdict direction an input. The rubric's only asymmetric-cost clause is `--type security AND confidence < 0.95 → ESCALATE` (line 39) — no analogue for REFUTE on testable runtime claims.

**Evidence**:
- `escalation-rubric.md:39` — only asymmetric-cost clause in the rubric.
- `confidence-calibrator.md` (entire file) — no mention of verdict direction as an input, scoring axis, or threshold modifier.
- `tier2-root-cause-analyst-hypothesis.md:102-105` — card's own self-confidence is internally bimodal (0.95 on chain, 0.75 on independence claim), but the calibrator returns a single blended 0.90.

**Per-theory confidence**: **0.78** (B's per-theory rating; the strongest of the three "third theories" surfaced across channels — A's stripped-context at 0.65 and C's anchoring at 0.45 were both weaker)

**Systemic fix**: Add a verdict-direction modifier — `verdict=REFUTE AND claim_class=runtime-behavior AND runtime_check < 1.0 → cap calibrated at 0.70` — so source-only REFUTEs of runtime claims cannot clear the STOP gate.

---

### M4 — Calibrator eval suite has silent-green coverage of structurally-unverifiable predicates (GUARDRAIL)

**Mechanism**. `confidence-check/SKILL.md:14-18` advertises "Test Results (2025-10-21): Precision 1.000, Recall 1.000, 8/8 test cases passed." The eval corpus scores the calibrator on hypotheses it *can* ground, but never on hypotheses where grounding is structurally impossible (sha-pinned PR diff; runtime behavior predicted from source-only reads). The calibrator passes the test suite for the *wrong reason* — the same anti-pattern that pr86 itself diagnosed at production-code scope (`adversarial/debate-transcript.md:69`: "test_t1/t6/t7 silently green-bar on substring containment of `FR-S10-02`"). Applied recursively: **the calibrator fails the H3 case the same way pr86's test_t1 failed F1 — green-bar on irrelevant invariant.** Even if M1/M2/M3 are fixed at the rubric layer, without pin tests the next regression institutionalizes the next blindness.

**Evidence**:
- `confidence-check/SKILL.md:14-18` — blanket 1.000/1.000 claim, no per-failure-mode breakdown.
- `confidence-calibrator.md:117-118` — "Placebo Risk" section uses soft language ("should periodically run head-to-head meta-evals") that does not enforce eval-suite contracts.
- `adversarial/debate-transcript.md:128-129` (pr86 substrate) — U-001 silent-green winner unanimous concession.

**Per-theory confidence**: **0.68** (C's per-theory rating)

**Systemic fix**: Add 3 pin tests to the calibrator eval suite —
(a) sha-pinned citation → calibrated ≤ 0.84,
(b) source-only runtime prediction → calibrated ≤ 0.84,
(c) property: `evidence_grounding ≤ 0.5` → calibrated ≤ 0.85 for any input.

---

## 3. Cross-theory implications (provenance: Variant A)

- **M1 and M2 compound multiplicatively, not additively.** The arithmetic-mean structure (M1) only produces a 0.90 from a 0.5 evidence-grounding because the OR clause (M2) lets four other dimensions honestly score 1.0 on prose. **Fix only M1 (cap rule) and well-written cards still pass; fix only M2 (Runtime-check dimension) and the dilution math still hides the new low dimension. Both fixes are required.**
- **M3 sits orthogonal to M1/M2.** Even with the M1 cap and the M2 Runtime-check dimension, a 0.95 calibrated REFUTE on a runtime claim is still dangerous if the verdict-direction modifier isn't applied. M3 attaches its modifier *after* M1+M2 produce their score.
- **M4 is the meta-layer.** Without pin tests, the next eval-corpus expansion can silently re-institutionalize the same blindness. M4 is the *only* prescription that does not require changes to the rubric or the calibrator agent itself — it changes the test suite.
- **All four share a common root**: the entire calibration apparatus treats **source-reading as a complete epistemology for code claims**. This is true for static defects (missing import, wrong regex literal) and structurally false for control-flow / runtime / environment-dependent claims. Both the H3 case (`zellij` subcommand dispatch) and the pr86 case (PR-sha citations + Layer 3 emptiness bypass) have a runtime dimension that source-only reading systematically under-detects.

---

## 4. Grounding caveat (provenance: Variant A)

The pr86 substrate calibrations are 0.90 and 0.60, not 0.95. The mechanism is structurally identical (`tier2-root-cause-analyst-calibration.md:11-19` shows evidence-grounding=0.5 + four 1.0s = 0.90). The H3 0.95 would require either (a) the upstream agent self-scoring evidence-grounding at 1.0 by claiming the source read *did* match runtime behavior (M2 in its strongest form), or (b) all five dimensions self-scored at 1.0 with the calibrator unable to dispute. Either route is consistent with the theories above; **without H3's calibration card on disk this merge cannot empirically distinguish which dominated.** Treat M1+M2 as load-bearing and M3 as the verdict-direction qualifier that explains the 0.95-specific shape if route (a) applied.

---

## 5. Methodology note (provenance: Variant B §1, abbreviated)

This merged output is the convergence of three investigative channels:
- **Channel A** (unmediated direct read): produced cleanest cross-theory synthesis (§3).
- **Channel B** (sc:reflect): degraded to direct-read mode because `mcp__serena__think_about_*` tools returned "No such tool available"; channel produced base-variant theories M1/M2/M3 from substrate Reads.
- **Channel C** (sc:troubleshoot --depth deep): ran the troubleshoot pipeline on the calibrator itself with `--no-mcp --no-doc-discovery`; produced Tier 1 + Tier 2 fan-out + adversarial debate inline-fallback; contributed M4.

**The 3-channel design specifically guards against single-tool blindness.** Even with B's channel degradation and C's `--no-mcp` flag, the cross-channel convergence on M1 and M2 makes those two theories the highest-confidence load-bearing claims in this merge.

---

## Provenance map

| Section | Source variant | Notes |
|---|---|---|
| §1 Top-line findings | merge-synthesis | Synthesizes A's cross-theory framing + B's primary theories |
| §2 M1 | B B1 (base) | All three channels converged; per-theory confidence averaged |
| §2 M2 | B B2 (base) | A T2 and B B2 directly mirror; C folds in via M1 predicate |
| §2 M3 | B B3 (base) | Novel verdict-direction asymmetry; B unique contribution |
| §2 M4 | C C2 (debate U-001 winner) | Eval-suite pin-test prescription; only non-rubric mechanism |
| §3 Cross-theory implications | A (debate U-003 winner) | Multiplicative-compounding insight |
| §4 Grounding caveat | A | Most-explicit framing of pr86→H3 inference gap |
| §5 Methodology note | B §1 (abbreviated) | Channel-degradation transparency |
