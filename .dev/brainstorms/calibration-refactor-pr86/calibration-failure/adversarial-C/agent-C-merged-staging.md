# Calibration-Failure Root Causes — Merged Theories (Agent C run)

**Source variants merged**: agent-A-theories.md (unmediated direct-read), agent-B-theories.md (sc:reflect channel — degraded mode), agent-C-theories.md (sc:troubleshoot --depth deep)
**Adversarial protocol**: sc:adversarial --compare --merge --depth quick (Round 1 only)
**Base variant selected**: A (unmediated) — quant_score 0.99, qual_score 0.93, combined 0.960
**Convergence**: 0.82 (above 0.80 default threshold)

---

## Mechanism M1 — Arithmetic-Mean Dilution of the Only Honest Dimension

*Provenance: A T1 (primary), B B1 (formula refinement), C C1 (predicate-type conditional)*

### Mechanism
The escalation rubric collapses five heterogeneous dimensions into an unweighted arithmetic mean (`escalation-rubric.md:19` — "Confidence = arithmetic mean of the five dimension scores"). Four of those dimensions (symptom coverage, reproducibility fit, fix directness, domain coherence) can be scored from the card's prose alone. Only **evidence grounding** asks the question that matters for runtime-behavior claims: "does the cited line actually do what the card says at runtime?" When evidence-grounding is honestly scored 0.5 (because the calibrator's `tools: Read` cannot execute), it is averaged against four 1.0s and the composite still lands at **(0.5 + 1 + 1 + 1 + 1) / 5 = 0.90** — clearing the 0.85 escalation gate. The dimension that should have *vetoed* the verdict contributes 20% weight. Same arithmetic explains the H3 0.95 REFUTE: prose-readable dimensions all score 1.0 and dilute the one honest doubt.

### Evidence
- `escalation-rubric.md:19` — unweighted arithmetic mean with no veto rule.
- `tier2-root-cause-analyst-calibration.md:11-17` — direct demonstration: evidence-grounding=0.5, other four=1.0, calibrated 0.90.
- `tier2-quality-engineer-calibration.md:13-17` — same shape, but a *second* dimension also dropped to 0.5, yielding 0.60. The single-dimension drop is structurally insufficient to defeat the average.
- `REPORT.md:114-116` — orchestrator confession that the calibrator's evidence-grounding score is structurally truncated, with no mechanism to translate that truncation into a confidence ceiling.
- `confidence-calibrator.md:7,8` — `tools: Read`, `permissionMode: plan`. The "verify with command output" half of the rubric's OR-clause is unreachable.

### Merged confidence
**0.88** (consensus across A=0.85, B=0.92, C=0.85).

### Systemic fix
Replace the unweighted arithmetic mean with a gated minimum:
- `calibrated = min(evidence_grounding + 0.3, mean(all_five))` for hypotheses predicting runtime behavior
- OR: any dimension scored ≤ 0.5 caps the composite at 0.75 (below the 0.85 escalation threshold)
- AND a new card field `predicate_type ∈ {static, runtime}`; runtime predicate + evidence_grounding < 1.0 caps calibrated at 0.84

---

## Mechanism M2 — "Evidence Grounding" Conflates Source-Citation with Runtime-Verification

*Provenance: A T2 (primary), B B2 (formula refinement: sixth dimension)*

### Mechanism
The rubric's Evidence-grounding row defines 1.0 as "Cited `file:line` matches a real code path that exhibits the symptom; OR diagnostic command output reproduces the symptom" (`escalation-rubric.md:13`). The OR is the trap. It permits 1.0 on source citation alone without ever requiring runtime reproduction. For static defects (missing import, wrong regex) this is fine — the source IS the runtime behavior. For dynamic-control-flow defects (does `Some(Command::Options(...))` fall through to `start_client`? Does empty `contract_idents` actually bypass the guard at runtime?) source citation can be deeply misleading: control flow that *appears* to fall through in static read can be diverted by a match arm, `?` operator, panic, feature flag, or side-effecting initializer. The rubric never names this distinction, and the calibrator's `tools: Read` (`confidence-calibrator.md:5`) physically cannot upgrade an evidence-grounding score by executing.

### Evidence
- `escalation-rubric.md:13` — the literal OR clause permitting source-citation-only 1.0.
- `escalation-rubric.md:15` — Reproducibility fit anchors: "deterministic exception with a clear trigger" scores 1.0 without anyone pulling the trigger.
- `confidence-calibrator.md:5` — `tools: Read`. Calibrator cannot execute.
- `confidence-calibrator.md:51` — "Spot-check the evidence: for each `file:line` cited, Read the file and verify the snippet matches." The instruction is about **snippet match**, not runtime behavior.
- `confidence-check/SKILL.md:53-110` — none of the 5 weighted checks ask "did you reproduce the symptom?" The cultural prior treats source-reading as the highest tier of evidence.
- `tier2-refactoring-expert-hypothesis.md:91-96` — even self-stated confidence (0.78) is calibrated against *structural* readability, not runtime probe.

