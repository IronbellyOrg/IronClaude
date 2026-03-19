---
stage: 6
stage_name: score
depth: quick
gate: SCORE_GATE
verdict: ADEQUATE
---

# Stage 6: score -- Adversarial Review

## Q1: Meaningful Output

The SCORE_GATE is STANDARD tier with two required frontmatter fields (`base_variant`, `variant_scores`) and a 20-line minimum. No semantic checks.

For the eval spec (FR-EVAL-001, progress reporting), the score stage selects the base variant for merging based on the debate transcript and diff analysis. With a MEDIUM-complexity spec and two seeded ambiguities, the two variants will have measurable differences in how they handle progress reporting architecture (callback mechanism, file format, deviation sub-entry schema, remediation trigger definition). The scoring criteria will reflect these differences, producing a non-trivial selection rationale.

**Assessment**: The gate will pass non-trivially, but it is the weakest gate among stages 4-6. The 20-line minimum is low -- even a minimal scoring table with 6 criteria meets this threshold. The `variant_scores` field has no format validation (no semantic check), so it could contain "A:80 B:70" or "A wins" or any arbitrary string. The `base_variant` field has no validation that it matches one of the actual variant labels. Both fields are checked only for presence, not correctness.

**Risk of trivial pass**: Moderate. A score artifact that writes `base_variant: A` and `variant_scores: "A:51 B:49"` with 20 lines of boilerplate would pass the gate without providing meaningful selection rationale. The lack of semantic checks means the gate cannot distinguish between a rigorous weighted-criteria analysis and a superficial pick-one-and-justify. However, the eval spec's progress reporting use case is simple enough that both variants will likely produce similar architectures, making the scoring genuinely close and the rationale more important than the selection itself.

## Q2: v3.0 Changes

The SCORE_GATE definition is unchanged in v3.0: `required_frontmatter_fields=["base_variant", "variant_scores"]`, `min_lines=20`, `enforcement_tier="STANDARD"`. No code changes to the score step logic.

**Indirect effects from upstream v3.0 changes**: None. The debate transcript feeding into the score stage is produced by an unchanged DEBATE_GATE. The score prompt builder (`build_score_prompt`) is unchanged.

**Indirect effects from downstream v3.0 changes**: The `base_variant` selection determines which roadmap variant becomes the merge base. The merged roadmap then enters the v3.0-specific stages (spec-fidelity, deviation-analysis, wiring-verification, remediate, certify). The choice of base variant can influence:

1. **Spec-fidelity findings**: If variant A handles FR-001.4's undefined schema more explicitly than variant B, selecting A as base may reduce the number of HIGH-severity findings in spec-fidelity. Conversely, selecting B might produce more findings, exercising the remediation path more thoroughly.
2. **Deviation count**: The base variant's treatment of seeded ambiguities determines how many deviations the convergence loop must resolve. A variant that acknowledges ambiguity produces fewer false-positive deviations than one that invents a resolution.

This indirect effect is important for eval design: the eval should not assume a specific base variant selection. Both outcomes (A or B as base) should produce valid downstream behavior, even if the specific findings differ.

## Q3: Artifact Verification

**Artifact produced**: `base-selection.md` -- a Markdown document with YAML frontmatter containing `base_variant` (string, typically "A" or "B") and `variant_scores` (string, typically formatted as "A:XX B:YY"), followed by scoring criteria, per-criterion assessments, overall scores, and a selection rationale.

**Third-party verification**:
1. **Structural**: Parse YAML frontmatter, confirm both required fields are present and non-empty. Count lines, confirm >= 20.
2. **Score consistency**: Parse `variant_scores` to extract numeric scores. Verify `base_variant` matches the variant with the higher total score. A selection of variant B when variant A scores higher (or vice versa) without explicit justification is a defect.
3. **Criteria traceability**: For each scoring criterion, verify it maps to at least one divergence point from the diff-analysis. Criteria that do not reference any divergence point are fabricated and reduce scoring validity.
4. **Debate integration**: Verify the scoring references debate concessions. If variant B conceded 4 points in the debate, the scoring should reflect B's weakness in those areas. A scoring that ignores debate outcomes is disconnected from the pipeline.
5. **Weight validation**: If scoring uses weighted criteria, verify weights sum to 100% and no single criterion dominates beyond reasonable bounds (e.g., a 60% weight on one criterion should be explicitly justified).

