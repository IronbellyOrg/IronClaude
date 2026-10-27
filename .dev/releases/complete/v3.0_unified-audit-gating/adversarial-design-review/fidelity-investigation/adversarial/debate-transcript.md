# Adversarial Debate: Fidelity Gate Convergence Mitigation

## Metadata
- Depth: deep
- Focus: fidelity-gate-effectiveness, severity-drift, attention-degradation, remediation-loops
- Variants: 3 (A: Wiring v2.0, B: Anti-Instincts, C: Wiring v1.0)
- Debate format: Structured scoring against 5 empirically-identified root causes

---

## Round 1: Per-Spec Effectiveness Assessment

### Root Cause 1: SEVERITY DRIFT
*Issues rated MEDIUM in Run 1 get elevated to HIGH in Run 3 by a different LLM invocation with no anchoring to prior severity judgments*

**Variant A (Wiring v2.0)**:
- **Strength**: Severity is a Python `Literal["critical", "major", "info"]` enum, not LLM-assessed. The `blocking_for_mode()` method deterministically maps severity to blocking status. No LLM invocation can reinterpret severity.
- **Weakness**: Does not address the SPEC_FIDELITY_GATE where severity drift actually occurs. This gate runs on a *different* artifact.
- **Score: 5/5 for its own gate; 1/5 for the existing fidelity gate problem**

**Variant B (Anti-Instincts)**:
- **Strength**: Binary pass/fail — `undischarged_obligations==0`, `uncovered_contracts==0`. No severity gradient exists that could drift. `fingerprint_coverage>=0.7` is a fixed numeric threshold.
- **Weakness**: Same as A — doesn't touch the spec-fidelity gate. The fingerprint threshold of 0.7 could theoretically be a source of drift if the fingerprint extraction were non-deterministic, but it IS deterministic.
- **Score: 5/5 for its own gate; 1/5 for the existing fidelity gate problem**