### Merged confidence
**0.84** (consensus across A=0.80, B=0.88; C subsumed it under C1).

### Systemic fix
Add a sixth rubric dimension **Runtime check** with anchors:
- 1.0 = hypothesis includes executed reproducer with captured stdout/stderr
- 0.5 = hypothesis includes a runnable command but no captured output
- 0.0 = hypothesis is source-only
Tier-gate: REFUTE/REJECT verdicts on runtime-behavior claims require Runtime check ≥ 0.5.

(Alternative framing — A's split: "Source-citation accuracy" + "Runtime verification" as two separate dimensions. Equivalent in spirit; B's "add a sixth" is cleaner.)

---

## Mechanism M3 — Verdict-Direction Asymmetry and Anchoring Channel Loss (composite)

*Provenance: B B3 (verdict-direction primary), A T3 (information-channel adjunct), C C3 (anchoring residual)*

The third mechanism does not converge on a single cause in the debate (X-001: distinct mechanisms, MERGE outcome). All three sub-mechanisms are orthogonal and each merits a fix.

### M3a — Verdict-direction asymmetry (B B3; debate-favored)
**Mechanism**: The rubric treats AFFIRM and REFUTE as symmetric assertions about a cause. But asymmetric cost-of-being-wrong: a wrong AFFIRM ships a fix that CI rolls back; a wrong REFUTE *closes the investigation door* and lets the real bug ship. The H3 0.95 REFUTE is the canonical case. Nowhere in `confidence-calibrator.md` or `escalation-rubric.md` is verdict direction an input. The only asymmetric-cost clause is `--type security AND confidence < 0.95 → ESCALATE` (`escalation-rubric.md:39`) — no analogue for REFUTE on testable runtime claims.

**Evidence**:
- `escalation-rubric.md:39` — sole asymmetric-cost clause is type=security, not verdict direction.
- `confidence-calibrator.md` entire file — no mention of verdict direction as scoring input.
- `tier2-root-cause-analyst-hypothesis.md:102-105` — internally bimodal self-confidence (0.95 on chain, 0.75 on independence sub-claim) blended into single 0.90 by calibrator.

**Fix**: Add verdict-direction modifier — `verdict=REFUTE AND claim_class=runtime-behavior AND runtime_check < 1.0 → cap calibrated at 0.70`.

**Merged confidence**: 0.78.

### M3b — Stripped-context removes the doubt signal (A T3; information-channel adjunct)
**Mechanism**: The calibrator is deliberately deprived of the upstream investigative trail (`confidence-calibrator.md:21`). The goal is anti-anchoring. But the strip also removes the upstream agent's hedges, doubts, and near-misses — the very signals that would tell a calibrator "this is the kind of question where source-only reading is insufficient." Clean finished cards optimize for the rubric's prose-readable dimensions; the doubts that should have been there were never written down, and the calibrator by design has no upstream signal to flag the missing-doubt.

**Evidence**:
- `confidence-calibrator.md:21` — explicit trail-strip; the cost (loss of doubt-signal) is unnamed.
- `hypothesis-card-template.md:104-108` — "If I'm wrong, it's probably because…" is a one-sentence alternative, NOT a "what evidence would falsify me."

**Fix**: Add mandatory **Falsification standard** field to the hypothesis card template — "what evidence would prove me wrong" — that survives the strip, AND require the calibrator to score whether the standard was met by actual evidence.

**Merged confidence**: 0.65.

### M3c — Residual anchoring leak from self-report (C C3; secondary)
**Mechanism**: `confidence-calibrator.md:25-27` instructs "Self-reported confidence on the card is a signal, not a number" — a *prompt-level norm*, not a structural constraint. The calibrator sees the card's self-report and confident prose inside its context window. Producing a divergent score imposes a cognitive cost without structural counter-pressure. Empirically: pr86 RCA delta +0.02 (self 0.88 → calibrated 0.90); the -0.28 case (QE) was driven by mechanical multi-dimension drop, not by anti-anchoring discipline.

**Evidence**:
- `confidence-calibrator.md:25-27,36-38` — prompt-norm phrasing only.
- `confidence-calibrator.md:117-118` — Placebo Risk acknowledgment.
- `tier2-root-cause-analyst-calibration.md:21-23` — calibrator's narrative *reasons about* the self-report number, the precise behavior the spec said not to do.