## Q4: Most Likely Failure Mode

**Disconnected scoring criteria**. The score stage receives both the diff-analysis and debate transcript as inputs. The most likely failure mode is that the LLM generates scoring criteria that are generic ("code quality," "documentation completeness," "test coverage") rather than derived from the specific divergence points identified in the diff. This produces a scoring artifact that reads well in isolation but does not actually reflect the differences between the two variants.

For the eval spec specifically: both variants will propose similar progress reporting architectures (the eval spec is MEDIUM complexity with straightforward requirements). The genuine differences will be in how they handle the seeded ambiguities and in implementation ordering details. Generic scoring criteria would miss these differences and produce arbitrary variant selection.

**Impact**: If the base variant is selected on generic criteria rather than the actual divergences, the merge step incorporates improvements from the "losing" variant based on debate concessions rather than on scoring-identified strengths. This is not catastrophic -- the merge prompt independently reads both variants and the debate -- but it means the scoring artifact adds less analytical value than intended. The downstream stages function correctly regardless of which variant is selected as base.

**Secondary failure mode**: The `variant_scores` field format is unconstrained. If the LLM writes `variant_scores: "Variant A is stronger overall"` (prose instead of numeric), the gate passes (the field is present and non-empty) but downstream tooling that expects parseable scores will fail silently. The eval spec's progress reporter would record this as a passed gate, masking the format issue.

## Q5: Eval Spec Coverage

**v3.0 changes to this stage**: None. The SCORE_GATE is unchanged.

**What the eval spec must exercise**: FR-EVAL-001.1 requires a `StepProgress` entry for the score step with the five core fields. Because SCORE_GATE is STANDARD tier with no semantic checks, the gate verdict is purely structural (frontmatter presence + line count). The progress entry will record a simple pass/fail.

**Does the eval spec account for this?** Yes, adequately. The eval spec's data flow diagram (Section 2.2) shows `[score] --> progress.json (step 6 entry)`. The `StepProgress` model covers the required fields. No special metadata is needed for the score step's progress entry because the gate produces no semantic check results to capture.

**Observation on eval sufficiency**: The score stage is the last of the three unchanged stages (4-6) before the pipeline enters v3.0-specific territory at stage 7 (merge, unchanged) and stage 9 (spec-fidelity, changed). The eval spec's coverage of stages 4-6 is essentially "write a progress entry with step_id, status, duration_ms, gate_verdict, output_file." This is appropriate -- these stages are not the eval's primary targets. The eval's value proposition is exercising the v3.0-specific downstream stages (spec-fidelity convergence, deviation-analysis, wiring-verification, remediate, certify). Stages 4-6 serve as realistic pipeline context that produces genuine artifacts for downstream consumption, which is exactly their role.

**Gap**: None blocking. The eval spec could optionally specify that the progress entry for the score step should include `base_variant` in the metadata dict, since this value is consumed by the merge step and would be useful for post-hoc pipeline analysis. But this is a nice-to-have, not a requirement for eval validity.

## Verdict

**ADEQUATE**. The score stage is unchanged in v3.0, the SCORE_GATE is the weakest of the three gates (stages 4-6) but will produce a non-trivial pass for this eval spec, and the eval spec's progress reporting requirements are well-specified. The SCORE_GATE's lack of semantic checks is a known limitation (no format validation on `variant_scores`, no consistency check between `base_variant` and scores), but this is an existing design decision, not an eval spec gap. The eval spec correctly treats stages 4-6 as pipeline infrastructure rather than primary evaluation targets, and its coverage is proportionate to their role.
