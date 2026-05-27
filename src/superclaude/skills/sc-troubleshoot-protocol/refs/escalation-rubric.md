# Escalation Rubric

Used in Wave 1.7 (to calibrate the Tier 1 hypothesis confidence) and in Wave 2 (to decide whether to escalate to Tier 2).

## Confidence calibration (Wave 1.7)

The `root-cause-analyst` returns a self-reported confidence. The skill **re-grades** it against this rubric — agent confidence is not trusted directly.

Score each dimension 0.0–1.0 and average.

| Dimension | 1.0 (strong) | 0.5 (partial) | 0.0 (weak) |
|-----------|--------------|---------------|------------|
| **Evidence grounding** | Cited `file:line` matches a real code path that exhibits the symptom (snippet match verified by calibrator's spot-check) | Cited file exists but the specific line/snippet is inferred, not verified | Hypothesis based on pattern-matching prior bugs; no real citation |
| **Symptom coverage** | Proposed cause explains 100% of the reported symptoms (stack trace, error message, observed behaviour all addressed) | Explains the main symptom but leaves secondary symptoms unexplained | Only explains part of the symptom |
| **Reproducibility fit** | Reproducer exists and matches the cited cause; OR symptom is a deterministic exception with a clear trigger | Symptom is deterministic but no reproducer attempted in Tier 1 | Symptom is intermittent or environment-dependent |
| **Fix directness** | Proposed fix touches the exact code identified in evidence; small, localised change | Fix is in the right area but requires broader changes | Fix is speculative or requires investigation to specify |
| **Domain coherence** | Single domain (e.g. pure logic bug, pure config issue) | Touches two related domains (e.g. logic + tests) | Spans unrelated domains (e.g. perf + auth) |
| **Runtime check** | Hypothesis includes an executed reproducer with captured stdout/stderr that reproduces the symptom; OR an asserted-by-test runtime invariant (test cited by name AND its execution-state declared) | Hypothesis includes a runnable command but no captured output; OR cites a test that exists but was not exercised at hypothesis time | Hypothesis is source-only — no executed reproducer, no test assertion. For `claim_class: static_defect`, this dimension inherits the Evidence grounding score (static defects' source IS their runtime). For `claim_class: runtime_behavior` or `environment_dependent`, source-only cards mandatorily score 0.0. |

**Confidence** = `min(arithmetic_mean(all_six_dimensions), evidence_grounding + 0.30, runtime_check + 0.30)`.

The +0.30 buffer means a 0.5 dimension caps the composite at 0.80, *below* the 0.85 STOP gate. A 0.0 dimension hard-caps the composite at 0.30. The gates apply unconditionally (no claim_class exemption); for `static_defect` claims, Runtime check auto-inherits Evidence grounding so the gate is satisfied whenever the citation is.

Round to two decimals.

### Verdict-direction modifier (M3a)

After computing the gated-minimum confidence, apply this modifier when the card's frontmatter declares `claim_class: runtime_behavior` AND `runtime_check < 1.0`:

| Verdict direction | Cap on calibrated confidence |
|-------------------|------------------------------|
| REFUTE / REJECT   | 0.70 |
| AFFIRM            | 0.84 |

Rationale: a wrong REFUTE on runtime behavior closes the investigation door (the H3 0.95-REFUTE case); a wrong AFFIRM is caught by CI. Source-only REFUTEs of runtime claims are the precise failure mode under repair and must not clear the 0.85 STOP gate. The 0.84 AFFIRM cap means source-only AFFIRMs of runtime claims still ESCALATE to Tier 2 (below the 0.85 STOP).

### Claim-class × evidence-class cross-tab [V2 merged]

The Runtime check dimension score is derived from the (claim_class, evidence_class) pair declared in the card frontmatter:

| claim_class \ evidence_class | runtime_repro | runtime_trace | log_evidence | source_static | doc_static | none |
|------------------------------|---------------|---------------|--------------|---------------|------------|------|
| `runtime_behavior`           | 1.0           | 1.0           | 0.5          | **0.0**       | **0.0**    | **0.0** |
| `environment_dependent`      | 1.0           | 1.0           | 0.5          | **0.0**       | **0.0**    | **0.0** |
| `static_defect`              | 1.0           | 1.0           | 1.0          | inherits EG   | inherits EG | 0.0  |
| `doc_contract`               | 1.0           | 1.0           | 1.0          | 0.5           | 1.0        | 0.0  |
| `config_value`               | 1.0           | 1.0           | 1.0          | inherits EG   | inherits EG | 0.0  |
| `mixed`                      | min of the two component classes' scores                                                          |

The bolded cells (0.0) trigger the verdict-direction modifier when the card's verdict is REFUTE/REJECT.

## Escalation decision (Wave 2)

After confidence is calibrated, apply these rules **in order**. The first matching rule wins.

1. **Hard stops**
   - `--no-escalate` set → STOP at Tier 1 (regardless of confidence). Note in report that escalation was suppressed.
   - `--depth quick` set → STOP at Tier 1.

2. **Forced escalation**
   - `--depth deep` set → ESCALATE (set `escalation_reason: forced_by_depth_deep`).

3. **Signal-driven escalation** (any one triggers escalation)
   - `confidence < 0.85` → ESCALATE (`escalation_reason: low_confidence`).
   - Multi-domain symptom (dimension score 0.5 or lower on "Domain coherence") → ESCALATE (`escalation_reason: multi_domain`).
   - Symptom described as intermittent / flaky / "only sometimes" → ESCALATE (`escalation_reason: intermittent`).
   - Reproducibility dimension scored 0.0 → ESCALATE (`escalation_reason: not_reproducible`).
   - `--type security` AND confidence < 0.95 → ESCALATE (`escalation_reason: security_caution`). Security bugs have asymmetric cost-of-being-wrong; raise the bar.
   - `claim_class ∈ {runtime_behavior, environment_dependent}` AND `runtime_check < 0.5` → ESCALATE (`escalation_reason: source_only_dynamic_claim`).

4. **Default**
   - `confidence ≥ 0.85` AND single-domain AND reproducible → STOP at Tier 1.

## Why 0.85?

Below 0.85, the average Tier 1 hypothesis card has at least one dimension scoring 0.5 or lower — meaning at least one piece of the puzzle is inferred rather than evidenced. That's the threshold where a second independent perspective begins to pay back its token cost. Above 0.85, additional hypotheses tend to converge on the same answer (waste).

This number is calibrated, not arbitrary — change it only based on eval data, not intuition.

## What escalation does NOT mean

Escalation does **not** mean the Tier 1 hypothesis was wrong. It means the skill judged that one perspective is insufficient evidence to recommend a fix with confidence. The Tier 1 card is always retained in the report as one of the candidate hypotheses.