**Variant C (Wiring v1.0)**:
- **Strength**: Zero-tolerance (`all counts must be 0`). Even simpler than A — no mode-aware blocking.
- **Weakness**: The `_deviation_counts_reconciled` companion feature DOES touch SPEC_FIDELITY_GATE and directly addresses a manifestation of severity drift (frontmatter/body count mismatch). This is the ONLY feature across all 3 specs that touches the problematic gate.
- **Score: 5/5 for its own gate; 2/5 for the existing fidelity gate (deviation recon helps but doesn't fix severity drift itself)**

### Root Cause 2: DOCUMENT REGENERATION
*The LLM sometimes produces an entirely new roadmap structure rather than preserving edits, destroying all prior fixes*

**Variant A (Wiring v2.0)**:
- **Strength**: `retry_limit=0` — step executes once. Report is emitted by Python code (`emit_report()`), not LLM. No regeneration is possible because no LLM generates the artifact.
- **Weakness**: Does not prevent document regeneration in the spec-fidelity remediation step, which is the actual problem location.
- **Score: 5/5 for its own gate; 1/5 for the existing problem**

**Variant B (Anti-Instincts)**:
- **Strength**: Same — `retry_limit=0`, Python-emitted report. Additionally, the `INTEGRATION_ENUMERATION_BLOCK` prompt injection DOES affect the roadmap generation step. If the LLM follows the prompt, it should produce more stable structure around integration points.
- **Weakness**: The prompt injection is a *generation-time* improvement, not a remediation-time fix. If spec-fidelity triggers remediation, the prompt injection doesn't prevent regeneration during remediation.
- **Score: 5/5 for its own gate; 2/5 for the existing problem (prompt injection helps at generation time)**

**Variant C (Wiring v1.0)**:
- **Strength**: Sprint-focused; no roadmap pipeline integration means no regeneration concern for its own gate.
- **Weakness**: Completely silent on roadmap document regeneration.
- **Score: 4/5 for its own gate (sprint context, no regeneration possible); 1/5 for the existing problem**

### Root Cause 3: ATTENTION DEGRADATION
*The fidelity check prompt embeds both the full spec and full roadmap inline. With large documents, the LLM exhibits attention drift*

**Variant A (Wiring v2.0)**:
- **Strength**: AST-based analysis doesn't use LLM at all — immune to attention degradation. Algorithms exhaustively walk the AST tree; they can't "miss" something due to context length.
- **Weakness**: Does not reduce the attention burden on the spec-fidelity check, which still embeds full documents inline.
- **Score: 5/5 for its own gate; 1/5 for the existing problem**

**Variant B (Anti-Instincts)**:
- **Strength**: All 4 modules are deterministic Python. Additionally, the `INTEGRATION_WIRING_DIMENSION` added to `build_spec_fidelity_prompt()` actually INCREASES the attention burden on the spec-fidelity LLM by adding a 6th comparison dimension.
- **Weakness**: The additional prompt dimension may *worsen* attention degradation in the spec-fidelity check by making the prompt longer and adding more comparison criteria.
- **Score: 5/5 for its own gate; 0/5 for the existing problem (may worsen it)**

**Variant C (Wiring v1.0)**:
- **Strength**: Deterministic analysis — immune for its own gate.
- **Weakness**: Does not address attention degradation in existing gates.
- **Score: 5/5 for its own gate; 1/5 for the existing problem**

### Root Cause 4: GOALPOST MOVEMENT
*No canonical list of "what constitutes HIGH" is enforced beyond the prompt's prose definition*

**Variant A (Wiring v2.0)**:
- **Strength**: Severity policy defined in code (§5.2.1): critical = "execution/dispatch/enforcement behavior depends on the seam"; major = "seam is dead but local fallback exists"; info = "whitelisted intentional optional". `blocking_for_mode()` is a pure function.
- **Weakness**: These definitions apply to WIRING findings, not to spec-fidelity severity. The spec-fidelity gate's "what constitutes HIGH" remains unanchored.
- **Score: 5/5 for its own gate; 1/5 for the existing problem**

**Variant B (Anti-Instincts)**:
- **Strength**: No severity gradient — binary pass/fail. Threshold is `0.7` for fingerprints, hardcoded. For obligations and contracts, it's zero-tolerance.
- **Weakness**: Does not define "what constitutes HIGH" for spec-fidelity deviations.
- **Score: 5/5 for its own gate; 1/5 for the existing problem**

**Variant C (Wiring v1.0)**:
- **Strength**: All-zero-tolerance (hardest possible goalpost, can't move).
- **Weakness**: The deviation count reconciliation companion does anchor one specific aspect — it verifies that the *count* of HIGH/MEDIUM/LOW in frontmatter matches body entries. This doesn't prevent goalpost movement on *what* is HIGH, but it catches *inconsistency* in the count.
- **Score: 5/5 for its own gate; 2/5 for the existing problem (partial anchor via deviation recon)**

### Root Cause 5: NO CONVERGENCE MECHANISM
*The gate has no memory of prior runs. Each fidelity check starts from zero context*

**Variant A (Wiring v2.0)**:
- **Strength**: `retry_limit=0` — convergence is not needed because the step never retries. The result is deterministic.
- **Weakness**: This design choice avoids convergence entirely rather than solving it. The spec-fidelity gate still has no memory of prior runs.
- **Score: 5/5 for its own gate (avoidance is a valid solution); 1/5 for the existing problem**

**Variant B (Anti-Instincts)**:
- **Strength**: Same — `retry_limit=0`, deterministic. No convergence needed.
- **Weakness**: Does not add memory or convergence to the spec-fidelity gate.
- **Score: 5/5 for its own gate; 1/5 for the existing problem**

**Variant C (Wiring v1.0)**:
- **Strength**: Sprint-focused; no pipeline retry.
- **Weakness**: Does not address convergence in the roadmap pipeline.
- **Score: 4/5 for its own gate; 1/5 for the existing problem**

---

## Round 2: Steelman Arguments and Cross-Variant Debate

### Key Debate Point: "Own gate" vs "existing fidelity gate" scoring

**Advocate for A**: "Variant A is the most comprehensive specification. It has the deepest substrate analysis, the most detailed gate definition, and the most nuanced mode-aware enforcement. Its `retry_limit=0` + deterministic design is the correct *architectural pattern* that should be applied to the spec-fidelity gate."

**Advocate for B**: "Variant B uniquely addresses the *generation-time* problem through prompt injection. It's the only spec that tries to prevent the root cause rather than just detecting it after the fact. The `INTEGRATION_ENUMERATION_BLOCK` and `INTEGRATION_WIRING_DIMENSION` directly improve the quality of LLM output, reducing the need for remediation loops."

**Advocate for C**: "Variant C's deviation count reconciliation is the ONLY feature that directly modifies the existing SPEC_FIDELITY_GATE. While A and B build new parallel gates, C actually touches the broken component. The deviation recon catches the specific failure mode where frontmatter severity counts don't match body entries — which is a direct manifestation of severity drift."

### Rebuttal

**Against A**: The advocate's claim that the pattern "should be applied" to spec-fidelity is aspirational, not in-spec. The spec does not modify spec-fidelity behavior.

**Against B**: The prompt injection may WORSEN attention degradation (#3) by adding a 6th dimension to an already-overloaded prompt. The steelman is correct about generation-time improvement, but the weak point is remediation-time — once the fidelity gate triggers, the prompt improvements don't prevent regeneration.

**Against C**: The deviation count reconciliation is the only direct touch on SPEC_FIDELITY_GATE, but it's a *consistency* check, not a *severity anchoring* mechanism. It catches "you said 3 HIGH but I count 2 in the body" — it doesn't prevent the LLM from deciding something IS HIGH when it was MEDIUM last run.

---

## Round 3: Convergence on Key Finding

**Consensus**: All three specs are architecturally excellent *for their own gates* — they all avoid the root causes by using deterministic Python instead of LLM evaluation. But **none of them fix the actual broken component** (the spec-fidelity gate's LLM-based severity assessment and remediation loop).

**Dissent**: Variant B's prompt-level improvements have indirect positive effect on generation quality, potentially reducing the frequency of fidelity gate failures. Variant C's deviation recon is a direct (if narrow) improvement to the fidelity gate.

---

## Scoring Matrix

| Diff Point | Category | Winner | Confidence | Evidence |
|------------|----------|--------|------------|----------|
| Own-gate severity anchoring | Gate design | Tie (A=B=C: all deterministic) | 95% | All use code-enforced pass/fail |
| Fidelity-gate severity drift fix | Root cause #1 | C (deviation recon) | 65% | Only spec touching SPEC_FIDELITY_GATE |
| Own-gate regeneration immunity | Gate design | A (most detailed) | 80% | retry_limit=0 + emit_report() docs |
| Fidelity-gate regeneration fix | Root cause #2 | B (prompt injection) | 55% | Generation-time improvement only |
| Own-gate attention immunity | Gate design | Tie (A=B=C) | 95% | All deterministic |
| Fidelity-gate attention fix | Root cause #3 | None (B worsens) | 90% | B adds 6th dimension to overloaded prompt |
| Own-gate goalpost anchoring | Gate design | A (most nuanced) | 75% | Mode-aware blocking with severity policy |
| Fidelity-gate goalpost fix | Root cause #4 | C (partial) | 60% | Deviation recon catches count mismatch |
| Own-gate convergence avoidance | Gate design | Tie (A=B) | 90% | Both use retry_limit=0 |
| Fidelity-gate convergence fix | Root cause #5 | None | 95% | No spec addresses this |