**Fix**: Spawn 2 calibrator instances per card (different seeds), take the minimum; OR mask the card's self-reported confidence in the calibrator's input.

**Merged confidence**: 0.45.

---

## Mechanism M4 — Eval-Suite Silent-Green Coverage of Structurally-Unverifiable Predicates (prevention)

*Provenance: C C2 — only variant naming this; KEEP per debate U-003 (0.85)*

### Mechanism
`confidence-check/SKILL.md:14-18` advertises "Test Results: Precision 1.000, Recall 1.000, 8/8 test cases passed." The eval corpus scores the calibrator on hypotheses it *can* ground — but never on hypotheses where grounding is structurally impossible (sha-pinned PR diff; runtime behavior predicted from source-only reads). The calibrator passes the test suite for the wrong reason — same anti-pattern V3 identified in pr86 itself (`adversarial/debate-transcript.md:69`: "test_t1/t6/t7 silently green-bar on substring containment"). The "1.000/1.000" claim does the work of a calibration-quality signal it cannot actually carry.

### Evidence
- `confidence-check/SKILL.md:14-18` — blanket 1.000/1.000, no per-failure-mode breakdown, no listed case for "structurally-unverifiable predicate."
- `confidence-calibrator.md:117-118` — Placebo Risk admission: "*should* and *periodically*" — soft language, not enforced eval-suite contracts.
- pr86's own debate-transcript.md:128-129 — U-001 silent-green winner: without pin tests, downstream cannot distinguish "fix worked" from "fix had no effect."

### Merged confidence
**0.68** (C's own assessment; held).

### Systemic fix
Add 3 pin tests to calibrator eval suite:
1. Sha-pinned citation when current HEAD differs → calibrated ≤ 0.84.
2. Source-only runtime prediction → calibrated ≤ 0.84.
3. Property test: `evidence_grounding ≤ 0.5` → calibrated ≤ 0.85 for any input.

---

## Cross-Mechanism Implications

- **M1 × M2 compound multiplicatively, not additively** (A T1+T2 framing). The arithmetic-mean structure only produces 0.90 from a 0.5 evidence-grounding because the OR clause lets four other dimensions honestly score 1.0 on prose. Fix only M1 (cap on low evidence-grounding) and well-written cards still pass; fix only M2 (split into source-citation + runtime-verification) and the dilution math still hides the low new dimension. **Both fixes are required, and applying either alone underfits the failure mode.**
- **M3 is upstream of M1 and M2**. Even with veto rules and a runtime dimension, if the calibrator never sees the trail of doubts (M3b) or accounts for verdict-direction cost (M3a), it cannot raise *new* concerns the upstream agent failed to articulate.
- **M4 is the prevention mechanism** for all three diagnostic mechanisms. Without pin tests, any fix to M1/M2/M3 will be regressed silently.
- **Recursion-of-anti-pattern** (from C): the calibration apparatus is failing the same way pr86's code was failing (silent-green coverage of structurally-unverifiable predicates). This isomorphism is a verification that the chosen root causes are real, not procedural artifacts.
- **Common root**: the entire calibration apparatus treats **source-reading as a complete epistemology for code claims**. This is true for static defects and structurally false for control-flow / runtime / environment-dependent claims.

## Known Substrate Caveats

- pr86 substrate calibrations are 0.90 and 0.60, not 0.95. The mechanism is structurally identical (`tier2-root-cause-analyst-calibration.md:11-19`) but the H3 0.95 would require either (a) the upstream agent self-scoring evidence-grounding at 1.0 (Theory M2 in its strongest form) or (b) all five dimensions self-scored at 1.0 with the calibrator unable to dispute. Both routes are consistent with the merged mechanisms; without H3's calibration card on disk neither can be cleanly distinguished.
- Risk per A: M3b's "Falsification standard" field could amplify well-written but wrong cards unless paired with M2's runtime-verification dimension demanding the standard *be applied*.

## Top 3 Root Causes (convergence summary)

1. **M1 (arithmetic-mean dilution)** — unanimous, confidence 0.88, load-bearing.
2. **M2 (evidence-grounding OR-clause + Read-only tool)** — unanimous, confidence 0.84, compounds with M1.
3. **M4 (eval-suite silent-green coverage)** — unique to C, prevention mechanism, confidence 0.68; M3a (verdict-direction asymmetry, B-unique, 0.78) is a strong alternative third pick depending on whether prevention or additional diagnostic axis is weighted higher.
