# Diff Analysis: Calibration-Failure Theory Comparison

## Metadata
- Generated: 2026-05-26
- Variants compared: 3 (Agent A unmediated; Agent B sc:reflect-degraded; Agent C sc:troubleshoot)
- Substrate referenced by all: `pr86-integration-contracts-20260526100600`
- Categories: structural (4), content (5), contradictions (1), unique (4), shared assumptions (3)

## Structural Differences

| #     | Area                          | Variant 1 (A)                                                        | Variant 2 (B)                                                          | Variant 3 (C)                                                                                  | Severity |
|-------|-------------------------------|----------------------------------------------------------------------|------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|----------|
| S-001 | Channel evidence              | Implicit ("unmediated first-principles")                             | Explicit § "Reflection invocation evidence" w/ MCP failure disclosure  | Explicit § "Troubleshoot invocation evidence" w/ Wave-by-Wave landing summary                  | Low      |
| S-002 | Theory section format         | "Mechanism / Evidence / Per-theory confidence / Systemic fix"        | "Mechanism / Evidence / Per-theory confidence / Systemic fix"          | "Mechanism / Evidence / Per-theory confidence / Systemic fix"                                  | Low (convergent) |
| S-003 | Cross-theory synthesis        | "Cross-theory implications" (T1/T2 multiplicative, T3 upstream)      | No synthesis section                                                   | "Where the troubleshoot tiers landed" (HYBRID winner: C1 primary, C2 guardrail, C3 defense)    | Medium   |
| S-004 | Reflection-vs-direct table    | None                                                                 | Present (§3): explicit N/A row admitting channel preempted             | None                                                                                           | Medium   |

## Content Differences

| #     | Topic                              | Variant 1 (A)                                                                                                 | Variant 2 (B)                                                                                                  | Variant 3 (C)                                                                                          | Severity |
|-------|------------------------------------|---------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|----------|
| C-001 | Theory 1 framing (rubric math)     | "Arithmetic-Mean Dilution of the Only Honest Dimension"                                                       | "Arithmetic-mean dilution: rubric structurally cannot let one 0.5 dimension veto"                              | "Arithmetic-mean rubric is dimension-orthogonality blind"                                              | Low      |
| C-002 | Theory 2 framing (evidence anchor) | "'Evidence Grounding' Conflates Source-Citation with Runtime-Verification"                                    | "'Evidence grounding' is a code-static-citation rubric, blind to runtime-behavior claims"                      | (Subsumed under C1; C's T2 is a different topic — eval-suite coverage)                                  | Medium   |
| C-003 | Theory 3 (third mechanism)         | "Stripped-Context Independence Removes the Doubt Signal Without Removing the Confidence Signal"               | "Verdict-direction asymmetry: calibrator scores diagnostic confidence, not refutation cost-of-being-wrong"     | "Residual anchoring leak from card's self-report + narrative framing defeats prompt-level norms"        | High     |
| C-004 | Recommended fix (rubric math)      | "Veto-or-cap rule: any dim ≤0.5 caps composite at 0.75"                                                       | "Gated minimum: calibrated = min(evidence_grounding, mean(other_four))"                                        | "min(mean, evidence_grounding + 0.3) when runtime; OR cap ≤0.84 when evidence<1.0 AND runtime"          | Medium   |
| C-005 | Recommended fix (evidence dimension) | "Split into Source-citation accuracy + Runtime verification; runtime ≥0.5 required before source >0.5"     | "Add 6th rubric dimension 'Runtime check'; tier-gate REFUTE on runtime claims behind Runtime ≥0.5"             | (Different fix — pin tests in eval suite)                                                              | Medium   |

## Contradictions

| #     | Point of Conflict                                                                                          | Variant A Position                                                                                                                                 | Variant B Position                                                                                                                          | Variant C Position                                                                                                              | Impact |
|-------|------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------|--------|
| X-001 | What is the *third* mechanism (after arithmetic-mean + evidence-anchor blindness)?                          | Stripped-context independence (calibrator deprived of upstream doubt-trail; missing-doubt cannot be raised)                                        | Verdict-direction asymmetry (REFUTE has different cost-of-being-wrong than AFFIRM; rubric ignores direction)                                | Residual anchoring leak (calibrator sees self-report; norm-only anti-anchoring fails under single-dim ambiguity)                | Medium |

Note: X-001 is not strictly contradictory — the three are compatible orthogonal mechanisms. But each variant treats *its* mechanism as the canonical T3, so the merged output must pick a primary T3 or carry all three.

## Unique Contributions

| #     | Variant | Contribution                                                                                                                                                            | Value Assessment |
|-------|---------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------|
| U-001 | A       | Cross-theory implications section: explicit claim that T1+T2 compound *multiplicatively*; T3 is upstream feeder. Identifies "source-reading as complete epistemology" as common root. | High             |
| U-002 | B       | Honest channel-failure disclosure: sc:reflect's mandatory MCP tools were absent, so the channel's value-add cannot be assessed. Methodological transparency.                | High             |
| U-003 | B       | Verdict-direction asymmetry framing (T3-B): REFUTE-wrong closes investigation, AFFIRM-wrong gets caught by CI. New axis the other two variants don't surface.              | High             |
| U-004 | C       | Eval-suite silent-green hypothesis (T2-C): the "1.000 precision/recall" claim covers only *groundable* hypotheses; structurally-unverifiable predicates are untested.    | High             |

## Shared Assumptions

| #     | Assumption                                                                                                                                                          | Source Agreement                                                                                  | Impact                                                                                                                          | Status     |
|-------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|------------|
| A-001 | The pr86 substrate's `tier2-root-cause-analyst-calibration.md` arithmetic (0.5 + 4×1.0 = 0.90) is structurally identical to the H3 0.95 REFUTE mechanism.            | All three cite this calculation as the canonical fingerprint.                                     | If pr86 substrate is NOT structurally analogous to H3 (e.g., H3's evidence-grounding was 1.0 not 0.5), the entire merged thesis weakens. | UNSTATED   |
| A-002 | The calibrator's `tools: Read` restriction is the load-bearing mechanical limit — the calibrator *cannot* run a Bash spot-check even when needed.                   | A:§T2 "tools: Read"; B:§T2 line 51; C:§T1 "Bash structurally absent"                              | If a future calibrator variant gains Bash, T2-A/T2-B fixes (runtime-verification dimension) become partially redundant.         | STATED     |
| A-003 | The unweighted arithmetic mean is the *current* rubric formula and has no veto/floor clause anywhere else in the protocol.                                          | All three cite `escalation-rubric.md:19` verbatim.                                                | If there *is* a veto clause elsewhere in the rubric or protocol the variants missed, the primary fix is unnecessary.            | STATED     |

## Summary
- Total structural differences: 4 (1 Medium, 3 Low)
- Total content differences: 5 (1 High, 2 Medium, 2 Low)
- Total contradictions: 1 (Medium, non-strict — orthogonal alternatives)
- Total unique contributions: 4 (all High value)
- Total shared assumptions surfaced: 3 (1 UNSTATED promoted to A-001, 2 STATED)
- Highest-severity items: C-003 (third-theory divergence); A-001 (pr86↔H3 fidelity assumption)

**Convergence signal**: Theories 1 (arithmetic-mean dilution) and 2 (evidence-anchor blindness for runtime claims) appear in all three variants with near-identical mechanism descriptions and citations. The merge will treat these as ROBUST CONVERGED ROOT CAUSES. The third theory diverges across variants and the merge will carry all three as ORTHOGONAL CONTRIBUTING MECHANISMS rather than forcing a single winner.
